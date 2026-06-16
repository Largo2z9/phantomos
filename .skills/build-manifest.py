#!/usr/bin/env python3
"""
Builds .skills/_manifest.json from all SKILL.md frontmatters.

The manifest is a single JSON file the agent reads at session start instead
of scanning 29+ SKILL.md files. Regenerated on any skill add/rename/edit.

Usage:
    python3 .skills/build-manifest.py

Run from workspace-template root or from anywhere (resolves paths relative
to this script's location).
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

import os

try:
    import yaml
except ImportError:
    yaml = None

# Degrade gracefully instead of hard-failing. If PyYAML is missing, a
# best-effort frontmatter parser keeps newly created skills discoverable in the
# manifest. The self-evolution loop (an operator scaffolding a new capability)
# must never break on a missing optional dependency. Set BUILD_MANIFEST_NO_YAML=1
# to force the fallback (used by the parser-parity test).
HAVE_YAML = yaml is not None and os.environ.get("BUILD_MANIFEST_NO_YAML") != "1"
if not HAVE_YAML:
    print(
        "WARN: PyYAML unavailable, using best-effort frontmatter parser "
        "(pip3 install --user pyyaml for strict parsing).",
        file=sys.stderr,
    )

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_DIR = SCRIPT_DIR / "skills"
OUTPUT = SCRIPT_DIR / "_manifest.json"
MATRIX = SCRIPT_DIR.parent / "resources" / "canon" / "model-provider-matrix.json"

# v2.42+ jargon bank generation
WORKSPACE_ROOT = SCRIPT_DIR.parent


def load_allowed_aliases():
    """Read the durable model tiers from the provider matrix (fail-open).

    The matrix (resources/canon/model-provider-matrix.json) is the single source
    of truth for which logical model aliases exist. A skill whose recommended_model
    is not in this set is a typo or a stale pin. Validation happens at BUILD time,
    never at runtime (model-versioning-canon.md v2.46 dropped the runtime check on
    purpose). If the matrix is missing or unreadable, fall back to the canonical
    default so the self-evolution loop never breaks on an absent file.
    """
    default = {"opus", "sonnet", "haiku"}
    try:
        data = json.loads(MATRIX.read_text(encoding="utf-8"))
        aliases = set(data.get("allowed_aliases") or [])
        return aliases or default
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default
JARGON_SOURCE = WORKSPACE_ROOT / "docs" / "system" / "operator-vocabulary-translation.md"
JARGON_OUTPUT = SCRIPT_DIR / "_jargon_bank.json"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
FLOW_SEQ_RE = re.compile(r"(\[)([^\[\]\n]*)(\])")


def _quote_flow_items_with_braces(match):
    """Coerce unquoted flow sequence items that contain `{` into quoted strings.

    Backward compat shim: pre-PyYAML legacy SKILL.md files stored values like
    `writes: [brands/{slug}/products/{slug}/spec.json via write_to_context]`
    where the unquoted `{slug}` would be parsed by PyYAML as a nested flow
    mapping and fail. The legacy regex parser tolerated this. We tolerate it
    here too by quoting any flow-sequence item containing a brace, before
    handing the block to yaml.safe_load.
    """
    open_b, body, close_b = match.group(1), match.group(2), match.group(3)
    parts = [p.strip() for p in body.split(",")]
    fixed = []
    for p in parts:
        if not p:
            continue
        if "{" in p and not (p.startswith('"') or p.startswith("'")):
            # escape any embedded double quote, then wrap
            p_escaped = p.replace('"', '\\"')
            fixed.append(f'"{p_escaped}"')
        else:
            fixed.append(p)
    return open_b + ", ".join(fixed) + close_b


def _preprocess_frontmatter(block):
    """Apply backward compat shims before yaml.safe_load."""
    return FLOW_SEQ_RE.sub(_quote_flow_items_with_braces, block)


def _split_flow(inner):
    """Split an inline flow-sequence body on commas, respecting quotes."""
    parts, cur, quote = [], [], None
    for ch in inner:
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = None
        elif ch in ('"', "'"):
            quote = ch
            cur.append(ch)
        elif ch == ",":
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if cur:
        parts.append("".join(cur))
    return parts


def _strip_inline_comment(s):
    """Remove a trailing ' # ...' YAML comment that sits outside quotes."""
    quote = None
    for idx, ch in enumerate(s):
        if quote:
            if ch == quote:
                quote = None
        elif ch in ('"', "'"):
            quote = ch
        elif ch == "#" and (idx == 0 or s[idx - 1] in (" ", "\t")):
            return s[:idx].rstrip()
    return s


def _fb_scalar(s):
    s = s.strip()
    if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        return s[1:-1]
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    if s in ("null", "~", ""):
        return None
    return s


def _fb_inline_list(s):
    s = s.strip()
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [] if not inner else [_fb_scalar(x) for x in _split_flow(inner)]
    return None


def _fallback_parse_frontmatter(block):
    """Best-effort YAML-subset parser used when PyYAML is unavailable.

    Covers the SKILL.md frontmatter shape build-manifest relies on: top-level
    scalars, block scalars (>-, |), inline flow lists [a, b], and one level of
    nested mappings/lists. Not a general YAML parser. Keeps a new skill
    discoverable (name / type / model / permissions / description+triggers)
    without the optional PyYAML dependency, so the self-evolution loop survives.
    """
    lines = block.split("\n")
    n = len(lines)
    data = {}
    i = 0
    while i < n:
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip())
        if indent != 0 or ":" not in raw:
            i += 1
            continue
        key, _, rest = raw.partition(":")
        key = key.strip()
        rest = _strip_inline_comment(rest.strip())
        # Block scalar (folded >- / literal |): gather indented continuation.
        if rest in (">", ">-", ">+", "|", "|-", "|+"):
            buf = []
            i += 1
            while i < n and (not lines[i].strip() or (len(lines[i]) - len(lines[i].lstrip())) > 0):
                buf.append(lines[i].strip())
                i += 1
            data[key] = " ".join(x for x in buf if x).strip()
            continue
        inline = _fb_inline_list(rest)
        if inline is not None:
            data[key] = inline
            i += 1
            continue
        # Nested mapping/list (key: with nothing after). Parse only the first
        # child-indent level; deeper structures (e.g. a sub-list under a nested
        # key) are consumed but skipped, so they never leak into this level.
        if rest == "":
            sub, sublist, child_indent = {}, [], None
            i += 1
            while i < n:
                line = lines[i]
                if not line.strip():
                    i += 1
                    continue
                cur_indent = len(line) - len(line.lstrip())
                if cur_indent <= indent:
                    break
                if child_indent is None:
                    child_indent = cur_indent
                if cur_indent > child_indent:
                    i += 1
                    continue
                child = line.strip()
                if child.startswith("- "):
                    sublist.append(_fb_scalar(_strip_inline_comment(child[2:])))
                elif ":" in child:
                    ck, _, cv = child.partition(":")
                    cv = _strip_inline_comment(cv.strip())
                    civ = _fb_inline_list(cv)
                    sub[ck.strip()] = civ if civ is not None else _fb_scalar(cv)
                i += 1
            data[key] = sublist if sublist else sub
            continue
        data[key] = _fb_scalar(rest)
        i += 1
    return data


def parse_frontmatter(text, skill_name=None):
    """Strict YAML parse of frontmatter between --- delimiters.

    Returns dict on success, None if no frontmatter or yaml error.
    YAML errors are logged with skill name and the skill is skipped
    (manifest build continues for the remaining skills).
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    if not HAVE_YAML:
        data = _fallback_parse_frontmatter(m.group(1))
        return data if isinstance(data, dict) and data else None
    block = _preprocess_frontmatter(m.group(1))
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as e:
        label = skill_name or "<unknown>"
        print(f"WARN: yaml parse error in {label}: {e}", file=sys.stderr)
        return None
    if not isinstance(data, dict):
        return None
    return data


