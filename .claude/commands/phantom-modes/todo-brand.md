## Mode todo-brand · `/phantom {brand} todo` (canon v2.87.5+ P1)

`/phantom {brand} todo` rend la liste des actions actives + dette workspace pour UNE brand spécifique (vs `/phantom todo` cross-brand workspace-level). Vue brand-level brand-todo proactif (P3 canon v2.87.5+ · maximiser contexte plateformes connectées + schedules actifs/manquants).

### Header breadcrumb

```
workspace > {brand} > todo
══════════════════════════════════════════════
{N} actions actives · {M} schedules · {K} connectors
```

### Sections canon · 4 blocs

**Actions** (top 5 max · priority_icon canon `⚠` `◐` `·`) ·
```
{priority_icon} [{brand_slug}] {action description}
   · `{paste-ready commande}` ({why})
```

**Connectors** (état actuel + suggestions priorisées ROI/effort) ·
```
✓ Paid · Meta connecté (last_sync {date})
○ Paid · TikTok non connecté · débloque audit cross-channel
✓ Analytics · GA4 connecté
○ Spy tools · TrendTrack non connecté · débloque competitive intel

Suggestions prioritaires (ranked ROI/effort) ·
1. Connecter Shopify (~10min · débloque AOV/LTV/cohorts)
2. Connecter TrendTrack (~5min · débloque competitive intel)
```

**Schedules** (canon v2.87.5+ P4 · état actuel + suggestions manquantes) ·
```
✓ mine-voc · refresh weekly · next run {date}
○ trendtrack-enrich-brand · suggestion weekly · débloque new winning ads detection
○ audit-creative-fatigue · suggestion monthly · spot fatigue avant CAC explose
```

**Atlas completeness** (état entités encodées + gaps détectés) ·
```
✓ Brand identity + positioning encodé
◐ Produits (1/6 enriched · 5 SKUs à drill)
◐ Audiences (3 hypothèses · 0 verbatim direct · récupère via mine-voc)
○ Angles dérivés · 0 (1066 ads observés · NEW /add angle pour démarrer)
○ Strategy.json · focus Q2 à poser
```

### Footer canon

```
─────
`/phantom {brand}` · vue cockpit complet
`/phantom todo` · vue cross-brand workspace
`/add audience {brand}` · ajouter audience proactif analytique
`/add angle {audience_slug}` · ajouter angle proactif analytique
`/phantom ?` pour les modes disponibles
```

### Triggers

- `/phantom {brand} todo`
- `/phantom todo {brand}` (alias)
- *"qu'est-ce qu'il reste à faire sur {brand}"* OR *"todo {brand}"* (natural language route)

### Garde-fous canon

- Iconographie canon OCD strict · `✓ ◐ ○ ✗ ⚠` · pas de légende au pied (canon v2.87.4.1 LITE /update · iconographie matricielle réservée slash commands · /phantom est matriciel donc OK)
- Voice-doctrine v2.84.1 · 0 em-dash · 0 banned terms · prose française naturelle
- 0 path technique exposé opérateur runtime · 0 jargon doctrine (EDD · OCD · DVD)
- Pattern proactif canon v2.87.5+ · `connectors checkup + schedules manquants + atlas gaps` surfacés ensemble (vs todo plat actions seules)
- Cross-ref `brand_connectors_onboarding_canon` memory · matrice 7 catégories + 7 skills schedulables + template canon

### Cross-refs canon

- `.claude/commands/phantom.md` · mode parent `/phantom todo` cross-brand workspace-level
- `brands/{slug}/status.json#connectors_state` · état connectors brand-level
- `brands/{slug}/scheduled.json` · schedules actifs brand-level (canon v2.87.5+ P4)
- `brands/{slug}/todos.md` · todos opérationnels brand-level
- Memory canon `brand_connectors_onboarding_canon` · pattern proactif référence
