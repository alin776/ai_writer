import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { User } from '@/types';

/**
 * 检查是否是配额超限错误
 */
const isQuotaExceeded = (error: unknown) => {
  if (!error || typeof error !== 'object') return false;
  const name = (error as { name?: string }).name;
  return name === 'QuotaExceededError' || name === 'NS_ERROR_DOM_QUOTA_REACHED';
};

/**
 * 安全的 localStorage 包装器
 * 处理配额超限等异常情况
 */
const safeStorage = {
  getItem: (name: string) => {
    try {
      return localStorage.getItem(name);
    } catch (error) {
      console.error('[authStore] localStorage 读取失败:', error);
      return null;
    }
  },
  setItem: (name: string, value: string) => {
    try {
      localStorage.setItem(name, value);
    } catch (error) {
      if (isQuotaExceeded(error)) {
        console.warn('[authStore] localStorage 配额超限，尝试清理后重试');
        try {
          // 尝试清除当前 key 后重新写入
          localStorage.removeItem(name);
          localStorage.setItem(name, value);
          return;
        } catch (retryError) {
          console.error('[authStore] localStorage 配额不足，认证信息无法持久化:', retryError);
          // 显示用户友好的错误提示
          if (typeof window !== 'undefined') {
            window.dispatchEvent(
              new CustomEvent('storage-quota-exceeded', {
                detail: { store: 'auth', message: '存储空间不足，请清理浏览器缓存' },
              })
            );
          }
          return;
        }
      }
      console.error('[authStore] localStorage 写入失败:', error);
    }
  },
  removeItem: (name: string) => {
    try {
      localStorage.removeItem(name);
    } catch (error) {
      console.error('[authStore] localStorage 删除失败:', error);
    }
  },
};

/**
 * 用户在线状态类型
 */
export type OnlineStatus = 'online' | 'idle' | 'dnd' | 'offline';

/**
 * 认证状态接口
 */
interface AuthState {
  // 状态
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  tokenExpiresAt: number | null;  // access token 过期时间戳（毫秒）
  refreshTokenExpiresAt: number | null;  // refresh token 过期时间戳（毫秒）
  isAuthenticated: boolean;
  hasHydrated: boolean;
  onlineStatus: OnlineStatus;  // 用户在线状态

  // 方法
  /**
   * 登录
   * @param user 用户信息
   * @param token 认证令牌
   * @param refreshToken 刷新令牌
   * @param tokenExpiresAt access token 过期时间戳（毫秒，可选）
   * @param refreshTokenExpiresAt refresh token 过期时间戳（毫秒，可选）
   */
  login: (
    user: User | null,
    token: string,
    refreshToken?: string | null,
    tokenExpiresAt?: number | null,
    refreshTokenExpiresAt?: number | null
  ) => void;

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

  /**
   * 设置用户在线状态
   * @param status 在线状态
   */
  setOnlineStatus: (status: OnlineStatus) => void;
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
      tokenExpiresAt: null,
      refreshTokenExpiresAt: null,
      isAuthenticated: false,
      hasHydrated: false,
      onlineStatus: 'online' as OnlineStatus,

      // 登录方法
      login: (
        user: User | null,
        token: string,
        refreshToken: string | null = null,
        tokenExpiresAt: number | null = null,
        refreshTokenExpiresAt: number | null = null
      ) => {
        // 从后端用户数据同步 onlineStatus，如果没有则默认为 'online'
        const userOnlineStatus = (user?.onlineStatus as OnlineStatus) || 'online';
        set({
          user,
          token,
          refreshToken,
          tokenExpiresAt,
          refreshTokenExpiresAt,
          isAuthenticated: true,
          onlineStatus: userOnlineStatus,
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
          tokenExpiresAt: null,
          refreshTokenExpiresAt: null,
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

      // 设置用户在线状态
      setOnlineStatus: (status: OnlineStatus) => {
        set({ onlineStatus: status });
      },
    }),
    {
      name: 'auth-storage', // localStorage 中的 key
      storage: createJSONStorage(() => safeStorage), // 使用安全的 localStorage 包装器
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        refreshToken: state.refreshToken,
        tokenExpiresAt: state.tokenExpiresAt,
        refreshTokenExpiresAt: state.refreshTokenExpiresAt,
        isAuthenticated: state.isAuthenticated,
        onlineStatus: state.onlineStatus,
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
