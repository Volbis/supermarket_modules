import api from '../api/api';

/**
 * Service API pour la gestion des stocks
 * Base URL: http://127.0.0.1:8000/api/stocks/stocks/
 */

const stocksAPI = {
  /**
   * GET /api/stocks/stocks/
   * Récupère la liste de tous les stocks
   * @returns {Promise} Liste des stocks
   */
  getAllStocks() {
    return api.get('stocks/');
  },

  /**
   * GET /api/stocks/stocks/{id}/
   * Récupère un stock spécifique par son ID
   * @param {string} id - UUID du stock
   * @returns {Promise} Détails du stock
   */
  getStockById(id) {
    return api.get(`stocks/${id}/`);
  },

  /**
   * POST /api/stocks/stocks/
   * Crée un nouveau stock
   * @param {Object} stockData - Données du stock
   * @param {string} stockData.produit - UUID du produit
   * @param {number} stockData.quantite - Quantité en stock
   * @returns {Promise} Stock créé
   */
  createStock(stockData) {
    return api.post('stocks/', stockData);
  },

  /**
   * PUT /api/stocks/stocks/{id}/
   * Met à jour un stock existant (mise à jour complète)
   * @param {string} id - UUID du stock
   * @param {Object} stockData - Nouvelles données du stock
   * @returns {Promise} Stock mis à jour
   */
  updateStock(id, stockData) {
    return api.put(`stocks/${id}/`, stockData);
  },

  /**
   * PATCH /api/stocks/stocks/{id}/
   * Met à jour partiellement un stock existant
   * @param {string} id - UUID du stock
   * @param {Object} stockData - Données partielles à mettre à jour
   * @returns {Promise} Stock mis à jour
   */
  patchStock(id, stockData) {
    return api.patch(`stocks/${id}/`, stockData);
  },

  /**
   * DELETE /api/stocks/stocks/{id}/
   * Supprime un stock
   * @param {string} id - UUID du stock
   * @returns {Promise} Confirmation de suppression
   */
  deleteStock(id) {
    return api.delete(`stocks/${id}/`);
  },

  /**
   * POST /api/stocks/stocks/{id}/ajouter/
   * Ajoute une quantité au stock
   * @param {string} id - UUID du stock
   * @param {number} quantite - Quantité à ajouter
   * @returns {Promise} Stock mis à jour
   */
  ajouterStock(id, quantite) {
    return api.post(`stocks/${id}/ajouter/`, { quantite });
  },

  /**
   * POST /api/stocks/stocks/{id}/retirer/
   * Retire une quantité du stock
   * @param {string} id - UUID du stock
   * @param {number} quantite - Quantité à retirer
   * @returns {Promise} Stock mis à jour
   */
  retirerStock(id, quantite) {
    return api.post(`stocks/${id}/retirer/`, { quantite });
  }
};

export default stocksAPI;
