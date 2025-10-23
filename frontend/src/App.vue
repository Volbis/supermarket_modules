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
        <div class="user-profile">
          <div class="user-avatar">DE</div>
          <span class="user-name">Déric EZIN</span>
        </div>
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

export default {
  name: 'App',
  components: {
    Statistics,
    Orders,
    Notifications,
    Products,
    Suppliers,
    Dashboard,
    Categories
  },
  data() {
    return {
      // Icônes importées
      logoutIcon: require('@/assets/icons/deconnexion.png'),
      refreshIcon: require('@/assets/icons/refresh.png'),
      
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
          icon: require('@/assets/icons/produit.png'),
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
      return activeItem ? activeItem.component : 'Dashboard'
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
      console.log('Déconnexion')
    },
    
    handleRefresh() {
      console.log('Actualisation')
    }
  }
}
</script>

<style>
/* Les styles sont dans main.css */
</style>