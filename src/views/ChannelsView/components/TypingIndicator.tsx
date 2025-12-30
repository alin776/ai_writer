/**
 * 正在输入指示器组件
 */

import React from 'react';

interface TypingIndicatorProps {
  typingUsers: Array<{ user_id: string; username: string }>;
}

export const TypingIndicator: React.FC<TypingIndicatorProps> = ({ typingUsers }) => {
  if (typingUsers.length === 0) return null;

  const text = typingUsers.length === 1
    ? `${typingUsers[0].username} 正在输入...`
    : typingUsers.length === 2
    ? `${typingUsers[0].username}、${typingUsers[1].username} 正在输入...`
    : '多人正在输入...';

  return (
    <div className="px-3 py-2 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-100 dark:border-gray-700 flex items-center gap-2">
      <div className="flex items-center gap-1">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="w-1.5 h-1.5 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce"
            style={{ animationDelay: `${i * 0.15}s` }}
          />
        ))}
      </div>
      <span className="text-xs text-gray-500 dark:text-gray-400">
        {text}
      </span>
    </div>
  );
};
