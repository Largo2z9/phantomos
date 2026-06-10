---
name: qc-creative
type: curator
version: "1.0.0"
recommended_model: sonnet
layer: meta
reasoning_pattern: null
operator_facing: false
invocable_by:
  - compose-creative
  - recompose-creative
  - adapt-from-competitor
  - "*"
description: >
  Output gate on a RENDERED creative BEFORE any media spend. Looks at the actual
  produced binary (vision) and checks it against the genome it was meant to execute
  and the brand facts: product fidelity, text/typo/legibility, claim/compliance, DA,
  anti AI-defect. Sub-skill, not invoked by operator directly. Called by the 3
  producers as a final gate after generation, before the creative is marked
  spend-eligible. Returns a structured PASS/FIX/KILL verdict + per-binary qc result.
  Does NOT rewrite or regenerate, only flags. Caller writes the verdict into
  produced-asset#qc and halts if not shippable.
  FR: "controle qualite de la creative" "gate avant spend" "verifie le rendu de l'ad" "qc creative".
  EN: "qc the creative" "output gate before spend" "check the rendered ad" "creative quality gate".
permissions:
  reads: [brand, product, profile, genome, creative]
  writes: []
  emits_events: [qc_check]
  mode: none
  subagent_safe: true
---

> Brique gate de sortie. Pendant de `validate-output-coherence` (qui garde la PROSE opérateur) : `qc-creative` garde la CRÉA RENDUE avant qu'on mette du budget média derrière. On dépense de l'argent sur ces assets, rien ne passe en spend sans gate vert.

## Tone

Structured machine output. Returns JSON, not prose. Human-facing notes go in `issues[].what` / `issues[].fix`, concise, actionable, no jargon.

---

# Skill: QC Creative (output gate before spend)

The final gate before a produced creative becomes spend-eligible. It MUST actually
LOOK at the rendered binary (vision read), not reason from the brief. It answers
five questions, each per binary, each with `pass | warn | block`:

1. **Product fidelity** · est-ce le VRAI produit de la marque, ou une réinvention IA ? (logo, features distinctives, colorway, compte/placement, déformations)
2. **Texte & lisibilité** · chaque mot correct, wordmark exact, lisible au pouce en 1,5s, rien de garbled/coupé
3. **Claim & compliance** · chaque claim étayé, disclaimers requis présents DANS le rendu, zéro claim santé risqué, zéro chiffre gonflé, zéro faux verbatim
4. **DA** · cohérence avec la DA de marque (`brand_da`) et le `style_id` déroulé
5. **Anti-défaut IA** · mains/doigts, texte halluciné, plastique 3D, artefacts, letterbox (vidéo), VO désync

---

## Input contract

Caller MUST provide :

- `creative_dir` — le dossier `brands/{slug}/creatives/{batch}/{CRT-NN}/` (le gate lit `genome.json`, `creative.json`, `produced/*.jpg|mp4`, `produced/*.json` sidecars)
- `brand_slug` — marque dont on charge la DA, les assets canon, et les faits
- *(optionnel)* `binaries` — sous-ensemble de binaires à gater (défaut : tous les `produced/*` à fidélité critique + le `composite-final`)

Si `creative_dir` n'a pas de binaire produit (génome seul), le gate retourne `indeterminate` (rien à regarder), jamais `pass`.

---

## Execution steps

### Step 1 — Charger la cible (ce que l'ad DEVRAIT être)

