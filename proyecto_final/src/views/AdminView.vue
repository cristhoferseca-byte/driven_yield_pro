<template>
  <main class="admin-root">
    
    <!-- Background effects -->
    <div class="bg-grid"></div>
    <div class="bg-orb bg-orb-1"></div>
    
    <div class="admin-layout">
      <!-- SIDEBAR -->
      <aside class="sidebar matte-card observe-me">
        <div class="brand">
          <span class="brand-dot"></span>
          <div class="brand-text">
            <h2>DRIVEN YIELD</h2>
            <p>Admin Control</p>
          </div>
        </div>

        <nav class="sidebar-nav">
          <button :class="['nav-btn', { active: activeTab === 'dashboard' }]" @click="setTab('dashboard')">
            <span class="nav-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span> DASHBOARD
          </button>
          <button :class="['nav-btn', { active: activeTab === 'citas' }]" @click="setTab('citas')">
            <span class="nav-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span> ÓRDENES ({{ citas.filter(c=>c.estado==='pendiente').length }})
          </button>
          <button :class="['nav-btn', { active: activeTab === 'calendario' }]" @click="setTab('calendario')">
            <span class="nav-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg>️</span> CALENDARIO
          </button>
          <button :class="['nav-btn', { active: activeTab === 'clientes' }]" @click="setTab('clientes')">
            <span class="nav-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span> CLIENTES
          </button>
          <button :class="['nav-btn', { active: activeTab === 'servicios' }]" @click="setTab('servicios')">
            <span class="nav-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span> SERVICIOS
          </button>
        </nav>

        <div class="sidebar-bottom">
          <div class="sys-status">
            <span class="pulse-dot"></span> SERVIDOR CONECTADO
          </div>
          <button class="nav-btn text-red mt-2" @click="handleLogout">
            <span class="nav-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg>️</span> SALIR
          </button>
        </div>
      </aside>

      <!-- CONTENT -->
      <div class="content-area observe-me" style="transition-delay: 0.1s">
        
        <header class="topbar">
          <h1 class="page-title">
            {{ activeTab === 'dashboard' ? 'PANEL CENTRAL' : activeTab === 'citas' ? 'GESTOR DE CITAS' : activeTab === 'calendario' ? 'CRONOGRAMA' : activeTab === 'servicios' ? 'GESTOR DE SERVICIOS' : 'BASE DE CLIENTES' }}
          </h1>
          <div class="date-badge">{{ new Date().toLocaleDateString('es-CO') }}</div>
        </header>

        <!-- Print Only Header -->
        <div class="print-header">
          <h1>DRIVEN YIELD <span>PRO</span></h1>
          <p>REPORTE DE OPERACIONES Y RENDIMIENTO - {{ new Date().toLocaleDateString() }}</p>
          <hr class="print-divider" />
        </div>

        <transition name="fade" mode="out-in">
          
          <!-- DASHBOARD TAB -->
          <div v-if="activeTab === 'dashboard'" key="dash" class="tab-panel">
            <div v-if="loadingStats" class="loading-state">SINCRONIZANDO MÉTRICAS...</div>
            <div v-else class="kpi-grid">
              <div class="kpi-card matte-card">
                <p class="kpi-label">INGRESOS TOTALES</p>
                <h3 class="kpi-value text-primary">${{ stats.ingresos?.toLocaleString('es-CO') }} <span>COP</span></h3>
              </div>
              <div class="kpi-card matte-card">
                <p class="kpi-label">ÓRDENES COMPLETADAS</p>
                <h3 class="kpi-value">{{ stats.citas_completadas }}</h3>
              </div>
              <div class="kpi-card matte-card">
                <p class="kpi-label">ATENCIÓN PENDIENTE</p>
                <h3 class="kpi-value">{{ stats.citas_pendientes }}</h3>
              </div>
              <div class="kpi-card matte-card">
                <p class="kpi-label">CLIENTES REGISTRADOS</p>
                <h3 class="kpi-value">{{ stats.usuarios }}</h3>
              </div>
            </div>

            <div class="chart-section matte-card mt-4" v-if="!loadingStats">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <h3 class="chart-title" style="margin: 0;">REPORTE DE INGRESOS Y ÓRDENES</h3>
                <div style="display: flex; gap: 1rem;">
                  <select v-model="ingresosFiltro" class="filter-select">
                    <option value="dia">Hoy</option>
                    <option value="semana">Esta Semana</option>
                    <option value="mes">Este Mes</option>
                    <option value="anio">Este Año</option>
                    <option value="historico">Histórico Total</option>
                  </select>
                  <button class="btn btn-primary" @click="downloadPDF"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg> EXPORTAR PDF</button>
                </div>
              </div>

              <!-- Ingresos Filtered -->
              <div class="kpi-card matte-card" style="margin-bottom: 2rem; border-left: 4px solid var(--primary);">
                <p class="kpi-label">INGRESOS GENERADOS ({{ ingresosFiltro.toUpperCase() }})</p>
                <h3 class="kpi-value text-green">${{ ingresosFiltrados.toLocaleString('es-CO') }} <span>COP</span></h3>
              </div>

              <h3 class="chart-title">DISTRIBUCIÓN DE ESTADOS ({{ ingresosFiltro.toUpperCase() }})</h3>
              <div class="bar-chart">
                <div class="bar-wrap">
                  <div class="bar-label">Completadas ({{ Math.round((citasCompletadasFiltro / citasTotalFiltro)*100) || 0 }}%)</div>
                  <div class="bar-track"><div class="bar-fill fill-green" :style="`width: ${(citasCompletadasFiltro / citasTotalFiltro)*100}%`"></div></div>
                </div>
                <div class="bar-wrap mt-3">
                  <div class="bar-label">Pendientes ({{ Math.round((citasPendientesFiltro / citasTotalFiltro)*100) || 0 }}%)</div>
                  <div class="bar-track"><div class="bar-fill fill-yellow" :style="`width: ${(citasPendientesFiltro / citasTotalFiltro)*100}%`"></div></div>
                </div>
              </div>
              
              <h3 class="chart-title mt-4" style="margin-top: 3rem;">DETALLE DE ÓRDENES ({{ ingresosFiltro.toUpperCase() }})</h3>
              <div class="table-container matte-card mt-3">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th>FECHA / HORA</th>
                      <th>CLIENTE</th>
                      <th>VEHÍCULO</th>
                      <th>SERVICIO</th>
                      <th>VALOR</th>
                      <th>ESTADO</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="c in citasFiltradasPeriodo" :key="c.id">
                      <td>{{ c.fecha }} <br><span class="text-muted">{{ c.hora }}</span></td>
                      <td>{{ c.cliente }}</td>
                      <td><span class="placa-badge">{{ c.placa }}</span></td>
                      <td>{{ c.servicio }}</td>
                      <td>${{ c.monto?.toLocaleString('es-CO') || 0 }}</td>
                      <td><span :class="['status-badge', c.estado]">{{ c.estado }}</span></td>
                    </tr>
                    <tr v-if="citasFiltradasPeriodo.length === 0">
                      <td colspan="6" style="text-align: center; color: var(--text-muted); padding: 2rem;">No hay citas registradas en este periodo.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- CITAS TAB -->
          <div v-else-if="activeTab === 'citas'" key="citas" class="tab-panel">
            <div class="filter-bar matte-card">
              <input v-model="citaSearch" type="text" placeholder="Buscar placa, cliente o servicio..." class="search-input" />
              <select v-model="citaFilter" class="filter-select">
                <option value="todos">Todos los Estados</option>
                <option value="pendiente">Pendientes</option>
                <option value="confirmada">Confirmadas</option>
                <option value="completada">Completadas</option>
                <option value="cancelada">Canceladas</option>
              </select>
            </div>

            <div class="table-container matte-card mt-4">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>FECHA / HORA</th>
                    <th>CLIENTE</th>
                    <th>VEHÍCULO</th>
                    <th>SERVICIO</th>
                    <th>ESTADO</th>
                    <th>ACCIONES</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="c in filteredCitas" :key="c.id" @click="openEditModal(c)" class="clickable-row">
                    <td>{{ c.fecha }} <br><span class="text-muted">{{ c.hora }}</span></td>
                    <td>{{ c.cliente }}</td>
                    <td><span class="placa-badge">{{ c.placa }}</span></td>
                    <td>{{ c.servicio }}</td>
                    <td><span :class="['status-badge', c.estado]">{{ c.estado }}</span></td>
                    <td @click.stop>
                      <div class="actions">
                        <button class="btn-action act-ok" title="Confirmar" @click="updateEstado(c.id, 'confirmada')"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></button>
                        <button class="btn-action act-done" title="Completar" @click="updateEstado(c.id, 'completada')">◎</button>
                        <button class="btn-action act-cancel" title="Cancelar" @click="updateEstado(c.id, 'cancelada')"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="filteredCitas.length === 0">
                    <td colspan="6" class="text-center py-4">No se encontraron órdenes de servicio.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- CALENDAR TAB -->
          <div v-else-if="activeTab === 'calendario'" key="calendario" class="tab-panel">
            <div class="matte-card p-4 fc-wrapper">
              <FullCalendar ref="fullCalendarRef" :options="calendarOptions" />
            </div>
          </div>

          <!-- CLIENTES TAB -->
          <div v-else-if="activeTab === 'clientes'" key="clientes" class="tab-panel">
            <div class="table-container matte-card">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>NOMBRE</th>
                    <th>USUARIO</th>
                    <th>CONTACTO</th>
                    <th>ROL</th>
                    <th>ACCIONES</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="u in clientes" :key="u.id" class="clickable-row">
                    <td @click="openClienteModal(u.id)"><strong>{{ u.name || u.nombre }}</strong></td>
                    <td @click="openClienteModal(u.id)" class="text-muted">{{ u.username }}</td>
                    <td @click="openClienteModal(u.id)">{{ u.email }} <br><span class="text-muted">{{ u.phone || u.telefono || 'Sin teléfono' }}</span></td>
                    <td @click="openClienteModal(u.id)"><span class="status-badge completada">CLIENTE</span></td>
                    <td>
                      <button class="btn btn-danger btn-sm" @click.stop="inactivarCliente(u.id, u.name || u.nombre)">
                        INACTIVAR
                      </button>
                    </td>
                  </tr>
                  <tr v-if="clientes.length === 0">
                    <td colspan="5" class="text-center py-4">No hay clientes registrados.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- SERVICIOS TAB -->
          <div v-else-if="activeTab === 'servicios'" key="servicios" class="tab-panel">
            <div class="actions mb-3">
              <button class="btn btn-primary" @click="abrirModalServicio()">+ AGREGAR SERVICIO</button>
            </div>
            <div class="table-container matte-card">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>NOMBRE</th>
                    <th>CATEGORÍA</th>
                    <th>PRECIO</th>
                    <th>DURACIÓN</th>
                    <th>ACCIONES</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="s in servicios" :key="s.id">
                    <td><strong>{{ s.nombre }}</strong></td>
                    <td class="text-muted">{{ s.categoria }}</td>
                    <td>${{ s.precio }}</td>
                    <td>{{ s.duracion }}</td>
                    <td>
                      <button class="btn btn-ghost" @click="abrirModalServicio(s)">Editar</button>
                      <button class="btn btn-ghost text-red" @click="eliminarServicio(s.id)">Eliminar</button>
                    </td>
                  </tr>
                  <tr v-if="servicios.length === 0">
                    <td colspan="5" class="text-center py-4">No hay servicios registrados.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </transition>
      </div>
    </div>

    <!-- Edit Modal -->
    <transition name="modal-anim">
      <div v-if="showEditModal" class="success-overlay" @click.self="showEditModal = false">
        <div class="success-modal matte-card" style="max-width: 500px; text-align: left;">
          <h2 class="sm-title">EDITAR <span>CITA</span></h2>
          <p class="sm-sub">Modifica los detalles operativos y el mecánico.</p>
          
          <div class="form-group">
            <label>NUEVA FECHA</label>
            <input v-model="editForm.fecha" type="date" />
          </div>
          <div class="form-group mt-3">
            <label>NUEVA HORA</label>
            <input v-model="editForm.hora" type="time" />
          </div>
          <div class="form-group mt-3">
            <label>MECÁNICO ASIGNADO</label>
            <select v-model="editForm.id_mecanico" class="filter-select w-100">
              <option value="">Automático / Sin Asignar</option>
              <option v-for="m in mecanicosList" :key="m.id_mecanico" :value="m.id_mecanico">
                {{ m.nombre }} - {{ m.especialidad }}
              </option>
            </select>
          </div>
          
          <div class="sm-actions" style="margin-top: 2rem;">
            <button class="btn btn-ghost" @click="showEditModal = false">Cancelar</button>
            <button class="btn btn-primary" @click="submitEdit">Guardar Cambios</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Cliente Detail Modal -->
    <transition name="modal-anim">
      <div v-if="showClienteModal" class="success-overlay" @click.self="showClienteModal = false">
        <div class="success-modal matte-card" style="max-width: 800px; text-align: left; max-height: 90vh; overflow-y: auto;">
          <h2 class="sm-title">EXPEDIENTE <span>CLIENTE</span></h2>
          <p class="sm-sub" v-if="clienteDetalle">Información confidencial de {{ clienteDetalle.info.nombre }}</p>
          
          <div v-if="loadingCliente" class="loading-state">CARGANDO...</div>
          <div v-else-if="clienteDetalle">
            <!-- Credenciales (sin contraseñas) -->
            <div class="mb-4">
              <h4 style="color:var(--primary); margin-bottom: 10px;">CREDENCIALES</h4>
              <div class="sm-details">
                <div class="sm-row"><span>NOMBRE:</span> <strong>{{ clienteDetalle.info.nombre }}</strong></div>
                <div class="sm-row"><span>USUARIO:</span> <strong>{{ clienteDetalle.info.username }}</strong></div>
                <div class="sm-row"><span>EMAIL:</span> <strong>{{ clienteDetalle.info.email }}</strong></div>
                <div class="sm-row"><span>TELÉFONO:</span> <strong>{{ clienteDetalle.info.telefono || 'N/A' }}</strong></div>
              </div>
            </div>

            <!-- Vehículos -->
            <div class="mb-4">
              <h4 style="color:var(--primary); margin-bottom: 10px;">VEHÍCULOS</h4>
              <div v-if="clienteDetalle.vehiculos.length === 0" class="text-muted">Sin vehículos.</div>
              <div v-else class="vehicles-mini-grid" style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                <div v-for="v in clienteDetalle.vehiculos" :key="v.id" class="sm-details" style="margin-bottom:0">
                  <div class="sm-row"><span>MARCA:</span> <strong>{{ v.marca }} {{ v.modelo }}</strong></div>
                  <div class="sm-row"><span>AÑO:</span> <strong>{{ v.año }}</strong></div>
                  <div class="sm-row"><span>PLACA:</span> <strong>{{ v.placa || 'SIN PLACA' }}</strong></div>
                </div>
              </div>
            </div>

            <!-- Citas -->
            <div class="mb-4">
              <h4 style="color:var(--primary); margin-bottom: 10px;">ÓRDENES DE SERVICIO</h4>
              <div v-if="clienteDetalle.citas.length === 0" class="text-muted">Sin historial de citas.</div>
              <div v-else class="citas-mini-list" style="display:flex; flex-direction:column; gap:10px;">
                <div v-for="c in clienteDetalle.citas" :key="c.id" class="sm-details" style="margin-bottom:0">
                  <div style="display:flex; justify-content:space-between;">
                    <strong>{{ c.fecha }} | {{ c.hora }}</strong>
                    <span :class="['status-badge', c.estado]">{{ c.estado }}</span>
                  </div>
                  <div class="mt-2">{{ c.servicio }}</div>
                  <div class="text-muted" style="font-size: 0.8rem;">Vehículo: {{ c.vehiculo }} ({{ c.placa }})</div>
                  <div class="text-muted" style="font-size: 0.8rem;">Monto: ${{ c.monto }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="sm-actions" style="margin-top: 2rem;">
            <button class="btn btn-ghost" @click="showClienteModal = false">Cerrar</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Servicio Modal -->
    <transition name="modal-anim">
      <div v-if="modalServicio.open" class="success-overlay" @click.self="modalServicio.open = false">
        <div class="success-modal matte-card" style="max-width: 500px; text-align: left;">
          <h2 class="sm-title">{{ modalServicio.editando ? 'EDITAR' : 'NUEVO' }} <span>SERVICIO</span></h2>
          <p class="sm-sub">Define los datos del servicio ofrecido en el taller.</p>

          <div class="form-group">
            <label>NOMBRE *</label>
            <input v-model="modalServicio.form.nombre" type="text" placeholder="Ej: Cambio de Aceite" />
          </div>
          <div class="form-group mt-3">
            <label>CATEGORÍA *</label>
            <input v-model="modalServicio.form.categoria" type="text" placeholder="Ej: Mantenimiento" />
          </div>
          <div class="form-group mt-3">
            <label>PRECIO *</label>
            <input v-model.number="modalServicio.form.precio" type="number" placeholder="0" />
          </div>
          <div class="form-group mt-3">
            <label>DURACIÓN *</label>
            <input v-model="modalServicio.form.duracion" type="text" placeholder="Ej: 30 min" />
          </div>
          <div class="form-group mt-3">
            <label>DESCRIPCIÓN</label>
            <textarea v-model="modalServicio.form.descripcion" rows="3" class="filter-select w-100" placeholder="Descripción del servicio..."></textarea>
          </div>
          <div class="form-group mt-3">
            <label>IMAGEN (URL)</label>
            <input v-model="modalServicio.form.imagen" type="url" placeholder="https://..." />
          </div>

          <div class="sm-actions" style="margin-top: 2rem;">
            <button class="btn btn-ghost" @click="modalServicio.open = false">Cancelar</button>
            <button class="btn btn-primary" @click="guardarServicio">
              {{ modalServicio.editando ? 'Guardar Cambios' : 'Agregar Servicio' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

  </main>
</template>

<script setup>
import { ref, computed, onMounted, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCitasStore } from '../stores/citas'
import { useToast } from '../stores/toast'
import { API_BASE_URL } from '../config/api'

// FullCalendar imports
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import esLocale from '@fullcalendar/core/locales/es'

const auth = useAuthStore()
const citasStore = useCitasStore()
const router = useRouter()
const toast = useToast()

const activeTab = ref('dashboard')
const loadingStats = ref(true)
const stats = ref({})
const clientes = ref([])
const mecanicosList = ref([])
const citaSearch = ref('')
const citaFilter = ref('todos')

const servicios = ref([])
const modalServicio = reactive({
  open: false,
  editando: false,
  editId: null,
  form: { nombre: '', categoria: '', precio: 0, duracion: '', descripcion: '', imagen: '' },
})

// Ingresos Filter state
const ingresosFiltro = ref('mes')

/**
 * Determina si dos fechas pertenecen a la misma semana natural.
 * @param {Date} d1 - Primera fecha
 * @param {Date} d2 - Segunda fecha
 * @returns {boolean} True si coinciden en la misma semana
 */
function isSameWeek(d1, d2) {
  const diff = d1 - d2;
  return diff >= 0 && diff < 7 * 24 * 60 * 60 * 1000;
}

const citasFiltradasPeriodo = computed(() => {
  const hoy = new Date()
  return citasStore.citas.filter(c => {
    if(!c.fecha) return false
    const d = new Date(c.fecha + 'T00:00:00')
    if(ingresosFiltro.value === 'dia') return d.toDateString() === hoy.toDateString()
    if(ingresosFiltro.value === 'mes') return d.getMonth() === hoy.getMonth() && d.getFullYear() === hoy.getFullYear()
    if(ingresosFiltro.value === 'anio') return d.getFullYear() === hoy.getFullYear()
    if(ingresosFiltro.value === 'semana') return isSameWeek(hoy, d)
    return true // historico
  })
})

const ingresosFiltrados = computed(() => {
  return citasFiltradasPeriodo.value
    .filter(c => c.estado === 'completada')
    .reduce((sum, c) => sum + (c.monto || 0), 0)
})

const citasTotalFiltro = computed(() => citasFiltradasPeriodo.value.length)
const citasCompletadasFiltro = computed(() => citasFiltradasPeriodo.value.filter(c => c.estado === 'completada').length)
const citasPendientesFiltro = computed(() => citasFiltradasPeriodo.value.filter(c => c.estado === 'pendiente').length)

async function downloadPDF() {
  const pwd = prompt('Para exportar el reporte de ingresos, ingrese su contraseña de administrador:')
  if (!pwd) return
  
  // Verify password using admin login endpoint
  try {
    const res = await fetch(`${API_BASE_URL}/admin/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: auth.user.email, contrasena: pwd })
    })
    if (res.ok) {
      toast.success('Validación exitosa. Generando PDF...')
      setTimeout(() => window.print(), 500)
    } else {
      toast.error('Contraseña incorrecta. Acceso denegado.')
    }
  } catch (e) {
    toast.error('Error de red al verificar credenciales.')
  }
}

function setTab(tab) {
  activeTab.value = tab
  if (tab === 'calendario') {
    // Force FullCalendar to recalculate its dimensions after the transition completes
    setTimeout(() => window.dispatchEvent(new Event('resize')), 50)
    setTimeout(() => window.dispatchEvent(new Event('resize')), 300)
  }
}

// Modal state
const showEditModal = ref(false)
const editingCitaId = ref(null)
const editForm = ref({ fecha: '', hora: '', id_mecanico: '' })

// Modal Cliente state
const showClienteModal = ref(false)
const loadingCliente = ref(false)
const clienteDetalle = ref(null)

onMounted(async () => {
  if (!auth.user) await auth.init()
  if (auth.user?.role !== 'admin') {
    router.push('/')
    return
  }

  citasStore.fetchCitas()
  fetchStats()
  fetchClientes()
  fetchMecanicos()
  cargarServicios()

  setTimeout(() => {
    document.querySelectorAll('.observe-me').forEach(el => el.classList.add('is-visible'))
  }, 100)
})

const fullCalendarRef = ref(null)

const citas = computed(() => citasStore.citas)

const calendarOptions = ref({
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  initialView: 'timeGridWeek',
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay'
  },
  locale: esLocale,
  eventClick: (info) => {
    const cita = citas.value.find(x => x.id == info.event.id)
    if(cita) openEditModal(cita)
  },
  height: 'auto',
  slotMinTime: "08:00:00",
  slotMaxTime: "18:00:00",
  allDaySlot: false,
  events: []
})

watch(() => citas.value, (newCitas) => {
  calendarOptions.value.events = newCitas.map(c => ({
    id: String(c.id),
    title: `${c.cliente} - ${c.servicio}`,
    start: `${c.fecha}T${c.hora}`,
    color: c.estado === 'pendiente' ? '#f59e0b' : c.estado === 'completada' ? '#10b981' : c.estado === 'cancelada' ? '#ef4444' : '#3b82f6'
  }))
}, { deep: true, immediate: true })

async function fetchMecanicos() {
  try {
    const res = await fetch(`${API_BASE_URL}/citas/mecanicos`)
    if(res.ok) mecanicosList.value = await res.json()
  } catch(e) {
    mecanicosList.value = [
      {id_mecanico: 1, nombre: "Juan Perez (Demo)", especialidad: "General"}
    ]
  }
}

async function fetchStats() {
  loadingStats.value = true
  try {
    const res = await fetch(`${API_BASE_URL}/admin/stats`, { headers: auth.authHeaders() })
    if (res.ok) {
      stats.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  } finally {
    loadingStats.value = false
  }
}

async function fetchClientes() {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/usuarios`, { headers: auth.authHeaders() })
    if (res.ok) {
      clientes.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  }
}

async function inactivarCliente(uid, nombre) {
  if (!confirm(`¿Seguro que quieres inactivar a "${nombre}"? Ya no podrá iniciar sesión.`)) return
  try {
    const res = await fetch(`${API_BASE_URL}/admin/usuarios/${uid}`, {
      method: 'DELETE',
      headers: auth.authHeaders(),
    })
    if (res.ok) {
      clientes.value = clientes.value.filter(c => c.id !== uid)
    } else {
      alert('No se pudo inactivar al cliente.')
    }
  } catch (e) {
    console.error(e)
    alert('Error de conexión al intentar inactivar al cliente.')
  }
}

// ==================== SERVICIOS ====================
async function cargarServicios() {
  try {
    const res = await fetch(`${API_BASE_URL}/servicios`)
    if (res.ok) {
      servicios.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  }
}

function abrirModalServicio(serv = null) {
  if (serv) {
    modalServicio.editando = true
    modalServicio.editId = serv.id
    Object.assign(modalServicio.form, { ...serv })
  } else {
    modalServicio.editando = false
    modalServicio.editId = null
    Object.assign(modalServicio.form, { nombre: '', categoria: '', precio: 0, duracion: '', descripcion: '', imagen: '' })
  }
  modalServicio.open = true
}

async function guardarServicio() {
  const { nombre, categoria, precio, duracion } = modalServicio.form
  if (!nombre || !categoria || !precio || !duracion) { alert('Completa los campos obligatorios'); return }

  const url = modalServicio.editando
    ? `${API_BASE_URL}/servicios/${modalServicio.editId}`
    : `${API_BASE_URL}/servicios`
  const method = modalServicio.editando ? 'PUT' : 'POST'

  try {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json', ...auth.authHeaders() },
      body: JSON.stringify(modalServicio.form),
    })
    if (!res.ok) { alert('Error al guardar el servicio'); return }
    await cargarServicios()
    modalServicio.open = false
  } catch (e) {
    console.error(e)
    alert('Error al guardar el servicio')
  }
}

async function eliminarServicio(id) {
  if (!confirm('¿Eliminar este servicio?')) return
  try {
    const res = await fetch(`${API_BASE_URL}/servicios/${id}`, {
      method: 'DELETE',
      headers: auth.authHeaders(),
    })
    if (!res.ok) { alert('Error al eliminar el servicio'); return }
    servicios.value = servicios.value.filter(s => s.id !== id)
  } catch (e) {
    console.error(e)
    alert('Error al eliminar el servicio')
  }
}

async function openClienteModal(uid) {
  showClienteModal.value = true
  loadingCliente.value = true
  clienteDetalle.value = null
  try {
    const res = await fetch(`${API_BASE_URL}/admin/usuarios/${uid}`, { headers: auth.authHeaders() })
    if (res.ok) {
      clienteDetalle.value = await res.json()
    } else {
      toast.error('No se pudo cargar detalles del cliente')
    }
  } catch (e) {
    console.error(e)
  } finally {
    loadingCliente.value = false
  }
}

const filteredCitas = computed(() => citas.value.filter(c => {
  const mF = citaFilter.value === 'todos' || c.estado === citaFilter.value
  const mS = !citaSearch.value ||
    c.cliente.toLowerCase().includes(citaSearch.value.toLowerCase()) ||
    c.placa?.toLowerCase().includes(citaSearch.value.toLowerCase()) ||
    c.servicio.toLowerCase().includes(citaSearch.value.toLowerCase())
  return mF && mS
}))

async function updateEstado(id, estado) {
  const res = await citasStore.actualizarEstado(id, estado)
  if (res.ok) {
    toast.success(`Cita marcada como ${estado}`)
    fetchStats()
  } else {
    toast.error(res.error)
  }
}

function openEditModal(cita) {
  editingCitaId.value = cita.id
  editForm.value.fecha = cita.fecha
  editForm.value.hora = cita.hora
  editForm.value.id_mecanico = cita.id_mecanico || ''
  showEditModal.value = true
}

async function submitEdit() {
  const cita = citasStore.citas.find(c => c.id === editingCitaId.value)
  if (cita) {
    try {
      const res = await fetch(`${API_BASE_URL}/citas/${editingCitaId.value}`, {
        method: 'PUT',
        headers: auth.authHeaders(),
        body: JSON.stringify({
          cliente: cita.cliente,
          vehiculo: cita.vehiculo,
          servicio: cita.servicio,
          fecha: editForm.value.fecha,
          hora: editForm.value.hora,
          id_mecanico: editForm.value.id_mecanico ? parseInt(editForm.value.id_mecanico) : null
        })
      })
      if (res.ok) {
        toast.success('Cita actualizada exitosamente')
        citasStore.fetchCitas()
      } else {
        toast.error('Error actualizando cita')
      }
    } catch(e) { toast.error('Error de red') }
  }
  showEditModal.value = false
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-root {
  min-height: 100vh; background: var(--bg-base); padding-top: calc(var(--nav-height) + 2rem);
  position: relative; overflow: hidden; padding-bottom: 3rem;
}

.bg-grid {
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background-image: linear-gradient(rgba(230,0,35,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(230,0,35,0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}
.bg-orb {
  position: fixed; border-radius: 50%; filter: blur(90px); pointer-events: none; z-index: 0;
  width: 500px; height: 500px; background: radial-gradient(circle, rgba(230,0,35,0.05) 0%, transparent 70%); top: -100px; left: -100px;
}

.admin-layout {
  display: flex; gap: 2rem; max-width: 1400px; margin: 0 auto; padding: 0 2rem; position: relative; z-index: 1;
}

.sidebar {
  flex: 0 0 280px; padding: 2rem 1.5rem; display: flex; flex-direction: column; height: calc(100vh - 120px); position: sticky; top: 100px;
}
.brand { display: flex; align-items: center; gap: 1rem; margin-bottom: 3rem; padding-bottom: 1.5rem; border-bottom: var(--border-matte); }
.brand-dot { width: 12px; height: 12px; background: var(--primary); border-radius: 50%; box-shadow: 0 0 10px var(--primary); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
.brand-text h2 { font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; font-weight: 900; color: white; letter-spacing: 1px; }
.brand-text p { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 2px; }

.sidebar-nav { display: flex; flex-direction: column; gap: 0.5rem; flex: 1; }
.nav-btn {
  background: transparent; border: 1px solid transparent; color: var(--text-secondary);
  font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; font-weight: 700; text-align: left;
  padding: 1rem; border-radius: 6px; cursor: pointer; transition: all 0.3s; display: flex; align-items: center; gap: 0.8rem; letter-spacing: 1px;
}
.nav-btn:hover { background: rgba(255,255,255,0.03); color: white; }
.nav-btn.active { background: rgba(230,0,35,0.1); border-color: rgba(230,0,35,0.3); color: white; }
.nav-icon { font-size: 1.2rem; }
.text-red { color: var(--primary) !important; }
.text-red:hover { background: rgba(230,0,35,0.1); }

.sidebar-bottom { padding-top: 2rem; border-top: var(--border-matte); }
.sys-status { font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; color: #10b981; letter-spacing: 1px; display: flex; align-items: center; gap: 0.5rem; }
.pulse-dot { width: 6px; height: 6px; background: #10b981; border-radius: 50%; box-shadow: 0 0 8px #10b981; animation: pulse 2s infinite; }

.content-area { flex: 1; min-width: 0; }
.observe-me { opacity: 0; transform: translateY(20px); transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
.observe-me.is-visible { opacity: 1; transform: translateY(0); }

.topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.page-title { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 900; color: white; }
.date-badge { background: rgba(255,255,255,0.05); padding: 0.4rem 1rem; border-radius: 4px; font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; color: var(--text-muted); font-weight: 700; letter-spacing: 1px; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; }
.kpi-card { padding: 1.5rem; border-top: 2px solid transparent; transition: all 0.3s; }
.kpi-card:hover { transform: translateY(-3px); border-top-color: var(--primary); }
.kpi-label { font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; color: var(--text-muted); letter-spacing: 2px; margin-bottom: 0.5rem; }
.kpi-value { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 900; color: white; line-height: 1; }
.kpi-value span { font-size: 0.9rem; color: var(--primary); }
.text-primary { color: var(--primary) !important; text-shadow: 0 0 10px rgba(230,0,35,0.5); }

.chart-title { font-family: 'Space Grotesk', sans-serif; font-size: 1rem; color: white; margin-bottom: 1.5rem; letter-spacing: 1px; }
.chart-section { padding: 2rem; }
.bar-wrap { width: 100%; }
.bar-label { font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.5rem; font-weight: 700; }
.bar-track { width: 100%; height: 12px; background: rgba(255,255,255,0.05); border-radius: 6px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 6px; transition: width 1s cubic-bezier(0.16, 1, 0.3, 1); }
.fill-green { background: #10b981; box-shadow: 0 0 10px #10b981; }
.fill-yellow { background: #f59e0b; box-shadow: 0 0 10px #f59e0b; }

.filter-bar { padding: 1rem 1.5rem; display: flex; gap: 1rem; align-items: center; }
.search-input, .filter-select {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);
  padding: 0.8rem 1rem; color: white; font-family: 'Outfit', sans-serif; border-radius: 4px;
  outline: none; transition: border-color 0.3s;
}
.search-input { flex: 1; }
.search-input:focus, .filter-select:focus { border-color: var(--primary); }
.filter-select { cursor: pointer; color: var(--text-secondary); }
.filter-select option { background: var(--bg-deep); color: white; }
.w-100 { width: 100%; }

.table-container { overflow-x: auto; padding: 1rem; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th { font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; color: var(--text-muted); letter-spacing: 2px; padding: 1.2rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.1); }
.data-table td { padding: 1.2rem 1rem; font-size: 0.9rem; color: white; border-bottom: 1px solid rgba(255,255,255,0.03); vertical-align: middle; }
.data-table tbody tr:hover { background: rgba(255,255,255,0.02); }
.clickable-row { cursor: pointer; }

.placa-badge { background: rgba(255,255,255,0.1); padding: 0.3rem 0.6rem; border-radius: 4px; font-family: 'Space Grotesk', sans-serif; font-weight: 900; letter-spacing: 1px; border: 1px solid rgba(255,255,255,0.2); }
.text-muted { color: var(--text-muted); font-size: 0.8rem; }

.status-badge { font-family: 'Space Grotesk', sans-serif; font-size: 0.65rem; font-weight: 700; padding: 0.3rem 0.6rem; border-radius: 4px; text-transform: uppercase; letter-spacing: 1px; }
.pendiente { background: rgba(245,158,11,0.1); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.confirmada { background: rgba(59,130,246,0.1); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.completada { background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.cancelada { background: rgba(239,68,68,0.1); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }

.actions { display: flex; gap: 0.5rem; }
.btn-action { width: 30px; height: 30px; border-radius: 6px; border: 1px solid transparent; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; background: transparent; }
.act-ok { color: #60a5fa; border-color: rgba(59,130,246,0.3); }
.act-ok:hover { background: rgba(59,130,246,0.1); }
.act-done { color: #10b981; border-color: rgba(16,185,129,0.3); }
.act-done:hover { background: rgba(16,185,129,0.1); }
.act-cancel { color: #ef4444; border-color: rgba(239,68,68,0.3); }
.act-cancel:hover { background: rgba(239,68,68,0.1); }

/* FullCalendar Custom Theme Overrides */
.fc-wrapper {
  --fc-page-bg-color: transparent;
  --fc-neutral-bg-color: var(--bg-deep);
  --fc-border-color: rgba(220, 38, 38, 0.15); /* Subtle red border */
  --fc-button-text-color: white;
  --fc-button-bg-color: #1a0a0a; /* Very dark black/red */
  --fc-button-border-color: rgba(220, 38, 38, 0.3);
  --fc-button-hover-bg-color: rgba(220, 38, 38, 0.2);
  --fc-button-hover-border-color: rgba(220, 38, 38, 0.6);
  --fc-button-active-bg-color: #dc2626; /* Strong Red */
  --fc-button-active-border-color: #dc2626;
  --fc-today-bg-color: rgba(220, 38, 38, 0.08); /* Faint red today background */
  color: white;
  font-family: 'Outfit', sans-serif;
}
:deep(.fc-theme-standard td), :deep(.fc-theme-standard th) {
  border-color: var(--fc-border-color);
}
:deep(.fc-col-header-cell) {
  background-color: #1a0505;
}
:deep(.fc-col-header-cell-cushion), :deep(.fc-daygrid-day-number) {
  color: #ff9999;
  font-family: 'Space Grotesk', sans-serif;
}
:deep(.fc-event) {
  cursor: pointer;
  border-radius: 6px !important;
  padding: 4px 6px;
  font-size: 0.75rem !important;
  border: 1px solid rgba(220, 38, 38, 0.3) !important;
  background-color: #1a0a0a !important; /* Black background for events */
  color: #ffcccc !important; /* Redish text */
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.1);
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
}
:deep(.fc-event:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(220, 38, 38, 0.3);
  border-color: #dc2626 !important;
}
/* Multiline Events Fix */
:deep(.fc-event),
:deep(.fc-daygrid-event),
:deep(.fc-event-main),
:deep(.fc-event-title),
:deep(.fc-event-main-frame) {
  white-space: normal !important;
  word-wrap: break-word !important;
  word-break: break-word !important;
  overflow: visible !important;
  display: block !important;
  height: auto !important;
  min-height: max-content !important;
  line-height: 1.3 !important;
}
:deep(.fc-daygrid-event-harness),
:deep(.fc-daygrid-event-harness-abs) {
  height: auto !important;
}
:deep(.fc-toolbar-title) {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  color: white;
  font-size: 1.5rem !important;
  letter-spacing: -0.5px;
}
:deep(.fc-button) {
  border-radius: 6px !important;
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 0.5rem 1rem !important;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Modal CSS */
.success-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.9); backdrop-filter: blur(15px);
  z-index: 9999; display: flex; align-items: center; justify-content: center;
}
.success-modal { text-align: center; max-width: 500px; width: 90%; padding: 4rem 3rem; }
.sm-title { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 900; color: white; margin-bottom: 0.5rem; }
.sm-title span { color: var(--primary); }
.sm-sub { color: var(--text-secondary); margin-bottom: 2rem; }
.form-group label { display: block; font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700; color: var(--primary); letter-spacing: 2px; margin-bottom: 0.5rem; }
.form-group input { width: 100%; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 0.8rem 1rem; color: white; font-family: 'Outfit', sans-serif; border-radius: 4px; }
.form-group input:focus { border-color: var(--primary); outline: none; }
.mt-3 { margin-top: 1rem; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.print-header { display: none; }

@media (max-width: 1024px) {
  .admin-layout { flex-direction: column; }
  .sidebar { height: auto; position: relative; top: 0; flex: none; }
}
@media print {
  @page {
    size: A4;
    margin: 1.5cm;
  }
  html, body, .admin-root {
    background-color: #050505 !important;
    color: white !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  .sidebar, .topbar, .filter-bar, .actions, .modal-overlay, .success-overlay, button {
    display: none !important;
  }
  .print-header { display: block !important; margin-bottom: 2rem !important; }
  .print-header h1 { font-family: 'Space Grotesk', sans-serif; font-size: 28px !important; font-weight: 900 !important; color: white !important; margin: 0 !important; }
  .print-header h1 span { color: transparent !important; -webkit-text-stroke: 1px #e60023 !important; }
  .print-header p { color: #888 !important; font-size: 12px !important; margin-top: 5px !important; letter-spacing: 2px !important; }
  .print-divider { border-top: 1px solid rgba(230,0,35,0.4) !important; margin-top: 10px !important; border-bottom: none !important; }

  .content-area { margin: 0 !important; padding: 0 !important; width: 100% !important; }
  
  .table-container { overflow: visible !important; width: 100% !important; padding: 0 !important; }
  
  .matte-card { 
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    box-shadow: none !important;
    page-break-inside: avoid !important;
    margin-bottom: 20px !important;
    border-radius: 8px !important;
  }

  h1, h2, h3, p, span, div, td, th { color: white !important; text-shadow: none !important; }
  .text-muted { color: #888 !important; }
  
  .hero-title span { color: transparent !important; -webkit-text-stroke: 1px #e60023 !important; }

  .bar-track { background: rgba(255,255,255,0.1) !important; border: none !important; }
  .bar-fill.fill-green { background-color: #00ff88 !important; }
  .bar-fill.fill-yellow { background-color: #ffcc00 !important; }

  .data-table { width: 100% !important; table-layout: auto !important; }
  .data-table th { background: rgba(255,255,255,0.05) !important; border-bottom: 1px solid rgba(230,0,35,0.3) !important; color: #e60023 !important; font-size: 10px !important; }
  .data-table td { border-bottom: 1px solid rgba(255,255,255,0.05) !important; font-size: 11px !important; white-space: normal !important; word-wrap: break-word !important; word-break: break-word !important; }

  .status-badge { border: 1px solid rgba(255,255,255,0.2) !important; background: transparent !important; font-weight: 700 !important; }
  .status-badge.completada { border-color: #00ff88 !important; color: #00ff88 !important; }
  .status-badge.pendiente { border-color: #ffcc00 !important; color: #ffcc00 !important; }
  .status-badge.cancelada { border-color: #e60023 !important; color: #e60023 !important; }
  .status-badge.confirmada { border-color: #00ccff !important; color: #00ccff !important; }

  .stats-grid { display: grid !important; grid-template-columns: repeat(3, 1fr) !important; gap: 1rem !important; }
}
</style>