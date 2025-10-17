# Supermarcher

🏪 Application de Gestion de Supermarché — Module Gestion des Stocks
📘 Description du Projet

Ce projet vise à développer une application de gestion intégrée destinée aux supermarchés de grande envergure (ex. Carrefour).
L’objectif principal est de centraliser et automatiser les opérations clés, notamment la gestion des stocks, des caisses, des ressources humaines et de la relation client (CRM).

La première phase de développement porte sur le module de gestion des stocks, qui constitue le cœur logistique du système. Ce module permettra de suivre les produits, de gérer les fournisseurs, d’anticiper les ruptures de stock et d’optimiser les approvisionnements.


🧭 Objectif Principal du Module

Assurer une gestion intelligente et automatisée des stocks, réduisant les ruptures, les surstocks et les pertes de produits périssables tout en optimisant les coûts de stockage.


🎯 Objectifs Spécifiques

Suivre en temps réel les niveaux de stock par produit, catégorie et entrepôt.

Automatiser les alertes de réapprovisionnement selon des seuils prédéfinis.

Gérer les fournisseurs, les commandes et les livraisons.

Générer des rapports sur l’état des stocks, la rotation des produits et les prévisions de demande.

Faciliter les décisions stratégiques à travers un tableau de bord analytique.


🧩 Fonctionnalités Principales

🔹 1. Suivi en Temps Réel

Visualisation instantanée des produits disponibles.

Affichage des quantités restantes, dates de péremption et emplacements.

Synchronisation automatique avec le module des ventes pour ajuster les stocks.


🔹 2. Réapprovisionnement Automatique

Notification lorsqu’un seuil critique est atteint.

Suggestion de commande basée sur l’historique de la demande.

Validation manuelle ou automatique des commandes auprès des fournisseurs.


🔹 3. Gestion des Fournisseurs

Enregistrement complet des informations fournisseurs (coordonnées, délais, tarifs).

Historique des transactions et évaluation de la fiabilité des fournisseurs.


🔹 4. Rapports et Tableaux de Bord

Visualisation des tendances de consommation.

Graphiques sur les produits les plus/moins vendus.

Indicateurs de performance (taux de rotation, valeur du stock, pertes).


🔹 5. Historisation et Traçabilité

Enregistrement de toutes les opérations (entrée, sortie, ajustement).

Suivi des mouvements de stock par utilisateur et par date.

| Composant                          | Technologie                           |
| ---------------------------------- | ------------------------------------- |
| **Back-end**                       | Django (Python) ou Spring Boot (Java) |
| **Front-end**                      | React.js ou Angular                   |
| **Base de Données**                | PostgreSQL ou MySQL                   |
| **API**                            | RESTful                               |
| **Sécurité**                       | OAuth2 / JWT                          |
| **Interface Mobile (optionnelle)** | Flutter ou React Native               |


🧮 Modèle de Données (exemple simplifié)
Entités principales :

Produit → (id, nom, catégorie, prix_unitaire, quantité_stock, seuil_minimum, date_péremption, fournisseur_id)

Fournisseur → (id, nom, adresse, contact, email)

CommandeFournisseur → (id, date_commande, produit_id, quantité_commandée, statut, date_livraison)

HistoriqueStock → (id, produit_id, type_mouvement, quantité, date_operation, utilisateur)



🧠 Exemple de Scénario Fonctionnel

Scénario : Réapprovisionnement automatique

Le responsable des stocks reçoit une alerte indiquant que le stock de farine T45 est bas (50 unités restantes, seuil : 100).
L’application suggère de commander 500 unités en se basant sur les ventes passées lors des fêtes.
Le responsable valide la commande, et le système envoie automatiquement la requête au fournisseur via l’API.



⚙️ Méthodologie de Développement

Approche Agile (Scrum) : développement itératif par modules.

Sprints de 2 à 3 semaines.

Livrables à chaque sprint : maquette + module fonctionnel + tests unitaires.

Tests automatisés avec PyTest / JUnit selon la stack choisie.


## 📁 Structure du projet

```plaintext
mon_app/
│
├── lib/
│   ├── core/                         # Composants communs à toute l’application
│   │   ├── utils/                    # Fonctions utilitaires (formatage, helpers...)
│   │   ├── widgets/                  # Widgets réutilisables (boutons, inputs...)
│   │   ├── theme/                    # Styles globaux : couleurs, typographie...
│   │   └── services/                 # Services globaux : Auth, API, Database...
│   │
│   ├── modules/                      # Chaque fonctionnalité de l’app = un module
│   │   ├── stock/                    # Module de gestion des stocks
│   │   │   ├── models/               # Classes de données (Product, Category...)
│   │   │   ├── pages/                # Interfaces (Liste, Formulaire…)
│   │   │   ├── controllers/          # Logique métier / gestion d’état
│   │   │   └── services/             # Accès aux données (BDD, API…)
│   │   │
│   │   ├── employees/                # Module gestion des employés
│   │   └── ventes/                   # Module gestion des ventes
│   │
│   ├── app.dart                      # Configuration globale de l'application
│   └── main.dart                     # Point d'entrée principal
│
├── assets/                           # Images, icônes, polices...
├── database/                        # Scripts SQL, migrations, seeds
├── docs/                            # Documentation technique et fonctionnelle
└── README.md                        # Guide principal du projet



📊 Indicateurs Clés de Performance (KPI)

Taux de rupture de stock (%)

Taux de rotation des produits

Valeur totale du stock

Taux d’automatisation des commandes

Temps moyen de traitement d’une commande fournisseur



🧰 Outils et Ressources

IDE : Visual Studio Code

Gestion de version : Git & GitHub

Base de données : PostgreSQL

Outils UML : StarUML
Serveur de test : Localhost



🚀 Livrables du Module

Code source complet du module “Gestion des Stocks”.

Base de données fonctionnelle (fichier SQL).

Documentation technique (API, modèles, endpoints).

Manuel utilisateur.

Rapport de tests.



🧾 Auteurs & Encadrement

Étudiant Développeur : @volbis @Linda @Déric @yezkélou

Encadrant : Dr. KOPOIN N'DIFFON Charlemagne

Établissement : ESATIC

Année académique : 2025–2026