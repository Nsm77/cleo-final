# Conclusion générale, Bibliographie, Résumé, Abréviations
FIN = [
    ("h1", "Conclusion générale"),
    ("p", "Au terme de ce Projet de Fin d'Études, l'objectif fixé avec la parapharmacie Cléopâtre est atteint : la maison dispose désormais d'une **plateforme e-commerce complète et fonctionnelle**, accessible en ligne, administrée au quotidien et déployée de façon reproductible. Le chemin parcouru, du cadrage Scrum à la conteneurisation Docker, mérite un bilan en trois temps : ce qui a été livré, ce qui a été appris, et ce qui reste à construire."),
    ("p", "Sur le plan **fonctionnel**, les 24 récits du backlog sont terminés et démontrés : site marchand (catalogue de 81 références en 7 univers et 16 marques, recherche à facettes, panier, tunnel de commande, paiement à la livraison, compte client, suivi invité sécurisé, journal), back-office (tableau de bord, commandes, catalogue, stock, promotions, avis, support, recherches, journal, boutiques, audit, exports) et industrialisation (Docker, seed, documentation). Sur le plan **qualité**, les huit besoins non fonctionnels sont couverts : sécurité (scrypt, sessions httpOnly, Zod, quotas), fiabilité (millimes, transactions, verrous, idempotence), performance (rendu serveur, pagination, index), ergonomie (« quiet luxury », mobile d'abord), traçabilité (timelines, mouvements, audit) et confidentialité (clé invitée de 256 bits)."),
    ("p", "Sur le plan **personnel et méthodologique**, ce projet a été une école complète du développement full-stack moderne : modélisation UML rigoureuse, découpage agile en sprints livrables, code TypeScript strict partagé entre client et serveur, persistance relationnelle exigeante (contraintes, index partiels, verrous), et culture de la revue (démonstrations, feedback, rétrospectives). La contrainte la plus formatrice fut la **fiabilité de l'argent et des stocks** : concevoir des transactions idempotentes et des quotas inviolables oblige à penser en termes de concurrence et de pannes, bien au-delà du « chemin heureux » des tutoriels."),
    ("p", "Les **perspectives** s'ordonnent en trois horizons. À court terme : le paiement par carte bancaire en ligne (via un prestataire tunisien agréé, avec 3-D Secure), la notification SMS des statuts, et l'application des retours clients de la recette. À moyen terme : la version arabe (RTL) — la structure internationalisée est prête —, un programme de fidélité complet (conversion des points), et l'ouverture d'un troisième point de retrait. À long terme : la recommandation personnalisée (« les clientes ayant acheté… »), l'abonnement (cures, protections solaires saisonnières) et l'interconnexion avec la comptabilité. La plateforme, par son architecture modulaire et sa documentation, est prête à accueillir ces évolutions : ce PFE en est le socle, pas le plafond."),
]

BIBLIO = [
    ("h1", "Bibliographie & Webographie"),
    ("p", "Les références ci-dessous ont nourri la conception et la réalisation : documentation officielle des technologies employées, ouvrages et ressources méthodologiques (UML, Scrum), et références métier (e-commerce, sécurité des applications web)."),
    ("bullets", [
        "Vercel — **Documentation Next.js 16 (App Router, Server Actions, mise en cache)**. https://nextjs.org/docs",
        "Meta / React — **Documentation React 19 (composants serveur, hooks)**. https://react.dev",
        "Microsoft — **Documentation TypeScript (manuel, strict mode)**. https://www.typescriptlang.org/docs",
        "Tailwind Labs — **Documentation Tailwind CSS**. https://tailwindcss.com/docs",
        "PostgreSQL Global Development Group — **Documentation PostgreSQL 18 (transactions, verrous, index)**. https://www.postgresql.org/docs",
        "Drizzle Team — **Documentation Drizzle ORM (schémas, requêtes, migrations)**. https://orm.drizzle.team/docs",
        "Colin McDonnell — **Documentation Zod (validation par schémas)**. https://zod.dev",
        "Docker Inc. — **Documentation Docker (Dockerfile multi-stage, Compose)**. https://docs.docker.com",
        "Schwaber, K. & Sutherland, J. — **Le Guide Scrum** (dernière édition). https://scrumguides.org",
        "OMG — **Spécification UML 2 (cas d'utilisation, classes, séquences, déploiement)**. https://www.omg.org/spec/UML",
        "OWASP — **Top 10 des risques applicatifs web & Cheat Sheets (sessions, validation, quotas)**. https://owasp.org",
        "Percival, C. — **Stronger Key Derivation via Sequential Memory-Hard Functions (scrypt)**. BSDCan 2009.",
        "Fielding, R. — **Architectural Styles and the Design of Network-based Software Architectures** (thèse REST, 2000) — pour la culture des styles d'API.",
        "Fowler, M. — **Patterns of Enterprise Application Architecture** (transactions, Unit of Work, Money pattern). Addison-Wesley.",
        "INS (Tunisie) & APII — **Statistiques du commerce électronique et du paiement en Tunisie** (contexte marché).",
    ]),
]

