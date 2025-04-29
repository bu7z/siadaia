<script setup lang="ts">
import { ref, onMounted } from 'vue'
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

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
)

const labels = ref<string[]>([])
const data = ref<number[]>([])

const chartData = ref({
  labels: [] as string[],
  datasets: [
    {
      label: 'Anzahl Personen',
      data: [] as number[],
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderWidth: 3,
      pointRadius: 4,
      tension: 0.2,
      fill: false
    }
  ]
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: false,
  scales: {
    y: {
      beginAtZero: true,
      suggestedMax: 10,
      ticks: {
        stepSize: 1,
        color: '#000'
      },
      grid: {
        color: '#ccc'
      }
    },
    x: {
      ticks: {
        color: '#000'
      },
      grid: {
        color: '#eee'
      }
    }
  },
  plugins: {
    legend: {
      labels: {
        color: '#000'
      }
    }
  }
}

const fetchPersonCount = async () => {
  try {
    const res = await fetch('/api/person-count')
    const json = await res.json()
    const timestamp = new Date().toLocaleTimeString()

    labels.value = [...labels.value, timestamp]
    data.value = [...data.value, json.count]

    if (labels.value.length > 20) {
      labels.value = labels.value.slice(-20)
      data.value = data.value.slice(-20)
    }

    // 🟢 WICHTIG: neue Referenz erzeugen
    chartData.value = {
      labels: [...labels.value],
      datasets: [
        {
          ...chartData.value.datasets[0],
          data: [...data.value]
        }
      ]
    }

    console.log('✅ Neue Personenzahl:', json.count)
  } catch (err) {
    console.error('Fehler beim Abrufen:', err)
  }
}

onMounted(() => {
  fetchPersonCount()
  setInterval(fetchPersonCount, 2000)
})
</script>

<template>
  <div style="height: 350px;">
    <Line :data="chartData" :options="chartOptions" :key="chartData.labels.length" />
  </div>
</template>
