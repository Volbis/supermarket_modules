import api from '../api/api';

/**
 * Service API pour la gestion de l'historique des stocks
 * Base URL: http://127.0.0.1:8000/api/stocks/historique-stock/
 */

const historiqueStockAPI = {
  /**
   * GET /api/stocks/historique-stock/
   * Récupère la liste complète de l'historique des stocks
   * @returns {Promise} Liste de l'historique des stocks
   */
  getAllHistoriqueStock() {
    return api.get('historique-stock/');
  },

  /**
   * GET /api/stocks/historique-stock/{id}/
   * Récupère un enregistrement d'historique spécifique par son ID
   * @param {string} id - UUID de l'historique
   * @returns {Promise} Détails de l'historique
   */
  getHistoriqueStockById(id) {
    return api.get(`historique-stock/${id}/`);
  },

  /**
   * POST /api/stocks/historique-stock/
   * Crée un nouveau enregistrement d'historique
   * @param {Object} historiqueData - Données de l'historique
   * @param {string} historiqueData.produit - UUID du produit
   * @param {number} historiqueData.quantite_modifiee - Quantité modifiée
   * @param {string} historiqueData.type_modification - Type (AJOUT ou RETRAIT)
   * @returns {Promise} Historique créé
   */
  createHistoriqueStock(historiqueData) {
    return api.post('historique-stock/', historiqueData);
  },

  /**
   * PUT /api/stocks/historique-stock/{id}/
   * Met à jour un enregistrement d'historique existant (mise à jour complète)
   * @param {string} id - UUID de l'historique
   * @param {Object} historiqueData - Nouvelles données de l'historique
   * @returns {Promise} Historique mis à jour
   */
  updateHistoriqueStock(id, historiqueData) {
    return api.put(`historique-stock/${id}/`, historiqueData);
  },

  /**
   * PATCH /api/stocks/historique-stock/{id}/
   * Met à jour partiellement un enregistrement d'historique existant
   * @param {string} id - UUID de l'historique
   * @param {Object} historiqueData - Données partielles à mettre à jour
   * @returns {Promise} Historique mis à jour
   */
  patchHistoriqueStock(id, historiqueData) {
    return api.patch(`historique-stock/${id}/`, historiqueData);
  },

  /**
   * DELETE /api/stocks/historique-stock/{id}/
   * Supprime un enregistrement d'historique
   * @param {string} id - UUID de l'historique
   * @returns {Promise} Confirmation de suppression
   */
  deleteHistoriqueStock(id) {
    return api.delete(`historique-stock/${id}/`);
  },

  /**
   * GET /api/stocks/historique-stock/par-produit/{produitId}/
   * Récupère l'historique des stocks pour un produit spécifique
   * @param {string} produitId - UUID du produit
   * @returns {Promise} Liste de l'historique du produit
   */
  getHistoriqueByProduit(produitId) {
    return api.get(`historique-stock/par-produit/${produitId}/`);
  },

  /**
   * GET /api/stocks/historique-stock/par-type/{type}/
   * Récupère l'historique par type de modification (AJOUT ou RETRAIT)
   * @param {string} type - Type de modification (AJOUT ou RETRAIT)
   * @returns {Promise} Liste de l'historique par type
   */
  getHistoriqueByType(type) {
    return api.get(`historique-stock/par-type/${type}/`);
  },

  /**
   * GET /api/stocks/historique-stock/par-periode/
   * Récupère l'historique sur une période donnée
   * @param {string} dateDebut - Date de début (YYYY-MM-DD)
   * @param {string} dateFin - Date de fin (YYYY-MM-DD)
   * @returns {Promise} Liste de l'historique sur la période
   */
  getHistoriqueByPeriode(dateDebut, dateFin) {
    return api.get(`historique-stock/par-periode/`, {
      params: { date_debut: dateDebut, date_fin: dateFin }
    });
  }
};

export default historiqueStockAPI;
