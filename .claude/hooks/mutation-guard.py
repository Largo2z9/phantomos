#!/usr/bin/env python3
"""
PreToolUse hook — brand/operator mutation guard + infrastructure guard.

Enforces two orthogonal rules:

1. BRAND/OPERATOR DATA — every mutation to brands/{slug}/* and operator/*
   must go through `write_to_context` (or a skill that wraps it). Direct
   file writes bypass the proposal/acceptance workflow and corrupt the
   event log.

2. WORKSPACE INFRASTRUCTURE — `.skills/*.py`, `.skills/skills/**/*.py`,
   `.claude/hooks/*.py`, `.claude/settings*.json` must NEVER be modified
   by an agent or subagent. These are workspace code, not operator data.
   Only the human maintainer edits them via a text editor outside the
   Claude Code tool loop. This closes the scope-violation gap detected
   in the v2.6.10 e-commerce pilot live onboarding (validate-resources subagent
   autonomously patched build-brand-snapshot.py, fix was correct, method wasn't).

Exemptions:
- brands/_TEMPLATE/* (scaffold source; template authoring is fine)
- brands/_EXAMPLE/* is NO LONGER exempt (M3 audit 2026-06-08): it is the read-only
  canon example, now PROTECTED at runtime so a deployed agent cannot corrupt it.
  R&D template maintenance runs outside a workspace root (no brands/+resources/ at
  the cwd), so the hook does not fire there.
- pure scaffold ops: `cp`, `mkdir`, `git`, `ls`, `find`, `cat`, `head`, `tail`, `grep`
- read-only inspection
- non-JSON writes under brand/ (markdown, .gitkeep) — those use append-only md skills
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# Paths under workspace_root that require write_to_context discipline.
# re.IGNORECASE closes the case-bypass (B3 audit 2026-06-08): on case-insensitive
# filesystems (APFS) `learnings.JSON` and `learnings.json` are the same file; a
# case-sensitive regex guarded only one.
PROTECTED_GLOBS = (
    re.compile(r"(?:^|/)brands/(?!_TEMPLATE)[^/]+/.+\.json$", re.IGNORECASE),
    re.compile(r"(?:^|/)operator/.+\.json$", re.IGNORECASE),
    # cross-brand expertise libraries (concepts, archetypes, hook-mechanics) — must transit
    # the gate like brand data (brick 2, D#481 fix for BUG-RESOURCES-UNGUARDED). Broad guard;
    # the precise allow-list lives in write-to-context.py ALLOWED_PATH_PATTERNS.
    re.compile(r"(?:^|/)resources/(?:concepts|registries|canon)/.+\.json$", re.IGNORECASE),
    # Brand Agent Contract = the brand-scoped system prompt. An agent must NOT rewrite
    # its own rules mid-session (M2 audit 2026-06-08, behavioral self-modification vector).
    # Scaffold via `cp -r brands/_TEMPLATE brands/{slug}` (dir copy) stays allowed; direct
    # Edit/Write/redirect of an existing brand CLAUDE.md is blocked.
    re.compile(r"(?:^|/)brands/(?!_TEMPLATE)[^/]+/CLAUDE\.md$", re.IGNORECASE),
)

# Workspace infrastructure — never modified by any agent/subagent during a session.
# Human maintainer edits these via a text editor outside the Claude Code tool loop.
INFRASTRUCTURE_GLOBS = (
    re.compile(r"(?:^|/)\.skills/[^/]+\.py$"),                # top-level scripts
    re.compile(r"(?:^|/)\.skills/skills/[^/]+/[^/]+\.py$"),   # skill-level scripts
    re.compile(r"(?:^|/)\.claude/hooks/[^/]+\.py$"),          # hooks themselves
    re.compile(r"(?:^|/)\.claude/settings(?:\.local)?\.json$"),
)

# Canonical writer exempted from all patterns below.
WRITE_TO_CONTEXT_RE = re.compile(r"(?:^|[;&|\s])python3?\s+[^\s;&|]*\.skills/write-to-context\.py\b")

# Bash patterns that indicate a write to a protected path (case-insensitive: B3).
BASH_WRITE_PATTERNS = (
    re.compile(r">>?\s*['\"]?([^\s'\";|&]+\.json)", re.IGNORECASE),                  # > foo.json
    re.compile(r"\btee\s+(?:-a\s+)?['\"]?([^\s'\";|&]+\.json)", re.IGNORECASE),      # tee foo.json
    re.compile(r"json\.dump\([^)]*open\(['\"]([^'\"]+\.json)", re.IGNORECASE),       # python json.dump
    re.compile(r"open\(['\"]([^'\"]+\.json)['\"],\s*['\"]w", re.IGNORECASE),         # open(...,'w')
    re.compile(r"\bsed\s+-i\b[^|]*?\s([^\s'\";|&]+\.json)", re.IGNORECASE),          # sed -i ... foo.json
    re.compile(r"\bjq\s+[^|]*?\|\s*tee\s+['\"]?([^\s'\";|&]+\.json)", re.IGNORECASE),
    # cp / mv / install / ln writing TO a protected target (B2 audit 2026-06-08).
    # Captures the LAST operand (the dest) only when it ends in .json or is a brand CLAUDE.md.
    # A directory dest (scaffold `cp -r brands/_TEMPLATE brands/{slug}`) has no such token -> not matched.
    re.compile(r"(?:^|[;&|]\s*)(?:cp|mv|install|ln)\b[^|&;]*?\s(\S+(?:\.json|/CLAUDE\.md))(?=\s*(?:$|[;&|]))", re.IGNORECASE),
    # python shutil copy/move/copyfile TO a protected target (2nd arg = dest).
    re.compile(r"shutil\.(?:copy2?|copyfile|move)\(\s*['\"][^'\"]+['\"]\s*,\s*['\"]([^'\"]+(?:\.json|/CLAUDE\.md))['\"]", re.IGNORECASE),
    # redirect / tee / sed targeting a brand CLAUDE.md contract (M2).
    re.compile(r">>?\s*['\"]?([^\s'\";|&]+/CLAUDE\.md)", re.IGNORECASE),
    re.compile(r"\btee\s+(?:-a\s+)?['\"]?([^\s'\";|&]+/CLAUDE\.md)", re.IGNORECASE),
    re.compile(r"\bsed\s+-i\b[^|]*?\s([^\s'\";|&]+/CLAUDE\.md)", re.IGNORECASE),
)


def is_protected(path_str: str) -> bool:
    return any(p.search(path_str) for p in PROTECTED_GLOBS)


def is_infrastructure(path_str: str) -> bool:
    return any(p.search(path_str) for p in INFRASTRUCTURE_GLOBS)


def block(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(2)


def allow() -> None:
    sys.exit(0)


def find_workspace_root(start: Path):
    cur = start.resolve()
    for _ in range(8):
        if (cur / "brands").is_dir() and (cur / "resources").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def block_msg(path: str, via: str) -> str:
    return (
        f"[mutation-guard] BLOCKED\n"
        f"Direct write to protected JSON via {via}: {path}\n\n"
        f"CLAUDE.md § Mutation rule: every mutation to brands/{{slug}}/* and operator/*\n"
        f"MUST go through write_to_context(field_path, value, source, confidence, mode='proposed').\n"
        f"Direct edits skip the proposal gate, corrupt the event log, and bypass validation.\n\n"
        f"What to do:\n"
        f"  - If you're scaffolding from template: use `cp -r brands/_TEMPLATE brands/{{slug}}` (allowed).\n"
        f"  - If you're filling a field: route via the relevant skill (setup-brand, snapshot-brand, capture-learning, ingest-resource).\n"
        f"  - If no skill covers your case: surface the gap to the operator instead of hand-editing.\n"
        f"  - brands/_TEMPLATE/ (scaffold source) is exempt. brands/_EXAMPLE/ is the read-only canon example and is now protected (visit it, never write it)."
    )


def block_msg_infra(path: str, via: str) -> str:
    return (
        f"[mutation-guard] BLOCKED (infrastructure)\n"
        f"Attempt to modify workspace infrastructure via {via}: {path}\n\n"
        f"Scripts under .skills/ and .claude/hooks/, plus .claude/settings.json,\n"
        f"are workspace code — not operator data and not agent-editable.\n"
        f"Only the human maintainer edits them via a text editor outside the\n"
        f"Claude Code tool loop.\n\n"
        f"What to do:\n"
        f"  - If you found a genuine bug, surface it to the operator with a clear\n"
        f"    description and a proposed fix. The maintainer applies the fix via\n"
        f"    the release/update-workspace channel, not via an agent autopatch.\n"
        f"  - If you're writing a NEW skill, use scaffold-skill-stub / build-agent\n"
        f"    (they write under .skills/skills/custom/, which IS allowed).\n"
        f"  - If you need a new hook or settings change, it's a maintainer task.\n"
        f"    Open a todo in the relevant project tracker, do not hand-edit."
    )


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        allow()
        return

    cwd = Path(payload.get("cwd") or os.getcwd())
    root = find_workspace_root(cwd)
    if root is None:
        allow()
        return

    tool = payload.get("tool_name", "")
    inp = payload.get("tool_input") or {}

    # Edit / Write / NotebookEdit — direct file_path inspection.
    if tool in ("Edit", "Write", "NotebookEdit", "MultiEdit"):
        fp = inp.get("file_path") or inp.get("notebook_path") or ""
        try:
            rel = str(Path(fp).resolve().relative_to(root))
        except Exception:
            rel = fp
        if is_infrastructure(rel):
            block(block_msg_infra(rel, tool))
        if is_protected(rel):
            block(block_msg(rel, tool))
        allow()
        return

    # Bash — scan command for write patterns hitting protected or infra paths.
    if tool == "Bash":
        cmd = inp.get("command", "") or ""
        # Canonical writer is always allowed, even though it opens files in 'w'.
        if WRITE_TO_CONTEXT_RE.search(cmd):
            allow()
            return
        # Extend bash scan to catch infra-targeted writes too.
        INFRA_BASH_PATTERNS = (
            re.compile(r">>?\s*['\"]?([^\s'\";|&]+\.(?:py|json))"),
            re.compile(r"\btee\s+(?:-a\s+)?['\"]?([^\s'\";|&]+\.(?:py|json))"),
            re.compile(r"\bsed\s+-i\b[^|]*?\s([^\s'\";|&]+\.(?:py|json))"),
            re.compile(r"open\(['\"]([^'\"]+\.(?:py|json))['\"],\s*['\"]w"),
        )
        for pat in BASH_WRITE_PATTERNS:
            for m in pat.finditer(cmd):
                target = m.group(1)
                try:
                    abs_target = (Path(cwd) / target).resolve()
                    rel = str(abs_target.relative_to(root))
                except Exception:
                    rel = target
                if is_protected(rel):
                    block(block_msg(rel, f"Bash ({pat.pattern[:30]}...)"))
        for pat in INFRA_BASH_PATTERNS:
            for m in pat.finditer(cmd):
                target = m.group(1)
                try:
                    abs_target = (Path(cwd) / target).resolve()
                    rel = str(abs_target.relative_to(root))
                except Exception:
                    rel = target
                if is_infrastructure(rel):
                    block(block_msg_infra(rel, f"Bash ({pat.pattern[:30]}...)"))
        allow()
        return

    allow()


if __name__ == "__main__":
    main()
