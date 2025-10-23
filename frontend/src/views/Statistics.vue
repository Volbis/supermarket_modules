<template>
  <div class="statistics-page">
    <!-- En-tête avec filtres -->
    <div class="page-header">
      <div class="filters-container">
        <select v-model="dateFilter" @change="loadData" class="filter-select">
          <option value="7">7 derniers jours</option>
          <option value="30">30 derniers jours</option>
          <option value="90">90 derniers jours</option>
          <option value="365">1 an</option>
        </select>
        
        <select v-model="categoryFilter" @change="applyFilters" class="filter-select">
          <option value="all">Toutes catégories</option>
          <option v-for="cat in categories" :key="cat.id_categorie" :value="cat.id_categorie">
            {{ cat.nom }}
          </option>
        </select>
        
        <select v-model="statusFilter" @change="applyFilters" class="filter-select">
          <option value="all">Tous statuts</option>
          <option value="EN_COURS">En cours</option>
          <option value="LIVREE">Livrées</option>
          <option value="ANNULEE">Annulées</option>
        </select>
        
        <button class="export-btn" @click="exportData">
          📥 Exporter
        </button>
      </div>
    </div>

    <!-- Indicateur de chargement -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Chargement des données...</p>
    </div>

    <!-- Contenu principal -->
    <div v-else>
      <!-- Cartes KPI -->
      <div class="cards-grid-top">
        <div class="dashboard-card card-kpi kpi-blue">
          <div class="kpi-content">
            <div class="kpi-info">
              <p class="kpi-label">Total Commandes</p>
              <h3 class="kpi-value">{{ totalCommandes }}</h3>
              <span class="kpi-trend positive">↗ {{ commandesTrend }}%</span>
            </div>
            <div class="kpi-icon">🛒</div>
          </div>
        </div>
        
        <div class="dashboard-card card-kpi kpi-green">
          <div class="kpi-content">
            <div class="kpi-info">
              <p class="kpi-label">Revenus Totaux</p>
              <h3 class="kpi-value">{{ formatCurrency(totalRevenue) }}</h3>
              <span class="kpi-trend positive">↗ {{ revenueTrend }}%</span>
            </div>
            <div class="kpi-icon">💰</div>
          </div>
        </div>
        
        <div class="dashboard-card card-kpi kpi-purple">
          <div class="kpi-content">
            <div class="kpi-info">
              <p class="kpi-label">Produits Actifs</p>
              <h3 class="kpi-value">{{ totalProduits }}</h3>
              <span class="kpi-trend" :class="stockTrend >= 0 ? 'positive' : 'negative'">
                {{ stockTrend >= 0 ? '↗' : '↘' }} {{ Math.abs(stockTrend) }}%
              </span>
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
            <div class="stat-box">
              <span class="label">Panier moyen</span>
              <span class="value">{{ formatCurrency(averageBasket) }}</span>
            </div>
            <div class="stat-box">
              <span class="label">Taux conversion</span>
              <span class="value">{{ conversionRate }}%</span>
            </div>
            <div class="stat-box">
              <span class="label">Commandes/jour</span>
              <span class="value">{{ ordersPerDay }}</span>
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

        <!-- Statistiques Ventes -->        
        <h3 class="card-title-centered">💰 Historique des Ventes</h3>

        <div class="dashboard-card chart-card">
          <!-- Graphique évolution des ventes -->
          <div class="chart-section">
            <canvas ref="ventesChart"></canvas>
          </div>
          
          <!-- Top produits vendus -->
          <div class="top-products">
            <h4 class="section-subtitle">Top 5 Produits les Plus Vendus</h4>
            <div class="products-list">
              <div v-for="(product, index) in topProductsVendus" :key="index" class="product-item">
                <div class="product-rank">{{ index + 1 }}</div>
                <div class="product-info">
                  <span class="product-name">{{ product.nom }}</span>
                  <span class="product-sales">{{ product.quantite_totale }} unités vendues</span>
                </div>
                <span class="product-revenue">{{ formatCurrency(product.chiffre_affaires) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Statistiques Stock -->        
        <h3 class="card-title-centered">📦 Mouvements de Stock</h3>

        <div class="dashboard-card chart-card">
          <div class="chart-section">
            <canvas ref="stockChart"></canvas>
          </div>
          
          <!-- Statistiques stock -->
          <div class="stock-stats">
            <div class="stat-card stat-ajout">
              <div class="stat-icon">📈</div>
              <div class="stat-details">
                <span class="stat-label">Total Ajouts</span>
                <span class="stat-value">{{ totalAjouts }}</span>
                <span class="stat-subtitle">{{ ajoutsCount }} opérations</span>
              </div>
            </div>
            
            <div class="stat-card stat-retrait">
              <div class="stat-icon">📉</div>
              <div class="stat-details">
                <span class="stat-label">Total Retraits</span>
                <span class="stat-value">{{ totalRetraits }}</span>
                <span class="stat-subtitle">{{ retraitsCount }} opérations</span>
              </div>
            </div>
            
            <div class="stat-card stat-bilan">
              <div class="stat-icon">⚖️</div>
              <div class="stat-details">
                <span class="stat-label">Bilan Net</span>
                <span class="stat-value" :class="bilanNet >= 0 ? 'positive' : 'negative'">
                  {{ bilanNet >= 0 ? '+' : '' }}{{ bilanNet }}
                </span>
                <span class="stat-subtitle">Différence ajouts/retraits</span>
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
                    <th>Produits</th>
                    <th>Commandes</th>
                    <th>Délai</th>
                    <th>Statut</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="supplier in fournisseurs" :key="supplier.id_fournisseur">
                    <td class="supplier-name">{{ supplier.nom }}</td>
                    <td>{{ supplier.nombre_produits }}</td>
                    <td>{{ supplier.nombre_commandes }}</td>
                    <td>{{ supplier.delais_livraison_jours }}j</td>
                    <td>
                      <span class="status-badge active">Actif</span>
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
import historiqueVentesAPI from '../services/historiqueVentesAPI';
import historiqueStockAPI from '../services/historiqueStockAPI';
import produitsAPI from '../services/produitsAPI';
import commandesAPI from '../services/commandesAPI';
import fournisseursAPI from '../services/fournisseursAPI';
import categoriesAPI from '../services/categoriesAPI';

export default {
  name: 'StatisticsView',
  data() {
    return {
      loading: true,
      dateFilter: '30',
      categoryFilter: 'all',
      statusFilter: 'all',
      
      // Données brutes de l'API
      historiqueVentes: [],
      historiqueStock: [],
      produits: [],
      commandes: [],
      fournisseurs: [],
      categories: [],
      
      // KPI calculés
      totalCommandes: 0,
      totalRevenue: 0,
      totalProduits: 0,
      averageBasket: 0,
      conversionRate: 0,
      ordersPerDay: 0,
      commandesTrend: 0,
      revenueTrend: 0,
      stockTrend: 0,
      
      // Données de ventes
      topProductsVendus: [],
      ventesParMois: [],
      
      // Données de stock
      totalAjouts: 0,
      totalRetraits: 0,
      ajoutsCount: 0,
      retraitsCount: 0,
      bilanNet: 0,
      mouvementsParMois: [],
      
      // Statuts commandes
      orderStatuses: [],
      
      // Instances de graphiques
      ordersChartInstance: null,
      ventesChartInstance: null,
      stockChartInstance: null,
      suppliersChartInstance: null
    };
  },
  
  async mounted() {
    await this.loadData();
  },
  
  beforeUnmount() {
    this.destroyCharts();
  },
  
  methods: {
    async loadData() {
      this.loading = true;
      try {
        // Charger toutes les données en parallèle
        const [ventesRes, stockRes, produitsRes, commandesRes, fournisseursRes, categoriesRes] = await Promise.all([
          historiqueVentesAPI.getAllHistoriqueVentes(),
          historiqueStockAPI.getAllHistoriqueStock(),
          produitsAPI.getAllProduits(),
          commandesAPI.getAllCommandes(),
          fournisseursAPI.getAllFournisseurs(),
          categoriesAPI.getAllCategories()
        ]);
        
        this.historiqueVentes = ventesRes.data;
        this.historiqueStock = stockRes.data;
        this.produits = produitsRes.data;
        this.commandes = commandesRes.data;
        this.fournisseurs = fournisseursRes.data;
        this.categories = categoriesRes.data;
        
        // Calculer les statistiques
        this.calculateKPIs();
        this.calculateVentesStats();
        this.calculateStockStats();
        this.calculateCommandesStats();
        this.prepareFournisseursData();
        
        // Créer les graphiques après un court délai pour s'assurer que le DOM est prêt
        this.$nextTick(() => {
          this.destroyCharts();
          this.initCharts();
        });
        
      } catch (error) {
        console.error('Erreur lors du chargement des données:', error);
        alert('Erreur lors du chargement des statistiques');
      } finally {
        this.loading = false;
      }
    },
    
    calculateKPIs() {
      // Filtrer par période
      const dateLimit = this.getDateLimit();
      const ventesFiltered = this.historiqueVentes.filter(v => 
        new Date(v.date_vente) >= dateLimit
      );
      const commandesFiltered = this.commandes.filter(c => 
        new Date(c.date_commande) >= dateLimit
      );
      
      // Total commandes
      this.totalCommandes = commandesFiltered.length;
      
      // Total revenus
      this.totalRevenue = ventesFiltered.reduce((sum, v) => 
        sum + parseFloat(v.montant_total || 0), 0
      );
      
      // Total produits
      this.totalProduits = this.produits.length;
      
      // Panier moyen
      this.averageBasket = ventesFiltered.length > 0 
        ? this.totalRevenue / ventesFiltered.length 
        : 0;
      
      // Commandes par jour
      const days = parseInt(this.dateFilter);
      this.ordersPerDay = (this.totalCommandes / days).toFixed(1);
      
      // Taux de conversion (simulé)
      this.conversionRate = (Math.random() * 5 + 2).toFixed(1);
      
      // Trends (comparaison avec période précédente - simulé)
      this.commandesTrend = (Math.random() * 20 + 5).toFixed(1);
      this.revenueTrend = (Math.random() * 25 + 10).toFixed(1);
      this.stockTrend = (Math.random() * 10 - 2).toFixed(1);
    },
    
    calculateVentesStats() {
      const dateLimit = this.getDateLimit();
      const ventesFiltered = this.historiqueVentes.filter(v => 
        new Date(v.date_vente) >= dateLimit
      );
      
      // Top produits vendus
      const produitsMap = {};
      ventesFiltered.forEach(vente => {
        const produitId = vente.produit;
        if (!produitsMap[produitId]) {
          const produit = this.produits.find(p => p.id_product === produitId);
          produitsMap[produitId] = {
            nom: produit ? produit.nom : 'Produit inconnu',
            quantite_totale: 0,
            chiffre_affaires: 0
          };
        }
        produitsMap[produitId].quantite_totale += vente.quantite_vendue;
        produitsMap[produitId].chiffre_affaires += parseFloat(vente.montant_total || 0);
      });
      
      this.topProductsVendus = Object.values(produitsMap)
        .sort((a, b) => b.quantite_totale - a.quantite_totale)
        .slice(0, 5);
      
      // Ventes par mois
      this.ventesParMois = this.groupByMonth(ventesFiltered, 'date_vente');
    },
    
    calculateStockStats() {
      const dateLimit = this.getDateLimit();
      const stockFiltered = this.historiqueStock.filter(h => 
        new Date(h.date_modification) >= dateLimit
      );
      
      // Calculs totaux
      const ajouts = stockFiltered.filter(h => h.type_modification === 'AJOUT');
      const retraits = stockFiltered.filter(h => h.type_modification === 'RETRAIT');
      
      this.totalAjouts = ajouts.reduce((sum, h) => sum + h.quantite_modifiee, 0);
      this.totalRetraits = retraits.reduce((sum, h) => sum + h.quantite_modifiee, 0);
      this.ajoutsCount = ajouts.length;
      this.retraitsCount = retraits.length;
      this.bilanNet = this.totalAjouts - this.totalRetraits;
      
      // Mouvements par mois
      this.mouvementsParMois = this.groupStockByMonth(stockFiltered);
    },
    
    calculateCommandesStats() {
      const dateLimit = this.getDateLimit();
      const commandesFiltered = this.commandes.filter(c => 
        new Date(c.date_commande) >= dateLimit
      );
      
      // Répartition par statut
      const statusCount = {
        'EN_COURS': 0,
        'LIVREE': 0,
        'ANNULEE': 0
      };
      
      commandesFiltered.forEach(c => {
        if (statusCount.hasOwnProperty(c.statut)) {
          statusCount[c.statut]++;
        }
      });
      
      const total = commandesFiltered.length || 1;
      this.orderStatuses = [
        { 
          name: 'Livrées', 
          count: statusCount.LIVREE, 
          percentage: (statusCount.LIVREE / total * 100).toFixed(0), 
          color: '#10B981' 
        },
        { 
          name: 'En cours', 
          count: statusCount.EN_COURS, 
          percentage: (statusCount.EN_COURS / total * 100).toFixed(0), 
          color: '#3B82F6' 
        },
        { 
          name: 'Annulées', 
          count: statusCount.ANNULEE, 
          percentage: (statusCount.ANNULEE / total * 100).toFixed(0), 
          color: '#EF4444' 
        }
      ];
    },
    
    prepareFournisseursData() {
      // Enrichir les données fournisseurs avec le nombre de commandes
      this.fournisseurs = this.fournisseurs.map(f => {
        const nombreCommandes = this.commandes.filter(c => 
          c.fournisseur === f.id_fournisseur
        ).length;
        
        return {
          ...f,
          nombre_commandes: nombreCommandes
        };
      });
    },
    
    groupByMonth(data, dateField) {
      const months = {};
      data.forEach(item => {
        const date = new Date(item[dateField]);
        const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        if (!months[key]) {
          months[key] = { count: 0, revenue: 0 };
        }
        months[key].count++;
        months[key].revenue += parseFloat(item.montant_total || 0);
      });
      return months;
    },
    
    groupStockByMonth(data) {
      const months = {};
      data.forEach(item => {
        const date = new Date(item.date_modification);
        const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        if (!months[key]) {
          months[key] = { ajouts: 0, retraits: 0 };
        }
        if (item.type_modification === 'AJOUT') {
          months[key].ajouts += item.quantite_modifiee;
        } else {
          months[key].retraits += item.quantite_modifiee;
        }
      });
      return months;
    },
    
    getDateLimit() {
      const days = parseInt(this.dateFilter);
      const date = new Date();
      date.setDate(date.getDate() - days);
      return date;
    },
    
    applyFilters() {
      // Recharger les données avec les nouveaux filtres
      this.calculateKPIs();
      this.calculateVentesStats();
      this.calculateStockStats();
      this.calculateCommandesStats();
      
      this.$nextTick(() => {
        this.destroyCharts();
        this.initCharts();
      });
    },
    
    initCharts() {
      this.createOrdersChart();
      this.createVentesChart();
      this.createStockChart();
      this.createSuppliersChart();
    },
    
    destroyCharts() {
      if (this.ordersChartInstance) this.ordersChartInstance.destroy();
      if (this.ventesChartInstance) this.ventesChartInstance.destroy();
      if (this.stockChartInstance) this.stockChartInstance.destroy();
      if (this.suppliersChartInstance) this.suppliersChartInstance.destroy();
    },
    
    createOrdersChart() {
      if (!this.$refs.ordersChart) return;
      
      const ctx = this.$refs.ordersChart.getContext('2d');
      const months = Object.keys(this.ventesParMois).sort().slice(-6);
      
      const data = {
        labels: months.map(m => {
          const [year, month] = m.split('-');
          return new Date(year, month - 1).toLocaleDateString('fr-FR', { month: 'short' });
        }),
        datasets: [
          {
            label: 'Commandes',
            data: months.map(m => this.ventesParMois[m]?.count || 0),
            backgroundColor: '#3B82F6',
            borderColor: '#2563eb',
            borderWidth: 2,
            borderRadius: 6,
          },
          {
            label: 'Revenus (÷1000)',
            data: months.map(m => (this.ventesParMois[m]?.revenue || 0) / 1000),
            backgroundColor: '#10B981',
            borderColor: '#059669',
            borderWidth: 2,
            borderRadius: 6,
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
            legend: { display: true, position: 'top' }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(0, 0, 0, 0.05)' }
            },
            x: { grid: { display: false } }
          }
        }
      });
    },
    
    createVentesChart() {
      if (!this.$refs.ventesChart) return;
      
      const ctx = this.$refs.ventesChart.getContext('2d');
      const months = Object.keys(this.ventesParMois).sort().slice(-6);
      
      const data = {
        labels: months.map(m => {
          const [year, month] = m.split('-');
          return new Date(year, month - 1).toLocaleDateString('fr-FR', { month: 'short' });
        }),
        datasets: [{
          label: 'Chiffre d\'affaires',
          data: months.map(m => this.ventesParMois[m]?.revenue || 0),
          borderColor: '#10B981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          tension: 0.4,
          fill: true
        }]
      };
      
      this.ventesChartInstance = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: true, position: 'top' }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(0, 0, 0, 0.05)' }
            }
          }
        }
      });
    },
    
    createStockChart() {
      if (!this.$refs.stockChart) return;
      
      const ctx = this.$refs.stockChart.getContext('2d');
      const months = Object.keys(this.mouvementsParMois).sort().slice(-6);
      
      const data = {
        labels: months.map(m => {
          const [year, month] = m.split('-');
          return new Date(year, month - 1).toLocaleDateString('fr-FR', { month: 'short' });
        }),
        datasets: [
          {
            label: 'Ajouts',
            data: months.map(m => this.mouvementsParMois[m]?.ajouts || 0),
            backgroundColor: '#10B981',
            borderRadius: 6,
          },
          {
            label: 'Retraits',
            data: months.map(m => this.mouvementsParMois[m]?.retraits || 0),
            backgroundColor: '#EF4444',
            borderRadius: 6,
          }
        ]
      };
      
      this.stockChartInstance = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: true, position: 'top' }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(0, 0, 0, 0.05)' }
            }
          }
        }
      });
    },
    
    createSuppliersChart() {
      if (!this.$refs.suppliersChart) return;
      
      const ctx = this.$refs.suppliersChart.getContext('2d');
      const topFournisseurs = this.fournisseurs
        .sort((a, b) => b.nombre_commandes - a.nombre_commandes)
        .slice(0, 5);
      
      const data = {
        labels: topFournisseurs.map(f => f.nom),
        datasets: [{
          label: 'Nombre de commandes',
          data: topFournisseurs.map(f => f.nombre_commandes),
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
            legend: { display: false }
          },
          scales: {
            x: {
              beginAtZero: true,
              grid: { color: 'rgba(0, 0, 0, 0.05)' }
            },
            y: { grid: { display: false } }
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
    
    exportData() {
      const data = {
        periode: `${this.dateFilter} derniers jours`,
        kpis: {
          total_commandes: this.totalCommandes,
          total_revenus: this.totalRevenue,
          total_produits: this.totalProduits,
          panier_moyen: this.averageBasket
        },
        ventes: this.topProductsVendus,
        stock: {
          total_ajouts: this.totalAjouts,
          total_retraits: this.totalRetraits,
          bilan_net: this.bilanNet
        }
      };
      
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `statistiques_${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
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

/* Chargement */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3B82F6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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

/* Conteneur des graphiques */
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
  padding: 20px;
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

.kpi-trend.negative {
  color: rgba(255, 200, 200, 0.95);
}

.kpi-icon {
  font-size: 48px;
  opacity: 0.3;
}

/* Titre centré */
.card-title-centered {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 16px;
  text-align: center;
}

/* Graphiques */
.chart-section {
  height: 250px;
  margin-bottom: 20px;
}

/* Stats grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.stat-box {
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
}

.stat-box .label {
  display: block;
  font-size: 12px;
  color: #64748b;
  margin-bottom: 8px;
  font-weight: 500;
}

.stat-box .value {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

/* Section statut */
.status-section {
  margin-top: 20px;
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
  margin-bottom: 6px;
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
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}

.status-progress {
  height: 100%;
  border-radius: 4px;
  transition: width 0.8s ease;
}

/* Produits */
.section-subtitle {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 16px;
}

.top-products {
  margin-top: 20px;
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
  white-space: nowrap;
}

/* Statistiques stock */
.stock-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 20px;
}

.stat-card {
  background: #f8fafc;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-ajout {
  border-left: 4px solid #10B981;
}

.stat-retrait {
  border-left: 4px solid #EF4444;
}

.stat-bilan {
  border-left: 4px solid #8B5CF6;
}

.stat-icon {
  font-size: 36px;
}

.stat-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.stat-value.positive {
  color: #10B981;
}

.stat-value.negative {
  color: #EF4444;
}

.stat-subtitle {
  font-size: 11px;
  color: #94a3b8;
}

/* Fournisseurs */
.suppliers-container {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 20px;
}

.suppliers-chart {
  height: 280px;
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

/* Responsive */
@media (max-width: 1200px) {
  .cards-grid-top {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .suppliers-container {
    grid-template-columns: 1fr;
  }
  
  .suppliers-chart {
    height: 250px;
  }
  
  .stock-stats {
    grid-template-columns: repeat(2, 1fr);
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
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .stock-stats {
    grid-template-columns: 1fr;
  }
  
  .dashboard-card {
    padding: 16px;
  }
  
  .chart-section {
    height: 200px;
  }
  
  .suppliers-chart {
    height: 200px;
  }
  
  .kpi-value {
    font-size: 28px;
  }
  
  .kpi-icon {
    font-size: 36px;
  }
  
  table {
    min-width: 500px;
  }
  
  th, td {
    padding: 8px;
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .statistics-page {
    padding: 12px;
  }
  
  .chart-section {
    height: 180px;
  }
  
  .kpi-value {
    font-size: 24px;
  }
  
  .stat-card {
    padding: 16px;
  }
  
  .stat-icon {
    font-size: 28px;
  }
  
  .stat-value {
    font-size: 20px;
  }
}