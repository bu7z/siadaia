<script setup>
import { useRouter } from 'vue-router'
import { onMounted, ref, watch } from 'vue'
import { Bar, Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
} from 'chart.js'
import HeroInventory from '@/components/HeroInventory.vue'
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'

// ChartJS-Setup
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement)

const router = useRouter()
const bestellungen = ref([])
const vergangeneBestellungen = ref([])
const umsatz = ref(0)
const zeitLabels = ref([])
const anzahlProStunde = ref([])
const umsatzProStunde = ref([])
const zeitraum = ref('heute')
const showHistorie = ref(false)
const showModal = ref(false)
const selectedBestellungId = ref(null)
const token = localStorage.getItem('token')
const user = ref(null)
const loading = ref(true)



let intervalRef = null

// Hilfsfunktion für fetch mit Token
const authFetch = (url, options = {}) => {
  return fetch(url, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...(options.headers || {})
    }
  })
}

// Bestellungen laden
const ladeBestellungen = async () => {
  try {
    const [offenRes, vergangenRes] = await Promise.all([
      authFetch('/api/bestellungen'),
      authFetch('/api/bestellungen/vergangene')
    ])

    const offenData = await offenRes.json()
    const vergangenData = await vergangenRes.json()

    if (Array.isArray(offenData)) {
      bestellungen.value = offenData.sort((a, b) => new Date(a.bestellt_am) - new Date(b.bestellt_am))
    }

    if (Array.isArray(vergangenData)) {
      vergangeneBestellungen.value = vergangenData.sort((a, b) => new Date(b.bestellt_am) - new Date(a.bestellt_am))
    }
  } catch (e) {
    console.error('❌ Fehler beim Laden der Bestellungen:', e)
  }
}

// Statistikdaten laden
const ladeStatistik = async () => {
  try {
    const res = await authFetch('/api/bestellungen/alle')
    const data = await res.json()
    if (Array.isArray(data)) berechneStatistik(data)
  } catch (e) {
    console.error('❌ Fehler beim Laden der Statistikdaten:', e)
  }
}

