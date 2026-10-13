/**
 * URL base para las peticiones a la API del backend.
 */
export const API_BASE_URL = (import.meta.env.VITE_API_URL || 'https://localhost:8000/api').replace(/\/$/, '')

/**
 * Parsea la respuesta HTTP recibida y lanza un error descriptivo si el estatus no es OK.
 * 
 * @param {Response} res - Objeto Response retornado por fetch
 * @param {string} fallbackMessage - Mensaje por defecto en caso de error
 * @returns {Promise<any>} Objeto JSON parseado
 */
export async function parseApiResponse(res, fallbackMessage = 'Error en la solicitud') {
  let data = null

  try {
    data = await res.json()
  } catch {
    data = null
  }

  if (!res.ok) {
    let message = data?.mensaje || fallbackMessage
    if (data?.detail) {
      if (Array.isArray(data.detail)) {
        message = data.detail.map(e => e.msg).join(', ')
      } else {
        message = data.detail
      }
    }
    const error = new Error(message)
    error.status = res.status
    throw error
  }

  return data
}

/**
 * Retorna un mensaje de error amigable para el usuario según el estatus o tipo de error.
 * 
 * @param {Error|any} error - Objeto de error capturado
 * @returns {string} Mensaje de error formateado
 */
export function networkErrorMessage(error) {
  if (error?.status === 401) return 'Tu sesión expiró. Inicia sesión nuevamente.'
  if (!error?.status && error instanceof TypeError) {
    return 'No se pudo conectar con el servidor. Verifica que el backend esté encendido.'
  }
  if (error?.message) return error.message
  return 'No se pudo conectar con el servidor. Verifica que el backend esté encendido.'
}