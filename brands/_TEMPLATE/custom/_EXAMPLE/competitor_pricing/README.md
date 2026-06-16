# competitor_pricing · example custom entity

Illustrative custom entity tracking competitor pricing over time. Copy this folder to start your own similar extension, or read through it to understand the canonical shape of a custom entity.

## Purpose

Track pricing observations for products sold by competitors. One file per (competitor, product) pair. Observations append over time as the operator or a scraper skill captures new prices.

## Files

- **`schema.json`** · JSON Schema for instances of this entity. Declares canon `_version`, `_schema`, `_field_types` and validates required fields at write time.
- **`nike-airmax-97.json`** · example instance, one (competitor, product) pair with three observations.
- **`README.md`** · this file.

## Cross-references to core entities

- `product_slug` resolves to `brands/{brand_slug}/products/{product_slug}/spec.json`. If the referenced product is renamed or deleted, `validate-resources` flags the orphan.

## Writing new observations

New observations are appended via `write_to_context`, never edited in place:

```
write_to_context(
  field_path="custom.competitor_pricing.nike-airmax-97.observations[]",
  value={observed_at: "...", price: ..., currency: "..."},
  source="scraper:nike.com",
  confidence=0.95,
  mode="direct"
)
```

## Index.json registration

Add once per entity type (not per instance):

```json
{
  "type": "competitor_pricing",
  "scope": "brand",
  "schema": "brands/{slug}/custom/competitor_pricing/schema.json",
  "cross_refs": ["product_slug → brands/{slug}/products/{product_slug}/spec.json"],
  "owner_skill": "custom:scrape-competitor-pricing"
}
```

## Clone this example

To use this as a starter for your own custom entity:

```bash
cp -R brands/_TEMPLATE/custom/_EXAMPLE/competitor_pricing brands/{your-slug}/custom/{your-entity-type}
```

Then: rename the folder, adjust `schema.json` to your fields, delete the example instance, update `index.json`, create a skill in `.skills/skills/custom/` that populates it.
