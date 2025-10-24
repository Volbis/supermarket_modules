<template>
  <div class="promotions-content">
    <div class="page-header">
      <div>
        <h2>🏷️ Gestion des Promotions</h2>
        <p class="subtitle">Gérez les remises et offres promotionnelles</p>
      </div>
      <button class="btn-primary" @click="showCreateModal = true">
        ➕ Nouvelle promotion
      </button>
    </div>

    <!-- Filtres -->
    <div class="filters-section">
      <button 
        :class="['filter-btn', { active: activeFilter === 'all' }]"
        @click="activeFilter = 'all'"
      >
        Toutes ({{ promotions.length }})
      </button>
      <button 
        :class="['filter-btn', { active: activeFilter === 'active' }]"
        @click="activeFilter = 'active'"
      >
        Actives ({{ activePromotions.length }})
      </button>
      <button 
        :class="['filter-btn', { active: activeFilter === 'scheduled' }]"
        @click="activeFilter = 'scheduled'"
      >
        Programmées ({{ scheduledPromotions.length }})
      </button>
      <button 
        :class="['filter-btn', { active: activeFilter === 'expired' }]"
        @click="activeFilter = 'expired'"
      >
        Expirées ({{ expiredPromotions.length }})
      </button>
    </div>

    <!-- Liste des promotions -->
    <div class="promotions-grid">
      <div
        v-for="promo in filteredPromotions"
        :key="promo.id"
        class="promo-card"
      >
        <div class="promo-header">
          <div class="promo-type-badge" :class="'type-' + promo.type">
            {{ getTypeLabel(promo.type) }}
          </div>
          <div class="promo-status" :class="'status-' + promo.status">
            {{ getStatusLabel(promo.status) }}
          </div>
        </div>

        <div class="promo-body">
          <h3 class="promo-title">{{ promo.name }}</h3>
          <p class="promo-description">{{ promo.description }}</p>

          <div class="promo-details">
            <div class="detail-item">
              <span class="detail-icon">💰</span>
              <span class="detail-text">
                {{ formatDiscount(promo) }}
              </span>
            </div>
            <div class="detail-item">
              <span class="detail-icon">📅</span>
              <span class="detail-text">
                {{ formatDateRange(promo.startDate, promo.endDate) }}
              </span>
            </div>
            <div class="detail-item" v-if="promo.timeRange">
              <span class="detail-icon">🕐</span>
              <span class="detail-text">
                {{ promo.timeRange }}
              </span>
            </div>
            <div class="detail-item" v-if="promo.minAmount">
              <span class="detail-icon">🛒</span>
              <span class="detail-text">
                Min. {{ formatPrice(promo.minAmount) }}
              </span>
            </div>
          </div>

          <div class="promo-products" v-if="promo.products && promo.products.length > 0">
            <span class="products-label">Produits concernés:</span>
            <div class="products-tags">
              <span v-for="product in promo.products.slice(0, 3)" :key="product" class="product-tag">
                {{ product }}
              </span>
              <span v-if="promo.products.length > 3" class="product-tag more">
                +{{ promo.products.length - 3 }}
              </span>
            </div>
          </div>
        </div>

        <div class="promo-footer">
          <button class="btn-icon" @click="editPromotion(promo)" title="Modifier">
            ✏️
          </button>
          <button class="btn-icon" @click="duplicatePromotion(promo)" title="Dupliquer">
            📋
          </button>
          <button 
            class="btn-icon" 
            @click="togglePromotion(promo)"
            :title="promo.status === 'active' ? 'Désactiver' : 'Activer'"
          >
            {{ promo.status === 'active' ? '⏸️' : '▶️' }}
          </button>
          <button class="btn-icon danger" @click="deletePromotion(promo)" title="Supprimer">
            🗑️
          </button>
        </div>
      </div>
    </div>

    <!-- Message si aucune promotion -->
    <div v-if="filteredPromotions.length === 0" class="empty-state">
      <div class="empty-icon">🏷️</div>
      <h3>Aucune promotion</h3>
      <p>Créez votre première promotion pour booster vos ventes</p>
      <button class="btn-primary" @click="showCreateModal = true">
        ➕ Créer une promotion
      </button>
    </div>

    <!-- Modal création/édition promotion -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="closeCreateModal">
      <div class="modal-content modal-lg">
        <div class="modal-header">
          <h3>{{ editingPromo ? '✏️ Modifier' : '➕ Créer' }} une promotion</h3>
          <button class="close-btn" @click="closeCreateModal">×</button>
        </div>

        <div class="modal-body">
          <div class="form-section">
            <h4>Informations générales</h4>
            <div class="form-row">
              <div class="form-group">
                <label>Nom de la promotion *</label>
                <input
                  type="text"
                  v-model="formData.name"
                  class="input"
                  placeholder="Ex: Happy Hour"
                >
              </div>
              <div class="form-group">
                <label>Type de promotion *</label>
                <select v-model="formData.type" class="input">
                  <option value="percentage">Pourcentage (%)</option>
                  <option value="fixed">Montant fixe</option>
                  <option value="bogo">BOGO (Achetez-en 1, obtenez-en 1)</option>
                  <option value="bundle">Lot groupé</option>
                  <option value="threshold">Seuil de remise</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>Description</label>
              <textarea
                v-model="formData.description"
                class="input"
                rows="3"
                placeholder="Décrivez la promotion..."
              ></textarea>
            </div>
          </div>

          <div class="form-section">
            <h4>Détails de la remise</h4>
            <div class="form-row">
              <div class="form-group" v-if="formData.type === 'percentage'">
                <label>Pourcentage de remise *</label>
                <div class="input-with-suffix">
                  <input
                    type="number"
                    v-model.number="formData.discountValue"
                    class="input"
                    placeholder="Ex: 10"
                    min="0"
                    max="100"
                  >
                  <span class="suffix">%</span>
                </div>
              </div>
              <div class="form-group" v-if="formData.type === 'fixed'">
                <label>Montant de remise *</label>
                <div class="input-with-suffix">
                  <input
                    type="number"
                    v-model.number="formData.discountValue"
                    class="input"
                    placeholder="Ex: 5000"
                    min="0"
                  >
                  <span class="suffix">CFA</span>
                </div>
              </div>
              <div class="form-group">
                <label>Montant minimum d'achat</label>
                <input
                  type="number"
                  v-model.number="formData.minAmount"
                  class="input"
                  placeholder="Ex: 10000"
                >
              </div>
            </div>
          </div>

          <div class="form-section">
            <h4>Période de validité</h4>
            <div class="form-row">
              <div class="form-group">
                <label>Date de début *</label>
                <input type="date" v-model="formData.startDate" class="input">
              </div>
              <div class="form-group">
                <label>Date de fin *</label>
                <input type="date" v-model="formData.endDate" class="input">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Heure de début (optionnel)</label>
                <input type="time" v-model="formData.startTime" class="input">
              </div>
              <div class="form-group">
                <label>Heure de fin (optionnel)</label>
                <input type="time" v-model="formData.endTime" class="input">
              </div>
            </div>
          </div>

          <div class="form-section">
            <h4>Produits concernés</h4>
            <div class="form-group">
              <label>
                <input type="checkbox" v-model="formData.allProducts">
                Tous les produits
              </label>
            </div>
            <div class="form-group" v-if="!formData.allProducts">
              <label>Sélectionner les produits</label>
              <div class="products-selector">
                <div
                  v-for="product in availableProducts"
                  :key="product"
                  class="product-checkbox"
                >
                  <label>
                    <input
                      type="checkbox"
                      :value="product"
                      v-model="formData.selectedProducts"
                    >
                    {{ product }}
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-secondary" @click="closeCreateModal">
            Annuler
          </button>
          <button class="btn-primary" @click="savePromotion">
            {{ editingPromo ? 'Modifier' : 'Créer' }} la promotion
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PromotionsManagement',
  data() {
    return {
      activeFilter: 'all',
      showCreateModal: false,
      editingPromo: null,
      formData: {
        name: '',
        type: 'percentage',
        description: '',
        discountValue: 0,
        minAmount: 0,
        startDate: '',
        endDate: '',
        startTime: '',
        endTime: '',
        allProducts: true,
        selectedProducts: []
      },
      promotions: [
        {
          id: 1,
          name: 'Happy Hour',
          description: '20% de réduction sur toutes les boissons entre 14h et 16h',
          type: 'percentage',
          discountValue: 20,
          status: 'active',
          startDate: '2025-01-20',
          endDate: '2025-01-31',
          timeRange: '14:00 - 16:00',
          minAmount: null,
          products: ['Coca-Cola 1.5L', 'Fanta Orange', 'Sprite', 'Eau minérale']
        },
        {
          id: 2,
          name: 'Promotion Lait',
          description: 'Achetez 2 boîtes de lait NIDO, obtenez 10% de remise',
          type: 'bogo',
          discountValue: 10,
          status: 'active',
          startDate: '2025-01-15',
          endDate: '2025-02-15',
          timeRange: null,
          minAmount: null,
          products: ['Lait NIDO 400g']
        },
        {
          id: 3,
          name: 'Remise panier 50k',
          description: '5000 CFA de remise pour tout achat supérieur à 50000 CFA',
          type: 'threshold',
          discountValue: 5000,
          status: 'active',
          startDate: '2025-01-01',
          endDate: '2025-12-31',
          timeRange: null,
          minAmount: 50000,
          products: []
        },
        {
          id: 4,
          name: 'Weekend Épicerie',
          description: '15% sur tous les produits d\'épicerie le weekend',
          type: 'percentage',
          discountValue: 15,
          status: 'scheduled',
          startDate: '2025-02-01',
          endDate: '2025-02-28',
          timeRange: null,
          minAmount: null,
          products: ['Riz 5kg', 'Huile 1L', 'Sucre 1kg', 'Farine 1kg', 'Pâtes']
        },
        {
          id: 5,
          name: 'Black Friday',
          description: '30% sur toute la boutique',
          type: 'percentage',
          discountValue: 30,
          status: 'expired',
          startDate: '2024-11-29',
          endDate: '2024-11-29',
          timeRange: null,
          minAmount: null,
          products: []
        }
      ],
      availableProducts: [
        'Coca-Cola 1.5L',
        'Lait NIDO 400g',
        'Pain de mie',
        'Riz 5kg',
        'Huile 1L',
        'Bananes (kg)',
        'Tomates (kg)',
        'Poulet entier',
        'Eau minérale',
        'Savon Lux'
      ]
    };
  },
  computed: {
    filteredPromotions() {
      switch (this.activeFilter) {
        case 'active':
          return this.activePromotions;
        case 'scheduled':
          return this.scheduledPromotions;
        case 'expired':
          return this.expiredPromotions;
        default:
          return this.promotions;
      }
    },
    activePromotions() {
      return this.promotions.filter(p => p.status === 'active');
    },
    scheduledPromotions() {
      return this.promotions.filter(p => p.status === 'scheduled');
    },
    expiredPromotions() {
      return this.promotions.filter(p => p.status === 'expired');
    }
  },
  methods: {
    refreshData() {
      console.log('🏷️ Promotions rafraîchies');
    },
    getTypeLabel(type) {
      const labels = {
        percentage: 'Pourcentage',
        fixed: 'Montant fixe',
        bogo: 'BOGO',
        bundle: 'Lot groupé',
        threshold: 'Seuil'
      };
      return labels[type] || type;
    },
    getStatusLabel(status) {
      const labels = {
        active: 'Active',
        scheduled: 'Programmée',
        expired: 'Expirée'
      };
      return labels[status] || status;
    },
    formatDiscount(promo) {
      if (promo.type === 'percentage') {
        return `-${promo.discountValue}%`;
      } else if (promo.type === 'fixed') {
        return `-${this.formatPrice(promo.discountValue)}`;
      } else if (promo.type === 'bogo') {
        return `Achetez 2, -${promo.discountValue}%`;
      } else if (promo.type === 'threshold') {
        return `-${this.formatPrice(promo.discountValue)}`;
      }
      return 'Remise';
    },
    formatDateRange(start, end) {
      const startDate = new Date(start).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' });
      const endDate = new Date(end).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' });
      return `${startDate} → ${endDate}`;
    },
    formatPrice(amount) {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF',
        minimumFractionDigits: 0
      }).format(amount);
    },
    editPromotion(promo) {
      this.editingPromo = promo;
      this.formData = {
        name: promo.name,
        type: promo.type,
        description: promo.description,
        discountValue: promo.discountValue,
        minAmount: promo.minAmount || 0,
        startDate: promo.startDate,
        endDate: promo.endDate,
        startTime: promo.timeRange ? promo.timeRange.split(' - ')[0] : '',
        endTime: promo.timeRange ? promo.timeRange.split(' - ')[1] : '',
        allProducts: !promo.products || promo.products.length === 0,
        selectedProducts: promo.products || []
      };
      this.showCreateModal = true;
    },
    duplicatePromotion(promo) {
      const newPromo = {
        ...promo,
        id: Date.now(),
        name: promo.name + ' (Copie)',
        status: 'scheduled'
      };
      this.promotions.unshift(newPromo);
      alert('✅ Promotion dupliquée');
    },
    togglePromotion(promo) {
      promo.status = promo.status === 'active' ? 'scheduled' : 'active';
      alert(`${promo.status === 'active' ? '✅ Promotion activée' : '⏸️ Promotion désactivée'}`);
    },
    deletePromotion(promo) {
      if (confirm(`Supprimer la promotion "${promo.name}" ?`)) {
        const index = this.promotions.findIndex(p => p.id === promo.id);
        if (index > -1) {
          this.promotions.splice(index, 1);
          alert('✅ Promotion supprimée');
        }
      }
    },
    closeCreateModal() {
      this.showCreateModal = false;
      this.editingPromo = null;
      this.resetForm();
    },
    resetForm() {
      this.formData = {
        name: '',
        type: 'percentage',
        description: '',
        discountValue: 0,
        minAmount: 0,
        startDate: '',
        endDate: '',
        startTime: '',
        endTime: '',
        allProducts: true,
        selectedProducts: []
      };
    },
    savePromotion() {
      if (!this.formData.name || !this.formData.startDate || !this.formData.endDate) {
        alert('⚠️ Veuillez remplir tous les champs obligatoires');
        return;
      }

      const timeRange = this.formData.startTime && this.formData.endTime
        ? `${this.formData.startTime} - ${this.formData.endTime}`
        : null;

      const promoData = {
        id: this.editingPromo ? this.editingPromo.id : Date.now(),
        name: this.formData.name,
        description: this.formData.description,
        type: this.formData.type,
        discountValue: this.formData.discountValue,
        status: 'active',
        startDate: this.formData.startDate,
        endDate: this.formData.endDate,
        timeRange,
        minAmount: this.formData.minAmount || null,
        products: this.formData.allProducts ? [] : this.formData.selectedProducts
      };

      if (this.editingPromo) {
        const index = this.promotions.findIndex(p => p.id === this.editingPromo.id);
        if (index > -1) {
          this.promotions[index] = promoData;
        }
        alert('✅ Promotion modifiée avec succès');
      } else {
        this.promotions.unshift(promoData);
        alert('✅ Promotion créée avec succès');
      }

      this.closeCreateModal();
    }
  }
};
</script>

