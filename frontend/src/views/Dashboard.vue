<template>
  <div class="dashboard-content">
    
    <!-- Toast Notifications -->
    <transition-group name="toast" tag="div" class="toast-container">
      <div
        v-for="notification in visibleNotifications"
        :key="notification.id"
        :class="['toast-notification', notification.type]"
      >
        <div class="toast-icon">
          <span v-if="notification.type === 'success'">✓</span>
          <span v-else-if="notification.type === 'warning'">⚠️</span>
          <span v-else-if="notification.type === 'info'">ℹ️</span>
          <span v-else>✕</span>
        </div>
        <div class="toast-content">
          <h4 class="toast-title">{{ notification.title }}</h4>
          <p class="toast-message">{{ notification.message }}</p>
        </div>
        <button @click="dismissNotification(notification.id)" class="toast-close">×</button>
      </div>
    </transition-group>

    <!-- Modal de chargement -->
    <div v-if="loading && ventesData.length === 0" class="loading-modal-backdrop">
      <div class="loading-modal">
        <div class="loading-spinner"></div>
        <p class="loading-text">Chargement des données...</p>
      </div>
    </div>
    
    <!-- Cartes de statistiques (top) -->
    <div class="cards-grid-top" :class="{ 'loading-blur': loading }">
      <!-- Carte 1: Ventes du jour -->
      <div class="dashboard-card card-top stat-card">
        <div class="stat-icon sales-icon">
          <img src="@/assets/icons/box.png" alt="Ventes" />
        </div>
        <div class="stat-content">
          <h3 class="stat-label">Ventes du jour</h3>
          <p class="stat-value">{{ formattedDailySales }}</p>
          
          <span :class="['stat-change', salesTrend.direction]">
            <span class="arrow" v-if="salesTrend.direction === 'positive'">↑</span>
            <span class="arrow" v-else-if="salesTrend.direction === 'negative'">↓</span>
            <span class="arrow" v-else>→</span>
            {{ salesTrend.direction === 'positive' ? '+' : salesTrend.direction === 'negative' ? '-' : '' }}{{ salesTrend.value }}% vs hier
          </span>
        </div>
      </div>

      <!-- Carte 2: Commandes en cours -->
      <div class="dashboard-card card-top stat-card">
        <div class="stat-icon orders-icon">
          <img src="@/assets/icons/commande.png" alt="Commandes" />
        </div>
        <div class="stat-content">
          <h3 class="stat-label">Commandes en cours</h3>
          <p class="stat-value">{{ activeOrders }}</p>
          <span class="stat-change neutral">
            {{ pendingOrders }} en attente
          </span>
        </div>
      </div>

      <!-- Carte 3: Alertes stock -->
      <div class="dashboard-card card-top stat-card">
        <div class="stat-icon alert-icon">
          <img src="@/assets/icons/stock.png" alt="Stock" />
        </div>
        <div class="stat-content">
          <h3 class="stat-label">Alertes stock</h3>
          <p class="stat-value">{{ lowStockItems }}</p>
          <span class="stat-change negative">
            <span class="arrow">⚠️</span> Produits à réapprovisionner
          </span>
        </div>
      </div>
    </div>
    
    <!-- Cartes larges (bottom) -->
    <div class="cards-grid-bottom">
      <!-- Carte 4: Graphique des ventes -->
      <div class="dashboard-card card-bottom">
        <div class="card-header">
          <h3 class="card-title">Ventes de la semaine</h3>
        </div>
        <div class="chart-container">
          <!-- Graphique moderne en ligne -->
          <div class="line-chart">
            <svg class="line-chart-svg" viewBox="0 0 700 240" preserveAspectRatio="xMidYMid meet">
              <!-- Grille de fond -->
              <g class="grid-lines">
                <line v-for="i in 5" :key="'grid-' + i" 
                      :x1="0" :y1="i * 48" :x2="700" :y2="i * 48" 
                      stroke="#e5e7eb" stroke-width="1" opacity="0.5"/>
              </g>
              
              <!-- Gradient pour l'aire sous la courbe -->
              <defs>
                <linearGradient id="lineGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color:#60a5fa;stop-opacity:0.4" />
                  <stop offset="100%" style="stop-color:#60a5fa;stop-opacity:0.05" />
                </linearGradient>
              </defs>
              
              <!-- Aire sous la courbe -->
              <path :d="getAreaPath()" fill="url(#lineGradient)" />
              
              <!-- Ligne principale -->
              <path :d="getLinePath()" 
                    fill="none" 
                    stroke="#3b82f6" 
                    stroke-width="3" 
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="line-path" />
              
              <!-- Points sur la courbe -->
              <g v-for="(day, index) in weekSales" :key="'point-' + index">
                <circle 
                  :cx="getPointX(index)" 
                  :cy="getPointY(day.amount)"
                  r="6"
                  fill="white"
                  stroke="#3b82f6"
                  stroke-width="3"
                  class="line-point"
                  @mouseenter="showTooltip(index)"
                  @mouseleave="hideTooltip(index)" />
              </g>
            </svg>
            
            <!-- Labels des jours -->
            <div class="line-labels">
              <span v-for="(day, index) in weekSales" :key="'label-' + index" class="line-label">
                {{ day.day }}
              </span>
            </div>
            
            <!-- Tooltips -->
            <div v-for="(day, index) in weekSales" :key="'tooltip-' + index"
                 v-show="activeTooltip === index"
                 class="line-tooltip"
                 :style="{ left: getTooltipX(index) + 'px', top: getTooltipY(day.amount) + 'px' }">
              <span class="tooltip-amount">{{ formatCurrency(day.amount) }}</span>
              <span class="tooltip-day">{{ day.day }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Carte 5: Dernières commandes -->
      <div class="dashboard-card card-bottom">
        <div class="card-header">
          <h3 class="card-title">Dernières commandes</h3>
        </div>
        <div class="orders-list">
          <div v-for="order in recentOrders" :key="order.id" class="order-item">
            <div class="order-icon">
              <img src="@/assets/icons/livraison.png" alt="Commande" />
            </div>
            <div class="order-info">
              <h4 class="order-title">{{ order.title }}</h4>
              <p class="order-date">{{ order.date }}</p>
            </div>
            <div class="order-status">
              <span :class="['status-badge', order.status]">
                {{ getStatusLabel(order.status) }}
              </span>
              <span class="order-amount">{{ formatCurrency(order.amount) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import historiqueVentesAPI from '@/services/historiqueVentes';
import commandesAPI from '@/services/commandes';
import alertesAPI from '@/services/alertes';
import produitsAPI from '@/services/produits';
import { useDataCache } from '@/composables/useDataCache';

export default {
  name: 'DashboardView',
  setup() {
    // Utiliser le cache global
    const { loadWithCache, invalidateCache, cacheStatus } = useDataCache();
    
    return {
      loadWithCache,
      invalidateCache,
      cacheStatus
    };
  },
  data() {
    return {
      loading: true,
      refreshInterval: null,
      lastUpdate: null,
      hasNotifiedAlerts: false,
      
      // Statistiques principales
      dailySales: 0,
      totalRevenue: 0,
      activeOrders: 0,
      pendingOrders: 0,
      lowStockItems: 0,
      totalProducts: 0,
      
      // Comparaison période précédente
      previousDaySales: 0,
      salesGrowth: 0,
      
      // Notifications toast
      notifications: [],
      notificationId: 0,
      
      // Ventes de la semaine (données dynamiques)
      weekSales: [],
      
      // Dernières commandes (données dynamiques)
      recentOrders: [],
      
      // Alertes actives
      activeAlerts: [],
      
      // Top produits
      topProducts: [],
      
      // Données brutes
      ventesData: [],
      commandesData: [],
      alertesData: [],
      
      // Line chart
      activeTooltip: null
    }
  },
  computed: {
    visibleNotifications() {
      return this.notifications.filter(n => n.visible)
    },
    
    formattedDailySales() {
      return this.formatCurrency(this.dailySales);
    },
    
    salesTrend() {
      if (this.previousDaySales === 0) return { direction: 'neutral', value: 0 };
      
      const growth = ((this.dailySales - this.previousDaySales) / this.previousDaySales) * 100;
      
      return {
        direction: growth > 0 ? 'positive' : growth < 0 ? 'negative' : 'neutral',
        value: Math.abs(growth).toFixed(1)
      };
    }
  },
  
  async mounted() {
    // Premier chargement (AVEC cache si disponible)
    await this.loadDashboardData(false, false);
    
    // Notification de bienvenue seulement si c'est la première visite
    const hasVisited = sessionStorage.getItem('dashboard_visited');
    if (!hasVisited) {
      setTimeout(() => {
        this.showNotification('Bienvenue !', 'Tableau de bord chargé avec succès', 'success');
        sessionStorage.setItem('dashboard_visited', 'true');
      }, 500);
    }
  },
  
  beforeUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  },
  methods: {
    // === MÉTHODE PUBLIQUE POUR REFRESH DEPUIS APP.VUE ===
    
    async refreshData() {
      console.log('🔄 Rafraîchissement forcé du Dashboard...');
      this.showNotification('Actualisation...', 'Rechargement des données', 'info');
      
      // Invalider tout le cache
      this.invalidateCache('ventes');
      this.invalidateCache('commandes');
      this.invalidateCache('alertes');
      this.invalidateCache('produits');
      
      // Recharger avec forceRefresh = true
      await this.loadDashboardData(false, true);
      
      this.showNotification('✅ Actualisé', 'Données rechargées avec succès', 'success');
    },
    
    // === CHARGEMENT DES DONNÉES ===
    
    async loadDashboardData(silent = false, forceRefresh = false) {
      // Ne montrer le loading QUE si on force le refresh ou si on n'a pas de données
      const showLoading = !silent && (forceRefresh || !this.ventesData.length);
      
      if (showLoading) {
        this.loading = true;
      }
      
      try {
        // Charger toutes les données en parallèle avec le cache global
        await Promise.all([
          this.loadVentesData(forceRefresh),
          this.loadCommandesData(forceRefresh),
          this.loadAlertesData(forceRefresh),
          this.loadProduitsData(forceRefresh)
        ]);
        
        // Calculer les statistiques
        this.calculateStatistics();
        this.calculateWeekSales();
        this.prepareRecentOrders();
        this.checkAndNotifyAlerts();
        
        // Mettre à jour l'heure de dernière mise à jour
        this.lastUpdate = new Date().toLocaleTimeString('fr-FR', { 
          hour: '2-digit', 
          minute: '2-digit' 
        });
        
      } catch (error) {
        console.error('Erreur lors du chargement du dashboard:', error);
        if (!silent) {
          this.showNotification('Erreur', 'Impossible de charger les données', 'error');
        }
      } finally {
        if (showLoading) {
          this.loading = false;
        }
      }
    },
    
    async loadVentesData(forceRefresh = false) {
      try {
        this.ventesData = await this.loadWithCache(
          'ventes',
          async () => {
            const response = await historiqueVentesAPI.getAllHistoriqueVentes();
            return response.data?.ventes || response.data || [];
          },
          forceRefresh
        );
      } catch (error) {
        console.error('❌ Erreur chargement ventes:', error);
        this.ventesData = [];
      }
    },
    
    async loadCommandesData(forceRefresh = false) {
      try {
        this.commandesData = await this.loadWithCache(
          'commandes',
          async () => {
            const response = await commandesAPI.getAllCommandes();
            return response.data || [];
          },
          forceRefresh
        );
      } catch (error) {
        console.error('❌ Erreur chargement commandes:', error);
        this.commandesData = [];
      }
    },
    
    async loadAlertesData(forceRefresh = false) {
      try {
        this.alertesData = await this.loadWithCache(
          'alertes',
          async () => {
            const response = await alertesAPI.getAllAlertes();
            return response.data || [];
          },
          forceRefresh
        );
        this.activeAlerts = this.alertesData.slice(0, 5);
      } catch (error) {
        console.error('❌ Erreur chargement alertes:', error);
        this.alertesData = [];
        this.activeAlerts = [];
      }
    },
    
    async loadProduitsData(forceRefresh = false) {
      try {
        const produits = await this.loadWithCache(
          'produits',
          async () => {
            const response = await produitsAPI.getAllProduits();
            return response.data || [];
          },
          forceRefresh
        );
        
        this.lowStockItems = produits.filter(p => 
          parseInt(p.quantite_stock || 0) <= parseInt(p.seuil_reapprovisionnement || 0)
        ).length;
        this.totalProducts = produits.length;
      } catch (error) {
        console.error('❌ Erreur chargement produits:', error);
        this.lowStockItems = 0;
        this.totalProducts = 0;
      }
    },
    
    // === CALCULS ET STATISTIQUES ===
    
    calculateStatistics() {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      
      // Ventes du jour
      this.dailySales = this.ventesData
        .filter(v => {
          const venteDate = new Date(v.date_vente);
          venteDate.setHours(0, 0, 0, 0);
          return venteDate.getTime() === today.getTime();
        })
        .reduce((sum, v) => sum + parseFloat(v.montant_total || 0), 0);
      
      // Ventes d'hier (pour comparaison)
      this.previousDaySales = this.ventesData
        .filter(v => {
          const venteDate = new Date(v.date_vente);
          venteDate.setHours(0, 0, 0, 0);
          return venteDate.getTime() === yesterday.getTime();
        })
        .reduce((sum, v) => sum + parseFloat(v.montant_total || 0), 0);
      
      // Revenu total
      this.totalRevenue = this.ventesData.reduce(
        (sum, v) => sum + parseFloat(v.montant_total || 0), 0
      );
      
      // Commandes actives
      this.activeOrders = this.commandesData.filter(
        c => c.statut === 'EN_COURS'
      ).length;
      
      // Commandes en attente
      this.pendingOrders = this.commandesData.filter(
        c => c.statut === 'EN_ATTENTE'
      ).length;
    },
    
    calculateWeekSales() {
      const daysOfWeek = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];
      const salesByDay = {};
      
      // Initialiser les 7 derniers jours
      for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        date.setHours(0, 0, 0, 0);
        
        const dayName = daysOfWeek[date.getDay()];
        salesByDay[dayName] = { day: dayName, amount: 0, date: date };
      }
      
      // Remplir avec les vraies données
      this.ventesData.forEach(vente => {
        const venteDate = new Date(vente.date_vente);
        venteDate.setHours(0, 0, 0, 0);
        
        const dayName = daysOfWeek[venteDate.getDay()];
        
        // Vérifier si c'est dans les 7 derniers jours
        const weekAgo = new Date();
        weekAgo.setDate(weekAgo.getDate() - 7);
        weekAgo.setHours(0, 0, 0, 0);
        
        if (venteDate >= weekAgo && salesByDay[dayName]) {
          salesByDay[dayName].amount += parseFloat(vente.montant_total || 0);
        }
      });
      
      this.weekSales = Object.values(salesByDay);
    },
    
    prepareRecentOrders() {
      // Trier les commandes par date (plus récentes d'abord)
      const sortedCommandes = [...this.commandesData]
        .sort((a, b) => new Date(b.date_commande) - new Date(a.date_commande))
        .slice(0, 4); // Top 4 commandes
      
      this.recentOrders = sortedCommandes.map(cmd => {
        const montantTotal = this.calculateCommandeTotal(cmd);
        
        return {
          id: cmd.id_commande,
          title: `Commande #${cmd.id_commande?.substring(0, 8) || 'N/A'} - ${cmd.fournisseur_nom || 'Fournisseur'}`,
          date: this.formatRelativeTime(cmd.date_commande),
          amount: montantTotal,
          status: this.mapStatus(cmd.statut)
        };
      });
    },
    
    calculateCommandeTotal(commande) {
      // Si le montant total est déjà disponible
      if (commande.montant_total) {
        return parseFloat(commande.montant_total);
      }
      
      // Sinon calculer depuis les détails (si disponibles)
      if (commande.details && Array.isArray(commande.details)) {
        return commande.details.reduce((sum, detail) => {
          return sum + (parseFloat(detail.prix_unitaire || 0) * parseInt(detail.quantite || 0));
        }, 0);
      }
      
      return 0;
    },
    
    mapStatus(statut) {
      const statusMap = {
        'EN_COURS': 'confirmed',
        'EN_ATTENTE': 'pending',
        'LIVREE': 'delivered',
        'ANNULEE': 'cancelled'
      };
      return statusMap[statut] || 'pending';
    },
    
    checkAndNotifyAlerts() {
      // Notifier seulement si nouvelles alertes critiques
      const criticalAlerts = this.alertesData.filter(a => 
        a.message?.includes('CRITIQUE') || a.message?.includes('🔴')
      );
      
      if (criticalAlerts.length > 0 && !this.hasNotifiedAlerts) {
        setTimeout(() => {
          this.showNotification(
            'Alertes Critiques', 
            `${criticalAlerts.length} alerte(s) nécessitent votre attention`, 
            'warning'
          );
        }, 1500);
        this.hasNotifiedAlerts = true;
      }
    },
    
    // === UTILITAIRES ===
    
    formatRelativeTime(date) {
      if (!date) return 'Date inconnue';
      
      const now = new Date();
      const past = new Date(date);
      const diffMs = now - past;
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);
      
      if (diffMins < 1) return 'À l\'instant';
      if (diffMins < 60) return `Il y a ${diffMins} minute${diffMins > 1 ? 's' : ''}`;
      if (diffHours < 24) return `Il y a ${diffHours} heure${diffHours > 1 ? 's' : ''}`;
      if (diffDays < 7) return `Il y a ${diffDays} jour${diffDays > 1 ? 's' : ''}`;
      
      return past.toLocaleDateString('fr-FR');
    },
    
    // === NOTIFICATIONS ===
    
    showNotification(title, message, type = 'info', duration = 5000) {
      const id = this.notificationId++
      const notification = {
        id,
        title,
        message,
        type,
        visible: true
      }
      
      this.notifications.push(notification)
      
      // Auto-dismiss après duration
      setTimeout(() => {
        this.dismissNotification(id)
      }, duration)
    },
    
    dismissNotification(id) {
      const notification = this.notifications.find(n => n.id === id)
      if (notification) {
        notification.visible = false
        // Supprimer complètement après l'animation
        setTimeout(() => {
          const index = this.notifications.findIndex(n => n.id === id)
          if (index > -1) {
            this.notifications.splice(index, 1)
          }
        }, 300)
      }
    },
    
    formatCurrency(amount, short = false) {
      if (short) {
        if (amount >= 1000000) {
          return (amount / 1000000).toFixed(1) + 'M'
        }
        if (amount >= 1000) {
          return (amount / 1000).toFixed(0) + 'K'
        }
        return amount.toString()
      }
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF',
        minimumFractionDigits: 0
      }).format(amount)
    },
    
    getBarHeight(amount) {
      const maxAmount = Math.max(...this.weekSales.map(s => s.amount))
      return (amount / maxAmount) * 100
    },
    
    // === LINE CHART METHODS ===
    
    getLinePath() {
      if (this.weekSales.length === 0) return '';
      
      const points = this.weekSales.map((day, index) => {
        const x = this.getPointX(index);
        const y = this.getPointY(day.amount);
        return { x, y };
      });
      
      // Créer une courbe lisse (Catmull-Rom spline)
      let path = `M ${points[0].x} ${points[0].y}`;
      
      for (let i = 0; i < points.length - 1; i++) {
        const p0 = points[Math.max(0, i - 1)];
        const p1 = points[i];
        const p2 = points[i + 1];
        const p3 = points[Math.min(points.length - 1, i + 2)];
        
        const cp1x = p1.x + (p2.x - p0.x) / 6;
        const cp1y = p1.y + (p2.y - p0.y) / 6;
        const cp2x = p2.x - (p3.x - p1.x) / 6;
        const cp2y = p2.y - (p3.y - p1.y) / 6;
        
        path += ` C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${p2.x} ${p2.y}`;
      }
      
      return path;
    },
    
    getAreaPath() {
      if (this.weekSales.length === 0) return '';
      
      const linePath = this.getLinePath();
      const lastPoint = this.getPointX(this.weekSales.length - 1);
      const firstPoint = this.getPointX(0);
      
      return `${linePath} L ${lastPoint} 240 L ${firstPoint} 240 Z`;
    },
    
    getPointX(index) {
      const width = 700;
      const padding = 50;
      const spacing = (width - padding * 2) / (this.weekSales.length - 1);
      return padding + index * spacing;
    },
    
    getPointY(amount) {
      const height = 200;
      const padding = 20;
      const maxAmount = Math.max(...this.weekSales.map(s => s.amount), 1);
      return height - ((amount / maxAmount) * (height - padding)) + padding;
    },
    
    getTooltipX(index) {
      const containerWidth = 700;
      const pointX = this.getPointX(index);
      return (pointX / containerWidth) * 100; // Percentage
    },
    
    getTooltipY(amount) {
      return this.getPointY(amount) - 10;
    },
    
    showTooltip(index) {
      this.activeTooltip = index;
    },
    
    hideTooltip(index) {
      if (this.activeTooltip === index) {
        this.activeTooltip = null;
      }
    },
    
    getStatusLabel(status) {
      const labels = {
        pending: 'En attente',
        confirmed: 'Confirmée',
        delivered: 'Livrée'
      }
      return labels[status] || status
    }
  }
}
</script>

