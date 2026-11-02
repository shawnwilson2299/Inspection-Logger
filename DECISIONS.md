# Decisions

## Where the AI got it wrong

The AI made a bookkeeping mistake in its handoff note. In `session-log.md`, under “GitHub publication status,” the original sentence was: “The local `main` branch has six meaningful commits and a clean worktree.” During final review, comparing that statement with `git log --oneline` showed seven commits: the note was written before, and then included in, an additional commit. I corrected the session log to explain the timing and the final count. The verdict rules were separately checked against the brief examples and boundary tests.

## What I chose not to build, and why

I kept the app to one in-memory inspection per run. I did not add accounts, a database, JSON persistence, editing or deleting defects, a web interface, deployment, or a dataset, because those are excluded or unnecessary in the brief.

## What was ambiguous

The brief allows memory or JSON storage but does not specify whether one program run should handle one inspection or multiple batches. I assumed one inspection per run to keep the CLI small. It also does not prescribe exact wording for invalid input, so the app prints an explanation and asks for a valid sample size again before it starts the inspection.

## Three things the tests do not cover

1. The CLI prompt sequence and printed messages are not tested end to end; the tests focus on the rule functions and inspection object.
2. Entries disappear on exit by design, so there is no recovery after the program closes unexpectedly.
3. There is no practical upper bound for a positive sample size; very large values use the highest table row, as specified by the row-selection rule, but that behavior is only tested at 900.
