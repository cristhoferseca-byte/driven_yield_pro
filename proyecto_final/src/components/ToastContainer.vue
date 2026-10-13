<template>
  <div class="toast-container" aria-live="polite" aria-atomic="true">
    <div v-for="t in toasts" :key="t.id" :class="['toast-item', t.type]" role="alert">
      <span>{{ t.type === 'success' ? '✓' : t.type === 'error' ? '✕' : 'ℹ' }}</span>
      {{ t.message }}
    </div>
  </div>
</template>

<script setup>
import { useToast } from '../stores/toast'
const { toasts } = useToast()
</script>
