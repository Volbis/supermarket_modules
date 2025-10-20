// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/App.vue'
import Products from '@/views/Products.vue'
import Orders from '@/views/Orders.vue'
import Statistics from '@/views/Statistics.vue'
import Suppliers from '@/views/Suppliers.vue'
import Notifications from '@/views/Notifications.vue'

const routes = [
  {
    path: '/', 
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/products', 
    name: 'Products',
    component: Products
  },
  {
    path: '/orders',
    name: 'Orders',
    component: Orders
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics
  },
  {
    path: '/suppliers',
    name: 'Suppliers',
    component: Suppliers
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: Notifications
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
