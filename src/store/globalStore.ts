import { create } from 'zustand';

/**
 * Toast 消息类型
 */
export type ToastType = 'success' | 'error' | 'warning' | 'info';

/**
 * Toast 消息接口
 */
export interface Toast {
  id: string;
  type: ToastType;
  message: string;
  duration?: number; // 显示时长（毫秒），默认 3000
}

/**
 * 全局状态接口
 */
interface GlobalState {
  // 状态
  toasts: Toast[];
  isLoading: boolean;
  loadingMessage?: string;

  // 方法
  /**
   * 显示 Toast 消息
   * @param type 消息类型
   * @param message 消息内容
   * @param duration 显示时长（毫秒）
   * @returns Toast ID
   */
  showToast: (
    type: ToastType,
    message: string,
    duration?: number
  ) => string;

  /**
   * 隐藏 Toast 消息
   * @param id Toast ID
   */
  hideToast: (id: string) => void;

  /**
   * 设置全局加载状态
   * @param isLoading 是否加载中
   * @param message 加载提示信息
   */
  setLoading: (isLoading: boolean, message?: string) => void;

  /**
   * 清除所有 Toast 消息
   */
  clearToasts: () => void;

  /**
   * 快捷方法：显示成功消息
   * @param message 消息内容
   * @param duration 显示时长（毫秒）
   */
  success: (message: string, duration?: number) => void;

  /**
   * 快捷方法：显示错误消息
   * @param message 消息内容
   * @param duration 显示时长（毫秒）
   */
  error: (message: string, duration?: number) => void;

  /**
   * 快捷方法：显示警告消息
   * @param message 消息内容
   * @param duration 显示时长（毫秒）
   */
  warning: (message: string, duration?: number) => void;

  /**
   * 快捷方法：显示信息消息
   * @param message 消息内容
   * @param duration 显示时长（毫秒）
   */
  info: (message: string, duration?: number) => void;
}

/**
 * 生成唯一 ID
 */
const generateId = (): string => {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

/**
 * 全局状态管理 Store
 * 管理应用的全局状态，如 Toast 消息、Loading 状态等
 */
export const useGlobalStore = create<GlobalState>((set, get) => ({
  // 初始状态
  toasts: [],
  isLoading: false,
  loadingMessage: undefined,

  // 显示 Toast
  showToast: (type: ToastType, message: string, duration = 3000) => {
    const id = generateId();
    const toast: Toast = {
      id,
      type,
      message,
      duration,
    };

    set((state) => ({
      toasts: [...state.toasts, toast],
    }));

    // 自动隐藏
    if (duration > 0) {
      setTimeout(() => {
        set((state) => ({
          toasts: state.toasts.filter((t) => t.id !== id),
        }));
      }, duration);
    }

    return id;
  },

  // 隐藏 Toast
  hideToast: (id: string) => {
    set((state) => ({
      toasts: state.toasts.filter((toast) => toast.id !== id),
    }));
  },

  // 设置加载状态
  setLoading: (isLoading: boolean, message?: string) => {
    set({
      isLoading,
      loadingMessage: message,
    });
  },

  // 清除所有 Toast
  clearToasts: () => {
    set({ toasts: [] });
  },

  // 快捷方法
  success: (message: string, duration?: number) => {
    get().showToast('success', message, duration);
  },

  error: (message: string, duration?: number) => {
    get().showToast('error', message, duration);
  },

  warning: (message: string, duration?: number) => {
    get().showToast('warning', message, duration);
  },

  info: (message: string, duration?: number) => {
    get().showToast('info', message, duration);
  },
}));
