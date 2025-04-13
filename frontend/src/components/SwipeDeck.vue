<script setup>
import { ref, onMounted } from 'vue'

const drinks = ref([])
const liked = ref([])
const passed = ref([])
const currentIndex = ref(0)
const cardClass = ref('')
const loading = ref(true)
const error = ref('')

const likeDrink = () => {
  cardClass.value = 'swipe-right'
  setTimeout(() => {
    liked.value.push(drinks.value[currentIndex.value])
    next()
  }, 300)
}

const passDrink = () => {
  cardClass.value = 'swipe-left'
  setTimeout(() => {
    passed.value.push(drinks.value[currentIndex.value])
    next()
  }, 300)
}

const next = () => {
  currentIndex.value++
  cardClass.value = ''
}

const reset = async () => {
  liked.value = []
  passed.value = []
  currentIndex.value = 0
  cardClass.value = ''
  await fetchDrinks()
}

const fetchDrinks = async () => {
  loading.value = true
  try {
    const res = await fetch('/api/examples')
    const data = await res.json()

    if (data.success && Array.isArray(data.drinks)) {
      drinks.value = data.drinks
    } else {
      error.value = '⚠️ Drinks konnten nicht geladen werden.'
    }
  } catch (err) {
    error.value = '🚫 Fehler beim Laden der Drinks.'
    console.error('❌ API Fehler:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchDrinks)
</script>

<template>
  <div class="swipe-deck-wrapper text-center">
    <!-- Ladeanimation -->
    <div v-if="loading" class="my-5 loading-container">
      <div class="cocktail-loader mb-3"></div>
      <p class="fs-5 fw-semibold text-dark">Lade Getränke...</p>
    </div>

    <!-- Fehler -->
    <div v-else-if="error" class="text-danger">
      <p>{{ error }}</p>
    </div>

    <!-- Drink-Karte -->
    <div
      v-else-if="currentIndex < drinks.length"
      :key="currentIndex"
      class="card shadow p-4 mb-4"
      :class="cardClass"
    >
      <h5 class="mb-1">{{ drinks[currentIndex].name }}</h5>
      <small class="text-muted">{{ drinks[currentIndex].preis }} – {{ drinks[currentIndex].alk }}</small>

      <div v-if="drinks[currentIndex].zutaten?.length" class="mt-3 text-start">
        <strong class="text-light">Zutaten:</strong>
        <ul class="list-unstyled small text-white-50 mt-2 ps-3">
          <li v-for="z in drinks[currentIndex].zutaten" :key="z">• {{ z }}</li>
        </ul>
      </div>

      <div class="d-flex justify-content-around mt-4">
        <button class="btn btn-outline-danger w-25" @click="passDrink">👎</button>
        <button class="btn btn-outline-success w-25" @click="likeDrink">👍</button>
      </div>
    </div>

    <!-- Ergebnisse -->
    <div v-else class="result text-center p-4">
      <h5>🎯 Deine Favoriten:</h5>
      <ul class="list-unstyled mt-3">
        <li v-for="drink in liked" :key="drink.name">🍹 {{ drink.name }} – {{ drink.preis }}</li>
      </ul>
      <button class="btn btn-outline-primary mt-3" @click="reset">🔁 Nochmal laden!</button>
    </div>
  </div>
</template>

<style scoped>
.swipe-deck-wrapper {
  max-width: 320px;
  margin: 0 auto;
}

.card {
  background-color: #1e293b;
  border: 1px solid #334155;
  color: white;
  border-radius: 1rem;
  transition: transform 0.4s ease-out, opacity 0.4s ease-out;
  min-height: 280px;
}

/* Swipe Animation */
.swipe-right {
  transform: translateX(25vw) rotate(20deg);
  opacity: 0;
}

.swipe-left {
  transform: translateX(-25vw) rotate(-20deg);
  opacity: 0;
}

/* Ladeanimation */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.cocktail-loader {
  width: 60px;
  height: 60px;
  background: radial-gradient(circle at 50% 50%, #ff6b6b 30%, transparent 30%),
              linear-gradient(to top, #ff6b6b 0%, #c73866 100%);
  border-radius: 30% 30% 10% 10%;
  animation: bounce 1s infinite ease-in-out;
  box-shadow: 0 0 15px rgba(199, 56, 102, 0.3);
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-12px);
  }
}
</style>