TRIGGER_FR_RE = re.compile(r"FR\s*:\s*(.+?)(?=\bEN\s*:|$)", re.DOTALL | re.IGNORECASE)
TRIGGER_EN_RE = re.compile(r"EN\s*:\s*(.+?)$", re.DOTALL | re.IGNORECASE)
QUOTED_RE = re.compile(r'"([^"]+)"')


def extract_triggers(description):
    """Pull FR and EN trigger phrases from the description text."""
    fr_match = TRIGGER_FR_RE.search(description or "")
    en_match = TRIGGER_EN_RE.search(description or "")
    fr = QUOTED_RE.findall(fr_match.group(1)) if fr_match else []
    en = QUOTED_RE.findall(en_match.group(1)) if en_match else []
    return {"fr": fr, "en": en}


# v2.42+ jargon bank parser
# Parses the markdown table in operator-vocabulary-translation.md and emits
# .skills/_jargon_bank.json for runtime post-render substitution in
# phantom-modes outputs. See `apply-jargon-filter.py` for the wrapper.

JARGON_TABLE_ROW_RE = re.compile(r"^\|(.+)\|(.+)\|(.+)\|\s*$")
JARGON_SEPARATOR_RE = re.compile(r"^\s*\|?\s*[:\-\s|]+\s*\|?\s*$")


