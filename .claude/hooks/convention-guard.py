#!/usr/bin/env python3
"""
PreToolUse hook · external tool convention guard.

Intercepts calls to external MCP servers (notion, supabase, shopify, meta-ads…)
and blocks them unless the matching resources/conventions/{platform}.json exists
and has a recent _doc_check.last_doc_read.

Fail-open on unmapped tool names · only enforces on known external platforms.
Fail-closed on missing/stale convention for a known platform.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Universal extraction. Any tool_name shaped `mcp__{server}__{op}` is auto-enrolled
# as platform = aliases.get(server, server). New MCPs require zero code change here.
MCP_PATTERN = re.compile(r"^mcp__([^_]+(?:_[^_]+)*)__")

# Normalize noisy MCP server names → clean convention slugs.
PLATFORM_ALIASES = {
    "facebook-graph": "meta-ads",
    "youtube-transcript": "youtube",
    "shopify-toutou": "shopify",
    "claude_ai_Slack": "slack",
    "claude_ai_Gmail": "gmail",
    "claude_ai_Google_Calendar": "google-calendar",
    "claude_ai_Google_Drive": "google-drive",
    "claude_ai_ClickUp": "clickup",
    "claude_ai_Excalidraw": "excalidraw",
    "claude_ai_Notion": "notion",
}

# Internal tooling exempt from convention enforcement (matched on raw server name).
PLATFORM_EXEMPT = {
    "plugin_vercel-plugin_vercel",
}

# Organizational / workspace / comms tools, exempt by RESOLVED slug. The guard
# disciplines DATA platforms (Meta, Shopify, GA4… where reading the API convention
# before a call is a real safeguard). It does NOT gate organizational tools : their
# first call would otherwise fail-closed for lack of a shipped convention and break
# the tool-first onboarding entry (Porte D · "organise tes outils"). Connecting one
# is handled by connect-mcp-server, not by the doc-read discipline. Matched on the
# resolved slug so any MCP that maps to one of these is covered, whatever its name.
PLATFORM_EXEMPT_SLUGS = {
    "notion", "clickup", "google-drive", "gmail", "slack",
    "google-calendar", "excalidraw", "youtube",
}

DOC_CHECK_MAX_AGE_DAYS = 90


def find_workspace_root(start: Path) -> Path | None:
    """Walk up from CWD to find the workspace (folder containing resources/conventions/)."""
    cur = start.resolve()
    for _ in range(8):
        if (cur / "resources" / "conventions").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def resolve_platform(tool_name: str) -> str | None:
    m = MCP_PATTERN.match(tool_name)
    if not m:
        return None
    raw = m.group(1)
    if raw in PLATFORM_EXEMPT:
        return None
    platform = PLATFORM_ALIASES.get(raw, raw).lower()
    if platform in PLATFORM_EXEMPT_SLUGS:
        return None
    return platform


def block(msg: str) -> None:
    """Emit a block decision on stderr, exit 2 (hook convention)."""
    print(msg, file=sys.stderr)
    sys.exit(2)


def allow() -> None:
    sys.exit(0)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        allow()
        return

    tool_name = payload.get("tool_name", "")
    platform = resolve_platform(tool_name)
    if not platform:
        allow()
        return

    cwd = Path(payload.get("cwd") or os.getcwd())
    root = find_workspace_root(cwd)
    if root is None:
        # Not inside a PhantomOS workspace · don't enforce.
        allow()
        return

    conv_path = root / "resources" / "conventions" / f"{platform}.json"
    if not conv_path.exists():
        block(
            f"[convention-guard] BLOCKED\n"
            f"Platform: {platform}\n"
            f"Missing convention file: {conv_path.relative_to(root)}\n\n"
            f"Required action:\n"
            f"  1. Copy resources/conventions/_TEMPLATE.json → {platform}.json\n"
            f"  2. Fill meta.platform, access.method, _doc_check.doc_source_urls\n"
            f"  3. Set _doc_check.last_doc_read to today after reading the official doc\n"
            f"  4. Retry the tool call\n\n"
            f"Rule source: workspace-template/CLAUDE.md § KB · ALWAYS read "
            f"resources/conventions/{{platform}}.json before any external tool/API call."
        )

    try:
        conv = json.loads(conv_path.read_text())
    except Exception as e:
        block(f"[convention-guard] BLOCKED · {conv_path.name} is not valid JSON: {e}")

    doc_check = conv.get("_doc_check") or {}
    last_read = doc_check.get("last_doc_read")
    if not last_read:
        block(
            f"[convention-guard] BLOCKED\n"
            f"Convention {platform}.json exists but _doc_check.last_doc_read is empty.\n"
            f"Read the official doc ({doc_check.get('doc_source_urls') or 'see platform docs'}), "
            f"then set _doc_check.last_doc_read to today's date (YYYY-MM-DD) and retry."
        )

    try:
        last_dt = datetime.strptime(last_read, "%Y-%m-%d")
    except Exception:
        block(
            f"[convention-guard] BLOCKED · _doc_check.last_doc_read has invalid format "
            f"({last_read!r}). Expected YYYY-MM-DD."
        )

    age = datetime.utcnow() - last_dt
    if age > timedelta(days=DOC_CHECK_MAX_AGE_DAYS):
        block(
            f"[convention-guard] BLOCKED · {platform}.json doc is stale "
            f"(last read {last_read}, {age.days}d ago, max {DOC_CHECK_MAX_AGE_DAYS}d).\n"
            f"Re-read the official doc, update _doc_check.last_doc_read, retry."
        )

    # Log successful pass for session audit.
    log_path = root / ".claude" / "convention-reads.log"
    try:
        with log_path.open("a") as f:
            f.write(
                f"{datetime.utcnow().isoformat()}Z\t{platform}\t{tool_name}\t"
                f"last_doc_read={last_read}\n"
            )
    except Exception:
        pass

    allow()


if __name__ == "__main__":
    main()
