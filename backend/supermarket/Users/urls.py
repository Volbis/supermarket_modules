"""
Configuration des URLs pour l'authentification et la gestion des utilisateurs.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # Profil utilisateur
    path('me/', views.current_user, name='current-user'),
    path('profile/', views.update_profile, name='update-profile'),
    path('change-password/', views.change_password, name='change-password'),
    
    # Gestion des utilisateurs (Admin)
    path('', views.UserListView.as_view(), name='user-list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('<int:user_id>/deactivate/', views.deactivate_user, name='deactivate-user'),
    path('<int:user_id>/activate/', views.activate_user, name='activate-user'),
]
