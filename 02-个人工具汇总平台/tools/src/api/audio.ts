// 音频处理相关接口
import request from "@/utils/request";

const API = {
  FORMAT_TRANSFORM: "/audio/fileFormateTransform"
}

export function fileFormatTransform(params: any) {
  return request<any, any>({
    method: "POST",
    url: API.FORMAT_TRANSFORM,
    data: params,
    responseType: 'blob',
  });
}