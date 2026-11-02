# Inspection Defect Logger

Inspection Defect Logger is a small Python notebook and calculator for factory inspection results. After checking the real items, enter a batch ID, sample size, and any critical, major, or minor defects. The command-line and browser versions both list defects and calculate the verdict using the same acceptance limits. Data is held in memory for one inspection and is cleared when the program exits. No dataset or real inspection items are included.

## Requirements and setup

Python 3.9 or newer. The project uses only the Python standard library; there are no packages to install.

From the repository directory, create and activate a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

## Command-line version

```sh
python inspection_logger.py
```

Enter a batch ID and a whole-number sample size of at least 1. At the prompt, use `record`, `list`, `verdict`, or `quit`. Each defect needs a severity (`critical`, `major`, or `minor`) and a short description. Invalid sample sizes are explained and rejected before an inspection starts.

## Browser version

```sh
python web_app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). The plain HTML page lets you start an inspection, record multiple defects, see the list, and see the current verdict. Successful submissions return to the main page, so refreshing does not submit the same entry again. Recorded defects cannot be edited or deleted. Stop the server with `Ctrl+C`; the in-memory inspection is then cleared.

## Run the tests

From the repository directory, with the virtual environment active:

```sh
python -m unittest discover -s tests -v
```

The 18 tests cover the verdict rules, sample-size boundaries, and HTTP form handling, including redirects, repeated page loads, input validation, HTML escaping, and protection against replacing an active inspection. The browser flow was also checked manually, including the verdict change from ACCEPT to REJECT and refresh behavior.

## Time spent

Approximately 6 hours elapsed across several sessions, including implementation, learning and reviewing the code, manual testing, documentation, and GitHub setup. This includes breaks and setup troubleshooting; active working time was not tracked separately.

## AI session

The Codex session record is in [`session-log.md`](session-log.md).
