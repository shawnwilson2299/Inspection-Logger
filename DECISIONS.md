# Decisions

## Where the AI got it wrong

The AI-generated browser handler in commit `e1a58ea` accepted another `/start` request even when an inspection was active. Submitting the old start form again could overwrite the inspection and lose its defects. This conflicted with preserving recorded defects. I requested a final audit; the AI found the bug during that review, rather than me independently discovering it.

The actual assistant response was: “I found one actual browser issue: resubmitting the old “Start inspection” form could replace the current inspection and lose its defects.” For the original punctuation and complete exchange, see [transcript-excerpts.md, record 1319](transcript-excerpts.md#record-1319--assistant--2026-11-02t185057379z), preceded by my audit request at record 1287. Commit `ae01687` added a guard that returns HTTP 409 and preserves the inspection, plus `test_repeat_start_does_not_erase_existing_inspection`. The final audit reran that regression test successfully. The earlier incorrect commit-count note remains documented in `session-log.md`; no verdict-rule error is being claimed.

## What I chose not to build, and why

I kept the app to one in-memory inspection per run. I initially chose a CLI, then added a plain HTML browser interface after the user requested one. The browser version uses Python's standard-library HTTP server and the same `Inspection` and verdict logic; it has no CSS, JavaScript, accounts, database, or JSON persistence. Successful form submissions redirect to the main page so refreshing does not repeat the POST. Defects cannot be edited or deleted, and no reset control was added, consistent with the brief's limits.

## What was ambiguous

The brief allows memory or JSON storage but does not specify whether one program run should handle one inspection or multiple batches. I assumed one inspection per run to keep the CLI small. It also does not prescribe exact wording for invalid input, so the app prints an explanation and asks for a valid sample size again before it starts the inspection.

## Three things the tests do not cover

1. The automated HTTP tests do not drive a real browser or check browser-specific form validation and keyboard accessibility. The browser flow was checked manually; see `session-log.md`.
2. Entries disappear on exit by design, so there is no recovery after the program closes unexpectedly.
3. There is no practical upper bound for a positive sample size; very large values use the highest table row, as specified by the row-selection rule, but that behavior is only tested at 900.
