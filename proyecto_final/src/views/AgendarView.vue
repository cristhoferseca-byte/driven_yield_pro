<template>
  <main class="agendar-root">
    
    <!-- Ambient glow & grid -->
    <div class="ambient-glow fixed-glow"></div>
    <div class="bg-grid"></div>

    <!-- Hero -->
    <div class="agendar-hero observe-me">
      <div class="hero-eyebrow">
        <span class="eyebrow-line"></span>
        INICIALIZACIÓN DE PROTOCOLO
        <span class="eyebrow-line"></span>
      </div>
      <h1 class="hero-title">PROGRAMACIÓN DE<br /><span>SERVICIOS</span></h1>
      <p class="hero-sub">Complete la secuencia para asegurar su espacio en el hangar de mantenimiento.</p>
    </div>

    <div class="agendar-wrapper observe-me" style="transition-delay: 0.2s;">
      <div class="agendar-layout matte-card">

        <!-- Steps sidebar -->
        <div class="steps-sidebar">
          <div class="steps-track">
            <div
              v-for="(step, idx) in steps" :key="idx"
              :class="['step-node', {
                active: currentStep === idx + 1,
                completed: currentStep > idx + 1
              }]"
            >
              <div class="step-bubble">
                <transition name="bubble-swap" mode="out-in">
                  <span v-if="currentStep > idx + 1" key="check" class="check-mark"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span>
                  <span v-else key="num">0{{ idx + 1 }}</span>
                </transition>
              </div>
              <div class="step-info">
                <span class="step-name">{{ step.label }}</span>
                <span class="step-desc">{{ step.desc }}</span>
              </div>
              <div v-if="idx < steps.length - 1" class="step-connector">
                <div class="connector-fill" :class="{ filled: currentStep > idx + 1 }"></div>
              </div>
            </div>
          </div>

          <!-- Price preview -->
          <div v-if="selectedService" class="price-preview">
            <div class="pp-glitch-border"></div>
            <p class="pp-label">VALOR ESTIMADO</p>
            <p class="pp-value">${{ selectedService.precio }} COP</p>
            <p class="pp-service">{{ selectedService.name }}</p>
          </div>
        </div>

        <!-- Form area -->
        <div class="form-area">

          <!-- Progress bar -->
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: ((currentStep - 1) / (steps.length - 1) * 100) + '%' }"></div>
            <span class="progress-label">Fase 0{{ currentStep }} // 0{{ steps.length }}</span>
          </div>

          <transition name="step-slide" mode="out-in">

            <!-- STEP 1: Servicio -->
            <div v-if="currentStep === 1" key="s1" class="step-panel">
              <div class="step-panel-header">
                <div class="sph-num">01</div>
                <div>
                  <h2 class="sph-title">SELECCIÓN DE <span>MÓDULO</span></h2>
                  <p class="sph-sub">Determine el requerimiento técnico necesario.</p>
                </div>
              </div>

              <!-- Service cards grid -->
              <div class="services-grid">
                <button
                  v-for="(s, i) in serviciosData" :key="s.name"
                  :class="['service-opt-card', { selected: form.servicio === s.name }]"
                  :style="`animation-delay: ${i * 0.05}s`"
                  @click="form.servicio = s.name"
                >
                  <div class="sc-icon" v-html="s.icon"></div>
                  <div class="sc-info">
                    <span class="sc-name">{{ s.name }}</span>
                    <span class="sc-desc">{{ s.desc }}</span>
                  </div>
                  <span class="sc-price">${{ s.precio }} COP</span>
                </button>
              </div>

              <div class="form-group" style="margin-top:2rem">
                <label>ESPECIFICACIONES ADICIONALES</label>
                <textarea v-model="form.notas" rows="3" placeholder="Describa síntomas inusuales, ruidos o comportamientos erráticos de la máquina..."></textarea>
              </div>
            </div>

            <!-- STEP 2: Vehículo -->
            <div v-else-if="currentStep === 2" key="s2" class="step-panel">
              <div class="step-panel-header">
                <div class="sph-num">02</div>
                <div>
                  <h2 class="sph-title">DATOS DEL <span>VEHÍCULO</span></h2>
                  <p class="sph-sub">Seleccione un vehículo registrado o ingrese los datos.</p>
                </div>
              </div>

              <!-- Selector de vehículos -->
              <div class="vehicle-selector" style="margin-bottom: 2rem; display: flex; gap: 1rem; overflow-x: auto; padding-bottom: 0.5rem;">
                <button
                  v-for="v in userVehicles" :key="v.id_vehiculo"
                  :class="['vehicle-btn matte-card', { selected: selectedVehicleId === v.id_vehiculo }]"
                  @click="selectVehicle(v)"
                  style="flex: 0 0 auto; text-align: left; padding: 1rem; border-radius: 8px;"
                >
                  <strong style="display:block; color: white;">{{v.marca}} {{v.modelo}}</strong>
                  <span style="font-size: 0.8rem; color: var(--primary);">{{v.numero_de_placa}}</span>
                </button>
                <button
                  :class="['vehicle-btn matte-card', { selected: selectedVehicleId === 'manual' }]"
                  @click="selectVehicle('manual')"
                  style="flex: 0 0 auto; text-align: center; padding: 1rem; border-radius: 8px; border: 1px dashed rgba(255,255,255,0.2);"
                >
                  <strong style="display:block; color: white;">+ Nuevo Vehículo</strong>
                  <span style="font-size: 0.8rem; color: var(--text-muted);">Ingresar manual</span>
                </button>
              </div>

              <div class="fields-grid" :class="{'locked-fields': selectedVehicleId !== 'manual'}">
                <div class="form-group">
                  <label>FABRICANTE <span class="req">*</span></label>
                  <input v-model="form.marca" type="text" placeholder="Ej: Toyota, Ford" />
                </div>
                <div class="form-group">
                  <label>MODELO <span class="req">*</span></label>
                  <input v-model="form.modelo" type="text" placeholder="Ej: Mustang, Corolla" />
                </div>
                <div class="form-group">
                  <label>AÑO DE ENSAMBLAJE <span class="req">*</span></label>
                  <input v-model="form.anio" type="number" placeholder="YYYY" min="1950" :max="new Date().getFullYear() + 1" />
                </div>
                <div class="form-group">
                  <label>MATRÍCULA <span class="req">*</span></label>
                  <input v-model="form.placa" type="text" placeholder="ABC-123" style="text-transform:uppercase" />
                </div>
                <div class="form-group fields-span">
                  <label>COLOR EXTERIOR</label>
                  <input v-model="form.color" type="text" placeholder="Ej: Negro Mate, Rojo Metálico" />
                </div>
              </div>
            </div>

            <!-- STEP 3: Fecha -->
            <div v-else-if="currentStep === 3" key="s3" class="step-panel">
              <div class="step-panel-header">
                <div class="sph-num">03</div>
                <div>
                  <h2 class="sph-title">HORARIO DE <span>RECEPCIÓN</span></h2>
                  <p class="sph-sub">Establezca el momento de ingreso a nuestras instalaciones.</p>
                </div>
              </div>

              <div class="fields-grid">
                <div class="form-group">
                  <label>FECHA OPERATIVA <span class="req">*</span></label>
                  <input v-model="form.fecha" type="date" :min="minDate" />
                  <p v-if="dateError" class="text-red mt-1" style="font-size: 0.85rem; margin-top: 0.5rem; text-shadow: 0 0 10px rgba(239,68,68,0.5);">{{ dateError }}</p>
                </div>
                <div class="form-group">
                  <label>VENTANA DE TIEMPO <span class="req">*</span></label>
                  <select v-model="form.hora" :disabled="!form.fecha">
                    <option value="">Seleccionar horario...</option>
                    <option v-for="h in horas" :key="h" :value="h">{{ h }}</option>
                  </select>
                </div>

                <div class="form-group fields-span">
                  <label>MECÁNICO ASIGNADO</label>
                  <select v-model="form.id_mecanico">
                    <option value="">Asignación Automática</option>
                    <option v-for="m in filteredMecanicos" :key="m.id_mecanico" :value="m.id_mecanico">{{ m.nombre }} - {{ m.especialidad || 'General' }}</option>
                  </select>
                </div>

                <div class="form-group fields-span" style="margin-top:-0.5rem">
                  <div class="time-slots">
                    <button
                      v-for="h in horas" :key="h"
                      :class="['time-slot', { selected: form.hora === h }]"
                      @click="form.hora = h"
                    >
                      {{ h }}
                    </button>
                  </div>
                </div>

                <div class="form-group fields-span">
                  <label>IDENTIFICADOR DE USUARIO <span class="req">*</span></label>
                  <input v-model="form.cliente" type="text" placeholder="Nombre completo" />
                </div>
                <div class="form-group fields-span">
                  <label>CANAL DE COMUNICACIÓN</label>
                  <input v-model="form.telefono" type="tel" placeholder="+1 234 567 8900" />
                </div>
              </div>
            </div>

            <!-- STEP 4: Confirmar -->
            <div v-else-if="currentStep === 4" key="s4" class="step-panel">
              <div class="step-panel-header">
                <div class="sph-num">04</div>
                <div>
                  <h2 class="sph-title">REVISIÓN DE <span>PARÁMETROS</span></h2>
                  <p class="sph-sub">Verifique los datos antes de ejecutar la solicitud.</p>
                </div>
              </div>

              <div class="summary-grid">
                <div class="summary-section matte-card-sub">
                  <p class="ss-title">MÓDULO TÉCNICO</p>
                  <div class="ss-row"><span>TIPO</span><strong>{{ form.servicio }}</strong></div>
                  <div class="ss-row" v-if="form.notas"><span>ESPECIFICACIONES</span><strong>{{ form.notas }}</strong></div>
                </div>

                <div class="summary-section matte-card-sub">
                  <p class="ss-title">VEHÍCULO</p>
                  <div class="ss-row"><span>ID VINCULADA</span><strong>{{ form.marca }} {{ form.modelo }} {{ form.anio }}</strong></div>
                  <div class="ss-row"><span>MATRÍCULA</span><strong>{{ form.placa }}</strong></div>
                  <div class="ss-row" v-if="form.color"><span>PIGMENTO</span><strong>{{ form.color }}</strong></div>
                </div>

                <div class="summary-section matte-card-sub">
                  <p class="ss-title">RECEPCIÓN & ENLACE</p>
                  <div class="ss-row"><span>FECHA</span><strong>{{ form.fecha }}</strong></div>
                  <div class="ss-row"><span>HORA</span><strong>{{ form.hora }}</strong></div>
                  <div class="ss-row"><span>OPERADOR</span><strong>{{ form.cliente }}</strong></div>
                </div>
              </div>

              <div class="total-box">
                <div class="total-left">
                  <span class="total-label">COSTE ESTIMADO DE OPERACIÓN</span>
                  <span class="total-note">Sujeto a variaciones post-diagnóstico.</span>
                </div>
                <div class="total-price">${{ selectedService?.precio || '—' }} COP</div>
              </div>
            </div>

          </transition>

          <!-- Actions -->
          <div class="step-actions">
            <button class="btn btn-ghost" @click="currentStep--" :disabled="currentStep === 1">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:8px;"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg> Retroceder
            </button>
            <button v-if="currentStep < 4" class="btn btn-primary" @click="nextStep">
              Siguiente Fase <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-left:8px;"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </button>
            <button v-else class="btn btn-primary btn-confirm" @click="submitForm" :disabled="citasStore.loading">
              {{ citasStore.loading ? 'Procesando...' : 'Agendar Cita' }}
            </button>
          </div>

        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <transition name="modal-anim">
      <div v-if="showSuccess" class="success-overlay" @click.self="showSuccess = false">
        <div class="success-modal matte-card">
          <div class="success-ring">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          </div>
          <h2 class="sm-title">SECUENCIA <span>COMPLETADA</span></h2>
          <p class="sm-sub">Su solicitud ha sido procesada e ingresada en el sistema.</p>
          
          <div class="sm-details">
            <div class="sm-row"><span>MÓDULO:</span> <strong>{{ form.servicio }}</strong></div>
            <div class="sm-row"><span>HORARIO:</span> <strong>{{ form.fecha }} // {{ form.hora }}</strong></div>
            <div class="sm-row"><span>VEHÍCULO:</span> <strong>{{ form.marca }} {{ form.modelo }}</strong></div>
          </div>
          
          <div class="sm-actions">
            <router-link to="/" class="btn btn-ghost">Retornar al Sistema</router-link>
            <router-link to="/perfil?tab=citas" class="btn btn-primary">Ver Detalles</router-link>
          </div>
        </div>
      </div>
    </transition>
  </main>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useCitasStore } from '../stores/citas'
