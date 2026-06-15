---
name: capture-learning
type: capturer
version: "1.0.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
description: >
  Quick append of a single operational learning to learnings.json.
  Low friction — no full ingest ceremony.
  FR: "capture ce learning" "note ça" "retiens que" "ajoute dans les learnings" "on a découvert que" "garde en tête".
  EN: "capture learning" "remember that" "note this" "save this learning" "log this insight".
permissions:
  reads: [brand]
  writes: [learning]
  mode: direct
  subagent_safe: true
pipeline:
  preconditions: brand slug known or inferable from context
  postconditions: one entry appended to brands/{slug}/learnings.json via write_to_context()
---

## Tone

Court et direct. "Noté." + rappel du fait capturé en une phrase. Pas de cérémonie.

# Skill: Capture Learning

Quick append d'un learning opérationnel. Un fait → une entrée → terminé.

---

## Step 1 — Extraire le fait

Si l'opérateur a donné le fait dans le trigger → l'utiliser directement.
Si le trigger est vague ("note ça") → demander : "Quel est le fait à capturer ?"

Identifier :
- **Le fait** : la règle, le comportement, le workaround, le résultat observé
- **La brand** : inférer depuis le contexte de session. Si ambigu → demander.
- **La plateforme** (optionnel) : Meta, Shopify, Google, etc. — si mentionnée
- **La source** (optionnel) : test, client call, platform docs, observation directe

---

## Step 2 — Classer le learning

Déterminer automatiquement :

| Champ | Règle d'inférence |
|---|---|
| `scope` | "platform" si plateforme mentionnée, "brand" sinon |
| `type` | "workaround" si contourne un problème · "compliance" si règle platform · "behavior" si comportement observé · "test_result" si résultat d'un test · "api_rule" si limite API |
| `tags` | Inférer 1-3 tags depuis le fait (ex: ["meta", "carousel", "links"]) |
| `status` | Toujours `"active"` à la création |
| `genericity` | "brand" par défaut · "sector" si probablement vrai pour le secteur · "universal" si vrai partout |

---

## Step 3 — Générer l'entrée

Format :

```json
{
  "id": "LRN-{NNN}",
  "kind": "{test_result|workaround|compliance|observation|decision_trace|hypothesis_validated|pattern_promoted|regulatory_signal|competitor_move}",
  "fact": "{le fait en une phrase claire}",
  "reasoning": "{pourquoi c'est vrai, ce qui l'a causé, ce que ça révèle — MANDATORY non-vide}",
  "scope": "{brand|platform|workspace}",
  "platform": "{platform ou null}",
  "type": "{workaround|compliance|behavior|api_rule|test_result}",
  "created_at": "{ISO date-time}",
  "date": "{YYYY-MM-DD}",
  "source": "{operator|test|client_call|platform_docs|observation}",
  "tags": ["{tag1}", "{tag2}"],
  "status": "active",
  "genericity": "{brand|sector|universal}",
  "superseded_by": null,
  "promoted_to": null
}
```

**Mapping kind ↔ type** · `kind` est l'autorité canon (9-enum, consommée par brief-day/learn-from-session detection). `type` est l'alias dialecte conservé pour compat. Règle rapide : test→`kind:test_result`, contournement→`workaround`, règle plateforme→`compliance`, comportement observé→`observation`. Toujours remplir `created_at` (date-time) ET `date` (court) — validate lit `date` puis fallback `created_at`.

**CRITICAL: `reasoning` field is MANDATORY, non-empty.** This is the **Decision Trace** (see D#308). The `fact` captures WHAT, the `reasoning` captures WHY. Without the why, the learning is just logged data, not codified expertise. **YOU MUST NEVER** write an entry with `reasoning: ""`, `reasoning: null`, or `reasoning: "n/a"`.

Examples:
- ❌ `fact: "Meta rejects ads with 'cure' claim"`, `reasoning: ""`
- ✅ `fact: "Meta rejects ads with 'cure' claim"`, `reasoning: "Healthcare claim policy, enforced since Jan 2025 — confirmed via policy doc + 3 rejections this month on Northsense's supplement angles"`

If the operator can't articulate the why, **push back** : *"Je peux pas ranger ça sans le pourquoi. Qu'est-ce qui a causé ça, ou ce que ça révèle ?"*. If after push-back the operator insists → flag entry with `reasoning: "[captured without rationale — revisit on first application]"` and continue, but this is degraded mode.

**ID generation :** lire `learnings.json → entries`, prendre le dernier ID, incrémenter. Si vide → commencer à LRN-001.

---

## Step 4 — Confirmer et écrire

Afficher un résumé court :

```
Learning capturé :
"{fait}"
→ Type : {type} · Scope : {scope} · Tags : {tags}

Confirme ? (ou dis "corrige {champ}" pour ajuster)
```

Si confirmé → **exécuter** (Bash, pas pseudo-code) :

```bash
python3 .skills/write-to-context.py \
  --path "brands/{slug}/learnings.json#entries[]" \
  --value '{entrée JSON complète sur une ligne}' \
  --source operator \
  --confidence 1.0 \
  --mode direct \
  --reason "{1 phrase: d'où vient ce learning}"
```

Le script est le SEUL canal sanctionné pour écrire dans `brands/` et `operator/`. Toute autre méthode (Edit, Write, python -c json.dump, echo >, sed -i, tee) est bloquée par le hook mutation-guard. Si le script échoue, surface l'erreur à l'opérateur — ne PAS contourner.

Confirmer :
```
✓ Noté dans les learnings de {brand}.
({N} learnings au total)
```

---

## Hard Rules

- **Un seul learning par invocation.** Si l'opérateur en mentionne plusieurs → traiter le premier, proposer de capturer les suivants.
- **Jamais modifier une entrée existante.** Si le fait contredit un learning existant → créer une nouvelle entrée avec `superseded_by: "LRN-XXX"` sur l'ancienne.
- **Toujours confirmer avant d'écrire.** Même pour Haiku — la confirmation prend 1 échange.
- **Pas de `_proposed: true`** pour les learnings opérateur. Confidence = 1.0, mode = direct.
