<template>
  <div class="format-convert-tool">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">格式转换</h1>
        <p class="page-desc">上传音频文件，一键转换为目标格式并下载</p>
      </div>
      <div class="header-stats">
        <div class="stat-card">
          <span class="stat-label">支持格式</span>
          <span class="stat-value">5+</span>
        </div>
      </div>
    </div>

    <!-- Bento Grid Layout -->
    <div class="bento-grid">

      <!-- Main Upload Card (Large) -->
      <div class="bento-card upload-card">
        <div class="card-icon">
          <el-icon><Headset /></el-icon>
        </div>
        <div class="card-content">
          <h3 class="card-title">上传音频文件</h3>
          <p class="card-desc">支持 MP3、FLAC、OGG、WAV、MP4 等多种格式</p>
          <div class="upload-zone-wrapper">
            <el-upload
              class="upload-demo"
              drag
              ref="uploadRef"
              :auto-upload="false"
              :on-change="handleFileChange"
              :show-file-list="false"
              :on-remove="handleFileRemove"
            >
              <div class="upload-inner">
                <div class="upload-icon-bg">
                  <el-icon><Upload /></el-icon>
                </div>
                <div class="upload-text">
                  <span class="upload-main">拖拽文件到此处</span>
                  <span class="upload-sub">或点击选择文件</span>
                </div>
              </div>
            </el-upload>
          </div>
        </div>
      </div>

      <!-- Quick Format Card -->
      <div class="bento-card format-card">
        <div class="card-icon secondary">
          <el-icon><RefreshRight /></el-icon>
        </div>
        <h3 class="card-title">快速转换</h3>
        <p class="card-desc">选择目标格式立即开始</p>
        <div class="format-grid">
          <button
            v-for="fmt in formats"
            :key="fmt"
            class="format-btn"
            :class="{ active: selectedFormat === fmt }"
            @click="selectedFormat = fmt"
          >
            {{ fmt.toUpperCase() }}
          </button>
        </div>
      </div>

      <!-- File Info Card (if file selected) -->
      <div v-if="selectedFile" class="bento-card file-card">
        <div class="card-icon tertiary">
          <el-icon><Document /></el-icon>
        </div>
        <div class="file-info">
          <h4 class="file-name">{{ selectedFile.name }}</h4>
          <div class="file-meta">
            <span class="file-type">{{ songInfo.type.toUpperCase() }}</span>
            <span class="file-size">{{ formatFileSize(selectedFile.size) }}</span>
          </div>
        </div>
        <button class="convert-action-btn" @click="convertFile" :disabled="isConverting">
          <el-icon v-if="isConverting"><Loading /></el-icon>
          <span>{{ isConverting ? '转换中...' : '开始转换' }}</span>
        </button>
      </div>

      <!-- Recent Activity Card -->
      <div v-if="recentFiles.length > 0" class="bento-card recent-card">
        <div class="card-header">
          <h3 class="card-title">最近转换</h3>
          <button class="clear-btn" @click="recentFiles = []">
            <el-icon><Delete /></el-icon>
          </button>
        </div>
        <div class="recent-list">
          <div
            v-for="(file, idx) in recentFiles"
            :key="idx"
            class="recent-item"
          >
            <div class="recent-icon">
              <el-icon><Check /></el-icon>
            </div>
            <div class="recent-info">
              <span class="recent-name">{{ file.name }}</span>
              <span class="recent-detail">{{ file.from }} → {{ file.to }}</span>
            </div>
            <span class="recent-time">{{ file.time }}</span>
          </div>
        </div>
      </div>

    </div>

    <!-- File Table Section (for multiple files) -->
    <div v-if="tableData.length > 0" class="table-section">
      <div class="section-header">
        <h2 class="section-title">文件列表</h2>
        <button class="clear-all-btn" @click="clearAllFiles">
          <el-icon><Delete /></el-icon>
          清空列表
        </button>
      </div>
      <div class="table-container">
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="fileName" label="文件名称" align="left" min-width="250">
            <template #default="{ row }">
              <div class="file-cell">
                <el-icon class="file-cell-icon"><Headset /></el-icon>
                <span class="file-cell-name">{{ row.fileName }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="type" label="当前格式" align="center" width="120">
            <template #default="{ row }">
              <span class="type-badge">{{ row.type }}</span>
            </template>
          </el-table-column>
          <el-table-column label="转换格式" align="right" width="320">
            <template #default="{ row }">
              <div class="format-actions">
                <el-button
                  v-for="fmt in formats"
                  :key="fmt"
                  class="format-action-btn"
                  size="small"
                  @click="formatChange(row, fmt)"
                >
                  {{ fmt.toUpperCase() }}
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus';
import type { UploadFile } from 'element-plus';
import { useAudioStore } from "@/stores/modules/audio"

const audioStore = useAudioStore()
const uploadRef = ref();
const selectedFile = ref<UploadFile | null>(null)
const isConverting = ref(false)
const selectedFormat = ref('mp3')

const formats = ['mp3', 'flac', 'ogg', 'wav', 'mp4']

interface tableType { fileName: string, type: string, raw?: File }
let tableData = reactive<tableType[]>([])

interface RecentFile {
  name: string
  from: string
  to: string
  time: string
}
const recentFiles = reactive<RecentFile[]>([])

let songInfo = reactive({ name: "", type: "" })

function handleFileChange(file: UploadFile) {
  if (!file.raw) { ElMessage.error('无效的文件'); return; }
  songInfo.name = file.name.split(".")[0]
  songInfo.type = file.name.split(".")[1]
  tableData.push({ fileName: file.name, type: file.raw.type, raw: file.raw })
  selectedFile.value = file;
  ElMessage.success(`已添加: ${file.name}`)
}

function handleFileRemove() {
  selectedFile.value = null;
  tableData.pop()
}

function clearAllFiles() {
  tableData.splice(0, tableData.length)
  selectedFile.value = null
}

function formatFileSize(bytes?: number): string {
  if (!bytes) return '-';
  const units = ['B', 'KB', 'MB', 'GB'];
  let size = bytes;
  let unitIndex = 0;
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  return `${size.toFixed(1)} ${units[unitIndex]}`;
}

function formatChange(row: tableType, type: string) {
  if (!row.raw) { ElMessage.error('文件数据无效'); return; }
  doConversion(row.raw, row.fileName, type);
}

function convertFile() {
  if (!selectedFile.value?.raw) { ElMessage.error('请先选择文件'); return; }
  doConversion(selectedFile.value.raw, selectedFile.value.name, selectedFormat.value);
}

function doConversion(file: File, fileName: string, targetType: string) {
  isConverting.value = true;
  const name = fileName.split(".")[0];
  const fromType = fileName.split(".")[1];

  const formData = new FormData()
  formData.append('file', file)
  formData.append('type', targetType)

  audioStore.fileFormatTransform(formData).then(res => {
    try {
      const blob = new Blob([res])
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `${name}.${targetType}`;
      document.body.appendChild(link);
      link.click();
      window.URL.revokeObjectURL(downloadUrl);
      document.body.removeChild(link);

      // Add to recent
      recentFiles.unshift({
        name: `${name}.${targetType}`,
        from: fromType.toUpperCase(),
        to: targetType.toUpperCase(),
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      });
      if (recentFiles.length > 5) recentFiles.pop();

      ElMessage.success('转换完成，正在下载...')
    } catch (error) {
      ElMessage.error('下载失败:' + error)
    }
  }).finally(() => {
    isConverting.value = false;
  })
}
</script>

<style scoped lang="scss">
.format-convert-tool {
  /* Page Header */
  .page-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 32px;
    padding-bottom: 8px;

    .header-content {
      .page-title {
        font-family: var(--font-display);
        font-size: 32px;
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

    .header-stats {
      .stat-card {
        background: var(--md-primary-container);
        padding: 16px 24px;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        min-width: 100px;

        .stat-label {
          font-size: 10px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          color: var(--md-on-primary-container);
          opacity: 0.8;
        }

        .stat-value {
          font-size: 28px;
          font-weight: 800;
          color: var(--md-primary);
          line-height: 1;
        }
      }
    }
  }

  /* Bento Grid */
  .bento-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 20px;
    margin-bottom: 32px;
  }

  /* Bento Card Base */
  .bento-card {
    background: var(--md-surface-container-lowest);
    border-radius: 24px;
    padding: 28px;
    box-shadow: var(--shadow-card);
    transition: all var(--transition-base);

    &:hover {
      box-shadow: var(--shadow-lg);
      transform: translateY(-2px);
    }

    .card-icon {
      width: 52px;
      height: 52px;
      border-radius: 16px;
      background: var(--md-primary-container);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 20px;
      color: var(--md-primary);
      font-size: 26px;

      &.secondary {
        background: var(--md-secondary-container);
        color: var(--md-on-secondary-container);
      }

      &.tertiary {
        background: var(--md-tertiary-container);
        color: var(--md-on-tertiary-container);
      }
    }

    .card-title {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 700;
      color: var(--md-on-surface);
      margin-bottom: 8px;
    }

    .card-desc {
      font-size: 13px;
      color: var(--md-on-surface-variant);
      margin-bottom: 20px;
      line-height: 1.5;
    }
  }

  /* Upload Card - Large */
  .upload-card {
    grid-column: span 8;
    display: flex;
    gap: 24px;

    .card-content {
      flex: 1;
    }

    .upload-zone-wrapper {
      .upload-demo {
        :deep(.el-upload-dragger) {
          padding: 0;
          border: 2px dashed var(--md-outline-variant);
          border-radius: 20px;
          background: var(--md-surface-container-low);
          transition: all var(--transition-fast);

          &:hover, &.is-dragover {
            border-color: var(--md-primary);
            background: var(--md-primary-container);
          }
        }
      }

      .upload-inner {
        padding: 40px 32px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;

        .upload-icon-bg {
          width: 64px;
          height: 64px;
          border-radius: 20px;
          background: var(--md-surface-container-high);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 28px;
          color: var(--md-primary);
        }

        .upload-text {
          text-align: center;

          .upload-main {
            display: block;
            font-size: 16px;
            font-weight: 600;
            color: var(--md-on-surface);
            margin-bottom: 4px;
          }

          .upload-sub {
            display: block;
            font-size: 13px;
            color: var(--md-on-surface-variant);
          }
        }
      }
    }
  }

  /* Format Card */
  .format-card {
    grid-column: span 4;

    .format-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;

      .format-btn {
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid var(--md-outline-variant);
        background: var(--md-surface-container-low);
        color: var(--md-on-surface-variant);
        font-family: var(--font-mono);
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: all var(--transition-fast);

        &:hover {
          border-color: var(--md-outline);
          background: var(--md-surface-container);
          color: var(--md-on-surface);
        }

        &.active {
          background: var(--md-primary);
          color: var(--md-on-primary);
          border-color: var(--md-primary);
        }
      }
    }
  }

  /* File Card */
  .file-card {
    grid-column: span 6;
    display: flex;
    flex-direction: column;

    .file-info {
      flex: 1;
      margin-bottom: 20px;

      .file-name {
        font-size: 16px;
        font-weight: 600;
        color: var(--md-on-surface);
        margin-bottom: 12px;
        word-break: break-all;
      }

      .file-meta {
        display: flex;
        gap: 12px;

        .file-type {
          font-family: var(--font-mono);
          font-size: 11px;
          font-weight: 600;
          padding: 4px 12px;
          background: var(--md-secondary-container);
          color: var(--md-on-secondary-container);
          border-radius: 50px;
        }

        .file-size {
          font-size: 12px;
          color: var(--md-on-surface-variant);
          padding: 4px 0;
        }
      }
    }

    .convert-action-btn {
      width: 100%;
      padding: 14px 24px;
      background: var(--md-primary);
      color: var(--md-on-primary);
      border: none;
      border-radius: 50px;
      font-family: var(--font-body);
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all var(--transition-fast);

      &:hover:not(:disabled) {
        background: var(--md-primary-dim);
        box-shadow: 0 4px 12px rgba(33, 100, 137, 0.3);
      }

      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    }
  }

  /* Recent Card */
  .recent-card {
    grid-column: span 6;

    .card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;

      .card-title {
        margin-bottom: 0;
      }

      .clear-btn {
        width: 32px;
        height: 32px;
        border-radius: 10px;
        border: none;
        background: var(--md-surface-container);
        color: var(--md-on-surface-variant);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all var(--transition-fast);

        &:hover {
          background: var(--md-error-container);
          color: var(--md-on-error-container);
        }
      }
    }

    .recent-list {
      display: flex;
      flex-direction: column;
      gap: 12px;

      .recent-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        background: var(--md-surface-container-low);
        border-radius: 16px;

        .recent-icon {
          width: 32px;
          height: 32px;
          border-radius: 10px;
          background: var(--md-primary-container);
          color: var(--md-primary);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 16px;
        }

        .recent-info {
          flex: 1;
          min-width: 0;

          .recent-name {
            display: block;
            font-size: 13px;
            font-weight: 600;
            color: var(--md-on-surface);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
          }

          .recent-detail {
            display: block;
            font-size: 11px;
            color: var(--md-on-surface-variant);
            margin-top: 2px;
          }
        }

        .recent-time {
          font-size: 11px;
          color: var(--md-outline);
          font-weight: 500;
        }
      }
    }
  }

  /* Table Section */
  .table-section {
    background: var(--md-surface-container-lowest);
    border-radius: 24px;
    padding: 28px;
    box-shadow: var(--shadow-card);

    .section-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;

      .section-title {
        font-family: var(--font-display);
        font-size: 18px;
        font-weight: 700;
        color: var(--md-on-surface);
      }

      .clear-all-btn {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        background: var(--md-surface-container);
        border: none;
        border-radius: 50px;
        font-size: 12px;
        font-weight: 600;
        color: var(--md-on-surface-variant);
        cursor: pointer;
        transition: all var(--transition-fast);

        &:hover {
          background: var(--md-error-container);
          color: var(--md-on-error-container);
        }
      }
    }

    .table-container {
      .file-cell {
        display: flex;
        align-items: center;
        gap: 12px;

        .file-cell-icon {
          width: 36px;
          height: 36px;
          border-radius: 10px;
          background: var(--md-primary-container);
          color: var(--md-primary);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 18px;
        }

        .file-cell-name {
          font-weight: 500;
          color: var(--md-on-surface);
        }
      }

      .type-badge {
        display: inline-block;
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 600;
        color: var(--md-primary);
        background: var(--md-primary-container);
        padding: 4px 12px;
        border-radius: 50px;
        letter-spacing: 0.02em;
      }

      .format-actions {
        display: flex;
        gap: 8px;
        justify-content: flex-end;
        flex-wrap: wrap;

        .format-action-btn {
          font-family: var(--font-mono);
          font-size: 11px;
          font-weight: 600;
          padding: 6px 14px;
          border-radius: 50px;
          background: var(--md-surface-container);
          color: var(--md-on-surface-variant);
          border: none;

          &:hover {
            background: var(--md-primary);
            color: var(--md-on-primary);
          }
        }
      }
    }
  }
}
</style>
