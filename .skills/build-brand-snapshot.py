#!/usr/bin/env python3
"""
Builds brands/{slug}/_snapshot.md from a brand's JSON files.

The snapshot is a 1-2KB plaintext digest the agent reads at session start
instead of reading brand.json + every product + every audience + offers +
strategy separately. Cache-friendly, compose-free.

Usage:
    python3 .skills/build-brand-snapshot.py {brand_slug}
    python3 .skills/build-brand-snapshot.py --all

Run from workspace-template root.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
BRANDS = ROOT / "brands"


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def short(s, n=120):
    if not s:
        return " · "
    s = str(s).replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def unwrap(value):
    """Return _value if value is a {_value, _proposed, ...} wrapper (legacy
    proposed-on-scalar artifact from <v2.6.6), otherwise return value unchanged."""
    if isinstance(value, dict) and "_value" in value and "_proposed" in value:
        return value["_value"]
    return value


def unwrap_list(value):
    """Coerce any input into a list. Handles wrapped arrays, None, and dict
    fallback (returns []) so callers can always slice safely."""
    value = unwrap(value)
    if isinstance(value, list):
        return value
    return []


def build_snapshot(brand_dir):
    slug = brand_dir.name
    brand = load_json(brand_dir / "brand.json") or {}
    strategy = load_json(brand_dir / "strategy.json") or {}

    lines = [f"# {slug} · snapshot", ""]

    # Identity
    identity = unwrap(brand.get("identity", {})) or {}
    lines.append("## Identity")
    lines.append(f"- Name: {short(unwrap(identity.get('name')) or unwrap(identity.get('brand_name')))}")
    lines.append(f"- Tagline: {short(unwrap(identity.get('tagline')) or unwrap(identity.get('positioning_statement')))}")
    lines.append(f"- Sector: {short(unwrap(identity.get('sector')) or unwrap(brand.get('sector')))}")
    lines.append(f"- Language: {short(unwrap(identity.get('language')))}")
    tone = unwrap(brand.get("tone_of_voice")) or unwrap(brand.get("voice")) or {}
    if isinstance(tone, dict) and tone:
        lines.append(f"- Tone essentials: {short(unwrap(tone.get('essence')) or unwrap(tone.get('register')) or unwrap(tone.get('signature')))}")
    lines.append("")

    # Products
    products_dir = brand_dir / "products"
    products = []
    if products_dir.exists():
        for p in sorted(products_dir.iterdir()):
            if p.is_dir() and not p.name.startswith("_"):
                spec = load_json(p / "spec.json") or {}
                pid = unwrap(spec.get("identity", {})) or {}
                pricing = unwrap(spec.get("pricing", {})) or {}
                products.append({
                    "slug": p.name,
                    "name": unwrap(pid.get("product_name")) or unwrap(pid.get("name")) or p.name,
                    "price": unwrap(pricing.get("price_display")) or unwrap(pricing.get("base_price")) or unwrap(pricing.get("price")),
                    "hero": bool(unwrap(pid.get("hero")) or unwrap(pid.get("is_hero"))),
                    "use_cases": unwrap_list(spec.get("use_cases")) or [],
                })
    lines.append(f"## Products ({len(products)})")
    for p in products[:10]:
        hero_mark = " ★" if p["hero"] else ""
        price = f" · {p['price']}" if p["price"] else ""
        lines.append(f"- {p['slug']}{hero_mark}{price}")
    if len(products) > 10:
        lines.append(f"- … +{len(products) - 10} more")
    lines.append("")

    # Use cases (Spectre · le nœud stratégique Mc → U)
    all_use_cases = [uc for p in products for uc in p["use_cases"] if isinstance(uc, dict)]
    if all_use_cases:
        by_status = {}
        for uc in all_use_cases:
            st = unwrap(uc.get("status")) or "?"
            by_status[st] = by_status.get(st, 0) + 1
        lines.append(f"## Cas d'usage ({len(all_use_cases)})")
        lines.append("- Par statut: " + ", ".join(f"{k}:{v}" for k, v in sorted(by_status.items())))
        labels = [short(unwrap(uc.get("label")), 50) for uc in all_use_cases[:8] if unwrap(uc.get("label"))]
        if labels:
            lines.append("- " + " · ".join(labels))
        lines.append("")

    # Audiences
    audiences_dir = brand_dir / "audiences"
    audiences = []
    if audiences_dir.exists():
        for a in sorted(audiences_dir.iterdir()):
            if a.is_dir() and not a.name.startswith("_"):
                profile = load_json(a / "profile.json") or {}
                pid = unwrap(profile.get("identity", {})) or {}
                pmeta = unwrap(profile.get("meta", {})) or {}
                psychology = unwrap(profile.get("psychology", {})) or {}
                pains = unwrap_list(psychology.get("pain_points")) or unwrap_list(profile.get("pain_points"))
                label = unwrap(pmeta.get("name")) or unwrap(pid.get("label")) or unwrap(pid.get("name")) or a.name
                audiences.append({
                    "slug": a.name,
                    "label": label if isinstance(label, str) else a.name,
                    "primary": (unwrap(pmeta.get("audience_type")) == "primary") or bool(unwrap(pid.get("primary")) or unwrap(pid.get("is_primary"))),
                    "pains": [
                        (unwrap(p.get("label")) or unwrap(p.get("formulation")) or "")
                        if isinstance(p, dict) else str(p)
                        for p in pains[:2]
                    ],
                })
    lines.append(f"## Audiences ({len(audiences)})")
    for a in audiences[:6]:
        primary_mark = " ★" if a["primary"] else ""
        lines.append(f"- {a['slug']}{primary_mark}: {short(a['label'], 60)}")
        if a["pains"]:
            lines.append(f"  Top pains: {', '.join(short(p, 40) for p in a['pains'])}")
    if len(audiences) > 6:
        lines.append(f"- … +{len(audiences) - 6} more")
    lines.append("")

    # Spectre (la carte du terrain produit × marché · M1)
    spectrum = load_json(brand_dir / "spectrum.json")
    if spectrum:
        cells = unwrap_list(spectrum.get("cells")) or []
        cov, blank_qual = {}, {}
        core = unwrap(spectrum.get("core_cell_ref"))  # canonical top-level field
        for c in cells:
            if not isinstance(c, dict):
                continue
            cs = unwrap(c.get("coverage_self")) or "?"
            cov[cs] = cov.get(cs, 0) + 1
            if cs == "blank":
                bq = unwrap(c.get("blank_qualification")) or "unqualified"
                blank_qual[bq] = blank_qual.get(bq, 0) + 1
            if not core and c.get("is_core"):  # fallback if core_cell_ref absent
                core = unwrap(c.get("cell_id"))
        lines.append(f"## Spectre ({len(cells)} cellules)")
        if cov:
            lines.append("- Couverture: " + ", ".join(f"{k}:{v}" for k, v in sorted(cov.items())))
        if blank_qual:
            lines.append("- Zones blanches: " + ", ".join(f"{k}:{v}" for k, v in sorted(blank_qual.items())))
        if core:
            lines.append(f"- Cœur de cible: {core}")
        meta_bits = []
        stage = unwrap(spectrum.get("stage_at_build"))
        refreshed = unwrap(spectrum.get("refreshed_at"))
        if stage:
            meta_bits.append(f"stade {stage}")
        if refreshed:
            meta_bits.append(f"refresh {short(refreshed, 19)}")
        if meta_bits:
            lines.append("- " + " · ".join(meta_bits))
        lines.append("")

    # Offers
    offers_count = 0
    offer_types = {}
    if products_dir.exists():
        for p in products_dir.iterdir():
            if p.is_dir() and not p.name.startswith("_"):
                offers_doc = load_json(p / "offers.json") or {}
                # Support both v1.x (flat offers[]) and v2.0 (offer_groups[].offers[])
                offer_groups = offers_doc.get("offer_groups", []) if isinstance(offers_doc, dict) else []
                for group in offer_groups:
                    if isinstance(group, dict):
                        for off in group.get("offers", []):
                            if isinstance(off, dict) and off.get("active", True) is not False:
                                offers_count += 1
                                t = off.get("type") or "other"
                                offer_types[t] = offer_types.get(t, 0) + 1
    lines.append(f"## Offers active: {offers_count}")
    if offer_types:
        breakdown = ", ".join(f"{k}:{v}" for k, v in sorted(offer_types.items()))
        lines.append(f"- By type: {breakdown}")
    lines.append("")

    # Strategy
    if strategy:
        focus = strategy.get("current_focus") or strategy.get("monthly_focus") or (strategy.get("goals", {}) or {}).get("current")
        lines.append("## Strategy")
        lines.append(f"- Current focus: {short(focus)}")
        if strategy.get("targets"):
            t = strategy["targets"] if isinstance(strategy["targets"], str) else short(json.dumps(strategy["targets"]), 100)
            lines.append(f"- Targets: {t}")
        lines.append("")

    # Pending / status
    status = load_json(brand_dir / "status.json") or {}
    if status:
        lines.append("## Status")
        lines.append(f"- Wedge complete: {status.get('wedge_complete', False)}")
        level = status.get("context_level") or status.get("level")
        if level:
            lines.append(f"- Context level: {level}")
        lines.append("")

    lines.append(f"_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}_")
    lines.append(f"_Refresh: python3 .skills/build-brand-snapshot.py {slug}_")

    (brand_dir / "_snapshot.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 .skills/build-brand-snapshot.py {slug} | --all", file=sys.stderr)
        sys.exit(1)
    arg = sys.argv[1]
    if arg == "--all":
        for d in sorted(BRANDS.iterdir()):
            if d.is_dir() and not d.name.startswith("_"):
                n = build_snapshot(d)
                print(f"{d.name}: {n} lines")
    else:
        d = BRANDS / arg
        if not d.exists():
            print(f"brand not found: {d}", file=sys.stderr)
            sys.exit(1)
        n = build_snapshot(d)
        print(f"{arg}: {n} lines")


if __name__ == "__main__":
    main()
