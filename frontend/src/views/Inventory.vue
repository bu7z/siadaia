<script setup>
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
import HeroInventory from '@/components/HeroInventory.vue'
import InventoryChart from '@/components/InventoryChart.vue'

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')

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
    console.error('❌ Fehler beim Token-Check:', err)
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
      <h2>Hallo, {{ user.username }} 👋</h2>
      <p class="mb-4">Du bist eingeloggt als <strong>{{ user.rolle }}</strong>.</p>

      <div class="container my-5">
        <div class="row g-4">
          <div class="col-md-6">
            <InventoryChart />
          </div>
          <div class="col-md-6">
            <InventoryChart />
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

.sidebar {
  width: 70px;
  background-color: #1f1f1f;
  border-right: 1px solid #333;
  min-height: 100%;
}

.main-content {
  flex: 1;
}

i {
  color: #ccc;
  cursor: pointer;
}

i:hover {
  color: white;
}
</style>
