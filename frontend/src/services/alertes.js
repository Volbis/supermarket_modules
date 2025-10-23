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
   * DELETE /api/stocks/alertes/{id}/
   * Supprime une alerte
   * @param {string} id - UUID de l'alerte
   * @returns {Promise} Confirmation de suppression
   */
  deleteAlerte(id) {
    return api.delete(`alertes/${id}/`);
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
