# Custom entities

Operator-built data types beyond the six core entities (brand, product, offer, audience, learnings, strategy). Live here when scoped to this brand specifically.

Each custom entity type follows convention:

```
custom/
├── {entity_type}/
│   ├── schema.json       JSON Schema · required, canon conventions (_version, _schema, _field_types)
│   ├── README.md         purpose + cross-references to core entities
│   ├── {instance}.json   one per data instance (or one aggregate file, depending on shape)
```

Every extension is:
- Registered in `../../../index.json` for agent discoverability.
- Validated by `validate-resources` against its declared schema.
- Visible to `query-context` via convention walk of this folder.

**Rules** · see `docs/system/extending.md` for the full specification.

Starter examples an operator typically adds:
- `competitor_ads/` · Meta Ads Library scrape with detected angle.
- `pricing_watchlist/` · competitor pricing tracked over time.
- `financial_cohorts/` · LTV / CAC / contribution margin per acquisition cohort.
- `hook_library/` · tested hooks with performance score.

Leave this folder empty until you actually need an extension. Empty custom folders cost nothing. Unused extensions add noise.
