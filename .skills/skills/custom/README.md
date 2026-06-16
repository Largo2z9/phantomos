# Custom skills

Operator-built skills live here, namespaced separately from the shipped core skills in `../core/` (or the root of `.skills/skills/` in V1).

Custom skills follow the exact same authoring conventions as core skills:

- YAML frontmatter with `name`, `type`, `version`, `recommended_model`, `description`, `permissions` (declared reads, writes, mode, `subagent_safe`).
- Body structured around the skill's execution pipeline.
- Voice canon respected (see `../../docs/system/voice.md`).
- Mutation through `write_to_context()`, never direct JSON editing.

See `../how-to-build-skills.md` for the full authoring guide and `../agent-design-guide.md` for when a custom skill is justified.

Custom skills can read and write:
- Core entities (`brands/{slug}/brand.json`, etc.)
- Custom entities (`brands/{slug}/custom/{entity_type}/`)
- Sidecar schemas (`brands/{slug}/{core_entity}.extensions.json`)
- Shared resources (`resources/` registries, routing tables, frameworks)

**Not touched by template upgrades.** The template's next release replaces the `core/` skills but leaves `custom/` untouched. This is by design · operator-built capabilities belong to the operator.

**Promotion path.** A custom skill that proves its value across multiple brands is a candidate for promotion into a vertical pack or, exceptionally, into the core. The process is manual: the pattern is codified, tested across operators, and merged upstream.

See `docs/system/extending.md` for the full extension architecture.
