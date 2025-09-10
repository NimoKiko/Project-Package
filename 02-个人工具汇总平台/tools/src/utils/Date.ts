// 时间转换 年月日-时分秒
export function formatDateYMDHMS(date: Date): string {
  date = new Date(date)
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

// 时间转换 年月日
export function formatDateYMD(date: Date): string {
  date = new Date(date)
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
}

// 获取当前时间-1天
export function getYesterday(): string {
  const date = new Date();
  date.setDate(date.getDate() - 1);
  return formatDateYMD(date);
}
// 获取当前日期
export function getToday(): string {
  const date = new Date();
  date.setDate(date.getDate());
  return formatDateYMD(date);
}