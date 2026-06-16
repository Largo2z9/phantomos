# Exemplars · the few-shot bank

For posture, style, and judgment, showing two examples beats thirty rules. The model has an RLHF bias toward the polite hedge; a rule pushes against it weakly, an example pushes hard. This bank is the positive (and negative) instances of the standards the doctrines describe in prose.

A skill or doctrine that produces a typed artifact (a close, an angle, a diagnostic) cites the matching file here so the runtime SEES the target instead of re-deriving it from rules. One file per artifact, same uniform frame, typed content. This is the function-pole-map pattern applied to teaching: shared skeleton, typed entries.

## How to read one

Each file holds the artifact's one-line target, a **sharp** instance to emulate, and a **mushy** instance to avoid, each with a one-line "why". The contrast (this, not that) is itself a strong few-shot signal.

## Relationship to evals/

The bank and `evals/` share the same standard and the same canonical scenario (liv konjac). The exemplars TEACH (cited at production time); the eval goldens MEASURE (scored at release). When the standard moves, update both: the exemplar here and the golden under `evals/golden/`. The rubric in `evals/rubrics/{artifact}.json` is the written specification both serve.

## Files

- `close.md` · the end of any strategic synthesis. Target: affirm the move, open the questions yourself, gate only when blocked.
- `angle.md` · a paid angle. Target: a falsifiable stance against a named negative, anchored to the mechanism.
- `diagnostic.md` · the brand-level read. Target: name the dominant wall, read position before audiences, confidence on every deduced claim.

## Adding an artifact

Drop `{artifact}.md` with the same three parts (target, sharp+why, mushy+why), add a rubric under `evals/rubrics/`, and a golden pair under `evals/golden/`. The three move together.
