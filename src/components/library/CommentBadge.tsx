/**
 * 评论数量标记组件
 * 显示在段落/句子末尾，点击后展开评论面板
 */
import { MessageCircle } from 'lucide-react';

interface CommentBadgeProps {
  count: number;
  onClick?: () => void;
  size?: 'sm' | 'md';
  className?: string;
}

export function CommentBadge({ count, onClick, size = 'sm', className = '' }: CommentBadgeProps) {
  if (count <= 0) return null;

  const sizeClasses = {
    sm: 'text-[10px] px-1 py-0.5 gap-0.5',
    md: 'text-xs px-1.5 py-0.5 gap-1',
  };

  const iconSize = size === 'sm' ? 10 : 12;

  return (
    <button
      onClick={(e) => {
        e.stopPropagation();
        e.preventDefault();
        onClick?.();
      }}
      className={`
        inline-flex items-center ${sizeClasses[size]}
        bg-blue-100 dark:bg-blue-900/50
        text-blue-600 dark:text-blue-400
        rounded-full
        hover:bg-blue-200 dark:hover:bg-blue-800/60
        transition-colors
        cursor-pointer
        select-none
        ml-1
        align-super
        ${className}
      `}
      title={`${count} 条评论`}
    >
      <MessageCircle size={iconSize} />
      <span>{count}</span>
    </button>
  );
}

export default CommentBadge;
