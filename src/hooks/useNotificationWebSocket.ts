/**
 * WebSocket 连接 Hook
 *
 * 在用户登录后自动连接 WebSocket 接收实时通知
 */

import { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { useNotificationStore } from '../store/notificationStore';
import type { UserNotification } from '../types/notification';
import { NotificationPriority } from '../types/notification';

/**
 * 使用通知 WebSocket
 *
 * @returns showModal - 是否显示弹窗
 * @returns modalNotification - 当前要展示的弹窗通知
 * @returns closeModal - 关闭弹窗的方法
 */
export const useNotificationWebSocket = () => {
  const user = useAuthStore((state) => state.user);
  const { connectWebSocket, disconnectWebSocket } = useNotificationStore();
  const [showModal, setShowModal] = useState(false);
  const [modalNotification, setModalNotification] = useState<UserNotification | null>(null);
  const [pendingModals, setPendingModals] = useState<UserNotification[]>([]);

  // 连接 WebSocket
  useEffect(() => {
    if (user?.id) {
      console.log('[useNotificationWebSocket] 连接 WebSocket...');
      connectWebSocket(user.id);

      return () => {
        console.log('[useNotificationWebSocket] 断开 WebSocket...');
        disconnectWebSocket();
      };
    }
  }, [user?.id, connectWebSocket, disconnectWebSocket]);

  // 监听新通知，判断是否需要弹窗
  useEffect(() => {
    const unsubscribe = useNotificationStore.subscribe((state, prevState) => {
      const notifications = state.notifications;
      const prevNotifications = prevState?.notifications || [];

      // 找出新增的通知
      const newNotifications = notifications.filter(
        (notif) => !prevNotifications.some((prev) => prev.id === notif.id)
      );

      // 过滤出需要弹窗的通知
      const modalNotifications = newNotifications.filter(
        (notif) =>
          notif.displayType?.includes('modal') &&
          !notif.isDismissed &&
          (notif.priority === NotificationPriority.URGENT ||
            notif.priority === NotificationPriority.IMPORTANT)
      );

      if (modalNotifications.length > 0) {
        // 当前没有弹窗则立即展示第一条
        if (!showModal && !modalNotification) {
          setModalNotification(modalNotifications[0]);
          setShowModal(true);

          // 剩余的进入待处理队列
          if (modalNotifications.length > 1) {
            setPendingModals(modalNotifications.slice(1));
          }
        } else {
          // 否则加入待处理队列
          setPendingModals((prev) => [...prev, ...modalNotifications]);
        }
      }
    });

    return unsubscribe;
  }, [showModal, modalNotification]);

  // 关闭弹窗
  const closeModal = () => {
    setShowModal(false);

    // 延迟清理，确保关闭动画完成
    setTimeout(() => {
      setModalNotification(null);

      // 如果有待处理的弹窗，显示下一条
      if (pendingModals.length > 0) {
        setModalNotification(pendingModals[0]);
        setPendingModals(pendingModals.slice(1));
        setShowModal(true);
      }
    }, 300);
  };

  return {
    showModal,
    modalNotification,
    closeModal,
  };
};
