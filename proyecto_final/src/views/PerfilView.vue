<template>
  <main class="perfil-root">
    
    <!-- Background effects -->
    <div class="bg-grid"></div>
    <div class="bg-orb bg-orb-1"></div>
    <div class="bg-orb bg-orb-2"></div>

    <div class="perfil-header observe-me">
      <div class="header-inner">
        <div class="header-text">
          <p class="hero-eyebrow">CENTRO DE CONTROL DE CLIENTE</p>
          <h1 class="hero-title">GARAGE <span>VIRTUAL</span></h1>
          <p class="hero-sub">Historial de telemetría y mantenimientos de tu flota.</p>
        </div>
        <div class="user-badge">
          <div class="user-avatar">{{ user?.name?.charAt(0)?.toUpperCase() || 'U' }}</div>
          <div class="user-info">
            <span class="user-name">{{ user?.name }}</span>
            <span class="user-role"><span class="pulse-dot"></span> {{ user?.role === 'admin' ? 'ADMINISTRADOR' : 'CLIENTE' }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="perfil-layout">
      <!-- SIDEBAR -->
      <aside class="sidebar observe-me" style="transition-delay: 0.1s">
        <nav class="sidebar-nav matte-card">
          <button :class="['nav-btn', { active: activeTab === 'garage' }]" @click="activeTab = 'garage'">
            <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg></span> GARAGE Y VEHÍCULOS
          </button>
          <button :class="['nav-btn', { active: activeTab === 'citas' }]" @click="activeTab = 'citas'">
            <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></span> HISTORIAL DE SERVICIOS
          </button>
          <button :class="['nav-btn', { active: activeTab === 'info' }]" @click="activeTab = 'info'">
            <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span> CREDENCIALES
          </button>
          <button class="nav-btn text-red" @click="handleLogout">
            <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg></span> CERRAR SESIÓN
          </button>
        </nav>

        <div class="stats-card matte-card" style="margin-top: 1.5rem">
          <h4 class="stats-title">ESTADÍSTICAS GLOBALES</h4>
          <div class="stat-row">
            <span>Vehículos Registrados</span>
            <strong>{{ vehiculos.length }}</strong>
          </div>
          <div class="stat-row">
            <span>Servicios Totales</span>
            <strong>{{ citas.length }}</strong>
          </div>
          <div class="stat-row">
            <span>Citas Pendientes</span>
            <strong class="text-primary">{{ citas.filter(c => c.estado === 'pendiente').length }}</strong>
          </div>
        </div>
      </aside>

      <!-- CONTENT -->
      <div class="content-area observe-me" style="transition-delay: 0.2s">
        
        <!-- CARGANDO -->
        <div v-if="loadingData" class="loading-state">
          <div class="spinner"></div>
          <p>ESTABLECIENDO CONEXIÓN SEGURA...</p>
        </div>

        <transition v-else name="fade" mode="out-in">
          
          <!-- TAB: GARAGE -->
          <div v-if="activeTab === 'garage'" key="garage" class="tab-panel">
            <div class="panel-header">
              <h2 class="panel-title">FLOTA <span>REGISTRADA</span></h2>
              <p class="panel-desc">Vehículos vinculados a este perfil operativo.</p>
              <button class="btn btn-ghost mt-3" style="border: 1px solid rgba(255,255,255,0.2);" @click="showAddVehicle = !showAddVehicle">
                + AGREGAR VEHÍCULO
              </button>
            </div>
            
            <transition name="fade">
              <div v-if="showAddVehicle" class="matte-card form-container" style="margin-bottom: 2rem;">
                <h3 style="color: white; margin-bottom: 1rem;">Registrar Vehículo</h3>
                <div class="form-group">
                  <label>PLACA</label>
                  <input v-model="newVehicle.placa" type="text" placeholder="AAA-123" />
                </div>
                <div class="form-group">
                  <label>AÑO</label>
                  <input v-model="newVehicle.anio" type="number" placeholder="2022" />
                </div>
                <div class="form-group">
                  <label>MARCA</label>
                  <input v-model="newVehicle.marca" type="text" placeholder="Toyota" />
                </div>
                <div class="form-group">
                  <label>MODELO</label>
                  <input v-model="newVehicle.modelo" type="text" placeholder="Corolla" />
                </div>
                <div class="form-group">
                  <label>COLOR</label>
                  <input v-model="newVehicle.color" type="text" placeholder="Blanco" />
                </div>
                <button class="btn btn-primary mt-3" @click="addVehicle">GUARDAR VEHÍCULO</button>
              </div>
            </transition>

            <div v-if="vehiculos.length === 0" class="empty-state matte-card">
              <span class="empty-icon"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="9" x2="15" y1="9" y2="15"/><line x1="15" x2="9" y1="9" y2="15"/></svg></span>
              <h3>Sin vehículos registrados</h3>
              <p>Tu expediente está vacío. Los vehículos se registrarán automáticamente al agendar tu primer servicio.</p>
              <router-link to="/agendar" class="btn btn-primary mt-4">AGENDAR SERVICIO <svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></router-link>
            </div>

            <div v-else class="vehicles-grid">
              <div v-for="v in vehiculos" :key="v.id_vehiculo" class="vehicle-card matte-card">
                <div class="v-header">
                  <div class="v-plate">{{ v.numero_de_placa || 'SIN PLACA' }}</div>
                  <div class="v-year">{{ v.año }}</div>
                </div>
                <div class="v-body">
                  <h3 class="v-brand">{{ v.marca }}</h3>
                  <p class="v-model">{{ v.modelo }}</p>
                  <p class="v-color">Color: {{ v.color }}</p>
                </div>
                <div class="v-footer">
                  <router-link :to="{ path: '/agendar', query: { vehiculoId: v.id_vehiculo } }" class="btn btn-ghost btn-sm">
                    AGENDAR SERVICIO
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB: HISTORIAL CITAS -->
          <div v-else-if="activeTab === 'citas'" key="citas" class="tab-panel">
            <div class="panel-header">
              <h2 class="panel-title">HISTORIAL DE <span>CITAS</span></h2>
              <p class="panel-desc">Historial completo de intervenciones mecánicas.</p>
            </div>

            <div v-if="citas.length === 0" class="empty-state matte-card">
              <span class="empty-icon"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="9" x2="15" y1="9" y2="15"/><line x1="15" x2="9" y1="9" y2="15"/></svg></span>
              <h3>Sin historial de servicios</h3>
              <p>Aún no se han registrado intervenciones en tus vehículos.</p>
            </div>

            <div v-else class="timeline">
              <div v-for="(cita, idx) in citas" :key="cita.id" class="timeline-item">
                <div class="tl-dot"></div>
                <div class="tl-content matte-card">
                  <div class="tl-header">
                    <span class="tl-date">{{ cita.fecha }} | {{ cita.hora }}</span>
                    <span :class="['status-badge', cita.estado]">{{ cita.estado }}</span>
                  </div>
                  <h3 class="tl-service">{{ cita.servicio }}</h3>
                  <div class="tl-details">
                    <span>Monto: ${{ cita.monto }} COP</span>
                  </div>
                  <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                    <button v-if="cita.estado === 'pendiente'" class="btn btn-ghost btn-sm text-red" @click="cancelarCita(cita.id)">
                      CANCELAR ORDEN
                    </button>
                    <button v-if="cita.estado === 'pendiente'" class="btn btn-ghost btn-sm text-primary" @click="abrirEditarCita(cita)">
                      EDITAR ORDEN
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB: CREDENCIALES -->
          <div v-else-if="activeTab === 'info'" key="info" class="tab-panel">
            <div class="panel-header">
              <h2 class="panel-title">CREDENCIALES DE <span>ACCESO</span></h2>
              <p class="panel-desc">Modifica tu información de contacto y cifrado.</p>
            </div>

            <div class="form-container matte-card">
              <div class="form-group">
                <label>NOMBRE OPERATIVO</label>
                <input v-model="editForm.nombre" type="text" />
              </div>
              <div class="form-group">
                <label>CORREO DE CONTACTO</label>
                <input v-model="editForm.email" type="email" />
              </div>
              <div class="form-group">
                <label>TELÉFONO</label>
                <input v-model="editForm.telefono" type="tel" />
              </div>
              
              <hr class="form-divider" />
              
              <transition name="fade">
                <div v-if="showPasswordChange" class="password-change-box" style="margin-bottom: 2rem; padding: 1.5rem; background: rgba(0,0,0,0.3); border: 1px solid rgba(230,0,35,0.3); border-radius: 8px;">
                  <h4 style="color: white; margin-bottom: 1rem; font-family: 'Space Grotesk', sans-serif; display: flex; align-items: center; gap: 0.5rem;">
                    <span style="display:inline-flex; align-items:center; margin-right: 8px;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span> CAMBIO DE CREDENCIALES
                  </h4>
                  <p class="form-note">Por seguridad, ingrese su clave actual para habilitar el cambio:</p>
                  <div class="form-group">
                    <label>CLAVE ACTUAL</label>
                    <input v-model="editForm.contrasena_actual" type="password" placeholder="••••••••" />
                  </div>
                  
                  <transition name="fade">
                    <div class="form-group" v-if="editForm.contrasena_actual.length > 3">
                      <label style="color: var(--primary);">NUEVA CLAVE SEGURA</label>
                      <input v-model="editForm.contrasena_nueva" type="password" placeholder="••••••••" />
                    </div>
                  </transition>
                </div>
              </transition>

              <div class="form-actions" style="display: flex; flex-direction: column; gap: 1rem; margin-top: 1rem;">
                <button class="btn btn-primary" @click="saveProfile" :disabled="!hasChanges">
                  ACTUALIZAR DATOS
                </button>
                
                <button v-if="!showPasswordChange" class="btn btn-ghost" style="border: 1px dashed rgba(255,255,255,0.2); width: 100%; transition: all 0.3s;" @click="showPasswordChange = true">
                  <span style="display:inline-flex; align-items:center; margin-right: 8px;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span> MODIFICAR CONTRASEÑA DE ACCESO
                </button>
              </div>
            </div>
          </div>

        </transition>
      </div>
    </div>

    <!-- Edit Cita Modal -->
    <transition name="fade">
      <div v-if="showEditModal" class="password-change-box" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(5px);" @click.self="showEditModal = false">
        <div class="matte-card" style="width: 100%; max-width: 450px; padding: 2rem;">
          <h2 class="sm-title" style="margin-bottom: 0.5rem; color: white;">MODIFICAR <span style="color: var(--primary);">ORDEN</span></h2>
          <p class="form-note" style="margin-bottom: 1.5rem; color: var(--text-muted);">Puedes cambiar la fecha y hora de tu cita pendiente.</p>
          
          <div class="form-group">
            <label>NUEVA FECHA</label>
            <input v-model="editCitaForm.fecha" type="date" :min="new Date().toISOString().split('T')[0]" />
          </div>
          <div class="form-group mt-3">
            <label>NUEVA HORA</label>
            <input v-model="editCitaForm.hora" type="time" />
          </div>

          <div style="display: flex; gap: 1rem; margin-top: 2rem;">
            <button class="btn btn-primary" style="flex: 1;" @click="guardarEdicionCita">GUARDAR CAMBIOS</button>
            <button class="btn btn-ghost" style="flex: 1;" @click="showEditModal = false">CANCELAR</button>
          </div>
        </div>
      </div>
    </transition>
  </main>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCitasStore } from '../stores/citas'
