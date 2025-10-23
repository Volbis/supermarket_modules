import api from '../api/api';

/**
 * Service API pour la gestion des alertes de stock
 * Base URL: http://127.0.0.1:8000/api/stocks/alertes/
 */

const alertesAPI = {
  /**
   * GET /api/stocks/alertes/
   * Récupère la liste de toutes les alertes
   * @returns {Promise} Liste des alertes
   */
  getAllAlertes() {
    return api.get('alertes/');
  },

  /**
   * GET /api/stocks/alertes/{id}/
   * Récupère une alerte spécifique par son ID
   * @param {string} id - UUID de l'alerte
   * @returns {Promise} Détails de l'alerte
   */
  getAlerteById(id) {
    return api.get(`alertes/${id}/`);
  },

  /**
   * POST /api/stocks/alertes/
   * Crée une nouvelle alerte
   * @param {Object} alerteData - Données de l'alerte
   * @param {string} alerteData.produit - UUID du produit
   * @param {string} alerteData.message - Message de l'alerte
   * @returns {Promise} Alerte créée
   */
  createAlerte(alerteData) {
    return api.post('alertes/', alerteData);
  },

  /**
   * PUT /api/stocks/alertes/{id}/
   * Met à jour une alerte existante (mise à jour complète)
   * @param {string} id - UUID de l'alerte
   * @param {Object} alerteData - Nouvelles données de l'alerte
   * @returns {Promise} Alerte mise à jour
   */
  updateAlerte(id, alerteData) {
    return api.put(`alertes/${id}/`, alerteData);
  },

  /**
   * PATCH /api/stocks/alertes/{id}/
   * Met à jour partiellement une alerte existante
   * @param {string} id - UUID de l'alerte
   * @param {Object} alerteData - Données partielles à mettre à jour
   * @returns {Promise} Alerte mise à jour
   */
  patchAlerte(id, alerteData) {
    return api.patch(`alertes/${id}/`, alerteData);
  },

  /**
   * DELETE /api/stocks/alertes/{id}/
   * Supprime une alerte
   * @param {string} id - UUID de l'alerte
   * @returns {Promise} Confirmation de suppression
   */
  deleteAlerte(id) {
    return api.delete(`alertes/${id}/`);
  },

  /**
   * GET /api/stocks/alertes/dashboard/
   * Récupère les statistiques du dashboard
   * @returns {Promise} Statistiques des alertes
   */
  getDashboardStats() {
    return api.get('alertes/dashboard/');
  },

  /**
   * GET /api/stocks/alertes/critiques/list/
   * Récupère uniquement les alertes critiques
   * @returns {Promise} Liste des alertes critiques
   */
  getAlertesCritiques() {
    return api.get('alertes/critiques/list/');
  },

  /**
   * GET /api/stocks/alertes/recentes/list/
   * Récupère les alertes des dernières 24 heures
   * @returns {Promise} Liste des alertes récentes
   */
  getAlertesRecentes() {
    return api.get('alertes/recentes/list/');
  },

  /**
   * GET /api/stocks/alertes/par-type/list/?type={type}
   * Récupère les alertes filtrées par type
   * @param {string} type - Type d'alerte (stock_critique, peremption, commandes, forte_demande, prix)
   * @returns {Promise} Liste des alertes du type spécifié
   */
  getAlertesByType(type) {
    return api.get('alertes/par-type/list/', {
      params: { type }
    });
  },

  /**
   * GET /api/stocks/alertes/par-priorite/list/?priorite={priorite}
   * Récupère les alertes filtrées par priorité
   * @param {string} priorite - Priorité (critique, haute, moyenne, basse)
   * @returns {Promise} Liste des alertes de la priorité spécifiée
   */
  getAlertesByPriorite(priorite) {
    return api.get('alertes/par-priorite/list/', {
      params: { priorite }
    });
  },

  /**
   * GET /api/stocks/alertes/par-produit/list/?produit_id={produitId}
   * Récupère toutes les alertes d'un produit spécifique
   * @param {string} produitId - UUID du produit
   * @returns {Promise} Liste des alertes du produit
   */
  getAlertesByProduit(produitId) {
    return api.get('alertes/par-produit/list/', {
      params: { produit_id: produitId }
    });
  },

  /**
   * POST /api/stocks/alertes/{id}/marquer-resolue/
   * Marquer une alerte comme résolue (la supprimer)
   * @param {string} id - UUID de l'alerte
   * @returns {Promise} Confirmation de résolution
   */
  markAsResolved(id) {
    return api.post(`alertes/${id}/marquer-resolue/`);
  },

  /**
   * POST /api/stocks/alertes/marquer-toutes-resolues/
   * Marquer toutes les alertes comme résolues (les supprimer)
   * @param {Object} data - Données optionnelles
   * @param {string} data.type - Type de filtre optionnel (stock_critique, peremption, commandes)
   * @returns {Promise} Confirmation de résolution
   */
  markAllAsResolved(data = {}) {
    return api.post('alertes/marquer-toutes-resolues/', data);
  },

  /**
   * Méthode helper pour obtenir le nombre d'alertes par catégorie
   * @returns {Promise} Statistiques des catégories
   */
  async getCategories() {
    const response = await this.getDashboardStats();
    const stats = response.data;
    
    return {
      toutes: stats.statistiques.total_alertes,
      critiques: stats.par_priorite.critique,
      stock: stats.par_type.stock_critique,
      peremption: stats.par_type.peremption,
      commandes: stats.par_type.commandes,
      forteDemande: stats.par_type.forte_demande,
      prix: stats.par_type.prix
    };
  },

  /**
   * Méthode helper pour filtrer les alertes localement
   * @param {Array} alertes - Liste des alertes
   * @param {string} type - Type de filtre
   * @returns {Array} Alertes filtrées
   */
  filterByType(alertes, type) {
    const filters = {
      'critique': (a) => a.message.includes('CRITIQUE') || a.message.includes('🔴') || a.message.includes('⛔'),
      'stock': (a) => a.message.includes('STOCK') || a.message.includes('RUPTURE'),
      'peremption': (a) => a.message.includes('PÉRIMÉ') || a.message.includes('PÉREMPTION'),
      'commandes': (a) => a.message.includes('COMMANDE') || a.message.includes('RETARD'),
      'forte_demande': (a) => a.message.includes('FORTE DEMANDE'),
      'prix': (a) => a.message.includes('PRIX')
    };

    return filters[type] ? alertes.filter(filters[type]) : alertes;
  },

  /**
   * Méthode helper pour obtenir la priorité d'une alerte
   * @param {Object} alerte - Alerte
   * @returns {string} Priorité (critique, haute, moyenne, basse)
   */
  getPriority(alerte) {
    if (alerte.message.includes('🔴') || alerte.message.includes('⛔') || alerte.message.includes('CRITIQUE')) {
      return 'critique';
    }
    if (alerte.message.includes('🟠') || alerte.message.includes('HAUTE')) {
      return 'haute';
    }
    if (alerte.message.includes('🟡') || alerte.message.includes('⚠️')) {
      return 'moyenne';
    }
    return 'basse';
  },

  /**
   * Méthode helper pour formater une alerte pour l'affichage
   * @param {Object} alerte - Alerte brute de l'API
   * @returns {Object} Alerte formatée
   */
  formatAlerte(alerte) {
    return {
      ...alerte,
      priority: this.getPriority(alerte),
      type: this.getType(alerte),
      icon: this.getIcon(alerte),
      title: this.getTitle(alerte)
    };
  },

  /**
   * Méthode helper pour obtenir le type d'une alerte
   * @param {Object} alerte - Alerte
   * @returns {string} Type d'alerte
   */
  getType(alerte) {
    if (alerte.message.includes('STOCK CRITIQUE') || alerte.message.includes('RUPTURE')) return 'stock';
    if (alerte.message.includes('PÉRIMÉ') || alerte.message.includes('PÉREMPTION')) return 'peremption';
    if (alerte.message.includes('RETARD COMMANDE')) return 'commandes';
    if (alerte.message.includes('FORTE DEMANDE')) return 'forte_demande';
    if (alerte.message.includes('PRIX')) return 'prix';
    return 'autre';
  },

  /**
   * Méthode helper pour obtenir l'icône d'une alerte
   * @param {Object} alerte - Alerte
   * @returns {string} Emoji icône
   */
  getIcon(alerte) {
    if (alerte.message.includes('🔴')) return '🔴';
    if (alerte.message.includes('⛔')) return '⛔';
    if (alerte.message.includes('🟠')) return '🟠';
    if (alerte.message.includes('🟡')) return '🟡';
    if (alerte.message.includes('⚠️')) return '⚠️';
    if (alerte.message.includes('📈')) return '📈';
    if (alerte.message.includes('⏰')) return '⏰';
    return '📋';
  },

  /**
   * Méthode helper pour obtenir le titre d'une alerte
   * @param {Object} alerte - Alerte
   * @returns {string} Titre
   */
  getTitle(alerte) {
    if (alerte.message.includes('STOCK CRITIQUE')) return 'Stock Critique';
    if (alerte.message.includes('RUPTURE DE STOCK')) return 'Rupture de Stock';
    if (alerte.message.includes('PRODUIT PÉRIMÉ')) return 'Produit Périmé';
    if (alerte.message.includes('PÉREMPTION IMMINENTE')) return 'Péremption Imminente';
    if (alerte.message.includes('PÉREMPTION PROCHE')) return 'Péremption Proche';
    if (alerte.message.includes('RETARD COMMANDE')) return 'Retard de Commande';
    if (alerte.message.includes('FORTE DEMANDE')) return 'Forte Demande';
    if (alerte.message.includes('SEUIL ATTEINT')) return 'Seuil Atteint';
    if (alerte.message.includes('CHANGEMENT DE PRIX')) return 'Changement de Prix';
    return 'Notification';
  }
};

export default alertesAPI;