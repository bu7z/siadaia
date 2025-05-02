<script setup>
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
import HeroInventory from '@/components/HeroInventory.vue'

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const user = ref(null)
const password = ref('')
const message = ref('')
const error = ref('')
const loading = ref(true)

const token = localStorage.getItem('token')

onMounted(async () => {
  if (!token) {
    router.push('/')
    return
  }

  try {
    const res = await fetch('/api/verify-token', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    })

    const data = await res.json()

    if (data.success) {
      user.value = data.user
      loading.value = false
    } else {
      localStorage.removeItem('token')
      router.push('/')
    }
  } catch (err) {
    console.error('Fehler beim Token-Check:', err)
    localStorage.removeItem('token')
    router.push('/')
  }
})

const changePassword = async () => {
  try {
    const res = await axios.post('/api/change-password', {
      id: user.value.id,
      new_password: password.value
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    message.value = 'Passwort erfolgreich geändert!'
    error.value = ''
    password.value = ''
  } catch (err) {
    error.value = 'Fehler beim Ändern des Passworts.'
    message.value = ''
    console.error(err)
  }
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/')
}
</script>

<template>
  <div class="page-wrapper">
    <!-- Header -->
    <HeroInventory />

    <!-- Loading Spinner -->
    <div v-if="loading" class="text-center text-white py-5">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Lade...</span>
      </div>
    </div>

    <!-- Dashboard Layout -->
    <div v-else class="dashboard-container text-white">
      <NavBar class="sidebar" />

      <main class="main-content px-4 py-4">
        <h2>Benutzerprofil</h2>
        <p class="mb-4">Hier kannst du deine Daten einsehen und dein Passwort ändern.</p>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-if="message" class="alert alert-success">{{ message }}</div>

        <div class="card bg-dark text-white p-4">
          <p><strong>Benutzername:</strong> {{ user.username }}</p>
          <p><strong>ID:</strong> {{ user.id }}</p>
          <p><strong>Rolle:</strong> {{ user.rolle }}</p>

          <div class="mt-4">
            <label for="password" class="form-label">Neues Passwort</label>
            <input
              type="password"
              class="form-control bg-dark text-white border-secondary"
              id="password"
              v-model="password"
              placeholder="Neues Passwort eingeben"
            />
            <button class="btn btn-primary mt-2" @click="changePassword">Passwort ändern</button>
          </div>

          <button class="btn btn-danger mt-4" @click="logout">Logout</button>
        </div>
      </main>
    </div>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #121212;
}

.dashboard-container {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 70px;
  background-color: #1f1f1f;
  border-right: 1px solid #333;
}

.main-content {
  flex: 1;
}

.card {
  border: 1px solid #444;
  border-radius: 10px;
}
</style>
