<template>
  <main class="home" @mousemove="handleMouseMove">
    
    <!-- FUTURISTIC GLOW ORB BACKGROUND -->
    <div class="ambient-glow" :style="glowStyle"></div>

    <!-- 1. HERO PARALLAX -->
    <section class="hero-parallax">
      <div class="hero-bg" :style="{ transform: `translateY(${scrollY * 0.4}px) scale(1.05)` }"></div>
      <div class="hero-grid-overlay"></div>
      
      <div class="hero-content" :style="{ transform: `translate3d(${mouseX * -30}px, ${scrollY * 0.15 + (mouseY * -30)}px, 0)` }">
        <div class="hero-eyebrow fade-up" style="animation-delay: 0.2s;">
          <span class="eyebrow-line"></span>
          TALLER AUTOMOTRIZ DE CONFIANZA
          <span class="eyebrow-line"></span>
        </div>
        
        <h1 class="hero-title fade-up" style="animation-delay: 0.4s;">
          MÁXIMO<br />
          <span class="glitch" data-text="RENDIMIENTO">RENDIMIENTO</span>
        </h1>
        
        <p class="hero-desc fade-up" style="animation-delay: 0.6s;">
          Cuidamos tu vehículo con la atención y el profesionalismo que merece. Desde mantenimientos preventivos hasta reparaciones complejas.
        </p>
        
        <div class="hero-actions fade-up" style="animation-delay: 0.8s;">
          <router-link v-if="user" to="/agendar" class="btn btn-primary">Agenda aquí</router-link>
          <button class="btn btn-ghost" @click="scrollToFeatures">Conoce más de nosotros</button>
        </div>
      </div>
      
      <div class="scroll-indicator fade-up" style="animation-delay: 1.2s;">
        <span>DESCUBRIR</span>
        <div class="scroll-line"></div>
      </div>
    </section>

    <!-- 2. FEATURES (Conoce más de nosotros) -->
    <section class="features" id="features">
      <div class="section-header observe-me">
        <h2>Servicios <span>Generales</span></h2>
        <p>Soluciones integrales para mantener tu auto seguro y en movimiento.</p>
      </div>

      <div class="features-grid">
        <div class="matte-card feature-card observe-me" v-for="(f, i) in features" :key="i" :style="{ transitionDelay: `${i * 0.15}s` }">
          <div class="feature-icon-wrap">
            <div class="feature-icon" v-html="f.icon"></div>
            <div class="icon-glow"></div>
          </div>
          <h3>{{ f.title }}</h3>
          <p>{{ f.desc }}</p>
          <div class="card-deco-line"></div>
        </div>
      </div>
    </section>

    <!-- 3. STATS BANNER -->
    <section class="stats-banner observe-me">
      <div class="stat-item">
        <h3>+15</h3>
        <p>Años de Experiencia</p>
      </div>
      <div class="stat-item">
        <h3>100%</h3>
        <p>Garantía de Servicio</p>
      </div>
      <div class="stat-item">
        <h3>24/7</h3>
        <p>Atención a Clientes</p>
      </div>
    </section>

    <!-- 4. REVIEWS CAROUSEL -->
    <section class="reviews observe-me">
      <div class="section-header">
        <h2>Lo que dicen <span>nuestros clientes</span></h2>
        <p>Tu satisfacción es nuestro motor principal.</p>
      </div>
      
      <div class="reviews-slider">
        <button class="slider-btn" @click="prevReview"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></button>
        <transition name="fade" mode="out-in">
          <div :key="activeReview" class="review-content matte-card">
            <div class="stars"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></div>
            <p class="review-text">"{{ reviews[activeReview].text }}"</p>
            <p class="review-author">- {{ reviews[activeReview].author }}</p>
          </div>
        </transition>
        <button class="slider-btn" @click="nextReview"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></button>
      </div>
      <div class="review-dots">
        <span v-for="(r, i) in reviews" :key="i" class="dot" :class="{ active: i === activeReview }" @click="activeReview = i"></span>
      </div>
    </section>

    <!-- 5. CTA -->
    <section class="parallax-cta">
      <div class="cta-bg" :style="{ transform: `translateY(${(scrollY - 2000) * 0.2}px) scale(1.1)` }"></div>
      <div class="cta-grid"></div>
      
      <div class="cta-content matte-card observe-me">
        <div class="cta-ring"></div>
        <h2>Optimiza tu vehículo <span>hoy</span></h2>
        <p>Agenda hoy y recibe una revisión general de cortesía en tu primera visita a nuestro taller.</p>
        <router-link v-if="user" to="/agendar" class="btn btn-primary">Agenda aquí</router-link>
        <router-link v-else to="/login" class="btn btn-primary">Iniciar Sesión para Agendar</router-link>
      </div>
    </section>

    <!-- FOOTER MATTE -->
    <footer class="footer">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="/logo.png" alt="Logo" class="footer-logo" />
          <p>El estándar definitivo en servicio automotriz profesional. Conducidos por la innovación.</p>
        </div>
        <div class="footer-links">
          <h4>Navegación</h4>
          <router-link to="/">Inicio</router-link>
          <router-link to="/servicios">Servicios</router-link>
          <router-link v-if="user" to="/agendar">Agendar Cita</router-link>
        </div>
        <div class="footer-contact">
          <h4>Terminal de Contacto</h4>
          <p><span class="fc-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span> Av. Principal 123, Sector 7</p>
          <p><span class="fc-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span> +1 234 567 890</p>
          <p><span class="fc-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span> sys@drivenyield.com</p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Driven Yield Pro System. Conexión segura establecida.</p>
      </div>
    </footer>

  </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const auth = useAuthStore()
