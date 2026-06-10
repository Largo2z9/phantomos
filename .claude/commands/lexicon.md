---
name: lexicon
description: Lexique opérateur-facing PhantomOS · 10-15 magic keywords canon (cartographie · atomicité · fractalité · composition · décompose · adapt · territoire · brief · audit · breakdown · etc.) + leur usage prompting + exemples concrets. Pour prompter efficient avec PhantomOS dès le premier jour et 6 mois après. Cible · opérateur novice complet pour onboarding + opérateur expert pour rappel.
---

# `/lexicon` · magic keywords PhantomOS pour prompter efficient

Lexique opérateur-facing PhantomOS. Liste 10-15 magic keywords canon qui débloquent les bons skills et les bons raisonnements quand tu prompts. Pour onboarding ET usage 6 mois après.

**Cible** · opérateur novice complet (premier jour) + opérateur expert (rappel). Vocabulaire universel · zéro jargon plumbing.

**Comment utiliser** · quand tu prompts PhantomOS, utilise ces termes pour activer les bons skills et obtenir des outputs structurés canon. L'agent comprend le terme canon · il route vers le bon skill ou la bonne mécanique.

---

## Magic keywords PhantomOS

### Cartographier

**Usage prompting** · "cartographie mes audiences" · "cartographie ce sujet" · "fais-moi une cartographie de X".

**Ce que ça déclenche** · l'agent identifie la hiérarchie des niveaux, mappe les éléments en grille structurée (parent/enfants OR matrice 2D selon contexte). Pour audiences · profil-audience hiérarchique. Pour livrables · score-matrix top-3 territoires.

**Exemple concret** · "cartographie mes 3 produits par audience visée" → matrice produits × audiences avec cellules scorées.

---

### Décomposer

**Usage prompting** · "décompose cette ad concurrente" · "décompose cet angle" · "que dit cette pub".

**Ce que ça déclenche** · skill `decompose-ad` v2.1.0 reverse-engineering microscopique · fiche 5 sections + grille ANATOMIE 3 niveaux + fit-check brand. Pour angle interne · `decompose-angle` 11 atoms canon.

**Exemple concret** · "décompose cette pub TikTok concurrente · regarde si ça fit ma brand" → fiche complète + scoring fit + reco adapt/skip.

---

### Adapter

**Usage prompting** · "adapte cette ad à ma brand" · "reprends ce concept" · "adapte-moi ça".

**Ce que ça déclenche** · skill `adapt-from-competitor` v1.0.0 orchestrator · pré-rempli refs canoniques brand + 3 paths flow (variant complet · 1 axe seul · registry promotion).

**Exemple concret** · "adapte ANG-01 concurrent à mon audience workers-shifts" → brief copy variant Meta-ready avec NOYAU preserved + CONTEXTE adapté.

---

### Composer

**Usage prompting** · "compose un brief copy" · "compose une variante visuelle" · "compose la créa hero".

**Ce que ça déclenche** · skill `creative-brief-composer` orchestrator OR `compose-creative` · pipeline produire brief copy + N variants visuels Meta-ready depuis angle interne canonical.

**Exemple concret** · "compose le brief copy de l'angle ANG-03 produit pour audience chronic-pain-45" → brief structuré + 3 variants visuels.

---

### Atomicité

**Usage prompting** · "encode cette douleur comme atome" · "atomise ce concept" · "isole l'atome de sortie de X".

**Ce que ça déclenche** · raisonnement canonique · découpe le savoir en entités identifiées réutilisables · cross-refs canonical entre atomes (PNT-NN · OBJ-NN · ANG-NN · FRC-NN · CRT-NN · etc.).

**Exemple concret** · "atomise les douleurs de mon audience workers-shifts" → 4-6 douleurs identifiées PNT-NN avec chain surface → consequence → deep.

---

### Fractalité

**Usage prompting** · "le même pattern à toutes les échelles" · "fractalise ce schéma" · "applique le motif à plusieurs niveaux".

**Ce que ça déclenche** · raisonnement canon · le motif observation/tension/réponse/appel revient à toutes les échelles (brand · audience · douleur · angle). Auto-similarité.

**Exemple concret** · "fractalise mon positionnement" → motif OTR appliqué à brand-level + audience-level + angle-level cohérent.

---

### Composition

**Usage prompting** · "compose les couches" · "applique l'équation noyau × contexte × modifieurs" · "calcule le livrable à partir de X".

**Ce que ça déclenche** · équation canon LIVRABLE = NOYAU × CONTEXTE × MODIFIEURS · le système combine les ingrédients à chaque invocation · tu choisis le contexte, le système compose.

**Exemple concret** · "compose un hook pour workers-shifts en saison hiver" → hook calculé selon noyau (composition produit) × contexte (audience + verbatim) × modifieurs (saison + canal + ton).

---

### Territoire

