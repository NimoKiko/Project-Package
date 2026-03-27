// pdf处理相关接口
import request from "@/utils/request";

const API = {
  MERGE_PDF: "/pdf/mergePdf",
  REVERSE_PDF: "/pdf/reversePdf",
  UNLOCK_PDF: "/pdf/unlockPdf"
}

// 按照文件的奇偶数页面 穿插合并文件
export function mergePdf(params: any) {
  return request<any, any>({
    method: "POST",
    url: API.MERGE_PDF,
    data: params,
    responseType: 'blob',
  });
}

// 逆序排列pdf文件
export function reversePdf(params: any) {
  return request<any, any>({
    method: "POST",
    url: API.REVERSE_PDF,
    data: params,
    responseType: 'blob',
  });
}

// 移除PDF权限限制
export function unlockPdf(params: any) {
  return request<any, any>({
    method: "POST",
    url: API.UNLOCK_PDF,
    data: params,
    responseType: 'blob',
  });
}