// 登录相关 状态管理
import { defineStore } from "pinia";
import {
  fileFormatTransform
} from "@/api/audio.ts";
// import { ElMessage } from "element-plus";


export const useAudioStore = defineStore("Audio", {
  state() {
    return {
      fileFormatTransform(params: any) {
        let p = fileFormatTransform(params)
        return p
      }
    };
  },
  actions: {},
  getters: {},
});
