<template>
  <div class="sales-tracking-content">
    <div class="page-header">
      <div>
        <h2>📊 Suivi des Ventes</h2>
        <p class="subtitle">Dashboard avec KPIs et graphiques en temps réel</p>
      </div>
      <div class="header-actions">
        <select v-model="selectedPeriod" class="period-selector">
          <option value="today">Aujourd'hui</option>
          <option value="week">Cette semaine</option>
          <option value="month">Ce mois</option>
          <option value="year">Cette année</option>
        </select>
        <button class="btn-secondary" @click="refreshData">
          🔄 Actualiser
        </button>
      </div>
    </div>
    
    <!-- KPIs -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon sales">💰</div>
        <div class="stat-info">
          <span class="stat-label">CA du jour</span>
          <span class="stat-value">{{ formatPrice(stats.todaySales) }}</span>
          <span :class="['stat-change', stats.salesGrowth >= 0 ? 'positive' : 'negative']">
            {{ stats.salesGrowth >= 0 ? '+' : '' }}{{ stats.salesGrowth }}% vs hier
          </span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon transactions">🧾</div>
        <div class="stat-info">
          <span class="stat-label">Transactions</span>
          <span class="stat-value">{{ stats.transactionCount }}</span>
          <span class="stat-change">{{ stats.avgTransactionTime }}min moy.</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon basket">🛒</div>
        <div class="stat-info">
          <span class="stat-label">Panier moyen</span>
          <span class="stat-value">{{ formatPrice(stats.avgBasket) }}</span>
          <span class="stat-change">{{ stats.itemsPerBasket }} articles/panier</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon customers">👥</div>
        <div class="stat-info">
          <span class="stat-label">Clients servis</span>
          <span class="stat-value">{{ stats.customersServed }}</span>
          <span class="stat-change positive">{{ stats.loyaltyRate }}% fidélité</span>
        </div>
      </div>
    </div>

    <!-- Graphiques -->
    <div class="charts-section">
      <!-- Ventes par heure -->
      <div class="chart-card full-width">
        <div class="chart-header">
          <h3>📈 Ventes par heure</h3>
          <button class="btn-export" @click="exportChart('hourly')">
            📥 Exporter
          </button>
        </div>
        <canvas ref="hourlySalesChart"></canvas>
      </div>

      <!-- Ventes de la semaine -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>📊 Ventes de la semaine</h3>
        </div>
        <canvas ref="weeklySalesChart"></canvas>
      </div>

      <!-- Top produits -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>🏆 Top 10 Produits</h3>
        </div>
        <div class="top-products-list">
          <div
            v-for="(product, index) in topProducts"
            :key="product.id"
            class="top-product-item"
          >
            <div class="product-rank" :class="'rank-' + (index + 1)">
              {{ index + 1 }}
            </div>
            <div class="product-details">
              <span class="product-name">{{ product.name }}</span>
              <span class="product-sales">{{ product.quantity }} vendus</span>
            </div>
            <div class="product-revenue">
              {{ formatPrice(product.revenue) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Ventes par catégorie -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>🎯 Ventes par catégorie</h3>
        </div>
        <canvas ref="categorySalesChart"></canvas>
      </div>

      <!-- Méthodes de paiement -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>💳 Méthodes de paiement</h3>
        </div>
        <div class="payment-methods-list">
          <div
            v-for="method in paymentMethodsStats"
            :key="method.name"
            class="payment-method-stat"
          >
            <div class="method-info">
              <span class="method-icon">{{ method.icon }}</span>
              <span class="method-name">{{ method.name }}</span>
            </div>
            <div class="method-stats">
              <span class="method-percentage">{{ method.percentage }}%</span>
              <span class="method-amount">{{ formatPrice(method.amount) }}</span>
            </div>
            <div class="method-bar">
              <div class="method-bar-fill" :style="{ width: method.percentage + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'SalesTracking',
  data() {
    return {
      selectedPeriod: 'today',
      stats: {
        todaySales: 2847500,
        salesGrowth: 12.5,
        transactionCount: 156,
        avgTransactionTime: 3.2,
        avgBasket: 18254,
        itemsPerBasket: 5.3,
        customersServed: 142,
        loyaltyRate: 34
      },
      topProducts: [
        { id: 1, name: 'Coca-Cola 1.5L', quantity: 89, revenue: 106800 },
        { id: 2, name: 'Riz 5kg', quantity: 45, revenue: 202500 },
        { id: 3, name: 'Lait NIDO 400g', quantity: 38, revenue: 133000 },
        { id: 4, name: 'Pain de mie', quantity: 67, revenue: 53600 },
        { id: 5, name: 'Huile végétale 1L', quantity: 34, revenue: 74800 },
        { id: 6, name: 'Eau minérale 1.5L', quantity: 112, revenue: 56000 },
        { id: 7, name: 'Bananes (kg)', quantity: 28, revenue: 42000 },
        { id: 8, name: 'Poulet entier', quantity: 19, revenue: 66500 },
        { id: 9, name: 'Tomates (kg)', quantity: 42, revenue: 50400 },
        { id: 10, name: 'Savon Lux x4', quantity: 31, revenue: 55800 }
      ],
      paymentMethodsStats: [
        { name: 'Espèces', icon: '💵', percentage: 45, amount: 1281375 },
        { name: 'Carte bancaire', icon: '💳', percentage: 30, amount: 854250 },
        { name: 'Mobile Money', icon: '📱', percentage: 20, amount: 569500 },
        { name: 'Carte cadeau', icon: '🎁', percentage: 5, amount: 142375 }
      ],
      charts: {}
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initCharts();
    });
  },
  beforeUnmount() {
    // Détruire les graphiques
    Object.values(this.charts).forEach(chart => {
      if (chart) chart.destroy();
    });
  },
  methods: {
    refreshData() {
      console.log('📊 Statistiques rafraîchies');
      // Simuler un refresh
      this.stats.todaySales += Math.floor(Math.random() * 10000);
      this.stats.transactionCount += Math.floor(Math.random() * 5);
    },
    initCharts() {
      this.createHourlySalesChart();
      this.createWeeklySalesChart();
      this.createCategorySalesChart();
    },
    createHourlySalesChart() {
      const ctx = this.$refs.hourlySalesChart;
      if (!ctx) return;

      const hours = ['8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h'];
      const salesData = [45000, 78000, 125000, 185000, 245000, 320000, 285000, 198000, 165000, 142000, 89000, 52000];

      this.charts.hourly = new Chart(ctx, {
        type: 'line',
        data: {
          labels: hours,
          datasets: [{
            label: 'Ventes (CFA)',
            data: salesData,
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4,
            pointRadius: 5,
            pointBackgroundColor: '#10b981',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointHoverRadius: 7
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: '#111827',
              padding: 12,
              titleFont: { size: 14, weight: 'bold' },
              bodyFont: { size: 13 },
              callbacks: {
                label: (context) => {
                  return 'Ventes: ' + this.formatPrice(context.parsed.y);
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: (value) => {
                  return (value / 1000) + 'k';
                }
              },
              grid: {
                color: '#f3f4f6'
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          }
        }
      });
    },
    createWeeklySalesChart() {
      const ctx = this.$refs.weeklySalesChart;
      if (!ctx) return;

      const days = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
      const salesData = [2150000, 1980000, 2340000, 2580000, 2890000, 3420000, 2650000];

      this.charts.weekly = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: days,
          datasets: [{
            label: 'Ventes (CFA)',
            data: salesData,
            backgroundColor: [
              '#3b82f6',
              '#3b82f6',
              '#3b82f6',
              '#3b82f6',
              '#3b82f6',
              '#10b981',
              '#f59e0b'
            ],
            borderRadius: 8,
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: '#111827',
              padding: 12,
              callbacks: {
                label: (context) => {
                  return 'CA: ' + this.formatPrice(context.parsed.y);
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: (value) => {
                  return (value / 1000000) + 'M';
                }
              },
              grid: {
                color: '#f3f4f6'
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          }
        }
      });
    },
    createCategorySalesChart() {
      const ctx = this.$refs.categorySalesChart;
      if (!ctx) return;

      const categories = ['Boissons', 'Épicerie', 'Fruits', 'Hygiène', 'Laitiers', 'Viandes'];
      const salesData = [450000, 680000, 320000, 280000, 380000, 420000];

      this.charts.category = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: categories,
          datasets: [{
            data: salesData,
            backgroundColor: [
              '#3b82f6',
              '#10b981',
              '#f59e0b',
              '#ef4444',
              '#8b5cf6',
              '#ec4899'
            ],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                padding: 15,
                font: {
                  size: 12,
                  weight: '600'
                }
              }
            },
            tooltip: {
              backgroundColor: '#111827',
              padding: 12,
              callbacks: {
                label: (context) => {
                  const label = context.label || '';
                  const value = this.formatPrice(context.parsed);
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((context.parsed / total) * 100).toFixed(1);
                  return label + ': ' + value + ' (' + percentage + '%)';
                }
              }
            }
          }
        }
      });
    },
    exportChart(chartName) {
      alert(`📥 Export du graphique "${chartName}" en cours...\n(Fonctionnalité à implémenter)`);
    },
    formatPrice(amount) {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF',
        minimumFractionDigits: 0
      }).format(amount);
    }
  }
};
</script>

