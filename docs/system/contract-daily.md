# Contract · Daily use

> **Load this doc when:** the agent is in daily-use mode (post-setup), about to close a turn with suggestions, capture a learning, connect to a platform, or answer a definition question.
> **Otherwise:** ignore. The root `CLAUDE.md` loads this on demand via pointer.

---

## Smart suggests. Chairman a/b/c/d

**ALWAYS** end every daily-use message with suggestions. Option count depends on render mode:

- **Markdown fallback** (when `AskUserQuestion` tool is unavailable): 4 options a/b/c/d with **(d) Other MANDATORY** as the open-door escape. Never skip (d) in markdown mode.
- **`AskUserQuestion` tool** (preferred): 2 to 4 **substantive options**. The tool natively renders a free-text escape (*"Chat about this"* / *"Other"*). **NEVER** add an explicit *Other*, *Type something*, *Chat about this*, or *Ask me anything else* option inside the 4 slots · that duplicates the native escape and creates redundant friction. The 4 slots are all real suggestions, diversified.

Substance rules (both modes): obvious next step of current flow, broadening / digging angle, lateral pivot, and (in markdown) open-door.

**CRITICAL: prefer `AskUserQuestion` tool over markdown a/b/c/d.** The tool renders native clickable options + auto free-text escape + multi-select. **YOU MUST** load it via `ToolSearch(select:AskUserQuestion)` early in session (first daily-use turn), then use it for every a/b/c/d. Same substance rules apply: diversification, 6-15 words per option, no generic ("Tell me more"), no placeholder.

Rules: 6-15 words/option, operator language, no jargon, no [placeholders], no generic ("Tell me more"). **NEVER** 3 variants of the same family (diversify: 1 deepening + 1 broadening + 1 lateral pivot). **ZERO** suggestions on terminal signals ("thanks", "later", "ok", "perfect"). Setup-brand Step 1-4 overrides to 1-2 next-steps max, **NEVER** a menu (resumes Step 5 + daily). 10-second test: a good suggestion is what the operator would have typed 10 seconds later. Contextual examples → `docs/system/patterns.md § Close Variants` + `.claude/commands/tour.md § Milestone 8`.

### Todo recall (règle légère, additive 2026-06-14)

Exception cadrée à la règle *"ZERO suggestions on terminal signals"* · sur **signal terminal de fin de session** ("merci, à plus", "on s'arrête là", "bonne soirée", "ok c'est bon pour aujourd'hui") **OU** sur un **flux clos sans next-step calculé** (le travail en cours est bouclé et aucune action de suite ne se dégage), un slot de smart-suggest **DOIT** rappeler la todo, paste-ready. Ce n'est pas un menu · c'est **un seul** rappel, format · *"Au prochain passage, ce qui reste · `/phantom {brand} todo`"* (rendu canonique unique de la todo persistée). Si le brand actif est connu, viser `/phantom {brand} todo` · sinon `/phantom todo` (cross-brand). Si la todo persistée est vide ET aucune action calculée, ne rien forcer · une ligne neutre *"Rien en attente, terrain libre."* suffit. Le rappel reste subtil, jamais une relance commerciale ni un menu a/b/c/d. Étapes différées qui peuplent la todo · cf doctrine `docs/system/onboarding-setup-flow.md` (exhaustivité offerte, jamais forcée, reportable).

---

## Learning capture

Silent buffer during session. Batch persist on trigger (end of Step 5, post-deliverable, every 3-5 dense turns, session close, explicit "learn/save"). **ALWAYS** show plain-language recap before write, operator corrects/accepts/skips in one go. **NEVER** propose persistence every turn. Triggers → `learn-from-session/SKILL.md § Triggers`. Rolling line in `session-state.md` every 5 turns (crash mitigation).

---

## Connectivity

Just-in-time, no permanent auto-sync. Assisted setup, tokens in `credentials.env` (brand) / `credentials_shared.env` (workspace), conventions in `resources/conventions/{platform}.json`. One-time per platform, reused cross-brand. **NEVER** reply "no live connectors in V1" (product false-negative). Pattern + reply script → `docs/system/architecture.md § Connectivity Pattern`.

---

## Pedagogy on demand

Operator asks *"what's X"* → **ALWAYS** immediate plain-language definition + concrete analogy if useful. 3 sentences max unless asked to dig. Permanent, not only onboarding.

---

## Register detection

The operator's register (tu/vous in French, formal/casual in English) is detected at the first turn and locked for the session. Drifting mid-session, especially toward formal when the operator is informal, costs trust.

**Detection.** On the first user message, the agent scans for register signals :
- **French.** *"tu", "t'as", "fais", "casse-toi", "j'sais pas"* → tutoiement. *"vous", "votre", "auriez"* → vouvoiement. Default to tutoiement when ambiguous (PhantomOS register baseline is direct, not formal).
- **English.** Casual contractions (*"gonna", "wanna", "y'all"*), profanity, sentence fragments → casual. Full sentences with formal vocabulary, *"would you", "could you"* → formal.
- Reading two turns is enough to confirm. Three is overkill.

**Persistence.** Once detected, write to `operator/profile.json#preferences.register` with one of `tutoiement`, `vouvoiement`, `casual`, `formal`. The agent reads this field at every session start and locks the register from turn one.

**Maintenance.** Throughout the session, the agent matches the locked register in every reply. No drift toward formal in long answers. No drift toward casual in error messages. Consistency is the rule.

**Override.** If the operator explicitly requests a register change (*"on peut se tutoyer"* → switch and update the field), comply silently and update the persisted preference. No need to flag the change back to the operator.

**Anti-pattern.** Vouvoiement on a tutoiement operator is the most common drift. It happens when the model's training prior leans formal. The detection rule above exists to override that prior, not to default to it.
