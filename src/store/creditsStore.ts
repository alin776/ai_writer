/**
 * 积分状态管理
 */
import { create } from 'zustand';
import { CreditsService, TransactionListResponse } from '../services/CreditsService';
import type { BalanceInfo, CreditTransaction, TransactionType, RedeemResponse } from '../types/credits';

interface CreditsState {
  // 余额信息
  balance: BalanceInfo | null;

  // 交易记录
  transactions: CreditTransaction[];
  transactionTotal: number;
  transactionPage: number;
  transactionPageSize: number;
  transactionTotalPages: number;

  // 加载和错误状态
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchBalance: () => Promise<void>;
  fetchTransactions: (page?: number, pageSize?: number, type?: TransactionType) => Promise<void>;
  redeem: (code: string) => Promise<RedeemResponse>;
  clearError: () => void;
}

export const useCreditsStore = create<CreditsState>((set, get) => ({
  // 初始状态
  balance: null,
  transactions: [],
  transactionTotal: 0,
  transactionPage: 1,
  transactionPageSize: 20,
  transactionTotalPages: 0,
  isLoading: false,
  error: null,

  // 获取余额
  fetchBalance: async () => {
    set({ isLoading: true, error: null });
    try {
      const balance = await CreditsService.getBalance();
      set({ balance, isLoading: false });
    } catch (error: any) {
      set({ error: error?.message || '获取余额失败', isLoading: false });
    }
  },

  // 获取交易记录
  fetchTransactions: async (page = 1, pageSize = 20, type?: TransactionType) => {
    set({ isLoading: true, error: null });
    try {
      const response: TransactionListResponse = await CreditsService.getTransactions({
        page,
        page_size: pageSize,
        type,
      });

      set({
        transactions: response.items,
        transactionTotal: response.total,
        transactionPage: response.page,
        transactionPageSize: response.pageSize,
        transactionTotalPages: response.totalPages,
        isLoading: false,
      });
    } catch (error: any) {
      set({ error: error?.message || '获取交易记录失败', isLoading: false });
    }
  },

  // 兑换积分
  redeem: async (code: string) => {
    set({ isLoading: true, error: null });
    try {
      const result = await CreditsService.redeem(code);
      // 兑换成功后，自动刷新余额
      await get().fetchBalance();
      set({ isLoading: false });
      return result;
    } catch (error: any) {
      // 后端返回 { detail: "错误信息" }
      const errorMsg = error?.detail || error?.message || '兑换失败';
      set({ error: errorMsg, isLoading: false });
      throw error;
    }
  },

  // 清除错误
  clearError: () => set({ error: null }),
}));
