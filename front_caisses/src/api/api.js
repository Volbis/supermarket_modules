/**
 * Configuration de base pour Axios
 * Toutes les requêtes API passent par cette instance configurée
 */

import axios from 'axios';

// URL de base de l'API backend
const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

// Créer une instance Axios avec configuration par défaut
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 secondes
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Intercepteur pour ajouter le token d'authentification si disponible
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs de réponse
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // Erreur HTTP (4xx, 5xx)
      console.error('API Error:', error.response.status, error.response.data);
      
      // Déconnexion si 401 Unauthorized
      if (error.response.status === 401) {
        localStorage.removeItem('auth_token');
        // Redirection vers login si nécessaire
        // window.location.href = '/login';
      }
    } else if (error.request) {
      // Pas de réponse reçue
      console.error('Network Error:', error.request);
    } else {
      // Erreur lors de la configuration de la requête
      console.error('Request Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
