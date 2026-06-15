---
name: promote-learning
type: curator
version: "1.0.0"
recommended_model: sonnet
layer: meta
reasoning_pattern: null
description: >
  Promotes a brand-specific learning to the shared KB when it proves generic.
  Evaluates if a learning from brands/{slug}/learnings.json applies across brands,
  then routes it to the appropriate shared resource (convention, catalogue, framework, etc.).
  FR: "promote ce learning" "ce learning est générique" "ajoute ça à la KB" "ce truc marche pour toutes les brands" "learning vers KB" "passe ça en shared".
  EN: "promote this learning" "make this learning shared" "add to KB" "this applies to all brands" "promote to shared".
permissions:
  reads: [learning]
  writes: [learning]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: learning must exist in brands/{slug}/learnings.json
  postconditions: run validate-resources to reconcile integrity
---

## Tone

Explique en langage simple pourquoi ce learning est promu (utile pour toutes les marques) et où il atterrit. Pas de paths techniques.
---

# Skill: Promote Learning

Pont entre les apprentissages brand-specific et la KB partagée.
Un learning brand naît dans `learnings.json`. S'il s'avère générique (applicable à d'autres brands), il est promu vers `resources/` comme convention, catalogue entry, ou framework update.

**Pourquoi ce skill existe** : sans promotion, le savoir s'accumule dans des fichiers brand isolés et n'est jamais réutilisé. Avec 8+ brands, les mêmes découvertes sont faites 8 fois.

---

## Step 1 — Identify the Learning

Trois entry points possibles :

### A — Opérateur pointe un learning spécifique
L'opérateur dit "promote ce learning" + référence (texte, index, ou description).
→ Lire `brands/{slug}/learnings.json`, trouver l'entrée correspondante.

### B — Agent détecte un candidat de promotion (1 marque suffit)
Lors d'un ingest ou validate, l'agent remarque un learning à forte généricité (`genericity: sector|universal`) OU un pattern récurrent. UNE seule marque suffit pour PROPOSER — l'agent propose, l'opérateur arbitre. La récurrence cross-brand (2+ brands) renforce le signal mais n'est pas un prérequis.
→ Lister le/les learning(s) candidat(s), proposer la promotion. L'opérateur tranche.

### C — Depuis le promote-backlog.json (si présent)
L'opérateur dit "quels learnings sont prêts à promouvoir ?" ou "promote backlog".
→ `promote-backlog.json` est un artefact OPTIONNEL, écrit par `validate-resources` Check 12b UNIQUEMENT si un run `validate all` (cross-brand) a détecté un candidat. Il N'EXISTE PAS sur un workspace fresh.
→ Si le fichier existe : lire → présenter les candidats ordonnés par priorité → l'opérateur choisit.
→ Si le fichier est absent : NE PAS échouer. Répondre "Pas de backlog pré-calculé (lance `validate all` pour scanner cross-brand). Je peux scanner les learnings de {brand} maintenant ?" puis basculer sur l'entry point B (détection live).

**Output Step 1** : le learning candidat avec son contexte :
```
Learning candidat :
  Brand : {slug}
  Fact : "{fact}"
  Platform : {platform}
  Tags : {tags}
  Date : {date}
  Source : {source}
```

---

## Step 2 — Evaluate Genericity

Le learning est-il brand-specific ou générique ?

| Test | Brand-specific | Générique |
|------|---------------|-----------|
| Mentionne un account ID, budget, ou KPI spécifique ? | Oui → brand | Non |
| Applicable sans modification à une autre brand du même secteur ? | Non | Oui → générique |
| Applicable à une autre brand d'un AUTRE secteur ? | Non | Oui → très générique |
| Contient un workaround technique plateforme ? | Parfois | Souvent → convention |
| Contient un pattern de performance validé ? | Parfois | Souvent → catalogue entry |

**Décision** :
- **Brand-specific** → NE PAS promouvoir. Dire à l'opérateur pourquoi. Fin du skill.
- **Secteur-générique** → promouvoir avec tag secteur
- **Universel** → promouvoir sans restriction

---

## Step 3 — Route to Shared Resource

Déterminer la destination dans `resources/` :

| Type de learning | Destination | Exemple |
|-----------------|-------------|---------|
| Workaround technique plateforme | `conventions/{platform}.json` | "Meta rejecte les images avec >20% texte → utiliser overlay" |
| Pattern de performance (angle, hook, format) | `catalogues/{domain}.json` (nouvelle entrée) | "Hook question + chiffre clinique = CTR >3% en skincare" |
| Règle de décision contextuelle | `routing/{dim1}-{dim2}.json` (nouvelle ligne) | "Audience problem-aware + prix >50€ → angle barrier-removal" |
| Modèle mental / principe | `frameworks/{slug}.json` (enrichir) | "En nutrition, benefit chains doivent mentionner le mécanisme pour convertir" |
| Procédure validée | `sops/{verb}-{object}.json` (enrichir ou créer) | "Pour scaler un adset, augmenter budget de 20% max/jour" |

**Si aucun type ne matche** → demander à l'opérateur : "Ce learning ne rentre pas dans les types existants. Tu veux créer une nouvelle convention ?"

---

## Step 4 — Write to KB (via ingest-resource)

Ne pas écrire directement. Appeler **ingest-resource** avec le learning reformulé :

1. **Reformuler** le learning en format KB :
   - Conventions : `{ "rule": "...", "platform": "...", "source": "learning promotion from {brand}", "validated_date": "..." }`
   - Catalogues : nouvelle entrée avec ID auto-généré
   - Routing : nouvelle ligne dans la table de décision

2. **Appeler ingest-resource** en mode "Call from learn-from-session" (Step 2 entry point, déjà classifié)

3. **Tagger la source** : ajouter `"promoted_from": "{brand_slug}"` et `"promotion_date": "{today}"` dans les métadonnées de la ressource

---

## Step 5 — Mark Learning as Promoted

Dans `brands/{slug}/learnings.json`, marquer l'entrée promue. `promoted_to` + `promoted_date` sont schema-legal (learnings/1.2) et visent la KB partagée `resources/` (distinct de `promoted_to_canon` + `promoted_canon_path` qui visent `resources/canon/copy/`). Append via write-to-context (jamais éditer en place — créer le marquage selon la discipline append-only de la skill) :

```json
{
  "fact": "...",
  "tags": ["meta_ads", "creative", "promoted:conventions/meta-ads"],
  "promoted_to": "resources/conventions/meta-ads.json",
  "promoted_date": "2026-04-04"
}
```

Le learning reste dans `learnings.json` (append-only, jamais supprimé). Le tag `promoted:` signale qu'il a été promu et où.

---

## Step 6 — Summary Output

```
📤 Learning promu vers la KB partagée

Brand source : {slug}
Learning : "{fact}"
Destination : {resources/{type}/{file}.json}
Action : {ENRICHI resource existante | CRÉÉ nouvelle entrée}
Tag promotion : promoted:{type}/{file}

Ce learning est maintenant accessible à toutes les brands du workspace.
```

---

## Détection automatique (pattern cross-brand)

Quand validate-resources scanne les learnings de plusieurs brands (mode all-brands), il peut détecter des candidats à la promotion :

**Critère** : même `platform` + tags overlap >60% + `fact` sémantiquement similaire dans 2+ brands.

**Action** : ajouter un flag `learning_promotion_candidate` dans `todos.md` de la première brand détectée :
```
- [ ] Learning promotion candidate | "{fact}" (also in {other_brand}) | P: 2
```

L'opérateur décide ensuite de promouvoir ou non.

---

## Hard Rules

- **Jamais supprimer** un learning de `learnings.json` — append-only. Marquer comme promu, jamais effacer.
- **Jamais promouvoir un learning brand-specific** — le test de généricité (Step 2) doit passer.
- **Toujours passer par ingest-resource** pour écrire dans la KB — ne pas écrire directement.
- **Toujours demander confirmation** avant de promouvoir — sauf si l'opérateur a explicitement dit "promote".
- **Toujours tagger la source** — `promoted_from` + `promotion_date` dans la ressource KB, `promoted_to` dans le learning.
- **Un learning = une promotion** — si un learning contient plusieurs insights, splitter en promotions séparées.
- **Après chaque promotion, retirer le candidat de promote-backlog.json _si le fichier existe_.** Ne jamais échouer si le backlog est absent (workspace fresh, ou aucun `validate all` lancé) — le backlog est un artefact optionnel, pas un prérequis.
