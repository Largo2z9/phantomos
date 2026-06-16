#!/usr/bin/env python3
"""
eval-runner.py ·Quality eval harness for PhantomOS strategic artifacts.

This is the instrument. It measures whether the runtime *tranche* (decides a move)
instead of *describing*, and it doubles as the regression detector that makes a
model swap safe: re-run it on a new model, and if the score drops you know the
model-dependent layer (exemplars, posture nudges) needs re-tuning, not the substrate.

It runs ENTIRELY off-runtime. It never touches a brand, never mutates, never
pre-validates the model at write time. It scores authored golden artifacts and,
at release, the judge scores real output.

Three layers, cheap to expensive:
  1. proxies  ·deterministic surface signals (proxies.py). Free, run always.
  2. calibrate ·agreement between the proxy verdict and the operator's own ratings
                 (ratings.jsonl). This is what keeps the cheap floor honest: a proxy
                 that disagrees with Largo is a proxy to fix.
  3. judge    ·assemble per-artifact LLM-judge prompts (judge.md) for the semantic
                verdict. Run by a model at release, calibrated by the same ratings.

Usage (from workspace-template/evals/):
  python3.11 eval-runner.py                 # proxies + calibration summary (default)
  python3.11 eval-runner.py --proxies       # proxy verdicts per golden, exit 1 if any mislabels
  python3.11 eval-runner.py --calibrate      # proxy-vs-operator agreement, exit 1 below threshold
  python3.11 eval-runner.py --assemble-judge # write filled judge prompts to _judge-queue/
  python3.11 eval-runner.py --artifact close # restrict to one artifact

Stdlib only. python3.11 (system python3 is 3.14 with a broken pyexpat).
"""

import argparse
import json
import sys
from pathlib import Path

import proxies as PX

HERE = Path(__file__).resolve().parent
RUBRICS_DIR = HERE / "rubrics"
GOLDEN_DIR = HERE / "golden"
RATINGS = HERE / "ratings.jsonl"
JUDGE_TEMPLATE = HERE / "judge.md"
JUDGE_QUEUE = HERE / "_judge-queue"

CALIBRATION_FLOOR = 0.80  # proxy verdict must agree with operator on >=80% of rated cases

SEED_BANNER = ("SEED-ONLY: every rated case is an authored golden, so this score is "
               "tautological (the proxies were tuned on these same texts). It is NOT yet a "
               "regression gate. Fill ratings.jsonl with real run outputs (see "
               "failure-taxonomy.md) before trusting it.")


def _seed_only(ratings, goldens):
    """True when every rated case is an authored seed golden. Then the alignment /
    calibration score is self-confirming and must not read as a passing gate."""
    return bool(ratings) and set(ratings) <= {case_name(g) for g in goldens}


# --------------------------------------------------------------------------- #
# Loaders
# --------------------------------------------------------------------------- #

def load_rubrics():
    out = {}
    for p in sorted(RUBRICS_DIR.glob("*.json")):
        if p.name.startswith("_"):
            continue
        r = json.loads(p.read_text(encoding="utf-8"))
        out[r["artifact"]] = r
    return out


def load_goldens(artifact_filter=None):
    out = []
    for p in sorted(GOLDEN_DIR.glob("*.md")):
        if p.name.startswith("_"):
            continue
        g = PX.parse_golden(p)
        if not g["artifact"]:
            continue
        if artifact_filter and g["artifact"] != artifact_filter:
            continue
        out.append(g)
    return out


def load_ratings():
    """Operator calibration: {case -> operator_rating in {good,bad}}."""
    out = {}
    if not RATINGS.exists():
        return out
    for line in RATINGS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        case = rec.get("case")
        rating = rec.get("operator_rating")
        if case and rating:
            out[case] = rating
    return out


def case_name(golden):
    return Path(golden["path"]).stem


# --------------------------------------------------------------------------- #
# Layers
# --------------------------------------------------------------------------- #

def proxy_eval(rubrics, goldens):
    """Run proxies per golden. Returns rows + a discrimination flag.

    A golden labelled 'sharp' should get verdict 'sharp'; 'mushy' -> 'mushy'.
    """
    rows = []
    mislabels = 0
    for g in goldens:
        rubric = rubrics.get(g["artifact"])
        if not rubric:
            rows.append({"case": case_name(g), "error": f"no rubric for {g['artifact']}"})
            mislabels += 1
            continue
        res = PX.run_proxies(g["body"], rubric["proxies"])
        expected = g["label"]
        ok = (res["verdict"] == expected)
        if not ok:
            mislabels += 1
        rows.append({
            "case": case_name(g), "artifact": g["artifact"], "expected": expected,
            "verdict": res["verdict"], "score": res["score"], "ok": ok,
            "signals": res["signals"],
        })
    return rows, mislabels


