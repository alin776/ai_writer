/**
 * AI 成本计算工具
 *
 * 根据 token 使用量和模型定价计算成本
 * 与后端 backend/app/utils/cost_calculator.py 保持一致
 */

import type { AIModel } from '../types';

/**
 * 成本计算结果
 */
export interface CostCalculation {
  inputCost: number;      // 输入成本（美元）
  outputCost: number;     // 输出成本（美元）
  totalCost: number;      // 总成本（美元）
}

/**
 * 计算 AI 调用成本
 *
 * @param model - AI 模型配置
 * @param inputTokens - 输入 token 数量
 * @param outputTokens - 输出 token 数量
 * @returns 成本计算结果（美元）
 *
 * @example
 * ```ts
 * const model = { inputPricePerMillion: 0.30, outputPricePerMillion: 2.50 };
 * const cost = calculateCost(model, 1000, 500);
 * // { inputCost: 0.0003, outputCost: 0.00125, totalCost: 0.00155 }
 * ```
 */
export function calculateCost(
  model: Pick<AIModel, 'inputPricePerMillion' | 'outputPricePerMillion'>,
  inputTokens: number,
  outputTokens: number
): CostCalculation {
  // 计算成本（价格是每百万 token 的美元数）
  const inputCost = (inputTokens / 1_000_000) * model.inputPricePerMillion;
  const outputCost = (outputTokens / 1_000_000) * model.outputPricePerMillion;
  const totalCost = inputCost + outputCost;

  return {
    inputCost,
    outputCost,
    totalCost,
  };
}

/**
 * 格式化成本显示
 *
 * @param cost - 成本金额（美元）
 * @param currency - 货币符号，默认为 '$'
 * @param decimals - 小数位数，默认为 4
 * @returns 格式化后的成本字符串
 *
 * @example
 * ```ts
 * formatCost(0.00155) // '$0.0016'
 * formatCost(0.00155, '¥', 2) // '¥0.00'
 * ```
 */
export function formatCost(
  cost: number,
  currency: string = '$',
  decimals: number = 4
): string {
  return `${currency}${cost.toFixed(decimals)}`;
}

/**
 * 计算典型请求的成本范围
 * 用于在 UI 中显示模型的大致成本
 *
 * @param model - AI 模型配置
 * @param typicalInputTokens - 典型输入 token 数，默认 1000
 * @param typicalOutputTokens - 典型输出 token 数，默认 500
 * @returns 格式化的成本范围字符串
 *
 * @example
 * ```ts
 * const model = { inputPricePerMillion: 0.30, outputPricePerMillion: 2.50 };
 * getTypicalCostRange(model) // '~$0.0016/次'
 * ```
 */
export function getTypicalCostRange(
  model: Pick<AIModel, 'inputPricePerMillion' | 'outputPricePerMillion'>,
  typicalInputTokens: number = 1000,
  typicalOutputTokens: number = 500
): string {
  const { totalCost } = calculateCost(model, typicalInputTokens, typicalOutputTokens);
  return `~${formatCost(totalCost)}/次`;
}

/**
 * 根据模型名称获取官方定价
 * 与后端 PRICING 字典保持一致
 *
 * @param modelName - 模型名称
 * @returns 定价配置，如果未找到则返回 null
 */
export function getOfficialPricing(modelName: string): {
  inputPricePerMillion: number;
  outputPricePerMillion: number;
} | null {
  const PRICING_MAP: Record<string, { inputPricePerMillion: number; outputPricePerMillion: number }> = {
    'gemini-2.5-pro': { inputPricePerMillion: 1.25, outputPricePerMillion: 10.0 },
    'gemini-2.5-flash': { inputPricePerMillion: 0.30, outputPricePerMillion: 2.50 },
    'gemini-2.5-flash-lite': { inputPricePerMillion: 0.10, outputPricePerMillion: 0.40 },
  };

  return PRICING_MAP[modelName] || null;
}
