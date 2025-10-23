import api from '../api/api';

/**
 * Service API pour la gestion des produits
 * Base URL: http://127.0.0.1:8000/api/stocks/produits/
 */

const produitsAPI = {
  /**
   * GET /api/stocks/produits/
   * Récupère la liste de tous les produits
   * @returns {Promise} Liste des produits
   */
  getAllProduits() {
    return api.get('produits/');
  },

  /**
   * GET /api/stocks/produits/{id}/
   * Récupère un produit spécifique par son ID
   * @param {string} id - UUID du produit
   * @returns {Promise} Détails du produit
   */
  getProduitById(id) {
    return api.get(`produits/${id}/`);
  },

  /**
   * POST /api/stocks/produits/
   * Crée un nouveau produit
   * @param {Object} produitData - Données du produit
   * @param {string} produitData.nom - Nom du produit
   * @param {string} produitData.reference - Référence unique
   * @param {string} produitData.designation - Description du produit
   * @param {number} produitData.prix_unitaire - Prix unitaire
   * @param {number} produitData.quantite_en_stock - Quantité en stock
   * @param {number} produitData.seuil_de_reapprovisionnement - Seuil de réapprovisionnement
   * @param {string} produitData.date_de_peremption - Date de péremption (YYYY-MM-DD)
   * @param {string} produitData.categorie - UUID de la catégorie
   * @param {string} produitData.fournisseur - UUID du fournisseur
   * @returns {Promise} Produit créé
   */
  createProduit(produitData) {
    return api.post('produits/', produitData);
  },

  /**
   * PUT /api/stocks/produits/{id}/
   * Met à jour un produit existant (mise à jour complète)
   * @param {string} id - UUID du produit
   * @param {Object} produitData - Nouvelles données du produit
   * @returns {Promise} Produit mis à jour
   */
  updateProduit(id, produitData) {
    return api.put(`produits/${id}/`, produitData);
  },

  /**
   * PATCH /api/stocks/produits/{id}/
   * Met à jour partiellement un produit existant
   * @param {string} id - UUID du produit
   * @param {Object} produitData - Données partielles à mettre à jour
   * @returns {Promise} Produit mis à jour
   */
  patchProduit(id, produitData) {
    return api.patch(`produits/${id}/`, produitData);
  },

  /**
   * DELETE /api/stocks/produits/{id}/
   * Supprime un produit
   * @param {string} id - UUID du produit
   * @returns {Promise} Confirmation de suppression
   */
  deleteProduit(id) {
    return api.delete(`produits/${id}/`);
  },

  /**
   * GET /api/stocks/produits/sous-seuil/
   * Récupère les produits sous le seuil de réapprovisionnement
   * @returns {Promise} Liste des produits sous seuil
   */
  getProduitsSousSeuil() {
    return api.get('produits/sous-seuil/');
  },

  /**
   * GET /api/stocks/produits/perimes/
   * Récupère les produits périmés
   * @returns {Promise} Liste des produits périmés
   */
  getProduitsPerimes() {
    return api.get('produits/perimes/');
  }
};

export default produitsAPI;
