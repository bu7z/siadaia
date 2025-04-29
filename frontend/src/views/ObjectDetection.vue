<script setup lang="ts">
import { ref } from 'vue'
import Footer from '@/components/Footer.vue'
import HeroInventory from '@/components/HeroInventory.vue'
import NavBar from '@/components/NavBar.vue'
import PersonCountChart from '@/components/PersonCountChart.vue'

const showCamera = ref(false)
</script>

<template>
  <HeroInventory />

  <div class="object-detection-container text-white">
    <NavBar />

    <main class="main-content px-4 py-4">
      <h2 class="fw-bold mb-4">Objekterkennung (Live Feed)</h2>

      <div class="row g-4">
        <!-- Kamera-Feed -->
        <div class="col-12 col-md-6">
          <div class="card shadow-lg h-100">
            <div class="card-body bg-white text-dark">
              <button
                class="btn btn-primary mb-3"
                @click="showCamera = !showCamera"
              >
                {{ showCamera ? 'Kamera ausblenden' : 'Kamera anzeigen' }}
              </button>

              <!-- Nur anzeigen wenn Kamera aktiv -->
              <div v-if="showCamera" class="border rounded overflow-hidden">
                <!-- Zeitstempel zwingt Browser, den Feed neu zu laden -->
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

        <!-- Live-Chart -->
        <div class="col-12 col-md-6">
          <div class="card shadow-lg h-100">
            <div class="card-body bg-white text-dark">
              <PersonCountChart />
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>

  <Footer />
</template>

<style scoped>
.object-detection-container {
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
