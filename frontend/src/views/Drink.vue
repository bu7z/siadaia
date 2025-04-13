<script setup>
import Footer from '@/components/Footer.vue'
import HeroDrink from '@/components/HeroDrink.vue'
import SwipeDeck from '@/components/SwipeDeck.vue'
import { ref } from 'vue'

const activeCard = ref('')
const step = ref(1)
const selectedVibe = ref('')
const preferences = ref([])
const drinkSuggestion = ref('')
const suggestionError = ref('')

const loadingOverlay = ref(false)
const responseText = ref('')
const showResponseModal = ref(false)

const vibes = [
  'Edle Stimmung', 'Entspannt', 'Brauche Energie',
  'Wenig Alkohol', 'Überrasch mich', 'Alkoholfrei'
]

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

const submitAdvisor = async () => {
  loadingOverlay.value = true
  try {
    const res = await fetch('/api/beratung', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        vibe: selectedVibe.value,
        preferences: preferences.value
      })
    })

    const data = await res.json()
    responseText.value = data.success ? data.drink : '❌ Leider kein passender Drink gefunden.'
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
    responseText.value = data.success ? data.drink : '❌ Zubereitung nicht möglich.'
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
  <!-- 🔄 Lade-Overlay -->
  <div v-if="loadingOverlay" class="loading-backdrop">
    <div class="spinner-border text-light" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <!-- 🧃 Antwort-Modal -->
  <div
    class="modal fade show"
    v-if="showResponseModal"
    tabindex="-1"
    style="display: block; background: rgba(0,0,0,0.6);"
    @click.self="showResponseModal = false"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark text-white border-0 rounded-4 shadow-lg p-4">
        <div class="modal-header border-0">
          <h5 class="modal-title">🍹 Drink Empfehlung</h5>
          <button type="button" class="btn-close btn-close-white" @click="showResponseModal = false"></button>
        </div>
        <div class="modal-body">
          <p class="mb-0">{{ responseText }}</p>
        </div>
      </div>
    </div>
  </div>

  <HeroDrink />

  <div class="container py-5">
    <h2 class="text-center fw-bold mb-5">Your personal drink advisor</h2>

    <div class="row justify-content-center g-4">
      <!-- Geführte Drink-Beratung -->
      <div class="col-12 col-md-6">
        <div class="flip-card" :class="{ flipped: activeCard === 'advisor' }">
          <div class="flip-card-inner">
            <!-- Front -->
            <div class="flip-card-front" @click="activeCard = 'advisor'">
              <div class="card bg-primary text-white p-4 h-100 d-flex justify-content-center align-items-center shadow-lg hover-scale">
                <h5 class="mb-0 fs-5">🍹 Geführte Drink-Beratung</h5>
              </div>
            </div>

            <!-- Back -->
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
                      >
                        {{ v }}
                      </button>
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
                      >
                        {{ pref }}
                      </button>
                    </div>
                    <div class="text-end mt-4">
                      <button class="btn btn-secondary me-2" @click="step = 1">Zurück</button>
                      <button class="btn btn-primary" @click="step = 3">Weiter</button>
                    </div>
                  </div>

                  <div v-else-if="step === 3">
                    <h5 class="text-center mb-3">Bereit für deinen Drink?</h5>
                    <button class="btn btn-success w-100" @click="submitAdvisor">
                      🍸 Drink vorschlagen
                    </button>
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
            <!-- Front -->
            <div class="flip-card-front" @click="activeCard = 'checker'">
              <div class="card bg-light text-dark p-4 h-100 d-flex justify-content-center align-items-center shadow-lg hover-scale">
                <h5 class="mb-0 fs-5">🔍 Zubereitung prüfen</h5>
              </div>
            </div>

            <!-- Back -->
            <div class="flip-card-back p-4 bg-dark text-white rounded border border-secondary">
              <h5 class="mb-2">Dein Wunschgetränk:</h5>
              <input
                v-model="drinkSuggestion"
                type="text"
                class="form-control bg-dark text-white border-secondary"
                placeholder="Vodka Bull"
              />
              <div v-if="suggestionError" class="text-danger mt-2">{{ suggestionError }}</div>
              <button class="btn btn-success mt-3 w-100" @click="validateDrinkName">
                ✅ Zubereitung prüfen
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Dekorativer Abschnitt -->
  <section class="bg-dark text-white py-5 mb-5">
    <div class="container text-center">
      <p class="lead mb-0">Lass dich überraschen, was wir für dich mixen!</p>
    </div>
  </section>

  <SwipeDeck />
  <Footer />
</template>

<style scoped>
/* Flip Card Layout */
.flip-card {
  perspective: 1000px;
  height: 250px;
}
.flip-card-inner {
  width: 100%;
  height: 100%;
  position: relative;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}
.flip-card.flipped .flip-card-inner {
  transform: rotateY(180deg);
}
.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
}
.flip-card-back {
  transform: rotateY(180deg);
  overflow-y: auto;
  padding-bottom: 1rem;
}

/* Slide Animation */
.slide-fade-enter-active {
  transition: all 0.4s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateX(-10px);
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

/* Hover */
.hover-scale {
  transition: transform 0.2s ease-in-out;
}
.hover-scale:hover {
  transform: scale(1.03);
}

/* Overlay */
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

/* Modal body */
.modal-content p {
  font-size: 1.1rem;
  white-space: pre-wrap;
}
</style>
