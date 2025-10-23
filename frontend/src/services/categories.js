import api from '../api/api';

/**
 * Service API pour la gestion des catégories
 * Base URL: http://127.0.0.1:8000/api/stocks/categories/
 */

const categoriesAPI = {
  /**
   * GET /api/stocks/categories/
   * Récupère la liste de toutes les catégories
   * @returns {Promise} Liste des catégories
   */
  getAllCategories() {
    return api.get('categories/');
  },

  /**
   * GET /api/stocks/categories/{id}/
   * Récupère une catégorie spécifique par son ID
   * @param {string} id - UUID de la catégorie
   * @returns {Promise} Détails de la catégorie
   */
  getCategoryById(id) {
    return api.get(`categories/${id}/`);
  },

  /**
   * POST /api/stocks/categories/
   * Crée une nouvelle catégorie
   * @param {Object} categoryData - Données de la catégorie
   * @param {string} categoryData.nom - Nom de la catégorie
   * @param {string} categoryData.description - Description de la catégorie
   * @returns {Promise} Catégorie créée
   */
  createCategory(categoryData) {
    return api.post('categories/', categoryData);
  },

  /**
   * PUT /api/stocks/categories/{id}/
   * Met à jour une catégorie existante (mise à jour complète)
   * @param {string} id - UUID de la catégorie
   * @param {Object} categoryData - Nouvelles données de la catégorie
   * @returns {Promise} Catégorie mise à jour
   */
  updateCategory(id, categoryData) {
    return api.put(`categories/${id}/`, categoryData);
  },

  /**
   * PATCH /api/stocks/categories/{id}/
   * Met à jour partiellement une catégorie existante
   * @param {string} id - UUID de la catégorie
   * @param {Object} categoryData - Données partielles à mettre à jour
   * @returns {Promise} Catégorie mise à jour
   */
  patchCategory(id, categoryData) {
    return api.patch(`categories/${id}/`, categoryData);
  },

  /**
   * DELETE /api/stocks/categories/{id}/
   * Supprime une catégorie
   * @param {string} id - UUID de la catégorie
   * @returns {Promise} Confirmation de suppression
   */
  deleteCategory(id) {
    return api.delete(`categories/${id}/`);
  },

  /**
   * GET /api/stocks/categories/{id}/produits/
   * Récupère tous les produits d'une catégorie spécifique
   * @param {string} id - UUID de la catégorie
   * @returns {Promise} Liste des produits de la catégorie
   */
  getCategoryProducts(id) {
    return api.get(`categories/${id}/produits/`);
  }
};

export default categoriesAPI;
