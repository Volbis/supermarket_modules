<template>
  <div class="statistics-content">
    <div class="stats-header">
      <h2>Statistiques de vente</h2>
      <p>Analysez les performances de votre magasin</p>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card">
        <h3>Ventes du mois</h3>
        <div class="stat-value">€12,450</div>
        <div class="stat-change positive">+15%</div>
      </div>
      
      <div class="stat-card">
        <h3>Commandes</h3>
        <div class="stat-value">156</div>
        <div class="stat-change positive">+8%</div>
      </div>
      
      <div class="stat-card">
        <h3>Clients actifs</h3>
        <div class="stat-value">89</div>
        <div class="stat-change negative">-2%</div>
      </div>
      
      <div class="stat-card">
        <h3>Panier moyen</h3>
        <div class="stat-value">€79.8</div>
        <div class="stat-change positive">+12%</div>
      </div>
    </div>
    
    <div class="charts-section">
      <div class="chart-container">
        <h3>Évolution des ventes</h3>
        <div class="chart-placeholder">
          <p>Graphique des ventes mensuelles</p>
        </div>
      </div>
      
      <div class="chart-container">
        <h3>Top produits</h3>
        <div class="chart-placeholder">
          <p>Graphique des produits les plus vendus</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatisticsView'
}
</script>

<style scoped>
.statistics-content {
  padding: 20px;
}

.stats-header {
  margin-bottom: 30px;
}

.stats-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.stats-header p {
  color: #6b7280;
  font-size: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #e5e7eb;
}

.stat-card h3 {
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
}

.stat-change {
  font-size: 14px;
  font-weight: 500;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change.negative {
  color: #ef4444;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-container {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #e5e7eb;
}

.chart-container h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
}

.chart-placeholder {
  height: 200px;
  background: #f9fafb;
  border: 2px dashed #d1d5db;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
}
</style>