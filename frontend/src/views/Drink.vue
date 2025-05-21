<script setup>
import Footer from '@/components/Footer.vue'
import HeroDrink from '@/components/HeroDrink.vue'
import SwipeDeck from '@/components/SwipeDeck.vue'
import OrderModal from '@/components/OrderModal.vue'
import { ref } from 'vue'

const activeCard = ref('')
const step = ref(1)
const selectedVibe = ref('')
const preferences = ref([])
const drinkSuggestion = ref('')
const suggestionError = ref('')
const responseText = ref('')
const parsedDrink = ref(null)
const recommendationText = ref('')
const showResponseModal = ref(false)
const loadingOverlay = ref(false)
const showOrderModal = ref(false)
const selectedDrink = ref(null)
const showSuccessToast = ref(false)

const vibes = ['Edle Stimmung', 'Entspannt', 'Brauche Energie', 'Wenig Alkohol', 'Überrasch mich', 'Alkoholfrei']
const prefOptions = ['Süß', 'Bitter', 'Fruchtig', 'Stark', 'Würzig', 'Saisonal']

const togglePref = (pref) => {
  preferences.value.includes(pref)
    ? preferences.value = preferences.value.filter(p => p !== pref)
    : preferences.value.push(pref)
}

const resetForm = () => {
  step.value = 1
  selectedVibe.value = ''
  preferences.value = []
}

const handleBestellClick = () => {
  showResponseModal.value = false
  selectedDrink.value = parsedDrink.value
  setTimeout(() => {
    showOrderModal.value = true
  }, 200)
}

const onBestellungAbgeschlossen = () => {
  showOrderModal.value = false
  selectedDrink.value = null
  parsedDrink.value = null
  showSuccessToast.value = true
  setTimeout(() => {
    showSuccessToast.value = false
  }, 3500)
}

const parseResponse = (data) => {
  try {
    const parsed = JSON.parse(data.drink)
    parsedDrink.value = parsed
    recommendationText.value = parsed.Empfehlungstext || ''
  } catch {
    parsedDrink.value = null
    recommendationText.value = data.drink
  }
}

const submitAdvisor = async () => {
  loadingOverlay.value = true
  try {
    const res = await fetch('/api/beratung', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ vibe: selectedVibe.value, preferences: preferences.value })
    })
    const data = await res.json()
    responseText.value = data.drink
    parseResponse(data)
    showResponseModal.value = true
  } catch (err) {
    console.error(err)
    responseText.value = '⚠️ Fehler beim Senden der Anfrage.'
    showResponseModal.value = true
  } finally {
    loadingOverlay.value = false
    resetForm()
    activeCard.value = ''
  }
}

const validateDrinkName = async () => {
  const trimmed = drinkSuggestion.value.trim()
  const isValid = /^[a-zA-ZäöüÄÖÜß\s]+$/.test(trimmed) && trimmed.split(' ').length <= 3

  if (!isValid) {
    suggestionError.value = 'Bitte nur einen Getränkenamen eingeben.'
    return
  }

  loadingOverlay.value = true
  try {
    const res = await fetch('/api/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ drink: trimmed })
    })
    const data = await res.json()
    responseText.value = data.drink
    parseResponse(data)
    showResponseModal.value = true
  } catch (err) {
    console.error(err)
    responseText.value = '⚠️ Fehler beim Prüfen.'
    showResponseModal.value = true
  } finally {
    loadingOverlay.value = false
    drinkSuggestion.value = ''
    suggestionError.value = ''
    activeCard.value = ''
  }
}
</script>