import { useToast } from '../stores/toast'
import { storeToRefs } from 'pinia'
import { API_BASE_URL } from '../config/api'
import { useRoute, useRouter } from 'vue-router'

const auth = useAuthStore()
const citasStore = useCitasStore()
const toast = useToast()
const route = useRoute()
const router = useRouter()
const { user } = storeToRefs(auth)

const currentStep = ref(1)
const showSuccess = ref(false)
const observer = ref(null)

onMounted(async () => {
  observer.value = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible')
      }
    })
  }, { threshold: 0.1 })

  document.querySelectorAll('.observe-me').forEach(el => observer.value.observe(el))

  try {
    const res = await fetch(`${API_BASE_URL}/citas/mecanicos`)
    if(res.ok) {
      const data = await res.json()
      mecanicos.value = data
    }
  } catch(e) {
    console.error("Error al cargar mecanicos:", e)
  }

  // Fetch Services
  try {
    const res = await fetch(`${API_BASE_URL}/servicios`)
    if(res.ok) {
      const data = await res.json()
      serviciosData.value = data.map(s => ({
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
        name: s.nombre,
        precio: s.precio.toLocaleString('es-CO'),
        desc: s.descripcion,
        precioRaw: s.precio,
        categoria: s.categoria
      }))
      
      const qService = route.query.servicioId
      if(qService) {
        const foundService = serviciosData.value.find(x => x.name === qService)
        if (foundService) {
          form.servicio = foundService.name
          currentStep.value = 2
        }
      }
    }
  } catch(e) {
    console.error("Error cargando servicios:", e)
  }

  // Fetch User Vehicles
  try {
    const res = await fetch(`${API_BASE_URL}/perfil`, { headers: auth.authHeaders() })
    if(res.ok) {
      const data = await res.json()
      userVehicles.value = data.vehiculos || []
      
      const qvId = route.query.vehiculoId
      if(qvId) {
        const v = userVehicles.value.find(x => x.id_vehiculo == qvId)
        if(v) selectVehicle(v)
      }
    }
  } catch(e) { console.error("Error cargando perfil:", e) }
})

