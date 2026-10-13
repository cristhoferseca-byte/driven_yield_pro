<template>
  <main class="admin-root mecanicos-page">

    <!-- Background effects -->
    <div class="bg-grid"></div>
    <div class="bg-orb bg-orb-1"></div>

    <div class="content-area observe-me is-visible" style="max-width: 1200px; margin: 0 auto; z-index: 1; position: relative;">
      
      <!-- HEADER -->
      <header class="topbar" style="margin-bottom: 2rem;">
        <div>
          <h1 class="page-title">EQUIPO <span>TÉCNICO</span></h1>
          <p class="text-muted" style="font-family: 'Space Grotesk', sans-serif; letter-spacing: 1px;">Rendimiento, ingresos y gestión del equipo</p>
        </div>
        <button v-if="isAdmin" class="btn btn-primary" @click="abrirModalCrear">
          NUEVO MECÁNICO
        </button>
      </header>

      <!-- STATS GENERALES -->
      <div class="kpi-grid">
        <div class="kpi-card matte-card">
          <p class="kpi-label">TOTAL MECÁNICOS</p>
          <h3 class="kpi-value">{{ mecanicos.length }}</h3>
        </div>
        <div class="kpi-card matte-card">
          <p class="kpi-label">DISPONIBLES</p>
          <h3 class="kpi-value text-primary">{{ mecanicosDisponibles }}</h3>
        </div>
        <div class="kpi-card matte-card">
          <p class="kpi-label">CITAS ATENDIDAS</p>
          <h3 class="kpi-value">{{ totalCitas }}</h3>
        </div>
        <div class="kpi-card matte-card" style="border-top-color: #10b981;">
          <p class="kpi-label">INGRESOS TOTALES</p>
          <h3 class="kpi-value text-green">{{ formatPeso(totalIngresos) }}</h3>
        </div>
      </div>

      <!-- LOADING -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>SINCRONIZANDO BASE DE DATOS...</p>
      </div>

      <!-- ERROR -->
      <div v-else-if="error" class="error-state matte-card" style="margin-top: 2rem;">
        <p class="text-red">{{ error }}</p>
        <button @click="cargarMecanicos" class="btn btn-ghost mt-3">Reintentar Conexión</button>
      </div>

      <template v-else>

        <!-- RANKING TOP 3 -->
        <h3 class="section-title">TOP RENDIMIENTO FINANCIERO</h3>
        <div class="ranking-grid">
          <div
            v-for="(m, i) in rankingTop3"
            :key="m.id"
            class="ranking-card matte-card"
          >
            <div class="ranking-pos">0{{ i + 1 }}</div>
            <div class="ranking-info">
              <div class="ranking-nombre">{{ m.nombre }}</div>
              <div class="ranking-especialidad">{{ m.especialidad || 'General' }}</div>
            </div>
            <div class="ranking-stats">
              <div class="ranking-monto">{{ formatPeso(m.total_generado) }}</div>
              <div class="ranking-citas">{{ m.citas_completadas || 0 }} COMPLETADAS</div>
            </div>
          </div>
        </div>

        <!-- TABLA -->
        <h3 class="section-title">LISTADO OPERATIVO</h3>
        <div class="table-container matte-card">
          <table class="data-table">
            <thead>
              <tr>
                <th>OPERADOR</th>
                <th>TELÉFONO</th>
                <th>ESPECIALIDAD</th>
                <th>ESTADO</th>
                <th>ATENCIONES</th>
                <th>COMPLETADAS</th>
                <th>INGRESOS GENERADOS</th>
                <th v-if="isAdmin">ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="m in mecanicos"
                :key="m.id"
                @click="verDetalle(m)"
                class="clickable-row"
              >
                <td>
                  <div class="mecanico-nombre">
                    <div class="avatar">{{ m.nombre.charAt(0).toUpperCase() }}</div>
                    <div>
                      <strong>{{ m.nombre }}</strong>
                    </div>
                  </div>
                </td>
                <td style="color: var(--text-secondary)">{{ m.telefono || '—' }}</td>
                <td style="color: var(--text-secondary)">{{ m.especialidad || '—' }}</td>
                <td>
                  <span :class="['status-badge', m.disponible ? 'completada' : 'cancelada']">
                    {{ m.disponible ? 'ACTIVO' : 'INACTIVO' }}
                  </span>
                </td>
                <td>{{ m.total_citas || 0 }}</td>
                <td>{{ m.citas_completadas || 0 }}</td>
                <td class="text-green fw-bold">{{ formatPeso(m.total_generado) }}</td>
                <td v-if="isAdmin" @click.stop>
                  <div class="actions">
                    <button class="btn-action act-ok" title="Editar" @click="abrirModalEditar(m)"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></button>
                    <button class="btn-action act-cancel" title="Eliminar" @click="confirmarEliminar(m)"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

      </template>
    </div>

    <!-- MODAL DETALLE -->
    <transition name="fade">
      <div v-if="mecanicoDetalle" class="success-overlay" @click.self="mecanicoDetalle = null">
        <div class="success-modal matte-card" style="max-width: 600px; text-align: left;">
          <h2 class="sm-title">EXPEDIENTE <span>MECÁNICO</span></h2>
          <p class="sm-sub">{{ detalle?.mecanico?.nombre || 'Cargando...' }} - {{ detalle?.mecanico?.especialidad || 'General' }}</p>
          
          <div v-if="loadingDetalle" class="loading-state"><div class="spinner"></div></div>
          
          <template v-else-if="detalle">
            <div class="kpi-grid mb-4" style="grid-template-columns: repeat(2, 1fr);">
              <div class="kpi-card matte-card p-3">
                <p class="kpi-label">TOTAL SERVICIOS</p>
                <h3 class="kpi-value" style="font-size: 1.5rem;">{{ detalle.resumen.total_citas }}</h3>
              </div>
              <div class="kpi-card matte-card p-3">
                <p class="kpi-label">COMPLETADAS</p>
                <h3 class="kpi-value text-green" style="font-size: 1.5rem;">{{ detalle.resumen.completadas }}</h3>
              </div>
              <div class="kpi-card matte-card p-3">
                <p class="kpi-label">PENDIENTES</p>
                <h3 class="kpi-value text-yellow" style="font-size: 1.5rem;">{{ detalle.resumen.pendientes }}</h3>
              </div>
              <div class="kpi-card matte-card p-3">
                <p class="kpi-label">INGRESOS</p>
                <h3 class="kpi-value text-green" style="font-size: 1.5rem;">{{ formatPeso(detalle.resumen.total_generado) }}</h3>
              </div>
            </div>

            <h4 class="form-group label mb-3" style="color: var(--text-secondary); letter-spacing: 2px;">REGISTRO DE INTERVENCIONES</h4>
            <div class="table-container" style="max-height: 250px; overflow-y: auto;">
              <table class="data-table" style="font-size: 0.8rem;">
                <thead>
                  <tr>
                    <th>FECHA</th>
                    <th>CLIENTE</th>
                    <th>ESTADO</th>
                    <th>MONTO</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="detalle.citas.length === 0"><td colspan="4" class="text-center">Sin intervenciones</td></tr>
                  <tr v-for="c in detalle.citas" :key="c.id">
                    <td>{{ c.fecha }} {{ c.hora }}</td>
                    <td>{{ c.cliente }}</td>
                    <td><span :class="['status-badge', c.estado]">{{ c.estado }}</span></td>
                    <td class="text-green">{{ formatPeso(c.monto) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="sm-actions mt-4 text-right">
              <button class="btn btn-primary" @click="mecanicoDetalle = null">Cerrar Expediente</button>
            </div>
          </template>
        </div>
      </div>
    </transition>

    <!-- MODAL CREAR/EDITAR -->
    <transition name="fade">
      <div v-if="modalForm" class="success-overlay" @click.self="modalForm = false">
        <div class="success-modal matte-card" style="max-width: 500px; text-align: left;">
          <h2 class="sm-title">{{ editando ? 'ACTUALIZAR' : 'NUEVO' }} <span>OPERADOR</span></h2>
          <p class="sm-sub">Ingresa los datos del perfil técnico.</p>

          <div class="form-group">
            <label>NOMBRE COMPLETO</label>
            <input v-model="form.nombre" type="text" placeholder="Ej: Roberto Gómez" />
          </div>
          <div class="form-group mt-3">
            <label>ESPECIALIDAD</label>
            <select v-model="form.especialidad" class="filter-select w-100">
              <option value="">Seleccionar especialidad...</option>
              <option value="Mecánica General">Mecánica General</option>
              <option value="Electrónica Automotriz">Electrónica Automotriz</option>
              <option value="Frenos y Suspensión">Frenos y Suspensión</option>
              <option value="Transmisiones">Transmisiones</option>
              <option value="Aire Acondicionado">Aire Acondicionado</option>
              <option value="Motor y Afinación">Motor y Afinación</option>
            </select>
          </div>
          <div class="form-group mt-3">
            <label>TELÉFONO DE CONTACTO</label>
            <input v-model="form.telefono" type="tel" placeholder="Ej: 3001234567" />
          </div>
          <div class="form-group mt-3">
            <label>ESTADO OPERATIVO</label>
            <select v-model="form.disponible" class="filter-select w-100">
              <option :value="true">Activo / Disponible</option>
              <option :value="false">Inactivo / Fuera de Servicio</option>
            </select>
          </div>
          
          <p v-if="formError" class="text-red mt-3 text-center" style="font-size: 0.85rem;">{{ formError }}</p>

          <div class="sm-actions mt-4" style="display: flex; gap: 1rem; justify-content: flex-end;">
            <button class="btn btn-ghost" @click="modalForm = false">Cancelar</button>
            <button class="btn btn-primary" @click="guardarMecanico" :disabled="guardando">
              {{ guardando ? 'Guardando...' : (editando ? 'Actualizar' : 'Crear Registro') }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- MODAL CONFIRMAR ELIMINAR -->
    <transition name="fade">
      <div v-if="mecanicoAEliminar" class="success-overlay" @click.self="mecanicoAEliminar = null">
        <div class="success-modal matte-card" style="max-width: 450px; text-align: center;">
          <h2 class="sm-title" style="color: #ef4444;">ALERTA DE SISTEMA</h2>
          <p class="sm-sub mt-2">¿Confirmas la eliminación del expediente de <strong>{{ mecanicoAEliminar.nombre }}</strong>?</p>
          <p class="text-muted" style="font-size: 0.85rem; margin-top: 1rem;">Las órdenes de servicio vinculadas quedarán sin asignar.</p>
          
          <div class="sm-actions mt-4" style="display: flex; justify-content: center; gap: 1rem;">
            <button class="btn btn-ghost" @click="mecanicoAEliminar = null">Cancelar</button>
            <button class="btn btn-primary" style="background: #ef4444;" @click="eliminarMecanico" :disabled="eliminando">
              {{ eliminando ? 'Procesando...' : 'Confirmar Eliminación' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { API_BASE_URL } from '../config/api'

const auth    = useAuthStore()
const isAdmin = computed(() => auth.user?.role === 'admin')
const token   = computed(() => auth.token)
const API     = API_BASE_URL

const mecanicos         = ref([])
const loading           = ref(true)
const error             = ref(null)
const mecanicoDetalle   = ref(null)
const detalle           = ref(null)
const loadingDetalle    = ref(false)
const modalForm         = ref(false)
const editando          = ref(false)
const guardando         = ref(false)
const formError         = ref('')
const mecanicoAEliminar = ref(null)
const eliminando        = ref(false)
const form = ref({ nombre: '', especialidad: '', telefono: '', disponible: true })

const mecanicosDisponibles = computed(() => mecanicos.value.filter(m => m.disponible).length)
const totalCitas           = computed(() => mecanicos.value.reduce((s, m) => s + (m.total_citas || 0), 0))
const totalIngresos        = computed(() => mecanicos.value.reduce((s, m) => s + (m.total_generado || 0), 0))
const rankingTop3          = computed(() =>
  [...mecanicos.value].sort((a, b) => b.total_generado - a.total_generado).slice(0, 3)
)

/**
 * Formatea un valor numérico a moneda COP.
 * @param {number} v - Valor a formatear
 * @returns {string} Cadena en formato de moneda colombiana
 */
const formatPeso = (v) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(v || 0)

const badgeEstado = (e) => ({
  completada: 'badge-green',
  pendiente:  'badge-yellow',
  cancelada:  'badge-red',
  confirmada: 'badge-blue',
}[e] || 'badge-gray')

const headers = () => ({ 'Authorization': `Bearer ${token.value}`, 'Content-Type': 'application/json' })

/**
 * Carga la lista completa de mecánicos registrados en la base de datos.
 */
async function cargarMecanicos() {
  loading.value = true
  error.value   = null
  try {
    const r = await fetch(`${API}/mecanicos`)
    const d = await r.json()
    mecanicos.value = d.mecanicos || []
  } catch {
    error.value = 'No se pudo conectar con el servidor.'
  } finally {
    loading.value = false
  }
}

async function verDetalle(m) {
  mecanicoDetalle.value = m
  detalle.value         = null
  loadingDetalle.value  = true
  try {
    const r = await fetch(`${API}/mecanicos/${m.id}/ingresos`, { headers: headers() })
    detalle.value = await r.json()
  } catch {
    detalle.value = null
  } finally {
    loadingDetalle.value = false
  }
}

function abrirModalCrear() {
  editando.value  = false
  form.value      = { nombre: '', especialidad: '', telefono: '', disponible: true }
  formError.value = ''
  modalForm.value = true
}

function abrirModalEditar(m) {
  editando.value  = true
  form.value      = { nombre: m.nombre, especialidad: m.especialidad || '', telefono: m.telefono || '', disponible: m.disponible }
  formError.value = ''
  modalForm.value = true
  mecanicoDetalle.value = m
}

async function guardarMecanico() {
  if (!form.value.nombre.trim()) { formError.value = 'El nombre es obligatorio'; return }
  guardando.value = true
  formError.value = ''
  try {
    const id  = editando.value ? mecanicoDetalle.value.id : null
    const url = id ? `${API}/mecanicos/${id}` : `${API}/mecanicos`
    const r   = await fetch(url, { method: id ? 'PUT' : 'POST', headers: headers(), body: JSON.stringify(form.value) })
    if (!r.ok) { const e = await r.json(); formError.value = e.detail || 'Error al guardar'; return }
    modalForm.value = false
    await cargarMecanicos()
  } catch {
    formError.value = 'Error de conexión'
  } finally {
    guardando.value = false
  }
}

function confirmarEliminar(m) { mecanicoAEliminar.value = m }

async function eliminarMecanico() {
  eliminando.value = true
  try {
    await fetch(`${API}/mecanicos/${mecanicoAEliminar.value.id}`, { method: 'DELETE', headers: headers() })
    mecanicoAEliminar.value = null
    await cargarMecanicos()
  } catch {
    alert('Error al eliminar')
  } finally {
    eliminando.value = false
  }
}

onMounted(cargarMecanicos)
</script>

<style scoped>
.admin-root { min-height: 100vh; background: var(--bg-base); padding-top: calc(var(--nav-height) + 2rem); position: relative; overflow: hidden; padding-bottom: 3rem; }
.bg-grid { position: fixed; inset: 0; z-index: 0; pointer-events: none; background-image: linear-gradient(rgba(230,0,35,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(230,0,35,0.03) 1px, transparent 1px); background-size: 50px 50px; }
.bg-orb { position: fixed; border-radius: 50%; filter: blur(90px); pointer-events: none; z-index: 0; width: 500px; height: 500px; background: radial-gradient(circle, rgba(230,0,35,0.05) 0%, transparent 70%); top: -100px; left: -100px; }

.page-title { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 900; color: white; margin: 0; }
.page-title span { color: var(--primary); }
.topbar { display: flex; justify-content: space-between; align-items: flex-end; }

.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
.kpi-card { padding: 1.5rem; border-top: 2px solid transparent; transition: all 0.3s; }
.kpi-card:hover { transform: translateY(-3px); border-top-color: var(--primary); }
.kpi-label { font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; color: var(--text-muted); letter-spacing: 2px; margin-bottom: 0.5rem; }
.kpi-value { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 900; color: white; line-height: 1; margin: 0; }
.text-primary { color: var(--primary) !important; text-shadow: 0 0 10px rgba(230,0,35,0.5); }
.text-green { color: #10b981 !important; text-shadow: 0 0 10px rgba(16,185,129,0.3); }
.text-yellow { color: #f59e0b !important; text-shadow: 0 0 10px rgba(245,158,11,0.3); }
.fw-bold { font-weight: 700; }

.section-title { font-family: 'Space Grotesk', sans-serif; font-size: 1rem; color: white; margin-bottom: 1.5rem; letter-spacing: 1px; text-transform: uppercase; }

.ranking-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 3rem; }
.ranking-card { display: flex; align-items: center; padding: 1.5rem; border-left: 3px solid var(--primary); gap: 1.5rem; }
.ranking-pos { font-family: 'Space Grotesk', sans-serif; font-size: 3rem; font-weight: 900; color: rgba(255,255,255,0.1); line-height: 1; }
.ranking-info { flex: 1; }
.ranking-nombre { font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; font-weight: 700; color: white; margin-bottom: 0.2rem; }
.ranking-especialidad { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; }
.ranking-stats { text-align: right; }
.ranking-monto { font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; color: #10b981; font-weight: 700; }
.ranking-citas { font-size: 0.7rem; color: var(--text-secondary); letter-spacing: 1px; margin-top: 0.2rem; }

.table-container { overflow-x: auto; padding: 1rem; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th { font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; color: var(--text-muted); letter-spacing: 2px; padding: 1.2rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.1); }
.data-table td { padding: 1.2rem 1rem; font-size: 0.9rem; color: white; border-bottom: 1px solid rgba(255,255,255,0.03); vertical-align: middle; }
.clickable-row { cursor: pointer; transition: background 0.2s; }
.clickable-row:hover { background: rgba(255,255,255,0.02); }

.mecanico-nombre { display: flex; align-items: center; gap: 0.8rem; }
.avatar { width: 36px; height: 36px; border-radius: 4px; background: rgba(230,0,35,0.1); color: var(--primary); border: 1px solid rgba(230,0,35,0.3); display: flex; align-items: center; justify-content: center; font-weight: 900; font-family: 'Space Grotesk', sans-serif; }

.status-badge { font-family: 'Space Grotesk', sans-serif; font-size: 0.65rem; font-weight: 700; padding: 0.3rem 0.6rem; border-radius: 4px; text-transform: uppercase; letter-spacing: 1px; }
.completada { background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.cancelada { background: rgba(239,68,68,0.1); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
.pendiente { background: rgba(245,158,11,0.1); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }

.actions { display: flex; gap: 0.5rem; }
.btn-action { width: 30px; height: 30px; border-radius: 6px; border: 1px solid transparent; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; background: transparent; display: flex; align-items: center; justify-content: center; }
.act-ok { color: #60a5fa; border-color: rgba(59,130,246,0.3); }
.act-ok:hover { background: rgba(59,130,246,0.1); }
.act-cancel { color: #ef4444; border-color: rgba(239,68,68,0.3); }
.act-cancel:hover { background: rgba(239,68,68,0.1); }

.success-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.9); backdrop-filter: blur(15px); z-index: 9999; display: flex; align-items: center; justify-content: center; }
.success-modal { padding: 4rem 3rem; width: 90%; }
.sm-title { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 900; color: white; margin-bottom: 0.5rem; margin-top: 0; }
.sm-title span { color: var(--primary); }
.sm-sub { color: var(--text-secondary); margin-bottom: 2rem; font-size: 0.9rem; }

.form-group label { display: block; font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700; color: var(--primary); letter-spacing: 2px; margin-bottom: 0.5rem; }
.form-group input, .filter-select { width: 100%; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 0.8rem 1rem; color: white; font-family: 'Outfit', sans-serif; border-radius: 4px; outline: none; transition: border-color 0.3s; }
.form-group input:focus, .filter-select:focus { border-color: var(--primary); }
.filter-select option { background: var(--bg-deep); color: white; }
.w-100 { width: 100%; }

.loading-state { text-align: center; padding: 5rem; color: var(--primary); font-family: 'Space Grotesk', sans-serif; letter-spacing: 2px; font-weight: 700; }
.spinner { width: 40px; height: 40px; border: 3px solid rgba(230,0,35,0.2); border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 900px) {
  .ranking-grid { grid-template-columns: 1fr; }
  .topbar { flex-direction: column; align-items: flex-start; gap: 1rem; }
}
</style>