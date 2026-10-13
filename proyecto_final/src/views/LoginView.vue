<template>
  <div class="login-root">
    
    <!-- LEFT PANEL: Brand & Tech Vibe -->
    <div class="left-panel">
      <!-- Background Elements -->
      <div class="left-grid"></div>
      <div class="ambient-glow orb orb-1"></div>
      <div class="ambient-glow orb orb-2"></div>
      <div class="noise-overlay"></div>

      <div class="left-content observe-me">
        <div class="brand-badge">
          <span class="badge-dot"></span>
          ENLACE SEGURO · V6.0
        </div>

        <div>
          <div class="brand-logo">DRIVEN<br/><span>YIELD</span></div>
          <p class="brand-tagline">PLATAFORMA DE GESTIÓN AVANZADA</p>
          <p class="brand-desc">Acceso restringido al sistema de administración de telemetría y protocolos de mantenimiento automotriz.</p>
        </div>

        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-value">99.9<span>%</span></div>
            <div class="stat-label">UPTIME</div>
            <div class="stat-bar"><div class="stat-fill" style="width:99.9%"></div></div>
          </div>
          <div class="stat-card">
            <div class="stat-value">256<span>b</span></div>
            <div class="stat-label">ENCRIPTACIÓN</div>
            <div class="stat-bar"><div class="stat-fill" style="width:100%"></div></div>
          </div>
          <div class="stat-card">
            <div class="stat-value">0<span>ms</span></div>
            <div class="stat-label">LATENCIA</div>
            <div class="stat-bar"><div class="stat-fill" style="width:5%"></div></div>
          </div>
        </div>

        <div class="trust-row">
          <div class="trust-item"><span class="check-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span> Conexión Cifrada</div>
          <div class="trust-item"><span class="check-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span> Respaldos en Tiempo Real</div>
          <div class="trust-item"><span class="check-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span> Protocolos de Privacidad</div>
        </div>
      </div>
    </div>

    <!-- RIGHT PANEL: Forms -->
    <div class="right-panel">
      <div class="form-container">
        <transition name="fade-slide" mode="out-in">

          <!-- LOGIN -->
          <div v-if="panel === 'login'" key="login" class="form-box observe-me">
            <p class="form-eyebrow">AUTENTICACIÓN REQUERIDA</p>
            <h1 class="form-title">INICIAR <span>SESIÓN</span></h1>
            <p class="form-subtitle">Ingrese sus credenciales operativas.</p>

            <div class="form-group">
              <label>IDENTIFICADOR (USUARIO)</label>
              <input v-model="loginForm.username" type="text" placeholder="Ej. jperez_01" @keyup.enter="handleLogin" />
            </div>

            <div class="form-group">
              <label>CLAVE DE ACCESO</label>
              <div class="pwd-wrap">
                <input v-model="loginForm.password" :type="showPwd ? 'text' : 'password'" placeholder="••••••••" @keyup.enter="handleLogin" />
                <button class="eye-btn" @click="showPwd = !showPwd" type="button">
                  {{ showPwd ? 'Ocultar' : 'Mostrar' }}
                </button>
              </div>
            </div>

            <button class="btn btn-primary btn-full" @click="handleLogin" :disabled="auth.loading">
              {{ auth.loading ? 'VALIDANDO...' : 'INICIAR SESIÓN' }}
            </button>

            <div class="divider"><span>O</span></div>

            <button class="btn btn-ghost btn-full" @click="panel = 'register'">
              SOLICITAR NUEVO ACCESO
            </button>

            <button class="btn btn-ghost btn-full" @click="panel = 'admin'">
              ACCESO ADMINISTRADOR
            </button>

            <button class="forgot-link-bottom" @click="panel = 'forgot'" type="button">
              ¿CREDENCIALES COMPROMETIDAS O PERDIDAS?
            </button>
          </div>

          <!-- REGISTER -->
          <div v-else-if="panel === 'register'" key="register" class="form-box observe-me">
            <p class="form-eyebrow">NUEVO EXPEDIENTE</p>
            <h1 class="form-title">CREAR <span>PERFIL</span></h1>
            <p class="form-subtitle">Complete el registro para habilitar su acceso.</p>

            <div class="register-scroll">
              <div class="form-group">
                <label>NOMBRE OPERATIVO</label>
                <input v-model="regForm.name" type="text" placeholder="Nombre completo" />
              </div>
              <div class="field-row">
                <div class="form-group">
                  <label>CORREO ELECTRÓNICO</label>
                  <input v-model="regForm.email" type="email" placeholder="correo@dominio.com" />
                </div>
                <div class="form-group">
                  <label>CANAL DE COMUNICACIÓN</label>
                  <input v-model="regForm.phone" type="tel" placeholder="+1 234 567 8900" />
                </div>
              </div>
              <div class="form-group">
                <label>IDENTIFICADOR DE SISTEMA</label>
                <input v-model="regForm.username" type="text" placeholder="usuario_id" />
              </div>
              <div class="field-row">
                <div class="form-group">
                  <label>CLAVE DE ACCESO</label>
                  <input v-model="regForm.password" type="password" placeholder="Mínimo 6 caracteres" />
                </div>
                <div class="form-group">
                  <label>VERIFICACIÓN DE CLAVE</label>
                  <input v-model="regForm.confirm" type="password" placeholder="Repetir clave" />
                </div>
              </div>

              <button class="btn btn-primary btn-full" @click="handleRegister" :disabled="auth.loading" style="margin-top: 1rem;">
                <template v-if="auth.loading">REGISTRANDO...</template>
                <template v-else>
                  REGISTRAR PERFIL
                  <svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg>
                </template>
              </button>
              
              <div class="divider"><span>O</span></div>
              
              <button class="btn btn-ghost btn-full" @click="panel = 'login'">
                VOLVER AL ACCESO
              </button>
            </div>
          </div>

          <!-- ADMIN LOGIN -->
          <div v-else-if="panel === 'admin'" key="admin" class="form-box observe-me">
            <button class="back-btn" @click="panel = 'login'"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg> Retornar</button>

            <p class="form-eyebrow" style="margin-top:1.5rem">NIVEL DE PRIVILEGIO: MÁXIMO</p>
            <h1 class="form-title">ACCESO <span>ADMIN</span></h1>
            <p class="form-subtitle">Autenticación para terminal de control.</p>

            <div class="form-group">
              <label>CORREO ADMINISTRATIVO</label>
              <input v-model="adminForm.email" type="email" placeholder="admin@dominio.com" @keyup.enter="handleAdminLogin" />
            </div>

            <div class="form-group">
              <label>CLAVE DE ENCRIPTACIÓN</label>
              <div class="pwd-wrap">
                <input v-model="adminForm.password" :type="showPwd ? 'text' : 'password'" placeholder="••••••••" @keyup.enter="handleAdminLogin" />
                <button class="eye-btn" @click="showPwd = !showPwd" type="button">
                  {{ showPwd ? 'Ocultar' : 'Mostrar' }}
                </button>
              </div>
            </div>

            <button class="btn btn-primary btn-full" @click="handleAdminLogin" :disabled="auth.loading">
              {{ auth.loading ? 'VALIDANDO...' : 'INICIAR SESIÓN' }}
            </button>
          </div>

          <!-- FORGOT -->
          <div v-else key="forgot" class="form-box observe-me">
            <button class="back-btn" @click="panel = 'login'"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg> Retornar</button>

            <p class="form-eyebrow" style="margin-top:1.5rem">RECUPERACIÓN DE CLAVE</p>
            <h1 class="form-title">RESTABLECER <span>ACCESO</span></h1>
            <p class="form-subtitle">Enviaremos un vector de recuperación a su correo.</p>

            <div class="form-group" style="margin-top: 2rem;">
              <label>CORREO ASOCIADO</label>
              <input v-model="forgotEmail" type="email" placeholder="correo@dominio.com" @keyup.enter="handleForgot" />
            </div>

            <button class="btn btn-primary btn-full" @click="handleForgot" :disabled="auth.loading">
              {{ auth.loading ? 'ENVIANDO...' : 'SOLICITAR RESTABLECIMIENTO' }}
            </button>
          </div>

        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../stores/toast'

