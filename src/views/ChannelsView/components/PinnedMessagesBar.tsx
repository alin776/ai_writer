import React, { useState, useEffect } from 'react';
import { Pin, ChevronDown, X } from 'lucide-react';
import { PinnedMessage, getPinnedMessages, unpinMessage } from '../../../services/channelApi';

interface PinnedMessagesBarProps {
  channelId: string;
  isAdmin: boolean;
  onMessageClick?: (messageId: string) => void;
  refreshTrigger?: number;
}

const PinnedMessagesBar: React.FC<PinnedMessagesBarProps> = ({
  channelId,
  isAdmin,
  onMessageClick,
  refreshTrigger
}) => {
  const [pinnedMessages, setPinnedMessages] = useState<PinnedMessage[]>([]);
  const [isExpanded, setIsExpanded] = useState(false);
  const [loading, setLoading] = useState(false);

  // 加载置顶消息
  const loadPinnedMessages = async () => {
    if (!channelId) return;

    try {
      setLoading(true);
      const response = await getPinnedMessages(channelId);
      setPinnedMessages(response.messages || []);
    } catch (error) {
      console.error('加载置顶消息失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPinnedMessages();
  }, [channelId, refreshTrigger]);

  // 取消置顶
  const handleUnpin = async (e: React.MouseEvent, messageId: string) => {
    e.stopPropagation();
    try {
      await unpinMessage(channelId, messageId);
      setPinnedMessages(prev => prev.filter(m => m.id !== messageId));
    } catch (error) {
      console.error('取消置顶失败:', error);
    }
  };

  // 没有置顶消息时不显示
  if (pinnedMessages.length === 0) {
    return null;
  }

  const latestPinned = pinnedMessages[0];

  return (
    <div className="border-b border-gray-200 dark:border-gray-700 bg-amber-50/50 dark:bg-amber-900/20">
      {/* 主栏 - 显示最新置顶 */}
      <div
        className="flex items-center gap-2 px-4 py-2 cursor-pointer hover:bg-amber-100/50 dark:hover:bg-amber-900/30 transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <Pin className="w-4 h-4 text-amber-600 dark:text-amber-400 flex-shrink-0" />

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-xs font-medium text-amber-700 dark:text-amber-300">
              置顶消息
            </span>
            {pinnedMessages.length > 1 && (
              <span className="px-1.5 py-0.5 text-xs rounded-full bg-amber-200 dark:bg-amber-800 text-amber-700 dark:text-amber-300">
                {pinnedMessages.length}
              </span>
            )}
          </div>
          <p className="text-sm text-amber-800 dark:text-amber-200 truncate">
            {latestPinned.content}
          </p>
        </div>

        <ChevronDown
          className={`w-4 h-4 text-amber-600 dark:text-amber-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
        />
      </div>

      {/* 展开的置顶列表 */}
      {isExpanded && (
        <div className="border-t border-amber-200 dark:border-amber-800 max-h-64 overflow-y-auto">
          {pinnedMessages.map((msg) => (
            <div
              key={msg.id}
              className="flex items-start gap-3 px-4 py-3 hover:bg-amber-100/50 dark:hover:bg-amber-900/30 transition-colors cursor-pointer border-b border-amber-100 dark:border-amber-800/50 last:border-b-0"
              onClick={() => onMessageClick?.(msg.id)}
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                    {msg.userName || '已删除用户'}
                  </span>
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {new Date(msg.createdAt).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">
                  {msg.content}
                </p>
                {msg.pinnedByName && (
                  <p className="text-xs text-amber-600 dark:text-amber-400 mt-1">
                    由 {msg.pinnedByName} 置顶
                  </p>
                )}
              </div>

              {isAdmin && (
                <button
                  className="p-1.5 rounded hover:bg-red-100 dark:hover:bg-red-900/30 text-red-500 dark:text-red-400 transition-colors flex-shrink-0"
                  onClick={(e) => handleUnpin(e, msg.id)}
                  title="取消置顶"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PinnedMessagesBar;
