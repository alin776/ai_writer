/**
 * 积分系统类型定义
 *
 * 包含余额信息、交易记录、兑换码等相关类型
 */

// ============================================
// 用户简要信息
// ============================================
export interface UserBrief {
  id: string;
  username: string;
}

// ============================================
// 余额信息
// ============================================
export interface BalanceInfo {
  /** 当前余额 */
  balance: number;
  /** 累计充值 */
  totalRecharged: number;
  /** 累计消耗 */
  totalConsumed: number;
  /** 累计赠送 */
  totalGifted: number;
  /** 过期时间 (null表示永不过期) */
  expiresAt: string | null;
  /** 是否已过期 */
  isExpired: boolean;
}

// ============================================
// 交易记录
// ============================================
export type TransactionType = 'recharge' | 'consume' | 'gift' | 'expire' | 'refund';

export interface CreditTransaction {
  /** 交易ID */
  id: string;
  /** 交易类型 */
  type: TransactionType;
  /** 交易金额 */
  amount: number;
  /** 交易前余额 */
  balanceBefore: number;
  /** 交易后余额 */
  balanceAfter: number;
  /** 描述信息 */
  description: string | null;
  /** 关联类型 (如: ai_call, redeem_code等) */
  relatedType: string | null;
  /** 关联ID */
  relatedId: string | null;
  /** 创建时间 */
  createdAt: string;
}

// ============================================
// 兑换码
// ============================================
export interface RedeemCode {
  /** 兑换码ID */
  id: string;
  /** 兑换码 */
  code: string;
  /** 积分数量 */
  credits: number;
  /** 是否已使用 */
  isUsed: boolean;
  /** 使用者信息 */
  usedBy: UserBrief | null;
  /** 使用时间 */
  usedAt: string | null;
  /** 过期时间 */
  expiresAt: string | null;
  /** 是否已过期 */
  isExpired: boolean;
  /** 创建者信息 */
  createdBy: UserBrief | null;
  /** 备注 */
  remark: string | null;
  /** 创建时间 */
  createdAt: string;
}

// ============================================
// 兑换请求和响应
// ============================================
export interface RedeemRequest {
  /** 兑换码 */
  code: string;
}

export interface RedeemResponse {
  /** 兑换的积分数 */
  credits: number;
  /** 兑换前余额 */
  balanceBefore: number;
  /** 兑换后余额 */
  balanceAfter: number;
}

// ============================================
// 生成兑换码请求 (管理端)
// ============================================
export interface GenerateCodesRequest {
  /** 生成数量 */
  count: number;
  /** 每张积分数 */
  credits: number;
  /** 有效期(天数), 不传表示使用默认值 */
  expiresDays?: number;
  /** 备注 */
  remark?: string;
}

export interface GenerateCodesResponse {
  /** 生成的兑换码列表 */
  codes: RedeemCode[];
}

// ============================================
// 分页响应
// ============================================
export interface PaginatedResponse<T> {
  /** 数据项 */
  items: T[];
  /** 总数 */
  total: number;
  /** 当前页码 (1-based) */
  page: number;
  /** 每页数量 */
  pageSize: number;
  /** 总页数 */
  totalPages: number;
}

// ============================================
// 查询参数
// ============================================
export interface TransactionQueryParams {
  /** 页码 */
  page?: number;
  /** 每页数量 */
  pageSize?: number;
  /** 交易类型 */
  type?: TransactionType;
  /** 开始日期 */
  startDate?: string;
  /** 结束日期 */
  endDate?: string;
}

export interface RedeemCodeQueryParams {
  /** 页码 */
  page?: number;
  /** 每页数量 */
  pageSize?: number;
  /** 是否已使用 */
  isUsed?: boolean;
  /** 是否已过期 */
  isExpired?: boolean;
  /** 创建者ID */
  createdById?: string;
}

// ============================================
// 交易类型显示配置
// ============================================
export interface TransactionTypeConfig {
  /** 显示文本 */
  label: string;
  /** 颜色类名 */
  color: string;
  /** 图标 */
  icon: string;
}

export const TRANSACTION_TYPE_CONFIG: Record<TransactionType, TransactionTypeConfig> = {
  recharge: {
    label: '充值',
    color: 'text-green-600 bg-green-50',
    icon: '💰',
  },
  consume: {
    label: '消费',
    color: 'text-red-600 bg-red-50',
    icon: '💸',
  },
  gift: {
    label: '赠送',
    color: 'text-blue-600 bg-blue-50',
    icon: '🎁',
  },
  expire: {
    label: '过期',
    color: 'text-gray-600 bg-gray-50',
    icon: '⏰',
  },
  refund: {
    label: '退款',
    color: 'text-purple-600 bg-purple-50',
    icon: '↩️',
  },
};

// ============================================
// AI操作类型友好名称映射
// ============================================
/**
 * 将后端 TaskType 技术术语转换为用户友好的中文描述
 */
export const AI_OPERATION_LABELS: Record<string, string> = {
  // 简单任务
  'quality_evaluation': '质量评估',
  'text_classification': '文本分类',
  'simple_qa': '智能问答',
  'keyword_extraction': '关键词提取',
  'humanize_detect': 'AI检测',
  'humanize_verify': '去痕验证',
  // 中等任务
  'text_polish': '文本润色',
  'text_expansion': '文本扩写',
  'summarization': '内容总结',
  'translation': '翻译',
  // 复杂任务
  'content_creation': '内容创作',
  'humanize_rewrite': '人性化改写',
  'story_planning': '故事规划',
  'character_design': '角色设计',
  'world_building': '世界观构建',
  'deep_analysis': '深度分析',
  // 通用
  'unknown': 'AI服务',
};

/**
 * 格式化交易描述，隐藏技术细节
 * @example "AI调用: simple_qa" -> "智能问答"
 * @example "AI调用: content_creation" -> "内容创作"
 */
export function formatTransactionDescription(description: string | null): string {
  if (!description) return '';

  // 匹配 "AI调用: xxx" 或 "AI调用：xxx" 格式
  const match = description.match(/^AI调用[：:]\s*(.+)$/);
  if (match) {
    const taskType = match[1].trim();
    return AI_OPERATION_LABELS[taskType] || 'AI服务';
  }

  // 其他描述保持原样（充值、赠送等）
  return description;
}
