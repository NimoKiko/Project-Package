<template>
  <div id="Home">
    <header class="quiet-header">
      <Header></Header>
    </header>
    <aside class="quiet-sidebar">
      <Side></Side>
    </aside>
    <main class="quiet-main">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import Header from '../components/common/Header.vue'
import Side from '../components/common/Side.vue'
</script>

<style scoped lang="scss">
#Home {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main";
  grid-template-columns: var(--sidebar-width) 1fr;
  grid-template-rows: var(--header-height) 1fr;
  height: 100vh;
  background-color: var(--md-background);
  overflow: hidden;

  .quiet-header {
    grid-area: header;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--md-outline-variant);
    position: relative;
    z-index: 50;
  }

  .quiet-sidebar {
    grid-area: sidebar;
    background-color: var(--md-surface-variant);
    overflow-y: auto;
    position: relative;
  }

  .quiet-main {
    grid-area: main;
    background-color: var(--md-background);
    padding: 32px 40px;
    overflow-y: auto;
    animation: fade-in-up 0.3s ease forwards;
  }
}
</style>
