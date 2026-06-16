# Template canonique · Operator fiche output

> Référence canonique v2.51+ pour toute fiche output operator-facing rendue par les skills production / curator / orchestrator (compose-creative, recompose-creative, craft-packshot, import-asset, decompose-ad, compose-overlay-text, etc.).
>
> Objectif · cohérence cross-skills, langage métier zéro jargon, posture neutre descriptive sans push, soft offer 1 ligne max au close.
>
> **Anti-pattern systémique A (red team audit 2026-05-13)** · les fiches historiques ship des headers `═══ COMPOSE CREATIVE · CRT-12 ═══`, des gates `flag _validated_by_operator: true + _canonical: true`, des blocs `TAGS RETRIEVAL` quasi-JSON. Le marketeux DTC qui voit `variant_axis : hook_swap` perd confiance en 1 seconde. Ce template canonique force la cohérence.

---

## Règles cardinales (anti-jargon)

### JAMAIS en surface operator-facing

- **Noms de skills** internes (`compose-creative`, `craft-packshot`, `import-asset`, `recompose-creative`, `compose-overlay-text`, `snapshot-brand`, `decompose-ad`, etc.)
- **IDs internes** (`CRT-N`, `CRT-12`, `concept_id`, `variant_of`, `cpt_id`)
- **Enum techniques** (`variant_axis: hook_swap`, `composite_mode: layered`, `asset_type: packshot_variant`, `intent_mix`, `craft_mode density=0.6`)
- **Field paths JSON** (`visual_identity.assets_canonical.logo_canonical._validated_by_operator`)
- **Flags techniques** (`_validated_by_operator: true`, `_canonical: true`, `_fallback_to_cdn: false`)
- **Schema versions** (`schema v1.2`, `creative.schema v1.2`, `visual_identity/1.2`)
- **HR section names** (`HR3b`, `HR-COMPOSITE`, `Step 3b.5`, `Step 0bis`)
- **Concepts techniques** (`pipeline`, `slot`, `mutation gate`, `frontmatter`, `endpoint`, `latency`, `prompt brief`, `payload`)
- **Doctrine names** (`Contextual Intelligence`, `Schema Encoding Discipline`, `Canonical Matrix Reasoning`, `atlas vivant`, `atlas canon copy`, `canon-tool`)
- **Endpoint URLs ou paths absolus** dans le body (les paths apparaissent uniquement dans la ligne "ouvre" pour Preview)

### TOUJOURS en surface operator-facing

- **Vocabulaire métier** · "photo officielle du produit", "logo brand", "badge certif", "pub branded", "audience cible", "type de campagne"
- **Numérotation simple** · "pub n°5", "version 2 de la pub n°5", pas `CRT-N`
- **Posture descriptive** · "X · OK", "Y · pas encore renseigné", jamais "tu dois", "il faut", "run Z"
- **Soft offer 1 ligne max** au close · "Si tu veux, on peut...", jamais menu de 5 chemins
- **Validation gates** en français accessible · "(a) Validé · marqué comme version officielle", pas "(a) flag _validated_by_operator: true + _canonical: true"

---

## Structure canonique d'une fiche output

### 1. Header (1 ligne · titre métier · pas de nom skill)

Format général ·

```
═══════════════════════════════════════════════════════════════
{BRAND_HUMAIN} · {ACTION_DESCRIPTIVE} · {INDEX_SIMPLE_OU_DATE}
═══════════════════════════════════════════════════════════════
```

**Mappings action descriptive cross-skills** ·

| Skill historique | ACTION_DESCRIPTIVE | Exemple INDEX |
|---|---|---|
| compose-creative | Pub n°{N} | `Pub n°17` |
| recompose-creative | Variante de la pub n°{N_source} | `Variante de la pub n°12` |
| craft-packshot | Photo officielle produit · {product_humain} | `Photo officielle · Cell Boost` |
| import-asset | Asset ajouté · {label_humain} | `Asset · Logo brand` ou `Asset · Badge "100% Plantes Naturelles"` |
| decompose-ad | Analyse pub · {source_humaine} | `Analyse pub · concurrent` ou `Analyse pub · interne n°17` |
| compose-overlay-text | Pub n°{N} · texte/logo affiné | `Pub n°17 · texte affiné` |

