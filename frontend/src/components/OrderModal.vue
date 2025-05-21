// === OrderModal.vue ===
<template>
  <div class="modal-backdrop" v-if="show">
    <div class="modal-content bg-dark text-white rounded-3 p-4 shadow-lg">
      <h4 class="mb-3">🍹 Bestellung bestätigen</h4>
      <p><strong>Getränk:</strong> {{ drink.name }}</p>
      <p><strong>Zutaten:</strong></p>
      <ul>
        <li v-for="z in drink.zutaten" :key="z">{{ z }}</li>
      </ul>
      <p><strong>Preis:</strong> {{ drink.preis }}</p>
      <div class="mt-3">
        <label for="kundenname" class="form-label">Dein Name:</label>
        <input v-model="kundenname" id="kundenname" type="text" class="form-control bg-dark text-white border-light" />
      </div>
      <div class="d-flex justify-content-end mt-4">
        <button class="btn btn-secondary me-2" @click="$emit('close')">Abbrechen</button>
        <button class="btn btn-success" :disabled="!kundenname.trim()" @click="sendeBestellung">Bestellen</button>
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

  console.log("Bestellung →", payload)

  const res = await fetch('/api/bestellungen', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })

  const result = await res.json()
  if (result.success) {
    emit('bestellt')
    kundenname.value = ''
  } else {
    alert('❌ Bestellung fehlgeschlagen: ' + result.message)
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  background: rgba(0, 0, 0, 0.7);
  z-index: 2000;
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  width: 90%;
  max-width: 500px;
}
</style>