const { user } = storeToRefs(auth)

const scrollY = ref(0)
const rawMouseX = ref(0)
const rawMouseY = ref(0)
const observer = ref(null)

const mouseX = computed(() => rawMouseX.value / window.innerWidth - 0.5)
const mouseY = computed(() => rawMouseY.value / window.innerHeight - 0.5)

const glowStyle = computed(() => ({
  top: `${rawMouseY.value}px`,
  left: `${rawMouseX.value}px`,
  transform: 'translate(-50%, -50%)'
}))

/** Guarda la posición actual de desplazamiento vertical. */
const onScroll = () => { scrollY.value = window.scrollY }

/** Guarda las coordenadas del cursor del ratón para efectos de resplandor y paralaje. */
const handleMouseMove = (e) => {
  rawMouseX.value = e.clientX
  rawMouseY.value = e.clientY
}

/** Desplaza suavemente la vista hasta la sección de características. */
const scrollToFeatures = () => {
  const el = document.getElementById('features')
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  
  observer.value = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible')
      }
    })
  }, { threshold: 0.15 })

  document.querySelectorAll('.observe-me').forEach(el => observer.value.observe(el))
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  if (observer.value) observer.value.disconnect()
})

const features = [
  { icon: `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 9.36l-7.1 7.1a1 1 0 0 1-1.42 0l-1.41-1.41a1 1 0 0 1 0-1.42l7.1-7.1a6 6 0 0 1 9.36-7.94l-3.76 3.76z"/></svg>`, title: 'Mantenimiento Preventivo', desc: 'Cambios de aceite, filtros y revisión de fluidos para mantener tu auto en óptimas condiciones.' },
  { icon: `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>`, title: 'Mecánica General', desc: 'Reparación de frenos, suspensión, dirección y componentes mecánicos de todas las marcas.' },
  { icon: `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`, title: 'Sistema Eléctrico', desc: 'Diagnóstico y reparación de baterías, alternadores, luces y sistemas electrónicos complejos.' },
]

const reviews = [
  { text: "Excelente servicio. Fueron rápidos, transparentes con los precios y dejaron mi auto como nuevo. ¡Totalmente recomendados!", author: "Carlos M." },
  { text: "El mejor taller al que he ido. Resolvieron un problema eléctrico que en otros lugares no pudieron. Muy profesionales.", author: "Andrea Gómez" },
  { text: "Atención de primera. Te explican todo detalladamente y el lugar es impecable. Los mecánicos saben lo que hacen.", author: "Luis Ramírez" },
  { text: "Llevé mi coche por un ruido en los frenos y me lo solucionaron el mismo día a un precio justo.", author: "Roberto F." }
]
const activeReview = ref(0)
const nextReview = () => { activeReview.value = (activeReview.value + 1) % reviews.length }
const prevReview = () => { activeReview.value = (activeReview.value - 1 + reviews.length) % reviews.length }

</script>

<style scoped>
/* AMBIENT GLOW */
.ambient-glow {
  position: fixed;
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(230,0,35,0.08) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
  transition: opacity 0.5s;
  mix-blend-mode: screen;
}

