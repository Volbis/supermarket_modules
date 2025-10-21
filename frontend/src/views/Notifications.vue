<template>
  <div class="notifications-content">
    <div class="notifications-header">
      <h2>Notifications</h2>
      <p>Restez informé des dernières activités</p>
    </div>
    
    <div class="notifications-list">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        :class="['notification-item', { unread: !notification.read }]"
      >
        <div class="notification-icon">
          <img :src="notification.icon" :alt="notification.type" />
        </div>
        <div class="notification-content">
          <h4>{{ notification.title }}</h4>
          <p>{{ notification.message }}</p>
          <span class="notification-time">{{ notification.time }}</span>
        </div>
        <div class="notification-actions">
          <button v-if="!notification.read" @click="markAsRead(notification.id)" class="mark-read-btn">
            Marquer comme lu
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotificationsView',
  data() {
    return {
      notifications: [
        {
          id: 1,
          title: 'Nouvelle commande',
          message: 'Une nouvelle commande #001 a été passée par Jean Dupont',
          time: 'Il y a 5 minutes',
          read: false,
          type: 'order',
          icon: require('@/assets/icons/commande.png')
        },
        {
          id: 2,
          title: 'Stock faible',
          message: 'Le produit "Pommes" est en rupture de stock',
          time: 'Il y a 1 heure',
          read: false,
          type: 'stock',
          icon: require('@/assets/icons/produit.png')
        },
        {
          id: 3,
          title: 'Livraison confirmée',
          message: 'La commande #002 a été livrée avec succès',
          time: 'Il y a 2 heures',
          read: true,
          type: 'delivery',
          icon: require('@/assets/icons/commande.png')
        },
        {
          id: 4,
          title: 'Nouveau fournisseur',
          message: 'Un nouveau fournisseur s\'est inscrit sur la plateforme',
          time: 'Il y a 3 heures',
          read: true,
          type: 'supplier',
          icon: require('@/assets/icons/fournisseur.png')
        }
      ]
    }
  },
  methods: {
    markAsRead(notificationId) {
      const notification = this.notifications.find(n => n.id === notificationId)
      if (notification) {
        notification.read = true
      }
    }
  }
}
</script>

<style scoped>
.notifications-content {
  padding: 20px;
}

.notifications-header {
  margin-bottom: 30px;
}

.notifications-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.notifications-header p {
  color: #6b7280;
  font-size: 16px;
}

.notifications-list {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.notification-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e5e7eb;
  transition: background-color 0.2s;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item.unread {
  background: #f0f9ff;
  border-left: 4px solid #3b82f6;
}

.notification-item:hover {
  background: #f9fafb;
}

.notification-icon {
  margin-right: 16px;
}

.notification-icon img {
  width: 24px;
  height: 24px;
}

.notification-content {
  flex: 1;
}

.notification-content h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.notification-content p {
  color: #6b7280;
  font-size: 14px;
  margin-bottom: 4px;
}

.notification-time {
  font-size: 12px;
  color: #9ca3af;
}

.notification-actions {
  margin-left: 16px;
}

.mark-read-btn {
  padding: 6px 12px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.mark-read-btn:hover {
  background: #2563eb;
}
</style>