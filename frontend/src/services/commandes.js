import api from '../api/api';

/**
 * Service API pour la gestion des commandes d'approvisionnement
 * Base URL: http://127.0.0.1:8000/api/stocks/commandes/
 */

const commandesAPI = {
  /**
   * GET /api/stocks/commandes/
   * Récupère la liste de toutes les commandes
   * @returns {Promise} Liste des commandes
   */
  getAllCommandes() {
    return api.get('commandes/');
  },

  /**
   * GET /api/stocks/commandes/{id}/
   * Récupère une commande spécifique par son ID
   * @param {string} id - UUID de la commande
   * @returns {Promise} Détails de la commande
   */
  getCommandeById(id) {
    return api.get(`commandes/${id}/`);
  },

  /**
   * POST /api/stocks/commandes/
   * Crée une nouvelle commande
   * @param {Object} commandeData - Données de la commande
   * @param {string} commandeData.fournisseur - UUID du fournisseur
   * @param {string} commandeData.date_livraison_prevue - Date de livraison prévue (ISO format)
   * @param {string} commandeData.statut - Statut (EN_COURS, LIVREE, ANNULEE)
   * @returns {Promise} Commande créée
   */
  createCommande(commandeData) {
    return api.post('commandes/', commandeData);
  },

  /**
   * PUT /api/stocks/commandes/{id}/
   * Met à jour une commande existante (mise à jour complète)
   * @param {string} id - UUID de la commande
   * @param {Object} commandeData - Nouvelles données de la commande
   * @returns {Promise} Commande mise à jour
   */
  updateCommande(id, commandeData) {
    return api.put(`commandes/${id}/`, commandeData);
  },

  /**
   * PATCH /api/stocks/commandes/{id}/
   * Met à jour partiellement une commande existante
   * @param {string} id - UUID de la commande
   * @param {Object} commandeData - Données partielles à mettre à jour
   * @returns {Promise} Commande mise à jour
   */
  patchCommande(id, commandeData) {
    return api.patch(`commandes/${id}/`, commandeData);
  },

  /**
   * DELETE /api/stocks/commandes/{id}/
   * Supprime une commande
   * @param {string} id - UUID de la commande
   * @returns {Promise} Confirmation de suppression
   */
  deleteCommande(id) {
    return api.delete(`commandes/${id}/`);
  },

  /**
   * POST /api/stocks/commandes/{id}/valider/
   * Valide une commande (change le statut en LIVREE)
   * @param {string} id - UUID de la commande
   * @returns {Promise} Commande validée
   */
  validerCommande(id) {
    return api.post(`commandes/${id}/valider/`);
  },

  /**
   * POST /api/stocks/commandes/{id}/annuler/
   * Annule une commande (change le statut en ANNULEE)
   * @param {string} id - UUID de la commande
   * @returns {Promise} Commande annulée
   */
  annulerCommande(id) {
    return api.post(`commandes/${id}/annuler/`);
  },

  /**
   * GET /api/stocks/commandes/{id}/montant-total/
   * Calcule le montant total de la commande
   * @param {string} id - UUID de la commande
   * @returns {Promise} Montant total
   */
  getMontantTotal(id) {
    return api.get(`commandes/${id}/montant-total/`);
  }
};

export default commandesAPI;
