# Pattern Detection · Observable Signals

> The agent watches the conversation flow for recurring signals it should later turn into structured knowledge. This is the daemon-level pattern detection that complements `learn-from-session` (which fires at explicit triggers, batch mode).

---

## Why this exists

`learn-from-session` is reactive : it processes a session in batch when triggered. It catches *what was said*, but it does not catch *what kept happening* unless the operator explicitly flags it.

The pattern detection daemon fills that gap. It runs implicitly every turn, watches for a small set of structured signals, buffers them silently, and surfaces or batches them when threshold is hit. The operator never sees the buffer ; they see the synthesis once a pattern is confirmed.

This is what turns a series of micro-frictions into a learning, a series of cross-brand observations into a shareable canon candidate, a series of micro-violations into a `correct-skill` [backlog, not shipped] ticket, without requiring the operator to remember and flag each one manually.

---

## Signals the agent watches every turn

### Friction signals (operator → agent loop)

| Signal | Trigger | Buffer entry |
|---|---|---|
| **Suggestion mismatch** | The agent proposes X, operator agrees, then within 1-2 turns reverses or rephrases. The applied output did not match what the operator actually meant. | `{type: suggestion_mismatch, what_was_proposed, what_operator_corrected, gap}` |
| **Repeat correction** | The operator corrects the same kind of output 2+ times in the session (tone too marketing, wrong audience, jargon leak). | `{type: repeat_correction, correction_pattern, occurrences}` |
| **Re-explanation** | Operator re-explains brand context that should already be encoded, the agent failed to surface or load it. | `{type: re_explanation_needed, context_missing}` |
| **Format pushback** | Operator rejects the format (too long, too many bullets, too academic, too direct response). | `{type: format_pushback, target_register}` |
| **Tunnel vision (canon-bound refusal)** | Agent answers a knowledge question with *"not in the workspace canon"* or hesitates because the encoded resources don't cover the domain. Operator follows up asking the agent to *"just look it up"* or volunteers the missing reference themselves. The agent stayed inside the canon when external fetch was the right move. | `{type: tunnel_vision, question_kind, canon_silent_on, external_source_needed}` |

### Cross-brand opportunity signals

| Signal | Trigger | Buffer entry |
|---|---|---|
| **Pattern transfer candidate** | Operator describes a problem on Brand A ; the agent recalls Brand B in the workspace solved a structurally similar problem. | `{type: cross_brand_transfer, source_brand, target_brand, pattern}` |
| **Canon promotion candidate** | A learning logged on Brand A repeats on Brand B and Brand C, same friction, same fix. Candidate for promotion to shared canon. | `{type: canon_promotion, learning_ids[], domain}` |

### Doctrine violation signals

| Signal | Trigger | Buffer entry |
|---|---|---|
| **Score leakage near-miss** | Agent produced an output where a numeric score almost surfaced (caught and reformulated). | `{type: score_leakage_near_miss, skill, draft}` |
| **Acronym leak near-miss** | Agent drafted a sentence with `CI / SED / CMR / SAD / PTD`, caught and rewrote before shipping. | `{type: acronym_leak_near_miss, skill, draft}` |
| **Modulator missing** | Multi-block output produced without voice consistency check, caught at finalize. | `{type: modulator_missing, skill, output}` |

### Decision reversal signals

| Signal | Trigger | Buffer entry |
|---|---|---|
| **Strategic reversal** | A previous session decision is contradicted by current session direction. The contradiction may be intentional (new info) or accidental (forgotten context). | `{type: decision_reversal, prior_decision_id, new_direction, surface_to_operator: bool}` |
| **Encoded fact drift** | A field encoded in `brand.json` is contradicted by what the operator says in conversation. | `{type: encoded_fact_drift, field_path, encoded_value, operator_value}` |

### Lifecycle / growth signals

