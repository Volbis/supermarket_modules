<template>
  <div class="history-content">
    <div class="page-header">
      <div>
        <h2>📜 Historique des Transactions</h2>
        <p class="subtitle">Consultez toutes les transactions effectuées</p>
      </div>
      <button class="btn-primary" @click="exportData">
        📥 Exporter
      </button>
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
          <label>Caissier</label>
          <select v-model="filters.cashier" class="input">
            <option value="">Tous</option>
            <option value="Marie K.">Marie K.</option>
            <option value="Jean T.">Jean T.</option>
            <option value="Aminata D.">Aminata D.</option>
          </select>
        </div>
        <div class="filter-item">
          <label>Méthode paiement</label>
          <select v-model="filters.method" class="input">
            <option value="">Toutes</option>
            <option value="cash">Espèces</option>
            <option value="card">Carte bancaire</option>
            <option value="mobile">Mobile Money</option>
            <option value="gift">Carte cadeau</option>
          </select>
        </div>
        <div class="filter-item">
          <label>Recherche</label>
          <input 
            type="text" 
            v-model="filters.search" 
            placeholder="N° transaction, montant..." 
            class="input" 
          />
        </div>
        <div class="filter-item filter-actions">
          <button class="btn-secondary btn-full" @click="resetFilters">
            🔄 Réinitialiser
          </button>
        </div>
      </div>
    </div>

    <!-- Stats rapides -->
    <div class="quick-stats">
      <div class="stat-box">
        <span class="stat-icon">📊</span>
        <div>
          <span class="stat-label">Total transactions</span>
          <span class="stat-value">{{ filteredTransactions.length }}</span>
        </div>
      </div>
      <div class="stat-box">
        <span class="stat-icon">💰</span>
        <div>
          <span class="stat-label">Montant total</span>
          <span class="stat-value">{{ formatPrice(totalAmount) }}</span>
        </div>
      </div>
      <div class="stat-box">
        <span class="stat-icon">🛒</span>
        <div>
          <span class="stat-label">Panier moyen</span>
          <span class="stat-value">{{ formatPrice(avgAmount) }}</span>
        </div>
      </div>
      <div class="stat-box">
        <span class="stat-icon">📦</span>
        <div>
          <span class="stat-label">Articles vendus</span>
          <span class="stat-value">{{ totalItems }}</span>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div class="table-header">
        <h3>Transactions ({{ filteredTransactions.length }})</h3>
        <div class="pagination">
          <button 
            class="btn-pagination" 
            @click="currentPage--" 
            :disabled="currentPage === 1"
          >
            ← Précédent
          </button>
          <span class="page-info">Page {{ currentPage }} / {{ totalPages }}</span>
          <button 
            class="btn-pagination" 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
          >
            Suivant →
          </button>
        </div>
      </div>
      
      <table class="data-table">
        <thead>
          <tr>
            <th>N° Transaction</th>
            <th>Date & Heure</th>
            <th>Caissier</th>
            <th>Articles</th>
            <th>Montant</th>
            <th>Paiement</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="trx in paginatedTransactions" 
            :key="trx.id" 
            class="table-row"
          >
            <td>
              <span class="trx-id">{{ trx.id }}</span>
            </td>
            <td>{{ formatDate(trx.date) }}</td>
            <td>
              <div class="cashier-info">
                <span class="cashier-avatar">{{ getCashierInitials(trx.cashier) }}</span>
                <span>{{ trx.cashier }}</span>
              </div>
            </td>
            <td>{{ trx.items }} articles</td>
            <td class="amount">{{ formatPrice(trx.amount) }}</td>
            <td>
              <span :class="['badge', 'badge-' + trx.method]">
                {{ getMethodLabel(trx.method) }}
              </span>
            </td>
            <td>
              <span :class="['status-badge', trx.status]">
                {{ getStatusLabel(trx.status) }}
              </span>
            </td>
            <td>
              <div class="action-buttons">
                <button 
                  class="btn-icon" 
                  @click="viewDetails(trx)" 
                  title="Détails"
                >
                  👁️
                </button>
                <button 
                  class="btn-icon" 
                  @click="printReceipt(trx)" 
                  title="Imprimer"
                >
                  🖨️
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal détails -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content modal-large">
        <div class="modal-header">
          <div>
            <h3>📋 Détails de la transaction</h3>
            <p class="modal-subtitle">{{ selectedTrx.id }}</p>
          </div>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        
        <div class="modal-body">
          <!-- Informations générales -->
          <div class="info-section">
            <h4>Informations générales</h4>
            <div class="details-grid">
              <div class="detail-item">
                <span class="detail-label">Date & Heure</span>
                <span class="detail-value">{{ formatDate(selectedTrx.date) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Caissier</span>
                <span class="detail-value">{{ selectedTrx.cashier }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Méthode de paiement</span>
                <span class="detail-value">
                  <span :class="['badge', 'badge-' + selectedTrx.method]">
                    {{ getMethodLabel(selectedTrx.method) }}
                  </span>
                </span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Statut</span>
                <span class="detail-value">
                  <span :class="['status-badge', selectedTrx.status]">
                    {{ getStatusLabel(selectedTrx.status) }}
                  </span>
                </span>
              </div>
            </div>
          </div>

          <!-- Articles -->
          <div class="info-section">
            <h4>Articles ({{ selectedTrx.products.length }})</h4>
            <div class="products-list">
              <div 
                v-for="(product, index) in selectedTrx.products" 
                :key="index"
                class="product-row"
              >
                <span class="product-name">{{ product.name }}</span>
                <span class="product-qty">{{ product.quantity }} x {{ formatPrice(product.price) }}</span>
                <span class="product-total">{{ formatPrice(product.quantity * product.price) }}</span>
              </div>
            </div>
          </div>

          <!-- Totaux -->
          <div class="info-section">
            <h4>Récapitulatif</h4>
            <div class="totals-grid">
              <div class="total-row">
                <span>Sous-total</span>
                <span>{{ formatPrice(selectedTrx.subtotal) }}</span>
              </div>
              <div class="total-row">
                <span>Remise ({{ selectedTrx.discount }}%)</span>
                <span class="discount-amount">-{{ formatPrice(selectedTrx.subtotal * selectedTrx.discount / 100) }}</span>
              </div>
              <div class="total-row">
                <span>TVA (18%)</span>
                <span>{{ formatPrice(selectedTrx.tax) }}</span>
              </div>
              <div class="total-row total-final">
                <span>Total</span>
                <span>{{ formatPrice(selectedTrx.amount) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeModal">Fermer</button>
          <button class="btn-primary" @click="printReceipt(selectedTrx)">
            🖨️ Réimprimer le ticket
          </button>
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
      currentPage: 1,
      itemsPerPage: 10,
      filters: {
        startDate: '',
        endDate: '',
        cashier: '',
        method: '',
        search: ''
      },
      showModal: false,
      selectedTrx: null,
      transactions: [
        {
          id: 'TRX20250124001',
          date: new Date('2025-01-24T08:15:30'),
          cashier: 'Marie K.',
          items: 5,
          amount: 25400,
          method: 'cash',
          status: 'completed',
          subtotal: 23500,
          discount: 5,
          tax: 4233,
          products: [
            { name: 'Coca-Cola 1.5L', quantity: 2, price: 1200 },
            { name: 'Pain de mie', quantity: 1, price: 800 },
            { name: 'Lait NIDO 400g', quantity: 1, price: 3500 },
            { name: 'Huile végétale 1L', quantity: 1, price: 2200 },
            { name: 'Riz 5kg', quantity: 1, price: 4500 }
          ]
        },
        {
          id: 'TRX20250124002',
          date: new Date('2025-01-24T08:32:15'),
          cashier: 'Jean T.',
          items: 3,
          amount: 12800,
          method: 'card',
          status: 'completed',
          subtotal: 12000,
          discount: 0,
          tax: 2160,
          products: [
            { name: 'Eau minérale 1.5L', quantity: 6, price: 500 },
            { name: 'Savon Lux x4', quantity: 2, price: 1800 },
            { name: 'Bananes (kg)', quantity: 2, price: 1500 }
          ]
        },
        {
          id: 'TRX20250124003',
          date: new Date('2025-01-24T09:05:42'),
          cashier: 'Aminata D.',
          items: 8,
          amount: 35200,
          method: 'mobile',
          status: 'completed',
          subtotal: 32500,
          discount: 10,
          tax: 5850,
          products: [
            { name: 'Poulet entier', quantity: 1, price: 3500 },
            { name: 'Tomates (kg)', quantity: 3, price: 1200 },
            { name: 'Oignons (kg)', quantity: 2, price: 800 },
            { name: 'Riz 5kg', quantity: 2, price: 4500 },
            { name: 'Huile végétale 1L', quantity: 2, price: 2200 }
          ]
        },
        {
          id: 'TRX20250124004',
          date: new Date('2025-01-24T09:28:18'),
          cashier: 'Marie K.',
          items: 2,
          amount: 8500,
          method: 'cash',
          status: 'completed',
          subtotal: 8000,
          discount: 0,
          tax: 1440,
          products: [
            { name: 'Lait NIDO 400g', quantity: 2, price: 3500 },
            { name: 'Pain de mie', quantity: 1, price: 800 }
          ]
        },
        {
          id: 'TRX20250124005',
          date: new Date('2025-01-24T10:12:55'),
          cashier: 'Jean T.',
          items: 6,
          amount: 18900,
          method: 'card',
          status: 'completed',
          subtotal: 17500,
          discount: 5,
          tax: 3150,
          products: [
            { name: 'Coca-Cola 1.5L', quantity: 4, price: 1200 },
            { name: 'Eau minérale 1.5L', quantity: 12, price: 500 },
            { name: 'Savon Lux x4', quantity: 3, price: 1800 }
          ]
        },
        {
          id: 'TRX20250124006',
          date: new Date('2025-01-24T10:45:20'),
          cashier: 'Aminata D.',
          items: 4,
          amount: 22300,
          method: 'mobile',
          status: 'completed',
          subtotal: 21000,
          discount: 0,
          tax: 3780,
          products: [
            { name: 'Riz 5kg', quantity: 3, price: 4500 },
            { name: 'Huile végétale 1L', quantity: 3, price: 2200 }
          ]
        },
        {
          id: 'TRX20250124007',
          date: new Date('2025-01-24T11:18:33'),
          cashier: 'Marie K.',
          items: 7,
          amount: 14750,
          method: 'cash',
          status: 'completed',
          subtotal: 13500,
          discount: 10,
          tax: 2430,
          products: [
            { name: 'Pain de mie', quantity: 5, price: 800 },
            { name: 'Lait NIDO 400g', quantity: 2, price: 3500 },
            { name: 'Bananes (kg)', quantity: 2, price: 1500 }
          ]
        },
        {
          id: 'TRX20250124008',
          date: new Date('2025-01-24T11:52:08'),
          cashier: 'Jean T.',
          items: 3,
          amount: 9200,
          method: 'gift',
          status: 'completed',
          subtotal: 8500,
          discount: 0,
          tax: 1530,
          products: [
            { name: 'Coca-Cola 1.5L', quantity: 3, price: 1200 },
            { name: 'Savon Lux x4', quantity: 2, price: 1800 }
          ]
        },
        {
          id: 'TRX20250124009',
          date: new Date('2025-01-24T12:25:40'),
          cashier: 'Aminata D.',
          items: 9,
          amount: 42800,
          method: 'card',
          status: 'completed',
          subtotal: 40000,
          discount: 5,
          tax: 7200,
          products: [
            { name: 'Poulet entier', quantity: 2, price: 3500 },
            { name: 'Riz 5kg', quantity: 4, price: 4500 },
            { name: 'Huile végétale 1L', quantity: 3, price: 2200 }
          ]
        },
        {
          id: 'TRX20250124010',
          date: new Date('2025-01-24T13:08:15'),
          cashier: 'Marie K.',
          items: 5,
          amount: 16500,
          method: 'mobile',
          status: 'completed',
          subtotal: 15200,
          discount: 10,
          tax: 2736,
          products: [
            { name: 'Tomates (kg)', quantity: 4, price: 1200 },
            { name: 'Oignons (kg)', quantity: 3, price: 800 },
            { name: 'Eau minérale 1.5L', quantity: 10, price: 500 }
          ]
        },
        {
          id: 'TRX20250124011',
          date: new Date('2025-01-24T13:42:28'),
          cashier: 'Jean T.',
          items: 2,
          amount: 7800,
          method: 'cash',
          status: 'cancelled',
          subtotal: 7200,
          discount: 0,
          tax: 1296,
          products: [
            { name: 'Lait NIDO 400g', quantity: 2, price: 3500 }
          ]
        },
        {
          id: 'TRX20250124012',
          date: new Date('2025-01-24T14:15:50'),
          cashier: 'Aminata D.',
          items: 6,
          amount: 28900,
          method: 'card',
          status: 'completed',
          subtotal: 27000,
          discount: 5,
          tax: 4860,
          products: [
            { name: 'Riz 5kg', quantity: 2, price: 4500 },
            { name: 'Huile végétale 1L', quantity: 4, price: 2200 },
            { name: 'Savon Lux x4', quantity: 2, price: 1800 }
          ]
        }
      ]
    };
  },
  computed: {
    filteredTransactions() {
      return this.transactions.filter(t => {
        // Filtre par recherche
        if (this.filters.search) {
          const searchLower = this.filters.search.toLowerCase();
          const matchId = t.id.toLowerCase().includes(searchLower);
          const matchAmount = t.amount.toString().includes(searchLower);
          if (!matchId && !matchAmount) return false;
        }
        
        // Filtre par caissier
        if (this.filters.cashier && t.cashier !== this.filters.cashier) {
          return false;
        }
        
        // Filtre par méthode
        if (this.filters.method && t.method !== this.filters.method) {
          return false;
        }
        
        // Filtre par date
        if (this.filters.startDate) {
          const startDate = new Date(this.filters.startDate);
          if (t.date < startDate) return false;
        }
        
        if (this.filters.endDate) {
          const endDate = new Date(this.filters.endDate);
          endDate.setHours(23, 59, 59);
          if (t.date > endDate) return false;
        }
        
        return true;
      });
    },
    paginatedTransactions() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredTransactions.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredTransactions.length / this.itemsPerPage) || 1;
    },
    totalAmount() {
      return this.filteredTransactions.reduce((sum, t) => sum + t.amount, 0);
    },
    avgAmount() {
      return this.filteredTransactions.length > 0 
        ? this.totalAmount / this.filteredTransactions.length 
        : 0;
    },
    totalItems() {
      return this.filteredTransactions.reduce((sum, t) => sum + t.items, 0);
    }
  },
  watch: {
    filteredTransactions() {
      // Reset à la page 1 quand les filtres changent
      this.currentPage = 1;
    }
  },
  methods: {
    refreshData() {
      console.log('📜 Historique rafraîchi');
    },
    resetFilters() {
      this.filters = {
        startDate: '',
        endDate: '',
        cashier: '',
        method: '',
        search: ''
      };
    },
    viewDetails(trx) {
      this.selectedTrx = trx;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedTrx = null;
    },
    printReceipt(trx) {
      alert(`🖨️ Impression du ticket ${trx.id} en cours...\n(Fonctionnalité à implémenter)`);
    },
    exportData() {
      alert(`📥 Export de ${this.filteredTransactions.length} transactions en cours...\n(Format: Excel, CSV ou PDF)`);
    },
    getMethodLabel(method) {
      const labels = {
        cash: 'Espèces',
        card: 'Carte bancaire',
        mobile: 'Mobile Money',
        gift: 'Carte cadeau'
      };
      return labels[method] || method;
    },
    getStatusLabel(status) {
      const labels = {
        completed: 'Complétée',
        cancelled: 'Annulée',
        refunded: 'Remboursée'
      };
      return labels[status] || status;
    },
    getCashierInitials(name) {
      return name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase();
    },
    formatPrice(amount) {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF',
        minimumFractionDigits: 0
      }).format(amount);
    },
    formatDate(date) {
      return new Intl.DateTimeFormat('fr-FR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    }
  }
};
</script>

