---
name: connect-mcp-server
type: orchestrator
version: "1.0.0"
recommended_model: sonnet
isolation_scope: workspace_global
layer: meta
description: >
  Guide opérateur dans setup MCP server. Layer 1 (MCP configurés au niveau
  Claude Code, pas shippés avec le template). Targets defaults PhantomOS :
  facebook-graph, youtube-transcript, supabase, google-calendar. Plus custom
  (gmail, slack, notion, clickup, excalidraw, etc.). Lit `.mcp.json.example`
  template + invoque `claude mcp add` interactif. Verify state via `claude mcp list`.
  FR: "connecte MCP", "ajoute MCP server", "setup MCP", "branche en MCP", "configure MCP".
  EN: "connect MCP", "add MCP server", "setup MCP", "wire as MCP", "configure MCP".
permissions:
  reads: [".mcp.json", ".mcp.json.example", "credentials_shared.env"]
  writes: []
  mode: interactive
  subagent_safe: true
  bash: ["claude mcp add", "claude mcp list", "claude mcp remove"]
pipeline:
  preconditions: operator on a Claude Code install with `claude` CLI on PATH
  postconditions: |
    - target MCP server registered (verified via `claude mcp list`)
    - operator-facing summary of newly activable downstream skills
    - no orphan output, contextual next-step proposed
disambiguates_against:
  connect-source: "connect-source links an external platform (API/SDK) to PhantomOS as a runtime data source for skills (Layer 2). connect-mcp-server registers an MCP server at the Claude Code level (Layer 1), which then exposes tools to the session agent."
  onboard-brand: "onboard-brand builds a brand workspace inside PhantomOS. connect-mcp-server wires connectivity outside the brand layer."
---

# connect-mcp-server, orchestrator

> Guide opérateur PhantomOS dans la configuration des MCP servers (Layer 1 connectivité). Lit `.mcp.json.example` + invoque `claude mcp add` de façon interactive. Verify post-add via `claude mcp list`.

---

## Quand l'invoquer

| Trigger | Cas |
|---|---|
| Premier setup opérateur | Besoin Meta Ads, Calendar, Supabase pour skills downstream qui dépendent de MCP |
| Ajout MCP custom | Slack, Notion, ClickUp, Gmail, Excalidraw, ou serveur custom hébergé |
| Diagnostic "MCP non connecté" | Un skill consumer flag *"MCP X non disponible"*, l'opérateur veut comprendre où ça bloque |
| Audit connectivité | Opérateur demande *"qu'est-ce qui est branché ?"* au niveau MCP |

NE PAS confondre avec `connect-source` (Layer 2, APIs callable via skills sur credentials shippés). Voir `disambiguates_against` dans la frontmatter.

---

## Sources à lire (Step 0bis, DRGFP v2.38)

L1 (template) :
1. `.mcp.json.example` (template + descriptions des 4 MCP defaults)
2. `docs/system/connectivity-layering.md` (canon Layer 1/2/3)
3. `docs/system/operator-vocabulary-translation.md` (translation jargon → operator-facing)

L2 (operator runtime) :
4. `~/.claude/mcp/` (config locale opérateur si existe, sinon vide)
5. Output `claude mcp list` (état actuel des MCP enregistrés)
6. `credentials_shared.env` (disponibilité tokens pour env vars MCP)

L3 (gap-filling) : si `.mcp.json.example` absent ou `claude mcp` CLI introuvable, surface à l'opérateur (binary fallback : edit direct `~/.claude/mcp/{name}.json`).

---

## Hard rules

### HR1 · Operator gate target

**Première action.** AskUserQuestion avec 4 options :

```
Quel outil tu veux brancher ?

(a) Pack defaults PhantomOS · facebook-graph + youtube-transcript + supabase + google-calendar (recommandé bootstrap)
(b) Outils perso · gmail, slack, notion, clickup, excalidraw, autre du catalogue Anthropic
(c) URL custom · serveur MCP que tu héberges ou un fournisseur tiers
(d) Status only · juste afficher ce qui est branché actuellement
```

Pas de gate target → pas de `claude mcp add`. L'opérateur décide la cible avant tout exec.

### HR2 · Verify avant add

Avant tout `claude mcp add`, dans l'ordre :

1. Run `claude mcp list` ; parse output. Si target déjà présent, surface : *"`{name}` déjà branché. Skip ou re-configurer ?"* (AskUserQuestion binaire).
2. Verify credentials env requis selon target. Mapping :
   - facebook-graph → `FACEBOOK_ACCESS_TOKEN` (alias possible `META_ACCESS_TOKEN` dans credentials_shared.env)
   - supabase → `SUPABASE_URL` + `SUPABASE_ANON_KEY`
   - google-calendar → `GOOGLE_OAUTH_TOKEN`
   - youtube-transcript → aucun token
3. Si credentials manquants : pointer vers `credentials_shared.env`, AskUserQuestion : *"Token Meta absent. Tu drop le token maintenant (je l'écris dans credentials_shared.env) ou tu reviens après ?"*

### HR3 · Invoke `claude mcp add` correctement

Format canon Claude Code CLI :

```bash
claude mcp add {name} --command {cmd} --args {args} --env {KEY}={value}
```

Exemples concrets, à exécuter via Bash tool (subagent_safe: true sur cette skill) :

```bash
claude mcp add facebook-graph --command npx --args "@anthropic-ai/mcp-server-facebook-graph" --env FACEBOOK_ACCESS_TOKEN=$META_ACCESS_TOKEN
claude mcp add youtube-transcript --command npx --args "@anthropic-ai/mcp-server-youtube-transcript"
claude mcp add supabase --command npx --args "@supabase/mcp-server" --env SUPABASE_URL=$SUPABASE_URL --env SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY
claude mcp add google-calendar --command npx --args "@google/mcp-server-calendar" --env GOOGLE_OAUTH_TOKEN=$GOOGLE_OAUTH_TOKEN
```

