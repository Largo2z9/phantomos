# Brief Distribution Doctrine · Operating Doctrine

> Canonique v2.90.0+. Doctrine canon qui codifie la distribution environnement-aware des briefs produits : le fork de sortie Route A/B (générer par IA vs faire produire par un humain) et le routage adaptatif vers l'outil de centralisation de l'opérateur, détecté et jamais présumé. Doctrine sœur de `contextual-intelligence.md` (no orphan output · le close porte la suite naturelle), `connectivity-layering.md` (distinction MCP / API callable / scripts shipped · vérifier avant d'affirmer), `output-clarity-doctrine.md` (la proposition de distribution respecte le format close canon), `contract-daily.md` (Smart suggests + Connectivity en mode daily). Ferme le gap *"un brief produit qui reste dans le workspace est un brief à moitié livré"* : les skills producteurs de briefs (`produce-copy-brief`, `creative-brief-composer`, `weave-hooks` route B) livrent l'artifact puis s'arrêtent, alors que la suite naturelle (génération IA ou transmission humaine, plus centralisation dans l'outil de l'opérateur) est connue et routable.

---

## 1. Thèse fondatrice

> Un brief produit qui reste dans le workspace est un brief à moitié livré. À la fin de toute production de briefs, le système propose la suite naturelle : générer par IA (Route A) ou faire produire par un humain ou un partenaire (Route B), et dans les deux cas, router les briefs vers l'outil de centralisation de l'opérateur s'il en a un. L'outil n'est JAMAIS présumé : il est DÉTECTÉ.

**Définition canon distribution environnement-aware** · ensemble des pratiques qui font qu'un skill producteur de briefs termine son run en proposant le chemin de sortie adapté à l'environnement réel de l'opérateur. Trois composants : la détection d'environnement (Section 3), la proposition adaptative au close (Section 4), le fork Route A/B (Section 5). Le tout sans aucun nom d'outil en dur dans les skills (Section 6) et sans jamais transformer le close en détour bloquant (Section 7).

Le workspace reste la source de vérité. La distribution est une copie sortante, jamais un déménagement : `brands/{slug}/briefs/` garde l'artifact canonique, l'outil externe reçoit le livrable.

---

## 2. Le problème résolu

1. **Brief orphelin.** Le skill écrit `brands/{slug}/briefs/{BRF-NN}.md`, pointe le path, close. L'opérateur copie-colle à la main vers son Notion, son ClickUp ou un mail à son partenaire vidéo. Friction systématique, à chaque batch, sur le geste le plus prévisible du pipeline.

2. **Outil présumé ou hardcodé.** Sans doctrine, chaque skill author tranche localement : l'un présume Notion, l'autre propose un menu de 5 outils, le troisième ignore la question. Drift cross-skills, et le jour où l'opérateur change d'outil, N skills à patcher.

3. **Question re-posée à chaque batch.** Sans mémorisation, l'agent re-demande "tu centralises où ?" à chaque production. Friction inverse du point 1, tout aussi corrosive pour le trust.

4. **Fork de sortie implicite.** L'opérateur qui reçoit 20 briefs ne sait pas que le système peut générer les créas lui-même (Route A) ou préparer un export propre pour son partenaire (Route B), ni que les deux peuvent coexister sur un même batch. La capacité existe, elle n'est pas matérialisée au moment où elle est actionnable.

---

## 3. Détection d'environnement · ordre canonique (Principe 1)

L'outil de centralisation se détecte en cascade, dans cet ordre. Le premier signal positif suffit, les suivants confirment ou enrichissent (ex : un MCP actif confirme qu'un push direct est possible, pas seulement un export).

| Ordre | Source | Quoi lire |
|---|---|---|
| a | `operator/connected-sources.json` + `brands/{slug}/connected-sources.json` | entrées `sources[]` de type `crm` ou `custom` avec capability `write` (outils de workspace : Notion, ClickUp, Linear, Slack, Drive...) |
| b | Table Ecosystem du `CLAUDE.md` de la marque | outils déclarés dans l'écosystème opérateur, même non câblés |
| c | Clés présentes dans `credentials.env` / `credentials_shared.env` | une clé `NOTION_*`, `CLICKUP_*`, etc. signale un outil actif même sans entrée connected-sources |
| d | MCP disponibles à la session | vérifier RÉELLEMENT (`claude mcp list` ou équivalent session), jamais affirmer sans vérifier |

**Le résultat de la détection** · l'outil de centralisation actif (Notion, ClickUp, Slack, Linear, Drive, email...) ou RIEN. Un résultat RIEN est un résultat valide : il route vers la question proactive unique (Section 4), pas vers une présomption.

**Règles canon détection** ·

