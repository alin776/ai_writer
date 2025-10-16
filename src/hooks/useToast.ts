/**
 * useToast Hook
 * 用于显示 Toast 通知
 */
import { useState, useCallback } from 'react';
import type { ToastMessage, ToastType } from '@/components/ui/Toast';

let toastId = 0;

export interface UseToastReturn {
  messages: ToastMessage[];
  showToast: (
    type: ToastType,
    title: string,
    message?: string,
    duration?: number
  ) => void;
  success: (title: string, message?: string) => void;
  error: (title: string, message?: string) => void;
  warning: (title: string, message?: string) => void;
  info: (title: string, message?: string) => void;
  close: (id: string) => void;
  clearAll: () => void;
}

/**
 * useToast Hook
 */
export function useToast(): UseToastReturn {
  const [messages, setMessages] = useState<ToastMessage[]>([]);

  const showToast = useCallback(
    (type: ToastType, title: string, message?: string, duration?: number) => {
      const id = `toast-${++toastId}`;
      const newMessage: ToastMessage = {
        id,
        type,
        title,
        message,
        duration,
      };

      setMessages((prev) => [...prev, newMessage]);
    },
    []
  );

  const success = useCallback(
    (title: string, message?: string) => {
      showToast('success', title, message);
    },
    [showToast]
  );

  const error = useCallback(
    (title: string, message?: string) => {
      showToast('error', title, message, 5000); // 错误提示显示更久
    },
    [showToast]
  );

  const warning = useCallback(
    (title: string, message?: string) => {
      showToast('warning', title, message);
    },
    [showToast]
  );

  const info = useCallback(
    (title: string, message?: string) => {
      showToast('info', title, message);
    },
    [showToast]
  );

  const close = useCallback((id: string) => {
    setMessages((prev) => prev.filter((msg) => msg.id !== id));
  }, []);

  const clearAll = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    showToast,
    success,
    error,
    warning,
    info,
    close,
    clearAll,
  };
}
