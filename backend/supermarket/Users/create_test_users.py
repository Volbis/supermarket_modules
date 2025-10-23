"""
Script pour créer des utilisateurs de test
Usage: python manage.py shell < Users/create_test_users.py
"""

from Users.models import CustomUser

# Créer des utilisateurs de test
users_data = [
    {
        'username': 'admin',
        'email': 'admin@expressmail.com',
        'password': 'admin123',
        'first_name': 'Admin',
        'last_name': 'System',
        'role': 'ADMIN',
        'telephone': '+225 00 00 00 00',
        'is_staff': True,
        'is_superuser': True
    },
    {
        'username': 'deric_ezin',
        'email': 'deric.ezin@expressmail.com',
        'password': 'deric123',
        'first_name': 'Déric',
        'last_name': 'EZIN',
        'role': 'ADMIN',
        'telephone': '+225 XX XX XX XX'
    },
    {
        'username': 'manager1',
        'email': 'manager@expressmail.com',
        'password': 'manager123',
        'first_name': 'Jean',
        'last_name': 'KOUASSI',
        'role': 'MANAGER',
        'telephone': '+225 01 02 03 04'
    },
    {
        'username': 'responsable1',
        'email': 'responsable@expressmail.com',
        'password': 'responsable123',
        'first_name': 'Marie',
        'last_name': 'DIABATE',
        'role': 'RESPONSABLE',
        'telephone': '+225 05 06 07 08'
    },
    {
        'username': 'vendeur1',
        'email': 'vendeur@expressmail.com',
        'password': 'vendeur123',
        'first_name': 'Paul',
        'last_name': 'KONE',
        'role': 'VENDEUR',
        'telephone': '+225 09 10 11 12'
    }
]

print("🚀 Création des utilisateurs de test...")
print("-" * 50)

for user_data in users_data:
    username = user_data['username']
    
    # Vérifier si l'utilisateur existe déjà
    if CustomUser.objects.filter(username=username).exists():
        print(f"⚠️  L'utilisateur '{username}' existe déjà - ignoré")
        continue
    
    # Créer l'utilisateur
    password = user_data.pop('password')
    user = CustomUser.objects.create_user(**user_data)
    user.set_password(password)
    user.save()
    
    print(f"✅ Utilisateur '{username}' créé avec succès")
    print(f"   Email: {user.email}")
    print(f"   Rôle: {user.role}")
    print(f"   Mot de passe: {password}")
    print()

print("-" * 50)
print("✨ Création des utilisateurs terminée !")
print("\n📋 Récapitulatif des identifiants:")
print("-" * 50)
for user_data in users_data:
    print(f"Username: {user_data['username']}")
    print(f"Password: {user_data.get('password', 'N/A')}")
    print()
