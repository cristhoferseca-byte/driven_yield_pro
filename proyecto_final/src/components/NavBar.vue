<template>
  <nav class="nav" :class="{ scrolled }">
    <router-link to="/" class="nav-logo">
      <img src="/logo.png" alt="Driven Yield Pro Logo" class="brand-image" />
      <div class="brand-text">
        <div class="logo-brand">DRIVEN<span>YIELD</span></div>
        <div class="logo-sub">PRO SYSTEM</div>
      </div>
    </router-link>

<ul class="nav-links">
  <li><router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">Inicio</router-link></li>
  <li><router-link to="/servicios" class="nav-link" :class="{ active: $route.path === '/servicios' }">Servicios</router-link></li>
  <li><router-link to="/agendar" class="nav-link" :class="{ active: $route.path === '/agendar' }">Agendar</router-link></li>
  <li v-if="user"><router-link to="/calendario" class="nav-link" :class="{ active: $route.path === '/calendario' }">Calendario</router-link></li>
  <li v-if="user?.role === 'admin'"><router-link to="/mecanicos" class="nav-link" :class="{ active: $route.path === '/mecanicos' }">Mecánicos</router-link></li>
  <li v-if="user?.role === 'admin'">
    <router-link to="/admin" class="nav-link" :class="{ active: $route.path === '/admin' }">Admin</router-link>
  </li>
</ul>

    <div class="nav-actions">
      <template v-if="!user">
        <router-link to="/login" class="btn btn-primary">Iniciar Sesión</router-link>
      </template>
      <template v-else>
        <NotificationBell v-if="user.role !== 'admin'" />
        <div class="user-menu" ref="menuRef">
          <!-- Avatar trigger -->
          <button class="user-avatar" @click="menuOpen = !menuOpen" :class="{ open: menuOpen }" aria-label="Menú de usuario" title="Opciones de perfil">
            <span class="avatar-letter">{{ (user?.nombre || user?.username || 'U').charAt(0).toUpperCase() }}</span>
            <span class="avatar-ring"></span>
          </button>

          <!-- Dropdown -->
          <transition name="dropdown-anim">
            <div v-if="menuOpen" class="user-dropdown matte-card">
              <!-- Header -->
              <div class="dropdown-header">
                <div class="dh-avatar">{{ (user?.nombre || user?.username || 'U').charAt(0).toUpperCase() }}</div>
                <div class="dh-info">
                  <span class="dh-name">{{ user.nombre }}</span>
                  <span class="dh-role">
                    <span class="dh-dot"></span>
                    {{ user.role === 'admin' ? 'Administrador' : 'Cliente' }}
                  </span>
                </div>
              </div>

              <div class="dropdown-divider"></div>

              <!-- Items -->
              <div class="dropdown-body">
                <button class="dropdown-item" @click="goTo('/perfil')">
                  <span class="item-icon">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  </span>
                  <span class="item-text">Mi Perfil</span>
                  <svg class="item-arrow" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                </button>

                <button v-if="user.role === 'cliente'" class="dropdown-item" @click="goTo('/agendar')">
                  <span class="item-icon">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                  </span>
                  <span class="item-text">Agendar Cita</span>
                  <svg class="item-arrow" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                </button>

                <button v-if="user.role === 'admin'" class="dropdown-item item-admin" @click="goTo('/admin')">
                  <span class="item-icon">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                  </span>
                  <span class="item-text">Panel Admin</span>
                  <svg class="item-arrow" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                </button>
              </div>

              <div class="dropdown-divider"></div>

              <!-- Logout -->
              <button class="dropdown-item item-logout" @click="handleLogout">
                <span class="item-icon">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                </span>
                <span class="item-text">Cerrar Sesión</span>
              </button>
            </div>
          </transition>
        </div>
      </template>

      <button class="nav-toggle" @click="mobileOpen = !mobileOpen" :class="{ open: mobileOpen }">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>

  <!-- Mobile menu -->
  <transition name="mobile-anim">
    <div v-if="mobileOpen" class="nav-mobile-menu">
      <router-link to="/" class="mob-link" @click="mobileOpen = false">Inicio</router-link>
      <router-link to="/servicios" class="mob-link" @click="mobileOpen = false">Servicios</router-link>
      <router-link to="/agendar" class="mob-link" @click="mobileOpen = false">Agendar</router-link>
      <router-link v-if="user" to="/perfil" class="mob-link" @click="mobileOpen = false">Mi Perfil</router-link>
      <router-link v-if="user" to="/calendario" class="mob-link" @click="mobileOpen = false">Calendario</router-link>
      <router-link v-if="user?.role === 'admin'" to="/admin" class="mob-link" @click="mobileOpen = false">Admin</router-link>
      <div class="mob-actions">
        <router-link v-if="user?.role === 'admin'" to="/mecanicos" class="mob-link" @click="mobileOpen = false">Mecánicos</router-link>
        <router-link v-if="!user" to="/login" class="btn btn-primary" @click="mobileOpen = false">Iniciar Sesión</router-link>
        <button v-else class="mob-logout" @click="handleLogout">Cerrar Sesión</button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { storeToRefs } from 'pinia'
