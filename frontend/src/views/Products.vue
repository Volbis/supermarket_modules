<template>
  <div class="products-content">
    <div class="products-header">
      <h2>Gestion des produits</h2>
      <p>Gérez votre inventaire de produits</p>
      <button class="add-product-btn">+ Ajouter un produit</button>
    </div>
    
    <div class="products-filters">
      <div class="search-box">
        <input type="text" placeholder="Rechercher un produit..." v-model="searchQuery">
      </div>
      <div class="filter-group">
        <label>Catégorie :</label>
        <select v-model="selectedCategory">
          <option value="">Toutes</option>
          <option value="fruits">Fruits</option>
          <option value="vegetables">Légumes</option>
          <option value="dairy">Produits laitiers</option>
        </select>
      </div>
    </div>
    
    <div class="products-grid">
      <div v-for="product in filteredProducts" :key="product.id" class="product-card">
        <div class="product-image">
          <img :src="product.image" :alt="product.name" />
        </div>
        <div class="product-info">
          <h3>{{ product.name }}</h3>
          <p class="product-category">{{ product.category }}</p>
          <p class="product-price">{{ product.price }}</p>
          <div class="product-stock">
            <span :class="['stock-badge', product.stock > 10 ? 'in-stock' : 'low-stock']">
              {{ product.stock }} en stock
            </span>
          </div>
        </div>
        <div class="product-actions">
          <button class="action-btn edit">Modifier</button>
          <button class="action-btn delete">Supprimer</button>
        </div>
      </div>
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
      products: [
        {
          id: 1,
          name: 'Pommes',
          category: 'Fruits',
          price: '€2.50/kg',
          stock: 45,
          image: 'https://via.placeholder.com/150x150?text=Pommes'
        },
        {
          id: 2,
          name: 'Bananes',
          category: 'Fruits',
          price: '€1.80/kg',
          stock: 8,
          image: 'https://via.placeholder.com/150x150?text=Bananes'
        },
        {
          id: 3,
          name: 'Carottes',
          category: 'Légumes',
          price: '€1.20/kg',
          stock: 32,
          image: 'https://via.placeholder.com/150x150?text=Carottes'
        },
        {
          id: 4,
          name: 'Lait',
          category: 'Produits laitiers',
          price: '€1.50/litre',
          stock: 5,
          image: 'https://via.placeholder.com/150x150?text=Lait'
        }
      ]
    }
  },
  computed: {
    filteredProducts() {
      return this.products.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        const matchesCategory = !this.selectedCategory || product.category.toLowerCase() === this.selectedCategory.toLowerCase()
        return matchesSearch && matchesCategory
      })
    }
  }
}
</script>

<style scoped>
.products-content {
  padding: 20px;
}

.products-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.products-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.products-header p {
  color: #6b7280;
  font-size: 16px;
}

.add-product-btn {
  padding: 12px 24px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
}

.add-product-btn:hover {
  background: #059669;
}

.products-filters {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #e5e7eb;
}

.search-box {
  flex: 1;
}

.search-box input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-weight: 500;
  color: #374151;
}

.filter-group select {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: white;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.product-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #e5e7eb;
  overflow: hidden;
  transition: transform 0.2s;
}

.product-card:hover {
  transform: translateY(-2px);
}

.product-image {
  height: 150px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  padding: 16px;
}

.product-info h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.product-category {
  color: #6b7280;
  font-size: 14px;
  margin-bottom: 8px;
}

.product-price {
  font-size: 20px;
  font-weight: 700;
  color: #059669;
  margin-bottom: 12px;
}

.stock-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.stock-badge.in-stock {
  background: #d1fae5;
  color: #065f46;
}

.stock-badge.low-stock {
  background: #fef3c7;
  color: #92400e;
}

.product-actions {
  padding: 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.action-btn.edit {
  background: #3b82f6;
  color: white;
}

.action-btn.delete {
  background: #ef4444;
  color: white;
}

.action-btn:hover {
  opacity: 0.8;
}
</style>