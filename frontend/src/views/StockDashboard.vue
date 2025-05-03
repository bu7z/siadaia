<script setup>
import Footer from '@/components/Footer.vue'
import HeroInventory from '@/components/HeroInventory.vue'
import NavBar from '@/components/NavBar.vue'
import { ref, onMounted } from 'vue'

const inventory = ref([])
const categories = ref([])
const openCategory = ref(null)

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('/api/inventar', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })

  const data = await res.json()
  if (data.success) {
    inventory.value = data.inventar

    // Einzigartige Kategorien extrahieren
    categories.value = [...new Set(inventory.value.map(item => item.kategorie))]
  }
})
</script>

<template>
  <div class="page-wrapper">
    <HeroInventory />

    <div class="dashboard-container text-white">
      <NavBar class="sidebar" />

      <main class="main-content p-4 flex-grow-1">
        <h2 class="mb-4">📦 Bestand nach Kategorie</h2>

        <div v-for="cat in categories" :key="cat" class="mb-3">
          <button class="btn btn-outline-light w-100 text-start" @click="openCategory = openCategory === cat ? null : cat">
            {{ cat }}
          </button>

          <div v-show="openCategory === cat" class="mt-2">
            <table class="table table-dark table-striped table-bordered">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Packungseinheit</th>
                  <th>ML pro Einheit</th>
                  <th>EK Preis (€)</th>
                  <th>VK Preis (€)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in inventory.filter(i => i.kategorie === cat)" :key="item.id">
                  <td>{{ item.name }}</td>
                  <td>{{ item.packungseinheit }}</td>
                  <td>{{ item.ml_pro_einheit }}</td>
                  <td>{{ item.ek_preis.toFixed(2) }}</td>
                  <td>{{ item.vk_preis.toFixed(2) }}</td>
                </tr>
              </tbody>
            </table>
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
