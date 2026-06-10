# Hook Mechanics Registry

> **TYPE:** Taxonomie — registre vivant (niveau HOOK)
> **C'EST LE `hook-mechanics-registry`** que référencent `decomposition.schema#script.hook.mechanic_id`, `genome.schema#hook.mechanic_id` et `#genome_tags.mechanic_id`. Avant le 2026-06-07, cet enum pointait vers un registre **orphelin jamais construit** ; ce dossier le matérialise (D#488).
> **NIVEAU:** HOOK = l'accroche, les 3 premières secondes. **Territoire VIDÉO (temporel).** DISTINCT de `creative-mechanics-registry.md` (niveau AD = le CONCEPT, territoire image + vidéo).
> **FORMAT:** 1 fichier `{slug}.json` par mécanique (schéma `library-pattern/1.0`) · provenance multi-source + squelette paramétrique + `vertical_scope` (curseur sectoriel) + `related_mechanic_ids` (pont vers l'enum).

## Les deux niveaux de mécanique (D#488)

| | AD-LEVEL (le concept) | HOOK-LEVEL (l'accroche) |
|---|---|---|
| Registre | `creative-mechanics-registry.md` | **ce dossier** (`registries/hooks/`) |
| Champ instance | `decomposition.mecanique.mecanique_id` | `decomposition.script.hook.mechanic_id` |
| Question | « c'est quoi le TYPE d'ad ? » | « comment ça OUVRE ? » |
| Support roi | image **et** vidéo | vidéo (temporel) |
| Sur un statique | **le tag ROI** | souvent absent → `other-uncategorized`, **ne pas forcer** |

## Couverture · enum `hook.mechanic_id` (25) → fiche

**Avec fiche `library-pattern` (promote-ready · ≥2 sources indépendantes) — 16 :**

| enum `hook.mechanic_id` | fiche |
|---|---|
| `resolution-promise` | `resolution-promise-effortless.json` |
| `before-after-timeline` | `before-after-timeline.json` |
| `category-of-one-claim` | `category-of-one-reframe.json` |
| `competitor-comparison-explicit` | `competitor-comparison.json` |
| `confrontation-rhetorical` | `confrontation-rhetorical.json` |
| `if-then-conditional-hook` | `if-then-conditional.json` |
| `listicle-curiosity` | `listicle-curiosity.json` |
| `macro-graphic-icons` | `macro-graphic-icons.json` |
| `mechanism-reveal` | `mechanism-reveal.json` |
| `negative-command` | `negative-command.json` |
| `paradox-testimonial` | `paradox-testimonial.json` |
| `pricing-anchor` | `pricing-anchor.json` |
| `scientific-claim-reveal` | `scientific-claim-reveal.json` |
| `social-relational-pain` | `social-relational-pain.json` |
| `rhetorical-shock-question` | `symptom-shock-question.json` |
| `visceral-specific-testimony` | `visceral-testimony.json` |

(+ le concept structurel `timeline-result-ladder.json` vit dans `resources/concepts/` — c'est un arc, pas un hook.)

**Sans fiche encore (`watch` · 1 source seule ou non curé) — 8 :**
`allegory-romance` · `authority-demolition` · `doctor-dialogue` · `false-solution-debunking` · `hidden-secret-framing` · `pov-illustrated-humor` · `taboo-signal` · `testimonial-paradox-numeric`
→ à curer quand une **2e source indépendante** les confirme (garde-fou `cross-brand-curation.md`).

(+ `other-uncategorized` = fourre-tout, pas une mécanique.)

## Note support (D#488)

Le hook est un objet **vidéo**. Sur une image, le scroll-stop est porté par le **CONCEPT** (la composition) ou par le **titre/accroche-texte** — encodés dans `creative-mechanics-registry.md` + `decomposition.mecanique`, **pas ici**. Ne jamais forcer un hook sur un statique (mettre `other-uncategorized`).

## Curation

Promotion `watch → promote-ready` = ≥2 sources indépendantes (factory multi-marques = 1 source). Doctrine complète : `resources/sops/creative-production/cross-brand-curation.md`. 3 sources indépendantes actuelles : karacare (FR-cheveux), naali (FR-wellness), himshers (US-telehealth).
