import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '@/types';

/**
 * 认证状态接口
 */
interface AuthState {
  // 状态
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  hasHydrated: boolean;

  // 方法
  /**
   * 登录
   * @param user 用户信息
   * @param token 认证令牌
   */
  login: (user: User | null, token: string, refreshToken?: string | null) => void;

  /**
   * 登出
   */
  logout: () => void;

  /**
   * 设置用户信息
   * @param user 用户信息
   */
  setUser: (user: User) => void;

  /**
   * 更新 token
   * @param token 新的认证令牌
   */
  setToken: (token: string) => void;

  /**
   * 更新 refresh token
   * @param refreshToken 新的刷新令牌
   */
  setRefreshToken: (refreshToken: string | null) => void;

  /**
   * 标记持久化是否完成
   */
  setHasHydrated: (value: boolean) => void;
}

/**
 * 认证状态管理 Store
 * 使用 persist 中间件将认证信息持久化到 localStorage
 */
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // 初始状态
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      hasHydrated: false,

      // 登录方法
      login: (user: User | null, token: string, refreshToken: string | null = null) => {
        set({
          user,
          token,
          refreshToken,
          isAuthenticated: true,
        });
      },

      // 登出方法
      logout: () => {
        // 清除活动弹窗标记，确保下次登录时重新显示
        sessionStorage.removeItem('activity_modal_shown');

        set({
          user: null,
          token: null,
          refreshToken: null,
          isAuthenticated: false,
        });
      },

      // 设置用户信息
      setUser: (user: User) => {
        set({ user });
      },

      // 更新 token
      setToken: (token: string) => {
        set({ token });
      },

      // 更新 refresh token
      setRefreshToken: (refreshToken: string | null) => {
        set({ refreshToken });
      },

      // 设置持久化完成标记
      setHasHydrated: (value: boolean) => {
        set({ hasHydrated: value });
      },
    }),
    {
      name: 'auth-storage', // localStorage 中的 key
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }), // 只持久化这些字段
      onRehydrateStorage: () => {
        return (state) => {
          // rehydrate 完成后再进行鉴权判断，避免刷新后立即被重定向
          state?.setHasHydrated?.(true);
        };
      },
    }
  )
);