**Sous-titre 1 ligne après header** · date + 1 phrase plain language qui décrit le contenu ·

```
{date YYYY-MM-DD} · {1 phrase plain language qui résume ce que la fiche contient}
```

### 2. Section 1 · Description objective (ce qui est rendu)

Format · sections labellées en plain language, valeurs en métier, jamais field path JSON.

Exemple compose-creative ·

```
───────────────────────────────────────────────────────────────
1 · CE QUE LA PUB MONTRE
───────────────────────────────────────────────────────────────
Format             carrousel · 4:5 · français
Accroche visuelle  {description scène en prose · 1-2 lignes}
Accroche texte     "{verbatim hook · max 8 mots}"
Corps              {description body · 1 ligne · ou "·" si pas de body}
Bouton             "{verbatim CTA}"
Branding           Logo en bas à droite · photo officielle du produit centrée
Photo générée      ouvre dans Preview · open {path}
```

Pas de · `format: static_image | ratio: 4:5 | language: fr` (JSON-style). Toujours plain language avec valeurs en clair.

### 3. Section 2 · Interprétation stratégique (ce que ça raconte)

Format · pareil section 1, plain language, jamais enum techniques.

Exemple compose-creative ·

```
───────────────────────────────────────────────────────────────
2 · CE QUE LA PUB RACONTE
───────────────────────────────────────────────────────────────
Cible              {1 phrase qui décrit l'audience · "femmes 35-45 post-grossesse, chute de cheveux mais aussi sentiment perte d'identité"}
Niveau conscience  {plain · "consciente du problème, pas du produit"}
Vérité non-dite    "{verbatim insight}" · {formulée | implicite | absente}
Angle              {1 phrase qui décrit l'angle · "frustration des soins de surface"}
Type de campagne   {direct response | branding | direct response avec touche brand}
Mécanique          {nom métier · "before-after-bridge", pas "BAB" ni "mecanique_id"}
```

Jamais · `intent_mix: {primary: DR, weights: {DR: 0.6, Brand: 0.4}}`. Toujours · *"Type de campagne · direct response avec touche brand (priorité direct response)"*.

### 4. Section 3 · Diagnostic (si applicable)

Format · prose courte, jamais scores numériques en surface (sauf 1-5 stars compréhensibles).

Exemple ·

```
───────────────────────────────────────────────────────────────
3 · DIAGNOSTIC
───────────────────────────────────────────────────────────────
Cohérence          {plain · "tient · la mécanique reflète l'insight, l'angle est cohérent avec la cible"}
Score arrêt-scroll {1-5 stars · ★★★★☆}
Forces             · {observable concret · "rupture pattern Meta feed via cadrage carré sur visage"}
                   · {observable}
                   · {observable}
Risques            · {observable · "claim 'cliniquement testé' nécessite preuve attachée"}
                   · {observable}
```

Pas · `Score prédictif : 4 / 5 · ...`. Plutôt en stars visuelles `★★★★☆`.

### 5. Section retrieval / metadata (OPTIONNELLE · backstage)

**CRITIQUE** · si cette section est rendue à l'écran, elle doit être en plain language. Sinon, garder en backstage (write JSON dans creative.json pour retrieval mais NE PAS render à operator).

Si rendue (rare, pour power users) ·

```
───────────────────────────────────────────────────────────────
TAGS (pour retrouver cette pub plus tard)
───────────────────────────────────────────────────────────────
Pour          {audience humaine · "femmes post-grossesse"}
Plateforme    {format · "Meta feed carrousel"}
Type          {plain · "direct response avec touche brand"}
Concept       {plain · "variante du concept 'frustration soins surface'"}
```

Pas de `concept_id: cpt_brand_audience_001`, `variant_of: cpt_brand_audience_000`, `intent_mix: {primary: DR}`. Plain language only.

**Pattern recommandé** · NE PAS rendre cette section par défaut. Elle vit en JSON dans le fichier persisté (creative.json) pour retrieval programmatique. Operator ne la voit pas.

