<template>
  <div class="products-content">
    <!-- Header avec statistiques -->
    <div class="products-header">
      <div class="header-info">
        <h2>Gestion des produits</h2>
        <p>{{ filteredProducts.length }} produits disponibles</p>
      </div>
      <button class="add-product-btn" @click="showAddModal">
        <span class="btn-icon">+</span>
        Ajouter un produit
      </button>
    </div>

    <!-- Stats rapides -->
    <div class="quick-stats">
      <div class="stat-item">
        <div class="stat-icon total">📦</div>
        <div class="stat-details">
          <span class="stat-value">{{ products.length }}</span>
          <span class="stat-label">Total produits</span>
        </div>
      </div>
      <div class="stat-item">
        <div class="stat-icon available">✓</div>
        <div class="stat-details">
          <span class="stat-value">{{ availableProducts }}</span>
          <span class="stat-label">En stock</span>
        </div>
      </div>
      <div class="stat-item">
        <div class="stat-icon low">⚠️</div>
        <div class="stat-details">
          <span class="stat-value">{{ lowStockProducts }}</span>
          <span class="stat-label">Stock faible</span>
        </div>
      </div>
      <div class="stat-item">
        <div class="stat-icon value">💰</div>
        <div class="stat-details">
          <span class="stat-value">{{ totalValue }} CFA</span>
          <span class="stat-label">Valeur totale</span>
        </div>
      </div>
    </div>
    
    <!-- Barre de recherche et filtres -->
    <div class="products-toolbar">
      <div class="search-container">
        <span class="search-icon">🔍</span>
        <input 
          type="text" 
          placeholder="Rechercher par nom, catégorie..." 
          v-model="searchQuery"
          class="search-input"
        >
        <button v-if="searchQuery" @click="searchQuery = ''" class="clear-btn">×</button>
      </div>
      
      <div class="filters-container">
        <div class="filter-item">
          <select v-model="selectedCategory" class="filter-select">
            <option value="">📂 Toutes les catégories</option>
            <option value="fruits">🍎 Fruits</option>
            <option value="légumes">🥕 Légumes</option>
            <option value="produits laitiers">🥛 Produits laitiers</option>
          </select>
        </div>
        
        <div class="filter-item">
          <select v-model="sortBy" class="filter-select">
            <option value="name">Trier par nom</option>
            <option value="price">Trier par prix</option>
            <option value="stock">Trier par stock</option>
          </select>
        </div>

        <div class="view-toggle">
          <button 
            :class="['view-btn', { active: viewMode === 'grid' }]"
            @click="viewMode = 'grid'"
            title="Vue grille"
          >
            ⊞
          </button>
          <button 
            :class="['view-btn', { active: viewMode === 'list' }]"
            @click="viewMode = 'list'"
            title="Vue liste"
          >
            ☰
          </button>
        </div>
      </div>
    </div>
    
    <!-- Grille de produits -->
    <div :class="['products-grid', viewMode]">
      <div v-for="product in sortedProducts" :key="product.id" class="product-card">
        <div class="product-badge" v-if="product.stock <= 10">
          <span class="badge-text">Stock faible</span>
        </div>
        
        <div class="product-image">
          <img :src="product.image" :alt="product.name" />
          <div class="product-overlay">
            <button class="quick-action" title="Voir détails">👁️</button>
            <button class="quick-action" title="Modifier">✏️</button>
          </div>
        </div>
        
        <div class="product-info">
          <div class="product-header">
            <h3 class="product-name">{{ product.name }}</h3>
            <span class="product-category-badge">{{ product.category }}</span>
          </div>
          
          <div class="product-details">
            <div class="price-section">
              <span class="product-price">{{ product.price }}</span>
              <span class="price-unit">par {{ product.unit }}</span>
            </div>
            
            <div class="stock-section">
              <div class="stock-progress">
                <div 
                  class="stock-bar" 
                  :style="{ width: getStockPercentage(product.stock) + '%' }"
                  :class="{ 'low': product.stock <= 10, 'medium': product.stock > 10 && product.stock <= 30 }"
                ></div>
              </div>
              <span class="stock-text">{{ product.stock }} unités</span>
            </div>
          </div>
        </div>
        
        <div class="product-actions">
          <button class="action-btn primary" @click="editProduct(product)">
            <span>✏️</span> Modifier
          </button>
          <button class="action-btn secondary" @click="viewProduct(product)">
            <span>👁️</span> Détails
          </button>
          <button class="action-btn danger" @click="deleteProduct(product)">
            <span>🗑️</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Message si aucun produit -->
    <div v-if="sortedProducts.length === 0" class="empty-state">
      <div class="empty-icon">📦</div>
      <h3>Aucun produit trouvé</h3>
      <p>Essayez de modifier vos filtres ou ajoutez un nouveau produit</p>
      <button class="add-product-btn" @click="showAddModal">
        <span class="btn-icon">+</span>
        Ajouter un produit
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductsView',
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      sortBy: 'name',
      viewMode: 'grid',
      products: [
        {
          id: 1,
          name: 'Pommes Golden',
          category: 'Fruits',
          price: '2.50',
          unit: 'kg',
          stock: 45,
          image: 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300&h=300&fit=crop'
        },
        {
          id: 2,
          name: 'Bananes',
          category: 'Fruits',
          price: '1.80',
          unit: 'kg',
          stock: 8,
          image: 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=300&h=300&fit=crop'
        },
        {
          id: 3,
          name: 'Carottes Bio',
          category: 'Légumes',
          price: '1.20',
          unit: 'kg',
          stock: 32,
          image: 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=300&h=300&fit=crop'
        },
        {
          id: 4,
          name: 'Lait entier',
          category: 'Produits laitiers',
          price: '1.50',
          unit: 'litre',
          stock: 5,
          image: 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300&h=300&fit=crop'
        },
        {
          id: 5,
          name: 'Tomates cerises',
          category: 'Légumes',
          price: '3.20',
          unit: 'kg',
          stock: 25,
          image: 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=300&h=300&fit=crop'
        },
        {
          id: 6,
          name: 'Fromage comté',
          category: 'Produits laitiers',
          price: '18.90',
          unit: 'kg',
          stock: 15,
          image: 'https://images.unsplash.com/photo-1452195100486-9cc805987862?w=300&h=300&fit=crop'
        },
        {
          id: 7,
          name: 'Oranges',
          category: 'Fruits',
          price: '2.20',
          unit: 'kg',
          stock: 38,
          image: 'https://images.unsplash.com/photo-1547514701-42782101795e?w=300&h=300&fit=crop'
        },
        {
          id: 8,
          name: 'Salade verte',
          category: 'Légumes',
          price: '1.50',
          unit: 'pièce',
          stock: 12,
          image: 'https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=300&h=300&fit=crop'
        }
      ]
    }
  },
  computed: {
    filteredProducts() {
      return this.products.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                             product.category.toLowerCase().includes(this.searchQuery.toLowerCase())
        const matchesCategory = !this.selectedCategory || 
                               product.category.toLowerCase() === this.selectedCategory.toLowerCase()
        return matchesSearch && matchesCategory
      })
    },
    sortedProducts() {
      const filtered = [...this.filteredProducts]
      return filtered.sort((a, b) => {
        switch(this.sortBy) {
          case 'price':
            return parseFloat(a.price) - parseFloat(b.price)
          case 'stock':
            return b.stock - a.stock
          default:
            return a.name.localeCompare(b.name)
        }
      })
    },
    availableProducts() {
      return this.products.filter(p => p.stock > 10).length
    },
    lowStockProducts() {
      return this.products.filter(p => p.stock <= 10).length
    },
    totalValue() {
      return this.products.reduce((sum, p) => sum + (parseFloat(p.price) * p.stock), 0).toFixed(2)
    }
  },
  methods: {
    getStockPercentage(stock) {
      const max = 50
      return Math.min((stock / max) * 100, 100)
    },
    showAddModal() {
      console.log('Ouvrir modal d\'ajout')
    },
    editProduct(product) {
      console.log('Modifier produit:', product.name)
    },
    viewProduct(product) {
      console.log('Voir détails:', product.name)
    },
    deleteProduct(product) {
      if (confirm(`Supprimer ${product.name} ?`)) {
        console.log('Supprimer:', product.name)
      }
    }
  }
}
</script>

