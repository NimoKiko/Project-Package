<template>
  <div class="audio-tool">

    <!-- Page header -->
    <div class="tool-header">
      <h1 class="tool-title">音频转换</h1>
      <p class="tool-desc">上传音频文件，一键转换为目标格式并下载</p>
    </div>

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
            <el-icon><Headset /></el-icon>
          </div>
          <div class="upload-main-text">拖拽文件到此处 或 <em>点击上传</em></div>
          <div class="upload-hint-text">支持 MP3 · FLAC · OGG · WAV · MP4</div>
        </el-upload>
      </div>
    </div>

    <!-- File table section -->
    <div class="tool-section" v-if="tableData.length > 0">
      <div class="section-label">
        <el-icon><List /></el-icon>
        文件列表
      </div>
      <div class="table-container">
        <el-table :data="tableData">
          <el-table-column prop="fileName" label="文件名称" align="left" min-width="200"></el-table-column>
          <el-table-column prop="type" label="格式" align="center" width="140">
            <template #default="{ row }">
              <span class="type-badge">{{ row.type }}</span>
            </template>
          </el-table-column>
          <el-table-column label="转换格式" align="right" width="300">
            <template #default="">
              <div class="format-actions">
                <el-button class="format-btn" @click="formatChange('mp3')">MP3</el-button>
                <el-button class="format-btn" @click="formatChange('flac')">FLAC</el-button>
                <el-button class="format-btn" @click="formatChange('ogg')">OGG</el-button>
                <el-button class="format-btn" @click="formatChange('wav')">WAV</el-button>
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
import "@/assets/scss/table-style.scss"
import "@/assets/scss/button-style.scss"
import "@/assets/scss/upload-zone.scss"

const audioStore = useAudioStore()
const uploadRef = ref();
let selectedFile = ref<UploadFile>()
let songInfo = reactive({ name: "", type: "" })

interface tableType { fileName: string, type: string }
let tableData = reactive<tableType[]>([])

function handleFileChange(file: UploadFile) {
  if (!file.raw) { ElMessage.error('无效的文件'); return; }
  songInfo.name = file.name.split(".")[0]
  songInfo.type = file.name.split(".")[1]
  tableData.push({ fileName: file.name, type: file.raw.type })
  selectedFile.value = file;
}

function formatChange(type: string) {
  if (!selectedFile.value?.raw) { ElMessage.error('请先选择文件'); return; }
  const formData = new FormData()
  formData.append('file', selectedFile.value.raw)
  formData.append('type', type)
  audioStore.fileFormatTransform(formData).then(res => {
    try {
      const blob = new Blob([res])
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `${songInfo.name}.${type}`;
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

function handleFileRemove() { tableData.pop() }
</script>

<style scoped lang="scss">
.audio-tool {
  max-width: 960px;

  .tool-header {
    margin-bottom: 32px;

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
  }

  .format-actions {
    display: flex;
    gap: 6px;
    justify-content: flex-end;
    flex-wrap: wrap;
  }
}
</style>
