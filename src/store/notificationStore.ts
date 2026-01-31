/**
 * 通知系统状态管理
 *
 * 使用 Zustand 管理通知状态和 WebSocket 连接
 */

import { create } from 'zustand';
import type {
  UserNotification,
  WebSocketNotificationMessage,
} from '../types/notification';
import {
  getUserNotifications,
  getUnreadCount,
  markNotificationsAsRead,
  dismissNotification,
  clickActionButton,
} from '../services/notificationApi';

interface NotificationState {
  // 状态
  notifications: UserNotification[];
  unreadCount: number;
  isLoading: boolean;
  error: string | null;

  // WebSocket
  ws: WebSocket | null;
  isConnected: boolean;

  // 方法
  fetchNotifications: (params?: { isRead?: boolean; displayType?: string }) => Promise<void>;
  fetchUnreadCount: () => Promise<void>;
  markAsRead: (notificationIds?: string[]) => Promise<void>;
  markAllAsRead: () => Promise<void>;
  dismiss: (notificationId: string) => Promise<void>;
  clickAction: (notificationId: string) => Promise<void>;

  // WebSocket 方法
  connectWebSocket: (userId: string) => void;
  disconnectWebSocket: () => void;

  // 内部方法
  addNotification: (notification: UserNotification) => void;
  updateUnreadCount: (count: number) => void;
  updateNotificationList: (notifications: UserNotification[]) => void;
}