**Usage prompting** · "regarde mon territoire" · "qu'est-ce que j'ai dans mon territoire" · "encode dans le territoire".

**Ce que ça déclenche** · raisonnement canon · le territoire = substrat stable de la brand (identity + positioning + audiences + produits + angles + offers) · encodé une fois · alimente les productions runtime à la demande.

**Exemple concret** · "regarde mon territoire Stepprs" → snapshot brand digest + 7 entités canon + cross-refs · l'agent charge tout en 1 lecture.

---

### Audit perf

**Usage prompting** · "audit mes performances Meta" · "audit ce compte" · "diagnostic CPA/ROAS".

**Ce que ça déclenche** · skill `audit-meta-account` · dimensions auditables canoniques + diagnostic frictions + recommandations stratégiques.

**Exemple concret** · "audit perf compte Meta Stepprs Q3" → rapport structuré 5 sections IP + verdict pass/fail par dimension + plan correction priorisé.

---

### Brief day

**Usage prompting** · "où j'en suis" · "fais-moi un brief journalier" · "état de la marque maintenant".

**Ce que ça déclenche** · skill `brief-day` · état brand · décisions en suspens · prochaines actions priorisées. Rituel canon début de session.

**Exemple concret** · "où j'en suis sur Stepprs" → 5 lignes synthese · 3 territoires top priorisés · angle hero testé sur 5 marchés · arbitrage en attente.

---

### Investigation 5 sections

**Usage prompting** · "synthese 5 sections" · "investigation-posture" · "ne ferme pas sur conclusion · garde ouvert".

**Ce que ça déclenche** · posture canon · toute synthese stratégique structurée Observé · Déduit · Inconnu · Leviers · Close ouvert. L'agent ne ferme jamais la conversation · l'opérateur arbitre.

**Exemple concret** · "audit en 5 sections" → output rigoureux avec étiquettes d'origine sur chaque assertion + leviers actionnable + close question opérateur.

---

### Apprends de la session

**Usage prompting** · "learn from session" · "persiste les learnings" · "enregistre ce qu'on a fait".

**Ce que ça déclenche** · skill `learn-from-session` · capture décisions + frictions + apprentissages dans session-log + project-state. Rituel canon fin de session.

**Exemple concret** · "learn from session" en fin de travail → session-log enrichi + project-state mis à jour + memory refreshed cross-sessions.

---

### Adapt extension

**Usage prompting** · "ajoute une NEW entity" · "scaffold extension" · "étends mon workspace pour tracker X".

**Ce que ça déclenche** · skill `scaffold-extension` orchestrator · 9 phases canon (intent · existing-coverage · domain-canon · schema-draft · naming · cross-refs · canon-validation · scaffold-files · register) avec méthode ECR runtime via analyze-extension-intent v2.0.0.

**Exemple concret** · "j'aimerais tracker les avis Reddit pour ma brand" → orchestrator chain · scaffold NEW skill ou NEW entity selon intent · décomposition ECR guidée.

---

### Breakdown

**Usage prompting** · "breakdown" · "explique-moi comment X marche" · "via Stepprs".

**Ce que ça déclenche** · slash command `/breakdown stepprs {topic}` · vitrine pédagogique 13 topics structurés 5 couches + 3 dimensions transverses · explique PhantomOS via cas concret réel Stepprs.

**Exemple concret** · "breakdown stepprs composition" → fiche pédagogique structurée + diagramme cartographique + propriété structurelle + lecture opérateur + drill suivant.

---

## Pattern canon · combiner les keywords

Tu peux combiner plusieurs keywords dans 1 prompt pour activer raisonnement multi-couches ·

- "cartographie mes audiences ET atomise les douleurs" → map-audiences + profile-audience pain_points
- "décompose cette ad concurrente ET adapte à ma brand" → decompose-ad + adapt-from-competitor chain
- "fractalise mon positionnement ET compose les hooks" → raisonnement canon multi-échelles + composition équation
- "audit perf ET brief day suivant" → audit-meta-account + brief-day chain quotidien

L'agent comprend les enchaînements canoniques sans que tu nommes les skills.

---

## Quand utiliser `/lexicon`

- **Onboarding** · première session · scanner les magic keywords pour savoir comment prompter
- **Rappel** · 3 mois après · oublié un terme · `/lexicon` rafraîchit
- **Avant un prompt complexe** · vérifier que tu utilises le bon vocabulaire canon
- **Quand l'agent ne fait pas ce que tu veux** · peut-être que ton prompt manque un magic keyword qui débloquerait le bon skill

## Cross-refs

- `/skills` · catalogue navigable des capacités (drill par catégorie)
- `/phantom` · cockpit de visualisation brand state
- `/breakdown stepprs {topic}` · vitrine pédagogique via cas concret
- `tour.md` Milestone 6 · introduction triade commands universal entry point
