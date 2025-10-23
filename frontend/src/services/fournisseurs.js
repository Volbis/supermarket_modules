import api from '../api/api';

/**
 * Service API pour la gestion des fournisseurs
 * Base URL: http://127.0.0.1:8000/api/stocks/fournisseurs/
 */

const fournisseursAPI = {
  /**
   * GET /api/stocks/fournisseurs/
   * Récupère la liste de tous les fournisseurs
   * @returns {Promise} Liste des fournisseurs
   */
  getAllFournisseurs() {
    return api.get('fournisseurs/');
  },

  /**
   * GET /api/stocks/fournisseurs/{id}/
   * Récupère un fournisseur spécifique par son ID
   * @param {string} id - UUID du fournisseur
   * @returns {Promise} Détails du fournisseur
   */
  getFournisseurById(id) {
    return api.get(`fournisseurs/${id}/`);
  },

  /**
   * POST /api/stocks/fournisseurs/
   * Crée un nouveau fournisseur
   * @param {Object} fournisseurData - Données du fournisseur
   * @param {string} fournisseurData.nom - Nom du fournisseur
   * @param {string} fournisseurData.contact - Contact du fournisseur
   * @param {string} fournisseurData.adresse - Adresse du fournisseur
   * @param {string} fournisseurData.catalogue_produits - Catalogue des produits
   * @param {number} fournisseurData.delais_livraison_jours - Délais de livraison en jours
   * @returns {Promise} Fournisseur créé
   */
  createFournisseur(fournisseurData) {
    return api.post('fournisseurs/', fournisseurData);
  },

  /**
   * PUT /api/stocks/fournisseurs/{id}/
   * Met à jour un fournisseur existant (mise à jour complète)
   * @param {string} id - UUID du fournisseur
   * @param {Object} fournisseurData - Nouvelles données du fournisseur
   * @returns {Promise} Fournisseur mis à jour
   */
  updateFournisseur(id, fournisseurData) {
    return api.put(`fournisseurs/${id}/`, fournisseurData);
  },

  /**
   * PATCH /api/stocks/fournisseurs/{id}/
   * Met à jour partiellement un fournisseur existant
   * @param {string} id - UUID du fournisseur
   * @param {Object} fournisseurData - Données partielles à mettre à jour
   * @returns {Promise} Fournisseur mis à jour
   */
  patchFournisseur(id, fournisseurData) {
    return api.patch(`fournisseurs/${id}/`, fournisseurData);
  },

  /**
   * DELETE /api/stocks/fournisseurs/{id}/
   * Supprime un fournisseur
   * @param {string} id - UUID du fournisseur
   * @returns {Promise} Confirmation de suppression
   */
  deleteFournisseur(id) {
    return api.delete(`fournisseurs/${id}/`);
  },

  /**
   * GET /api/stocks/fournisseurs/{id}/produits/
   * Récupère tous les produits fournis par un fournisseur
   * @param {string} id - UUID du fournisseur
   * @returns {Promise} Liste des produits du fournisseur
   */
  getFournisseurProduits(id) {
    return api.get(`fournisseurs/${id}/produits/`);
  }
};

export default fournisseursAPI;
