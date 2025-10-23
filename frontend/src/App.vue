<template>
  <div class="app-container">
    <!-- Sidebar -->
    <aside class="sidebar">
      <!-- Logo -->
      <div class="logo-section">
        <div class="logo-container">
          <div class="logo-icon">EM</div>
          <span class="logo-text">ExpressMall</span>
        </div>
      </div>
 
      <!-- Navigation -->
      <nav class="nav-menu">
        <button
          v-for="item in menuItems"
          :key="item.name"
          :class="['nav-item', { active: item.active }]"
          @click="handleMenuClick(item.name)"
        >
          <img :src="item.icon" :alt="item.name" class="nav-icon-img" />
          <span>{{ item.name }}</span>
        </button>
      </nav>

      <!-- User section -->
      <div class="user-section">

        <button class="logout-btn" @click="handleProfile">
          <img :src="profilIcon" alt="Déconnexion" class="nav-icon-img" />
          <span class="user-name">Déric EZIN</span>
        </button>

        <button class="logout-btn" @click="handleLogout">
          <img :src="logoutIcon" alt="Déconnexion" class="nav-icon-img" />
          <span>Déconnexion</span>
        </button>

      </div>
    </aside>

    <!-- Main content -->
    <main class="main-content">
      <!-- Header dynamique -->
      <header class="header">
        <div class="header-content">
          <div class="header-title">
            <h1>{{ currentPage.title }}</h1>
            <p class="header-subtitle">{{ currentPage.subtitle }}</p>
          </div>
          <button class="refresh-btn" @click="handleRefresh">
            <span>Actualiser</span>
            <img :src="refreshIcon" alt="Actualiser" class="refresh-icon" />
          </button>
        </div>
      </header>

      <!-- Contenu dynamique -->
      <div class="page-content">
        <component :is="currentComponent" />
      </div>
    </main>

    <!-- Modal de déconnexion -->
    <div v-if="showLogoutModal" class="modal-overlay" @click="closeLogoutModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <span class="modal-icon">🚪</span>
          <h3>Confirmer la déconnexion</h3>
        </div>
        <div class="modal-body">
          <p>Êtes-vous sûr de vouloir vous déconnecter ?</p>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeLogoutModal">Annuler</button>
          <button class="btn-confirm" @click="confirmLogout">Se déconnecter</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Import des composants de vues
import Statistics from '@/views/Statistics.vue'
import Orders from '@/views/Orders.vue'
import Notifications from '@/views/Notifications.vue'
import Products from '@/views/Products.vue'
import Suppliers from '@/views/Suppliers.vue'
import Dashboard from '@/views/Dashboard.vue'
import Categories from '@/views/Categories.vue'
import Settings from '@/views/Settings.vue'

