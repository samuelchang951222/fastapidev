import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import { router, setupAuthGuard } from './router'

import './styles/main.scss'

setupAuthGuard(router)

createApp(App).use(createPinia()).use(router).mount('#app')
