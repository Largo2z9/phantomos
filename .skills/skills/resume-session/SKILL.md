---
name: resume-session
type: navigator
version: "1.0.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
description: >
  Clean resumption after absence. Reads last session state, pending work, open threads.
  Produces a recap of where we stopped + what's still in flight + one clear next action.
  Distinct from brief-day: resume-session is continuity-oriented (what was happening),
  brief-day is portfolio-overview oriented (what's the state).
  FR: "resume", "reprends", "je reviens", "on en était où", "continue".
  EN: "resume", "pick up", "where were we", "continue".
permissions:
  reads: [brand, product, offer, profile, learning, strategy]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: at least one active brand with session-state.md or recent activity
  postconditions: none, read-only
---

# Skill: resume-session

**CRITICAL:** this is a Navigator for continuity. **NEVER** restart from scratch. **ALWAYS** reconstruct the last active thread and surface it precisely.

## Tone

Project lead back from vacation, caught up by their senior. Direct, 5-7 bullets max, zero unnecessary context, zero "let me summarize the whole project".

Posture adapted to the **register of the last session** (detected from session-state.md content): strategic → CTO recap, operational → project lead recap, creative → CD recap, debug → senior engineer recap, audit → auditor recap.

---

## Step 1 · Locate the thread (silent)

Find the active context in this priority order:

1. **`session-state.md` at root** (if present): last 20 lines of Activity Log, Active Decisions section, Open Threads if any
2. **`brands/*/session-state.md`** for brands touched in the last 7 days
3. **`brands/*/pending-validations.md`** unchecked items to identify what was in flight
4. **`brands/*/todos.md`** `## In Progress` sections across brands

Build a mental map: **last brand active, last skill executed, last decision made, next step that was queued but not executed**.

## Step 2 · Classify the thread (silent)

Label the thread by one of:

- **Mid-deliverable** · a skill was running or produced output, not validated / persisted yet
- **Mid-setup** · setup-brand was in progress, Step N incomplete
- **Mid-validation** · inferred fields posted, waiting for operator review
- **Mid-learning** · batch learning flush was shown, not yet confirmed
- **Idle** · session closed cleanly, no thread pending

If **multiple threads open across brands**, pick the most recent. Surface others as "aside" mentions, not in the main recap.

## Step 3 · Deliver the resume

**Template** (adapt to detected register):

> **Where we stopped**
> - Last active: Northsense, ~2 days ago
> - Thread: running the Meta audit. We hit the access gate, I proposed token vs declarative mode. You didn't pick yet.
>
> **What's still in flight**
> - 1 audit paused (above)
> - Northsense inferred audience (Maghrebi/ME women) still marked "to review" in pending-validations
>
> **Aside (other brands)**
> - {brand B} had a snapshot-brand queued but was waiting for URL confirmation. No change since.
>
> **Next action**
> - Pick API vs declarative for Northsense Meta audit. 30 seconds. Then we're back in flight.

**ALWAYS** close with `AskUserQuestion` tool: *"Resume Northsense Meta audit (pick access mode) / Switch brand / Show me what I missed last 7 days across all brands / Other"*.

---

## Step 4 · What this skill NEVER does

- **NEVER** re-ask for context that's in session-state or learnings. Reconstruct silently, surface only the decision point.
- **NEVER** produce a full history log. 5-7 bullets, focus on the thread and the next action.
- **NEVER** auto-resume by running the queued skill. Confirm with operator first (they may want to change course).
- **NEVER** conflate resume-session with brief-day. If operator wants portfolio state → redirect to brief-day.

## Edge cases

- **No session-state.md anywhere, no recent brand activity** → "No active thread found. Want a portfolio brief instead? (brief-day)"
- **Session-state.md exists but all threads are idle / closed** → "Nothing mid-flight. Last action: {X, date}. Want to start something new?"
- **Multiple brands with equally recent activity** → ask: *"You have 2 threads warm. {brand A}: {thread}. {brand B}: {thread}. Which do we resume?"*
- **Thread is stale (> 14 days)** → flag: "This thread has cooled. Context may have shifted. Confirm or restart?"
