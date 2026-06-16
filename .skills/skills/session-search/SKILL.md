---
name: session-search
type: navigator
version: "1.0.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
description: >
  Search the narrative memory index (SQLite FTS5) for past sessions, decisions,
  learnings, snapshots, and events. Returns ranked results with source,
  date, brand, and a highlighted snippet. Use when the operator asks what was
  decided, discussed, or learned across sessions · instead of grepping markdown.
  FR: "qu'a-t-on dit sur", "retrouve", "cherche dans l'historique", "quelle décision
  sur", "session de février", "notre discussion sur X".
  EN: "what did we say about", "search history", "which decision", "past session".
permissions:
  reads: [index]
  writes: []
  mode: none
  subagent_safe: true
disambiguates_against:
  query-context: "route to query-context for CURRENT brand state (live JSON entities). Route to session-search for PAST narrative (sessions, decisions, history)."
---

## Tone

Return the hits as a short readable list, not raw JSON. Say how many, the top 3-5, with one-line snippet and source. If zero hits, say zero and suggest a looser query. Never hallucinate content outside the snippets returned.

---

# Skill: Session Search

Narrative retrieval across the workspace. The index is populated by `.skills/memory-index.py` which reads (when present): `session-log.md` (per-session chunks), `decisions.md` (per-decision rows), `brands/{slug}/learnings.json`, `brands/{slug}/_snapshot.md`, `brands/{slug}/session-state.md`, `.phantom/context-engine-events.jsonl`.

## Step 0 · Ensure index fresh

Run this ONE line before every query. It is idempotent and cheap: if the index is already up to date, it returns in milliseconds without rebuilding. If any source file has changed since the last build, it rebuilds automatically.

```bash
python3 .skills/ensure-memory-fresh.py --quiet
```

Do not do the mtime check yourself and do not call `memory-index.py` directly; the helper handles both paths.

## Step 1 · Parse operator intent

From the operator's question, extract:
- **query** · the search terms (concept, topic, keyword)
- **type filter** · if the operator says "decision" / "décision" / "session" / "learning" / "snapshot" / "event" → pass `--type`
- **brand filter** · if the operator mentions a specific brand slug → pass `--brand`
- **date filter** · if the operator says "since X" / "depuis X" / "en février" → pass `--since YYYY-MM-DD`

Preserve the operator's literal search terms. Do not rewrite "hero" into "héros" or vice versa; the index is case-insensitive.

## Step 2 · Run the query

```bash
python3 .skills/session-search.py \
  --query "{terms}" \
  [--type decision|session|learning|snapshot|event|session_state] \
  [--brand {slug}] \
  [--since {YYYY-MM-DD}] \
  [--limit 10]
```

Default limit is 10. Use a higher limit only if the operator asked for a broad sweep ("tout ce qu'on a dit sur…").

## Step 3 · Present results

For 1-5 hits, list each with source, date, and snippet. For more hits, show top 3 and say `+N more, refine with…`. If zero hits, propose one looser variant (drop a constraint) and ask the operator if they want to rerun.

Never copy the full chunk content unless explicitly asked · the snippet is the deliberate summary surface.

## Hard Rules

- **Never fabricate.** Only report what the index returned. If the snippet is truncated, do not fill the gap from training data or assumption.
- **Never write back.** This skill is read-only. Corrections to a decision go through `capture-learning` or a manual edit of the source file followed by reindex.
- **Always ensure freshness.** If the operator reports a hit is stale or missing, rebuild the index and retry before debating.
- **FTS5 syntax escape.** The script quotes the query automatically. Do not pre-escape or add your own `AND`/`OR` operators unless the operator explicitly requested boolean logic.
- **Respect the operator's language.** If they asked in French, present the results in French. If English, English. The index content is bilingual.
