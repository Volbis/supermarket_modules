/**
 * Service API pour la gestion des rapports quotidiens
 * 
 * Endpoints:
 * - GET  /reports/daily/:date - Récupérer le rapport d'une date
 * - POST /reports/daily/close - Clôturer la journée
 * - GET  /reports/cash-drawer/:registerId - État du tiroir-caisse
 * - POST /reports/cash-drawer/open - Ouvrir le tiroir-caisse
 * - POST /reports/cash-drawer/close - Fermer le tiroir-caisse
 */

import apiClient from '@/api/api';

const ENDPOINT = '/reports';

export default {
  /**
   * Récupérer le rapport quotidien
   * @param {string} date - Date au format YYYY-MM-DD
   * @returns {Promise}
   */
  getDailyReport(date) {
    return apiClient.get(`${ENDPOINT}/daily/${date}`);
  },

  /**
   * Récupérer tous les rapports quotidiens
   * @param {Object} filters - Filtres (date_debut, date_fin, caisse, etc.)
   * @returns {Promise}
   */
  getAllDailyReports(filters = {}) {
    return apiClient.get(`${ENDPOINT}/daily`, { params: filters });
  },

  /**
   * Clôturer la journée de caisse
   * @param {Object} closingData - Données de clôture
   * @returns {Promise}
   */
  closeDailyReport(closingData) {
    return apiClient.post(`${ENDPOINT}/daily/close`, closingData);
  },

  /**
   * Récupérer l'état du tiroir-caisse
   * @param {string} registerId - ID de la caisse
   * @returns {Promise}
   */
  getCashDrawerStatus(registerId) {
    return apiClient.get(`${ENDPOINT}/cash-drawer/${registerId}`);
  },

  /**
   * Ouvrir le tiroir-caisse
   * @param {Object} openingData - Données d'ouverture (fond de caisse, caissier, etc.)
   * @returns {Promise}
   */
  openCashDrawer(openingData) {
    return apiClient.post(`${ENDPOINT}/cash-drawer/open`, openingData);
  },

  /**
   * Fermer le tiroir-caisse
   * @param {Object} closingData - Données de fermeture (comptage, écarts, etc.)
   * @returns {Promise}
   */
  closeCashDrawer(closingData) {
    return apiClient.post(`${ENDPOINT}/cash-drawer/close`, closingData);
  },

  /**
   * Ajouter un mouvement de caisse
   * @param {Object} movementData - Données du mouvement (entrée/sortie)
   * @returns {Promise}
   */
  addCashMovement(movementData) {
    return apiClient.post(`${ENDPOINT}/cash-drawer/movement`, movementData);
  },

  /**
   * Effectuer un comptage intermédiaire
   * @param {string} registerId - ID de la caisse
   * @param {Object} countData - Données du comptage
   * @returns {Promise}
   */
  intermediateCount(registerId, countData) {
    return apiClient.post(`${ENDPOINT}/cash-drawer/${registerId}/count`, countData);
  },

  /**
   * Exporter un rapport au format PDF
   * @param {string} reportId - ID du rapport
   * @returns {Promise}
   */
  exportReportPDF(reportId) {
    return apiClient.get(`${ENDPOINT}/${reportId}/export/pdf`, {
      responseType: 'blob'
    });
  },

  /**
   * Exporter un rapport au format Excel
   * @param {string} reportId - ID du rapport
   * @returns {Promise}
   */
  exportReportExcel(reportId) {
    return apiClient.get(`${ENDPOINT}/${reportId}/export/excel`, {
      responseType: 'blob'
    });
  },

  /**
   * Générer le rapport Z (rapport de clôture)
   * @param {string} registerId - ID de la caisse
   * @param {string} date - Date du rapport
   * @returns {Promise}
   */
  generateZReport(registerId, date) {
    return apiClient.post(`${ENDPOINT}/z-report`, {
      register_id: registerId,
      date: date
    });
  }
};
