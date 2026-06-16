# tickets/

Lightweight async tickets for long-running deliverables. One file per ticket, markdown, append-only.

## When to open a ticket

A skill **MUST** open a ticket when :

- Execution will take > 10 minutes of wall-clock time
- The deliverable spans multiple sessions (operator might walk away and come back)
- Multiple sub-skills are orchestrated (any Orchestrator)
- The output is a client-facing deliverable (audit report, weekly report, brief)
- The operator explicitly says "this might take a while, log progress"

Skills that should NOT open a ticket : pure Curators (query, validate), Navigators (brief-day, resume-session), quick Producers (3 hooks, short brief). Use cases where the operator expects answer within 1-2 minutes.

## File naming

`{YYYY-MM-DD}-{HHMM}-{ticket-slug}.md`

Example: `2026-04-19-1430-klaviyo-audit.md`

## Format (template)

```markdown
# Ticket: {concise intent, operator language}

**Opened**: YYYY-MM-DD HH:MM
**Owner skill**: {skill-name}
**Status**: running | paused | done | cancelled | blocked
**Last update**: YYYY-MM-DD HH:MM

## Intent
{What the operator asked for, reformulated in operator language}

## Plan
1. {Step 1 · what it does, not which skill calls it}
2. {Step 2}
3. ...

## Current state
{Where we are right now, 1-2 lines}

## Log
- YYYY-MM-DD HH:MM · {event, 1 line}
- YYYY-MM-DD HH:MM · {event}

## Cost estimate
- Tokens: ~{N}
- Wall-clock: ~{minutes}
- External calls: {N API calls, which platform}

## Blockers
{list if any, otherwise "none"}

## Output
{link to the deliverable when done, or "pending"}
```

## Operator interaction

- `"where is ticket {id}"` → read the ticket, show current state + log tail
- `"pause ticket {id}"` → set status to `paused`, log timestamp
- `"resume ticket {id}"` → set status to `running`, continue where stopped
- `"close ticket {id}"` → set status to `done`, archive under `tickets/_done/` if > 30 days old

## Rule

The ticket is the **authoritative state** for long-running work. If the skill crashes, the ticket is read on resume to rebuild context. **NEVER** duplicate ticket state in session-state.md or other files.
