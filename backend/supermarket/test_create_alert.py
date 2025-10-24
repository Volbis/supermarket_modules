"""
Script pour créer une notification de test manuellement.
Usage: python test_create_alert.py
"""

import os
import sys
import django

# Configuration Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supermarket.settings')
django.setup()

from gestion_stocks.models import AlertStock, Produit

def create_test_notification():
    """Créer une notification de test pour le premier produit."""
    
    # Récupérer le premier produit disponible
    produit = Produit.objects.first()
    
    if not produit:
        print("❌ Aucun produit trouvé dans la base de données.")
        print("💡 Créez d'abord des produits avec : python create_sample_stock.py")
        return
    
    # Créer une alerte de stock critique
    alerte = AlertStock.objects.create(
        produit=produit,
        message=f"🔴 STOCK CRITIQUE : {produit.nom} - Seulement {produit.quantite_en_stock} unités restantes (seuil: {produit.seuil_de_reapprovisionnement})"
    )
    
    print("✅ Notification créée avec succès !")
    print(f"📦 Produit : {produit.nom}")
    print(f"📝 Message : {alerte.message}")
    print(f"🕒 Date : {alerte.date_creation}")
    print(f"🆔 ID : {alerte.id_alert}")
    
    # Afficher toutes les alertes
    total_alertes = AlertStock.objects.count()
    print(f"\n📊 Total d'alertes dans la base : {total_alertes}")

def create_multiple_test_notifications():
    """Créer plusieurs types de notifications de test."""
    
    produits = Produit.objects.all()[:5]  # Prendre les 5 premiers produits
    
    if not produits:
        print("❌ Aucun produit trouvé.")
        return
    
    messages_templates = [
        "🔴 STOCK CRITIQUE : Stock inférieur au seuil minimum",
        "⛔ RUPTURE DE STOCK : Plus de stock disponible",
        "🟠 STOCK BAS : Réapprovisionnement recommandé",
        "⏰ PÉREMPTION PROCHE : Expire dans 7 jours",
        "🔴 PRODUIT PÉRIMÉ : Date de péremption dépassée"
    ]
    
    created_count = 0
    for i, produit in enumerate(produits):
        if i < len(messages_templates):
            message = f"{messages_templates[i]} - {produit.nom}"
            AlertStock.objects.create(
                produit=produit,
                message=message
            )
            created_count += 1
            print(f"✅ Notification {i+1} créée : {message}")
    
    print(f"\n🎉 {created_count} notifications créées avec succès !")

if __name__ == "__main__":
    print("=== CRÉATION DE NOTIFICATIONS DE TEST ===\n")
    
    choice = input("Créer (1) une notification ou (5) plusieurs notifications ? [1/5] : ").strip()
    
    if choice == "5":
        create_multiple_test_notifications()
    else:
        create_test_notification()
    
    print("\n🔄 Rechargez la page Notifications dans l'application pour voir les nouvelles alertes.")