/* BASE ANIMATIONS */
.fade-up {
  opacity: 0; transform: translateY(30px);
  animation: introFadeUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes introFadeUp { to { opacity: 1; transform: translateY(0); } }

.observe-me {
  opacity: 0; transform: translateY(40px);
  transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.observe-me.is-visible { opacity: 1; transform: translateY(0); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* HERO PARALLAX */
.hero-parallax {
  position: relative; height: 100vh;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.hero-bg {
  position: absolute; inset: -10%;
  background: url('https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=1600&q=80') center/cover no-repeat;
  filter: grayscale(100%) brightness(0.2) contrast(1.2);
  z-index: 0; will-change: transform;
}
.hero-grid-overlay {
  position: absolute; inset: 0;
  background-image: 
    linear-gradient(rgba(230,0,35,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(230,0,35,0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  background-position: center center;
  z-index: 1;
}
.hero-content {
  position: relative; z-index: 2;
  text-align: center; max-width: 900px; padding: 0 2rem;
  will-change: transform;
}
.hero-eyebrow {
  display: flex; align-items: center; justify-content: center; gap: 1rem;
  font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700;
  letter-spacing: 4px; color: var(--primary); margin-bottom: 2rem;
}
.eyebrow-line { width: 50px; height: 1px; background: rgba(230,0,35,0.5); }
.hero-title {
  font-family: 'Space Grotesk', sans-serif; font-size: clamp(3.5rem, 7vw, 6.5rem);
  font-weight: 900; line-height: 1; color: white; margin-bottom: 1.5rem;
  text-transform: uppercase; letter-spacing: -2px;
}
.glitch {
  position: relative; color: var(--primary); display: inline-block;
  text-shadow: 0 0 30px rgba(230,0,35,0.4);
}
.hero-desc {
  font-size: 1.15rem; color: var(--text-secondary); margin-bottom: 3.5rem;
  max-width: 650px; margin-left: auto; margin-right: auto; line-height: 1.8;
}
.hero-actions { display: flex; gap: 1.5rem; justify-content: center; }
.scroll-indicator {
  position: absolute; bottom: 3rem; left: 50%; transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center; gap: 1rem;
  z-index: 2;
}
.scroll-indicator span {
  font-family: 'Space Grotesk', sans-serif; font-size: 0.6rem;
  letter-spacing: 3px; color: rgba(255,255,255,0.3);
}
.scroll-line {
  width: 1px; height: 50px;
  background: linear-gradient(to bottom, rgba(230,0,35,0.5), transparent);
  animation: scrollDown 2s ease-in-out infinite;
}
@keyframes scrollDown {
  0% { transform: scaleY(0); transform-origin: top; }
  50% { transform: scaleY(1); transform-origin: top; }
  100% { transform: scaleY(0); transform-origin: bottom; }
}

/* SECTION HEADER */
.section-header h2 span { color: var(--primary); font-style: italic; padding-right: 0.2rem; }
.section-header p { color: var(--text-secondary); margin-top: 10px; }

/* FEATURES */
.features { padding: 8rem 2rem 4rem; max-width: 1300px; margin: 0 auto; position: relative; z-index: 10; }
.features-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2.5rem; margin-top: 5rem;
}
.feature-card { padding: 3rem 2.5rem; text-align: left; }
.feature-icon-wrap { position: relative; margin-bottom: 2rem; display: inline-block; }
.feature-icon {
  font-size: 3rem; line-height: 1; position: relative; z-index: 2;
}
.icon-glow {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  width: 60px; height: 60px; background: var(--primary); filter: blur(30px);
  opacity: 0.3; z-index: 1; transition: opacity 0.4s;
}
.feature-card:hover .icon-glow { opacity: 0.6; }
.feature-card h3 { font-size: 1.4rem; margin-bottom: 1rem; color: white; letter-spacing: 1px; }
.feature-card p { color: var(--text-secondary); font-size: 0.95rem; line-height: 1.7; }
.card-deco-line {
  width: 0; height: 2px; background: var(--primary); margin-top: 2rem;
  transition: width 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.feature-card:hover .card-deco-line { width: 40px; }

/* STATS BANNER */
.stats-banner {
  background: var(--bg-card);
  border-top: 1px solid rgba(255,255,255,0.05);
  border-bottom: 1px solid rgba(255,255,255,0.05);
  padding: 4rem 2rem;
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 2rem;
  position: relative;
  z-index: 10;
}
.stat-item { text-align: center; }
.stat-item h3 { font-family: 'Space Grotesk', sans-serif; font-size: 3.5rem; font-weight: 900; color: var(--primary); margin-bottom: 0.5rem; }
.stat-item p { color: white; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }

/* REVIEWS */
.reviews { padding: 8rem 2rem; max-width: 900px; margin: 0 auto; position: relative; z-index: 10; text-align: center; }
.reviews-slider { display: flex; align-items: center; justify-content: center; gap: 2rem; margin-top: 4rem; }
.slider-btn {
  background: transparent; border: 1px solid rgba(255,255,255,0.2);
  width: 50px; height: 50px; border-radius: 50%; color: white;
  font-size: 1.5rem; cursor: pointer; transition: all 0.3s;
}
.slider-btn:hover { background: var(--primary); border-color: var(--primary); }
.review-content { padding: 3rem; flex: 1; border-radius: 12px; }
.stars { font-size: 1.5rem; margin-bottom: 1.5rem; }
.review-text { font-size: 1.2rem; font-style: italic; color: white; line-height: 1.6; margin-bottom: 1.5rem; }
.review-author { font-weight: 700; color: var(--primary); text-transform: uppercase; letter-spacing: 1px; }
.review-dots { display: flex; justify-content: center; gap: 10px; margin-top: 2rem; }
.dot { width: 10px; height: 10px; border-radius: 50%; background: rgba(255,255,255,0.2); cursor: pointer; transition: 0.3s; }
.dot.active { background: var(--primary); transform: scale(1.3); }

/* PARALLAX CTA */
.parallax-cta {
  position: relative; padding: 10rem 2rem; margin-top: 5rem;
  display: flex; align-items: center; justify-content: center; overflow: hidden;
}
.cta-bg {
  position: absolute; inset: -15%;
  background: url('https://images.unsplash.com/photo-1503375839088-33eb0e94770d?w=1600&q=80') center/cover no-repeat;
  filter: grayscale(100%) brightness(0.15); z-index: 0; will-change: transform;
}
.cta-grid {
  position: absolute; inset: 0;
  background: radial-gradient(circle at center, transparent 0%, var(--bg-deep) 80%),
              linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
              linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 100% 100%, 40px 40px, 40px 40px; z-index: 1;
}
.cta-content { position: relative; z-index: 2; text-align: center; padding: 5rem 4rem; max-width: 800px; border-radius: 24px; }
.cta-ring {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  width: 150%; height: 150%; border-radius: 50%; border: 1px solid rgba(230,0,35,0.1);
  animation: pulseRing 4s linear infinite; pointer-events: none; z-index: -1;
}
@keyframes pulseRing {
  0% { transform: translate(-50%, -50%) scale(0.8); opacity: 0; }
  50% { opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(1.2); opacity: 0; }
}
.cta-content h2 { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 1.5rem; line-height: 1.1; }
.cta-content h2 span { color: var(--primary); }
.cta-content p { color: var(--text-secondary); margin-bottom: 3rem; font-size: 1.1rem; line-height: 1.6; }

/* FOOTER */
.footer {
  background: var(--bg-deep); border-top: 1px solid rgba(255,255,255,0.03);
  padding: 6rem 2rem 2rem; position: relative; z-index: 10;
}
.footer-grid {
  max-width: 1300px; margin: 0 auto 4rem;
  display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 4rem;
}
.footer-logo { height: 40px; margin-bottom: 1.5rem; filter: grayscale(100%) brightness(200%); opacity: 0.8; }
.footer-brand p { color: var(--text-secondary); font-size: 0.95rem; max-width: 350px; line-height: 1.6; }
.footer h4 { color: white; margin-bottom: 2rem; font-size: 1.1rem; font-family: 'Space Grotesk', sans-serif; letter-spacing: 1px; }
.footer-links { display: flex; flex-direction: column; gap: 1rem; }
.footer-links a { color: var(--text-secondary); font-size: 0.95rem; transition: color 0.3s; }
.footer-links a:hover { color: var(--primary); padding-left: 5px; }
.footer-contact p { color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.8rem; }
.fc-icon { color: var(--primary); font-size: 1.2rem; }
.footer-bottom {
  border-top: 1px solid rgba(255,255,255,0.03); padding-top: 2rem; text-align: center;
  color: var(--text-muted); font-size: 0.8rem; font-family: 'Space Grotesk', sans-serif; letter-spacing: 2px; text-transform: uppercase;
}

@media (max-width: 900px) {
  .hero-title { font-size: 3rem; }
  .footer-grid { grid-template-columns: 1fr; gap: 3rem; }
  .hero-actions { flex-direction: column; }
  .reviews-slider { flex-direction: column; }
  .slider-btn { display: none; }
}
</style>