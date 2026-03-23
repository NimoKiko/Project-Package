<template>
  <div class="merge-pdf-tool">

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
          multiple
          :limit="2"
        >
          <div class="upload-icon-wrap">
            <el-icon><DocumentCopy /></el-icon>
          </div>
          <div class="upload-main-text">拖拽两个 PDF 到此处 或 <em>点击上传</em></div>
          <div class="upload-hint-text">文件将按交替页码顺序合并</div>
        </el-upload>
      </div>
    </div>

    <!-- File table section -->
    <div class="tool-section" v-if="tableList.length > 0">
      <div class="section-label">
        <el-icon><Files /></el-icon>
        待合并文件
      </div>
      <div class="table-container">
        <el-table :data="tableList">
          <el-table-column label="文件 1" align="left" min-width="180">
            <template #default="{ row }">
              <span class="filename">{{ row.file1 }}</span>
            </template>
          </el-table-column>
          <el-table-column label="文件 2" align="left" min-width="180">
            <template #default="{ row }">
              <span class="filename">{{ row.file2 }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="right" width="130">
            <template #default="">
              <el-button class="action-btn" @click="mergeFile">
                <el-icon><Link /></el-icon>
                合并
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
let selectedFile1 = ref<UploadFile>()
let selectedFile2 = ref<UploadFile>()

interface tableType { file1: string, file2: string }
let tableList = reactive<tableType[]>([])

function handleFileChange(file: UploadFile, fileList: UploadFile[]) {
  if (tableList) tableList.pop()
  if (fileList.length == 2) {
    selectedFile1.value = fileList[0]
    selectedFile2.value = fileList[1]
    tableList.push({ file1: fileList[0].name, file2: fileList[1].name })
  }
}

function mergeFile() {
  if (!selectedFile1.value?.raw || !selectedFile2.value?.raw) {
    ElMessage.error('请先选择文件'); return;
  }
  let formData = new FormData()
  formData.append("file1", selectedFile1.value.raw)
  formData.append("file2", selectedFile2.value.raw)
  pdfStore.mergePDF(formData).then(res => {
    try {
      const blob = new Blob([res])
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `merged.pdf`;
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
.merge-pdf-tool {
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
}
</style>
