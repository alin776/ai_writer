import { useState } from 'react';
import { Reply, Share, MoreHorizontal, Smile, Edit2, Trash2, Pin, AlertCircle, Star } from 'lucide-react';
import { cn } from '@/lib/utils';
import MiniEmojiPicker from './MiniEmojiPicker';

interface MessageActionBarProps {
  messageId: string;
  isOwnMessage: boolean;
  isPinned?: boolean;
  canEdit?: boolean;
  canRecall?: boolean;
  canPin?: boolean;
  hasImage?: boolean;
  onReply: () => void;
  onQuickReact: (emoji: string) => void;
  onOpenEmojiPicker: () => void;
  onForward?: () => void;
  onEdit?: () => void;
  onRecall?: () => void;
  onPin?: () => void;
  onReport?: () => void;
  onAddToSticker?: () => void;
}

// 快速表情
const QUICK_EMOJIS = ['👍', '💯', '👎'];

export function MessageActionBar({
  messageId,
  isOwnMessage,
  isPinned,
  canEdit,
  canRecall,
  canPin,
  hasImage,
  onReply,
  onQuickReact,
  onOpenEmojiPicker,
  onForward,
  onEdit,
  onRecall,
  onPin,
  onReport,
  onAddToSticker,
}: MessageActionBarProps) {
  const [showMoreMenu, setShowMoreMenu] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);

  return (
    <div
      className={cn(
        "absolute right-4 top-1 flex items-center gap-0.5",
        "bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700",
        "rounded-md shadow-sm px-1",
        "opacity-0 group-hover:opacity-100 transition-opacity duration-150"
      )}
    >
      {/* 快速表情按钮 */}
      {QUICK_EMOJIS.map((emoji) => (
        <button
          key={emoji}
          onClick={() => onQuickReact(emoji)}
          className="text-lg py-0.5 px-1 rounded cursor-pointer transition-all duration-100 hover:bg-black/[0.06] dark:hover:bg-white/[0.06] hover:scale-110"
        >
          {emoji}
        </button>
      ))}

      {/* 分隔线 */}
      <div className="w-px h-5 bg-gray-200 dark:bg-gray-700 mx-1" />

      {/* 表情选择器按钮 */}
      <div className="relative">
        <button
          onClick={() => setShowEmojiPicker(!showEmojiPicker)}
          className="py-1 px-1.5 rounded text-gray-500 dark:text-gray-400 transition-all duration-100 hover:bg-black/[0.06] dark:hover:bg-white/[0.06] hover:text-gray-900 dark:hover:text-gray-100"
          title="添加表情"
        >
          <Smile className="w-4 h-4" />
        </button>

        {/* 迷你表情选择器 */}
        {showEmojiPicker && (
          <>
            <div
              className="fixed inset-0 z-40"
              onClick={() => setShowEmojiPicker(false)}
            />
            <div className="absolute right-0 top-full mt-1 z-50">
              <MiniEmojiPicker
                onSelect={(emoji) => {
                  onQuickReact(emoji);
                  setShowEmojiPicker(false);
                }}
                onClose={() => setShowEmojiPicker(false)}
              />
            </div>
          </>
        )}
      </div>

      {/* 回复按钮 */}
      <button
        onClick={onReply}
        className="py-1 px-1.5 rounded text-gray-500 dark:text-gray-400 transition-all duration-100 hover:bg-black/[0.06] dark:hover:bg-white/[0.06] hover:text-gray-900 dark:hover:text-gray-100"
        title="回复"
      >
        <Reply className="w-4 h-4" />
      </button>

      {/* 转发按钮 */}
      {onForward && (
        <button
          onClick={onForward}
          className="py-1 px-1.5 rounded text-gray-500 dark:text-gray-400 transition-all duration-100 hover:bg-black/[0.06] dark:hover:bg-white/[0.06] hover:text-gray-900 dark:hover:text-gray-100"
          title="转发"
        >
          <Share className="w-4 h-4" />
        </button>
      )}

      {/* 更多按钮 */}
      <div className="relative">
        <button
          onClick={() => setShowMoreMenu(!showMoreMenu)}
          className="py-1 px-1.5 rounded text-gray-500 dark:text-gray-400 transition-all duration-100 hover:bg-black/[0.06] dark:hover:bg-white/[0.06] hover:text-gray-900 dark:hover:text-gray-100"
          title="更多"
        >
          <MoreHorizontal className="w-4 h-4" />
        </button>

        {/* 更多菜单 */}
        {showMoreMenu && (
          <>
            <div
              className="fixed inset-0 z-40"
              onClick={() => setShowMoreMenu(false)}
            />
            <div className="absolute right-0 top-full mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl z-50 py-1 min-w-[140px]">
              {/* 添加到表情 */}
              {hasImage && onAddToSticker && (
                <button
                  className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2 text-amber-600 dark:text-amber-400"
                  onClick={() => {
                    onAddToSticker();
                    setShowMoreMenu(false);
                  }}
                >
                  <Star className="w-3.5 h-3.5" />
                  添加到表情
                </button>
              )}

              {/* 编辑 */}
              {canEdit && onEdit && (
                <button
                  className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2 text-blue-600 dark:text-blue-400"
                  onClick={() => {
                    onEdit();
                    setShowMoreMenu(false);
                  }}
                >
                  <Edit2 className="w-3.5 h-3.5" />
                  编辑
                </button>
              )}

              {/* 置顶/取消置顶 */}
              {canPin && onPin && (
                <button
                  className={cn(
                    "w-full px-3 py-2 text-xs text-left hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2",
                    isPinned ? "text-orange-600 dark:text-orange-400" : "text-amber-600 dark:text-amber-400"
                  )}
                  onClick={() => {
                    onPin();
                    setShowMoreMenu(false);
                  }}
                >
                  <Pin className="w-3.5 h-3.5" />
                  {isPinned ? '取消置顶' : '置顶'}
                </button>
              )}

              {/* 撤回 */}
              {canRecall && onRecall && (
                <button
                  className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2 text-orange-600 dark:text-orange-400"
                  onClick={() => {
                    onRecall();
                    setShowMoreMenu(false);
                  }}
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  撤回
                </button>
              )}

              {/* 举报 */}
              {!isOwnMessage && onReport && (
                <button
                  className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2 text-red-600 dark:text-red-400"
                  onClick={() => {
                    onReport();
                    setShowMoreMenu(false);
                  }}
                >
                  <AlertCircle className="w-3.5 h-3.5" />
                  举报
                </button>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
