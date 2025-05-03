<script setup>
import { ref, watch } from 'vue'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  category: String,
  data: Array
})

const chartData = ref({
  labels: [],
  datasets: []
})

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        color: '#fff',
        font: { size: 13 }
      }
    },
    title: {
      display: true,
      text: 'Aktueller Bestand',
      color: '#fff',
      font: { size: 16, weight: 'bold' }
    },
    tooltip: {
      backgroundColor: '#222',
      titleColor: '#fff',
      bodyColor: '#ddd'
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
      grid: { color: 'rgba(255,255,255,0.1)' }
    }
  }
})

const colorPalette = [
  '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
  '#9966FF', '#FF9F40', '#00C49F', '#F95F62'
]

const updateChart = () => {
  const datasets = props.data.map((item, index) => ({
    label: item.name,
    data: [item.bestand],
    backgroundColor: colorPalette[index % colorPalette.length],
    borderColor: colorPalette[index % colorPalette.length],
    borderWidth: 1
  }))

  chartData.value = {
    labels: [props.category],
    datasets
  }
}

watch(() => props.data, updateChart, { immediate: true })
</script>

<template>
  <div style="height: 300px;">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>
