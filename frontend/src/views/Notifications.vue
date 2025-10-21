<template>
  <div class="notifications-container">
   

    <!-- Tabs de catégories -->
    <div class="tabs-container">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
        <span v-if="getUnreadCount(tab.id) > 0" class="badge">
          {{ getUnreadCount(tab.id) }}
        </span>
      </button>
    </div>

    <!-- Liste des notifications -->
    <div class="notifications-content">
      <div class="notifications-section" v-for="category in filteredCategories" :key="category.title">
        <h3 class="section-title">{{ category.title }}</h3>
        
        <div class="notifications-list">
          <div 
            v-for="notification in category.items" 
            :key="notification.id"
            :class="['notification-card', { unread: !notification.read }]"
          >
            <!-- Indicateur non lu -->
            <div v-if="!notification.read" class="unread-indicator"></div>

            <!-- Contenu de la notification -->
            <div class="notification-body">
              <div class="notification-main">
                <div class="notification-icon">
                  <img :src="notification.icon" :alt="notification.type" />
                </div>
                
                <div class="notification-content">
                  <h4 class="notification-title">{{ notification.title }}</h4>
                  <p class="notification-message">{{ notification.message }}</p>
                </div>
              </div>

              <div class="notification-meta">
                <span class="notification-time">{{ notification.time }}</span>
                <button 
                  v-if="!notification.read" 
                  @click="markAsRead(notification.id)"
                  class="mark-read-btn"
                  title="Marquer comme lu"
                >
                  Marquer comme lu
                </button>
              </div>
            </div>
          </div>

          <!-- Message si aucune notification -->
          <div v-if="category.items.length === 0" class="empty-state">
            <p>Aucune notification dans cette catégorie</p>
          </div>
        </div>
      </div>

      <!-- Message si tout est vide -->
      <div v-if="filteredNotifications.length === 0" class="empty-state-main">
        <div class="empty-icon">📭</div>
        <h3>Aucune notification</h3>
        <p>Vous êtes à jour ! Aucune nouvelle notification pour le moment.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotificationsView',
  data() {
    return {
      activeTab: 'all',
      tabs: [
        { id: 'all', label: 'Toutes' },
        { id: 'system', label: 'Système' },
        { id: 'orders', label: 'Envoyés / Reçus' }
      ],
      notifications: [
        // Système
        {
          id: 1,
          title: 'Alerte Stock',
          message: 'Selon des prédictions, le stock du produit "Sac de riz rizière (25kg)" sera épuisé le 02/01/2026',
          time: "Aujourd'hui",
          read: false,
          type: 'stock',
          category: 'system',
          icon: require('@/assets/icons/stock.png')
        },
        {
          id: 2,
          title: 'Recommandation de commande',
          message: 'Selon des prédictions, le stock du produit "Sac de riz rizière (25kg)" sera épuisé le 02/01/2026',
          time: 'Hier',
          read: true,
          type: 'recommendation',
          category: 'system',
          icon: require('@/assets/icons/box.png')
        },
        {
          id: 3,
          title: 'Arrivage validé',
          message: 'Selon des prédictions, le stock du produit "Sac de riz rizière (25kg)" sera épuisé le 02/01/2026',
          time: 'Hier',
          read: true,
          type: 'arrival',
          category: 'system',
          icon: require('@/assets/icons/livraison.png')
        },
        {
          id: 4,
          title: 'Création de nouveau produit',
          message: 'Selon des prédictions, le stock du produit "Sac de riz rizière (25kg)" sera épuisé le 02/01/2026',
          time: 'Hier',
          read: true,
          type: 'product',
          category: 'system',
          icon: require('@/assets/icons/plus.png')
        },

        // Envoyés / Reçus
        {
          id: 5,
          title: 'Alerte Stock',
          message: 'Selon des prédictions, le stock du produit "Sac de riz rizière (25kg)" sera épuisé le 02/01/2026',
          time: "Aujourd'hui",
          read: false,
          type: 'stock',
          category: 'orders',
          icon: require('@/assets/icons/stock.png')
        },
        {
          id: 6,
          title: 'Recommandation de commande',
          message: 'Selon des prédictions, le stock du produit "Sac de riz rizière (25kg)" sera épuisé le 02/01/2026',
          time: 'Hier',
          read: true,
          type: 'recommendation',
          category: 'orders',
          icon: require('@/assets/icons/box.png')
        },
        {
          id: 7,
          title: 'Arrivage validé',
          message: 'Selon des prédictions, le stock du produit "Sac de riz rizière (25kg)" sera épuisé le 02/01/2026',
          time: 'Hier',
          read: true,
          type: 'arrival',
          category: 'orders',
          icon: require('@/assets/icons/livraison.png')
        },
        {
          id: 8,
          title: 'Création de nouveau produit',
          message: 'Selon des prédictions, le stock du produit "Sac de riz rizière (25kg)" sera épuisé le 02/01/2026',
          time: 'Hier',
          read: true,
          type: 'product',
          category: 'orders',
          icon: require('@/assets/icons/plus.png')
        }
      ]
    }
  },
  computed: {
    filteredNotifications() {
      if (this.activeTab === 'all') {
        return this.notifications
      }
      return this.notifications.filter(n => n.category === this.activeTab)
    },
    filteredCategories() {
      const categories = []
      
      if (this.activeTab === 'all' || this.activeTab === 'system') {
        categories.push({
          title: 'Système',
          items: this.notifications.filter(n => n.category === 'system')
        })
      }
      
      if (this.activeTab === 'all' || this.activeTab === 'orders') {
        categories.push({
          title: 'Envoyés / Reçus',
          items: this.notifications.filter(n => n.category === 'orders')
        })
      }
      
      return categories
    }
  },
  methods: {
    markAsRead(notificationId) {
      const notification = this.notifications.find(n => n.id === notificationId)
      if (notification) {
        notification.read = true
      }
    },
    getUnreadCount(tabId) {
      if (tabId === 'all') {
        return this.notifications.filter(n => !n.read).length
      }
      return this.notifications.filter(n => n.category === tabId && !n.read).length
    },
    refreshNotifications() {
      console.log('Actualisation des notifications...')
      // Plus tard : appel API pour recharger les notifications
    }
  }
}
</script>