def _split_variants(cell):
    """Split a markdown cell into variants on `·` or `,` separators."""
    if cell is None:
        return []
    text = cell.strip()
    if not text:
        return []
    # Normalize separators: middle dot · is canonical, comma is fallback.
    # Some rows use ` · ` and others use `,` · handle both.
    parts = []
    for chunk in text.split("·"):
        for piece in chunk.split(","):
            piece = piece.strip()
            if piece:
                parts.append(piece)
    return parts


def _is_header_or_separator(cells):
    """Detect markdown table header / separator rows to skip them."""
    joined = " ".join(cells).strip().lower()
    if "interne" in joined and "operator" in joined:
        return True
    if all(JARGON_SEPARATOR_RE.match(c) for c in cells):
        return True
    if all(set(c.strip()) <= set("-: |") for c in cells):
        return True
    return False


def build_jargon_bank():
    """Parse operator-vocabulary-translation.md table into _jargon_bank.json.

    Schema jargon-bank/1.0:
      entries[]: {internal[], operator_fr, operator_en, case_sensitive, context}

    Multi-variant `internal` allows the runtime filter to match any spelling
    of a jargon token (atlas vivant / atlas-vivant / atlas_vivant). Operator
    locale is selected at filter time (default FR).
    """
    if not JARGON_SOURCE.exists():
        print(f"WARN: jargon source not found: {JARGON_SOURCE}", file=sys.stderr)
        return

    text = JARGON_SOURCE.read_text(encoding="utf-8")
    entries = []
    in_mapping_section = False

    for line in text.splitlines():
        # Track entry into the canonical mapping section
        if line.strip().startswith("## Mapping canonique"):
            in_mapping_section = True
            continue
        if in_mapping_section and line.strip().startswith("## "):
            # Left the mapping section
            in_mapping_section = False
            continue
        if not in_mapping_section:
            continue

        m = JARGON_TABLE_ROW_RE.match(line)
        if not m:
            continue

        cells = [m.group(1), m.group(2), m.group(3)]
        if _is_header_or_separator(cells):
            continue

        internal_variants = _split_variants(cells[0])
        operator_fr = cells[1].strip()
        operator_en = cells[2].strip()

        if not internal_variants or not operator_fr:
            continue

        # Skip rows where internal already equals operator-facing (no-op rows)
        if operator_fr.startswith("(operator-facing déjà)"):
            continue

        entries.append({
            "internal": internal_variants,
            "operator_fr": operator_fr,
            "operator_en": operator_en,
            "case_sensitive": False,
            "context": "phantom-modes",
        })

    bank = {
        "_schema": "jargon-bank/1.0",
        "_generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "_source": "docs/system/operator-vocabulary-translation.md",
        "_total_entries": len(entries),
        "entries": entries,
    }
    JARGON_OUTPUT.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {JARGON_OUTPUT} with {len(entries)} jargon entries")


