# Where Does It Go?

> Decision tree for placing any piece of information in PhantomOS.
> Use when you're not sure if something is a brand entity, a resource, or a learning.

---

## The core question

**"Is this knowledge reusable by another brand, or is it specific to mine?"**

```
Reusable by other brands?
├─ YES → resources/ (shared KB)
│   └─ Another e-com brand could use it?
│       ├─ YES → resources/{type}/
│       │   ├─ A list or catalog       → catalogues/
│       │   ├─ A decision table        → routing/
│       │   ├─ A methodology/model     → frameworks/
│       │   ├─ A step-by-step process  → sops/
│       │   ├─ A quality checklist     → quality-specs/
│       │   ├─ A platform rule         → conventions/
│       │   └─ A reusable format       → templates/
│       └─ NO → brands/{slug}/learnings.json
│               (it's a rule that applies to this brand only)
│
└─ NO → brands/{slug}/ (brand entity)
    └─ Which entity?
        ├─ Who the brand is            → brand.json
        ├─ What it sells               → products/{slug}/spec.json
        ├─ How it sells it             → products/{slug}/offers.json
        ├─ Who buys it                 → audiences/{slug}/profile.json
        ├─ What it's learned           → learnings.json
        └─ What it's trying to achieve → strategy.json
```

---

## Common cases

| "I have a..." | Goes in... |
|---|---|
| Tone of voice guide (full doc) | `sources/` (archive) + tone extracted to `brand.json → tone` |
| Brand origin story | `brand.json → origin_story` |
| Product specification sheet | `products/{slug}/spec.json` |
| Current promotions | `products/{slug}/offers.json` |
| Customer persona description | `audiences/{slug}/profile.json` |
| Copywriting framework we use for all brands | `resources/frameworks/` |
| Instagram compliance rule discovered via testing | `brands/{slug}/learnings.json` |
| Platform ad policy that applies to every brand | `resources/conventions/` |
| Email template we reuse | `resources/templates/` |
| Active campaigns list | `resources/templates/campaigns-active.json` (see template) |
| Competitor analysis | `brands/{slug}/brand.json → market.competitors[]` |
| Annual revenue targets | `brands/{slug}/strategy.json` |

---

## The three traps

**Trap 1 · Dumping docs into resources/**
A 40-page brand guidelines PDF is not a resource. Extract the 3 key facts (tone adjectives, forbidden words, visual rules) into the right entity fields. Archive the PDF in `sources/`.

**Trap 2 · Putting brand-specific rules in shared resources/**
"We never discount more than 20%" is a brand rule → `learnings.json`. A shared resource is something any operator could use for any brand.

**Trap 3 · Creating a new entity type**
There are 6 fixed entities. Campaigns, projects, briefs, reports · these are operational metadata → `resources/templates/` or `strategy.json`. If you're unsure, use `learnings.json` temporarily and promote later.

---

*When in doubt: ask the agent "where should I put [X] for [brand]?" · it knows this tree.*
