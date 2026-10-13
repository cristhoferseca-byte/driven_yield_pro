// src/stores/notificaciones.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './auth'
import { API_BASE_URL, networkErrorMessage, parseApiResponse } from '../config/api'

const POLL_MS = 20000
let pollHandle = null

export const useNotificacionesStore = defineStore('notificaciones', () => {
  const notificaciones = ref([])
  const noLeidas       = ref(0)
  const loading        = ref(false)
  const error          = ref(null)

  function headers() {
    const auth = useAuthStore()
    return {
      'Content-Type': 'application/json',
      ...(auth.token ? { Authorization: `Bearer ${auth.token}` } : {})
    }
  }

  async function fetchNotificaciones() {
    const auth = useAuthStore()
    if (!auth.isLoggedIn) return

    loading.value = true; error.value = null
    try {
      const res  = await fetch(`${API_BASE_URL}/notificaciones`, { headers: headers() })
      const data = await parseApiResponse(res, 'Error al cargar notificaciones')
      notificaciones.value = data.notificaciones
      noLeidas.value = data.no_leidas
    } catch (e) {
      error.value = networkErrorMessage(e)
    } finally {
      loading.value = false
    }
  }

  async function marcarLeida(id) {
    try {
      const res = await fetch(`${API_BASE_URL}/notificaciones/${id}/leer`, {
        method: 'PUT',
        headers: headers()
      })
      await parseApiResponse(res, 'Error al marcar notificación')
      const n = notificaciones.value.find(n => n.id === id)
      if (n && !n.leida) { n.leida = true; noLeidas.value = Math.max(0, noLeidas.value - 1) }
    } catch (e) {
      error.value = networkErrorMessage(e)
    }
  }

  async function marcarTodasLeidas() {
    try {
      const res = await fetch(`${API_BASE_URL}/notificaciones/leer-todas`, {
        method: 'PUT',
        headers: headers()
      })
      await parseApiResponse(res, 'Error al marcar notificaciones')
      notificaciones.value.forEach(n => (n.leida = true))
      noLeidas.value = 0
    } catch (e) {
      error.value = networkErrorMessage(e)
    }
  }

  async function eliminarNotificacion(id) {
    try {
      const res = await fetch(`${API_BASE_URL}/notificaciones/${id}`, {
        method: 'DELETE',
        headers: headers()
      })
      await parseApiResponse(res, 'Error al eliminar notificación')
      const idx = notificaciones.value.findIndex(n => n.id === id)
      if (idx !== -1) {
        if (!notificaciones.value[idx].leida) noLeidas.value = Math.max(0, noLeidas.value - 1)
        notificaciones.value.splice(idx, 1)
      }
    } catch (e) {
      error.value = networkErrorMessage(e)
    }
  }

  function startPolling() {
    stopPolling()
    fetchNotificaciones()
    pollHandle = setInterval(fetchNotificaciones, POLL_MS)
  }

  function stopPolling() {
    if (pollHandle) { clearInterval(pollHandle); pollHandle = null }
  }

  return {
    notificaciones, noLeidas, loading, error,
    fetchNotificaciones, marcarLeida, marcarTodasLeidas, eliminarNotificacion,
    startPolling, stopPolling
  }
})
