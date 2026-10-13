<template>
  <main class="reset-root">
    <section class="reset-panel matte-card">
      <p class="form-eyebrow">RECUPERACIÓN DE ACCESO</p>
      <h1 class="form-title">Nueva <span>Contraseña</span></h1>
      <p class="form-subtitle">Ingresa una clave segura para volver al sistema.</p>

      <div v-if="!token" class="alert-box">
        Enlace inválido o incompleto. Solicita un nuevo restablecimiento desde el login.
      </div>

      <template v-else>
        <div class="form-group">
          <label>Nueva contraseña</label>
          <input v-model="password" type="password" placeholder="Mínimo 6 caracteres" @keyup.enter="handleReset" />
        </div>

        <div class="form-group">
          <label>Confirmar contraseña</label>
          <input v-model="confirm" type="password" placeholder="Repite la contraseña" @keyup.enter="handleReset" />
        </div>

        <button class="btn btn-primary btn-full" :disabled="auth.loading" @click="handleReset">
          {{ auth.loading ? 'ACTUALIZANDO...' : 'ACTUALIZAR CONTRASEÑA' }}
        </button>
      </template>

      <router-link to="/login" class="btn btn-ghost btn-full">Volver al login</router-link>
    </section>
  </main>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../stores/toast'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const password = ref('')
const confirm = ref('')
const token = computed(() => String(route.query.token || ''))

/**
 * Valida y procesa el restablecimiento de la contraseña mediante token de recuperación.
 */
async function handleReset() {
  if (!token.value) { toast.error('Enlace inválido.'); return }
  if (password.value.length < 6) { toast.error('La contraseña debe tener al menos 6 caracteres.'); return }
  if (password.value !== confirm.value) { toast.error('Las contraseñas no coinciden.'); return }

  const res = await auth.resetPassword(token.value, password.value)
  if (!res.ok) { toast.error(res.error); return }

  toast.success(res.message)
  router.push('/login')
}
</script>

<style scoped>
.reset-root {
  min-height: 100vh;
  padding: calc(var(--nav-height) + 2rem) 1.5rem 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-base);
}

.reset-panel {
  width: min(100%, 460px);
  padding: 2.5rem;
}

.form-eyebrow {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: 2px;
  margin-bottom: 0.5rem;
}

.form-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 2rem;
  font-weight: 900;
  color: white;
  line-height: 1.1;
  margin-bottom: 0.5rem;
}

.form-title span { color: var(--primary); }
.form-subtitle { color: var(--text-secondary); margin-bottom: 2rem; }
.btn-full { width: 100%; margin-top: 0.5rem; }
.alert-box {
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 8px;
  background: rgba(255, 184, 0, 0.08);
  border: 1px solid rgba(255, 184, 0, 0.25);
  color: var(--warning);
}
</style>