<style scoped>
/* ==================== CONTAINER ==================== */
.products-content {
  padding: 20px 40px 40px 40px;
  background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
  min-height: 100vh;
}

/* ==================== HEADER ==================== */
.products-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-info h2 {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 4px;
  background: linear-gradient(135deg, #111827 0%, #374151 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-info p {
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
}

.add-product-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.add-product-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.btn-icon {
  font-size: 18px;
  font-weight: bold;
}

/* ==================== QUICK STATS ==================== */
.quick-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.stat-icon.total {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-icon.available {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-icon.low {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-icon.value {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.stat-details {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  line-height: 1;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  margin-top: 4px;
}

/* ==================== TOOLBAR ==================== */
.products-toolbar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-container {
  flex: 1;
  min-width: 300px;
  position: relative;
  display: flex;
  align-items: center;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 12px 16px;
  transition: all 0.3s ease;
}

.search-container:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-icon {
  font-size: 18px;
  margin-right: 12px;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: #111827;
}

.search-input::placeholder {
  color: #9ca3af;
}

.clear-btn {
  width: 24px;
  height: 24px;
  border: none;
  background: #f3f4f6;
  border-radius: 50%;
  color: #6b7280;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: #e5e7eb;
  color: #111827;
}

.filters-container {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-select {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: white;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-select:hover {
  border-color: #3b82f6;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.view-toggle {
  display: flex;
  gap: 4px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  padding: 4px;
}

.view-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #6b7280;
}

.view-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

.view-btn.active {
  background: #3b82f6;
  color: white;
}

/* ==================== PRODUCTS GRID ==================== */
.products-grid {
  display: grid;
  gap: 20px;
  animation: fadeIn 0.5s ease;
}

.products-grid.grid {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

.products-grid.list {
  grid-template-columns: 1fr;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.product-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  border-color: #3b82f6;
}

.product-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.product-image {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: #f3f4f6;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.1);
}

.product-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover .product-overlay {
  opacity: 1;
}

.quick-action {
  width: 40px;
  height: 40px;
  border: none;
  background: white;
  border-radius: 50%;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.quick-action:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.product-info {
  padding: 20px;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 12px;
}

.product-name {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  line-height: 1.3;
  flex: 1;
}

.product-category-badge {
  padding: 4px 10px;
  background: #f3f4f6;
  color: #6b7280;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.price-section {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.product-price {
  font-size: 24px;
  font-weight: 700;
  color: #10b981;
}

.price-unit {
  font-size: 12px;
  color: #9ca3af;
}

.stock-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stock-progress {
  width: 100%;
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.stock-bar {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  transition: width 0.3s ease;
  border-radius: 3px;
}

.stock-bar.medium {
  background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
}

.stock-bar.low {
  background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
}

.stock-text {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.product-actions {
  padding: 16px 20px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn.primary {
  background: #3b82f6;
  color: white;
}

.action-btn.primary:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.action-btn.secondary {
  background: #f3f4f6;
  color: #374151;
}

.action-btn.secondary:hover {
  background: #e5e7eb;
}

.action-btn.danger {
  background: #fee2e2;
  color: #ef4444;
  padding: 10px;
}

.action-btn.danger:hover {
  background: #ef4444;
  color: white;
}

/* ==================== EMPTY STATE ==================== */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  border: 2px dashed #e5e7eb;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
}

.empty-state p {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 24px;
}

/* ==================== LIST VIEW ==================== */
.products-grid.list .product-card {
  display: flex;
  flex-direction: row;
}

.products-grid.list .product-image {
  width: 200px;
  height: auto;
}

.products-grid.list .product-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 24px;
}

.products-grid.list .product-actions {
  border-top: none;
  border-left: 1px solid #e5e7eb;
  flex-direction: column;
  min-width: 140px;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 1024px) {
  .products-content {
    padding: 16px 20px;
  }
  
  .quick-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .products-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .quick-stats {
    grid-template-columns: 1fr;
  }
  
  .products-toolbar {
    flex-direction: column;
  }
  
  .search-container {
    width: 100%;
  }
  
  .filters-container {
    width: 100%;
    flex-wrap: wrap;
  }
  
  .filter-select {
    flex: 1;
  }
  
  .products-grid.grid {
    grid-template-columns: 1fr;
  }
  
  .products-grid.list .product-card {
    flex-direction: column;
  }
  
  .products-grid.list .product-image {
    width: 100%;
    height: 200px;
  }
  
  .products-grid.list .product-actions {
    border-left: none;
    border-top: 1px solid #e5e7eb;
    flex-direction: row;
    min-width: auto;
  }
}
</style>