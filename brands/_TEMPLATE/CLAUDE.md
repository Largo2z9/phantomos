# Brand: {brand-name}

> Auto-loaded when working in this brand folder.
> Note. This file complements the parent CLAUDE.md (workspace root). Always open the workspace from the root folder, never open a brand folder directly. Opening just the brand folder loses the OS, skills, and all behavioral rules.
> Shared resources → `../../resources/` (reference by ID, never duplicate).
> Resource discovery → `../../index.json`.

## Ecosystem

Platforms this brand operates on. The agent uses these identifiers for on-demand API calls when the operator asks for data (campaigns, orders, emails, analytics).

| Platform | Account / Store | Status |
|----------|----------------|--------|
| Meta Ads | `act_XXXXXXXXX` | — |
| Shopify | `{slug}.myshopify.com` | — |
| Google Ads | `XXX-XXX-XXXX` | — |
| GA4 | `G-XXXXXXXXXX` | — |
| Klaviyo | — | — |

API tokens and secrets → `credentials.env` (gitignored, never in context).
Shared workspace tokens → `../../credentials_shared.env` (gitignored).

**Credential loading** — before any API call:
```python
from dotenv import load_dotenv; import os
load_dotenv(os.path.join(BRAND_PATH, 'credentials.env'))
# For workspace tools (Slack, ClickUp, Google Suite):
load_dotenv(os.path.join(WORKSPACE_ROOT, 'credentials_shared.env'))
```
Never display tokens in output. Install deps: `pip install requests python-dotenv --break-system-packages -q`

## Data Access

- **Sources** : `sources/` — raw files (briefs, PDFs, screenshots, exports). Never auto-loaded. No impact on context budget.

## Workspace State

- **Status**: `status.json` — completeness, freshness, flags (auto-maintained)
- **Todos**: `todos.md` — tasks, backlog, flags
- **Config**: `config.json` — brand-specific customization
- **Session relay**: `session-state.md` — rolling activity log, auto-maintained on every write (no manual rotation)
- **Learnings**: `learnings.json` — append-only operational facts (API workarounds, test results, compliance rules)

## Context DB — 7 Entities

| Entity | File | Status |
|--------|------|--------|
| Brand | `brand.json` | empty |
| Products | `products/{slug}/spec.json` | — |
| Offers | `products/{slug}/offers.json` | — |
| Audiences | `audiences/{slug}/profile.json` | — |
| Angles | `angles/{slug}/angle.json` | — |
| Learnings | `learnings.json` | empty |
| Strategy | `strategy.json` | empty |

### Context state

Context completeness is a continuous state, not a checklist. The agent reads `_snapshot.md` (auto-regenerated on every mutation) to know what is currently knowable about this brand and what the next operator-shareable input would unlock. Three reference depths exist (basics / enriched / operational) but they are descriptive, not prescriptive — the agent never asks the operator to "fill the boxes". Full narrative reference: `docs/system/patterns.md § Context Levels`.

## How to Reference Resources

- Catalogue entries: `{PREFIX}-{NN}` (e.g. `ANG-01`, `FMT-03`)
- Other resources: `id` field from `../../index.json`
- To find: read `../../index.json` → filter by `type` and `domain`
- Cross-refs in context files: use `ref` fields pointing to IDs in spec.json or index.json

## Field Types

All JSON files contain `_field_types`. See parent CLAUDE.md and docs/system/architecture.md for details. Agents must respect types: never fill derived fields manually, never inject decisions into any field.
