// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { API_BASE_URL, networkErrorMessage, parseApiResponse } from '../config/api'

const TOKEN_KEY = 'driven_yield_token'
export const useAuthStore = defineStore('auth', () => {
  const user    = ref(null)
  const token   = ref(sessionStorage.getItem(TOKEN_KEY) || null)
  const loading = ref(false)
  const error   = ref(null)
  const initialized = ref(false)
  let initPromise = null
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin    = computed(() => user.value?.role === 'admin')

  /**
   * Normaliza los campos del usuario para mantener consistencia en la interfaz.
   * @param {Object} data - Datos del usuario retornados por el backend
   * @returns {Object|null}
   */
  function normalizeUser(data) {
    if (!data) return null
    return {
      ...data,
      nombre: data.nombre || data.name || '',
      name: data.name || data.nombre || '',
      telefono: data.telefono || data.phone || '',
      phone: data.phone || data.telefono || '',
    }
  }

  /**
   * Retorna los encabezados HTTP estándar con el token de autorización si existe.
   * @returns {Object} Encabezados HTTP
   */
  function authHeaders() {
    return {
      'Content-Type': 'application/json',
      ...(token.value ? { Authorization: `Bearer ${token.value}` } : {})
    }
  }

  async function init() {
    if (initialized.value && (user.value || !token.value)) return user.value
    if (initPromise) return initPromise

    initPromise = (async () => {
      try {
        if (!token.value) {
          initialized.value = true
          return null
        }

        const res = await fetch(`${API_BASE_URL}/auth/me`, { headers: authHeaders() })
        if (res.ok) {
          user.value = normalizeUser(await res.json())
          return user.value
        }

        _clear()
        return null
      } catch {
        _clear()
        return null
      } finally {
        initialized.value = true
        initPromise = null
      }
    })()

    return initPromise
  }

  /**
   * Registra un nuevo usuario cliente y guarda la sesión automáticamente.
   */
  async function register(nombre, username, email, contrasena, telefono = '') {
    loading.value = true; error.value = null
    try {
      const res  = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, username, email, contrasena, telefono })
      })
      const data = await parseApiResponse(res, 'Error al registrar')
      _save(data.token, data.user)
      return { ok: true }
    } catch (e) {
      error.value = networkErrorMessage(e)
      return { ok: false, error: error.value }
    } finally { loading.value = false }
  }

  /**
   * Inicia sesión como cliente con nombre de usuario o email.
   */
  async function login(username, contrasena) {
    loading.value = true; error.value = null
    try {
      const res = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, contrasena })
      })
      const data = await parseApiResponse(res, 'Error al iniciar sesión')
      _save(data.token, data.user)
      return { ok: true }
    } catch (e) {
      error.value = networkErrorMessage(e)
      return { ok: false, error: error.value }
    } finally { loading.value = false }
  }

  /**
   * Inicia sesión en el portal de administración con credenciales de admin.
   */
  async function loginAdmin(email, contrasena) {
    loading.value = true; error.value = null
    try {
      const res = await fetch(`${API_BASE_URL}/admin/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, contrasena })
      })
      const data = await parseApiResponse(res, 'Credenciales de administrador inválidas')
      _save(data.token, data.user)
      return { ok: true }
    } catch (e) {
      error.value = networkErrorMessage(e)
      return { ok: false, error: error.value }
    } finally { loading.value = false }
  }

  async function updateProfile(datos) {
    loading.value = true; error.value = null
    try {
      const payload = {
        nombre: datos.nombre || datos.name,
        email: datos.email,
        telefono: datos.telefono || datos.phone,
      }
      const res = await fetch(`${API_BASE_URL}/perfil`, {
        method: 'PUT',
        headers: authHeaders(),
        body: JSON.stringify(payload)
      })
      await parseApiResponse(res, 'Error al actualizar perfil')
      user.value = normalizeUser({ ...user.value, ...payload })
      return { ok: true }
    } catch (e) {
      error.value = networkErrorMessage(e)
      return { ok: false, error: error.value }
    } finally { loading.value = false }
  }

  async function logout() {
    if (token.value) {
      try {
        await fetch(`${API_BASE_URL}/auth/logout`, { method: 'POST', headers: authHeaders() })
      } catch {}
    }
    _clear()
  }

  async function forgotPassword(email) {
    loading.value = true; error.value = null
    try {
      const res = await fetch(`${API_BASE_URL}/auth/forgot-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      })
      const data = await parseApiResponse(res, 'Error al solicitar recuperación')
      return { ok: true, message: data?.mensaje || 'Si el correo existe, recibirás instrucciones en breve.' }
    } catch (e) {
      error.value = networkErrorMessage(e)
      return { ok: false, error: error.value }
    } finally { loading.value = false }
  }

  async function resetPassword(resetToken, contrasena) {
    loading.value = true; error.value = null
    try {
      const res = await fetch(`${API_BASE_URL}/auth/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: resetToken, contrasena })
      })
      const data = await parseApiResponse(res, 'Error al restablecer contraseña')
      return { ok: true, message: data?.mensaje || 'Contraseña actualizada correctamente' }
    } catch (e) {
      error.value = networkErrorMessage(e)
      return { ok: false, error: error.value }
    } finally { loading.value = false }
  }

  function _save(t, u) {
    token.value = t
    user.value  = normalizeUser(u)
    initialized.value = true
    sessionStorage.setItem(TOKEN_KEY, t)
    // Limpieza de legacy
    sessionStorage.removeItem('driven yield_token')
  }

  function _clear() {
    token.value = null
    user.value  = null
    initialized.value = true
    sessionStorage.removeItem(TOKEN_KEY)
    // Limpieza de legacy
    sessionStorage.removeItem('driven yield_token')
  }

  async function getUsers() {
    try {
      const res = await fetch(`${API_BASE_URL}/admin/usuarios`, { headers: authHeaders() })
      const data = await parseApiResponse(res, 'Error al cargar usuarios')
      return data.map(normalizeUser)
    } catch {
      return []
    }
  }

  return {
    user, token, loading, error, initialized,
    isLoggedIn, isAdmin,
    authHeaders, init,
    register, login, loginAdmin, logout, updateProfile, forgotPassword, resetPassword, getUsers
  }
})