<style scoped>
/* ==================== TOAST NOTIFICATIONS ==================== */
.toast-container {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 420px;
}

.toast-notification {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 18px 20px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15), 0 4px 12px rgba(0, 0, 0, 0.08);
  border-left: 4px solid;
  min-width: 340px;
  animation: slideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  backdrop-filter: blur(10px);
}

.toast-notification.success {
  border-left-color: #10b981;
  background: #f0fdf4;
}

.toast-notification.warning {
  border-left-color: #f59e0b;
  background: #fffbeb;
}

.toast-notification.error {
  border-left-color: #ef4444;
  background: #fef2f2;
}

.toast-notification.info {
  border-left-color: #3b82f6;
  background: #eff6ff;
}

.toast-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
  font-weight: bold;
}

.toast-notification.success .toast-icon {
  background: #d1fae5;
  color: #059669;
}

.toast-notification.warning .toast-icon {
  background: #fef3c7;
  color: #d97706;
}

.toast-notification.error .toast-icon {
  background: #fee2e2;
  color: #dc2626;
}

.toast-notification.info .toast-icon {
  background: #dbeafe;
  color: #2563eb;
}

.toast-content {
  flex: 1;
  padding-top: 2px;
}

.toast-title {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 6px;
  letter-spacing: -0.01em;
}

