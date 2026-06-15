# Style Registry · index de la style-library

> SSOT-index des fiches-style (`registries/styles/{style_id}.json`, schema `style-recipe/1.0`). Backing du tag `genome_tags.primary_style_id` (enum 22, miroir A=B genome.schema <-> decomposition.schema). Jumeau de `creative-mechanics-registry.md` mais pour le STYLE VISUEL/VIDEO. CONSOMME par compose/recompose/adapt (render_recipe -> prompt) et par qc-creative (Axe 4 DA via da_compat). Unifie visuel+video (`model_params.video_params` pour les styles temporels). SSOT semantique du style_id (meme doctrine que creative-mechanics-registry pour mecanique_id) : l'enum style_id cote genome/decomposition/genome-package est un snapshot DERIVE de cet index (sync rebuild-index), pas l'inverse. Une fiche perf-validee (>=2 sources independantes) etend le vocabulaire.

**22 fiches · couverture enum 22/22.**

`typologie` : spatial (image) · temporel (video/motion natif) · variable (les deux). `zone DA` = creative_zone_fit [min,max] (0 ultra-propre brand-safe, 10 raw/agressif).


## real-photo

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `macro-photo-mouth-skin-etc` | Macro corps reel | spatial | 1-6 | Gros plan macro photorealiste sur une zone CORPORELLE humaine (bouche/levres, peau, ongl.. |
| `real-photo-lifestyle` | Photo lifestyle reelle | spatial | 2-7 | Photo reelle d'un humain en situation d'usage du produit, candid (pris sur le vif) pas p.. |
| `real-photo-macro-detail` | Macro détail réel | spatial | 0-6 | Gros plan macro photoréaliste sur la texture ou la matière du produit (grain, fibre, sur.. |
| `real-photo-testimonial-static` | Photo temoignage statique | spatial | 0-6 | Photo reelle d'une personne (client, utilisateur) associee a une citation/verbatim de te.. |

## packshot

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `pack-shot-brand-template` | Packshot gabarit marque | spatial | 0-5 | Gabarit packshot recurrent de marque: un layout fige et reutilisable (zones constantes p.. |
| `real-photo-product-studio` | Packshot studio produit | spatial | 0-5 | Packshot studio du produit isole sur fond uni, lumiere douce et controlee, rendu photogr.. |

## ugc

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `ugc-selfie-talking` | UGC selfie face cam | temporel | 4-9 | Une vraie personne tient son telephone a bout de bras et parle direct camera, comme un m.. |

## 3d-anatomy

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `3d-anatomy-realistic` | Anatomie 3D realiste | variable | 3-8 | Rendu 3D photorealiste d'un mecanisme corporel (digestion, articulation, follicule, vais.. |
| `3d-anatomy-stylized` | Anatomie 3D stylisee | variable | 3-8 | Rendu 3D d'une zone du corps (peau, follicule, articulation, intestin, dent) ou se joue .. |
| `3d-anatomy-xray` | Anatomie 3D rayons-X | variable | 1-6 | Rendu 3D anatomique en vue rayons-X : un corps ou un membre semi-transparent (peau trans.. |

## ai-generated

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `ai-generated-realistic-photo` | Photo IA hyperrealiste | variable | 3-8 | Image generee par IA qui vise le photoreel indistinguable d'une vraie prise de vue, mais.. |
| `ai-generated-stylized` | Rendu IA stylisé | variable | 5-10 | Rendu IA assumé et non-photo : esthétique surréelle, hyper-stylisée, volontairement impo.. |
| `claymation-3d-ai` | Claymation 3D IA | variable | 2-7 | Pâte à modeler 3D générée par IA : personnages et produits sculptés type claymation/stop.. |
| `illustrated-pov-cartoon` | Cartoon POV illustré | variable | 3-9 | Illustration cartoon dessinée à la main vue en point de vue subjectif (first-person POV).. |

## graphic-overlay

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `graphic-icons-overlay` | Overlay icones graphiques | spatial | 0-4 | Composition graphique d'icones/pictos lignes ou solides + courts labels texte poses sur .. |

## motion-graphic

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `brand-motion-graphic` | Motion graphic marque | temporel | 0-6 | Animation 2D de marque pilotee par la charte : typo cinetique, formes geometriques, icon.. |

## comparison

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `split-screen-comparison` | Split-screen comparatif | variable | 2-8 | Cadre divise en deux moities cote a cote (ou avant/apres) qui confronte deux etats: prob.. |

## screen-mockup

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `screen-recording-mockup` | Screen recording / mockup app | temporel | 3-9 | Capture d'ecran filmee ou mockup d'interface qui montre une UI en action: fil de message.. |

## diagram

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `diagram-medical-2d` | Schéma médical 2D | spatial | 0-5 | Diagramme médical 2D explicatif : illustration vectorielle plate qui montre un mécanisme.. |

## stop-motion

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `stop-motion-physical` | Stop-motion objets reels | temporel | 2-7 | De vrais objets physiques (le produit, son packaging, ses ingredients, des accessoires) .. |

## stock

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `stock-footage-broll` | B-roll stock (plans d'ambiance) | temporel | 0-5 | Plans d'ambiance generiques de banque d'images : mains qui versent, nature qui respire, .. |

## other

| style_id | nom | typologie | zone DA | description |
|---|---|---|---|---|
| `other` | Autre (echappatoire) | variable | 0-10 | Catch-all generique pour tout style visuel/video qui ne tombe dans aucun des 21 styles c.. |

## Promotion

Un `style_id` perf-valide monte `watch -> promote-ready` par la MEME doctrine que les hooks (>=2 sources independantes), via `library-pattern` `pattern_type: visual-style`. Statut courant porte dans chaque fiche `promotion.status`.

