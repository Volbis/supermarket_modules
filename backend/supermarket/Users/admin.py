"""
Configuration de l'administration Django pour les utilisateurs
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Configuration de l'interface d'administration pour CustomUser
    """
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_creation']
    list_filter = ['role', 'is_active', 'is_staff', 'date_creation']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'telephone']
    ordering = ['-date_creation']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('telephone', 'role', 'photo_profil')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('email', 'first_name', 'last_name', 'telephone', 'role', 'photo_profil')
        }),
    )
