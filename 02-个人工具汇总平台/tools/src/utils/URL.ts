// 保存BASE_URL
export function SET_BASE_URL(url:string){
  localStorage.setItem('BASEURL',url)
}
// 获取BASE_URL
export function GET_BASE_URL(){
  return localStorage.getItem('BASEURL')
}