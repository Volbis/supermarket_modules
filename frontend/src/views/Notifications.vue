<template>
  <div class="notifications-container">
    <!-- Loader -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Chargement des notifications...</p>
    </div>

    <!-- Header avec bouton refresh -->
    <div class="notifications-header">
      <div>
        <h1>Notifications</h1>
        <p class="subtitle">{{ totalAlertes }} notification(s) au total</p>
      </div>
      <button @click="refreshNotifications" class="refresh-btn" :disabled="loading">
        <span class="refresh-icon">🔄</span>
        Actualiser
      </button>
    </div>

    <!-- Tabs de catégories -->
    <div class="tabs-container">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
        <span v-if="getUnreadCount(tab.id) > 0" class="badge">
          {{ getUnreadCount(tab.id) }}
        </span>
      </button>
    </div>

    <!-- Statistiques Dashboard (uniquement pour l'onglet "Toutes") -->
    <div v-if="activeTab === 'all' && dashboardStats" class="dashboard-stats">
      <div class="stat-card">
        <span class="stat-icon">📊</span>
        <div class="stat-content">
          <p class="stat-value">{{ dashboardStats.statistiques.total_alertes }}</p>
          <p class="stat-label">Total alertes</p>
        </div>
      </div>
      <div class="stat-card">
        <span class="stat-icon">🔴</span>
        <div class="stat-content">
          <p class="stat-value">{{ dashboardStats.par_priorite.critique }}</p>
          <p class="stat-label">Critiques</p>
        </div>
      </div>
      <div class="stat-card">
        <span class="stat-icon">📦</span>
        <div class="stat-content">
          <p class="stat-value">{{ dashboardStats.par_type.stock_critique }}</p>
          <p class="stat-label">Stock critique</p>
        </div>
      </div>
      <div class="stat-card">
        <span class="stat-icon">⏰</span>
        <div class="stat-content">
          <p class="stat-value">{{ dashboardStats.par_type.peremption }}</p>
          <p class="stat-label">Péremption</p>
        </div>
      </div>
    </div>

    <!-- Filtres par priorité -->
    <div class="filters-container">
      <button 
        v-for="filter in priorityFilters" 
        :key="filter.id"
        :class="['filter-btn', { active: activePriorityFilter === filter.id }]"
        @click="activePriorityFilter = filter.id"
      >
        <span>{{ filter.icon }}</span>
        {{ filter.label }}
      </button>
    </div>

    <!-- Liste des notifications -->
    <div class="notifications-content">
      <div v-if="error" class="error-message">
        <span class="error-icon">⚠️</span>
        <p>{{ error }}</p>
        <button @click="refreshNotifications" class="retry-btn">Réessayer</button>
      </div>

      <div v-else-if="filteredNotifications.length > 0" class="notifications-list">
        <div 
          v-for="notification in paginatedNotifications" 
          :key="notification.id_alert"
          :class="['notification-card', getPriorityClass(notification.message)]"
        >
          <!-- Indicateur de priorité -->
          <div class="priority-indicator" :style="{ backgroundColor: getPriorityColor(notification.message) }"></div>

          <!-- Contenu de la notification -->
          <div class="notification-body">
            <div class="notification-main">
              <div class="notification-icon">
                <span>{{ getNotificationIcon(notification.message) }}</span>
              </div>
              
              <div class="notification-content">
                <h4 class="notification-title">{{ getNotificationTitle(notification.message) }}</h4>
                <p class="notification-message">{{ notification.message }}</p>
                <div class="notification-product">
                  <span class="product-badge">{{ notification.produit_details?.nom }}</span>
                  <span class="product-ref">Réf: {{ notification.produit_details?.reference }}</span>
                </div>
              </div>
            </div>

            <div class="notification-meta">
              <span class="notification-time">{{ formatDate(notification.date_creation) }}</span>
              <div class="notification-actions">
                <button 
                  @click="viewProductDetails(notification.produit)"
                  class="action-btn view-btn"
                  title="Voir le produit"
                >
                  👁️ Voir
                </button>
                <button 
                  @click="markAsResolved(notification.id_alert)"
                  class="action-btn resolve-btn"
                  title="Marquer comme résolu"
                  :disabled="resolvingAlerts.includes(notification.id_alert)"
                >
                  ✓ Résoudre
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1"
            class="pagination-btn"
          >
            ← Précédent
          </button>
          <span class="pagination-info">
            Page {{ currentPage }} sur {{ totalPages }}
          </span>
          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            class="pagination-btn"
          >
            Suivant →
          </button>
        </div>
      </div>

      <!-- Message si aucune notification -->
      <div v-else class="empty-state-main">
        <div class="empty-icon">📭</div>
        <h3>Aucune notification</h3>
        <p>Vous êtes à jour ! Aucune nouvelle notification pour le moment.</p>
      </div>
    </div>

    <!-- Bouton pour tout marquer comme résolu -->
    <div v-if="filteredNotifications.length > 0" class="bulk-actions">
      <button 
        @click="markAllAsResolved"
        class="bulk-action-btn"
        :disabled="resolvingAll"
      >
        <span v-if="!resolvingAll">✓ Tout marquer comme résolu</span>
        <span v-else>⏳ Traitement en cours...</span>
      </button>
    </div>
  </div>
</template>

<script>
import alertesAPI from '@/services/alertes';

export default {
  name: 'NotificationsView',
  data() {
    return {
      activeTab: 'all',
      activePriorityFilter: 'all',
      loading: false,
      error: null,
      resolvingAlerts: [],
      resolvingAll: false,
      currentPage: 1,
      itemsPerPage: 10,
      tabs: [
        { id: 'all', label: 'Toutes' },
        { id: 'critique', label: 'Critiques' },
        { id: 'stock', label: 'Stock' },
        { id: 'peremption', label: 'Péremption' },
        { id: 'commandes', label: 'Commandes' }
      ],
      priorityFilters: [
        { id: 'all', label: 'Toutes', icon: '📋' },
        { id: 'critique', label: 'Critique', icon: '🔴' },
        { id: 'haute', label: 'Haute', icon: '🟠' },
        { id: 'moyenne', label: 'Moyenne', icon: '🟡' },
        { id: 'basse', label: 'Basse', icon: '⏰' }
      ],
      notifications: [],
      dashboardStats: null
    }
  },
  computed: {
    filteredNotifications() {
      let filtered = this.notifications;

      // Filtrer par type (onglet)
      if (this.activeTab !== 'all') {
        const typeFilters = {
          'critique': (n) => n.message.includes('CRITIQUE') || n.message.includes('🔴') || n.message.includes('⛔'),
          'stock': (n) => n.message.includes('STOCK') || n.message.includes('RUPTURE'),
          'peremption': (n) => n.message.includes('PÉRIMÉ') || n.message.includes('PÉREMPTION'),
          'commandes': (n) => n.message.includes('COMMANDE') || n.message.includes('RETARD')
        };
        
        if (typeFilters[this.activeTab]) {
          filtered = filtered.filter(typeFilters[this.activeTab]);
        }
      }

      // Filtrer par priorité
      if (this.activePriorityFilter !== 'all') {
        const priorityFilters = {
          'critique': (n) => n.message.includes('🔴') || n.message.includes('⛔') || n.message.includes('CRITIQUE'),
          'haute': (n) => n.message.includes('🟠') || n.message.includes('HAUTE'),
          'moyenne': (n) => n.message.includes('🟡') || n.message.includes('⚠️'),
          'basse': (n) => n.message.includes('⏰') || n.message.includes('BASSE')
        };
        
        if (priorityFilters[this.activePriorityFilter]) {
          filtered = filtered.filter(priorityFilters[this.activePriorityFilter]);
        }
      }

      return filtered;
    },
    paginatedNotifications() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredNotifications.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredNotifications.length / this.itemsPerPage);
    },
    totalAlertes() {
      return this.notifications.length;
    }
  },
  methods: {
    async loadNotifications() {
      this.loading = true;
      this.error = null;
      try {
        const response = await alertesAPI.getAllAlertes();
        this.notifications = response.data;
      } catch (err) {
        this.error = 'Erreur lors du chargement des notifications. Veuillez réessayer.';
        console.error('Erreur:', err);
      } finally {
        this.loading = false;
      }
    },

    async loadDashboardStats() {
      try {
        const response = await alertesAPI.getDashboardStats();
        this.dashboardStats = response.data;
      } catch (err) {
        console.error('Erreur lors du chargement des statistiques:', err);
      }
    },

    async refreshNotifications() {
      await Promise.all([
        this.loadNotifications(),
        this.loadDashboardStats()
      ]);
      this.currentPage = 1;
    },

    async markAsResolved(alertId) {
      if (this.resolvingAlerts.includes(alertId)) return;
      
      this.resolvingAlerts.push(alertId);
      try {
        await alertesAPI.markAsResolved(alertId);
        // Retirer l'alerte de la liste
        this.notifications = this.notifications.filter(n => n.id_alert !== alertId);
        // Recharger les stats
        await this.loadDashboardStats();
      } catch (err) {
        this.error = 'Erreur lors de la résolution de l\'alerte.';
        console.error('Erreur:', err);
      } finally {
        this.resolvingAlerts = this.resolvingAlerts.filter(id => id !== alertId);
      }
    },

    async markAllAsResolved() {
      if (!confirm('Êtes-vous sûr de vouloir marquer toutes les alertes comme résolues ?')) {
        return;
      }

      this.resolvingAll = true;
      try {
        const typeMapping = {
          'stock': 'stock_critique',
          'peremption': 'peremption',
          'commandes': 'commandes'
        };

        const body = this.activeTab !== 'all' && typeMapping[this.activeTab]
          ? { type: typeMapping[this.activeTab] }
          : {};

        await alertesAPI.markAllAsResolved(body);
        await this.refreshNotifications();
      } catch (err) {
        this.error = 'Erreur lors de la résolution des alertes.';
        console.error('Erreur:', err);
      } finally {
        this.resolvingAll = false;
      }
    },

    viewProductDetails(produitId) {
      // Navigation vers la page de détail du produit
      this.$router.push({ name: 'ProductDetail', params: { id: produitId } });
    },

    getUnreadCount(tabId) {
      if (tabId === 'all') {
        return this.notifications.length;
      }
      const typeFilters = {
        'critique': (n) => n.message.includes('CRITIQUE') || n.message.includes('🔴'),
        'stock': (n) => n.message.includes('STOCK'),
        'peremption': (n) => n.message.includes('PÉREMPTION'),
        'commandes': (n) => n.message.includes('COMMANDE')
      };
      return typeFilters[tabId] 
        ? this.notifications.filter(typeFilters[tabId]).length 
        : 0;
    },

    getNotificationIcon(message) {
      if (message.includes('🔴') || message.includes('⛔')) return '🔴';
      if (message.includes('🟠')) return '🟠';
      if (message.includes('🟡') || message.includes('⚠️')) return '⚠️';
      if (message.includes('📈')) return '📈';
      if (message.includes('⏰')) return '⏰';
      return '📋';
    },

    getNotificationTitle(message) {
      if (message.includes('STOCK CRITIQUE')) return 'Stock Critique';
      if (message.includes('RUPTURE')) return 'Rupture de Stock';
      if (message.includes('PÉRIMÉ')) return 'Produit Périmé';
      if (message.includes('PÉREMPTION IMMINENTE')) return 'Péremption Imminente';
      if (message.includes('PÉREMPTION PROCHE')) return 'Péremption Proche';
      if (message.includes('RETARD COMMANDE')) return 'Retard de Commande';
      if (message.includes('FORTE DEMANDE')) return 'Forte Demande';
      if (message.includes('SEUIL ATTEINT')) return 'Seuil Atteint';
      return 'Notification';
    },

    getPriorityClass(message) {
      if (message.includes('🔴') || message.includes('⛔')) return 'priority-critique';
      if (message.includes('🟠')) return 'priority-haute';
      if (message.includes('🟡') || message.includes('⚠️')) return 'priority-moyenne';
      return 'priority-basse';
    },

    getPriorityColor(message) {
      if (message.includes('🔴') || message.includes('⛔')) return '#ef4444';
      if (message.includes('🟠')) return '#f97316';
      if (message.includes('🟡') || message.includes('⚠️')) return '#eab308';
      return '#3b82f6';
    },

    formatDate(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
      const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
      const diffMinutes = Math.floor(diffTime / (1000 * 60));

      if (diffMinutes < 1) return 'À l\'instant';
      if (diffMinutes < 60) return `Il y a ${diffMinutes} min`;
      if (diffHours < 24) return `Il y a ${diffHours}h`;
      if (diffDays === 0) return 'Aujourd\'hui';
      if (diffDays === 1) return 'Hier';
      if (diffDays < 7) return `Il y a ${diffDays} jours`;
      
      return date.toLocaleDateString('fr-FR', { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric' 
      });
    }
  },
  mounted() {
    this.refreshNotifications();
    
    // Auto-refresh toutes les 5 minutes
    this.refreshInterval = setInterval(() => {
      this.loadNotifications();
      this.loadDashboardStats();
    }, 5 * 60 * 1000);
  },
  beforeUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  },
  watch: {
    activeTab() {
      this.currentPage = 1;
    },
    activePriorityFilter() {
      this.currentPage = 1;
    }
  }
}
</script>

