# Failure taxonomy · error-analysis first

The rubrics in `rubrics/` were authored top-down from the doctrine. The field is emphatic that authored criteria drift and miss the real failure surface (Hamel Husain, Shreya Shankar: error-analysis is 60-80% of an eval's value, write evals for the errors you DISCOVER, not the ones you imagine). This file is the discipline that keeps the eval an instrument instead of a guess.

## The loop

1. **Collect.** Drop 20-30 real run outputs (close / angle / diagnostic, sharp and mushy) into `ratings.jsonl` with the operator's good/bad call. Real outputs beat authored ones; the slot exists for exactly this.
2. **Open-code.** Read each, name the failure in plain words, group recurring failures into modes. Stop when two consecutive rounds surface no new mode (saturation).
3. **Cheapest assertion per mode.** For each mode, write the cheapest check that catches it: a deterministic proxy if it is mechanizable, else a judge criterion, else a manual watch item. Do not reach for the judge when a regex suffices.
4. **Let the taxonomy drive the rubric.** A criterion or proxy exists because a real failure mode demanded it, not because the doctrine listed it. Add and cut accordingly.
5. **Guard the instrument.** A 100% pass rate means the suite is too weak, not that the output is perfect (the eval is a reward surface; a hollow artifact will learn to game it). When the suite goes all-green, harden it. Run a periodic adversarial audit that tries to PASS the eval with deliberately hollow output.

## Seed (known modes, from doctrine + the liv/onday runs)

**Every row below is IMAGINED, not DISCOVERED.** It is doctrine-seeded (AP-1..7 plus the two historical liv/onday runs), not yet open-coded from a real output, which is the exact thing this file warns against. Treat the table as a checklist of work-to-do, not a finished taxonomy: a row earns "discovered" only once a real coded output exhibits it. Until error-analysis runs on real outputs, this is a placeholder.

| Mode | Artifact | Tell | Rubric criterion violated | Cheapest check | Status | Source |
|---|---|---|---|---|---|---|
| **WEATHER-REPORT** | close | facts shown, no interpretation, then a passive question | `expert_reading_present` | proxy (low decision-verb) + judge | proxy+judge | liv/onday, the core failure |
| **MENU-HANDOFF** | close | flat symmetric menu, "lequel veux-tu creuser ?" | `proactive_motion` | proxy `menu_of_axes`, `ends_with_operator_question` | proxy | liv run |
| **HOMEWORK-PILE** | close | 2+ questions the operator must answer before anything moves | `at_most_one_gate` | proxy `question_to_operator_count` | proxy | liv run |
| **NO-NOTICING** | all | facts + a generic read, nothing non-obvious seen | `expert_reading_present` (the subtle one) | judge only | judge | the noticing gap |
| **HYPOTHESIS-AS-FACT** | all | a deduced claim (audience, ROAS, driver) stated as established fact | `fact_hypothesis_separated` | proxy `has_confidence_chain` absence + judge | proxy+judge | investigation-posture AP-1 |
| **INVENTED-PERSONA** | diagnostic/audience | a persona presented as analytical with no verbatim data | `factual_grounding` / position-before-audiences | judge | judge | AP-2 |
| **NARRATIVE-COPY** | all | landing-page copywriting disguised as analysis | (cross) | proxy `generic_filler` + judge | proxy+judge | AP-3 |
| **CONCLUSION-NO-INVESTIGATION** | all | a number/verdict with no conditioning assumption named | `fact_hypothesis_separated` | judge | judge | AP-4 |
| **GENERIC-ANGLE** | angle | truism, no named negative, passes the rename test | `negative_named` / `anti_generic` | proxy `has_negative_coordinate` absence, `generic_filler` | proxy+judge | angle rubric |
| **FLAT-INVENTORY** | diagnostic | a checklist of "could improve", no dominant wall ranked | `dominant_wall_named` | judge | judge | diagnostic rubric |
| **FALSE-GATE** | close | blocks on a question that is knowable from data or not on the critical path | `at_most_one_gate` (quality) | judge | judge | the gate trichotomy |

## Coverage check

`eval-runner.py --alignment` reports, per artifact: which taxonomy modes have a deterministic proxy vs are judge-only vs manual, and the agreement between the cheap proxy verdict and the operator's ratings (the alignment score, floored at `CALIBRATION_FLOOR`). A mode with no check and no golden is a blind spot. A judge-only mode with no golden example is unverified. The alignment score is the regression metric: when it drops on a model swap or after a rubric edit, the instrument moved, not just the output.

## Discipline notes

- Write the assertion for the error you SAW in a real output, not the one you can imagine.
- Prefer a proxy; reserve the judge for genuinely subjective qualities (the noticing, the persona-as-fact).
- Recalibrate, do not set-and-forget: the operator's notion of "expert" sharpens as he sees more outputs, so the golden set and judge prompt are versioned, not one-time.
- A mode that the current model has stopped producing is a removal candidate (the Bitter Lesson applies to eval criteria too): drop it, or keep one golden as a regression guard and note why.
