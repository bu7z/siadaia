<script setup>
import Footer from '@/components/Footer.vue'
import HeroInventory from '@/components/HeroInventory.vue'
import NavBar from '@/components/NavBar.vue'
import StockChart from '@/components/StockChart.vue'
import AddDrinkForm from '@/components/AddDrinkForm.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const openCategory = ref(null)
const categorizedDrinks = ref({})
const showForm = ref({})
const user = ref(null)
const loading = ref(true)

const kategorien = [
  'Biere',
  'Softdrinks 0,33l',
  'Softdrinks 1l',
  'Spirituosen'
]

const toggleCategory = async (category) => {
  if (openCategory.value === category) {
    openCategory.value = null
    return
  }

  const token = localStorage.getItem('token')
  const res = await fetch(`/api/bestand-kategorie/${encodeURIComponent(category)}`, {
    headers: { Authorization: `Bearer ${token}` }
  })

  const data = await res.json()
  if (data?.data) {
    categorizedDrinks.value[category] = data.data
    openCategory.value = category
  } else {
    categorizedDrinks.value[category] = []
    openCategory.value = category
  }
}

const toggleForm = (category) => {
  showForm.value[category] = !showForm.value[category]
}

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
    console.error('Fehler beim Token-Check:', err)
    localStorage.removeItem('token')
    router.push('/')
  }
})
</script>

<template>
  <div class="page-wrapper">
    <HeroInventory />

    <div class="dashboard-container text-white" v-if="!loading">
      <NavBar class="sidebar" />

      <main class="main-content p-4">
        <h2 class="text-white mb-4">
          <i class="bi bi-box-seam"></i> Bestand nach Kategorie
        </h2>

        <div v-for="cat in kategorien" :key="cat" class="mb-4">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <button
              class="btn btn-outline-light w-100 text-start me-2"
              @click="toggleCategory(cat)"
            >
              {{ cat }}
            </button>
            <button
              class="btn btn-sm btn-success ms-2"
              title="Getränk hinzufügen"
              @click="toggleForm(cat)"
            >
              <i class="bi bi-plus-lg"></i>
            </button>
          </div>

          <!-- Formular zum Hinzufügen -->
          <AddDrinkForm
            v-if="showForm[cat]"
            :category="cat"
            @success="() => toggleCategory(cat)"
          />

          <!-- Tabelle + Chart -->
          <div v-if="openCategory === cat" class="mt-3">
            <!-- Tabelle -->
            <div class="overflow-auto mb-4">
              <table class="table table-dark table-bordered text-center w-100">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Packungseinheit</th>
                    <th>ML pro Einheit</th>
                    <th>EK Preis (€)</th>
                    <th>VK Preis (€)</th>
                    <th>Bestand</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in categorizedDrinks[cat] || []" :key="item.name">
                    <td>{{ item.name }}</td>
                    <td>{{ item.packungseinheit }}</td>
                    <td>{{ item.ml_pro_einheit }}</td>
                    <td>{{ item.ek_preis.toFixed(2) }}</td>
                    <td>{{ item.vk_preis.toFixed(2) }}</td>
                    <td>{{ item.bestand }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Chart -->
            <div class="overflow-auto mb-4">
              <StockChart
                v-if="categorizedDrinks[cat]"
                :category="cat"
                :data="categorizedDrinks[cat].map(item => ({
                  name: item.name,
                  bestand: item.bestand
                }))"
              />
            </div>
          </div>
        </div>
      </main>
    </div>

    <Footer />
  </div>
</template>

<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #121212;
  overflow-x: hidden;
}

.dashboard-container {
  display: flex;
  flex: 1;
  flex-wrap: wrap;
  width: 100%;
}

.sidebar {
  width: 70px;
  background-color: #1f1f1f;
  border-right: 1px solid #333;
}

.main-content {
  flex: 1;
  min-width: 0;
}

.overflow-auto {
  overflow-x: auto;
}
</style>
