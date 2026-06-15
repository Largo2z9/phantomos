---
name: query-context
type: curator
version: "1.1.0"
isolation_scope: brand_only
layer: meta
recommended_model: haiku
reasoning_pattern: null
description: >
  Reads the workspace KB and returns relevant resources for agent consumption.
  Covers shared resources (resources/), single brand context (brands/{slug}/),
  and cross-brand queries (all brands).
  Read-only — never modifies files.
  FR: "trouve" "cherche" "donne-moi" "montre-moi" "qu'est-ce qu'on a sur" "quels frameworks" "quel routing pour" "contexte brand" "compare brands" "toutes les brands" "cross-brand".
  EN: "find" "get" "what do we have on" "show me" "lookup" "fetch context" "compare brands" "which brands have" "across all brands".
permissions:
  reads: [brand, product, offer, profile, learning, strategy]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: ingest-resource must have run at least once (index.json populated)
  postconditions: none — read-only
---

## Tone

Réponds avec les données demandées, en langage courant. L'opérateur ne voit pas d'où vient l'info (quel fichier, quel champ). Il voit la réponse.

# Skill: Query Resource

Interface de lecture standardisée pour tous les agents consumers.
Traduit une intention en langage naturel → ressources JSON prêtes à consommer.
Ne modifie rien. Ne crée rien. Ne logge pas dans CHANGELOG.

---

## Step 1 — Parse Intent

Extraire de l'input :

| Dimension | Quoi | Exemple |
|-----------|------|---------|
| `scope` | kb, brand, all_brands, ou auto | "angles disponibles" → KB / "brief Glowco" → brand / "quelles brands ont LTV > 500" → all_brands |
| `type` | type de ressource cherché (optionnel) | catalogue, routing, framework, sop… |
| `domain` | domaine métier | "messaging", "media buying", "CRO" |
| `context` | situation d'usage qui guidera la sélection | "cold traffic Meta, audience problem-unaware" |
| `brand_slug` | slug brand si scope = brand (optionnel si all_brands) | "glowco", "nestra" |
| `compare` | brand slugs à comparer (optionnel) | ["glowco", "nestra"] |

**Scope detection:**
- "brand X" ou slug explicite → `brand`
- "toutes les brands", "quelles brands ont", "cross-brand", "compare X vs Y" → `all_brands`
- "angles", "framework", "routing" sans mention de brand → `kb`
- Ambigu → tenter `kb` + `brand` en parallèle, merger les résultats

---

## Step 2A — Lookup Shared KB

