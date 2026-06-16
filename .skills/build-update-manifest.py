#!/usr/bin/env python3
"""
Pre-fills docs/releases/{to_version}-manifest.json from a git diff.

Reads git diff between two refs (typically the previous release tag and HEAD),
classifies each changed file into a change type (doc-change, infra-change,
skill-added, skill-renamed, skill-removed), and emits a draft manifest.

The maintainer reviews and augments it manually with:
- schema-bump entries (diff cannot infer schema semantics)
- breaking flag when applicable
- note fields with meaningful descriptions

Usage:
    python3 .skills/build-update-manifest.py {from_ref} {to_version}

Examples:
    python3 .skills/build-update-manifest.py v2.6.2 2.6.3
    python3 .skills/build-update-manifest.py HEAD~20 2.6.4

Output: docs/releases/{to_version}-manifest.draft.json (never overwrites a real manifest).
"""

import json
import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent


def git(*args):
    result = subprocess.run(
        ["git"] + list(args),
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"git {' '.join(args)} failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def classify_change(path, status):
    """Classify a changed file into a manifest change type. Returns dict or None."""
    # Path is relative to repo root; we're interested only in files under workspace-template
    if not path.startswith("05-projects/context-engine/workspace-template/"):
        return None
    rel = path[len("05-projects/context-engine/workspace-template/"):]

    # Skip operator-owned paths (should never appear in template updates anyway)
    if rel.startswith("brands/") and not (rel.startswith("brands/_TEMPLATE/") or rel.startswith("brands/_EXAMPLE/") or rel == "brands/README.md"):
        return None
    if rel.startswith("operator/"):
        return None

    # Skill folder changes
    skill_match = re.match(r"^\.skills/skills/([^/]+)/SKILL\.md$", rel)
    if skill_match:
        skill_name = skill_match.group(1)
        if skill_name.startswith("_") or skill_name == "custom":
            return None
        if status == "A":
            return {
                "type": "skill-added",
                "skill": skill_name,
                "files": [rel],
                "action": "create",
                "safe": True,
                "note": "TODO: describe new skill purpose",
            }
        if status == "D":
            return {
                "type": "skill-removed",
                "skill": skill_name,
                "alternative": None,
                "safe": True,
                "note": "TODO: declare alternative or confirm deprecation",
            }
        return {
            "type": "doc-change",
            "file": rel,
            "action": "overwrite",
            "safe": True,
            "note": "TODO: describe what changed in the skill",
        }

    # Infra (scripts)
    if rel.endswith(".py") or rel.endswith(".sh") or rel.startswith("Makefile") or rel.startswith("scripts/"):
        return {
            "type": "infra-added" if status == "A" else "infra-change",
            "file": rel,
            "action": "create" if status == "A" else "overwrite",
            "safe": True,
            "note": "TODO: describe script change and any post_step needed",
        }

    # Schema change · flagged for manual schema-bump entry
    if "schema.json" in rel or rel.startswith("resources/schemas/"):
        return {
            "type": "_TODO_schema-bump",
            "file": rel,
            "action": "overwrite",
            "safe": False,
            "requires_confirmation": True,
            "note": "REVIEW: schema change detected. If this is a schema-bump, add migration_script, from/to_schema_version, and affected_files_glob.",
        }

    # Docs + markdown
    if rel.endswith(".md") or rel.endswith(".json") or rel.endswith(".yaml") or rel.endswith(".yml"):
        return {
            "type": "doc-added" if status == "A" else "doc-change",
            "file": rel,
            "action": "create" if status == "A" else "overwrite",
            "safe": True,
            "note": "TODO: describe the change",
        }

    return None


def detect_renames(diff_output):
    """Parse git diff --name-status output for renames (R lines).
    Returns list of (old, new) paths under workspace-template.
    """
    renames = []
    for line in diff_output.splitlines():
        parts = line.split("\t")
        if not parts or not parts[0].startswith("R"):
            continue
        if len(parts) < 3:
            continue
        old, new = parts[1], parts[2]
        tpl = "05-projects/context-engine/workspace-template/"
        if not old.startswith(tpl) or not new.startswith(tpl):
            continue
        old_rel = old[len(tpl):]
        new_rel = new[len(tpl):]
        # Skill rename only when both are under .skills/skills/{name}/SKILL.md
        m_old = re.match(r"^\.skills/skills/([^/]+)/SKILL\.md$", old_rel)
        m_new = re.match(r"^\.skills/skills/([^/]+)/SKILL\.md$", new_rel)
        if m_old and m_new and m_old.group(1) != m_new.group(1):
            renames.append({
                "type": "skill-renamed",
                "from": m_old.group(1),
                "to": m_new.group(1),
                "aliases_to_keep": [m_old.group(1)],
                "safe": True,
                "note": "TODO: confirm or remove aliases_to_keep",
            })
    return renames


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 .skills/build-update-manifest.py {from_ref} {to_version}", file=sys.stderr)
        sys.exit(1)
    from_ref, to_version = sys.argv[1], sys.argv[2]

    # Read current installed version for from_version field
    current_version = "unknown"
    v_file = ROOT / "_version.json"
    if v_file.exists():
        try:
            current_version = json.loads(v_file.read_text()).get("template_version", "unknown")
        except Exception:
            pass

    # Git diff
    diff_output = git("diff", "--name-status", from_ref, "HEAD", "--", "05-projects/context-engine/workspace-template/")
    changes = []
    seen = set()

    # First pass · renames
    renames = detect_renames(diff_output)
    for r in renames:
        changes.append(r)
        # Mark the paths as handled
        seen.add(f".skills/skills/{r['from']}/SKILL.md")
        seen.add(f".skills/skills/{r['to']}/SKILL.md")

    # Second pass · other changes
    for line in diff_output.splitlines():
        parts = line.split("\t")
        if not parts or parts[0].startswith("R"):
            continue
        status = parts[0][0]  # A, D, M, etc.
        path = parts[-1]
        classified = classify_change(path, status)
        if classified is None:
            continue
        # Skip if already handled by rename
        file_key = classified.get("file") or ""
        if file_key in seen:
            continue
        changes.append(classified)

    manifest = {
        "_schema": "update-manifest/1.0",
        "from_version": current_version,
        "to_version": to_version,
        "released_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "summary": "TODO: short human-readable description",
        "breaking": False,
        "requires_confirmation": False,
        "notes": "TODO: key info the receiver's agent needs to know (or remove this field)",
        "changes": changes,
        "post_update_checklist": [
            "python3 .skills/build-manifest.py",
            "python3 .skills/build-brand-snapshot.py --all",
            "Run validate-resources on each brand",
            f"Update /operator/installation.json → template_version_installed = {to_version}",
        ],
        "_draft_notice": "AUTO-GENERATED DRAFT. Review every entry. Fill TODO fields. Add schema-bump entries for any schema changes (diff cannot infer schema semantics).",
    }

    output_path = ROOT / "docs" / "releases" / f"{to_version}-manifest.draft.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote draft manifest: {output_path}")
    print(f"changes detected: {len(changes)}")
    print(f"NEXT: review, fill TODO fields, rename to {to_version}-manifest.json")


if __name__ == "__main__":
    main()
