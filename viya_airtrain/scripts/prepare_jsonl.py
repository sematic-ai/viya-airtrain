import argparse
import json
import pdb
from pathlib import Path

from viya_airtrain.data_transforms import raw_transcript_to_conversation_turns
from viya_airtrain.typed_dicts import FullRawTranscript


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "Transform from raw transcripts to data for Airtrain to use."
    )

    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--interactive", default=False, action="store_true")
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
    transcripts = []
    for json_path in path.glob("*.json"):
        with open(json_path, "r") as fp:
            transcripts.append(json.load(fp))  # type: ignore
    return transcripts


def main():
    args = parse_args()
    raw_transcripts = list_raw_transcripts(args.source_dir)
    turns = []
    for transcript in raw_transcripts:
        turns.extend(
            raw_transcript_to_conversation_turns(transcript, args.include_agents)
        )

    if args.interactive:
        pdb.set_trace()


if __name__ == "__main__":
    main()
