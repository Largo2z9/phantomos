#!/usr/bin/env python3
"""
write_to_context — canonical mutation gateway for brands/ and operator/ JSON.

The ONLY sanctioned writer for protected JSON files (enforced by mutation-guard
PreToolUse hook). Skills MUST route every mutation through this script.

Writes the target JSON and appends an event entry to
`<workspace_root>/.phantom/context-engine-events.jsonl`.

Usage:
    python3 .skills/write-to-context.py \\
        --path "brands/{slug}/learnings.json#entries[]" \\
        --value '{"id":"LRN-001", "fact":"...", "reasoning":"..."}' \\
        --source operator \\
        --confidence 1.0 \\
        --mode direct

Path syntax:
    <relative_path>#<json_pointer>
    json_pointer forms:
        identity.name               → set scalar at dotted path
        contacts[0].email           → set scalar at indexed array element
        entries[]                   → append to array
        (empty)                     → replace whole document (use with care)

Modes:
    direct     → write clean value (use for scalars, arrays, or confirmed dicts)
    proposed   → stamp {_proposed:true, _source, _confidence} inside a dict value;
                 REJECTED for scalars/arrays (would corrupt consumers)

Exit codes:
    0  success
    1  argument / validation error
    2  IO / JSON error
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

VALID_MODES = {"direct", "proposed"}
VALID_SOURCES = {"operator", "agent", "scrape", "inference", "import"}

# Security scan patterns. Applied to every string leaf in --value and to --reason.
# Ported from NousResearch/hermes-agent tools/memory_tool.py security scan.
# On match, write is refused and a `refused` event is logged to events.jsonl.
SECURITY_PATTERNS = [
    ("prompt_injection", re.compile(
        r"(?i)(ignore\s+(all\s+|the\s+)?(previous|prior|above)\s+"
        r"(instructions|rules|prompts|directives|context))"
        r"|(disregard\s+(all\s+|previous\s+)?(instructions|rules|prompts))"
        r"|(system\s*:\s*you\s+are\s+now)"
        r"|(new\s+instructions\s*:)"
    )),
    ("credential_exfil", re.compile(
        r"(curl|wget|fetch|http\.get|requests\.(get|post))"
        r"[^\n]{0,200}"
        r"\$(ANTHROPIC|OPENAI|GITHUB|AWS|GOOGLE|SUPABASE|META|FACEBOOK|"
        r"STRIPE|SHOPIFY|CLAUDE|GEMINI|HF|OPENROUTER)[_A-Z0-9]*",
        re.IGNORECASE,
    )),
    ("ssh_backdoor", re.compile(
        r"(-----BEGIN\s+(RSA|OPENSSH|EC|DSA|PGP)\s+PRIVATE\s+KEY-----)"
        r"|(ssh-(rsa|ed25519|dss)\s+AAAA)"
        r"|(~?/?\.ssh/(authorized_keys|id_(rsa|ed25519|dsa)))"
    )),
    ("invisible_unicode", re.compile(
        r"[​-‍‪-‮⁦-⁩﻿]"
    )),
    ("destructive_shell", re.compile(
        r"(rm\s+-[rRfF]+[rRfF\s]*\s+/(\s|$|\w))"
        r"|(:\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:)"
        r"|(chmod\s+[0-7]*777\s+/(\s|$))"
        r"|(dd\s+if=/dev/(zero|random)\s+of=/dev/[sh]d)"
        r"|(mkfs\.\w+\s+/dev/[sh]d)"
    )),
]


def scan_string(text: str) -> list:
    """Return list of (pattern_name, matched_excerpt) for each SECURITY_PATTERNS hit."""
    hits = []
    for name, pat in SECURITY_PATTERNS:
        m = pat.search(text)
        if m:
            excerpt = m.group(0)
            if len(excerpt) > 80:
                excerpt = excerpt[:77] + "..."
            hits.append((name, excerpt))
    return hits


def scan_value(value) -> list:
    """Recursively walk value, scan every string leaf. Returns list of (path, name, excerpt)."""
    violations = []

    def walk(node, path):
        if isinstance(node, str):
            for name, excerpt in scan_string(node):
                violations.append((path or "<root>", name, excerpt))
        elif isinstance(node, dict):
            for k, v in node.items():
                if isinstance(k, str):
                    for name, excerpt in scan_string(k):
                        violations.append((f"{path}.<key:{k[:20]}>", name, excerpt))
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")

    walk(value, "")
    return violations


# Whitelist of allowed target files. Any write to a path not matching one of
# these is blocked — protects against shell-escaping typos that would otherwise
# create garbage files (e.g. `profile.jsonontrainte-sante`) because the script
# silently mkdir+touch any path it's given.
ALLOWED_PATH_PATTERNS = [
    re.compile(r"^brands/[^/]+/brand\.json$"),
    re.compile(r"^brands/[^/]+/status\.json$"),
    re.compile(r"^brands/[^/]+/config\.json$"),
    re.compile(r"^brands/[^/]+/learnings\.json$"),
    re.compile(r"^brands/[^/]+/strategy\.json$"),
    re.compile(r"^brands/[^/]+/products/[^/]+/spec\.json$"),
    re.compile(r"^brands/[^/]+/products/[^/]+/offers\.json$"),
    re.compile(r"^brands/[^/]+/audiences/[^/]+/profile\.json$"),
    re.compile(r"^brands/[^/]+/angles/[^/]+\.json$"),
    re.compile(r"^brands/[^/]+/custom/.+\.json$"),
    re.compile(r"^brands/[^/]+/[^/]+\.extensions\.json$"),
    # creatives organized by BATCH folder: creatives/{batch}/{CRT-NN}/ (bricks 1+3, D#480/481).
    # batch = a production run, date-stamped (e.g. 2026-06-06-01) → groups for scale (10k+ creatives,
    # navigable, git-friendly) instead of a flat dir. CRT = our own creatives. The id is claimed by
    # mkdir of the {CRT-NN}/ folder (no central allocator/lock). Brand-scoped → covered by mutation-guard.
    re.compile(r"^brands/[^/]+/creatives/[a-z0-9-]+/CRT-[0-9]{2,4}/creative\.json$"),
    re.compile(r"^brands/[^/]+/creatives/[a-z0-9-]+/CRT-[0-9]{2,4}/genome\.json$"),
    re.compile(r"^brands/[^/]+/creatives/[a-z0-9-]+/CRT-[0-9]{2,4}/produced/[a-z0-9_-]+\.json$"),
    # decomposed competitor ads — SEPARATE root (competitive-intel) + SEPARATE id namespace (RCV).
    re.compile(r"^brands/[^/]+/competitive-intel/[a-z0-9-]+/RCV-[0-9]{2,4}/decomposition\.json$"),
    # benchmark ref-image sidecar manifest (symmetric with CRT produced/, brick 4 step D).
    re.compile(r"^brands/[^/]+/competitive-intel/[a-z0-9-]+/RCV-[0-9]{2,4}/produced/[a-z0-9_-]+\.json$"),
    re.compile(r"^operator/[^/]+\.json$"),
    # canon validations (v2.26.0+) — append-only validations[] from learn-from-session promotion.
    re.compile(r"^resources/canon/[a-z-]+/[a-z-]+/[a-z0-9-]+\.json$"),
    # cross-brand expertise libraries (brick 2, D#481) — guarded by mutation-guard PROTECTED_GLOBS.
    # Filenames = lowercase-dash slug (the structured ID like CONCEPT-NN lives inside the file).
    re.compile(r"^resources/concepts/[a-z0-9-]+\.json$"),
    re.compile(r"^resources/registries/[a-z-]+/[a-z0-9-]+\.json$"),
    # asset-library json sidecars (brand-level · binaires .png/.jpg ecrits direct comme produced/).
    # Nom canonique = asset-library/ (aligne genome.schema + produced-asset.schema · D#491). Guard via brands/ glob.
    re.compile(r"^brands/[^/]+/asset-library/[a-z0-9_-]+\.json$"),
]


def check_target_allowed(rel_path: str) -> None:
    for pat in ALLOWED_PATH_PATTERNS:
        if pat.match(rel_path):
            return
    die(
        f"target path '{rel_path}' is not a known schema file. "
        f"Expected filename among: brand.json, status.json, config.json, "
        f"learnings.json, strategy.json, spec.json, offers.json, profile.json, "
        f"or *.extensions.json / custom/*.json. "
        f"Likely a typo or shell-escaping bug — recheck the --path argument.",
        1,
    )

# Workflow checkpoint gates. Each entry: (path_regex, required_checkpoint, slug_group).
# slug_group = index of regex group capturing product slug, or None if global checkpoint.
WORKFLOW_GATES = [
    (re.compile(r"^brands/(?P<brand>[^/]+)/products/(?P<slug>[^/_][^/]*)/spec\.json$"),
     "confirmed_products", "slug"),
    (re.compile(r"^brands/(?P<brand>[^/]+)/products/(?P<slug>[^/_][^/]*)/offers\.json$"),
     "confirmed_products", "slug"),
    (re.compile(r"^brands/(?P<brand>[^/]+)/audiences/[^/_][^/]*/profile\.json$"),
     "audience_q1q4_answered", None),
]


def _gate_message(brand: str, checkpoint: str, slug: str | None, rel_path: str, reason: str) -> str:
    """Build a self-documenting block message with the exact stage-proposal
    command the agent should run next."""
    slug_arg = f" --product-slug {slug}" if slug else ""
    cmd = (
        f"python3 .skills/stage-proposal.py "
        f"--brand {brand} "
        f"--checkpoint {checkpoint}"
        f"{slug_arg} "
        f'--summary "{{plain-language proposal: what you detected, why you propose it}}"'
    )
    return (
        f"workflow gate — {reason}\n"
        f"  target: {rel_path}\n"
        f"  checkpoint required: {checkpoint}"
        + (f" (product={slug})" if slug else "")
        + f"\n\n"
        f"NEXT ACTION — stage a proposal, then wait for the operator's reply:\n"
        f"  {cmd}\n\n"
        f"The checkpoint-resolver hook promotes the checkpoint from the operator's "
        f"next message. Do not write, retry, or bypass until the operator answers."
    )


def check_workflow_gate(root: Path, rel_path: str, source: str) -> None:
    """Block write if target path is gated and required checkpoint not resolved.
    Operator-sourced writes bypass (user is the authority)."""
    if source == "operator":
        return
    for pattern, checkpoint, slug_group in WORKFLOW_GATES:
        m = pattern.match(rel_path)
        if not m:
            continue
        brand = m.group("brand")
        wf = root / "brands" / brand / ".workflow.json"
        slug = m.group(slug_group) if slug_group else None
        if not wf.exists():
            die(_gate_message(brand, checkpoint, slug, rel_path,
                              f"brands/{brand}/.workflow.json not yet created"),
                1)
        try:
            state = json.loads(wf.read_text())
        except json.JSONDecodeError as e:
            die(f"workflow gate: {wf} corrupt: {e}", 2)
        checkpoints = state.get("checkpoints", {})
        if checkpoint == "confirmed_products":
            confirmed = checkpoints.get("confirmed_products", [])
            if slug not in confirmed:
                die(_gate_message(brand, checkpoint, slug, rel_path,
                                  f"product '{slug}' not in confirmed_products {confirmed}"),
                    1)
        else:
            if not checkpoints.get(checkpoint, False):
                die(_gate_message(brand, checkpoint, None, rel_path,
                                  f"checkpoint '{checkpoint}' still false"),
                    1)
        return


def die(msg: str, code: int = 1) -> None:
    print(f"[write_to_context] ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def find_workspace_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(8):
        if (cur / "brands").is_dir() and (cur / "resources").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    die(f"not inside a PhantomOS workspace (looked from {start})", 1)


def parse_pointer(ptr: str) -> list:
    """
    Accepts TWO syntaxes (detected automatically):

    1. JSON Pointer (RFC 6901, preferred by most LLMs):
       '/entries/-'      → append
       '/meta/name'      → set scalar
       '/contacts/0/email'
       Empty segments, '~0' → '~', '~1' → '/' per spec.

    2. Custom dotted/bracket:
       'entries[]'
       'meta.name'
       'contacts[0].email'
    """
    if not ptr:
        return []

    # Heuristic: leading '/' means JSON Pointer.
    if ptr.startswith("/"):
        tokens: list = []
        for seg in ptr[1:].split("/"):
            seg = seg.replace("~1", "/").replace("~0", "~")
            if seg == "-":
                tokens.append("[]")
            elif seg.isdigit():
                tokens.append(int(seg))
            else:
                tokens.append(seg)
        return tokens

    # Custom syntax fallback.
    tokens = []
    parts = re.split(r"\.|(\[\d*\])", ptr)
    for p in parts:
        if p is None or p == "":
            continue
        if p == "[]":
            tokens.append("[]")
        elif re.fullmatch(r"\[\d+\]", p):
            tokens.append(int(p[1:-1]))
        else:
            tokens.append(p)
    return tokens


def walk_set(doc, tokens: list, value):
    """Navigate doc via tokens and set value at the terminal. Returns mutated doc."""
    if not tokens:
        return value
    cur = doc
    for i, tok in enumerate(tokens[:-1]):
        if isinstance(tok, int):
            if not isinstance(cur, list) or tok >= len(cur):
                die(f"invalid index {tok} at segment {i} of pointer", 1)
            cur = cur[tok]
        elif tok == "[]":
            die(f"'[]' (append) only valid as final pointer segment", 1)
        else:
            if not isinstance(cur, dict):
                die(f"expected dict at segment {i} (got {type(cur).__name__})", 1)
            if tok not in cur:
                cur[tok] = {}
            cur = cur[tok]
    last = tokens[-1]
    if last == "[]":
        if not isinstance(cur, list):
            die("append '[]' on non-array terminal", 1)
        cur.append(value)
    elif isinstance(last, int):
        if not isinstance(cur, list):
            die("numeric index on non-array terminal", 1)
        if last > len(cur):
            die(f"index {last} out of range (len {len(cur)})", 1)
        if last == len(cur):
            cur.append(value)
        else:
            cur[last] = value
    else:
        if not isinstance(cur, dict):
            die("key set on non-object terminal", 1)
        cur[last] = value
    return doc


def wrap_proposed(value, source: str, confidence: float) -> dict:
    """mode=proposed stamps metadata *in place* on a dict value. It is intentionally
    rejected on scalars and arrays — wrapping them in {_value: ..., _proposed: true}
    corrupts downstream consumers (they see an object where they expect a scalar
    or list). Agents writing scalars/arrays should use mode=direct; the source
    and confidence are already preserved in the event log."""
    if not isinstance(value, dict):
        die(
            "mode=proposed requires --value to be a JSON object. "
            "Scalars and arrays cannot be wrapped — they corrupt consumers. "
            "Use --mode direct; source and confidence still recorded in the event log.",
            1,
        )
    out = dict(value)
    out["_proposed"] = True
    out["_source"] = source
    out["_confidence"] = confidence
    return out


def digest(value) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()[:12]


def append_event(root: Path, entry: dict) -> None:
    log_dir = root / ".phantom"
    log_dir.mkdir(exist_ok=True)
    with (log_dir / "context-engine-events.jsonl").open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(prog="write-to-context")
    ap.add_argument("--path", required=True,
                    help="<relative_path>#<json_pointer> (pointer optional, '[]' for append)")
    ap.add_argument("--value", required=True,
                    help="JSON-encoded value (scalar, object, or array)")
    ap.add_argument("--source", required=True, choices=sorted(VALID_SOURCES))
    ap.add_argument("--confidence", type=float, required=True,
                    help="0.0 (worst) to 1.0 (human-authoritative)")
    ap.add_argument("--mode", required=True, choices=sorted(VALID_MODES))
    ap.add_argument("--reason", default="",
                    help="Free-text rationale persisted in the event log")
    ap.add_argument("--cwd", default=os.getcwd())
    args = ap.parse_args()

    if not (0.0 <= args.confidence <= 1.0):
        die("confidence must be in [0.0, 1.0]", 1)
    if args.source == "operator" and args.confidence < 1.0:
        die("--source operator requires --confidence 1.0 (operator = user authority)", 1)
    if args.mode == "direct" and args.source == "agent" and args.confidence >= 1.0:
        die("confidence=1.0 is operator-only; agent writes max 0.9", 1)

    root = find_workspace_root(Path(args.cwd))

    if "#" not in args.path:
        rel_file, pointer = args.path, ""
    else:
        rel_file, pointer = args.path.split("#", 1)

    if args.mode == "proposed" and not pointer:
        die(
            "mode=proposed requires a JSONPointer fragment (e.g. file.json#/field). "
            "Writing a whole file in proposed mode stamps _proposed/_source/_confidence "
            "at the root object, corrupting consumers. Scaffold the file in mode=direct, "
            "then stamp individual fields in mode=proposed.",
            1,
        )

    check_target_allowed(rel_file)

    target = (root / rel_file).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        die(f"target {target} escapes workspace root {root}", 1)

    try:
        value = json.loads(args.value)
    except json.JSONDecodeError as e:
        die(f"--value is not valid JSON: {e}", 1)

    violations = scan_value(value)
    violations += [("<reason>", n, e) for n, e in scan_string(args.reason or "")]
    if violations:
        append_event(root, {
            "ts": datetime.utcnow().isoformat() + "Z",
            "path": args.path,
            "op": "refused",
            "source": args.source,
            "reason": "security_scan",
            "violations": [
                {"at": path, "pattern": name, "excerpt": excerpt}
                for path, name, excerpt in violations
            ],
        })
        lines = ["security scan refused write. matches:"]
        for path, name, excerpt in violations:
            lines.append(f"  - {name} at {path}: {excerpt!r}")
        lines.append("if this is a legitimate write, sanitize the value and retry.")
        die("\n".join(lines), 1)

    check_workflow_gate(root, rel_file, args.source)

    if args.mode == "proposed":
        value = wrap_proposed(value, args.source, args.confidence)

    tokens = parse_pointer(pointer)

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        try:
            doc = json.loads(target.read_text() or "null")
        except json.JSONDecodeError as e:
            die(f"{target} is not valid JSON: {e}", 2)
    else:
        doc = {} if tokens else None

    mutated = walk_set(doc, tokens, value) if tokens else value
    target.write_text(json.dumps(mutated, indent=2, ensure_ascii=False) + "\n")

    event = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "path": args.path,
        "op": "append" if tokens and tokens[-1] == "[]" else ("set" if tokens else "replace"),
        "source": args.source,
        "confidence": args.confidence,
        "mode": args.mode,
        "value_digest": digest(value),
        "reason": args.reason,
    }
    append_event(root, event)

    print(f"[write_to_context] OK {args.path} ({event['op']}, digest={event['value_digest']})")


if __name__ == "__main__":
    main()
