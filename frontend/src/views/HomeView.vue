<script setup>
import AuthModal from '../components/AuthModal.vue'
import Footer from '@/components/Footer.vue'
import FadeOverlay from '@/components/FadeOverlay.vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()
const isFading = ref(false)

const handleFadeAndRedirect = () => {
  isFading.value = true
  setTimeout(() => {
    router.push('/inventory')
  }, 600)
}

const goToDrinkView = () => {
  isFading.value = true
  setTimeout(() => {
    router.push('/drink')
  }, 600)
}
</script>

<template>
  <div class="home-view-container position-relative overflow-hidden">
    <!-- Reusable Fade Transition -->
    <FadeOverlay :visible="isFading" />
    

    <!-- HERO -->
    <div class="bg-dark text-white text-center p-5 rounded-bottom shadow-sm">
      <img
        src="@/assets/SIA_logo.svg"
        alt="SIA Logo"
        class="img-fluid mb-3"
        style="max-height: 100px;"
      />
      <p class="text-white-50 mb-1 fs-6">Drink & Inventory Advisory</p>
      <p class="lead mb-0">Der Erste seiner Art.</p>
    </div>

    <!-- BERATUNGSAUSWAHL -->
    <section class="container text-center py-5">
      <h2 class="mb-5 fw-semibold">Nach welcher Art von Beratung suchen Sie?</h2>
      <div class="d-flex flex-column flex-md-row justify-content-center align-items-center gap-4 mb-5">
        <button class="btn advisory-btn btn-drink px-5 py-3" @click="goToDrinkView">
          🍹 Drink Advisory
        </button>
        <button class="btn advisory-btn btn-inventory px-5 py-3" data-bs-toggle="modal" data-bs-target="#authModal">
          📦 Inventory Advisory
        </button>
      </div>
    </section>

    <!-- FEATURES -->
    <section class="bg-dark text-white py-5">
      <div class="container">
        <div class="row g-4 text-center">
          <div class="col-md-4">
            <div class="p-4 card-box h-100">
              <i class="bi bi-graph-up-arrow display-5 text-info mb-2"></i>
              <h5 class="fw-semibold">Visualisierte Daten</h5>
              <p class="text-white-50 mb-0">Kennzahlen klar und verständlich aufbereitet.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="p-4 card-box h-100">
              <i class="bi bi-lightning-charge display-5 text-success mb-2"></i>
              <h5 class="fw-semibold">Echtzeit-Analyse</h5>
              <p class="text-white-50 mb-0">Direkte Einblicke in Verbrauch und Bestand.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="p-4 card-box h-100">
              <i class="bi bi-people display-5 text-warning mb-2"></i>
              <h5 class="fw-semibold">Benutzerrollen</h5>
              <p class="text-white-50 mb-0">Verwalte Team und Rechte komfortabel.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- WHY SIA -->
    <section class="bg-dark text-white py-5 border-top">
      <div class="container text-center">
        <h3 class="mb-3">
          Warum
          <img
            src="@/assets/Sia_klein_Schwarz_Transp.svg"
            alt="SIA Logo"
            class="img-fluid mb-2"
            style="max-height: 35px;"
          />?
        </h3>
        <p class="text-white-50 fs-5">
          Weil moderne Bars und Events datengetrieben arbeiten. SIA bietet dir smarte Einblicke – damit du immer weißt, was läuft.
        </p>
      </div>
    </section>

    <!-- MOCKUP -->
    <section class="bg-black text-white py-5">
      <div class="container text-center">
        <h3 class="mb-4">Ein Blick in dein zukünftiges Dashboard</h3>
        <img src="@/assets/mockup-placeholder.png" class="img-fluid rounded shadow" alt="Dashboard Preview" />
      </div>
    </section>

    <AuthModal @startFade="handleFadeAndRedirect" />
    <Footer />
  </div>
</template>

<style scoped>
h2 {
  font-weight: 600;
}

.advisory-btn {
  font-size: 1.2rem;
  font-weight: 500;
  border-radius: 50px;
  min-width: 240px;
  transition: all 0.2s ease-in-out;
}

.btn-drink {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  border: none;
}

.btn-inventory {
  background: linear-gradient(135deg, #f8f9fa, #dee2e6);
  color: #212529;
  border: none;
}

.advisory-btn:hover {
  transform: scale(1.04);
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.3);
}

.card-box {
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(6px);
  border-radius: 1rem;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card-box:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
}
</style>