### 6. Gate validation (si applicable · craft-packshot, import-asset)

Format · "À toi de valider" en français accessible, options en métier, jamais flags techniques.

Exemple craft-packshot ·

```
───────────────────────────────────────────────────────────────
À toi de valider
───────────────────────────────────────────────────────────────
(a) Validé · je marque comme version officielle de ta photo produit
(b) Re-essayer · ajustements (précise quoi)
(c) Autre source · je re-pick une photo différente du carousel
```

Exemple import-asset ·

```
───────────────────────────────────────────────────────────────
À toi de valider
───────────────────────────────────────────────────────────────
(a) Validé · marqué comme version officielle réutilisable
(b) Je re-upload une version plus propre (résolution + haute, fond transparent)
(c) Annule
```

Pas · `flag _validated_by_operator: true + _canonical: true`. Toujours en français.

### 7. Footer · 1 reco soft offer (jamais menu, jamais push)

Format · 1 phrase soft offer ancrée sur ce qui vient d'être produit. Soit "Si tu veux, on peut...", soit information passive ("Cette photo est réutilisable sur toutes tes prochaines pubs."). Jamais "Tape la commande X".

Exemples cross-skills ·

```
───────────────────────────────────────────────────────────────
Si tu veux, on peut tester cette pub en live sur Meta sur ton audience principale.
```

```
───────────────────────────────────────────────────────────────
Cette photo officielle est réutilisable sur toutes tes prochaines pubs sans la regénérer.
```

```
───────────────────────────────────────────────────────────────
Si pertinent, on peut aussi préparer la vue 3/4 du produit pour avoir une photothèque complète.
```

**Anti-pattern footer** ·
- ❌ `Next · A, ou B, ou C` (menu à plat)
- ❌ `(a) Tape "compose layered" · (b) ...` (push avec commande)
- ❌ `Tu peux maintenant : tester, adapter, refaire.` (menu déguisé)
- ❌ Footer absent (orphan close)

---

## Headers strict · cross-skills mapping canonique

Pour éliminer le drift "═══ COMPOSE CREATIVE · CRT-12 ═══" ·

### compose-creative
```
{BRAND_HUMAIN} · Pub n°{N}
{date} · {1 phrase plain language description}
```

### recompose-creative
```
{BRAND_HUMAIN} · Variante de la pub n°{N_source}
{date} · {1 phrase plain language · "même concept, audience changée pour {new_audience_humaine}"}
```

### craft-packshot
```
{BRAND_HUMAIN} · Photo officielle · {product_humain}
{date} · {1 phrase plain language · "version {N}, prête pour ta validation"}
```

### import-asset
```
{BRAND_HUMAIN} · Asset ajouté · {label_humain}
{date} · {1 phrase plain language · "rangé dans tes assets brand, prêt pour réutilisation sur tes pubs"}
```

### decompose-ad
```
{BRAND_HUMAIN} · Analyse pub · {source_humaine}
{date} · {1 phrase plain language · "décomposition de la pub {concurrent | interne n°N}"}
```

### compose-overlay-text
```
{BRAND_HUMAIN} · Pub n°{N} · texte/logo affiné
{date} · {1 phrase plain language · "passe propre sur l'overlay pour rendre le texte et le logo nets"}
```

---

## Mappings vocabulaire canonique cross-skills

Vocabulaire à utiliser uniformément cross-skills (anti-drift) ·

| Concept | Vocabulaire canon operator-facing | À éviter |
|---|---|---|
| Asset photo produit canon | "photo officielle du produit" | "packshot canonique", "canonical packshot", "packshot canon" |
| Asset logo canon | "logo brand officiel" | "logo canonical", "_canonical logo" |
| Asset badge canon | "badge {claim humain}" (ex 'Badge "100% Plantes Naturelles"') | "badge_canonical.cert_plantes_naturelles" |
| Validation operator | "validé" / "marqué comme version officielle" | "_validated_by_operator: true", "canonical flag" |
| Audience mère | "audience mère" / "audience principale" | "mother audience", "parent audience" |
| Sous-audience | "sous-audience" / "poche audience" | "sub-audience", "segment" |
| Pub layered packshot collé | "photo studio · produit pixel-exact" | "layered compositing", "composite_mode: layered" |
| Pub mode classique | "génération classique" | "full_regen", "composite_mode: full_regen" |
| Mode adapter une pub | "version adaptée" / "variante" | "recompose", "variant_axis: X" |
| État rempli | "OK" / "renseigné" | "flag canonical · true" |
| État vide | "pas encore renseigné" | "null · empty · L3 degraded" |

