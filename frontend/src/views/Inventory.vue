<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import HeroInventory from '../components/HeroInventory.vue'
import Footer from '@/components/Footer.vue'

const router = useRouter()
const user = ref(null)
const error = ref('')
const loading = ref(true)

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
    localStorage.removeItem('token')
    router.push('/')
  }
})
</script>

<template>
  <div v-if="loading" class="text-center text-white py-5">
    <div class="spinner-border text-light" role="status">
      <span class="visually-hidden">Lade...</span>
    </div>
  </div>

  <div v-else class="dashboard-container text-white">
    <aside class="sidebar d-flex flex-column align-items-center pt-4">
      <img src="@/assets/SIA_logo.svg" alt="SIA Logo" style="width: 40px; margin-bottom: 2rem;" />
      <i class="bi bi-box-seam fs-4 mb-4" title="Inventory"></i>
      <i class="bi bi-bar-chart-line fs-4 mb-4" title="Statistics"></i>
      <i class="bi bi-person-circle fs-4" title="User"></i>
    </aside>

    <main class="main-content px-4 py-4">
      <h2>Hallo, {{ user.username }} 👋</h2>
      <p class="mb-4">Du bist eingeloggt als <strong>{{ user.rolle }}</strong>.</p>

      <HeroInventory />
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
