<template>
  <div class="statistics-page">
    <!-- En-tête avec filtres -->
    <div class="page-header">
      <div class="filters-container">
        <select v-model="dateFilter" class="filter-select">
          <option value="7">7 derniers jours</option>
          <option value="30">30 derniers jours</option>
          <option value="90">90 derniers jours</option>
          <option value="365">1 an</option>
        </select>
        
        <select v-model="categoryFilter" class="filter-select">
          <option value="all">Toutes catégories</option>
          <option value="electronics">Électronique</option>
          <option value="clothes">Vêtements</option>
          <option value="food">Alimentaire</option>
        </select>
        
        <select v-model="statusFilter" class="filter-select">
          <option value="all">Tous statuts</option>
          <option value="delivered">Livrées</option>
          <option value="pending">En cours</option>
          <option value="cancelled">Annulées</option>
        </select>
        
        <button class="export-btn" @click="exportData">
          📥 Exporter
        </button>
      </div>
    </div>

    <!-- Cartes KPI -->
    <div class="cards-grid-top">
      <div class="dashboard-card card-kpi kpi-blue">
        <div class="kpi-content">
          <div class="kpi-info">
            <p class="kpi-label">Total Commandes</p>
            <h3 class="kpi-value">{{ filteredOrdersCount }}</h3>
            <span class="kpi-trend positive">↗ +12.5%</span>
          </div>
          <div class="kpi-icon">🛒</div>
        </div>
      </div>
      
      <div class="dashboard-card card-kpi kpi-green">
        <div class="kpi-content">
          <div class="kpi-info">
            <p class="kpi-label">Revenus Totaux</p>
            <h3 class="kpi-value">{{ formatCurrency(totalRevenue) }}</h3>
            <span class="kpi-trend positive">↗ +18.2%</span>
          </div>
          <div class="kpi-icon">💰</div>
        </div>
      </div>
      
      <div class="dashboard-card card-kpi kpi-purple">
        <div class="kpi-content">
          <div class="kpi-info">
            <p class="kpi-label">Produits Actifs</p>
            <h3 class="kpi-value">{{ activeProducts }}</h3>
            <span class="kpi-trend positive">↗ +5 nouveaux</span>
          </div>
          <div class="kpi-icon">📦</div>
        </div>
      </div>
    </div>
    
    <!-- Graphiques principaux - Conteneur unique -->
    <div class="charts-container">
      <!-- Statistiques Commandes -->        
      <h3 class="card-title-centered">📊 Statistiques des Commandes</h3>

      <div class="dashboard-card chart-card">
        <!-- Graphique d'évolution -->
        <div class="chart-section">
          <canvas ref="ordersChart"></canvas>
        </div>

        <!-- Indicateurs clés -->
        <div class="stats-grid">
          <div class="stat-box" v-for="(item, idx) in keyStats" :key="idx">
            <span class="label">{{ item.label }}</span>
            <span class="value">{{ item.value }}</span>
          </div>
        </div>

        <!-- Répartition par statut -->
        <div class="status-section">
          <h4>Répartition des statuts</h4>
          <div
            v-for="status in orderStatuses"
            :key="status.name"
            class="status-row"
          >
            <div class="status-info">
              <span class="status-name">{{ status.name }}</span>
              <span class="status-count">{{ status.count }}</span>
            </div>
            <div class="status-bar">
              <div
                class="status-progress"
                :style="{ width: status.percentage + '%', backgroundColor: status.color }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Statistiques Produits -->        
      <h3 class="card-title-centered">📦 Statistiques des Produits</h3>

      <div class="dashboard-card chart-card">
        
        <!-- Graphique répartition -->
        <div class="chart-container">
          <canvas ref="productsChart"></canvas>
        </div>
        
        <!-- Top produits -->
        <div class="top-products">
          <h4 class="section-subtitle">Top 5 Produits</h4>
          <div class="products-list">
            <div v-for="(product, index) in topProducts" :key="index" class="product-item">
              <div class="product-rank">{{ index + 1 }}</div>
              <div class="product-info">
                <span class="product-name">{{ product.name }}</span>
                <span class="product-sales">{{ product.sales }} ventes</span>
              </div>
              <span class="product-revenue">{{ formatCurrency(product.revenue) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Statistiques Fournisseurs -->        
      <h3 class="card-title-centered">🏢 Statistiques des Fournisseurs</h3>

      <div class="dashboard-card chart-card">
        
        <div class="suppliers-container">
          <!-- Graphique performance -->
          <div class="suppliers-chart">
            <canvas ref="suppliersChart"></canvas>
          </div>
          
          <!-- Tableau fournisseurs -->
          <div class="suppliers-table">
            <table>
              <thead>
                <tr>
                  <th>Fournisseur</th>
                  <th>Commandes</th>
                  <th>Fiabilité</th>
                  <th>Délai moyen</th>
                  <th>Statut</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="supplier in suppliers" :key="supplier.name">
                  <td class="supplier-name">{{ supplier.name }}</td>
                  <td>{{ supplier.orders }}</td>
                  <td>
                    <div class="reliability-badge" :class="getReliabilityClass(supplier.reliability)">
                      {{ supplier.reliability }}%
                    </div>
                  </td>
                  <td>{{ supplier.avgDelay }}j</td>
                  <td>
                    <span class="status-badge" :class="supplier.status">
                      {{ supplier.statusLabel }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'StatisticsView',
  data() {
    return {
      dateFilter: '30',
      categoryFilter: 'all',
      statusFilter: 'all',
      
      // Données KPI
      filteredOrdersCount: 1345,
      totalRevenue: 110300,
      activeProducts: 456,
      averageBasket: 82.05,
      conversionRate: 3.2,
      ordersPerDay: 44.8,
      
      // Statuts commandes
      orderStatuses: [
        { name: 'Livrées', count: 856, percentage: 64, color: '#10B981' },
        { name: 'En cours', count: 312, percentage: 23, color: '#3B82F6' },
        { name: 'En attente', count: 134, percentage: 10, color: '#F59E0B' },
        { name: 'Annulées', count: 43, percentage: 3, color: '#EF4444' }
      ],
      
      // Top produits
      topProducts: [
        { name: 'iPhone 15 Pro', sales: 234, revenue: 234000 },
        { name: 'MacBook Air M3', sales: 189, revenue: 189000 },
        { name: 'AirPods Pro', sales: 456, revenue: 91200 },
        { name: 'iPad Air', sales: 178, revenue: 106800 },
        { name: 'Apple Watch', sales: 267, revenue: 106800 }
      ],
      
      // Fournisseurs
      suppliers: [
        { name: 'TechSupply Co.', orders: 156, reliability: 98, avgDelay: 2, status: 'active', statusLabel: 'Actif' },
        { name: 'Global Parts Ltd', orders: 142, reliability: 95, avgDelay: 3, status: 'active', statusLabel: 'Actif' },
        { name: 'Express Logistics', orders: 128, reliability: 92, avgDelay: 4, status: 'active', statusLabel: 'Actif' },
        { name: 'Prime Distributors', orders: 98, reliability: 89, avgDelay: 5, status: 'warning', statusLabel: 'Surveillance' },
        { name: 'Quick Trade Inc', orders: 76, reliability: 94, avgDelay: 3, status: 'active', statusLabel: 'Actif' }
      ],
      
      // Graphiques
      ordersChartInstance: null,
      productsChartInstance: null,
      suppliersChartInstance: null
    };
  },
  
  mounted() {
    this.initCharts();
  },
  
  beforeUnmount() {
    if (this.ordersChartInstance) this.ordersChartInstance.destroy();
    if (this.productsChartInstance) this.productsChartInstance.destroy();
    if (this.suppliersChartInstance) this.suppliersChartInstance.destroy();
  },
  
  methods: {
    initCharts() {
      this.createOrdersChart();
      this.createProductsChart();
      this.createSuppliersChart();
    },
    
    createOrdersChart() {
      const ctx = this.$refs.ordersChart.getContext('2d');
      
      const data = {
        labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
        datasets: [
          {
            label: 'Commandes',
            data: [145, 189, 234, 198, 267, 312],
            backgroundColor: '#3B82F6',
            borderColor: '#2563eb',
            borderWidth: 2,
            borderRadius: 6,
            borderSkipped: false,
          },
          {
            label: 'Revenus (x100)',
            data: [125, 158, 189, 162, 214, 256],
            backgroundColor: '#10B981',
            borderColor: '#059669',
            borderWidth: 2,
            borderRadius: 6,
            borderSkipped: false,
          }
        ]
      };
      
      this.ordersChartInstance = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top'
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
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
    
    createProductsChart() {
      const ctx = this.$refs.productsChart.getContext('2d');
      
      const data = {
        labels: ['Électronique', 'Vêtements', 'Alimentaire', 'Mobilier', 'Autres'],
        datasets: [{
          data: [35, 28, 20, 12, 5],
          backgroundColor: [
            '#3B82F6',
            '#10B981',
            '#F59E0B',
            '#8B5CF6',
            '#EC4899'
          ],
          borderWidth: 0
        }]
      };
      
      this.productsChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'bottom'
            }
          }
        }
      });
    },
    
    createSuppliersChart() {
      const ctx = this.$refs.suppliersChart.getContext('2d');
      
      const data = {
        labels: ['TechSupply Co.', 'Global Parts', 'Express Log.', 'Prime Dist.', 'Quick Trade'],
        datasets: [{
          label: 'Fiabilité (%)',
          data: [98, 95, 92, 89, 94],
          backgroundColor: '#8B5CF6',
          borderRadius: 6
        }]
      };
      
      this.suppliersChartInstance = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              max: 100,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              }
            },
            y: {
              grid: {
                display: false
              }
            }
          }
        }
      });
    },
    
    formatCurrency(value) {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'CFA',
        minimumFractionDigits: 0
      }).format(value);
    },
    
    getReliabilityClass(reliability) {
      if (reliability >= 95) return 'high';
      if (reliability >= 90) return 'medium';
      return 'low';
    },
    
    exportData() {
      alert('Export des données en cours...');
    }
  }
};
</script>

