/**
 * 通知弹窗组件
 *
 * 用户登录后，如果有重要通知会弹出模态框展示
 */

import React, { useEffect, useState } from 'react';
import { X, ExternalLink } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import type { UserNotification } from '../../types/notification';
import { NotificationPriority } from '../../types/notification';
import { useNotificationStore } from '../../store/notificationStore';

interface NotificationModalProps {
  notification: UserNotification;
  onClose: () => void;
}

const NotificationModal: React.FC<NotificationModalProps> = ({
  notification,
  onClose,
}) => {
  const navigate = useNavigate();
  const { dismiss, clickAction } = useNotificationStore();
  const [currentIndex, setCurrentIndex] = useState(0);

  // 处理关闭
  const handleClose = async () => {
    await dismiss(notification.id);
    onClose();
  };

  // 处理"稍后查看"
  const handleLater = () => {
    onClose(); // 只关闭弹窗，不标记为已读
  };

  // 处理"立即参与/查看"
  const handleAction = async () => {
    if (notification.actionButton) {
      await clickAction(notification.id);
      navigate(notification.actionButton.url);
      onClose();
    }
  };

  // 防止背景滚动
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      {/* 弹窗容器 */}
      <div
        className="relative w-full max-w-2xl bg-white dark:bg-gray-900 rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* 关闭按钮 */}
        <button
          onClick={handleClose}
          className="absolute top-4 right-4 p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors z-10"
          aria-label="关闭"
        >
          <X className="w-5 h-5" />
        </button>

        {/* 封面图 */}
        {notification.coverImageUrl && (
          <div className="relative w-full h-64 bg-gradient-to-br from-blue-500 to-purple-600">
            <img
              src={notification.coverImageUrl}
              alt={notification.title}
              className="w-full h-full object-cover"
            />
          </div>
        )}

        {/* 内容区域 */}
        <div className="p-8">
          {/* 标题 */}
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            {notification.title}
          </h2>

          {/* 正文 */}
          {notification.content && (
            <div className="prose dark:prose-invert max-w-none mb-6">
              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                {notification.content}
              </p>
            </div>
          )}

          {/* 操作按钮 */}
          <div className="flex items-center justify-end gap-3">
            <button
              onClick={handleLater}
              className="px-6 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            >
              稍后查看
            </button>

            {notification.actionButton && (
              <button
                onClick={handleAction}
                className="flex items-center gap-2 px-6 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors"
              >
                {notification.actionButton.text}
                <ExternalLink className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* 优先级指示条 */}
        {notification.priority === NotificationPriority.URGENT && (
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-red-500 to-orange-500"></div>
        )}
        {notification.priority === NotificationPriority.IMPORTANT && (
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-yellow-500 to-orange-500"></div>
        )}
      </div>
    </div>
  );
};

export default NotificationModal;