<style scoped>
.history-content {
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

.filters-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e5e7eb;
  margin-bottom: 20px;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.filter-item label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-item.filter-actions {
  display: flex;
  align-items: flex-end;
}

.input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  background: white;
  transition: border-color 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: #3b82f6;
}

.btn-full {
  width: 100%;
}

.quick-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-box {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 32px;
}

.stat-box div {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 20px;
  font-weight: 800;
  color: #111827;
}

.table-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.table-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-pagination {
  padding: 8px 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-pagination:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.btn-pagination:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: #f9fafb;
}

.data-table th {
  padding: 16px;
  text-align: left;
  font-size: 12px;
  font-weight: 700;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #e5e7eb;
}

.table-row {
  transition: background 0.2s ease;
}

.table-row:hover {
  background: #f9fafb;
}

.data-table td {
  padding: 16px;
  border-bottom: 1px solid #f3f4f6;
  font-size: 14px;
  color: #374151;
}

.trx-id {
  font-family: 'Courier New', monospace;
  font-weight: 700;
  color: #3b82f6;
  font-size: 13px;
}

.cashier-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.cashier-avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}

.amount {
  font-weight: 700;
  color: #10b981;
  font-size: 15px;
}

.badge {
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  display: inline-block;
}

.badge-cash {
  background: #dcfce7;
  color: #166534;
}

