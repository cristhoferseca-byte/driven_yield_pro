<template>
  <main class="calendario-root">
    <div class="cal-hero">
      <p class="hero-eyebrow">{{ isAdmin ? "Panel de gestión" : "Mis reservas" }}</p>
      <h1 class="hero-title">{{ isAdmin ? "Driven Yield" : "Driven Yield" }} <span>Citas</span></h1>
      <p class="hero-sub">{{ isAdmin ? "Visualiza y gestiona todas las citas del taller" : "Consulta y administra tus citas agendadas" }}</p>
    </div>
    <div class="stats-row">
      <div class="stat-card"><span class="stat-num">{{ totalPendientes }}</span><span class="stat-label">Pendientes</span><div class="stat-dot dot-pendiente"></div></div>
      <div class="stat-card"><span class="stat-num">{{ totalConfirmadas }}</span><span class="stat-label">Confirmadas</span><div class="stat-dot dot-confirmada"></div></div>
      <div class="stat-card"><span class="stat-num">{{ totalCompletadas }}</span><span class="stat-label">Completadas</span><div class="stat-dot dot-completada"></div></div>
      <div class="stat-card"><span class="stat-num">{{ totalCanceladas }}</span><span class="stat-label">Canceladas</span><div class="stat-dot dot-cancelada"></div></div>
    </div>
    <div class="cal-container">
      <div v-if="citasStore.loading" class="loading-state"><div class="spinner"></div><p>Cargando citas...</p></div>
      <div v-else-if="citasStore.error" class="error-state"><p>Error: {{ citasStore.error }}</p></div>
      <div class="fc-wrapper"><CitasCalendar /></div>
    </div>
    <div class="cal-actions" v-if="!isAdmin">
      <router-link to="/agendar" class="btn-agendar">+ Nueva cita</router-link>
    </div>
  </main>
</template>

<script setup>
import { computed, onMounted } from "vue"
import CitasCalendar from "@/components/CitasCalendar.vue"
import { useCitasStore } from "@/stores/citas"
import { useAuthStore } from "@/stores/auth"

const citasStore = useCitasStore()
const authStore  = useAuthStore()
const isAdmin    = computed(() => authStore.isAdmin)

// Contadores reactivos por estado de cita para la barra de estadísticas
const totalPendientes  = computed(() => citasStore.citas.filter(c => c.estado === "pendiente").length)
const totalConfirmadas = computed(() => citasStore.citas.filter(c => c.estado === "confirmada").length)
const totalCompletadas = computed(() => citasStore.citas.filter(c => c.estado === "completada").length)
const totalCanceladas  = computed(() => citasStore.citas.filter(c => c.estado === "cancelada").length)

onMounted(() => citasStore.fetchCitas())
</script>

<style scoped>
.calendario-root { min-height: 100vh; padding: 2rem 1.5rem 4rem; }

.cal-hero { text-align: center; margin-bottom: 2rem; }
.hero-eyebrow { font-size: 12px; font-weight: 500; letter-spacing: .12em; text-transform: uppercase; color: #534AB7; margin-bottom: .5rem; }
.hero-title { font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 700; margin-bottom: .5rem; }
.hero-title span { color: #dc2626; }
.hero-sub { color: var(--color-text-secondary); font-size: 1rem; }

.stats-row { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 2rem; }
.stat-card {
  background: var(--color-background-secondary, #1a1a1a);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: .9rem 1.4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 110px;
  position: relative;
  overflow: hidden;
}
.stat-num   { font-size: 1.8rem; font-weight: 700; line-height: 1; }
.stat-label { font-size: 12px; color: rgba(255,255,255,0.5); }

/* <svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg> Corregido: CSS válido con background y colores correctos */
.stat-dot { position: absolute; bottom: 0; left: 0; right: 0; height: 3px; }
.dot-pendiente  { background: #f59e0b; }
.dot-confirmada { background: #534AB7; }
.dot-completada { background: #22c55e; }
.dot-cancelada  { background: #6b7280; }

.cal-container {
  background: var(--color-background-secondary, #1a1a1a);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 1.5rem;
  max-width: 1100px;
  margin: 0 auto;
}
.loading-state, .error-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 3rem; }
.spinner {
  width: 32px; height: 32px;
  border-radius: 50%;
  border: 3px solid rgba(255,255,255,0.1);
  border-top-color: #534AB7;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.cal-actions { text-align: center; margin-top: 1.5rem; }
.btn-agendar {
  background: #dc2626; /* Strong red */
  color: #fff;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
  transition: all 0.3s;
}
.btn-agendar:hover { 
  background: #ef4444;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(220, 38, 38, 0.6);
}

/* Custom Sleek FullCalendar Theme (Red & Black) */
.fc-wrapper {
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
  background-color: #0d0000; /* Pure deep black with a hint of red */
  padding: 15px;
  border-radius: 12px;
  border: 1px solid rgba(220, 38, 38, 0.2);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 20px rgba(220,38,38,0.05);
}

:deep(.fc-theme-standard td), :deep(.fc-theme-standard th) {
  border-color: var(--fc-border-color);
}
:deep(.fc-col-header-cell) {
  background-color: #1a0505; /* Darker header row */
}
:deep(.fc-col-header-cell-cushion), :deep(.fc-daygrid-day-number) {
  color: #ff9999; /* Bright red tint for numbers and text */
  font-family: 'Space Grotesk', sans-serif;
  text-decoration: none !important;
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

</style>