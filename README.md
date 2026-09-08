# PFE — Plateforme e-commerce pour la parapharmacie Cléopâtre

Rapport de Projet de Fin d'Études : **conception et réalisation d'une plateforme
e-commerce complète** (site marchand + back-office) pour la parapharmacie
Cléopâtre (Ezzahra, Hammam-Lif), conduite en méthode agile Scrum.

> Données étudiant / établissement / jury : champs à compléter `[…]` sur la
> page de garde et la page jury — aucune donnée réelle dans le dépôt.

## Contenu

| Dossier / fichier | Description |
|---|---|
| `rapport/Rapport_PFE_Cleopatre.pdf` | **Livrable** — rapport final (117 p., signets + sommaire cliquable) |
| `rapport/build.py` + `content_*.py` + `doc.py` | Chaîne de génération du PDF (fpdf2, 4 passes) |
| `rapport/figs*.py` + `rapport/figs/` | 80+ figures vectorielles (matplotlib) — jamais de raster décoratif |
| `rapport/fonts/` | Newsreader (titres) + Manrope (texte) — statiques instanciés via fonttools |
| `soutenance/` | Diaporama de soutenance (`slides.py` → `.pptx`) |
| `PROMPT_MAITRE.md` | Prompt maître du projet |

Chiffres verrou : 24 récits (MoSCoW), 24 tables, 16 marques, 81 références,
7 univers, 4+1 sprints, 83 figures, 45 tableaux, 7 extraits de code.

## Reconstruire le rapport

```bash
cd rapport
python -m venv .venv && source .venv/bin/activate
pip install fpdf2 matplotlib pillow fonttools pymupdf
python build.py   # → Rapport_PFE_Cleopatre.pdf
```

## Captures AVANT (à insérer par l'auteur)

Le § V.3 réserve 6 cadres `[CAPTURE À INSÉRER]` (ancien site, format 16:9) :
aucune fausse capture n'est générée — l'auteur y colle ses propres copies
d'écran avant impression.
