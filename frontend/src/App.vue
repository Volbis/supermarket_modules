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
      <!-- Header -->
      <header class="header">
        <div class="header-content">
          <div class="header-title">
            <h1>Tableau de bord</h1>
            <p class="header-subtitle">Bienvenue sur votre tableau de bord monsieur Déric</p>
          </div>
          <button class="refresh-btn" @click="handleRefresh">
            <span>Actualiser</span>
            <img :src="refreshIcon" alt="Actualiser" class="refresh-icon" />
          </button>
        </div>
      </header>

      <!-- Dashboard content -->
      <div class="dashboard-content">
        <div class="cards-grid-top">
          <div v-for="i in 3" :key="'top-' + i" class="dashboard-card card-top">
            Carte {{ i }}
          </div>
        </div>
        
        <div class="cards-grid-bottom">
          <div v-for="i in 2" :key="'bottom-' + i" class="dashboard-card card-bottom">
            Carte {{ i + 3 }}
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      // Icônes importées
      logoutIcon: require('@/assets/icons/deconnexion.png'),
      refreshIcon: require('@/assets/icons/refresh.png'),
      
      // Menu items avec icônes
      menuItems: [
        { 
          name: 'Tableau de bord', 
          icon: require('@/assets/icons/tableau-bord.png'),
          active: true 
        },
        { 
          name: 'Statistiques', 
          icon: require('@/assets/icons/statistiques.png'),
          active: false 
        },
        { 
          name: 'Commandes', 
          icon: require('@/assets/icons/commande.png'),
          active: false 
        },
        { 
          name: 'Notifications', 
          icon: require('@/assets/icons/notifications.png'),
          active: false 
        },
        { 
          name: 'Produits', 
          icon: require('@/assets/icons/produit.png'),
          active: false 
        },
        { 
          name: 'Fournisseurs', 
          icon: require('@/assets/icons/fournisseur.png'),
          active: false 
        },
      ]
    }
  },
  methods: {
    handleMenuClick(menuName) {
      this.menuItems.forEach(item => {
        item.active = item.name === menuName
      })
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