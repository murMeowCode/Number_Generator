import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'primeicons/primeicons.css'
import './assets/styless/main.css'
import App from './App.vue'
import router from './router'
import AOS from 'aos'
import 'aos/dist/aos.css'
import PrimeVue from 'primevue/config'

import { createNotivue } from 'notivue'
import DialogService from 'primevue/dialogservice'
import 'notivue/notification.css' // Only needed if using built-in notifications
import 'notivue/animations.css' // Only needed if using built-in animations
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import { QueryClient, VueQueryPlugin } from '@tanstack/vue-query'
const app = createApp(App)
const notivue = createNotivue({
  position: 'top-right',
  limit: 5,
  enqueue: true,
  notifications: {
    global: {
      duration: 4000,
    },
  },
})
app.use(Toast, {
  transition: 'Vue-Toastification__bounce',
  maxToasts: 20,
  newestOnTop: true,
  position: 'top-center',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: true,
  closeButton: 'button',
  icon: true,
  rtl: false,
})
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 минут кеш
      cacheTime: 10 * 60 * 1000, // 10 минут жизнь кеша
    },
  },
})
app.use(notivue)
app.use(PrimeVue)
app.use(DialogService)
AOS.init({
  duration: 800,
  once: false,
})
app.use(createPinia())
app.use(router)

app.use(VueQueryPlugin, { queryClient })
app.mount('#app')