Read :
- `{creative_dir}/genome.json` — l'ADN : `hook`, `frames[]` (copy_script + visual_script), `genome_tags` (mecanique_id, style_id, angle_id, audience_slug), `copy_meta.compliance_disclaimers_required[]`
- `{creative_dir}/creative.json` — lignage (variant_of, refs)
- `brands/{slug}/products/{product_slug}/spec.json#visual_identity` — `assets_canonical` (logo_canonical, packshot_*, badge_*), `color_palette`, `distinctive_features[]` (= la signature produit à vérifier au pixel)
- `brands/{slug}/brand.json` — `tone_of_voice`, `brand_da` (palette mood, do/don't, `allowed_style_ids`), `proofs` (les seuls claims/chiffres autorisés), `banned_words`
- `brands/{slug}/_snapshot.md` — index rapide des faits

### Step 2 — REGARDER le binaire (vision, NON négociable)

Pour chaque binaire à gater, **YOU MUST** Read l'image/vidéo réellement (Read tool, vision). Zoomer mentalement sur les zones à risque : le logo embossé, le badge d'autorité, le compte de features distinctives, le texte du hook. **Ne jamais gater depuis le brief seul.** Si tu ne peux pas voir le binaire, le verdict est `block` (un asset non vu ne passe pas).

### Step 3 — Axe 1 · Fidélité produit (le plus dur)

Comparer le produit visible dans le rendu au `visual_identity.assets_canonical` + `distinctive_features[]` :
- Logo : lecture exacte du wordmark vs `assets_canonical.logo_canonical` (lettrage, casse, ponctuation). Un logo redessiné/amputé par l'IA = `block`.
- Features distinctives : compte + placement vs `distinctive_features[]` (ex « 6 nodes : 4 avant-pied + 2 voûte »). Réinvention = `block`.
- Colorway / matière : conforme au canon (ex mesh orange + base blanche), pas une fantaisie monobloc.
- Déformations, artefacts, formes impossibles.

**RÈGLE ANTI-DÉFAUT (load-bearing, ferme la cause-racine).** Si la créa est d'une catégorie à **fidélité critique** (supplement, cosmetic, food, pharma, tout produit physique reconnaissable) ET que le produit/logo a été **re-généré** (`produced-asset#source_asset_ref.kind` ≠ `asset_library`/`scraped_packshot`, ou `composite_mode` = `full_regen`) → fidélité = `block` automatique. Le fix imposé : **compositer le vrai asset** (`composite_mode: layered`, packshot/logo canon collés), JAMAIS laisser le modèle redessiner. Un logo/produit fidélité-critique se COLLE, ne se génère pas.

### Step 4 — Axe 2 · Texte & lisibilité

- Chaque mot du rendu : orthographe exacte, aucun glyphe garbled/fondu.
- Wordmark == `assets_canonical.logo_canonical` texte (casse + ponctuation exactes).
- Headline == le `hook` du génome (ou variante validée), pas une dérive.
- Lisibilité mobile au pouce en 1,5s : hiérarchie, contraste, rien de coupé/chevauché.
- Typo dans le hook ou le wordmark = `block`. Coquille secondaire = `warn`.

### Step 5 — Axe 3 · Claim & compliance

- Chaque `genome.copy_meta.compliance_disclaimers_required[]` doit être **effectivement présent et lisible dans le rendu** (array déclaratif → vérifié visuellement). Absent = `block`.
- Chaque chiffre/claim visible doit tracer à `brand.proofs` (verbatim). Chiffre gonflé/inventé = `block`.
- Faux verbatim nominatif (un nom cite une phrase non canon) = `block`.
- Claim santé absolu/non encadré (« cure », « 95% less pain » balancé sans cadre) ou `banned_words` présents = `block`.
- Contradiction avec une preuve réelle (ex note Trustpilot affichée ≠ réelle) = `block`.

### Step 6 — Axe 4 · DA

- Cohérence avec `brand_da` (palette mood, grain/texture, do/don't) et avec la fiche du `genome_tags.style_id` (`registries/styles/{style_id}.json` une fois la style-library câblée). Style hors `brand_da.allowed_style_ids` = `warn` (signaler à l'opérateur), incohérence DA franche = `block`.

### Step 7 — Axe 5 · Anti-défaut IA générique

Mains/doigts, texte halluciné en arrière-plan, rendu plastique 3D involontaire, artefacts de fonte, watermark parasite. Vidéo : letterbox/bandes noires, VO désync, captions absentes (`captions_required`). Sévérité selon visibilité.

### Step 8 — Emit audit event (MANDATORY)

```bash
python3 .skills/emit-event.py \
  --kind qc_check \
  --payload '{"brand_slug":"{slug}","creative_dir":"{dir}","shippable":{true|false},"decision":"{PASS|FIX|KILL}","blocking":{N}}'
```

Skipping = le hook traite la créa comme non-gatée.

---

## Output

Structured JSON to stdout :

```json
{
  "shippable": false,
  "decision": "FIX",
  "per_binary": [
    {
      "file": "produced/composite-final.jpg",
      "passed": false,
      "checks": [
        {"name": "product_fidelity", "passed": false, "note": "wordmark rendu 'steppre', point final absent vs canon 'stepprs.'"},
        {"name": "text_legibility", "passed": true, "note": ""},
        {"name": "claim_compliance", "passed": true, "note": ""},
        {"name": "da", "passed": true, "note": ""},
        {"name": "anti_ai_defect", "passed": true, "note": ""}
      ]
    }
  ],
  "blocking_issues": [
    "Logo héros re-généré (full_regen) sur catégorie fidélité-critique : wordmark déformé. Imposer composite_mode=layered avec logo_canonical."
  ],
  "fix_list": [
    "Recomposer le binaire en composite_mode=layered : coller logo_canonical + packshot canon, ne pas re-générer le produit.",
    "Re-passer au gate après correction (zoom logo + recompte features) avant tout spend."
  ],
  "validated_at": "2026-06-08T...",
  "brand_slug": "...",
  "creative_dir": "..."
}
```

`shippable: true` SEULEMENT si tous les binaires fidélité-critique ont `passed: true` ET zéro `blocking_issues`. `decision` :
- **PASS** — shippable tel quel, éligible au spend.
- **FIX** — corrigeable sans tout refaire ; `fix_list` ordonné ; re-gate obligatoire après.
- **KILL** — produit faux / concept troué / non récupérable ; refaire.

`shippable` est un **jalon dérivé**, distinct du `creative.validation_status` (cycle perf hypothesis→tested→...→fatigued). Une créa peut être `shippable: true` et `validation_status: hypothesis` (gatée mais pas encore testée en campagne).

---

## Hard Rules

- **Regarder, jamais deviner.** Le verdict exige un vision-read réel du binaire (Step 2). Pas de binaire vu = `block`.
- **Read-only.** Ce skill ne réécrit ni ne re-génère rien. Il retourne le verdict ; le CALLER écrit le résultat dans `produced-asset#qc` (passed/checks/regen_count) via `write_to_context`, et halte si non shippable.
- **Pas de spend sans PASS.** Un seul `block` (produit faux, claim santé faux, typo dans le hook, disclaimer manquant) interdit `shippable: true`. Règle d'or : on ne met jamais de budget média derrière une créa non gatée.
- **Fidélité critique = compositing obligatoire.** Logo/badge/features distinctives d'un produit physique se COLLENT depuis l'asset canon (`layered`), ne se génèrent pas. Re-génération sur catégorie fidélité-critique = `block` automatique (Step 3). C'est la cause-racine du défaut logo, fermée structurellement.
- **Comparaison littérale.** Fidélité, orthographe, chiffres = comparaison stricte au canon, petite tolérance paraphrase. Incertain → `warn`, l'opérateur tranche.
- **Event non optionnel.** Step 8 ferme la boucle avec le hook d'audit.

---

## Cross-references

- `resources/schemas/produced-asset.schema.json#qc` — le réceptacle (`passed`/`checks[]`/`regen_count`) que le caller remplit depuis ce verdict
- `resources/schemas/creative.schema.json#validation_status` — cycle PERF distinct (ne pas confondre `shippable` avec ce champ)
- `.skills/skills/compose-creative/SKILL.md` — caller principal : invoque ce gate après gen, avant de marquer la créa spend-eligible
- `.skills/skills/validate-output-coherence/SKILL.md` — skill frère (gate de la prose opérateur ; celui-ci gate la créa rendue)
- `resources/registries/styles/{style_id}.json` — fiche style (DA Axe 4), câblée en vague style-library
- `.skills/emit-event.py` — canal d'audit (Step 8)
- `.skills/write-to-context.py` — canal de mutation canonique (le CALLER l'utilise pour écrire `produced-asset#qc`, ce skill ne mute pas)
</content>
</invoke>
