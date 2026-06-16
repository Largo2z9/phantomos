#!/usr/bin/env python3
"""
audit-context-budget · compute the total lines / estimated tokens of the
CLAUDE.md cascade and all lazy-loaded docs referenced from it. Pre-release
gate helper. Reports a warning if totals exceed configured thresholds.

Thresholds (soft · warn but don't fail):
  root CLAUDE.md         ≤ 140 lines  (cross-context rules only)
  always-loaded cascade  ≤ 250 lines  (root + child CLAUDE.md in brand path)
  lazy-loaded doc        ≤ 200 lines  (contract-build, contract-daily, etc.)
  full cascade (session) ≤ 600 lines  (root + 1 brand CLAUDE.md + 2 lazy)

Tokens estimated as lines * 8 (4 chars/token, ~30 chars/line average).

Usage:
  python3 .skills/audit-context-budget.py            # audit workspace root
  python3 .skills/audit-context-budget.py --json     # machine output
  python3 .skills/audit-context-budget.py --strict   # exit 1 if any overflow
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

THRESHOLDS = {
    "root": 140,
    "always_loaded": 250,
    "lazy_doc": 200,
    "full_session": 600,
}

# Lazy-loaded doc paths mentioned in the root CLAUDE.md.
LAZY_REFS_RE = re.compile(r"`(docs/system/[^`]+\.md)`")


def die(msg, code=1):
    print(f"[audit-context-budget] ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def find_workspace_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(8):
        if (cur / "CLAUDE.md").is_file() and (cur / "brands").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    die(f"no workspace with CLAUDE.md + brands/ found (from {start})")


def count_lines(p: Path) -> int:
    if not p.is_file():
        return 0
    return sum(1 for _ in p.open(encoding="utf-8"))


def tokens(lines: int) -> int:
    return lines * 8


def main():
    ap = argparse.ArgumentParser(prog="audit-context-budget")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any threshold breached")
    ap.add_argument("--cwd", default=os.getcwd())
    args = ap.parse_args()

    root = find_workspace_root(Path(args.cwd))
    root_claude = root / "CLAUDE.md"
    root_text = root_claude.read_text(encoding="utf-8")
    root_lines = root_text.count("\n") + 1

    # Brand-level CLAUDE.md (only one loads per session · pick the _TEMPLATE as
    # reference, operator-instance brands have one each same size).
    tmpl_claude = root / "brands" / "_TEMPLATE" / "CLAUDE.md"
    brand_lines = count_lines(tmpl_claude)

    # Lazy-loaded docs referenced from root CLAUDE.md.
    lazy_refs = sorted(set(LAZY_REFS_RE.findall(root_text)))
    lazy_stats = []
    for ref in lazy_refs:
        p = root / ref
        lazy_stats.append({"path": ref, "lines": count_lines(p)})

    # Always-loaded total = root + brand CLAUDE.md.
    always = root_lines + brand_lines
    # Worst-case session = always + up to 2 lazy docs co-loaded.
    top_2_lazy = sorted((d["lines"] for d in lazy_stats), reverse=True)[:2]
    full = always + sum(top_2_lazy)

    findings = []
    if root_lines > THRESHOLDS["root"]:
        findings.append(("WARN", f"CLAUDE.md {root_lines} > {THRESHOLDS['root']} lines · push single-pillar rules to child CLAUDE.md"))
    if always > THRESHOLDS["always_loaded"]:
        findings.append(("WARN", f"always-loaded cascade {always} > {THRESHOLDS['always_loaded']} lines · shrink root or brand CLAUDE.md"))
    for d in lazy_stats:
        if d["lines"] > THRESHOLDS["lazy_doc"]:
            findings.append(("WARN", f"{d['path']} {d['lines']} > {THRESHOLDS['lazy_doc']} lines · split"))
    if full > THRESHOLDS["full_session"]:
        findings.append(("WARN", f"worst-case session {full} > {THRESHOLDS['full_session']} lines · cascade too fat"))

    report = {
        "root": {"lines": root_lines, "tokens_est": tokens(root_lines),
                 "threshold": THRESHOLDS["root"]},
        "brand_template": {"lines": brand_lines, "tokens_est": tokens(brand_lines)},
        "always_loaded": {"lines": always, "tokens_est": tokens(always),
                          "threshold": THRESHOLDS["always_loaded"]},
        "lazy_docs": lazy_stats,
        "worst_case_session": {"lines": full, "tokens_est": tokens(full),
                               "threshold": THRESHOLDS["full_session"]},
        "findings": [{"severity": s, "message": m} for s, m in findings],
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"[audit-context-budget] {root}")
        print(f"  root CLAUDE.md           {root_lines:>5d} lines  (~{tokens(root_lines)} tok)  threshold {THRESHOLDS['root']}")
        print(f"  brand _TEMPLATE          {brand_lines:>5d} lines")
        print(f"  always-loaded total      {always:>5d} lines  (~{tokens(always)} tok)  threshold {THRESHOLDS['always_loaded']}")
        if lazy_stats:
            print(f"  lazy-loaded docs:")
            for d in lazy_stats:
                mark = "!" if d["lines"] > THRESHOLDS["lazy_doc"] else " "
                print(f"   {mark} {d['path']:<40s} {d['lines']:>5d} lines")
        print(f"  worst-case session       {full:>5d} lines  (~{tokens(full)} tok)  threshold {THRESHOLDS['full_session']}")
        if findings:
            print(f"\nfindings ({len(findings)}):")
            for s, m in findings:
                print(f"  [{s}] {m}")
        else:
            print("\nbudget OK · all thresholds respected.")

    if args.strict and findings:
        sys.exit(1)


if __name__ == "__main__":
    main()
