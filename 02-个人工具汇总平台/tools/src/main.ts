import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
// 导入pinia状态管理
import pinia from "./stores";
// 导入路由
import router from './router'
// 导入element-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css' // 引入样式
import * as ElementPlusIconsVue from '@element-plus/icons-vue' // 
// 引入element汉化
import zhCn from "element-plus/es/locale/lang/zh-cn";
// 引入axios
import axios from 'axios';

import { SET_BASE_URL } from './utils/URL';

const app = createApp(App)

// 注册全局图标（可选）
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 使用element-plus
app.use(ElementPlus, {
  locale: zhCn,
});

// 使用pinia
app.use(pinia)
// 使用router
app.use(router)

// 设置axios的基础URL
let getUrl = function () {
  axios.get("/config.json").then((res) => {
    SET_BASE_URL(res.data.BASE_URL);
  });
};

getUrl(); // 调用函数设置基础URL

app.mount('#app')
