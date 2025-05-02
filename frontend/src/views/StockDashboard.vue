<script setup lang="ts">
import Footer from '@/components/Footer.vue';
import HeroInventory from '@/components/HeroInventory.vue';
import NavBar from '@/components/NavBar.vue';

</script>

<template>
    <div class="page-wrapper">
        <HeroInventory/>

        <!-- Dashboard Layout -->
        <div class="dashboard-container text-white">
        <NavBar class="sidebar" />
        </div>
        <Footer/>

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
</style>