onUnmounted(() => {
  if (observer.value) observer.value.disconnect()
})

const steps = [
  { label: 'Requerimiento',  desc: 'Tipo de servicio' },
  { label: 'Telemetría',     desc: 'Datos de máquina' },
  { label: 'Cronograma',     desc: 'Fecha y hora' },
  { label: 'Validación',     desc: 'Verificación' },
]

const form = reactive({
  servicio: '', notas: '',
  marca: '', modelo: '', anio: '', placa: '', color: '',
  fecha: '', hora: '', cliente: user.value?.nombre || '', telefono: user.value?.phone || '',
  id_mecanico: ''
})

const dateError = ref('')

const serviciosData = ref([])

const selectedService = computed(() => serviciosData.value.find(s => s.name === form.servicio))
const horas = ref([])
const mecanicos = ref([])

const categoryToSpecialty = {
  'Mantenimiento': 'Mecánica General',
  'Suspensión': 'Frenos y Suspensión',
  'Frenos': 'Frenos y Suspensión',
  'Diagnóstico': 'Electrónica Automotriz',
  'Eléctrico': 'Electrónica Automotriz',
  'Confort': 'Aire Acondicionado',
  'Transmisión': 'Transmisiones',
  'Motor': 'Motor y Afinación'
}

const filteredMecanicos = computed(() => {
  if (!selectedService.value || !selectedService.value.categoria) return mecanicos.value;
  const targetSpec = categoryToSpecialty[selectedService.value.categoria];
  const filtered = mecanicos.value.filter(m => m.especialidad === targetSpec || !m.especialidad || m.especialidad === 'Mecánica General');
  return filtered.length > 0 ? filtered : mecanicos.value;
})
const userVehicles = ref([])
const selectedVehicleId = ref('manual')
const tzOffset = (new Date()).getTimezoneOffset() * 60000
const localISOTime = (new Date(Date.now() - tzOffset)).toISOString().slice(0, 10)
const minDate = localISOTime