import { useToast } from '../stores/toast'
import { storeToRefs } from 'pinia'
import { API_BASE_URL } from '../config/api'

const auth = useAuthStore()
const citasStore = useCitasStore()
const router = useRouter()
const route = useRoute()
const toast = useToast()
const { user } = storeToRefs(auth)

const activeTab = ref(route.query.tab || 'garage')
const loadingData = ref(true)
const vehiculos = ref([])
const citas = computed(() => citasStore.citas)
const observer = ref(null)

const editForm = ref({
  nombre: '', email: '', telefono: '', contrasena_actual: '', contrasena_nueva: ''
})

const originalData = ref({
  nombre: '', email: '', telefono: ''
})

const showPasswordChange = ref(false)
const showAddVehicle = ref(false)
const newVehicle = ref({ placa: '', anio: '', marca: '', modelo: '', color: '' })

// Modal Edit Cita
const showEditModal = ref(false)
const editCitaSelected = ref(null)
const editCitaForm = ref({ fecha: '', hora: '' })

const hasChanges = computed(() => {
  return editForm.value.nombre !== originalData.value.nombre ||
         editForm.value.email !== originalData.value.email ||
         editForm.value.telefono !== originalData.value.telefono ||
         (editForm.value.contrasena_nueva && editForm.value.contrasena_actual)
})

