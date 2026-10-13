<template>
  <main class="servicios-page">

    <!-- Ambient Glow -->
    <div class="ambient-glow fixed-glow"></div>

    <!-- Header Section -->
    <div class="page-header observe-me">
      <div class="header-eyebrow">
        <span class="eyebrow-line"></span>
        CATÁLOGO DE MÓDULOS
        <span class="eyebrow-line"></span>
      </div>
      <h1 class="page-title">OPTIMIZACIÓN<br /><em>ESTRUCTURAL</em></h1>
      <p class="page-sub">Protocolos avanzados para el mantenimiento y mejora de tu vehículo.</p>
    </div>

    <!-- Filtros -->
    <section class="filters-section observe-me" style="transition-delay: 0.2s">
      <div class="filters-inner matte-card">
        <div class="search-wrap">
          <span class="search-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span>
          <input v-model="search" type="text" placeholder="Ingresar parámetro de búsqueda..." />
        </div>

        <div class="filter-pills">
          <button
            v-for="f in filters"
            :key="f.value"
            :class="['fpill', { active: currentFilter === f.value }]"
            @click="currentFilter = f.value"
          >
            {{ f.label }}
          </button>
        </div>

        <div class="result-count">
          <span class="rc-num">{{ filteredServices.length }}</span> RESULTADOS
        </div>
      </div>
    </section>

    <!-- Grid de servicios -->
    <section class="services-section">
      <transition-group name="list" tag="div" class="services-grid" v-if="filteredServices.length">
        <div
          v-for="s in filteredServices"
          :key="s.id"
          class="matte-card srv-card"
        >
          <!-- Imagen -->
          <div class="srv-img-wrap">
            <div class="srv-img" :style="{ backgroundImage: `url(${s.img})` }"></div>
            <div class="srv-img-overlay"></div>
            <span class="srv-cat">{{ s.categoria }}</span>
            <div class="srv-price-tag">${{ s.precio }}<span>COP</span></div>
          </div>

          <!-- Cuerpo -->
          <div class="srv-body">
            <h3 class="srv-name">{{ s.name }}</h3>

            <div class="srv-footer">
              <div class="srv-meta">
                <div class="srv-time">
                  <span class="time-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span>
                  {{ s.tiempo }}
                </div>
              </div>
              <router-link :to="{ path: '/agendar', query: { servicioId: s.name } }" class="srv-btn">
                Seleccionar <span class="arr"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span>
              </router-link>
            </div>
          </div>
        </div>
      </transition-group>

      <!-- Sin resultados -->
      <div v-else class="no-results observe-me">
        <div class="no-results-icon">∅</div>
        <h3>Parámetro No Encontrado</h3>
        <p>Los registros no muestran coincidencias para "<em>{{ search }}</em>"</p>
        <button class="btn btn-ghost" @click="search = ''; currentFilter = 'todos'">Restablecer Parámetros</button>
      </div>
    </section>

    <!-- CTA banner -->
    <section class="cta-strip observe-me">
      <div class="cta-strip-inner matte-card">
        <div class="cta-strip-text">
          <h2>¿Requieres diagnóstico especializado?</h2>
          <p>Nuestros técnicos pueden evaluar anomalías específicas en tu sistema.</p>
        </div>
        <router-link to="/agendar" class="btn btn-primary">
          Solicitar Evaluación
        </router-link>
      </div>
    </section>

  </main>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { API_BASE_URL } from '../config/api'

const search = ref('')
const currentFilter = ref('todos')
const observer = ref(null)

onMounted(() => {
  fetchServices().then(() => {
    observer.value = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
        }
      })
    }, { threshold: 0.1 })
  
    document.querySelectorAll('.observe-me').forEach(el => observer.value.observe(el))
  })
})

onUnmounted(() => {
  if (observer.value) observer.value.disconnect()
})

const filters = [
  { label: 'Todos',          value: 'todos' },
  { label: 'Mantenimiento',  value: 'Mantenimiento' },
  { label: 'Suspensión',     value: 'Suspensión' },
  { label: 'Frenos',         value: 'Frenos' },
  { label: 'Diagnóstico',    value: 'Diagnóstico' },
  { label: 'Llantas',        value: 'Llantas' },
  { label: 'Estética',       value: 'Estética' }
]

const services = ref([])

