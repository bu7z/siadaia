<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navigate = (path) => {
  router.push(path)
}
</script>

<template>
  <!-- HERO -->
  <div class="bg-dark text-white text-center p-5 shadow-sm">
    <img
      src="@/assets/SIA_logo.svg"
      alt="SIA Logo"
      @click="navigate('/')"
      style="max-height: 100px; cursor: pointer;"
    />
    <p class="text-white-50 mb-1 fs-6">Inventory Advisory</p>
    <p class="lead mb-0">Der Erste seiner Art.</p>
  </div>

</template>