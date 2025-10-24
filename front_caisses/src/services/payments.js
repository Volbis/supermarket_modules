/**
 * Service API pour la gestion des paiements
 * 
 * Endpoints:
 * - POST /payments/process - Traiter un paiement
 * - POST /payments/validate - Valider un paiement
 * - GET  /payments/methods - Récupérer les méthodes de paiement disponibles
 * - POST /payments/:id/refund - Rembourser un paiement
 */

import apiClient from '@/api/api';

const ENDPOINT = '/payments';

export default {
  /**
   * Traiter un paiement
   * @param {Object} paymentData - Données du paiement
   * @returns {Promise}
   */
  processPayment(paymentData) {
    return apiClient.post(`${ENDPOINT}/process`, paymentData);
  },

  /**
   * Valider un paiement
   * @param {string} transactionId - ID de la transaction
   * @param {Array} payments - Liste des paiements
   * @returns {Promise}
   */
  validatePayment(transactionId, payments) {
    return apiClient.post(`${ENDPOINT}/validate`, {
      transaction_id: transactionId,
      payments: payments
    });
  },

  /**
   * Récupérer les méthodes de paiement disponibles
   * @returns {Promise}
   */
  getPaymentMethods() {
    return apiClient.get(`${ENDPOINT}/methods`);
  },

  /**
   * Rembourser un paiement
   * @param {string} paymentId - ID du paiement
   * @param {number} amount - Montant à rembourser
   * @param {string} reason - Raison du remboursement
   * @returns {Promise}
   */
  refundPayment(paymentId, amount, reason = '') {
    return apiClient.post(`${ENDPOINT}/${paymentId}/refund`, {
      amount: amount,
      reason: reason
    });
  },

  /**
   * Simuler un paiement par carte bancaire
   * @param {Object} cardData - Données de la carte
   * @returns {Promise}
   */
  simulateCardPayment(cardData) {
    return apiClient.post(`${ENDPOINT}/simulate/card`, cardData);
  },

  /**
   * Simuler un paiement mobile money
   * @param {Object} mobileData - Données du paiement mobile
   * @returns {Promise}
   */
  simulateMobilePayment(mobileData) {
    return apiClient.post(`${ENDPOINT}/simulate/mobile`, mobileData);
  },

  /**
   * Vérifier le solde d'une carte cadeau
   * @param {string} cardNumber - Numéro de la carte cadeau
   * @returns {Promise}
   */
  checkGiftCardBalance(cardNumber) {
    return apiClient.get(`${ENDPOINT}/gift-card/${cardNumber}/balance`);
  }
};
