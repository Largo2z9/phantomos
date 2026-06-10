# Creative storage convention (Phase 0 brique 3, D#481)

## Forme des dossiers
```
brands/{slug}/creatives/{batch}/{CRT-NN}/          <- nos propres creas
brands/{slug}/competitive-intel/{batch}/{RCV-NN}/  <- pubs concurrentes decortiquees
```
- {batch} = une session de prod, slug date-stampe (ex 2026-06-06-01 ; lowercase + chiffres + tirets).
  Groupe par run/date -> scale a 10k+ (des centaines de dossiers-batch de quelques dizaines chacun,
  navigable + git-friendly) au lieu d'un dossier plat de 10k. Couvre "par batch" ET "par date".
- {CRT-NN} = id de nos creas (CRT-[0-9]{2,4}). {RCV-NN} = id des concurrentes decortiquees (RCV-[0-9]{2,4}).
  DEUX namespaces separes, jamais de collision forward/reverse.
- Dans chaque {CRT-NN}/ : genome.json (l'ADN), creative.json (lignage/tracabilite),
  produced/ (binaires + sidecars json), brief.md.

## Allocation d'id (PAS d'allocateur central)
- Le prochain CRT-NN est reserve en CREANT son dossier (mkdir {CRT-NN}/).
- mkdir est atomique : reussit = l'id est a toi ; echoue (existe deja) = +1 et retry.
  Zero fichier-index central, zero verrou, zero chemin d'ecriture privilegie. Les trous d'id sont
  inoffensifs (les id doivent etre UNIQUES, pas sans-trou). Sur-safe meme en cas de concurrence reelle.
- L'id de stockage (CRT-NN) est SEPARE de la cle de join perf : le genome porte script_id (GSC-NN) et
  l'ad_id externe (facebook_/tiktok_/snapchat_/google_) pour la boucle perf (brique 5).

## Gate
- write-to-context.py ALLOWED_PATH_PATTERNS impose cette forme (briques 1+3).
- mutation-guard.py PROTECTED_GLOBS (brands/.+\\.json) couvre tout l'arbre -> chaque ecriture transite par le gate.

## PAS construit maintenant (anti over-engineering)
- Un catalogue/index de toutes les creas + un dashboard = utile SEULEMENT au volume (des milliers).
  Lit les memes donnees. A batir quand le volume le justifie, pas avant.
