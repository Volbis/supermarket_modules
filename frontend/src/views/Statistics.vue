<template>
  <div class="statistics-page">
    <!-- En-tête avec filtres -->
    <div class="page-header">
      <div class="filters-container">
        <div class="filter-group">
          <label class="filter-label">📅 Période</label>
          <select v-model="dateFilter" @change="applyFilters" class="filter-select">
            <option value="7">7 derniers jours</option>
            <option value="30">30 derniers jours</option>
            <option value="90">90 derniers jours</option>
            <option value="180">6 mois</option>
            <option value="365">1 an</option>
            <option value="all">Tout</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label class="filter-label">📦 Produit</label>
          <select v-model="productFilter" @change="applyFilters" class="filter-select">
            <option value="all">Tous les produits</option>
            <option v-for="product in availableProducts" :key="product" :value="product">
              {{ product }}
            </option>
          </select>
        </div>
        
        <div class="filter-group">
          <label class="filter-label">💰 Montant</label>
          <select v-model="amountFilter" @change="applyFilters" class="filter-select">
            <option value="all">Tous montants</option>
            <option value="low">Moins de 10 000 XOF</option>
            <option value="medium">10 000 - 50 000 XOF</option>
            <option value="high">Plus de 50 000 XOF</option>
          </select>
        </div>
        
        <button class="reset-btn" @click="resetFilters" title="Réinitialiser les filtres">
          🔄 Réinitialiser
        </button>
        
        <button class="export-btn" @click="exportData">
          📥 Exporter
        </button>
      </div>
      
      <!-- Indicateurs de filtres actifs -->
      <div v-if="hasActiveFilters" class="active-filters">
        <span class="filter-badge">Filtres actifs:</span>
        <span v-if="dateFilter !== '30'" class="filter-tag">
          📅 {{ getDateFilterLabel() }}
          <button @click="dateFilter = '30'; applyFilters()" class="remove-filter">×</button>
        </span>
        <span v-if="productFilter !== 'all'" class="filter-tag">
          📦 {{ productFilter }}
          <button @click="productFilter = 'all'; applyFilters()" class="remove-filter">×</button>
        </span>
        <span v-if="amountFilter !== 'all'" class="filter-tag">
          💰 {{ getAmountFilterLabel() }}
          <button @click="amountFilter = 'all'; applyFilters()" class="remove-filter">×</button>
        </span>
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
import historiqueVentesAPI from '@/services/historiqueVentes';
import historiqueStockAPI from '@/services/historiqueStock';
import { useDataCache } from '@/composables/useDataCache';