.toast-message {
  font-size: 13px;
  color: #6b7280;
  line-height: 1.5;
  font-weight: 400;
}

.toast-close {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: #9ca3af;
  font-size: 22px;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: -2px;
}

.toast-close:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #111827;
  transform: scale(1.1);
}

/* Toast animations */
.toast-enter-active {
  animation: slideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.toast-leave-active {
  animation: slideOut 0.3s ease-in;
}

@keyframes slideIn {
  from {
    transform: translateX(450px) scale(0.9);
    opacity: 0;
  }
  to {
    transform: translateX(0) scale(1);
    opacity: 1;
  }
}

@keyframes slideOut {
  from {
    transform: translateX(0) scale(1);
    opacity: 1;
  }
  to {
    transform: translateX(450px) scale(0.9);
    opacity: 0;
  }
}

/* ==================== CONTAINER ==================== */
.dashboard-content {
  padding: 32px 48px;
  background: #f3f4f6;
  min-height: 100vh;
}

/* ==================== HEADER ==================== */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 2px solid #e5e7eb;
}

.header-left {
  flex: 1;
}

.dashboard-title {
  font-size: 32px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.dashboard-subtitle {
  font-size: 15px;
  color: #64748b;
  font-weight: 500;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.last-update {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 500;
  white-space: nowrap;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  color: #475569;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.refresh-btn:hover:not(:disabled) {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-icon {
  font-size: 18px;
  display: inline-block;
  transition: transform 0.3s ease;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ==================== LOADING MODAL ==================== */
.loading-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.loading-modal {
  background: white;
  border-radius: 20px;
  padding: 40px 50px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  animation: slideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  min-width: 280px;
}

.loading-spinner {
  width: 56px;
  height: 56px;
  border: 5px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-text {
  font-size: 16px;
  font-weight: 600;
  color: #64748b;
  margin: 0;
  text-align: center;
}

.loading-blur {
  opacity: 0.6;
  pointer-events: none;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(30px) scale(0.95);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

/* ==================== GRIDS ==================== */
.cards-grid-top {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.cards-grid-bottom {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

/* ==================== DASHBOARD CARD ==================== */
.dashboard-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.dashboard-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
  border-color: #d1d5db;
}

.card-top {
  min-height: 150px;
  display: flex;
  align-items: center;
}

.card-bottom {
  min-height: 320px;
  display: flex;
  flex-direction: column;
}

/* ==================== STAT CARD ==================== */
.stat-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 32px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-8px);
  }
}

.stat-icon img {
  width: 32px;
  height: 32px;
  object-fit: contain;
  filter: brightness(0) invert(1);
}

.sales-icon {
  background: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.orders-icon {
  background: #10b981;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
}

.alert-icon {
  background: #f59e0b;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
  animation: shake 4s ease-in-out infinite;
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0) rotate(0deg);
  }
  10%, 30%, 50%, 70%, 90% {
    transform: translateX(-3px) rotate(-2deg);
  }
  20%, 40%, 60%, 80% {
    transform: translateX(3px) rotate(2deg);
  }
}

.stat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 600;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 32px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 8px;
  line-height: 1;
  letter-spacing: -0.02em;
}

.stat-change {
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 0;
}

.stat-change.positive {
  color: #059669;
}

.stat-change.negative {
  color: #dc2626;
}

.stat-change.neutral {
  color: #64748b;
}

.arrow {
  font-size: 16px;
  font-weight: bold;
}

/* ==================== CARD HEADER ==================== */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f1f5f9;
}