**Note de robustesse.** La syntaxe `claude mcp add` peut varier selon la version installée. Si la commande retourne une erreur de flag inconnu :

1. Run `claude mcp add --help` ; parse les flags réels disponibles.
2. Adapter le call à la version (certains builds attendent `claude mcp add {name} --stdio-command "..."` au lieu de `--command + --args`).
3. Si le CLI bloque définitivement, fallback : edit direct `~/.claude/mcp/{name}.json` selon le pattern du `.mcp.json.example`. Surface fallback à l'opérateur (binary : *"CLI ne marche pas sur ta version. Je drop le JSON direct ?"*).

### HR4 · Post-add verification

Après chaque add, run `claude mcp list` pour confirmer présence. Puis test rapide selon target :

| MCP | Test ping |
|---|---|
| facebook-graph | Tenter `list-accounts` skill (lit Meta Graph) |
| supabase | Query simple read-only |
| google-calendar | Tenter list calendars |
| youtube-transcript | Skip (pas de test ping triviale) |

Si fail → diagnostic. Tokens invalides ou syntax MCP server foireuse ? Surface diagnostic binaire, pas de tunnel.

### HR5 · Operator-facing translation

Jargon interne → operator-facing. Cf `docs/system/operator-vocabulary-translation.md`.

| Interne | Opérateur |
|---|---|
| MCP server | outil branché, connexion |
| `claude mcp add` | OK montrer en code block (commande backend), avec phrase d'intro plain-language |
| `FACEBOOK_ACCESS_TOKEN` | token Meta |
| `stdio command` | backend technical, ne pas évoquer |
| Layer 1 / 2 / 3 | NEVER. Dire "branché au niveau Claude Code", "branché côté skill", "shippé d'office" |

NEVER exposer dans l'output : "MCP server", "stdio", "Layer 1", noms d'env vars en clair (dire "le token" ou "tes clés"), `disambiguates_against`, `isolation_scope`, etc.

---

## Steps

### Step 0bis · Prerequisite check (DRGFP)

L1 (template) : Read `.mcp.json.example` et `docs/system/connectivity-layering.md` (skim).
L2 (operator runtime) : Run `claude mcp list` pour état actuel.
L3 (gap-filling) : Read `credentials_shared.env` pour disponibilité tokens (alias `META_ACCESS_TOKEN` → `FACEBOOK_ACCESS_TOKEN`, etc.).

Sortie de Step 0bis : tableau interne {target candidate, déjà connecté ?, credentials prêts ?}. Pas opérateur-facing yet.

### Step 1 · Detection target

HR1, AskUserQuestion 4 options. Réponse → branche selon :

- (a) → loop sur les 4 defaults
- (b) → AskUserQuestion 2 : lequel ?
- (c) → AskUserQuestion 3 : nom serveur + command + args + env requis
- (d) → run `claude mcp list`, format opérateur-facing, fin (skip Steps 2-4)

### Step 2 · Verify préconditions

HR2. Pour chaque target sélectionné :
- Check `claude mcp list` (déjà présent ?)
- Check credentials env (token dispo ?)
- Surface gap binaire si manque

### Step 3 · Invoke add

HR3. Run `claude mcp add ...`. Capture stdout/stderr.

Si erreur de syntax : fallback `claude mcp add --help` → adapter → retry. Si toujours fail : fallback edit direct JSON.

### Step 4 · Verification + test

HR4. `claude mcp list` post-add + test ping si applicable.

### Step 5 · No orphan output

Output operator-facing structuré (format ci-dessous) + 1 contextual next-step.

Recommandation context-aware :
- Si facebook-graph fraîchement branché → *"lance audit-meta-account sur {brand} pour tester."*
- Si supabase branché → *"tape /phantom pour voir ton cockpit alimenté."*
- Si google-calendar branché → *"lance brief-daily demain matin, tu auras ton agenda dedans."*
- Si tous branchés et rien d'évident → *"tu es prêt côté connexions. La prochaine étape, c'est setup-brand ou onboard-brand."*

---

## Output format

```
═══════════════════════════════════════════════════
OUTILS BRANCHÉS · état actuel

  ✓ facebook-graph     prêt
  ✓ youtube-transcript prêt
  ⚠ supabase           tokens absents (URL et clé manquantes dans tes credentials)
  ○ google-calendar    pas configuré

ACTIONS APPLIQUÉES CE TURN
  → facebook-graph branché (token Meta lu depuis credentials_shared.env)
  → test ping OK (compte ads listé)

NEXT
  → tape : drop tes clés Supabase dans credentials_shared.env (URL + clé manquantes)
  → ou tape : lance audit-meta-account vitatone (Meta prêt)
═══════════════════════════════════════════════════
```

Statuts canon :
- `✓ prêt` : MCP enregistré + credentials présents + test ping OK
- `✓ branché` : MCP enregistré + credentials présents, test ping non applicable
- `⚠ tokens absents` : MCP enregistré mais credentials manquants (l'outil ne marchera pas tant que le token n'est pas drop)
- `○ pas configuré` : MCP non enregistré

---

## Cross-refs

- `docs/system/connectivity-layering.md` (canon 3 layers, source de vérité Layer 1 vs 2 vs 3)
- `.mcp.json.example` (template MCP defaults)
- `docs/system/operator-vocabulary-translation.md` (jargon translation HR5)
- `docs/system/dependency-resolution-protocol.md` (DRGFP Step 0bis L1/L2/L3)
- Skill `connect-source` (Layer 2 sibling, distinct routing)
- `credentials_shared.env` (workspace-level tokens)