const auth = useAuthStore()
const router = useRouter()
const toast = useToast()
const panel = ref('login')
const showPwd = ref(false)
const forgotEmail = ref('')
const observer = ref(null)

onMounted(() => {
  observer.value = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible')
      }
    })
  }, { threshold: 0.1 })

  document.querySelectorAll('.observe-me').forEach(el => observer.value.observe(el))
})

onUnmounted(() => {
  if (observer.value) observer.value.disconnect()
})

const loginForm = reactive({ username: '', password: '' })
const regForm = reactive({ name: '', email: '', phone: '', username: '', password: '', confirm: '' })
const adminForm = reactive({ email: '', password: '' })

/**
 * Procesa el inicio de sesión para usuarios clientes.
 */
async function handleLogin() {
  if (!loginForm.username || !loginForm.password) { toast.error('Parámetros incompletos.'); return }
  const res = await auth.login(loginForm.username, loginForm.password)
  if (!res.ok) { toast.error(res.error); return }
  toast.success(`Acceso concedido, ${auth.user.nombre}.`)
  router.push(auth.user.role === 'admin' ? '/admin' : '/')
}

/**
 * Procesa el inicio de sesión exclusivo para administradores del taller.
 */
async function handleAdminLogin() {
  if (!adminForm.email || !adminForm.password) { toast.error('Parámetros incompletos.'); return }
  const res = await auth.loginAdmin(adminForm.email, adminForm.password)
  if (!res.ok) { toast.error(res.error); return }
  toast.success(`Privilegios elevados confirmados, ${auth.user.nombre}.`)
  router.push('/admin')
}

