<template>
  <div id="Header" class="Header">
    <span>Personal Toolkit Site</span>
  </div>
</template>

<script setup lang="ts">
// Composition API with TypeScript
import { onMounted } from 'vue'

// Lifecycle hook
onMounted(() => {
  console.log('Component mounted')
})

// Methods
</script>

<style scoped lang="scss">
@use "@/assets/scss/variable.scss" as vars;
.Header {
  // padding: 1rem;
  height: vars.$header-height;
  background: vars.$background-color1;
  box-shadow: vars.$box-shadow1;
  display: flex;
  justify-content: center;
  align-items: center;
  span{
    color: white;
    font-size: 40px;
  }
}
</style>