---

## Process check avant ship d'une fiche output

Avant qu'une fiche soit rendue à l'opérateur, le skill DOIT vérifier ·

1. **Header** · pas de `COMPOSE CREATIVE`, `CRAFT PACKSHOT`, `IMPORT ASSET`, `CRT-N`, `variant_axis`, etc.
2. **Body** · pas de field path JSON, pas de flag technique, pas de schema version
3. **Gate** · options en français accessible, pas `flag X: true + Y: true`
4. **Footer** · 1 soft offer max, pas de menu, pas de push, pas d'orphan
5. **Vocabulaire** · cohérent avec mappings table ci-dessus

Si une fiche viole 1+ critère, **bug**. Refactor avant ship.

---

## Backstage vs operator-facing · clarification

**Le bloc JSON `creative.schema v1.2` persisté** (avec `intent_mix`, `concept_id`, `variant_of`, `composite_mode`, etc.) est **backstage** · vit dans `brands/{slug}/produced/{CRT-N}.json` pour retrieval programmatique et audit. L'opérateur ne le voit pas. Pas de leak dans la fiche rendue.

**Le markdown brief rendu à l'écran** (`brands/{slug}/produced/{CRT-N}.md` ou prose chat) est **operator-facing** · plain language obligatoire, vocabulaire métier.

Cette distinction est non-négociable. Le pattern v2.51+ force le respect via ce template canonique.

---

## Visual rendering refresh v2.69+ · format opérateur sobre

Refresh canon pour fiches opérateur-facing rendues post-v2.69. Le format ASCII separator box (`═══════════`) reste valide pour fiches creative production (compose-creative, craft-packshot etc · structuré rigide). Pour fiches état brand / atlas / synthèse opérateur (snapshot-brand, brief-day, profile-audience, build-atlas-complete), appliquer le pattern visuel sobre suivant.

### Header sobre · pas raw markdown level mismatch

Format ·

```
## {Brand X} · état atlas
{date YYYY-MM-DD} · {1 phrase plain language résumé}
```

Pas de `# {Brand} ATLAS` (H1 monolithique) ni `### {brand}` (H3 sous-niveau ambigu). H2 simple, sous-titre 1 ligne.

### Tableau visuel pour metrics quantitatifs

Quand un rendu agrège plusieurs metrics quantitatifs (reviews count, rating, taille audience estimée, prix produits), utiliser tableau markdown · pas prose ·

```markdown
| Metric | Valeur | Source |
|---|---|---|
| Reviews count | 2127 | Trustpilot [observé] |
| Rating moyenne | 3.4/5 | Trustpilot [observé] |
| Produits actifs | 12 | Site scrape [observé] |
| Audience mère estimée | 50k EU | Cartographie [déduit] |
```

Pas de prose équivalente *"Trustpilot a 2127 reviews avec une note de 3.4/5, et le site présente 12 produits actifs..."* (scannable beaucoup moins vite).

### Bullets courts pour insights qualitatifs

Insights qualitatifs en bullets courts (1 ligne par insight max) · pas paragraphes denses ·

```markdown
**Forces observées** ·
- Hero angle plantar fasciitis dominant 27 EU countries [observé]
- Single narrative cross-audience reproductible [déduit]
- Trustpilot review velocity stable Q1-Q2 [observé]

**Inconnu macro** ·
- Conversion rate par audience non observable depuis scrape public
- Allocation budget réelle inconnue
```

### Annotations source/confidence subtiles

Pattern canon · suffixe entre crochets simple, pas field path JSON ·

