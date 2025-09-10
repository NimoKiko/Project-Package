import axios from "axios";
import { GET_BASE_URL } from "./URL";
// import { GET_TOKEN } from "./token";
import router from "../router";
import { ElMessage } from "element-plus";
import { ElLoading } from "element-plus";

const request = axios.create({
  baseURL: GET_BASE_URL()!,
  timeout: 100000,
});

let loadingNum = 0;
let loading: any = null;
function startLoading() {
  if (loadingNum === 0) {
    loading = ElLoading.service({
      lock: true,
      text: "拼命加载中...",
      background: "rgba(255,255,255,0.5)",
    });
  }
  loadingNum++;
}

function endLoading() {
  if (loadingNum === 1) {
    loading.close();
  }
  loadingNum--;
}

// 请求拦截器
request.interceptors.request.use((config) => {
  //2.比如发送网络请求时，显示一个请求中的图标
  startLoading();

  // 配置token
  // let token = GET_TOKEN();
  // if (token) {
  //   config.headers["Authorization"] = `Bearer ${token}`;
  // }
  // if (config.method == "post") {
  //   // config.headers["Content-Type"] = "application/x-www-form-urlencoded";
  //   config.headers["Content-Type"] = " application/json";
  // }

  return config;
});

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    endLoading();
    // 简化数据

    return response.data;
  },
  (err) => {
    
    // 定义一个变量：存储网络错误信息
    let message = "";
    // http状态码
    let status = err.response.status;
    switch (status) {
      case 401:
        message = "用户信息过期，请重新登录";
        router.push("/");
        break;
      case 403:
        message = "你无权访问";
        break;
      case 404:
        message = "请求地址错误";
        break;
      case 500:
        message = "服务器出现问题";
        break;
      default:
        message = "网络出现问题";
        break;
    }

    // 提示错误信息
    ElMessage({
      type: "error",
      message
    });
    endLoading();

    return Promise.reject(err);
  }
);

// 对外暴露
export default request;