<style scoped>
  .statistics-page {
    padding: 24px;
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    min-height: 100vh;
  }

  /* En-tête */
  .page-header {
    margin-bottom: 32px;
  }

  .page-title {
    font-size: 32px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 20px;
  }

  .filters-container {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    background: white;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    border: 1px solid #e5e7eb;
  }

  .filter-select {
    padding: 10px 16px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    background: white;
    font-size: 14px;
    color: #475569;
    cursor: pointer;
    transition: all 0.2s;
  }

  .filter-select:hover {
    border-color: #3B82F6;
  }

  .filter-select:focus {
    outline: none;
    border-color: #3B82F6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .export-btn {
    margin-left: auto;
    padding: 10px 20px;
    background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }

  .export-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  }

  /* Grilles */
  .cards-grid-top {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 20px;
  }

  /* Conteneur des graphiques en ligne */
  .charts-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 2px;
  }

  .dashboard-card {
    background: white;
    border-radius: 16px;
    padding: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
    transition: all 0.3s;
  }

  /* Cartes de graphiques avec padding réduit */
  .chart-card {
    padding: 10px;
    min-height: 300px;
  }

  .dashboard-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }

  /* Cartes KPI */
  .card-kpi {
    overflow: hidden;
    position: relative;
  }

  .kpi-blue { background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%); }
  .kpi-green { background: linear-gradient(135deg, #10B981 0%, #059669 100%); }
  .kpi-purple { background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%); }

  .kpi-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
  }

  .kpi-label {
    font-size: 14px;
    opacity: 0.9;
    margin-bottom: 8px;
    text-align: center;
  }

  .kpi-value {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 8px;
  }

  .kpi-trend {
    font-size: 14px;
    font-weight: 600;
  }

  .kpi-trend.positive {
    color: rgba(255, 255, 255, 0.95);
  }

  .kpi-icon {
    font-size: 48px;
    opacity: 0.3;
  }

  /* Cartes principales */
  .card-bottom {
    min-height: 500px;
  }

  .card-title {
    font-size: 20px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 24px;
  }

  /* Titre centré pour les cartes de graphiques */
  .card-title-centered {
    font-size: 20px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 16px;
    text-align: center;
  }


  /* Graphiques */
  .chart-container {
    height: 220px;
    margin-bottom: 16px;
  }

  .chart-section {
    height: 220px;
    margin-bottom: 16px;
  }

  /* Stats grid */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 16px;
  }

  .stat-item {
    background: #f8fafc;
    padding: 12px;
    border-radius: 8px;
    text-align: center;
  }

  .stat-label {
    display: block;
    font-size: 12px;
    color: #64748b;
    margin-bottom: 8px;
  }

  .stat-value {
    display: block;
    font-size: 20px;
    font-weight: 700;
    color: #1e293b;
  }

  /* Barres de statut */
  .status-bars {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .status-bar-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 14px;
  }

  .status-name {
    font-weight: 600;
    color: #475569;
  }

  .status-count {
    color: #64748b;
  }

  .status-bar-bg {
    height: 12px;
    background: #f1f5f9;
    border-radius: 6px;
    overflow: hidden;
  }

  .status-bar-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.8s ease;
  }

  /* Produits */
  .section-subtitle {
    font-size: 16px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 16px;
  }

  .products-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .product-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px;
    background: #f8fafc;
    border-radius: 8px;
    transition: all 0.2s;
  }

  .product-item:hover {
    background: #f1f5f9;
    transform: translateX(4px);
  }

  .product-rank {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
  }

  .product-info {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .product-name {
    font-weight: 600;
    color: #1e293b;
    font-size: 14px;
  }

  .product-sales {
    font-size: 12px;
    color: #64748b;
  }

  .product-revenue {
    font-weight: 700;
    color: #10B981;
    font-size: 14px;
  }

  /* Fournisseurs - maintenant dans le conteneur principal */

  .suppliers-container {
    display: grid;
    grid-template-columns: 1fr 1.5fr;
    gap: 20px;
  }

  .suppliers-chart {
    height: 250px;
  }

  .suppliers-table {
    overflow-x: auto;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }

  thead {
    background: #f8fafc;
  }

  th {
    padding: 12px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
    color: #475569;
    border-bottom: 2px solid #e5e7eb;
  }

  td {
    padding: 12px;
    font-size: 14px;
    color: #1e293b;
    border-bottom: 1px solid #f1f5f9;
  }

  .supplier-name {
    font-weight: 600;
  }

  .reliability-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
  }

  .reliability-badge.high {
    background: #D1FAE5;
    color: #065F46;
  }

  .reliability-badge.medium {
    background: #FEF3C7;
    color: #92400E;
  }

  .reliability-badge.low {
    background: #FEE2E2;
    color: #991B1B;
  }

  .status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
  }

  .status-badge.active {
    background: #D1FAE5;
    color: #065F46;
  }

  .status-badge.warning {
    background: #FEF3C7;
    color: #92400E;
  }

  /* Responsive */
  @media (max-width: 1200px) {
    .cards-grid-top {
      grid-template-columns: repeat(2, 1fr);
    }
    
    .charts-container {
      gap: 16px;
    }
    
    .suppliers-container {
      grid-template-columns: 1fr;
    }
    
    .suppliers-chart {
      height: 250px;
    }
  }

  @media (max-width: 768px) {
    .statistics-page {
      padding: 16px;
    }
    
    .page-title {
      font-size: 24px;
      text-align: center;
    }
    
    .filters-container {
      flex-direction: column;
      gap: 8px;
    }
    
    .filter-select {
      width: 100%;
    }
    
    .export-btn {
      margin-left: 0;
      width: 100%;
    }
    
    .cards-grid-top {
      grid-template-columns: 1fr;
      gap: 16px;
    }
    
    .charts-container {
      gap: 16px;
    }
    
    .stats-grid {
      grid-template-columns: 1fr;
      gap: 12px;
    }
    
    .dashboard-card {
      padding: 16px;
    }
    
    .card-title {
      font-size: 18px;
    }
    
    .kpi-value {
      font-size: 28px;
    }
    
    .kpi-icon {
      font-size: 36px;
    }
    
    .chart-container {
      height: 180px;
    }
    
    .suppliers-chart {
      height: 200px;
    }
    
    .suppliers-table {
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }
    
    table {
      min-width: 500px;
    }
    
    th, td {
      padding: 8px;
      font-size: 12px;
    }
    
    .product-item {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }
    
    .product-rank {
      align-self: flex-start;
    }
  }

  @media (max-width: 480px) {
    .statistics-page {
      padding: 12px;
    }
    
    .page-title {
      font-size: 20px;
    }
    
    .dashboard-card {
      padding: 12px;
    }
    
    .card-title {
      font-size: 16px;
    }
    
    .kpi-value {
      font-size: 24px;
    }
    
    .kpi-icon {
      font-size: 32px;
    }
    
    .chart-container {
      height: 150px;
    }
    
    .suppliers-chart {
      height: 180px;
    }
    
    .stat-item {
      padding: 12px;
    }
    
    .stat-value {
      font-size: 16px;
    }
  }
</style>