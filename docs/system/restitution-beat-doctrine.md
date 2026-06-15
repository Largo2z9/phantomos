# Doctrine · le beat de restitution (D#520)

> SSOT du **beat de restitution** · comment une phase d'encodage MONTRE son travail à
> l'opérateur, au lieu de le compresser en une phrase météo. Référencé par
> `snapshot-brand`, `map-audiences`, `map-angles`, `build-atlas-complete`. Ne pas
> dupliquer le contrat dans les skills · ils pointent ici + passent leurs params.

## Le problème que ça résout

Un run produit un raisonnement dense (sources lues, rejets argumentés, confiance avec
sa cause) puis l'écrase en « la carte est posée ». La cause · le ton ordonne « une
phrase par handoff », et la prose se fait sauter au runtime. **Seul le mécanique tient**
(leçon D#520 · les garanties vont dans le code, pas dans la prose SKILL.md).

Le substrat EXISTE déjà sur disque (provenance, confiance, rejets, journal d'events).
Le beat ne fabrique pas de cognition neuve, il **restitue** ce qui est déjà écrit.

## Le contrat (payload)

Le producteur dépose, pendant que son contexte est frais, un beat-payload à
`.phantom/beats/{slug}/{phase}.json` (état système hors `brands/`, donc **hors gate
mutation** · `Write` direct autorisé, ne transite pas par `write-to-context`).

```json
{
  "phase": "scan|audiences|spectrum|angles|close",
  "verdict":  "<lecture experte top-line, tranchée, une ligne>",
  "read":     "<2-3 phrases · le POURQUOI et son SECOND ORDRE, en prose>",
  "found":    ["<faits / déductions saillants · amorce grasse possible>"],
  "blocked":  [{"source": "<ex Trustpilot>", "reason": "<ex 403, fallback forums>"}],
  "analyzed": ["<déductions, recoupements>"],
  "rejected": [{"what": "<piste écartée>", "why": "<la raison, défendable>"}],
  "encoded":  ["<artefacts posés · pour le record>"],
  "confidence": [{"claim": "<assertion>", "level": "forte|moyenne|faible", "reason": "<la VRAIE cause>"}],
  "basis":    "<une ligne · les sources lues, la largeur du travail · rendue « Lu · ... »>",
  "tease":    "<l'accroche · la valeur DANS la vue · PAS de chemin, le code l'ajoute>"
}
```

Champ vide = omis, jamais inventé.

## Les quatre règles dures

1. **Décision-d'abord, pas process-d'abord.** Le renderer (`render-beat.py`) réorganise
   en · ouverture `verdict` + `read`, puis le raisonnement qui flue (`analyzed` +
   `found` + `rejected`), puis **Ce sur quoi je reste prudent** (`blocked` + confiance
   non-forte, avec leur cause), puis `basis`, puis le CTA, puis la temporalité. Pas de
   labels Trouvé/Analysé/Encodé (c'est le nombril du système, pas la décision de
   l'opérateur). La confiance **forte** n'apparaît pas seule · elle vit dans le verdict.

2. **Richesse · le second ordre, pas le constat.** `read` et `analyzed` déroulent la
   CONSÉQUENCE · l'implication économique, la texture concurrentielle (pourquoi le lane
   est libre, ce qu'il coûte, sa fragilité), et **le nerf** (la tension qui décide tout).
   La densité d'insight fait l'expert 360, pas la longueur.

3. **CTA · `tease` propose, le code exécute.** Le renderer appose la commande
   `/phantom {slug} {vue}` paste-ready et **choisit la vue selon la phase** (table
   ci-dessous). Jamais une vue pas encore construite.

4. **Temporalité + mode.** Le beat connaît sa place dans la chaîne (forward-look) et son
   mode. Les items `prudent` peuvent pointer l'étape qui les lèvera (« à confirmer à
   l'étape voix-client qui vient »). Le mode arme la proactivité ·
   - **orchestré** (`--mode orchestrated`, défaut) · le beat signale le cap
     (« _Et après · …_ »), l'orchestrateur enchaîne tout seul.
   - **standalone** (`--mode standalone`) · le skill modulaire est arrivé seul, il
     **propose** la suite (« Prochaine étape · … Je lance ? ») · la proactivité vient de là.

## Tables (le code décide, pas le modèle)

| phase | vue `/phantom` (construite à ce moment) | forward-look (`PHASE_NEXT`) |
|---|---|---|
| `scan` | `products` (décompo · le spectre n'existe pas encore) | dériver les audiences du mécanisme |
| `audiences` | `audiences` | croiser en carte de marché (le spectre) |
| `spectrum` | `spectre` | écrire les angles par territoire |
| `angles` | `matrix` | scorer la matrice, sortir les axes |
| `close` | `atlas` | terminal |

## Émission (mécanique, D#520)

1. Le producteur écrit le payload (`Write` → `.phantom/beats/{slug}/{phase}.json`).
2. L'orchestrateur (ou le skill standalone) émet le beat ·
   `python3 .skills/render-beat.py --brand {slug} --phase {phase} --mode {mode}` et
   présente sa sortie **telle quelle**. NE re-narre pas, NE re-résume pas.
3. Le hook `beat-emit` (PostToolUse/Task) garantit qu'un payload frais non-émis est
   montré (il pousse l'orchestrateur s'il l'oublie). `render-beat` écrit un marqueur
   `.emitted` pour ne pas re-pousser.
4. **Filet** · si `render-beat` rend du vide (pas de payload), retomber sur la synthèse
   en prose · ne JAMAIS laisser un trou à la place de la phase.

## Format report (cf Shape of Key)

Prose d'ouverture (verdict + read), puis bullets à **amorce grasse**
(`**la thèse.** le pourquoi en clair`), puis le CTA. Registre sharp, pair-expert,
jamais météo. « Montrer le travail » = les faits, les rejets, la confiance-avec-cause ·
JAMAIS les noms de skills, les chemins, les scores bruts (cf operator contract).

## La modalité suit le contenu (le beat n'a pas une vue, il en a le bon type)

Le bon format dépend du TYPE LOGIQUE de la réponse · forcer une matrice là où il faut
un listing (ou de la prose là où il faut une carte) brouille.

| Type de réponse | Modalité | Exemples |
|---|---|---|
| Énumération | **listing** | les audiences, les angles, les inconnus, les sources lues |
| Jugement | **interprétation** (prose) | le verdict de position, le wedge, le second ordre |
| Croisement 2D | **matrice** | couverture use_case × audience, scoring audience × angle |
| Topologie / flux | **carte / graphe** | sankey Mc → audiences, 2x2 de position, graphe de relations |

**Plusieurs vues par étape.** Une étape a souvent plusieurs FACETTES, chacune servie par
une modalité différente, chacune répondant à une question différente. L'arbre d'audiences ·
listing (« c'est quoi ? ») + interprétation (« laquelle compte ? ») + graphe (« d'où elles
viennent ? · Mc → use_case → audience ») + matrice (« comment elles mappent aux douleurs ? »).
Une étape rend un SET de vues complémentaires quand les facettes diffèrent, pas une vue unique.
L'opérateur choisit la profondeur.

## Les deux registres (toujours les deux, jamais l'un sans l'autre)

- **R1 · l'interprétation experte** · le verdict, l'analyse fine, le second ordre → pour
  **DÉCIDER**. C'est le beat / le close / la prose du drill.
- **R2 · la situation back-end / les sources of truth** · quel fichier porte le claim, sa
  **provenance** (vu / déduit), le `reliability_tier`, l'event qui l'a produit, le
  `confidence_chain` → pour **SE SITUER, FAIRE CONFIANCE, AUDITER**.

Le lien obligatoire = **le drill garanti** · depuis tout read (R1), la source (R2) est à
UN hop (`/phantom {brand} {entity} {item}` → la pièce + sa provenance + sa confiance).
L'opérateur reste sur le read, ou plonge dans la vérité. R2 ne fabrique rien · il réutilise
le substrat qui existe (les JSON SSOT, le journal d'events avec son `reason`, la provenance
3 couches, le `confidence_chain`) · invocation, pas contenu neuf. Un read dont la SSOT
n'est pas atteignable d'un hop est un read qui demande de le croire sur parole · interdit.
