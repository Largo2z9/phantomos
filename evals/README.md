# evals · the quality instrument

PhantomOS puts teeth into everything structural (encoding integrity, mutation guard, the beat) and nothing into what is expert: the judgment, the actual value. So the runtime *describes* (safe) instead of *deciding* (the move), and no gate catches it. This directory is the missing instrument. It measures whether a strategic artifact *tranche* instead of narrating.

It is the keystone of the prompting work: without a measure, every posture change is tuned blind. It is also the regression detector that makes a model swap safe (see Durability below).

## What it is not

- Not a runtime gate. Nothing here runs at write time. Nothing imports a brand or mutates anything. It scores finished artifacts off-runtime, at release.
- Not a single LLM grade trusted on faith. The judge is calibrated against the operator's own good/bad calls (`ratings.jsonl`) and floored by deterministic proxies.

## The three layers (cheap to expensive)

1. **proxies** (`proxies.py`) · deterministic surface signals, stdlib only, free. Does the close commit to a move (a decision verb)? Does it end on a menu of axes handed to the operator? Hedge density? These catch the obvious failures for nothing and anchor the judge.
2. **calibration** (`ratings.jsonl`) · the operator's own good/bad ratings. The proxy and judge verdicts are checked against these. Disagreement means the rubric is wrong, not Largo. Floor: proxy must agree with the operator on >=80% of rated cases (`CALIBRATION_FLOOR`).
3. **judge** (`judge.md`) · a per-artifact LLM-judge prompt, assembled by the runner, scored by a model at release. Carries the semantic verdict the proxies cannot.

## Structure (uniform frame, typed registry)

```
evals/
  rubrics/
    _rubric.schema.json   the shared frame (every rubric validates against this)
    close.json            typed: what a sharp close is, the criteria, the proxies
    angle.json            typed
    diagnostic.json       typed
  golden/
    close-sharp.md        authored gold: a close that decides
    close-mushy.md        authored anti-gold: the weather report
    angle-{sharp,mushy}.md
    diagnostic-{sharp,mushy}.md
  proxies.py              the deterministic check library + golden parser
  judge.md                the judge prompt template ({{ARTIFACT}}/{{TARGET}}/{{BODY}})
  ratings.jsonl           operator calibration (seeded; Largo adds real ratings)
  eval-runner.py          orchestrator
```

The frame is uniform (one rubric schema, one ton/posture target shape); the content is typed per artifact (a close is not an angle is not a diagnostic). Same pattern as `resources/canon/operator/function-pole-map.json`: shared skeleton, typed entries.

## Run it

```
cd workspace-template/evals
python3.11 eval-runner.py                 # proxies + calibration summary
python3.11 eval-runner.py --proxies --detail   # per-signal breakdown
python3.11 eval-runner.py --calibrate     # proxy-vs-operator agreement, exit 1 below floor
python3.11 eval-runner.py --assemble-judge     # write filled judge prompts to _judge-queue/
python3.11 eval-runner.py --beats <workspace>  # advisory scan of real close payloads (.phantom/beats/), never blocks
python3.11 eval-runner.py --alignment          # per-artifact alignment score (proxy vs operator), the regression metric
```

The `--beats` scan is the post-hoc tooth for the close: it reads finished `close.json` beat payloads from a real workspace, flags any with no verdict or a verdict that reads mushy (the weather report), and blocks nothing. It also feeds calibration: real closes become rating candidates over time.

Use `python3.11` (system `python3` is 3.14 with a broken pyexpat). Stdlib only, no install.

## Error-analysis first, and the looped judge

The rubrics were authored top-down from the doctrine, which the field says will drift and miss the real failure surface. `failure-taxonomy.md` is the correction: collect 20-30 real outputs into `ratings.jsonl`, open-code them into named failure modes until saturation, and write the cheapest check per mode (a proxy if mechanizable, else a judge criterion). The taxonomy drives the rubric, not the other way round. `--alignment` is the regression metric: per-artifact agreement between the cheap proxy and the operator's ratings; when it drops on a model swap or a rubric edit, the instrument moved.

The judge is run by a model at release, not by `eval-runner.py`: the runner only assembles the filled prompt (`--assemble-judge`); a model then scores it and runs the repair loop. The judge contract is asymmetric (terse on a pass, full structured diagnostics on a fail: the named failure mode + a `rewrite_hint`), then it rewrites the artifact per the hint and re-scores it (`repaired_verdict`). The eval is also a reward surface, so it is guarded: a 100% pass rate on real outputs means the suite is too weak (harden it), and a periodic adversarial audit tries to make a hollow artifact pass to find the holes. See `judge.md`. The deterministic `proxies.py` floor is what runs without a model.

## The target the rubrics encode

The close rubric encodes the resolved posture (affirm the move, open the questions yourself, gate only when blocked). This intentionally moves beyond `docs/system/investigation-posture.md` Section 5 (close = a macro question the operator answers), which produced the describe-and-outsource failure. The mapping rigor (Observé/Déduit/Inconnu) stays. The doctrine is amended to match in the same body of work; `close.json#supersedes` names the dependency.

## Durability · the test that matters

Re-run the eval on a different model (or a simulated one). If the score drops, the decoupling did its job: you know the model-dependent layer (exemplars, posture nudges, thresholds) needs re-tuning, and the substrate (schemas, data, the mechanical layer) did not move. The eval is how a model swap stays safe instead of silent.

## Adding a golden or a rating

- Golden: drop `evals/golden/{artifact}-{label}.md` with frontmatter `artifact`, `label` (sharp|mushy), `brand`, `note`, then the body. The runner picks it up automatically.
- Rating: append one line to `ratings.jsonl` (`case`, `artifact`, `operator_rating`, `note`). Real run outputs are the highest-value ratings.