export default {
  name: 'StatisticsView',
  setup() {
    const { loadWithCache, invalidateCache } = useDataCache();
    return { loadWithCache, invalidateCache };
  },
  data() {
    return {
      loading: true,
      error: null,
      dateFilter: '30',
      productFilter: 'all',
      amountFilter: 'all',
      
      // Données brutes de l'API
      ventesData: [],
      ventesDataRaw: [], // Données non filtrées
      stockData: [],
      availableProducts: [], // Liste des produits disponibles
      
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
    },
    
    hasActiveFilters() {
      return this.dateFilter !== '30' || 
             this.productFilter !== 'all' || 
             this.amountFilter !== 'all';
    }
  },
  
  mounted() {
    // Charger avec cache si disponible
    this.loadStatistics(false);
  },
  
  beforeUnmount() {
    this.destroyCharts();
  },
  
  methods: {
    // === MÉTHODE PUBLIQUE POUR REFRESH DEPUIS APP.VUE ===
    async refreshData() {
      console.log('🔄 Rafraîchissement forcé des Statistiques...');
      this.invalidateCache('ventes');
      this.invalidateCache('stocks');
      await this.loadStatistics(true);
      if (this.$toast) {
        this.$toast.success('✅ Statistiques actualisées');
      }
    },
    
    async loadStatistics(forceRefresh = false) {
      // Ne montrer le loading QUE si on force le refresh ou si pas de données
      const showLoading = forceRefresh || !this.ventesDataRaw.length;
      
      if (showLoading) {
        this.loading = true;
      }
      this.error = null;
      
      try {
        // Calculer les dates selon le filtre
        const { dateDebut } = this.calculateDateRange();
        
        // Charger les données de ventes avec cache
        this.ventesDataRaw = await this.loadWithCache('ventes', async () => {
          const ventesResponse = await historiqueVentesAPI.getAllHistoriqueVentes();
          console.log('📦 Ventes chargées depuis l\'API:', ventesResponse.data);
          return ventesResponse.data?.ventes || ventesResponse.data || [];
        }, forceRefresh);
        
        // Extraire les produits disponibles
        this.extractAvailableProducts();
        
        // Appliquer les filtres
        this.applyFilters();
        
        // Charger les données d'historique stock avec cache
        this.stockData = await this.loadWithCache('stocks', async () => {
          const stockResponse = await historiqueStockAPI.getAllHistoriqueStock();
          console.log('📦 Stocks chargés depuis l\'API:', stockResponse.data);
          return stockResponse.data || [];
        }, forceRefresh);
        
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
          
          // Attendre un peu pour s'assurer que le DOM est bien rendu
          setTimeout(() => {
            console.log('Initialisation des graphiques...');
            this.initCharts();
          }, 100);
        });
        
      } catch (error) {
        console.error('Erreur lors du chargement des statistiques:', error);
        this.error = 'Erreur lors du chargement des données. Veuillez réessayer.';
        
        if (this.$toast) {
          this.$toast.error('Erreur lors du chargement des statistiques');
        }
      } finally {
        if (showLoading) {
          this.loading = false;
        }
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
      console.log('=== INITIALISATION DES GRAPHIQUES ===');
      console.log('ventesData:', this.ventesData.length);
      console.log('topProducts:', this.topProducts.length);
      console.log('suppliers:', this.suppliers.length);
      
      try {
        this.createOrdersChart();
        this.createProductsChart();
        this.createSuppliersChart();
        console.log('✅ Graphiques créés avec succès');
      } catch (error) {
        console.error('❌ Erreur lors de la création des graphiques:', error);
      }
    },
    
    createOrdersChart() {
      const canvas = this.$refs.ordersChart;
      console.log('Canvas ordersChart:', canvas);
      
      if (!canvas) {
        console.error('Canvas ordersChart non trouvé');
        return;
      }
      
      const ctx = canvas.getContext('2d');
      if (!ctx) {
        console.error('Contexte 2D non disponible');
        return;
      }
      
      console.log('Création du graphique des commandes...');
      
      // Grouper les ventes par période (jour, semaine ou mois selon le filtre)
      const salesByPeriod = this.groupSalesByPeriod();
      console.log('Données groupées:', salesByPeriod);
      
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
      
      try {
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
      
      console.log('✅ Graphique des commandes créé');
      } catch (error) {
        console.error('❌ Erreur création graphique commandes:', error);
      }
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
      
      // Si aucune donnée, retourner des valeurs par défaut
      if (labels.length === 0) {
        return {
          labels: ['Aucune donnée'],
          orders: [0],
          revenue: [0]
        };
      }
      
      return { labels, orders, revenue };
    },
    
    createProductsChart() {
      const canvas = this.$refs.productsChart;
      console.log('Canvas productsChart:', canvas);
      
      if (!canvas) {
        console.error('Canvas productsChart non trouvé');
        return;
      }
      
      const ctx = canvas.getContext('2d');
      if (!ctx) {
        console.error('Contexte 2D non disponible pour productsChart');
        return;
      }
      
      console.log('Création du graphique des produits...');
      
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
      
      try {
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
      
      console.log('✅ Graphique des produits créé');
      } catch (error) {
        console.error('❌ Erreur création graphique produits:', error);
      }
    },
    
    createSuppliersChart() {
      const canvas = this.$refs.suppliersChart;
      console.log('Canvas suppliersChart:', canvas);
      
      if (!canvas) {
        console.error('Canvas suppliersChart non trouvé');
        return;
      }
      
      const ctx = canvas.getContext('2d');
      if (!ctx) {
        console.error('Contexte 2D non disponible pour suppliersChart');
        return;
      }
      
      console.log('Création du graphique des fournisseurs...');
      
      const data = {
        labels: this.suppliers.map(s => s.name),
        datasets: [{
          label: 'Fiabilité (%)',
          data: this.suppliers.map(s => s.reliability),
          backgroundColor: '#8B5CF6',
          borderRadius: 6
        }]
      };
      
      try {
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
      
      console.log('✅ Graphique des fournisseurs créé');
      } catch (error) {
        console.error('❌ Erreur création graphique fournisseurs:', error);
      }
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
    },
    
    // === MÉTHODES DE FILTRAGE ===
    
    extractAvailableProducts() {
      const productsSet = new Set();
      this.ventesDataRaw.forEach(vente => {
        const produitNom = vente.produit_nom || 'Produit inconnu';
        productsSet.add(produitNom);
      });
      this.availableProducts = Array.from(productsSet).sort();
    },
    
    applyFilters() {
      console.log('Application des filtres...', {
        date: this.dateFilter,
        product: this.productFilter,
        amount: this.amountFilter
      });
      
      let filteredData = [...this.ventesDataRaw];
      
      // Filtre par période
      if (this.dateFilter !== 'all') {
        const days = parseInt(this.dateFilter);
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - days);
        
        filteredData = filteredData.filter(vente => {
          const venteDate = new Date(vente.date_vente);
          return venteDate >= cutoffDate;
        });
      }
      
      // Filtre par produit
      if (this.productFilter !== 'all') {
        filteredData = filteredData.filter(vente => {
          return vente.produit_nom === this.productFilter;
        });
      }
      
      // Filtre par montant
      if (this.amountFilter !== 'all') {
        filteredData = filteredData.filter(vente => {
          const montant = parseFloat(vente.montant_total || 0);
          
          switch(this.amountFilter) {
            case 'low':
              return montant < 10000;
            case 'medium':
              return montant >= 10000 && montant <= 50000;
            case 'high':
              return montant > 50000;
            default:
              return true;
          }
        });
      }
      
      this.ventesData = filteredData;
      
      console.log(`Résultats filtrés: ${filteredData.length} sur ${this.ventesDataRaw.length}`);
      
      // Recalculer les statistiques
      this.calculateKPIs();
      this.calculateTopProducts();
      this.calculateOrderStatuses();
      
      // Recharger les fournisseurs (données simulées)
      this.loadSuppliersData();
      
      // Mettre à jour les graphiques
      this.$nextTick(() => {
        this.destroyCharts();
        
        setTimeout(() => {
          console.log('Mise à jour des graphiques avec filtres...');
          this.initCharts();
        }, 100);
      });
    },
    
    resetFilters() {
      console.log('Réinitialisation des filtres');
      this.dateFilter = '30';
      this.productFilter = 'all';
      this.amountFilter = 'all';
      this.applyFilters();
    },
    
    getDateFilterLabel() {
      const labels = {
        '7': '7 jours',
        '30': '30 jours',
        '90': '90 jours',
        '180': '6 mois',
        '365': '1 an',
        'all': 'Tout'
      };
      return labels[this.dateFilter] || this.dateFilter;
    },
    
    getAmountFilterLabel() {
      const labels = {
        'low': 'Moins de 10K',
        'medium': '10K - 50K',
        'high': 'Plus de 50K'
      };
      return labels[this.amountFilter] || 'Tous montants';
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
  align-items: flex-end;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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

.reset-btn {
  padding: 10px 20px;
  background: white;
  color: #64748b;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.reset-btn:hover {
  border-color: #3B82F6;
  color: #3B82F6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

/* Filtres actifs */
.active-filters {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  background: #f8fafc;
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 12px;
  border: 1px solid #e5e7eb;
}

.filter-badge {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
  color: white;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.remove-filter {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  background: rgba(255, 255, 255, 0.3);
  border: none;
  border-radius: 50%;
  color: white;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-filter:hover {
  background: rgba(255, 255, 255, 0.5);
  transform: scale(1.1);
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
  padding: 24px;
  min-height: 400px;
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
  height: 300px;
  margin-bottom: 24px;
  position: relative;
}

.chart-section {
  height: 300px;
  margin-bottom: 24px;
  position: relative;
}

.chart-container canvas,
.chart-section canvas,
.suppliers-chart canvas {
  max-width: 100%;
  max-height: 100%;
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
.top-products {
  margin-top: 16px;
}

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
  height: 300px;
  position: relative;
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
    gap: 12px;
    align-items: stretch;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .filter-select {
    width: 100%;
  }
  
  .reset-btn,
  .export-btn {
    margin-left: 0;
    width: 100%;
  }
  
  .active-filters {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-tag {
    font-size: 12px;
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