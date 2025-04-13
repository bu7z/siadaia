<!-- src/components/FadeOverlay.vue -->
<template>
    <transition name="fade">
      <div v-if="visible" class="fade-overlay d-flex justify-content-center align-items-center">
        <div class="spinner-border text-light" role="status">
          <span class="visually-hidden">Lade...</span>
        </div>
      </div>
    </transition>
  </template>
  
  <script setup>
  defineProps({
    visible: Boolean
  })
  </script>
  
  <style scoped>
  .fade-overlay {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    background-color: rgba(0, 0, 0, 0.92);
    backdrop-filter: blur(3px);
    z-index: 9999;
    transition: opacity 0.6s ease-in-out;
  }
  
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.6s;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
  }
  .fade-enter-to, .fade-leave-from {
    opacity: 1;
  }
  </style>
  