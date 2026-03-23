<template>
  <div id="Header" class="obsidian-header-inner">
    <div class="header-left-accent"></div>
    <div class="brand">
      <div class="brand-icon">
        <el-icon><Tools /></el-icon>
      </div>
      <div class="brand-text">
        <h1>Personal Toolkit</h1>
        <span class="tagline">Developer Utilities Platform</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped lang="scss">
.obsidian-header-inner {
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 16px;
  position: relative;

  .header-left-accent {
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 3px;
    height: 28px;
    background: linear-gradient(to bottom, var(--accent), var(--accent-secondary));
    border-radius: 0 2px 2px 0;
    box-shadow: 0 0 12px var(--accent-glow);
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 14px;

    .brand-icon {
      width: 38px;
      height: 38px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%);
      border-radius: 10px;
      color: var(--bg-deep);
      font-size: 18px;
      flex-shrink: 0;
      box-shadow: 0 0 16px var(--accent-glow);
    }

    .brand-text {
      h1 {
        font-family: var(--font-display);
        font-size: 18px;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.02em;
        line-height: 1.2;
      }

      .tagline {
        font-family: var(--font-body);
        font-size: 10px;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        display: block;
        margin-top: 2px;
      }
    }
  }
}
</style>
