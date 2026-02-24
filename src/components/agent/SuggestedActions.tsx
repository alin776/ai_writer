/**
 * SuggestedActions - 建议操作按钮组件
 */

import React from 'react';

interface SuggestedActionsProps {
  actions: string[];
  onActionClick: (action: string) => void;
}

export default function SuggestedActions({
  actions,
  onActionClick
}: SuggestedActionsProps) {
  const getActionIcon = (action: string) => {
    if (action.includes('大纲')) return '📋';
    if (action.includes('续写')) return '✍️';
    if (action.includes('检查') || action.includes('一致性')) return '✅';
    if (action.includes('评估') || action.includes('质量')) return '📊';
    if (action.includes('改进') || action.includes('建议')) return '💡';
    if (action.includes('改写') || action.includes('版本')) return '🔄';
    if (action.includes('世界观') || action.includes('设定')) return '🌍';
    if (action.includes('角色') || action.includes('人物')) return '👥';
    if (action.includes('分析')) return '🔍';
    if (action.includes('方向')) return '🧭';
    return '⭐';
  };

  return (
    <div className="suggested-actions">
      <div className="text-xs text-gray-600 dark:text-gray-400 mb-1.5 font-medium">
        💡 建议操作:
      </div>
      <div className="flex flex-wrap gap-1.5">
        {actions.map((action, index) => (
          <button
            key={index}
            onClick={() => onActionClick(action)}
            className="px-2.5 py-1.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 hover:border-blue-400 dark:hover:border-blue-500 hover:text-blue-600 dark:hover:text-blue-400 transition-all flex items-center gap-1.5 text-xs shadow-sm dark:text-gray-200"
          >
            <span>{getActionIcon(action)}</span>
            <span>{action}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