<template>
  <div v-if="loadingOverlay" class="loading-backdrop">
    <div class="spinner-border text-light" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <!-- Drink Info Modal -->
  <div v-if="showResponseModal" class="modal fade show" tabindex="-1" style="display: block; background: rgba(0,0,0,0.6);" @click.self="showResponseModal = false">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark text-white border-0 rounded-4 shadow-lg p-4">
        <div class="modal-header border-0">
          <h5 class="modal-title">🍹 Drink Info</h5>
          <button type="button" class="btn-close btn-close-white" @click="showResponseModal = false"></button>
        </div>
        <div class="modal-body">
          <div v-if="parsedDrink">
            <p>{{ recommendationText }}</p>
            <p class="mt-3"><strong>{{ parsedDrink.name }}</strong></p>
            <ul class="mb-2">
              <li v-for="z in parsedDrink.zutaten" :key="z">{{ z }}</li>
            </ul>
            <p><strong>Preis:</strong> {{ parsedDrink.preis }}</p>
            <button class="btn btn-success mt-3" @click="handleBestellClick">Jetzt bestellen</button>
          </div>
          <div v-else>
            <p>{{ responseText }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Bestellung Modal -->
  <OrderModal
    v-if="selectedDrink"
    :show="showOrderModal"
    :drink="selectedDrink"
    @close="showOrderModal = false"
    @bestellt="onBestellungAbgeschlossen"
  />

  <!-- Bestellung Erfolgreich Toast -->
  <transition name="fade">
    <div
      v-if="showSuccessToast"
      class="toast-success position-fixed bottom-0 end-0 m-4 p-3 bg-success text-white rounded shadow-lg d-flex align-items-center gap-3"
      style="z-index: 3000; min-width: 220px;"
    >
      <span class="fs-4">✅</span>
      <span>Bestellung erfolgreich!</span>
    </div>
  </transition>

  <HeroDrink />
  <div class="container py-5">
    <h2 class="text-center fw-bold mb-5">Your personal drink advisor</h2>
    <div class="row justify-content-center g-4">
      <!-- Beratung -->
      <div class="col-12 col-md-6">
        <div class="flip-card" :class="{ flipped: activeCard === 'advisor' }">
          <div class="flip-card-inner">
            <div class="flip-card-front" @click="activeCard = 'advisor'">
              <div class="card bg-primary text-white p-4 h-100 d-flex justify-content-center align-items-center shadow-lg hover-scale">
                <h5 class="mb-0 fs-5">🍹 Geführte Drink-Beratung</h5>
              </div>
            </div>
            <div class="flip-card-back p-4 bg-dark text-white rounded border border-secondary">
              <transition name="slide-fade" mode="out-in">
                <div :key="step">
                  <div v-if="step === 1">
                    <h5>1. Wähle deine Stimmung:</h5>
                    <div class="d-flex flex-wrap gap-2 mt-3">
                      <button
                        v-for="v in vibes"
                        :key="v"
                        class="btn btn-sm"
                        :class="selectedVibe === v ? 'btn-success' : 'btn-outline-light'"
                        @click="selectedVibe = v; step = 2"
                      >{{ v }}</button>
                    </div>
                  </div>
                  <div v-else-if="step === 2">
                    <h5>2. Zusätzliche Präferenzen (optional):</h5>
                    <div class="d-flex flex-wrap gap-2 mt-3">
                      <button
                        v-for="pref in prefOptions"
                        :key="pref"
                        class="btn btn-sm"
                        :class="preferences.includes(pref) ? 'btn-success' : 'btn-outline-light'"
                        @click="togglePref(pref)"
                      >{{ pref }}</button>
                    </div>
                    <div class="text-end mt-4">
                      <button class="btn btn-secondary me-2" @click="step = 1">Zurück</button>
                      <button class="btn btn-primary" @click="step = 3">Weiter</button>
                    </div>
                  </div>
                  <div v-else-if="step === 3">
                    <h5 class="text-center mb-3">Bereit für deinen Drink?</h5>
                    <button class="btn btn-success w-100" @click="submitAdvisor">🍸 Drink vorschlagen</button>
                    <div class="text-end mt-3">
                      <button class="btn btn-secondary" @click="step = 2">Zurück</button>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
          </div>
        </div>
      </div>

      <!-- Zubereitung prüfen -->
      <div class="col-12 col-md-6">
        <div class="flip-card" :class="{ flipped: activeCard === 'checker' }">
          <div class="flip-card-inner">
            <div class="flip-card-front" @click="activeCard = 'checker'">
              <div class="card bg-light text-dark p-4 h-100 d-flex justify-content-center align-items-center shadow-lg hover-scale">
                <h5 class="mb-0 fs-5">🔍 Zubereitung prüfen</h5>
              </div>
            </div>
            <div class="flip-card-back p-4 bg-dark text-white rounded border border-secondary">
              <h5 class="mb-2">Dein Wunschgetränk:</h5>
              <input v-model="drinkSuggestion" type="text" class="form-control bg-dark text-white border-secondary" placeholder="Vodka Bull" />
              <div v-if="suggestionError" class="text-danger mt-2">{{ suggestionError }}</div>
              <button class="btn btn-success mt-3 w-100" @click="validateDrinkName">✅ Zubereitung prüfen</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <section class="bg-dark text-white py-5 mb-5">
    <div class="container text-center">
      <p class="lead mb-0">Lass dich überraschen, was wir für dich mixen!</p>
    </div>
  </section>
  <SwipeDeck />
  <Footer />
</template>

<style scoped>
.loading-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  z-index: 1050;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content p {
  font-size: 1.1rem;
  white-space: pre-wrap;
}

.flip-card {
  perspective: 1000px;
  height: 250px;
}
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}
.flip-card .flip-card-front,
.flip-card .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  top: 0;
  left: 0;
}
.flip-card .flip-card-front {
  z-index: 2;
  transform: rotateY(0deg);
}
.flip-card .flip-card-back {
  transform: rotateY(180deg);
  z-index: 1;
}
.flip-card.flipped .flip-card-inner {
  transform: rotateY(180deg);
}
.hover-scale {
  transition: transform 0.2s ease-in-out;
}
.hover-scale:hover {
  transform: scale(1.03);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
