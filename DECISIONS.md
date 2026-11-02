# Decisions

## Where the AI got it wrong

No specific AI error was found during this session. The verdict implementation was checked against the six examples in the brief and additional table-boundary tests; all passed. I have not invented a mistake or an exchange. The session record is in `session-log.md`.

## What I chose not to build, and why

I kept the app to one in-memory inspection per run. I did not add accounts, a database, JSON persistence, editing or deleting defects, a web interface, deployment, or a dataset, because those are excluded or unnecessary in the brief.

## What was ambiguous

The brief allows memory or JSON storage but does not specify whether one program run should handle one inspection or multiple batches. I assumed one inspection per run to keep the CLI small. It also does not prescribe exact wording for invalid input, so the app prints an explanation and asks for a valid sample size again before it starts the inspection.

## Three things the tests do not cover

1. The CLI prompt sequence and printed messages are not tested end to end; the tests focus on the rule functions and inspection object.
2. Entries disappear on exit by design, so there is no recovery after the program closes unexpectedly.
3. There is no practical upper bound for a positive sample size; very large values use the highest table row, as specified by the row-selection rule, but that behavior is only tested at 900.
