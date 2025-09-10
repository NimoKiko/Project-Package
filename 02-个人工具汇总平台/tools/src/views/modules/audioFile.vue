<template>
  <div class="Audio-File container">
    <div class="file-upload-wrap">
      <el-upload class="upload-demo" drag ref="uploadRef" :auto-upload="false" :on-change="handleFileChange"
        :show-file-list="true" :on-remove="handleFileRemove">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽到此上传 或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            仅支持 MP3, MP4, OGG, FLAC, WAV格式
          </div>
        </template>
      </el-upload>

    </div>
    <el-divider />
    <div class="file-table">
      <el-table :data="tableData" style="width:98%">
        <el-table-column prop="fileName" label="文件名称" align="center"></el-table-column>
        <el-table-column prop="type" label="格式" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template #default="">
            <el-button @click="formatChange('mp3')">MP3</el-button>
            <el-button @click="formatChange('flac')">FLAC</el-button>
            <el-button @click="formatChange('ogg')">OGG</el-button>
            <el-button @click="formatChange('wav')">WAV</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
// Composition API with TypeScript
import { onMounted, ref, reactive } from 'vue'
import { ElMessage } from 'element-plus';
// import { GET_BASE_URL } from '../../utils/URL'
import type { UploadFile } from 'element-plus';
import { useAudioStore } from "@/stores/modules/audio"
import "@/assets/scss/table-style.scss"

// let URL = GET_BASE_URL() + "/audio/fileFormateTransform"
const audioStore = useAudioStore()
const uploadRef = ref();
let selectedFile = ref<UploadFile>()
let songInfo = reactive({
  name: "",
  type: ""
})

interface tableType {
  fileName: string,
  type: string
}

let tableData = reactive<tableType[]>([])

// 选择文件后触发
function handleFileChange(file: UploadFile) {

  if (!file.raw) {
    ElMessage.error('无效的文件');
    return;
  }
  songInfo.name = file.name.split(".")[0]
  songInfo.type = file.name.split(".")[1]

  let temp = {
    fileName: file.name,
    type: file.raw.type
  }
  tableData.push(temp)
  selectedFile.value = file;

};
// 文件转换
function formatChange(type: string) {

  if (!selectedFile.value?.raw) {
    ElMessage.error('请先选择文件');
    return;
  }

  const formData = new FormData()
  console.log(selectedFile.value.raw);

  formData.append('file', selectedFile.value.raw)
  formData.append('type', type)
  // 调用转换格式的API
  audioStore.fileFormatTransform(formData).then(res => {

    try {
      // 1. 创建 blob对象
      const blob = new Blob([res])

      // 2. 创建下载链接
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;

      // 3. 从后端响应头或前端自定义文件名
      let fileName = `${songInfo.name}.${type}`; // 默认文件名

      link.download = fileName;

      // 4. 触发点击下载
      document.body.appendChild(link);
      link.click();

      // 5. 清理
      window.URL.revokeObjectURL(downloadUrl);
      document.body.removeChild(link);

      ElMessage.success('转换完成，正在下载...')
    } catch (error) {
      ElMessage.error('下载失败:' + error)
    }
  })
}

// 处理文件移除
function handleFileRemove() {
  tableData.pop()
}

// Lifecycle hook
onMounted(() => {
  console.log('Component mounted')
})

// Methods
</script>

<style scoped lang="scss">

</style>