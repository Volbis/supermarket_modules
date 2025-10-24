<template>
  <div class="suppliers-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <p class="page-subtitle">{{ filteredSuppliers.length }} fournisseurs</p>
        </div>
        <button class="btn-add" @click="showAddModal">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          <span>Nouveau fournisseur</span>
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-container">
      <div class="stat-card">
        <div class="stat-icon" style="background: #EEF2FF;">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4F46E5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Total</p>
          <p class="stat-value">{{ suppliers.length }}</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #ECFDF5;">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Produits fournis</p>
          <p class="stat-value">{{ totalProduits }}</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #FFF7ED;">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#EA580C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Commandes</p>
          <p class="stat-value">{{ totalOrders }}</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #FEF2F2;">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 8v4M12 16h.01"></path>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Délai moyen</p>
          <p class="stat-value">{{ averageDelay }} j</p>
        </div>
      </div>
    </div>

    <!-- Filters & Search -->
    <div class="controls-container">
      <div class="search-box">
        <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <path d="m21 21-4.35-4.35"></path>
        </svg>
        <input 
          type="text" 
          placeholder="Rechercher un fournisseur..." 
          v-model="searchQuery"
          class="search-input"
        >
        <button v-if="searchQuery" @click="searchQuery = ''" class="clear-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <div class="filters">
        <select v-model="sortBy" class="filter-select">
          <option value="name">Nom (A-Z)</option>
          <option value="orders">Commandes</option>
          <option value="delay">Délai de livraison</option>
        </select>

        <div class="view-toggle">
          <button 
            :class="['toggle-btn', { active: viewMode === 'grid' }]"
            @click="viewMode = 'grid'"
            title="Vue grille"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
          </button>
          <button 
            :class="['toggle-btn', { active: viewMode === 'list' }]"
            @click="viewMode = 'list'"
            title="Vue liste"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="8" y1="6" x2="21" y2="6"></line>
              <line x1="8" y1="12" x2="21" y2="12"></line>
              <line x1="8" y1="18" x2="21" y2="18"></line>
              <line x1="3" y1="6" x2="3.01" y2="6"></line>
              <line x1="3" y1="12" x2="3.01" y2="12"></line>
              <line x1="3" y1="18" x2="3.01" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Message de chargement -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Chargement des fournisseurs...</p>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h3>Erreur</h3>
      <p>{{ error }}</p>
      <button class="btn-add" @click="loadSuppliers">
        🔄 Réessayer
      </button>
    </div>

    <!-- Suppliers Grid -->
    <div v-if="!loading && !error && sortedSuppliers.length > 0" :class="['suppliers-grid', viewMode]">
      <div v-for="supplier in sortedSuppliers" :key="supplier.id_fournisseur" class="supplier-card">
        <div class="card-header">
          <div class="avatar" :style="{ background: getSupplierColor(supplier.nom) }">
            {{ getInitials(supplier.nom) }}
          </div>
          <div class="header-info">
            <h3 class="supplier-name">{{ supplier.nom }}</h3>
            <div class="rating">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="#FBBF24" stroke="none">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
              <span class="rating-value">{{ supplier.produits_count || 0 }} produits</span>
            </div>
          </div>
          <span class="badge active">
            {{ supplier.delais_livraison_jours }}j
          </span>
        </div>

        <div class="card-body">
          <div class="info-row">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
            </svg>
            <span>{{ supplier.contact }}</span>
          </div>

          <div class="info-row">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
            <span>{{ supplier.adresse }}</span>
          </div>

          <div class="info-row">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            </svg>
            <span>{{ supplier.commandes_count || 0 }} commandes</span>
          </div>

          <div class="info-row">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <span>Délai: {{ supplier.delais_livraison_jours }} jour(s)</span>
          </div>
        </div>

        <div class="tags" v-if="supplier.categories_produits && supplier.categories_produits.length > 0">
          <span v-for="(category, index) in supplier.categories_produits" :key="index" class="tag">
            {{ category }}
          </span>
        </div>

        <div class="card-actions">
          <button class="action-btn edit" @click="editSupplier(supplier)" title="Modifier">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
            </svg>
          </button>
          <button class="action-btn contact" @click="contactSupplier(supplier)" title="Contacter">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
          </button>
          <button class="action-btn view" @click="viewSupplier(supplier)" title="Voir détails">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
          </button>
          <button class="action-btn delete" @click="deleteSupplier(supplier)" title="Supprimer">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && !error && sortedSuppliers.length === 0" class="empty-state">
      <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
      <h3>Aucun fournisseur trouvé</h3>
      <p>Modifiez vos critères de recherche ou ajoutez un nouveau fournisseur</p>
      <button class="btn-add" @click="showAddModal">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        <span>Ajouter un fournisseur</span>
      </button>
    </div>

    <!-- Modal Ajout/Édition de fournisseur -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ isEditMode ? 'Modifier le fournisseur' : 'Ajouter un fournisseur' }}</h3>
          <button class="close-btn" @click="closeModal">✕</button>
        </div>
        
        <form @submit.prevent="submitSupplier" class="modal-body">
          <div class="form-grid">
            <div class="form-group full-width">
              <label for="nom">Nom du fournisseur *</label>
              <input 
                type="text" 
                id="nom" 
                v-model="formData.nom" 
                required 
                placeholder="Ex: Ferme Bio Martin"
              />
            </div>

            <div class="form-group full-width">
              <label for="contact">Contact *</label>
              <input 
                type="text" 
                id="contact" 
                v-model="formData.contact" 
                required 
                placeholder="Ex: +225 01 23 45 67 89 ou email@exemple.com"
              />
            </div>

            <div class="form-group full-width">
              <label for="adresse">Adresse *</label>
              <textarea 
                id="adresse" 
                v-model="formData.adresse" 
                required 
                rows="3"
                placeholder="Adresse complète du fournisseur"
              ></textarea>
            </div>

            <div class="form-group full-width">
              <label for="delais_livraison_jours">Délai de livraison (jours) *</label>
              <input 
                type="number" 
                id="delais_livraison_jours" 
                v-model="formData.delais_livraison_jours" 
                required 
                min="0"
                placeholder="Ex: 3"
              />
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

    <!-- Modal Détails du fournisseur -->
    <div v-if="showDetailsModal" class="modal-overlay" @click.self="closeDetailsModal">
      <div class="modal-content details-modal">
        <div class="modal-header">
          <h3>Détails du fournisseur</h3>
          <button class="close-btn" @click="closeDetailsModal">✕</button>
        </div>
        
        <div class="modal-body details-body" v-if="selectedSupplier">
          <div class="supplier-header-detail">
            <div class="avatar-large" :style="{ background: getSupplierColor(selectedSupplier.nom) }">
              {{ getInitials(selectedSupplier.nom) }}
            </div>
            <div>
              <h2>{{ selectedSupplier.nom }}</h2>
              <p class="supplier-subtitle">{{ selectedSupplier.produits_count || 0 }} produits • {{ selectedSupplier.commandes_count || 0 }} commandes</p>
            </div>
          </div>

          <div class="details-grid">
            <div class="detail-item">
              <span class="detail-label">Contact</span>
              <span class="detail-value">{{ selectedSupplier.contact }}</span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Délai de livraison</span>
              <span class="detail-value">{{ selectedSupplier.delais_livraison_jours }} jour(s)</span>
            </div>

            <div class="detail-item full-width">
              <span class="detail-label">Adresse</span>
              <span class="detail-value">{{ selectedSupplier.adresse }}</span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Produits fournis</span>
              <span class="detail-value">{{ selectedSupplier.produits_count || 0 }} produit(s)</span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Commandes passées</span>
              <span class="detail-value">{{ selectedSupplier.commandes_count || 0 }} commande(s)</span>
            </div>

            <div class="detail-item full-width" v-if="selectedSupplier.categories_produits && selectedSupplier.categories_produits.length > 0">
              <span class="detail-label">Catégories de produits</span>
              <div class="categories-list">
                <span v-for="(cat, index) in selectedSupplier.categories_produits" :key="index" class="category-badge">
                  {{ cat }}
                </span>
              </div>
            </div>
          </div>

          <div v-if="supplierProducts.length > 0" class="products-section">
            <h4>Produits fournis</h4>
            <div class="products-list">
              <div v-for="product in supplierProducts.slice(0, 5)" :key="product.id_product" class="product-item">
                <span class="product-name">{{ product.nom }}</span>
                <span class="product-price">{{ product.prix_unitaire }} CFA</span>
              </div>
              <p v-if="supplierProducts.length > 5" class="more-products">
                +{{ supplierProducts.length - 5 }} autres produits
              </p>
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
import fournisseursAPI from '../services/fournisseurs';
import produitsAPI from '../services/produits';
import commandesAPI from '../services/commandes';
import { useDataCache } from '@/composables/useDataCache';

