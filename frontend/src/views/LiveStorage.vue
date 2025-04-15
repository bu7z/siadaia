<script setup>
import HeroInventory from '../components/HeroInventory.vue'
import Footer from '@/components/Footer.vue'
import { ref, onMounted } from 'vue'

const cameraUrls = ref([])

onMounted(() => {
  const ips = [
    import.meta.env.VITE_STORAGE_CAM_1,
    import.meta.env.VITE_STORAGE_CAM_2,
    import.meta.env.VITE_STORAGE_CAM_3,
    import.meta.env.VITE_STORAGE_CAM_4
  ].filter(Boolean)

  cameraUrls.value = ips.map(ip => `http://${ip}/axis-cgi/mjpg/video.cgi`)
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