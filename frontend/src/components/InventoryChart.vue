<script setup>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { ref, onMounted, watch } from 'vue'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

const rawData = ref([])
const chartData = ref({ labels: [], datasets: [] })
const startDate = ref('')
const endDate = ref('')

const colors = [
  '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
  '#9966FF', '#FF9F40', '#00C49F', '#F95F62'
]

function getColor(index) {
  return colors[index % colors.length]
}

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  layout: {
    padding: {
      top: 30,
      bottom: 20,
      left: 15,
      right: 15
    }
  },
  plugins: {
    legend: {
      labels: {
        color: '#fff',
        font: { size: 14, weight: 'bold' }
      }
    },
    title: {
      display: true,
      text: 'Bestandsverlauf',
      color: '#fff',
      font: { size: 18, weight: 'bold' }
    },
    tooltip: {
      backgroundColor: '#222',
      titleColor: '#fff',
      bodyColor: '#ddd',
      borderColor: '#444',
      borderWidth: 1
    }
  },
  scales: {
    x: {
      ticks: { color: '#ffffff' },
      grid: { color: 'rgba(255,255,255,0.1)' }
    },
    y: {
      beginAtZero: true,
      ticks: { color: '#ffffff' },
      grid: { color: 'rgba(255,255,255,0.1)' },
      suggestedMax: 20
    }
  },
  elements: {
    line: { tension: 0.3, borderWidth: 3 },
    point: { radius: 5, backgroundColor: '#fff', borderWidth: 2 }
  }
})

const updateChart = () => {
  const grouped = {}

  const filtered = rawData.value.filter(entry => {
    const dateOnly = entry.datum?.split('T')[0]
    return (!startDate.value || dateOnly >= startDate.value) &&
           (!endDate.value || dateOnly <= endDate.value)
  })

  filtered.forEach(entry => {
    const date = entry.datum.split('T')[0]
    const key = entry.produktname
    if (!grouped[key]) grouped[key] = {}
    grouped[key][date] = entry.anzahl
  })

  const labels = [...new Set(filtered.map(e => e.datum.split('T')[0]))].sort()

  const datasets = Object.entries(grouped).map(([name, daten], index) => ({
    label: name,
    data: labels.map(d => daten[d] ?? null),
    borderColor: getColor(index),
    pointBackgroundColor: '#fff',
    pointBorderColor: getColor(index),
    pointHoverRadius: 7,
    tension: 0.3,
    borderWidth: 3,
    fill: false
  }))

  chartData.value = { labels, datasets }

  const alleWerte = datasets.flatMap(ds => ds.data).filter(val => typeof val === 'number')
  const maxWert = alleWerte.length ? Math.max(...alleWerte) : 10
  chartOptions.value.scales.y.suggestedMax = Math.ceil(maxWert * 1.2)
}

onMounted(async () => {
  const token = localStorage.getItem('token')

  const res = await fetch('/api/bestand', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
    const json = await res.json()
  rawData.value = json.inventar

  const allDates = rawData.value.map(e => e.datum?.split('T')[0]).sort()
  startDate.value = allDates[0]
  endDate.value = allDates[allDates.length - 1]

  updateChart()
})

watch([startDate, endDate], () => {
  updateChart()
})
</script>

<template>
  <div class="custom-chart-container rounded shadow p-4 mb-4">
    <h4 class="text-white mb-4">📊 Übersicht der Bestände</h4>

    <!-- Zeitraum-Auswahl -->
    <div class="row mb-4 g-3">
      <div class="col-md-6">
        <label class="form-label text-white">Startdatum</label>
        <input type="date" class="form-control bg-dark text-white border-secondary" v-model="startDate" />
      </div>
      <div class="col-md-6">
        <label class="form-label text-white">Enddatum</label>
        <input type="date" class="form-control bg-dark text-white border-secondary" v-model="endDate" />
      </div>
    </div>

    <!-- Chart -->
    <div class="chart-wrapper">
      <div v-if="chartData.datasets.length > 0">
        <Line
          :data="chartData"
          :options="chartOptions"
          style="height: 400px; width: 100%;"
        />
      </div>
      <div v-else class="text-center text-white">
        <p>⚠️ Keine Daten zum Anzeigen verfügbar.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-chart-container {
  background-color: #1e293b;
  border: 1px solid #2d3748;
  margin: 1rem;
}

.chart-wrapper {
  position: relative;
  width: 100%;
}
</style>
