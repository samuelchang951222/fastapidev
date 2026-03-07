import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '../views/HomePage.vue'
import ShopPage from '../views/ShopPage.vue'
import ProductPage from '../views/ProductPage.vue'
import CheckoutPage from '../views/CheckoutPage.vue'
import AboutPage from '../views/AboutPage.vue'
import ContactPage from '../views/ContactPage.vue'

export const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/shop', name: 'shop', component: ShopPage },
  { path: '/product/:id', name: 'product', component: ProductPage, props: true },
  { path: '/checkout', name: 'checkout', component: CheckoutPage },
  { path: '/about', name: 'about', component: AboutPage },
  { path: '/contact', name: 'contact', component: ContactPage },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.path !== from.path) return { top: 0 }
    return {}
  },
})