<style scoped>
.sales-tracking-content {
  padding: 20px 40px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
}

.subtitle {
  color: #6b7280;
  font-size: 15px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.period-selector {
  padding: 10px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  background: white;
  cursor: pointer;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  flex-shrink: 0;
}

.stat-icon.sales {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-icon.transactions {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-icon.basket {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-icon.customers {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 24px;
  font-weight: 800;
  color: #111827;
}

.stat-change {
  font-size: 13px;
  color: #6b7280;
  font-weight: 600;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change.negative {
  color: #ef4444;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.chart-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e5e7eb;
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.btn-export {
  padding: 8px 16px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  color: #374151;
  transition: all 0.2s ease;
}

.btn-export:hover {
  background: #e5e7eb;
}

canvas {
  max-height: 300px;
}

.top-products-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.top-product-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 10px;
  transition: background 0.2s ease;
}

.top-product-item:hover {
  background: #f3f4f6;
}

.product-rank {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 800;
  color: white;
  flex-shrink: 0;
}

.product-rank.rank-1 {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
}

.product-rank.rank-2 {
  background: linear-gradient(135deg, #d1d5db 0%, #9ca3af 100%);
}

.product-rank.rank-3 {
  background: linear-gradient(135deg, #fb923c 0%, #ea580c 100%);
}

.product-rank:not(.rank-1):not(.rank-2):not(.rank-3) {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.product-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-name {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.product-sales {
  font-size: 12px;
  color: #6b7280;
}

.product-revenue {
  font-size: 15px;
  font-weight: 700;
  color: #10b981;
}

.payment-methods-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.payment-method-stat {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.method-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.method-icon {
  font-size: 24px;
}

.method-name {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.method-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.method-percentage {
  font-size: 13px;
  font-weight: 700;
  color: #6b7280;
}

.method-amount {
  font-size: 15px;
  font-weight: 700;
  color: #10b981;
}

.method-bar {
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}

.method-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  transition: width 0.3s ease;
}
</style>