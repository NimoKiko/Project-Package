<template>
  <div class="convert-pdf-tool">

    <div class="bento-grid">
      <!-- Upload Card -->
      <div class="bento-card upload-card">
        <div class="card-icon">
          <el-icon><Document /></el-icon>
        </div>
        <div class="card-content">
          <h3 class="card-title">上传 PDF 文件</h3>
          <p class="card-desc">转换为可编辑的 Word 文档</p>
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
                  <span class="upload-main">拖拽 PDF 到此处</span>
                  <span class="upload-sub">或点击选择文件</span>
                </div>
              </div>
            </el-upload>
          </div>
        </div>
      </div>

      <!-- File Info Card -->
      <div v-if="selectedFile" class="bento-card file-card">
        <div class="card-icon secondary">
          <el-icon><Files /></el-icon>
        </div>
        <div class="file-info">
          <h4 class="file-name">{{ selectedFile.name }}</h4>
          <span class="file-type">PDF</span>
        </div>
        <button class="convert-action-btn" @click="convertToWordFile" :disabled="isConverting">
          <el-icon v-if="isConverting"><Loading /></el-icon>
          <span>{{ isConverting ? '转换中...' : '转换为 Word' }}</span>
        </button>
      </div>

      <!-- Info Card -->
      <div v-else class="bento-card info-card">
        <div class="card-icon tertiary">
          <el-icon><InfoFilled /></el-icon>
        </div>
        <h3 class="card-title">功能说明</h3>
        <ul class="info-list">
          <li>将 PDF 转换为可编辑的 Word 文档</li>
          <li>保留文字、图片和表格</li>
          <li>复杂排版可能存在偏差</li>
        </ul>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus';
import type { UploadFile } from 'element-plus'
import { usePDFStore } from '@/stores/modules/pdf';

const pdfStore = usePDFStore()
const uploadRef = ref()
const selectedFile = ref<UploadFile | null>(null)
const isConverting = ref(false)

function handleFileChange(file: UploadFile) {
  if (!file.raw) { ElMessage.error('无效的文件'); return; }
  selectedFile.value = file
  ElMessage.success(`已添加: ${file.name}`)
}

function handleFileRemove() {
  selectedFile.value = null
}

function convertToWordFile() {
  if (!selectedFile.value?.raw) { ElMessage.error('请先选择文件'); return; }
  isConverting.value = true
  const fileName = selectedFile.value.name.replace('.pdf', '')
  let formData = new FormData()
  formData.append("file", selectedFile.value.raw)
  pdfStore.convertToWord(formData).then(res => {
    try {
      const blob = new Blob([res])
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `${fileName}.docx`;
      document.body.appendChild(link);
      link.click();
      window.URL.revokeObjectURL(downloadUrl);
      document.body.removeChild(link);
      ElMessage.success('转换完成，正在下载...')
    } catch (error) {
      ElMessage.error('下载失败:' + error)
    }
  }).finally(() => {
    isConverting.value = false
  })
}
</script>

<style scoped lang="scss">
.convert-pdf-tool {
  .bento-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 20px;
  }

  .bento-card {
    background: var(--md-surface-container-lowest);
    border-radius: 24px;
    padding: 28px;
    box-shadow: var(--shadow-card);

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
      margin-bottom: 12px;
    }

    .card-desc {
      font-size: 13px;
      color: var(--md-on-surface-variant);
      margin-bottom: 20px;
    }
  }

  .upload-card {
    grid-column: span 7;
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

  .file-card {
    grid-column: span 5;
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

      .file-type {
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 600;
        padding: 4px 12px;
        background: var(--md-secondary-container);
        color: var(--md-on-secondary-container);
        border-radius: 50px;
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

  .info-card {
    grid-column: span 5;

    .info-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 12px;

      li {
        position: relative;
        padding-left: 20px;
        font-size: 13px;
        color: var(--md-on-surface-variant);
        line-height: 1.6;

        &::before {
          content: '';
          position: absolute;
          left: 0;
          top: 8px;
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: var(--md-primary);
        }
      }
    }
  }
}
</style>