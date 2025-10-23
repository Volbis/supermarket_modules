"""
Vues pour l'authentification et la gestion des utilisateurs
"""

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import CustomUser
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Enregistrer un nouvel utilisateur
    POST /api/users/register/
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_data = UserSerializer(user).data
        return Response({
            'message': 'Utilisateur créé avec succès',
            'user': user_data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Connecter un utilisateur
    POST /api/users/login/
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        user_data = UserSerializer(user).data
        return Response({
            'message': 'Connexion réussie',
            'user': user_data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Déconnecter un utilisateur
    POST /api/users/logout/
    """
    logout(request)
    return Response({
        'message': 'Déconnexion réussie'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Obtenir les informations de l'utilisateur connecté
    GET /api/users/me/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Mettre à jour le profil de l'utilisateur connecté
    PUT/PATCH /api/users/profile/
    """
    serializer = UserProfileSerializer(
        request.user,
        data=request.data,
        partial=request.method == 'PATCH',
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profil mis à jour avec succès',
            'user': UserSerializer(request.user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Changer le mot de passe de l'utilisateur connecté
    POST /api/users/change-password/
    """
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Mot de passe modifié avec succès'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    """
    Liste de tous les utilisateurs
    GET /api/users/ 
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détails, mise à jour et suppression d'un utilisateur
    GET/PUT/PATCH/DELETE /api/users/<id>/
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deactivate_user(request, user_id):
    """
    Désactiver un utilisateur
    POST /api/users/<id>/deactivate/
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return Response({
            'message': f'Utilisateur {user.username} désactivé avec succès'
        }, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({
            'error': 'Utilisateur non trouvé'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def activate_user(request, user_id):
    """
    Activer un utilisateur
    POST /api/users/<id>/activate/
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return Response({
            'message': f'Utilisateur {user.username} activé avec succès'
        }, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({
            'error': 'Utilisateur non trouvé'
        }, status=status.HTTP_404_NOT_FOUND)
