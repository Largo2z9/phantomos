---
name: add
description: Slash command pre-flight proactif analytique pour ajouter une entité à l'atlas (audience · angle · pain · objection · product · friction). L'agent décompose seul, cross-check, propose chain optimal. Jamais menu de questions sauf unfog absolu.
version: v1.0.0
---

# /add · ajouter une entité à l'atlas · pre-flight proactif analytique

Canon v2.87.5+. Pattern miroir senior media buyer brief équipe · *"voici ce que je vois, voici ce que je propose, OK ?"*. Pas *"remplis ce formulaire pour que je décide"*.

> **Note · spec interne vs rendu opérateur runtime**
>
> Cette spec mélange instructions agent et rendu opérateur runtime. L'agent fait le travail cognitif lourd (lit atlas existing + raisonne CC v3.1 + cross-check overlap) en silence. L'opérateur voit uniquement la proposition tranchée + rationale courte + close binaire. Aucun jargon doctrine, aucun path technique, aucun NIVEAU 0 décomposition matricielle exposée.

## Triggers

| Argument | Mode |
|---|---|
| `/add audience [brand]` | ajout audience nouvelle (mère OR sous-poche détectée) |
| `/add angle [audience_slug]` | ajout angle nouveau (cross-refs audience + pain + mechanism inférés) |
| `/add pain [audience_slug]` | ajout pain point sub-audience |
| `/add objection [audience_slug]` | ajout objection sub-audience |
| `/add product [brand]` | ajout produit catalog |
| `/add friction [product_slug]` | ajout friction sub-product |
| `/add {entity}` générique | détection auto type optimal selon intent verbal opérateur |

Natural language route · *"ajoute une audience sur Fincut"* · *"je veux ajouter un angle"* · *"add audience"* etc.

## Workflow canon · 8 étapes

### Step 1 · Receive intent

Receive operator intent · entity type explicit OR inféré depuis verbal phrasing.

### Step 2 · Read atlas existing (silent)

Phantom LIT en silence ·
- `brands/{slug}/brand.json` · identity + positioning + voice canon + market
- `brands/{slug}/audiences/*/profile.json` · audiences déjà encodées + meta.overlap_with
- `brands/{slug}/audiences/*/pain_points/*.json` · pains owned cross audiences
- `brands/{slug}/audiences/*/objections/*.json` · objections owned cross audiences
- `brands/{slug}/products/*/spec.json` · mechanisms + benefits chain
- `brands/{slug}/angles/*.json` · existing angles + lineage refs
- `brands/{slug}/learnings.json` · 5 most recent LRN entries
- `brands/{slug}/status.json#connectors_state` · connectors actifs (Trustpilot accessible · TrendTrack accessible · etc.)

### Step 3 · Raisonner compositionnellement (CC v3.1)

NOYAU · ce qui ressort le plus pertinent à ajouter selon analyse atlas (e.g. audience gap MECE détecté · angle pivot manquant · pain orphelin observé verbatims · etc.). Inférer via signaux atlas existing, pas générique.

CONTEXTE · cross-refs entrantes (verbatim source disponible OR pas · audience cible cohérente · mechanism activable · awareness stage cohérent).

MODIFIEURS · si applicable (canal placement · Schwartz movement · format si angle/creative).

### Step 4 · Cross-check overlap detection

Pour entity type ·
- `audience` · scan audiences existing meta + psychology · semantic similarity sur drivers · pain dominant · target_recipient (canon v2.87.4 dream_scenario). Flag cousine MECE si overlap > 0.6.
- `angle` · scan existing angles lineage · même audience+pain+mechanism = duplicate. Flag.
- `pain` · scan pain_points sub-collections audiences · semantic similarity formulation. Flag cousine si owned cross-audiences même chain.
- `objection` · scan objections sub-collections · pattern recurrent cross-audiences = canon objection brand.
- `product` · scan products_index brand.json + visual_identity SKUs.
- `friction` · scan frictions sub-products · same usage_context = duplicate.

### Step 5 · Propose response (rendu opérateur)

Format canon rendu opérateur runtime ·

```
/add {entity} {brand} · pré-flight analyse atlas
─────────────────────────────────────────────────────
J'ai lu · {N} {entités} encodées + {M} learnings + {K} ads observed · tone canon
Ce que je vois ·
  · {NOYAU inféré · ce qui ressort comme entité candidate prioritaire}
  · {CONTEXTE · cross-refs disponibles · audience cible · pain/mechanism source}
  · {MODIFIEURS si applicable}

Cross-check · {N} overlap détectés OR 0 overlap (proposition unique)

Proposition · {skill chain optimal + paramètres pré-remplis cohérents canon}

Lance OR ajuste ?
```

