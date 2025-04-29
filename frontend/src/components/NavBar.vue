<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navigate = (path) => {
  router.push(path)
}
</script>

<template>
  <aside class="sidebar d-flex flex-column align-items-center pt-4">
    <img src="@/assets/SIA_logo.svg" alt="SIA Logo" title="Inventory" @click="navigate('/inventory')" style="width: 40px; margin-bottom: 2rem; cursor: pointer;" />

    <i class="bi bi-box-seam fs-4 mb-4" title="Stock" @click="navigate('/stock')"></i>
    <i class="bi bi-bar-chart-line fs-4 mb-4" title="Statistics" @click="navigate('/statistics')"></i>
    <i class="bi bi-person-circle fs-4" title="User" @click="navigate('/user')"></i>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 70px;
  background-color: #1f1f1f;
  border-right: 1px solid #333;
  min-height: 100%;
}

i {
  color: #ccc;
  cursor: pointer;
}

i:hover {
  color: white;
}
</style>