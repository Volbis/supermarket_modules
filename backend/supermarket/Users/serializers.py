"""
Serializers pour l'authentification et la gestion des utilisateurs
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour les informations complètes de l'utilisateur
    """
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'telephone', 'role', 'photo_profil', 'is_active',
            'date_creation', 'date_modification'
        ]
        read_only_fields = ['id', 'date_creation', 'date_modification']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un nouvel utilisateur
    """
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'telephone', 'role'
        ]
    
    def validate(self, data):
        """Valider que les mots de passe correspondent"""
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return data
    
    def validate_email(self, value):
        """Valider que l'email est unique"""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value
    
    def validate_username(self, value):
        """Valider que le nom d'utilisateur est unique"""
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return value
    
    def create(self, validated_data):
        """Créer un nouvel utilisateur avec un mot de passe hashé"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer pour la connexion d'un utilisateur
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    def validate(self, data):
        """Authentifier l'utilisateur"""
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Identifiants invalides.")
            if not user.is_active:
                raise serializers.ValidationError("Ce compte est désactivé.")
            data['user'] = user
        else:
            raise serializers.ValidationError("Le nom d'utilisateur et le mot de passe sont requis.")
        
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer pour la mise à jour du profil utilisateur
    """
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'telephone', 'photo_profil'
        ]
    
    def validate_email(self, value):
        """Valider que l'email est unique (sauf pour l'utilisateur actuel)"""
        user = self.context.get('request').user
        if CustomUser.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer pour le changement de mot de passe
    """
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    new_password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    def validate_old_password(self, value):
        """Vérifier que l'ancien mot de passe est correct"""
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect.")
        return value
    
    def validate(self, data):
        """Valider que les nouveaux mots de passe correspondent"""
        if data.get('new_password') != data.get('new_password_confirm'):
            raise serializers.ValidationError({"new_password": "Les nouveaux mots de passe ne correspondent pas."})
        return data
    
    def save(self):
        """Changer le mot de passe"""
        user = self.context.get('request').user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
