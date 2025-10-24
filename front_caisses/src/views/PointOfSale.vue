<template>
  <div class="pos-content">
    <!-- Interface de caisse en 2 colonnes -->
    <div class="pos-layout">
      
      <!-- Colonne gauche: Produits et recherche -->
      <div class="pos-left">
        <!-- Barre de recherche produit -->
        <div class="search-section">
          <div class="search-container-pos">
            <span class="search-icon">🔍</span>
            <input 
              type="text" 
              placeholder="Rechercher un produit ou scanner code-barres..."
              v-model="searchQuery"
              @keyup.enter="searchProduct"
              @input="handleSearchInput"
              ref="searchInput"
              class="search-input-pos"
            >
            <button v-if="searchQuery" @click="clearSearch" class="clear-btn-pos">×</button>
          </div>
          
          <!-- Résultats de recherche -->
          <div v-if="searchResults.length > 0" class="search-results">
            <div
              v-for="product in searchResults"
              :key="product.id"
              class="search-result-item"
              @click="addToCart(product)"
            >
              <div class="product-info-search">
                <span class="product-name-search">{{ product.nom }}</span>
                <span class="product-price-search">{{ formatPrice(product.prix_unitaire) }}</span>
              </div>
              <div class="product-stock-search">
                <span :class="['stock-badge', { 'low': product.quantite_en_stock < 10 }]">
                  Stock: {{ product.quantite_en_stock }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Raccourcis catégories -->
        <div class="categories-quick">
          <h3 class="section-title">Catégories rapides</h3>
          <div class="categories-grid">
            <button
              v-for="category in quickCategories"
              :key="category.id"
              :class="['category-btn', { active: selectedCategory === category.id }]"
              @click="selectCategory(category.id)"
            >
              <span class="category-icon">{{ category.icon }}</span>
              <span class="category-name">{{ category.nom }}</span>
            </button>
          </div>
        </div>

        <!-- Liste produits de la catégorie sélectionnée -->
        <div v-if="selectedCategory" class="products-list">
          <div class="products-header">
            <h3>Produits</h3>
            <button class="btn-secondary-sm" @click="selectedCategory = null">
              ← Retour
            </button>
          </div>
          <div class="products-grid-pos">
            <div
              v-for="product in categoryProducts"
              :key="product.id"
              class="product-card-pos"
              @click="addToCart(product)"
            >
              <div class="product-image-pos">
                <span class="product-emoji">📦</span>
              </div>
              <div class="product-details-pos">
                <h4 class="product-name-pos">{{ product.nom }}</h4>
                <p class="product-price-pos">{{ formatPrice(product.prix_unitaire) }}</p>
                <span class="product-stock-pos">{{ product.quantite_en_stock }} en stock</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Colonne droite: Panier et actions -->
      <div class="pos-right">
        <!-- En-tête du panier -->
        <div class="cart-header">
          <h2 class="cart-title">🛒 Panier</h2>
          <div class="cart-actions-header">
            <button class="btn-secondary-sm" @click="suspendTransaction" v-if="cart.length > 0">
              ⏸️ Suspendre
            </button>
            <button class="btn-danger-sm" @click="clearCart" v-if="cart.length > 0">
              🗑️ Vider
            </button>
          </div>
        </div>

        <!-- Liste des articles du panier -->
        <div class="cart-items">
          <div v-if="cart.length === 0" class="cart-empty">
            <div class="empty-icon">🛒</div>
            <p>Le panier est vide</p>
            <span class="empty-hint">Scannez ou recherchez un produit pour commencer</span>
          </div>

          <div v-else class="cart-list">
            <div
              v-for="(item, index) in cart"
              :key="index"
              class="cart-item"
            >
              <div class="cart-item-info">
                <h4 class="cart-item-name">{{ item.nom }}</h4>
                <p class="cart-item-price">{{ formatPrice(item.prix_unitaire) }} × {{ item.quantity }}</p>
              </div>
              
              <div class="cart-item-controls">
                <div class="quantity-controls">
                  <button class="qty-btn" @click="decreaseQuantity(index)">−</button>
                  <input
                    type="number"
                    v-model.number="item.quantity"
                    @input="updateQuantity(index)"
                    class="qty-input"
                    min="1"
                  >
                  <button class="qty-btn" @click="increaseQuantity(index)">+</button>
                </div>
                
                <div class="cart-item-total">
                  {{ formatPrice(item.prix_unitaire * item.quantity) }}
                </div>
                
                <button class="remove-btn" @click="removeFromCart(index)">
                  🗑️
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Résumé du panier -->
        <div class="cart-summary">
          <div class="summary-row">
            <span>Sous-total</span>
            <span class="summary-value">{{ formatPrice(subtotal) }}</span>
          </div>
          <div class="summary-row">
            <span>Remise</span>
            <span class="summary-value discount">-{{ formatPrice(discount) }}</span>
          </div>
          <div class="summary-row">
            <span>TVA (18%)</span>
            <span class="summary-value">{{ formatPrice(tax) }}</span>
          </div>
          <div class="summary-row total">
            <span>TOTAL</span>
            <span class="summary-total">{{ formatPrice(total) }}</span>
          </div>
        </div>

        <!-- Boutons d'action -->
        <div class="cart-actions">
          <button
            class="btn btn-secondary btn-full"
            @click="applyDiscount"
            :disabled="cart.length === 0"
          >
            🏷️ Appliquer une remise
          </button>
          <button
            class="btn btn-primary btn-full"
            @click="proceedToPayment"
            :disabled="cart.length === 0"
          >
            💳 Payer ({{ formatPrice(total) }})
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Remise manuelle -->
    <div v-if="showDiscountModal" class="modal-overlay" @click.self="closeDiscountModal">
      <div class="modal-content modal-sm">
        <div class="modal-header">
          <h3>🏷️ Appliquer une remise</h3>
          <button class="close-btn" @click="closeDiscountModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Type de remise</label>
            <select v-model="discountType" class="input">
              <option value="percent">Pourcentage (%)</option>
              <option value="fixed">Montant fixe (CFA)</option>
            </select>
          </div>
          <div class="form-group">
            <label>Valeur</label>
            <input
              type="number"
              v-model.number="discountValue"
              class="input"
              :placeholder="discountType === 'percent' ? 'Ex: 10 pour 10%' : 'Ex: 5000'"
              min="0"
            >
          </div>
          <div class="form-group">
            <label>Raison (optionnel)</label>
            <input
              type="text"
              v-model="discountReason"
              class="input"
              placeholder="Ex: Client fidèle"
            >
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeDiscountModal">Annuler</button>
          <button class="btn-submit" @click="confirmDiscount">Appliquer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useDataCache } from '@/composables/useDataCache';
