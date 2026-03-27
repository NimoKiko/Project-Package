<template>
  <div class="pdf-tool">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">PDF 处理</h1>
        <p class="page-desc">专业的 PDF 文件处理工具箱</p>
      </div>
    </div>

    <!-- Main Layout: Sidebar + Content -->
    <div class="pdf-layout">
      <!-- Left Sidebar: Tool List -->
      <aside class="tools-sidebar">
        <nav class="tools-nav">
          <ul class="tools-list">
            <li
              v-for="tool in tools"
              :key="tool.id"
              class="tool-item"
              :class="{ active: activeTool === tool.id }"
              @click="activeTool = tool.id"
            >
              <div class="tool-icon" :class="tool.iconClass">
                <el-icon>
                  <component :is="tool.icon" />
                </el-icon>
              </div>
              <div class="tool-info">
                <h3 class="tool-name">{{ tool.name }}</h3>
                <p class="tool-desc">{{ tool.desc }}</p>
              </div>
            </li>
          </ul>
        </nav>
      </aside>

      <!-- Right Content: Tool Interface -->
      <main class="tool-content">
        <component :is="currentComponent" />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, markRaw } from 'vue'
import { DocumentCopy, RefreshRight, Unlock, Document } from '@element-plus/icons-vue'
import mergePDF from './mergePDF.vue'
import singlePDF from './singlePDF.vue'
import unlockPDF from './unlockPDF.vue'
import convertPDFtoWord from './convertPDFtoWord.vue'

// Tool configurations
const tools = [
  {
    id: 'merge',
    name: '合并文件',
    desc: '交替页码合并两个 PDF',
    icon: markRaw(DocumentCopy),
    iconClass: 'primary',
    component: markRaw(mergePDF)
  },
  {
    id: 'reverse',
    name: '页面逆序',
    desc: '反转 PDF 页面顺序',
    icon: markRaw(RefreshRight),
    iconClass: 'secondary',
    component: markRaw(singlePDF)
  },
  {
    id: 'unlock',
    name: '权限解锁',
    desc: '移除复制打印等限制',
    icon: markRaw(Unlock),
    iconClass: 'tertiary',
    component: markRaw(unlockPDF)
  },
  {
    id: 'convertWord',
    name: '转 Word',
    desc: 'PDF 转可编辑文档',
    icon: markRaw(Document),
    iconClass: 'quaternary',
    component: markRaw(convertPDFtoWord)
  }
]

const activeTool = ref('merge')

const currentComponent = computed(() => {
  const tool = tools.find(t => t.id === activeTool.value)
  return tool?.component || mergePDF
})
</script>

<style scoped lang="scss">
.pdf-tool {
  max-width: 1200px;

  /* Page Header */
  .page-header {
    margin-bottom: 24px;

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

  /* Main Layout */
  .pdf-layout {
    display: flex;
    gap: 24px;
    min-height: 600px;
  }

  /* Left Sidebar */
  .tools-sidebar {
    width: 240px;
    flex-shrink: 0;
    background: var(--md-surface-container-low);
    border-radius: 20px;
    padding: 16px;
    box-shadow: var(--shadow-card);

    .tools-nav {
      height: 100%;
    }

    .tools-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .tool-item {
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 14px 16px;
      border-radius: 16px;
      cursor: pointer;
      transition: all var(--transition-fast);
      border-left: 3px solid transparent;

      &:hover {
        background: var(--md-surface-container-high);
      }

      &.active {
        background: var(--md-surface-container-highest);
        border-left-color: var(--md-primary);

        .tool-icon.primary {
          background: var(--md-primary);
          color: var(--md-on-primary);
        }

        .tool-icon.secondary {
          background: var(--md-secondary);
          color: var(--md-on-secondary);
        }

        .tool-icon.tertiary {
          background: var(--md-tertiary);
          color: var(--md-on-tertiary);
        }

        .tool-icon.quaternary {
          background: #f59e0b;
          color: #fff;
        }

        .tool-name {
          color: var(--md-on-surface);
        }

        .tool-desc {
          color: var(--md-on-surface-variant);
        }
      }
    }

    .tool-icon {
      width: 44px;
      height: 44px;
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
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

      &.tertiary {
        background: var(--md-tertiary-container);
        color: var(--md-on-tertiary-container);
      }

      &.quaternary {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
      }
    }

    .tool-info {
      flex: 1;
      min-width: 0;

      .tool-name {
        font-family: var(--font-display);
        font-size: 15px;
        font-weight: 700;
        color: var(--md-on-surface);
        margin-bottom: 4px;
        transition: color var(--transition-fast);
      }

      .tool-desc {
        font-size: 12px;
        color: var(--md-on-surface-variant);
        line-height: 1.4;
        transition: color var(--transition-fast);
      }
    }
  }

  /* Right Content */
  .tool-content {
    flex: 1;
    min-width: 0;
    animation: fade-in-up 0.3s ease forwards;
  }
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
