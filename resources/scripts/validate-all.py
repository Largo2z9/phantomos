#!/usr/bin/env python3
"""
validate-all.py — Global workspace cleanliness check.

Scans every brand instance under workspace-template/brands/ (excluding _ARCHIVE)
and runs a battery of checks:

  1. JSON parse
  2. Schema validation (brand/spec/offers/profile)
  3. _template_version stamping drift
  4. Cross-file coherence (product_slug, brand_slug, orphan audiences)
  5. Duplicate IDs (offer_id, product slugs)
  6. Orphan files (JSON not matching any schema)

Output: JSON report to stdout + human-readable summary.

Usage:
    python3 validate-all.py [--root PATH] [--strict] [--include-archive]

Requires Python 3.9+ and jsonschema. Schemas under resources/schemas/ use
relative $ref (e.g. "_shared/validation-status.json"): on jsonschema >= 4.18
they are resolved through a referencing.Registry built from the schemas dir,
on older versions through a file:// RefResolver. Both paths are handled below.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: jsonschema not installed. Run: pip install jsonschema --break-system-packages")
    sys.exit(2)

try:
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
    HAVE_REFERENCING = True
except ImportError:
    HAVE_REFERENCING = False


# ---------- Config ----------

SCHEMA_FILES = {
    "brand": "resources/schemas/brand.schema.json",
    "spec": "resources/schemas/spec.schema.json",
    "offers": "resources/schemas/offer.schema.json",
    "profile": "resources/schemas/profile.schema.json",
}

# Expected versions read dynamically from _TEMPLATE at load time.
# Each entity evolves at its own pace — spec/offers bumped to 1.8,
# brand still 1.5, profile still 1.2 (legitimate, not drift).
EXPECTED_VERSIONS = {}

# Instance folders explicitly excluded from validation by default.
# _ARCHIVE is a bucket of retired pilots, not an instance.
# _EXAMPLE is the filled demo, scanned but flagged separately.
# _TEMPLATE is the skeleton, always scanned.
DEFAULT_EXCLUDED_INSTANCES = {"_ARCHIVE"}

SEVERITY = {
    "parse_error": "CRITICAL",
    "schema_error": "HIGH",
    "orphan_file": "MED",
    "version_drift": "MED",
    "slug_mismatch": "HIGH",
    "duplicate_id": "HIGH",
    "missing_required_file": "HIGH",

    # Semantic (deep) checks
    "unknown_ref_pain": "MED",
    "unknown_ref_benefit": "MED",
    "audience_folder_not_indexed": "LOW",
    "audience_index_no_folder": "MED",
    "product_folder_not_indexed": "MED",
    "product_enriched_no_folder": "HIGH",
    "product_index_enriched_mismatch": "LOW",
    "audience_product_id_unknown": "MED",
    "audience_parent_slug_unknown": "MED",
    "offers_cycle": "HIGH",
    "offers_dangling_requires": "MED",
    "mechanism_other_saturation": "MED",
}


# ---------- Helpers ----------

def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"{e.msg} at line {e.lineno} col {e.colno}"
    except Exception as e:
        return None, str(e)


def _build_ref_support(root: Path):
    """Make relative $ref ("_shared/x.json") resolvable across jsonschema versions.

    Returns a dict of kwargs to pass to Draft202012Validator(...).
    """
    schemas_dir = root / "resources/schemas"
    if HAVE_REFERENCING:
        resources = []
        for p in schemas_dir.rglob("*.json"):
            data, err = load_json(p)
            if err:
                continue
            uri = p.relative_to(schemas_dir).as_posix()
            resources.append((uri, Resource.from_contents(data, default_specification=DRAFT202012)))
        return {"registry": Registry().with_resources(resources)}
    # Legacy jsonschema (< 4.18): RefResolver resolves file:// URIs relative to schemas dir.
    from jsonschema import RefResolver  # deprecated upstream, kept as fallback only
    return {"resolver": RefResolver(base_uri=schemas_dir.as_uri() + "/", referrer={})}


def load_schemas(root: Path):
    schemas = {}
    ref_kwargs = _build_ref_support(root)
    for key, rel in SCHEMA_FILES.items():
        path = root / rel
        data, err = load_json(path)
        if err:
            print(f"FATAL: cannot load schema {key}: {err}", file=sys.stderr)
            sys.exit(2)
        Draft202012Validator.check_schema(data)
        schemas[key] = Draft202012Validator(data, **ref_kwargs)
    return schemas


def load_expected_versions(root: Path):
    """Read _version from _TEMPLATE files — source of truth for per-entity version."""
    template_files = {
        "brand": root / "brands/_TEMPLATE/brand.json",
        "spec": root / "brands/_TEMPLATE/products/_example/spec.json",
        "offers": root / "brands/_TEMPLATE/products/_example/offers.json",
        "profile": root / "brands/_TEMPLATE/audiences/_example/profile.json",
    }
    expected = {}
    for key, path in template_files.items():
        data, err = load_json(path)
        if err or not data:
            print(f"WARN: cannot read {path} for version check", file=sys.stderr)
            continue
        expected[key] = str(data.get("_version") or data.get("_template_version") or "?")
    return expected


def _deep_merge_into(base: dict, override: dict) -> None:
    """Mutate `base` with `override`. Dict→dict = recurse, else replace."""
    for key, val in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(val, dict):
            _deep_merge_into(base[key], val)
        else:
            base[key] = val


def merge_offers_shared(doc: dict) -> dict:
    """Resolve shared→offer merge for v2.0 offers.json docs.

    Returns a NEW document with offer_groups[*].offers[*] having merged attributes.
    Merge rules (per schema v2.0 description):
      1. Nested objects merge deep. Offer wins on key collisions within the object.
      2. Arrays REPLACE entirely (no concat).
      3. Scalars and booleans override explicitly when set at offer level.
    Keys absent on the offer are inherited from shared.
    Docs that are not v2.0 (no offer_groups) are returned unchanged.
    """
    if "offer_groups" not in doc:
        return doc
    merged = json.loads(json.dumps(doc))  # deep copy
    for group in merged.get("offer_groups", []) or []:
        shared = group.get("shared", {}) or {}
        for offer in group.get("offers", []) or []:
            for key, shared_val in shared.items():
                if key.startswith("$"):
                    continue
                if key not in offer:
                    offer[key] = json.loads(json.dumps(shared_val))
                elif isinstance(shared_val, dict) and isinstance(offer[key], dict):
                    base = json.loads(json.dumps(shared_val))
                    _deep_merge_into(base, offer[key])
                    offer[key] = base
                # scalars and arrays at offer level always win
    return merged


def detect_offers_cycle(doc: dict) -> tuple[list[str] | None, list[str]]:
    """DFS cycle detection on requires_offer_id graph.

    Returns (cycle_path | None, dangling_refs). cycle_path is a list of offer_ids
    forming the cycle (first == last). dangling_refs lists offer_ids pointing to
    unknown targets.
    """
    graph: dict[str, str | None] = {}
    for group in doc.get("offer_groups", []) or []:
        for offer in group.get("offers", []) or []:
            oid = offer.get("offer_id")
            if not oid:
                continue
            graph[oid] = offer.get("requires_offer_id")

    # Dangling refs (pointing outside the known set — may be cross-product, flag as warning)
    dangling = []
    for src, tgt in graph.items():
        if tgt and tgt not in graph:
            dangling.append(f"{src} → {tgt}")

    # DFS cycle detection
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {k: WHITE for k in graph}
    parent: dict[str, str | None] = {k: None for k in graph}

    def visit(node: str) -> list[str] | None:
        color[node] = GRAY
        nxt = graph.get(node)
        if nxt and nxt in graph:
            if color[nxt] == GRAY:
                # Build cycle path
                cycle = [nxt, node]
                cur = parent[node]
                while cur and cur != nxt:
                    cycle.append(cur)
                    cur = parent[cur]
                cycle.append(nxt)
                cycle.reverse()
                return cycle
            if color[nxt] == WHITE:
                parent[nxt] = node
                result = visit(nxt)
                if result:
                    return result
        color[node] = BLACK
        return None

    for node in graph:
        if color[node] == WHITE:
            cycle = visit(node)
            if cycle:
                return cycle, dangling
    return None, dangling


def classify_file(path: Path) -> str | None:
    """Return schema key ('brand'|'spec'|'offers'|'profile') or None if orphan."""
    name = path.name
    parts = path.parts
    if name == "brand.json":
        return "brand"
    if name == "spec.json" and "products" in parts:
        return "spec"
    if name == "offers.json" and "products" in parts:
        return "offers"
    if name == "profile.json" and "audiences" in parts:
        return "profile"
    return None


# ---------- Checks ----------

def check_instance(brand_dir: Path, schemas, expected_versions, report):
    """Run all checks for a single brand instance."""
    brand_slug = brand_dir.name
    issues = []

    # 1. brand.json required
    brand_path = brand_dir / "brand.json"
    if not brand_path.exists():
        issues.append({
            "type": "missing_required_file",
            "severity": SEVERITY["missing_required_file"],
            "file": str(brand_path.relative_to(brand_dir.parent.parent.parent)),
            "msg": "brand.json missing at instance root",
        })
        counts = defaultdict(int)
        for i in issues:
            counts[i["severity"]] += 1
        report["instances"][brand_slug] = {"issues": issues, "counts": dict(counts)}
        return

    brand_data, err = load_json(brand_path)
    if err:
        issues.append({
            "type": "parse_error",
            "severity": SEVERITY["parse_error"],
            "file": str(brand_path),
            "msg": err,
        })

    declared_brand_slug = (brand_data or {}).get("meta", {}).get("slug") if brand_data else None

    # Collect index data from brand.json for semantic checks
    products_index = (brand_data or {}).get("products_index", []) or []
    audiences_index = (brand_data or {}).get("audiences_index", []) or []
    indexed_product_slugs = {p.get("slug"): p for p in products_index if p.get("slug")}
    indexed_audience_slugs = {a.get("slug"): a for a in audiences_index if a.get("slug")}

    # 2. Walk all json files in instance
    products_seen = set()  # folder slugs
    offer_ids = defaultdict(list)
    audiences_declared = set()  # folder slugs
    product_slugs_in_offers = set()

    # Semantic collection (populated during walk, checked after)
    specs_by_product = {}   # product_slug -> {"problem_ids": set, "benefit_ids": set}
    profiles_by_audience = {}  # audience_slug -> {"pain_refs": set, "benefit_refs": set, "product_id": str|None, "parent_slug": str|None}

    for jf in brand_dir.rglob("*.json"):
        rel = jf.relative_to(brand_dir.parent.parent.parent)
        kind = classify_file(jf)

        data, err = load_json(jf)
        if err:
            issues.append({
                "type": "parse_error",
                "severity": SEVERITY["parse_error"],
                "file": str(rel),
                "msg": err,
            })
            continue

        if kind is None:
            # orphan non-core file (config, strategy, status, learnings, etc)
            # skip silently — only flag if in products/ or audiences/ with wrong name
            if "products" in jf.parts or "audiences" in jf.parts:
                # Canonical sub-collections (v2.63+ pain/objection collections, frictions,
                # production namespaces) are first-class citizens, never orphans.
                canonical_subdirs = {"pain_points", "objections", "frictions", "sources",
                                     "creatives", "competitive-intel", "asset-library", "extensions"}
                if canonical_subdirs & set(jf.parts):
                    continue
                expected_names = {"spec.json", "offers.json", "profile.json", "visual_identity.json"}
                if jf.name not in expected_names:
                    issues.append({
                        "type": "orphan_file",
                        "severity": SEVERITY["orphan_file"],
                        "file": str(rel),
                        "msg": f"unexpected file in products/ or audiences/: {jf.name}",
                    })
            continue

        # v2.0 offers: resolve shared→offer merge BEFORE schema validation.
        # Merge rules live in merge_offers_shared(). See D#215.
        data_for_validation = data
        if kind == "offers" and "offer_groups" in data:
            data_for_validation = merge_offers_shared(data)

        # Schema validation
        validator = schemas[kind]
        errs = list(validator.iter_errors(data_for_validation))
        for e in errs[:5]:  # cap at 5 per file
            issues.append({
                "type": "schema_error",
                "severity": SEVERITY["schema_error"],
                "file": str(rel),
                "path": ".".join(str(p) for p in e.absolute_path),
                "msg": e.message[:200],
            })
        if len(errs) > 5:
            issues.append({
                "type": "schema_error",
                "severity": SEVERITY["schema_error"],
                "file": str(rel),
                "msg": f"... and {len(errs) - 5} more schema errors",
            })

        # Version drift — per-entity, read from _TEMPLATE
        tv = data.get("_template_version") or data.get("_version")
        expected = expected_versions.get(kind)
        if tv and expected and str(tv) != expected:
            issues.append({
                "type": "version_drift",
                "severity": SEVERITY["version_drift"],
                "file": str(rel),
                "msg": f"_version={tv}, expected {expected} (per _TEMPLATE)",
            })

        # Cross-file coherence
        # Skeleton folders starting with '_' (e.g. _example) use a convention
        # prefix and cannot match the slug pattern ^[a-z0-9-]+$ — skip slug check.
        if kind == "spec":
            parent_slug = jf.parent.name
            is_skeleton = parent_slug.startswith("_")
            meta_slug = data.get("meta", {}).get("product_slug") or data.get("meta", {}).get("slug")
            if not is_skeleton and meta_slug and meta_slug != parent_slug:
                issues.append({
                    "type": "slug_mismatch",
                    "severity": SEVERITY["slug_mismatch"],
                    "file": str(rel),
                    "msg": f"meta.slug='{meta_slug}' ≠ folder='{parent_slug}'",
                })
            products_seen.add(parent_slug)

            # brand_slug coherence
            meta_brand = data.get("meta", {}).get("brand_slug")
            if meta_brand and declared_brand_slug and meta_brand != declared_brand_slug:
                issues.append({
                    "type": "slug_mismatch",
                    "severity": SEVERITY["slug_mismatch"],
                    "file": str(rel),
                    "msg": f"brand_slug='{meta_brand}' ≠ brand.json slug='{declared_brand_slug}'",
                })

            # Collect problem/benefit IDs for semantic cross-ref
            problem_ids = set()
            for p in data.get("problems_solved", []) or []:
                pid = p.get("problem_id")
                if pid:
                    problem_ids.add(pid)
            benefit_ids = set()
            for b in data.get("benefits", []) or []:
                bid = b.get("benefit_id")
                if bid:
                    benefit_ids.add(bid)
            specs_by_product[parent_slug] = {
                "problem_ids": problem_ids,
                "benefit_ids": benefit_ids,
                "mech_modes": [m.get("mode_of_action") for m in data.get("mechanisms", []) or [] if m.get("mode_of_action")],
                "file": str(rel),
            }

        if kind == "offers":
            parent_slug = jf.parent.name
            is_skeleton = parent_slug.startswith("_")
            meta_slug = data.get("meta", {}).get("product_slug")
            if meta_slug:
                product_slugs_in_offers.add(meta_slug)
                if not is_skeleton and meta_slug != parent_slug:
                    issues.append({
                        "type": "slug_mismatch",
                        "severity": SEVERITY["slug_mismatch"],
                        "file": str(rel),
                        "msg": f"meta.product_slug='{meta_slug}' ≠ folder='{parent_slug}'",
                    })

            # v2.0: offers live in offer_groups[*].offers[]. v1.x fallback: top-level offers[].
            all_offers_in_doc = []
            if "offer_groups" in data:
                for group in data.get("offer_groups", []) or []:
                    for offer in group.get("offers", []) or []:
                        all_offers_in_doc.append(offer)
            else:
                all_offers_in_doc = data.get("offers", []) or []

            # duplicate offer_ids (post-merge shape doesn't matter — offer_id is never in shared)
            for offer in all_offers_in_doc:
                oid = offer.get("offer_id")
                if oid:
                    offer_ids[oid].append(str(rel))

            # 9th semantic check: requires_offer_id cycle detection + dangling refs
            if "offer_groups" in data:
                cycle, dangling = detect_offers_cycle(data)
                if cycle:
                    issues.append({
                        "type": "offers_cycle",
                        "severity": SEVERITY["offers_cycle"],
                        "file": str(rel),
                        "msg": f"requires_offer_id cycle: {' → '.join(cycle)}",
                    })
                for dr in dangling:
                    issues.append({
                        "type": "offers_dangling_requires",
                        "severity": SEVERITY["offers_dangling_requires"],
                        "file": str(rel),
                        "msg": f"requires_offer_id references unknown offer: {dr}",
                    })

        if kind == "profile":
            audience_slug = jf.parent.name
            audiences_declared.add(audience_slug)
            pain_refs = set()
            benefit_refs = set()
            # Legacy instances may carry pre-v2.0 string entries here; the
            # jsonschema pass already reports the type mismatch — never crash on it.
            for p in data.get("pain_points", []) or []:
                if isinstance(p, dict) and p.get("ref"):
                    pain_refs.add(p["ref"])
            for b in data.get("benefits", []) or []:
                if isinstance(b, dict) and b.get("ref"):
                    benefit_refs.add(b["ref"])
            profiles_by_audience[audience_slug] = {
                "pain_refs": pain_refs,
                "benefit_refs": benefit_refs,
                "product_id": data.get("meta", {}).get("product_id"),
                "parent_slug": data.get("meta", {}).get("parent_slug"),
                "file": str(rel),
            }

    # Duplicate offer_ids
    for oid, locs in offer_ids.items():
        if len(locs) > 1:
            issues.append({
                "type": "duplicate_id",
                "severity": SEVERITY["duplicate_id"],
                "msg": f"offer_id '{oid}' duplicated in: {', '.join(locs)}",
            })

    # ============================================================
    # SEMANTIC (DEEP) CHECKS — cross-references and orphans
    # ============================================================

    # Skip semantic checks entirely for skeleton instances (_TEMPLATE).
    # They contain placeholder data with intentional convention mismatches
    # (e.g. _example folder vs example-audience slug) that aren't real gaps.
    if brand_slug.startswith("_") and brand_slug == "_TEMPLATE":
        counts = defaultdict(int)
        for i in issues:
            counts[i["severity"]] += 1
        report["instances"][brand_slug] = {
            "issues": issues,
            "counts": dict(counts),
            "products_count": len(products_seen),
            "audiences_count": len(audiences_declared),
        }
        return

    # Union of all problem_ids and benefit_ids across specs of this brand.
    # Profile refs can match any product's problem/benefit (brand-level audience
    # or multi-product resonance).
    all_problem_ids = set()
    all_benefit_ids = set()
    for ps, meta in specs_by_product.items():
        all_problem_ids |= meta["problem_ids"]
        all_benefit_ids |= meta["benefit_ids"]

    # Skeleton folders (_TEMPLATE/_example etc.) have empty refs on purpose;
    # skip dangling-ref checks for them.
    def _is_skeleton_audience(slug): return slug.startswith("_")

    # 1. Dangling pain_point.ref → problems_solved.problem_id
    for aud_slug, prof in profiles_by_audience.items():
        if _is_skeleton_audience(aud_slug):
            continue
        for ref in prof["pain_refs"]:
            if not ref or ref in all_problem_ids:
                continue
            issues.append({
                "type": "unknown_ref_pain",
                "severity": SEVERITY["unknown_ref_pain"],
                "file": prof["file"],
                "msg": f"pain_points[].ref='{ref}' not found in any spec.problems_solved[].problem_id",
            })

    # 2. Dangling benefits.ref → spec.benefits[].benefit_id
    for aud_slug, prof in profiles_by_audience.items():
        if _is_skeleton_audience(aud_slug):
            continue
        for ref in prof["benefit_refs"]:
            if not ref or ref in all_benefit_ids:
                continue
            issues.append({
                "type": "unknown_ref_benefit",
                "severity": SEVERITY["unknown_ref_benefit"],
                "file": prof["file"],
                "msg": f"benefits[].ref='{ref}' not found in any spec.benefits[].benefit_id",
            })

    # 3. Audience folder exists but not in brand.audiences_index
    for aud_slug in audiences_declared:
        if _is_skeleton_audience(aud_slug):
            continue
        if aud_slug not in indexed_audience_slugs:
            issues.append({
                "type": "audience_folder_not_indexed",
                "severity": SEVERITY["audience_folder_not_indexed"],
                "msg": f"audience folder '{aud_slug}/' exists but not in brand.audiences_index",
            })

    # 4. Audience declared in index but no folder
    for aud_slug in indexed_audience_slugs:
        if not aud_slug or _is_skeleton_audience(aud_slug):
            continue
        if aud_slug not in audiences_declared:
            issues.append({
                "type": "audience_index_no_folder",
                "severity": SEVERITY["audience_index_no_folder"],
                "msg": f"audiences_index entry '{aud_slug}' has no folder at audiences/{aud_slug}/",
            })

    # 5. Product folder exists but not in products_index
    for prod_slug in products_seen:
        if prod_slug.startswith("_"):
            continue
        if prod_slug not in indexed_product_slugs:
            issues.append({
                "type": "product_folder_not_indexed",
                "severity": SEVERITY["product_folder_not_indexed"],
                "msg": f"product folder '{prod_slug}/' exists but not in brand.products_index",
            })

    # 6. Product indexed as enriched:true but no folder / missing spec.json
    for prod_slug, idx_entry in indexed_product_slugs.items():
        if not prod_slug or prod_slug.startswith("_"):
            continue
        enriched = idx_entry.get("enriched", False)
        folder_exists = prod_slug in products_seen
        if enriched and not folder_exists:
            issues.append({
                "type": "product_enriched_no_folder",
                "severity": SEVERITY["product_enriched_no_folder"],
                "msg": f"products_index[{prod_slug}].enriched=true but no folder at products/{prod_slug}/",
            })
        if (not enriched) and folder_exists:
            issues.append({
                "type": "product_index_enriched_mismatch",
                "severity": SEVERITY["product_index_enriched_mismatch"],
                "msg": f"products_index[{prod_slug}].enriched=false but folder exists — flip to true or delete folder",
            })

    # 7. audience.meta.product_id must reference a known product slug
    for aud_slug, prof in profiles_by_audience.items():
        if _is_skeleton_audience(aud_slug):
            continue
        pid = prof.get("product_id")
        if pid and pid not in indexed_product_slugs and pid not in products_seen:
            issues.append({
                "type": "audience_product_id_unknown",
                "severity": SEVERITY["audience_product_id_unknown"],
                "file": prof["file"],
                "msg": f"meta.product_id='{pid}' does not match any known product slug",
            })

    # 8. audience.meta.parent_slug must reference a known audience slug
    for aud_slug, prof in profiles_by_audience.items():
        if _is_skeleton_audience(aud_slug):
            continue
        parent = prof.get("parent_slug")
        if parent and parent not in indexed_audience_slugs and parent not in audiences_declared:
            issues.append({
                "type": "audience_parent_slug_unknown",
                "severity": SEVERITY["audience_parent_slug_unknown"],
                "file": prof["file"],
                "msg": f"meta.parent_slug='{parent}' does not match any known audience",
            })

    # 9. mode_of_action 'other' saturation — signals a missing family in the
    # registry, not an unclassifiable product. SSOT: resources/registries/mechanism-families.md
    all_modes = []
    for ps, meta in specs_by_product.items():
        all_modes += meta.get("mech_modes", [])
    if len(all_modes) >= 3:
        n_other = all_modes.count("other")
        if n_other / len(all_modes) > 0.30:
            issues.append({
                "type": "mechanism_other_saturation",
                "severity": SEVERITY["mechanism_other_saturation"],
                "msg": f"mode_of_action='other' on {n_other}/{len(all_modes)} mechanisms (>30%) — a family is missing: promote it in resources/registries/mechanism-families.md instead of defaulting to 'other'",
            })

    # Count severity
    counts = defaultdict(int)
    for i in issues:
        counts[i["severity"]] += 1

    report["instances"][brand_slug] = {
        "issues": issues,
        "counts": dict(counts),
        "products_count": len(products_seen),
        "audiences_count": len(audiences_declared),
    }


# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="workspace-template root")
    ap.add_argument("--include-archive", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any HIGH+ issue")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    schemas = load_schemas(root)
    expected_versions = load_expected_versions(root)

    brands_dir = root / "brands"
    if not brands_dir.exists():
        print(f"FATAL: {brands_dir} not found", file=sys.stderr)
        sys.exit(2)

    report = {
        "root": str(root),
        "expected_versions": expected_versions,
        "instances": {},
    }

    for brand_dir in sorted(brands_dir.iterdir()):
        if not brand_dir.is_dir():
            continue
        # Skip explicitly excluded buckets (e.g. _ARCHIVE) unless forced
        if brand_dir.name in DEFAULT_EXCLUDED_INSTANCES and not args.include_archive:
            continue
        check_instance(brand_dir, schemas, expected_versions, report)

    # Global summary
    total = defaultdict(int)
    for inst in report["instances"].values():
        for sev, n in inst["counts"].items():
            total[sev] += n
    report["summary"] = dict(total)

    # ---- Human output ----
    print("=" * 70)
    print(f"WORKSPACE VALIDATION — {root.name}")
    print(f"Expected versions (from _TEMPLATE): {expected_versions}")
    print("=" * 70)
    print()

    for slug, data in report["instances"].items():
        counts = data["counts"]
        status = "OK " if not counts else "FAIL"
        flags = " ".join(f"{k}:{v}" for k, v in counts.items()) or "clean"
        print(f"[{status}] {slug:20s}  products:{data.get('products_count', 0):2d}  audiences:{data.get('audiences_count', 0):2d}  {flags}")

    print()
    print("-" * 70)
    print("GLOBAL SUMMARY")
    print("-" * 70)
    for sev in ["CRITICAL", "HIGH", "MED", "LOW"]:
        n = total.get(sev, 0)
        mark = "X" if n else "."
        print(f"  [{mark}] {sev:10s} {n}")
    print()

    # Top issues
    all_issues = []
    for slug, data in report["instances"].items():
        for i in data["issues"]:
            all_issues.append((slug, i))

    if all_issues:
        print("-" * 70)
        print("TOP ISSUES (first 30)")
        print("-" * 70)
        sev_order = {"CRITICAL": 0, "HIGH": 1, "MED": 2, "LOW": 3}
        all_issues.sort(key=lambda x: sev_order.get(x[1]["severity"], 9))
        for slug, i in all_issues[:30]:
            loc = i.get("file", "")
            path = f" :: {i['path']}" if i.get("path") else ""
            print(f"  [{i['severity']:8s}] {slug} / {loc}{path}")
            print(f"             {i['msg']}")
    print()

    # JSON report to file
    out = root / "_validation-report.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"Full report: {out}")

    if args.strict and (total.get("CRITICAL", 0) or total.get("HIGH", 0)):
        sys.exit(1)


if __name__ == "__main__":
    main()