1. **Lire `index.json`**
2. **Filtrer par type** si spécifié (utiliser `stats.by_type` d'abord pour vérifier que le type existe)
3. **Scorer chaque ressource candidate** :
   - +3 pts : `domain` match exact
   - +2 pts : tag overlap avec le contexte parsé (chaque tag matching = +1, max +2)
   - +1 pt : `type` match avec l'intent
4. **Sélectionner top 1-3 ressources** par score
5. **Lire les fichiers JSON** des candidats retenus
6. **Retourner** avec contenu + metadata

**Cas "routing"** : si l'intent mentionne une situation de décision (ex: "quelle approche pour une audience X"), prioriser les routing tables. Lire le routing + les catalogues référencés dans `catalogues_required`.

---

## Step 2B — Lookup Brand Context

1. **Identifier `brand_slug`** — depuis l'intent ou demander une seule fois si ambigu
2. **Lire `brands/{slug}/status.json`** pour état de complétude
3. **Pour toute query sur les learnings** — utiliser l'index en priorité :
   - Lire `brands/{slug}/learnings-index.json` (léger)
   - Filtrer par `scope`, `platform`, `type`, `tags` selon l'intent
   - Charger uniquement les entrées `learnings.json` dont les IDs matchent
   - Ne jamais charger `learnings.json` entier si l'index est présent
   - Si `learnings-index.json` absent → charger `learnings.json` entier + signaler index manquant
4. **Router selon l'intent** :

| Intent | Fichier(s) à lire |
|--------|------------------|
| Identité, positionnement, ton, preuves | `brand.json` |
| Marché, concurrents, awareness | `brand.json` → section `market` |
| Specs produit, mécanisme, bénéfices | `products/{slug}/spec.json` |
| Offres, pricing, bundles | `products/{slug}/offers.json` |
| Audience, psychologie, objections, douleurs | `audiences/{slug}/profile.json` |
| Vue complète brand (brief, onboarding) | `brand.json` + spec(s) + profile(s) principaux |

4. **Si status.json indique `completeness = empty` ou `draft`** sur l'entité demandée → signaler à l'agent appelant : "Entité {entity} incomplète ({status}) — données partielles."

---

## Step 2C — Cross-Brand Query (scope = all_brands)

Scan all brands and return aggregated or comparative results.

### Discovery

1. **List all brand slugs**: scan `brands/*/brand.json` (skip `_TEMPLATE/`, `_EXAMPLE/`)
2. **Read `status.json`** for each brand (quick health check)

### Query Types

**Filter query** — "quelles brands ont X ?"
Extract the filter condition from the intent. Scan the target field across all brands.

| Intent pattern | Target field | Condition |
|---------------|-------------|-----------|
| "brands avec LTV > X" | `brand.json → financials.customer_ltv` | numeric comparison |
| "brands avec offres actives" | `products/*/offers.json → offer_groups[].offers[]` (v2 schema) | any group has a non-empty offers array |
| "brands dans le secteur X" | `brand.json → meta.vertical` | string match |
| "brands avec audience X" | `audiences/*/profile.json → meta.name` | string contains |
| "brands incomplètes" | `status.json → wedge_complete` | = false |
| "brands stale" | `status.json → freshness` | any file stale |
| "brands avec learnings sur X" | `learnings.json → entries[].tags` | tag match |
| "brands sans stratégie" | `strategy.json → annual_goals` | array empty |

For unrecognized patterns: read the relevant entity from each brand, apply the condition, return matches.

**Compare query** — "compare X vs Y"
1. Parse brand slugs from intent (2-5 brands max)
2. Read same entities from each brand
3. Return side-by-side comparison table

Default comparison dimensions (if no specific dimension requested):
- `meta.vertical`, `meta.stage`
- `financials.aov`, `financials.monthly_revenue`, `financials.roas_breakeven`
- `positioning.value_proposition`
- `market.competitors[].length` (number of declared competitors)
- Product count, audience count
- `status.json.wedge_complete`, context level (Tier 1/2/3)

**Aggregate query** — "résumé cross-brand", "portfolio overview"
1. Read all brands' `status.json` + `brand.json` (meta + financials only)
2. Return aggregated view:
   - Total brands, brands by stage, brands by vertical
   - Revenue range (min/max/avg monthly_revenue)
   - Completeness distribution (how many Tier 1/2/3)
   - Stale brands count

### Output Format — Cross-brand

**Filter result:**
```
[QUERY RESULT — cross-brand filter]
Filter: {condition}
Matches: {N}/{total brands}

| Brand | {relevant field} | Context Level |
|-------|-----------------|---------------|
| {slug} | {value} | Tier {1/2/3} |
| {slug} | {value} | Tier {1/2/3} |

No match: {slugs that didn't match}
```

**Compare result:**
```
[QUERY RESULT — compare: {brand1} vs {brand2}]

| Dimension | {brand1} | {brand2} |
|-----------|----------|----------|
| Vertical | {val} | {val} |
| AOV | {val} | {val} |
| Positioning | {val} | {val} |
| Products | {count} | {count} |
| Audiences | {count} | {count} |
| Context Level | Tier {N} | Tier {N} |
```

**Aggregate result:**
```
[QUERY RESULT — portfolio overview]
Brands: {N} total | {N} active | {N} paused
Context: {N} Tier 1 | {N} Tier 2 | {N} Tier 3
Revenue: {min}€ — {max}€ (avg {avg}€)
Health: {N} stale | {N} incomplete wedge
```

### Performance

- Cross-brand queries read multiple files. For >10 brands, read only `status.json` + `brand.json` (meta/financials) first, then drill into specific entities only for matching brands.
- Max 20 brands per cross-brand query. Beyond that, suggest filtering first.

---

## Step 3 — Format Response

Retourner les ressources dans un format exploitable directement par l'agent consumer :

### Pour shared resources :
```
[QUERY RESULT — {type}: {slug}]
Source: resources/{type}/{slug}.json
Domain: {domain} | Tags: {tags}
Relevance: {score}/{max_possible}

{contenu JSON de la ressource}
---
```

### Pour brand context :
```
[QUERY RESULT — brand context: {brand_slug}]
Entity: {entity type} | Completeness: {status}

{contenu JSON de l'entité}
---
```

### Si aucun résultat :
```
[QUERY — no match]
Intent: {intent parsé}
Searched: {types/domains/brands cherchés}
Closest: {slug du plus proche avec score} (score trop bas pour être retourné)
Suggestion: run ingest-resource to add relevant content.
```

---

## Patterns fréquents

**Agent hooks-generator** cherche les angles + routing awareness :
→ query("angles publicitaires + routing awareness-angle, contexte cold traffic problem-unaware")
→ retourne : `catalogues/angles.json` + `routing/awareness-angle.json`

**Agent media buyer** prépare un brief brand :
→ query("contexte complet brand glowco")
→ retourne : `brand.json` + `spec.json` principal + `profile.json` principal

**Agent copywriter** cherche le ton d'une brand :
→ query("brand tone voice glowco")
→ retourne : `brand.json` → sections `identity` + `tone`

**Agent performance** cherche les KPIs de référence :
→ query("sop pilotage COS, formules métriques")
→ retourne : `sops/piloter-cos.json`

**Operator multi-brand** cherche les brands avec offres manquantes :
→ query("quelles brands n'ont pas d'offres ?")
→ retourne : table avec brands filtrées, offers_missing flag

**Operator compare** compare deux brands :
→ query("compare glowco vs nestra")
→ retourne : table comparative (vertical, AOV, positioning, products, audiences, context level)

**Agent portfolio** veut un résumé global :
→ query("portfolio overview")
→ retourne : agrégat (N brands, revenue range, completeness distribution, stale count)

---

## MCP Interface — external agents

query-context can be exposed as an MCP server tool for external agents (custom agents, n8n workflows, dashboards).

### Tool Definition

```json
{
  "name": "query_phantomos",
  "description": "Query a PhantomOS workspace for brand context or shared KB resources. Read-only.",
  "input_schema": {
    "type": "object",
    "properties": {
      "scope": {
        "type": "string",
        "enum": ["kb", "brand", "all_brands", "auto"],
        "description": "Search shared KB, single brand, all brands (cross-brand), or auto-detect. Default: auto."
      },
      "brand_slug": {
        "type": "string",
        "description": "Brand slug (required if scope=brand). Example: 'glowco'."
      },
      "entity": {
        "type": "string",
        "enum": ["brand", "product", "offer", "audience", "all"],
        "description": "Entity type to query (brand scope only). Default: all."
      },
      "product_slug": {
        "type": "string",
        "description": "Product slug for product/offer queries. Optional."
      },
      "audience_slug": {
        "type": "string",
        "description": "Audience slug for audience queries. Optional."
      },
      "resource_type": {
        "type": "string",
        "enum": ["catalogue", "routing", "framework", "sop", "quality-spec", "convention", "template"],
        "description": "KB resource type filter (kb scope only). Optional."
      },
      "query": {
        "type": "string",
        "description": "Natural language query describing what you need. Example: 'angles for cold traffic problem-unaware audience'."
      },
      "max_results": {
        "type": "integer",
        "default": 3,
        "maximum": 5,
        "description": "Max resources to return."
      }
    },
    "required": ["query"]
  }
}
```

### MCP Server Configuration

When implemented, the MCP server config lives in the workspace root:

```json
// .mcp.json (workspace root)
{
  "mcpServers": {
    "phantomos-query": {
      "command": "node",
      "args": [".skills/mcp/query-server.js"],
      "env": {
        "WORKSPACE_ROOT": "."
      }
    }
  }
}
```

### Implementation Notes

- The MCP server wraps Steps 1-3 of this skill into a programmatic tool
- Same scoring logic, same hard rules (read-only, max results, no interpolation)
- Returns JSON (not formatted text) — MCP consumers parse JSON directly
- No auth layer in V1 (local-only assumption). V2: API key or workspace token.
- Rate limiting: 60 calls/minute per workspace (prevent runaway agents)
- The workspace path is resolved from `WORKSPACE_ROOT` env var

### Implementation Status

**Spec complete.** MCP server implementation in `.skills/mcp/query-server.js`.
Covers: kb scope, brand scope, all_brands scope (filter, compare, aggregate).
See `.skills/mcp/README.md` for setup instructions.

---

## Hard Rules

- **Read-only** — aucune écriture, aucune modification
- **Jamais de CHANGELOG** — les queries ne laissent pas de trace
- **Max 3 ressources retournées** (5 via MCP) — qualité > quantité. Si l'agent a besoin de plus, relancer avec un intent plus précis
- **Toujours inclure le path source** dans la réponse — l'agent consumer peut aller chercher plus si besoin
- **Ne pas interpoler ni synthétiser** le contenu des ressources — retourner le JSON tel quel, l'interprétation appartient à l'agent consumer
- **Si brand incomplète**, signaler mais retourner quand même ce qui existe
- **MCP = same logic** — the MCP interface exposes the exact same query engine, not a separate implementation
- **Cross-brand max 20 brands** — beyond that, suggest filtering first to avoid performance degradation
- **Cross-brand reads meta first** — for >10 brands, only read status.json + brand.json meta/financials, then drill into matching brands
- **Never expose cross-brand data to restricted brands** — if a brand has restricted flag in config, skip it in cross-brand results