- La détection est silencieuse. L'opérateur ne voit jamais la cascade, il voit son outil nommé dans la proposition.
- Signal (b) ou (c) sans connexion vérifiée = outil candidat, pas outil poussable. La proposition devient alors *"je peux me brancher à ton {outil} et y pousser les briefs, on le câble ?"* (route `connect-source`), jamais *"j'envoie dans ton {outil}"* (HR-BD-2).
- Détection au moment du close, pas en pré-flight : l'environnement peut avoir changé depuis le dernier run.

---

## 4. Proposition adaptative au close (Principe 2)

Deux états, deux comportements, zéro menu.

**Outil détecté et connecté** · le close du skill producteur propose le push vers CET outil, nommé, en 1 ligne : *"j'envoie les 20 briefs dans ton ClickUp, liste Briefs créa ?"*. Confirmation explicite avant push (AP-BD-1). Après push, le brief reste consultable dans le workspace (HR-BD-4).

**Rien détecté** · UNE question proactive, une seule fois par marque : *"tu centralises tes briefs quelque part : Notion, ClickUp, autre ? je peux m'y brancher"*. Le traitement de la réponse :

- Réponse positive → router vers `connect-source` (qui écrit l'entrée `connected-sources.json` et gère credentials + scope workspace vs brand). Au prochain batch, l'outil est détecté en cascade (a), la question ne se repose jamais.
- Réponse négative ("nulle part", "je gère à la main") → mémoriser le refus dans `brands/{slug}/config.json#preferences.brief_distribution: "workspace_only"` (réceptacle minimal per-brand, pas de sur-structure · config.json est brand-level et couvert par les ALLOWED_PATH_PATTERNS). La question ne se repose jamais pour cette marque (HR-BD-3). L'opérateur peut rouvrir lui-même via `connect-source` quand il s'équipe.

La question proactive vit au close, après la livraison du brief, jamais au milieu de la production (AP-BD-3).

---

## 5. Fork Route A/B (Principe 3)

À la fin de toute production de briefs, deux routes de matérialisation existent. Le close propose celle qui colle au contexte, l'opérateur arbitre.

**Route A · générer par IA.** Le brief part en génération : `compose-creative` produit les variants, `qc-creative` gate avant toute éligibilité spend. Chemin par défaut pour les formats statiques que le bras de génération couvre.

**Route B · faire produire par un humain ou un partenaire.** Export du brief en markdown propre (l'artifact `briefs/{BRF-NN}.md` est déjà copy-pasteable par construction), push vers l'outil de centralisation détecté, et si pertinent un message d'accompagnement court (contexte + deadline + attentes) prêt à transmettre. Route B est aussi :

- le chemin d'amorçage de l'asset-library : les assets produits par l'humain reviennent dans le workspace via `import-asset`, et nourrissent les composites Route A futurs ;
- le chemin vidéo par défaut tant que le bras de génération vidéo n'est pas câblé.

**Coexistence canon.** Les deux routes coexistent dans un même batch, ventilées par brief : sur 20 briefs, 14 statiques partent en Route A, 6 vidéo partent en Route B vers le partenaire. La ventilation est proposée par l'agent (reco défendue, par format et par capacité du bras de génération), arbitrée par l'opérateur.

---

## 6. Jamais de hardcode (Principe 4)

Aucun outil nommé en dur dans les skills. Les skills producteurs consomment cette doctrine et le résultat de la détection (Section 3), jamais une constante.

- Un skill qui contient *"propose le push vers Notion"* est un bug doctrine. La forme canon : *"propose le push vers l'outil de centralisation détecté"*.
- Si l'environnement change (nouvel outil connecté, ancien outil débranché), le comportement de TOUS les skills producteurs suit au prochain run, sans patch de skill.
- Les exemples avec outils nommés restent légitimes dans les SKILL.md (illustration), tant que la logique reste détection-driven.

---

## 7. Proactivité calibrée (Principe 5)

La proposition de distribution est le next-step contextuel du close, 1 ligne, intégrée à la recommandation forte que tout producer ship déjà (no orphan output). Elle n'est :

- jamais un menu d'outils ou de routes equal-weight (AP-BD-2) : 1 reco défendue (route + outil), alternative en 1 ligne si elle existe vraiment ;
- jamais un détour bloquant avant la livraison du contenu (HR-BD-5) : le brief est livré, pointé, consultable, PUIS la distribution est proposée ;
- jamais une re-négociation de ce qui est déjà mémorisé (HR-BD-3).

---

## 8. Hard Rules canon (HR-BD-1 à HR-BD-5)

### HR-BD-1 · Never présumer un outil non détecté

Aucune proposition de push vers un outil que la cascade Section 3 n'a pas surfacé. Pas de "la plupart des opérateurs ont Notion". Détection ou question, jamais présomption. Violation = bug invalid output canon.

### HR-BD-2 · Always vérifier la connexion avant d'affirmer pouvoir pousser

Un outil déclaré (table Ecosystem, clé env) n'est pas un outil poussable. Avant toute formulation *"j'envoie dans ton X"*, vérifier que la connexion est réelle (entrée connected-sources active OU MCP vérifié à la session). Sinon proposer le câblage via `connect-source`. Cohérent contrat racine *"verify before claiming"*. Violation = bug invalid output canon.

### HR-BD-3 · Never re-poser la question de centralisation si déjà répondue

Réponse positive mémorisée dans `connected-sources.json` (via `connect-source`), réponse négative dans `brands/{slug}/config.json#preferences.brief_distribution` (per-brand, donc "une fois par marque" est littéralement vrai). Une fois par marque, jamais à chaque batch. Violation = bug invalid output canon.

### HR-BD-4 · Always laisser le brief consultable dans le workspace même après push

`brands/{slug}/briefs/` reste la source de vérité. Le push est une copie sortante : jamais de suppression, jamais de "déplacé vers Notion". Le drill workspace (`/phantom {brand}`, `query-context`) doit retrouver le brief après distribution. Violation = bug invalid output canon.

### HR-BD-5 · Never bloquer la livraison du brief sur la distribution

Échec de push, outil down, credentials expirés, opérateur silencieux sur la question : le brief est livré et pointé quand même. La distribution est un enrichissement du close, pas un gate de livraison. Violation = bug invalid output canon.

---

## 9. Anti-patterns canon (AP-BD-1 à AP-BD-3)

### AP-BD-1 · Le push silencieux vers un outil externe sans confirmation

L'agent détecte ClickUp et pousse les 20 briefs sans demander. L'opérateur découvre 20 tâches dans une liste client partagée. Sortie de workspace = action visible par des tiers, confirmation explicite obligatoire (1 ligne au close, réponse binaire). Pattern correctif · Section 4 + HR-BD-2.

### AP-BD-2 · Le menu d'outils à choix multiples au lieu de la détection

*"Tu veux que j'envoie ça vers : (a) Notion (b) ClickUp (c) Slack (d) Drive (e) autre ?"*. Le menu délègue à l'opérateur un travail que la cascade Section 3 fait silencieusement. Pattern correctif · détection d'abord, et si RIEN, une question ouverte unique, pas un menu.

### AP-BD-3 · La question de centralisation posée au milieu de la production

L'agent interrompt le run entre le scoring et l'écriture de l'artifact pour demander où centraliser. Détour bloquant, contenu pas encore livré, friction maximale. Pattern correctif · la question vit au close, après livraison, une fois par marque (Section 4 + HR-BD-5).

---

## 10. Cross-refs

- `.skills/skills/connect-source/SKILL.md` · le mécanisme canon de connexion d'un outil (credentials, scope workspace vs brand, convention, verify) · la réponse positive à la question proactive route ici
- `resources/schemas/connected-sources.schema.json` · runtime state des connexions · entrées type `crm` / `custom` + capability `write` = candidats centralisation (cascade a)
- `.skills/skills/weave-hooks/SKILL.md` · producteur dont la route B est l'incarnation native du fork (export humain/partenaire + amorçage asset-library + chemin vidéo)
- `.skills/skills/produce-copy-brief/SKILL.md` · producer brief mono-angle · consomme cette doctrine au Step 7 (operator-facing chat)
- `.skills/skills/creative-brief-composer/SKILL.md` · orchestrator brief + variants · consomme cette doctrine au Step 5 (synthesis + close ouvert)
- `docs/system/contract-daily.md` · mode daily Connectivity + Smart suggests · la proposition de distribution est un Smart suggest canon
- `docs/system/connectivity-layering.md` · distinction MCP / API / scripts · fonde HR-BD-2 (vérifier avant d'affirmer)
- `docs/system/contextual-intelligence.md` · no orphan output · la distribution EST le next-step naturel post-production de briefs

---

## Status

- **Canonique v2.90.0+.** Codifie le fork de sortie Route A/B et la centralisation adaptative cross-skills producteurs de briefs. Strict additif : les closes existants (`produce-copy-brief` Step 7, `creative-brief-composer` Step 5) sont enrichis, pas remplacés.
- **First applications** · `produce-copy-brief`, `creative-brief-composer`, `weave-hooks` (route B native).
- **Promotion criterion** · à reviewer après 3+ batches distribués sur 2+ environnements distincts (1 outil connecté, 1 workspace_only) sans re-question ni push silencieux.

---

*Doctrine canonique skill-author-facing plus agent-facing. Un brief livré = un brief routé vers sa suite naturelle : Route A (génération IA gatée) ou Route B (production humaine), plus centralisation dans l'outil DÉTECTÉ de l'opérateur. Jamais présumé, jamais hardcodé, jamais bloquant, jamais re-demandé.*
