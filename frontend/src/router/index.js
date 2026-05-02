import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '../views/HomePage.vue'
import ShopPage from '../views/ShopPage.vue'
import ProductPage from '../views/ProductPage.vue'
import CheckoutPage from '../views/CheckoutPage.vue'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import AboutPage from '../views/AboutPage.vue'
import ContactPage from '../views/ContactPage.vue'
import { useAuthStore } from '../stores/auth'

export const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/shop', name: 'shop', component: ShopPage },
  { path: '/product/:id', name: 'product', component: ProductPage, props: true },
  { path: '/checkout', name: 'checkout', component: CheckoutPage, meta: { requiresAuth: true } },
  { path: '/login', name: 'login', component: LoginPage },
  { path: '/register', name: 'register', component: RegisterPage },
  { path: '/about', name: 'about', component: AboutPage },
  { path: '/contact', name: 'contact', component: ContactPage },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

// 導航守衛：需要登入的路由導到登入頁
export function setupAuthGuard(router) {
  router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
      const auth = useAuthStore()
      if (!auth.isLoggedIn) {
        next({ name: 'login', query: { redirect: to.fullPath } })
        return
      }
    }
    next()
  })
}

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.path !== from.path) return { top: 0 }
    return {}
  },
})