### Step 6 · Si tout clair · trigger direct

Si Step 4 cross-check = 0 overlap critique + Step 3 raisonnement converge sur 1 candidate prioritaire → propose chain skill optimal + paramètres pré-remplis + close binaire *"Lance OR ajuste ?"*. JAMAIS menu de 5 questions.

### Step 7 · Si unfog vraiment nécessaire · 1 question pivotale

Si Step 4 révèle 2-3 candidates équivalentes OR signal atlas ambigu →  1 question pivotale UNIQUEMENT (pas menu de 5). Exemple ·

```
J'ai 3 audiences cousines candidates · {A} {B} {C}.
Tu cibles plutôt {axe1} ou {axe2} ?
```

Pas *"réponds à ces 5 questions structurées"*. Une question pivotale tranche.

### Step 8 · Si TRÈS ambiguous · STOP signal honnêteté discipline

Si Step 2 révèle atlas trop vide pour décomposition fiable (e.g. 0 audience encodée · 0 verbatim · brand vide) → STOP signal proactif ·

```
J'ai pas assez de signaux pour décomposer un {entity} pertinent.
{raison · e.g. 'aucune audience encodée encore · pain orphelin'}.
Veux-tu lancer `mine-voc` OR `setup-brand` OR `snapshot-brand` d'abord ?
```

## Hard Rules (interne agent · jamais citées en rendu opérateur)

> Note pour l'agent · ces règles sont contraintes d'exécution internes. Ne jamais les citer ni leur format `HR ·` dans le rendu opérateur runtime.

- HR · TOUJOURS lire atlas existing AVANT de proposer (Step 2 non-négociable)
- HR · TOUJOURS appliquer CC v3.1 raisonnement compositionnel NOYAU × CONTEXTE × MODIFIEURS (canon `compositional-cartography.md` v3.1)
- HR · TOUJOURS cross-check overlap detection AVANT de proposer (Step 4 non-négociable · évite duplicates atlas)
- HR · JAMAIS menu de 5 questions structurées · proposition tranchée + rationale courte + close binaire
- HR · 1 question pivotale UNIQUEMENT si unfog vraiment nécessaire (pas confort agent · vraie ambiguïté atlas)
- HR · STOP signal proactif si atlas trop vide pour décomposition fiable (honnêteté discipline canon)
- HR · JAMAIS exposer paths techniques (`audiences/{slug}/pain_points/*.json` · `angles/{ANG-NN}/angle.json`) dans rendu opérateur runtime
- HR · JAMAIS exposer noms doctrines (CC v3.1 · CMR · IP · DVD · EDD · OCD) dans rendu opérateur runtime
- HR · JAMAIS exposer JSON field paths (`lineage.audience_ref` · `psychology.dream_scenario_narrative`) dans rendu opérateur runtime
- HR · TOUJOURS chain skill optimal post-validation opérateur (e.g. ajout audience → `map-audiences` scaffold light · ajout angle → `produce-paid-angles` avec params)

## Cross-refs canon

- `docs/system/compositional-cartography.md` v3.1 · raisonnement NOYAU × CONTEXTE × MODIFIEURS
- `docs/system/investigation-posture.md` v2.79.3+ · 5 sections IP + confidence chain
- `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ · NIVEAU 0 paramètres décomposés pré-exec
- `docs/system/engagement-disclosure-doctrine.md` v2.79.5+ · close binaire pattern
- `.skills/skills/map-audiences/SKILL.md` · skill chain audience scaffold (mère OR sous-poche)
- `.skills/skills/profile-audience/SKILL.md` · skill chain audience deep drill post-scaffold
- `.skills/skills/produce-paid-angles/SKILL.md` · skill chain angle generation
- `.skills/skills/mine-voc/SKILL.md` · skill chain VOC mining si verbatim manque
- Memory canon `brand_connectors_onboarding_canon` · pattern proactif référence + rendu format opérateur canon

## Anti-patterns banned

- `/add audience` → menu *"Quel type d'audience ? Pain-driven ? Goal-driven ? Identity-driven ? Quelle granularité ? Mère ou sous-poche ? Sourcing ?"* (anti-pattern formulaire)
- `/add angle` → demander *"Quelle audience ? Quel pain ? Quel mechanism ? Quel canal ? Quel format ?"* (anti-pattern collecte info opérateur)
- Lancer skill chain SANS Step 2 read atlas existing préalable (anti-pattern proactif insuffisant)
- Propose 5 options equal-weight sans rationale (anti-pattern menu vs proposition tranchée)
- Skip Step 4 cross-check overlap (anti-pattern duplicates atlas)