import { useNotificacionesStore } from '../stores/notificaciones'
import NotificationBell from './NotificationBell.vue'

const auth = useAuthStore()
const { user } = storeToRefs(auth)
const notifStore = useNotificacionesStore()
const router = useRouter()
const scrolled = ref(false)
const menuOpen = ref(false)
const mobileOpen = ref(false)
const menuRef = ref(null)

watch(user, (u) => {
  if (u && u.role !== 'admin') notifStore.startPolling()
  else notifStore.stopPolling()
}, { immediate: true })

function goTo(path) { menuOpen.value = false; router.push(path) }
function handleLogout() { menuOpen.value = false; mobileOpen.value = false; auth.logout(); router.push('/') }
function onScroll() { scrolled.value = window.scrollY > 20 }
function onClickOutside(e) { if (menuRef.value && !menuRef.value.contains(e.target)) menuOpen.value = false }

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  document.addEventListener('click', onClickOutside)
})
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  document.removeEventListener('click', onClickOutside)
})
</script>

<style scoped>
.nav {
  position: fixed; top: 0; left: 0; right: 0;
  z-index: 1000; height: var(--nav-height);
  padding: 0 4rem;
  background: rgba(10,10,10,0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,0.02);
  display: flex; align-items: center; justify-content: space-between;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.nav.scrolled {
  background: var(--bg-matte);
  border-bottom-color: var(--border-red);
  box-shadow: var(--shadow-matte);
}

/* Logo */
.nav-logo { display: flex; align-items: center; gap: 1rem; text-decoration: none; }
.brand-image { width: 85px; height: 85px; object-fit: contain; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.6)); transition: transform 0.3s ease; }
.nav-logo:hover .brand-image { transform: scale(1.08) rotate(-2deg); }
.brand-text { display: flex; flex-direction: column; line-height: 1.1; }
.logo-brand {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.4rem; font-weight: 900;
  color: white; letter-spacing: 1.5px;
}
.logo-brand span { color: var(--primary); }
.logo-sub {
  font-size: 0.6rem; letter-spacing: 4px;
  color: var(--text-secondary); text-transform: uppercase;
  margin-top: 3px; font-weight: 700;
}

/* Links */
.nav-links { display: flex; gap: 1rem; list-style: none; margin: 0; padding: 0; }
.nav-link {
  padding: 0.5rem 1rem;
  color: var(--text-secondary);
  font-weight: 600; font-size: 0.85rem;
  text-transform: uppercase; letter-spacing: 1px;
  border-radius: 4px; transition: all 0.3s ease;
  position: relative; overflow: hidden;
}
.nav-link::after {
  content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
  width: 0; height: 2px; background: var(--primary); transition: width 0.3s ease;
}
.nav-link:hover { color: white; }
.nav-link:hover::after { width: 100%; }
.nav-link.active { color: white; }
.nav-link.active::after { width: 100%; }

/* Actions & Avatar */
.nav-actions { display: flex; align-items: center; gap: 1rem; }
.user-menu { position: relative; }
.user-avatar {
  width: 42px; height: 42px; border-radius: 8px;
  background: var(--bg-card); border: var(--border-matte);
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all 0.3s ease; position: relative;
}
.user-avatar:hover { border-color: var(--primary); box-shadow: var(--shadow-red); }
.avatar-letter { font-family: 'Montserrat', sans-serif; font-size: 1.1rem; font-weight: 900; color: white; z-index: 1; }
.avatar-ring {
  position: absolute; inset: -2px; border-radius: 8px;
  border: 1px solid var(--primary); opacity: 0; transition: opacity 0.3s;
}
.user-avatar.open .avatar-ring, .user-avatar:hover .avatar-ring { opacity: 1; }

/* Dropdown */
.user-dropdown {
  position: absolute; top: calc(100% + 15px); right: 0;
  width: 250px; z-index: 10000;
}