export const useNotificationStore = create<NotificationState>((set, get) => ({
  // 初始状态
  notifications: [],
  unreadCount: 0,
  isLoading: false,
  error: null,
  ws: null,
  isConnected: false,

  // 获取通知列表
  fetchNotifications: async (params) => {
    set({ isLoading: true, error: null });
    try {
      const response = await getUserNotifications({
        page: 1,
        pageSize: 50,
        ...params,
      });
      set({
        notifications: response.items,
        unreadCount: response.unreadCount,
        isLoading: false,
      });
    } catch (error: any) {
      set({
        error: error.message || '获取通知失败',
        isLoading: false,
      });
    }
  },

  // 获取未读数量
  fetchUnreadCount: async () => {
    try {
      const count = await getUnreadCount();
      set({ unreadCount: count });
    } catch (error: any) {
      console.error('获取未读数量失败:', error);
    }
  },

  // 标记为已读
  markAsRead: async (notificationIds) => {
    try {
      await markNotificationsAsRead(notificationIds);

      // 更新本地状态
      const { notifications } = get();
      const updatedNotifications = notifications.map((notif) => {
        if (!notificationIds || notificationIds.includes(notif.id)) {
          return { ...notif, isRead: true, readAt: new Date().toISOString() };
        }
        return notif;
      });

      const newUnreadCount = updatedNotifications.filter((n) => !n.isRead).length;
      set({ notifications: updatedNotifications, unreadCount: newUnreadCount });
    } catch (error: any) {
      console.error('标记已读失败:', error);
    }
  },

  // 全部标记为已读
  markAllAsRead: async () => {
    try {
      await markNotificationsAsRead();

      // 更新本地状态
      const { notifications } = get();
      const updatedNotifications = notifications.map((notif) => ({
        ...notif,
        isRead: true,
        readAt: new Date().toISOString(),
      }));

      set({ notifications: updatedNotifications, unreadCount: 0 });
    } catch (error: any) {
      console.error('全部标记已读失败:', error);
    }
  },

  // 关闭通知弹窗
  dismiss: async (notificationId) => {
    try {
      await dismissNotification(notificationId);

      // 更新本地状态
      const { notifications } = get();
      const updatedNotifications = notifications.map((notif) => {
        if (notif.id === notificationId) {
          return { ...notif, isDismissed: true, dismissedAt: new Date().toISOString() };
        }
        return notif;
      });

      set({ notifications: updatedNotifications });
    } catch (error: any) {
      console.error('关闭通知失败:', error);
    }
  },

  // 点击行动按钮
  clickAction: async (notificationId) => {
    try {
      await clickActionButton(notificationId);

      // 更新本地状态
      const { notifications } = get();
      const updatedNotifications = notifications.map((notif) => {
        if (notif.id === notificationId) {
          return {
            ...notif,
            clicked: true,
            clickedAt: new Date().toISOString(),
            isRead: true,
            readAt: new Date().toISOString(),
          };
        }
        return notif;
      });

      const newUnreadCount = updatedNotifications.filter((n) => !n.isRead).length;
      set({ notifications: updatedNotifications, unreadCount: newUnreadCount });
    } catch (error: any) {
      console.error('点击行动按钮失败:', error);
    }
  },

  // 连接 WebSocket
  connectWebSocket: (userId: string) => {
    const { ws, isConnected } = get();

    // 如果已连接，先断开
    if (ws && isConnected) {
      ws.close();
    }

    try {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}/api/v1/ws/notifications/${userId}`;

      const newWs = new WebSocket(wsUrl);

      newWs.onopen = () => {
        console.log('[WebSocket] 通知连接已建立');
        set({ isConnected: true });
      };

      newWs.onmessage = (event) => {
        try {
          const message: WebSocketNotificationMessage = JSON.parse(event.data);

          switch (message.type) {
            case 'notification':
              // 收到新通知
              if (message.data) {
                get().addNotification(message.data);
              }
              break;

            case 'unread_count':
              // 更新未读数量
              if (message.data && typeof message.data.count === 'number') {
                get().updateUnreadCount(message.data.count);
              }
              break;

            case 'notifications_list':
              // 更新通知列表
              if (message.data && Array.isArray(message.data.notifications)) {
                get().updateNotificationList(message.data.notifications);
              }
              break;

            case 'heartbeat':
              // 心跳，无需处理
              break;

            case 'pong':
              // Pong 响应，无需处理
              break;

            case 'error':
              console.error('[WebSocket] 错误:', message.message);
              break;

            default:
              console.warn('[WebSocket] 未知消息类型:', message.type);
          }
        } catch (error) {
          console.error('[WebSocket] 解析消息失败:', error);
        }
      };

      newWs.onerror = (error) => {
        console.error('[WebSocket] 连接错误:', error);
        set({ isConnected: false });
      };

      newWs.onclose = () => {
        console.log('[WebSocket] 连接已关闭');
        set({ isConnected: false, ws: null });

        // 5秒后尝试重连
        setTimeout(() => {
          const { ws } = get();
          if (!ws || ws.readyState === WebSocket.CLOSED) {
            console.log('[WebSocket] 尝试重新连接...');
            get().connectWebSocket(userId);
          }
        }, 5000);
      };

      set({ ws: newWs });

      // 定期发送心跳（每25秒）
      const heartbeatInterval = setInterval(() => {
        if (newWs.readyState === WebSocket.OPEN) {
          newWs.send(JSON.stringify({ type: 'ping' }));
        } else {
          clearInterval(heartbeatInterval);
        }
      }, 25000);

    } catch (error) {
      console.error('[WebSocket] 创建连接失败:', error);
      set({ isConnected: false });
    }
  },

  // 断开 WebSocket
  disconnectWebSocket: () => {
    const { ws } = get();
    if (ws) {
      ws.close();
      set({ ws: null, isConnected: false });
    }
  },

  // 添加新通知到列表
  addNotification: (notification: UserNotification) => {
    const { notifications, unreadCount } = get();

    // 检查是否已存在
    const exists = notifications.some((n) => n.id === notification.id);
    if (!exists) {
      set({
        notifications: [notification, ...notifications],
        unreadCount: notification.isRead ? unreadCount : unreadCount + 1,
      });
    }
  },

  // 更新未读数量
  updateUnreadCount: (count: number) => {
    set({ unreadCount: count });
  },

  // 更新通知列表
  updateNotificationList: (notifications: UserNotification[]) => {
    const currentNotifications = get().notifications;

    // 合并新通知（避免重复）
    const mergedNotifications = [...notifications];
    currentNotifications.forEach((current) => {
      if (!notifications.some((n) => n.id === current.id)) {
        mergedNotifications.push(current);
      }
    });

    // 按创建时间排序
    mergedNotifications.sort((a, b) =>
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );

    set({ notifications: mergedNotifications });
  },
}));
