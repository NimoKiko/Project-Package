<template>
  <div class="single-pdf-tool">

    <!-- Upload section -->
    <div class="tool-section">
      <div class="section-label">
        <el-icon><Upload /></el-icon>
        上传文件
      </div>
      <div class="upload-zone-wrapper">
        <el-upload
          class="upload-demo"
          drag
          ref="uploadRef"
          :auto-upload="false"
          :on-change="handleFileChange"
          :show-file-list="true"
          :on-remove="handleFileRemove"
        >
          <div class="upload-icon-wrap">
            <el-icon><Document /></el-icon>
          </div>
          <div class="upload-main-text">拖拽 PDF 文件到此处 或 <em>点击上传</em></div>
          <div class="upload-hint-text">支持页面逆序等操作</div>
        </el-upload>
      </div>
    </div>

    <!-- File table section -->
    <div class="tool-section" v-if="tableList.length > 0">
      <div class="section-label">
        <el-icon><List /></el-icon>
        文件信息
      </div>
      <div class="table-container">
        <el-table :data="tableList">
          <el-table-column label="文件名" align="left" min-width="200">
            <template #default="{ row }">
              <span class="filename">{{ row.fileName }}</span>
            </template>
          </el-table-column>
          <el-table-column label="格式" align="center" width="120">
            <template #default="{ row }">
              <span class="type-badge">{{ row.type }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="right" width="140">
            <template #default="">
              <el-button class="action-btn" @click="reversePage">
                <el-icon><RefreshRight /></el-icon>
                逆序
              </el-button>
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
import type { UploadFile } from 'element-plus'
import { usePDFStore } from '@/stores/modules/pdf';
import "@/assets/scss/table-style.scss"
import "@/assets/scss/button-style.scss"
import "@/assets/scss/upload-zone.scss"

const pdfStore = usePDFStore()
const uploadRef = ref()
let selectedFile = ref<UploadFile>()

interface tableType { fileName: string, type: string }
let tableList = reactive<tableType[]>([])

function handleFileChange(file: UploadFile) {
  if (!file.raw) { ElMessage.error('无效的文件'); return; }
  let [fileName, type] = file.raw.name.split(".")
  tableList.push({ fileName, type })
  selectedFile.value = file
}

function reversePage() {
  if (!selectedFile.value?.raw) { ElMessage.error('请先选择文件'); return; }
  let formData = new FormData()
  formData.append("file", selectedFile.value.raw)
  pdfStore.reversePDF(formData).then(res => {
    try {
      const blob = new Blob([res])
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `${tableList[0].fileName}_reversed.pdf`;
      document.body.appendChild(link);
      link.click();
      window.URL.revokeObjectURL(downloadUrl);
      document.body.removeChild(link);
      ElMessage.success('转换完成，正在下载...')
    } catch (error) {
      ElMessage.error('下载失败:' + error)
    }
  })
}

function handleFileRemove() { tableList.pop() }
</script>

<style scoped lang="scss">
.single-pdf-tool {
  .tool-section {
    margin-bottom: 28px;

    .section-label {
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-body);
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--text-muted);
      margin-bottom: 12px;

      .el-icon { color: var(--accent); font-size: 13px; }
    }
  }

  .filename {
    font-family: var(--font-mono);
    font-size: 13px;
    color: var(--text-primary);
  }

  .type-badge {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    color: var(--accent);
    background: var(--accent-glow);
    padding: 3px 12px;
    border-radius: 50px;
    border: 1px solid rgba(56, 189, 248, 0.25);
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
}
</style>
