# Capabilities

What the workspace covers today, what's next, what's explicitly out of scope. Not a feature list — a map of your work.

At any moment in a session, type `?` or `skills` and the agent surfaces the section relevant to your current context.

## The four layers

PhantomOS organizes your work on four layers that feed each other.

- **Strategy.** Direction: what makes the brand unique, roadmap, portfolio, competitive landscape, goals.
- **Research.** Input to decisions: voice of customer, setup audits, offer diagnostic, competitor analysis.
- **Production.** Output: creative briefs, copy (emails, landing, ads), concepts, editorial calendar.
- **Ops.** Measurement and loop: campaign piloting, reporting, A/B tests, learnings that feed back into strategy.

Each layer feeds the next. Ops learnings loop back into strategy. It's a cycle, not a stack.

The four-layer structure is illustrated here on the DTC-marketing kit shipped by default in V1. The same structure applies to any domain the operator chooses to encode : a consultant runs Strategy (positioning) → Research (client intel) → Production (deliverables) → Ops (engagement learnings). A coach runs Strategy (curriculum frame) → Research (cohort signals) → Production (sessions, materials) → Ops (cohort feedback). The kit demonstrates ; the structure is agnostic.

## Maturity state by layer

Current version: V1.

| Layer | What V1 ships | What arrives with skills to build | V2 roadmap |
|---|---|---|---|
| **Strategy & Macro** | Brand identity, positioning, annual roadmap, portfolio, strategic learnings | Goal tracking, auto-generated investor updates, risk registry | Scenario planning, forecasting |
| **Research & Analysis** | Product/brand scan, doc ingestion, Meta setup audit | Full voice of customer (Reddit, Trustpilot, YouTube), market comparatives, competitor ads tracking | Social listening, trend detection |
| **Production & Creative** | Briefs, copy, concepts, hooks, emails, landing copy, **visuel paid composé en couches (packshot officiel + logo + badges, pixel-exact)** | Per-channel production capability library | Video generation, motion design |
| **Ops & Iteration** | Learning capture, session relay, environment validation, platform setup audit | Daily KPI dashboard, LTV/CAC cohort, creative fatigue detection, A/B test tracking, auto weekly reporting | Attribution reconciliation, anomaly detection |

Pick the layer where your current work lives. The rest fills as work requires it.

## What V1 ships today

> The capabilities below are demonstrations of what the workspace produces once it is encoded — they are not the substrate itself. The substrate is the workspace, its encoding disciplines, the agent's reasoning mechanics, and the extensibility. The kit shipped here illustrates these on DTC marketing and direct response copy. Operators in other domains encode their own kit, with the same mechanics underneath.