.card-title {
  font-size: 19px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.01em;
}

.view-details-btn {
  padding: 8px 16px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  color: #6b7280;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-details-btn:hover {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
  transform: translateX(4px);
}

/* ==================== LINE CHART ==================== */
.chart-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 50px;
  position: relative;
}

.line-chart {
  width: 100%;
  height: 260px;
  position: relative;
  padding: 10px 0;
}

.line-chart-svg {
  width: 100%;
  height: 240px;
  overflow: visible;
}

/* Grille de fond */
.grid-lines line {
  stroke-dasharray: 4 4;
  transition: opacity 0.3s ease;
}

/* Animation de la ligne */
.line-path {
  stroke-dasharray: 2000;
  stroke-dashoffset: 2000;
  animation: drawLine 1.5s ease-out forwards;
  filter: drop-shadow(0 2px 8px rgba(59, 130, 246, 0.3));
}

@keyframes drawLine {
  to {
    stroke-dashoffset: 0;
  }
}

/* Points interactifs */
.line-point {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  filter: drop-shadow(0 2px 6px rgba(59, 130, 246, 0.4));
}

.line-point:hover {
  r: 8;
  stroke-width: 4;
  filter: drop-shadow(0 4px 12px rgba(59, 130, 246, 0.6));
}

/* Labels des jours */
.line-labels {
  display: flex;
  justify-content: space-between;
  padding: 12px 50px 0;
  margin-top: -10px;
}

