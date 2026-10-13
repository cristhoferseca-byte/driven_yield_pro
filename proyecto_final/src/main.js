import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import { useCitasStore } from './stores/citas'
import './assets/global.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

async function bootstrap() {
  const auth = useAuthStore()
  await auth.init()

  const citas = useCitasStore()
  await citas.init()

  app.mount('#app')
}

bootstrap()