function selectVehicle(v) {
  if(v === 'manual') {
    selectedVehicleId.value = 'manual'
    form.marca = ''
    form.modelo = ''
    form.anio = ''
    form.placa = ''
    form.color = ''
  } else {
    selectedVehicleId.value = v.id_vehiculo
    form.marca = v.marca
    form.modelo = v.modelo
    form.anio = v.año || ''
    form.placa = v.numero_de_placa || ''
    form.color = v.color || ''
  }
}

watch(() => form.fecha, async (newFecha) => {
  dateError.value = ''
  if(!newFecha) { horas.value = []; return }
  try {
    const res = await fetch(`${API_BASE_URL}/citas/disponibilidad?fecha=${newFecha}`)
    if(res.ok) horas.value = await res.json()
  } catch(e) {
    // FALLBACK BYPASS DEMO
    horas.value = ['08:00', '10:00', '14:00', '16:00']
  }
})

/**
 * Valida la fase actual y avanza a la siguiente en el asistente de agendamiento.
 */
function nextStep() {
  if (currentStep.value === 1 && !form.servicio) { toast.error('Seleccione un módulo técnico.'); return }
  if (currentStep.value === 2) {
    if (selectedVehicleId.value === 'manual' && (!form.marca || !form.modelo || !form.anio || !form.placa)) {
      toast.error('Ingrese los datos requeridos del vehículo.')
      return
    }
  }
  if (currentStep.value === 3) {
    if (!form.fecha || !form.hora || !form.cliente) {
      toast.error('Establezca el cronograma y operador.')
      return
    }
    const selectedDate = new Date(form.fecha + 'T00:00:00')
    const today = new Date(minDate + 'T00:00:00')
    if (selectedDate < today) {
      dateError.value = 'Atención: No se puede agendar para fechas que ya pasaron.'
      toast.error('No se puede agendar para fechas pasadas.')
      return
    }
    dateError.value = ''
  }
  currentStep.value++
}

