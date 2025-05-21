<script setup>
import { onMounted, ref } from 'vue'
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
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement)

const bestellungen = ref([])
const umsatz = ref(0)
const zeitLabels = ref([])
const anzahlProStunde = ref([])
const umsatzProStunde = ref([])
const zeitraum = ref('heute')
let intervalRef

const ladeBestellungen = async () => {
  try {
    const res = await fetch('/api/bestellungen')
    const data = await res.json()
    if (Array.isArray(data)) bestellungen.value = data
  } catch (e) {
    console.error('❌ Fehler beim Laden der Bestellungen', e)
  }
}

const ladeStatistik = async () => {
  try {
    const res = await fetch('/api/bestellungen/alle')
    const data = await res.json()
    if (Array.isArray(data)) berechneStatistik(data)
  } catch (e) {
    console.error('❌ Fehler beim Laden der Statistikdaten', e)
  }
}

onMounted(() => {
  ladeBestellungen()
  ladeStatistik()
  intervalRef = setInterval(() => {
    ladeBestellungen()
    ladeStatistik()
  }, 30000)
})

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

const markiereAlsZubereitet = async (id) => {
  if (!confirm('Als zubereitet markieren?')) return
  try {
    const res = await fetch(`/api/bestellungen/${id}/zubereitet`, { method: 'PATCH' })
    const result = await res.json()
    if (result.success) {
      await Promise.all([ladeBestellungen(), ladeStatistik()])
    }
  } catch (e) {
    console.error('Fehler beim Aktualisieren der Bestellung:', e)
  }
}
</script>

<template>
  <div class="page-wrapper">
    <div class="dashboard-container text-white">
      <NavBar class="sidebar" />
      <div class="content d-flex flex-wrap p-4 gap-4">

        <div class="bestellungen col-12 col-lg-4">
          <h2 class="text-white">📦 Aktuelle Bestellungen</h2>
          <ul class="list-group">
            <li v-for="b in bestellungen" :key="b.id" class="list-group-item bg-dark text-white d-flex justify-content-between">
              <div>
                <strong>{{ b.drink_name }}</strong> – {{ b.preis }} € für {{ b.kundenname }}<br />
                <small>{{ new Date(b.bestellt_am).toLocaleString() }}</small>
              </div>
              <button class="btn btn-sm btn-outline-success" @click="markiereAlsZubereitet(b.id)">✔️ Zubereitet</button>
            </li>
          </ul>
        </div>

        <div class="statistiken col">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h2 class="text-white">📊 Statistik</h2>
            <div>
              <select class="form-select bg-dark text-white" v-model="zeitraum" @change="ladeStatistik">
                <option value="heute">Heute (24h)</option>
                <option value="woche">Diese Woche</option>
                <option value="monat">Dieser Monat</option>
              </select>
            </div>
          </div>
          <div class="mb-4">
            <h5>Anzahl Bestellungen</h5>
            <Bar :data="{
              labels: zeitLabels,
              datasets: [{
                label: 'Bestellungen',
                data: anzahlProStunde,
                backgroundColor: '#0d6efd'
              }]
            }" :options="{ indexAxis: 'x' }" />
          </div>
          <div class="mb-4">
            <h5>Umsatz (€)</h5>
            <Line :data="{
              labels: zeitLabels,
              datasets: [{
                label: 'Umsatz',
                data: umsatzProStunde,
                borderColor: '#198754',
                backgroundColor: 'rgba(25,135,84,0.2)'
              }]
            }" />
          </div>
          <div class="mt-3">
            <h4>💰 Gesamtumsatz: {{ umsatz }} €</h4>
          </div>
        </div>
      </div>
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