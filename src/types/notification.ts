/**
 * 通知系统 - TypeScript 类型定义
 */

// ==================== 枚举类型 ====================

/**
 * 通知分类
 */
export enum NotificationCategory {
  SYSTEM = 'system',           // 系统自动通知
  ANNOUNCEMENT = 'announcement' // 运营通知/活动
}

/**
 * 通知类型
 */
export enum NotificationType {
  // 系统通知类型
  AI_TASK_COMPLETED = 'ai_task_completed',   // AI任务完成
  ANALYSIS_READY = 'analysis_ready',         // 分析报告生成
  SMART_REMINDER = 'smart_reminder',         // 智能提醒
  MILESTONE = 'milestone',                   // 里程碑达成
  INACTIVITY_ALERT = 'inactivity_alert',     // 灵感保鲜提醒

  // 运营通知类型
  EVENT = 'event',                           // 活动
  FEATURE = 'feature',                       // 新功能上线
  ANNOUNCEMENT = 'announcement',             // 公告
  MAINTENANCE = 'maintenance'                // 系统维护
}

/**
 * 通知优先级
 */
export enum NotificationPriority {
  URGENT = 'urgent',       // 紧急（Banner + 弹窗）
  IMPORTANT = 'important', // 重要（弹窗）
  NORMAL = 'normal'        // 普通（仅通知列表）
}

/**
 * 通知状态
 */
export enum NotificationStatus {
  DRAFT = 'draft',         // 草稿
  SCHEDULED = 'scheduled', // 已定时
  ACTIVE = 'active',       // 进行中
  EXPIRED = 'expired'      // 已过期
}

/**
 * 目标用户类型
 */
export enum TargetUserType {
  ALL = 'all',           // 全部用户
  ACTIVE = 'active',     // 活跃用户
  INACTIVE = 'inactive', // 不活跃用户
  CUSTOM = 'custom'      // 自定义用户列表
}

// ==================== 接口类型 ====================

/**
 * 行动按钮
 */
export interface ActionButton {
  text: string;  // 按钮文字
  url: string;   // 跳转链接
}

/**
 * 通知基础接口
 */
export interface NotificationBase {
  id: string;
  title: string;
  content?: string;
  coverImageUrl?: string;

  category: NotificationCategory;
  type: NotificationType;
  priority: NotificationPriority;

  displayType: string[];  // ['modal', 'banner', 'notification']
  actionButton?: ActionButton;
  bannerColor?: string;

  createdAt: string;
  publishedAt?: string;
  validFrom?: string;
  validUntil?: string;

  // 活动相关字段（仅当 type 为 EVENT 时使用）
  activity_type?: string;   // 活动类型：invitation, competition, points 等
  activity_rules?: any;     // 活动规则，根据 activity_type 不同而不同
}

/**
 * 用户通知（包含已读状态）
 */
export interface UserNotification extends NotificationBase {
  // 用户特定状态
  isRead: boolean;
  readAt?: string;
  isDismissed: boolean;
  dismissedAt?: string;
  clicked: boolean;
  clickedAt?: string;
}

/**
 * 管理员视角的通知
 */
export interface Notification extends NotificationBase {
  status: NotificationStatus;
  targetUsers: TargetUserType;
  customUserIds?: string[];
  allowDismiss: boolean;
  showOnce: boolean;
  createdBy?: string;
  updatedAt: string;
  validFrom?: string;
}

/**
 * 通知响应（别名，用于管理后台）
 */
export type NotificationResponse = Notification;

/**
 * 创建通知请求
 */
export interface CreateNotificationRequest {
  title: string;
  content?: string;
  coverImageUrl?: string;

  category?: NotificationCategory;
  type: NotificationType;
  priority?: NotificationPriority;

  displayType?: string[];
  actionButton?: ActionButton;
  bannerColor?: string;

  targetUsers?: TargetUserType;
  customUserIds?: string[];

  validFrom?: string;
  validUntil?: string;
  publishType?: 'immediate' | 'scheduled' | 'draft';
  scheduledAt?: string;

  allowDismiss?: boolean;
  showOnce?: boolean;

  // 活动相关字段
  activity_type?: string;
  activity_rules?: any;
}

/**
 * 更新通知请求
 */
export interface UpdateNotificationRequest {
  title?: string;
  content?: string;
  coverImageUrl?: string;
  type?: NotificationType;
  priority?: NotificationPriority;
  displayType?: string[];
  actionButton?: ActionButton;
  bannerColor?: string;
  targetUsers?: TargetUserType;
  customUserIds?: string[];
  validFrom?: string;
  validUntil?: string;
  allowDismiss?: boolean;
  showOnce?: boolean;
  status?: NotificationStatus;

  // 活动相关字段
  activity_type?: string;
  activity_rules?: any;
}

/**
 * 通知列表响应
 */
export interface NotificationListResponse {
  total: number;
  page: number;
  pageSize: number;
  items: Notification[];
}

/**
 * 用户通知列表响应
 */
export interface UserNotificationListResponse {
  total: number;
  unreadCount: number;
  page: number;
  pageSize: number;
  items: UserNotification[];
}

/**
 * 通知统计
 */
export interface NotificationStats {
  notificationId: string;
  title: string;
  totalUsers: number;      // 总触达用户数
  readCount: number;       // 已读用户数
  dismissedCount: number;  // 关闭弹窗用户数
  clickedCount: number;    // 点击行动按钮用户数
  readRate: number;        // 查看率（百分比）
  clickRate: number;       // 点击率（百分比）
  publishedAt?: string;
  validUntil?: string;
}

/**
 * WebSocket 通知消息
 */
export interface WebSocketNotificationMessage {
  type: 'notification' | 'unread_count' | 'notifications_list' | 'heartbeat' | 'pong' | 'error';
  data?: any;
  message?: string;
}

/**
 * 标记已读请求
 */
export interface MarkReadRequest {
  notificationIds?: string[]; // 为空则标记全部
}

/**
 * 批量操作响应
 */
export interface BatchOperationResponse {
  success: boolean;
  message: string;
  affectedCount: number;
}
