<script setup>
import { ref, onMounted } from 'vue'
import OrderModal from '@/components/OrderModal.vue'

const drinks = ref([])
const liked = ref([])
const passed = ref([])
const currentIndex = ref(0)
const cardClass = ref('')
const loading = ref(true)
const error = ref('')
const showOrderModal = ref(false)
const selectedDrink = ref(null)
const showSuccessToast = ref(false)

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
  error.value = ''

  try {
    const res = await fetch('/api/examples')

    // ❗ Erst prüfen, ob HTTP-Status erfolgreich ist
    if (!res.ok) {
      throw new Error(`Serverantwort war nicht ok: ${res.status}`)
    }

    // ✅ Versuche JSON zu parsen
    const data = await res.json()

    // ✅ Log für Debug-Zwecke
    console.log("✅ API-Daten erhalten:", data)

    if (data.success && Array.isArray(data.drinks)) {
      drinks.value = data.drinks
    } else {
      throw new Error('Antwortstruktur ungültig oder keine Drinks vorhanden.')
    }

  } catch (err) {
    error.value = '🚫 Fehler beim Laden der Drinks.'
    console.error('❌ API Fehler:', err.message || err)
  } finally {
    loading.value = false
  }
}


const bestelleDrink = (drink) => {
  selectedDrink.value = drink
  showOrderModal.value = true
}

const onBestellungAbgeschlossen = () => {
  showOrderModal.value = false
  selectedDrink.value = null
  showSuccessToast.value = true
  setTimeout(() => {
    showSuccessToast.value = false
  }, 3500)
}

onMounted(fetchDrinks)
</script>

<template>
  <div class="swipe-deck-wrapper text-center">
    <OrderModal
      v-if="selectedDrink"
      :show="showOrderModal"
      :drink="selectedDrink"
      @close="showOrderModal = false"
      @bestellt="onBestellungAbgeschlossen"
    />

    <div v-if="loading" class="my-5 loading-container">
      <div class="shaker-svg-container">
        <svg
          viewBox="0 0 100 200"
          class="shaker-svg"
          xmlns="http://www.w3.org/2000/svg"
        >
          <!-- Shaker-Body -->
          <rect x="20" y="30" width="60" height="140" rx="20" ry="20" fill="#bbb" />
          <!-- Cap -->
          <rect x="35" y="10" width="30" height="20" rx="5" ry="5" fill="#ccc" />
          <!-- Flüssigkeit mit animierter Welle -->
          <clipPath id="liquidClip">
            <path
              class="wave-path"
              d=""
              fill="red"
            />
          </clipPath>
          <g clip-path="url(#liquidClip)">
            <rect x="20" y="90" width="60" height="80" fill="#ff6b6b" />
          </g>
        </svg>
      </div>
      <p class="fs-5 fw-semibold text-dark mt-3">Mixing Drinks...</p>
    </div>

    <div v-else-if="error" class="text-danger">
      <p>{{ error }}</p>
    </div>

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

    <div v-else class="result text-center p-4">
      <h5>🎯 Deine Favoriten:</h5>
      <ul class="list-unstyled mt-3">
        <li v-for="drink in liked" :key="drink.name">
          🍹 {{ drink.name }} – {{ drink.preis }}
          <button class="btn btn-sm btn-outline-primary ms-2" @click="bestelleDrink(drink)">Jetzt bestellen</button>
        </li>
      </ul>
      <button class="btn btn-outline-primary mt-3" @click="reset">🔁 Nochmal laden!</button>
    </div>

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
.swipe-right {
  transform: translateX(25vw) rotate(20deg);
  opacity: 0;
}
.swipe-left {
  transform: translateX(-25vw) rotate(-20deg);
  opacity: 0;
}
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* SVG Shaker */
.shaker-svg-container {
  width: 80px;
  height: 160px;
  animation: shaker-move 1.5s infinite ease-in-out;
}
.shaker-svg {
  width: 100%;
  height: 100%;
}

/* Animierte Wellenpfad */
@keyframes wave {
  0% {
    d: path("M20,110 Q40,105 60,110 T100,110 L100,200 L0,200 Z");
  }
  50% {
    d: path("M20,110 Q40,115 60,110 T100,110 L100,200 L0,200 Z");
  }
  100% {
    d: path("M20,110 Q40,105 60,110 T100,110 L100,200 L0,200 Z");
  }
}

/* Bewegung des Shakers */
@keyframes shaker-move {
  0%, 100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(3deg);
  }
  50% {
    transform: rotate(-3deg);
  }
  75% {
    transform: rotate(2deg);
  }
}

/* Fallback für Safari: wellenlose Flüssigkeit */
.wave-path {
  animation: wave 2s infinite ease-in-out;
  d: path("M20,110 Q40,105 60,110 T100,110 L100,200 L0,200 Z");
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
