<template>
  <div class="history-content">
    <div class="page-header">
      <div>
        <h2>📜 Historique des Transactions</h2>
        <p class="subtitle">Consultez toutes les transactions effectuées</p>
      </div>
      <button class="btn-primary" @click="exportData">📥 Exporter</button>
    </div>

    <!-- Filtres -->
    <div class="filters-card">
      <div class="filters-grid">
        <div class="filter-item">
          <label>Date début</label>
          <input type="date" v-model="filters.startDate" class="input" />
        </div>
        <div class="filter-item">
          <label>Date fin</label>
          <input type="date" v-model="filters.endDate" class="input" />
        </div>
        <div class="filter-item">
          <label>Recherche</label>
          <input type="text" v-model="filters.search" placeholder="N° transaction..." class="input" />
        </div>
        <div class="filter-item">
          <button class="btn btn-secondary btn-full" @click="resetFilters">Réinitialiser</button>
        </div>
      </div>
    </div>

    <!-- Stats rapides -->
    <div class="quick-stats">
      <div class="stat-box">
        <span class="stat-label">Total</span>
        <span class="stat-value">{{ transactions.length }}</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">Montant total</span>
        <span class="stat-value">{{ formatPrice(totalAmount) }}</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">Panier moyen</span>
        <span class="stat-value">{{ formatPrice(avgAmount) }}</span>
      </div>
    </div>

    <!-- Table -->
    <div class="table-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>N° Transaction</th>
            <th>Date & Heure</th>
            <th>Caissier</th>
            <th>Articles</th>
            <th>Montant</th>
            <th>Paiement</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="trx in displayedTransactions" :key="trx.id" class="table-row">
            <td><span class="trx-id">{{ trx.id }}</span></td>
            <td>{{ formatDate(trx.date) }}</td>
            <td>{{ trx.cashier }}</td>
            <td>{{ trx.items }} articles</td>
            <td class="amount">{{ formatPrice(trx.amount) }}</td>
            <td>
              <span :class="['badge', 'badge-' + trx.method]">{{ getMethodLabel(trx.method) }}</span>
            </td>
            <td>
              <button class="btn-icon" @click="viewDetails(trx)" title="Détails">👁️</button>
              <button class="btn-icon" @click="printReceipt(trx)" title="Imprimer">🖨️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal détails -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>📋 Détails - {{ selectedTrx.id }}</h3>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <div class="details-grid">
            <div><strong>Caissier:</strong> {{ selectedTrx.cashier }}</div>
            <div><strong>Date:</strong> {{ formatDate(selectedTrx.date) }}</div>
            <div><strong>Articles:</strong> {{ selectedTrx.items }}</div>
            <div><strong>Montant:</strong> {{ formatPrice(selectedTrx.amount) }}</div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeModal">Fermer</button>
          <button class="btn-primary" @click="printReceipt(selectedTrx)">🖨️ Imprimer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TransactionHistory',
  data() {
    return {
      filters: { startDate: '', endDate: '', search: '' },
      showModal: false,
      selectedTrx: null,
      transactions: [
        { id: 'TRX20250124001', date: new Date('2025-01-24T14:30'), cashier: 'Marie K.', items: 5, amount: 25400, method: 'cash' },
        { id: 'TRX20250124002', date: new Date('2025-01-24T14:45'), cashier: 'Jean T.', items: 3, amount: 12800, method: 'card' },
        { id: 'TRX20250124003', date: new Date('2025-01-24T15:10'), cashier: 'Aminata D.', items: 8, amount: 35200, method: 'mobile' },
        { id: 'TRX20250124004', date: new Date('2025-01-24T15:25'), cashier: 'Marie K.', items: 2, amount: 8500, method: 'cash' },
        { id: 'TRX20250124005', date: new Date('2025-01-24T15:40'), cashier: 'Jean T.', items: 6, amount: 18900, method: 'card' }
      ]
    };
  },
  computed: {
    displayedTransactions() {
      return this.transactions.filter(t => {
        if (this.filters.search && !t.id.toLowerCase().includes(this.filters.search.toLowerCase())) return false;
        return true;
      });
    },
    totalAmount() {
      return this.displayedTransactions.reduce((sum, t) => sum + t.amount, 0);
    },
    avgAmount() {
      return this.displayedTransactions.length > 0 ? this.totalAmount / this.displayedTransactions.length : 0;
    }
  },
  methods: {
    refreshData() { console.log('📜 Rafraîchi'); },
    resetFilters() { this.filters = { startDate: '', endDate: '', search: '' }; },
    viewDetails(trx) { this.selectedTrx = trx; this.showModal = true; },
    closeModal() { this.showModal = false; this.selectedTrx = null; },
    printReceipt(trx) { alert(`🖨️ Impression ticket ${trx.id}`); },
    exportData() { alert('📥 Export en cours...'); },
    getMethodLabel(m) { return { cash: 'Espèces', card: 'Carte', mobile: 'Mobile' }[m]; },
    formatPrice(amt) { return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'XOF', minimumFractionDigits: 0 }).format(amt); },
    formatDate(d) { return new Intl.DateTimeFormat('fr-FR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }).format(d); }
  }
};
</script>

<style scoped>
.history-content { padding: 20px 40px; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.page-header h2 { font-size: 28px; font-weight: 700; color: #111827; margin-bottom: 8px; }
.subtitle { color: #6b7280; font-size: 15px; }
.filters-card { background: white; border-radius: 16px; padding: 24px; border: 1px solid #e5e7eb; margin-bottom: 20px; }
.filters-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.filter-item label { display: block; font-size: 13px; font-weight: 600; color: #374151; margin-bottom: 8px; }
.quick-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-box { background: white; border-radius: 12px; padding: 20px; border: 1px solid #e5e7eb; display: flex; flex-direction: column; gap: 8px; }
.stat-label { font-size: 13px; color: #6b7280; font-weight: 600; }
.stat-value { font-size: 24px; font-weight: 800; color: #111827; }
.table-card { background: white; border-radius: 16px; border: 1px solid #e5e7eb; overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table thead { background: #f9fafb; }
.data-table th { padding: 16px; text-align: left; font-size: 13px; font-weight: 700; color: #374151; text-transform: uppercase; border-bottom: 2px solid #e5e7eb; }
.table-row:hover { background: #f9fafb; }
.data-table td { padding: 16px; border-bottom: 1px solid #f3f4f6; font-size: 14px; color: #374151; }
.trx-id { font-family: monospace; font-weight: 700; color: #3b82f6; }
.amount { font-weight: 700; color: #10b981; font-size: 15px; }
.badge { padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; }
.badge-cash { background: #dcfce7; color: #166534; }
.badge-card { background: #dbeafe; color: #1e40af; }
.badge-mobile { background: #fef3c7; color: #92400e; }
.btn-icon { width: 32px; height: 32px; border: 1px solid #e5e7eb; background: white; border-radius: 6px; cursor: pointer; margin-right: 4px; }
.btn-icon:hover { background: #f3f4f6; }
.details-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
</style>
