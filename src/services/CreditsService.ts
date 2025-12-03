/**
 * 积分服务
 *
 * 封装所有积分相关的 API 调用
 */
import { ApiAdapter } from './ApiAdapter';
import type {
  BalanceInfo,
  CreditTransaction,
  RedeemResponse,
  TransactionType,
} from '../types/credits';

/**
 * 交易记录列表响应
 */
export interface TransactionListResponse {
  /** 数据项 */
  items: CreditTransaction[];
  /** 总数 */
  total: number;
  /** 当前页码 */
  page: number;
  /** 每页数量 */
  pageSize: number;
  /** 总页数 */
  totalPages: number;
}

/**
 * 积分服务
 */
export class CreditsService {
  private static adapter = new ApiAdapter();

  /**
   * 获取余额信息
   */
  static async getBalance(): Promise<BalanceInfo> {
    return this.adapter.get<BalanceInfo>('/credits/balance');
  }

  /**
   * 获取交易记录
   *
   * 注意: GET 请求的 params 参数使用 snake_case
   */
  static async getTransactions(params?: {
    page?: number;
    page_size?: number;
    type?: TransactionType;
    start_date?: string;
    end_date?: string;
  }): Promise<TransactionListResponse> {
    return this.adapter.get<TransactionListResponse>('/credits/transactions', params);
  }

  /**
   * 兑换积分
   */
  static async redeem(code: string): Promise<RedeemResponse> {
    return this.adapter.post<RedeemResponse>('/credits/redeem', { code });
  }
}
