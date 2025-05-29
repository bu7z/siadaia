<script setup>
import HeroInventory from '../components/HeroInventory.vue'
import Footer from '@/components/Footer.vue'
import { ref, onMounted } from 'vue'

const cameraUrls = ref([])

onMounted(() => {
  cameraUrls.value = [
    '/cam/1',
    '/cam/2',
    '/cam/3',
    '/cam/4'
  ]
})
</script>


<template>
    <HeroInventory />
  
    <div v-if="cameraUrls.length" class="camera-grid">
      <div v-for="(url, i) in cameraUrls" :key="i" class="camera-feed">
        <h6>Kamera {{ i + 1 }}</h6>
        <img :src="url" class="w-100 border rounded shadow-sm" />
      </div>
    </div>
  
    <Footer />
</template>


<style scoped>
.camera-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.camera-feed {
  flex: 1 1 45%;
}
</style>
