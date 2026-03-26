<template>
  <div class="merge-pdf-tool">

    <div class="bento-grid">
      <!-- Upload Card -->
      <div class="bento-card upload-card">
        <div class="card-icon">
          <el-icon><DocumentCopy /></el-icon>
        </div>
        <div class="card-content">
          <h3 class="card-title">上传两个 PDF 文件</h3>
          <p class="card-desc">文件将按交替页码顺序合并</p>
          <div class="upload-zone-wrapper">
            <el-upload
              class="upload-demo"
              drag
              ref="uploadRef"
              :auto-upload="false"
              :on-change="handleFileChange"
              :show-file-list="false"
              :on-remove="handleFileRemove"
              multiple
              :limit="2"
            >
              <div class="upload-inner">
                <div class="upload-icon-bg">
                  <el-icon><Upload /></el-icon>
                </div>
                <div class="upload-text">
                  <span class="upload-main">拖拽两个 PDF 到此处</span>
                  <span class="upload-sub">或点击选择文件</span>
                </div>
              </div>
            </el-upload>
          </div>
        </div>
      </div>

      <!-- File Status Card -->
      <div v-if="files.length > 0" class="bento-card status-card">
        <div class="card-icon secondary">
          <el-icon><Files /></el-icon>
        </div>
        <h3 class="card-title">待合并文件</h3>
        <div class="file-list">
          <div v-for="(file, idx) in files" :key="idx" class="file-item">
            <div class="file-number">{{ idx + 1 }}</div>
            <div class="file-info">
              <span class="file-name">{{ file.name }}</span>
            </div>
          </div>
        </div>
        <button
          v-if="files.length === 2"
          class="merge-action-btn"
          @click="mergeFile"
          :disabled="isMerging"
        >
          <el-icon v-if="isMerging"><Loading /></el-icon>
          <span>{{ isMerging ? '合并中...' : '开始合并' }}</span>
        </button>
      </div>

      <!-- Info Card -->
      <div v-else class="bento-card info-card">
        <div class="card-icon tertiary">
          <el-icon><InfoFilled /></el-icon>
        </div>
        <h3 class="card-title">合并说明</h3>
        <ul class="info-list">
          <li>支持两个 PDF 文件交替合并</li>
          <li>文件 1 的页 1 → 文件 2 的页 1 → 文件 1 的页 2...</li>
          <li>合并后保留原有格式和矢量质量</li>
        </ul>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus';
import type { UploadFile } from 'element-plus'
import { usePDFStore } from '@/stores/modules/pdf';

const pdfStore = usePDFStore()
const uploadRef = ref()
const isMerging = ref(false)
const files = reactive<UploadFile[]>([])

function handleFileChange(file: UploadFile, fileList: UploadFile[]) {
  files.splice(0, files.length, ...fileList)
  if (files.length === 2) {
    ElMessage.success('文件已就绪，可以开始合并')
  }
}

function handleFileRemove() {
  files.splice(0, files.length)
}

function mergeFile() {
  if (files.length !== 2) {
    ElMessage.error('请先选择两个文件'); return;
  }
  isMerging.value = true;
  let formData = new FormData()
  formData.append("file1", files[0].raw!)
  formData.append("file2", files[1].raw!)
  pdfStore.mergePDF(formData).then(res => {
    try {
      const blob = new Blob([res])
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `merged_${Date.now()}.pdf`;
      document.body.appendChild(link);
      link.click();
      window.URL.revokeObjectURL(downloadUrl);
      document.body.removeChild(link);
      ElMessage.success('合并完成，正在下载...')
    } catch (error) {
      ElMessage.error('下载失败:' + error)
    }
  }).finally(() => {
    isMerging.value = false;
  })
}
</script>

<style scoped lang="scss">
.merge-pdf-tool {
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

  .status-card {
    grid-column: span 5;
    display: flex;
    flex-direction: column;

    .file-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 20px;

      .file-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 16px;
        background: var(--md-surface-container-low);
        border-radius: 16px;

        .file-number {
          width: 28px;
          height: 28px;
          border-radius: 50%;
          background: var(--md-primary-container);
          color: var(--md-primary);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 12px;
          font-weight: 700;
        }

        .file-info {
          flex: 1;
          min-width: 0;

          .file-name {
            display: block;
            font-size: 13px;
            font-weight: 600;
            color: var(--md-on-surface);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
          }
        }
      }
    }

    .merge-action-btn {
      margin-top: auto;
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
