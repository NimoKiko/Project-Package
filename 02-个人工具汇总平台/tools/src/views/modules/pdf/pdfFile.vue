<template>
  <div class="PDF-File container">
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
      <el-tab-pane label="合并" name="merge"><mergePDF></mergePDF></el-tab-pane>
      <el-tab-pane label="单文件操作" name="second"><singlePDF></singlePDF></el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
// Composition API with TypeScript
import { ref, onMounted } from 'vue'
import type { TabsPaneContext } from 'element-plus'
import mergePDF from './mergePDF.vue'
import singlePDF from './singlePDF.vue'

const activeName = ref('merge')

const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event)
}

// Lifecycle hook
onMounted(() => {
  console.log('Component mounted')
})

// Methods
</script>

<style scoped lang="scss">
.PDF-File {
  border: 1px solid black;
}
</style>