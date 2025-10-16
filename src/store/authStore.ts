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
  isAuthenticated: boolean;

  // 方法
  /**
   * 登录
   * @param user 用户信息
   * @param token 认证令牌
   */
  login: (user: User, token: string) => void;

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
      isAuthenticated: false,

      // 登录方法
      login: (user: User, token: string) => {
        set({
          user,
          token,
          isAuthenticated: true,
        });
      },

      // 登出方法
      logout: () => {
        set({
          user: null,
          token: null,
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
    }),
    {
      name: 'auth-storage', // localStorage 中的 key
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }), // 只持久化这些字段
    }
  )
);
