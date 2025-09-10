<template>
  <div id="Side" class="Side">
    <el-menu active-text-color="#ffd04b" background-color="#545c64" class="el-menu-vertical-demo" default-active="2"
      text-color="#fff" router>
      <el-sub-menu index="1">
        <template #title>
          <el-icon>
            <location />
          </el-icon>
          <span>文件转换类型工具</span>
        </template>
         <el-menu-item index="audio">音频文件转换</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
// Composition API with TypeScript
import { onMounted } from 'vue'

// Lifecycle hook
onMounted(() => {
  console.log('Component mounted')
})

// Methods
</script>

<style scoped lang="scss">
.Side {
  // border: 1px solid black;
  height: 100%;
  // background: aquamarine;

  .el-menu{
    height: 100%;
  }
}
</style>