/**
 * Consulta el catálogo de servicios desde la API del backend.
 */
async function fetchServices() {
  try {
    const res = await fetch(`${API_BASE_URL}/servicios`)
    if (res.ok) {
      const data = await res.json()
      const customImages = {
        'Mantenimiento Preventivo PRO': '/img/servicios/mantenimiento.png',
        'Diagnóstico Computarizado Avanzado': '/img/servicios/diagnostico.png',
        'Actualización a Frenos Cerámicos': '/img/servicios/frenos.png',
        'Sincronización Electrónica': '/img/servicios/sincronizacion.png',
        'Alineación y Balanceo Láser 3D': '/img/servicios/alineacion.png',
        'Mantenimiento Transmisión Automática': '/img/servicios/transmision.png',
        'Detailing y Recubrimiento Cerámico': '/img/servicios/detailing.png',
        'Restauración de Suspensión Deportiva': '/img/servicios/suspension.png'
      }

      services.value = data.map(s => ({
        id: s.id,
        name: s.nombre,
        categoria: s.categoria,
        precio: s.precio.toLocaleString('es-CO'),
        tiempo: s.duracion,
        desc: s.descripcion,
        img: s.imagen || customImages[s.nombre] || '/img/servicios/mantenimiento.png',
        features: ['Calidad garantizada', 'Atención profesional']
      }))
    }
  } catch (e) {
    console.error(e)
  }
}

const filteredServices = computed(() => {
  const norm = (str) => {
    if (!str) return ''
    return String(str).normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim().toLowerCase()
  }
  const fNorm = norm(currentFilter.value)
  const sNorm = norm(search.value)

  return services.value.filter(s => {
    const cNorm = norm(s.categoria)
    const matchCat = currentFilter.value === 'todos' || cNorm === fNorm || cNorm.includes(fNorm)
    
    const matchSearch = !search.value || 
      norm(s.name).includes(sNorm) || 
      norm(s.desc).includes(sNorm) ||
      cNorm.includes(sNorm)

    return matchCat && matchSearch
  })
})
</script>

<style scoped>
.servicios-page {
  padding-top: var(--nav-height);
  min-height: 100vh;
  position: relative;
}

.fixed-glow {
  position: fixed;
  top: 20%; left: 10%;
  width: 800px; height: 800px;
  background: radial-gradient(circle, rgba(230,0,35,0.05) 0%, transparent 60%);
  z-index: 0;
  pointer-events: none;
}

/* BASE ANIMATIONS */
.observe-me {
  opacity: 0; transform: translateY(30px);
  transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.observe-me.is-visible { opacity: 1; transform: translateY(0); }

/* LIST TRANSITIONS FOR FILTERS */
.list-enter-active,
.list-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
.list-leave-active {
  position: absolute;
}

/* HEADER */
.page-header {
  text-align: center;
  padding: 5rem 2rem 3rem;
  position: relative; z-index: 1;
}

.header-eyebrow {
  display: flex; align-items: center; justify-content: center; gap: 1rem;
  font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700;
  letter-spacing: 4px; color: var(--primary); margin-bottom: 1.5rem;
}
.eyebrow-line { width: 30px; height: 1px; background: rgba(230,0,35,0.5); }

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(3rem, 6vw, 4.5rem);
  font-weight: 900;
  color: white;
  line-height: 1;
  letter-spacing: -1px;
  margin-bottom: 1rem;
}
.page-title em { font-style: normal; color: transparent; -webkit-text-stroke: 1px var(--primary); }

.page-sub {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

/* FILTERS */
.filters-section {
  padding: 0 2rem 4rem;
  position: relative; z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
}
.filters-inner {
  display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; flex-wrap: wrap;
  padding: 1rem 1.5rem;
}

.search-wrap {
  display: flex; align-items: center; gap: 0.8rem;
  background: var(--bg-base);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 8px;
  padding: 0.8rem 1rem;
  flex: 1; min-width: 250px;
  transition: border-color 0.3s;
}
.search-wrap:focus-within { border-color: var(--primary); }
.search-icon { color: var(--primary); font-size: 1.2rem; line-height: 1; }
.search-wrap input {
  background: transparent; border: none; outline: none;
  color: white; font-family: 'Outfit', sans-serif; font-size: 0.95rem; width: 100%;
}

.filter-pills { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.fpill {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.1);
  color: var(--text-secondary);
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
  cursor: pointer; transition: all 0.3s ease;
}
.fpill:hover { background: rgba(255,255,255,0.05); color: white; }
.fpill.active { background: var(--primary); border-color: var(--primary); color: white; box-shadow: var(--shadow-red); }

.result-count {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.75rem;
  color: var(--text-muted);
  letter-spacing: 2px;
}
.rc-num { color: white; font-size: 0.9rem; font-weight: 700; margin-right: 0.3rem; }

/* SERVICES GRID */
.services-section {
  padding: 0 2rem 6rem;
  max-width: 1300px; margin: 0 auto;
  position: relative; z-index: 2;
}
.services-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}