import produitsAPI from '@/services/produits';

export default {
  name: 'PointOfSale',
  setup() {
    const { loadWithCache, invalidateCache } = useDataCache();
    return { loadWithCache, invalidateCache };
  },
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      selectedCategory: null,
      cart: [],
      products: [
        // Boissons (catégorie 1)
        { id: 1, nom: 'Coca-Cola 1.5L', reference: 'BV001', prix_unitaire: 1200, quantite_en_stock: 45, categorie: 1 },
        { id: 2, nom: 'Fanta Orange 1.5L', reference: 'BV002', prix_unitaire: 1100, quantite_en_stock: 38, categorie: 1 },
        { id: 3, nom: 'Sprite 1.5L', reference: 'BV003', prix_unitaire: 1100, quantite_en_stock: 42, categorie: 1 },
        { id: 4, nom: 'Eau minérale 1.5L', reference: 'BV004', prix_unitaire: 500, quantite_en_stock: 120, categorie: 1 },
        { id: 5, nom: 'Jus d\'orange Tropicana 1L', reference: 'BV005', prix_unitaire: 1800, quantite_en_stock: 25, categorie: 1 },
        { id: 6, nom: 'Bière Castel 33cl', reference: 'BV006', prix_unitaire: 800, quantite_en_stock: 60, categorie: 1 },
        
        // Fruits (catégorie 2)
        { id: 7, nom: 'Bananes (kg)', reference: 'FR001', prix_unitaire: 1500, quantite_en_stock: 50, categorie: 2 },
        { id: 8, nom: 'Oranges (kg)', reference: 'FR002', prix_unitaire: 2000, quantite_en_stock: 35, categorie: 2 },
        { id: 9, nom: 'Pommes (kg)', reference: 'FR003', prix_unitaire: 2500, quantite_en_stock: 28, categorie: 2 },
        { id: 10, nom: 'Mangues (kg)', reference: 'FR004', prix_unitaire: 1800, quantite_en_stock: 40, categorie: 2 },
        { id: 11, nom: 'Pastèque (unité)', reference: 'FR005', prix_unitaire: 3500, quantite_en_stock: 15, categorie: 2 },
        { id: 12, nom: 'Ananas (unité)', reference: 'FR006', prix_unitaire: 1200, quantite_en_stock: 22, categorie: 2 },
        
        // Légumes (catégorie 3)
        { id: 13, nom: 'Tomates (kg)', reference: 'LG001', prix_unitaire: 1200, quantite_en_stock: 45, categorie: 3 },
        { id: 14, nom: 'Oignons (kg)', reference: 'LG002', prix_unitaire: 1000, quantite_en_stock: 55, categorie: 3 },
        { id: 15, nom: 'Carottes (kg)', reference: 'LG003', prix_unitaire: 1100, quantite_en_stock: 38, categorie: 3 },
        { id: 16, nom: 'Pommes de terre (kg)', reference: 'LG004', prix_unitaire: 900, quantite_en_stock: 70, categorie: 3 },
        { id: 17, nom: 'Salade verte (unité)', reference: 'LG005', prix_unitaire: 600, quantite_en_stock: 30, categorie: 3 },
        { id: 18, nom: 'Poivrons (kg)', reference: 'LG006', prix_unitaire: 1500, quantite_en_stock: 25, categorie: 3 },
        
        // Produits laitiers (catégorie 4)
        { id: 19, nom: 'Lait NIDO 400g', reference: 'PL001', prix_unitaire: 3500, quantite_en_stock: 48, categorie: 4 },
        { id: 20, nom: 'Yaourt Danone x4', reference: 'PL002', prix_unitaire: 1800, quantite_en_stock: 35, categorie: 4 },
        { id: 21, nom: 'Fromage Vache qui rit', reference: 'PL003', prix_unitaire: 2200, quantite_en_stock: 40, categorie: 4 },
        { id: 22, nom: 'Beurre 250g', reference: 'PL004', prix_unitaire: 2000, quantite_en_stock: 28, categorie: 4 },
        { id: 23, nom: 'Crème fraîche 200ml', reference: 'PL005', prix_unitaire: 1500, quantite_en_stock: 22, categorie: 4 },
        
        // Viandes (catégorie 5)
        { id: 24, nom: 'Poulet entier (kg)', reference: 'VD001', prix_unitaire: 3500, quantite_en_stock: 18, categorie: 5 },
        { id: 25, nom: 'Bœuf (kg)', reference: 'VD002', prix_unitaire: 5000, quantite_en_stock: 12, categorie: 5 },
        { id: 26, nom: 'Mouton (kg)', reference: 'VD003', prix_unitaire: 4500, quantite_en_stock: 15, categorie: 5 },
        { id: 27, nom: 'Saucisses (kg)', reference: 'VD004', prix_unitaire: 3000, quantite_en_stock: 25, categorie: 5 },
        
        // Poissons (catégorie 6)
        { id: 28, nom: 'Tilapia (kg)', reference: 'PS001', prix_unitaire: 2800, quantite_en_stock: 20, categorie: 6 },
        { id: 29, nom: 'Carpe (kg)', reference: 'PS002', prix_unitaire: 3200, quantite_en_stock: 15, categorie: 6 },
        { id: 30, nom: 'Thon en boîte', reference: 'PS003', prix_unitaire: 1500, quantite_en_stock: 45, categorie: 6 },
        { id: 31, nom: 'Sardines en boîte', reference: 'PS004', prix_unitaire: 800, quantite_en_stock: 60, categorie: 6 },
        
        // Épicerie (catégorie 7)
        { id: 32, nom: 'Riz 5kg', reference: 'EP001', prix_unitaire: 4500, quantite_en_stock: 35, categorie: 7 },
        { id: 33, nom: 'Huile végétale 1L', reference: 'EP002', prix_unitaire: 2200, quantite_en_stock: 50, categorie: 7 },
        { id: 34, nom: 'Pâtes alimentaires 500g', reference: 'EP003', prix_unitaire: 800, quantite_en_stock: 65, categorie: 7 },
        { id: 35, nom: 'Sucre 1kg', reference: 'EP004', prix_unitaire: 1200, quantite_en_stock: 45, categorie: 7 },
        { id: 36, nom: 'Sel 1kg', reference: 'EP005', prix_unitaire: 400, quantite_en_stock: 80, categorie: 7 },
        { id: 37, nom: 'Farine 1kg', reference: 'EP006', prix_unitaire: 900, quantite_en_stock: 55, categorie: 7 },
        { id: 38, nom: 'Café Nescafé 200g', reference: 'EP007', prix_unitaire: 3500, quantite_en_stock: 28, categorie: 7 },
        { id: 39, nom: 'Thé Lipton x100', reference: 'EP008', prix_unitaire: 2500, quantite_en_stock: 32, categorie: 7 },
        
        // Hygiène (catégorie 8)
        { id: 40, nom: 'Savon Lux x4', reference: 'HY001', prix_unitaire: 1800, quantite_en_stock: 42, categorie: 8 },
        { id: 41, nom: 'Dentifrice Colgate', reference: 'HY002', prix_unitaire: 1500, quantite_en_stock: 38, categorie: 8 },
        { id: 42, nom: 'Shampoing 400ml', reference: 'HY003', prix_unitaire: 2500, quantite_en_stock: 30, categorie: 8 },
        { id: 43, nom: 'Papier toilette x12', reference: 'HY004', prix_unitaire: 3000, quantite_en_stock: 25, categorie: 8 },
        { id: 44, nom: 'Lessive OMO 1kg', reference: 'HY005', prix_unitaire: 2800, quantite_en_stock: 35, categorie: 8 },
        { id: 45, nom: 'Désodorisant', reference: 'HY006', prix_unitaire: 1200, quantite_en_stock: 40, categorie: 8 },
      ],
      categories: [],
      quickCategories: [
        { id: 1, nom: 'Boissons', icon: '🥤' },
        { id: 2, nom: 'Fruits', icon: '🍎' },
        { id: 3, nom: 'Légumes', icon: '🥕' },
        { id: 4, nom: 'Produits laitiers', icon: '🥛' },
        { id: 5, nom: 'Viandes', icon: '🥩' },
        { id: 6, nom: 'Poissons', icon: '🐟' },
        { id: 7, nom: 'Épicerie', icon: '🌾' },
        { id: 8, nom: 'Hygiène', icon: '🧴' },
      ],
      showDiscountModal: false,
      discountType: 'percent',
      discountValue: 0,
      discountReason: '',
      manualDiscount: 0,
      loading: false
    };
  },
  computed: {
    categoryProducts() {
      if (!this.selectedCategory) return [];
      return this.products.filter(p => p.categorie === this.selectedCategory);
    },
    subtotal() {
      return this.cart.reduce((sum, item) => sum + (item.prix_unitaire * item.quantity), 0);
    },
    discount() {
      return this.manualDiscount;
    },
    tax() {
      return (this.subtotal - this.discount) * 0.18;
    },
    total() {
      return this.subtotal - this.discount + this.tax;
    }
  },
  mounted() {
    // Pas besoin de charger depuis l'API, on utilise les données mockées
    // this.loadProducts();
    this.focusSearch();
  },
  methods: {
    async refreshData() {
      console.log('🔄 Rafraîchissement Point de vente...');
      this.invalidateCache('produits');
      await this.loadProducts(true);
    },
    async loadProducts(forceRefresh = false) {
      this.loading = true;
      try {
        this.products = await this.loadWithCache('produits', async () => {
          const response = await produitsAPI.getAllProduits();
          return response.data || [];
        }, forceRefresh);
      } catch (error) {
        console.error('Erreur chargement produits:', error);
        this.products = [];
      } finally {
        this.loading = false;
      }
    },
    handleSearchInput() {
      if (this.searchQuery.length >= 2) {
        this.searchResults = this.products.filter(p =>
          p.nom.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          p.reference?.toLowerCase().includes(this.searchQuery.toLowerCase())
        ).slice(0, 5);
      } else {
        this.searchResults = [];
      }
    },
    searchProduct() {
      if (this.searchResults.length > 0) {
        this.addToCart(this.searchResults[0]);
      }
    },
    clearSearch() {
      this.searchQuery = '';
      this.searchResults = [];
      this.focusSearch();
    },
    focusSearch() {
      this.$nextTick(() => {
        this.$refs.searchInput?.focus();
      });
    },
    selectCategory(categoryId) {
      this.selectedCategory = categoryId;
    },
    addToCart(product) {
      const existingIndex = this.cart.findIndex(item => item.id === product.id);
      
      if (existingIndex > -1) {
        this.cart[existingIndex].quantity++;
      } else {
        this.cart.push({
          ...product,
          quantity: 1
        });
      }
      
      this.clearSearch();
      this.selectedCategory = null;
      
      // Bip sonore (optionnel)
      this.playBeep();
    },
    removeFromCart(index) {
      this.cart.splice(index, 1);
    },
    increaseQuantity(index) {
      this.cart[index].quantity++;
    },
    decreaseQuantity(index) {
      if (this.cart[index].quantity > 1) {
        this.cart[index].quantity--;
      } else {
        this.removeFromCart(index);
      }
    },
    updateQuantity(index) {
      if (this.cart[index].quantity < 1) {
        this.cart[index].quantity = 1;
      }
    },
    clearCart() {
      if (confirm('Êtes-vous sûr de vouloir vider le panier ?')) {
        this.cart = [];
        this.manualDiscount = 0;
      }
    },
    suspendTransaction() {
      if (confirm('Suspendre cette transaction ?')) {
        // Sauvegarder la transaction suspendue
        const suspended = {
          id: Date.now(),
          cart: [...this.cart],
          discount: this.manualDiscount,
          date: new Date()
        };
        
        const suspendedTransactions = JSON.parse(localStorage.getItem('suspended_transactions') || '[]');
        suspendedTransactions.push(suspended);
        localStorage.setItem('suspended_transactions', JSON.stringify(suspendedTransactions));
        
        this.cart = [];
        this.manualDiscount = 0;
        
        alert('✅ Transaction suspendue avec succès');
      }
    },
    applyDiscount() {
      this.showDiscountModal = true;
    },
    closeDiscountModal() {
      this.showDiscountModal = false;
      this.discountValue = 0;
      this.discountReason = '';
    },
    confirmDiscount() {
      if (this.discountType === 'percent') {
        this.manualDiscount = this.subtotal * (this.discountValue / 100);
      } else {
        this.manualDiscount = this.discountValue;
      }
      
      this.closeDiscountModal();
    },
    proceedToPayment() {
      alert(`Passage au paiement: ${this.formatPrice(this.total)}\n(Fonctionnalité à implémenter dans la vue Payment)`);
      // TODO: Naviguer vers la vue Payment avec les données du panier
    },
    playBeep() {
      // Simulation d'un bip sonore
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);
      
      oscillator.frequency.value = 800;
      oscillator.type = 'sine';
      
      gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
      
      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + 0.1);
    },
    formatPrice(amount) {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF',
        minimumFractionDigits: 0
      }).format(amount);
    }
  }
};
</script>

