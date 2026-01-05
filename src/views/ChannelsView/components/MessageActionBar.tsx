import { useState, useRef } from 'react';
import { Reply, MoreHorizontal, Smile, Edit2, Trash2, Pin, AlertCircle, Star, Forward } from 'lucide-react';
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
  messageContent?: string;
  channelId?: string;
  onReply: () => void;
  onQuickReact: (emoji: string) => void;
  onOpenEmojiPicker: () => void;
  onEdit?: () => void;
  onRecall?: () => void;
  onPin?: () => void;
  onReport?: () => void;
  onAddToSticker?: () => void;
  onForward?: () => void;
}

// 快速表情
const QUICK_EMOJIS = ['👍', '💯', '👎'];

// 更多表情（用于悬浮子菜单）
const MORE_REACTION_EMOJIS = ['❤️', '😊', '😢', '😮', '😡', '🎉', '🔥', '👀', '🙏', '💪', '✅', '❌'];

export function MessageActionBar({
  messageId,
  isOwnMessage,
  isPinned,
  canEdit,
  canRecall,
  canPin,
  hasImage,
  messageContent,
  channelId,
  onReply,
  onQuickReact,
  onOpenEmojiPicker,
  onEdit,
  onRecall,
  onPin,
  onReport,
  onAddToSticker,
  onForward,
}: MessageActionBarProps) {
  const [showMoreMenu, setShowMoreMenu] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [emojiPickerDirection, setEmojiPickerDirection] = useState<'up' | 'down'>('down');
  const emojiButtonRef = useRef<HTMLButtonElement>(null);

  // 复制文字
  const handleCopyText = () => {
    if (messageContent) {
      const plainText = messageContent
        .replace(/!\[.*?\]\(.*?\)/g, '')
        .replace(/\[.*?\]\(.*?\)/g, (match) => {
          const textMatch = match.match(/\[(.*?)\]/);
          return textMatch ? textMatch[1] : '';
        })
        .trim();
      navigator.clipboard.writeText(plainText || messageContent);
    }
    setShowMoreMenu(false);
  };

  // 复制消息链接
  const handleCopyLink = () => {
    const link = `${window.location.origin}/channels/${channelId}?message=${messageId}`;
    navigator.clipboard.writeText(link);
    setShowMoreMenu(false);
  };

  // 菜单项样式
  const menuItemClass = "w-full px-2 py-1.5 text-sm text-left rounded-sm flex items-center justify-between text-gray-600 dark:text-[#b9bbbe] hover:bg-[#5865f2] hover:text-white transition-colors";
  const menuItemDangerClass = "w-full px-2 py-1.5 text-sm text-left rounded-sm flex items-center justify-between text-[#ed4245] hover:bg-[#ed4245] hover:text-white transition-colors";
  const dividerClass = "h-px bg-gray-200 dark:bg-[#2e3035] my-1";

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
          ref={emojiButtonRef}
          onClick={() => {
            if (!showEmojiPicker && emojiButtonRef.current) {
              const rect = emojiButtonRef.current.getBoundingClientRect();
              const spaceBelow = window.innerHeight - rect.bottom;
              const pickerHeight = 320; // MiniEmojiPicker 高度
              setEmojiPickerDirection(spaceBelow < pickerHeight ? 'up' : 'down');
            }
            setShowEmojiPicker(!showEmojiPicker);
          }}
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
            <div className={cn(
              "absolute right-0 z-50",
              emojiPickerDirection === 'down' ? 'top-full mt-1' : 'bottom-full mb-1'
            )}>
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
          <Forward className="w-4 h-4" />
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

        {/* 更多菜单 - Discord风格 */}
        {showMoreMenu && (
          <>
            <div
              className="fixed inset-0 z-40"
              onClick={() => setShowMoreMenu(false)}
            />
            <div
              className="absolute right-0 top-full mt-1 bg-white dark:bg-[#18191c] rounded shadow-lg z-50 w-[188px] p-1.5"
              style={{ boxShadow: '0 0 0 1px rgba(0,0,0,.05), 0 2px 10px rgba(0,0,0,.1)' }}
            >
              {/* 顶部快捷表情栏 */}
              <div className="flex gap-0.5 pb-2">
                {QUICK_EMOJIS.concat(['😂']).map((emoji) => (
                  <button
                    key={emoji}
                    onClick={() => {
                      onQuickReact(emoji);
                      setShowMoreMenu(false);
                    }}
                    className="w-8 h-8 flex items-center justify-center text-xl rounded hover:bg-gray-100 dark:hover:bg-[#4f545c99] hover:scale-110 transition-all"
                  >
                    {emoji}
                  </button>
                ))}
              </div>

              {/* 添加反应 - 带悬浮子菜单 */}
              <div className="relative group/reaction">
                <button
                  className={menuItemClass}
                  onClick={() => {
                    onOpenEmojiPicker();
                    setShowMoreMenu(false);
                  }}
                >
                  <span>添加反应</span>
                  <svg className="w-2.5 h-2.5 opacity-60" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
                  </svg>
                </button>

                {/* 悬浮子菜单 - 更多表情 */}
                <div className="absolute right-full top-0 mr-1 hidden group-hover/reaction:block">
                  <div className="bg-white dark:bg-[#18191c] rounded shadow-lg p-2 w-[200px]" style={{ boxShadow: '0 0 0 1px rgba(0,0,0,.05), 0 2px 10px rgba(0,0,0,.1)' }}>
                    <div className="grid grid-cols-6 gap-1">
                      {MORE_REACTION_EMOJIS.map((emoji) => (
                        <button
                          key={emoji}
                          onClick={() => {
                            onQuickReact(emoji);
                            setShowMoreMenu(false);
                          }}
                          className="w-7 h-7 flex items-center justify-center text-lg rounded hover:bg-gray-100 dark:hover:bg-[#4f545c99] hover:scale-110 transition-all"
                        >
                          {emoji}
                        </button>
                      ))}
                    </div>
                    <div className="mt-2 pt-2 border-t border-gray-200 dark:border-[#2e3035]">
                      <button
                        onClick={() => {
                          onOpenEmojiPicker();
                          setShowMoreMenu(false);
                        }}
                        className="w-full text-xs text-center py-1.5 text-gray-500 dark:text-gray-400 hover:text-[#5865f2] dark:hover:text-[#5865f2] hover:bg-gray-50 dark:hover:bg-[#2e3035] rounded transition-colors"
                      >
                        显示更多
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div className={dividerClass} />

              {/* 回复 */}
              <button
                className={menuItemClass}
                onClick={() => {
                  onReply();
                  setShowMoreMenu(false);
                }}
              >
                <span>回复</span>
                <Reply className="w-4 h-4 opacity-80" />
              </button>

              {/* 转发 */}
              {onForward && (
                <button
                  className={menuItemClass}
                  onClick={() => {
                    onForward();
                    setShowMoreMenu(false);
                  }}
                >
                  <span>转发</span>
                  <Forward className="w-4 h-4 opacity-80" />
                </button>
              )}

              {/* 编辑 */}
              {canEdit && onEdit && (
                <button
                  className={menuItemClass}
                  onClick={() => {
                    onEdit();
                    setShowMoreMenu(false);
                  }}
                >
                  <span>编辑消息</span>
                  <Edit2 className="w-4 h-4 opacity-80" />
                </button>
              )}

              {/* 置顶/取消置顶 */}
              {canPin && onPin && (
                <button
                  className={menuItemClass}
                  onClick={() => {
                    onPin();
                    setShowMoreMenu(false);
                  }}
                >
                  <span>{isPinned ? '取消置顶' : '置顶消息'}</span>
                  <Pin className="w-4 h-4 opacity-80" />
                </button>
              )}

              <div className={dividerClass} />

              {/* 复制文字 */}
              <button className={menuItemClass} onClick={handleCopyText}>
                <span>复制文字</span>
                <svg className="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                </svg>
              </button>

              {/* 复制消息链接 */}
              <button className={menuItemClass} onClick={handleCopyLink}>
                <span>复制消息链接</span>
                <svg className="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                </svg>
              </button>

              {/* 添加到表情 */}
              {hasImage && onAddToSticker && (
                <>
                  <div className={dividerClass} />
                  <button
                    className={menuItemClass}
                    onClick={() => {
                      onAddToSticker();
                      setShowMoreMenu(false);
                    }}
                  >
                    <span>添加到表情</span>
                    <Star className="w-4 h-4 opacity-80" />
                  </button>
                </>
              )}

              {/* 删除 */}
              {canRecall && onRecall && (
                <>
                  <div className={dividerClass} />
                  <button
                    className={menuItemDangerClass}
                    onClick={() => {
                      onRecall();
                      setShowMoreMenu(false);
                    }}
                  >
                    <span>删除信息</span>
                    <Trash2 className="w-4 h-4 opacity-80" />
                  </button>
                </>
              )}

              {/* 举报 */}
              {!isOwnMessage && onReport && (
                <>
                  <div className={dividerClass} />
                  <button
                    className={menuItemDangerClass}
                    onClick={() => {
                      onReport();
                      setShowMoreMenu(false);
                    }}
                  >
                    <span>举报消息</span>
                    <AlertCircle className="w-4 h-4 opacity-80" />
                  </button>
                </>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
