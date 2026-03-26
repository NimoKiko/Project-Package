<template>
  <div id="Header" class="quiet-header-inner">
    <div class="brand">
      <div class="brand-icon">
        <el-icon><Tools /></el-icon>
      </div>
      <div class="brand-text">
        <h1>QuietUtility</h1>
        <span class="tagline">Precision Toolkit</span>
      </div>
    </div>
    <nav class="header-nav">
      <router-link to="/audio" class="nav-link" :class="{ active: $route.path.includes('/audio') }">
        音频转换
      </router-link>
      <router-link to="/pdf" class="nav-link" :class="{ active: $route.path.includes('/pdf') }">
        PDF 处理
      </router-link>
    </nav>
    <div class="header-actions">
      <button class="action-btn">
        <el-icon><Bell /></el-icon>
      </button>
      <button class="action-btn">
        <el-icon><User /></el-icon>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped lang="scss">
.quiet-header-inner {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;

  .brand {
    display: flex;
    align-items: center;
    gap: 14px;

    .brand-icon {
      width: 42px;
      height: 42px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--md-primary);
      border-radius: 12px;
      color: var(--md-on-primary);
      font-size: 20px;
      flex-shrink: 0;
      box-shadow: 0 4px 12px rgba(33, 100, 137, 0.25);
    }

    .brand-text {
      h1 {
        font-family: var(--font-display);
        font-size: 20px;
        font-weight: 800;
        color: var(--md-on-background);
        letter-spacing: -0.02em;
        line-height: 1.2;
      }

      .tagline {
        font-family: var(--font-body);
        font-size: 10px;
        color: var(--md-on-surface-variant);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        display: block;
        margin-top: 1px;
      }
    }
  }

  .header-nav {
    display: flex;
    align-items: center;
    gap: 8px;

    .nav-link {
      padding: 10px 20px;
      border-radius: 50px;
      font-family: var(--font-body);
      font-size: 13px;
      font-weight: 600;
      color: var(--md-on-surface-variant);
      text-decoration: none;
      transition: all var(--transition-fast);
      letter-spacing: 0.01em;

      &:hover {
        color: var(--md-on-surface);
        background-color: var(--md-surface-container);
      }

      &.active {
        color: var(--md-primary);
        background-color: var(--md-primary-container);
      }
    }
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 8px;

    .action-btn {
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: transparent;
      border: none;
      border-radius: 12px;
      color: var(--md-on-surface-variant);
      font-size: 20px;
      cursor: pointer;
      transition: all var(--transition-fast);

      &:hover {
        background-color: var(--md-surface-container);
        color: var(--md-on-surface);
        transform: scale(1.05);
      }
    }
  }
}
</style>