def calibrate(rows, ratings):
    """Agreement between proxy verdict and operator rating (sharp~good / mushy~bad)."""
    verdict_to_rating = {"sharp": "good", "mushy": "bad"}
    rated, agree = 0, 0
    misses = []
    for r in rows:
        if "verdict" not in r:
            continue
        op = ratings.get(r["case"])
        if not op:
            continue
        rated += 1
        mapped = verdict_to_rating.get(r["verdict"], "neutral")
        if mapped == op:
            agree += 1
        else:
            misses.append({"case": r["case"], "proxy": mapped, "operator": op})
    rate = (agree / rated) if rated else 0.0
    return {"rated": rated, "agree": agree, "rate": round(rate, 3), "misses": misses}


def alignment_by_artifact(rows, ratings):
    """Per-artifact alignment score (proxy verdict vs operator rating).

    The named regression metric: when this drops after a model swap or a rubric
    edit, the instrument moved, not just the output. Which failure modes have a
    proxy at all lives in failure-taxonomy.md; this measures whether the proxies
    that exist still agree with the operator. Error-analysis-first (see the
    taxonomy) is what fills ratings.jsonl with the real signal this reads.
    """
    verdict_to_rating = {"sharp": "good", "mushy": "bad"}
    by = {}
    for r in rows:
        if "verdict" not in r:
            continue
        op = ratings.get(r["case"])
        if not op:
            continue
        d = by.setdefault(r["artifact"], {"rated": 0, "agree": 0})
        d["rated"] += 1
        if verdict_to_rating.get(r["verdict"], "neutral") == op:
            d["agree"] += 1
    for d in by.values():
        d["score"] = round(d["agree"] / d["rated"], 3) if d["rated"] else 0.0
    return by


def assemble_judge(rubrics, goldens):
    """Fill the judge template per golden, write to _judge-queue/."""
    if not JUDGE_TEMPLATE.exists():
        print("✗ judge.md template missing", file=sys.stderr)
        return 0
    template = JUDGE_TEMPLATE.read_text(encoding="utf-8")
    JUDGE_QUEUE.mkdir(exist_ok=True)
    written = 0
    for g in goldens:
        rubric = rubrics.get(g["artifact"])
        if not rubric:
            continue
        criteria_block = "\n".join(
            f"- **{c['id']}** (weight {c['weight']}): PASS = {c['pass']} | FAIL = {c['fail']}"
            for c in rubric["criteria"]
        )
        filled = (template
                  .replace("{{ARTIFACT}}", rubric["artifact"])
                  .replace("{{DEFINITION}}", rubric["definition"])
                  .replace("{{TARGET}}", rubric["target"])
                  .replace("{{CRITERIA}}", criteria_block)
                  .replace("{{BODY}}", g["body"]))
        out = JUDGE_QUEUE / f"{case_name(g)}.md"
        out.write_text(filled, encoding="utf-8")
        written += 1
    return written


