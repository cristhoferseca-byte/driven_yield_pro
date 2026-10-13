<template>
  <div class="notif-menu" ref="menuRef">
    <button class="notif-bell" @click="toggle" :class="{ open }">
      <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/>
        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
      </svg>
      <span v-if="noLeidas > 0" class="notif-badge">{{ noLeidas > 9 ? '9+' : noLeidas }}</span>
    </button>

    <transition name="dropdown-anim">
      <div v-if="open" class="notif-dropdown matte-card">
        <div class="notif-header">
          <span>Notificaciones</span>
          <button v-if="noLeidas > 0" class="notif-marcar-todas" @click="marcarTodasLeidas">
            Marcar todas leídas
          </button>
        </div>

        <div class="notif-body">
          <p v-if="loading && !notificaciones.length" class="notif-empty">Cargando...</p>
          <p v-else-if="!notificaciones.length" class="notif-empty">No tienes notificaciones</p>

          <div
            v-for="n in notificaciones"
            :key="n.id"
            class="notif-item"
            :class="{ unread: !n.leida }"
            @click="onClickNotif(n)"
          >
            <div class="notif-dot" v-if="!n.leida"></div>
            <div class="notif-content">
              <span class="notif-titulo">{{ n.titulo }}</span>
              <span class="notif-mensaje">{{ n.mensaje }}</span>
              <span class="notif-fecha">{{ formatFecha(n.created_at) }}</span>
            </div>
            <button class="notif-del" @click.stop="eliminarNotificacion(n.id)" title="Eliminar">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useNotificacionesStore } from '../stores/notificaciones'

const store = useNotificacionesStore()
const { notificaciones, noLeidas, loading } = storeToRefs(store)
const { marcarLeida, marcarTodasLeidas, eliminarNotificacion } = store

const open = ref(false)
const menuRef = ref(null)

function toggle() { open.value = !open.value }

function onClickNotif(n) {
  if (!n.leida) marcarLeida(n.id)
}

function formatFecha(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('es-CO', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })
}

function onClickOutside(e) {
  if (menuRef.value && !menuRef.value.contains(e.target)) open.value = false
}

onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))
</script>

<style scoped>
.notif-menu { position: relative; }

.notif-bell {
  position: relative;
  display: flex; align-items: center; justify-content: center;
  width: 40px; height: 40px;
  border-radius: 50%;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  color: var(--text-secondary, #ccc);
  cursor: pointer;
  transition: all 0.25s ease;
}
.notif-bell:hover, .notif-bell.open {
  background: rgba(255,255,255,0.08);
  color: #fff;
  border-color: var(--border-red, rgba(255,0,0,0.3));
}

.notif-badge {
  position: absolute; top: -4px; right: -4px;
  min-width: 17px; height: 17px; padding: 0 4px;
  border-radius: 999px;
  background: var(--primary, #e50914);
  color: #fff;
  font-size: 0.65rem; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  line-height: 1;
  box-shadow: 0 0 0 2px var(--bg-matte, #0a0a0a);
}

.notif-dropdown {
  position: absolute; top: calc(100% + 12px); right: 0;
  width: 340px; max-height: 420px;
  display: flex; flex-direction: column;
  border-radius: 14px;
  overflow: hidden;
  z-index: 1200;
}

.notif-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.9rem 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  font-weight: 700; font-size: 0.9rem; color: #fff;
}
.notif-marcar-todas {
  background: none; border: none; cursor: pointer;
  font-size: 0.72rem; font-weight: 600;
  color: var(--primary, #e50914);
}

.notif-body { overflow-y: auto; max-height: 360px; }

.notif-empty {
  padding: 1.5rem 1rem; text-align: center;
  color: var(--text-secondary, #888); font-size: 0.85rem;
}

.notif-item {
  position: relative;
  display: flex; align-items: flex-start; gap: 0.6rem;
  padding: 0.8rem 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  cursor: pointer;
  transition: background 0.2s ease;
}
.notif-item:hover { background: rgba(255,255,255,0.03); }
.notif-item.unread { background: rgba(229,9,20,0.06); }

.notif-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--primary, #e50914);
  margin-top: 6px; flex-shrink: 0;
}

.notif-content { display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 0; }
.notif-titulo { font-size: 0.83rem; font-weight: 700; color: #fff; }
.notif-mensaje { font-size: 0.78rem; color: var(--text-secondary, #aaa); line-height: 1.35; }
.notif-fecha { font-size: 0.68rem; color: var(--text-secondary, #777); margin-top: 2px; }

.notif-del {
  background: none; border: none; cursor: pointer;
  color: var(--text-secondary, #777);
  padding: 2px; flex-shrink: 0;
  opacity: 0; transition: opacity 0.2s ease;
}
.notif-item:hover .notif-del { opacity: 1; }
.notif-del:hover { color: var(--primary, #e50914); }

.dropdown-anim-enter-active, .dropdown-anim-leave-active { transition: all 0.2s ease; }
.dropdown-anim-enter-from, .dropdown-anim-leave-to { opacity: 0; transform: translateY(-8px); }
</style>
