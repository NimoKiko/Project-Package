<template>
  <div class="pdf-tool">

    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">PDF 处理</h1>
        <p class="page-desc">合并多个 PDF 文件，或对单个文件进行页面操作</p>
      </div>
    </div>

    <!-- Tool Cards Grid -->
    <div class="tools-grid">
      <!-- Merge Tool Card -->
      <div class="tool-card" :class="{ active: activeTab === 'merge' }" @click="activeTab = 'merge'">
        <div class="card-icon primary">
          <el-icon><DocumentCopy /></el-icon>
        </div>
        <div class="card-info">
          <h3 class="card-title">合并文件</h3>
          <p class="card-desc">交替页码合并两个 PDF 文档</p>
        </div>
        <div class="card-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
      </div>

      <!-- Reverse Tool Card -->
      <div class="tool-card" :class="{ active: activeTab === 'reverse' }" @click="activeTab = 'reverse'">
        <div class="card-icon secondary">
          <el-icon><RefreshRight /></el-icon>
        </div>
        <div class="card-info">
          <h3 class="card-title">页面逆序</h3>
          <p class="card-desc">反转 PDF 页面顺序</p>
        </div>
        <div class="card-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
      </div>
    </div>

    <!-- Tool Content Area -->
    <div class="tool-content">
      <mergePDF v-if="activeTab === 'merge'" />
      <singlePDF v-if="activeTab === 'reverse'" />
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import mergePDF from './mergePDF.vue'
import singlePDF from './singlePDF.vue'

const activeTab = ref('merge')
</script>

<style scoped lang="scss">
.pdf-tool {
  max-width: 1200px;

  /* Page Header */
  .page-header {
    margin-bottom: 32px;

    .page-title {
      font-family: var(--font-display);
      font-size: 40px;
      font-weight: 800;
      color: var(--md-on-background);
      letter-spacing: -0.03em;
      line-height: 1.1;
      margin-bottom: 8px;
    }

    .page-desc {
      font-family: var(--font-body);
      font-size: 15px;
      color: var(--md-on-surface-variant);
      font-weight: 500;
    }
  }

  /* Tools Grid */
  .tools-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin-bottom: 32px;
  }

  .tool-card {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 24px 28px;
    background: var(--md-surface-container-lowest);
    border-radius: 20px;
    box-shadow: var(--shadow-card);
    cursor: pointer;
    transition: all var(--transition-base);
    border: 2px solid transparent;

    &:hover {
      box-shadow: var(--shadow-lg);
      transform: translateY(-2px);
    }

    &.active {
      border-color: var(--md-primary);
      background: var(--md-primary-container);

      .card-icon.primary {
        background: var(--md-primary);
        color: var(--md-on-primary);
      }

      .card-icon.secondary {
        background: var(--md-secondary);
        color: var(--md-on-secondary);
      }

      .card-title {
        color: var(--md-on-primary-container);
      }

      .card-desc {
        color: var(--md-on-primary-container);
        opacity: 0.8;
      }

      .card-arrow {
        color: var(--md-primary);
      }
    }

    .card-icon {
      width: 56px;
      height: 56px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      flex-shrink: 0;
      transition: all var(--transition-fast);

      &.primary {
        background: var(--md-primary-container);
        color: var(--md-primary);
      }

      &.secondary {
        background: var(--md-secondary-container);
        color: var(--md-on-secondary-container);
      }
    }

    .card-info {
      flex: 1;

      .card-title {
        font-family: var(--font-display);
        font-size: 18px;
        font-weight: 700;
        color: var(--md-on-surface);
        margin-bottom: 4px;
        transition: color var(--transition-fast);
      }

      .card-desc {
        font-size: 13px;
        color: var(--md-on-surface-variant);
        transition: color var(--transition-fast);
      }
    }

    .card-arrow {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--md-outline);
      font-size: 20px;
      transition: all var(--transition-fast);
    }
  }

  /* Tool Content */
  .tool-content {
    animation: fade-in-up 0.3s ease forwards;
  }
}
</style>
