"""
Script pour SUPPRIMER TOUTES les migrations et recommencer proprement
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supermarket.settings')
django.setup()

from django.db import connection

def clean_all_migrations():
    """Supprimer TOUTES les migrations de la base de données"""
    print("🔧 Nettoyage complet des migrations...\n")
    
    try:
        with connection.cursor() as cursor:
            print("1. Suppression de TOUTES les migrations enregistrées...")
            cursor.execute("DELETE FROM django_migrations")
            print("   ✅ Toutes les migrations supprimées\n")
        
        print("✅ Nettoyage terminé!")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Exécutez: python3 manage.py makemigrations Users")
        print("2. Exécutez: python3 manage.py migrate")
        print("3. Exécutez: python3 manage.py createsuperuser")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("\n⚠️  SOLUTION ALTERNATIVE:")
        print("\nSupprimez TOUTES les tables et recommencez:")
        print("1. Ouvrez le shell Django: python3 manage.py shell")
        print("2. Exécutez:")
        print("   from django.db import connection")
        print("   with connection.cursor() as c:")
        print("       c.execute('DROP SCHEMA public CASCADE')")
        print("       c.execute('CREATE SCHEMA public')")
        print("   exit()")
        print("3. Puis: python3 manage.py migrate")

if __name__ == '__main__':
    clean_all_migrations()