- Configure one or several brands and keep their context up to date without re-briefing.
- **Start the day fast** — on-demand session briefing (portfolio health, pending validations, what's in flight).
- **Pick up where you left off** — clean resumption after absence, the agent reconstructs the last active thread.
- Ingest briefs, docs, exports. The agent files them in the right layer.
- Ask contextual questions (*"tone of brand X"*, *"customer objections Y"*) and get answers without re-setup.
- Produce creative deliverables, hooks, angles, scripts, emails, landing copy, calibrated on brand context.
- **Atlas brand · cartographie holistique data e-commerce** v2.36+. Concept canonique upstream qui structure la matière brand (audiences + products + angles + creatives + scoring + verbatims + tests). Navigable via `/phantom` cockpit. Skills d'enrichissement progressif P0 → P5 (snapshot-brand · define-specs · profile-audience · produce-paid-angles · score-matrix · compose-creative · etc.).
- **Atlas canon copy** (v2.26+). Shared typed registry, 11 layers × 58 fiches (frameworks, hooks, angles, awareness levels, voice archetypes, headline formulas, objections, offer construction, leads, deliverable formats, persuasion). Sources : Schwartz, Cialdini, Halbert, Sugarman, Hormozi, Carlton, Jung. Skills consume the registry at runtime AND feed it via `validations[]` append-only on operator-gated promotion. The atlas becomes brand-specific with use (living atlas).
- **Production by canon composition** (v2.27+). `produce-paid-angles`, `produce-copy-brief`, `mine-voc`, `learn-from-session` operate by canon reference. Each output carries explicit lineage (audience, awareness stage, hook canon id, framework canon id, angle canon id, archetype canon id), enabling traceability and reproducibility across sessions.
- Audit Meta configuration (pixel, attribution, account structure, naming, DSA).
- **Adversarial review on any deliverable** — multi-expert panel challenges a plan, brief, strategy, or setup. Zero compliments, verdict with priority actions.
- Capture learnings (API workarounds, compliance rules, observed patterns) and promote them when they become universal.
- Compare brands across customers, offers, completeness levels.
- Validate workspace integrity (broken references, missing fields, obsolete learnings).

## What arrives with primitives connected

As soon as you connect Meta Ads, Shopify, Klaviyo, Google Ads, GA4, ClickUp, Notion, or Google Calendar, the workspace unlocks a wider surface. **None of the items below ships as a ready-made skill in V1** — they get built on demand via `build-agent` or arrive in later versions.

- Auto daily and weekly reporting (headline KPIs, flags, recos).
- LTV cohorts by vintage, multi-channel attribution.
- Creative fatigue detection, quick budget wins, ad sets kill list.
- RFM segments, churn tracking, Klaviyo flow audit.
- Stock alert, real margins per SKU, monthly P&L.
- Support tickets cross-referenced with audience objections, FAQ gaps, copy gaps.

In V1 you get the context substrate and the core skills. The agent can be asked to build new skills against the connected primitives as needs come up.

## Production créa visuelle

PhantomOS produit la créa visuelle de tes campagnes paid, sans repasser par un designer pour chaque variation. Le principe : tu prépares **une fois** les briques canon de ta marque (photo produit officielle, logo, badges, mascotte, patterns), ensuite le système les compose en couches sur chaque nouvelle pub. Pixel-exact, sans dérive de marque, sans regénérer le produit à chaque ad.

- **Génère une fois la photo officielle de ton produit, réutilise-la partout.** Tu donnes ton produit en input, PhantomOS te sort un packshot canon que tu valides. Sur toutes tes pubs suivantes, le système réutilise cette photo intacte au lieu d'en regénérer une variante différente à chaque fois. Plus de dérive visuelle entre deux ads de la même campagne.
- **Importe tes assets de marque une fois, ils servent partout.** Logo, badges (certif bio, made in France, awards), mascotte, patterns de fond. Tu apportes le fichier ou tu pointes ton site, PhantomOS canonise et range. Les pubs suivantes les utilisent automatiquement, pas de re-upload à chaque création.
- **Récupère ton logo et tes badges depuis ton site web automatiquement.** Si tu n'as pas tes fichiers sous la main, PhantomOS va les chercher sur ton site, identifie ce qui est logo / badge / certification, et importe le tout dans ton workspace.
- **Génère une pub complète (visuel + brief copy) en une opération.** Tu choisis l'angle, le système compose : packshot officiel + logo + badges en couches, pixel-exact, plus le brief copy aligné. Tu obtiens un livrable Meta-ready, branding consistant d'une ad à l'autre.
- **Décompose une pub d'un concurrent (ou la tienne) pour comprendre ce qui marche.** Tu donnes une ad existante, PhantomOS la décompose en briques (angle, hook, mécanique créative, structure visuelle). Tu récupères les patterns transposables sans copier.

L'enjeu derrière : tu sors du loop *"chaque ad redessine le produit depuis zéro et le branding dérive"*. La photo officielle et les assets canon sont des **constantes** dans ta pipeline, les couches sémantiques (angle, audience, hook) sont les **variables**. Tu scales le volume sans casser la cohérence visuelle.

## What stays out of scope

- Real-time social trends (TikTok, Instagram).
- Live social listening community.
- Video editing and motion design.

These blocks are handled by native specialized tools (Motion, Foreplay, Triple Whale, CapCut). PhantomOS does not compete on that surface.

## Workflows you can build on top

The shipped skills are the foundation, not the ceiling. PhantomOS is a platform where the operator composes skills, orchestrators, agents, and sub-agents into workflows specific to their business. The value scales with context density — the more the workspace knows about your brands, audiences, products, and past performance, the more coherent the output at volume.

The core pattern is **parametric composition**: decompose a proven craft into atomic variables, store them as curated banks in `resources/registries/` and `resources/routing/`, then traverse the matrix of their combinations to generate output at volume. PhantomOS ships registries out of the box — `angle-registry.md` (14 psychological angles), `creative-mechanics-registry.md` (28 mechanics), `proof-registry.md` (14 proof types ranked), `awareness-angle-matrix.md` (awareness level × angle router), `hook-formulas.md` (15 hook families). These are not documentation. They are the parameter space agents walk at generation time.

Three patterns operators build on PhantomOS (not shipped as ready skills in V1 — assembled via `build-agent` or by chaining existing skills):

**Mass creative generation with coherence.** One hundred Meta statiques in ten minutes, not by writing a hundred blank prompts but by walking `creative-mechanics-registry × angle-registry × audience profile × proof-registry × format`. Each variant is grounded in coordinates from stored banks, anchored in the product benefit from `spec.json`, the audience pain from `profile.json`, and what converted before from `learnings.json`. Sub-agents generate variants in parallel; the main agent ensures the set covers distinct angles and does not duplicate. High variety + high coherence because the atoms are curated and the combinations are grounded.

**Klaviyo flow design grounded in existing signal.** Build a welcome flow for a new brand by reusing what converted in a sibling brand's workspace (if you run a portfolio), crossed with LTV data and segmented by current audience profiles. The workflow picks which segments need which cadence, which copy family has already performed, and iterates on what underperformed. Each email is grounded in an encoded decision, not generated from a blank prompt.

**Cross-brand performance review.** A recurring audit skill reads `learnings.json` across the portfolio, identifies patterns that generalize, and proposes promoting them to `resources/` as shared playbooks. Proactive by design — it surfaces what the operator has not yet consolidated, rather than waiting to be asked.

The common pattern: dense context plus orchestrated skills equals proactive, consistent output at volume. This is where PhantomOS becomes a platform, not just a workspace. Build your own workflows via `build-agent` in direct or guided-mission mode. See [`../system/cookbook.md`](../system/cookbook.md) for concrete build patterns.

## How the work compounds

You file nothing yourself. You talk, the agent classifies into the right layer. Each correction you make becomes a rule the agent applies on the next request — the context gets denser with use, not with effort.

Come back whenever. Everything persists. The agent picks up where you left off.

## When PhantomOS pays off

The return on setup is not instant for every profile. The honest curve depends on three conditions.

**Time in the saddle.** The first value is felt from session one — context loaded, no re-briefing. The compound, where encoded decisions reduce cognitive load and speed up delivery, lands between month three and month six of active use for a DTC solo operator, faster for a consultant running five to eight client brands. Pre-traction founders who adopt day one typically encode decisions that will pivot within weeks; the system densifies on a dead thesis. See `fit.md` for adoption timing by profile.

**Capture discipline.** The moat is the continuous capture process, not the graph at any moment. An operator who skips logging corrections for two weeks gets a Notion clone that nobody reads. The agent proposes capture after every deliverable and `learn-from-session` batches on demand, but neither replaces the operator's reflex to log the reasoning behind a correction, not just the correction itself.

**Operator comfort with Claude Code.** Initial setup uses Claude Code (a command-line interface) for around fifteen minutes via a guided flow. After that, the web app and the desktop app work against the same workspace, with zero re-setup. An operator with no terminal experience encounters one short guided session on day one, then the surface choice is theirs.

See [`fit.md`](fit.md) for a full audit of best fit, conditional fit, and misfit profiles.

## Scénarios Notion ↔ PhantomOS

PhantomOS expose un bridge bidirectionnel optionnel avec Notion via le skill `sync-notion-atlas` (Layer 1 MCP, opt-in). Notion sert d'UI navigable pour les opérateurs qui préfèrent une interface tabulaire, PhantomOS reste la source of truth canonique. Doctrine complète · `docs/system/notion-bridge-doctrine.md`.

**Scénario 1 · Onboard from Notion existant.** L'opérateur a déjà peuplé son workspace Notion (manuellement ou via collab agency) avec les 11 collections canon (Produits · Personae · Pain Points · Angles · etc.). Commande `/sync-notion-atlas {brand_slug} --mode=pull {notion_url}` · le bridge ingère les rows Notion, applique les mappings cross-platform, stage chaque mutation en mode proposed côté PhantomOS, valide silencieusement, surface synthesis 5 sections. L'opérateur accepte via `pending-validations.md`. Cycle complet en 5-10 minutes selon volume.

**Scénario 2 · Export atlas vers Notion pour client review.** L'opérateur a peuplé PhantomOS via `build-atlas-complete` ou skills individuels. Pour exposer le state en UI navigable pour client agency ou collab externe · `/sync-notion-atlas {brand_slug} --mode=push {notion_parent_url}` · le bridge crée les 11 databases Notion sous le canvas parent, populate les rows depuis les JSON brand, set les relations cross-collections. URL workspace Notion partagée au client en 3-5 minutes.

**Scénario 3 · Workflow 4-zones in Notion → push PhantomOS.** L'opérateur préfère raisonner en UI Notion (drill-down persona × pain points × angles activables filtré). Il bosse en Notion, ajoute des angles, valide des audiences, met à jour le roadmap. En fin de session · `--mode=push` (si PhantomOS antérieur) ou `--mode=pull` (si Notion canon de session). PhantomOS ingère le travail opérateur, les skills downstream (produce-paid-angles, compose-creative) consument la nouvelle matière.

**Scénario 4 · Audit gap Notion vs PhantomOS.** L'opérateur veut vérifier ce qui diverge entre les 2 systèmes après une période d'édition double. `--mode=diff` (v2.59+) compare row par row, surface les conflits, liste les divergences. L'opérateur arbitre par item · garder Notion · garder PhantomOS · merger.

**Scénario 5 · Friction tracking Notion → push.** Une équipe d'opérateurs logge les frictions usage (verbatims clients, retours support) directement dans Notion sous la collection Frictions usage. `--mode=pull` ingère les frictions dans `brands/{slug}/frictions/{FRC-NN}.json` (schema canon v1.0). Skills downstream (produce-paid-angles, score-matrix) consument les frictions pour prioriser les territoires qui adressent les pains réels.

**Scénario 6 · Roadmap planning Notion → consume score-matrix.** L'opérateur veut planifier les angles à produire sur 30/60/90j. Il peuple `Roadmap [angles/audiences]` dans Notion (timeline + Mix + statuts production). `--mode=pull` ingère dans `brands/{slug}/roadmap.json`. Le skill `score-matrix` consume le roadmap pour scorer les territoires en cours/à venir, surface top-3 priorités opérationnelles. La roadmap Notion devient la source de la matrice scorée PhantomOS.

**Scénario 7 · Brief créa start Notion → execute PhantomOS.** L'opérateur a sélectionné un angle prioritaire dans Notion (Angle filtré par persona) et veut générer le brief créa + visuels. Au lieu de freestyler dans Notion · `/creative-brief-composer {brand_slug} {angle_id}` côté PhantomOS · chain produce-copy-brief + compose-creative + variants. Le brief généré peut ensuite être push back en Notion via `--mode=push` partial (collection Full funnel Meta uniquement).

**Scénario 8 · Agency sync 5 brands Notion vers single PhantomOS.** Un opérateur agency gère 5 à 10 brands clientes, chaque brand a son workspace Notion. Isolation `brand_only` strict respectée · 1 sync per brand · `/sync-notion-atlas brand-a --mode=pull {notion_url_a}`, puis `/sync-notion-atlas brand-b --mode=pull {notion_url_b}`, etc. Le bridge ne fuit JAMAIS de data cross-brand. L'opérateur peut ensuite tourner les skills agency cross-brand (analyse de patterns transverses, promotion learnings cross-brand) côté PhantomOS qui agrège les 5 instances localement sans dépendance Notion runtime.
