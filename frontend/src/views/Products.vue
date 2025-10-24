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
            <option v-for="category in uniqueCategories" :key="category" :value="category">
              {{ category }}
            </option>
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
    
    <!-- Message de chargement -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Chargement des produits...</p>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h3>Erreur</h3>
      <p>{{ error }}</p>
      <button class="add-product-btn" @click="loadProducts">
        🔄 Réessayer
      </button>
    </div>

    <!-- Grille de produits -->
    <div v-if="!loading && !error" :class="['products-grid', viewMode]">
      <div v-for="product in sortedProducts" :key="product.id_product" class="product-card">
        <div class="product-badge" v-if="product.est_sous_seuil || product.atteint_seuil">
          <span class="badge-text">Stock faible</span>
        </div>
        <div class="product-badge" v-else-if="product.est_perime" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);">
          <span class="badge-text">Périmé</span>
        </div>
        
        <div class="product-image">
          <img :src="getProductImage(product)" :alt="product.nom" />
          <div class="product-overlay">
            <button class="quick-action" title="Voir détails" @click="viewProduct(product)">👁️</button>
            <button class="quick-action" title="Modifier" @click="editProduct(product)">✏️</button>
          </div>
        </div>
        
        <div class="product-info">
          <div class="product-header">
            <h3 class="product-name">{{ product.nom }}</h3>
            <span class="product-category-badge">{{ product.categorie_nom }}</span>
          </div>
          
          <div class="product-details">
            <div class="price-section">
              <span class="product-price">{{ product.prix_unitaire }} CFA</span>
              <span class="price-unit">Réf: {{ product.reference }}</span>
            </div>
            
            <div class="stock-section">
              <div class="stock-progress">
                <div 
                  class="stock-bar" 
                  :style="{ width: getStockPercentage(product.quantite_en_stock) + '%' }"
                  :class="{ 
                    'low': product.est_sous_seuil, 
                    'medium': product.atteint_seuil && !product.est_sous_seuil 
                  }"
                ></div>
              </div>
              <span class="stock-text">{{ product.quantite_en_stock }} unités (seuil: {{ product.seuil_de_reapprovisionnement }})</span>
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
    <div v-if="!loading && !error && sortedProducts.length === 0" class="empty-state">
      <div class="empty-icon">📦</div>
      <h3>Aucun produit trouvé</h3>
      <p>Essayez de modifier vos filtres ou ajoutez un nouveau produit</p>
      <button class="add-product-btn" @click="showAddModal">
        <span class="btn-icon">+</span>
        Ajouter un produit
      </button>
    </div>

    <!-- Modal Ajout/Édition de produit -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ isEditMode ? 'Modifier le produit' : 'Ajouter un produit' }}</h3>
          <button class="close-btn" @click="closeModal">✕</button>
        </div>
        
        <form @submit.prevent="submitProduct" class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label for="nom">Nom du produit *</label>
              <input 
                type="text" 
                id="nom" 
                v-model="formData.nom" 
                required 
                placeholder="Ex: Savon antiseptique"
              />
            </div>

            <div class="form-group">
              <label for="reference">Référence *</label>
              <input 
                type="text" 
                id="reference" 
                v-model="formData.reference" 
                required 
                placeholder="Ex: PRD-001"
              />
            </div>

            <div class="form-group full-width">
              <label for="designation">Description *</label>
              <textarea 
                id="designation" 
                v-model="formData.designation" 
                required 
                rows="3"
                placeholder="Description du produit"
              ></textarea>
            </div>

            <div class="form-group">
              <label for="prix_unitaire">Prix unitaire (CFA) *</label>
              <input 
                type="number" 
                id="prix_unitaire" 
                v-model="formData.prix_unitaire" 
                required 
                step="0.01"
                min="0"
                placeholder="0.00"
              />
            </div>

            <div class="form-group">
              <label for="quantite_en_stock">Quantité en stock *</label>
              <input 
                type="number" 
                id="quantite_en_stock" 
                v-model="formData.quantite_en_stock" 
                required 
                min="0"
                placeholder="0"
              />
            </div>

            <div class="form-group">
              <label for="seuil_de_reapprovisionnement">Seuil de réappro. *</label>
              <input 
                type="number" 
                id="seuil_de_reapprovisionnement" 
                v-model="formData.seuil_de_reapprovisionnement" 
                required 
                min="0"
                placeholder="0"
              />
            </div>

            <div class="form-group">
              <label for="date_de_peremption">Date de péremption *</label>
              <input 
                type="date" 
                id="date_de_peremption" 
                v-model="formData.date_de_peremption" 
                required 
              />
            </div>

            <div class="form-group">
              <label for="categorie">Catégorie *</label>
              <select 
                id="categorie" 
                v-model="formData.categorie" 
                required
              >
                <option value="">-- Sélectionner une catégorie --</option>
                <option 
                  v-for="cat in categoriesList" 
                  :key="cat.id_categorie" 
                  :value="cat.id_categorie"
                >
                  {{ cat.nom }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="fournisseur">Fournisseur *</label>
              <select 
                id="fournisseur" 
                v-model="formData.fournisseur" 
                required
              >
                <option value="">-- Sélectionner un fournisseur --</option>
                <option 
                  v-for="fourni in fournisseursList" 
                  :key="fourni.id_fournisseur" 
                  :value="fourni.id_fournisseur"
                >
                  {{ fourni.nom }}
                </option>
              </select>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="closeModal">
              Annuler
            </button>
            <button type="submit" class="btn-submit" :disabled="submitting">
              {{ submitting ? 'Enregistrement...' : (isEditMode ? 'Mettre à jour' : 'Ajouter') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Détails du produit -->
    <div v-if="showDetailsModal" class="modal-overlay" @click.self="closeDetailsModal">
      <div class="modal-content details-modal">
        <div class="modal-header">
          <h3>Détails du produit</h3>
          <button class="close-btn" @click="closeDetailsModal">✕</button>
        </div>
        
        <div class="modal-body details-body" v-if="selectedProduct">
          <div class="details-image">
            <img :src="getProductImage(selectedProduct)" :alt="selectedProduct.nom" />
          </div>

          <div class="details-grid">
            <div class="detail-item">
              <span class="detail-label">Nom</span>
              <span class="detail-value">{{ selectedProduct.nom }}</span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Référence</span>
              <span class="detail-value">{{ selectedProduct.reference }}</span>
            </div>

            <div class="detail-item full-width">
              <span class="detail-label">Description</span>
              <span class="detail-value">{{ selectedProduct.designation }}</span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Prix unitaire</span>
              <span class="detail-value price">{{ selectedProduct.prix_unitaire }} CFA</span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Quantité en stock</span>
              <span class="detail-value" :class="{ 'text-danger': selectedProduct.est_sous_seuil }">
                {{ selectedProduct.quantite_en_stock }} unités
              </span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Seuil de réappro.</span>
              <span class="detail-value">{{ selectedProduct.seuil_de_reapprovisionnement }} unités</span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Date de péremption</span>
              <span class="detail-value" :class="{ 'text-danger': selectedProduct.est_perime }">
                {{ formatDate(selectedProduct.date_de_peremption) }}
              </span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Catégorie</span>
              <span class="detail-value badge-cat">{{ selectedProduct.categorie_nom }}</span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Fournisseur</span>
              <span class="detail-value">{{ selectedProduct.fournisseur_nom }}</span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Statut</span>
              <span class="detail-value">
                <span v-if="selectedProduct.est_perime" class="status-badge danger">Périmé</span>
                <span v-else-if="selectedProduct.est_sous_seuil" class="status-badge warning">Stock faible</span>
                <span v-else-if="selectedProduct.atteint_seuil" class="status-badge warning">Seuil atteint</span>
                <span v-else class="status-badge success">Disponible</span>
              </span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Valeur totale</span>
              <span class="detail-value price">
                {{ (parseFloat(selectedProduct.prix_unitaire) * selectedProduct.quantite_en_stock).toFixed(2) }} CFA
              </span>
            </div>
          </div>

          <div class="details-actions">
            <button class="btn-edit" @click="editFromDetails">
              <span>✏️</span> Modifier
            </button>
            <button class="btn-delete" @click="deleteFromDetails">
              <span>🗑️</span> Supprimer
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import produitsAPI from '../services/produits';
import categoriesAPI from '../services/categories';
import fournisseursAPI from '../services/fournisseurs';
import { useDataCache } from '@/composables/useDataCache';

export default {
  name: 'ProductsView',
  setup() {
    const { loadWithCache, invalidateCache } = useDataCache();
    return { loadWithCache, invalidateCache };
  },
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      sortBy: 'name',
      viewMode: 'grid',
      products: [],
      loading: false,
      error: null,
      categories: [],
      showModal: false,
      showDetailsModal: false,
      isEditMode: false,
      submitting: false,
      selectedProduct: null,
      categoriesList: [],
      fournisseursList: [],
      formData: {
        nom: '',
        reference: '',
        designation: '',
        prix_unitaire: '',
        quantite_en_stock: '',
        seuil_de_reapprovisionnement: '',
        date_de_peremption: '',
        categorie: '',
        fournisseur: ''
      }
    }
  },
  mounted() {
    // Charger avec cache si disponible
    this.loadProducts(false);
    this.loadCategories(false);
    this.loadFournisseurs(false);
  },
  computed: {
    filteredProducts() {
      return this.products.filter(product => {
        const matchesSearch = product.nom.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                             product.categorie_nom.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                             product.designation.toLowerCase().includes(this.searchQuery.toLowerCase())
        const matchesCategory = !this.selectedCategory || 
                               product.categorie_nom.toLowerCase() === this.selectedCategory.toLowerCase()
        return matchesSearch && matchesCategory
      })
    },
    sortedProducts() {
      const filtered = [...this.filteredProducts]
      return filtered.sort((a, b) => {
        switch(this.sortBy) {
          case 'price':
            return parseFloat(a.prix_unitaire) - parseFloat(b.prix_unitaire)
          case 'stock':
            return b.quantite_en_stock - a.quantite_en_stock
          default:
            return a.nom.localeCompare(b.nom)
        }
      })
    },
    availableProducts() {
      return this.products.filter(p => p.quantite_en_stock > p.seuil_de_reapprovisionnement).length
    },
    lowStockProducts() {
      return this.products.filter(p => p.est_sous_seuil || p.atteint_seuil).length
    },
    totalValue() {
      return this.products.reduce((sum, p) => sum + (parseFloat(p.prix_unitaire) * p.quantite_en_stock), 0).toFixed(2)
    },
    uniqueCategories() {
      const categoriesSet = new Set(this.products.map(p => p.categorie_nom));
      return Array.from(categoriesSet).sort();
    }
  },
  methods: {
    // === MÉTHODE PUBLIQUE POUR REFRESH DEPUIS APP.VUE ===
    async refreshData() {
      console.log('🔄 Rafraîchissement forcé des Produits...');
      this.invalidateCache('produits');
      this.invalidateCache('categories');
      this.invalidateCache('fournisseurs');
      await Promise.all([
        this.loadProducts(true),
        this.loadCategories(true),
        this.loadFournisseurs(true)
      ]);
      this.showNotification('success', '✅ Données actualisées');
    },
    
    async loadProducts(forceRefresh = false) {
      // Ne montrer le loading QUE si on force le refresh ou si pas de données
      const showLoading = forceRefresh || !this.products.length;
      
      if (showLoading) {
        this.loading = true;
      }
      this.error = null;
      
      try {
        this.products = await this.loadWithCache('produits', async () => {
          const response = await produitsAPI.getAllProduits();
          console.log('📦 Produits chargés depuis l\'API:', response.data.length);
          return response.data;
        }, forceRefresh);
      } catch (error) {
        console.error('Erreur lors du chargement des produits:', error);
        this.error = 'Impossible de charger les produits. Veuillez réessayer.';
        this.products = [];
      } finally {
        if (showLoading) {
          this.loading = false;
        }
      }
    },
    async loadCategories(forceRefresh = false) {
      try {
        this.categoriesList = await this.loadWithCache('categories', async () => {
          const response = await categoriesAPI.getAllCategories();
          console.log('📦 Catégories chargées depuis l\'API:', response.data.length);
          return response.data;
        }, forceRefresh);
      } catch (error) {
        console.error('Erreur lors du chargement des catégories:', error);
      }
    },
    async loadFournisseurs(forceRefresh = false) {
      try {
        this.fournisseursList = await this.loadWithCache('fournisseurs', async () => {
          const response = await fournisseursAPI.getAllFournisseurs();
          console.log('📦 Fournisseurs chargés depuis l\'API:', response.data.length);
          return response.data;
        }, forceRefresh);
      } catch (error) {
        console.error('Erreur lors du chargement des fournisseurs:', error);
      }
    },
    getStockPercentage(stock) {
      const max = 100;
      return Math.min((stock / max) * 100, 100);
    },
    showAddModal() {
      this.isEditMode = false;
      this.resetForm();
      this.showModal = true;
    },
    async editProduct(product) {
      this.isEditMode = true;
      this.selectedProduct = product;
      this.formData = {
        nom: product.nom,
        reference: product.reference,
        designation: product.designation,
        prix_unitaire: product.prix_unitaire,
        quantite_en_stock: product.quantite_en_stock,
        seuil_de_reapprovisionnement: product.seuil_de_reapprovisionnement,
        date_de_peremption: product.date_de_peremption,
        categorie: product.categorie,
        fournisseur: product.fournisseur
      };
      this.showModal = true;
    },
    viewProduct(product) {
      this.selectedProduct = product;
      this.showDetailsModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.resetForm();
    },
    closeDetailsModal() {
      this.showDetailsModal = false;
      this.selectedProduct = null;
    },
    resetForm() {
      this.formData = {
        nom: '',
        reference: '',
        designation: '',
        prix_unitaire: '',
        quantite_en_stock: '',
        seuil_de_reapprovisionnement: '',
        date_de_peremption: '',
        categorie: '',
        fournisseur: ''
      };
      this.selectedProduct = null;
    },
    async submitProduct() {
      this.submitting = true;
      try {
        if (this.isEditMode) {
          await produitsAPI.updateProduit(this.selectedProduct.id_product, this.formData);
          this.showNotification('success', `Le produit "${this.formData.nom}" a été mis à jour avec succès.`);
        } else {
          await produitsAPI.createProduit(this.formData);
          this.showNotification('success', `Le produit "${this.formData.nom}" a été ajouté avec succès.`);
        }
        this.closeModal();
        
        // Invalider le cache et recharger
        this.invalidateCache('produits');
        await this.loadProducts(true);
      } catch (error) {
        console.error('Erreur lors de la soumission:', error);
        const message = this.isEditMode 
          ? 'Impossible de mettre à jour le produit.' 
          : 'Impossible d\'ajouter le produit.';
        this.showNotification('error', message);
      } finally {
        this.submitting = false;
      }
    },
    async deleteProduct(product) {
      if (confirm(`Êtes-vous sûr de vouloir supprimer "${product.nom}" ?`)) {
        try {
          await produitsAPI.deleteProduit(product.id_product);
          this.showNotification('success', `Le produit "${product.nom}" a été supprimé avec succès.`);
          
          // Invalider le cache et recharger
          this.invalidateCache('produits');
          await this.loadProducts(true);
        } catch (error) {
          console.error('Erreur lors de la suppression:', error);
          this.showNotification('error', 'Impossible de supprimer le produit. Veuillez réessayer.');
        }
      }
    },
    editFromDetails() {
      this.closeDetailsModal();
      this.editProduct(this.selectedProduct);
    },
    async deleteFromDetails() {
      const product = this.selectedProduct;
      this.closeDetailsModal();
      await this.deleteProduct(product);
    },
    showNotification(type, message) {
      // Émet un événement pour afficher une notification
      this.$emit('show-notification', { type, message });
      // Alternative: afficher une alerte simple
      if (type === 'error') {
        alert('❌ ' + message);
      } else {
        alert('✅ ' + message);
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('fr-FR', options);
    },
    getProductImage(product) {
      // Image par défaut basée sur la catégorie
      const categoryImages = {
        'BOISSON': 'https://images.unsplash.com/photo-1437418747212-8d9709afab22?w=300&h=300&fit=crop',
        'FRUITS': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300&h=300&fit=crop',
        'LÉGUMES': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=300&h=300&fit=crop',
        'PRODUITS LAITIERS': 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300&h=300&fit=crop',
        'VIANDES': 'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=300&h=300&fit=crop',
        'POISSONS': 'https://images.unsplash.com/photo-1535140728325-a4d3707eee61?w=300&h=300&fit=crop',
        'ÉPICERIE': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop',
        'HYGIÈNE': 'https://images.unsplash.com/photo-1556228578-dd165a1d5b31?w=300&h=300&fit=crop'
      };
      return categoryImages[product.categorie_nom.toUpperCase()] || 'https://images.unsplash.com/photo-1523294587484-bae6cc870010?w=300&h=300&fit=crop';
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

/* ==================== LOADING STATE ==================== */
.loading-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

/* ==================== ERROR STATE ==================== */
.error-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  border: 2px solid #fee2e2;
}

.error-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.7;
}

.error-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #ef4444;
  margin-bottom: 8px;
}

.error-state p {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 24px;
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

  .modal-content {
    width: 95%;
    max-height: 95vh;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .details-modal {
    width: 95%;
  }
}

/* ==================== MODAL STYLES ==================== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  font-size: 22px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.close-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: #f3f4f6;
  border-radius: 8px;
  color: #6b7280;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: #e5e7eb;
  color: #111827;
}

.modal-body {
  padding: 24px;
  max-height: calc(90vh - 180px);
  overflow-y: auto;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  color: #111827;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.btn-cancel,
.btn-submit {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel {
  background: #f3f4f6;
  color: #374151;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-submit {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ==================== DETAILS MODAL ==================== */
.details-modal {
  max-width: 700px;
}

.details-body {
  padding: 24px;
}

.details-image {
  width: 100%;
  height: 250px;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 24px;
  background: #f3f4f6;
}

.details-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-label {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 15px;
  font-weight: 500;
  color: #111827;
}

.detail-value.price {
  font-size: 18px;
  font-weight: 700;
  color: #10b981;
}

.detail-value.text-danger {
  color: #ef4444;
  font-weight: 600;
}

.badge-cat {
  display: inline-block;
  padding: 6px 12px;
  background: #f3f4f6;
  color: #6b7280;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  width: fit-content;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  width: fit-content;
}

.status-badge.success {
  background: #d1fae5;
  color: #059669;
}

.status-badge.warning {
  background: #fed7aa;
  color: #d97706;
}

.status-badge.danger {
  background: #fee2e2;
  color: #dc2626;
}

.details-actions {
  display: flex;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.btn-edit,
.btn-delete {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit {
  background: #3b82f6;
  color: white;
}

.btn-edit:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-delete {
  background: #fee2e2;
  color: #ef4444;
}

.btn-delete:hover {
  background: #ef4444;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}
</style>