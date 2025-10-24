<script setup>
import MainHead from './components/Header/MainHead.vue'
import { VueQueryDevtools } from '@tanstack/vue-query-devtools'
</script>

<template>
  <div class="app">
    <MainHead />
    
    <div class="page-container">
      <RouterView />
    </div>
  </div>
</template>

<style>
/* УБРАТЬ SCOPED - стили будут глобальными */
.app {
  min-height: 100vh;
  background-color: var(--color-bg);
}

.page-container {
  max-width: 1800px;
  margin: 0 auto;
}
</style>
