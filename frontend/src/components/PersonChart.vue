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
import dayjs from 'dayjs'
import 'dayjs/locale/de'

dayjs.locale('de')

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

const rawData = ref([])
const chartData = ref({ labels: [], datasets: [] })
const startDate = ref('')
const endDate = ref('')
const groupBy = ref('day')

const options = ['minute', 'hour', 'day']

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: { color: '#fff', font: { size: 14, weight: 'bold' } }
    },
    title: {
      display: true,
      text: 'Besucherzahlen',
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
      ticks: { color: '#ffffff', autoSkip: true, maxTicksLimit: 15 },
      grid: { color: 'rgba(255,255,255,0.1)' }
    },
    y: {
      beginAtZero: true,
      ticks: { color: '#ffffff' },
      grid: { color: 'rgba(255,255,255,0.1)' },
      suggestedMax: 12
    }
  },
  elements: {
    line: { tension: 0.3, borderWidth: 3 },
    point: { radius: 5, backgroundColor: '#fff', borderWidth: 2 }
  }
})

const updateChart = () => {
  let filtered = rawData.value.filter(entry => {
    const date = entry.timestamp.split('T')[0]
    return (!startDate.value || date >= startDate.value) &&
           (!endDate.value || date <= endDate.value)
  })

  let grouped = {}

  filtered.forEach(entry => {
    let key = ''
    const time = dayjs(entry.timestamp)
    if (groupBy.value === 'minute') key = time.format('DD.MM.YYYY HH:mm')
    else if (groupBy.value === 'hour') key = time.startOf('hour').format('DD.MM.YYYY HH:00')
    else if (groupBy.value === 'day') key = time.startOf('day').format('DD.MM.YYYY')

    if (!grouped[key]) grouped[key] = []
    grouped[key].push(entry.count)
  })

  const labels = Object.keys(grouped).sort()
  const data = labels.map(label => {
    const values = grouped[label]
    return values.reduce((a, b) => a + b, 0) / values.length
  })

  chartData.value = {
    labels,
    datasets: [{
      label: 'Personenzahl',
      data,
      borderColor: '#36A2EB',
      backgroundColor: '#36A2EB',
      pointBackgroundColor: '#fff',
      pointBorderColor: '#36A2EB',
      pointHoverRadius: 7,
      tension: 0.3,
      borderWidth: 3,
      fill: false
    }]
  }

  const max = Math.max(...data)
  chartOptions.value.scales.y.suggestedMax = Math.ceil(max * 1.2)
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('/api/person-history', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  const json = await res.json()
  rawData.value = json.person_count || []


  if (!rawData.value.length) return

  const allDates = rawData.value.map(e => e.timestamp.split('T')[0]).sort()
  startDate.value = allDates[0]
  endDate.value = allDates[allDates.length - 1]

  updateChart()
})


watch([startDate, endDate, groupBy], updateChart)
</script>

<template>
  <div class="custom-chart-container rounded shadow p-4 mb-4">
    <h4 class="text-white mb-4">👥 Besucherstatistik</h4>

    <div class="row mb-4 g-3">
      <div class="col-md-4">
        <label class="form-label text-white">Startdatum</label>
        <input type="date" class="form-control bg-dark text-white border-secondary" v-model="startDate" />
      </div>
      <div class="col-md-4">
        <label class="form-label text-white">Enddatum</label>
        <input type="date" class="form-control bg-dark text-white border-secondary" v-model="endDate" />
      </div>
      <div class="col-md-4">
        <label class="form-label text-white">Group By</label>
        <select class="form-select bg-dark text-white border-secondary" v-model="groupBy">
          <option value="minute">Minute</option>
          <option value="hour">Stunde</option>
          <option value="day">Tag</option>
        </select>
      </div>
    </div>

    <div class="chart-wrapper">
      <div v-if="chartData.datasets.length > 0">
        <Line
          :data="chartData"
          :options="chartOptions"
          style="height: 400px; width: 100%;"
        />
      </div>
      <div v-else class="text-center text-white">
        <p>⚠️ Keine Daten verfügbar.</p>
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