<template>
  <div class="calendar-wrapper">
    <FullCalendar :options="calendarOptions" />
    <div v-if="citaSeleccionada" class="modal-overlay" @click.self="cerrarModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>Detalle de cita</h3>
          <button class="modal-close" @click="cerrarModal">X</button>
        </div>
        <div class="modal-body">
          <div class="detail-row"><span class="detail-label">Cliente</span><span>{{ citaSeleccionada.extendedProps.cliente }}</span></div>
          <div class="detail-row"><span class="detail-label">Vehiculo</span><span>{{ citaSeleccionada.extendedProps.vehiculo }}</span></div>
          <div class="detail-row"><span class="detail-label">Servicio</span><span>{{ citaSeleccionada.title }}</span></div>
          <div class="detail-row"><span class="detail-label">Fecha</span><span>{{ citaSeleccionada.extendedProps.fecha }}</span></div>
          <div class="detail-row"><span class="detail-label">Hora</span><span>{{ citaSeleccionada.extendedProps.hora }}</span></div>
          <div class="detail-row"><span class="detail-label">Notas</span><span>{{ citaSeleccionada.extendedProps.notas || "-" }}</span></div>
          <div class="detail-row"><span class="detail-label">Monto</span><span>${{ citaSeleccionada.extendedProps.monto }}</span></div>
          <div class="detail-row"><span class="detail-label">Estado</span><span :class="'badge badge-' + citaSeleccionada.extendedProps.estado">{{ citaSeleccionada.extendedProps.estado }}</span></div>
        </div>
        <div class="modal-footer" v-if="isAdmin">
          <select v-model="nuevoEstado" class="estado-select">
            <option value="pendiente">Pendiente</option>
            <option value="confirmada">Confirmada</option>
            <option value="completada">Completada</option>
            <option value="cancelada">Cancelada</option>
          </select>
          <button class="btn-guardar" :disabled="cargando" @click="cambiarEstado">{{ cargando ? "Guardando..." : "Guardar" }}</button>
          <button class="btn-eliminar" :disabled="cargando" @click="eliminarEsta">Eliminar</button>
        </div>
        <div class="modal-footer" v-else-if="citaSeleccionada.extendedProps.estado === 'pendiente'">
          <button class="btn-eliminar" :disabled="cargando" @click="cancelarEsta">{{ cargando ? "Cancelando..." : "Cancelar cita" }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
import FullCalendar from "@fullcalendar/vue3"
import dayGridPlugin from "@fullcalendar/daygrid"
import timeGridPlugin from "@fullcalendar/timegrid"
import interactionPlugin from "@fullcalendar/interaction"
import listPlugin from "@fullcalendar/list"
import esLocale from "@fullcalendar/core/locales/es"
import { useCitasStore } from "@/stores/citas"
import { useAuthStore } from "@/stores/auth"
const citasStore = useCitasStore()
const authStore  = useAuthStore()
const isAdmin    = computed(() => authStore.isAdmin)
const citaSeleccionada = ref(null)
const nuevoEstado      = ref("")
const cargando         = ref(false)
const colores = {
  pendiente:  { backgroundColor: "#FAEEDA", borderColor: "#EF9F27", textColor: "#854F0B" },
  confirmada: { backgroundColor: "#E6F1FB", borderColor: "#378ADD", textColor: "#185FA5" },
  completada: { backgroundColor: "#EAF3DE", borderColor: "#639922", textColor: "#3B6D11" },
  cancelada:  { backgroundColor: "#FCEBEB", borderColor: "#E24B4A", textColor: "#A32D2D" },
}
const calendarOptions = ref({
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin, listPlugin],
  initialView: "dayGridMonth",
  headerToolbar: { left: "prev,next today", center: "title", right: "dayGridMonth,timeGridWeek,listMonth" },
  buttonText: { today: "Hoy", month: "Mes", week: "Semana", list: "Lista" },
  eventClick: handleEventClick,
  height: "auto",
  nowIndicator: true,
  locale: esLocale,
  events: []
})

import { watch } from 'vue'

watch(() => citasStore.citas, (newCitas) => {
  calendarOptions.value.events = newCitas.map(c => ({
    id:    String(c.id),
    title: c.servicio,
    start: c.fecha + "T" + c.hora,
    ...(colores[c.estado] || colores.pendiente),
    extendedProps: { cliente: c.cliente, vehiculo: c.vehiculo, fecha: c.fecha, hora: c.hora, notas: c.notas, monto: c.monto, estado: c.estado },
  }))
}, { deep: true, immediate: true })
/**
 * Maneja el clic en un evento del calendario abriendo el modal de detalle.
 */
function handleEventClick({ event }) {
  citaSeleccionada.value = event
  nuevoEstado.value = event.extendedProps.estado
}

/** Cierra el modal de detalle de cita. */
function cerrarModal() { citaSeleccionada.value = null }

/** Actualiza el estado de la cita seleccionada en el backend. */
async function cambiarEstado() {
  if (!citaSeleccionada.value || cargando.value) return
  cargando.value = true
  await citasStore.actualizarEstado(Number(citaSeleccionada.value.id), nuevoEstado.value)
  cargando.value = false
  cerrarModal()
}

/** Elimina la cita seleccionada del sistema. */
async function eliminarEsta() {
  if (!citaSeleccionada.value || cargando.value) return
  cargando.value = true
  await citasStore.eliminarCita(Number(citaSeleccionada.value.id))
  cargando.value = false
  cerrarModal()
}

/** Cancela la cita solicitada por el usuario cliente. */
async function cancelarEsta() {
  if (!citaSeleccionada.value || cargando.value) return
  cargando.value = true
  await citasStore.actualizarEstado(Number(citaSeleccionada.value.id), "cancelada")
  cargando.value = false
  cerrarModal()
}

</script>
<style scoped>
.calendar-wrapper { padding: 0.5rem 0; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; z-index: 9999; }
.modal-card { background: #1a1a1a; border-radius: 14px; width: 440px; max-width: 95vw; box-shadow: 0 8px 40px rgba(0,0,0,0.4); overflow: hidden; }
.modal-header { display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.25rem; border-bottom: 1px solid rgba(255,255,255,0.1); }
.modal-header h3 { font-size: 15px; font-weight: 500; margin: 0; color: #fff; }
.modal-close { background: none; border: none; cursor: pointer; color: rgba(255,255,255,0.5); font-size: 18px; }
.modal-body { padding: 1rem 1.25rem; display: flex; flex-direction: column; gap: 10px; }
.detail-row { display: flex; justify-content: space-between; font-size: 13px; color: rgba(255,255,255,0.7); }
.detail-label { font-weight: 500; color: #fff; }
.modal-footer { padding: 0.75rem 1.25rem; border-top: 1px solid rgba(255,255,255,0.1); display: flex; gap: 8px; }
.badge { padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: 500; }
.badge-pendiente { background: #FAEEDA; color: #854F0B; }
.badge-confirmada { background: #E6F1FB; color: #185FA5; }
.badge-completada { background: #EAF3DE; color: #3B6D11; }
.badge-cancelada { background: #FCEBEB; color: #A32D2D; }
.estado-select { flex: 1; padding: 7px 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); background: #2a2a2a; color: #fff; font-size: 13px; }
.btn-guardar { padding: 7px 16px; border-radius: 8px; border: none; background: #534AB7; color: #fff; cursor: pointer; font-size: 13px; }
.btn-eliminar { padding: 7px 16px; border-radius: 8px; border: none; background: #FCEBEB; color: #A32D2D; cursor: pointer; font-size: 13px; }
</style>
