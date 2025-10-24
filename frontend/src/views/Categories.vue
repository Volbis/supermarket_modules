<template>
  <div class="categories-content">
    <!-- Header -->
    <div class="categories-header">
      <div class="header-info">
        <h2>Gestion des catégories</h2>
        <p>{{ categories.length }} catégorie(s) disponible(s)</p>
      </div>
      <button class="add-category-btn" @click="showAddModal">
        <span class="btn-icon">+</span>
        Ajouter une catégorie
      </button>
    </div>

    <!-- Message de chargement -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Chargement des catégories...</p>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h3>Erreur de chargement</h3>
      <p>{{ error }}</p>
      <button @click="fetchCategories" class="retry-btn">Réessayer</button>
    </div>

    <!-- Grille des catégories -->
    <div v-if="!loading && !error" class="categories-grid">
      <div 
        v-for="category in categories" 
        :key="category.id_categorie" 
        class="category-card"
      >
        <div class="category-icon">📦</div>
        <div class="category-info">
          <h3 class="category-name">{{ category.nom }}</h3>
          <p class="category-description">{{ category.description }}</p>
          <div class="category-id">
            <span class="id-label">ID:</span>
            <span class="id-value">{{ formatId(category.id_categorie) }}</span>
          </div>
        </div>
        <div class="category-actions">
          <button 
            class="action-btn view" 
            @click="viewCategoryProducts(category)"
            title="Voir les produits"
          >
            👁️
          </button>
          <button 
            class="action-btn edit" 
            @click="editCategory(category)"
            title="Modifier"
          >
            ✏️
          </button>
          <button 
            class="action-btn delete" 
            @click="confirmDelete(category)"
            title="Supprimer"
          >
            🗑️
          </button>
        </div>
      </div>
    </div>

    <!-- État vide -->
    <div v-if="!loading && !error && categories.length === 0" class="empty-state">
      <div class="empty-icon">📦</div>
      <h3>Aucune catégorie trouvée</h3>
      <p>Commencez par créer votre première catégorie de produits</p>
      <button class="add-category-btn" @click="showAddModal">
        <span class="btn-icon">+</span>
        Ajouter une catégorie
      </button>
    </div>

    <!-- Modal d'ajout/modification -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ isEditing ? 'Modifier la catégorie' : 'Nouvelle catégorie' }}</h3>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        <form @submit.prevent="saveCategory" class="modal-body">
          <div class="form-group">
            <label for="nom">Nom de la catégorie *</label>
            <input 
              type="text" 
              id="nom"
              v-model="formData.nom"
              placeholder="Ex: BOISSON, ÉPICERIE..."
              required
              class="form-input"
            >
          </div>
          <div class="form-group">
            <label for="description">Description *</label>
            <textarea 
              id="description"
              v-model="formData.description"
              placeholder="Description de la catégorie..."
              required
              rows="3"
              class="form-textarea"
            ></textarea>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="closeModal">
              Annuler
            </button>
            <button type="submit" class="btn-submit" :disabled="saving">
              {{ saving ? 'Enregistrement...' : (isEditing ? 'Mettre à jour' : 'Créer') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de confirmation de suppression -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal-content delete-modal">
        <div class="modal-header danger">
          <h3>Confirmer la suppression</h3>
          <button class="close-btn" @click="showDeleteModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="delete-warning">
            <div class="warning-icon">⚠️</div>
            <p>Êtes-vous sûr de vouloir supprimer la catégorie :</p>
            <strong>{{ categoryToDelete?.nom }}</strong>
            <p class="warning-text">Cette action est irréversible !</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showDeleteModal = false">
            Annuler
          </button>
          <button class="btn-delete" @click="deleteCategory" :disabled="deleting">
            {{ deleting ? 'Suppression...' : 'Supprimer' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import categoriesAPI from '../services/categories';
import { useDataCache } from '@/composables/useDataCache';

export default {
  name: 'CategoriesView',
  setup() {
    const { loadWithCache, invalidateCache } = useDataCache();
    return { loadWithCache, invalidateCache };
  },
  data() {
    return {
      categories: [],
      loading: false,
      error: null,
      showModal: false,
      showDeleteModal: false,
      isEditing: false,
      saving: false,
      deleting: false,
      formData: {
        nom: '',
        description: ''
      },
      currentCategory: null,
      categoryToDelete: null
    };
  },
  mounted() {
    // Charger avec cache si disponible
    this.fetchCategories(false);
  },
  methods: {
    // === MÉTHODE PUBLIQUE POUR REFRESH DEPUIS APP.VUE ===
    async refreshData() {
      console.log('🔄 Rafraîchissement forcé des Catégories...');
      this.invalidateCache('categories');
      await this.fetchCategories(true);
      alert('✅ Catégories actualisées');
    },
    
    /**
     * Récupère toutes les catégories depuis l'API
     */
    async fetchCategories(forceRefresh = false) {
      // Ne montrer le loading QUE si on force le refresh ou si pas de données
      const showLoading = forceRefresh || !this.categories.length;
      
      if (showLoading) {
        this.loading = true;
      }
      this.error = null;
      
      try {
        this.categories = await this.loadWithCache('categories', async () => {
          const response = await categoriesAPI.getAllCategories();
          console.log('📦 Catégories chargées depuis l\'API:', response.data);
          return response.data;
        }, forceRefresh);
      } catch (err) {
        this.error = err.response?.data?.message || 'Erreur lors du chargement des catégories';
        console.error('Erreur de chargement:', err);
      } finally {
        if (showLoading) {
          this.loading = false;
        }
      }
    },

    /**
     * Affiche le modal d'ajout d'une nouvelle catégorie
     */
    showAddModal() {
      this.isEditing = false;
      this.formData = {
        nom: '',
        description: ''
      };
      this.currentCategory = null;
      this.showModal = true;
    },

    /**
     * Affiche le modal de modification d'une catégorie
     */
    editCategory(category) {
      this.isEditing = true;
      this.currentCategory = category;
      this.formData = {
        nom: category.nom,
        description: category.description
      };
      this.showModal = true;
    },

    /**
     * Ferme le modal
     */
    closeModal() {
      this.showModal = false;
      this.formData = {
        nom: '',
        description: ''
      };
      this.currentCategory = null;
      this.isEditing = false;
    },

    /**
     * Enregistre une catégorie (création ou modification)
     */
    async saveCategory() {
      this.saving = true;
      try {
        if (this.isEditing) {
          // Mise à jour
          await categoriesAPI.updateCategory(
            this.currentCategory.id_categorie, 
            this.formData
          );
          console.log('Catégorie mise à jour avec succès');
        } else {
          // Création
          await categoriesAPI.createCategory(this.formData);
          console.log('Catégorie créée avec succès');
        }
        
        this.closeModal();
        
        // Invalider le cache et recharger
        this.invalidateCache('categories');
        await this.fetchCategories(true);
        
        // Afficher un message de succès (vous pouvez utiliser une bibliothèque de notifications)
        alert(this.isEditing ? 'Catégorie mise à jour avec succès !' : 'Catégorie créée avec succès !');
        
      } catch (err) {
        console.error('Erreur lors de l\'enregistrement:', err);
        alert(err.response?.data?.message || 'Erreur lors de l\'enregistrement');
      } finally {
        this.saving = false;
      }
    },

    /**
     * Affiche le modal de confirmation de suppression
     */
    confirmDelete(category) {
      this.categoryToDelete = category;
      this.showDeleteModal = true;
    },

    /**
     * Supprime une catégorie
     */
    async deleteCategory() {
      this.deleting = true;
      try {
        await categoriesAPI.deleteCategory(this.categoryToDelete.id_categorie);
        console.log('Catégorie supprimée avec succès');
        
        this.showDeleteModal = false;
        this.categoryToDelete = null;
        
        // Invalider le cache et recharger
        this.invalidateCache('categories');
        await this.fetchCategories(true);
        
        alert('Catégorie supprimée avec succès !');
        
      } catch (err) {
        console.error('Erreur lors de la suppression:', err);
        alert(err.response?.data?.message || 'Erreur lors de la suppression');
      } finally {
        this.deleting = false;
      }
    },

    /**
     * Affiche les produits d'une catégorie
     */
    async viewCategoryProducts(category) {
      try {
        const response = await categoriesAPI.getCategoryProducts(category.id_categorie);
        console.log(`Produits de la catégorie ${category.nom}:`, response.data);
        
        // Vous pouvez naviguer vers une autre vue ou afficher un modal
        alert(`${response.data.length} produit(s) dans la catégorie ${category.nom}`);
        
      } catch (err) {
        console.error('Erreur lors du chargement des produits:', err);
        alert('Erreur lors du chargement des produits');
      }
    },

    /**
     * Formate l'UUID pour l'affichage (affiche seulement les premiers caractères)
     */
    formatId(id) {
      return id ? id.substring(0, 8) + '...' : '';
    }
  }
};
</script>

<style scoped>
/* ==================== CONTAINER ==================== */
.categories-content {
  padding: 20px 40px 40px 40px;
  background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
  min-height: 100vh;
}

/* ==================== HEADER ==================== */
.categories-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
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

.add-category-btn {
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

.add-category-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.btn-icon {
  font-size: 18px;
  font-weight: bold;
}

/* ==================== LOADING STATE ==================== */
.loading-state {
  text-align: center;
  padding: 60px 20px;
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
  to { transform: rotate(360deg); }
}

.loading-state p {
  color: #6b7280;
  font-size: 14px;
}

/* ==================== ERROR STATE ==================== */
.error-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  border: 1px solid #fee2e2;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
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

.retry-btn {
  padding: 10px 24px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

/* ==================== CATEGORIES GRID ==================== */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  animation: fadeIn 0.5s ease;
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

.category-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  border-color: #3b82f6;
}

.category-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.category-info {
  flex: 1;
}

.category-name {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
  text-transform: uppercase;
}

.category-description {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
  margin-bottom: 12px;
}

.category-id {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.id-label {
  color: #9ca3af;
  font-weight: 500;
}

.id-value {
  font-family: 'Courier New', monospace;
  color: #6b7280;
  background: #f3f4f6;
  padding: 2px 8px;
  border-radius: 4px;
}

.category-actions {
  display: flex;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.action-btn {
  flex: 1;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn.view {
  background: #eff6ff;
  color: #3b82f6;
}

.action-btn.view:hover {
  background: #3b82f6;
  color: white;
  transform: translateY(-2px);
}

.action-btn.edit {
  background: #f3f4f6;
  color: #6b7280;
}

.action-btn.edit:hover {
  background: #e5e7eb;
  color: #111827;
  transform: translateY(-2px);
}

.action-btn.delete {
  background: #fee2e2;
  color: #ef4444;
}

.action-btn.delete:hover {
  background: #ef4444;
  color: white;
  transform: translateY(-2px);
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

/* ==================== MODAL ==================== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header.danger {
  border-bottom-color: #fee2e2;
}

.modal-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: #f3f4f6;
  border-radius: 8px;
  font-size: 24px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.close-btn:hover {
  background: #e5e7eb;
  color: #111827;
}

.modal-body {
  padding: 24px;
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

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  color: #111827;
  transition: all 0.2s ease;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  resize: vertical;
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #e5e7eb;
}

.btn-cancel,
.btn-submit,
.btn-delete {
  flex: 1;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
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
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-delete {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.btn-delete:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.btn-delete:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Delete modal specific styles */
.delete-modal {
  max-width: 450px;
}

.delete-warning {
  text-align: center;
  padding: 20px 0;
}

.warning-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.delete-warning p {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.delete-warning strong {
  display: block;
  font-size: 18px;
  color: #111827;
  margin: 16px 0;
}

.warning-text {
  color: #ef4444 !important;
  font-weight: 600;
  margin-top: 12px !important;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 768px) {
  .categories-content {
    padding: 16px 20px;
  }

  .categories-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .categories-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95%;
    margin: 0 10px;
  }
}
</style>
