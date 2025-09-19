<template>
  <div class="single-pdf">
    <div class="file-upload-wrap">
      <el-upload class="upload-demo" drag ref="uploadRef" :auto-upload="false" :on-change="handleFileChange"
        :show-file-list="true" :on-remove="handleFileRemove">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽到此上传 或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            上传单个PDF文件
          </div>
        </template>
      </el-upload>
    </div>
    <el-divider />
    <div class="file-table">
      <el-table :data="tableList">
        <el-table-column label="文件名" align="center" prop="fileName"></el-table-column>
        <el-table-column label="格式" align="center" prop="type"></el-table-column>
        <el-table-column label="操作" align="center">
          <template #default="">
            <el-button link type="primary" @click="reversePage">逆序</el-button>
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

let selectedFile = ref<UploadFile>()

interface tableType {
  fileName: string,
  type: string
}

let tableList = reactive<tableType[]>([])


// 方法
// 处理文件列表改变
function handleFileChange(file: UploadFile) {

  if (!file.raw) {
    ElMessage.error('无效的文件');
    return;
  }

  let [fileName, type] = file.raw.name.split(".")

  let temp = {
    fileName: fileName,
    type: type
  }

  tableList.push(temp)

  selectedFile.value = file

}

// 逆序排列pdf文件页面
function reversePage() {

  if (!selectedFile.value?.raw) {
    ElMessage.error('请先选择文件');
    return;
  }

  let formData = new FormData()

  formData.append("file", selectedFile.value.raw)

  pdfStore.reversePDF(formData).then(res => {

    // console.log(res);

    try {
      // 1. 创建 blob对象
      const blob = new Blob([res])

      // 2. 创建下载链接
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;

      // 3. 从后端响应头或前端自定义文件名
      let fileName = `${tableList[0].fileName}_reversed.pdf`; // 默认文件名

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
.single-pdf {
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