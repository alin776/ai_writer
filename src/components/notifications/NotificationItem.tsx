/**
 * 通知项组件
 *
 * 单个通知的展示，支持点击标记已读、跳转等操作
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { formatDistanceToNow } from 'date-fns';
import { zhCN, zhTW, enUS } from 'date-fns/locale';
import {
  Bell,
  AlertCircle,
  CheckCircle,
  Info,
  Sparkles,
  Calendar,
  Settings,
  Megaphone,
  MessageCircle,
  Heart,
} from 'lucide-react';
import type { UserNotification } from '../../types/notification';
import { NotificationType, NotificationPriority } from '../../types/notification';
import { useNotificationStore } from '../../store/notificationStore';

interface NotificationItemProps {
  notification: UserNotification;
  onClose: () => void;
}

const NotificationItem: React.FC<NotificationItemProps> = ({ notification, onClose }) => {
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
  const { markAsRead, clickAction } = useNotificationStore();

  // 获取当前语言对应的 date-fns locale
  const getDateLocale = () => {
    switch (i18n.language) {
      case 'zh-TW':
        return zhTW;
      case 'en-US':
        return enUS;
      default:
        return zhCN;
    }
  };

  // 获取通知图标 - 更小更精致
  const getIcon = () => {
    const iconClass = "w-3.5 h-3.5";
    switch (notification.type) {
      case NotificationType.AI_TASK_COMPLETED:
        return <CheckCircle className={`${iconClass} text-green-500`} />;
      case NotificationType.ANALYSIS_READY:
        return <Sparkles className={`${iconClass} text-purple-500`} />;
      case NotificationType.SMART_REMINDER:
        return <Bell className={`${iconClass} text-blue-500`} />;
      case NotificationType.MILESTONE:
        return <Sparkles className={`${iconClass} text-amber-500`} />;
      case NotificationType.INACTIVITY_ALERT:
        return <AlertCircle className={`${iconClass} text-orange-500`} />;
      case NotificationType.EVENT:
        return <Calendar className={`${iconClass} text-pink-500`} />;
      case NotificationType.FEATURE:
        return <Sparkles className={`${iconClass} text-indigo-500`} />;
      case NotificationType.ANNOUNCEMENT:
        return <Megaphone className={`${iconClass} text-blue-500`} />;
      case NotificationType.MAINTENANCE:
        return <Settings className={`${iconClass} text-gray-400`} />;
      case NotificationType.COMMENT_REPLY:
        return <MessageCircle className={`${iconClass} text-blue-500`} />;
      case NotificationType.WORK_FAVORITED:
        return <Heart className={`${iconClass} text-red-500`} />;
      default:
        return <Info className={`${iconClass} text-gray-400`} />;
    }
  };

  // 处理点击通知
  const handleClick = async () => {
    // 标记为已读
    if (!notification.isRead) {
      await markAsRead([notification.id]);
    }

    // 如果有行动按钮，跳转到指定URL
    if (notification.actionButton) {
      await clickAction(notification.id);
      navigate(notification.actionButton.url);
      onClose();
    }
  };

  // 格式化时间
  const getFormattedTime = () => {
    try {
      const date = new Date(notification.createdAt);
      // 检查日期是否有效
      if (isNaN(date.getTime())) {
        return t('date.justNow');
      }
      return formatDistanceToNow(date, {
        addSuffix: true,
        locale: getDateLocale(),
      });
    } catch (error) {
      console.error('日期格式化错误:', error, notification.createdAt);
      return t('date.justNow');
    }
  };

  const formattedTime = getFormattedTime();

  return (
    <div
      onClick={handleClick}
      className={`
        group relative px-3 py-2.5 cursor-pointer transition-all duration-200
        ${!notification.isRead
          ? 'bg-gray-50/50 dark:bg-gray-800/30'
          : 'hover:bg-gray-50/30 dark:hover:bg-gray-800/20'
        }
        ${notification.priority === NotificationPriority.URGENT
          ? 'border-l-2 border-red-400/60'
          : notification.priority === NotificationPriority.IMPORTANT
          ? 'border-l-2 border-amber-400/60'
          : ''
        }
      `}
    >
      <div className="flex items-start gap-2.5">
        {/* 图标 - 更小更精致 */}
        <div className="flex-shrink-0 mt-0.5 opacity-60 group-hover:opacity-100 transition-opacity">
          {getIcon()}
        </div>

        {/* 内容 */}
        <div className="flex-1 min-w-0 space-y-0.5">
          {/* 标题 + 时间在同一行 */}
          <div className="flex items-baseline justify-between gap-2">
            <p className={`text-xs font-medium leading-tight ${
              !notification.isRead
                ? 'text-gray-900 dark:text-gray-100'
                : 'text-gray-600 dark:text-gray-400'
            }`}>
              {notification.title}
            </p>
            <span className="text-[10px] text-gray-400 dark:text-gray-600 whitespace-nowrap">
              {formattedTime}
            </span>
          </div>

          {/* 内容摘要 */}
          {notification.content && (
            <p className="text-[11px] leading-relaxed text-gray-500 dark:text-gray-500 line-clamp-2">
              {notification.content}
            </p>
          )}

          {/* 行动按钮 - 更轻量 */}
          {notification.actionButton && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleClick();
              }}
              className="mt-1.5 inline-flex items-center text-[10px] font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors"
            >
              {notification.actionButton.text}
              <span className="ml-0.5">→</span>
            </button>
          )}
        </div>

        {/* 未读标记 - 更小 */}
        {!notification.isRead && (
          <div className="flex-shrink-0 mt-1.5">
            <div className="w-1.5 h-1.5 bg-blue-500 rounded-full"></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default NotificationItem;
