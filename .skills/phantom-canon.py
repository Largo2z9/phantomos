#!/usr/bin/env python3
"""
phantom-canon · read the canon atlas structure for /phantom canon mode.

Usage:
    python3 .skills/phantom-canon.py                   # list atlases (v2.26: only 'copy')
    python3 .skills/phantom-canon.py {atlas}           # list layers + tool count per layer
    python3 .skills/phantom-canon.py {atlas} {layer}   # list tools in a layer (one-line each)
    python3 .skills/phantom-canon.py {atlas} {layer} {tool}   # full tool card

Output: JSON. Operator-facing rendering is done by the caller (the agent).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(10):
        if (cur / ".skills").is_dir() and (cur / "brands").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def list_atlases(canon_root: Path) -> list[dict]:
    if not canon_root.is_dir():
        return []
    out = []
    for atlas in sorted(canon_root.iterdir()):
        if not atlas.is_dir() or atlas.name.startswith("_"):
            continue
        layer_count = sum(1 for d in atlas.iterdir() if d.is_dir() and not d.name.startswith("_"))
        tool_count = sum(1 for f in atlas.rglob("*.json") if not f.name.startswith("_"))
        out.append({"atlas": atlas.name, "layers": layer_count, "tools": tool_count})
    return out


def list_layers(atlas_dir: Path) -> list[dict]:
    out = []
    for layer in sorted(atlas_dir.iterdir()):
        if not layer.is_dir() or layer.name.startswith("_"):
            continue
        tools = sorted(layer.glob("*.json"))
        out.append({"layer": layer.name, "tools": len(tools)})
    return out


def list_tools(layer_dir: Path) -> list[dict]:
    out = []
    for tool_path in sorted(layer_dir.glob("*.json")):
        try:
            with tool_path.open("r", encoding="utf-8") as f:
                doc = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        out.append({
            "id": doc.get("id"),
            "name": doc.get("name"),
            "principle": doc.get("principle", ""),
            "validations_count": len(doc.get("validations", [])),
            "combines_count": sum(len(v) for v in doc.get("combines_with", {}).values() if isinstance(v, list))
        })
    return out


def read_tool(tool_path: Path) -> dict | None:
    try:
        with tool_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def main():
    root = find_workspace_root(Path.cwd())
    if root is None:
        print(json.dumps({"error": "workspace root not found"}), file=sys.stderr)
        sys.exit(1)

    canon_root = root / "resources" / "canon"
    args = sys.argv[1:]

    if not args:
        out = {"mode": "atlas-index", "atlases": list_atlases(canon_root)}
    elif len(args) == 1:
        atlas = args[0]
        atlas_dir = canon_root / atlas
        if not atlas_dir.is_dir():
            print(json.dumps({"error": f"atlas '{atlas}' not found"}), file=sys.stderr)
            sys.exit(1)
        out = {"mode": "layer-index", "atlas": atlas, "layers": list_layers(atlas_dir)}
    elif len(args) == 2:
        atlas, layer = args
        layer_dir = canon_root / atlas / layer
        if not layer_dir.is_dir():
            print(json.dumps({"error": f"layer '{layer}' not found in atlas '{atlas}'"}), file=sys.stderr)
            sys.exit(1)
        out = {"mode": "tools-in-layer", "atlas": atlas, "layer": layer, "tools": list_tools(layer_dir)}
    else:
        atlas, layer, tool_id = args[0], args[1], args[2]
        tool_path = canon_root / atlas / layer / f"{tool_id}.json"
        if not tool_path.is_file():
            print(json.dumps({"error": f"tool '{tool_id}' not found in {atlas}/{layer}"}), file=sys.stderr)
            sys.exit(1)
        doc = read_tool(tool_path)
        out = {"mode": "tool-card", "atlas": atlas, "layer": layer, "tool": doc}

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
