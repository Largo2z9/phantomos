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
    "style_other_saturation": "MED",
    "mecanique_other_saturation": "MED",
    "beat_type_other_saturation": "MED",

    # Spectre / fraîcheur post-hoc (D#518) · intégrité, jamais pré-validation (Master rule).
    # MED/LOW pour rester sous le gate dur (CRITICAL+HIGH==0) ; promouvoir en HIGH
    # seulement après avoir seedé _EXAMPLE avec la donnée conforme.
    "use_cases_no_speculative": "MED",
    "angle_spectrum_untraced": "MED",
    "angle_negative_untraced": "MED",
    "angle_negative_missing": "LOW",
    "naked_number_unsourced": "LOW",

    # Évaporation de profondeur (D#519) · le raisonnement narré qui n'atteint pas l'artefact.
    "use_cases_missing": "MED",
    "benefits_missing": "MED",
    "audience_profile_template_clone": "MED",
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

    # Saturation accumulators for A=B bridge tags (decomposition.json under competitive-intel/).
    # 'other' saturation on any of these signals a MISSING family in its registry,
    # not an unclassifiable ad. Same doctrine as mechanism_other_saturation (check 9).
    decomp_tags = {"style_id": [], "mecanique_id": [], "beat_type": []}

    # Spectre trace accumulators (D#518). angle back-refs + spectrum cell use_case_refs.
    # Both files are None-classified by classify_file, harvested in the walk like decomp_tags.
    angles_seen = []            # list of dicts (rel, use_case_ref, angle_id, negative_cell_ref, has_reframe, has_negative, is_skeleton)
    spectrum_use_case_refs = set()
    spectrum_cell_ids = set()   # cell_id de chaque cellule spectrum.json (trace negative.spectrum_cell_ref · D#523)

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

        # Saturation tag harvest — decomposition.json (reverse benchmark) carries the
        # A=B bridge enums style_id / mecanique_id / beat_type. classify_file returns
        # None for it, so collect here before the orphan branch.
        if jf.name == "decomposition.json" and "competitive-intel" in jf.parts:
            for s in (data.get("visual", {}) or {}).get("styles_observed", []) or []:
                if s.get("style_id"):
                    decomp_tags["style_id"].append(s["style_id"])
            mid = (data.get("mecanique", {}) or {}).get("mecanique_id")
            if mid:
                decomp_tags["mecanique_id"].append(mid)
            for b in (data.get("script", {}) or {}).get("body_arc", []) or []:
                if b.get("beat_type"):
                    decomp_tags["beat_type"].append(b["beat_type"])

        # Spectre trace harvest (D#518) · spectrum.json cells + angle back-refs.
        # classify_file returns None for both, so collect here before the orphan branch.
        if jf.name == "spectrum.json":
            for c in data.get("cells", []) or []:
                uc = c.get("use_case_ref")
                if uc:
                    spectrum_use_case_refs.add(uc)
                cid = c.get("cell_id")
                if cid:
                    spectrum_cell_ids.add(cid)
        if "angles" in jf.parts and (jf.name.startswith("ANG") or jf.name == "angle.json"):
            lineage = data.get("lineage", {}) or {}
            negative = data.get("negative", {}) or {}
            reframe = (data.get("formula", {}) or {}).get("reframe", {}) or {}
            angles_seen.append({
                "rel": str(rel),
                "use_case_ref": lineage.get("use_case_ref"),
                "angle_id": data.get("angle_id") or jf.stem,
                "negative_cell_ref": negative.get("spectrum_cell_ref"),
                "has_reframe": bool(reframe.get("summary") or reframe.get("perceptual_pivot")),
                "has_negative": bool(negative.get("summary") or negative.get("type")),
                "is_skeleton": brand_dir.name.startswith("_"),
            })

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

            # E7 (D#518) · use_cases présents mais aucun speculative = carte d'expansion
            # sans hypothèse (la chaîne Mc→U→A s'est arrêtée à l'évident, le Spectre est
            # avorté). Post-hoc MED, _EXAMPLE-safe (use_cases absent → ne tire pas).
            # Le vrai verrou des DEUX portes (scan + phase 3) = la postcondition
            # orchestrateur build-atlas, qui inspecte l'artefact écrit quelle que soit
            # la porte. Ici = le filet post-hoc qui attrape l'artefact dégénéré.
            use_cases = data.get("use_cases", []) or []
            if not is_skeleton and not brand_slug.startswith("_") and use_cases and not any(
                (u or {}).get("status") == "speculative" for u in use_cases
            ):
                issues.append({
                    "type": "use_cases_no_speculative",
                    "severity": SEVERITY["use_cases_no_speculative"],
                    "file": str(rel),
                    "msg": "spec.use_cases[] présent mais aucun status=speculative · la carte d'expansion n'a pas d'hypothèse (D#502 Mc→U→A) ; ajouter un usage spéculatif ou flagger le spectre incomplet",
                })

            # E7-bis (D#519) · l'angle mort du cas VIDE. use_cases_no_speculative ne tire
            # que sur une carte mince (présente sans speculative) ; il est aveugle au cas
            # « pas de carte du tout », qui est l'échec dominant quand le run pause avant le
            # Close (le pont mécanisme→usage narré dans le fil mais jamais persisté). Un
            # produit assez riche pour avoir des mécanismes mais ZÉRO use_cases = le pont
            # n'a pas été écrit. _EXAMPLE/skeleton exclus comme au-dessus.
            mechanisms = data.get("mechanisms") or []
            if not is_skeleton and not brand_slug.startswith("_") and mechanisms and not use_cases:
                issues.append({
                    "type": "use_cases_missing",
                    "severity": SEVERITY["use_cases_missing"],
                    "file": str(rel),
                    "msg": "spec a des mechanisms[] mais ZÉRO use_cases[] · le pont mécanisme→usage n'a jamais été écrit (carte vide, pire qu'une carte mince) ; la cartographie d'audiences retombe sur le miroir des avis",
                })

            # define-specs décrochage (sprint base-saine) · la décompo produit profonde
            # (l'orchestrateur define-specs chaîne map-mechanisms + map-benefits + map-specs ·
            # bénéfices 3 couches functional/emotional/identity) n'est jamais atteinte par
            # l'onboarding · snapshot hand-roll une passe mince. Un produit avec des mécanismes
            # mais ZÉRO benefits[] = la chaîne bénéfice n'a jamais été écrite → le pont Mc→U→A
            # part pauvre (l'atlas « marche » mais creux). Filet post-hoc, _EXAMPLE/skeleton exclus.
            benefits = data.get("benefits") or []
            if not is_skeleton and not brand_slug.startswith("_") and mechanisms and not benefits:
                issues.append({
                    "type": "benefits_missing",
                    "severity": SEVERITY["benefits_missing"],
                    "file": str(rel),
                    "msg": "spec a des mechanisms[] mais ZÉRO benefits[] · la décompo produit profonde (define-specs / map-benefits) n'a jamais tourné, snapshot a hand-rollé une passe mince ; la chaîne bénéfice 3 couches manque et le pont mécanisme→usage part pauvre",
                })

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

            # FIX 4 (D#519) · profil-clone-du-template. Le split narrate-puis-écris laisse un
            # `cp -r _example` brut dans un dossier audience RÉEL (run onday · actifs-fatigue
            # = octet pour octet le template, slug resté example-audience) pendant que le vrai
            # raisonnement reste gelé dans .workflow.json#pending. Aucun guard existant ne
            # l'attrapait (validate-all ne checkait que dangling-refs + cohérence index/dossier).
            meta_aud = data.get("meta", {}) or {}
            jtbd_primary = str(((data.get("psychology", {}) or {}).get("jtbd", {}) or {}).get("primary") or "")
            ident_desc = str((data.get("identity", {}) or {}).get("description") or "")
            is_clone = meta_aud.get("slug") == "example-audience" or (
                not meta_aud.get("entry_door") and not jtbd_primary.strip() and not ident_desc.strip()
            )
            if not audience_slug.startswith("_") and not brand_slug.startswith("_") and is_clone:
                issues.append({
                    "type": "audience_profile_template_clone",
                    "severity": SEVERITY["audience_profile_template_clone"],
                    "file": str(rel),
                    "msg": f"audiences/{audience_slug}/profile.json est le template dégénéré (slug=example-audience, ou entry_door+jtbd.primary+identity.description tous vides) · le raisonnement narré n'a jamais atteint l'artefact (split narrate-puis-écris, D#519)",
                })

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

    # 9. 'other' saturation — a high share of 'other' signals a MISSING family in
    # the backing registry, not an unclassifiable item. Generalised guardrail: same
    # threshold across every registry-backed axis. Replaces the single hardcoded
    # mode_of_action check. Each axis points at its own SSOT registry.
    # (axis_label, samples, issue_type, registry_path, other_token)
    saturation_axes = [
        ("mode_of_action",
         [m for meta in specs_by_product.values() for m in meta.get("mech_modes", [])],
         "mechanism_other_saturation",
         "resources/registries/mechanism-families.md", "other"),
        ("style_id", decomp_tags["style_id"],
         "style_other_saturation",
         "resources/registries/style-registry.md", "other"),
        ("mecanique_id", decomp_tags["mecanique_id"],
         "mecanique_other_saturation",
         "resources/registries/creative-mechanics-registry.md", "other"),
        ("beat_type", decomp_tags["beat_type"],
         "beat_type_other_saturation",
         "resources/registries/beat-registry.md", "other"),
    ]
    for axis_label, samples, issue_type, registry_path, other_token in saturation_axes:
        if len(samples) >= 3:
            n_other = samples.count(other_token)
            if n_other / len(samples) > 0.30:
                issues.append({
                    "type": issue_type,
                    "severity": SEVERITY[issue_type],
                    "msg": f"{axis_label}='{other_token}' on {n_other}/{len(samples)} (>30%) — a family is missing: promote it in {registry_path} instead of defaulting to '{other_token}'",
                })

    # 10. E8 (D#518) · Spectre trace · un angle qui DÉCLARE un lineage.use_case_ref
    # (back-ref optionnel) doit tracer vers une cellule du spectrum (usage porté par le
    # terrain cartographié). Intégrité post-hoc QUAND le ref est présent · jamais forcer
    # sa présence (pré-valider le choix d'angle = interdit, Master rule). _EXAMPLE-safe :
    # ses angles n'ont pas encore de use_case_ref → ne tire pas.
    for a in angles_seen:
        ang_rel, ang_id = a["rel"], a["angle_id"]
        uc_ref = a["use_case_ref"]
        if uc_ref and uc_ref not in spectrum_use_case_refs:
            issues.append({
                "type": "angle_spectrum_untraced",
                "severity": SEVERITY["angle_spectrum_untraced"],
                "file": ang_rel,
                "msg": f"{ang_id}.lineage.use_case_ref='{uc_ref}' ne trace vers aucune cellule spectrum.json · l'angle flotte hors carte (D#502/D#518)",
            })

        # E12 (D#523) · le pont carte→négatif. La coordonnée negative.spectrum_cell_ref
        # (le négatif concurrentiel sourcé du Spectre) doit tracer vers une cellule réelle.
        # Intégrité post-hoc QUAND le ref est présent · jamais forcer sa présence (Master rule).
        ncell = a["negative_cell_ref"]
        if ncell and ncell not in spectrum_cell_ids:
            issues.append({
                "type": "angle_negative_untraced",
                "severity": SEVERITY["angle_negative_untraced"],
                "file": ang_rel,
                "msg": f"{ang_id}.negative.spectrum_cell_ref='{ncell}' ne trace vers aucune cellule spectrum.json · le négatif concurrentiel déplace une alternative que la carte de marché n'a jamais vue (D#523)",
            })

        # E13 (D#523) · advisory awareness+négatif systématisé. Un angle qui a ARTICULÉ son
        # recadrage (formula.reframe rempli) sans nommer le NÉGATIF qu'il déplace prêche dans
        # le vide · le reframe est le pivot, le négatif en est la cible (les deux vont en paire).
        # LOW = advisory pur, jamais bloquant (le choix de quoi déplacer = jugement stratégique,
        # trust the model · Master rule) · ne tire que sur un angle déjà travaillé, jamais sur
        # une coquille light-pass nue, jamais sur _EXAMPLE.
        if not a["is_skeleton"] and a["has_reframe"] and not a["has_negative"]:
            issues.append({
                "type": "angle_negative_missing",
                "severity": SEVERITY["angle_negative_missing"],
                "file": ang_rel,
                "msg": f"{ang_id} a un recadrage (formula.reframe) mais ZÉRO négatif (coordonnée 5) · l'angle affirme une promesse sans déloger l'option en place · nommer l'alternative déplacée (negative.summary + type)",
            })

    # 11. E10 (D#518) · nombre marché nu · un nombre marché/concurrent/audience présent
    # SANS marqueur de fiabilité (entrée _extraction sur ce chemin OU market.meta.confidence)
    # entre comme un fait nu (scrapé ≠ fait, D#503). Post-hoc LOW : advisory, jamais un gate
    # (la prose/sémantique se fait confiance, Master rule). Le seuil de fiabilité réel se
    # pose côté skill (snapshot reliability_tier) ; ici = le filet qui rend le nu visible.
    # Scope = les nombres marché INFÉRÉS (le hasard "60k clients" : taille de marché,
    # revenu concurrent estimé). Pas awareness_distribution (split normalisé auto-labellé)
    # ni proofs.total_customers (déclaré opérateur, couvert par reliability_tier=declared
    # côté skill). Garde le filet net et _EXAMPLE-safe (ces deux nombres sont null).
    market = (brand_data or {}).get("market", {}) or {}
    extraction_map = (brand_data or {}).get("_extraction") or {}
    if not isinstance(extraction_map, dict):
        extraction_map = {}
    has_market_conf = (market.get("meta", {}) or {}).get("confidence") is not None
    def _has_prov(path_key):
        return has_market_conf or any(path_key in k for k in extraction_map)
    naked = []
    mo = market.get("market_overview", {}) or {}
    if mo.get("size_estimate") is not None and not _has_prov("size_estimate"):
        naked.append("market_overview.size_estimate")
    for i, c in enumerate(market.get("competitors", []) or []):
        if c.get("estimated_monthly_revenue") is not None and not _has_prov("estimated_monthly_revenue"):
            naked.append(f"competitors[{i}].estimated_monthly_revenue")
    for fld in naked:
        issues.append({
            "type": "naked_number_unsourced",
            "severity": SEVERITY["naked_number_unsourced"],
            "file": str((brand_dir / "brand.json").relative_to(brand_dir.parent.parent.parent)),
            "msg": f"market.{fld} = nombre sans marqueur de fiabilité (_extraction ou market.meta.confidence) · scrapé ≠ fait (D#503/D#518)",
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
