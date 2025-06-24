<script setup>
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
import HeroInventory from '@/components/HeroInventory.vue'
import InventoryChart from '@/components/InventoryChart.vue'
import PersonChart from '@/components/PersonChart.vue'
import PersonCountChart from '@/components/PersonCountChart.vue'

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)
const loading = ref(true)
const showCamera = ref(false)

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

        <!-- Accordion für Objekterkennung -->
        <div class="accordion mt-5" id="objectDetectionAccordion">
          <div class="accordion-item bg-dark text-white border-secondary">
            <h2 class="accordion-header" id="headingDetection">
              <button
                class="accordion-button collapsed bg-dark text-white"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#collapseDetection"
                aria-expanded="false"
                aria-controls="collapseDetection"
              >
                Objekterkennung (Live Feed)
              </button>
            </h2>
            <div
              id="collapseDetection"
              class="accordion-collapse collapse"
              aria-labelledby="headingDetection"
              data-bs-parent="#objectDetectionAccordion"
            >
              <div class="accordion-body">
                <!-- Kamera-Feed & Chart -->
                <div class="row g-4">
                  <div class="col-md-6">
                    <div class="card shadow-lg h-100">
                      <div class="card-body dark-card text-dark">
                        <button
                          class="btn btn-primary mb-3"
                          @click="showCamera = !showCamera"
                        >
                          {{ showCamera ? 'Kamera ausblenden' : 'Kamera anzeigen' }}
                        </button>

                        <div v-if="showCamera" class="border rounded overflow-hidden">
                          <img
                            :src="'/api/camera-feed-aud?' + Date.now()"
                            alt="Kamera Feed"
                            class="img-fluid w-100"
                            style="object-fit: contain;"
                          />
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="card shadow-lg h-100">
                      <div class="card-body dark-card">
                        <PersonCountChart />
                      </div>
                    </div>
                  </div>
                </div>
                <!-- Ende Kamera & Chart -->
              </div>
            </div>
          </div>
        </div>
        <!-- Ende Accordion -->
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

.accordion-button:not(.collapsed) {
  background-color: #2c2c2c;
  color: #fff;
}

.accordion-body {
  background-color: #1f1f1f;
}

.dark-card {
  background-color: #1e293b;
  border: 1px solid #2d3748;
  color: #fff;
  padding: 1rem;
  border-radius: 0.5rem;
}
</style>