<style scoped>
/* ==================== CONTAINER ==================== */
.notifications-container {
  background-color: #f9fafb;
  min-height: 100vh;
  padding-bottom: 80px;
}

/* ==================== LOADING ==================== */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ==================== HEADER ==================== */
.notifications-header {
  background-color: #ffffff;
  padding: 28px 40px 20px 40px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  border-bottom: 1px solid #e5e7eb;
}

.notifications-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 6px;
}

.subtitle {
  color: #6b7280;
  font-size: 15px;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}

.refresh-btn:hover:not(:disabled) {
  background-color: #f9fafb;
  border-color: #3b82f6;
  color: #3b82f6;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ==================== DASHBOARD STATS ==================== */
.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  padding: 20px 40px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.stat-icon {
  font-size: 32px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.stat-label {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
}

/* ==================== TABS ==================== */
.tabs-container {
  padding: 0 40px;
  display: flex;
  gap: 8px;
  background-color: #ffffff;
  border-bottom: 2px solid #e5e7eb;
}

.tab-btn {
  padding: 12px 20px;
  background: transparent;
  border: none;
  color: #6b7280;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-btn:hover {
  color: #111827;
  background-color: #f3f4f6;
  border-radius: 8px 8px 0 0;
}

.tab-btn.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
  font-weight: 600;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: #ef4444;
  color: white;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}

/* ==================== FILTERS ==================== */
.filters-container {
  padding: 16px 40px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 8px 16px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-btn:hover {
  background: #e5e7eb;
  border-color: #d1d5db;
}

.filter-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

/* ==================== CONTENT ==================== */
.notifications-content {
  padding: 20px 40px 40px 40px;
}

.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* ==================== NOTIFICATION CARD ==================== */
.notification-card {
  position: relative;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px 20px 16px 26px;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.notification-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  border-color: #d1d5db;
  transform: translateY(-2px);
}

.priority-indicator {
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  border-radius: 12px 0 0 12px;
}

.notification-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notification-main {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.notification-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  background: #f3f4f6;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 6px;
}

.notification-message {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
  margin-bottom: 8px;
}

.empty-state-main p {
  font-size: 15px;
  color: #6b7280;
}

/* ==================== ERROR MESSAGE ==================== */
.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
}

.error-icon {
  font-size: 48px;
}

.error-message p {
  color: #dc2626;
  font-size: 15px;
  font-weight: 500;
  margin: 0;
}

.retry-btn {
  padding: 8px 20px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-btn:hover {
  background: #b91c1c;
}

/* ==================== PRIORITY CLASSES ==================== */
.priority-critique {
  background: #fef2f2;
  border-left-color: #ef4444;
  border-left-width: 4px;
}

.priority-haute {
  background: #fff7ed;
  border-left-color: #f97316;
  border-left-width: 4px;
}

.priority-moyenne {
  background: #fefce8;
  border-left-color: #eab308;
  border-left-width: 4px;
}

.priority-basse {
  background: #eff6ff;
  border-left-color: #3b82f6;
  border-left-width: 4px;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 768px) {
  .notifications-header {
    flex-direction: column;
    gap: 16px;
    padding: 20px;
  }

  .dashboard-stats {
    grid-template-columns: 1fr;
    padding: 16px 20px;
  }

  .tabs-container {
    padding: 0 20px;
    overflow-x: auto;
    scrollbar-width: none;
  }

  .tabs-container::-webkit-scrollbar {
    display: none;
  }

  .filters-container {
    padding: 12px 20px;
  }

  .notifications-content {
    padding: 16px 20px 100px 20px;
  }

  .notification-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding-left: 0;
  }

  .notification-actions {
    width: 100%;
  }

  .action-btn {
    flex: 1;
  }

  .bulk-actions {
    padding: 12px 20px;
  }

  .bulk-action-btn {
    width: 100%;
  }

  .pagination {
    flex-direction: column;
    gap: 12px;
  }

  .pagination-btn {
    width: 100%;
  }
}

/* ==================== ANIMATIONS ==================== */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.notification-card {
  animation: fadeIn 0.3s ease-out;
}

/* ==================== PRINT STYLES ==================== */
@media print {
  .notifications-header,
  .tabs-container,
  .filters-container,
  .bulk-actions,
  .pagination {
    display: none;
  }

  .notification-actions {
    display: none;
  }

  .notification-card {
    break-inside: avoid;
    box-shadow: none;
    border: 1px solid #e5e7eb;
  }
}
}

