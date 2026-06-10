---
name: connect-source
description: >
  Connect an external platform (Meta Ads, Shopify, Klaviyo, GA4, etc.) to PhantomOS.
  Guides operator through credentials setup, scope choice (workspace or brand), and
  capabilities. Uses convention if available in resources/conventions/, otherwise invokes
  scope skill (BUILD mode) to map the new platform first.
  FR: "connecte meta ads", "connecte shopify", "branche une source externe", "connecte mes outils".
  EN: "connect meta ads", "connect shopify", "connect a source", "connect my tools".
type: orchestrator
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
subagent_safe: false
mode: interactive
triggers:
  - "connect {platform}"
  - "ajoute {plateforme}"
  - "branch {tool}"
  - "connect external tool"
  - "ajoute meta ads"
  - "ajoute shopify"
  - "connect a new source"
disambiguates_against:
  setup-brand: "setup-brand creates a new brand workspace. connect-source links an external platform to an existing brand or workspace."
  scaffold-extension: "scaffold-extension adds a custom entity to the substrate. connect-source adds a runtime data source to consume."
---

# connect-source, orchestrator

Connect any external platform to PhantomOS. Guides operator through credentials, scope, capabilities. Read top to bottom before acting.

---

## Phase 0, intent capture

Identify the target platform from operator input.

| Input pattern | Platform |
|---|---|
| explicit name (`connect meta ads`, `ajoute shopify`) | extract directly |
| category only (`connect a paid ads platform`) | ask which one with AskUserQuestion |
| ambiguous (`connect external tool`) | ask platform name |

If platform name is provided but doesn't match a known convention file in `resources/conventions/{platform}.json`, ask for confirmation : *"Plateforme '{name}' inconnue. C'est un nouveau outil ? Je lance scope BUILD pour le cartographier."*

---

## Phase 1, convention lookup

Check `resources/conventions/` :

| Result | Action |
|---|---|
| `{platform}.json` exists | **templated mode** : pre-fill auth method, credential keys, rate limits, capabilities from convention. Phase 2 = guided fill of runtime fields only. |
| no match | **untemplated mode** : invoke `scope` skill (mode BUILD, modifier `--for-skill=connect-source`) to map the platform. Output = new convention drafted. Operator validates. Then Phase 2. |

For untemplated mode, the scope invocation should ask :
- What does this platform do (category : paid_ads / analytics / ecommerce / email_sms / attribution / creative_intelligence / crm / custom) ?
- Auth method (api_rest / oauth / sdk / browser_only) ?
- API documentation URL ?
- Top 3 operations the operator wants the agent to perform ?
- Rate limits known ?

Save the resulting convention as `resources/conventions/{platform-slug}.json` with `_version: "0.1"` (operator-authored, not template-shipped).

---

## Phase 2, runtime fill

For each `credential_keys` entry in the convention, ask the operator :

```
Token / key value for {KEY_NAME} ?
(Will be stored in {credentials_location}/credentials.env, never in JSON)
```

Use AskUserQuestion for credential prompts. Never log credential values to chat or to any file other than the target credentials.env.

Then ask :

| Question | Field |
|---|---|
| Scope of this connection : workspace (mutualisé) ou brand-specific ? | `meta.scope` |
| If brand : which brand slug ? | `meta.brand_slug` |
| Account or property ID specific to this brand connection ? | `sources[].account_id` |
| Capabilities : read only, write only, both ? | `sources[].capabilities` |

For multi-tenant platforms (Meta BM, Klaviyo Partner, Shopify Partner), if a workspace-level connection already exists, ask :
*"Auth Meta workspace-level déjà configurée. Cette brand utilise un sub-account ({account_id}) sur le même token, ou une auth dédiée ?"*

If shared : set `resolves_to_workspace_auth: true`, credentials_ref pointer goes to workspace-level entry.

---

## Phase 3, write

Write to the appropriate `connected-sources.json` :

- Workspace scope → `operator/connected-sources.json`
- Brand scope → `brands/{slug}/connected-sources.json`

Use `write_to_context` with `mode: "proposed"` for review, then operator validates. Convention : append to `sources[]` array, never overwrite existing entries (use `platform` + `account_id` as unique key).

Update `meta.updated` timestamp.

---

## Phase 4, verify (optional)

If the convention has a `verify_connection` operation defined, invoke it (silent ping to platform API). Report back :

```
✓ {platform} connection verified ({account_id}, {capabilities}).
  Credentials stored at {credentials_location}/credentials.env.
  Sync status : active.
```

If verification fails or convention has no verify operation :

```
⚠ {platform} entry created. Verification not run (no test endpoint defined).
  Run /phantom {brand} to confirm sync status updates after first skill use.
```

---

## Phase 5, no orphan output

End with one contextual next-step proposal :

| Context | Suggestion |
|---|---|
| First connected source for this brand | *"Run audit-meta-account to test the connection on a real audit."* |
| Multi-tenant Meta BM, second brand | *"Run /phantom workspace pour voir tes brands connectés Meta."* |
| New custom platform (untemplated) | *"Convention drafted at resources/conventions/{platform}.json. Run validate-resources to check schema compliance."* |
| Klaviyo or email connected | *"Test le flow J+1 sur un account perso avant d'activer pour de vrai."* |

---

## Hard rules

- **Never log credentials in chat.** Tokens go to `credentials.env` directly via secure prompt. The chat output mentions only that the credential was stored, never the value.
- **Convention is source of truth.** If `resources/conventions/{platform}.json` says auth method is `oauth`, don't accept `api_rest` from operator without asking why.
- **One platform per `sources[]` entry.** A brand connecting Meta + TikTok = 2 entries.
- **Workspace-level resolution.** If platform is multi-tenant, prefer workspace-level auth + brand-level account_id resolution.
- **Untemplated mode = explicit scope invocation.** Never write a convention from scratch without the scope skill output. Operators new to a platform need the scope discipline to capture the right fields.
- **Read-after-write.** After writing to `connected-sources.json`, re-read the file to confirm the entry shape matches the schema. If validate-resources flags an issue, surface to operator immediately.

---

## Cross-references

- `resources/conventions/_TEMPLATE.json` : convention schema base
- `resources/conventions/{platform}.json` : platform-specific conventions (Meta, TikTok, Google Ads, GA4, Shopify, Klaviyo, TripleWhale shipped)
- `resources/schemas/connected-sources.schema.json` : runtime state schema
- `scope` skill : invoked for untemplated platforms (mode BUILD)
- `/phantom` slash command : reads connected-sources to display sync status in cockpit
