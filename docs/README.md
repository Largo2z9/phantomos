# Documentation

PhantomOS documentation lives here, organized by audience and intent. Five types of docs exist in this project — four in this folder, one outside it.

## The five doc types

| Type | Audience | Question answered | Location |
|---|---|---|---|
| **Product** | Operator using PhantomOS | *How do I use it ?* | `docs/product/` |
| **Vision** | Anyone evaluating PhantomOS | *Why does it exist ?* | `docs/vision/` |
| **System** | Contributor extending PhantomOS | *How does it work, how do I extend it ?* | `docs/system/` |
| **Internal** | Core maintainers and integrators | *How is it maintained, what changed technically ?* | `docs/internal/` |
| **Runtime** | The agent itself | *What rules do I execute on ?* | `CLAUDE.md` files, `.skills/**/SKILL.md`, `lexicon.md`, `operator/profile.json` |

Each type has its own register, budget, and conventions. Runtime docs are auto-injected into the agent's system prompt and live where the runtime expects them — outside this folder.

## Directory map

```
docs/
├── README.md              you are here
│
├── product/               operator-facing
│   ├── getting-started.md     quickstart
│   ├── capabilities.md        what PhantomOS can do
│   ├── fit.md                 who PhantomOS is for (and who it isn't)
│   └── guides/                task-oriented how-tos
│       └── first-session-example.md
│
├── vision/                public-facing
│   ├── prisms.md              eight framings of PhantomOS
│   ├── roadmap.md             what ships next
│   └── manifesto.md           the thesis behind the product
│
├── system/                contributor-facing
│   ├── voice.md               writing style canon
│   ├── architecture.md        entities, field types, dependency graph, session relay, connectivity, rules
│   ├── agent-contracts.md     CLAUDE.md specification — types, loading, precedence, write discipline
│   ├── patterns.md            close variants, sharpening, context levels, model routing, skill taxonomy
│   ├── cookbook.md            how to extend PhantomOS
│   └── extending.md           custom entities, sidecar schemas, extension architecture
│
└── internal/              maintainer-facing (contributor-only)
    ├── canon.md               design decisions locked into this workspace
    └── releases/              technical release manifests
        └── manifest/          schema mutations and breaking changes per version
```

## Navigation by audience

- **I want to use PhantomOS.** → `product/getting-started.md`, then `product/capabilities.md`.
- **I want to understand what PhantomOS is.** → `vision/prisms.md` first, then `vision/manifesto.md` if you want the thesis.
- **I want to build on PhantomOS or contribute.** → `system/voice.md` for the writing canon, `system/architecture.md` for technical architecture, `system/agent-contracts.md` for CLAUDE.md specification, `system/patterns.md` for taxonomies, `system/cookbook.md` for extension patterns.
- **I am an agent executing in PhantomOS.** → your contract is `CLAUDE.md` at the workspace root (plus the brand-level one when applicable); your capabilities are in `.skills/skills/`; your lexicon is `lexicon.md`; the operator's persistent preferences live in `operator/profile.json`.
- **I am integrating a new version or maintaining the template.** → `internal/canon.md` for locked decisions, `internal/releases/manifest/` for technical change history.

## Conventions

Every doc in this folder follows the canon in `system/voice.md`. Links across docs use relative paths. English throughout. No emojis. No name-dropping outside `vision/manifesto.md`.