/**
 * Envía los datos del formulario de la cita al store de citas.
 */
async function submitForm() {
  const result = await citasStore.agregarCita({
    cliente:  form.cliente || '',
    vehiculo: `${form.marca || ''} ${form.modelo || ''} ${form.anio || ''}`.trim(),
    marca:    form.marca || '',
    modelo:   form.modelo || '',
    anio:     form.anio ? String(form.anio) : '',
    color:    form.color || '',
    placa:    form.placa || '',
    servicio: form.servicio || '',
    fecha:    form.fecha || '',
    hora:     form.hora || '',
    notas:    form.notas || '',
    monto:    selectedService.value?.precioRaw || 0,
    id_mecanico: form.id_mecanico ? parseInt(form.id_mecanico) : null,
  })
  if (result.ok) {
    showSuccess.value = true
  } else {
    toast.error(result.error || 'Error en la solicitud.')
  }
}
</script>

<style scoped>
/* AMBIENT & BASE */
.agendar-root {
  min-height: 100vh;
  padding-top: var(--nav-height);
  position: relative;
  overflow: hidden;
}

.fixed-glow {
  position: fixed;
  top: 10%; right: 10%;
  width: 700px; height: 700px;
  background: radial-gradient(circle, rgba(230,0,35,0.06) 0%, transparent 60%);
  z-index: 0;
  pointer-events: none;
}
.bg-grid {
  position: fixed; inset: 0; z-index: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 60px 60px; pointer-events: none;
}

