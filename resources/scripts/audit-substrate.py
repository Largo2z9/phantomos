#!/usr/bin/env python3
"""
audit-substrate.py · freshness + coherence audit of a brand's encoded substrate.

The substrate (the encoded domain model: brand, products, audiences, angles,
spectrum, learnings) is PhantomOS's biggest lever and, per the 2025-2026 agent
literature, its biggest unguarded risk: a rich substrate rots harder than thin
context, and there is no algorithmic fix but curation. This is the curation tooth.

It is ADVISORY and post-hoc. It reads finished JSON and flags two things:
  1. STALE regions   · a freshness timestamp older than its declared TTL, or older
                       than a velocity-adjusted default when no TTL is declared.
  2. INCOHERENT refs · a strategic pointer that dangles, e.g. an angle whose
                       spectrum_cell_ref points at a cell that no longer exists.

It never blocks, never mutates, makes no model call, and degrades gracefully when
the freshness clock or the spectrum is not populated (a thin or fresh brand simply
reports nothing). Run on a schedule or at release.

Usage (from workspace-template root):
    python3.11 resources/scripts/audit-substrate.py [--root PATH] [--brand SLUG]
        [--default-ttl-days N] [--json] [--strict]

--strict exits 1 if any STALE or DANGLING item is found (for a scheduled gate).
Stdlib only. python3.11 (system python3 is 3.14 with a broken pyexpat).
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Freshness timestamps (data recency), NOT structural ones (created_at / scaffolded_at
# record when a file was made, not how fresh its data is). `extracted_at` is the
# REQUIRED timestamp of the canonical provenance object
# (resources/schemas/_shared/extraction-provenance.json, required: extraction_method
# + extracted_at), so it leads the list.
FRESHNESS_TS = ("extracted_at", "captured_at", "scraped_at", "validated_at",
                "last_updated", "refreshed_at", "as_of")
TTL_FIELDS = ("ttl_days", "freshness_ttl_days", "decay_ttl_days")
# Canonical velocity tiers and their ttl_days, mirrored from
# extraction-provenance.json _meta.velocity_tiers. The longevity of a signal feeds
# its freshness, so ttl is the decay horizon per tier, not the brick's age.
VELOCITY_DEFAULT_TTL = {"static": 365, "slow": 180, "drift": 90, "weekly": 21, "live": 3}


def _parse_date(s):
    if not isinstance(s, str) or len(s) < 8:
        return None
    txt = s.strip().replace("Z", "+00:00")
    for cut in (txt, txt[:10]):
        try:
            d = datetime.fromisoformat(cut)
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _walk_objects(obj, path="$"):
    """Yield every dict in the tree with its path, so we can inspect each object
    for a freshness timestamp paired with a TTL in the SAME object."""
    if isinstance(obj, dict):
        yield path, obj
        for k, v in obj.items():
            yield from _walk_objects(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk_objects(v, f"{path}[{i}]")


def _object_ttl(obj):
    for f in TTL_FIELDS:
        if isinstance(obj.get(f), (int, float)) and obj[f] > 0:
            return int(obj[f]), f
    vt = obj.get("velocity_tier")
    if isinstance(vt, str) and vt.lower() in VELOCITY_DEFAULT_TTL:
        return VELOCITY_DEFAULT_TTL[vt.lower()], f"velocity:{vt.lower()}"
    return None, None


def check_staleness(data, rel, now, default_ttl):
    """Flag objects whose freshness timestamp exceeds its TTL."""
    out = []
    for path, obj in _walk_objects(data):
        if not isinstance(obj, dict):
            continue
        ts_field = next((f for f in FRESHNESS_TS if f in obj), None)
        if not ts_field:
            continue
        dt = _parse_date(obj.get(ts_field))
        if not dt:
            continue
        age = (now - dt).days
        ttl, ttl_src = _object_ttl(obj)
        if ttl is None:
            ttl, ttl_src = default_ttl, "default"
        if age > ttl:
            out.append({
                "file": rel, "path": path, "field": ts_field,
                "age_days": age, "ttl_days": ttl, "ttl_from": ttl_src,
            })
    return out


def collect_spectrum_cells(brand_dir):
    """Cell ids declared in the brand's spectrum, if any. Empty set if none."""
    cells = set()
    for sp in list(brand_dir.glob("spectrum.json")) + list(brand_dir.glob("**/spectrum.json")):
        try:
            data = json.loads(sp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for _, obj in _walk_objects(data):
            if isinstance(obj, dict) and isinstance(obj.get("cell_id"), str):
                cells.add(obj["cell_id"])
    return cells


def _find_cell_ref(angle):
    for _, obj in _walk_objects(angle):
        if isinstance(obj, dict) and isinstance(obj.get("spectrum_cell_ref"), str):
            return obj["spectrum_cell_ref"]
    return None


def check_coherence(brand_dir):
    """Flag angles whose spectrum_cell_ref dangles. Skipped if no spectrum exists
    (cannot check a reference against an absent target without false alarms)."""
    cells = collect_spectrum_cells(brand_dir)
    if not cells:
        return [], False  # no spectrum populated, coherence check not applicable
    out = []
    for af in brand_dir.glob("angles/*.json"):
        try:
            angle = json.loads(af.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        ref = _find_cell_ref(angle)
        if ref and ref not in cells:
            out.append({"file": str(af.name), "spectrum_cell_ref": ref,
                        "reason": "points at a spectrum cell that does not exist"})
    return out, True


def audit_brand(brand_dir, now, default_ttl):
    stale = []
    for jf in brand_dir.glob("**/*.json"):
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        rel = str(jf.relative_to(brand_dir))
        stale.extend(check_staleness(data, rel, now, default_ttl))
    dangling, coherence_ran = check_coherence(brand_dir)
    return {"brand": brand_dir.name, "stale": stale, "dangling": dangling,
            "coherence_ran": coherence_ran}


def main():
    ap = argparse.ArgumentParser(description="Freshness + coherence audit of the encoded substrate")
    ap.add_argument("--root", default=".", help="workspace-template root")
    ap.add_argument("--brand", default=None, help="restrict to one brand slug")
    ap.add_argument("--default-ttl-days", type=int, default=180,
                    help="staleness threshold when no TTL/velocity is declared")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any stale or dangling item")
    args = ap.parse_args()

    brands_root = Path(args.root) / "brands"
    if not brands_root.is_dir():
        print(f"no brands/ under {args.root}", file=sys.stderr)
        return 0  # fail-open

    now = datetime.now(timezone.utc)
    results = []
    for bd in sorted(brands_root.iterdir()):
        if not bd.is_dir() or bd.name.startswith("_ARCHIVE"):
            continue
        if bd.name.startswith("_"):
            continue  # _EXAMPLE / _TEMPLATE are not runtime brands
        if args.brand and bd.name != args.brand:
            continue
        results.append(audit_brand(bd, now, args.default_ttl_days))

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        total = 0
        for r in results:
            n = len(r["stale"]) + len(r["dangling"])
            total += n
            coh = "ran" if r["coherence_ran"] else "skipped (no spectrum)"
            print(f"SUBSTRATE AUDIT · {r['brand']}  ·  stale={len(r['stale'])}  "
                  f"dangling={len(r['dangling'])}  (coherence {coh})")
            for s in r["stale"]:
                print(f"  stale   {s['file']} {s['path']} · {s['field']} is {s['age_days']}d old "
                      f"(ttl {s['ttl_days']}d, {s['ttl_from']})")
            for d in r["dangling"]:
                print(f"  dangle  {d['file']} · spectrum_cell_ref {d['spectrum_cell_ref']!r} {d['reason']}")
        if not results:
            print("no runtime brands to audit (only _EXAMPLE/_TEMPLATE).")
        else:
            print(f"\ntotal advisory items: {total}. Advisory only, nothing blocked.")

    flagged = sum(len(r["stale"]) + len(r["dangling"]) for r in results)
    return 1 if (args.strict and flagged) else 0


if __name__ == "__main__":
    sys.exit(main())
