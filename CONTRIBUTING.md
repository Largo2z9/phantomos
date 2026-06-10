# Contributing to PhantomOS

PhantomOS is the agentic workspace for DTC paid acquisition operators. Contributions are welcome from operators extending capabilities, skill developers, and users reporting bugs or suggesting features.

## Local setup

```bash
git clone https://github.com/Largo2z9/phantomos.git
cd phantomos
```

Open in [Claude Code](https://claude.ai/code). The workspace loads its contracts automatically from `CLAUDE.md`.

## How to add a skill

Skills are the executable capabilities the agent triggers on context. To add one:

1. Read `.skills/how-to-build-skills.md` for the format.
2. Read `docs/system/skill-creation-protocol.md` for the discipline.
3. Create `.skills/skills/{name}/SKILL.md` with the required frontmatter (name, type, recommended_model, subagent_safe, mode, triggers, disambiguates_against).
4. Register your skill : `python3 .skills/build-manifest.py`.
5. Add an entry to `.skills/INDEX.md` under the relevant operator intent.

## How to extend the workspace

Custom entities, sidecar schemas, custom skills are all supported via the extension layer. Read `docs/system/extending.md` for the canon.

## Coding conventions

- **Tone and voice** for any operator-facing output : follow `docs/system/voice.md`.
- **JSON Schema** : 2020-12.
- **Documentation** : Markdown. Avoid internal jargon and acronyms in operator-facing surfaces.
- **No em-dashes** in docs (use commas, parentheses, or two sentences).

## Pull request process

1. Branch from `main`.
2. Test locally in Claude Code.
3. Open a PR with a description of the change, the type (skill, doc, schema, infra), how you tested, and links to related issues.
4. PRs are reviewed before merge.

## Reporting bugs and requesting features

Use the GitHub issue templates in `.github/ISSUE_TEMPLATE/`.

## Audience boundary

If you are an operator using PhantomOS, you don't need to read `docs/system/` or `docs/internal/`. See `docs/product/` for operator guidance instead. The `docs/system/` and `docs/internal/` folders are for contributors and core maintainers.
