import api from '../api/api';

/**
 * Service API pour la gestion des responsables de stock
 * Base URL: http://127.0.0.1:8000/api/stocks/responsables/
 */

const responsablesAPI = {
  /**
   * GET /api/stocks/responsables/
   * Récupère la liste de tous les responsables
   * @returns {Promise} Liste des responsables
   */
  getAllResponsables() {
    return api.get('responsables/');
  },

  /**
   * GET /api/stocks/responsables/{id}/
   * Récupère un responsable spécifique par son ID
   * @param {string} id - UUID du responsable
   * @returns {Promise} Détails du responsable
   */
  getResponsableById(id) {
    return api.get(`responsables/${id}/`);
  },

  /**
   * POST /api/stocks/responsables/
   * Crée un nouveau responsable
   * @param {Object} responsableData - Données du responsable
   * @param {string} responsableData.nom - Nom du responsable
   * @param {string} responsableData.email - Email du responsable
   * @param {string} responsableData.telephone - Téléphone du responsable
   * @returns {Promise} Responsable créé
   */
  createResponsable(responsableData) {
    return api.post('responsables/', responsableData);
  },

  /**
   * PUT /api/stocks/responsables/{id}/
   * Met à jour un responsable existant (mise à jour complète)
   * @param {string} id - UUID du responsable
   * @param {Object} responsableData - Nouvelles données du responsable
   * @returns {Promise} Responsable mis à jour
   */
  updateResponsable(id, responsableData) {
    return api.put(`responsables/${id}/`, responsableData);
  },

  /**
   * PATCH /api/stocks/responsables/{id}/
   * Met à jour partiellement un responsable existant
   * @param {string} id - UUID du responsable
   * @param {Object} responsableData - Données partielles à mettre à jour
   * @returns {Promise} Responsable mis à jour
   */
  patchResponsable(id, responsableData) {
    return api.patch(`responsables/${id}/`, responsableData);
  },

  /**
   * DELETE /api/stocks/responsables/{id}/
   * Supprime un responsable
   * @param {string} id - UUID du responsable
   * @returns {Promise} Confirmation de suppression
   */
  deleteResponsable(id) {
    return api.delete(`responsables/${id}/`);
  },

  /**
   * POST /api/stocks/responsables/{id}/valider-commande/
   * Valide une commande via un responsable
   * @param {string} id - UUID du responsable
   * @param {string} commandeId - UUID de la commande à valider
   * @returns {Promise} Résultat de la validation
   */
  validerCommande(id, commandeId) {
    return api.post(`responsables/${id}/valider-commande/`, { commande_id: commandeId });
  },

  /**
   * GET /api/stocks/responsables/{id}/rapport-inventaire/
   * Consulte le rapport d'inventaire via un responsable
   * @param {string} id - UUID du responsable
   * @returns {Promise} Rapport d'inventaire complet
   */
  consulterRapportInventaire(id) {
    return api.get(`responsables/${id}/rapport-inventaire/`);
  }
};

export default responsablesAPI;
