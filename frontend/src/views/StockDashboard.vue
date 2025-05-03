<script setup>
import Footer from '@/components/Footer.vue'
import HeroInventory from '@/components/HeroInventory.vue'
import NavBar from '@/components/NavBar.vue'
import StockChart from '@/components/StockChart.vue'
import { ref, onMounted } from 'vue'

const openCategory = ref(null)
const categorizedDrinks = ref({})

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
</script>

<template>
  <div class="page-wrapper">
    <HeroInventory />

    <div class="dashboard-container text-white">
      <NavBar class="sidebar" />

      <main class="main-content p-4">
        <h2 class="text-white mb-4"><i class="bi bi-box-seam"></i> Bestand nach Kategorie</h2>

        <div v-for="cat in kategorien" :key="cat" class="mb-3">
          <button
            class="btn btn-outline-light w-100 text-start"
            @click="toggleCategory(cat)"
          >
            {{ cat }}
          </button>

          <div v-if="openCategory === cat" class="mt-3">
            <!-- Tabelle -->
            <div class="table-responsive mb-4">
              <table class="table table-dark table-bordered text-center">
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
                  <tr v-for="item in categorizedDrinks[cat] || []" :key="item.id">
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
</style>
