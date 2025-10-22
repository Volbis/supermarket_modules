<template>
  <div class="dashboard-content">
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
  methods: {
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
/* ==================== CONTAINER ==================== */
.dashboard-content {
  padding: 20px 40px 32px 40px;
}

/* ==================== GRIDS ==================== */
.cards-grid-top {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.cards-grid-bottom {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

/* ==================== DASHBOARD CARD ==================== */
.dashboard-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.dashboard-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.card-top {
  min-height: 140px;
}

.card-bottom {
  min-height: 280px;
}

/* ==================== STAT CARD ==================== */
.stat-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon img {
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.sales-icon {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.orders-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.alert-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 6px;
  line-height: 1;
}

.stat-change {
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change.negative {
  color: #ef4444;
}

.stat-change.neutral {
  color: #6b7280;
}

.arrow {
  font-size: 14px;
}

/* ==================== CARD HEADER ==================== */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.view-details-btn {
  padding: 6px 12px;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  color: #6b7280;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-details-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

/* ==================== BAR CHART ==================== */
.chart-container {
  height: 200px;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  height: 180px;
  gap: 12px;
}

.bar-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.bar {
  width: 100%;
  background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 6px 6px 0 0;
  position: relative;
  min-height: 20px;
  transition: all 0.3s ease;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 8px;
}

.bar:hover {
  background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%);
  transform: scaleY(1.05);
}

.bar-value {
  font-size: 11px;
  font-weight: 600;
  color: white;
}

.bar-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

/* ==================== ORDERS LIST ==================== */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.order-item:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.order-icon {
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.order-icon img {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

.order-info {
  flex: 1;
}

.order-title {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 4px;
}

.order-date {
  font-size: 12px;
  color: #9ca3af;
}

.order-status {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
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
  font-size: 14px;
  font-weight: 700;
  color: #111827;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 1024px) {
  .cards-grid-top {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .cards-grid-bottom {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-content {
    padding: 16px 20px;
  }
  
  .cards-grid-top {
    grid-template-columns: 1fr;
  }
  
  .stat-value {
    font-size: 24px;
  }
}
</style>