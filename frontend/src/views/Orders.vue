<template>
  <div class="orders-page">
    <!-- Cartes de statistiques -->
    <div class="stats-container">
      <div class="stat-card">
        <div class="stat-content">
          <h3>Total commande Mois <br>Octobre 2024</h3>
          <div class="stat-icon">
            <img src="@/assets/icons/form.svg" alt="Total Commandes" />
          </div>
        </div>
        <div class="stat-bar"></div>
      </div>
      
      <div class="stat-card">
        <div class="stat-content">
          <h3>Commande en cours</h3>
          <div class="stat-icon">
            <img src="@/assets/icons/box.png" alt="Total Commandes" />
          </div>
        </div>
        <div class="stat-bar"></div>
      </div>
      
      <div class="stat-card">
        <div class="stat-content">
          <h3>Total Fournisseurs</h3>
          <div class="stat-icon">
            <img src="@/assets/icons/livraison.png" alt="Total Commandes" />
          </div>
        </div>
        <div class="stat-bar"></div>
      </div>
    </div>

    <!-- Barre de recherche -->

    <div class="search-bar-container">
        <div class="search-wrapper">
            <span class="search-icon">🔍</span>
            <div class="input-bg">
                <input type="text" placeholder="Rechercher commande" v-model="searchQuery">
            </div>
            <div class="status-bg">
                <select v-model="selectedStatus" class="status-filter">
                    <option value="">Statut</option>
                    <option value="pending">En attente</option>
                    <option value="processing">En cours</option>
                    <option value="shipped">Expédié</option>
                    <option value="delivered">Livré</option>
                </select>
            </div>
        </div>
        <button class="pass-order-btn" @click="openModal">
            <span class="btn-icon">
              <img src="@/assets/icons/plus.png" alt="Nouvelle commande" style="width: 1em; color: white; height: 1em; vertical-align: middle; margin-right: 5px;">
            </span>
            Passer commande
        </button>
    </div>


    <!-- Tableau des commandes -->
    <div class="orders-list-container">
      <h2>Liste des commandes</h2>
      
      <table class="orders-table">
        <thead>
          <tr>
            <th>Produit</th>
            <th>Qte</th>
            <th>Fournisseur</th>
            <th>Date Arrivage</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in filteredOrders" :key="order.id">
            <td>{{ order.product }}</td>
            <td>{{ order.quantity }}</td>
            <td>{{ order.supplier }}</td>
            <td>{{ order.arrivalDate }}</td>
            <td>
              <span :class="['status-badge', order.status]">
                {{ getStatusLabel(order.status) }}
              </span>
            </td>
            <td class="actions-cell">
              <button class="action-icon" title="Modifier">✏️</button>
              <button class="action-icon" title="Voir">👁️</button>
              <button class="action-icon delete" title="Supprimer">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Modal: Nouvelle commande -->
  <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
    <div class="modal-card">
      <div class="modal-header">
        <h3>Nouvelle commande</h3>
        <button class="close-btn" @click="closeModal">✕</button>
      </div>
      <form class="modal-body" @submit.prevent="submitOrder">
        <div class="form-row">
          <label for="product">Produit</label>
          <input id="product" v-model="form.product" type="text" placeholder="Ex: Coca-Cola" required>
        </div>

        <div class="form-row">
          <label for="quantity">Quantité</label>
          <input id="quantity" v-model="form.quantity" type="text" placeholder="Ex: 500 Packs" required>
        </div>

        <div class="form-row">
          <label for="supplier">Fournisseur</label>
          <input id="supplier" v-model="form.supplier" type="text" placeholder="Ex: Solibra" required>
        </div>

        <div class="form-row">
          <label for="arrivalDate">Date d'arrivage</label>
          <input id="arrivalDate" v-model="form.arrivalDate" type="date" required>
        </div>

        <div class="form-row">
          <label for="status">Statut</label>
          <select id="status" v-model="form.status" required>
            <option value="pending">En attente</option>
            <option value="processing">En cours</option>
            <option value="shipped">Expédié</option>
            <option value="delivered">Livré</option>
          </select>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn-secondary" @click="closeModal">Annuler</button>
          <button type="submit" class="btn-primary">Ajouter</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrdersManagementPage',
  data() {
    return {
      searchQuery: '',
      selectedStatus: '',
      showModal: false,
      nextOrderId: 5,
      form: {
        product: '',
        quantity: '',
        supplier: '',
        arrivalDate: '',
        status: 'pending'
      },
      orders: [
        {
          id: 1,
          product: 'Coca-Cola II',
          quantity: '500 Packs',
          supplier: 'Solibra',
          arrivalDate: '20/12/2025',
          status: 'processing'
        },
        {
          id: 2,
          product: 'Fanta Orange',
          quantity: '300 Packs',
          supplier: 'Solibra',
          arrivalDate: '22/12/2025',
          status: 'pending'
        },
        {
          id: 3,
          product: 'Sprite Lemon',
          quantity: '250 Packs',
          supplier: 'Maison Africaine',
          arrivalDate: '18/12/2025',
          status: 'shipped'
        },
        {
          id: 4,
          product: 'Jus Tropical',
          quantity: '150 Packs',
          supplier: 'Solibra',
          arrivalDate: '15/12/2025',
          status: 'delivered'
        }
      ]
    };
  },
  computed: {
    filteredOrders() {
      return this.orders.filter(order => {
        const matchesSearch =
          order.product.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          order.supplier.toLowerCase().includes(this.searchQuery.toLowerCase());
        const matchesStatus = !this.selectedStatus || order.status === this.selectedStatus;
        return matchesSearch && matchesStatus;
      });
    }
  },
  methods: {
    getStatusLabel(status) {
      const labels = {
        pending: 'En attente',
        processing: 'En cours',
        shipped: 'Expédié',
        delivered: 'Livré'
      };
      return labels[status] || status;
    },
    getStatusStyle(status) {
      // Les styles corrects selon le design général de status-badge dans le CSS du composant
      switch (status) {
        case 'pending':
          return {
            background: '#fff3cd',
            color: '#856404',
            fontWeight: 600,
            borderRadius: '20px',
            padding: '6px 12px',
            textTransform: 'capitalize',
            fontSize: '12px',
            minWidth: '110px',
            textAlign: 'center',
            display: 'inline-block',
            boxSizing: 'border-box'
          };
        case 'processing':
          return {
            background: '#cce5ff',
            color: '#003d99',
            fontWeight: 600,
            borderRadius: '20px',
            padding: '6px 12px',
            textTransform: 'capitalize',
            fontSize: '12px',
            minWidth: '110px',
            textAlign: 'center',
            display: 'inline-block',
            boxSizing: 'border-box'
          };
        case 'shipped':
          return {
            background: '#d4edda',
            color: '#155724',
            fontWeight: 600,
            borderRadius: '20px',
            padding: '6px 12px',
            textTransform: 'capitalize',
            fontSize: '12px',
            minWidth: '110px',
            textAlign: 'center',
            display: 'inline-block',
            boxSizing: 'border-box'
          };
        case 'delivered':
          return {
            background: '#e2d9f3',
            color: '#6f42c1',
            fontWeight: 600,
            borderRadius: '20px',
            padding: '6px 12px',
            textTransform: 'capitalize',
            fontSize: '12px',
            minWidth: '110px',
            textAlign: 'center',
            display: 'inline-block',
            boxSizing: 'border-box'
          };
        default:
          return {
            background: '#f5f5f5',
            color: '#333',
            fontWeight: 600,
            borderRadius: '20px',
            padding: '6px 12px',
            textTransform: 'capitalize',
            fontSize: '12px',
            minWidth: '110px',
            textAlign: 'center',
            display: 'inline-block',
            boxSizing: 'border-box'
          };
      }
    },
    openModal() {
      this.resetForm();
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    submitOrder() {
      const newOrder = {
        id: this.nextOrderId++,
        product: this.form.product.trim(),
        quantity: this.form.quantity.trim(),
        supplier: this.form.supplier.trim(),
        arrivalDate: this.formatDateDisplay(this.form.arrivalDate),
        status: this.form.status
      };

      if (!newOrder.product || !newOrder.quantity || !newOrder.supplier || !this.form.arrivalDate) {
        return;
      }

      this.orders.unshift(newOrder);
      this.closeModal();
    },
    resetForm() {
      this.form = {
        product: '',
        quantity: '',
        supplier: '',
        arrivalDate: '',
        status: 'pending'
      };
    },
    formatDateDisplay(isoDate) {
      // Convertit yyyy-mm-dd en dd/mm/yyyy
      if (!isoDate) return '';
      const [y, m, d] = isoDate.split('-');
      return `${d}/${m}/${y}`;
    }
    }
  
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.orders-page {
  padding: 20px;
  background: #F9F9FA;
  min-height: 100vh;
}

/* Cartes de statistiques */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 17px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

.stat-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.stat-card h3 {
  font-size: 14px;
  font-weight: 500;
  color: #666;
  flex: 1;
}

.stat-icon {
  font-size: 32px;
  margin-left: 10px;
}

.stat-bar {
  height: 3px;
  width: 10%;
  border-radius: 2px;
  margin-left: 0;
}

/* Couleurs différentes pour chaque card */
.stats-container .stat-card:nth-child(1) .stat-bar {
  background: linear-gradient(to right, #ffc107, #ffecb3); /* Jaune doré */
}
.stats-container .stat-card:nth-child(2) .stat-bar {
  background: linear-gradient(to right, #2196f3, #b3e5fc); /* Bleu */
}
.stats-container .stat-card:nth-child(3) .stat-bar {
  background: linear-gradient(to right, #4caf50, #c8e6c9); /* Vert */
}


/* Barre de recherche */
.search-bar-container {

  width: 100%;
  height: 45px;
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  border-radius: 17px;
  align-items: center;
}

.search-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 17px;
  padding: 0 20px;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.search-icon {
  font-size: 18px;
  color: #999;
  flex-shrink: 0;
}

.search-wrapper input {
  flex: 1;
  border: none;
  outline: none;
  padding: 12px 0;
  font-size: 14px;
  background: transparent;
  color: #333;
}

.search-wrapper input::placeholder {
  color: #999;
}

.status-filter {
  padding: 8px 12px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  outline: none;
  flex-shrink: 0;
}

.status-filter option {
  color: #333;
}

.pass-order-btn {
  background: #D08700;
  color: white;
  border: none;
  padding: 12px 28px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(255, 193, 7, 0.35);
  transition: all 0.3s ease;
  white-space: nowrap;
  font-size: 14px;
}


.pass-order-btn:active {
  transform: translateY(0);
}

.btn-icon {
  font-size: 16px;
  display: flex;
  align-items: center;
}

@media (max-width: 768px) {
  .search-bar-container {
    flex-direction: column;
    gap: 12px;
  }

  .search-wrapper {
    width: 100%;
  }

  .pass-order-btn {
    width: 100%;
    justify-content: center;
  }
}

/* barre backgrounds */
.input-bg {
  background:rgba(249, 249, 249, 0);
  border-radius: 17px;
  padding: 0 10px;
  width: 80%;
  height: 80%;
}

.status-bg {
  background: #f9f9f9;
  border-radius: 17px;
  padding: 0 10px;
  height: 100%;
  border: 1px solid #F5F5F5;
}

/* Tableau des commandes */
.orders-list-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.orders-list-container h2 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
}

.orders-table th {
  background: #f9f9f9;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
  color: #666;
  border-bottom: 2px solid #e0e0e0;
}

.orders-table td {
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
  font-size: 14px;
  color: #333;
}

.orders-table tbody tr:hover {
  background: #fafafa;
}

.status-badge {
  display: inline-block;
  min-width: 110px;
  text-align: center;
  box-sizing: border-box;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.status-badge.processing {
  background: #cce5ff;
  color: #003d99;
}

.status-badge.shipped {
  background: #d4edda;
  color: #155724;
}

.status-badge.delivered {
  background: #e2d9f3;
  color: #6f42c1;
}

.actions-cell {
  display: flex;
  gap: 10px;
}

.action-icon {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.2s;
  padding: 4px 8px;
}

.action-icon:hover {
  transform: scale(1.2);
}

.action-icon.delete:hover {
  color: red;
}

/* Responsive */
@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: 1fr;
  }

  .search-bar-container {
    flex-direction: column;
  }

  .search-wrapper {
    width: 100%;
  }

  .pass-order-btn {
    width: 100%;
    justify-content: center;
  }

  .orders-table th,
  .orders-table td {
    padding: 10px;
    font-size: 12px;
  }
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 1000;
}

.modal-card {
  width: 100%;
  max-width: 520px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 6px 8px;
}

.modal-body {
  padding: 18px 20px 20px 20px;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 14px;
}

.form-row label {
  font-size: 13px;
  color: #555;
}

.form-row input,
.form-row select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #fff;
  font-size: 14px;
  outline: none;
}

.form-row input:focus,
.form-row select:focus {
  border-color: #93c5fd;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #e5e7eb;
  padding: 10px 16px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary {
  background: #2563eb;
  color: #ffffff;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(37, 99, 235, 0.25);
}
</style>