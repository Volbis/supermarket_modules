# stock/signals.py
"""
Système d'alertes automatiques pour la gestion de stock.
Les alertes sont créées automatiquement lors des modifications de produits.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Produit, AlertStock, CommandeApprovisionnement, HistoriqueVente
from django.db.models import Sum


# ============================================================================
# ALERTES STOCK
# ============================================================================

@receiver(post_save, sender=Produit)
def alerte_stock_critique(sender, instance, **kwargs):
    """
    Alerte CRITIQUE: Stock sous le seuil de réapprovisionnement.
    Priorité: HAUTE
    """
    if instance.estSousSeuil():
        # Vérifier si l'alerte existe déjà aujourd'hui
        alerte_existe = AlertStock.objects.filter(
            produit=instance,
            message__contains="STOCK CRITIQUE",
            date_creation__date=timezone.now().date()
        ).exists()
        
        if not alerte_existe:
            pourcentage = (instance.quantite_en_stock / instance.seuil_de_reapprovisionnement * 100) if instance.seuil_de_reapprovisionnement > 0 else 0
            
            AlertStock.objects.create(
                produit=instance,
                message=f"🔴 STOCK CRITIQUE: {instance.nom} (Réf: {instance.reference}) "
                       f"est sous le seuil! Stock actuel: {instance.quantite_en_stock} unités, "
                       f"Seuil minimum: {instance.seuil_de_reapprovisionnement} unités "
                       f"({pourcentage:.1f}% du seuil). Réapprovisionnement URGENT requis!"
            )


@receiver(post_save, sender=Produit)
def alerte_stock_zero(sender, instance, **kwargs):
    """
    Alerte URGENTE: Stock épuisé (0 unités).
    Priorité: CRITIQUE
    """
    if instance.quantite_en_stock == 0:
        alerte_existe = AlertStock.objects.filter(
            produit=instance,
            message__contains="RUPTURE DE STOCK",
            date_creation__date=timezone.now().date()
        ).exists()
        
        if not alerte_existe:
            AlertStock.objects.create(
                produit=instance,
                message=f"⛔ RUPTURE DE STOCK: {instance.nom} (Réf: {instance.reference}) "
                       f"est en rupture totale! Stock: 0 unités. "
                       f"Action immédiate requise - Produit indisponible à la vente!"
            )


@receiver(post_save, sender=Produit)
def alerte_stock_atteint_seuil(sender, instance, **kwargs):
    """
    Alerte INFO: Stock atteint exactement le seuil.
    Priorité: MOYENNE
    """
    if instance.atteintSeuil():
        alerte_existe = AlertStock.objects.filter(
            produit=instance,
            message__contains="SEUIL ATTEINT",
            date_creation__date=timezone.now().date()
        ).exists()
        
        if not alerte_existe:
            AlertStock.objects.create(
                produit=instance,
                message=f"⚠️ SEUIL ATTEINT: {instance.nom} (Réf: {instance.reference}) "
                       f"a exactement {instance.quantite_en_stock} unités en stock "
                       f"(seuil: {instance.seuil_de_reapprovisionnement}). "
                       f"Envisager un réapprovisionnement prochainement."
            )


# ============================================================================
# ALERTES PÉREMPTION
# ============================================================================

@receiver(post_save, sender=Produit)
def alerte_produit_perime(sender, instance, **kwargs):
    """
    Alerte CRITIQUE: Produit périmé.
    Priorité: CRITIQUE
    """
    if instance.estPerime():
        alerte_existe = AlertStock.objects.filter(
            produit=instance,
            message__contains="PRODUIT PÉRIMÉ",
            date_creation__date=timezone.now().date()
        ).exists()
        
        if not alerte_existe:
            jours_perime = (timezone.now().date() - instance.date_de_peremption).days
            
            AlertStock.objects.create(
                produit=instance,
                message=f"🔴 PRODUIT PÉRIMÉ: {instance.nom} (Réf: {instance.reference}) "
                       f"est périmé depuis {jours_perime} jour(s)! "
                       f"Date de péremption: {instance.date_de_peremption}. "
                       f"Stock restant: {instance.quantite_en_stock} unités. "
                       f"RETRAIT IMMÉDIAT DE LA VENTE REQUIS!"
            )


@receiver(post_save, sender=Produit)
def alerte_peremption_imminente_7j(sender, instance, **kwargs):
    """
    Alerte HAUTE: Produit périme dans 7 jours ou moins.
    Priorité: HAUTE
    """
    jours_avant_peremption = (instance.date_de_peremption - timezone.now().date()).days
    
    if 0 < jours_avant_peremption <= 7 and not instance.estPerime():
        alerte_existe = AlertStock.objects.filter(
            produit=instance,
            message__contains="PÉREMPTION IMMINENTE",
            date_creation__date=timezone.now().date()
        ).exists()
        
        if not alerte_existe:
            AlertStock.objects.create(
                produit=instance,
                message=f"🟠 PÉREMPTION IMMINENTE: {instance.nom} (Réf: {instance.reference}) "
                       f"périme dans {jours_avant_peremption} jour(s)! "
                       f"Date de péremption: {instance.date_de_peremption}. "
                       f"Stock: {instance.quantite_en_stock} unités. "
                       f"Prioriser la vente ou retrait immédiat!"
            )


@receiver(post_save, sender=Produit)
def alerte_peremption_proche_30j(sender, instance, **kwargs):
    """
    Alerte INFO: Produit périme dans 30 jours.
    Priorité: MOYENNE
    """
    jours_avant_peremption = (instance.date_de_peremption - timezone.now().date()).days
    
    if 7 < jours_avant_peremption <= 30:
        alerte_existe = AlertStock.objects.filter(
            produit=instance,
            message__contains="PÉREMPTION PROCHE",
            date_creation__date=timezone.now().date()
        ).exists()
        
        if not alerte_existe:
            AlertStock.objects.create(
                produit=instance,
                message=f"🟡 PÉREMPTION PROCHE: {instance.nom} (Réf: {instance.reference}) "
                       f"périme dans {jours_avant_peremption} jour(s). "
                       f"Date de péremption: {instance.date_de_peremption}. "
                       f"Stock: {instance.quantite_en_stock} unités. "
                       f"Planifier une promotion ou ajuster les commandes."
            )


# ============================================================================
# ALERTES COMMANDES
# ============================================================================

@receiver(post_save, sender=CommandeApprovisionnement)
def alerte_commande_retard(sender, instance, **kwargs):
    """
    Alerte: Commande en retard de livraison.
    Priorité: HAUTE
    """
    if instance.statut == 'EN_COURS' and instance.date_livraison_prevue < timezone.now():
        jours_retard = (timezone.now() - instance.date_livraison_prevue).days
        
        alerte_existe = AlertStock.objects.filter(
            produit__fournisseur=instance.fournisseur,
            message__contains=f"RETARD COMMANDE {instance.id_commande}",
            date_creation__date=timezone.now().date()
        ).exists()
        
        if not alerte_existe:
            # Créer une alerte pour chaque produit de la commande
            details = instance.detailcommande_set.all()
            
            for detail in details:
                AlertStock.objects.create(
                    produit=detail.produit,
                    message=f"🟠 RETARD COMMANDE: La commande {instance.id_commande} "
                           f"pour {detail.produit.nom} (Réf: {detail.produit.reference}) "
                           f"est en retard de {jours_retard} jour(s)! "
                           f"Livraison prévue: {instance.date_livraison_prevue.date()}. "
                           f"Fournisseur: {instance.fournisseur.nom}. "
                           f"Quantité attendue: {detail.quantite} unités."
                )


# ============================================================================
# ALERTES VENTES
# ============================================================================

@receiver(post_save, sender=HistoriqueVente)
def alerte_forte_demande(sender, instance, created, **kwargs):
    """
    Alerte: Forte demande détectée (vente > 50% du stock).
    Priorité: MOYENNE
    """
    if created:
        pourcentage_vendu = (instance.quantite_vendue / instance.produit.quantite_en_stock * 100) if instance.produit.quantite_en_stock > 0 else 100
        
        if pourcentage_vendu >= 50:
            alerte_existe = AlertStock.objects.filter(
                produit=instance.produit,
                message__contains="FORTE DEMANDE",
                date_creation__date=timezone.now().date()
            ).exists()
            
            if not alerte_existe:
                AlertStock.objects.create(
                    produit=instance.produit,
                    message=f"📈 FORTE DEMANDE: {instance.produit.nom} (Réf: {instance.produit.reference}) "
                           f"connaît une forte demande! Vente de {instance.quantite_vendue} unités "
                           f"({pourcentage_vendu:.1f}% du stock actuel). "
                           f"Stock restant: {instance.produit.quantite_en_stock} unités. "
                           f"Envisager d'augmenter les commandes."
                )


# ============================================================================
# ALERTES FOURNISSEURS
# ============================================================================

def alerte_delai_livraison_long(produit):
    """
    Alerte: Délai de livraison du fournisseur trop long.
    Priorité: BASSE
    """
    if produit.fournisseur.delais_livraison_jours > 7 and produit.estSousSeuil():
        alerte_existe = AlertStock.objects.filter(
            produit=produit,
            message__contains="DÉLAI LIVRAISON LONG",
            date_creation__date=timezone.now().date()
        ).exists()
        
        if not alerte_existe:
            AlertStock.objects.create(
                produit=produit,
                message=f"⏰ DÉLAI LIVRAISON LONG: {produit.nom} (Réf: {produit.reference}) "
                       f"a un stock bas ET un délai de livraison de {produit.fournisseur.delais_livraison_jours} jours. "
                       f"Fournisseur: {produit.fournisseur.nom}. "
                       f"Commander dès maintenant pour éviter une rupture!"
            )


@receiver(post_save, sender=Produit)
def verifier_delai_livraison(sender, instance, **kwargs):
    """Vérifier le délai de livraison quand le stock change."""
    alerte_delai_livraison_long(instance)


# ============================================================================
# ALERTES PRIX
# ============================================================================

@receiver(pre_save, sender=Produit)
def alerte_changement_prix(sender, instance, **kwargs):
    """
    Alerte: Prix modifié (augmentation ou baisse significative).
    Priorité: BASSE
    """
    if instance.pk:  # Si le produit existe déjà
        try:
            ancien_produit = Produit.objects.get(pk=instance.pk)
            
            if ancien_produit.prix_unitaire != instance.prix_unitaire:
                variation = ((instance.prix_unitaire - ancien_produit.prix_unitaire) / ancien_produit.prix_unitaire * 100)
                
                if abs(variation) >= 10:  # Changement de 10% ou plus
                    symbole = "📈" if variation > 0 else "📉"
                    action = "augmenté" if variation > 0 else "diminué"
                    
                    AlertStock.objects.create(
                        produit=instance,
                        message=f"{symbole} CHANGEMENT DE PRIX: {instance.nom} (Réf: {instance.reference}) "
                               f"a {action} de {abs(variation):.1f}%! "
                               f"Ancien prix: {ancien_produit.prix_unitaire} FCFA, "
                               f"Nouveau prix: {instance.prix_unitaire} FCFA. "
                               f"Mettre à jour les étiquettes et le système de caisse."
                    )
        except Produit.DoesNotExist:
            pass


# ============================================================================
# NETTOYAGE AUTOMATIQUE DES ANCIENNES ALERTES
# ============================================================================

def nettoyer_anciennes_alertes():
    """
    Supprimer les alertes de plus de 30 jours (à exécuter périodiquement).
    Peut être appelé via une tâche Celery ou un management command.
    """
    date_limite = timezone.now() - timedelta(days=30)
    alertes_supprimees = AlertStock.objects.filter(
        date_creation__lt=date_limite
    ).delete()
    
    return alertes_supprimees[0]  # Nombre d'alertes supprimées