from rest_framework import serializers
from .models import (
    Produit, Categorie, Stock, Fournisseur, CommandeApprovisionnement,
    DetailCommande, AlertStock, HistoriqueStock, ResponsableStock, HistoriqueVente
)


class CategorieSerializer(serializers.ModelSerializer):
    """
    Sérializeur pour le modèle Categorie.
    Gère la sérialisation et désérialisation des catégories de produits.
    """
    class Meta:
        model = Categorie
        fields = ['id_categorie', 'nom', 'description']
        read_only_fields = ['id_categorie']


class FournisseurSerializer(serializers.ModelSerializer):
    """
    Sérializeur pour le modèle Fournisseur.
    Gère les informations de base du fournisseur.
    """
    nombre_produits = serializers.SerializerMethodField()

    class Meta:
        model = Fournisseur
        fields = [
            'id_fournisseur', 'nom', 'contact', 'adresse',
            'catalogue_produits', 'delais_livraison_jours', 'nombre_produits'
        ]
        read_only_fields = ['id_fournisseur', 'nombre_produits']

    def get_nombre_produits(self, obj):
        """Retourne le nombre de produits fournis par ce fournisseur."""
        return obj.getProduitsFournis().count()


class ProduitSerializer(serializers.ModelSerializer):
    """
    Sérializeur pour le modèle Produit.
    Gère la sérialisation complète des produits avec détails des relations.
    """
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    est_sous_seuil = serializers.SerializerMethodField()
    est_perime = serializers.SerializerMethodField()
    atteint_seuil = serializers.SerializerMethodField()

    class Meta: 
        model = Produit
        fields = [
            'id_product', 'nom', 'reference', 'designation', 'prix_unitaire',
            'quantite_en_stock', 'seuil_de_reapprovisionnement',
            'date_de_peremption', 'categorie', 'fournisseur',
            'categorie_nom', 'fournisseur_nom', 'est_sous_seuil',
            'est_perime', 'atteint_seuil'
        ]
        read_only_fields = ['id_product', 'est_sous_seuil', 'est_perime', 'atteint_seuil']

    def get_est_sous_seuil(self, obj):
        """Vérifie si le produit est sous le seuil de réapprovisionnement."""
        return obj.estSousSeuil()

    def get_est_perime(self, obj):
        """Vérifie si le produit est périmé."""
        return obj.estPerime()

    def get_atteint_seuil(self, obj):
        """Vérifie si le produit atteint exactement le seuil."""
        return obj.atteintSeuil()


class StockSerializer(serializers.ModelSerializer):
    """
    Sérializeur pour le modèle Stock.
    Gère les opérations sur le stock avec détails du produit.
    """
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    produit_reference = serializers.CharField(source='produit.reference', read_only=True)
    quantite_disponible = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = [
            'id_stock', 'produit', 'quantite', 'date_ajout',
            'date_modification', 'produit_nom', 'produit_reference',
            'quantite_disponible'
        ]
        read_only_fields = ['id_stock', 'date_ajout', 'date_modification']

    def get_quantite_disponible(self, obj):
        """Retourne la quantité disponible du stock."""
        return obj.quantiteDisponible()


class DetailCommandeSerializer(serializers.ModelSerializer):
    """
    Sérializeur pour le modèle DetailCommande.
    Gère les détails des lignes de commande d'approvisionnement.
    """
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    produit_reference = serializers.CharField(source='produit.reference', read_only=True)
    prix_unitaire = serializers.DecimalField(
        source='produit.prix_unitaire', read_only=True, max_digits=10, decimal_places=2
    )
    sous_total = serializers.SerializerMethodField()

    class Meta:
        model = DetailCommande
        fields = [
            'id_detail', 'commande', 'produit', 'quantite',
            'produit_nom', 'produit_reference', 'prix_unitaire', 'sous_total'
        ]
        read_only_fields = ['id_detail', 'sous_total']

    def get_sous_total(self, obj):
        """Calcule le sous-total pour cette ligne de commande."""
        return obj.calculerSousTotal()


class CommandeApprovisionnementSerializer(serializers.ModelSerializer):
    """
    Sérializeur pour le modèle CommandeApprovisionnement.
    Gère les commandes d'approvisionnement avec détails complets.
    """
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    details = DetailCommandeSerializer(
        source='detailcommande_set', many=True, read_only=True
    )
    montant_total = serializers.SerializerMethodField()

    class Meta:
        model = CommandeApprovisionnement
        fields = [
            'id_commande', 'fournisseur', 'date_commande',
            'date_livraison_prevue', 'statut', 'fournisseur_nom',
            'details', 'montant_total'
        ]
        read_only_fields = ['id_commande', 'date_commande', 'montant_total']

    def get_montant_total(self, obj):
        """Calcule le montant total de la commande."""
        return obj.calculerMotantTotal()


class AlertStockSerializer(serializers.ModelSerializer):
    """
    Sérializeur pour le modèle AlertStock.
    Gère les alertes de stock avec informations du produit.
    """
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    produit_reference = serializers.CharField(source='produit.reference', read_only=True)

    class Meta:
        model = AlertStock
        fields = [
            'id_alert', 'produit', 'message', 'date_creation',
            'produit_nom', 'produit_reference'
        ]
        read_only_fields = ['id_alert', 'date_creation']


class HistoriqueStockSerializer(serializers.ModelSerializer):
    """
    Sérializeur pour le modèle HistoriqueStock.
    Trace les modifications du stock des produits.
    """
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    produit_reference = serializers.CharField(source='produit.reference', read_only=True)

    class Meta:
        model = HistoriqueStock
        fields = [
            'id_historique', 'produit', 'quantite_modifiee',
            'date_modification', 'type_modification',
            'produit_nom', 'produit_reference'
        ]
        read_only_fields = ['id_historique', 'date_modification']


class HistoriqueVenteSerializer(serializers.ModelSerializer):
    """
    Sérializeur pour le modèle HistoriqueVente.
    Gère l'historique des ventes de produits.
    """
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    produit_reference = serializers.CharField(source='produit.reference', read_only=True)
    tendance_vente = serializers.SerializerMethodField()
    prevision_demande = serializers.SerializerMethodField()

    class Meta:
        model = HistoriqueVente
        fields = [
            'id_historique_vente', 'produit', 'quantite_vendue',
            'date_vente', 'montant_total', 'chiffre_affaires_journalier',
            'produit_nom', 'produit_reference', 'tendance_vente', 'prevision_demande'
        ]
        read_only_fields = ['id_historique_vente', 'date_vente']

    def get_tendance_vente(self, obj):
        """Retourne la tendance de vente pour ce produit."""
        return obj.calculerTendanceVente()

    def get_prevision_demande(self, obj):
        """Retourne la prévision de demande pour ce produit."""
        return obj.prevoirDemande()


class ResponsableStockSerializer(serializers.ModelSerializer):
    """
    Sérializeur pour le modèle ResponsableStock.
    Gère les responsables de stock.
    """
    class Meta:
        model = ResponsableStock
        fields = ['id_responsable', 'nom', 'email', 'telephone']
        read_only_fields = ['id_responsable']