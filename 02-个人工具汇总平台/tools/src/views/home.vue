<template>
  <div id="Home">
    <header class="obsidian-header">
      <Header></Header>
    </header>
    <aside class="obsidian-sidebar">
      <Side></Side>
    </aside>
    <main class="obsidian-main">
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
  background-color: var(--bg-deep);
  overflow: hidden;

  .obsidian-header {
    grid-area: header;
    background-color: var(--bg-card);
    border-bottom: 1px solid var(--border);
    position: relative;
    z-index: 10;

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(
        90deg,
        transparent 0%,
        var(--accent) 20%,
        var(--accent) 80%,
        transparent 100%
      );
      opacity: 0.4;
    }
  }

  .obsidian-sidebar {
    grid-area: sidebar;
    background-color: var(--bg-card);
    border-right: 1px solid var(--border);
    overflow-y: auto;
    position: relative;

    &::after {
      content: '';
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      width: 1px;
      background: linear-gradient(
        to bottom,
        transparent 0%,
        var(--accent) 30%,
        var(--accent) 70%,
        transparent 100%
      );
      opacity: 0.35;
      pointer-events: none;
    }
  }

  .obsidian-main {
    grid-area: main;
    background-color: var(--bg-deep);
    padding: 28px 32px;
    overflow-y: auto;
    animation: fade-in-up 0.3s ease forwards;
  }
}
</style>
