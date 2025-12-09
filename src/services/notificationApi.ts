/**
 * 通知系统 API 服务
 */

import { ApiAdapter } from './ApiAdapter';
import type {
  UserNotification,
  UserNotificationListResponse,
  Notification,
  NotificationListResponse,
  NotificationStats,
  CreateNotificationRequest,
  UpdateNotificationRequest,
  MarkReadRequest,
  BatchOperationResponse,
  NotificationCategory,
  NotificationType,
  NotificationStatus,
} from '../types/notification';

const api = new ApiAdapter();

// ==================== 用户端 API ====================

/**
 * 获取当前用户的通知列表
 */
export const getUserNotifications = async (params: {
  page?: number;
  pageSize?: number;
  isRead?: boolean;
  displayType?: string;
}): Promise<UserNotificationListResponse> => {
  // ApiAdapter.get() 直接返回转换后的数据，不需要解构 data
  const data = await api.get<UserNotificationListResponse>(
    '/notifications/user/notifications',
    { params }
  );
  return data;
};

/**
 * 获取未读通知数量
 */
export const getUnreadCount = async (): Promise<number> => {
  const data = await api.get<{ unreadCount: number }>(
    '/notifications/user/notifications/unread-count'
  );
  return data.unreadCount;
};

/**
 * 标记通知为已读
 * @param notificationIds 要标记的通知ID列表，为空则标记全部
 */
export const markNotificationsAsRead = async (
  notificationIds?: string[]
): Promise<BatchOperationResponse> => {
  const data = await api.post<BatchOperationResponse>(
    '/notifications/user/notifications/mark-read',
    { notificationIds }
  );
  return data;
};

/**
 * 关闭通知弹窗
 */
export const dismissNotification = async (
  notificationId: string
): Promise<BatchOperationResponse> => {
  const data = await api.post<BatchOperationResponse>(
    `/notifications/user/notifications/${notificationId}/dismiss`
  );
  return data;
};

/**
 * 记录点击行动按钮
 */
export const clickActionButton = async (
  notificationId: string
): Promise<BatchOperationResponse> => {
  const data = await api.post<BatchOperationResponse>(
    `/notifications/user/notifications/${notificationId}/click`
  );
  return data;
};

// ==================== 管理员 API ====================

/**
 * 创建通知/活动（管理员）
 */
export const createNotification = async (
  notificationData: CreateNotificationRequest
): Promise<Notification> => {
  const data = await api.post<Notification>(
    '/notifications/admin/notifications',
    notificationData
  );
  return data;
};

/**
 * 获取通知列表（管理员）
 */
export const getNotifications = async (params: {
  page?: number;
  pageSize?: number;
  category?: NotificationCategory;
  status?: NotificationStatus;
  type?: NotificationType;
}): Promise<NotificationListResponse> => {
  const data = await api.get<NotificationListResponse>(
    '/notifications/admin/notifications',
    { params }
  );
  return data;
};

/**
 * 获取单个通知详情（管理员）
 */
export const getNotification = async (
  notificationId: string
): Promise<Notification> => {
  const data = await api.get<Notification>(
    `/notifications/admin/notifications/${notificationId}`
  );
  return data;
};

/**
 * 更新通知（管理员）
 */
export const updateNotification = async (
  notificationId: string,
  notificationData: UpdateNotificationRequest
): Promise<Notification> => {
  const data = await api.put<Notification>(
    `/notifications/admin/notifications/${notificationId}`,
    notificationData
  );
  return data;
};

/**
 * 删除通知（管理员）
 */
export const deleteNotification = async (
  notificationId: string
): Promise<void> => {
  await api.delete(`/notifications/admin/notifications/${notificationId}`);
};

/**
 * 发布通知（管理员）
 */
export const publishNotification = async (
  notificationId: string
): Promise<Notification> => {
  const data = await api.post<Notification>(
    `/notifications/admin/notifications/${notificationId}/publish`
  );
  return data;
};

/**
 * 获取通知统计数据（管理员）
 */
export const getNotificationStats = async (
  notificationId: string
): Promise<NotificationStats> => {
  const data = await api.get<NotificationStats>(
    `/notifications/admin/notifications/${notificationId}/stats`
  );
  return data;
};
