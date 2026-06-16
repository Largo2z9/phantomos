#!/usr/bin/env python3
"""
migrate-nomenclature-v2-29.py · snake_case strict ASCII enforcement on JSON field names.

Scope:
  - resources/schemas/*.schema.json (canonical schemas)
  - brands/{slug}/**.json (data files, idempotent rename of legacy keys)

Renames applied (low-risk, safe, idempotent):
  insight.modalité           -> insight.modalite                    (angle.schema, creative.schema, brand data)
  pain_point.modalité        -> pain_point.modalite                 (creative.schema, brand data)
  cta.modalité               -> cta.modalite                        (creative.schema, brand data)
  atome_irréductible         -> atome_irreductible                  (creative.schema, brand data)
  delta_si_changé            -> delta_si_change                     (creative.schema nested, brand data)
  mini-skill (in JSON)       -> mini_skill                          (sop.schema, SOP YAML frontmatter)

NOT applied here (high-risk, flagged for operator arbitration):
  lineage.schwartz_conscience -> lineage.awareness_stage  (downstream skills produce-paid-angles,
                                                          produce-copy-brief still reference old name)
  origin_axis enum dash values (audience-derived, etc.)   (canon ; would break existing data/docs)
  cta.locus enum 'in-creative'                            (canon)
  status.json keys 'creme-eclat', 'femmes-40-55'          (these ARE slugs, dash is convention)

Usage:
  python3 .skills/migrate-nomenclature-v2-29.py            # dry-run
  python3 .skills/migrate-nomenclature-v2-29.py --apply    # apply
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Field renames: each entry = (legacy_key, new_key, key_path_predicate_or_None)
# key_path_predicate: callable taking parent_key_path str; returns True if rename applies.
# None means rename anywhere.
RENAMES = [
    ("modalité", "modalite", None),
    ("atome_irréductible", "atome_irreductible", None),
    ("delta_si_changé", "delta_si_change", None),
    ("mini-skill", "mini_skill", None),
]

LOG = []


def rename_keys(obj, path=""):
    """Recursively rename keys per RENAMES table. Returns mutated obj."""
    changed = False
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            new_k = k
            for legacy, new_, _ in RENAMES:
                if k == legacy:
                    new_k = new_
                    LOG.append(f"  {path}.{k} -> {path}.{new_k}")
                    changed = True
                    break
            new_v, sub_changed = rename_keys(v, f"{path}.{new_k}")
            new_dict[new_k] = new_v
            changed = changed or sub_changed
        return new_dict, changed
    elif isinstance(obj, list):
        new_list = []
        any_changed = False
        for i, item in enumerate(obj):
            new_item, sub_changed = rename_keys(item, f"{path}[{i}]")
            new_list.append(new_item)
            any_changed = any_changed or sub_changed
        return new_list, any_changed
    return obj, False


def process_file(p, apply):
    try:
        original = open(p).read()
        data = json.loads(original)
    except Exception as e:
        print(f"SKIP {p}: {e}", file=sys.stderr)
        return False
    new_data, changed = rename_keys(data)
    if not changed:
        return False
    if apply:
        with open(p, "w") as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"APPLIED  {p.relative_to(ROOT)}")
    else:
        print(f"WOULD-FIX {p.relative_to(ROOT)}")
    return True


def main():
    apply = "--apply" in sys.argv
    targets = []
    targets += list((ROOT / "resources/schemas").glob("*.schema.json"))
    targets += list((ROOT / "brands").rglob("*.json"))
    targets = [t for t in targets if "/_archive/" not in str(t)]

    n_changed = 0
    for t in targets:
        if process_file(t, apply):
            n_changed += 1

    print()
    print(f"=== Migration v2.29 nomenclature ===")
    print(f"Mode:      {'APPLY' if apply else 'DRY-RUN'}")
    print(f"Files hit: {n_changed}")
    if LOG:
        print(f"Changes:")
        for line in LOG[:200]:
            print(line)
        if len(LOG) > 200:
            print(f"  ... {len(LOG) - 200} more")
    if not apply and n_changed:
        print()
        print("Re-run with --apply to persist.")


if __name__ == "__main__":
    main()