.notification-product {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.product-badge {
  padding: 4px 10px;
  background: #eff6ff;
  color: #3b82f6;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.product-ref {
  font-size: 12px;
  color: #9ca3af;
}

.notification-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-left: 56px;
  gap: 16px;
}

.notification-time {
  font-size: 13px;
  color: #9ca3af;
  font-weight: 500;
}

.notification-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid;
}

.view-btn {
  background: transparent;
  color: #3b82f6;
  border-color: #3b82f6;
}

.view-btn:hover {
  background: #3b82f6;
  color: white;
}

.resolve-btn {
  background: transparent;
  color: #10b981;
  border-color: #10b981;
}

.resolve-btn:hover:not(:disabled) {
  background: #10b981;
  color: white;
}

.resolve-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ==================== PAGINATION ==================== */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.pagination-btn {
  padding: 8px 16px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #3b82f6;
  color: #3b82f6;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

/* ==================== BULK ACTIONS ==================== */
.bulk-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px 40px;
  background: #ffffff;
  border-top: 1px solid #e5e7eb;
  box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: center;
}

.bulk-action-btn {
  padding: 12px 24px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.bulk-action-btn:hover:not(:disabled) {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);
}

.bulk-action-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* ==================== EMPTY STATE ==================== */
.empty-state-main {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state-main h3 {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
}