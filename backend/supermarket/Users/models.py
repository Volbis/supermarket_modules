from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé pour l'application ExpressMall
    """
    ROLE_CHOICES = [
        ('RESPONSABLE', 'Responsable Stock'),
    ]

    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='RESPONSABLE', verbose_name="Rôle")
    photo_profil = models.ImageField(upload_to='profils/', blank=True, null=True, verbose_name="Photo de profil")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        db_table = 'custom_users'
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
