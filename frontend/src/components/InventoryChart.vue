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
import { ref, onMounted, watch, computed } from 'vue'
import Multiselect from '@vueform/multiselect'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

const rawData = ref([])
const chartData = ref({ labels: [], datasets: [] })
const startDate = ref('')
const endDate = ref('')
const selectedProducts = ref(['Hirsch Helle'])
const allProducts = ref([])

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
  plugins: {
    legend: {
      labels: {
        color: '#fff',
        font: { size: 14, weight: 'bold' },
        boxWidth: 20,
        padding: 20
      },
      onClick: (e, legendItem, legend) => {
        e.stopPropagation()
        const index = selectedProducts.value.indexOf(legendItem.text)
        if (index === -1) {
          selectedProducts.value.push(legendItem.text)
        } else {
          selectedProducts.value.splice(index, 1)
        }
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

// Installiere zuerst das Multiselect-Paket: npm install @vueform/multiselect

const updateChart = () => {
  const grouped = {}
  const filtered = rawData.value.filter(entry => {
    const dateOnly = entry.datum?.split('T')[0]
    return (!startDate.value || dateOnly >= startDate.value) &&
           (!endDate.value || dateOnly <= endDate.value)
  })

  filtered.forEach(entry => {
    if (!selectedProducts.value.includes(entry.produktname) || typeof entry.anzahl !== 'number') return
    
    const date = entry.datum.split('T')[0]
    const key = entry.produktname

    if (!grouped[key]) grouped[key] = {}
    grouped[key][date] = entry.anzahl
  })

  const labels = [...new Set(filtered.map(e => e.datum.split('T')[0]))].sort()

  const datasets = selectedProducts.value
    .filter(product => grouped[product])
    .map((product, index) => ({
      label: product,
      data: labels.map(d => grouped[product][d] ?? null),
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

  allProducts.value = [...new Set(rawData.value.map(item => item.produktname))].sort()
  
  const allDates = rawData.value.map(e => e.datum?.split('T')[0]).sort()
  startDate.value = allDates[0]
  endDate.value = allDates[allDates.length - 1]

  updateChart()
})

watch([startDate, endDate, selectedProducts], updateChart, { deep: true })
</script>

<template>
  <div class="custom-chart-container rounded shadow p-4 mb-4">
    <h4 class="text-white mb-4">📊 Bestanderstatistik</h4>

    <!-- Zeitraum-Auswahl in einer Zeile -->
    <div class="row mb-4 g-3">
      <div class="col-md-3">
        <label class="form-label text-white">Startdatum</label>
        <input type="date" class="form-control bg-dark text-white border-secondary" v-model="startDate" />
      </div>
      <div class="col-md-3">
        <label class="form-label text-white">Enddatum</label>
        <input type="date" class="form-control bg-dark text-white border-secondary" v-model="endDate" />
      </div>
    </div>

    <!-- Produktauswahl in voller Breite -->
    <div class="row mb-4">
      <div class="col-12">
        <label class="form-label text-white">Produkte</label>
        <Multiselect
          v-model="selectedProducts"
          :options="allProducts"
          mode="tags"
          :close-on-select="false"
          placeholder="Produkte auswählen..."
          :searchable="true"
          :create-option="false"
          class="multiselect-custom"
        />
      </div>
    </div>

    <!-- Chart mit mehr Höhe -->
    <div class="chart-wrapper">
      <div v-if="chartData.datasets.length > 0">
        <Line
          :data="chartData"
          :options="chartOptions"
          style="height: 500px; width: 100%;"
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
  margin-top: 1rem;
}

:deep(.multiselect) {
  background-color: #1a1a1a;
  border-color: #444;
  color: white;
}

:deep(.multiselect-input),
:deep(.multiselect-search) {
  background-color: #1a1a1a !important;
  color: white !important;
  border: none !important;
}

:deep(.multiselect-dropdown),
:deep(.multiselect-option),
:deep(.multiselect-option:hover) {
  background-color: #1a1a1a;
  color: white;
}

:deep(.multiselect-option:hover) {
  background-color: #333;
}

:deep(.multiselect-input[type="search"]) {
  background-color: #1a1a1a !important;
  color: white !important;
  border: none !important;
}

</style>

<style src="@vueform/multiselect/themes/default.css"></style>