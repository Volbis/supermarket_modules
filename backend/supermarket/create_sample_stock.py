"""
Script pour créer des données de test pour l'historique des stocks
"""
import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supermarket.settings')
django.setup()

from gestion_stocks.models import HistoriqueStock, Produit

def create_sample_historique_stock():
    """Créer des mouvements de stock de test"""
    print("📦 Création de mouvements de stock de test...\n")
    
    # Récupérer quelques produits
    produits = Produit.objects.all()[:5]
    
    if not produits:
        print("❌ Aucun produit trouvé ! Créez d'abord des produits.")
        return
    
    mouvements_created = 0
    types_modification = ['AJOUT', 'RETRAIT']
    
    # Créer des mouvements sur les 60 derniers jours
    for i in range(40):
        produit = random.choice(produits)
        type_modif = random.choice(types_modification)
        
        # Quantité selon le type
        if type_modif == 'AJOUT':
            quantite = random.randint(10, 100)
        else:
            quantite = random.randint(1, 20)
        
        # Date aléatoire dans les 60 derniers jours
        jours_avant = random.randint(0, 60)
        date_modification = datetime.now() - timedelta(days=jours_avant)
        
        mouvement = HistoriqueStock.objects.create(
            produit=produit,
            quantite_modifiee=quantite,
            type_modification=type_modif
        )
        
        # Mettre à jour la date manuellement
        HistoriqueStock.objects.filter(id_historique=mouvement.id_historique).update(
            date_modification=date_modification
        )
        
        mouvements_created += 1
        emoji = "📈" if type_modif == "AJOUT" else "📉"
        print(f"{emoji} Mouvement {mouvements_created}: {type_modif} de {quantite} unités - {produit.nom} ({date_modification.strftime('%Y-%m-%d')})")
    
    print(f"\n✅ {mouvements_created} mouvements de stock créés avec succès!")
    
    # Calculer les statistiques
    ajouts = HistoriqueStock.objects.filter(type_modification='AJOUT')
    retraits = HistoriqueStock.objects.filter(type_modification='RETRAIT')
    
    total_ajouts = sum(h.quantite_modifiee for h in ajouts)
    total_retraits = sum(h.quantite_modifiee for h in retraits)
    
    print(f"\n📊 Statistiques:")
    print(f"   - Nombre d'ajouts: {ajouts.count()} ({total_ajouts} unités)")
    print(f"   - Nombre de retraits: {retraits.count()} ({total_retraits} unités)")
    print(f"   - Bilan net: {total_ajouts - total_retraits} unités")
    
    print("\nVous pouvez maintenant voir les données dans:")
    print("  GET http://127.0.0.1:8000/api/stocks/historique-stock/")

if __name__ == '__main__':
    try:
        create_sample_historique_stock()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
