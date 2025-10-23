"""
Script FINAL pour supprimer TOUTES les tables et recommencer proprement
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supermarket.settings')
django.setup()

from django.db import connection

def drop_all_tables():
    """Supprimer TOUTES les tables de la base de données"""
    print("⚠️  ATTENTION : Ce script va supprimer TOUTES les tables !")
    print("Cela inclut :")
    print("  - Toutes les données de gestion_stocks")
    print("  - Tous les utilisateurs")
    print("  - Toutes les sessions")
    print("  - TOUT !\n")
    
    response = input("Tapez 'SUPPRIMER' pour confirmer : ")
    
    if response != 'SUPPRIMER':
        print("❌ Opération annulée.")
        return
    
    print("\n🗑️  Suppression de toutes les tables...\n")
    
    try:
        with connection.cursor() as cursor:
            # Récupérer la liste de toutes les tables
            cursor.execute("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            tables = cursor.fetchall()
            
            if not tables:
                print("✅ Aucune table trouvée.")
                print("\nVous pouvez maintenant exécuter:")
                print("  python3 manage.py migrate")
                return
            
            print(f"Trouvé {len(tables)} table(s) à supprimer:")
            for table in tables:
                print(f"  - {table[0]}")
            
            print("\n🔨 Suppression en cours...")
            
            # Supprimer toutes les tables
            for table in tables:
                cursor.execute(f'DROP TABLE IF EXISTS "{table[0]}" CASCADE')
                print(f"  ✅ {table[0]} supprimée")
            
            # Supprimer les séquences
            cursor.execute("""
                SELECT sequence_name 
                FROM information_schema.sequences 
                WHERE sequence_schema = 'public'
            """)
            sequences = cursor.fetchall()
            for seq in sequences:
                cursor.execute(f'DROP SEQUENCE IF EXISTS "{seq[0]}" CASCADE')
            
        print("\n✅ Toutes les tables ont été supprimées avec succès!")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Exécutez: python3 manage.py migrate")
        print("2. Exécutez: python3 manage.py createsuperuser")
        print("3. Exécutez: python3 manage.py runserver")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == '__main__':
    drop_all_tables()
