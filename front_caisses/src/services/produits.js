/**
 * Service API pour la gestion des produits (réutilisé depuis le module stocks)
 * 
 * Endpoints:
 * - GET  /products - Récupérer tous les produits
 * - GET  /products/:id - Récupérer un produit par ID
 * - GET  /products/barcode/:barcode - Récupérer un produit par code-barres
 * - GET  /products/search - Rechercher des produits
 */

import apiClient from '@/api/api';

const ENDPOINT = '/produits';

export default {
  /**
   * Récupérer tous les produits
   * @returns {Promise}
   */
  getAllProduits() {
    return apiClient.get(ENDPOINT);
  },

  /**
   * Récupérer un produit par ID
   * @param {string} id - ID du produit
   * @returns {Promise}
   */
  getProduitById(id) {
    return apiClient.get(`${ENDPOINT}/${id}`);
  },

  /**
   * Rechercher un produit par code-barres
   * @param {string} barcode - Code-barres du produit
   * @returns {Promise}
   */
  getProduitByBarcode(barcode) {
    return apiClient.get(`${ENDPOINT}/barcode/${barcode}`);
  },

  /**
   * Rechercher des produits par nom
   * @param {string} query - Terme de recherche
   * @returns {Promise}
   */
  searchProduits(query) {
    return apiClient.get(`${ENDPOINT}/search`, {
      params: { q: query }
    });
  },

  /**
   * Récupérer les produits par catégorie
   * @param {string} categoryId - ID de la catégorie
   * @returns {Promise}
   */
  getProduitsByCategory(categoryId) {
    return apiClient.get(`${ENDPOINT}/category/${categoryId}`);
  },

  /**
   * Vérifier la disponibilité d'un produit
   * @param {string} productId - ID du produit
   * @param {number} quantity - Quantité demandée
   * @returns {Promise}
   */
  checkProductAvailability(productId, quantity) {
    return apiClient.post(`${ENDPOINT}/${productId}/check-availability`, {
      quantity: quantity
    });
  },

  /**
   * Mettre à jour le stock après une vente
   * @param {string} productId - ID du produit
   * @param {number} quantity - Quantité vendue
   * @returns {Promise}
   */
  updateStockAfterSale(productId, quantity) {
    return apiClient.post(`${ENDPOINT}/${productId}/update-stock`, {
      quantity: -quantity,
      type: 'sale'
    });
  }
};