.line-label {
  font-size: 12px;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: all 0.3s ease;
  padding: 4px 8px;
  border-radius: 6px;
  text-align: center;
}

.line-label:hover {
  color: #3b82f6;
  background: #eff6ff;
  transform: scale(1.05);
}

/* Tooltip moderne */
.line-tooltip {
  position: absolute;
  transform: translateX(-50%) translateY(-100%);
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  color: white;
  padding: 12px 18px;
  border-radius: 12px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25), 
              0 0 0 1px rgba(255, 255, 255, 0.1);
  pointer-events: none;
  white-space: nowrap;
  z-index: 100;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  animation: tooltipAppear 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  backdrop-filter: blur(10px);
}

.line-tooltip::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(96, 165, 250, 0.1) 0%, transparent 100%);
  border-radius: 12px;
  pointer-events: none;
}

.line-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 8px solid transparent;
  border-top-color: #1e293b;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
}

@keyframes tooltipAppear {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-90%) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(-100%) scale(1);
  }
}

.tooltip-amount {
  font-size: 16px;
  font-weight: 800;
  color: #60a5fa;
  letter-spacing: -0.02em;
  text-shadow: 0 2px 8px rgba(96, 165, 250, 0.3);
}

.tooltip-day {
  font-size: 11px;
  font-weight: 600;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* ==================== ORDERS LIST ==================== */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  flex: 1;
  overflow-y: auto;
  padding-right: 4px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 18px;
  background: #f9fafb;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
  cursor: pointer;
}

