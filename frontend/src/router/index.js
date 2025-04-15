import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Inventory from '../views/Inventory.vue'
import Drink from '../views/Drink.vue'
import LiveStorage from '@/views/LiveStorage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/inventory',
    name: 'inventory',
    component: Inventory,
  },
  {
    path: '/drink',
    name: 'drink',
    component: Drink,
  },
  {
    path: '/live',
    name: 'live',
    component: LiveStorage,
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
