<template>
  <div class="reports-content">
    <div class="page-header">
      <div>
        <h2>📄 Rapports Quotidiens</h2>
        <p class="subtitle">Consultez les rapports de caisse du {{ formatDate(selectedDate) }}</p>
      </div>
      <div class="header-actions">
        <input 
          type="date" 
          v-model="selectedDate" 
          class="date-picker"
        />
        <button class="btn-secondary" @click="refreshData">
          🔄 Actualiser
        </button>
        <button class="btn-primary" @click="exportReport">
          📥 Exporter
        </button>
      </div>
    </div>

    <!-- KPIs Financiers -->
    <div class="financial-summary">
      <h3>💰 Résumé Financier</h3>
      <div class="kpis-grid">
        <div class="kpi-card highlight">
          <div class="kpi-header">
            <span class="kpi-icon">�</span>
            <span class="kpi-label">Chiffre d'Affaires Total</span>
          </div>
          <div class="kpi-value">{{ formatPrice(report.totalRevenue) }}</div>
          <div class="kpi-trend positive">
            ↗ +{{ report.revenueGrowth }}% vs hier
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-icon">🧾</span>
            <span class="kpi-label">Transactions</span>
          </div>
          <div class="kpi-value">{{ report.transactionCount }}</div>
          <div class="kpi-detail">{{ formatPrice(report.avgTransaction) }} moy.</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-icon">👥</span>
            <span class="kpi-label">Clients</span>
          </div>
          <div class="kpi-value">{{ report.customersCount }}</div>
          <div class="kpi-detail">{{ report.loyalCustomers }} fidèles</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-icon">📦</span>
            <span class="kpi-label">Articles vendus</span>
          </div>
          <div class="kpi-value">{{ report.itemsSold }}</div>
          <div class="kpi-detail">{{ report.avgItemsPerBasket }} par panier</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-icon">💳</span>
            <span class="kpi-label">Paiements CB</span>
          </div>
          <div class="kpi-value">{{ formatPrice(report.cardPayments) }}</div>
          <div class="kpi-detail">{{ report.cardPercentage }}% du CA</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon">💵</div>
          <div class="kpi-header">
            <span class="kpi-label">Espèces</span>
          </div>
          <div class="kpi-value">{{ formatPrice(report.cashPayments) }}</div>
          <div class="kpi-detail">{{ report.cashPercentage }}% du CA</div>
        </div>
      </div>
    </div>

    <!-- Répartition par méthode de paiement -->
    <div class="section-card">
      <div class="section-header">
        <h3>💳 Répartition par Méthode de Paiement</h3>
      </div>
      <div class="payment-methods-table">
        <table class="data-table">
          <thead>
            <tr>
              <th>Méthode</th>
              <th>Nombre</th>
              <th>Montant</th>
              <th>% du CA</th>
              <th>Ticket moyen</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="method in report.paymentMethods" :key="method.name">
              <td>
                <div class="method-cell">
                  <span class="method-icon">{{ method.icon }}</span>
                  <span class="method-name">{{ method.name }}</span>
                </div>
              </td>
              <td class="number-cell">{{ method.count }}</td>
              <td class="amount-cell">{{ formatPrice(method.amount) }}</td>
              <td>
                <div class="percentage-bar">
                  <div 
                    class="percentage-fill" 
                    :style="{ width: method.percentage + '%' }"
                  ></div>
                  <span class="percentage-text">{{ method.percentage }}%</span>
                </div>
              </td>
              <td class="amount-cell">{{ formatPrice(method.avgTicket) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Top 10 Produits -->
    <div class="section-card">
      <div class="section-header">
        <h3>🏆 Top 10 des Produits Vendus</h3>
      </div>
      <div class="top-products-table">
        <table class="data-table">
          <thead>
            <tr>
              <th>Rang</th>
              <th>Produit</th>
              <th>Quantité</th>
              <th>Chiffre d'Affaires</th>
              <th>Marge</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(product, index) in report.topProducts" :key="product.id">
              <td>
                <span :class="['rank-badge', 'rank-' + (index + 1)]">
                  {{ index + 1 }}
                </span>
              </td>
              <td>
                <div class="product-cell">
                  <span class="product-name">{{ product.name }}</span>
                  <span class="product-category">{{ product.category }}</span>
                </div>
              </td>
              <td class="number-cell">{{ product.quantity }} unités</td>
              <td class="amount-cell revenue">{{ formatPrice(product.revenue) }}</td>
              <td class="amount-cell margin">{{ formatPrice(product.margin) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Statistiques par caissier -->
    <div class="section-card">
      <div class="section-header">
        <h3>👤 Performance des Caissiers</h3>
      </div>
      <div class="cashiers-table">
        <table class="data-table">
          <thead>
            <tr>
              <th>Caissier</th>
              <th>Transactions</th>
              <th>CA Réalisé</th>
              <th>Panier moyen</th>
              <th>Temps moy./vente</th>
              <th>Performance</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cashier in report.cashiers" :key="cashier.id">
              <td>
                <div class="cashier-cell">
                  <span class="cashier-avatar">{{ getCashierInitials(cashier.name) }}</span>
                  <span class="cashier-name">{{ cashier.name }}</span>
                </div>
              </td>
              <td class="number-cell">{{ cashier.transactions }}</td>
              <td class="amount-cell">{{ formatPrice(cashier.revenue) }}</td>
              <td class="amount-cell">{{ formatPrice(cashier.avgBasket) }}</td>
              <td class="time-cell">{{ cashier.avgTime }} min</td>
              <td>
                <span :class="['performance-badge', cashier.performance]">
                  {{ getPerformanceLabel(cashier.performance) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Actions rapides -->
    <div class="actions-section">
      <button class="btn-action" @click="generateZReport">
        📋 Générer Rapport Z
      </button>
      <button class="btn-action" @click="exportPDF">
        📄 Exporter en PDF
      </button>
      <button class="btn-action" @click="exportExcel">
        📊 Exporter en Excel
      </button>
      <button class="btn-action" @click="emailReport">
        📧 Envoyer par Email
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DailyReports',
  data() {
    return {
      selectedDate: new Date().toISOString().split('T')[0],
      report: {
        totalRevenue: 2847500,
        revenueGrowth: 12.5,
        transactionCount: 156,
        avgTransaction: 18254,
        customersCount: 142,
        loyalCustomers: 48,
        itemsSold: 827,
        avgItemsPerBasket: 5.3,
        cardPayments: 854250,
        cardPercentage: 30,
        cashPayments: 1281375,
        cashPercentage: 45,
        paymentMethods: [
          {
            name: 'Espèces',
            icon: '💵',
            count: 70,
            amount: 1281375,
            percentage: 45,
            avgTicket: 18305
          },
          {
            name: 'Carte bancaire',
            icon: '💳',
            count: 47,
            amount: 854250,
            percentage: 30,
            avgTicket: 18175
          },
          {
            name: 'Mobile Money',
            icon: '📱',
            count: 31,
            amount: 569500,
            percentage: 20,
            avgTicket: 18371
          },
          {
            name: 'Carte cadeau',
            icon: '🎁',
            count: 8,
            amount: 142375,
            percentage: 5,
            avgTicket: 17797
          }
        ],
        topProducts: [
          {
            id: 1,
            name: 'Coca-Cola 1.5L',
            category: 'Boissons',
            quantity: 89,
            revenue: 106800,
            margin: 32040
          },
          {
            id: 2,
            name: 'Riz 5kg',
            category: 'Épicerie',
            quantity: 45,
            revenue: 202500,
            margin: 60750
          },
          {
            id: 3,
            name: 'Lait NIDO 400g',
            category: 'Produits laitiers',
            quantity: 38,
            revenue: 133000,
            margin: 39900
          },
          {
            id: 4,
            name: 'Pain de mie',
            category: 'Boulangerie',
            quantity: 67,
            revenue: 53600,
            margin: 16080
          },
          {
            id: 5,
            name: 'Huile végétale 1L',
            category: 'Épicerie',
            quantity: 34,
            revenue: 74800,
            margin: 22440
          },
          {
            id: 6,
            name: 'Eau minérale 1.5L',
            category: 'Boissons',
            quantity: 112,
            revenue: 56000,
            margin: 16800
          },
          {
            id: 7,
            name: 'Bananes (kg)',
            category: 'Fruits',
            quantity: 28,
            revenue: 42000,
            margin: 12600
          },
          {
            id: 8,
            name: 'Poulet entier',
            category: 'Viandes',
            quantity: 19,
            revenue: 66500,
            margin: 19950
          },
          {
            id: 9,
            name: 'Tomates (kg)',
            category: 'Légumes',
            quantity: 42,
            revenue: 50400,
            margin: 15120
          },
          {
            id: 10,
            name: 'Savon Lux x4',
            category: 'Hygiène',
            quantity: 31,
            revenue: 55800,
            margin: 16740
          }
        ],
        cashiers: [
          {
            id: 1,
            name: 'Marie K.',
            transactions: 58,
            revenue: 1052400,
            avgBasket: 18145,
            avgTime: 3.2,
            performance: 'excellent'
          },
          {
            id: 2,
            name: 'Jean T.',
            transactions: 52,
            revenue: 948200,
            avgBasket: 18234,
            avgTime: 3.8,
            performance: 'good'
          },
          {
            id: 3,
            name: 'Aminata D.',
            transactions: 46,
            revenue: 846900,
            avgBasket: 18411,
            avgTime: 3.5,
            performance: 'good'
          }
        ]
      }
    };
  },
  methods: {
    refreshData() {
      console.log('📄 Rapport rafraîchi pour le', this.selectedDate);
    },
    exportReport() {
      alert('📥 Export du rapport en cours...\n(Format: PDF, Excel ou CSV)');
    },
    generateZReport() {
      alert('📋 Génération du Rapport Z en cours...\n\nRapport de clôture quotidien\nDate: ' + this.formatDate(this.selectedDate) + '\nCA Total: ' + this.formatPrice(this.report.totalRevenue));
    },
    exportPDF() {
      alert('📄 Export PDF en cours...\n(Rapport complet avec graphiques)');
    },
    exportExcel() {
      alert('📊 Export Excel en cours...\n(Tableau détaillé avec tous les indicateurs)');
    },
    emailReport() {
      alert('📧 Envoi du rapport par email...\n(À: direction@supermarket.com)');
    },
    getCashierInitials(name) {
      return name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase();
    },
    getPerformanceLabel(performance) {
      const labels = {
        excellent: 'Excellent',
        good: 'Bon',
        average: 'Moyen',
        low: 'Faible'
      };
      return labels[performance] || performance;
    },
    formatPrice(amount) {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF',
        minimumFractionDigits: 0
      }).format(amount);
    },
    formatDate(dateString) {
      return new Intl.DateTimeFormat('fr-FR', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(new Date(dateString));
    }
  }
};
</script>

<style scoped>
.reports-content {
  padding: 20px 40px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
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
  align-items: center;
}

.date-picker {
  padding: 10px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  background: white;
  cursor: pointer;
}

.financial-summary {
  background: white;
  border-radius: 16px;
  padding: 32px;
  border: 1px solid #e5e7eb;
  margin-bottom: 24px;
}

.financial-summary h3 {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 24px;
}

.kpis-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.kpi-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.kpi-card.highlight {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  color: white;
}

.kpi-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.kpi-icon {
  font-size: 24px;
}

.kpi-label {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
}

.kpi-card.highlight .kpi-label {
  color: rgba(255, 255, 255, 0.9);
}

.kpi-value {
  font-size: 28px;
  font-weight: 800;
  color: #111827;
  margin-bottom: 8px;
}

.kpi-card.highlight .kpi-value {
  color: white;
}

.kpi-trend {
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}

.kpi-trend.positive {
  color: #10b981;
}

.kpi-card.highlight .kpi-trend.positive {
  color: rgba(255, 255, 255, 0.95);
}

.kpi-detail {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
}

.section-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  border: 1px solid #e5e7eb;
  margin-bottom: 24px;
}

.section-header {
  margin-bottom: 24px;
}

.section-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: #f9fafb;
}

.data-table th {
  padding: 14px 16px;
  text-align: left;
  font-size: 12px;
  font-weight: 700;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #e5e7eb;
}

.data-table tbody tr {
  transition: background 0.2s ease;
}

.data-table tbody tr:hover {
  background: #f9fafb;
}

.data-table td {
  padding: 16px;
  border-bottom: 1px solid #f3f4f6;
  font-size: 14px;
  color: #374151;
}

.method-cell,
.cashier-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.method-icon {
  font-size: 24px;
}

.method-name {
  font-weight: 600;
  color: #111827;
}

.number-cell {
  font-weight: 600;
  color: #6b7280;
}

.amount-cell {
  font-weight: 700;
  color: #111827;
}

.amount-cell.revenue {
  color: #10b981;
}

.amount-cell.margin {
  color: #3b82f6;
}

.percentage-bar {
  position: relative;
  height: 24px;
  background: #f3f4f6;
  border-radius: 6px;
  overflow: hidden;
}

.percentage-fill {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  transition: width 0.3s ease;
}

.percentage-text {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-size: 12px;
  font-weight: 700;
  color: #111827;
  z-index: 1;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 800;
  color: white;
}

.rank-badge.rank-1 {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
}

.rank-badge.rank-2 {
  background: linear-gradient(135deg, #d1d5db 0%, #9ca3af 100%);
}

.rank-badge.rank-3 {
  background: linear-gradient(135deg, #fb923c 0%, #ea580c 100%);
}

.rank-badge:not(.rank-1):not(.rank-2):not(.rank-3) {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.product-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-name {
  font-weight: 600;
  color: #111827;
}

.product-category {
  font-size: 12px;
  color: #6b7280;
}

.cashier-avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
}

.cashier-name {
  font-weight: 600;
  color: #111827;
}

.time-cell {
  font-weight: 600;
  color: #6b7280;
}

.performance-badge {
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
}

.performance-badge.excellent {
  background: #dcfce7;
  color: #166534;
}

.performance-badge.good {
  background: #dbeafe;
  color: #1e40af;
}

.performance-badge.average {
  background: #fef3c7;
  color: #92400e;
}

.performance-badge.low {
  background: #fee2e2;
  color: #991b1b;
}

.actions-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.btn-action {
  padding: 16px 24px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 700;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-action:hover {
  background: #f9fafb;
  border-color: #3b82f6;
  color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}
</style>