onMounted(async () => {
  if (!user.value) await auth.init()
  if (user.value?.role === 'admin') {
    router.push('/admin')
    return
  }

  editForm.value.nombre = user.value?.name || ''
  editForm.value.email = user.value?.email || ''
  editForm.value.telefono = user.value?.phone || ''
  
  originalData.value.nombre = editForm.value.nombre
  originalData.value.email = editForm.value.email
  originalData.value.telefono = editForm.value.telefono

  await citasStore.fetchCitas()
  await fetchPerfilData()

  // Intersection Observer for animations
  observer.value = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('is-visible') })
  }, { threshold: 0.1 })
  setTimeout(() => {
    document.querySelectorAll('.observe-me').forEach(el => observer.value?.observe(el))
  }, 100)
})

onUnmounted(() => {
  if (observer.value) observer.value.disconnect()
})

async function fetchPerfilData() {
  loadingData.value = true
  try {
    const res = await fetch(`${API_BASE_URL}/perfil`, { headers: auth.authHeaders() })
    if (res.ok) {
      const data = await res.json()
      vehiculos.value = data.vehiculos || []
    }
  } catch (e) {
    console.error(e)
    toast.error('Error de conexión.')
  } finally {
    loadingData.value = false
  }
}

/**
 * Guarda las modificaciones del perfil del usuario y/o actualización de clave en la base de datos.
 */