/* ANIMATIONS */
.observe-me {
  opacity: 0; transform: translateY(30px);
  transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.observe-me.is-visible { opacity: 1; transform: translateY(0); }

/* HERO */
.agendar-hero {
  position: relative; z-index: 1;
  text-align: center;
  padding: 4rem 2rem 2rem;
  max-width: 900px;
  margin: 0 auto;
}
.hero-eyebrow {
  display: flex; align-items: center; justify-content: center; gap: 1rem;
  font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700;
  letter-spacing: 4px; color: var(--primary); margin-bottom: 1rem;
}
.eyebrow-line { width: 40px; height: 1px; background: rgba(230,0,35,0.5); }
.hero-title {
  font-family: 'Space Grotesk', sans-serif; font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 900; color: white; line-height: 1; letter-spacing: -1px; margin-bottom: 0.8rem;
}
.hero-title span { color: transparent; -webkit-text-stroke: 1px var(--primary); text-shadow: 0 0 20px rgba(230,0,35,0.3); }
.hero-sub { font-size: 1.05rem; color: var(--text-secondary); }

/* WRAPPER & LAYOUT */
.agendar-wrapper {
  position: relative; z-index: 1;
  max-width: 1200px; margin: 0 auto;
  padding: 0 2rem 5rem;
}
.agendar-layout {
  display: flex; gap: 0;
  padding: 0;
  border-radius: 16px;
}

/* SIDEBAR */
.steps-sidebar {
  flex: 0 0 300px;
  display: flex; flex-direction: column;
  background: rgba(0,0,0,0.3);
  border-right: var(--border-matte);
  padding: 3rem 2rem;
}
.steps-track { display: flex; flex-direction: column; flex: 1; gap: 1rem; }

.step-node { display: flex; align-items: flex-start; gap: 1.2rem; position: relative; padding-bottom: 2.5rem; }
.step-node:last-child { padding-bottom: 0; }

.step-bubble {
  width: 40px; height: 40px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; font-weight: 700;
  background: var(--bg-deep); border: var(--border-matte);
  color: var(--text-muted);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative; z-index: 2;
}
.step-node.active .step-bubble {
  background: var(--primary); border-color: var(--primary-light); color: white;
  box-shadow: 0 0 20px rgba(230,0,35,0.4);
}
.step-node.completed .step-bubble {
  background: rgba(255,255,255,0.05); color: white; border-color: rgba(255,255,255,0.3);
}

.step-info { display: flex; flex-direction: column; gap: 0.2rem; padding-top: 0.5rem; }
.step-name { font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem; font-weight: 700; color: var(--text-muted); transition: color 0.3s; text-transform: uppercase; letter-spacing: 1px; }
.step-node.active .step-name { color: white; }
.step-node.completed .step-name { color: var(--text-secondary); }
.step-desc { font-size: 0.75rem; color: var(--text-muted); }

.step-connector { position: absolute; left: 19px; top: 40px; bottom: 0; width: 2px; background: rgba(255,255,255,0.05); z-index: 1; }
.connector-fill { height: 0; width: 100%; background: var(--primary); transition: height 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
.connector-fill.filled { height: 100%; }

/* Price Preview */
.price-preview {
  margin-top: 3rem; padding: 1.5rem;
  background: rgba(230,0,35,0.03); border: 1px solid rgba(230,0,35,0.2);
  border-radius: 12px; text-align: center; position: relative; overflow: hidden;
}
.pp-glitch-border {
  position: absolute; top: 0; left: 0; width: 100%; height: 2px;
  background: var(--primary); animation: scanline 2s linear infinite;
}
@keyframes scanline { 0% { top: 0; opacity: 1; } 100% { top: 100%; opacity: 0; } }
.pp-label { font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; color: var(--primary); letter-spacing: 2px; margin-bottom: 0.5rem; }
.pp-value { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 900; color: white; line-height: 1; margin-bottom: 0.5rem; }
.pp-service { font-size: 0.8rem; color: var(--text-secondary); }

/* FORM AREA */
.form-area {
  flex: 1; padding: 3rem 4rem; display: flex; flex-direction: column; min-width: 0;
}

.progress-bar {
  height: 2px; background: rgba(255,255,255,0.05); border-radius: 2px;
  position: relative; margin-bottom: 3rem;
}
.progress-fill { height: 100%; background: var(--primary); transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
.progress-label {
  position: absolute; right: 0; top: 10px;
  font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; letter-spacing: 2px; color: var(--text-muted);
}

.step-panel { flex: 1; }

.step-panel-header { display: flex; align-items: center; gap: 1.5rem; margin-bottom: 3rem; }
.sph-num {
  font-family: 'Space Grotesk', sans-serif; font-size: 4rem; font-weight: 900;
  color: transparent; -webkit-text-stroke: 1px rgba(255,255,255,0.1);
  line-height: 1;
}
.sph-title { font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 900; color: white; margin-bottom: 0.3rem; letter-spacing: -0.5px; text-transform: uppercase; }
.sph-title span { color: var(--primary); }
.sph-sub { font-size: 0.95rem; color: var(--text-secondary); }

/* SERVICE CARDS GRID */
.services-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.2rem; }
.service-opt-card {
  display: flex; align-items: center; gap: 1rem; padding: 1.2rem;
  background: var(--bg-deep); border: var(--border-matte); border-radius: 12px;
  cursor: pointer; text-align: left; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  animation: fadeUp 0.4s ease both;
}
.service-opt-card:hover { border-color: rgba(255,255,255,0.2); transform: translateY(-3px); }
.service-opt-card.selected { border-color: var(--primary); background: rgba(230,0,35,0.05); box-shadow: 0 5px 20px rgba(230,0,35,0.2); }

.sc-icon { font-size: 2rem; filter: grayscale(100%); transition: filter 0.3s; }
.service-opt-card.selected .sc-icon { filter: grayscale(0%); }
.sc-info { flex: 1; }
.sc-name { display: block; font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 700; color: white; margin-bottom: 0.2rem; }
.sc-desc { display: block; font-size: 0.8rem; color: var(--text-secondary); }
.sc-price { font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: var(--primary); font-size: 1.1rem; }

/* FIELDS */
.fields-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.fields-span { grid-column: 1 / -1; }
.req { color: var(--primary); }

.time-slots { display: flex; flex-wrap: wrap; gap: 0.8rem; }
.time-slot {
  padding: 0.6rem 1.2rem;
  background: var(--bg-deep); border: var(--border-matte); border-radius: 6px;
  color: var(--text-secondary); font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; font-weight: 600;
  cursor: pointer; transition: all 0.2s;
}
.time-slot:hover { border-color: rgba(255,255,255,0.3); color: white; }
.time-slot.selected { background: var(--primary); border-color: var(--primary); color: white; box-shadow: var(--shadow-red); }

/* SUMMARY GRID */
.summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 2rem; }
.matte-card-sub {
  background: var(--bg-deep); border: var(--border-matte); border-radius: 12px; padding: 1.5rem;
}
.ss-title { font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 700; color: var(--primary); letter-spacing: 2px; margin-bottom: 1rem; }
.ss-row { margin-bottom: 0.8rem; }
.ss-row span { display: block; font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.2rem; }
.ss-row strong { font-size: 0.95rem; color: white; }

.total-box {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.5rem 2rem; background: rgba(230,0,35,0.05); border: 1px solid rgba(230,0,35,0.2); border-radius: 12px;
}
.total-left { display: flex; flex-direction: column; gap: 0.3rem; }
.total-label { font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 700; color: white; letter-spacing: 1px; }
.total-note { font-size: 0.8rem; color: var(--text-secondary); }
.total-price { font-family: 'Space Grotesk', sans-serif; font-size: 2.5rem; font-weight: 900; color: var(--primary); }

/* ACTIONS */
.step-actions {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 3rem; padding-top: 2rem; border-top: var(--border-matte);
}
.btn-confirm { background: var(--success); border-color: var(--success); box-shadow: 0 0 20px rgba(0,255,136,0.2); }
.btn-confirm:hover { background: #00cc6d; border-color: #00cc6d; box-shadow: 0 0 30px rgba(0,255,136,0.4); }

.step-slide-enter-active,.step-slide-leave-active { transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.step-slide-enter-from { opacity:0; transform:translateX(30px); }
.step-slide-leave-to   { opacity:0; transform:translateX(-30px); }

/* SUCCESS MODAL */
.success-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.9); backdrop-filter: blur(15px);
  z-index: 9999; display: flex; align-items: center; justify-content: center;
}
.success-modal { text-align: center; max-width: 500px; width: 90%; padding: 4rem 3rem; }
.success-ring {
  width: 80px; height: 80px; border-radius: 50%;
  background: var(--success); color: var(--bg-deep);
  display: flex; align-items: center; justify-content: center;
  font-size: 2.5rem; font-weight: 900; margin: 0 auto 2rem;
  box-shadow: 0 0 40px rgba(0,255,136,0.4);
  animation: popIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes popIn { 0% { transform: scale(0); } 70% { transform: scale(1.2); } 100% { transform: scale(1); } }
.sm-title { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 900; color: white; margin-bottom: 0.5rem; }
.sm-title span { color: var(--success); }
.sm-sub { color: var(--text-secondary); margin-bottom: 2rem; }
.sm-details {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05);
  border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; text-align: left;
}
.sm-row { display: flex; gap: 1rem; margin-bottom: 0.8rem; font-size: 0.9rem; }
.sm-row span { color: var(--text-muted); width: 100px; }
.sm-row strong { color: white; }
.sm-actions { display: flex; gap: 1rem; justify-content: center; }

@media (max-width: 900px) {
  .agendar-layout { flex-direction: column; }
  .steps-sidebar { border-right: none; border-bottom: var(--border-matte); padding: 2rem; flex: auto; }
  .steps-track { flex-direction: row; overflow-x: auto; }
  .step-node { flex-direction: column; align-items: center; padding-bottom: 0; padding-right: 2rem; }
  .step-connector { display: none; }
  .step-info { text-align: center; }
  .form-area { padding: 2rem; }
  .services-grid, .fields-grid, .summary-grid { grid-template-columns: 1fr; }
}

/* VEHICLE SELECTOR */
.vehicle-btn {
  border: 1px solid rgba(255,255,255,0.1); cursor: pointer; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  background: rgba(0,0,0,0.3);
}
.vehicle-btn:hover { border-color: rgba(255,255,255,0.3); transform: translateY(-2px); }
.vehicle-btn.selected {
  border-color: var(--primary); background: rgba(230,0,35,0.05); box-shadow: 0 5px 15px rgba(230,0,35,0.2);
}
.locked-fields { opacity: 0.7; pointer-events: none; }
</style>