<style scoped>
.promotions-content {
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

.filters-section {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.filter-btn {
  padding: 10px 20px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.filter-btn.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-color: #3b82f6;
  color: white;
}

.promotions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.promo-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  transition: all 0.2s ease;
}

.promo-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.promo-header {
  padding: 16px;
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.promo-type-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.type-percentage { background: #dbeafe; color: #1e40af; }
.type-fixed { background: #dcfce7; color: #166534; }
.type-bogo { background: #fef3c7; color: #92400e; }
.type-bundle { background: #f3e8ff; color: #6b21a8; }
.type-threshold { background: #fce7f3; color: #9f1239; }

.promo-status {
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.status-active { background: #dcfce7; color: #166534; }
.status-scheduled { background: #fef3c7; color: #92400e; }
.status-expired { background: #fee2e2; color: #991b1b; }

.promo-body {
  padding: 20px;
}

.promo-title {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
}

.promo-description {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 16px;
  line-height: 1.5;
}

.promo-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #374151;
}

.detail-icon {
  font-size: 16px;
}

.promo-products {
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

.products-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
  display: block;
  margin-bottom: 8px;
}

.products-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.product-tag {
  padding: 4px 10px;
  background: #f3f4f6;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #374151;
}

.product-tag.more {
  background: #e5e7eb;
}

.promo-footer {
  padding: 12px 16px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn-icon {
  width: 36px;
  height: 36px;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
}

.btn-icon:hover {
  background: #f3f4f6;
  transform: scale(1.1);
}

.btn-icon.danger:hover {
  background: #fee2e2;
  border-color: #fecaca;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 24px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 12px;
}

.empty-state p {
  color: #6b7280;
  margin-bottom: 24px;
}

.modal-lg {
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.form-section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.form-section:last-child {
  border-bottom: none;
}

.form-section h4 {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.input-with-suffix {
  position: relative;
}

.input-with-suffix .input {
  padding-right: 50px;
}

.suffix {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 14px;
  font-weight: 700;
  color: #6b7280;
}

.products-selector {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  background: #f9fafb;
}

.product-checkbox {
  padding: 8px;
  border-bottom: 1px solid #e5e7eb;
}

.product-checkbox:last-child {
  border-bottom: none;
}

.product-checkbox label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #374151;
}

.product-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}
</style>