```markdown
- Trustpilot 3.4/5 · 2127 reviews [observé]
- Audience mère 50k EU estimation [déduit]
- Pricing tier premium 79€ [observé]
- Brand cohérence narrative cross-channels [déduit · confiance moyenne]
```

Pas de · `trustpilot.rating: 3.4 [field source: observed, confidence: 0.95]` · field path + numeric confidence violent règle "no internal plumbing operator" (canon `feedback_no_jargon_to_operator` Memory).

Mappings annotations operator-facing ·

| Annotation interne | Operator-facing |
|---|---|
| `source: scraped, confidence: high` | `[observé]` |
| `source: derived, confidence: medium` | `[déduit]` |
| `source: stated, confidence: authoritative` | `[déclaré]` |
| `source: derived, confidence: low` | `[incertain]` |

### Couleurs / emojis SOBRES

Règles ·

- ✓ pour state OK / validé (un seul caractère ASCII checkmark)
- ⚠ pour state incertain / risque (un seul caractère warning sign)
- Aucun emoji décoratif (📋 💡 🎯 🚀 ✨ 🔥 banni)
- Pas de couleurs runtime (markdown rendu plain, pas terminal ANSI)

Exemple usage ·

```markdown
**État atlas Brand X** ·
- Audiences cartographiées ✓ (2 mères × 5 sous-poches)
- Pain points encodés ✓ (12 PNT, validés)
- Ad targeting strategy ⚠ (1 hero angle seul testé · diversification non démarrée)
- Frictions produit ⚠ (3 FRC observées · severity à confirmer ops)
```

### Zero raw JSON / paths / field names dans rendu opérateur-facing

JAMAIS dans fiche operator-facing ·

```
brands/stepprs/audiences/workers-shifts/profile.json
audience.psychographics.identity: "blue-collar pride"
_field_types.workers_shifts.profile: "structured"
```

TOUJOURS plain language ·

```
Audience workers-shifts · identité "blue-collar pride" · validée
```

Si l'opérateur demande explicitement le path (power user `?` shortcut), surfacer dans une ligne dédiée backstage · pas dans body fiche.

### Exemple fiche complète post-refresh v2.69+

```markdown
## Stepprs · état atlas
2026-05-14 · synthèse post-snapshot, 2 audiences mères cartographiées, hero angle live observé.

### Substrat encodé

| Entité | Count | État |
|---|---|---|
| Audiences mères | 2 | ✓ cartographiées |
| Sous-poches | 5 | ✓ encodées |
| Pain points | 12 | ✓ validés |
| Frictions produit | 3 | ⚠ severity à confirmer |

### Forces observées

- Hero angle plantar fasciitis dominant 27 EU countries [observé]
- Single narrative cross-audience reproductible [déduit]
- Trustpilot 3.4/5 · 2127 reviews [observé]

### Inconnu macro

- Conversion rate par audience non observable [scrape public limité]
- Allocation budget réelle inconnue [auth Meta Ads requise]

### Leviers

- `mine-voc` pour densifier verbatims (Trustpilot 1-2 stars riches)
- `audit-meta-account` si credentials Meta fournis pour conversion par audience

### Close

Si tu veux, on peut creuser la cartographie audience workers-shifts (sous-poches mining vs validation directe).
```

Pattern visuel · sobre, scannable, opérateur lit en 30s, zéro jargon.

---

## Cross-refs

- Doctrine source · `docs/system/contextual-intelligence.md` "Operator-facing rule absolue"
- Audit red team source · session 2026-05-13 patterns systémiques A + B
- Workspace CLAUDE.md root · ligne 132 "NEVER expose paths, field names, internal codes"
- Skills concernés v2.51+ · compose-creative, recompose-creative, craft-packshot, import-asset, decompose-ad, compose-overlay-text · DOIVENT référencer ce template dans leur HR `Operator output template` section
- Visual refresh v2.69+ · `audiences-cartography-doctrine.md § Cartographie ≠ ad targeting` (substrat cartographié vs runtime production · respecté en rendu fiche), `territory-doctrine.md` (encodage stable), `progressive-cartography-doctrine.md` (annotations confidence sobres operator-facing)