async function saveProfile() {
  if (!editForm.value.nombre || !editForm.value.email) {
    toast.error('Nombre y email son requeridos')
    return
  }
  const payload = {
    nombre: editForm.value.nombre,
    email: editForm.value.email,
    telefono: editForm.value.telefono
  }
  if (editForm.value.contrasena_nueva) {
    payload.contrasena_actual = editForm.value.contrasena_actual
    payload.contrasena_nueva = editForm.value.contrasena_nueva
  }

  try {
    const res = await fetch(`${API_BASE_URL}/perfil`, {
      method: 'PUT',
      headers: auth.authHeaders(),
      body: JSON.stringify(payload)
    })
    if (res.ok) {
      toast.success('Datos actualizados.')
      auth.user.name = payload.nombre
      auth.user.email = payload.email
      auth.user.phone = payload.telefono
      originalData.value.nombre = payload.nombre
      originalData.value.email = payload.email
      originalData.value.telefono = payload.telefono
      editForm.value.contrasena_actual = ''
      editForm.value.contrasena_nueva = ''
      showPasswordChange.value = false
    } else {
      const err = await res.json()
      toast.error(err.detail || 'Error al actualizar.')
    }
  } catch (e) {
    toast.error('Error de conexión.')
  }
}

async function addVehicle() {
  if (!newVehicle.value.placa || !newVehicle.value.anio || !newVehicle.value.marca || !newVehicle.value.modelo) {
    toast.error('Complete los datos principales del vehículo.')
    return
  }
  
  try {
    const payload = {
      numero_de_placa: newVehicle.value.placa,
      año: parseInt(newVehicle.value.anio),
      marca: newVehicle.value.marca,
      modelo: newVehicle.value.modelo,
      color: newVehicle.value.color
    }
    const res = await fetch(`${API_BASE_URL}/perfil/vehiculos`, {
      method: 'POST',
      headers: auth.authHeaders(),
      body: JSON.stringify(payload)
    })
    
    if (res.ok) {
      toast.success('Vehículo registrado.')
      showAddVehicle.value = false
      newVehicle.value = { placa: '', anio: '', marca: '', modelo: '', color: '' }
      await fetchPerfilData() // Recargar flota
    } else {
      const err = await res.json()
      toast.error(err.detail || 'Error al registrar vehículo.')
    }
  } catch (e) {
    toast.error('Error de conexión.')
  }
}

async function cancelarCita(id) {
  if(!confirm('¿Estás seguro de cancelar esta orden de servicio?')) return
  try {
    const res = await citasStore.actualizarEstado(id, 'cancelada')
    if (res.ok) {
      toast.success('Orden cancelada.')
    } else {
      toast.error('No se pudo cancelar.')
    }
  } catch (e) {
    toast.error('Error de red.')
  }
}

function abrirEditarCita(cita) {
  editCitaSelected.value = cita
  editCitaForm.value.fecha = cita.fecha
  editCitaForm.value.hora = cita.hora
  showEditModal.value = true
}

