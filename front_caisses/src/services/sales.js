/**
 * Service API pour la gestion des statistiques de ventes
 * 
 * Endpoints:
 * - GET /sales/statistics - Statistiques générales des ventes
 * - GET /sales/by-period - Ventes par période
 * - GET /sales/top-products - Produits les plus vendus
 * - GET /sales/by-category - Ventes par catégorie
 * - GET /sales/trends - Tendances des ventes
 */

import apiClient from '@/api/api';

const ENDPOINT = '/sales';

export default {
  /**
   * Récupérer les statistiques générales des ventes
   * @param {Object} filters - Filtres (date_debut, date_fin, caisse, caissier)
   * @returns {Promise}
   */
  getSalesStatistics(filters = {}) {
    return apiClient.get(`${ENDPOINT}/statistics`, { params: filters });
  },

  /**
   * Récupérer les ventes par période
   * @param {string} period - Période (day, week, month, year)
   * @param {Object} filters - Filtres additionnels
   * @returns {Promise}
   */
  getSalesByPeriod(period, filters = {}) {
    return apiClient.get(`${ENDPOINT}/by-period/${period}`, { params: filters });
  },

  /**
   * Récupérer les produits les plus vendus
   * @param {number} limit - Nombre de produits à retourner
   * @param {Object} filters - Filtres (date_debut, date_fin)
   * @returns {Promise}
   */
  getTopProducts(limit = 10, filters = {}) {
    return apiClient.get(`${ENDPOINT}/top-products`, {
      params: { limit, ...filters }
    });
  },

  /**
   * Récupérer les ventes par catégorie
   * @param {Object} filters - Filtres (date_debut, date_fin)
   * @returns {Promise}
   */
  getSalesByCategory(filters = {}) {
    return apiClient.get(`${ENDPOINT}/by-category`, { params: filters });
  },

  /**
   * Récupérer les tendances des ventes
   * @param {string} period - Période d'analyse
   * @returns {Promise}
   */
  getSalesTrends(period = 'week') {
    return apiClient.get(`${ENDPOINT}/trends`, { params: { period } });
  },

  /**
   * Récupérer les ventes par heure de la journée
   * @param {string} date - Date au format YYYY-MM-DD
   * @returns {Promise}
   */
  getSalesByHour(date) {
    return apiClient.get(`${ENDPOINT}/by-hour`, { params: { date } });
  },

  /**
   * Comparer les ventes entre deux périodes
   * @param {string} startDate1 - Date de début période 1
   * @param {string} endDate1 - Date de fin période 1
   * @param {string} startDate2 - Date de début période 2
   * @param {string} endDate2 - Date de fin période 2
   * @returns {Promise}
   */
  compareSalesPeriods(startDate1, endDate1, startDate2, endDate2) {
    return apiClient.post(`${ENDPOINT}/compare`, {
      period1: { start: startDate1, end: endDate1 },
      period2: { start: startDate2, end: endDate2 }
    });
  },

  /**
   * Récupérer le panier moyen
   * @param {Object} filters - Filtres (date_debut, date_fin)
   * @returns {Promise}
   */
  getAverageBasket(filters = {}) {
    return apiClient.get(`${ENDPOINT}/average-basket`, { params: filters });
  },

  /**
   * Récupérer les performances par caissier
   * @param {Object} filters - Filtres (date_debut, date_fin)
   * @returns {Promise}
   */
  getCashierPerformance(filters = {}) {
    return apiClient.get(`${ENDPOINT}/cashier-performance`, { params: filters });
  }
};