.badge-card {
  background: #dbeafe;
  color: #1e40af;
}

.badge-mobile {
  background: #fef3c7;
  color: #92400e;
}

.badge-gift {
  background: #fce7f3;
  color: #9f1239;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  display: inline-block;
}

.status-badge.completed {
  background: #dcfce7;
  color: #166534;
}

.status-badge.cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.status-badge.refunded {
  background: #fef3c7;
  color: #92400e;
}

.action-buttons {
  display: flex;
  gap: 6px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.modal-large {
  max-width: 900px;
}

.modal-subtitle {
  font-size: 13px;
  color: #6b7280;
  font-family: 'Courier New', monospace;
  font-weight: 600;
  margin-top: 4px;
}

.info-section {
  margin-bottom: 32px;
}

.info-section:last-child {
  margin-bottom: 0;
}

.info-section h4 {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e5e7eb;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 14px;
  color: #111827;
  font-weight: 600;
}

.products-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.product-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 16px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  align-items: center;
}

.product-name {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.product-qty {
  font-size: 13px;
  color: #6b7280;
}

.product-total {
  font-size: 14px;
  font-weight: 700;
  color: #10b981;
  text-align: right;
}

.totals-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  font-size: 14px;
  color: #374151;
}

.total-row.total-final {
  padding-top: 16px;
  margin-top: 8px;
  border-top: 2px solid #e5e7eb;
  font-size: 18px;
  font-weight: 800;
  color: #111827;
}

.discount-amount {
  color: #ef4444;
  font-weight: 600;
}
</style>