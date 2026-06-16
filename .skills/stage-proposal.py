#!/usr/bin/env python3
"""
stage-proposal · register a pending proposal tied to a workflow checkpoint.

Called by a skill when it wants to propose a value that requires operator
confirmation before being persisted. Writes to brands/{slug}/.workflow.json
under `pending`. The next operator turn is resolved by the checkpoint-resolver
UserPromptSubmit hook.

Usage:
    python3 .skills/stage-proposal.py \\
        --brand {slug} \\
        --checkpoint confirmed_products \\
        --product-slug {product-slug} \\
        --summary "Hero detected: {product name} · {url}" \\
        [--product-slug vitamines-hair-boost]

Checkpoints known:
    audience_q1q4_answered      · unlocks audiences/*/profile.json writes
    confirmed_products          · per-product gate, pass --product-slug,
                                  unlocks products/{slug}/spec.json + offers.json

Exit codes:
    0 success
    1 arg / state error
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

KNOWN_CHECKPOINTS = {
    "audience_q1q4_answered",
    "confirmed_products",
}


def die(msg, code=1):
    print(f"[stage_proposal] ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def find_workspace_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(8):
        if (cur / "brands").is_dir() and (cur / "resources").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    die(f"not inside a PhantomOS workspace (from {start})")


def load_workflow(brand_dir: Path) -> dict:
    wf = brand_dir / ".workflow.json"
    if wf.exists():
        try:
            return json.loads(wf.read_text())
        except json.JSONDecodeError as e:
            die(f"{wf} corrupt: {e}")
    return {
        "_schema": "workflow-state/1.0",
        "checkpoints": {
            "audience_q1q4_answered": False,
            "confirmed_products": [],
        },
        "pending": None,
        "history": [],
    }


def save_workflow(brand_dir: Path, state: dict) -> None:
    (brand_dir / ".workflow.json").write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n"
    )


def main():
    ap = argparse.ArgumentParser(prog="stage-proposal")
    ap.add_argument("--brand", required=True)
    ap.add_argument("--checkpoint", required=True, choices=sorted(KNOWN_CHECKPOINTS))
    ap.add_argument("--summary", required=True,
                    help="Plain-language summary shown in the audit trail")
    ap.add_argument("--product-slug", default=None,
                    help="Required when checkpoint=confirmed_products")
    ap.add_argument("--cwd", default=os.getcwd())
    args = ap.parse_args()

    if args.checkpoint == "confirmed_products" and not args.product_slug:
        die("--product-slug required for checkpoint=confirmed_products")

    root = find_workspace_root(Path(args.cwd))
    brand_dir = root / "brands" / args.brand
    if not brand_dir.is_dir():
        die(f"brand not found: {brand_dir}")

    state = load_workflow(brand_dir)

    if state.get("pending"):
        die(
            "a proposal is already pending. Resolve it before staging a new one "
            f"(current: {state['pending'].get('checkpoint')} · "
            f"{state['pending'].get('summary')})"
        )

    state["pending"] = {
        "checkpoint": args.checkpoint,
        "product_slug": args.product_slug,
        "summary": args.summary,
        "staged_at": datetime.utcnow().isoformat() + "Z",
    }
    save_workflow(brand_dir, state)
    print(f"[stage_proposal] staged: {args.checkpoint}"
          + (f":{args.product_slug}" if args.product_slug else ""))


if __name__ == "__main__":
    main()
