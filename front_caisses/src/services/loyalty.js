/**
 * Service API pour la gestion du programme de fidélité
 * 
 * Endpoints:
 * - GET  /loyalty/card/:cardNumber - Récupérer les informations d'une carte
 * - POST /loyalty/card/validate - Valider une carte de fidélité
 * - POST /loyalty/points/earn - Ajouter des points
 * - POST /loyalty/points/redeem - Utiliser des points
 * - GET  /loyalty/customer/:customerId - Récupérer le profil client
 */

import apiClient from '@/api/api';

const ENDPOINT = '/loyalty';

export default {
  /**
   * Récupérer les informations d'une carte de fidélité
   * @param {string} cardNumber - Numéro de la carte
   * @returns {Promise}
   */
  getCardInfo(cardNumber) {
    return apiClient.get(`${ENDPOINT}/card/${cardNumber}`);
  },

  /**
   * Valider une carte de fidélité
   * @param {string} cardNumber - Numéro de la carte
   * @returns {Promise}
   */
  validateCard(cardNumber) {
    return apiClient.post(`${ENDPOINT}/card/validate`, { card_number: cardNumber });
  },

  /**
   * Ajouter des points de fidélité
   * @param {string} cardNumber - Numéro de la carte
   * @param {number} points - Nombre de points à ajouter
   * @param {string} transactionId - ID de la transaction
   * @returns {Promise}
   */
  earnPoints(cardNumber, points, transactionId) {
    return apiClient.post(`${ENDPOINT}/points/earn`, {
      card_number: cardNumber,
      points: points,
      transaction_id: transactionId
    });
  },

  /**
   * Utiliser des points de fidélité
   * @param {string} cardNumber - Numéro de la carte
   * @param {number} points - Nombre de points à utiliser
   * @param {string} transactionId - ID de la transaction
   * @returns {Promise}
   */
  redeemPoints(cardNumber, points, transactionId) {
    return apiClient.post(`${ENDPOINT}/points/redeem`, {
      card_number: cardNumber,
      points: points,
      transaction_id: transactionId
    });
  },

  /**
   * Récupérer le profil client
   * @param {string} customerId - ID du client
   * @returns {Promise}
   */
  getCustomerProfile(customerId) {
    return apiClient.get(`${ENDPOINT}/customer/${customerId}`);
  },

  /**
   * Calculer les remises basées sur le statut client
   * @param {string} cardNumber - Numéro de la carte
   * @param {number} amount - Montant de la transaction
   * @returns {Promise}
   */
  calculateLoyaltyDiscount(cardNumber, amount) {
    return apiClient.post(`${ENDPOINT}/calculate-discount`, {
      card_number: cardNumber,
      amount: amount
    });
  },

  /**
   * Récupérer l'historique des points
   * @param {string} cardNumber - Numéro de la carte
   * @returns {Promise}
   */
  getPointsHistory(cardNumber) {
    return apiClient.get(`${ENDPOINT}/points/history/${cardNumber}`);
  }
};
