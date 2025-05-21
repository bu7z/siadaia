<template>
  <div class="modal-backdrop" v-if="show">
    <div class="modal-card bg-dark text-white shadow-lg rounded-4 p-4">
      <div class="modal-header border-0 mb-3">
        <h4 class="modal-title d-flex align-items-center gap-2">
          🍹 <span>Bestellung bestätigen</span>
        </h4>
        <button class="btn-close btn-close-white ms-auto" @click="$emit('close')"></button>
      </div>

      <div class="modal-body">
        <p><strong>Getränk:</strong> {{ drink.name }}</p>
        <p class="mb-1"><strong>Zutaten:</strong></p>
        <ul class="list-unstyled ms-3 mb-3">
          <li v-for="z in drink.zutaten" :key="z" class="small">
            <span class="text-muted">–</span> {{ z }}
          </li>
        </ul>
        <p><strong>Preis:</strong> {{ drink.preis }}</p>

        <div class="mt-4">
          <label for="kundenname" class="form-label">Dein Name:</label>
          <input
            v-model="kundenname"
            id="kundenname"
            type="text"
            class="form-control bg-dark text-white border-light"
            placeholder="Max Mustermann"
          />
        </div>
      </div>

      <div class="modal-footer border-0 mt-4 d-flex justify-content-end">
        <button class="btn btn-outline-light me-2" @click="$emit('close')">Abbrechen</button>
        <button class="btn btn-success" :disabled="!kundenname.trim()" @click="sendeBestellung">
          Bestellen
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  drink: Object,
  show: Boolean
})
const emit = defineEmits(['close', 'bestellt'])
const kundenname = ref('')

const sendeBestellung = async () => {
  const preisZahl = parseFloat(props.drink.preis.replace('€', '').trim())

  const payload = {
    drink_name: props.drink.name,
    zutaten: props.drink.zutaten,
    preis: preisZahl,
    kundenname: kundenname.value.trim()
  }

  const res = await fetch('/api/bestellungen', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })

  const result = await res.json()
  if (result.success) {
  emit('bestellt')
  kundenname.value = ''
} else {
  errorMessage.value = '❌ Bestellung fehlgeschlagen: ' + result.message
  showErrorToast.value = true
  setTimeout(() => showErrorToast.value = false, 4000)
}

}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-card {
  width: 90%;
  max-width: 500px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  animation: popIn 0.2s ease-out;
}

@keyframes popIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
