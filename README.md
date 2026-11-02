# Inspection Defect Logger

A small command-line notebook and calculator for inspection results. The inspector checks real items, then enters one batch ID, sample size, and any critical, major, or minor defects found; the program lists the recorded defects and recalculates an ACCEPT or REJECT verdict. Entries are held in memory for one run and disappear when the program exits. No items or external dataset are included.

## Requirements

Python 3.9 or newer. The app and tests use only the Python standard library; there are no packages to download.

## Install / set up

From the repository directory:

```sh
python3 -m venv .venv
```

Activate the environment:

```sh
source .venv/bin/activate
```

## Run

```sh
python inspection_logger.py
```

Enter a batch ID and a whole-number sample size of at least 1. At the prompt, use `record`, `list`, `verdict`, or `quit`. Each defect needs a severity (`critical`, `major`, or `minor`) and a short description. If a sample size is invalid, the program explains the problem and asks again before starting the inspection.

## Run the tests

```sh
python -m unittest discover -s tests -v
```

## Time spent

About 15 minutes, including implementation, the automated tests, and submission notes.

## AI session

The Codex session record is in [`session-log.md`](session-log.md).
