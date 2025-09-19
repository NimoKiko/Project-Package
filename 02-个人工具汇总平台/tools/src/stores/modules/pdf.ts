// 登录相关 状态管理
import { defineStore } from "pinia";
import {
  mergePdf,
  reversePdf
} from "@/api/pdf.ts";
// import { ElMessage } from "element-plus";


export const usePDFStore = defineStore("PDF", {
  state() {
    return {
    };
  },
  actions: {
    // 按照文件的奇偶数页面 穿插合并文件
    mergePDF(params: any) {
      let p = mergePdf(params)
      return p
    },
    // 按照文件的奇偶数页面 穿插合并文件
    reversePDF(params: any) {
      let p = reversePdf(params)
      return p
    },
  },
  getters: {},
});