export default {
  name: 'FournisseursView',
  setup() {
    const { loadWithCache, invalidateCache } = useDataCache();
    return { loadWithCache, invalidateCache };
  },
  data() {
    return {
      searchQuery: '',
      sortBy: 'name',
      viewMode: 'grid',
      suppliers: [],
      loading: false,
      error: null,
      showModal: false,
      showDetailsModal: false,
      isEditMode: false,
      submitting: false,
      selectedSupplier: null,
      supplierProducts: [],
      supplierCommandes: [],
      formData: {
        nom: '',
        contact: '',
        adresse: '',
        delais_livraison_jours: ''
      }
    }
  },
  mounted() {
    // Charger avec cache si disponible
    this.loadSuppliers(false);
  },
  computed: {
    filteredSuppliers() {
      return this.suppliers.filter(supplier => {
        const matchesSearch = supplier.nom.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                             supplier.contact.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                             supplier.adresse.toLowerCase().includes(this.searchQuery.toLowerCase())
        return matchesSearch
      })
    },
    sortedSuppliers() {
      const filtered = [...this.filteredSuppliers]
      return filtered.sort((a, b) => {
        switch(this.sortBy) {
          case 'orders':
            return (b.commandes_count || 0) - (a.commandes_count || 0)
          case 'delay':
            return a.delais_livraison_jours - b.delais_livraison_jours
          default:
            return a.nom.localeCompare(b.nom)
        }
      })
    },
    totalProduits() {
      return this.suppliers.reduce((sum, s) => sum + (s.produits_count || 0), 0)
    },
    totalOrders() {
      return this.suppliers.reduce((sum, s) => sum + (s.commandes_count || 0), 0)
    },
    averageDelay() {
      if (this.suppliers.length === 0) return 0
      const total = this.suppliers.reduce((sum, s) => sum + s.delais_livraison_jours, 0)
      return Math.round(total / this.suppliers.length)
    }
  },
  methods: {
    // === MÉTHODE PUBLIQUE POUR REFRESH DEPUIS APP.VUE ===
    async refreshData() {
      console.log('🔄 Rafraîchissement forcé des Fournisseurs...');
      this.invalidateCache('fournisseurs');
      this.invalidateCache('produits');
      this.invalidateCache('commandes');
      await this.loadSuppliers(true);
      this.showNotification('success', '✅ Fournisseurs actualisés');
    },
    
    async loadSuppliers(forceRefresh = false) {
      // Ne montrer le loading QUE si on force le refresh ou si pas de données
      const showLoading = forceRefresh || !this.suppliers.length;
      
      if (showLoading) {
        this.loading = true;
      }
      this.error = null;
      
      try {
        this.suppliers = await this.loadWithCache('fournisseurs', async () => {
          const response = await fournisseursAPI.getAllFournisseurs();
          console.log('📦 Fournisseurs chargés depuis l\'API:', response.data.length);
          return response.data;
        }, forceRefresh);
        
        // Charger les produits et commandes pour chaque fournisseur
        await this.loadSuppliersData(forceRefresh);
      } catch (error) {
        console.error('Erreur lors du chargement des fournisseurs:', error);
        this.error = 'Impossible de charger les fournisseurs. Veuillez réessayer.';
        this.suppliers = [];
      } finally {
        if (showLoading) {
          this.loading = false;
        }
      }
    },
    async loadSuppliersData(forceRefresh = false) {
      try {
        // Charger tous les produits avec cache
        const produits = await this.loadWithCache('produits', async () => {
          const response = await produitsAPI.getAllProduits();
          console.log('📦 Produits chargés pour fournisseurs:', response.data.length);
          return response.data;
        }, forceRefresh);
        
        // Charger toutes les commandes avec cache
        const commandes = await this.loadWithCache('commandes', async () => {
          const response = await commandesAPI.getAllCommandes();
          console.log('📦 Commandes chargées pour fournisseurs:', response.data.length);
          return response.data;
        }, forceRefresh);
        
        // Compter les produits et commandes par fournisseur
        this.suppliers = this.suppliers.map(supplier => {
          const supplierProduits = produits.filter(p => p.fournisseur === supplier.id_fournisseur);
          const supplierCommandes = commandes.filter(c => c.fournisseur === supplier.id_fournisseur);
          
          // Extraire les catégories uniques des produits du fournisseur
          const categories = [...new Set(supplierProduits.map(p => p.categorie_nom))];
          
          return {
            ...supplier,
            produits_count: supplierProduits.length,
            commandes_count: supplierCommandes.length,
            categories_produits: categories
          };
        });
      } catch (error) {
        console.error('Erreur lors du chargement des données supplémentaires:', error);
      }
    },
    getInitials(name) {
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    },
    getSupplierColor(name) {
      const colors = [
        '#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', 
        '#ec4899', '#06b6d4', '#84cc16', '#f97316', '#6366f1'
      ];
      const index = name.length % colors.length;
      return colors[index];
    },
    showAddModal() {
      this.isEditMode = false;
      this.resetForm();
      this.showModal = true;
    },
    async editSupplier(supplier) {
      this.isEditMode = true;
      this.selectedSupplier = supplier;
      this.formData = {
        nom: supplier.nom,
        contact: supplier.contact,
        adresse: supplier.adresse,
        delais_livraison_jours: supplier.delais_livraison_jours
      };
      this.showModal = true;
    },
    contactSupplier(supplier) {
      console.log('Contacter fournisseur:', supplier.nom);
      alert(`Contacter ${supplier.nom} au ${supplier.contact}`);
    },
    async viewSupplier(supplier) {
      this.selectedSupplier = supplier;
      
      // Charger les produits et commandes du fournisseur
      try {
        const produitsResponse = await fournisseursAPI.getFournisseurProduits(supplier.id_fournisseur);
        this.supplierProducts = produitsResponse.data;
      } catch (error) {
        console.error('Erreur lors du chargement des produits:', error);
        this.supplierProducts = [];
      }
      
      this.showDetailsModal = true;
    },
    async deleteSupplier(supplier) {
      if (confirm(`Êtes-vous sûr de vouloir supprimer "${supplier.nom}" ?\n\nAttention: Cette action supprimera également tous les produits associés à ce fournisseur.`)) {
        try {
          await fournisseursAPI.deleteFournisseur(supplier.id_fournisseur);
          this.showNotification('success', `Le fournisseur "${supplier.nom}" a été supprimé avec succès.`);
          
          // Invalider le cache et recharger
          this.invalidateCache('fournisseurs');
          await this.loadSuppliers(true);
        } catch (error) {
          console.error('Erreur lors de la suppression:', error);
          this.showNotification('error', 'Impossible de supprimer le fournisseur. Veuillez réessayer.');
        }
      }
    },
    closeModal() {
      this.showModal = false;
      this.resetForm();
    },
    closeDetailsModal() {
      this.showDetailsModal = false;
      this.selectedSupplier = null;
      this.supplierProducts = [];
    },
    resetForm() {
      this.formData = {
        nom: '',
        contact: '',
        adresse: '',
        delais_livraison_jours: ''
      };
      this.selectedSupplier = null;
    },
    async submitSupplier() {
      this.submitting = true;
      try {
        if (this.isEditMode) {
          await fournisseursAPI.updateFournisseur(this.selectedSupplier.id_fournisseur, this.formData);
          this.showNotification('success', `Le fournisseur "${this.formData.nom}" a été mis à jour avec succès.`);
        } else {
          await fournisseursAPI.createFournisseur(this.formData);
          this.showNotification('success', `Le fournisseur "${this.formData.nom}" a été ajouté avec succès.`);
        }
        this.closeModal();
        
        // Invalider le cache et recharger
        this.invalidateCache('fournisseurs');
        await this.loadSuppliers(true);
      } catch (error) {
        console.error('Erreur lors de la soumission:', error);
        const message = this.isEditMode 
          ? 'Impossible de mettre à jour le fournisseur.' 
          : 'Impossible d\'ajouter le fournisseur.';
        this.showNotification('error', message);
      } finally {
        this.submitting = false;
      }
    },
    editFromDetails() {
      this.closeDetailsModal();
      this.editSupplier(this.selectedSupplier);
    },
    async deleteFromDetails() {
      const supplier = this.selectedSupplier;
      this.closeDetailsModal();
      await this.deleteSupplier(supplier);
    },
    showNotification(type, message) {
      if (type === 'error') {
        alert('❌ ' + message);
      } else {
        alert('✅ ' + message);
      }
    }
  }
}
</script>