onMounted(async () => {
  const token = localStorage.getItem('token')

  if (!token) {
    router.push('/')
    return
  }

  try {
    const res = await fetch('/api/verify-token', {
      method: 'GET',
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
    console.error('Fehler beim Token-Check:', err)
    localStorage.removeItem('token')
    router.push('/')
  }
  ladeBestellungen()
  ladeStatistik()
  intervalRef = setInterval(() => {
    ladeBestellungen()
    ladeStatistik()
  }, 30000)
})

watch(zeitraum, ladeStatistik)

const berechneStatistik = (liste) => {
  const map = new Map()
  let total = 0
  const now = new Date()

  const getKey = (d) => {
    if (zeitraum.value === 'heute') {
      const past24h = new Date(now.getTime() - 24 * 60 * 60 * 1000)
      if (d < past24h) return null
      return `${d.getHours().toString().padStart(2, '0')}:${Math.floor(d.getMinutes() / 10) * 10}`
    } else if (zeitraum.value === 'woche') {
      return `${d.getDate()}.${d.getMonth() + 1} ${d.getHours()}h`
    } else if (zeitraum.value === 'monat') {
      return `${d.getDate()}.${d.getMonth() + 1}`
    }
    return null
  }

  liste.forEach(b => {
    const d = new Date(b.bestellt_am)
    const key = getKey(d)
    const preisNum = Number(b.preis) || 0
    if (!key) return

    total += preisNum
    if (!map.has(key)) map.set(key, { count: 0, sum: 0 })
    map.get(key).count++
    map.get(key).sum += preisNum
  })

  const sortedKeys = Array.from(map.keys()).sort()
  zeitLabels.value = sortedKeys
  anzahlProStunde.value = sortedKeys.map(k => map.get(k).count)
  umsatzProStunde.value = sortedKeys.map(k => map.get(k).sum.toFixed(2))
  umsatz.value = total.toFixed(2)
}

// Modal öffnen
const openModal = (id) => {
  selectedBestellungId.value = id
  showModal.value = true
}

// PATCH-Bestellung als zubereitet
const bestätigeZubereitet = async () => {
  if (!selectedBestellungId.value) return
  try {
    const res = await authFetch(`/api/bestellungen/${selectedBestellungId.value}/zubereitet`, {
      method: 'PATCH'
    })
    const result = await res.json()
    if (result.success) {
      showModal.value = false
      selectedBestellungId.value = null
      await Promise.all([ladeBestellungen(), ladeStatistik()])
    }
  } catch (e) {
    console.error('❌ Fehler beim Markieren als zubereitet:', e)
  }
}
</script>

<template>
  <HeroInventory />
  <div class="page-wrapper">
    <div class="dashboard-container text-white">
      <NavBar class="sidebar" />
      <div class="content d-flex flex-wrap p-4 gap-4">
        <div class="bestellungen col-12 col-lg-4">
          <h2 class="text-white">Aktuelle Bestellungen</h2>
          <ul class="list-group mb-3">
            <li v-for="b in bestellungen" :key="b.id" class="list-group-item bg-dark text-white">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <strong>{{ b.drink_name }}</strong> – {{ b.preis }} €<br />
                  <small>für {{ b.kundenname }} • {{ new Date(b.bestellt_am).toLocaleString('de-DE', { dateStyle: 'short', timeStyle: 'short' }) }}</small>
                  <ul class="mt-2 ms-3 small" v-if="Array.isArray(b.zutaten)">
                    <li v-for="z in b.zutaten" :key="z">{{ z }}</li>
                  </ul>
                </div>
                <button class="btn btn-sm btn-outline-success mt-1" @click="openModal(b.id)">✔️</button>
              </div>
            </li>
          </ul>

          <div>
            <button class="btn btn-outline-light w-100 mb-2" @click="showHistorie = !showHistorie">
              Vergangene Bestellungen
            </button>
            <div v-if="showHistorie">
              <ul class="list-group">
                <li v-for="b in vergangeneBestellungen" :key="b.id" class="list-group-item text-white bg-light bg-opacity-10" style="opacity: 0.65;">
                  <div>
                    <strong>{{ b.drink_name }}</strong> – {{ b.preis }} € für {{ b.kundenname }}<br />
                    <small>{{ new Date(b.bestellt_am).toLocaleString('de-DE', { dateStyle: 'short', timeStyle: 'short' }) }}</small>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="statistiken col">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h2 class="text-white">Statistik</h2>
            <select class="form-select bg-dark text-white w-auto" v-model="zeitraum">
              <option value="heute">Heute (24h)</option>
              <option value="woche">Diese Woche</option>
              <option value="monat">Dieser Monat</option>
            </select>
          </div>

          <div class="mb-3" style="height: 220px;">
            <Bar
              :data="{
                labels: zeitLabels,
                datasets: [{
                  label: 'Bestellungen',
                  data: anzahlProStunde,
                  backgroundColor: '#0d6efd'
                }]
              }"
              :options="{ responsive: true, maintainAspectRatio: false }"
            />
          </div>

          <div style="height: 220px;">
            <Line
              :data="{
                labels: zeitLabels,
                datasets: [{
                  label: 'Umsatz (€)',
                  data: umsatzProStunde,
                  borderColor: '#198754',
                  backgroundColor: 'rgba(25,135,84,0.2)',
                  tension: 0.3
                }]
              }"
              :options="{ responsive: true, maintainAspectRatio: false }"
            />
          </div>

          <div class="mt-4">
            <h4>Gesamtumsatz: {{ umsatz }} €</h4>
          </div>
        </div>
      </div>
    </div>

    <Footer />

    <!-- Bestätigungs-Modal -->
    <div class="modal fade show" tabindex="-1" style="display: block;" v-if="showModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-dark text-white border border-secondary rounded-4 shadow-lg">
          <div class="modal-header border-0">
            <h5 class="modal-title">Bestellung als zubereitet markieren?</h5>
            <button type="button" class="btn-close btn-close-white" @click="showModal = false"></button>
          </div>
          <div class="modal-body">
            <p>Du bist dabei, diese Bestellung als <strong>zubereitet</strong> zu markieren. Möchtest du fortfahren?</p>
          </div>
          <div class="modal-footer border-0">
            <button class="btn btn-secondary" @click="showModal = false">Abbrechen</button>
            <button class="btn btn-success" @click="bestätigeZubereitet">Bestätigen</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 82vh;
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
.content {
  flex-grow: 1;
  display: flex;
  flex-wrap: wrap;
}
.bestellungen {
  min-width: 300px;
  max-width: 450px;
}
.statistiken {
  flex-grow: 1;
  min-width: 300px;
}
</style>
