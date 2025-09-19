<template>
  <div class="merge-pdf">
    <div class="file-upload-wrap">
      <el-upload class="upload-demo" drag ref="uploadRef" :auto-upload="false" :on-change="handleFileChange"
        :show-file-list="true" :on-remove="handleFileRemove" multiple :limit="2">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽到此上传 或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            需要上传两个pdf文件
          </div>
        </template>
      </el-upload>
    </div>
    <el-divider />
    <div class="file-table">
      <el-table :data="tableList">
        <el-table-column label="文件1" align="center" prop="file1"></el-table-column>
        <el-table-column label="文件2" align="center" prop="file2"></el-table-column>
        <el-table-column label="操作" align="center">
          <template #default="">
            <el-button link type="primary" @click="mergeFile">合并</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
// Composition API with TypeScript
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus';
import type { UploadFile } from 'element-plus'
import { usePDFStore } from '@/stores/modules/pdf';
// style
import "@/assets/scss/table-style.scss"

const pdfStore = usePDFStore()

const uploadRef = ref()

let selectedFile1 = ref<UploadFile>()
let selectedFile2 = ref<UploadFile>()

interface tableType {
  file1: string,
  file2: string
}

let tableList = reactive<tableType[]>([])


// 方法
// 处理文件列表改变
function handleFileChange(file: UploadFile, fileList: UploadFile[]) {
  if (tableList) tableList.pop()

  if (fileList.length == 2) {
    selectedFile1.value = fileList[0]
    selectedFile2.value = fileList[1]

    // 创建临时对象
    let temp = {
      file1: fileList[0].name,
      file2: fileList[1].name
    }
    // 加入文件列表中
    tableList.push(temp)
  }

}

// 合并文件
function mergeFile() {

  if (!selectedFile1.value?.raw || !selectedFile2.value?.raw) {
    ElMessage.error('请先选择文件');
    return;
  }

  let formData = new FormData()

  formData.append("file1", selectedFile1.value.raw)
  formData.append("file2", selectedFile2.value.raw)

  pdfStore.mergePDF(formData).then(res => {

    console.log(res);


    try {
      // 1. 创建 blob对象
      const blob = new Blob([res])

      // 2. 创建下载链接
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;

      // 3. 从后端响应头或前端自定义文件名
      let fileName = `merged.pdf`; // 默认文件名

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
  tableList.pop()
}



// Lifecycle hook
onMounted(() => {
  console.log('Component mounted')
})

// Methods
</script>

<style scoped lang="scss">
.merge-pdf {
  // border: 1px solid black;
  display: flex;
  justify-content: center;
  position: relative;
  height: 45rem;

  .file-upload-wrap {
    width: 100%;
    position: absolute;
    // border:1px solid black;
  }

  .el-divider {
    position: absolute;
    top: 32%;
  }

  .file-table {
    width: 100%;
    position: absolute;
    top: 40%;
  }
}
</style>