<style scoped>
.pos-content {
  padding: 20px;
  height: calc(100vh - 160px);
  overflow: hidden;
}

.pos-layout {
  display: grid;
  grid-template-columns: 1fr 480px;
  gap: 24px;
  height: 100%;
}

/* === COLONNE GAUCHE === */
.pos-left {
  background: white;
  border-radius: 16px;
  padding: 24px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
}

.search-section {
  margin-bottom: 24px;
  position: relative;
}

.search-container-pos {
  position: relative;
  display: flex;
  align-items: center;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 14px 18px;
  transition: all 0.3s ease;
}

.search-container-pos:focus-within {
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-icon {
  font-size: 20px;
  margin-right: 12px;
}

.search-input-pos {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  color: #111827;
  background: transparent;
}

.clear-btn-pos {
  width: 28px;
  height: 28px;
  border: none;
  background: #e5e7eb;
  border-radius: 50%;
  color: #6b7280;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-btn-pos:hover {
  background: #d1d5db;
  color: #111827;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 8px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  max-height: 400px;
  overflow-y: auto;
  z-index: 100;
}

.search-result-item {
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
  transition: background 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background: #f9fafb;
}

.product-info-search {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-name-search {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
}

.product-price-search {
  font-size: 14px;
  color: #10b981;
  font-weight: 600;
}

.stock-badge {
  padding: 4px 10px;
  background: #d1fae5;
  color: #065f46;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.stock-badge.low {
  background: #fed7aa;
  color: #92400e;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 16px;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
}

.category-btn {
  padding: 16px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.category-btn:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.category-btn.active {
  border-color: #3b82f6;
  background: #eff6ff;
}

.category-icon {
  font-size: 32px;
}

.category-name {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  text-align: center;
}

.products-list {
  margin-top: 24px;
}

.products-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.btn-secondary-sm {
  padding: 8px 16px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  color: #374151;
}

.btn-danger-sm {
  padding: 8px 16px;
  background: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  color: #dc2626;
}

.products-grid-pos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.product-card-pos {
  padding: 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.product-card-pos:hover {
  border-color: #10b981;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
}

.product-image-pos {
  width: 100%;
  height: 80px;
  background: #f9fafb;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.product-emoji {
  font-size: 40px;
}

.product-name-pos {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 4px;
}

.product-price-pos {
  font-size: 15px;
  font-weight: 700;
  color: #10b981;
  margin-bottom: 4px;
}

.product-stock-pos {
  font-size: 12px;
  color: #6b7280;
}

/* === COLONNE DROITE === */
.pos-right {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.cart-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cart-title {
  font-size: 22px;
  font-weight: 700;
  color: #111827;
}

.cart-actions-header {
  display: flex;
  gap: 8px;
}

.cart-items {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.cart-empty {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-hint {
  font-size: 13px;
  color: #d1d5db;
  margin-top: 8px;
}

.cart-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cart-item {
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.cart-item-info {
  margin-bottom: 12px;
}

.cart-item-name {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 4px;
}

.cart-item-price {
  font-size: 13px;
  color: #6b7280;
}

.cart-item-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.qty-btn {
  width: 32px;
  height: 32px;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.qty-btn:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.qty-input {
  width: 50px;
  text-align: center;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 6px;
  font-size: 14px;
  font-weight: 600;
}

.cart-item-total {
  flex: 1;
  text-align: right;
  font-size: 16px;
  font-weight: 700;
  color: #10b981;
}

.remove-btn {
  width: 32px;
  height: 32px;
  border: 1px solid #fecaca;
  background: #fee2e2;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-btn:hover {
  background: #ef4444;
  color: white;
}

.cart-summary {
  padding: 20px 24px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  font-size: 14px;
  color: #374151;
}

.summary-value {
  font-weight: 600;
}

.summary-value.discount {
  color: #10b981;
}

.summary-row.total {
  margin-top: 12px;
  padding-top: 16px;
  border-top: 2px solid #e5e7eb;
  font-size: 18px;
  font-weight: 700;
}

.summary-total {
  font-size: 24px;
  font-weight: 800;
  color: #10b981;
}

.cart-actions {
  padding: 16px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-full {
  width: 100%;
  justify-content: center;
  padding: 14px 24px;
  font-size: 15px;
}

/* Modal styles */
.modal-sm {
  max-width: 500px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.btn-cancel,
.btn-submit {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #e5e7eb;
}

.btn-submit {
  background: #10b981;
  color: white;
  border: none;
}

.btn-submit:hover {
  background: #059669;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}
</style>