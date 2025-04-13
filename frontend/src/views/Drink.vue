<script setup>
import Footer from '@/components/Footer.vue'
import HeroDrink from '@/components/HeroDrink.vue'
import { ref } from 'vue'

const step = ref(1)
const showAdvisor = ref(false)
const showChecker = ref(false)

const selectedVibe = ref('')
const preferences = ref([])
const drinkSuggestion = ref('')
const suggestionError = ref('')

const vibes = [
  'Edle Stimmung', 'Entspannt', 'Brauche Energie',
  'Wenig Alkohol', 'Überrasch mich', 'Alkoholfrei'
]

const prefOptions = ['Süß', 'Bitter', 'Fruchtig', 'Stark', 'Würzig', 'Saisonal']

const togglePref = (pref) => {
  if (preferences.value.includes(pref)) {
    preferences.value = preferences.value.filter(p => p !== pref)
  } else {
    preferences.value.push(pref)
  }
}

const resetForm = () => {
  step.value = 1
  selectedVibe.value = ''
  preferences.value = []
}

const submitAdvisor = () => {
  alert(`🎉 Vorschlag wird basierend auf:
- Stimmung: ${selectedVibe.value}
- Präferenzen: ${preferences.value.join(', ')}`)
  resetForm()
  showAdvisor.value = false
}

const validateDrinkName = () => {
  const isValid = /^[a-zA-ZäöüÄÖÜß\s]+$/.test(drinkSuggestion.value.trim()) &&
                  drinkSuggestion.value.trim().split(' ').length <= 3
  if (!isValid) {
    suggestionError.value = 'Bitte gib nur einen Getränkenamen ein (keine Sätze).'
    return
  }
  alert(`🍸 Wir prüfen, ob du "${drinkSuggestion.value}" zubereiten kannst.`)
  drinkSuggestion.value = ''
  suggestionError.value = ''
  showChecker.value = false
}
</script>

<template>
  <HeroDrink/>

  <div class="container py-4 text-white">
    <h2 class="text-center">Drink Advisory</h2>
    <p class="text-center text-white-50 mb-4">Dein persönlicher Getränkeberater</p>

    <div class="d-flex flex-column gap-3">
      <button class="btn btn-primary" @click="showAdvisor = true">🍹 Geführte Drink-Beratung</button>
      <button class="btn btn-outline-light" @click="showChecker = true">🔍 Zubereitung prüfen</button>
    </div>

    <!-- A: Geführte Drink-Beratung -->
    <div v-if="showAdvisor" class="mt-4 p-3 rounded bg-dark border border-secondary">
      <div v-if="step === 1">
        <h5 class="mb-3">1. Wähle deine Stimmung:</h5>
        <div class="d-flex flex-wrap gap-2">
          <button
            v-for="v in vibes"
            :key="v"
            @click="selectedVibe = v; step = 2"
            :class="['btn', selectedVibe === v ? 'btn-success' : 'btn-outline-light']"
          >
            {{ v }}
          </button>
        </div>
      </div>

      <div v-else-if="step === 2">
        <h5 class="mb-3">2. Zusätzliche Präferenzen (optional):</h5>
        <div class="d-flex flex-wrap gap-2 mb-3">
          <button
            v-for="pref in prefOptions"
            :key="pref"
            @click="togglePref(pref)"
            :class="['btn', preferences.includes(pref) ? 'btn-success' : 'btn-outline-light']"
          >
            {{ pref }}
          </button>
        </div>
        <div class="text-end">
          <button class="btn btn-secondary me-2" @click="step = 1">Zurück</button>
          <button class="btn btn-primary" @click="step = 3">Weiter</button>
        </div>
      </div>

      <div v-else-if="step === 3">
        <h5 class="mb-3 text-center">Bereit für deinen Drink?</h5>
        <button class="btn btn-success w-100" @click="submitAdvisor">🍸 Drink vorschlagen</button>
        <div class="text-end mt-3">
          <button class="btn btn-secondary" @click="step = 2">Zurück</button>
        </div>
      </div>
    </div>

    <!-- B: Zubereitung prüfen -->
    <div v-if="showChecker" class="mt-4 p-3 rounded bg-dark border border-secondary">
      <h5>Gib dein Wunschgetränk ein:</h5>
      <input
        v-model="drinkSuggestion"
        type="text"
        class="form-control bg-dark text-white border-secondary mt-2"
        placeholder="z. B. Gin Tonic"
      />
      <div v-if="suggestionError" class="text-danger mt-2">{{ suggestionError }}</div>
      <button class="btn btn-success mt-3 w-100" @click="validateDrinkName">
        ✅ Zubereitung prüfen
      </button>
    </div>
  </div>

  <Footer />
</template>

<style scoped>
button {
  white-space: nowrap;
}
</style>
