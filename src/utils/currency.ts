/**
 * 货币汇率工具函数
 *
 * 用于将美元金额转换为人民币显示
 * 汇率基于 2025-01-10 中国人民银行官方汇率
 */

/**
 * 美元到人民币汇率常量
 * 1 USD = 7.19 CNY (2025-01-10)
 */
export const USD_TO_CNY_RATE = 7.19;

/**
 * 将美元转换为人民币
 * @param usd - 美元金额
 * @returns 人民币金额（不格式化）
 */
export function usdToCny(usd: number): number {
  return usd * USD_TO_CNY_RATE;
}

/**
 * 将美元转换为人民币并格式化显示
 * @param usd - 美元金额
 * @param decimals - 保留小数位数（默认2位）
 * @returns 格式化后的人民币字符串，如 "¥7.19"
 */
export function formatUsdToCny(usd: number, decimals: number = 2): string {
  const cny = usdToCny(usd);
  return `¥${cny.toFixed(decimals)}`;
}

/**
 * 同时显示美元和人民币
 * @param usd - 美元金额
 * @returns 双币种显示字符串，如 "$1.00 (¥7.19)"
 */
export function formatCostDual(usd: number): string {
  const cny = usdToCny(usd);
  return `$${usd.toFixed(2)} (¥${cny.toFixed(2)})`;
}
