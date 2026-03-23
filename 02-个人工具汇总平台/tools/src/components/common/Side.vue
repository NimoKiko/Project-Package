<template>
  <div id="Side" class="obsidian-sidebar-inner">
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
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style scoped lang="scss">
.obsidian-sidebar-inner {
  height: 100%;
  padding: 24px 0 20px;

  .sidebar-nav {
    .nav-section {
      .section-label {
        display: block;
        font-family: var(--font-body);
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: var(--text-muted);
        padding: 0 28px;
        margin-bottom: 10px;
      }

      .nav-list {
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 2px;
        padding: 0 12px;

        .nav-item {
          position: relative;
          border-radius: 8px;
          overflow: hidden;

          &.active .nav-link {
            background: var(--bg-elevated);
            color: var(--accent);

            .nav-icon { color: var(--accent); }

            &::before { opacity: 1; }
          }

          .nav-link {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 11px 16px;
            border-radius: 8px;
            color: var(--text-secondary);
            text-decoration: none;
            transition: all var(--transition-fast);
            position: relative;

            &::before {
              content: '';
              position: absolute;
              left: 0;
              top: 50%;
              transform: translateY(-50%);
              width: 3px;
              height: 22px;
              background: var(--accent);
              border-radius: 0 2px 2px 0;
              opacity: 0;
              transition: opacity var(--transition-fast);
              box-shadow: 0 0 8px var(--accent-glow);
            }

            &:hover {
              background: var(--bg-elevated);
              color: var(--text-primary);
            }

            .nav-icon {
              font-size: 16px;
              display: flex;
              align-items: center;
              justify-content: center;
              color: var(--text-muted);
              transition: color var(--transition-fast);
              flex-shrink: 0;
            }

            .nav-text {
              font-family: var(--font-body);
              font-size: 13px;
              font-weight: 500;
            }
          }
        }
      }
    }
  }
}
</style>
