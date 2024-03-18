import argparse
import json
import pdb
import random
from enum import Enum
from pathlib import Path

from viya_airtrain.core_prompt_paraphrasing import randomized_core_prompt_templates
from viya_airtrain.data_transforms import (
    get_appearing_agents,
    multiplex_agent_transcript,
    randomly_select_agent,
    raw_transcript_to_conversation_turns,
    replace_names_in_transcripts,
    to_agent_transcript,
)
from viya_airtrain.typed_dicts import (
    AgentName,
    AgentTranscript,
    ConversationTurn,
    FullRawTranscript,
)


SEED = 42
TEST_FRACTION = 0.10


class OutputMode(Enum):
    turn = "turn"
    conversation = "conversation"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "Transform from raw transcripts to data for Airtrain to use."
    )

    parser.add_argument(
        "--source-dir",
        type=Path,
        required=True,
        help="A directory containing .json files with full transcripts",
    )
    parser.add_argument(
        "--destination",
        type=Path,
        required=True,
        help="Path for jsonl file where the training data will be put.",
    )
    parser.add_argument(
        "--test-destination",
        type=Path,
        required=True,
        help="Path for jsonl file where test data will be put.",
    )
    parser.add_argument(
        "--interactive",
        default=False,
        action="store_true",
        help="Advanced: open a pdb session while writing data.",
    )
    parser.add_argument(
        "--isolate-agents",
        default=False,
        action="store_true",
        help="Only include one agent at a time in resulting conversations.",
    )
    parser.add_argument(
        "--agent",
        dest="include_agents",
        action="append",
        default=[],
        type=str,
        help=("The id of an agent to include in the tuning."),
    )
    parser.add_argument(
        "--output-mode",
        default=OutputMode.turn,
        type=OutputMode,
        choices=list(OutputMode),
        help=(
            "Whether the output jsonl should have "
            "one row per conversation or one per turn."
        ),
    )

    args = parser.parse_args()
    return args


def list_raw_transcripts(path: Path) -> list[FullRawTranscript]:
    """Read raw transcripts from .json files in given directory"""
    transcripts = []
    for json_path in path.glob("*.json"):
        with open(json_path, "r") as fp:
            transcripts.append(json.load(fp))  # type: ignore
    return transcripts


def write_jsonls(
    path: Path, rows: list[ConversationTurn] | list[AgentTranscript]
) -> None:
    """Write output rows in given jsonl file."""
    with open(path, "w+") as fp:
        for row in rows:
            fp.write(f"{json.dumps(row)}\n")


def split_transcripts(
    transcripts: list[FullRawTranscript],
) -> tuple[list[FullRawTranscript], list[FullRawTranscript]]:
    """Split transcripts such that some are used for test and some for train."""
    n_test_samples = int(TEST_FRACTION * len(transcripts))
    n_test_samples = max(n_test_samples, 1)
    test_transcripts = random.sample(transcripts, n_test_samples)

    test_transcript_session_ids = {
        transcript["session_id"] for transcript in test_transcripts
    }

    train_transcripts = list(
        filter(
            lambda trans: trans["session_id"] not in test_transcript_session_ids,
            transcripts,
        )
    )

    return train_transcripts, test_transcripts


def process_split_turn_mode(
    output_path: Path,
    include_agents: list[AgentName],
    transcripts: list[FullRawTranscript],
    interactive: bool,
):
    """Given full transcripts, preprocess them and write to a jsonl file on disk."""
    turns = []
    for transcript in transcripts:
        turns.extend(raw_transcript_to_conversation_turns(transcript, include_agents))

    random.shuffle(turns)
    write_jsonls(output_path, turns)

    if interactive:
        pdb.set_trace()


def process_split_conversation_mode(
    output_path: Path,
    is_train: bool,
    isolate_agents: bool,
    include_agents: list[AgentName],
    transcripts: list[FullRawTranscript],
    interactive: bool,
):
    """Given full transcripts, preprocess them and write to a jsonl file on disk."""
    agent_transcripts: list[AgentTranscript] = []
    for transcript, system_prompt_template in zip(
        transcripts, randomized_core_prompt_templates()
    ):
        if isolate_agents:
            # If agents are isolated, having an output transcript for each
            # doesn't repeat any data.
            selected_agents = list(
                set(include_agents).intersection(get_appearing_agents(transcript))
            )
        else:
            # If agents are NOT isolated, having an output transcript for
            # each would repeat data: later agents would include conversation
            # turns that were also present with earlier agents. So limit
            # to selecting one agent per conversation.
            selected_agents = [randomly_select_agent(include_agents, transcript)]

        for agent in selected_agents:
            agent_transcript = to_agent_transcript(
                transcript=transcript,
                isolate_agent=isolate_agents,
                selected_agent=agent,
                system_prompt_template=system_prompt_template,
                use_fixed_task_prompts=not is_train,
            )
            if is_train:
                agent_transcripts.append(agent_transcript)
            else:
                agent_transcripts.extend(multiplex_agent_transcript(agent_transcript))

    write_jsonls(output_path, agent_transcripts)

    if interactive:
        pdb.set_trace()


def main():
    random.seed(SEED)
    args = parse_args()
    all_raw_transcripts = list_raw_transcripts(args.source_dir)
    all_raw_transcripts = replace_names_in_transcripts(all_raw_transcripts)

    train_transcripts, test_transcripts = split_transcripts(all_raw_transcripts)

    print(f"Output mode: {args.output_mode.value}")
    if args.output_mode == OutputMode.conversation:
        process_split_conversation_mode(
            output_path=args.destination,
            is_train=True,
            isolate_agents=args.isolate_agents,
            include_agents=args.include_agents,
            transcripts=train_transcripts,
            interactive=args.interactive,
        )
        process_split_conversation_mode(
            output_path=args.test_destination,
            is_train=False,
            isolate_agents=args.isolate_agents,
            include_agents=args.include_agents,
            transcripts=test_transcripts,
            interactive=args.interactive,
        )
    else:
        process_split_turn_mode(
            output_path=args.destination,
            include_agents=args.include_agents,
            transcripts=train_transcripts,
            interactive=args.interactive,
        )
        process_split_turn_mode(
            output_path=args.test_destination,
            include_agents=args.include_agents,
            transcripts=test_transcripts,
            interactive=args.interactive,
        )


if __name__ == "__main__":
    main()