async function handleRegister() {
  const { name, email, phone, username, password, confirm } = regForm
  if (!name || name.length < 2) { toast.error('Nombre inválido.'); return }
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { toast.error('Correo inválido.'); return }
  if (!phone || phone.length < 7) { toast.error('Canal de comunicación inválido.'); return }
  if (!username || username.length < 3) { toast.error('Identificador muy corto.'); return }
  if (password.length < 6) { toast.error('Clave débil. Mínimo 6 caracteres.'); return }
  if (password !== confirm) { toast.error('Las claves no coinciden.'); return }
  const res = await auth.register(name, username, email, password, phone)
  if (!res.ok) { toast.error(res.error); return }
  toast.success('Perfil creado. Redirigiendo...')
  router.push('/')
}

async function handleForgot() {
  if (!forgotEmail.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(forgotEmail.value)) {
    toast.error('Ingrese un correo válido.'); return
  }
  const res = await auth.forgotPassword(forgotEmail.value)
  if (!res.ok) { toast.error(res.error); return }
  toast.success(res.message)
  panel.value = 'login'
}
</script>

<style scoped>
/* BASE */
.login-root {
  display: flex; min-height: 100vh; overflow: hidden;
  background: var(--bg-base);
}

/* ANIMATIONS */
.observe-me {
  opacity: 0; transform: translateY(20px);
  transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.observe-me.is-visible { opacity: 1; transform: translateY(0); }

/* LEFT PANEL (BRANDING) */
.left-panel {
  width: 450px; flex-shrink: 0; position: relative;
  background: var(--bg-deep); border-right: var(--border-matte);
  display: flex; flex-direction: column; justify-content: center;
  overflow: hidden; padding: 3rem;
}
.left-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(230,0,35,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(230,0,35,0.05) 1px, transparent 1px);
  background-size: 40px 40px; pointer-events: none; z-index: 1;
}
.orb { position: absolute; border-radius: 50%; z-index: 0; }
.orb-1 { width: 300px; height: 300px; background: radial-gradient(circle, rgba(230,0,35,0.15) 0%, transparent 70%); top: -50px; left: -50px; }
.orb-2 { width: 400px; height: 400px; background: radial-gradient(circle, rgba(230,0,35,0.1) 0%, transparent 70%); bottom: -100px; right: -100px; }

.left-content { position: relative; z-index: 2; display: flex; flex-direction: column; gap: 2rem; }

