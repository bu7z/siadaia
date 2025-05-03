<!-- components/AddStockOverlay.vue -->
<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: Boolean,
  drink: Object
})

const emit = defineEmits(['close', 'success'])

const anzahl = ref(null)
const saving = ref(false)

watch(() => props.show, (visible) => {
  if (visible) anzahl.value = null
})

const speichern = async () => {
  if (!anzahl.value || isNaN(anzahl.value)) return

  saving.value = true
  const token = localStorage.getItem('token')

  try {
    const res = await fetch('/api/bestand', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        inventar_id: props.drink.id,
        anzahl: anzahl.value
      })
    })

    const data = await res.json()
    saving.value = false

    if (data.success) {
      emit('success')
      emit('close')
    } else {
      alert(data.message || 'Fehler beim Speichern')
    }
  } catch (err) {
    saving.value = false
    console.error(err)
    alert('Serverfehler')
  }
}
</script>

<template>
  <div v-if="show" class="overlay">
    <div class="overlay-content bg-dark text-white p-4 rounded shadow">
      <h5>📦 Bestand aktualisieren – {{ drink.name }}</h5>

      <input
        v-model.number="anzahl"
        type="number"
        class="form-control bg-dark text-white border-secondary mt-3"
        placeholder="Neue Anzahl Flaschen"
      />

      <div class="mt-4 d-flex justify-content-end gap-2">
        <button class="btn btn-secondary" @click="emit('close')">Abbrechen</button>
        <button class="btn btn-success" :disabled="saving" @click="speichern">
          {{ saving ? 'Speichern...' : 'Speichern' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.7);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.overlay-content {
  width: 100%;
  max-width: 400px;
}
</style>
