import api from '../api/api';

/**
 * Service API pour la gestion des alertes de stock
 * Base URL: http://127.0.0.1:8000/api/stocks/alertes/
 */

const alertesAPI = {
  /**
   * GET /api/stocks/alertes/
   * Récupère la liste de toutes les alertes
   * @returns {Promise} Liste des alertes
   */
  getAllAlertes() {
    return api.get('alertes/');
  },

  /**
   * GET /api/stocks/alertes/{id}/
   * Récupère une alerte spécifique par son ID
   * @param {string} id - UUID de l'alerte
   * @returns {Promise} Détails de l'alerte
   */
  getAlerteById(id) {
    return api.get(`alertes/${id}/`);
  },

  /**
   * POST /api/stocks/alertes/
   * Crée une nouvelle alerte
   * @param {Object} alerteData - Données de l'alerte
   * @param {string} alerteData.produit - UUID du produit
   * @param {string} alerteData.message - Message de l'alerte
   * @returns {Promise} Alerte créée
   */
  createAlerte(alerteData) {
    return api.post('alertes/', alerteData);
  },

  /**
   * PUT /api/stocks/alertes/{id}/
   * Met à jour une alerte existante (mise à jour complète)
   * @param {string} id - UUID de l'alerte
   * @param {Object} alerteData - Nouvelles données de l'alerte
   * @returns {Promise} Alerte mise à jour
   */
  updateAlerte(id, alerteData) {
    return api.put(`alertes/${id}/`, alerteData);
  },

  /**
   * PATCH /api/stocks/alertes/{id}/
   * Met à jour partiellement une alerte existante
   * @param {string} id - UUID de l'alerte
   * @param {Object} alerteData - Données partielles à mettre à jour
   * @returns {Promise} Alerte mise à jour
   */
  patchAlerte(id, alerteData) {
    return api.patch(`alertes/${id}/`, alerteData);
  },

  /**
   * DELETE /api/stocks/alertes/{id}/
   * Supprime une alerte
   * @param {string} id - UUID de l'alerte
   * @returns {Promise} Confirmation de suppression
   */
  deleteAlerte(id) {
    return api.delete(`alertes/${id}/`);
  },

  /**
   * GET /api/stocks/alertes/actives/
   * Récupère toutes les alertes actives
   * @returns {Promise} Liste des alertes actives
   */
  getAlertesActives() {
    return api.get('alertes/actives/');
  },

  /**
   * GET /api/stocks/alertes/par-produit/{produitId}/
   * Récupère toutes les alertes d'un produit spécifique
   * @param {string} produitId - UUID du produit
   * @returns {Promise} Liste des alertes du produit
   */
  getAlertesByProduit(produitId) {
    return api.get(`alertes/par-produit/${produitId}/`);
  }
};

export default alertesAPI;
