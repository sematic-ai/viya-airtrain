from viya_airtrain.task_prompts import TASK_PROMPT_BY_AGENT_NAME
from viya_airtrain.typed_dicts import (
    ALL_DONE,
    AgentName,
    ConversationTurn,
    FullRawTranscript,
    RawMessage,
    SimpleTurn,
)


def raw_transcript_to_conversation_turns(
    full_transcript: FullRawTranscript, include_agents: list[AgentName]
) -> list[ConversationTurn]:
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
                    task_prompt=TASK_PROMPT_BY_AGENT_NAME[prior_agent_name],
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
                task_prompt=TASK_PROMPT_BY_AGENT_NAME[agent_name],
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
                task_prompt=TASK_PROMPT_BY_AGENT_NAME[agent_name],
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
    turns: list[SimpleTurn] = []
    for message in raw_messages:
        turns.append(SimpleTurn(role=message["role"], content=message["content"]))

    return turns


def _render_prior_turns(prior_turns: list[SimpleTurn]) -> str:
    def render_turn(turn: SimpleTurn):
        role_marker = "<|user|>" if turn["role"] == "user" else "<|assistant|>"
        return f"{role_marker}\n{turn['content']}"

    return "\n".join(render_turn(turn) for turn in prior_turns)