export default {
  name: 'App',
  components: {
    Statistics,
    Orders,
    Notifications,
    Products,
    Suppliers,
    Dashboard,
    Categories,
    Settings
  },
  data() {
    return {
      // Icônes importées
      profilIcon: require('@/assets/icons/profil.png'),
      logoutIcon: require('@/assets/icons/deconnexion.png'),
      refreshIcon: require('@/assets/icons/refresh.png'),
      
      // Modal de déconnexion
      showLogoutModal: false,
      
      // Page actuelle
      currentPage: {
        title: 'Tableau de bord',
        subtitle: 'Bienvenue sur votre tableau de bord monsieur Déric'
      },
      
      // Menu items avec icônes et configuration
      menuItems: [
        { 
          name: 'Tableau de bord', 
          icon: require('@/assets/icons/tableau-bord.png'),
          active: true,
          component: 'Dashboard',
          title: 'Tableau de bord',
          subtitle: 'Bienvenue sur votre tableau de bord monsieur Déric'
        },
        { 
          name: 'Statistiques', 
          icon: require('@/assets/icons/statistiques.png'),
          active: false,
          component: 'Statistics',
          title: 'Statistiques',
          subtitle: 'Analysez les performances de votre magasin'
        },
        { 
          name: 'Commandes', 
          icon: require('@/assets/icons/commande.png'),
          active: false,
          component: 'Orders',
          title: 'Commandes',
          subtitle: 'Gérez les commandes de vos clients'
        },
        { 
          name: 'Notifications', 
          icon: require('@/assets/icons/notifications.png'),
          active: false,
          component: 'Notifications',
          title: 'Notifications',
          subtitle: 'Restez informé des dernières activités'
        },
        { 
          name: 'Catégories', 
          icon: require('@/assets/icons/categorie.png'),
          active: false,
          component: 'Categories',
          title: 'Catégories',
          subtitle: 'Gérez les catégories de produits'
        },
        { 
          name: 'Produits', 
          icon: require('@/assets/icons/produit.png'),
          active: false,
          component: 'Products',
          title: 'Produits',
          subtitle: 'Gérez votre inventaire de produits'
        },
        { 
          name: 'Fournisseurs', 
          icon: require('@/assets/icons/fournisseur.png'),
          active: false,
          component: 'Suppliers',
          title: 'Fournisseurs',
          subtitle: 'Gérez vos partenaires fournisseurs'
        },
      ]
    }
  },
  computed: {
    currentComponent() {
      const activeItem = this.menuItems.find(item => item.active)
      // Si aucun élément du menu n'est actif, afficher Settings (pour le profil)
      return activeItem ? activeItem.component : 'Settings'
    }
  },
  methods: {
    handleMenuClick(menuName) {
      // Mettre à jour l'état actif des éléments du menu
      this.menuItems.forEach(item => {
        item.active = item.name === menuName
      })
      
      // Mettre à jour la page actuelle
      const selectedItem = this.menuItems.find(item => item.name === menuName)
      if (selectedItem) {
        this.currentPage = {
          title: selectedItem.title,
          subtitle: selectedItem.subtitle
        }
      }
      
      console.log('Menu cliqué:', menuName)
    },
    
    handleLogout() {
      this.showLogoutModal = true
    },

    closeLogoutModal() {
      this.showLogoutModal = false
    },

    confirmLogout() {
      console.log('Déconnexion confirmée')
      this.showLogoutModal = false
      // Ici, vous pouvez ajouter la logique de déconnexion (redirection, clear storage, etc.)
      // Par exemple: window.location.href = '/login'
    },

    handleProfile() {
      // Désactiver tous les éléments du menu
      this.menuItems.forEach(item => {
        item.active = false
      })
      
      // Mettre à jour la page actuelle pour afficher Settings
      this.currentPage = {
        title: 'Paramètres',
        subtitle: 'Gérez vos paramètres et préférences'
      }
      
      // Forcer l'affichage du composant Settings
      this.$forceUpdate()
    },
    
    handleRefresh() {
      console.log('Actualisation')
    }
  }
}
</script>

<style>
/* Les styles sont dans main.css */

/* ==================== MODAL DE DÉCONNEXION ==================== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeInOverlay 0.2s ease-out;
}

.modal-content {
  background: #ffffff;
  border-radius: 16px;
  padding: 0;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  min-width: 420px;
  max-width: 500px;
  animation: slideUp 0.3s ease-out;
}

.modal-header {
  padding: 24px 32px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.modal-icon {
  font-size: 32px;
}

.modal-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.modal-body {
  padding: 24px 32px;
}

.modal-body p {
  font-size: 15px;
  color: #374151;
  margin: 0 0 8px 0;
}


.modal-footer {
  padding: 20px 32px;
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-cancel {
  padding: 10px 20px;
  background: transparent;
  color: #6b7280;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: #f3f4f6;
  color: #111827;
}

.btn-confirm {
  padding: 10px 20px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-confirm:hover {
  background: #dc2626;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(239, 68, 68, 0.3);
}

@keyframes fadeInOverlay {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
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

/* Responsive */
@media (max-width: 768px) {
  .modal-content {
    min-width: 90%;
    max-width: 90%;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>