def scan_beats(root, rubrics):
    """Advisory post-hoc scan of real close/beat payloads (.phantom/beats/**.json).

    The post-hoc tooth for the close. It reuses the close rubric proxies to flag a
    close that does not tranche (the weather report) or that carries no verdict at
    all. It NEVER blocks and never touches the write path: it observes a finished
    artifact. It also feeds the eval, real closes become calibration data over time.
    Returns rows.
    """
    close_rubric = rubrics.get("close")
    proxy_specs = close_rubric["proxies"] if close_rubric else []
    root = Path(root)
    rows = []
    for bf in sorted(root.glob("**/.phantom/beats/*/*.json")):
        try:
            payload = json.loads(bf.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            rows.append({"path": str(bf), "error": str(e)})
            continue
        verdict = str(payload.get("verdict") or "").strip()
        read = str(payload.get("read") or "").strip()
        text = (verdict + "\n" + read).strip()
        res = PX.run_proxies(text, proxy_specs) if text else {"verdict": "empty", "score": 0.0}
        try:
            rel = str(bf.relative_to(root))
        except ValueError:
            rel = str(bf)
        rows.append({
            "path": rel,
            "phase": str(payload.get("phase") or "?"),
            "has_verdict": bool(verdict),
            "verdict": res["verdict"],
            "score": res["score"],
        })
    return rows


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #

def print_proxy_table(rows):
    print("PROXY VERDICTS")
    print(f"  {'case':28s} {'artifact':11s} {'exp':6s} {'got':7s} {'score':>6s}  ok")
    for r in rows:
        if "error" in r:
            print(f"  {r['case']:28s} ERROR: {r['error']}")
            continue
        mark = "✓" if r["ok"] else "✗"
        print(f"  {r['case']:28s} {r['artifact']:11s} {r['expected']:6s} "
              f"{r['verdict']:7s} {r['score']:6.1f}  {mark}")


def print_signal_detail(rows):
    print("\nSIGNAL DETAIL (what fired)")
    for r in rows:
        if "signals" not in r:
            continue
        fired = [f"{s['name']}={s['raw']}({s['contribution']:+g})"
                 for s in r["signals"] if s.get("fired")]
        print(f"  {r['case']:28s} -> {', '.join(fired) if fired else '(no signal fired)'}")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description="PhantomOS quality eval harness")
    ap.add_argument("--proxies", action="store_true", help="proxy verdicts only")
    ap.add_argument("--calibrate", action="store_true", help="proxy-vs-operator agreement only")
    ap.add_argument("--assemble-judge", action="store_true", help="write filled judge prompts")
    ap.add_argument("--artifact", default=None, help="restrict to one artifact")
    ap.add_argument("--detail", action="store_true", help="show per-signal detail")
    ap.add_argument("--beats", default=None, metavar="PATH",
                    help="advisory post-hoc scan of real .phantom/beats payloads under PATH")
    ap.add_argument("--alignment", action="store_true",
                    help="per-artifact alignment score (proxy vs operator ratings), the regression metric")
    args = ap.parse_args()

    rubrics = load_rubrics()

    if args.beats:
        beat_rows = scan_beats(args.beats, rubrics)
        if not beat_rows:
            print(f"no beat payloads found under {args.beats}/**/.phantom/beats/")
            return 0
        print("BEAT ADVISORY (post-hoc, never blocks)")
        print(f"  {'beat':46s} {'phase':10s} {'verdict?':8s} {'reads':7s} {'score':>6s}")
        flagged = 0
        for r in beat_rows:
            if "error" in r:
                print(f"  {r['path']:46s} ERROR: {r['error']}")
                continue
            v = "yes" if r["has_verdict"] else "NO"
            advisory = (not r["has_verdict"]) or (r["verdict"] in ("mushy", "neutral"))
            mark = "  <-- advisory" if advisory else ""
            flagged += 1 if advisory else 0
            print(f"  {r['path']:46s} {r['phase']:10s} {v:8s} {r['verdict']:7s} {r['score']:6.1f}{mark}")
        print(f"\n{flagged} close/beat(s) flagged (no verdict or reads mushy). Advisory only, nothing blocked.")
        real = len([r for r in beat_rows if "error" not in r])
        if flagged == 0 and real >= 5:
            print("note: 0 flagged across many real closes. If the operator disagrees with any of them, "
                  "the suite is too weak (see failure-taxonomy.md): harden a proxy or add a golden.")
        return 0

    goldens = load_goldens(args.artifact)
    if not goldens:
        print("✗ no golden artifacts found under evals/golden/", file=sys.stderr)
        return 2

    if args.assemble_judge:
        n = assemble_judge(rubrics, goldens)
        print(f"✓ assembled {n} judge prompt(s) -> {JUDGE_QUEUE.relative_to(HERE.parent)}/")
        return 0

    rows, mislabels = proxy_eval(rubrics, goldens)

    if args.alignment:
        ratings = load_ratings()
        by = alignment_by_artifact(rows, ratings)
        print(f"ALIGNMENT SCORE (proxy vs operator ratings, floor {CALIBRATION_FLOOR})")
        if _seed_only(ratings, goldens):
            print("  " + SEED_BANNER)
        if not by:
            print("  no rated cases yet. Fill ratings.jsonl with real outputs (see failure-taxonomy.md).")
            return 0
        worst = 1.0
        for art in sorted(by):
            d = by[art]
            mark = "" if d["score"] >= CALIBRATION_FLOOR else "  <-- below floor"
            worst = min(worst, d["score"])
            print(f"  {art:12s} {d['agree']}/{d['rated']}  score={d['score']}{mark}")
        print(f"\nworst-artifact alignment = {round(worst, 3)}. A drop here on a model swap or rubric edit = the instrument moved.")
        return 0 if worst >= CALIBRATION_FLOOR else 1

    if args.calibrate:
        ratings = load_ratings()
        cal = calibrate(rows, ratings)
        print(f"CALIBRATION  rated={cal['rated']}  agree={cal['agree']}  rate={cal['rate']}")
        if _seed_only(ratings, goldens):
            print("  " + SEED_BANNER)
        for m in cal["misses"]:
            print(f"  ✗ {m['case']:28s} proxy={m['proxy']} operator={m['operator']}")
        return 0 if cal["rate"] >= CALIBRATION_FLOOR else 1

    print_proxy_table(rows)
    if args.detail:
        print_signal_detail(rows)

    if not args.proxies:
        ratings = load_ratings()
        cal = calibrate(rows, ratings)
        print(f"\nCALIBRATION  rated={cal['rated']}  agree={cal['agree']}  rate={cal['rate']} "
              f"(floor {CALIBRATION_FLOOR})")
        if _seed_only(ratings, goldens):
            print("  " + SEED_BANNER)
        for m in cal["misses"]:
            print(f"  ✗ {m['case']:28s} proxy={m['proxy']} operator={m['operator']}")

    print(f"\nDISCRIMINATION  {len(rows) - mislabels}/{len(rows)} goldens correctly separated")
    return 0 if mislabels == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
