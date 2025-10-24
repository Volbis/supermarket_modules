/**
 * Service API pour la gestion des transactions de caisse
 * 
 * Endpoints:
 * - GET    /transactions - Récupérer toutes les transactions
 * - GET    /transactions/:id - Récupérer une transaction spécifique
 * - POST   /transactions - Créer une nouvelle transaction
 * - PUT    /transactions/:id - Mettre à jour une transaction
 * - DELETE /transactions/:id - Supprimer une transaction
 * - POST   /transactions/:id/suspend - Suspendre une transaction
 * - POST   /transactions/:id/resume - Reprendre une transaction suspendue
 * - POST   /transactions/:id/cancel - Annuler une transaction
 */

import apiClient from '@/api/api';

const ENDPOINT = '/transactions';

export default {
  /**
   * Récupérer toutes les transactions
   * @param {Object} filters - Filtres optionnels (date, caissier, statut, etc.)
   * @returns {Promise}
   */
  getAllTransactions(filters = {}) {
    return apiClient.get(ENDPOINT, { params: filters });
  },

  /**
   * Récupérer une transaction par ID
   * @param {string} id - ID de la transaction
   * @returns {Promise}
   */
  getTransactionById(id) {
    return apiClient.get(`${ENDPOINT}/${id}`);
  },

  /**
   * Créer une nouvelle transaction
   * @param {Object} transactionData - Données de la transaction
   * @returns {Promise}
   */
  createTransaction(transactionData) {
    return apiClient.post(ENDPOINT, transactionData);
  },

  /**
   * Mettre à jour une transaction
   * @param {string} id - ID de la transaction
   * @param {Object} transactionData - Données à mettre à jour
   * @returns {Promise}
   */
  updateTransaction(id, transactionData) {
    return apiClient.put(`${ENDPOINT}/${id}`, transactionData);
  },

  /**
   * Supprimer une transaction
   * @param {string} id - ID de la transaction
   * @returns {Promise}
   */
  deleteTransaction(id) {
    return apiClient.delete(`${ENDPOINT}/${id}`);
  },

  /**
   * Suspendre une transaction en cours
   * @param {string} id - ID de la transaction
   * @returns {Promise}
   */
  suspendTransaction(id) {
    return apiClient.post(`${ENDPOINT}/${id}/suspend`);
  },

  /**
   * Reprendre une transaction suspendue
   * @param {string} id - ID de la transaction
   * @returns {Promise}
   */
  resumeTransaction(id) {
    return apiClient.post(`${ENDPOINT}/${id}/resume`);
  },

  /**
   * Annuler une transaction
   * @param {string} id - ID de la transaction
   * @param {string} reason - Raison de l'annulation
   * @returns {Promise}
   */
  cancelTransaction(id, reason = '') {
    return apiClient.post(`${ENDPOINT}/${id}/cancel`, { reason });
  },

  /**
   * Récupérer les transactions par date
   * @param {string} date - Date au format YYYY-MM-DD
   * @returns {Promise}
   */
  getTransactionsByDate(date) {
    return apiClient.get(`${ENDPOINT}/by-date/${date}`);
  },

  /**
   * Récupérer les transactions par caissier
   * @param {string} cashierId - ID du caissier
   * @returns {Promise}
   */
  getTransactionsByCashier(cashierId) {
    return apiClient.get(`${ENDPOINT}/by-cashier/${cashierId}`);
  },

  /**
   * Récupérer les transactions suspendues
   * @returns {Promise}
   */
  getSuspendedTransactions() {
    return apiClient.get(`${ENDPOINT}/suspended`);
  }
};
