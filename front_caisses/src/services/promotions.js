/**
 * Service API pour la gestion des promotions et remises
 * 
 * Endpoints:
 * - GET  /promotions - Récupérer toutes les promotions
 * - GET  /promotions/active - Récupérer les promotions actives
 * - POST /promotions/:id/apply - Appliquer une promotion
 * - POST /promotions/calculate - Calculer les remises applicables
 */

import apiClient from '@/api/api';

const ENDPOINT = '/promotions';

export default {
  /**
   * Récupérer toutes les promotions
   * @returns {Promise}
   */
  getAllPromotions() {
    return apiClient.get(ENDPOINT);
  },

  /**
   * Récupérer les promotions actives
   * @returns {Promise}
   */
  getActivePromotions() {
    return apiClient.get(`${ENDPOINT}/active`);
  },

  /**
   * Récupérer une promotion par ID
   * @param {string} id - ID de la promotion
   * @returns {Promise}
   */
  getPromotionById(id) {
    return apiClient.get(`${ENDPOINT}/${id}`);
  },

  /**
   * Créer une nouvelle promotion
   * @param {Object} promotionData - Données de la promotion
   * @returns {Promise}
   */
  createPromotion(promotionData) {
    return apiClient.post(ENDPOINT, promotionData);
  },

  /**
   * Mettre à jour une promotion
   * @param {string} id - ID de la promotion
   * @param {Object} promotionData - Données à mettre à jour
   * @returns {Promise}
   */
  updatePromotion(id, promotionData) {
    return apiClient.put(`${ENDPOINT}/${id}`, promotionData);
  },

  /**
   * Supprimer une promotion
   * @param {string} id - ID de la promotion
   * @returns {Promise}
   */
  deletePromotion(id) {
    return apiClient.delete(`${ENDPOINT}/${id}`);
  },

  /**
   * Appliquer une promotion à une transaction
   * @param {string} promotionId - ID de la promotion
   * @param {Object} transactionData - Données de la transaction
   * @returns {Promise}
   */
  applyPromotion(promotionId, transactionData) {
    return apiClient.post(`${ENDPOINT}/${promotionId}/apply`, transactionData);
  },

  /**
   * Calculer les remises applicables pour un panier
   * @param {Object} cartData - Données du panier
   * @returns {Promise}
   */
  calculateDiscounts(cartData) {
    return apiClient.post(`${ENDPOINT}/calculate`, cartData);
  },

  /**
   * Vérifier l'éligibilité d'une promotion
   * @param {string} promotionId - ID de la promotion
   * @param {Object} cartData - Données du panier
   * @returns {Promise}
   */
  checkEligibility(promotionId, cartData) {
    return apiClient.post(`${ENDPOINT}/${promotionId}/check-eligibility`, cartData);
  }
};