def build_manifest():
    entries = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
            continue
        if skill_dir.name == "custom":
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        try:
            text = skill_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"WARN: {skill_file}: {e}", file=sys.stderr)
            continue
        fm = parse_frontmatter(text, skill_name=skill_dir.name)
        if not fm:
            print(f"WARN: no frontmatter or invalid yaml in {skill_file}", file=sys.stderr)
            continue

        perm = fm.get("permissions", {}) if isinstance(fm.get("permissions"), dict) else {}
        disamb = fm.get("disambiguates_against", {}) if isinstance(fm.get("disambiguates_against"), dict) else {}
        entry = {
            "name": fm.get("name", skill_dir.name),
            "type": fm.get("type", "unknown"),
            "model": fm.get("recommended_model", "sonnet"),
            "subagent_safe": fm.get("subagent_safe", perm.get("subagent_safe", False)),
            "mode": fm.get("mode", perm.get("mode", "direct")),
            "triggers": extract_triggers(fm.get("description", "")),
            "disambiguates_against": disamb,
            "isolation_scope": fm.get("isolation_scope", "brand_only"),
            "layer": fm.get("layer"),
            "path": f".skills/skills/{skill_dir.name}/SKILL.md",
        }
        entries.append(entry)

    manifest = {
        "_version": "1.0",
        "_generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_count": len(entries),
        "skills": entries,
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT} with {len(entries)} skills")

    # Durability check (build-time, not runtime): every skill must name a model tier
    # that exists in the provider matrix. A stray value is a typo or a stale pin that
    # would route a skill to nothing. Returns the offenders so a release gate can fail.
    allowed = load_allowed_aliases()
    offenders = [(e["name"], e["model"]) for e in entries if e["model"] not in allowed]
    if offenders:
        print(f"WARN: {len(offenders)} skill(s) name a model outside the provider matrix "
              f"({sorted(allowed)}):", file=sys.stderr)
        for name, model in offenders:
            print(f"  - {name}: recommended_model={model!r}", file=sys.stderr)

    # De-bloat guard (anti re-accretion): no patch_notes / version-history in skill
    # frontmatter. Changelog lives in CHANGELOG.md; patch_notes in a SKILL.md is
    # always-loaded bloat the router never reads (the manifest never extracted it).
    # Flag any that creep back so the de-bloat cannot silently regrow.
    pn_offenders = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        sf = skill_dir / "SKILL.md"
        if not sf.is_file():
            continue
        m = FRONTMATTER_RE.match(sf.read_text(encoding="utf-8"))
        if m and re.search(r"^patch_notes", m.group(1), re.M):
            pn_offenders.append(skill_dir.name)
    if pn_offenders:
        print(f"WARN: {len(pn_offenders)} skill(s) carry patch_notes in frontmatter "
              f"(changelog belongs in CHANGELOG.md, not always-loaded context):", file=sys.stderr)
        for n in pn_offenders:
            print(f"  - {n}", file=sys.stderr)

    return offenders + [(n, "patch_notes-in-frontmatter") for n in pn_offenders]


if __name__ == "__main__":
    offenders = build_manifest()
    build_jargon_bank()
    # --strict turns the model-tier check into a release gate (exit 1 on any offender).
    if "--strict" in sys.argv and offenders:
        sys.exit(1)
