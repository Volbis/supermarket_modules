<template>
  <div class="statistics-page">
    <!-- En-tête avec filtres -->
    <div class="page-header">
      <div class="filters-container">
        <select v-model="dateFilter" @change="loadStatistics" class="filter-select">
          <option value="7">7 derniers jours</option>
          <option value="30">30 derniers jours</option>
          <option value="90">90 derniers jours</option>
          <option value="365">1 an</option>
        </select>
        
        <select v-model="categoryFilter" @change="loadStatistics" class="filter-select">
          <option value="all">Toutes catégories</option>
          <option value="electronics">Électronique</option>
          <option value="clothes">Vêtements</option>
          <option value="food">Alimentaire</option>
        </select>
        
        <select v-model="statusFilter" @change="loadStatistics" class="filter-select">
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

    <!-- État de chargement -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Chargement des statistiques...</p>
    </div>

    <!-- Message d'erreur -->
    <div v-else-if="error" class="error-state">
      <p class="error-message">{{ error }}</p>
      <button @click="loadStatistics" class="retry-btn">Réessayer</button>
    </div>

    <!-- Contenu principal -->
    <div v-else>
      <!-- Cartes KPI -->
      <div class="cards-grid-top">
        <div class="dashboard-card card-kpi kpi-blue">
          <div class="kpi-content">
            <div class="kpi-info">
              <p class="kpi-label">Total Commandes</p>
              <h3 class="kpi-value">{{ filteredOrdersCount }}</h3>
              <span class="kpi-trend positive">↗ +{{ calculateGrowth('orders') }}%</span>
            </div>
            <div class="kpi-icon">🛒</div>
          </div>
        </div>
        
        <div class="dashboard-card card-kpi kpi-green">
          <div class="kpi-content">
            <div class="kpi-info">
              <p class="kpi-label">Revenus Totaux</p>
              <h3 class="kpi-value">{{ formatCurrency(totalRevenue) }}</h3>
              <span class="kpi-trend positive">↗ +{{ calculateGrowth('revenue') }}%</span>
            </div>
            <div class="kpi-icon">💰</div>
          </div>
        </div>
        
        <div class="dashboard-card card-kpi kpi-purple">
          <div class="kpi-content">
            <div class="kpi-info">
              <p class="kpi-label">Produits Vendus</p>
              <h3 class="kpi-value">{{ totalProductsSold }}</h3>
              <span class="kpi-trend positive">↗ +{{ calculateGrowth('products') }}%</span>
            </div>
            <div class="kpi-icon">📦</div>
          </div>
        </div>
      </div>
      
      <!-- Graphiques principaux -->
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
            <div v-if="topProducts.length > 0" class="products-list">
              <div v-for="(product, index) in topProducts" :key="index" class="product-item">
                <div class="product-rank">{{ index + 1 }}</div>
                <div class="product-info">
                  <span class="product-name">{{ product.name }}</span>
                  <span class="product-sales">{{ product.sales }} ventes</span>
                </div>
                <span class="product-revenue">{{ formatCurrency(product.revenue) }}</span>
              </div>
            </div>
            <div v-else class="no-data">
              <p>Aucune donnée de vente disponible</p>
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
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import historiqueVentesAPI from '@/services/historiqueVentesAPI';
import historiqueStockAPI from '@/services/historiqueStockAPI';

