// src/stores/citas.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './auth'
import { useNotificacionesStore } from './notificaciones'
import { API_BASE_URL, networkErrorMessage, parseApiResponse } from '../config/api'

export const useCitasStore = defineStore('citas', () => {
  const citas   = ref([])
  const loading = ref(false)
  const error   = ref(null)

  /**
   * Retorna los encabezados HTTP con token de autenticación.
   * @returns {Object} Encabezados HTTP
   */
  function headers() {
    const auth = useAuthStore()
    return {
      'Content-Type': 'application/json',
      ...(auth.token ? { Authorization: `Bearer ${auth.token}` } : {})
    }
  }

  /**
   * Retorna la URL del endpoint de citas según el rol de usuario.
   * @returns {string} URL del endpoint
   */
  function citasUrl() {
    const auth = useAuthStore()
    return auth.isAdmin ? `${API_BASE_URL}/admin/citas` : `${API_BASE_URL}/citas`
  }

  /**
   * Obtiene la lista de citas desde la API (diferenciando admin de cliente).
   */
  async function fetchCitas() {
    loading.value = true; error.value = null
    try {
      const res = await fetch(citasUrl(), { headers: headers() })
      citas.value = await parseApiResponse(res, 'Error al cargar citas')
    } catch (e) {
      error.value = networkErrorMessage(e)
    } finally { loading.value = false }
  }

  /**
   * Envía una solicitud para agendar una nueva cita en el taller.
   */
  async function agregarCita(datos) {
    loading.value = true; error.value = null
    try {
      const res = await fetch(`${API_BASE_URL}/citas`, {
        method: 'POST',
        headers: headers(),
        body: JSON.stringify(datos)
      })
      const data = await parseApiResponse(res, 'Error al agendar cita')
      await fetchCitas()
      useNotificacionesStore().fetchNotificaciones()
      return { ok: true, cita: data }
    } catch (e) {
      error.value = networkErrorMessage(e)
      return { ok: false, error: error.value }
    } finally { loading.value = false }
  }

  /**
   * Modifica el estado actual de una cita (e.g. pendiente, confirmada, cancelada).
   */
  async function actualizarEstado(citaId, estado) {
    try {
      const res = await fetch(`${API_BASE_URL}/citas/${citaId}/estado`, {
        method: 'PUT',
        headers: headers(),
        body: JSON.stringify({ estado })
      })
      await parseApiResponse(res, 'Error al actualizar estado')
      await fetchCitas()
      return { ok: true }
    } catch (e) {
      return { ok: false, error: networkErrorMessage(e) }
    }
  }

  /**
   * Cancela o elimina permanentemente una cita agendada.
   */
  async function eliminarCita(citaId) {
    try {
      const res = await fetch(`${API_BASE_URL}/citas/${citaId}`, {
        method: 'DELETE',
        headers: headers()
      })
      await parseApiResponse(res, 'Error al eliminar cita')
      await fetchCitas()
      return { ok: true }
    } catch (e) {
      return { ok: false, error: networkErrorMessage(e) }
    }
  }

  async function init() {
    const auth = useAuthStore()
    if (auth.isLoggedIn) await fetchCitas()
  }

  return {
    citas, loading, error,
    fetchCitas, agregarCita, actualizarEstado, eliminarCita, init
  }
})
