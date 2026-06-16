#!/usr/bin/env python3
"""
seed-canon-copy · one-shot seeder for resources/canon/copy/{layer}/{tool}.json.

Writes the v1 canon copy atlas: 11 layers, ~70 tools. Idempotent: skips files
that already exist (use --force to overwrite). Run once after v2.26.0.

Usage:
    python3 .skills/seed-canon-copy.py [--force] [--dry-run]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(10):
        if (cur / ".skills").is_dir() and (cur / "brands").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


CANON: dict = {
    "frameworks": [
        {
            "id": "aida",
            "name": "AIDA",
            "principle": "Squelette de message en 4 mouvements : Attention, Intérêt, Désir, Action. Le plus ancien framework DR, base universelle.",
            "structure": "Attention (capter) → Intérêt (qualifier) → Désir (projeter le résultat) → Action (CTA).",
            "gabarits": [
                "[hook] [contexte audience] [proof + bénéfice] [CTA + offre]",
                "Tu sais quoi de [X] / Voilà ce que j'ai testé / Résultat / Voilà comment faire pareil"
            ],
            "when_works": ["audiences solution-aware ou product-aware", "format court à moyen (ad, email, landing courte)", "trafic chaud à tiède"],
            "when_avoid": ["unaware (pas de manque cognitif à combler)", "long-form complexe où PAS ou QUEST sont plus adaptés"],
            "combines_with": {"hooks": ["question-callout", "stat-choc", "avant-apres"], "angles": ["mecanisme-unique", "identite"], "formats": ["ad-statique", "email-sequence", "landing"]},
            "anti_patterns": ["sauter le D (désir) → on tombe dans 'feature dump puis CTA'", "A et I confondus en une seule phrase"],
            "examples": [
                "Marre de la chute saisonnière ? J'ai testé 14 produits, un seul a marché : la cure 3 mois Hair Boost. Voici le résultat à 8 semaines.",
                "[Attention] Tu perds 100 cheveux par jour. [Intérêt] Normal sauf si... [Désir] Voilà à quoi ressemble une cure réussie. [Action] Commence aujourd'hui."
            ],
            "lineage": {"source": "public-doctrine", "references": ["E. St. Elmo Lewis 1898", "Halbert"]}
        },
        {
            "id": "pas",
            "name": "PAS",
            "principle": "Problem · Agitate · Solve. Frame de copy émotionnel : on identifie une douleur, on l'amplifie en la rendant tangible, puis on offre la résolution.",
            "structure": "Problem (nommer) → Agitate (amplifier les conséquences) → Solve (la solution).",
            "gabarits": [
                "Tu vis [problème] ? / Voilà ce que ça te coûte vraiment / Voilà comment on règle ça",
                "Le truc avec [problème] / [conséquences ignorées] / [solution]"
            ],
            "when_works": ["audiences problem-aware ou solution-aware avec pain émotionnel fort", "trafic froid à tiède", "formats moyens à longs"],
            "when_avoid": ["audiences most-aware (déjà convaincu, agitate les ennuie)", "marchés à sophistication 5+ (dramatisation perçue comme manipulation)"],
            "combines_with": {"hooks": ["confession", "question-callout", "stat-choc"], "angles": ["ennemi-commun", "retour-en-arriere"], "emotions": ["frustration", "peur", "culpabilite", "espoir"]},
            "anti_patterns": ["over-agitate sans solve crédible (manipulation perçue)", "agitate sur un pain non-réel pour l'audience (faux pain)"],
            "examples": [
                "Tes cheveux tombent depuis l'accouchement. Tu te dis que ça va passer. 6 mois après c'est pire, et la repousse n'est pas là. Voilà ce qu'il fallait commencer dès la 6e semaine.",
                "[P] La chute post-partum. [A] Si tu attends 3 mois sans rien faire, la perte de densité devient permanente. [S] Cure ciblée biotine + B6 + zinc démarrée tôt."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Halbert", "Sugarman"]}
        },
        {
            "id": "bab",
            "name": "BAB",
            "principle": "Before · After · Bridge. Frame visuel court : on peint l'avant, on peint l'après, on montre le pont entre les deux.",
            "structure": "Before (réalité actuelle) → After (réalité visée) → Bridge (le mécanisme qui fait passer).",
            "gabarits": [
                "Avant / Après / Comment",
                "Voilà où tu en es / Voilà où tu peux être / Voilà ce qui fait la bascule"
            ],
            "when_works": ["formats courts (UGC, ad statique, hero LP)", "audiences qui voient un résultat tangible (visuel, mesurable)", "produits avec transformation visible"],
            "when_avoid": ["produits sans before/after clair (catégorie commodity)", "audiences sceptiques sur la promesse de transformation"],
            "combines_with": {"hooks": ["avant-apres", "transformation"], "angles": ["mecanisme-unique", "status-shift"], "formats": ["UGC-ad", "ad-statique", "testimonial"]},
            "anti_patterns": ["After irréaliste (perd la crédibilité)", "Bridge flou (pas de mécanisme nommé, juste 'ce produit')"],
            "examples": [
                "Cheveux fins, plats, casse à la racine / Cheveux denses, brillants, +6 cm / 90 jours de cure ciblée biotine + zinc.",
                "Avant : 100 cheveux par brossage. Après : 10. Bridge : le complexe Cellule Boost agit sur la phase anagène."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Direct Response canon"]}
        },
        {
            "id": "quest",
            "name": "QUEST",
            "principle": "Qualify · Understand · Educate · Stimulate · Transition. Frame long-form pour pages de vente, VSL, advertorials. Plus pédagogique que PAS.",
            "structure": "Qualify (filtre l'audience) → Understand (montre que tu comprends leur situation) → Educate (donne du contexte qu'ils n'avaient pas) → Stimulate (active le désir) → Transition (passe à l'offre).",
            "gabarits": [
                "Si tu es [profil], cette lettre te concerne / Voilà la situation / Ce que personne ne te dit / Voilà ce que ça change / Voilà l'offre",
                "[Qualify] Tu fais partie de [profil] ? [Understand] [paraphrase de leur réalité]. [Educate] Ce que la plupart ignorent. [Stimulate] [bénéfice projeté]. [Transition] [offre + CTA]."
            ],
            "when_works": ["VSL, sales letter, advertorial long", "audiences problem-aware sophistication 3+", "produits avec mécanisme à expliquer"],
            "when_avoid": ["formats courts (perd son intérêt sous 600 mots)", "trafic ultra-conscient (court-circuite la phase Educate)"],
            "combines_with": {"hooks": ["curiosity-gap", "contrarian"], "angles": ["mecanisme-unique", "contre-intuitif"], "leads": ["mechanism-led", "story-led"], "formats": ["VSL", "landing", "email-sequence"]},
            "anti_patterns": ["sauter Understand (l'audience se sent pas comprise)", "Educate qui devient encyclopédie (perd le rythme)"],
            "examples": [
                "Si tu as plus de 35 ans et que ton cheveu s'affine / Voilà la séquence biologique / Ce que la plupart ignorent sur la phase télogène / Voilà comment on inverse / Cure 6 mois.",
                "VSL Karacare : Qualify (femmes 28-50 chute) → Understand (post-grossesse, stress, hormonal) → Educate (3 phases du cycle pilaire) → Stimulate (densité retrouvée) → Transition (cure + bonus)."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Michael Fortin", "Direct Response"]}
        },
        {
            "id": "fab",
            "name": "FAB",
            "principle": "Features · Advantages · Benefits. Frame d'argumentation produit. Convertit chaque feature en avantage puis en bénéfice émotionnel.",
            "structure": "Feature (caractéristique) → Advantage (ce que ça permet techniquement) → Benefit (ce que ça change pour le lecteur).",
            "gabarits": [
                "Feature [X] / qui te permet [Y] / pour que tu [Z]",
                "[caractéristique] · [implication technique] · [résultat dans la vie]"
            ],
            "when_works": ["sections produit de landing", "fiches produit", "comparaisons", "audiences product-aware"],
            "when_avoid": ["copy émotionnel pur (FAB est rationnel)", "audiences problem-aware (besoin de pain reconnu d'abord)"],
            "combines_with": {"frameworks": ["aida", "quest"], "leads": ["mechanism-led", "proof-led"], "formats": ["landing", "email-sequence"]},
            "anti_patterns": ["F sans B (feature dump)", "B sans F (promesse vague non ancrée)"],
            "examples": [
                "Biotine 8000mcg [F] / dosage thérapeutique vs cosmétique [A] / phase anagène prolongée, repousse visible 8-12 sem [B]",
                "Format gummy [F] / pas de pilule à avaler [A] / tu prends ta cure même les jours de rush [B]"
            ],
            "lineage": {"source": "public-doctrine", "references": ["Sales canon"]}
        },
        {
            "id": "4ps",
            "name": "4Ps",
            "principle": "Picture · Promise · Prove · Push. Frame visuel orienté action, plus émotionnel que AIDA. Halbert / Carlton style.",
            "structure": "Picture (peindre la scène) → Promise (la transformation) → Prove (preuves) → Push (CTA urgent).",
            "gabarits": [
                "Imagine / Voilà ce qu'on te promet / Voilà comment on prouve / Voilà ce que tu fais maintenant",
                "[scène vivante] / [bénéfice ultime] / [proof concret] / [CTA + urgence]"
            ],
            "when_works": ["ads émotionnels", "long-form persuasif", "produits transformation visible"],
            "when_avoid": ["B2B technique", "audiences sceptiques sur la promesse"],
            "combines_with": {"hooks": ["avant-apres", "transformation", "social-proof-front"], "angles": ["status-shift", "identite"], "emotions": ["espoir", "envie"]},
            "anti_patterns": ["Picture sans Promise (joli mais sans direction)", "Push sans Prove (pression sans crédibilité)"],
            "examples": [
                "[P] Tu sors de la douche, t'as une serviette pleine de cheveux. [P] D'ici 12 semaines, plus aucun. [P] 60k clientes, ROAS 4x sur Trustpilot. [P] Cure 3 mois -10% jusqu'à dimanche."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Halbert", "Carlton"]}
        }
    ],

    "hooks": [
        {
            "id": "curiosity-gap",
            "name": "Curiosity gap",
            "principle": "Crée un écart entre ce que le lecteur sait et ce qu'il devrait savoir. La curiosité tire vers la résolution.",
            "structure": "Affirmation non-évidente → promesse d'explication différée.",
            "gabarits": [
                "La vraie raison pour laquelle [X] n'est pas [Y]",
                "Ce que [autorité] ne dit pas sur [X]",
                "Pourquoi [résultat attendu] échoue malgré [effort logique]"
            ],
            "when_works": ["stade conscience problem-aware ou solution-aware", "sophistication marché 3+ (claims simples saturés)", "trafic froid à tiède"],
            "when_avoid": ["audience unaware (pas de manque cognitif → curiosité non déclenchée)", "sophistication 1-2 (claim direct suffit)", "trafic ultra-conscient (perçu clickbait)"],
            "combines_with": {"angles": ["contre-intuitif", "mecanisme-unique"], "frameworks": ["pas", "quest"], "emotions": ["mefiance-eveillee", "frustration"], "formats": ["VSL", "landing", "ad-statique"]},
            "anti_patterns": ["Cliffhanger sans payoff (frustration, churn)", "Curiosité gratuite (déconnectée du pain réel)"],
            "examples": [
                "Pourquoi ta routine cheveux empire la chute (et personne te le dit)",
                "Ce que les dermatos prescrivent pour la pousse, mais pas en parapharmacie"
            ],
            "lineage": {"source": "public-doctrine", "references": ["George Loewenstein 1994", "Sugarman"]}
        },
        {
            "id": "contrarian",
            "name": "Contrarian",
            "principle": "Prend le contre-pied d'une croyance dominante de l'audience. Crée du choc cognitif et positionne l'auteur comme insider.",
            "structure": "Affirmation qui contredit le consensus → annonce d'une vérité cachée.",
            "gabarits": [
                "Arrête de [X], c'est ce qui empire [Y]",
                "Tout le monde te dit [X]. C'est faux.",
                "[Pratique populaire] = la pire chose pour [résultat]"
            ],
            "when_works": ["sophistication marché 4+ (audience saturée des claims)", "audiences problem-aware fatiguées des solutions classiques", "positionnement de marque insider/authorité"],
            "when_avoid": ["audiences fragiles ou sceptiques (le choc devient agression)", "sophistication 1-2 (consensus pas encore formé, contrarian sans cible)"],
            "combines_with": {"angles": ["contre-intuitif", "ennemi-commun"], "frameworks": ["pas", "quest"], "emotions": ["surprise", "indignation", "soulagement"], "formats": ["VSL", "ad-statique", "advertorial"]},
            "anti_patterns": ["Contre-pied gratuit non étayé (perd la crédibilité)", "Trop violent (choc devient repoussoir)"],
            "examples": [
                "Arrête la biotine. C'est ce qui sature ton foie sans rien donner à tes cheveux.",
                "Le shampoing à la kératine ? La pire chose pour la chute hormonale."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Halbert", "Schwartz Breakthrough Advertising"]}
        },
        {
            "id": "stat-choc",
            "name": "Stat choc",
            "principle": "Ouvre sur une statistique surprenante qui valide implicitement le pain. Fait office de proof immédiat tout en accrochant.",
            "structure": "Chiffre marquant + cible spécifique + implication.",
            "gabarits": [
                "[X]% des [profil] ne savent pas que [vérité]",
                "[chiffre] [contexte] / et seulement [autre chiffre] [outcome]"
            ],
            "when_works": ["trafic froid", "audience problem-aware avec besoin de validation externe", "marchés à sophistication moyenne où le pain n'est pas encore évident"],
            "when_avoid": ["audiences saturées de stats (B2B SaaS)", "produits où le chiffre paraît fabriqué"],
            "combines_with": {"angles": ["ennemi-commun", "contre-intuitif"], "frameworks": ["pas"], "emotions": ["peur", "surprise"], "formats": ["ad-statique", "landing", "email-sequence"]},
            "anti_patterns": ["Chiffre sans source (perd crédibilité)", "Stat triviale (everybody knows)"],
            "examples": [
                "73% des femmes post-grossesse ressentent une chute aiguë entre le 3e et le 6e mois. La plupart pensent que c'est passager. Pour 22%, ça ne passe pas seul.",
                "100 cheveux perdus par jour, c'est normal. 200, c'est le signal que ton cycle pilaire dérape."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Direct Response"]}
        },
        {
            "id": "avant-apres",
            "name": "Avant-après",
            "principle": "Ouvre sur le contraste visuel ou narratif entre l'état initial et l'état cible. Hook visuel puissant pour produits transformation.",
            "structure": "État présent (avant) ↔ état projeté (après). Idéalement visuel.",
            "gabarits": [
                "[Avant le produit] / [après le produit]",
                "Il y a [X mois] / aujourd'hui"
            ],
            "when_works": ["UGC, ad statique, vidéo testimonial", "produits avec transformation tangible (skincare, hair, fitness)", "audiences solution-aware ou product-aware"],
            "when_avoid": ["audiences unaware (pas de référent avant)", "produits sans transformation visible"],
            "combines_with": {"frameworks": ["bab", "4ps"], "angles": ["mecanisme-unique", "status-shift"], "emotions": ["espoir", "envie"], "formats": ["UGC-ad", "ad-statique", "testimonial"]},
            "anti_patterns": ["Après photoshopé (perte de crédibilité instantanée)", "Avant trop dramatique (perçu manipulé)"],
            "examples": [
                "Octobre : 50% du volume habituel. Janvier : tout est revenu, plus dense que jamais. 90 jours de cure.",
                "Avant : casse à chaque brossage. Après : aucune."
            ],
            "lineage": {"source": "public-doctrine", "references": ["DR canon", "UGC playbook"]}
        },
        {
            "id": "question-callout",
            "name": "Question callout",
            "principle": "Pose une question qui qualifie l'audience cible et active la reconnaissance. 'C'est moi.'",
            "structure": "Question fermée qui touche un détail spécifique du pain.",
            "gabarits": [
                "Tu te reconnais si [détail spécifique] ?",
                "[Profil] qui [comportement spécifique] ?",
                "Tu [comportement étrange] aussi ?"
            ],
            "when_works": ["audiences segmentées finement", "trafic froid pour qualifier", "ouvertures d'UGC, hooks de vidéo courte"],
            "when_avoid": ["questions trop génériques ('tu veux des beaux cheveux ?')", "audiences déjà convaincu (qualification redondante)"],
            "combines_with": {"frameworks": ["aida", "pas"], "angles": ["identite", "retour-en-arriere"], "emotions": ["reconnaissance", "soulagement"], "formats": ["UGC-ad", "ad-statique"]},
            "anti_patterns": ["Question fermée à laquelle personne ne dit oui", "Question qui ressemble à un quiz markéto"],
            "examples": [
                "Tu te brosses les cheveux et t'as peur de regarder la brosse ?",
                "Mamans 6 mois post-partum : la chute t'a pris par surprise ?"
            ],
            "lineage": {"source": "public-doctrine", "references": ["Direct Response"]}
        },
        {
            "id": "confession",
            "name": "Confession",
            "principle": "Ouvre sur un aveu personnel qui crée connexion et proof simultanément. Bypass des défenses publicitaires.",
            "structure": "Aveu vulnérable de l'auteur ou narrateur → bascule vers le produit/solution.",
            "gabarits": [
                "J'ai longtemps cru que [croyance fausse]. Voilà ce qui m'a fait changer.",
                "Pendant [durée] j'ai [comportement gênant]. Aujourd'hui [résultat]."
            ],
            "when_works": ["UGC créatrices, founder story, témoignages", "marchés à sophistication 4+ saturés des claims commerciaux", "audiences sceptiques"],
            "when_avoid": ["B2B (registre trop personnel)", "marques sans visage humain identifiable"],
            "combines_with": {"frameworks": ["bab", "pas"], "angles": ["retour-en-arriere", "identite"], "emotions": ["culpabilite", "espoir", "complicite"], "formats": ["UGC-ad", "founder-story", "testimonial"]},
            "anti_patterns": ["Confession trop polie (perçue comme scriptée)", "Confession sans bascule (juste un drama)"],
            "examples": [
                "J'ai dépensé 800€ en shampoings prétendument anti-chute en 2 ans. Aucun n'a marché. Voilà ce qui a changé.",
                "Pendant 6 mois post-bébé, j'ai caché ma chevelure sous des bonnets. J'avais honte."
            ],
            "lineage": {"source": "public-doctrine", "references": ["UGC playbook", "Founder story canon"]}
        }
    ],

    "angles": [
        {
            "id": "mecanisme-unique",
            "name": "Mécanisme unique",
            "principle": "Met en avant le 'pourquoi-ça-marche' que personne d'autre ne dit. Différencie en sortant du registre 'meilleurs ingrédients'.",
            "structure": "Identifier le mécanisme physiologique/psychologique réel → l'expliquer simplement → montrer comment le produit l'active.",
            "gabarits": [
                "[Produit] active [mécanisme] que [concurrents] ignorent",
                "La vraie raison pour laquelle [résultat] : [mécanisme]. Voici comment on l'active."
            ],
            "when_works": ["sophistication marché 3-5", "audience product-aware ou most-aware", "produits avec un actif différenciant réel"],
            "when_avoid": ["sophistication 1-2 (pas besoin)", "produits sans différenciation mécanique réelle"],
            "combines_with": {"frameworks": ["quest", "fab"], "hooks": ["curiosity-gap", "contrarian"], "leads": ["mechanism-led"], "formats": ["VSL", "landing", "advertorial"]},
            "anti_patterns": ["Mécanisme inventé qui ne tient pas à la lecture critique", "Mécanisme trop technique (perd l'audience)"],
            "examples": [
                "Cellule Boost agit sur la phase anagène, pas sur le cuir chevelu. C'est pour ça que la repousse est durable.",
                "La biotine seule ne suffit pas. Il faut le complexe B6+zinc pour que la kératine se forme."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Schwartz Breakthrough Advertising"]}
        },
        {
            "id": "identite",
            "name": "Identité",
            "principle": "Cible un profil identitaire spécifique : 'pour les femmes qui...'. L'audience se reconnaît, l'achat devient affirmation de soi.",
            "structure": "Phrase qualifiante précise + bénéfice qui matche cette identité.",
            "gabarits": [
                "Pour les [profil] qui [comportement/situation]",
                "Si tu fais partie des [N%] qui [trait spécifique]"
            ],
            "when_works": ["niches identitaires (mamans, sportifs, intellectuels, femmes voilées, etc.)", "audiences à fort signal communautaire", "trafic tiède à chaud"],
            "when_avoid": ["audiences mass-market sans identité spécifique partagée", "marchés où segmentation identitaire vexe"],
            "combines_with": {"frameworks": ["aida", "quest"], "hooks": ["question-callout", "confession"], "emotions": ["appartenance", "fierte"], "formats": ["UGC-ad", "ad-statique", "email-sequence"]},
            "anti_patterns": ["Identité trop large (perd la spécificité)", "Identité forcée (l'audience ne se reconnaît pas)"],
            "examples": [
                "Pour les mamans qui ont vu leurs cheveux changer après bébé.",
                "Pour les femmes voilées qui sentent leur cuir chevelu fragilisé."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Schwartz", "DR canon"]}
        },
        {
            "id": "retour-en-arriere",
            "name": "Retour en arrière",
            "principle": "L'auteur partage ce qu'il aurait aimé savoir avant. Crée empathie avec l'audience qui vit cette phase actuellement.",
            "structure": "'J'aurais aimé savoir [X] à [moment de vie]' → enseigner X.",
            "gabarits": [
                "J'aurais aimé qu'on me dise [X] quand [moment]",
                "Si je devais reprendre [phase] aujourd'hui, voilà ce que je ferais."
            ],
            "when_works": ["UGC, créatrices, founder story", "audiences en début de phase (post-grossesse, transition de vie)"],
            "when_avoid": ["audiences déjà sorties de la phase (registre passé non pertinent)", "marques sans figure humaine"],
            "combines_with": {"hooks": ["confession"], "frameworks": ["pas", "bab"], "emotions": ["regret", "soulagement", "espoir"], "formats": ["UGC-ad", "founder-story", "email-sequence"]},
            "anti_patterns": ["Pseudo-regret (perçu scripté)", "Regret sans enseignement actionnable"],
            "examples": [
                "J'aurais aimé qu'on me dise, à 3 mois post-partum, qu'attendre n'allait rien arranger.",
                "Si je reprenais ma cure, je commencerais 6 semaines plus tôt."
            ],
            "lineage": {"source": "public-doctrine", "references": ["UGC playbook"]}
        },
        {
            "id": "ennemi-commun",
            "name": "Ennemi commun",
            "principle": "Désigne un coupable extérieur (industrie, mythe, pratique) que l'audience peut détester ensemble. Lien tribal.",
            "structure": "Nommer l'ennemi → montrer son méfait → positionner le produit comme alternative ou résistance.",
            "gabarits": [
                "L'industrie [X] te fait croire [mensonge]",
                "Le vrai problème, ce n'est pas toi. C'est [système]."
            ],
            "when_works": ["audiences avec frustration accumulée envers une catégorie", "sophistication marché 3+", "marques challengers"],
            "when_avoid": ["marques leaders (l'ennemi commun renvoie à elles)", "audiences peu engagées émotionnellement sur le sujet"],
            "combines_with": {"hooks": ["contrarian", "stat-choc"], "frameworks": ["pas", "quest"], "emotions": ["indignation", "soulagement"], "angles": ["contre-intuitif"], "formats": ["VSL", "advertorial"]},
            "anti_patterns": ["Ennemi caricaturé (perd la crédibilité)", "Ennemi sans alternative crédible (juste plainte)"],
            "examples": [
                "L'industrie capillaire vend des shampoings 'anti-chute' qui ne traitent que le cheveu. Le problème est interne.",
                "On t'a dit 'mange bien, ça repousse'. Mensonge. La carence est métabolique, pas alimentaire."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Schwartz", "Halbert"]}
        },
        {
            "id": "status-shift",
            "name": "Status shift",
            "principle": "Met en avant le changement de statut social ou de perception après transformation. Vise l'identité projetée.",
            "structure": "Avant (statut perçu) → après (statut projeté) → produit comme catalyseur.",
            "gabarits": [
                "Avant on me disait [X]. Maintenant on me demande [Y].",
                "[Trait extérieur] change tout : on te traite comme [statut nouveau]."
            ],
            "when_works": ["audiences en quête de validation extérieure", "produits beauté, fitness, mode", "trafic chaud"],
            "when_avoid": ["audiences à valeurs internes fortes (rejettent la quête de statut)", "marques à positionnement humble"],
            "combines_with": {"frameworks": ["bab", "4ps"], "hooks": ["avant-apres"], "emotions": ["fierte", "envie"], "formats": ["UGC-ad", "testimonial", "ad-statique"]},
            "anti_patterns": ["Status shift superficiel (cheap)", "Trop centré sur le regard des autres (clivant)"],
            "examples": [
                "Mes collègues me demandent quel coiffeur je vois. Je leur dis : aucun, juste 90 jours de cure.",
                "Avant j'attachais. Maintenant je laisse libre."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Status pyramid canon"]}
        },
        {
            "id": "contre-intuitif",
            "name": "Contre-intuitif",
            "principle": "Affirme l'inverse de ce que l'audience pense vrai. Crée un puzzle cognitif qui force la lecture.",
            "structure": "Affirmation qui paraît fausse → démonstration de pourquoi c'est vrai.",
            "gabarits": [
                "[Pratique attendue] empire [résultat], voilà pourquoi",
                "Pour [résultat], il faut faire l'inverse de [croyance commune]"
            ],
            "when_works": ["sophistication 4+", "audiences saturées", "long-form où on a la place d'expliquer"],
            "when_avoid": ["formats courts (pas le temps de démontrer)", "audiences peu patientes (l'inversion devient juste paradoxe)"],
            "combines_with": {"hooks": ["curiosity-gap", "contrarian"], "frameworks": ["quest", "pas"], "leads": ["mechanism-led"], "formats": ["VSL", "advertorial", "long-form-email"]},
            "anti_patterns": ["Contre-intuition non démontrée (juste prétention)", "Contre-intuition triviale (everybody knows the inverse already)"],
            "examples": [
                "Plus tu shampouines, plus tu accélères la chute.",
                "Pour faire pousser, il faut couper ? Faux et vrai en même temps. Voilà la vérité."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Schwartz", "Sugarman"]}
        }
    ],

    "heuristiques-persuasion": [
        {
            "id": "reciprocite",
            "name": "Réciprocité",
            "principle": "L'humain rend ce qu'on lui donne. Donner d'abord (valeur, info, échantillon) crée une dette psychologique vers l'achat.",
            "structure": "Don gratuit substantiel → demande proportionnée plus tard.",
            "gabarits": [
                "[ressource gratuite] / [appel à l'action proportionné]"
            ],
            "when_works": ["funnels lead-magnet", "email nurture", "trafic froid à éduquer"],
            "when_avoid": ["produits impulse buying", "audiences habituées au gratuit générique (saturé)"],
            "combines_with": {"formats": ["lead-magnet", "email-sequence", "VSL"], "leads": ["proof-led"]},
            "anti_patterns": ["Don superficiel (perçu comme bait)", "Demande disproportionnée après le don"],
            "examples": [
                "Guide PDF '7 erreurs en cure capillaire' → email day 7 cure 3 mois -10%",
                "Diagnostic gratuit personnalisé → recommandation cure ciblée"
            ],
            "lineage": {"source": "public-doctrine", "references": ["Cialdini Influence"]}
        },
        {
            "id": "engagement-coherence",
            "name": "Engagement-cohérence",
            "principle": "Une fois engagé sur petit, on se sent obligé de rester cohérent. Petit oui → grand oui.",
            "structure": "Demande petite (clic, quiz, micro-commitment) → demande engageante (achat).",
            "gabarits": [
                "Quiz 30 sec → recommandation personnalisée → cure adaptée"
            ],
            "when_works": ["quiz funnels", "diagnostic personnalisé", "trafic froid à qualifier"],
            "when_avoid": ["audiences pressées", "marchés ultra-sophistiqués (quiz perçu obvious)"],
            "combines_with": {"formats": ["quiz", "VSL", "landing"], "leads": ["problem-led"]},
            "anti_patterns": ["Quiz qui force des oui artificiels", "Engagement sans pertinence vers l'achat"],
            "examples": [
                "Diagnostic en 5 questions → 'voilà la cure pour ton profil' → checkout pré-rempli."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Cialdini Influence", "Freedman & Fraser 1966"]}
        },
        {
            "id": "preuve-sociale",
            "name": "Preuve sociale",
            "principle": "On suit ce que d'autres similaires à nous font. Plus le 'similaire' est précis, plus la preuve est puissante.",
            "structure": "Témoignages, reviews, compteurs, mentions presse → idéalement segmentés par profil.",
            "gabarits": [
                "[N] [audience cible] ont déjà [action]",
                "[Témoignage profil similaire au lecteur]"
            ],
            "when_works": ["audiences sceptiques", "marchés saturés où la preuve fait la différence", "trafic froid à tiède"],
            "when_avoid": ["produits ultra-niches (pas assez de preuves)", "audiences qui rejettent le mainstream"],
            "combines_with": {"hooks": ["social-proof-front"], "formats": ["testimonial", "landing", "ad-statique"]},
            "anti_patterns": ["Témoignages génériques sans visage", "Compteurs ronds (60.000 perçu fabriqué vs 62.483)"],
            "examples": [
                "63.247 mamans post-partum ont retrouvé leur densité avec la cure 3 mois.",
                "Avis Trustpilot de Sarah, 32 ans, 4 mois post-partum : ..."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Cialdini Influence"]}
        },
        {
            "id": "autorite",
            "name": "Autorité",
            "principle": "On suit les experts perçus. Médecins, scientifiques, célébrités, données mesurées sont des marqueurs d'autorité.",
            "structure": "Mention crédible + ancrage de l'expertise (titre, étude, source).",
            "gabarits": [
                "[Expert/source] confirme que [claim]",
                "Étude [source] : [résultat mesuré]"
            ],
            "when_works": ["catégories santé/beauté/nutrition", "audiences product-aware sceptiques", "marchés à régulation forte"],
            "when_avoid": ["audiences anti-establishment", "claims non vérifiables (risque légal + crédibilité)"],
            "combines_with": {"frameworks": ["quest", "fab"], "leads": ["proof-led"], "formats": ["VSL", "landing", "advertorial"]},
            "anti_patterns": ["Expert anonyme ou inventé", "Étude tirée hors contexte"],
            "examples": [
                "Dr Cohen, dermatologue : 'la cure 3 mois est le minimum pour observer un cycle pilaire complet.'",
                "Étude clinique Karacare 2024 : +37% de densité observée à 12 semaines."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Cialdini Influence", "Milgram"]}
        },
        {
            "id": "rarete",
            "name": "Rareté",
            "principle": "Ce qui est limité (temps, stock, accès) prend de la valeur. Le FOMO active l'action.",
            "structure": "Annonce de la limite + deadline crédible.",
            "gabarits": [
                "Plus que [X] [unités] / Offre se termine [date]",
                "[N] places / [date limite]"
            ],
            "when_works": ["closing de funnel", "fin de séquence email", "promotions saisonnières crédibles"],
            "when_avoid": ["urgences fabriquées (cliquables countdown timer reset)", "audiences sceptiques au marketing de rareté"],
            "combines_with": {"frameworks": ["aida", "4ps"], "formats": ["ad-statique", "email-sequence", "landing"]},
            "anti_patterns": ["Rareté permanente (toujours 'last chance')", "Stock fictif (illegal selon juridiction)"],
            "examples": [
                "Cure 6 mois en stock limité après rupture mai (production en cours).",
                "Offre Mother's Day fin dimanche 18h."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Cialdini Influence"]}
        },
        {
            "id": "sympathie",
            "name": "Sympathie",
            "principle": "On dit oui aux gens qu'on aime. Affinité, attractivité, similarité, compliments, coopération.",
            "structure": "Construire une relation perçue (founder visible, ton humain, valeurs partagées) avant l'ask.",
            "gabarits": [
                "[Founder story relatable] / [valeurs explicites] / [puis offre]"
            ],
            "when_works": ["DTC à fondatrice visible", "marques communautaires", "audiences valeurs-driven"],
            "when_avoid": ["B2B technique", "marques sans visage humain"],
            "combines_with": {"hooks": ["confession"], "angles": ["identite", "retour-en-arriere"], "formats": ["founder-story", "UGC-ad"]},
            "anti_patterns": ["Founder story générique (aucune vraie connexion)", "Sympathie forcée (paraît marketing)"],
            "examples": [
                "Jeanne, fondatrice : 'J'ai créé Karacare après ma 2e grossesse parce que rien ne marchait sur ma chute.'"
            ],
            "lineage": {"source": "public-doctrine", "references": ["Cialdini Influence"]}
        },
        {
            "id": "unite-tribale",
            "name": "Unité tribale",
            "principle": "On agit pour 'les nôtres'. Activer une identité partagée plus forte que l'argument rationnel.",
            "structure": "Désigner le 'nous' (génération, profession, situation, valeurs) → l'offre comme acte d'appartenance.",
            "gabarits": [
                "Pour nous, les [identité]",
                "[Identité] qui [valeur partagée] : [offre]"
            ],
            "when_works": ["niches identitaires fortes", "audiences communautaires", "marques challengers"],
            "when_avoid": ["mass-market", "audiences à identité diffuse"],
            "combines_with": {"angles": ["identite"], "emotions": ["appartenance", "fierte"], "formats": ["UGC-ad", "ad-statique"]},
            "anti_patterns": ["Tribu trop large (dilution)", "Identité plaquée (perçue cynique)"],
            "examples": [
                "Pour nous, les mamans qui ne se résignent pas à la chute post-bébé."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Cialdini Pre-Suasion"]}
        }
    ],

    "niveaux-schwartz": [
        {
            "id": "conscience",
            "name": "Stades de conscience (Schwartz)",
            "principle": "Le lecteur traverse 5 stades selon ce qu'il sait du problème, des solutions et du produit. Chaque stade demande un copy différent.",
            "structure": "unaware → problem-aware → solution-aware → product-aware → most-aware.",
            "gabarits": [
                "unaware : éduquer sur le pain (storytelling, stats)",
                "problem-aware : amplifier le pain et présenter les solutions (PAS, contrarian)",
                "solution-aware : différencier ta solution (mécanisme unique, avant-après)",
                "product-aware : prouver et lever objection (preuves, témoignages, garantie)",
                "most-aware : offre directe, urgence, rareté"
            ],
            "when_works": ["toujours, c'est une grille de lecture, pas un outil"],
            "when_avoid": ["jamais, mais à compléter avec sophistication"],
            "combines_with": {"frameworks": ["aida", "pas", "quest"], "hooks": ["confession", "contrarian", "stat-choc", "avant-apres", "social-proof-front"], "leads": ["story-led", "problem-led", "mechanism-led", "proof-led", "offer-led"]},
            "anti_patterns": ["Copy unaware appliqué à audience most-aware (perd son temps)", "Copy most-aware appliqué à audience unaware (perd l'attention)"],
            "examples": [
                "unaware : 'Tu sais combien de cheveux tu perds par jour ?' / problem-aware : 'La chute post-grossesse est plus longue qu'on dit' / solution-aware : 'Toutes les cures ne se valent pas' / product-aware : 'Pourquoi Cellule Boost est différent' / most-aware : 'Cure 3 mois -10% jusqu'à dimanche'."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Schwartz Breakthrough Advertising 1966"]}
        },
        {
            "id": "sophistication",
            "name": "Sophistication du marché (Schwartz)",
            "principle": "Le marché traverse 5 vagues selon combien de claims similaires ont été émis. Chaque vague demande un angle différent.",
            "structure": "Vague 1 (claim brut) → 2 (claim + bénéfice) → 3 (mécanisme expliqué) → 4 (mécanisme + différenciation) → 5 (identification, vibe, expérience).",
            "gabarits": [
                "Vague 1-2 : claim direct (rare aujourd'hui)",
                "Vague 3 : 'voilà comment ça marche'",
                "Vague 4 : 'voilà ce que les autres ne font pas'",
                "Vague 5 : 'pour les femmes qui [identité]'"
            ],
            "when_works": ["toujours, comme grille d'analyse marché"],
            "when_avoid": ["jamais"],
            "combines_with": {"frameworks": ["quest"], "hooks": ["contrarian", "curiosity-gap"], "angles": ["mecanisme-unique", "identite", "contre-intuitif"]},
            "anti_patterns": ["Claim vague 1 sur marché vague 4+ (sons obsolète)", "Identité vague 5 sur marché vague 1-2 (over-engineered)"],
            "examples": [
                "Marché compléments cheveux 2026 : vague 4 (mécanismes différenciants) à 5 (identité). Karacare vise l'identité (pour les femmes qui post-grossesse).",
                "Vague 5 : 'Karacare, pour celles qui ne se résignent pas.'"
            ],
            "lineage": {"source": "public-doctrine", "references": ["Schwartz Breakthrough Advertising 1966"]}
        }
    ],

    "archetypes-voix": [
        {
            "id": "caregiver",
            "name": "Caregiver",
            "principle": "Voix qui prend soin, rassure, accompagne. Bienveillante, douce, attentive.",
            "structure": "Vocabulaire d'attention, ton calme, reconnaissance du pain.",
            "gabarits": [
                "Tu n'es pas seule. Voilà ce qui peut aider.",
                "Prends soin de toi d'abord. La cure suit ton rythme."
            ],
            "when_works": ["produits santé, soin, parenting, wellness", "audiences vulnérables ou en transition"],
            "when_avoid": ["produits performance ou aspirationnels (trop mou)", "audiences cyniques ou anti-marketing soft"],
            "combines_with": {"hooks": ["confession", "question-callout"], "angles": ["identite", "retour-en-arriere"], "emotions": ["reconnaissance", "espoir", "soulagement"]},
            "anti_patterns": ["Mou sans direction (voix qui n'incite à rien)", "Maternant condescendant"],
            "examples": [
                "On sait que la chute post-grossesse est dure. La cure t'accompagne 3 mois, pas plus. Tu reprends la main."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Jung archetypes", "Mark & Pearson Hero and Outlaw"]}
        },
        {
            "id": "sage",
            "name": "Sage",
            "principle": "Voix qui sait, qui éclaire. Pédagogique, calme, autorité douce.",
            "structure": "Vocabulaire technique accessible, structure démonstrative, sources citées.",
            "gabarits": [
                "Voilà ce que la science dit, sans le jargon.",
                "Le mécanisme est simple : [explication claire]."
            ],
            "when_works": ["catégories santé, sciences, éducation", "audiences en recherche d'information vraie", "marchés à sophistication 3+"],
            "when_avoid": ["produits émotionnels ou aspirationnels", "audiences pressées (sage prend du temps)"],
            "combines_with": {"frameworks": ["quest", "fab"], "leads": ["mechanism-led", "proof-led"], "angles": ["mecanisme-unique"]},
            "anti_patterns": ["Sage qui devient prof ennuyeux", "Sage condescendant"],
            "examples": [
                "Le cycle pilaire dure 3 à 6 ans en phase anagène. La cure cible cette phase, c'est pour ça qu'on parle 90 jours minimum."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Jung archetypes"]}
        },
        {
            "id": "rebelle",
            "name": "Rebelle",
            "principle": "Voix qui s'oppose, qui casse les conventions. Tranchante, directe, parfois provocante.",
            "structure": "Vocabulaire frontal, ton sec, contre-pieds explicites.",
            "gabarits": [
                "Arrête tout. Ce que tu fais empire le truc.",
                "L'industrie te ment. Voilà la vérité."
            ],
            "when_works": ["marques challengers", "audiences frustrées", "marchés saturés à sophistication 4+"],
            "when_avoid": ["audiences conservatrices", "catégories régulées (rebelle paraît irresponsable)"],
            "combines_with": {"hooks": ["contrarian", "stat-choc"], "angles": ["ennemi-commun", "contre-intuitif"], "emotions": ["indignation", "soulagement"]},
            "anti_patterns": ["Rebelle pour la pose (pas de fond)", "Trop violent (devient repoussoir)"],
            "examples": [
                "Les shampoings 'anti-chute' ? La pire arnaque de la beauté. Voilà ce qui marche vraiment."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Jung archetypes"]}
        },
        {
            "id": "amante",
            "name": "Amante",
            "principle": "Voix sensuelle, qui célèbre le corps, le plaisir, l'image. Chaleureuse, complicit, tactile.",
            "structure": "Vocabulaire sensoriel, métaphores tactiles, complicit girl-talk.",
            "gabarits": [
                "Tu sens la différence dès le premier mois.",
                "Le toucher, la densité, le tombé du cheveu : tout change."
            ],
            "when_works": ["beauté, intimité, sensorialité", "audiences féminines à fort registre esthétique", "marques expérience plus que résultat"],
            "when_avoid": ["catégories cliniques", "audiences pressées par le résultat mesurable"],
            "combines_with": {"hooks": ["avant-apres"], "angles": ["status-shift"], "emotions": ["envie", "fierte"]},
            "anti_patterns": ["Sensualité plaquée (paraît cheap)", "Trop centré image (perd la substance)"],
            "examples": [
                "Le cheveu reprend du corps. Tu le sens sous la main, tu le vois en photo."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Jung archetypes"]}
        },
        {
            "id": "heros",
            "name": "Héros",
            "principle": "Voix qui motive à dépasser. Courage, action, volonté. Active la version 'meilleure soi'.",
            "structure": "Vocabulaire d'effort, dépassement, victoire. Verbes forts.",
            "gabarits": [
                "Tu décides aujourd'hui.",
                "90 jours pour reprendre la main sur ton cheveu."
            ],
            "when_works": ["fitness, performance, transformation", "audiences action-driven", "trafic chaud"],
            "when_avoid": ["audiences en détresse (héros dur sur soi)", "produits soin doux"],
            "combines_with": {"frameworks": ["bab", "4ps"], "angles": ["status-shift"], "emotions": ["fierte", "volonte"]},
            "anti_patterns": ["Bro-talk déconnecté", "Héroïque déplacé sur audience vulnérable"],
            "examples": [
                "Tu n'attends pas que ça passe. Tu agis. 90 jours."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Jung archetypes"]}
        },
        {
            "id": "homme-ordinaire",
            "name": "Homme ordinaire",
            "principle": "Voix de tout le monde. Honnête, simple, sans piédestal. Pratique avant tout.",
            "structure": "Vocabulaire courant, exemples du quotidien, ton casual.",
            "gabarits": [
                "Pas de magie. Ce qu'on a, c'est [X]. Et ça marche pour [profil].",
                "Soyons honnêtes : [vérité brute]."
            ],
            "when_works": ["audiences pragmatiques", "marchés saturés des claims aspirationnels", "trafic tiède"],
            "when_avoid": ["produits luxe ou aspirationnels", "audiences en quête d'élévation"],
            "combines_with": {"hooks": ["confession", "question-callout"], "frameworks": ["bab"], "emotions": ["complicite"]},
            "anti_patterns": ["Faux-modeste (perçu comme pose)", "Trop plat (manque d'aspiration)"],
            "examples": [
                "On ne va pas te promettre la lune. Ce qu'on a, c'est une cure 3 mois qui marche pour 6 mamans sur 10."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Jung archetypes"]}
        }
    ],

    "formules-titres": [
        {
            "id": "4u",
            "name": "4U",
            "principle": "Useful · Urgent · Unique · Ultra-spécifique. Grille de score d'un titre. Plus le titre coche les 4U, plus il convertit.",
            "structure": "Test mental : le titre est-il utile, urgent, unique, ultra-spécifique ?",
            "gabarits": [
                "[bénéfice ultra-spécifique] avant [deadline] pour [profil unique]"
            ],
            "when_works": ["toujours, comme checklist de réécriture de titre"],
            "when_avoid": ["titre qui ne peut être que 1-2 U (acceptable mais sub-optimal)"],
            "combines_with": {"formats": ["ad-statique", "email-sequence", "landing"]},
            "anti_patterns": ["Forcer les 4U au détriment de la voix naturelle"],
            "examples": [
                "Retrouver +37% de densité capillaire en 12 semaines même après 3 grossesses (4 U sur 4)."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Carlton, Halbert"]}
        },
        {
            "id": "how-to",
            "name": "How-to",
            "principle": "'Comment X sans Y'. Promesse pédagogique avec retrait d'obstacle. Très efficace SEO et hook curiosité.",
            "structure": "Comment [obtenir résultat] sans [obstacle perçu].",
            "gabarits": [
                "Comment [X] sans [Y]",
                "Comment [résultat] en [contrainte temporelle]"
            ],
            "when_works": ["contenu éducatif, blog, advertorial", "audiences problem-aware"],
            "when_avoid": ["copy émotionnel pur"],
            "combines_with": {"frameworks": ["quest"], "leads": ["mechanism-led"], "formats": ["advertorial", "landing", "email-sequence"]},
            "anti_patterns": ["How-to vague ('comment être heureux')", "How-to qui n'est pas réellement actionnable dans le copy"],
            "examples": [
                "Comment freiner la chute post-partum sans hormones",
                "Comment retrouver de la densité en 90 jours sans changer de routine"
            ],
            "lineage": {"source": "public-doctrine", "references": ["DR canon", "BuzzFeed playbook"]}
        },
        {
            "id": "listicle",
            "name": "Listicle",
            "principle": "'7 façons de X'. Format à pourquoi neurologique : promesse de complétude, scannabilité.",
            "structure": "Nombre + bénéfice + (optionnel) qualifier.",
            "gabarits": [
                "[N] façons de [résultat]",
                "[N] erreurs à éviter pour [résultat]"
            ],
            "when_works": ["contenu blog, advertorial, email", "audiences scrollers", "trafic froid"],
            "when_avoid": ["copy long-form profond (listicle reste surface)"],
            "combines_with": {"formats": ["advertorial", "blog", "email-sequence"]},
            "anti_patterns": ["Listicle dilué (5 points faibles vs 3 puissants)", "Numéros forcés (5 quand 3 suffit)"],
            "examples": [
                "7 erreurs qui sabotent ta cure capillaire (et comment les éviter)",
                "5 raisons pour lesquelles ta repousse stagne"
            ],
            "lineage": {"source": "public-doctrine", "references": ["BuzzFeed", "DR canon"]}
        },
        {
            "id": "secret",
            "name": "Secret / what they don't tell you",
            "principle": "Promet une info réservée. Active le curiosity-gap et l'autorité (l'auteur sait ce que les autres taisent).",
            "structure": "[Info cachée] que [autorité/groupe] ne te dit pas sur [sujet].",
            "gabarits": [
                "Le truc que les [groupe] ne disent pas sur [X]",
                "[N] vérités cachées sur [sujet]"
            ],
            "when_works": ["sophistication 3+", "audiences sceptiques", "VSL et advertorials"],
            "when_avoid": ["audiences saturées du clickbait", "claims non vérifiables"],
            "combines_with": {"hooks": ["curiosity-gap", "contrarian"], "angles": ["ennemi-commun"], "formats": ["VSL", "advertorial"]},
            "anti_patterns": ["Secret qui n'est pas un secret", "Cliffhanger sans payoff"],
            "examples": [
                "Le truc que les marques de shampoing ne te disent pas sur la chute post-partum"
            ],
            "lineage": {"source": "public-doctrine", "references": ["DR canon"]}
        },
        {
            "id": "commande",
            "name": "Commande / impératif",
            "principle": "Ouvre par un verbe à l'impératif. Ton tranchant, direct, frontal.",
            "structure": "Verbe à l'impératif + objet/cible.",
            "gabarits": [
                "Arrête de [pratique]",
                "Lis ça avant de [action courante]"
            ],
            "when_works": ["marques challengers, voix rebelle", "audiences fatiguées du registre soft"],
            "when_avoid": ["marques caregiver (clash de voix)", "audiences vulnérables"],
            "combines_with": {"angles": ["contre-intuitif", "ennemi-commun"], "archetypes": ["rebelle", "heros"]},
            "anti_patterns": ["Commande sans payoff", "Trop militaire (perd la chaleur)"],
            "examples": [
                "Arrête ta cure de biotine. Tu sabote ta repousse."
            ],
            "lineage": {"source": "public-doctrine", "references": ["DR canon"]}
        },
        {
            "id": "question",
            "name": "Question",
            "principle": "Ouvre par une question qui force la réflexion. Active l'engagement.",
            "structure": "Question ouverte ou rhétorique sur le pain ou l'attente.",
            "gabarits": [
                "Et si [X] était la cause de [Y] ?",
                "Pourquoi [résultat attendu] ne marche pas pour toi ?"
            ],
            "when_works": ["sophistication 3+", "audiences problem-aware", "advertorial, blog, email"],
            "when_avoid": ["question rhétorique vide", "audiences pressées"],
            "combines_with": {"hooks": ["question-callout", "curiosity-gap"], "frameworks": ["pas", "quest"]},
            "anti_patterns": ["Question fermée à laquelle on répond non", "Question génériquement marketing"],
            "examples": [
                "Et si la chute post-partum n'était pas hormonale ?",
                "Pourquoi ta cure stagne après 30 jours ?"
            ],
            "lineage": {"source": "public-doctrine", "references": ["DR canon"]}
        }
    ],

    "objections": [
        {
            "id": "feel-felt-found",
            "name": "Feel · Felt · Found",
            "principle": "Empathie d'abord, puis preuve. 'Je comprends ce que tu ressens. D'autres l'ont ressenti. Voilà ce qu'ils ont trouvé.'",
            "structure": "Feel (acknowledge) → Felt (others did too) → Found (la résolution).",
            "gabarits": [
                "Je comprends que tu te dises [objection]. C'est ce que [N personnes similaires] se disent. Voilà ce qu'on a trouvé : [résolution]."
            ],
            "when_works": ["objections émotionnelles", "audiences sceptiques mais pas hostiles", "messaging long-form"],
            "when_avoid": ["objections rationnelles (prix, délais)", "audiences déjà convaincues"],
            "combines_with": {"frameworks": ["pas", "quest"], "archetypes": ["caregiver", "sage"], "formats": ["VSL", "email-sequence", "landing"]},
            "anti_patterns": ["Empathie plaquée non sentie", "Sauter Felt (perd la dimension sociale)"],
            "examples": [
                "Tu te dis 'encore un produit miracle'. C'est ce que beaucoup de mamans pensaient avant. Ce qu'elles ont trouvé : 90 jours de cure ciblée, pas une promesse magique."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Sales canon", "Carnegie"]}
        },
        {
            "id": "reframe-positif",
            "name": "Reframe positif",
            "principle": "Transforme l'objection en argument positif. Renverse le cadre mental.",
            "structure": "Reconnaître l'objection → la requalifier sous un autre angle.",
            "gabarits": [
                "Tu dis [objection]. C'est précisément pour ça que [angle inverse]."
            ],
            "when_works": ["objections fréquentes et prévisibles", "audiences ouvertes au dialogue"],
            "when_avoid": ["objections fondamentales (le reframe paraît tordu)"],
            "combines_with": {"hooks": ["contrarian"], "angles": ["contre-intuitif"], "frameworks": ["pas"]},
            "anti_patterns": ["Reframe forcé (perçu manipulation)", "Inverser sans démontrer"],
            "examples": [
                "Tu trouves la cure 3 mois longue ? C'est précisément la durée d'un cycle pilaire complet. Plus court = pas de transformation."
            ],
            "lineage": {"source": "public-doctrine", "references": ["NLP", "Sales canon"]}
        },
        {
            "id": "pre-emption",
            "name": "Pre-emption",
            "principle": "Traite l'objection avant qu'elle vienne. Désamorce en l'incluant dans le copy.",
            "structure": "Énoncer l'objection probable + la résoudre proactivement.",
            "gabarits": [
                "Tu vas peut-être te dire [objection]. Voilà pourquoi ce n'est pas le cas : [résolution].",
                "Avant que tu te poses la question : [objection nommée], [résolution]."
            ],
            "when_works": ["objections récurrentes connues du brand", "audiences sceptiques", "long-form"],
            "when_avoid": ["objections trop spécifiques (les évoquer ouvre la porte)"],
            "combines_with": {"frameworks": ["quest", "pas"], "leads": ["proof-led"], "formats": ["VSL", "advertorial", "landing"]},
            "anti_patterns": ["Pre-empt trop tôt (ouvre des doutes non-existants)", "Lister 10 objections (paraît défensif)"],
            "examples": [
                "Tu vas te dire 'j'ai déjà testé la biotine, ça marche pas'. C'est normal : la biotine seule ne suffit pas. Voilà le complexe complet."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Sales canon", "DR"]}
        },
        {
            "id": "comparaison-cout-inaction",
            "name": "Comparaison coût d'inaction",
            "principle": "Compare le coût du produit au coût de ne rien faire. Recadre le prix comme investissement.",
            "structure": "Coût visible (produit) vs coût caché (inaction prolongée).",
            "gabarits": [
                "[Prix produit] / vs [coût d'inaction calculé]",
                "Ne rien faire te coûte plus que [investissement nommé]."
            ],
            "when_works": ["objections prix", "produits dont l'inaction a un coût mesurable", "audiences rationnelles"],
            "when_avoid": ["audiences à pouvoir d'achat très contraint", "produits impulse buying"],
            "combines_with": {"frameworks": ["fab"], "leads": ["proof-led"], "emotions": ["regret-anticipe"]},
            "anti_patterns": ["Coût d'inaction inventé (perd crédibilité)", "Calcul tordu"],
            "examples": [
                "Cure 3 mois : 89€. Attendre 12 mois sans rien faire : 6 mois supplémentaires de chute, perte de densité partiellement irréversible."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Sales canon"]}
        }
    ],

    "construction-offre": [
        {
            "id": "anchor-decoy",
            "name": "Anchor / Decoy",
            "principle": "Présente une option chère (anchor) qui rend la cible visée plus attractive. Ou une option leurre (decoy) qui pousse vers le bundle.",
            "structure": "3 prix : low / target / high. Le target devient le 'best value' relatif.",
            "gabarits": [
                "Cure 1 mois 39€ / Cure 3 mois 89€ (-25%) / Cure 6 mois 169€ (-30%)"
            ],
            "when_works": ["e-commerce avec gammes", "produits récurrents (cures, abonnements)", "audiences price-sensitive"],
            "when_avoid": ["mono-produit sans gamme", "audiences luxe (le decoy paraît cheap)"],
            "combines_with": {"formats": ["landing", "checkout"], "leads": ["offer-led"]},
            "anti_patterns": ["3 options avec prix très proches (anchor non visible)", "Decoy mal calibré (la cible n'apparaît pas comme deal)"],
            "examples": [
                "Hair Boost : 1 mois 29.90€ / 3 mois 69.90€ -22% / 6 mois 132.90€ -26% + bonus."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Behavioral economics", "Ariely"]}
        },
        {
            "id": "bundle-stack",
            "name": "Bundle stack",
            "principle": "Empile produits/bonus pour augmenter la valeur perçue tout en gardant un prix qui ressemble à du bargain.",
            "structure": "Produit principal + accessoires + bonus information + garantie. Total perçu >> prix.",
            "gabarits": [
                "Cure 3 mois (89€) + brosse stimulante (15€) + guide PDF (gratuit) + garantie 60j = 89€"
            ],
            "when_works": ["closing de funnel", "saisonnalités (Black Friday, fête des Mères)", "AOV à pousser"],
            "when_avoid": ["audiences habituées au bundle (saturé)", "produits à AOV déjà élevé"],
            "combines_with": {"formats": ["landing", "checkout", "VSL"], "frameworks": ["aida", "4ps"]},
            "anti_patterns": ["Bundle gonflé d'objets sans valeur", "Bundle illisible (trop d'éléments)"],
            "examples": [
                "Cure Hair Boost + Cellule Boost + bonnet serviette + applicateur huile = 132.90€ au lieu de 167€."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Hormozi $100M Offers"]}
        },
        {
            "id": "garantie-risk-reversal",
            "name": "Garantie / risk reversal",
            "principle": "Renverse le risque de l'acheteur vers le vendeur. Lève l'objection 'et si ça ne marche pas pour moi'.",
            "structure": "Promesse garantie + condition simple + procédure de remboursement.",
            "gabarits": [
                "Tu testes [N jours]. Si tu ne vois rien, on rembourse intégralement.",
                "Garantie [durée] : pas de résultat = remboursement automatique."
            ],
            "when_works": ["produits à promesse mesurable", "audiences sceptiques", "produits chers"],
            "when_avoid": ["produits où le résultat est subjectif (esthétique pure)", "marchés où le SAV ne suit pas"],
            "combines_with": {"objections": ["pre-emption", "comparaison-cout-inaction"], "leads": ["offer-led"], "formats": ["landing", "checkout"]},
            "anti_patterns": ["Garantie avec conditions cachées", "Garantie courte sur produit à effet long (cure 3 mois, garantie 14j)"],
            "examples": [
                "Garantie 90 jours résultats : pas de freinage de chute visible ? Remboursement intégral, pas de questions."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Hormozi", "Halbert"]}
        },
        {
            "id": "urgence-rarete-temps",
            "name": "Urgence / rareté temporelle",
            "principle": "Active le FOMO via deadline visible. La rareté de temps déclenche l'action.",
            "structure": "Annonce d'une fin claire (date, heure) + conséquence concrète (perte d'offre, retour au prix plein).",
            "gabarits": [
                "Offre [nom] valable jusqu'à [date heure]. Après : retour au prix plein.",
                "Plus que [N] jours pour [bénéfice de l'offre]."
            ],
            "when_works": ["closing", "promotions saisonnières crédibles", "trafic chaud"],
            "when_avoid": ["urgence permanente (cliquables fakes)", "audiences anti-FOMO"],
            "combines_with": {"frameworks": ["aida", "4ps"], "objections": ["comparaison-cout-inaction"], "formats": ["email-sequence", "ad-statique"]},
            "anti_patterns": ["Countdown qui reset à chaque visite", "Urgence sans raison crédible"],
            "examples": [
                "Offre Mother's Day Karacare : -15% sur la cure 3m + brosse offerte. Fin dimanche 18h."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Cialdini", "DR canon"]}
        }
    ],

    "leads": [
        {
            "id": "offer-led",
            "name": "Offer-led",
            "principle": "Ouvre directement sur l'offre. Pour audience most-aware ou trafic chaud.",
            "structure": "Annonce de l'offre + prix + deadline. Pas de pitch préalable.",
            "gabarits": [
                "Cure 3 mois Hair Boost à -25% jusqu'à dimanche."
            ],
            "when_works": ["most-aware", "retargeting", "promotions courte durée"],
            "when_avoid": ["trafic froid", "audiences problem-aware"],
            "combines_with": {"frameworks": ["aida"], "construction-offre": ["urgence-rarete-temps", "anchor-decoy"]},
            "anti_patterns": ["Offer-led sur trafic froid (perd l'audience)"],
            "examples": [
                "30% sur la cure 6 mois jusqu'à dimanche minuit. Repousse 12 sem garantie."
            ],
            "lineage": {"source": "public-doctrine", "references": ["DR canon"]}
        },
        {
            "id": "mechanism-led",
            "name": "Mechanism-led",
            "principle": "Ouvre sur l'explication du mécanisme unique du produit. Pour audience product-aware ou solution-aware en quête de différenciation.",
            "structure": "Annonce du mécanisme + démonstration de pourquoi c'est différent.",
            "gabarits": [
                "Voilà pourquoi [produit] active [mécanisme] que [autres] ignorent."
            ],
            "when_works": ["solution-aware, product-aware", "marché sophistication 3+", "VSL et long-form"],
            "when_avoid": ["unaware", "trafic ultra-froid"],
            "combines_with": {"frameworks": ["quest"], "angles": ["mecanisme-unique"], "archetypes": ["sage"]},
            "anti_patterns": ["Mécanisme bidon", "Trop technique"],
            "examples": [
                "Cellule Boost active la phase anagène. C'est ce que les vitamines classiques manquent."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Schwartz"]}
        },
        {
            "id": "story-led",
            "name": "Story-led",
            "principle": "Ouvre sur une histoire (founder, customer, narrative). Bypass des défenses publicitaires par récit.",
            "structure": "Anecdote concrète + bascule + apprentissage + offre.",
            "gabarits": [
                "Il y a [durée], [protagoniste] vivait [situation pénible]. Voilà ce qui a changé."
            ],
            "when_works": ["UGC, founder, advertorial", "marques humaines", "tous stades sauf most-aware"],
            "when_avoid": ["B2B technique", "audiences pressées"],
            "combines_with": {"hooks": ["confession"], "angles": ["retour-en-arriere", "identite"], "archetypes": ["caregiver", "homme-ordinaire"]},
            "anti_patterns": ["Histoire trop longue avant le point", "Histoire qui n'enseigne rien"],
            "examples": [
                "Quand Jeanne a accouché de son 2e enfant, elle ne se reconnaissait plus dans le miroir. 6 mois plus tard..."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Halbert", "Donald Miller"]}
        },
        {
            "id": "problem-led",
            "name": "Problem-led",
            "principle": "Ouvre sur le pain de l'audience. Activation immédiate de la reconnaissance.",
            "structure": "Description précise du pain + amplification + bascule vers solution.",
            "gabarits": [
                "[Description du pain spécifique] / Voilà ce qui se passe vraiment / Voilà ce qui aide."
            ],
            "when_works": ["problem-aware, solution-aware", "trafic froid", "advertorial"],
            "when_avoid": ["most-aware", "audiences déjà éduquées"],
            "combines_with": {"frameworks": ["pas"], "hooks": ["question-callout", "stat-choc"], "emotions": ["frustration", "espoir"]},
            "anti_patterns": ["Pain trop générique", "Sauter sur la solution sans amplifier"],
            "examples": [
                "Tu te brosses, tu vois la touffe sur la brosse. Tu te dis que ça va passer. Voilà pourquoi ça ne passe pas seul."
            ],
            "lineage": {"source": "public-doctrine", "references": ["DR canon"]}
        },
        {
            "id": "proof-led",
            "name": "Proof-led",
            "principle": "Ouvre sur la preuve : témoignage, étude, before/after. Court-circuite le pitch par l'autorité immédiate.",
            "structure": "Preuve forte (visuel, chiffre, témoignage) + contextualisation + offre.",
            "gabarits": [
                "[N personnes profil similaire] / [résultat mesuré] / [comment]"
            ],
            "when_works": ["trafic froid sceptique", "marchés saturés", "produits transformation visible"],
            "when_avoid": ["produits sans preuve forte", "audiences qui rejettent le statistique"],
            "combines_with": {"hooks": ["social-proof-front", "stat-choc"], "heuristiques-persuasion": ["preuve-sociale", "autorite"]},
            "anti_patterns": ["Preuve fabriquée", "Preuve hors-contexte"],
            "examples": [
                "63 000 mamans post-partum ont retrouvé leur densité. Voilà ce qu'elles ont fait."
            ],
            "lineage": {"source": "public-doctrine", "references": ["DR canon"]}
        }
    ],

    "formats-livrables": [
        {
            "id": "ugc-ad",
            "name": "UGC ad",
            "principle": "Vidéo selfie format mobile par créatrice ou customer. Effet authentique, low-fi, contourne les défenses publicitaires.",
            "structure": "Hook 3 sec + situation relatable + démo/résultat + CTA. 15-60 sec.",
            "gabarits": [
                "[hook attention 3s] [contexte 5s] [résultat/démo 15s] [CTA 5s]"
            ],
            "when_works": ["Meta, TikTok, Reels", "audiences scrollers", "marques DTC"],
            "when_avoid": ["B2B premium", "audiences ultra-segmentées non-scrollers"],
            "combines_with": {"hooks": ["confession", "question-callout", "avant-apres"], "archetypes": ["amante", "caregiver", "homme-ordinaire"], "leads": ["story-led"]},
            "anti_patterns": ["UGC trop produit (perd le low-fi)", "Hook qui prend 8 secondes"],
            "examples": [
                "Maman 32 ans face cam, brosse à la main, montre le résultat à 12 sem."
            ],
            "lineage": {"source": "public-doctrine", "references": ["DTC paid playbook 2024+"]}
        },
        {
            "id": "vsl",
            "name": "VSL",
            "principle": "Video Sales Letter. 5-30 min de vidéo qui suit un script DR complet (qualify, problem, solution, proof, offer). Long mais converti fort.",
            "structure": "QUEST framework étendu en vidéo. Voix-off + visuels supports.",
            "gabarits": [
                "Si tu es [profil], cette vidéo est pour toi / Voilà la situation / Ce que personne ne te dit / Voilà comment on règle ça / Voilà l'offre"
            ],
            "when_works": ["produits à AOV moyen-élevé", "audiences problem-aware sophistication 3+", "remarketing"],
            "when_avoid": ["audiences pressées", "produits impulse buying"],
            "combines_with": {"frameworks": ["quest"], "leads": ["mechanism-led", "story-led"], "objections": ["pre-emption"]},
            "anti_patterns": ["VSL trop courte (sous-utilise le format)", "VSL plate sans modulation rythmique"],
            "examples": [
                "VSL Karacare 12 min : qualifie mamans 28-45, raconte la chute post-partum, mécanisme cycle pilaire, témoignages, offre cure 6 mois."
            ],
            "lineage": {"source": "public-doctrine", "references": ["DR canon", "Russell Brunson"]}
        },
        {
            "id": "landing",
            "name": "Landing page",
            "principle": "Page web dédiée à une seule action (achat, lead). Hiérarchie above-the-fold + sections persuasion + closing.",
            "structure": "Hero (headline + sub + CTA + visuel) → social proof → mécanisme → offre détaillée → garantie → FAQ → CTA final.",
            "gabarits": [
                "Hero 4U / 3 reviews social proof / mécanisme avec visuel / offre anchor-decoy / garantie risk-reversal / FAQ pre-emption objections"
            ],
            "when_works": ["e-commerce DTC", "lead gen", "campagnes paid"],
            "when_avoid": ["pages multi-produits (cannibalise)", "trafic à intent ultra-faible"],
            "combines_with": {"frameworks": ["aida", "fab"], "construction-offre": ["anchor-decoy", "bundle-stack", "garantie-risk-reversal"]},
            "anti_patterns": ["Landing à scroll infini sans CTA répété", "Hero qui ne fait pas le 4U test"],
            "examples": [
                "Landing Hair Boost cure 3 mois : hero promesse densité, 6 témoignages, mécanisme cycle pilaire visuel, anchor-decoy 3 cures, garantie 90j, FAQ 5 objections."
            ],
            "lineage": {"source": "public-doctrine", "references": ["DR canon", "CRO playbook"]}
        },
        {
            "id": "email-sequence",
            "name": "Email sequence",
            "principle": "Série d'emails programmés qui éduque, prouve, convertit. Permet de traiter les objections une par une dans le temps.",
            "structure": "Welcome → éducation → proof → offre → urgence. 5-12 emails.",
            "gabarits": [
                "D1 welcome / D2 problem-led / D4 mechanism-led / D7 social-proof / D10 offer / D14 urgency"
            ],
            "when_works": ["funnels lead-magnet, post-purchase, abandon panier", "audiences éducables sur la durée"],
            "when_avoid": ["audiences à intention immédiate", "produits commodity"],
            "combines_with": {"frameworks": ["pas", "quest"], "objections": ["pre-emption"], "construction-offre": ["urgence-rarete-temps"]},
            "anti_patterns": ["Séquence trop poussive (chaque mail = pitch)", "Cadence trop espacée (perd l'engagement)"],
            "examples": [
                "Lead-magnet 'Guide chute post-partum' → séquence 7 emails : éducation cycle, mécanisme, témoignages, cure offre."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Klaviyo playbook", "DR canon"]}
        },
        {
            "id": "ad-statique",
            "name": "Ad statique",
            "principle": "Image fixe optimisée scroll-stop. 1 message clair, hierarchie visuelle nette.",
            "structure": "Visuel stop-scrolling + headline 4U + sous-texte court + CTA.",
            "gabarits": [
                "[Visuel before/after ou scène pain] / [headline 4U] / [CTA 3 mots]"
            ],
            "when_works": ["Meta, Pinterest, display", "complément aux UGC", "remarketing"],
            "when_avoid": ["TikTok native (vidéo dominante)", "audiences ultra-scroll-blind"],
            "combines_with": {"hooks": ["avant-apres", "stat-choc"], "formules-titres": ["4u", "how-to"]},
            "anti_patterns": ["Visuel trop branding pas assez stop", "Trop de texte"],
            "examples": [
                "Visuel maman se brossant les cheveux + headline 'Retrouve ta densité en 90 jours' + bouton 'Voir la cure'."
            ],
            "lineage": {"source": "public-doctrine", "references": ["Meta playbook"]}
        },
        {
            "id": "advertorial",
            "name": "Advertorial",
            "principle": "Article éditorial qui ressemble à du contenu mais convertit. Mid-funnel entre ad et landing.",
            "structure": "Headline curieux → intro éditoriale → exposition pain → exposition mécanisme → preuve → bascule offre → CTA. 800-2500 mots.",
            "gabarits": [
                "Pourquoi [résultat] échoue malgré [effort] (et ce qui marche vraiment)"
            ],
            "when_works": ["trafic froid à éduquer", "produits à mécanisme à expliquer", "marchés sophistiqués"],
            "when_avoid": ["audiences pressées", "produits impulse"],
            "combines_with": {"frameworks": ["quest"], "hooks": ["curiosity-gap"], "leads": ["mechanism-led", "story-led"], "formules-titres": ["secret", "how-to"]},
            "anti_patterns": ["Advertorial trop branded (perd le côté éditorial)", "Pivot offre trop abrupt"],
            "examples": [
                "Article 'Ce que les dermatos ne disent pas sur la chute post-partum' → mécanisme cycle pilaire → témoignages → cure Karacare."
            ],
            "lineage": {"source": "public-doctrine", "references": ["DR canon", "Halbert"]}
        }
    ]
}


def main():
    force = "--force" in sys.argv
    dry_run = "--dry-run" in sys.argv

    root = find_workspace_root(Path.cwd())
    if root is None:
        print("ERROR: workspace root not found", file=sys.stderr)
        sys.exit(1)

    canon_dir = root / "resources" / "canon" / "copy"
    counts = {"created": 0, "skipped": 0, "overwritten": 0}
    now = datetime.utcnow().isoformat() + "Z"

    for layer, tools in CANON.items():
        layer_dir = canon_dir / layer
        if not dry_run:
            layer_dir.mkdir(parents=True, exist_ok=True)
        for tool in tools:
            target = layer_dir / f"{tool['id']}.json"
            doc = {
                "_schema": "canon-tool/1.0",
                "_version": "1.0",
                "id": tool["id"],
                "atlas": "copy",
                "layer": layer,
                "name": tool["name"],
                "principle": tool["principle"],
                "structure": tool.get("structure", ""),
                "gabarits": tool.get("gabarits", []),
                "when_works": tool.get("when_works", []),
                "when_avoid": tool.get("when_avoid", []),
                "combines_with": tool.get("combines_with", {}),
                "anti_patterns": tool.get("anti_patterns", []),
                "examples": tool.get("examples", []),
                "validations": [],
                "lineage": tool.get("lineage", {"source": "public-doctrine", "references": []}),
                "_field_types": {
                    "id": "stated",
                    "atlas": "stated",
                    "layer": "stated",
                    "name": "stated",
                    "principle": "stated",
                    "structure": "stated",
                    "gabarits[]": "stated",
                    "when_works[]": "stated",
                    "when_avoid[]": "stated",
                    "combines_with.*": "stated",
                    "anti_patterns[]": "stated",
                    "examples[]": "stated",
                    "validations[]": "observed",
                    "lineage.*": "stated"
                },
                "_seeded_at": now
            }

            exists = target.exists()
            if exists and not force:
                counts["skipped"] += 1
                continue
            if dry_run:
                action = "would-overwrite" if exists else "would-create"
                print(f"  {action}: {layer}/{tool['id']}")
                counts["created" if not exists else "overwritten"] += 1
                continue
            with target.open("w", encoding="utf-8") as f:
                json.dump(doc, f, ensure_ascii=False, indent=2)
                f.write("\n")
            if exists:
                counts["overwritten"] += 1
                print(f"  overwritten: {layer}/{tool['id']}")
            else:
                counts["created"] += 1
                print(f"  created: {layer}/{tool['id']}")

    print()
    print(f"Summary: created={counts['created']}, overwritten={counts['overwritten']}, skipped={counts['skipped']}")
    if dry_run:
        print("(dry-run, no files written)")
    else:
        total = sum(len(t) for t in CANON.values())
        print(f"Atlas canon copy seeded: {total} tools across {len(CANON)} layers.")
        print(f"Location: {canon_dir}")


if __name__ == "__main__":
    main()
