<template>
  <div class="suppliers-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <p class="page-subtitle">{{ filteredSuppliers.length }} fournisseurs • {{ activeSuppliers }} actifs</p>
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
          <p class="stat-label">Actifs</p>
          <p class="stat-value">{{ activeSuppliers }}</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #FEF2F2;">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Inactifs</p>
          <p class="stat-value">{{ inactiveSuppliers }}</p>
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
        <select v-model="filterStatus" class="filter-select">
          <option value="">Tous les statuts</option>
          <option value="active">Actifs</option>
          <option value="inactive">Inactifs</option>
        </select>

        <select v-model="sortBy" class="filter-select">
          <option value="name">Nom (A-Z)</option>
          <option value="orders">Commandes</option>
          <option value="rating">Note</option>
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

    <!-- Suppliers Grid -->
    <div v-if="sortedSuppliers.length > 0" :class="['suppliers-grid', viewMode]">
      <div v-for="supplier in sortedSuppliers" :key="supplier.id" class="supplier-card">
        <div class="card-header">
          <div class="avatar" :style="{ background: supplier.color }">
            {{ getInitials(supplier.name) }}
          </div>
          <div class="header-info">
            <h3 class="supplier-name">{{ supplier.name }}</h3>
            <div class="rating">
              <svg v-for="i in 5" :key="i" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" :fill="i <= supplier.rating ? '#FBBF24' : '#E5E7EB'" stroke="none">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
              <span class="rating-value">{{ supplier.rating }}/5</span>
            </div>
          </div>
          <span :class="['badge', supplier.status]">
            {{ supplier.status === 'active' ? 'Actif' : 'Inactif' }}
          </span>
        </div>

        <div class="card-body">
          <div class="info-row">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
            <span>{{ supplier.email }}</span>
          </div>

          <div class="info-row">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
            </svg>
            <span>{{ supplier.phone }}</span>
          </div>

          <div class="info-row">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
            <span>{{ supplier.location }}</span>
          </div>

          <div class="info-row">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            </svg>
            <span>{{ supplier.totalOrders }} commandes</span>
          </div>
        </div>

        <div class="tags">
          <span v-for="(category, index) in supplier.categories" :key="index" class="tag">
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
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
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
  </div>
</template>

<script>
export default {
  name: 'FournisseursView',
  data() {
    return {
      searchQuery: '',
      filterStatus: '',
      sortBy: 'name',
      viewMode: 'grid',
      suppliers: [
        {
          id: 1,
          name: 'Ferme Bio Martin',
          email: 'contact@fermebiomartin.fr',
          phone: '01 23 45 67 89',
          location: 'Normandie, France',
          status: 'active',
          rating: 5,
          totalOrders: 145,
          categories: ['Bio', 'Fruits', 'Légumes'],
          color: '#10b981'
        },
        {
          id: 2,
          name: 'Légumes du Sud',
          email: 'info@legumesdusud.com',
          phone: '04 56 78 90 12',
          location: 'Provence, France',
          status: 'active',
          rating: 4,
          totalOrders: 98,
          categories: ['Légumes', 'Local'],
          color: '#f59e0b'
        },
        {
          id: 3,
          name: 'Fruits & Co',
          email: 'hello@fruitsco.fr',
          phone: '02 34 56 78 90',
          location: 'Bretagne, France',
          status: 'inactive',
          rating: 3,
          totalOrders: 52,
          categories: ['Fruits', 'Import'],
          color: '#ef4444'
        },
        {
          id: 4,
          name: 'Produits Laitiers Dupont',
          email: 'contact@laitiersdupont.fr',
          phone: '03 45 67 89 01',
          location: 'Auvergne, France',
          status: 'active',
          rating: 5,
          totalOrders: 187,
          categories: ['Laitier', 'Bio', 'Local'],
          color: '#3b82f6'
        },
        {
          id: 5,
          name: 'Epicerie Fine Paris',
          email: 'info@epiceriefineparis.fr',
          phone: '01 98 76 54 32',
          location: 'Paris, France',
          status: 'active',
          rating: 4,
          totalOrders: 203,
          categories: ['Épicerie', 'Premium'],
          color: '#8b5cf6'
        },
        {
          id: 6,
          name: 'Viandes de Qualité',
          email: 'contact@viandesqualite.com',
          phone: '05 67 89 01 23',
          location: 'Limousin, France',
          status: 'active',
          rating: 5,
          totalOrders: 134,
          categories: ['Viande', 'Bio'],
          color: '#ec4899'
        }
      ]
    }
  },
  computed: {
    filteredSuppliers() {
      return this.suppliers.filter(supplier => {
        const matchesSearch = supplier.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                             supplier.email.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                             supplier.location.toLowerCase().includes(this.searchQuery.toLowerCase())
        const matchesStatus = !this.filterStatus || supplier.status === this.filterStatus
        return matchesSearch && matchesStatus
      })
    },
    sortedSuppliers() {
      const filtered = [...this.filteredSuppliers]
      return filtered.sort((a, b) => {
        switch(this.sortBy) {
          case 'orders':
            return b.totalOrders - a.totalOrders
          case 'rating':
            return b.rating - a.rating
          default:
            return a.name.localeCompare(b.name)
        }
      })
    },
    activeSuppliers() {
      return this.suppliers.filter(s => s.status === 'active').length
    },
    inactiveSuppliers() {
      return this.suppliers.filter(s => s.status === 'inactive').length
    },
    totalOrders() {
      return this.suppliers.reduce((sum, s) => sum + s.totalOrders, 0)
    }
  },
  methods: {
    getInitials(name) {
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    },
    showAddModal() {
      console.log('Ouvrir modal d\'ajout fournisseur')
    },
    editSupplier(supplier) {
      console.log('Modifier fournisseur:', supplier.name)
    },
    contactSupplier(supplier) {
      console.log('Contacter fournisseur:', supplier.name)
      window.location.href = `mailto:${supplier.email}`
    },
    viewSupplier(supplier) {
      console.log('Voir détails fournisseur:', supplier.name)
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
