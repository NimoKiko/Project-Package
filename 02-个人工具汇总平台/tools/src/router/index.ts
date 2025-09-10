// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// 定义路由规则
export const routes = [
  {
    path: '/',
    redirect: "/home"
  },
  {
    path: '/home', // 404 路由
    name: 'home',
    component: () => import('../views/home.vue'), // 懒加载
    children:[
      {
        path:'/audio',
        name:'audio',
        component: () => import("../views/modules/audioFile.vue")
      }
    ]
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(), // 使用 HTML5 模式（无 #）
  routes // 路由规则
})

export default router