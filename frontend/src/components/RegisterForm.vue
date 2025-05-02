<template>
    <div class="modal fade" id="registerModal" tabindex="-1" aria-labelledby="registerModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-dark text-white border-0 shadow-lg">
          <div class="modal-header border-0">
            <h5 class="modal-title" id="registerModalLabel">Registrierung</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
  
          <div class="modal-body">

             <!-- Alert für Erfolg / Fehler -->
            <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger']" role="alert">
              {{ message }}
            </div>

            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label for="username" class="form-label">Benutzername</label>
                <input
                  v-model="username"
                  type="text"
                  class="form-control bg-dark text-white border-secondary"
                  id="username"
                  required
                />
              </div>
  
              <div class="mb-3">
                <label for="password" class="form-label">Passwort</label>
                <input
                  v-model="password"
                  type="password"
                  class="form-control bg-dark text-white border-secondary"
                  id="password"
                  required
                />
              </div>
  
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">Passwort bestätigen</label>
                <input
                  v-model="confirmPassword"
                  type="password"
                  class="form-control bg-dark text-white border-secondary"
                  id="confirmPassword"
                  required
                />
              </div>
  
              <div class="mb-3">
                <label for="vorname" class="form-label">Vorname</label>
                <input
                  v-model="vorname"
                  type="text"
                  class="form-control bg-dark text-white border-secondary"
                  id="vorname"
                />
              </div>
  
              <div class="mb-3">
                <label for="nachname" class="form-label">Nachname</label>
                <input
                  v-model="nachname"
                  type="text"
                  class="form-control bg-dark text-white border-secondary"
                  id="nachname"
                />
              </div>
  
              <div class="d-grid mt-4">
                <button type="submit" class="btn btn-primary">
                  Registrierung abschicken
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, defineEmits } from 'vue'
  import * as bootstrap from 'bootstrap'

const emit = defineEmits(['switchToLogin'])

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const vorname = ref('')
const nachname = ref('')
const message = ref('')
const messageType = ref('') // success | danger

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    message.value = 'Passwörter stimmen nicht überein.'
    messageType.value = 'danger'
    return
  }

  try {
    const res = await fetch('http://localhost:5000/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        vorname: vorname.value,
        nachname: nachname.value
      })
    })

    const data = await res.json()

    if (data.success) {
      message.value = data.message || 'Registrierung erfolgreich!'
      messageType.value = 'success'
      
      // NICHT SOFORT Form schließen
      setTimeout(() => {
        const modal = bootstrap.Modal.getOrCreateInstance('#registerModal')
        modal.hide()

        emit('switchToLogin', {
          username: username.value,
          password: password.value
        })
      }, 500)


    } else {
      message.value = data.message || 'Fehler bei der Registrierung'
      messageType.value = 'danger'
    }
  } catch (err) {
    message.value = 'Verbindungsfehler mit dem Server.'
    messageType.value = 'danger'
  }
}

const resetForm = () => {
  username.value = ''
  password.value = ''
  confirmPassword.value = ''
  vorname.value = ''
  nachname.value = ''
}
  </script>
  