<style scoped>
.suppliers-page {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  background: #f9fafb;
  min-height: 100vh;
}

/* Header */
.page-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.title-section {
  flex: 1;
  min-width: 250px;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.025em;
}

.page-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-add:hover {
  background: #4338ca;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.btn-add svg {
  flex-shrink: 0;
}

/* Stats */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: #d1d5db;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.625rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-label {
  display: block;
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.stat-value {
  display: block;
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  line-height: 1;
}

/* Controls */
.controls-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 280px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  background: white;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.clear-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: #f3f4f6;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: #e5e7eb;
  color: #374151;
}

.filters {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  background: white;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 140px;
}

.filter-select:hover {
  border-color: #d1d5db;
}

.filter-select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.view-toggle {
  display: flex;
  gap: 0.25rem;
  background: white;
  padding: 0.25rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.toggle-btn {
  padding: 0.5rem;
  background: transparent;
  border: none;
  border-radius: 0.375rem;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.toggle-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.toggle-btn.active {
  background: #4f46e5;
  color: white;
}

/* Grid */
.suppliers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.25rem;
}

.suppliers-grid.list {
  grid-template-columns: 1fr;
}

.supplier-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.supplier-card:hover {
  border-color: #d1d5db;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.avatar {
  width: 52px;
  height: 52px;
  border-radius: 0.625rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  font-weight: 600;
  color: white;
  flex-shrink: 0;
  letter-spacing: -0.025em;
}

.header-info {
  flex: 1;
  min-width: 0;
}

.supplier-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.375rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.rating svg {
  flex-shrink: 0;
}

.rating-value {
  font-size: 0.8125rem;
  color: #6b7280;
  font-weight: 500;
}

.badge {
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.badge.active {
  background: #d1fae5;
  color: #065f46;
}

.badge.inactive {
  background: #fee2e2;
  color: #991b1b;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #f3f4f6;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.info-row svg {
  flex-shrink: 0;
  color: #9ca3af;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.tag {
  padding: 0.375rem 0.75rem;
  background: #f3f4f6;
  color: #374151;
  border-radius: 0.375rem;
  font-size: 0.8125rem;
  font-weight: 500;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  padding: 0.625rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.action-btn.edit:hover {
  background: #eef2ff;
  border-color: #c7d2fe;
  color: #4f46e5;
}

.action-btn.edit:hover svg {
  stroke: #4f46e5;
}

.action-btn.contact:hover {
  background: #ecfdf5;
  border-color: #a7f3d0;
  color: #059669;
}

.action-btn.contact:hover svg {
  stroke: #059669;
}

.action-btn.view:hover {
  background: #fef3c7;
  border-color: #fde68a;
  color: #d97706;
}

.action-btn.view:hover svg {
  stroke: #d97706;
}

.action-btn.delete {
  background: #fee2e2;
  border-color: #fecaca;
}

.action-btn.delete:hover {
  background: #fecaca;
  border-color: #fca5a5;
  color: #dc2626;
}

.action-btn.delete:hover svg {
  stroke: #dc2626;
}

/* List View */
.suppliers-grid.list .supplier-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.25rem 1.5rem;
}

.suppliers-grid.list .card-header {
  margin-bottom: 0;
  flex: 0 0 auto;
}

.suppliers-grid.list .card-body {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
  flex: 1;
}

.suppliers-grid.list .tags {
  margin-bottom: 0;
  flex: 0 0 auto;
}

.suppliers-grid.list .card-actions {
  flex: 0 0 auto;
}

/* Empty State */
.empty-state {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 4rem 2rem;
  text-align: center;
}

.empty-state svg {
  color: #d1d5db;
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0 0 1.5rem 0;
}

/* Responsive */
@media (max-width: 768px) {
  .suppliers-page {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .header-content {
    flex-direction: column;
    align-items: stretch;
  }

  .btn-add {
    width: 100%;
    justify-content: center;
  }

  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .controls-container {
    flex-direction: column;
  }

  .search-box {
    min-width: 100%;
  }

  .filters {
    width: 100%;
    justify-content: space-between;
  }

  .filter-select {
    flex: 1;
    min-width: 0;
  }

  .suppliers-grid {
    grid-template-columns: 1fr;
  }

  .suppliers-grid.list .supplier-card {
    flex-direction: column;
    align-items: stretch;
  }

  .suppliers-grid.list .card-header {
    margin-bottom: 1.25rem;
  }

  .suppliers-grid.list .card-body {
    grid-template-columns: 1fr;
    margin-bottom: 1.25rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid #f3f4f6;
  }

  .suppliers-grid.list .tags {
    margin-bottom: 1.25rem;
  }
}

/* ==================== LOADING & ERROR STATES ==================== */
.loading-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #4f46e5;
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

.error-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 12px;
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
  max-width: 600px;
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

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
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
  font-size: 20px;
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
.form-group textarea {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  color: #111827;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
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
  background: #4f46e5;
  color: white;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.btn-submit:hover:not(:disabled) {
  background: #4338ca;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
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

.supplier-header-detail {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.avatar-large {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 600;
  color: white;
  flex-shrink: 0;
}

.supplier-header-detail h2 {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 4px 0;
}

.supplier-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
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

.categories-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-badge {
  padding: 6px 12px;
  background: #f3f4f6;
  color: #374151;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.products-section {
  margin-bottom: 24px;
  padding: 20px;
  background: #f9fafb;
  border-radius: 12px;
}

.products-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 16px 0;
}

.products-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.product-name {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

.product-price {
  font-size: 14px;
  color: #10b981;
  font-weight: 600;
}

.more-products {
  font-size: 13px;
  color: #6b7280;
  text-align: center;
  margin: 8px 0 0 0;
  font-style: italic;
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
  background: #4f46e5;
  color: white;
}

.btn-edit:hover {
  background: #4338ca;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
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

@media (max-width: 480px) {
  .stats-container {
    grid-template-columns: 1fr;
  }

  .card-header {
    flex-wrap: wrap;
  }

  .badge {
    width: 100%;
    text-align: center;
  }
}
</style>
