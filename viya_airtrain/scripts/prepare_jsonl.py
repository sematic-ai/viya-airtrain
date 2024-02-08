import argparse
import json
import pdb
import random
from pathlib import Path

from viya_airtrain.data_transforms import (
    raw_transcript_to_conversation_turns,
    replace_names_in_transcripts,
)
from viya_airtrain.typed_dicts import AgentName, ConversationTurn, FullRawTranscript


SEED = 42
TEST_FRACTION = 0.10


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
        "--agent",
        dest="include_agents",
        action="append",
        default=[],
        type=str,
        help=("The id of an agent to include in the tuning."),
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


def write_turns(path: Path, turns: list[ConversationTurn]) -> None:
    """Write individual conversation turns as rows in given jsonl file."""
    with open(path, "w+") as fp:
        for turn in turns:
            fp.write(f"{json.dumps(turn)}\n")


def split_transcripts(
    transcripts: list[FullRawTranscript],
) -> tuple[list[FullRawTranscript], list[FullRawTranscript]]:
    """Split transcripts such that some are used for test and some for train."""
    random.seed(SEED)

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


def process_split(
    output_path: Path,
    include_agents: list[AgentName],
    transcripts: list[FullRawTranscript],
    interactive: bool,
):
    """Given full transcripts, preprocess them and write to a jsonl file on disk."""
    turns = []
    for transcript in transcripts:
        turns.extend(raw_transcript_to_conversation_turns(transcript, include_agents))

    random.seed(SEED)
    random.shuffle(turns)
    write_turns(output_path, turns)

    if interactive:
        pdb.set_trace()


def main():
    args = parse_args()
    all_raw_transcripts = list_raw_transcripts(args.source_dir)
    all_raw_transcripts = replace_names_in_transcripts(all_raw_transcripts)

    train_transcripts, test_transcripts = split_transcripts(all_raw_transcripts)

    process_split(
        output_path=args.destination,
        include_agents=args.include_agents,
        transcripts=train_transcripts,
        interactive=args.interactive,
    )
    process_split(
        output_path=args.test_destination,
        include_agents=args.include_agents,
        transcripts=test_transcripts,
        interactive=args.interactive,
    )


if __name__ == "__main__":
    main()
