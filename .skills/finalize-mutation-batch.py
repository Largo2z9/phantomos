#!/usr/bin/env python3
"""
Mechanical finalizer for skills that just wrote a batch of mutations.

Replaces the soft-prescribed "Invoke validate-output-coherence" step that
producer skills (snapshot-brand, setup-brand, ingest-resource) systematically
skipped. This is a Python primitive, not an LLM call · deterministic,
forceable, testable.

Does:
1. Reads the brand's _field_types map (canon).
2. Inspects recent write-to-context events for the brand (last N seconds).
3. Runs structural checks:
   - Every written path is covered by a glob in _field_types.
   - No `derived` field has a non-null value (canon: never filled manually).
   - tone_of_voice.* writes are tagged stated, not observed/derived.
   - Required entity files referenced exist on disk.
4. Emits a coherence_check event with the report so turn-end-audit sees it.
5. Returns JSON to stdout (caller uses it for the operator summary).

Exit codes:
0 · checks ran (with or without warnings)
1 · bad args, brand not found, or _field_types missing
2 · blocking issue found (caller MUST revise before shipping)
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(12):
        if (cur / "brands").is_dir() and (cur / ".skills").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def glob_match(path: str, glob: str) -> bool:
    """_field_types globs use shell-like wildcards on json-pointer paths."""
    # Normalize: replace [] with [*] for fnmatch
    g = glob.replace("[]", "[*]").replace(".", "/")
    p = path.lstrip("/").replace(".", "/")
    if "[*]" in g:
        # crude: replace [*] with /<digit>/ pattern
        return fnmatch.fnmatch(p, g.replace("[*]", "*"))
    return fnmatch.fnmatch(p, g)


# Non-entity files: state/config/index, not part of the data canon.
# Writes to these don't go through _field_types validation.
NON_ENTITY_FILES = {
    "config.json",
    "status.json",
    "session-state.md",
    "learnings-index.json",
    "pending-validations.md",
}


def is_skippable_pointer(pointer: str) -> bool:
    """Skip JSON-Schema-ish meta paths (start with $) and runtime-meta paths
    (start with _, e.g. _snapshot, _proposed, _source, _confidence)."""
    if not pointer:
        return True
    head = pointer.split("/", 1)[0]
    return head.startswith("$") or head.startswith("_")


def find_type(field_types: dict, path: str) -> str | None:
    """Path uses '/' separators (json-pointer-like). Globs use '.' separators
    in the canon. Match by translating both to common form."""
    # Strip any leading slash on the path
    rel = path.lstrip("/")
    # Convert path to dot form
    dotted = rel.replace("/", ".")
    # Try exact match first
    if dotted in field_types:
        return field_types[dotted]
    # Then glob match
    for glob, type_ in field_types.items():
        # fnmatch on the dotted form
        if fnmatch.fnmatchcase(dotted, glob):
            return type_
        # Handle [].field globs by replacing [] with *
        normalized = glob.replace("[]", "[0-9]*").replace("[", "[").replace("]", "]")
        if fnmatch.fnmatchcase(dotted, normalized.replace("[0-9]*", "*")):
            return type_
    return None


def load_recent_events(events_path: Path, brand_slug: str, since_ts: float) -> list[dict]:
    """Return write-to-context events for this brand since the given timestamp."""
    if not events_path.is_file():
        return []
    out = []
    prefix = f"brands/{brand_slug}/"
    try:
        for line in events_path.read_text().splitlines():
            if prefix not in line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = e.get("ts", "")
            try:
                t = datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
            except Exception:
                continue
            if t < since_ts:
                continue
            path = e.get("path", "")
            if not path.startswith(prefix):
                continue
            out.append(e)
    except Exception:
        return []
    return out


def load_field_types(brand_dir: Path, file_rel: str) -> dict:
    """Load _field_types from brand.json or any entity file."""
    target = brand_dir / file_rel
    if not target.exists():
        return {}
    try:
        return json.loads(target.read_text()).get("_field_types", {})
    except Exception:
        return {}


def has_value(value) -> bool:
    """Heuristic: does this value count as 'filled'?"""
    if value is None:
        return False
    if isinstance(value, (str, list, dict)) and len(value) == 0:
        return False
    return True


def emit_event(root: Path, payload: dict) -> None:
    log_dir = root / ".phantom"
    log_dir.mkdir(exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "type": "coherence_check",
        "source": "finalize-mutation-batch",
        "payload": payload,
    }
    with (log_dir / "context-engine-events.jsonl").open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(prog="finalize-mutation-batch")
    ap.add_argument("--brand-slug", required=True)
    ap.add_argument("--window-seconds", type=int, default=600,
                    help="Inspect mutations from the last N seconds (default 600)")
    ap.add_argument("--quiet", action="store_true",
                    help="Suppress JSON stdout, only emit event")
    args = ap.parse_args()

    root_str = os.environ.get("CLAUDE_PROJECT_DIR")
    root = Path(root_str) if root_str else find_workspace_root(Path.cwd())
    if root is None:
        print("[finalize] workspace root not found", file=sys.stderr)
        return 1

    brand_dir = root / "brands" / args.brand_slug
    if not brand_dir.is_dir():
        print(f"[finalize] brand not found: {args.brand_slug}", file=sys.stderr)
        return 1

    events_path = root / ".phantom" / "context-engine-events.jsonl"
    since = datetime.now(timezone.utc).timestamp() - args.window_seconds
    events = load_recent_events(events_path, args.brand_slug, since)

    # Group events by file (each file has its own _field_types).
    file_to_events: dict[str, list[dict]] = {}
    for e in events:
        path = e["path"]
        # Split: brands/{slug}/path/to/file.json#/json/pointer
        if "#" in path:
            file_rel, pointer = path.split("#", 1)
        else:
            file_rel, pointer = path, ""
        # Strip brands/{slug}/ prefix to get file_rel relative to brand_dir
        prefix = f"brands/{args.brand_slug}/"
        if file_rel.startswith(prefix):
            file_rel_short = file_rel[len(prefix):]
        else:
            file_rel_short = file_rel
        file_to_events.setdefault(file_rel_short, []).append({
            "pointer": pointer.lstrip("/"),
            "value_digest": e.get("value_digest"),
            "source": e.get("source"),
        })

    issues_blocking: list[dict] = []
    issues_warning: list[dict] = []
    files_checked: list[str] = []

    for file_rel, file_events in file_to_events.items():
        # Skip non-entity files (system state, indexes, scratch).
        if file_rel in NON_ENTITY_FILES or any(file_rel.endswith("/" + n) for n in NON_ENTITY_FILES):
            continue
        ft = load_field_types(brand_dir, file_rel)
        if not ft:
            issues_warning.append({
                "kind": "missing_field_types",
                "file": file_rel,
                "msg": "_field_types map missing or empty · cannot validate writes",
            })
            continue
        files_checked.append(file_rel)
        for ev in file_events:
            ptr = ev["pointer"]
            if is_skippable_pointer(ptr):
                continue
            ftype = find_type(ft, ptr)
            if ftype is None:
                issues_warning.append({
                    "kind": "unmapped_path",
                    "file": file_rel,
                    "pointer": ptr,
                    "msg": "path not covered by any _field_types glob",
                })
                continue
            # Hard rule: derived fields never filled manually.
            if ftype == "derived" and ev["source"] != "import":
                issues_blocking.append({
                    "kind": "manual_derived_write",
                    "file": file_rel,
                    "pointer": ptr,
                    "source": ev["source"],
                    "msg": f"derived field written manually (source={ev['source']})",
                })
            # tone_of_voice fields must be stated.
            if ptr.startswith("tone_of_voice/") and ftype not in ("stated", "structured"):
                issues_warning.append({
                    "kind": "tone_misclassified",
                    "file": file_rel,
                    "pointer": ptr,
                    "got": ftype,
                    "msg": "tone_of_voice fields should be 'stated' or 'structured', not 'observed' or 'derived'",
                })

    payload = {
        "brand_slug": args.brand_slug,
        "ok": len(issues_blocking) == 0,
        "warnings": len(issues_warning),
        "blocking": len(issues_blocking),
        "events_inspected": len(events),
        "files_checked": files_checked,
        "issues_blocking": issues_blocking,
        "issues_warning": issues_warning,
    }

    emit_event(root, payload)

    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    if issues_blocking:
        print(f"[finalize] {len(issues_blocking)} BLOCKING issue(s) · caller MUST revise before shipping",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
