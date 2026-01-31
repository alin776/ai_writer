/**
 * 邀请状态管理
 */
import { create } from 'zustand';
import { InvitationsService } from '../services/InvitationsService';
import type { InvitationStats, InvitationCodeDetail } from '../types/invitations';

interface InvitationsState {
  // 统计信息
  stats: InvitationStats | null;

  // 我的邀请码列表
  myCodes: InvitationCodeDetail[];

  // 加载和错误状态
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchStats: () => Promise<void>;
  fetchMyCodes: () => Promise<void>;
  generateCode: (maxUses?: number, expiresDays?: number) => Promise<InvitationCodeDetail>;
  clearError: () => void;
}

export const useInvitationsStore = create<InvitationsState>((set, get) => ({
  // 初始状态
  stats: null,
  myCodes: [],
  isLoading: false,
  error: null,

  // 获取统计信息
  fetchStats: async () => {
    set({ isLoading: true, error: null });
    try {
      const stats = await InvitationsService.getStats();
      set({ stats, isLoading: false });
    } catch (error: any) {
      set({ error: error?.message || '获取统计信息失败', isLoading: false });
    }
  },

  // 获取我的邀请码
  fetchMyCodes: async () => {
    set({ isLoading: true, error: null });
    try {
      const myCodes = await InvitationsService.getMyCodes();
      set({ myCodes, isLoading: false });
    } catch (error: any) {
      set({ error: error?.message || '获取邀请码列表失败', isLoading: false });
    }
  },

  // 生成新邀请码
  generateCode: async (maxUses?: number, expiresDays?: number) => {
    set({ isLoading: true, error: null });
    try {
      const newCode = await InvitationsService.generate({
        max_uses: maxUses,
        expires_days: expiresDays,
      });

      // 生成成功后，自动刷新列表和统计
      await get().fetchMyCodes();
      await get().fetchStats();

      set({ isLoading: false });
      return newCode;
    } catch (error: any) {
      set({ error: error?.message || '生成邀请码失败', isLoading: false });
      throw error;
    }
  },

  // 清除错误
  clearError: () => set({ error: null }),
}));