.order-item:hover {
  background: white;
  border-color: #3b82f6;
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.order-icon {
  width: 48px;
  height: 48px;
  background: #ffffff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid #e5e7eb;
}

.order-icon img {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.order-info {
  flex: 1;
}

.order-title {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 6px;
  letter-spacing: -0.01em;
}

.order-date {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
}

.order-status {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.status-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.confirmed {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.delivered {
  background: #d1fae5;
  color: #065f46;
}

.order-amount {
  font-size: 15px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.01em;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 1280px) {
  .dashboard-content {
    padding: 24px 32px;
  }
  
  .cards-grid-top {
    gap: 20px;
  }
  
  .cards-grid-bottom {
    gap: 20px;
  }
}

@media (max-width: 1024px) {
  .cards-grid-top {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .cards-grid-bottom {
    grid-template-columns: 1fr;
  }
  
  .stat-value {
    font-size: 28px;
  }
}

@media (max-width: 768px) {
  .dashboard-content {
    padding: 20px;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .dashboard-title {
    font-size: 24px;
  }
  
  .refresh-btn {
    width: 100%;
    justify-content: center;
  }
  
  .cards-grid-top {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .cards-grid-bottom {
    gap: 16px;
  }
  
  .stat-card {
    padding: 24px;
  }
  
  .stat-icon {
    width: 56px;
    height: 56px;
  }
  
  .stat-value {
    font-size: 24px;
  }
  
  .toast-container {
    right: 12px;
    left: 12px;
    max-width: none;
  }
  
  .toast-notification {
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .dashboard-content {
    padding: 16px;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .stat-change {
    justify-content: center;
  }
  
  .order-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .order-status {
    width: 100%;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}
</style>