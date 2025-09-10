<template>
  <div id="Home">
    <el-container>
      <el-header>
        <Header></Header>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <Side></Side>
        </el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
// Composition API with TypeScript
import { onMounted } from 'vue'
import Header from '../components/common/Header.vue'
import Side from '../components/common/Side.vue'

// Lifecycle hook
onMounted(() => {
  console.log('Component mounted')
})

// Methods
</script>

<style scoped lang="scss">
@use "@/assets/scss/variable.scss" as vars;
#Home {
  .el-container {
    height: 100vh;
    /* Full viewport height */
  }

  .el-header {
    padding: 0;
    height: vars.$header-height;
    /* Adjust based on your header height */
  }

  .el-aside {
    height: 100%;
  }


}
</style>