| Signal | Trigger | Buffer entry |
|---|---|---|
| **Core saturated (Spectre · D#506)** | `import-meta-results` détecte `perf_signal == established` (état courant) ET `brand.meta.stage ≠ launch` ET pas de `spectrum.json` frais (absent ou `refreshed_at` > 90j) ET le signal pas déjà dans le buffer pour cette marque (dédupe) ET, jugement agent, le mur dominant est le MARCHÉ (`strategic-diagnostic-doctrine` · ne pas confondre cœur prouvé et mur ANGLE). Le cœur sature, il est temps de cartographier où aller ensuite. | `{type: core_saturated, brand, suggest: spectre}` |

---

## Batch and surface protocol

**Buffer every turn, scan every 3-5 turns.** The agent maintains the signal buffer silently. No interruption mid-flow.

**Threshold rules :**

- **≥2 same-type signals in the buffer** → flag for `learn-from-session` queue with *"pattern alert"* tag. Agent surfaces nothing immediately.
- **≥3 same-type signals within 7 days across sessions** → escalate to `correct-skill` [backlog, not shipped] candidate. Agent flags to operator briefly (*"j'ai noté que [pattern] revient · tu veux qu'on encode une règle ?"*) and waits for confirm.
- **1 signal of `decision_reversal` type** → surface immediately (single occurrence is high-cost). Operator decides if intentional or accidental.
- **1 signal of `encoded_fact_drift` type** → surface immediately with framed options (*"the brand.json says X, you just said Y. Update the brand or keep the conversational version local ?"*).
- **1 signal of `core_saturated` type** → surface immediately (single high-value · le moment d'ouvrir le Spectre est passager). Proposer la carte via le protocole Background (*"ton cœur sature, je peux cartographier où aller ensuite · on lance ?"*), integrate-or-defer. JAMAIS suggérer si le mur est OFFRE/ANGLE (route le diagnostic).

**Where the buffer lives.** In-session : agent's working memory. Cross-session : appended to `operator/session-state.md § Pattern buffer` as `[YYYY-MM-DD] {type}: {summary}`. `learn-from-session` reads this section at next batch fire and decides which signals graduate.

---

## What is NOT a pattern signal

To avoid noise, the daemon does **not** capture :

- One-off operator preferences (*"this time, longer please"*) · those are turn-local, not patterns
- Routine corrections that are part of the work (*"actually pivot the angle to anti-pitch"*) · that is collaboration, not friction
- Anything the operator already explicitly flagged as a learning (`capture-learning` already handles)
- Aesthetic preferences without structural impact (*"shorter lines"*) · register calibration, not pattern

The threshold is : *"would a senior operator reviewing this session say `we keep doing X, fix it`?"* If yes → signal. If no → skip.

---

## Hard Rules

1. **The buffer is silent unless threshold hit.** Operator never sees a signal mid-flow unless it is `decision_reversal` or `encoded_fact_drift` (high-cost singletons).
2. **Threshold is data-driven, not theoretical.** Working rule = ≥2 same-type signals to flag, ≥3 to escalate. After 30 days live, recalibrate.
3. **Pattern detection complements, never replaces, `learn-from-session`.** The daemon catches drift between batches ; `learn-from-session` does the deep extraction at trigger.
4. **Buffer entries are typed objects, not free prose.** Each entry follows the schema in tables above. Free-text observations route to `learnings.json` proper, not the pattern buffer.
5. **Singletons of high-cost types surface immediately.** Decision reversal and encoded fact drift skip the buffer entirely, they are surfaced in the same turn.
6. **The agent never editorializes the buffer.** It records observations, not interpretations. *"Operator corrected tone 3 times"* is a buffer entry. *"Operator seems frustrated with the tone"* is interpretation, refused.

---

## Cross-references

- `learn-from-session` · consumes the buffer at batch trigger fires. Patched v2.11.1 to log runtime patterns + session journal.
- `autonomous-correction-pattern.md` · also logs after 3 same-type refusals within 7 days. Both daemons feed the same pattern queue.
- `voice.md` § Anti-patterns · pattern types to watch (acronym leak, score leakage, plumbing leak)
- `contextual-intelligence.md` · the doctrine this daemon protects ; pattern detection is what keeps the contract alive across sessions
- `delegation-pattern.md` · sister doctrine ; delegation frictions (run-away, blackhole, dump, premature) are flagged in the buffer here for `correct-skill` [backlog, not shipped] candidacy

---

## Status

- **v1.0 doctrine** · operational. Ship the rules, calibrate thresholds after 30 days of live data.
- **Implementation note** · this is a doctrine document for skill authors. The actual daemon mechanics (when to scan, where to write the buffer, how to escalate) is operationalized via `learn-from-session` + future `invariant-violation-detector.py` hook (Phase 4.5 backlog).
