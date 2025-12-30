/**
 * 消息反应组件
 *
 * 显示消息的 Emoji 反应，支持添加/移除反应
 */

import { useState, useRef, useEffect } from 'react';
import { Smile, Plus } from 'lucide-react';
import { cn } from '@/lib/utils';
import { channelApi, type ReactionSummary } from '@/services/channelApi';
import { useAuthStore } from '@/store/authStore';

interface MessageReactionsProps {
  channelId: string;
  messageId: string;
  reactions: ReactionSummary[];
  onReactionsChange?: (reactions: ReactionSummary[]) => void;
}

// 常用快捷反应
const quickReactions = ['👍', '❤️', '😂', '😮', '😢', '🙏'];

// 完整表情列表（用于选择器）
const allEmojis = [
  '👍', '👎', '❤️', '😂', '😮', '😢', '🙏', '🎉',
  '👏', '🔥', '💯', '✨', '🤔', '😊', '😍', '🥰',
  '😎', '🤩', '😭', '😡', '👀', '💪', '✅', '❌',
];

export const MessageReactions: React.FC<MessageReactionsProps> = ({
  channelId,
  messageId,
  reactions,
  onReactionsChange,
}) => {
  const { user } = useAuthStore();
  const [showPicker, setShowPicker] = useState(false);
  const [loading, setLoading] = useState<string | null>(null);
  const pickerRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  // 点击外部关闭选择器
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        showPicker &&
        pickerRef.current &&
        buttonRef.current &&
        !pickerRef.current.contains(event.target as Node) &&
        !buttonRef.current.contains(event.target as Node)
      ) {
        setShowPicker(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showPicker]);

  // 处理反应点击（切换）
  const handleReactionClick = async (emoji: string, hasReacted: boolean) => {
    if (loading) return;

    setLoading(emoji);
    try {
      if (hasReacted) {
        // 移除反应
        await channelApi.removeReaction(channelId, messageId, emoji);
        // 更新本地状态
        const newReactions = reactions
          .map((r) => {
            if (r.emoji === emoji) {
              return { ...r, count: r.count - 1, hasReacted: false };
            }
            return r;
          })
          .filter((r) => r.count > 0);
        onReactionsChange?.(newReactions);
      } else {
        // 添加反应
        await channelApi.addReaction(channelId, messageId, emoji);
        // 更新本地状态
        const existingIndex = reactions.findIndex((r) => r.emoji === emoji);
        let newReactions: ReactionSummary[];
        if (existingIndex >= 0) {
          newReactions = reactions.map((r, i) => {
            if (i === existingIndex) {
              return { ...r, count: r.count + 1, hasReacted: true };
            }
            return r;
          });
        } else {
          newReactions = [...reactions, { emoji, count: 1, hasReacted: true }];
        }
        onReactionsChange?.(newReactions);
      }
    } catch (error) {
      console.error('反应操作失败:', error);
    } finally {
      setLoading(null);
      setShowPicker(false);
    }
  };

  // 处理快速添加反应
  const handleQuickReaction = async (emoji: string) => {
    const existing = reactions.find((r) => r.emoji === emoji);
    await handleReactionClick(emoji, existing?.hasReacted || false);
  };

  if (reactions.length === 0 && !showPicker) {
    return null;
  }

  return (
    <div className="flex flex-wrap items-center gap-1 mt-1.5">
      {/* 已有反应 */}
      {reactions.map((reaction) => (
        <button
          key={reaction.emoji}
          onClick={() => handleReactionClick(reaction.emoji, reaction.hasReacted)}
          disabled={loading === reaction.emoji}
          className={cn(
            'inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full transition-colors cursor-pointer',
            reaction.hasReacted
              ? 'bg-blue-100 dark:bg-blue-900/50 border border-blue-300 dark:border-blue-700 text-blue-700 dark:text-blue-300'
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-600 dark:text-gray-400',
            loading === reaction.emoji && 'opacity-50'
          )}
          title={reaction.hasReacted ? '点击取消' : '点击添加'}
        >
          <span className="text-sm">{reaction.emoji}</span>
          <span>{reaction.count}</span>
        </button>
      ))}

      {/* 添加反应按钮 */}
      <div className="relative">
        <button
          ref={buttonRef}
          onClick={() => setShowPicker(!showPicker)}
          className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-500 dark:text-gray-400 transition-colors"
          title="添加反应"
        >
          <Plus className="w-3 h-3" />
        </button>

        {/* 反应选择器 */}
        {showPicker && (
          <div
            ref={pickerRef}
            className="absolute bottom-full left-0 mb-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg p-2 z-50"
            style={{ minWidth: '200px' }}
          >
            {/* 快捷反应 */}
            <div className="flex gap-1 pb-2 border-b border-gray-100 dark:border-gray-700 mb-2">
              {quickReactions.map((emoji) => (
                <button
                  key={emoji}
                  onClick={() => handleQuickReaction(emoji)}
                  className="text-xl p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                >
                  {emoji}
                </button>
              ))}
            </div>

            {/* 完整表情列表 */}
            <div className="grid grid-cols-6 gap-1">
              {allEmojis.map((emoji) => (
                <button
                  key={emoji}
                  onClick={() => handleQuickReaction(emoji)}
                  className="text-lg p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                >
                  {emoji}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
