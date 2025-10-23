import api from '../api/api';

/**
 * Service API pour la gestion des détails de commandes
 * Base URL: http://127.0.0.1:8000/api/stocks/details-commandes/
 */

const detailsCommandesAPI = {
  /**
   * GET /api/stocks/details-commandes/
   * Récupère la liste de tous les détails de commandes
   * @returns {Promise} Liste des détails de commandes
   */
  getAllDetailsCommandes() {
    return api.get('details-commandes/');
  },

  /**
   * GET /api/stocks/details-commandes/{id}/
   * Récupère un détail de commande spécifique par son ID
   * @param {string} id - UUID du détail de commande
   * @returns {Promise} Détails du détail de commande
   */
  getDetailCommandeById(id) {
    return api.get(`details-commandes/${id}/`);
  },

  /**
   * POST /api/stocks/details-commandes/
   * Crée un nouveau détail de commande
   * @param {Object} detailData - Données du détail de commande
   * @param {string} detailData.commande - UUID de la commande
   * @param {string} detailData.produit - UUID du produit
   * @param {number} detailData.quantite - Quantité commandée
   * @returns {Promise} Détail de commande créé
   */
  createDetailCommande(detailData) {
    return api.post('details-commandes/', detailData);
  },

  /**
   * PUT /api/stocks/details-commandes/{id}/
   * Met à jour un détail de commande existant (mise à jour complète)
   * @param {string} id - UUID du détail de commande
   * @param {Object} detailData - Nouvelles données du détail de commande
   * @returns {Promise} Détail de commande mis à jour
   */
  updateDetailCommande(id, detailData) {
    return api.put(`details-commandes/${id}/`, detailData);
  },

  /**
   * PATCH /api/stocks/details-commandes/{id}/
   * Met à jour partiellement un détail de commande existant
   * @param {string} id - UUID du détail de commande
   * @param {Object} detailData - Données partielles à mettre à jour
   * @returns {Promise} Détail de commande mis à jour
   */
  patchDetailCommande(id, detailData) {
    return api.patch(`details-commandes/${id}/`, detailData);
  },

  /**
   * DELETE /api/stocks/details-commandes/{id}/
   * Supprime un détail de commande
   * @param {string} id - UUID du détail de commande
   * @returns {Promise} Confirmation de suppression
   */
  deleteDetailCommande(id) {
    return api.delete(`details-commandes/${id}/`);
  },

  /**
   * GET /api/stocks/details-commandes/{id}/sous-total/
   * Calcule le sous-total d'un détail de commande
   * @param {string} id - UUID du détail de commande
   * @returns {Promise} Sous-total
   */
  getSousTotal(id) {
    return api.get(`details-commandes/${id}/sous-total/`);
  }
};

export default detailsCommandesAPI;
