// 保存token
export function SAVE_TOKEN(token: any) {
  localStorage.setItem("TOKEN", JSON.stringify(token));
}

// 获取token
export function GET_TOKEN() {
  return JSON.parse(localStorage.getItem("TOKEN")!);
}
