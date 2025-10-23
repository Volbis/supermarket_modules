from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Sum, F
from .models import (
    Produit, Categorie, Stock, Fournisseur, CommandeApprovisionnement,
    DetailCommande, AlertStock, HistoriqueStock, ResponsableStock, HistoriqueVente
)
from .serializers import (
    ProduitSerializer, CategorieSerializer, StockSerializer, FournisseurSerializer,
    CommandeApprovisionnementSerializer, DetailCommandeSerializer, AlertStockSerializer,
    HistoriqueStockSerializer, ResponsableStockSerializer, HistoriqueVenteSerializer
)


class CategorieViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les catégories de produits.
    
    Endpoints:
    - GET /api/categories/ : Lister toutes les catégories
    - POST /api/categories/ : Créer une nouvelle catégorie
    - GET /api/categories/{id}/ : Récupérer une catégorie
    - PUT /api/categories/{id}/ : Mettre à jour une catégorie
    - DELETE /api/categories/{id}/ : Supprimer une catégorie
    - GET /api/categories/{id}/produits/ : Lister les produits d'une catégorie
    """
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]  # Modifié pour le développement
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom', 'description']
    ordering_fields = ['nom']
    ordering = ['nom']

    @action(detail=True, methods=['get'])
    def produits(self, request, pk=None):
        """
        Action personnalisée pour récupérer tous les produits d'une catégorie.
        GET /api/categories/{id}/produits/
        """
        categorie = self.get_object()
        produits = categorie.getProduits()
        serializer = ProduitSerializer(produits, many=True)
        return Response({
            'categorie': categorie.nom,
            'nombre_produits': produits.count(),
            'produits': serializer.data
        })


class FournisseurViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les fournisseurs.
    
    Endpoints:
    - GET /api/fournisseurs/ : Lister tous les fournisseurs
    - POST /api/fournisseurs/ : Créer un nouveau fournisseur
    - GET /api/fournisseurs/{id}/ : Récupérer un fournisseur
    - PUT /api/fournisseurs/{id}/ : Mettre à jour un fournisseur
    - DELETE /api/fournisseurs/{id}/ : Supprimer un fournisseur
    - GET /api/fournisseurs/{id}/produits/ : Lister les produits fournis
    - GET /api/fournisseurs/{id}/prix/ : Obtenir le prix d'un produit
    """
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom', 'contact', 'adresse']
    ordering_fields = ['nom', 'delais_livraison_jours']

    @action(detail=True, methods=['get'])
    def produits(self, request, pk=None):
        """
        Action pour récupérer tous les produits fournis par ce fournisseur.
        GET /api/fournisseurs/{id}/produits/
        """
        fournisseur = self.get_object()
        produits = fournisseur.getProduitsFournis()
        serializer = ProduitSerializer(produits, many=True)
        return Response({
            'fournisseur': fournisseur.nom,
            'nombre_produits': produits.count(),
            'produits': serializer.data
        })

    @action(detail=True, methods=['get'])
    def prix(self, request, pk=None):
        """
        Action pour obtenir le prix d'un produit chez ce fournisseur.
        GET /api/fournisseurs/{id}/prix/?produit_id={produit_id}
        """
        fournisseur = self.get_object()
        produit_id = request.query_params.get('produit_id')
        
        if not produit_id:
            return Response(
                {'erreur': 'Le paramètre produit_id est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            produit = Produit.objects.get(id_product=produit_id)
            prix = fournisseur.obtenirPrixProduit(produit)
            return Response({
                'fournisseur': fournisseur.nom,
                'produit': produit.nom,
                'prix_unitaire': prix
            })
        except Produit.DoesNotExist:
            return Response(
                {'erreur': 'Produit non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProduitViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les produits.
    
    Endpoints principaux:
    - GET /api/produits/ : Lister tous les produits
    - POST /api/produits/ : Créer un nouveau produit
    - GET /api/produits/{id}/ : Récupérer un produit
    - PUT /api/produits/{id}/ : Mettre à jour un produit
    - DELETE /api/produits/{id}/ : Supprimer un produit
    
    Actions personnalisées:
    - GET /api/produits/sous-seuil/list/ : Lister les produits sous le seuil
    - GET /api/produits/perimés/list/ : Lister les produits périmés
    - POST /api/produits/{id}/incrementer-stock/ : Augmenter le stock
    - POST /api/produits/{id}/decrementer-stock/ : Diminuer le stock
    """
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categorie', 'fournisseur']
    search_fields = ['nom', 'reference', 'designation']
    ordering_fields = ['nom', 'prix_unitaire', 'quantite_en_stock', 'date_de_peremption']
    ordering = ['nom']

    @action(detail=False, methods=['get'])
    def sous_seuil(self, request): 
        """
        Action pour récupérer tous les produits sous le seuil de réapprovisionnement.
        GET /api/produits/sous-seuil/list/
        """
        produits_sous_seuil = [p for p in self.queryset if p.estSousSeuil()]
        serializer = self.get_serializer(produits_sous_seuil, many=True)
        return Response({
            'nombre_produits': len(produits_sous_seuil),
            'produits': serializer.data
        })

    @action(detail=False, methods=['get'])
    def perimés(self, request):
        """
        Action pour récupérer tous les produits périmés.
        GET /api/produits/perimés/list/
        """
        produits_perimes = [p for p in self.queryset if p.estPerime()]
        serializer = self.get_serializer(produits_perimes, many=True)
        return Response({
            'nombre_produits': len(produits_perimes),
            'produits': serializer.data
        })

    @action(detail=False, methods=['get'])
    def atteint_seuil(self, request):
        """
        Action pour récupérer les produits qui atteignent exactement le seuil.
        GET /api/produits/atteint-seuil/list/
        """
        produits_seuil = [p for p in self.queryset if p.atteintSeuil()]
        serializer = self.get_serializer(produits_seuil, many=True)
        return Response({
            'nombre_produits': len(produits_seuil),
            'produits': serializer.data
        })

    @action(detail=True, methods=['post'])
    def incrementer_stock(self, request, pk=None):
        """
        Action pour augmenter le stock d'un produit.
        POST /api/produits/{id}/incrementer-stock/
        Body: {"quantite": 10}
        """
        produit = self.get_object()
        quantite = request.data.get('quantite')

        if quantite is None:
            return Response(
                {'erreur': 'Le champ quantite est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantite = int(quantite)
            if quantite <= 0:
                raise ValueError('La quantité doit être positive')
            
            produit.incrementerStock(quantite)
            
            # Créer un enregistrement dans l'historique
            HistoriqueStock.objects.create(
                produit=produit,
                quantite_modifiee=quantite,
                type_modification='AJOUT'
            )

            return Response({
                'message': f'Stock augmenté de {quantite}',
                'nouvelle_quantite': produit.quantite_en_stock
            }, status=status.HTTP_200_OK)
        except (ValueError, TypeError) as e:
            return Response(
                {'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def decrementer_stock(self, request, pk=None):
        """
        Action pour diminuer le stock d'un produit.
        POST /api/produits/{id}/decrementer-stock/
        Body: {"quantite": 5}
        """
        produit = self.get_object()
        quantite = request.data.get('quantite')

        if quantite is None:
            return Response(
                {'erreur': 'Le champ quantite est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantite = int(quantite)
            if quantite <= 0:
                raise ValueError('La quantité doit être positive')
            if quantite > produit.quantite_en_stock:
                return Response(
                    {'erreur': f'Quantité insuffisante. Stock disponible: {produit.quantite_en_stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            produit.decrementerStock(quantite)
            
            # Créer un enregistrement dans l'historique
            HistoriqueStock.objects.create(
                produit=produit,
                quantite_modifiee=quantite,
                type_modification='RETRAIT'
            )

            return Response({
                'message': f'Stock diminué de {quantite}',
                'nouvelle_quantite': produit.quantite_en_stock
            }, status=status.HTTP_200_OK)
        except (ValueError, TypeError) as e:
            return Response(
                {'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class StockViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les stocks.
    
    Endpoints:
    - GET /api/stocks/ : Lister tous les stocks
    - POST /api/stocks/ : Créer un nouveau stock
    - GET /api/stocks/{id}/ : Récupérer un stock
    - PUT /api/stocks/{id}/ : Mettre à jour un stock
    - DELETE /api/stocks/{id}/ : Supprimer un stock
    - POST /api/stocks/{id}/ajouter/ : Ajouter une quantité
    - POST /api/stocks/{id}/retirer/ : Retirer une quantité
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['produit']
    ordering_fields = ['quantite', 'date_ajout', 'date_modification']
    ordering = ['-date_modification']

    @action(detail=True, methods=['post'])
    def ajouter(self, request, pk=None):
        """
        Action pour ajouter une quantité au stock.
        POST /api/stocks/{id}/ajouter/
        Body: {"quantite": 20}
        """
        stock = self.get_object()
        quantite = request.data.get('quantite')

        try:
            quantite = int(quantite)
            if quantite <= 0:
                raise ValueError('La quantité doit être positive')
            
            stock.ajouterStock(quantite)
            serializer = self.get_serializer(stock)
            return Response({
                'message': 'Stock ajouté avec succès',
                'stock': serializer.data
            }, status=status.HTTP_200_OK)
        except (ValueError, TypeError) as e:
            return Response(
                {'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def retirer(self, request, pk=None):
        """
        Action pour retirer une quantité du stock.
        POST /api/stocks/{id}/retirer/
        Body: {"quantite": 10}
        """
        stock = self.get_object()
        quantite = request.data.get('quantite')

        try:
            quantite = int(quantite)
            if quantite <= 0:
                raise ValueError('La quantité doit être positive')
            
            stock.retirerStock(quantite)
            serializer = self.get_serializer(stock)
            return Response({
                'message': 'Stock retiré avec succès',
                'stock': serializer.data
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CommandeApprovisionnementViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commandes d'approvisionnement.
    
    Endpoints:
    - GET /api/commandes/ : Lister toutes les commandes
    - POST /api/commandes/ : Créer une nouvelle commande
    - GET /api/commandes/{id}/ : Récupérer une commande
    - PUT /api/commandes/{id}/ : Mettre à jour une commande
    - DELETE /api/commandes/{id}/ : Supprimer une commande
    - GET /api/commandes/statut/en-cours/ : Commandes en cours
    - GET /api/commandes/{id}/valider/ : Valider une commande
    - GET /api/commandes/{id}/annuler/ : Annuler une commande
    """
    queryset = CommandeApprovisionnement.objects.all()
    serializer_class = CommandeApprovisionnementSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['fournisseur', 'statut']
    ordering_fields = ['date_commande', 'date_livraison_prevue', 'statut']
    ordering = ['-date_commande']

    @action(detail=False, methods=['get'])
    def en_cours(self, request):
        """
        Action pour récupérer les commandes en cours.
        GET /api/commandes/en-cours/list/
        """
        commandes = self.queryset.filter(statut='EN_COURS')
        serializer = self.get_serializer(commandes, many=True)
        return Response({
            'nombre_commandes': commandes.count(),
            'commandes': serializer.data
        })

    @action(detail=False, methods=['get'])
    def livrees(self, request):
        """
        Action pour récupérer les commandes livrées.
        GET /api/commandes/livrees/list/
        """
        commandes = self.queryset.filter(statut='LIVREE')
        serializer = self.get_serializer(commandes, many=True)
        return Response({
            'nombre_commandes': commandes.count(),
            'commandes': serializer.data
        })

    @action(detail=False, methods=['get'])
    def annulees(self, request):
        """
        Action pour récupérer les commandes annulées.
        GET /api/commandes/annulees/list/
        """
        commandes = self.queryset.filter(statut='ANNULEE')
        serializer = self.get_serializer(commandes, many=True)
        return Response({
            'nombre_commandes': commandes.count(),
            'commandes': serializer.data
        })

    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        """
        Action pour valider une commande (changer le statut à LIVREE).
        POST /api/commandes/{id}/valider/
        """
        commande = self.get_object()
        try:
            commande.valider()
            serializer = self.get_serializer(commande)
            return Response({
                'message': 'Commande validée avec succès',
                'commande': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """
        Action pour annuler une commande.
        POST /api/commandes/{id}/annuler/
        """
        commande = self.get_object()
        try:
            commande.annuler()
            serializer = self.get_serializer(commande)
            return Response({
                'message': 'Commande annulée avec succès',
                'commande': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class DetailCommandeViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les détails des commandes d'approvisionnement.
    
    Endpoints:
    - GET /api/details-commandes/ : Lister tous les détails
    - POST /api/details-commandes/ : Créer un nouveau détail
    - GET /api/details-commandes/{id}/ : Récupérer un détail
    - PUT /api/details-commandes/{id}/ : Mettre à jour un détail
    - DELETE /api/details-commandes/{id}/ : Supprimer un détail
    """
    queryset = DetailCommande.objects.all()
    serializer_class = DetailCommandeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['commande', 'produit']
    ordering_fields = ['quantite', 'produit__prix_unitaire']
    ordering = ['-commande__date_commande']


class AlertStockViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les alertes de stock.
    
    Endpoints:
    - GET /api/alertes/ : Lister toutes les alertes
    - POST /api/alertes/ : Créer une nouvelle alerte
    - GET /api/alertes/{id}/ : Récupérer une alerte
    - PUT /api/alertes/{id}/ : Mettre à jour une alerte
    - DELETE /api/alertes/{id}/ : Supprimer une alerte
    - GET /api/alertes/non-lues/list/ : Lister les alertes non lues
    """
    queryset = AlertStock.objects.all()
    serializer_class = AlertStockSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['produit']
    search_fields = ['message', 'produit__nom']
    ordering_fields = ['date_creation']
    ordering = ['-date_creation']

    @action(detail=False, methods=['get'])
    def par_produit(self, request):
        """
        Action pour récupérer les alertes groupées par produit.
        GET /api/alertes/par-produit/list/
        """
        produit_id = request.query_params.get('produit_id')
        
        if produit_id:
            alertes = self.queryset.filter(produit_id=produit_id)
        else:
            alertes = self.queryset.all()
        
        serializer = self.get_serializer(alertes, many=True)
        return Response({
            'nombre_alertes': alertes.count(),
            'alertes': serializer.data
        })


class HistoriqueStockViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer l'historique des modifications de stock.
    
    Endpoints:
    - GET /api/historique-stock/ : Lister tout l'historique
    - POST /api/historique-stock/ : Créer un nouvel enregistrement
    - GET /api/historique-stock/{id}/ : Récupérer un enregistrement
    - PUT /api/historique-stock/{id}/ : Modifier un enregistrement
    - DELETE /api/historique-stock/{id}/ : Supprimer un enregistrement
    - GET /api/historique-stock/produit/detail/ : Historique d'un produit
    - GET /api/historique-stock/type/ajouts/ : Historique des ajouts
    - GET /api/historique-stock/type/retraits/ : Historique des retraits
    """
    queryset = HistoriqueStock.objects.all()
    serializer_class = HistoriqueStockSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['produit', 'type_modification']
    ordering_fields = ['date_modification', 'quantite_modifiee']
    ordering = ['-date_modification']

    @action(detail=False, methods=['get'])
    def par_produit(self, request):
        """
        Action pour récupérer l'historique d'un produit spécifique.
        GET /api/historique-stock/par-produit/list/?produit_id={produit_id}
        """
        produit_id = request.query_params.get('produit_id')
        
        if not produit_id:
            return Response(
                {'erreur': 'Le paramètre produit_id est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            produit = Produit.objects.get(id_product=produit_id)
            historique = self.queryset.filter(produit=produit)
            serializer = self.get_serializer(historique, many=True)
            
            # Calculer les statistiques
            total_ajouts = sum(h.quantite_modifiee for h in historique if h.type_modification == 'AJOUT')
            total_retraits = sum(h.quantite_modifiee for h in historique if h.type_modification == 'RETRAIT')
            
            return Response({
                'produit': produit.nom,
                'nombre_operations': historique.count(),
                'total_ajouts': total_ajouts,
                'total_retraits': total_retraits,
                'bilan_net': total_ajouts - total_retraits,
                'historique': serializer.data
            })
        except Produit.DoesNotExist:
            return Response(
                {'erreur': 'Produit non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def ajouts(self, request):
        """
        Action pour récupérer uniquement les ajouts de stock.
        GET /api/historique-stock/ajouts/list/
        """
        historique = self.queryset.filter(type_modification='AJOUT')
        serializer = self.get_serializer(historique, many=True)
        total = sum(h.quantite_modifiee for h in historique)
        
        return Response({
            'nombre_operations': historique.count(),
            'total_quantite': total,
            'historique': serializer.data
        })

    @action(detail=False, methods=['get'])
    def retraits(self, request):
        """
        Action pour récupérer uniquement les retraits de stock.
        GET /api/historique-stock/retraits/list/
        """
        historique = self.queryset.filter(type_modification='RETRAIT')
        serializer = self.get_serializer(historique, many=True)
        total = sum(h.quantite_modifiee for h in historique)
        
        return Response({
            'nombre_operations': historique.count(),
            'total_quantite': total,
            'historique': serializer.data
        })


class ResponsableStockViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les responsables de stock.
    
    Endpoints:
    - GET /api/responsables/ : Lister tous les responsables
    - POST /api/responsables/ : Créer un nouveau responsable
    - GET /api/responsables/{id}/ : Récupérer un responsable
    - PUT /api/responsables/{id}/ : Mettre à jour un responsable
    - DELETE /api/responsables/{id}/ : Supprimer un responsable
    - POST /api/responsables/{id}/valider-commande/ : Valider une commande
    - GET /api/responsables/{id}/rapport-inventaire/ : Rapport d'inventaire
    """
    queryset = ResponsableStock.objects.all()
    serializer_class = ResponsableStockSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom', 'email', 'telephone']
    ordering_fields = ['nom', 'email']
    ordering = ['nom']

    @action(detail=True, methods=['post'])
    def valider_commande(self, request, pk=None):
        """
        Action pour valider une commande d'approvisionnement.
        POST /api/responsables/{id}/valider-commande/
        Body: {"commande_id": "uuid-de-la-commande"}
        """
        responsable = self.get_object()
        commande_id = request.data.get('commande_id')
        
        if not commande_id:
            return Response(
                {'erreur': 'Le champ commande_id est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            commande = CommandeApprovisionnement.objects.get(id_commande=commande_id)
            responsable.validerCommande(commande)
            serializer = CommandeApprovisionnementSerializer(commande)
            
            return Response({
                'message': f'Commande validée par {responsable.nom}',
                'commande': serializer.data
            }, status=status.HTTP_200_OK)
        except CommandeApprovisionnement.DoesNotExist:
            return Response(
                {'erreur': 'Commande non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def rapport_inventaire(self, request, pk=None):
        """
        Action pour obtenir le rapport d'inventaire du responsable.
        GET /api/responsables/{id}/rapport-inventaire/
        """
        responsable = self.get_object()
        rapport = responsable.consulterRapportInventaire()
        
        # Analyser le rapport
        total_produits = len(rapport)
        sous_seuil = sum(1 for p in rapport if p['est_sous_seuil'])
        perimes = sum(1 for p in rapport if p['est_perime'])
        
        return Response({
            'responsable': responsable.nom,
            'date_rapport': timezone.now().isoformat(),
            'statistiques': {
                'total_produits': total_produits,
                'produits_sous_seuil': sous_seuil,
                'produits_perimes': perimes,
                'produits_ok': total_produits - sous_seuil - perimes
            },
            'rapport_detaille': rapport
        })


class HistoriqueVenteViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer l'historique des ventes.
    
    Endpoints:
    - GET /api/historique-ventes/ : Lister tout l'historique
    - POST /api/historique-ventes/ : Créer une nouvelle vente
    - GET /api/historique-ventes/{id}/ : Récupérer une vente
    - PUT /api/historique-ventes/{id}/ : Modifier une vente
    - DELETE /api/historique-ventes/{id}/ : Supprimer une vente
    - GET /api/historique-ventes/par-produit/detail/ : Ventes d'un produit
    - GET /api/historique-ventes/par-periode/detail/ : Ventes sur une période
    - GET /api/historique-ventes/statistiques/chiffre-affaires/ : Chiffre d'affaires
    """
    queryset = HistoriqueVente.objects.all()
    serializer_class = HistoriqueVenteSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['produit']
    ordering_fields = ['date_vente', 'montant_total', 'quantite_vendue']
    ordering = ['-date_vente']

    @action(detail=False, methods=['get'])
    def par_produit(self, request):
        """
        Action pour récupérer les ventes d'un produit spécifique.
        GET /api/historique-ventes/par-produit/list/?produit_id={produit_id}
        """
        produit_id = request.query_params.get('produit_id')
        
        if not produit_id:
            return Response(
                {'erreur': 'Le paramètre produit_id est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            produit = Produit.objects.get(id_product=produit_id)
            ventes = self.queryset.filter(produit=produit)
            serializer = self.get_serializer(ventes, many=True)
            
            # Calculer les statistiques
            total_quantite = ventes.aggregate(Sum('quantite_vendue'))['quantite_vendue__sum'] or 0
            total_chiffre = ventes.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
            nombre_ventes = ventes.count()
            
            return Response({
                'produit': produit.nom,
                'reference': produit.reference,
                'statistiques': {
                    'nombre_ventes': nombre_ventes,
                    'total_quantite_vendue': total_quantite,
                    'total_chiffre_affaires': str(total_chiffre),
                    'moyenne_vente': str(total_chiffre / nombre_ventes) if nombre_ventes > 0 else 0
                },
                'ventes': serializer.data
            })
        except Produit.DoesNotExist:
            return Response(
                {'erreur': 'Produit non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def statistiques_chiffre_affaires(self, request):
        """
        Action pour obtenir les statistiques de chiffre d'affaires.
        GET /api/historique-ventes/statistiques-chiffre-affaires/list/
        """
        ventes = self.queryset.all()
        
        total_chiffre = ventes.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
        total_quantite = ventes.aggregate(Sum('quantite_vendue'))['quantite_vendue__sum'] or 0
        nombre_ventes = ventes.count()
        
        # Produit le plus vendu
        ventes_par_produit = (
            ventes.values('produit__nom', 'produit__reference')
            .annotate(total=Sum('quantite_vendue'))
            .order_by('-total')
            .first()
        )
        
        return Response({
            'date_rapport': timezone.now().isoformat(),
            'statistiques_globales': {
                'nombre_transactions': nombre_ventes,
                'quantite_totale_vendue': total_quantite,
                'chiffre_affaires_total': str(total_chiffre),
                'vente_moyenne': str(total_chiffre / nombre_ventes) if nombre_ventes > 0 else 0,
                'produit_plus_vendu': ventes_par_produit
            }
        })

    @action(detail=False, methods=['get'])
    def par_periode(self, request):
        """
        Action pour récupérer les ventes sur une période.
        GET /api/historique-ventes/par-periode/list/?date_debut=2024-01-01&date_fin=2024-12-31
        """
        date_debut = request.query_params.get('date_debut')
        date_fin = request.query_params.get('date_fin')
        
        if not date_debut or not date_fin:
            return Response(
                {'erreur': 'Les paramètres date_debut et date_fin sont obligatoires'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            ventes = self.queryset.filter(
                date_vente__date__gte=date_debut,
                date_vente__date__lte=date_fin
            )
            serializer = self.get_serializer(ventes, many=True)
            
            total_quantite = ventes.aggregate(Sum('quantite_vendue'))['quantite_vendue__sum'] or 0
            total_chiffre = ventes.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
            
            return Response({
                'periode': {
                    'debut': date_debut,
                    'fin': date_fin
                },
                'statistiques': {
                    'nombre_ventes': ventes.count(),
                    'total_quantite_vendue': total_quantite,
                    'total_chiffre_affaires': str(total_chiffre)
                },
                'ventes': serializer.data
            })
        except Exception as e:
            return Response(
                {'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )