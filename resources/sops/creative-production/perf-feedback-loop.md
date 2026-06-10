# Perf feedback loop — l'analyse fine (CHANTIER, TBD)

> Brique 5 a posé le RÉCEPTACLE (la plomberie). CE DOC = le marqueur du chantier d'INTELLIGENCE qui reste à construire. Le réceptacle landé n'est PAS le système qui apprend.

## POSÉ (brique 5, minimal)
- Clé de jointure : `creative.json#lineage.ad_id` (format `plateforme_NNN` : facebook_/tiktok_/snapchat_/google_).
- Réceptacle ouvert : `creative.json#performance` (additionalProperties — avale n'importe quelles métriques brutes de n'importe quelle plateforme, dans `performance.raw`).
- Branchement : `import-meta-results` pull la perf par `ad_id` → écrit dans `performance.raw`. Le signal « qu'est-ce qui a marché » est joignable via les `genome_tags` (mécanique/style/structure) déjà présents — on JOINT, on ne re-modélise pas.
- Résultat : la perf ATTERRIT + est JOIGNABLE + l'opérateur peut la VOIR. Le système n'APPREND PAS encore tout seul.

## RESTE à construire (l'analyse fine — analyse métier profonde)
1. **Sémantique par plateforme** — Meta/TikTok/Snapchat : métriques + seuils différents. Quelle métrique = quel signal (CTR, hold-rate, ROAS, CPA, thumb-stop, days_running). Normalisation cross-plateforme.
2. **Gagnant / perdant / « ça coupe »** — les seuils de décision, par rapport à quelle baseline (marque, batch, benchmark).
3. **Recalibrage régime explore/exploit** — comment la perf met à jour la jauge `perf_signal` (A3) → prochain régime + le curseur sectoriel.
4. **Promotion canon (3e signal)** — quel principe abstrait se promeut vers la banque de concepts quand N créas convergentes gagnent. La règle exacte.
5. **Attribution** — multi-touch, fenêtre, multi-plateforme. Sujet en soi.
6. **Dashboard** — couche au-dessus, lit le même réceptacle (vue opérateur).

## Principe directeur
Data-vs-logique : le réceptacle est GÉNÉRIQUE (la donnée), l'analyse est SPÉCIFIQUE (la logique, dans des skills/doctrines à écrire). Ne PAS figer l'ontologie des métriques dans le schéma.
