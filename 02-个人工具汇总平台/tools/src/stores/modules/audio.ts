// 登录相关 状态管理
import { defineStore } from "pinia";
import {
  fileFormatTransform,
  extractAudio
} from "@/api/audio.ts";
// import { ElMessage } from "element-plus";


export const useAudioStore = defineStore("Audio", {
  state() {
    return {
      fileFormatTransform(params: any) {
        let p = fileFormatTransform(params)
        return p
      },
      extractAudio(params: any) {
        let p = extractAudio(params)
        return p
      }
    };
  },
  actions: {},
  getters: {},
});
