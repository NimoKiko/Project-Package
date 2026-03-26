<template>
  <div id="Side" class="quiet-sidebar-inner">
    <nav class="sidebar-nav">
      <div class="nav-section">
        <span class="section-label">Tools</span>
        <ul class="nav-list">
          <li class="nav-item" :class="{ active: route.name === 'audio' }">
            <router-link to="/audio" class="nav-link">
              <span class="nav-icon">
                <el-icon><Headset /></el-icon>
              </span>
              <span class="nav-text">音频转换</span>
            </router-link>
          </li>
          <li class="nav-item" :class="{ active: route.name === 'pdf' }">
            <router-link to="/pdf" class="nav-link">
              <span class="nav-icon">
                <el-icon><Document /></el-icon>
              </span>
              <span class="nav-text">PDF 处理</span>
            </router-link>
          </li>
        </ul>
      </div>
    </nav>
    <div class="sidebar-footer">
      <button class="new-project-btn">
        <el-icon><Plus /></el-icon>
        <span>新建任务</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style scoped lang="scss">
.quiet-sidebar-inner {
  height: 100%;
  padding: 32px 16px 24px;
  display: flex;
  flex-direction: column;

  .sidebar-nav {
    flex: 1;

    .nav-section {
      .section-label {
        display: block;
        font-family: var(--font-body);
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: var(--md-on-surface-variant);
        padding: 0 16px;
        margin-bottom: 12px;
      }

      .nav-list {
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 4px;

        .nav-item {
          position: relative;
          border-radius: 0 50px 50px 0;
          overflow: hidden;
          margin-right: -16px;

          &.active .nav-link {
            background: var(--md-surface-container-lowest);
            color: var(--md-primary);
            box-shadow: var(--shadow-sm);

            .nav-icon { color: var(--md-primary); }
          }

          .nav-link {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 14px 20px;
            color: var(--md-on-surface-variant);
            text-decoration: none;
            transition: all var(--transition-fast);
            position: relative;
            border-radius: 0 50px 50px 0;
            margin-right: 16px;

            &:hover {
              background: rgba(255, 255, 255, 0.5);
              color: var(--md-on-surface);
            }

            .nav-icon {
              font-size: 22px;
              display: flex;
              align-items: center;
              justify-content: center;
              color: var(--md-on-surface-variant);
              transition: color var(--transition-fast);
              flex-shrink: 0;
            }

            .nav-text {
              font-family: var(--font-body);
              font-size: 14px;
              font-weight: 600;
              letter-spacing: 0.01em;
            }
          }
        }
      }
    }
  }

  .sidebar-footer {
    padding: 0 12px;

    .new-project-btn {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 14px 20px;
      background: var(--md-primary);
      color: var(--md-on-primary);
      border: none;
      border-radius: 50px;
      font-family: var(--font-body);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.02em;
      cursor: pointer;
      transition: all var(--transition-fast);
      box-shadow: 0 4px 12px rgba(33, 100, 137, 0.25);

      &:hover {
        background: var(--md-primary-dim);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(33, 100, 137, 0.35);
      }

      .el-icon {
        font-size: 18px;
      }
    }
  }
}
</style>
