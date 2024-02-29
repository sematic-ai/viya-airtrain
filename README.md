# Viya/Airtrain

This repo contains some code for pre-processing ViyaMD data for purposes
of usage with Airtrain. It's primary purpose is to start from a directory
containing json files with synthetic chats and convert them to jsonl
files ready for training and tuning in Airtrain.

## Setup

- Make sure you have python3.10 installed
- Change your working directory to the root of this repo
- `make prep  # will prepare a python virtial env in .venv within the repo`

## Basic Usage

- Every time you want to work in the repo: `source .venv/bin/activate`
- To automatically format and address simple lint errors: `make fix`
- To check formatting, linting, and type-checks: `make lint`
- To add a new dependency, edit `requirements.in` then `make refresh-dependencies`
which will update `requirements.txt`
- To sync with the contents of `requirements.txt`: `make sync`

## Converting Data

Make sure you have a directory filled with json files, each of which
contains a full simulated session between the user and Viya.

To see script usage:
```
python3 viya_airtrain/scripts/prepare_jsonl.py --help
```

Example:

```
python3 viya_airtrain/scripts/prepare_jsonl.py \
    --source-dir ~/datasets/viya1/all/ \
    --destination ~/datasets/viya1/jsonls/train-history.jsonl \
    --output-mode turn \
    --test-destination ~/datasets/viya1/jsonls/test-history.jsonl \
    --agent MedicalHistoryAgent \
    --agent FamilyHistoryAgent \
    --agent SocialHistoryAgent
```
