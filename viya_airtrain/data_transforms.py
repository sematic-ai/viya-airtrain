import random
import re
from copy import deepcopy

from viya_airtrain.names import get_names
from viya_airtrain.task_prompts import get_task_prompt
from viya_airtrain.typed_dicts import (
    ALL_DONE,
    AgentName,
    ConversationTurn,
    FullRawTranscript,
    RawMessage,
    SimpleTranscript,
    SimpleTurn,
)


def raw_transcript_to_conversation_turns(
    full_transcript: FullRawTranscript, include_agents: list[AgentName]
) -> list[ConversationTurn]:
    """Convert from chat transcripts to a row-per-turn.

    Parameters
    ----------
    full_transcript:
        A single transcript of a full conversation between Viya and a user.
    include_agents:
        Only agents with names in this list will have their conversation turns
        included in the output.

    Returns
    -------
    A list of individual turns from the conversation, filtered to only include
    ones for the specified agents. ALL_DONE rows which are implicit in the source
    data will also be included.
    """
    turns: list[ConversationTurn] = []
    sim_context = full_transcript["sim_context"]
    patient_profile = sim_context["patient_profile"]
    simple_turns = messages_as_simple_turns(full_transcript["messages"])

    agent_name: None | AgentName = None
    for i, message in enumerate(full_transcript["messages"]):
        role = message["role"]
        if role == "user":
            continue

        rendered_prior_turns = _render_prior_turns(simple_turns[:i])

        prior_agent_name = agent_name
        agent_name = message["agent_name"]

        base_kwargs = dict(
            session_id=full_transcript["session_id"],
            message_index=i,
            role=role,
            prior_turns=simple_turns[:i],
            rendered_prior_turns=rendered_prior_turns,
            chief_complaint=patient_profile["chief_complaint"],
            patient_age_in_years=patient_profile["age_in_years"],
            patient_first_name=patient_profile["first_name"],
            patient_last_name=patient_profile["last_name"],
            patient_gender=patient_profile["gender"],
        )

        if prior_agent_name in include_agents and prior_agent_name != agent_name:
            # Show the hidden ALL_DONE from the agent saying the next agent
            # can take over.
            turns.append(
                ConversationTurn(
                    is_hidden=True,
                    agent_name=prior_agent_name,
                    content=ALL_DONE,
                    task_prompt=get_task_prompt(prior_agent_name),
                    **base_kwargs,  # type: ignore
                )
            )

        if agent_name not in include_agents:
            continue

        turns.append(
            ConversationTurn(
                is_hidden=False,
                agent_name=agent_name,
                content=message["content"],
                task_prompt=get_task_prompt(agent_name),
                **base_kwargs,  # type: ignore
            )
        )

    if agent_name in include_agents:
        # If the final active agent was one of the included ones,
        # show its hidden message that says it's done.
        i = len(full_transcript["messages"])
        rendered_prior_turns = _render_prior_turns(simple_turns[:i])
        turns.append(
            ConversationTurn(
                is_hidden=True,
                agent_name=agent_name,
                content=ALL_DONE,
                task_prompt=get_task_prompt(agent_name),
                session_id=full_transcript["session_id"],
                message_index=i,
                role=role,
                prior_turns=simple_turns[:i],
                rendered_prior_turns=rendered_prior_turns,
                chief_complaint=patient_profile["chief_complaint"],
                patient_age_in_years=patient_profile["age_in_years"],
                patient_first_name=patient_profile["first_name"],
                patient_last_name=patient_profile["last_name"],
                patient_gender=patient_profile["gender"],
            )
        )
    return turns


def messages_as_simple_turns(raw_messages: list[RawMessage]) -> list[SimpleTurn]:
    """Shorten raw messages into a more simple format with only role & content."""
    turns: list[SimpleTurn] = []
    for message in raw_messages:
        turns.append(SimpleTurn(role=message["role"], content=message["content"]))

    return turns