export default {
  name: 'StatisticsView',
  data() {
    return {
      loading: true,
      error: null,
      dateFilter: '30',
      categoryFilter: 'all',
      statusFilter: 'all',
      
      // Données brutes de l'API
      ventesData: [],
      stockData: [],
      
      // Données KPI
      filteredOrdersCount: 0,
      totalRevenue: 0,
      totalProductsSold: 0,
      averageBasket: 0,
      conversionRate: 3.2,
      ordersPerDay: 0,
      
      // Croissance (comparaison période précédente)
      previousPeriodData: {
        orders: 0,
        revenue: 0,
        products: 0
      },
      
      // Statuts commandes
      orderStatuses: [
        { name: 'Livrées', count: 0, percentage: 0, color: '#10B981' },
        { name: 'En cours', count: 0, percentage: 0, color: '#3B82F6' },
        { name: 'En attente', count: 0, percentage: 0, color: '#F59E0B' },
        { name: 'Annulées', count: 0, percentage: 0, color: '#EF4444' }
      ],
      
      // Top produits
      topProducts: [],
      
      // Fournisseurs
      suppliers: [],
      
      // Graphiques
      ordersChartInstance: null,
      productsChartInstance: null,
      suppliersChartInstance: null
    };
  },
  
  computed: {
    keyStats() {
      return [
        { label: 'Panier Moyen', value: this.formatCurrency(this.averageBasket) },
        { label: 'Commandes/jour', value: this.ordersPerDay.toFixed(1) },
        { label: 'Taux conversion', value: `${this.conversionRate}%` }
      ];
    }
  },
  
  mounted() {
    this.loadStatistics();
  },
  
  beforeUnmount() {
    this.destroyCharts();
  },
  
  methods: {
    async loadStatistics() {
      this.loading = true;
      this.error = null;
      
      try {
        // Calculer les dates selon le filtre
        const { dateDebut, dateFin } = this.calculateDateRange();
        
        // Charger les données de ventes
        const ventesResponse = await historiqueVentesAPI.getVentesByPeriode(dateDebut, dateFin);
        console.log('Réponse API ventes:', ventesResponse);
        
        // Adapter selon la structure de votre API
        this.ventesData = ventesResponse.data?.ventes || ventesResponse.data || [];
        
        // Charger les données d'historique stock
        const stockResponse = await historiqueStockAPI.getAllHistoriqueStock();
        console.log('Réponse API stock:', stockResponse);
        this.stockData = stockResponse.data || [];
        
        // Charger aussi la période précédente pour calculer la croissance
        await this.loadPreviousPeriodData(dateDebut);
        
        // Calculer les statistiques
        this.calculateKPIs();
        this.calculateTopProducts();
        this.calculateOrderStatuses();
        
        // Charger les fournisseurs (données simulées pour l'instant)
        this.loadSuppliersData();
        
        // Mettre à jour les graphiques
        this.$nextTick(() => {
          this.destroyCharts();
          this.initCharts();
        });
        
      } catch (error) {
        console.error('Erreur lors du chargement des statistiques:', error);
        this.error = 'Erreur lors du chargement des données. Veuillez réessayer.';
        
        if (this.$toast) {
          this.$toast.error('Erreur lors du chargement des statistiques');
        }
      } finally {
        this.loading = false;
      }
    },
    
    async loadPreviousPeriodData(dateDebut) {
      try {
        const days = parseInt(this.dateFilter);
        const previousDateFin = new Date(dateDebut);
        previousDateFin.setDate(previousDateFin.getDate() - 1);
        
        const previousDateDebut = new Date(previousDateFin);
        previousDateDebut.setDate(previousDateDebut.getDate() - days);
        
        const previousResponse = await historiqueVentesAPI.getVentesByPeriode(
          this.formatDate(previousDateDebut),
          this.formatDate(previousDateFin)
        );
        
        const previousVentes = previousResponse.data?.ventes || previousResponse.data || [];
        
        this.previousPeriodData.orders = previousVentes.length;
        this.previousPeriodData.revenue = previousVentes.reduce((sum, vente) => {
          return sum + parseFloat(vente.montant_total || 0);
        }, 0);
        this.previousPeriodData.products = previousVentes.reduce((sum, vente) => {
          return sum + parseInt(vente.quantite_vendue || 0);
        }, 0);
      } catch (error) {
        console.error('Erreur lors du chargement de la période précédente:', error);
        // Continuer même en cas d'erreur
      }
    },
    
    calculateDateRange() {
      const dateFin = new Date();
      const dateDebut = new Date();
      dateDebut.setDate(dateFin.getDate() - parseInt(this.dateFilter));
      
      return {
        dateDebut: this.formatDate(dateDebut),
        dateFin: this.formatDate(dateFin)
      };
    },
    
    formatDate(date) {
      return date.toISOString().split('T')[0];
    },
    
    calculateKPIs() {
      // Nombre total de commandes (transactions)
      this.filteredOrdersCount = this.ventesData.length;
      
      // Revenus totaux
      this.totalRevenue = this.ventesData.reduce((sum, vente) => {
        return sum + parseFloat(vente.montant_total || 0);
      }, 0);
      
      // Produits vendus
      this.totalProductsSold = this.ventesData.reduce((sum, vente) => {
        return sum + parseInt(vente.quantite_vendue || 0);
      }, 0);
      
      // Panier moyen
      this.averageBasket = this.filteredOrdersCount > 0 
        ? this.totalRevenue / this.filteredOrdersCount 
        : 0;
      
      // Commandes par jour
      const days = parseInt(this.dateFilter);
      this.ordersPerDay = days > 0 ? this.filteredOrdersCount / days : 0;
    },
    
    calculateTopProducts() {
      // Grouper les ventes par produit
      const productMap = {};
      
      this.ventesData.forEach(vente => {
        const produitNom = vente.produit_nom || 'Produit inconnu';
        
        if (!productMap[produitNom]) {
          productMap[produitNom] = {
            name: produitNom,
            sales: 0,
            revenue: 0
          };
        }
        
        productMap[produitNom].sales += parseInt(vente.quantite_vendue || 0);
        productMap[produitNom].revenue += parseFloat(vente.montant_total || 0);
      });
      
      // Convertir en tableau et trier par revenus
      this.topProducts = Object.values(productMap)
        .sort((a, b) => b.revenue - a.revenue)
        .slice(0, 5);
    },
    
    calculateOrderStatuses() {
      // Simulation de répartition des statuts (à adapter selon vos données)
      const total = this.filteredOrdersCount;
      
      if (total === 0) {
        this.orderStatuses.forEach(status => {
          status.count = 0;
          status.percentage = 0;
        });
        return;
      }
      
      this.orderStatuses[0].count = Math.floor(total * 0.64); // Livrées
      this.orderStatuses[1].count = Math.floor(total * 0.23); // En cours
      this.orderStatuses[2].count = Math.floor(total * 0.10); // En attente
      this.orderStatuses[3].count = total - this.orderStatuses[0].count - 
                                     this.orderStatuses[1].count - 
                                     this.orderStatuses[2].count; // Annulées
      
      // Calculer les pourcentages
      this.orderStatuses.forEach(status => {
        status.percentage = total > 0 ? (status.count / total) * 100 : 0;
      });
    },
    
    loadSuppliersData() {
      // Données simulées pour les fournisseurs
      // À remplacer par un appel API réel si disponible
      this.suppliers = [
        { name: 'TechSupply Co.', orders: 156, reliability: 98, avgDelay: 2, status: 'active', statusLabel: 'Actif' },
        { name: 'Global Parts Ltd', orders: 142, reliability: 95, avgDelay: 3, status: 'active', statusLabel: 'Actif' },
        { name: 'Express Logistics', orders: 128, reliability: 92, avgDelay: 4, status: 'active', statusLabel: 'Actif' },
        { name: 'Prime Distributors', orders: 98, reliability: 89, avgDelay: 5, status: 'warning', statusLabel: 'Surveillance' },
        { name: 'Quick Trade Inc', orders: 76, reliability: 94, avgDelay: 3, status: 'active', statusLabel: 'Actif' }
      ];
    },
    
    calculateGrowth(type) {
      let currentValue, previousValue;
      
      switch(type) {
        case 'orders':
          currentValue = this.filteredOrdersCount;
          previousValue = this.previousPeriodData.orders;
          break;
        case 'revenue':
          currentValue = this.totalRevenue;
          previousValue = this.previousPeriodData.revenue;
          break;
        case 'products':
          currentValue = this.totalProductsSold;
          previousValue = this.previousPeriodData.products;
          break;
        default:
          return 0;
      }
      
      if (previousValue === 0) return 0;
      
      const growth = ((currentValue - previousValue) / previousValue) * 100;
      return Math.abs(growth).toFixed(1);
    },
    
    destroyCharts() {
      if (this.ordersChartInstance) this.ordersChartInstance.destroy();
      if (this.productsChartInstance) this.productsChartInstance.destroy();
      if (this.suppliersChartInstance) this.suppliersChartInstance.destroy();
    },
    
    initCharts() {
      this.createOrdersChart();
      this.createProductsChart();
      this.createSuppliersChart();
    },
    
    createOrdersChart() {
      const ctx = this.$refs.ordersChart?.getContext('2d');
      if (!ctx) return;
      
      // Grouper les ventes par période (jour, semaine ou mois selon le filtre)
      const salesByPeriod = this.groupSalesByPeriod();
      
      const data = {
        labels: salesByPeriod.labels,
        datasets: [
          {
            label: 'Commandes',
            data: salesByPeriod.orders,
            backgroundColor: '#3B82F6',
            borderColor: '#2563eb',
            borderWidth: 2,
            borderRadius: 6,
            borderSkipped: false,
          },
          {
            label: 'Revenus (÷1000)',
            data: salesByPeriod.revenue.map(v => v / 1000),
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
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  let label = context.dataset.label || '';
                  if (label) {
                    label += ': ';
                  }
                  if (context.parsed.y !== null) {
                    if (context.dataset.label === 'Revenus (÷1000)') {
                      label += (context.parsed.y * 1000).toFixed(0) + ' XOF';
                    } else {
                      label += context.parsed.y;
                    }
                  }
                  return label;
                }
              }
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
    
    groupSalesByPeriod() {
      const periodMap = {};
      const days = parseInt(this.dateFilter);
      
      // Choisir le format selon la période
      let formatDate;
      if (days <= 7) {
        // Par jour pour 7 jours
        formatDate = (date) => {
          const options = { weekday: 'short', day: 'numeric' };
          return new Date(date).toLocaleDateString('fr-FR', options);
        };
      } else if (days <= 90) {
        // Par semaine pour 30-90 jours
        formatDate = (date) => {
          const d = new Date(date);
          const weekNum = Math.ceil((d.getDate()) / 7);
          return `S${weekNum} ${d.toLocaleDateString('fr-FR', { month: 'short' })}`;
        };
      } else {
        // Par mois pour 1 an
        formatDate = (date) => {
          return new Date(date).toLocaleDateString('fr-FR', { month: 'short', year: 'numeric' });
        };
      }
      
      this.ventesData.forEach(vente => {
        const dateKey = formatDate(vente.date_vente);
        
        if (!periodMap[dateKey]) {
          periodMap[dateKey] = { orders: 0, revenue: 0 };
        }
        
        periodMap[dateKey].orders++;
        periodMap[dateKey].revenue += parseFloat(vente.montant_total || 0);
      });
      
      const labels = Object.keys(periodMap);
      const orders = labels.map(label => periodMap[label].orders);
      const revenue = labels.map(label => periodMap[label].revenue);
      
      return { labels, orders, revenue };
    },
    
    createProductsChart() {
      const ctx = this.$refs.productsChart?.getContext('2d');
      if (!ctx) return;
      
      // Utiliser les données des top produits
      const labels = this.topProducts.length > 0 
        ? this.topProducts.map(p => p.name) 
        : ['Aucune donnée'];
      const dataValues = this.topProducts.length > 0
        ? this.topProducts.map(p => p.revenue)
        : [1];
      
      const data = {
        labels: labels,
        datasets: [{
          data: dataValues,
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
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.parsed || 0;
                  return label + ': ' + value.toFixed(0) + ' XOF';
                }
              }
            }
          }
        }
      });
    },
    
    createSuppliersChart() {
      const ctx = this.$refs.suppliersChart?.getContext('2d');
      if (!ctx) return;
      
      const data = {
        labels: this.suppliers.map(s => s.name),
        datasets: [{
          label: 'Fiabilité (%)',
          data: this.suppliers.map(s => s.reliability),
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
        currency: 'XOF',
        minimumFractionDigits: 0
      }).format(value);
    },
    
    getReliabilityClass(reliability) {
      if (reliability >= 95) return 'high';
      if (reliability >= 90) return 'medium';
      return 'low';
    },
    
    exportData() {
      if (this.ventesData.length === 0) {
        if (this.$toast) {
          this.$toast.warning('Aucune donnée à exporter');
        }
        return;
      }
      
      // Créer un CSV avec les données
      const csvData = this.ventesData.map(vente => ({
        Date: vente.date_vente,
        Produit: vente.produit_nom,
        Quantité: vente.quantite_vendue,
        Montant: vente.montant_total
      }));
      
      const csv = this.convertToCSV(csvData);
      const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `statistiques-${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    },
    
    convertToCSV(data) {
      if (data.length === 0) return '';
      
      const headers = Object.keys(data[0]).join(',');
      const rows = data.map(row => Object.values(row).map(val => `"${val}"`).join(','));
      
      return [headers, ...rows].join('\n');
    }
  }
};
</script>

<style scoped>
/* Reprise du CSS existant avec ajout pour les erreurs */
.statistics-page {
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  min-height: 100vh;
}

/* État de chargement */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #3B82F6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  color: #64748b;
  font-size: 16px;
}

/* État d'erreur */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
}

.error-message {
  color: #EF4444;
  font-size: 16px;
  font-weight: 600;
}

.retry-btn {
  padding: 10px 20px;
  background: #3B82F6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.retry-btn:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.no-data {
  padding: 32px;
  text-align: center;
  color: #64748b;
  background: #f8fafc;
  border-radius: 8px;
}

.no-data p {
  margin: 0;
  font-size: 14px;
}

/* En-tête */
.page-header {
  margin-bottom: 32px;
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

.stat-box {
  background: #f8fafc;
  padding: 12px;
  border-radius: 8px;
  text-align: center;
}

.stat-box .label {
  display: block;
  font-size: 12px;
  color: #64748b;
  margin-bottom: 8px;
}

.stat-box .value {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

/* Section statut */
.status-section {
  margin-top: 16px;
}

.status-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 16px;
}

.status-row {
  margin-bottom: 12px;
}

.status-info {
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

.status-bar {
  height: 12px;
  background: #f1f5f9;
  border-radius: 6px;
  overflow: hidden;
}

.status-progress {
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
  flex-shrink: 0;
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

/* Fournisseurs */
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
  
  .dashboard-card {
    padding: 12px;
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
  
  .stat-box {
    padding: 12px;
  }
  
  .stat-box .value {
    font-size: 16px;
  }
}
</style>