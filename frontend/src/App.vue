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
        <button class="user-profile-btn" @click="goToSettings">
          <div class="user-avatar">DE</div>
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
    Settings
  },
  data() {
    return {
      logoutIcon: require('@/assets/icons/deconnexion.png'),
      refreshIcon: require('@/assets/icons/refresh.png'),

      currentPage: {
        title: 'Tableau de bord',
        subtitle: 'Bienvenue sur votre tableau de bord monsieur Déric'
      },

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
      // Supprimer l'item temporaire Paramètres s'il existe
      this.menuItems = this.menuItems.filter(item => !item._isTemp)

      // Mettre à jour l'état actif
      this.menuItems.forEach(item => {
        item.active = item.name === menuName
      })

      // Mettre à jour currentPage
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
    },

    goToSettings() {
      const existing = this.menuItems.find(i => i.component === 'Settings')
      if (existing) {
        this.menuItems.forEach(i => i.active = false)
        existing.active = true
        this.currentPage = { title: existing.title, subtitle: existing.subtitle }
        return
      }

      // Ajouter temporairement l'item Paramètres
      this.menuItems.forEach(i => i.active = false)
      const tempSettings = {
        name: 'Paramètres',
        icon: require('@/assets/icons/parametres.png'),
        active: true,
        component: 'Settings',
        title: 'Paramètres',
        subtitle: 'Gérez vos préférences',
        _isTemp: true
      }
      this.menuItems.push(tempSettings)
      this.currentPage = {
        title: tempSettings.title,
        subtitle: tempSettings.subtitle
      }
    },

    goToPage(item) {
      this.menuItems.forEach(i => i.active = false)
      item.active = true
      this.currentPage = { title: item.title, subtitle: item.subtitle }
    }
  }
}
</script>

<style>
/* Les styles sont dans main.css */
</style>
