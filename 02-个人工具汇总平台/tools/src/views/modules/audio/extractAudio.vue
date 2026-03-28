<template>
  <div class="extract-audio-tool">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">音频提取</h1>
        <p class="page-desc">上传视频文件，提取其中的音频轨道并下载</p>
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
          <el-icon><VideoCamera /></el-icon>
        </div>
        <div class="card-content">
          <h3 class="card-title">上传视频文件</h3>
          <p class="card-desc">支持 MP4、AVI、MOV、MKV、WEBM 等多种视频格式</p>
          <div class="upload-zone-wrapper">
            <el-upload
              class="upload-demo"
              drag
              ref="uploadRef"
              :auto-upload="false"
              :on-change="handleFileChange"
              :show-file-list="false"
              :on-remove="handleFileRemove"
              accept=".mp4,.avi,.mov,.mkv,.webm"
            >
              <div class="upload-inner">
                <div class="upload-icon-bg">
                  <el-icon><Upload /></el-icon>
                </div>
                <div class="upload-text">
                  <span class="upload-main">拖拽视频到此处</span>
                  <span class="upload-sub">或点击选择视频文件</span>
                </div>
              </div>
            </el-upload>
          </div>
        </div>
      </div>

      <!-- Output Format Card -->
      <div class="bento-card format-card">
        <div class="card-icon secondary">
          <el-icon><Headset /></el-icon>
        </div>
        <h3 class="card-title">输出格式</h3>
        <p class="card-desc">选择提取的音频格式</p>
        <div class="format-grid">
          <button
            v-for="fmt in audioFormats"
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
            <span class="file-type">{{ videoInfo.type.toUpperCase() }}</span>
            <span class="file-size">{{ formatFileSize(selectedFile.size) }}</span>
          </div>
        </div>
        <button class="extract-action-btn" @click="extractAudio" :disabled="isExtracting">
          <el-icon v-if="isExtracting"><Loading /></el-icon>
          <span>{{ isExtracting ? '提取中...' : '提取音频' }}</span>
        </button>
      </div>

      <!-- Recent Activity Card -->
      <div v-if="recentFiles.length > 0" class="bento-card recent-card">
        <div class="card-header">
          <h3 class="card-title">最近提取</h3>
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
              <span class="recent-detail">{{ file.source }} → {{ file.output }}</span>
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
                <el-icon class="file-cell-icon"><VideoCamera /></el-icon>
                <span class="file-cell-name">{{ row.fileName }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="type" label="视频格式" align="center" width="120">
            <template #default="{ row }">
              <span class="type-badge video">{{ row.type }}</span>
            </template>
          </el-table-column>
          <el-table-column label="提取格式" align="right" width="320">
            <template #default="{ row }">
              <div class="format-actions">
                <el-button
                  v-for="fmt in audioFormats"
                  :key="fmt"
                  class="format-action-btn"
                  size="small"
                  @click="extractWithFormat(row, fmt)"
                >
                  提取 {{ fmt.toUpperCase() }}
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
const isExtracting = ref(false)
const selectedFormat = ref('mp3')

const audioFormats = ['mp3', 'wav', 'flac', 'ogg', 'aac']
const videoFormats = ['mp4', 'avi', 'mov', 'mkv', 'webm']

interface tableType { fileName: string, type: string, raw?: File }
let tableData = reactive<tableType[]>([])

interface RecentFile {
  name: string
  source: string
  output: string
  time: string
}
const recentFiles = reactive<RecentFile[]>([])

let videoInfo = reactive({ name: "", type: "" })

function handleFileChange(file: UploadFile) {
  if (!file.raw) { ElMessage.error('无效的文件'); return; }

  // 检查是否为视频文件
  const ext = file.name.split(".").pop()?.toLowerCase() || ''
  if (!videoFormats.includes(ext)) {
    ElMessage.warning('请选择视频文件格式 (MP4, AVI, MOV, MKV, WEBM)')
    return
  }

  videoInfo.name = file.name.split(".")[0]
  videoInfo.type = ext
  tableData.push({ fileName: file.name, type: ext, raw: file.raw })
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

function extractWithFormat(row: tableType, format: string) {
  if (!row.raw) { ElMessage.error('文件数据无效'); return; }
  doExtraction(row.raw, row.fileName, format);
}

function extractAudio() {
  if (!selectedFile.value?.raw) { ElMessage.error('请先选择视频文件'); return; }
  doExtraction(selectedFile.value.raw, selectedFile.value.name, selectedFormat.value);
}

function doExtraction(file: File, fileName: string, targetFormat: string) {
  isExtracting.value = true;
  const name = fileName.split(".")[0];
  const sourceType = fileName.split(".").pop() || 'video';

  const formData = new FormData()
  formData.append('file', file)
  formData.append('type', targetFormat)

  audioStore.extractAudio(formData).then(res => {
    try {
      const blob = new Blob([res])
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `${name}_audio.${targetFormat}`;
      document.body.appendChild(link);
      link.click();
      window.URL.revokeObjectURL(downloadUrl);
      document.body.removeChild(link);

      // Add to recent
      recentFiles.unshift({
        name: `${name}_audio.${targetFormat}`,
        source: sourceType.toUpperCase(),
        output: targetFormat.toUpperCase(),
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      });
      if (recentFiles.length > 5) recentFiles.pop();

      ElMessage.success('音频提取完成，正在下载...')
    } catch (error) {
      ElMessage.error('下载失败:' + error)
    }
  }).catch(err => {
    ElMessage.error('提取失败: ' + (err.message || '未知错误'))
  }).finally(() => {
    isExtracting.value = false;
  })
}
</script>

<style scoped lang="scss">
.extract-audio-tool {
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
        background: var(--md-secondary-container);
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
          color: var(--md-on-secondary-container);
          opacity: 0.8;
        }

        .stat-value {
          font-size: 28px;
          font-weight: 800;
          color: var(--md-secondary);
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
          background: var(--md-secondary);
          color: var(--md-on-secondary);
          border-color: var(--md-secondary);
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

    .extract-action-btn {
      width: 100%;
      padding: 14px 24px;
      background: var(--md-secondary);
      color: var(--md-on-secondary);
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
        background: var(--md-secondary-dim);
        box-shadow: 0 4px 12px rgba(100, 100, 100, 0.3);
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
          background: var(--md-secondary-container);
          color: var(--md-secondary);
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
          background: var(--md-secondary-container);
          color: var(--md-secondary);
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
        color: var(--md-secondary);
        background: var(--md-secondary-container);
        padding: 4px 12px;
        border-radius: 50px;
        letter-spacing: 0.02em;

        &.video {
          color: var(--md-tertiary);
          background: var(--md-tertiary-container);
        }
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
            background: var(--md-secondary);
            color: var(--md-on-secondary);
          }
        }
      }
    }
  }
}
</style>
