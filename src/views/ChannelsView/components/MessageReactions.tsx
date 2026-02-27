/**
 * 消息反应组件
 *
 * 显示消息的 Emoji 反应，支持添加/移除反应
 * 使用本地 state + flushSync 保证点击后立即同步渲染。
 */

import { useState, useRef, useEffect } from 'react';
import { Plus } from 'lucide-react';
import { cn } from '@/lib/utils';
import { channelApi, type ReactionSummary } from '@/services/channelApi';

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
  reactions: reactionsProp,
  onReactionsChange,
}) => {
  const [localReactions, setLocalReactions] = useState<ReactionSummary[]>(reactionsProp);
  const [showPicker, setShowPicker] = useState(false);
  const [loading, setLoading] = useState<string | null>(null);
  const pickerRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  // 从 props 同步到本地 state（"setState during render" 模式）
  const propKey = reactionsProp.map(r => `${r.emoji}:${r.count}:${r.hasReacted}`).join(',');
  const localKey = localReactions.map(r => `${r.emoji}:${r.count}:${r.hasReacted}`).join(',');
  if (propKey !== localKey && !loading) {
    setLocalReactions(reactionsProp);
  }

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

  const handleReactionClick = async (emoji: string, hasReacted: boolean) => {
    if (loading) return;

    const originalReactions = localReactions;
    let newReactions: ReactionSummary[];
    if (hasReacted) {
      newReactions = localReactions
        .map(r => r.emoji === emoji ? { ...r, count: r.count - 1, hasReacted: false } : r)
        .filter(r => r.count > 0);
    } else {
      const idx = localReactions.findIndex(r => r.emoji === emoji);
      if (idx >= 0) {
        newReactions = localReactions.map((r, i) =>
          i === idx ? { ...r, count: r.count + 1, hasReacted: true } : r
        );
      } else {
        newReactions = [...localReactions, { emoji, count: 1, hasReacted: true }];
      }
    }

    // 立即更新本地 state
    setLocalReactions(newReactions);
    setLoading(emoji);
    setShowPicker(false);

    // 同步通知父组件
    onReactionsChange?.(newReactions);

    try {
      if (hasReacted) {
        await channelApi.removeReaction(channelId, messageId, emoji);
      } else {
        await channelApi.addReaction(channelId, messageId, emoji);
      }
      // API 成功后从服务器拉取最新数据
      try {
        const fresh = await channelApi.getMessageReactions(channelId, messageId);
        setLocalReactions(fresh.reactions);
        onReactionsChange?.(fresh.reactions);
      } catch {
        // 拉取失败不影响
      }
    } catch (error) {
      console.error('反应操作失败:', error);
      setLocalReactions(originalReactions);
      onReactionsChange?.(originalReactions);
    } finally {
      setLoading(null);
    }
  };

  const handleQuickReaction = async (emoji: string) => {
    const existing = localReactions.find(r => r.emoji === emoji);
    await handleReactionClick(emoji, existing?.hasReacted || false);
  };

  if (localReactions.length === 0 && !showPicker) {
    return null;
  }

  return (
    <div className="flex flex-wrap items-center gap-1 mt-1.5">
      {localReactions.map((reaction) => (
        <button
          key={reaction.emoji}
          onClick={() => handleReactionClick(reaction.emoji, reaction.hasReacted)}
          disabled={loading === reaction.emoji}
          className={cn(
            'inline-flex items-center gap-1 px-2 py-0.5 text-sm rounded transition-all duration-100 cursor-pointer',
            'bg-black/[0.04] dark:bg-white/[0.04] border border-transparent',
            'hover:bg-black/[0.08] dark:hover:bg-white/[0.08]',
            reaction.hasReacted && 'bg-[#5865f2]/10 border-[#5865f2]',
            loading === reaction.emoji && 'opacity-50'
          )}
          title={reaction.hasReacted ? '点击取消' : '点击添加'}
        >
          <span>{reaction.emoji}</span>
          <span className="text-gray-700 dark:text-gray-300">{reaction.count}</span>
        </button>
      ))}

      <div className="relative">
        <button
          ref={buttonRef}
          onClick={() => setShowPicker(!showPicker)}
          className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-500 dark:text-gray-400 transition-colors"
          title="添加反应"
        >
          <Plus className="w-3 h-3" />
        </button>

        {showPicker && (
          <div
            ref={pickerRef}
            className="absolute bottom-full left-0 mb-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg p-2 z-50"
            style={{ minWidth: '200px' }}
          >
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
