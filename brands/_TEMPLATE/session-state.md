# Session State · {brand-name}

> Rolling activity log. Auto-maintained by skills on every write operation.
> Max 30 lines. Oldest entries drop when limit exceeded.
> Read at session start to recover context. No manual "persist" needed.

## Activity Log

{Entries auto-appended by skills. Format: [YYYY-MM-DD HH:mm] {skill}: {1-line summary} → {files changed}}

## Open Threads

{Persistent until resolved. Added by learn-from-session or manually. Removed when resolved.}

## Active Decisions

{Key decisions from recent sessions. Migrated from activity log by learn-from-session.}

## Task In Progress

{Auto-maintained by skills during multi-step tasks. Cleared on completion or explicit cancel.
Format: skill | step_current/step_total | what was done | what remains}

Example:
[snapshot-brand] 3/7 · spec.json generated ✅, offers.json generated ✅ | Remaining: Q1-Q4 audience + profile.json
