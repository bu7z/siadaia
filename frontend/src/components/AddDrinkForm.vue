<script setup>
import { ref } from 'vue'

const emit = defineEmits(['success'])

const props = defineProps({
  category: {
    type: String,
    required: true
  }
})

const newDrink = ref({
  name: '',
  packungseinheit: null,
  ml_pro_einheit: null,
  ek_preis: null,
  vk_preis: null
})

const loading = ref(false)

const resetForm = () => {
  newDrink.value = {
    name: '',
    packungseinheit: null,
    ml_pro_einheit: null,
    ek_preis: null,
    vk_preis: null
  }
}

const submitDrink = async () => {
  loading.value = true
  const token = localStorage.getItem('token')

  try {
    const res = await fetch('/api/inventar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        ...newDrink.value,
        kategorie: props.category
      })
    })

    const data = await res.json()
    loading.value = false

    if (data.success) {
      emit('success')
      resetForm()
    } else {
      alert(data.message || 'Fehler beim Hinzufügen')
    }
  } catch (err) {
    loading.value = false
    console.error(err)
    alert('Serverfehler beim Hinzufügen.')
  }
}
</script>

<template>
  <div class="card card-body bg-dark text-white mb-3 border-secondary">
    <form @submit.prevent="submitDrink">
      <div class="row g-3">
        <div class="col-md-4">
          <input
            v-model="newDrink.name"
            type="text"
            class="form-control bg-dark text-white border-secondary"
            placeholder="Name"
            required
          />
        </div>
        <div class="col-md-2">
          <input
            v-model.number="newDrink.packungseinheit"
            type="number"
            class="form-control bg-dark text-white border-secondary"
            placeholder="Packung"
            required
          />
        </div>
        <div class="col-md-2">
          <input
            v-model.number="newDrink.ml_pro_einheit"
            type="number"
            class="form-control bg-dark text-white border-secondary"
            placeholder="ML"
            required
          />
        </div>
        <div class="col-md-2">
          <input
            v-model.number="newDrink.ek_preis"
            type="number"
            step="0.01"
            class="form-control bg-dark text-white border-secondary"
            placeholder="EK (€)"
            required
          />
        </div>
        <div class="col-md-2">
          <input
            v-model.number="newDrink.vk_preis"
            type="number"
            step="0.01"
            class="form-control bg-dark text-white border-secondary"
            placeholder="VK (€)"
            required
          />
        </div>
      </div>

      <div class="text-end mt-3">
        <button :disabled="loading" type="submit" class="btn btn-success">
          {{ loading ? 'Speichern...' : 'Hinzufügen' }}
        </button>
      </div>
    </form>
  </div>
</template>
<style scoped>
::v-deep input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}
</style>