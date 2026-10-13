import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Definición del mapa de rutas del sistema
const routes = [
  // Rutas públicas
  { path: '/', name: 'Home', component: () => import('../views/HomeView.vue') },
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue') },
  { path: '/reset-password', name: 'ResetPassword', component: () => import('../views/ResetPasswordView.vue') },
  { path: '/servicios', name: 'Servicios', component: () => import('../views/ServiciosView.vue') },

  // Rutas protegidas (requieren sesión activa)
  { path: '/agendar', name: 'Agendar', component: () => import('../views/AgendarView.vue'), meta: { requiresAuth: true } },
  { path: '/perfil', name: 'Perfil', component: () => import('../views/PerfilView.vue'), meta: { requiresAuth: true } },
  { path: '/calendario', name: 'Calendario', component: () => import('../views/CalendarioView.vue'), meta: { requiresAuth: true } },
  { path: '/mecanicos', name: 'Mecanicos', component: () => import('../views/MecanicosView.vue'), meta: { requiresAuth: true } },

  // Rutas exclusivas para administradores
  { path: '/admin', name: 'Admin', component: () => import('../views/AdminView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

/**
 * Guard de navegación global para verificar la autenticación y roles de usuario.
 */
router.beforeEach(async (to) => {
  const auth = useAuthStore()
  await auth.init()

  // Redirigir a login si la ruta requiere autenticación y el usuario no ha iniciado sesión
  if (to.meta.requiresAuth && !auth.isLoggedIn) return { name: 'Login' }
  // Redirigir a inicio si la ruta requiere rol de administrador y el usuario no lo tiene
  if (to.meta.requiresAdmin && auth.user?.role !== 'admin') return { name: 'Home' }
  // Redirigir fuera de la página de login si ya hay una sesión activa
  if (to.name === 'Login' && auth.isLoggedIn) return auth.user.role === 'admin' ? { name: 'Admin' } : { name: 'Home' }
})

export default router
