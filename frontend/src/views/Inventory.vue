<script setup>
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
import HeroInventory from '@/components/HeroInventory.vue'
import InventoryChart from '@/components/InventoryChart.vue'
import PersonChart from '@/components/PersonChart.vue'

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)
const loading = ref(true)

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/')

  try {
    const res = await fetch('/api/verify-token', {
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
    console.error('Token-Fehler:', err)
    localStorage.removeItem('token')
    router.push('/')
  }
})
</script>

<template>
  <HeroInventory />

  <div v-if="loading" class="text-center text-white py-5">
    <div class="spinner-border text-light" role="status">
      <span class="visually-hidden">Lade...</span>
    </div>
  </div>

  <div v-else class="dashboard-container text-white">
    <NavBar />

    <main class="main-content px-4 py-4">
      <h2>Hallo, {{ user.username }}</h2>
      <p class="mb-4">Du bist eingeloggt als <strong>{{ user.rolle }}</strong>.</p>

      <div class="container my-5">
        <div class="row g-4">
          <div class="col-md-6">
            <InventoryChart />
          </div>
          <div class="col-md-6">
            <PersonChart />
          </div>
        </div>
      </div>
    </main>
  </div>

  <Footer />
</template>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background-color: #121212;
}

.main-content {
  flex: 1;
}
</style>
