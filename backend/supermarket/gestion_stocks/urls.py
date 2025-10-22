"""
Configuration des URLs pour l'API de gestion de stock.

Ce fichier configure tous les endpoints de l'API REST en utilisant
un routeur Django REST Framework pour la génération automatique des URLs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategorieViewSet,
    FournisseurViewSet,
    ProduitViewSet,
    StockViewSet,
    CommandeApprovisionnementViewSet,
    DetailCommandeViewSet,
    AlertStockViewSet,
    HistoriqueStockViewSet,
    ResponsableStockViewSet,
    HistoriqueVenteViewSet
)

# ============================================================================
# Configuration du routeur pour la génération automatique des URLs
# ============================================================================
router = DefaultRouter()

# Enregistrement des ViewSets principaux
router.register(r'categories', CategorieViewSet, basename='categorie')
router.register(r'fournisseurs', FournisseurViewSet, basename='fournisseur')
router.register(r'produits', ProduitViewSet, basename='produit')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'commandes', CommandeApprovisionnementViewSet, basename='commande')
router.register(r'details-commandes', DetailCommandeViewSet, basename='detail-commande')
router.register(r'alertes', AlertStockViewSet, basename='alerte')
router.register(r'historique-stock', HistoriqueStockViewSet, basename='historique-stock')
router.register(r'responsables', ResponsableStockViewSet, basename='responsable')
router.register(r'historique-ventes', HistoriqueVenteViewSet, basename='historique-vente')

# ============================================================================
# Pattern URLs
# ============================================================================
"""
Structure générale des URLs :

API_ROOT: /api/

CATEGORIES:
  GET     /api/categories/                      - Lister tous les catégories
  POST    /api/categories/                      - Créer une catégorie
  GET     /api/categories/{id}/                 - Détails d'une catégorie
  PUT     /api/categories/{id}/                 - Mettre à jour une catégorie
  DELETE  /api/categories/{id}/                 - Supprimer une catégorie
  GET     /api/categories/{id}/produits/        - Produits d'une catégorie

FOURNISSEURS:
  GET     /api/fournisseurs/                    - Lister tous les fournisseurs
  POST    /api/fournisseurs/                    - Créer un fournisseur
  GET     /api/fournisseurs/{id}/               - Détails d'un fournisseur
  PUT     /api/fournisseurs/{id}/               - Mettre à jour un fournisseur
  DELETE  /api/fournisseurs/{id}/               - Supprimer un fournisseur
  GET     /api/fournisseurs/{id}/produits/      - Produits fournis
  GET     /api/fournisseurs/{id}/prix/          - Obtenir le prix d'un produit

PRODUITS:
  GET     /api/produits/                        - Lister tous les produits
  POST    /api/produits/                        - Créer un produit
  GET     /api/produits/{id}/                   - Détails d'un produit
  PUT     /api/produits/{id}/                   - Mettre à jour un produit
  DELETE  /api/produits/{id}/                   - Supprimer un produit
  GET     /api/produits/sous-seuil/list/        - Produits sous seuil
  GET     /api/produits/perimés/list/           - Produits périmés
  GET     /api/produits/atteint-seuil/list/     - Produits au seuil
  POST    /api/produits/{id}/incrementer-stock/ - Augmenter stock
  POST    /api/produits/{id}/decrementer-stock/ - Diminuer stock

STOCKS:
  GET     /api/stocks/                          - Lister tous les stocks
  POST    /api/stocks/                          - Créer un stock
  GET     /api/stocks/{id}/                     - Détails d'un stock
  PUT     /api/stocks/{id}/                     - Mettre à jour un stock
  DELETE  /api/stocks/{id}/                     - Supprimer un stock
  POST    /api/stocks/{id}/ajouter/             - Ajouter une quantité
  POST    /api/stocks/{id}/retirer/             - Retirer une quantité

COMMANDES D'APPROVISIONNEMENT:
  GET     /api/commandes/                       - Lister toutes les commandes
  POST    /api/commandes/                       - Créer une commande
  GET     /api/commandes/{id}/                  - Détails d'une commande
  PUT     /api/commandes/{id}/                  - Mettre à jour une commande
  DELETE  /api/commandes/{id}/                  - Supprimer une commande
  GET     /api/commandes/en-cours/list/         - Commandes en cours
  GET     /api/commandes/livrees/list/          - Commandes livrées
  GET     /api/commandes/annulees/list/         - Commandes annulées
  POST    /api/commandes/{id}/valider/          - Valider une commande
  POST    /api/commandes/{id}/annuler/          - Annuler une commande

DETAILS DE COMMANDES:
  GET     /api/details-commandes/               - Lister tous les détails
  POST    /api/details-commandes/               - Créer un détail
  GET     /api/details-commandes/{id}/          - Détails d'une ligne
  PUT     /api/details-commandes/{id}/          - Mettre à jour une ligne
  DELETE  /api/details-commandes/{id}/          - Supprimer une ligne

ALERTES DE STOCK:
  GET     /api/alertes/                         - Lister toutes les alertes
  POST    /api/alertes/                         - Créer une alerte
  GET     /api/alertes/{id}/                    - Détails d'une alerte
  PUT     /api/alertes/{id}/                    - Mettre à jour une alerte
  DELETE  /api/alertes/{id}/                    - Supprimer une alerte
  GET     /api/alertes/par-produit/list/        - Alertes par produit

HISTORIQUE STOCK:
  GET     /api/historique-stock/                - Lister tout l'historique
  GET     /api/historique-stock/{id}/           - Détails d'une entrée
  GET     /api/historique-stock/par-produit/list/ - Historique d'un produit
  GET     /api/historique-stock/ajouts/list/    - Historique des ajouts
  GET     /api/historique-stock/retraits/list/  - Historique des retraits

RESPONSABLES DE STOCK:
  GET     /api/responsables/                    - Lister tous les responsables
  POST    /api/responsables/                    - Créer un responsable
  GET     /api/responsables/{id}/               - Détails d'un responsable
  PUT     /api/responsables/{id}/               - Mettre à jour un responsable
  DELETE  /api/responsables/{id}/               - Supprimer un responsable
  POST    /api/responsables/{id}/valider-commande/ - Valider une commande
  GET     /api/responsables/{id}/rapport-inventaire/ - Rapport d'inventaire

HISTORIQUE VENTES:
  GET     /api/historique-ventes/               - Lister tout l'historique
  GET     /api/historique-ventes/{id}/          - Détails d'une vente
  GET     /api/historique-ventes/par-produit/list/ - Ventes d'un produit
  GET     /api/historique-ventes/statistiques-chiffre-affaires/list/ - Stats
  GET     /api/historique-ventes/par-periode/list/ - Ventes par période
"""

# Intégration des URLs du routeur
urlpatterns = [
    path('api/', include(router.urls)),
]