def replace_name_in_transcript(
    transcript: FullRawTranscript, first_name: str, last_name: str
) -> FullRawTranscript:
    """Replace the name of the patient in the source transcript with the specified one"""
    new_transcript = deepcopy(transcript)
    old_first_name = new_transcript["sim_context"]["patient_profile"]["first_name"]
    old_last_name = new_transcript["sim_context"]["patient_profile"]["last_name"]
    new_transcript["sim_context"]["patient_profile"]["first_name"] = first_name
    new_transcript["sim_context"]["patient_profile"]["last_name"] = last_name

    for message in new_transcript["messages"]:
        message["content"] = message["content"].replace(old_first_name, first_name)
        message["content"] = message["content"].replace(old_last_name, last_name)

    return new_transcript


def replace_names_in_transcripts(
    transcripts: list[FullRawTranscript],
) -> list[FullRawTranscript]:
    """Replace all the patient names in transcripts with randomly generated ones."""
    return [
        replace_name_in_transcript(transcript, name[0], name[1])
        for transcript, name in zip(transcripts, get_names())
    ]


def _render_prior_turns(prior_turns: list[SimpleTurn]) -> str:
    """Render prior turns from the conversation into a single string."""

    def render_turn(turn: SimpleTurn):
        role_marker = "Patient" if turn["role"] == "user" else "Viya"
        return f"{role_marker}: {turn['content']}"

    return "\n".join(render_turn(turn) for turn in prior_turns)


def to_simple_transcript(
    transcript: FullRawTranscript,
    selected_agent: AgentName,
    system_prompt_template: str,
) -> SimpleTranscript:
    """Extract the conversation to a simple transcript ending with the specified agent.

    A system prompt will be rendered including patient information and the task prompt
    for the agent.
    """
    simple_turns: list[SimpleTurn] = []
    session_id = transcript["session_id"]
    found_agent = False
    for message in transcript["messages"]:
        if found_agent and message["role"] == "user":
            simple_turns.append(
                SimpleTurn(role=message["role"], content=message["content"])
            )
            simple_turns.append(SimpleTurn(role="assistant", content="ALL_DONE"))
            break

        simple_turns.append(SimpleTurn(role=message["role"], content=message["content"]))

        if message["agent_name"] == selected_agent:
            found_agent = True

    if not found_agent:
        raise ValueError(
            f"Session {session_id} has no inclusion of agent {selected_agent}"
        )

    task_prompt = get_task_prompt(selected_agent)
    system_prompt = render_system_prompt(system_prompt_template, transcript, task_prompt)
    simple_turns.insert(0, SimpleTurn(role="system", content=system_prompt))

    return SimpleTranscript(
        session_id=session_id,
        messages=simple_turns,
        patient_first_name=transcript["sim_context"]["patient_profile"]["first_name"],
        patient_last_name=transcript["sim_context"]["patient_profile"]["last_name"],
        patient_gender=transcript["sim_context"]["patient_profile"]["gender"],
        patient_age_in_years=transcript["sim_context"]["patient_profile"]["age_in_years"],
        task_prompt=task_prompt,
    )


def render_system_prompt(
    system_prompt_template: str, transcript: FullRawTranscript, task_prompt: str
):
    context = dict(
        patient_first_name=transcript["sim_context"]["patient_profile"]["first_name"],
        patient_last_name=transcript["sim_context"]["patient_profile"]["last_name"],
        patient_gender=transcript["sim_context"]["patient_profile"]["gender"],
        patient_age_in_years=transcript["sim_context"]["patient_profile"]["age_in_years"],
        task_prompt=task_prompt,
    )
    prompt = system_prompt_template
    for key, value in context.items():
        pattern = r"\{\{\s*" + key + r"\s*\}\}"
        prompt = re.sub(pattern=pattern, repl=value, string=prompt)

    return prompt


def randomly_select_agent(
    agent_names: list[AgentName], transcript: FullRawTranscript
) -> AgentName:
    "Choose an agent name for an agent appearing in the conversation"
    appearing_agents = set()
    session_id = transcript["session_id"]
    for message in transcript["messages"]:
        appearing_agents.add(message["agent_name"])
    choices = appearing_agents.intersection(agent_names)
    if len(choices) == 0:
        raise ValueError(
            f"Transcript {session_id} contains none of: {', '.join(agent_names)}"
        )
    return random.choice(list(choices))
