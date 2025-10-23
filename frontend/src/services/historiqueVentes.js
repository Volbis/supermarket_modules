import api from '../api/api';

/**
 * Service API pour la gestion de l'historique des ventes
 * Base URL: http://127.0.0.1:8000/api/stocks/historique-ventes/
 */

const historiqueVentesAPI = {
  /**
   * GET /api/stocks/historique-ventes/
   * Récupère la liste complète de l'historique des ventes
   * @returns {Promise} Liste de l'historique des ventes
   */
  getAllHistoriqueVentes() {
    return api.get('historique-ventes/');
  },

  /**
   * GET /api/stocks/historique-ventes/{id}/
   * Récupère un enregistrement de vente spécifique par son ID
   * @param {string} id - UUID de l'historique de vente
   * @returns {Promise} Détails de la vente
   */
  getHistoriqueVenteById(id) {
    return api.get(`historique-ventes/${id}/`);
  },

  /**
   * POST /api/stocks/historique-ventes/
   * Crée un nouveau enregistrement de vente
   * @param {Object} venteData - Données de la vente
   * @param {string} venteData.produit - UUID du produit
   * @param {number} venteData.quantite_vendue - Quantité vendue
   * @param {number} venteData.montant_total - Montant total de la vente
   * @param {number} venteData.chiffre_affaires_journalier - Chiffre d'affaires journalier (optionnel)
   * @returns {Promise} Historique de vente créé
   */
  createHistoriqueVente(venteData) {
    return api.post('historique-ventes/', venteData);
  },

  /**
   * PUT /api/stocks/historique-ventes/{id}/
   * Met à jour un enregistrement de vente existant (mise à jour complète)
   * @param {string} id - UUID de l'historique de vente
   * @param {Object} venteData - Nouvelles données de la vente
   * @returns {Promise} Historique de vente mis à jour
   */
  updateHistoriqueVente(id, venteData) {
    return api.put(`historique-ventes/${id}/`, venteData);
  },

  /**
   * PATCH /api/stocks/historique-ventes/{id}/
   * Met à jour partiellement un enregistrement de vente existant
   * @param {string} id - UUID de l'historique de vente
   * @param {Object} venteData - Données partielles à mettre à jour
   * @returns {Promise} Historique de vente mis à jour
   */
  patchHistoriqueVente(id, venteData) {
    return api.patch(`historique-ventes/${id}/`, venteData);
  },

  /**
   * DELETE /api/stocks/historique-ventes/{id}/
   * Supprime un enregistrement de vente
   * @param {string} id - UUID de l'historique de vente
   * @returns {Promise} Confirmation de suppression
   */
  deleteHistoriqueVente(id) {
    return api.delete(`historique-ventes/${id}/`);
  },

  /**
   * GET /api/stocks/historique-ventes/par-produit/{produitId}/
   * Récupère l'historique des ventes pour un produit spécifique
   * @param {string} produitId - UUID du produit
   * @returns {Promise} Liste de l'historique des ventes du produit
   */
  getVentesByProduit(produitId) {
    return api.get(`historique-ventes/par-produit/${produitId}/`);
  },

  /**
   * GET /api/stocks/historique-ventes/par-periode/
   * Récupère l'historique des ventes sur une période donnée
   * @param {string} dateDebut - Date de début (YYYY-MM-DD)
   * @param {string} dateFin - Date de fin (YYYY-MM-DD)
   * @returns {Promise} Liste de l'historique des ventes sur la période
   */
  getVentesByPeriode(dateDebut, dateFin) {
    return api.get(`historique-ventes/par-periode/`, {
      params: { date_debut: dateDebut, date_fin: dateFin }
    });
  },

  /**
   * GET /api/stocks/historique-ventes/{id}/tendance/
   * Calcule la tendance des ventes pour un enregistrement
   * @param {string} id - UUID de l'historique de vente
   * @returns {Promise} Tendance des ventes
   */
  getTendanceVente(id) {
    return api.get(`historique-ventes/${id}/tendance/`);
  },

  /**
   * GET /api/stocks/historique-ventes/{id}/prevision-demande/
   * Prévoit la demande future basée sur l'historique
   * @param {string} id - UUID de l'historique de vente
   * @returns {Promise} Prévision de demande
   */
  getProvisionDemande(id) {
    return api.get(`historique-ventes/${id}/prevision-demande/`);
  },

  /**
   * GET /api/stocks/historique-ventes/chiffre-affaires-total/
   * Calcule le chiffre d'affaires total sur une période
   * @param {string} dateDebut - Date de début (YYYY-MM-DD)
   * @param {string} dateFin - Date de fin (YYYY-MM-DD)
   * @returns {Promise} Chiffre d'affaires total
   */
  getChiffAffairesTotal(dateDebut, dateFin) {
    return api.get(`historique-ventes/chiffre-affaires-total/`, {
      params: { date_debut: dateDebut, date_fin: dateFin }
    });
  }
};

export default historiqueVentesAPI;
