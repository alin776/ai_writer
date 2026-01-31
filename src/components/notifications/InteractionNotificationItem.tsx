/**
 * 互动通知项组件
 *
 * 专门用于显示评论回复、收藏等互动通知
 * 支持点击跳转到原评论位置和直接回复功能
 */

import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { formatDistanceToNow } from 'date-fns';
import { zhCN, zhTW, enUS } from 'date-fns/locale';
import { MessageCircle, Heart, Circle, Smile } from 'lucide-react';
import MiniEmojiPicker from '../../views/ChannelsView/components/MiniEmojiPicker';
import type { UserNotification } from '../../types/notification';
import { NotificationType } from '../../types/notification';
import { useNotificationStore } from '../../store/notificationStore';
import { DataService } from '../../services/DataService';
import { chapterCommentApi } from '../../services/chapterCommentApi';
import { useToast } from '../../hooks/useToast';

interface InteractionNotificationItemProps {
  notification: UserNotification;
  onReplySuccess?: () => void;
}

// 评论回复的元数据类型（ApiAdapter 已转换为 camelCase）
interface CommentReplyMetadata {
  workId: string;
  commentId: string;
  parentCommentId?: string;
  replierId: string;
  replierName: string;
  replierAvatar?: string;
}

export function InteractionNotificationItem({
  notification,
  onReplySuccess
}: InteractionNotificationItemProps) {
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
  const { markAsRead } = useNotificationStore();
  const toast = useToast();

  const [showReplyInput, setShowReplyInput] = useState(false);
  const [replyContent, setReplyContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const emojiButtonRef = useRef<HTMLButtonElement>(null);
  const emojiPickerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const isComposingRef = useRef(false);

  // 获取元数据
  const metadata = notification.activityRules as CommentReplyMetadata | undefined;
  const isCommentReply = notification.type === NotificationType.COMMENT_REPLY;

  // 获取日期 locale
  const getDateLocale = () => {
    switch (i18n.language) {
      case 'zh-TW': return zhTW;
      case 'en-US': return enUS;
      default: return zhCN;
    }
  };

  // 格式化时间
  const formatTime = () => {
    try {
      const date = new Date(notification.createdAt);
      if (isNaN(date.getTime())) return t('date.justNow');
      return formatDistanceToNow(date, {
        addSuffix: false,
        locale: getDateLocale(),
      });
    } catch {
      return t('date.justNow');
    }
  };

  // 点击 emoji 外部关闭
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        emojiPickerRef.current &&
        !emojiPickerRef.current.contains(e.target as Node) &&
        emojiButtonRef.current &&
        !emojiButtonRef.current.contains(e.target as Node)
      ) {
        setShowEmojiPicker(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // 处理点击通知内容 - 跳转到评论位置
  const handleContentClick = async () => {
    // 标记已读
    if (!notification.isRead) {
      await markAsRead([notification.id]);
    }

    // Prefer explicit action URL when available (e.g. chapter comment links)
    if (notification.actionButton?.url) {
      navigate(notification.actionButton.url);
      return;
    }

    // Fallback to metadata-driven URL
    if (metadata?.workId) {
      const url = metadata.commentId
        ? `/library/novel-square?openNovel=${metadata.workId}&comment=${metadata.commentId}`
        : `/library/novel-square?openNovel=${metadata.workId}`;
      navigate(url);
    }
  };

  // 处理回复按钮点击
  const handleReplyClick = () => {
    setShowReplyInput(true);
    // 延迟聚焦输入框
    setTimeout(() => inputRef.current?.focus(), 100);
  };

  // 处理取消回复
  const handleCancelReply = () => {
    setShowReplyInput(false);
    setReplyContent('');
    setShowEmojiPicker(false);
  };

  // 处理提交回复
  const getActionParams = () => {
    const actionUrl = notification.actionButton?.url;
    if (!actionUrl) return null;
    try {
      const parsed = new URL(actionUrl, window.location.origin);
      return {
        workId: parsed.searchParams.get('openNovel') || undefined,
        commentId: parsed.searchParams.get('comment') || undefined,
        chapterId: parsed.searchParams.get('chapter') || undefined,
        chapterCommentId: parsed.searchParams.get('chapterComment') || undefined,
      };
    } catch {
      return null;
    }
  };

  const handleSubmitReply = async (content?: string) => {
    if (isSubmitting) return;
    const trimmed = (content ?? replyContent).trim();
    if (!trimmed) return;

    const actionParams = getActionParams();
    const workId = metadata?.workId || actionParams?.workId;
    const parentCommentId = metadata?.commentId || actionParams?.commentId || actionParams?.chapterCommentId;
    const isChapterComment = !!(actionParams?.chapterId || actionParams?.chapterCommentId);

    // 验证必要的元数据
    if (!parentCommentId || (!workId && !actionParams?.chapterId)) {
      console.error('缺少必要的元数据:', {
        metadata,
        activityRules: notification.activityRules,
        notificationId: notification.id,
        notificationType: notification.type
      });
      toast.error(`无法回复：缺少 ${!workId ? 'workId' : 'commentId'}`);
      return;
    }

    setIsSubmitting(true);
    try {
      if (isChapterComment && actionParams?.chapterId) {
        await chapterCommentApi.createComment(actionParams.chapterId, {
          content: trimmed,
          parentId: parentCommentId,
          replyToUserId: metadata?.replierId,
        });
      } else if (workId) {
        // 调用 API 创建评论
        await DataService.createComment(workId, {
          content: trimmed,
          parentId: parentCommentId, // 回复这条评论
          replyToUserId: metadata?.replierId // 回复给原回复者
        });
      }

      // 成功后清空输入
      setReplyContent('');
      setShowReplyInput(false);
      setShowEmojiPicker(false);
      onReplySuccess?.();

      // 提示用户回复成功
      toast.success('回复成功！');
    } catch (error) {
      console.error('回复失败:', error);
      toast.error('回复失败，请稍后重试');
    } finally {
      setIsSubmitting(false);
    }
  };

  // 处理 emoji 选择
  const handleEmojiSelect = (emoji: string) => {
    setReplyContent(prev => prev + emoji);
    setShowEmojiPicker(false);
    inputRef.current?.focus();
  };

  // 表情包位置状态
  const [emojiPickerStyle, setEmojiPickerStyle] = useState<React.CSSProperties>({});

  // 处理 emoji 按钮点击 - 计算最佳位置（使用 fixed 定位）
  const handleEmojiButtonClick = () => {
    if (!showEmojiPicker && emojiButtonRef.current) {
      const rect = emojiButtonRef.current.getBoundingClientRect();
      const emojiPickerHeight = 340;
      const emojiPickerWidth = 288; // w-72 = 18rem = 288px
      const spaceBelow = window.innerHeight - rect.bottom;
      const spaceAbove = rect.top;

      // 计算 fixed 定位的位置
      let top: number;
      if (spaceBelow >= emojiPickerHeight) {
        // 显示在下方
        top = rect.bottom + 8;
      } else if (spaceAbove >= emojiPickerHeight) {
        // 显示在上方
        top = rect.top - emojiPickerHeight - 8;
      } else {
        // 空间都不够，选择更大的一边
        top = spaceBelow >= spaceAbove ? rect.bottom + 8 : rect.top - emojiPickerHeight - 8;
      }

      // 确保不超出右边界
      let left = rect.right - emojiPickerWidth;
      if (left < 8) left = 8;

      setEmojiPickerStyle({
        position: 'fixed',
        top: `${top}px`,
        left: `${left}px`,
        zIndex: 9999,
      });
    }
    setShowEmojiPicker(!showEmojiPicker);
  };

  // 获取图标
  const getIcon = () => {
    if (notification.type === NotificationType.COMMENT_REPLY) {
      return <MessageCircle className="w-5 h-5" />;
    }
    if (notification.type === NotificationType.WORK_FAVORITED) {
      return <Heart className="w-5 h-5 text-red-500" />;
    }
    return <MessageCircle className="w-5 h-5" />;
  };

  return (
    <div className="group py-4 border-b border-gray-100 dark:border-gray-800 last:border-0">
      <div className="flex gap-3">
        {/* 用户头像 */}
        <div className="flex-shrink-0 mt-1">
          {metadata?.replierAvatar ? (
            <img
              src={metadata.replierAvatar}
              alt={metadata.replierName || '用户头像'}
              className="w-10 h-10 rounded-full object-cover"
            />
          ) : (
            <div className="w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-500 dark:text-gray-400 text-sm font-medium">
              {metadata?.replierName?.[0]?.toUpperCase() || getIcon()}
            </div>
          )}
        </div>

        {/* 主内容区域 */}
        <div className="flex-1 min-w-0">
          {/* 标题行 */}
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
              {metadata?.replierName || notification.title.split(' ')[0]}
            </span>
            <span className="text-sm text-gray-500 dark:text-gray-400">
              {isCommentReply ? '回复了你的评论' : '收藏了你的作品'}
            </span>
            {!notification.isRead && (
              <Circle className="w-2 h-2 fill-blue-500 text-blue-500 flex-shrink-0" />
            )}
            <span className="text-xs text-gray-400 dark:text-gray-500 ml-auto">
              {formatTime()}
            </span>
          </div>

          {/* 评论内容 - 可点击跳转 */}
          <div
            onClick={handleContentClick}
            className="mt-1 text-sm text-gray-600 dark:text-gray-400 cursor-pointer hover:text-gray-900 dark:hover:text-gray-200 transition-colors"
          >
            {notification.content}
          </div>

          {/* 操作按钮区域 */}
          {isCommentReply && !showReplyInput && (
            <div className="mt-3 flex items-center gap-4">
              <button
                onClick={handleReplyClick}
                className="flex items-center gap-1.5 px-4 py-1.5 text-sm text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-full transition-colors"
              >
                <MessageCircle className="w-4 h-4" />
                回复
              </button>
            </div>
          )}

          {/* 回复输入框 */}
          {showReplyInput && (
            <div className="mt-3">
              <div className="flex items-center gap-2 bg-gray-100 dark:bg-gray-800 rounded-full px-4 py-2">
                <input
                  ref={inputRef}
                  type="text"
                  value={replyContent}
                  onChange={(e) => setReplyContent(e.target.value)}
                  onCompositionStart={() => {
                    isComposingRef.current = true;
                  }}
                  onCompositionEnd={() => {
                    isComposingRef.current = false;
                  }}
                  onKeyDown={(e) => {
                    // Skip while composing (IME)
                    if (isComposingRef.current) return;
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSubmitReply(e.currentTarget.value);
                    }
                  }}
                  placeholder="回复"
                  className="flex-1 bg-transparent border-none outline-none text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400"
                  disabled={isSubmitting}
                />

                {/* Emoji 按钮 */}
                <div className="relative">
                  <button
                    ref={emojiButtonRef}
                    onClick={handleEmojiButtonClick}
                    className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                  >
                    <Smile className="w-5 h-5" />
                  </button>

                  {showEmojiPicker && (
                    <div
                      ref={emojiPickerRef}
                      style={emojiPickerStyle}
                    >
                      <MiniEmojiPicker
                        onSelect={handleEmojiSelect}
                        onClose={() => setShowEmojiPicker(false)}
                      />
                    </div>
                  )}
                </div>

                {/* 取消按钮 */}
                <button
                  onClick={handleCancelReply}
                  className="px-3 py-1 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors"
                >
                  取消
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default InteractionNotificationItem;