.srv-card {
  display: flex; flex-direction: column; padding: 0;
}
.srv-img-wrap {
  position: relative; height: 220px; overflow: hidden;
}
.srv-img {
  width: 100%; height: 100%; background-size: cover; background-position: center;
  filter: grayscale(80%) contrast(1.1); transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.srv-card:hover .srv-img { transform: scale(1.1); filter: grayscale(0%); }
.srv-img-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to top, var(--bg-card) 0%, transparent 80%);
}
.srv-cat {
  position: absolute; top: 15px; left: 15px;
  background: var(--primary); color: white; font-family: 'Space Grotesk', sans-serif;
  font-size: 0.65rem; font-weight: 700; letter-spacing: 2px; padding: 0.4rem 0.8rem; border-radius: 4px;
}
.srv-price-tag {
  position: absolute; bottom: 15px; right: 15px;
  font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; font-weight: 900; color: white;
  text-shadow: 0 4px 12px rgba(0,0,0,0.8);
}
.srv-price-tag span { font-size: 0.8rem; color: var(--primary); font-weight: 700; margin-left: 2px; }

.srv-body { padding: 1.8rem; display: flex; flex-direction: column; flex: 1; }
.srv-name { font-family: 'Space Grotesk', sans-serif; font-size: 1.4rem; font-weight: 900; color: white; margin-bottom: 0.8rem; line-height: 1.1; }
.srv-desc { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 1.5rem; flex: 1; }

.srv-features { list-style: none; margin-bottom: 2rem; }
.srv-features li { display: flex; align-items: center; gap: 0.8rem; color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.5rem; }
.feat-bullet { width: 6px; height: 6px; background: var(--primary); border-radius: 50%; box-shadow: 0 0 10px var(--primary); }

.srv-footer {
  display: flex; align-items: center; justify-content: space-between;
  padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.05);
}
.srv-time { font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; color: var(--text-muted); display: flex; align-items: center; gap: 0.5rem; }
.time-icon { color: var(--primary); }

.srv-btn {
  font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; font-weight: 700; color: white;
  text-transform: uppercase; letter-spacing: 1px; transition: color 0.3s;
}
.srv-btn .arr { color: var(--primary); transition: transform 0.3s; display: inline-block; }
.srv-btn:hover { color: var(--primary); }
.srv-btn:hover .arr { transform: translateX(5px); color: white; }

/* NO RESULTS */
.no-results { text-align: center; padding: 5rem 2rem; max-width: 500px; margin: 0 auto; }
.no-results-icon { font-size: 4rem; color: rgba(255,255,255,0.1); margin-bottom: 1rem; }
.no-results h3 { font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; color: white; margin-bottom: 1rem; }
.no-results p { color: var(--text-secondary); margin-bottom: 2rem; }
.no-results em { color: var(--primary); font-style: normal; }

/* CTA STRIP */
.cta-strip { padding: 0 2rem 6rem; max-width: 1000px; margin: 0 auto; }
.cta-strip-inner {
  display: flex; align-items: center; justify-content: space-between; gap: 2rem;
  padding: 3rem 4rem; border: 1px solid rgba(230,0,35,0.3); background: rgba(230,0,35,0.05);
}
.cta-strip-text h2 { font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; color: white; margin-bottom: 0.5rem; }
.cta-strip-text p { color: var(--text-secondary); font-size: 1rem; }

@media (max-width: 900px) {
  .filters-inner { flex-direction: column; align-items: stretch; }
  .search-wrap { width: 100%; }
  .cta-strip-inner { flex-direction: column; text-align: center; padding: 2rem; }
}
</style>