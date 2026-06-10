# Agent Cookbook. PhantomOS

> Concrete patterns to build skills consuming PhantomOS context.
> Each recipe: what to load, in what order, what to do if a field is missing.
> Before building any skill that consumes these patterns, read `docs/system/patterns.md § Skill Taxonomy` (every skill MUST declare a `type:` field) and `§ Skill Philosophy` (complex tasks require codified expert methodology, not improvised reasoning).

---

## Pattern 1 · Generate product copy (hook, description, email)

**When to use**: you want to produce advertising or editorial content for a product.

### What to load

```
1. brand.json → identity.name, positioning.value_proposition, tone_of_voice.style, tone_of_voice.banned_words
2. products/{slug}/spec.json → identity.name, description, benefits[], problems_solved[], pricing.price
3. audiences/{slug}/profile.json → identity.label, pain.primary_problem, psychology.objections[]
4. (optional) products/{slug}/offers.json → active offer for CTA with right price
```

**Mandatory order**: brand → spec → profile. Tone comes from brand, product from spec, target from profile.

### Behavior if field is missing

| Missing field | Behavior |
|---|---|
| `tone_of_voice.style` | Generate in neutral language. Flag at end of output: "⚠ Brand tone not configured, content in neutral style." |
| `positioning.value_proposition` | Use `spec.description` as fallback. Flag. |
| `benefits[]` empty | Deduce from `description` (extraction, not invention). Flag. |
| `profile.psychology.objections[]` empty | Generate without addressing objections. Flag. |
| `pricing.price` null | Omit price from CTA. Never invent a number. |

### Load template (pseudo-code)

```
brand = query("brand.json", fields=["identity.name", "positioning", "tone_of_voice"])
product = query("products/{slug}/spec.json", fields=["identity", "benefits", "problems_solved", "pricing"])
audience = query("audiences/{slug}/profile.json", fields=["pain", "psychology.objections"])

if tone_of_voice.style is null:
 signal_list.append("Brand tone not configured")
 use_style = "neutral"

generate_copy(brand, product, audience, style=use_style)

if signal_list:
 append("⚠ " + signal_list.join(" / "))
```

---

## Pattern 2 · Generate ad hooks (Meta, TikTok)

**When to use**: creative brief, variation generator, angle A/B test.

### What to load

```
1. brand.json → tone_of_voice, positioning
2. spec.json → problems_solved[], benefits[]
3. profile.json → pain.primary_problem, pain.trigger_primary, market_position.awareness_dominant
4. resources/catalogues/angles.json → available angles (if present in KB)
5. resources/quality-specs/hook.json → hook quality criteria (if present in KB)
```

### Angle selection logic

```
awareness_level = profile.market_position.awareness_dominant

if awareness_level == "unaware":
 angle_type = "problem agitation"
elif awareness_level == "problem_aware":
 angle_type = "solution introduction"
elif awareness_level == "solution_aware":
 angle_type = "product differentiation"
else:
 angle_type = "social proof" # default if null
 signal("Awareness level unknown, social proof angle by default")
```

### Behavior if KB empty

If `resources/catalogues/angles.json` absent: generate from universal patterns (AIDA, PAS, Before/After). Do not block.

---

## Pattern 3 · Generate a creative brief

**When to use**: brief for designer, creative, motion, photo.

### What to load

```
1. brand.json → identity.name, identity.url, tone_of_voice, positioning
2. spec.json → identity.name, description, benefits[] (top 3)
3. profile.json → identity.label, pain.primary_problem, psychology.objections[]
4. offers.json → active offer (type, price, duration) → for the CTA
5. strategy.json → current_focus → if filled, align brief with current focus
6. resources/templates/brief-crea.json → brief structure (if present in KB)
```

### What NOT to load

- `learnings.json` → too operational, not relevant for a creative brief
- `financials` → private data, out of scope for creative brief

### Multi-product handling

If the operator doesn't specify a product:
1. Read `brand.json.products_index[]`
2. Identify the product with `role: "hero"`
3. Load its spec.json
4. Flag: "Brief generated for {hero_product}. Specify another product if needed."

---

## Pattern 4 · Analyze performance (with learnings)

**When to use**: piloting agent, weekly routine, anomaly diagnostic.

### What to load

```
1. learnings-index.json → filter by scope="platform" + platform="meta" (or shopify, etc.)
2. For matched IDs → load only these entries from learnings.json
3. strategy.json → monthly_targets, current_focus
4. (fresh data) → Supabase / live API per credentials.env
```

**Index-first mandatory**: never load full learnings.json. Always go through the index.

### Contradiction detection with learnings

If the agent is about to apply a rule that contradicts an active learning:
```
signal("⚠ Active learning {LRN-XXX} says: {fact}. Check before applying.")
```

---

## Pattern 5 · Onboarding agent (new product, new audience)

**When to use**: snapshot-brand + ingest for a new product. The agent receives a URL and raw data.

### Load order

```
1. brand.json → check that brand exists (meta.name non-empty)
2. index.json → check if product already declared in products_index
3. If new → trigger snapshot-brand (Step 0 pre-flight)
4. After snapshot-brand → trigger ingest-resource on enriched data
5. After ingest → trigger validate-resources to check integrity
```

### Anti-duplication rule

Before creating a product or audience:
```
existing_products = brand.json.products_index[].slug
if new_slug in existing_products:
 ask("This product already exists ({slug}). Enrich the existing sheet or create a variant?")
```

---

## General rules (apply to all patterns)

1. **Load the minimum sufficient**, don't inject everything. A creative brief doesn't need learnings.
2. **Always flag inferences**, if a field is null and the agent assumes something, flag at end of output.
3. **Never invent a number**, price, rate, revenue. If null → omit or ask.
4. **Index-first for learnings**, `learnings-index.json` first, targeted entries after.
5. **brand.json first**, tone always comes from brand.json. Load brand before generating copy.
6. **One signal per output**, group all `⚠` at the end. Not one signal per field.
7. **Propose next step**, every agent output ends with a concrete action ("To enrich, say Ingest…").
