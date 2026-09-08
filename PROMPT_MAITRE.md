# MEGA-PROMPT — Rapport PFE + Soutenance « Cléopâtre » (tout reproduire)

> Prompt maître, autonome et réutilisable : donne ce prompt à un agent IA pour régénérer
> l'intégralité des livrables (rapport PDF ~115 pages + PowerPoint de soutenance avec Morph).

---

## ROLE

Tu es un ingénieur full-stack + designer éditorial + rédacteur académique francophone.
Tu produis DEUX livrables professionnels pour un Projet de Fin d'Études (PFE) :
1. Un **rapport PDF** d'environ 110-120 pages, généré en Python (fpdf2 + matplotlib).
2. Un **PowerPoint de soutenance** (~25 diapos + annexes) avec **vraies transitions Morph**.

## CONTEXTE PROJET (à respecter fidèlement)

- **Sujet** : « Conception et réalisation d'une plateforme e-commerce pour la parapharmacie Cléopâtre
  — Espace Santé Beauté » (2 boutiques : Ezzahra et Hammam-Lif, Tunisie).
- **Point clé** : l'ancien site vitrine a été **entièrement reconstruit de zéro** (zéro reprise de code).
- **Méthode** : Scrum — 1 sprint 0 (cadrage) + 4 sprints (2 semaines) en 2 releases.
  - Release 1 : S1 Socle (comptes, rôles, dashboard) + S2 Commerce (catalogue, stock, commandes).
  - Release 2 : S3 Relation client (avis, support) + S4 Recherche, journal, Docker.
- **Stack** : Next.js 16, React 19, TypeScript strict, Tailwind, PostgreSQL 18, Drizzle ORM,
  Zod, scrypt, Docker. Chiffres officiels : **24 récits (US01–US24), 81 produits, 16 marques,
  7 univers, 24 tables, 10 énumérations, 7 statuts commande, ~30 Server Actions**.
- **Garanties** : montants en millimes (entiers), scrypt salé, sessions httpOnly 256 bits,
  gardes serveur, verrous `FOR UPDATE`, commandes idempotentes, audit complet.
- **Langue** : français soigné (typographie FR : espace avant `: ; ! ?`, guillemets « »).
  Résumé FR + Abstract EN en fin de rapport.
- **Placeholders** : TOUTE info personnelle/école en `[crochets]` (jamais de fausse donnée réelle).

## LIVRABLE 1 — RAPPORT PDF

### Structure imposée (dans cet ordre)
1. Couverture (double cadre or, double logo haut : `[Établissement]` + Cléopâtre, titre, encadrants).
2. Jury, Dédicaces, Remerciements.
3. Table des matières + Liste des figures + Liste des tableaux + Liste des extraits de code
   (TOUTES cliquables : liens internes vers la page exacte) + Liste des abréviations.
4. **Pages intercalaires de chapitre** (pleine page : grand chiffre romain fantôme, titre serif,
   épigraphe en italique) avant : Introduction, Ch. I–IV, Conclusion, Annexes.
5. Introduction générale + Chapitre I (étude préalable, existant, critique, solution, Scrum).
6. Chapitre II = Sprint 0 (acteurs, besoins BF1–BF8/BNF1–BNF8, UC général, backlog 24 récits,
   releases + feuille de route, technologies, architectures).
7. Chapitres III–IV = releases (par sprint : backlog, analyse UC + descriptions textuelles,
   conception UML classes/séquences, réalisation avec maquettes + extraits de code).
8. **2 diagrammes de classes consolidés** : release 1 (14 classes, §III.3.3.3) et modèle global
   (10 tables, §IV.3.3.3) + renvoi au dictionnaire.
9. Conclusion générale (ouvrir sur une infographie « Le projet en chiffres » : 6 tuiles).
10. Bibliographie & Webographie.
11. **Annexes A–E** : A = comparatif avant/après refonte (6 cadres « AVANT » à remplir par
    captures + renvois « APRÈS » + tableau de synthèse) ; B = dictionnaire de données
    (24 tables en 3 tableaux + 10 énumérations) ; C = guide de déploiement Docker ;
    D = backlog consolidé des 24 récits ; E = comptes de démo + tests d'acceptation.
12. Résumé FR + Abstract EN + mots-clés. **4e de couverture** (fond encre, résumé bilingue court).

### Figures (~96, style homogène, 100 % matplotlib)
- Palette : encre `#2B2620`, or `#C9A959`, champagne, papier `#FAF7F0`, ardoise, sauge, rouille.
- Polices figures : DejaVu Sans / Serif / Mono UNIQUEMENT.
- **CONTRAINTE CRITIQUE** : DejaVu ne contient NI emoji NI ⛔ NI ⚠(serif). N'utiliser que :
  texte + `• ◆ → ★ ☆ ✓ ✕ ①② — … « »`. Zéro « tofu » (vérifier chaque PNG).
