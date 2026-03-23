<template>
  <div class="pdf-tool">

    <!-- Page header -->
    <div class="tool-header">
      <h1 class="tool-title">PDF 处理</h1>
      <p class="tool-desc">合并多个 PDF 文件，或对单个文件进行页面操作</p>
    </div>

    <el-tabs v-model="activeName" class="obsidian-tabs" @tab-click="handleClick">
      <el-tab-pane name="merge">
        <template #label>
          <span class="tab-label">
            <el-icon><DocumentCopy /></el-icon>
            合并文件
          </span>
        </template>
        <mergePDF></mergePDF>
      </el-tab-pane>
      <el-tab-pane name="second">
        <template #label>
          <span class="tab-label">
            <el-icon><Sort /></el-icon>
            页面操作
          </span>
        </template>
        <singlePDF></singlePDF>
      </el-tab-pane>
    </el-tabs>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { TabsPaneContext } from 'element-plus'
import mergePDF from './mergePDF.vue'
import singlePDF from './singlePDF.vue'

const activeName = ref('merge')
const handleClick = (tab: TabsPaneContext, event: Event) => {}
</script>

<style scoped lang="scss">
.pdf-tool {
  max-width: 960px;

  .tool-header {
    margin-bottom: 28px;

    .tool-title {
      font-family: var(--font-display);
      font-size: 26px;
      font-weight: 700;
      color: var(--text-primary);
      letter-spacing: -0.02em;
      margin-bottom: 6px;
    }

    .tool-desc {
      font-family: var(--font-body);
      font-size: 14px;
      color: var(--text-muted);
    }
  }

  .obsidian-tabs {
    :deep(.el-tabs__header) {
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border);
    }

    :deep(.el-tabs__nav-wrap::after) {
      display: none;
    }

    :deep(.el-tabs__active-bar) {
      background: var(--accent);
      height: 2px;
      box-shadow: 0 0 12px var(--accent-glow);
    }

    :deep(.el-tabs__item) {
      font-family: var(--font-body);
      font-size: 14px;
      font-weight: 500;
      color: var(--text-muted);
      padding: 0 24px;
      height: 44px;
      line-height: 44px;
      transition: color var(--transition-fast);

      &:hover {
        color: var(--text-secondary);
      }

      &.is-active {
        color: var(--accent);
      }

      .tab-label {
        display: flex;
        align-items: center;
        gap: 7px;
      }
    }
  }
}
</style>
