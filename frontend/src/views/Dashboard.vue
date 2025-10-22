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

    <!-- Cartes de statistiques (top) -->
    <div class="cards-grid-top">
      <!-- Carte 1: Ventes du jour -->
      <div class="dashboard-card card-top stat-card">
        <div class="stat-icon sales-icon">
          <img src="@/assets/icons/box.png" alt="Ventes" />
        </div>
        <div class="stat-content">
          <h3 class="stat-label">Ventes du jour</h3>
          <p class="stat-value">{{ formatCurrency(dailySales) }}</p>
          <span class="stat-change positive">
            <span class="arrow">↑</span> +12.5% vs hier
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
          <button class="view-details-btn">Voir détails →</button>
        </div>
        <div class="chart-container">
          <!-- Graphique simple en barres -->
          <div class="bar-chart">
            <div v-for="(day, index) in weekSales" :key="index" class="bar-wrapper">
              <div class="bar" :style="{ height: getBarHeight(day.amount) + '%' }">
                <span class="bar-value">{{ formatCurrency(day.amount, true) }}</span>
              </div>
              <span class="bar-label">{{ day.day }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Carte 5: Dernières commandes -->
      <div class="dashboard-card card-bottom">
        <div class="card-header">
          <h3 class="card-title">Dernières commandes</h3>
          <button class="view-details-btn">Voir tout →</button>
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
export default {
  name: 'DashboardView',
  data() {
    return {
      // Statistiques principales
      dailySales: 1250000,
      activeOrders: 24,
      pendingOrders: 8,
      lowStockItems: 12,
      
      // Notifications toast
      notifications: [],
      notificationId: 0,
      
      // Ventes de la semaine
      weekSales: [
        { day: 'Lun', amount: 850000 },
        { day: 'Mar', amount: 920000 },
        { day: 'Mer', amount: 1100000 },
        { day: 'Jeu', amount: 980000 },
        { day: 'Ven', amount: 1350000 },
        { day: 'Sam', amount: 1650000 },
        { day: 'Dim', amount: 1200000 }
      ],
      
      // Dernières commandes
      recentOrders: [
        {
          id: 1,
          title: 'Commande #001 - Supermarché Central',
          date: 'Il y a 5 minutes',
          amount: 45000,
          status: 'pending'
        },
        {
          id: 2,
          title: 'Commande #002 - Boutique Express',
          date: 'Il y a 15 minutes',
          amount: 32000,
          status: 'confirmed'
        },
        {
          id: 3,
          title: 'Commande #003 - Mini Market',
          date: 'Il y a 1 heure',
          amount: 78000,
          status: 'delivered'
        },
        {
          id: 4,
          title: 'Commande #004 - Grocery Store',
          date: 'Il y a 2 heures',
          amount: 56000,
          status: 'confirmed'
        }
      ]
    }
  },
  computed: {
    visibleNotifications() {
      return this.notifications.filter(n => n.visible)
    }
  },
  mounted() {
    // Afficher des notifications de bienvenue
    setTimeout(() => {
      this.showNotification('Bienvenue !', 'Tableau de bord chargé avec succès', 'success')
    }, 500)
    
    setTimeout(() => {
      this.showNotification('Attention', `${this.lowStockItems} produits en rupture de stock`, 'warning')
    }, 2000)
    
    setTimeout(() => {
      this.showNotification('Nouvelle commande', 'Commande #001 reçue de Supermarché Central', 'info')
    }, 4000)
  },
  methods: {
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
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
}

.toast-notification.warning {
  border-left-color: #f59e0b;
  background: linear-gradient(135deg, #ffffff 0%, #fffbeb 100%);
}

.toast-notification.error {
  border-left-color: #ef4444;
  background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
}

.toast-notification.info {
  border-left-color: #3b82f6;
  background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
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
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #059669;
}

.toast-notification.warning .toast-icon {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #d97706;
}

.toast-notification.error .toast-icon {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #dc2626;
}

.toast-notification.info .toast-icon {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
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
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  min-height: 100vh;
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
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 8px 24px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(226, 232, 240, 0.8);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.dashboard-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.dashboard-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 16px 40px rgba(0, 0, 0, 0.12);
  transform: translateY(-6px);
  border-color: rgba(59, 130, 246, 0.3);
}

.dashboard-card:hover::before {
  opacity: 1;
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
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.35), 0 4px 12px rgba(37, 99, 235, 0.2);
}

.orders-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.35), 0 4px 12px rgba(5, 150, 105, 0.2);
}

.alert-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.35), 0 4px 12px rgba(217, 119, 6, 0.2);
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
  padding: 5px 10px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #475569;
  bottom: 50px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-details-btn:hover {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-color: #3b82f6;
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

/* ==================== BAR CHART ==================== */
.chart-container {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 8px 0;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  height: 220px;
  width: 100%;
  gap: 16px;
  padding: 0 8px;
}

.bar-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.bar {
  width: 100%;
  background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 10px 10px 0 0;
  position: relative;
  min-height: 30px;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 10px;
  box-shadow: 0 -4px 16px rgba(59, 130, 246, 0.25);
  cursor: pointer;
}

.bar:hover {
  background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%);
  transform: scaleY(1.05) scaleX(1.08);
  box-shadow: 0 -8px 24px rgba(37, 99, 235, 0.45);
}

.bar-value {
  font-size: 12px;
  font-weight: 700;
  color: white;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.bar-label {
  font-size: 13px;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
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
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  cursor: pointer;
}

.order-item:hover {
  background: white;
  border-color: #3b82f6;
  transform: translateX(6px) scale(1.02);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
}

.order-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.status-badge.pending {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
}

.status-badge.confirmed {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
}

.status-badge.delivered {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
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