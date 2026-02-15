/**
 * 在线状态指示器组件
 */

import React from 'react';

interface OnlineStatusProps {
  isOnline: boolean;
  size?: 'sm' | 'md' | 'lg';
  showBorder?: boolean;
}

export const OnlineStatus: React.FC<OnlineStatusProps> = ({
  isOnline,
  size = 'md',
  showBorder = false
}) => {
  const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-2.5 h-2.5',
    lg: 'w-3 h-3'
  };

  return (
    <span
      className={`
        ${sizeClasses[size]}
        rounded-full
        ${isOnline ? 'bg-green-500' : 'bg-gray-400 dark:bg-gray-600'}
        ${showBorder ? 'border-2 border-white dark:border-gray-800' : ''}
      `}
      title={isOnline ? '在线' : '离线'}
    />
  );
};