.brand-badge {
  display: inline-flex; align-items: center; gap: 0.5rem;
  padding: 0.4rem 1rem; background: rgba(230,0,35,0.08); border: 1px solid rgba(230,0,35,0.2);
  border-radius: 4px; font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; color: var(--primary);
  letter-spacing: 2px; font-weight: 700; width: fit-content;
}
.badge-dot { width: 6px; height: 6px; background: var(--primary); border-radius: 50%; box-shadow: 0 0 10px var(--primary); animation: blink 2s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

.brand-logo { font-family: 'Space Grotesk', sans-serif; font-size: 4rem; font-weight: 900; line-height: 0.9; letter-spacing: -2px; color: white; margin-bottom: 0.5rem; }
.brand-logo span { color: transparent; -webkit-text-stroke: 1px var(--primary); }
.brand-tagline { font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; color: var(--primary); letter-spacing: 3px; font-weight: 700; margin-bottom: 1rem; }
.brand-desc { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6; }

.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.stat-card { background: rgba(255,255,255,0.02); border: var(--border-matte); border-radius: 8px; padding: 1rem; }
.stat-value { font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 900; color: white; line-height: 1; }
.stat-value span { font-size: 1rem; color: var(--primary); }
.stat-label { font-family: 'Space Grotesk', sans-serif; font-size: 0.65rem; color: var(--text-muted); letter-spacing: 1px; margin: 0.5rem 0; }
.stat-bar { height: 2px; background: rgba(255,255,255,0.05); border-radius: 2px; }
.stat-fill { height: 100%; background: var(--primary); box-shadow: 0 0 10px var(--primary); }

.trust-row { display: flex; flex-direction: column; gap: 0.6rem; }
.trust-item { font-size: 0.85rem; color: var(--text-muted); display: flex; align-items: center; gap: 0.5rem; }
.check-icon { color: var(--primary); font-weight: 900; }

/* RIGHT PANEL (FORMS) */
.right-panel {
  flex: 1; display: flex; align-items: center; justify-content: center;
  padding: 3rem; background: var(--bg-base); position: relative;
}
.right-panel::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at 70% 50%, rgba(230,0,35,0.03) 0%, transparent 60%); pointer-events: none;
}

.form-container { width: 100%; max-width: 440px; position: relative; z-index: 1; }
.form-box { width: 100%; }
.form-box.observe-me { opacity: 1; transform: none; }

.form-eyebrow { font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700; color: var(--primary); letter-spacing: 2px; margin-bottom: 0.5rem; }
.form-title { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 900; color: white; line-height: 1.1; margin-bottom: 0.5rem; }
.form-title span { color: transparent; -webkit-text-stroke: 1px var(--primary); }
.form-subtitle { font-size: 0.95rem; color: var(--text-secondary); margin-bottom: 2.5rem; }

/* Form Controls Specifics */
.pwd-wrap { position: relative; display: flex; align-items: center; }
.pwd-wrap input { width: 100%; padding-right: 4.5rem; }
.eye-btn {
  position: absolute; right: 1rem; background: none; border: none;
  font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700;
  color: var(--primary); cursor: pointer; transition: color 0.3s;
}
.eye-btn:hover { color: white; }

.btn-full { width: 100%; margin-bottom: 1rem; justify-content: center; }

.divider { display: flex; align-items: center; gap: 1rem; margin: 1.5rem 0; }
.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.1); }
.divider span { font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700; color: var(--text-muted); }

.forgot-link-bottom {
  width: 100%; background: none; border: none; cursor: pointer;
  font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700;
  color: var(--text-muted); padding: 1rem 0; transition: color 0.3s; letter-spacing: 1px;
}
.forgot-link-bottom:hover { color: var(--primary); }

.register-scroll { max-height: 60vh; overflow-y: auto; padding-right: 5px; }
.register-scroll::-webkit-scrollbar { width: 4px; }
.register-scroll::-webkit-scrollbar-thumb { background: rgba(230,0,35,0.3); border-radius: 4px; }

.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

.back-btn {
  background: none; border: none; cursor: pointer; font-family: 'Space Grotesk', sans-serif;
  font-size: 0.85rem; font-weight: 700; color: var(--text-muted); transition: color 0.3s; padding: 0;
}
.back-btn:hover { color: white; }

/* Transitions */
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.fade-slide-enter-from { opacity: 0; transform: translateX(20px); }
.fade-slide-leave-to { opacity: 0; transform: translateX(-20px); }

/* Responsive */
@media (max-width: 900px) {
  .left-panel { display: none; }
  .right-panel { padding: 2rem; }
  .field-row { grid-template-columns: 1fr; }
}
</style>
