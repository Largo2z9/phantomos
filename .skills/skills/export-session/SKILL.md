---
name: export-session
type: capturer
version: "1.0.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
description: >
  Export a Claude Code conversation (current or past) to a clean markdown transcript stored
  under _sessions-archive/. Useful to archive friction sessions for later doctrine audit, to
  build an external knowledge base of how the agent behaves, or to share a session with a
  collaborator. Defaults to interactive pick when ambiguous, exports the current session
  when explicitly asked.
  FR triggers: "exporte la session" "exporte cette conversation" "archive cette session"
  "garde une trace de cette conv" "exporte la session d'hier" "exporte les sessions de
  cette semaine".
  EN triggers: "export this session" "archive this conversation" "save this session"
  "export last session" "export sessions from this week" "dump session as markdown".
  FR: "exporte cette session", "archive cette conversation", "exporte la conversation en markdown".
  EN: "export this session", "archive this conversation", "export session transcript".
permissions:
  reads: [workspace]
  writes: [workspace]
  mode: direct
  subagent_safe: true
pipeline:
  preconditions: Claude Code is the runtime, the session JSONL is reachable under ~/.claude/projects/.
  postconditions: One or more markdown files written under _sessions-archive/{YYYY-MM-DD}-{slug}.md.
disambiguates_against:
  capture-learning: "route to capture-learning when the operator wants to persist a single fact or insight as a structured learning entry. export-session captures the entire conversation as a transcript, not a learning."
  ingest-resource: "route to ingest-resource when the operator brings external content (PDF, article, transcript from a different system) to integrate into the workspace knowledge layer. export-session is one-way out, ingest is one-way in."
---

## Tone

Court et factuel. "Exportée. Lien vers le fichier." Pas de cérémonie. Si plusieurs sessions matchent ou sont ambiguës, montrer la liste et demander quel numéro.

# Skill: Export Session

Capture une session de conversation Claude Code en markdown propre, lisible, archivable. Utile pour auditer rétrospectivement les frictions, pour partager une session, ou pour alimenter une base de connaissances de comportement agent.

---

## Step 1, identifier la session à exporter

Le mode dépend du trigger naturel et des arguments éventuels.

**Mode courant (défaut implicite)**. Trigger : *"exporte cette conversation"*, *"exporte la session"* sans plus de contexte. Action : exporter la session en cours (la plus récente dans le dossier `~/.claude/projects/{escapedpath}/`).

**Mode pick (interactif)**. Trigger : *"exporte une session"*, *"laquelle ?"*, ou ambiguïté détectée. Action : lister les 20 sessions les plus récentes avec timestamp, premier message, modèle, nombre de turns, et demander à l'opérateur quel numéro choisir. Pas de questionnaire avant, juste la liste.

**Mode filter (par critère)**. Trigger : *"exporte la session d'hier"*, *"exporte la session sur les créatives"*, *"exporte la session 4f3a"*. Action : matcher par date (YYYY-MM-DD prefix), par UUID prefix, ou par topic substring dans le premier message. Si plusieurs matchs, basculer en mode pick avec les matchs filtrés.

**Mode batch (par durée)**. Trigger : *"exporte toutes les sessions de cette semaine"*, *"archive les sessions des 3 derniers jours"*. Action : parser la durée et exporter toutes les sessions plus récentes que le cutoff. Pratique pour archivage périodique.

---

## Step 2, exécuter l'export via le helper Python

Le script `.skills/export-session.py` fait le travail. Invocation par mode :

**Courant** :
```bash
python3 .skills/export-session.py --current
```

**Pick interactif** :
```bash
python3 .skills/export-session.py --pick
```

**Filter** :
```bash
python3 .skills/export-session.py --session "2026-04-29"
python3 .skills/export-session.py --session "creative-analysis"
python3 .skills/export-session.py --session "4f3a8b2c"
```

**Batch** :
```bash
python3 .skills/export-session.py --since "1 week"
python3 .skills/export-session.py --since "3 days"
```

**Lister sans exporter** :
```bash
python3 .skills/export-session.py --list
```

**Options communes** :
- `--to <path>` change le dossier de sortie (défaut `_sessions-archive/`)
- `--no-thinking` retire les blocs de réflexion interne du markdown
- `--workspace <path>` pour cibler un workspace différent du cwd

---

## Step 3, surfacing à l'opérateur

Aprés export, surface en une phrase :
- Mode mono-session : *"Exportée vers `_sessions-archive/2026-04-29-creative-analysis.md`."*
- Mode batch : *"Exporté 7 sessions vers `_sessions-archive/`. Liste : ..."* (max 5 noms inline, le reste en `..` et N).

Pas de récap du contenu. Pas de demande de validation. C'est un export, pas un audit.

---

## Step 4, optional, push vers un repo Git

Si le workspace est un repo Git ET si la variable `SESSIONS_ARCHIVE_REMOTE` est définie dans `credentials_shared.env` (URL du repo distant dédié aux archives), l'agent peut proposer en fin d'export :

> *"Veux-tu que je push vers `phantomos-sessions-archive` ?"*

Si confirmé, l'agent exécute :
```bash
cd _sessions-archive && git add . && git commit -m "Archive session {date} {slug}" && git push
```

Si la variable n'est pas définie, ne pas proposer. L'export reste local.

---

## Hard rules

- Le helper Python `.skills/export-session.py` est la seule porte d'écriture. L'agent ne fabrique pas le markdown lui-même.
- Si aucune session n'est trouvée pour le workspace courant, signaler honnêtement *"Aucune session Claude Code trouvée pour ce workspace"*. Ne pas inventer.
- Le mode pick est le défaut quand l'opérateur dit *"exporte"* sans préciser. Pas d'assumption sur "courante" qui peut surprendre.
- Le markdown généré inclut les blocs de thinking par défaut (visibilité maximale pour audit). L'opérateur peut demander `--no-thinking` s'il veut un transcript plus léger.
- Pas de duplicata : si le fichier de sortie existe déjà, le script ajoute un suffixe `-2`, `-3`, etc.

---

## Cross-references

- `.skills/export-session.py` · helper Python qui fait le parsing et l'écriture
- `~/.claude/projects/` · racine où Claude Code stocke les JSONL de session
- `_sessions-archive/` · dossier de sortie par défaut dans le workspace
- `capture-learning` · sister skill pour persister un fait ponctuel (pas une session entière)

---

## Status

- **v1.0** · ship 2026-04-29.
- **Suivi** : si un repo `phantomos-sessions-archive` est créé et configuré dans `credentials_shared.env`, le push automatique devient une option fin de Step 4.
- **Pattern detection** : sessions exportées peuvent être analysées par un futur skill `audit-friction-patterns` côté build operator-kb pour identifier patterns récurrents (questionnaire avant action, sycophant pavlov, vouvoiement raté, etc.) et patcher la doctrine.
