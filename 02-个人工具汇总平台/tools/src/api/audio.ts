// 音频处理相关接口
import request from "@/utils/request";

const API = {
  FORMAT_TRANSFORM: "/audio/fileFormateTransform",
  EXTRACT_AUDIO: "/audio/extractAudio"
}

export function fileFormatTransform(params: any) {
  return request<any, any>({
    method: "POST",
    url: API.FORMAT_TRANSFORM,
    data: params,
    responseType: 'blob',
  });
}

export function extractAudio(params: any) {
  return request<any, any>({
    method: "POST",
    url: API.EXTRACT_AUDIO,
    data: params,
    responseType: 'blob',
  });
}