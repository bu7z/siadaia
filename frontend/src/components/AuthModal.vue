<template>
    <div
      class="modal fade"
      id="authModal"
      tabindex="-1"
      aria-labelledby="authModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-dark text-white border-0 shadow-lg">
          <div class="modal-header border-0">
            <h5 class="modal-title" id="authModalLabel">Login oder Registrierung</h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="username" class="form-label">Benutzername</label>
                <input
                  v-model="username"
                  type="text"
                  class="form-control bg-dark text-white border-secondary"
                  id="username"
                  placeholder="z. B. admin01"
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
                  placeholder="••••••••"
                  required
                />
              </div>
              <div class="d-flex justify-content-between mt-4">
                <button type="submit" class="btn btn-outline-light w-50 me-2">
                  Login
                </button>
                <button
                    type="button"
                    class="btn btn-primary w-50"
                    data-bs-toggle="modal"
                    data-bs-target="#registerModal"
                    >
                    Registrieren
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>


    <RegisterForm />
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import RegisterForm from './RegisterForm.vue'
  
  const username = ref('')
  const password = ref('')
  
  const handleLogin = () => {
    console.log('Login:', username.value, password.value)
    // Hier kommt später dein API-Call hin
    // z.B. fetch('/api/login', { method: 'POST', body: JSON.stringify(...) })
  }
  
  const handleRegister = () => {
    console.log('Register:', username.value, password.value)
    // Hier ebenfalls Registrierungshandler
  }
  </script>
  