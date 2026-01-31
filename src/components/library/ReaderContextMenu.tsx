/**
 * 阅读器右键菜单组件
 */
import { Copy, MessageCircle, MessageSquare } from 'lucide-react';
import { useEffect, useRef } from 'react';
import { useTheme } from '../../hooks/useTheme';

interface ReaderContextMenuProps {
  x: number;
  y: number;
  selectedText: string;
  paragraphIndex: number;
  sentenceIndex?: number;
  onClose: () => void;
  onCopy: () => void;
  onCommentSentence: () => void;
  onCommentParagraph: () => void;
}

export function ReaderContextMenu({
  x,
  y,
  selectedText,
  paragraphIndex,
  sentenceIndex,
  onClose,
  onCopy,
  onCommentSentence,
  onCommentParagraph,
}: ReaderContextMenuProps) {
  const menuRef = useRef<HTMLDivElement>(null);
  const { effectiveTheme } = useTheme();
  const isDarkMode = effectiveTheme === 'dark';

  // 点击外部关闭菜单
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        onClose();
      }
    };

    // 使用 setTimeout 避免立即触发
    const timer = setTimeout(() => {
      document.addEventListener('click', handleClickOutside);
    }, 0);

    return () => {
      clearTimeout(timer);
      document.removeEventListener('click', handleClickOutside);
    };
  }, [onClose]);

  // ESC 关闭菜单
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  // 计算菜单位置，确保不超出视口
  const adjustPosition = () => {
    const menuWidth = 180;
    const menuHeight = 140;
    const padding = 10;

    let adjustedX = x;
    let adjustedY = y;

    if (x + menuWidth > window.innerWidth - padding) {
      adjustedX = window.innerWidth - menuWidth - padding;
    }

    if (y + menuHeight > window.innerHeight - padding) {
      adjustedY = y - menuHeight;
    }

    return { x: adjustedX, y: adjustedY };
  };

  const position = adjustPosition();

  const menuItems = [
    {
      icon: Copy,
      label: '复制',
      onClick: onCopy,
      show: selectedText.length > 0,
    },
    {
      icon: MessageCircle,
      label: '评论当前句子',
      onClick: onCommentSentence,
      show: sentenceIndex !== undefined,
    },
    {
      icon: MessageSquare,
      label: '评论当前段落',
      onClick: onCommentParagraph,
      show: true,
    },
  ];

  return (
    <>
      {/* 遮罩层 - 透明，只用于捕获点击 */}
      <div
        className="fixed inset-0 z-40"
        onClick={onClose}
      />
      {/* 菜单 */}
      <div
        ref={menuRef}
        className="fixed z-50 bg-white dark:bg-slate-800 rounded-2xl p-2 min-w-[160px]"
        style={{
          left: position.x,
          top: position.y,
          boxShadow: isDarkMode
            ? '0 0 20px 4px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.08)'
            : '0 4px 20px rgba(0, 0, 0, 0.15)',
        }}
      >
        <div className="space-y-1">
          {menuItems.filter(item => item.show).map((item, index) => (
            <button
              key={index}
              onClick={() => {
                item.onClick();
                onClose();
              }}
              className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 dark:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-700 transition-colors rounded-xl"
            >
              <item.icon className="w-4 h-4" />
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      </div>
    </>
  );
}

export default ReaderContextMenu;
