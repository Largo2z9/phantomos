# PhantomOS

PhantomOS is an agentic workspace for DTC operations. You encode your brand once (products, audiences, strategy, learnings), the agent reasons and executes on it across sessions, and every validated output enriches your knowledge for what's next.

The methodology lives in the workspace, not in chat threads. Context is read from disk before every agent response. Intelligence compounds with use across every session, every brand, every channel.

The system targets DTC operators whose paid acquisition is a craft · brand founders past month 6, growth leads at agencies running multiple DTC clients, solo operators spending most of their time on Meta, TikTok, and Google Ads. It is not a chatbot with memory.

The product is the workspace plus the DTC paid kit. PhantomOS ships with the full DTC paid acquisition kit : angles library, creative mechanics, proof types, audience encoding patterns, advertorial LP frameworks, hook formulas. Day-1 operational on a first brand, no encoding from scratch required. The platform itself is extensible if operating outside DTC, the kit is optimized for DTC paid.

**Best fit.** DTC brand founders past month 6 with stable ROAS (return on ad spend). Growth leads at agencies running 3 to 15 DTC accounts. Solo operators productizing their paid acquisition methodology. **Conditional fit.** DTC operators month 3 to 6 (still finding what works), small DTC teams of 2 to 4. **Not fit today.** Pre-traction founders, info-products, B2B services, agencies focused on social organic, performance creators focused on volume. Detailed audit in [`docs/product/fit.md`](docs/product/fit.md).

## Requirements

PhantomOS runs inside [Claude Code](https://claude.ai/code), the Anthropic CLI. Not ChatGPT, not Cursor : the agent needs filesystem access to read and write the workspace. A Claude Pro, Team, or Max subscription is required ; files stay on the operator's machine, the agent calls the Anthropic API for inference.

## First steps

From an empty clone to a first asset shipped : about thirty minutes.

1. **Open the workspace in Claude Code.** Open the root folder, not a subfolder.
2. **Say hi.** On first run, the agent detects no brand is configured and starts onboarding. It asks the operator's DTC stack (Shopify, Klaviyo, Meta, TikTok, Google) and seniority on paid.
3. **Drop the brand URL.** The agent scans for 3 to 5 minutes, pre-fills the brand at roughly 60% of Level 1 completeness, hands back for validation.
4. **Connect the sources.** Meta Ads, TikTok Ads, Google Ads, Shopify, Klaviyo, GA4 : connect on demand as needed.
5. **Run the first skill** : `audit-meta-account` for a concrete setup diagnostic, or `produce-paid-angles` to generate a first angle batch from the encoded audiences.

No package to install. Everything ships in this repo. Sessions can stop mid-setup and resume the next day. Nothing told to the agent is lost.

## What lives here

- **`CLAUDE.md`** : root agent contract. Auto-loaded every session.
- **`lexicon.md`** : the operator-facing vocabulary used in this workspace.
- **`brands/`** : one folder per brand operated. Encoded knowledge per brand.
- **`resources/`** : shared library across brands. Frameworks, angles, creative mechanics, platform conventions.
- **`.skills/skills/`** : executable capabilities the agent triggers on context.
- **`docs/`** : product, vision, system docs. Start at `docs/README.md`.
- **`CHANGELOG.md`** : version history.

External tools (Meta Ads, TikTok Ads, Google Ads, Shopify, Klaviyo, GA4, TripleWhale) connect on demand when a skill needs them. No continuous sync.

## The one rule

The operator guides the agent through language. The agent handles file operations internally ; results are surfaced, not the mechanics. If something is wrong, *"fix X on the brand"* records the change with a trace.

## Install Claude Code (one-time)

```
npm install -g @anthropic-ai/claude-code
```

Then `cd` into this folder and run `claude`. Auth on first launch.

## Updates

PhantomOS ships incremental releases. When a new version is available, a direct notification is sent with a one-line summary. To install :

1. `git pull` (if cloned from git) or rsync the new template files into the workspace folder.
2. In Claude Code, *"update workspace"*. The `update-workspace` skill reads installed version vs target, applies every change.

Operator data is preserved end-to-end : brand folders, operator settings, credentials, learnings. Only template files (skills, docs, schemas) are updated.

Detail per release : `docs/internal/releases/manifest/{version}-manifest.json`. Human-readable history : `CHANGELOG.md`.

## Going further

- **To use PhantomOS on a DTC brand** → `docs/product/getting-started.md`
- **To understand the architecture** → `docs/vision/prisms.md`
- **To extend it for non-DTC use cases** → `docs/system/extending.md`
- At any moment in a session, type `?` or `skills`. The agent pulls the right section from `docs/product/capabilities.md`.