- Types : logos, organigramme, Scrum, UC (acteurs + ellipse centrale), classes, séquences,
  maquettes d'écrans, machine à états, architecture, Docker, pipeline, modèles consolidés,
  cadres AVANT pointillés or avec marche à suivre, KPI, roadmap.
- Légendes auto-numérotées « Figure N – … », cadre pierre fin autour de chaque figure.

### Moteur PDF (exigences techniques)
- fpdf2, A4, marges 22/20mm. En-tête courant = chapitre en capitales ; folio or « — N — ».
- **Signets PDF** (`start_section`, 3 niveaux) + **métadonnées** (titre, auteur, sujet).
- Build **multi-passes déterministe** : mesure → front → destinations → finale ; assertions
  de stabilité (TOC/figures/tableaux/extraits identiques entre passes) ; le build ÉCHOUE si instable.
- Tableaux : grille manuelle (fonds pleine hauteur, jamais de trous blancs), mesure exacte des
  lignes par `multi_cell(dry_run=True, output='LINES')`, rupture de page par ligne.
- `current_chapter` TOUJOURS affecté AVANT `add_page()` (sinon en-tête obsolète).
- QA obligatoire : recompter figures/tableaux vs résumé, vérifier liens (pymupdf), rendre et
  inspecter visuellement : couverture, sommaire, 1 intercalaire, 1 tableau dense, 1 modèle, 1 annexe.

## LIVRABLE 2 — POWERPOINT (python-pptx + Morph réel)

- Format 16:9. Thème sombre « quiet luxury » : fond `#201A13`, texte `#F3ECDD`, or `#C9A959`.
  Polices SURES partout : Georgia (titres) + Calibri (texte). Zéro police exotique.
- **Morph VÉRITABLE** injecté en XML sur CHAQUE diapo (spec Microsoft MS-PPTX §2.2.1/2.6.1.1) :
  `mc:AlternateContent` après `clrMapOvr` → `Choice Requires="p159"` :
  `<p:transition spd="med" advOnClk="1" p14:dur="900"><p159:morph option="byObject"/></>`
  (`p159` = `http://schemas.microsoft.com/office/powerpoint/2015/09/main`) + `Fallback` en fondu.
- Chorégraphie Morph : formes homologues nommées `!!` (fond, eyebrow, titre, filet, pied,
  numéro, logo) ; **grand chiffre de section fantôme** qui morph à chaque section ;
  **5 dividers de section** (chiffre géant → zoom Morph vers le coin) ; 2 slides « build »
  (sécurité 3+3, bilan 2+2 : les éléments glissent à l'apparition).
- Contenu (~19 + 4 secours) : couverture à double cadre or, plan 5 temps, contexte,
  problématique + refonte, solution, Scrum/releases, acteurs/besoins, stack en **cartes logos**,
  architecture, modèle de données, S1→S4 (captures du rapport), avant/après, sécurité,
  bilan chiffré, **slide Démonstration** (scénario 6 min + QR/URL/comptes `[à compléter]`),
  Merci/perspectives + **4 slides secours jury** (machine à états, sécurité, modèle global,
  déploiement, avec notes d'anticipation).
- Finitions : coins arrondis sur TOUTES les images (`roundRect` injecté), numérotation
  auto-post-traitée, **notes présentateur en français + minutage** sur chaque diapo (total ~15 min).
- Validation : rouvrir le PPTX, vérifier Morph sur N/N diapos, aucune forme hors cadre,
  aucun chevauchement non voulu (texte-dans-panneau excepté), toutes notes ≥ 40 caractères.

## RÈGLES DE TRAVAIL

1. Une seule chose à la fois ; jamais d'éditions parallèles sur le même fichier.
2. Chaque figure régénérée est contrôlée (glyphes + mise en page) avant usage.
3. Chiffres cohérents PARTOUT (récits, produits, marques, tables, pages, figures, tableaux).
4. Tout nouveau contenu s'insère dans la structure existante (numérotation auto).
5. Commit + push sur la branche de session à chaque étape validée.
6. Réponse finale : ce qui a été livré, fichiers, comptes, tests effectués, reste à compléter.

## CRITÈRE DE SUCCÈS

Un jury exigeant doit être impressionné à l'ouverture (couverture, intercalaires, design),
convaincu à la lecture (rigueur UML, code réel, chiffres cohérents, annexes utiles) et
conquis en soutenance (Morph fluides, rythme, démo, réponses prêtes). Niveau : mention.