.dropdown-header { display: flex; align-items: center; gap: 0.85rem; padding: 1.25rem; }
.dh-avatar {
  width: 40px; height: 40px; border-radius: 6px; flex-shrink: 0;
  background: var(--primary); display: flex; align-items: center; justify-content: center;
  font-family: 'Montserrat', sans-serif; font-size: 1rem; font-weight: 900; color: white;
}
.dh-info { display: flex; flex-direction: column; gap: 0.2rem; overflow: hidden; }
.dh-name { font-size: 0.9rem; font-weight: 700; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.dh-role { display: flex; align-items: center; gap: 0.35rem; font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase; }
.dh-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--primary); animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.dropdown-divider { height: 1px; background: rgba(255,255,255,0.05); margin: 0 1rem; }
.dropdown-body { padding: 0.5rem; }
.dropdown-item {
  width: 100%; padding: 0.75rem 1rem; display: flex; align-items: center; gap: 0.75rem;
  background: transparent; border: none; border-radius: 6px; color: var(--text-secondary);
  font-family: inherit; font-size: 0.85rem; font-weight: 600; cursor: pointer; text-align: left; transition: all 0.2s ease;
}
.dropdown-item:hover { color: white; background: rgba(255,255,255,0.05); }
.item-icon {
  width: 30px; height: 30px; border-radius: 6px; background: var(--bg-deep);
  display: flex; align-items: center; justify-content: center; flex-shrink: 0; transition: background 0.2s;
}
.dropdown-item:hover .item-icon { background: rgba(217,4,41,0.2); color: var(--primary); }
.item-text { flex: 1; }
.item-arrow { color: rgba(255,255,255,0.15); transition: transform 0.2s, color 0.2s; }
.dropdown-item:hover .item-arrow { transform: translateX(3px); color: white; }
.item-logout { margin: 0.5rem; width: calc(100% - 1rem); color: var(--danger); }
.item-logout:hover { color: var(--primary-light); background: rgba(217,4,41,0.1); }
.item-logout:hover .item-icon { background: rgba(217,4,41,0.2); color: var(--primary-light); }
.dropdown-anim-enter-active { animation: dropIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.dropdown-anim-leave-active { animation: dropOut 0.2s ease; }
@keyframes dropIn { from { opacity:0; transform: translateY(-15px) scale(0.95); } to { opacity:1; transform: translateY(0) scale(1); } }
@keyframes dropOut { from { opacity:1; transform: translateY(0) scale(1); } to { opacity:0; transform: translateY(-10px) scale(0.95); } }

/* Toggle */
.nav-toggle { display: none; flex-direction: column; gap: 6px; background: transparent; border: none; padding: 8px; cursor: pointer; }
.nav-toggle span { display: block; width: 24px; height: 2px; background: white; border-radius: 2px; transition: all 0.3s ease; }
.nav-toggle.open span:nth-child(1) { transform: translateY(8px) rotate(45deg); }
.nav-toggle.open span:nth-child(2) { opacity: 0; }
.nav-toggle.open span:nth-child(3) { transform: translateY(-8px) rotate(-45deg); }

/* Mobile menu */
.nav-mobile-menu {
  position: fixed; top: var(--nav-height); left: 0; right: 0;
  background: var(--bg-card); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border-bottom: var(--border-matte); padding: 1.5rem; z-index: 999;
  display: flex; flex-direction: column; gap: 0.5rem;
}
.mob-link {
  padding: 1rem; color: var(--text-secondary); font-weight: 700; font-size: 1rem; text-transform: uppercase;
  border-radius: 8px; text-decoration: none; transition: all 0.2s; border: 1px solid transparent;
}
.mob-link:hover { color: white; background: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.1); }
.mob-actions { margin-top: 1rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1); }
.mob-logout {
  width: 100%; padding: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;
  background: rgba(217,4,41,0.1); border: 1px solid rgba(217,4,41,0.3); border-radius: 8px;
  color: var(--primary-light); font-family: inherit; font-size: 1rem; font-weight: 700; cursor: pointer; transition: all 0.2s;
}
.mob-logout:hover { background: var(--primary); color: white; box-shadow: var(--shadow-red); }

.mobile-anim-enter-active { animation: mobileIn 0.3s ease; }
.mobile-anim-leave-active { animation: mobileOut 0.2s ease; }
@keyframes mobileIn { from { opacity:0; transform:translateY(-20px) } to { opacity:1; transform:translateY(0) } }
@keyframes mobileOut { from { opacity:1; transform:translateY(0) } to { opacity:0; transform:translateY(-20px) } }

@media (max-width: 768px) {
  .nav { padding: 0 1.5rem; }
  .nav-links { display: none; }
  .nav-actions .btn { display: none; }
  .nav-toggle { display: flex; }
}
.nav-links {
  flex-wrap: wrap;
}
</style>
