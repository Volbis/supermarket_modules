/**
 * Service d'authentification pour ExpressMall
 * Gère la connexion, l'inscription et la gestion du profil utilisateur
 */

import api from './api';

const AUTH_ENDPOINTS = {
  REGISTER: '/auth/register/',
  LOGIN: '/auth/login/',
  LOGOUT: '/auth/logout/',
  ME: '/auth/me/',
  PROFILE: '/auth/profile/',
  CHANGE_PASSWORD: '/auth/change-password/',
  USERS: '/auth/',
  USER_DETAIL: (id) => `/auth/${id}/`,
  DEACTIVATE: (id) => `/auth/${id}/deactivate/`,
  ACTIVATE: (id) => `/auth/${id}/activate/`,
};

const USER_STORAGE_KEY = 'expressmail_user';

export default {
  /**
   * Inscription d'un nouvel utilisateur
   * @param {Object} userData - Données de l'utilisateur
   * @returns {Promise}
   */
  async register(userData) {
    try {
      const response = await api.post(AUTH_ENDPOINTS.REGISTER, userData);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de l\'inscription:', error);
      throw error;
    }
  },

  /**
   * Connexion d'un utilisateur
   * @param {string} username - Nom d'utilisateur
   * @param {string} password - Mot de passe
   * @returns {Promise}
   */
  async login(username, password) {
    try {
      const response = await api.post(AUTH_ENDPOINTS.LOGIN, {
        username,
        password
      });
      
      if (response.data.user) {
        // Sauvegarder l'utilisateur dans le localStorage
        this.saveUser(response.data.user);
      }
      
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la connexion:', error);
      throw error;
    }
  },

  /**
   * Déconnexion de l'utilisateur
   * @returns {Promise}
   */
  async logout() {
    try {
      await api.post(AUTH_ENDPOINTS.LOGOUT);
      this.removeUser();
      return { message: 'Déconnexion réussie' };
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error);
      // Supprimer l'utilisateur même en cas d'erreur
      this.removeUser();
      throw error;
    }
  },

  /**
   * Obtenir l'utilisateur connecté depuis le serveur
   * @returns {Promise}
   */
  async getCurrentUser() {
    try {
      const response = await api.get(AUTH_ENDPOINTS.ME);
      this.saveUser(response.data);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération de l\'utilisateur:', error);
      this.removeUser();
      throw error;
    }
  },

  /**
   * Mettre à jour le profil de l'utilisateur
   * @param {Object} profileData - Nouvelles données du profil
   * @returns {Promise}
   */
  async updateProfile(profileData) {
    try {
      const response = await api.put(AUTH_ENDPOINTS.PROFILE, profileData);
      
      if (response.data.user) {
        this.saveUser(response.data.user);
      }
      
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la mise à jour du profil:', error);
      throw error;
    }
  },

  /**
   * Changer le mot de passe
   * @param {string} oldPassword - Ancien mot de passe
   * @param {string} newPassword - Nouveau mot de passe
   * @param {string} newPasswordConfirm - Confirmation du nouveau mot de passe
   * @returns {Promise}
   */
  async changePassword(oldPassword, newPassword, newPasswordConfirm) {
    try {
      const response = await api.post(AUTH_ENDPOINTS.CHANGE_PASSWORD, {
        old_password: oldPassword,
        new_password: newPassword,
        new_password_confirm: newPasswordConfirm
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors du changement de mot de passe:', error);
      throw error;
    }
  },

  /**
   * Obtenir la liste de tous les utilisateurs (Admin uniquement)
   * @returns {Promise}
   */
  async getAllUsers() {
    try {
      const response = await api.get(AUTH_ENDPOINTS.USERS);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des utilisateurs:', error);
      throw error;
    }
  },

  /**
   * Obtenir les détails d'un utilisateur (Admin uniquement)
   * @param {number} userId - ID de l'utilisateur
   * @returns {Promise}
   */
  async getUserById(userId) {
    try {
      const response = await api.get(AUTH_ENDPOINTS.USER_DETAIL(userId));
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération de l\'utilisateur:', error);
      throw error;
    }
  },

  /**
   * Désactiver un utilisateur (Admin uniquement)
   * @param {number} userId - ID de l'utilisateur
   * @returns {Promise}
   */
  async deactivateUser(userId) {
    try {
      const response = await api.post(AUTH_ENDPOINTS.DEACTIVATE(userId));
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la désactivation de l\'utilisateur:', error);
      throw error;
    }
  },

  /**
   * Activer un utilisateur (Admin uniquement)
   * @param {number} userId - ID de l'utilisateur
   * @returns {Promise}
   */
  async activateUser(userId) {
    try {
      const response = await api.post(AUTH_ENDPOINTS.ACTIVATE(userId));
      return response.data;
    } catch (error) {
      console.error('Erreur lors de l\'activation de l\'utilisateur:', error);
      throw error;
    }
  },

  /**
   * Vérifier si l'utilisateur est authentifié
   * @returns {boolean}
   */
  isAuthenticated() {
    return !!this.getUser();
  },

  /**
   * Obtenir l'utilisateur depuis le localStorage
   * @returns {Object|null}
   */
  getUser() {
    try {
      const user = localStorage.getItem(USER_STORAGE_KEY);
      return user ? JSON.parse(user) : null;
    } catch (error) {
      console.error('Erreur lors de la lecture du localStorage:', error);
      return null;
    }
  },

  /**
   * Sauvegarder l'utilisateur dans le localStorage
   * @param {Object} user - Données de l'utilisateur
   */
  saveUser(user) {
    try {
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
    } catch (error) {
      console.error('Erreur lors de la sauvegarde dans le localStorage:', error);
    }
  },

  /**
   * Supprimer l'utilisateur du localStorage
   */
  removeUser() {
    try {
      localStorage.removeItem(USER_STORAGE_KEY);
    } catch (error) {
      console.error('Erreur lors de la suppression du localStorage:', error);
    }
  },

  /**
   * Vérifier si l'utilisateur a un rôle spécifique
   * @param {string} role - Rôle à vérifier
   * @returns {boolean}
   */
  hasRole(role) {
    const user = this.getUser();
    return user && user.role === role;
  },

  /**
   * Vérifier si l'utilisateur est admin
   * @returns {boolean}
   */
  isAdmin() {
    return this.hasRole('ADMIN');
  },

  /**
   * Vérifier si l'utilisateur est manager
   * @returns {boolean}
   */
  isManager() {
    return this.hasRole('MANAGER');
  },

  /**
   * Obtenir le nom complet de l'utilisateur
   * @returns {string}
   */
  getFullName() {
    const user = this.getUser();
    if (!user) return '';
    
    const fullName = `${user.first_name || ''} ${user.last_name || ''}`.trim();
    return fullName || user.username;
  }
};