async function guardarEdicionCita() {
  if (!editCitaForm.value.fecha || !editCitaForm.value.hora) {
    toast.error('Por favor selecciona fecha y hora.')
    return
  }
  const payload = {
    cliente: editCitaSelected.value.cliente || auth.user.name,
    vehiculo: editCitaSelected.value.vehiculo || '',
    placa: editCitaSelected.value.placa || '',
    servicio: editCitaSelected.value.servicio,
    fecha: editCitaForm.value.fecha,
    hora: editCitaForm.value.hora,
    notas: editCitaSelected.value.notas || '',
    monto: editCitaSelected.value.monto || 0,
    id_mecanico: null
  }

  try {
    const res = await fetch(`${API_BASE_URL}/citas/${editCitaSelected.value.id}`, {
      method: 'PUT',
      headers: auth.authHeaders(),
      body: JSON.stringify(payload)
    })
    
    if (res.ok) {
      toast.success('Cita modificada con éxito.')
      showEditModal.value = false
      await citasStore.fetchCitas()
    } else {
      const err = await res.json()
      toast.error(err.detail || 'Error al modificar cita.')
    }
  } catch (e) {
    toast.error('Error de red.')
  }
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.perfil-root {
  min-height: 100vh; background: var(--bg-base); padding-top: var(--nav-height);
  position: relative; overflow: hidden;
}

.bg-grid {
  position: absolute; inset: 0; z-index: 0; pointer-events: none;
  background-image: linear-gradient(rgba(230,0,35,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(230,0,35,0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* Animations */
.observe-me { opacity: 0; transform: translateY(20px); transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
.observe-me.is-visible { opacity: 1; transform: translateY(0); }

/* Header */
.perfil-header { position: relative; z-index: 1; padding: 4rem 2rem 2rem; max-width: 1200px; margin: 0 auto; }
.header-inner { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: var(--border-matte); padding-bottom: 2rem; }
.hero-eyebrow { font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700; color: var(--primary); letter-spacing: 3px; margin-bottom: 0.5rem; }
.hero-title { font-family: 'Space Grotesk', sans-serif; font-size: 3rem; font-weight: 900; color: white; line-height: 1; margin-bottom: 0.5rem; }
.hero-title span { color: transparent; -webkit-text-stroke: 1px var(--primary); }
.hero-sub { color: var(--text-secondary); font-size: 1rem; }

.user-badge { display: flex; align-items: center; gap: 1rem; background: rgba(255,255,255,0.02); padding: 0.8rem 1.5rem; border-radius: 8px; border: var(--border-matte); }
.user-avatar { width: 50px; height: 50px; background: var(--primary); color: white; display: flex; align-items: center; justify-content: center; font-family: 'Space Grotesk', sans-serif; font-size: 1.5rem; font-weight: 900; border-radius: 4px; }
.user-info { display: flex; flex-direction: column; }
.user-name { color: white; font-weight: 700; font-size: 1.1rem; }
.user-role { color: var(--text-muted); font-size: 0.7rem; letter-spacing: 1px; display: flex; align-items: center; gap: 0.4rem; margin-top: 0.2rem; }
.pulse-dot { width: 6px; height: 6px; background: var(--primary); border-radius: 50%; box-shadow: 0 0 8px var(--primary); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* Layout */
.perfil-layout { display: flex; gap: 2rem; max-width: 1200px; margin: 0 auto; padding: 2rem; position: relative; z-index: 1; }
.sidebar { flex: 0 0 280px; }
.content-area { flex: 1; min-height: 500px; }

/* Sidebar Nav */
.sidebar-nav { display: flex; flex-direction: column; padding: 1rem; gap: 0.5rem; }
.nav-btn { background: transparent; border: 1px solid transparent; color: var(--text-secondary); font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; font-weight: 700; text-align: left; padding: 1rem; border-radius: 6px; cursor: pointer; transition: all 0.3s; display: flex; align-items: center; gap: 0.8rem; letter-spacing: 1px; }
.nav-btn:hover { background: rgba(255,255,255,0.03); color: white; }
.nav-btn.active { background: rgba(230,0,35,0.1); border-color: rgba(230,0,35,0.3); color: white; }
.nav-icon { font-size: 1.2rem; }
.text-red { color: var(--primary); }
.text-red:hover { background: rgba(230,0,35,0.1); }

.stats-card { padding: 1.5rem; }
.stats-title { font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; color: var(--text-muted); letter-spacing: 2px; margin-bottom: 1rem; }
.stat-row { display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.8rem; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 0.5rem; }
.stat-row strong { color: white; font-family: 'Space Grotesk', sans-serif; font-size: 1rem; }
.text-primary { color: var(--primary) !important; text-shadow: 0 0 10px rgba(230,0,35,0.5); }

/* Panels */
.panel-header { margin-bottom: 2rem; }
.panel-title { font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 900; color: white; line-height: 1; margin-bottom: 0.5rem; }
.panel-title span { color: transparent; -webkit-text-stroke: 1px var(--primary); }
.panel-desc { color: var(--text-secondary); font-size: 0.95rem; }

/* Garage Grid */
.vehicles-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
.vehicle-card { padding: 1.5rem; position: relative; overflow: hidden; border-top: 2px solid var(--primary); }
.vehicle-card::after { content: ''; position: absolute; top:0; right:0; width: 100px; height: 100px; background: radial-gradient(circle, rgba(230,0,35,0.1), transparent); pointer-events: none; }
.v-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.v-plate { background: rgba(255,255,255,0.1); padding: 0.4rem 0.8rem; border-radius: 4px; font-family: 'Space Grotesk', sans-serif; font-weight: 900; color: white; letter-spacing: 2px; border: 1px solid rgba(255,255,255,0.2); }
.v-year { color: var(--text-muted); font-size: 0.85rem; font-weight: 700; }
.v-brand { font-family: 'Space Grotesk', sans-serif; font-size: 1.5rem; font-weight: 900; color: white; line-height: 1.1; }
.v-model { color: var(--primary); font-size: 0.9rem; margin-bottom: 0.5rem; font-weight: 700; }
.v-color { color: var(--text-secondary); font-size: 0.85rem; }
.v-footer { margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.05); }

/* Timeline */
.timeline { position: relative; padding-left: 20px; border-left: 2px solid rgba(230,0,35,0.3); display: flex; flex-direction: column; gap: 2rem; }
.timeline-item { position: relative; }
.tl-dot { position: absolute; left: -27px; top: 15px; width: 12px; height: 12px; border-radius: 50%; background: var(--primary); box-shadow: 0 0 10px var(--primary); }
.tl-content { padding: 1.5rem; }
.tl-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.tl-date { font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; color: var(--text-muted); letter-spacing: 1px; }
.status-badge { font-family: 'Space Grotesk', sans-serif; font-size: 0.65rem; font-weight: 700; padding: 0.3rem 0.6rem; border-radius: 4px; text-transform: uppercase; letter-spacing: 1px; }
.pendiente { background: rgba(245,158,11,0.1); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.completada { background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.cancelada { background: rgba(239,68,68,0.1); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
.tl-service { font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; font-weight: 700; color: white; margin-bottom: 0.5rem; }
.tl-details { color: var(--text-secondary); font-size: 0.9rem; }

/* Forms */
.form-container { padding: 2rem; max-width: 600px; }
.form-group { margin-bottom: 1.5rem; }
.form-group label { display: block; font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700; color: var(--primary); letter-spacing: 2px; margin-bottom: 0.5rem; }
.form-group input { width: 100%; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 0.8rem 1rem; color: white; font-family: 'Outfit', sans-serif; border-radius: 4px; transition: border-color 0.3s; }
.form-group input:focus { border-color: var(--primary); outline: none; }
.form-divider { border: 0; height: 1px; background: rgba(255,255,255,0.1); margin: 2rem 0; }
.form-note { color: var(--text-muted); font-size: 0.8rem; margin-bottom: 1rem; }

/* Utilities */
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-icon { font-size: 3rem; color: rgba(255,255,255,0.1); display: block; margin-bottom: 1rem; }
.empty-state h3 { font-family: 'Space Grotesk', sans-serif; color: white; margin-bottom: 0.5rem; font-size: 1.4rem; }
.empty-state p { color: var(--text-secondary); font-size: 0.9rem; }
.loading-state { text-align: center; padding: 5rem; color: var(--primary); font-family: 'Space Grotesk', sans-serif; letter-spacing: 2px; font-weight: 700; }
.spinner { width: 40px; height: 40px; border: 3px solid rgba(230,0,35,0.2); border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 900px) {
  .perfil-layout { flex-direction: column; }
  .sidebar { flex: none; }
  .header-inner { flex-direction: column; align-items: flex-start; gap: 1.5rem; }
}
</style>
