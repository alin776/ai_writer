/**
 * 管理员积分服务
 *
 * 封装所有管理员积分相关的 API 调用
 */
import { ApiAdapter } from './ApiAdapter';

/**
 * 生成兑换码请求
 */
export interface GenerateCodesRequest {
  /** 生成数量 (1-100) */
  count: number;
  /** 每个兑换码的积分数 */
  credits: number;
  /** 有效期天数 (可选) */
  expires_days?: number;
  /** 备注信息 (可选) */
  remark?: string;
}

/**
 * 兑换码信息
 */
export interface RedeemCodeInfo {
  /** ID */
  id: string;
  /** 兑换码 */
  code: string;
  /** 积分数 */
  credits: number;
  /** 是否已使用 */
  is_used: boolean;
  /** 使用者ID (可选) */
  used_by?: string;
  /** 使用时间 (可选) */
  used_at?: string;
  /** 过期时间 (可选) */
  expires_at?: string;
  /** 创建者 */
  creator_username?: string;
  /** 备注 */
  remark?: string;
  /** 创建时间 */
  created_at: string;
}

/**
 * 兑换码列表响应
 */
export interface RedeemCodesListResponse {
  /** 数据项 */
  items: RedeemCodeInfo[];
  /** 总数 */
  total: number;
  /** 当前页码 */
  page: number;
  /** 每页数量 */
  page_size: number;
  /** 总页数 */
  total_pages: number;
}

/**
 * 生成兑换码响应
 */
export interface GenerateCodesResponse {
  /** 兑换码列表 */
  codes: RedeemCodeInfo[];
  /** 生成数量 */
  count: number;
}

/**
 * 赠送积分请求
 */
export interface GiftCreditsRequest {
  /** 用户ID */
  user_id: string;
  /** 积分数 */
  amount: number;
  /** 描述信息 */
  description: string;
}

/**
 * 赠送积分响应
 */
export interface GiftCreditsResponse {
  /** 是否成功 */
  success: boolean;
  /** 消息 */
  message: string;
  /** 交易ID */
  transaction_id: string;
}

/**
 * 统计信息
 */
export interface AdminCreditsStats {
  /** 兑换码总数 */
  total_codes: number;
  /** 已使用兑换码数 */
  used_codes: number;
  /** 未使用兑换码数 */
  unused_codes: number;
  /** 已过期兑换码数 */
  expired_codes: number;
  /** 总积分发放量 */
  total_credits_issued: number;
  /** 总积分使用量 */
  total_credits_used: number;
}

/**
 * 管理员积分服务
 */
export class AdminCreditsService {
  private static adapter = new ApiAdapter();

  /**
   * 批量生成兑换码
   */
  static async generateCodes(request: GenerateCodesRequest): Promise<GenerateCodesResponse> {
    return this.adapter.post<GenerateCodesResponse>('/admin/credits/codes/generate', request);
  }

  /**
   * 查询兑换码列表
   */
  static async listCodes(params?: {
    page?: number;
    page_size?: number;
    is_used?: boolean;
    search?: string;
  }): Promise<RedeemCodesListResponse> {
    return this.adapter.get<RedeemCodesListResponse>('/admin/credits/codes', params);
  }

  /**
   * 删除兑换码
   */
  static async deleteCode(codeId: string): Promise<{ success: boolean; message: string }> {
    return this.adapter.delete(`/admin/credits/codes/${codeId}`);
  }

  /**
   * 赠送积分给用户
   */
  static async giftCredits(request: GiftCreditsRequest): Promise<GiftCreditsResponse> {
    return this.adapter.post<GiftCreditsResponse>('/admin/credits/gift', request);
  }

  /**
   * 获取统计信息
   */
  static async getStats(): Promise<AdminCreditsStats> {
    return this.adapter.get<AdminCreditsStats>('/admin/credits/stats');
  }
}