RESUME = [
    ("h1", "Résumé"),
    ("p", "**Résumé.** — Ce rapport présente la conception et la réalisation d'une plateforme e-commerce pour la parapharmacie tunisienne Cléopâtre (Ezzahra, Hammam-Lif), dans le cadre d'un Projet de Fin d'Études conduit selon la méthode agile Scrum (un sprint 0, quatre sprints en deux releases). La plateforme comprend un site marchand (catalogue de 81 références en 7 univers, recherche à facettes, panier, tunnel de commande, paiement à la livraison, compte client, suivi invité sécurisé) et un back-office complet (tableau de bord, commandes, catalogue, stock, promotions, avis, support, journal, audit). Réalisée en Next.js 16, React 19, TypeScript et PostgreSQL 18 (Drizzle ORM, Zod, Docker), elle applique des exigences fortes : montants en millimes, mots de passe scrypt, sessions httpOnly, validation serveur, transactions verrouillées, commandes idempotentes. Le rapport détaille, sprint par sprint, l'analyse (cas d'utilisation), la conception (classes, séquences) et la réalisation (86 figures, 32 tableaux), et s'achève sur un bilan et des perspectives (paiement en ligne, version arabe, recommandation)."),
    ("p", "**Mots-clés :** e-commerce, parapharmacie, Scrum, Next.js, TypeScript, PostgreSQL, UML, transactions, idempotence, Docker."),
    ("p", "**Abstract.** — This report presents the design and implementation of an e-commerce platform for the Tunisian parapharmacy Cléopâtre (Ezzahra, Hammam-Lif), as a graduation project conducted with the Scrum agile method (one sprint 0, four sprints in two releases). The platform includes a storefront (81-product catalog across 7 universes, faceted search, cart, checkout flow, cash on delivery, customer account, secured guest tracking) and a full back-office (dashboard, orders, catalog, inventory, promotions, reviews, support, journal, audit). Built with Next.js 16, React 19, TypeScript and PostgreSQL 18 (Drizzle ORM, Zod, Docker), it enforces strong guarantees: integer millimes, scrypt hashing, httpOnly sessions, server-side validation, locked transactions, idempotent orders. The report details, sprint by sprint, analysis (use cases), design (class and sequence diagrams) and implementation (86 figures, 32 tables), and closes with an assessment and outlook (online payment, Arabic version, recommendations)."),
    ("p", "**Keywords:** e-commerce, parapharmacy, Scrum, Next.js, TypeScript, PostgreSQL, UML, transactions, idempotency, Docker."),
]

ABBR = [
    ["PFE", "Projet de Fin d'Études"],
    ["UML", "Unified Modeling Language (langage de modélisation unifié)"],
    ["API", "Application Programming Interface (interface de programmation)"],
    ["ORM", "Object-Relational Mapping (Drizzle : correspondance objet-relationnel)"],
    ["SSR", "Server-Side Rendering (rendu côté serveur)"],
    ["SQL", "Structured Query Language (langage de requêtes)"],
    ["ACID", "Atomicité, Cohérence, Isolation, Durabilité (propriétés des transactions)"],
    ["CRUD", "Create, Read, Update, Delete (opérations de base)"],
    ["COD", "Cash On Delivery (paiement à la livraison)"],
    ["SKU", "Stock Keeping Unit (référence produit)"],
    ["DT", "Dinar tunisien (1 DT = 1 000 millimes)"],
    ["SPF", "Sun Protection Factor (indice de protection solaire)"],
    ["CSV", "Comma-Separated Values (format d'export tableur)"],
    ["HTTPS", "HyperText Transfer Protocol Secure (HTTP chiffré)"],
    ["CSRF", "Cross-Site Request Forgery (attaque par requête contrefaite)"],
    ["RBAC", "Role-Based Access Control (contrôle d'accès par rôles)"],
    ["RTL", "Right-To-Left (écriture de droite à gauche, arabe)"],
    ["SEO", "Search Engine Optimization (référencement naturel)"],
    ["UI / UX", "User Interface / User Experience (interface / expérience utilisateur)"],
    ["TPE", "Terminal de Paiement Électronique"],
]