<style scoped>
/* ==================== CONTAINER ==================== */
.notifications-container {
  background-color: #f9fafb;
  min-height: 100%;
}

/* ==================== HEADER ==================== */
.notifications-header {
  background-color: #f9fafb;
  padding: 28px 40px 20px 40px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.notifications-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 6px;
  letter-spacing: -0.5px;
}

.subtitle {
  color: #6b7280;
  font-size: 15px;
  font-weight: 400;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}

.refresh-btn:hover {
  background-color: #f9fafb;
  border-color: #d1d5db;
}

.refresh-icon {
  font-size: 18px;
}

/* ==================== TABS ==================== */
.tabs-container {
  padding: 0 40px 20px 40px;
  display: flex;
  gap: 8px;
  border-bottom: 1px solid #e5e7eb;
  background-color: #f9fafb;
}

.tab-btn {
  position: relative;
  padding: 12px 20px;
  background: transparent;
  border: none;
  color: #6b7280;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-btn:hover {
  color: #111827;
  background-color: #f3f4f6;
  border-radius: 8px 8px 0 0;
}

.tab-btn.active {
  color: #111827;
  border-bottom-color: #3b82f6;
  font-weight: 600;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: #ef4444;
  color: white;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}

/* ==================== CONTENT ==================== */
.notifications-content {
  padding: 20px 40px 40px 40px;
}

.notifications-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* ==================== NOTIFICATION CARD ==================== */
.notification-card {
  position: relative;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px 20px;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.notification-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  border-color: #d1d5db;
}

.notification-card.unread {
  background: #f0f9ff;
  border-left: 4px solid #3b82f6;
}

.unread-indicator {
  position: absolute;
  top: 20px;
  left: 8px;
  width: 8px;
  height: 8px;
  background: #3b82f6;
  border-radius: 50%;
}

.notification-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notification-main {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.notification-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  background: #f3f4f6;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-icon img {
  width: 22px;
  height: 22px;
  object-fit: contain;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 6px;
}

.notification-message {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
}

.notification-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-left: 56px;
}

.notification-time {
  font-size: 13px;
  color: #9ca3af;
  font-weight: 500;
}

.mark-read-btn {
  padding: 6px 14px;
  background: transparent;
  color: #3b82f6;
  border: 1px solid #3b82f6;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mark-read-btn:hover {
  background: #3b82f6;
  color: white;
}

/* ==================== EMPTY STATE ==================== */
.empty-state {
  text-align: center;
  padding: 32px;
  color: #9ca3af;
  font-size: 14px;
}

.empty-state-main {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state-main h3 {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
}

.empty-state-main p {
  font-size: 15px;
  color: #6b7280;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 768px) {
  .notifications-header {
    flex-direction: column;
    gap: 16px;
    padding: 20px;
  }

  .tabs-container {
    padding: 0 20px 16px 20px;
    overflow-x: auto;
  }

  .notifications-content {
    padding: 16px 20px;
  }

  .notification-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    padding-left: 56px;
  }
}
</style>