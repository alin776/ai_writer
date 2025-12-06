/**
 * ModeSelector - Agent模式选择器
 *
 * 当前只支持 Planning 模式（Multi-Agent 架构）
 * ReAct 模式已移除
 */

import React from 'react';

export type AgentMode = 'planning';

interface ModeSelectorProps {
  mode: AgentMode;
  onModeChange: (mode: AgentMode) => void;
  compact?: boolean;
  disabled?: boolean;
}

interface ModeConfig {
  label: string;
  icon: string;
  description: string;
  color: string;
}

const MODE_CONFIG: Record<AgentMode, ModeConfig> = {
  'planning': {
    label: 'Planning',
    icon: '📋',
    description: '先规划再执行，多Agent协作',
    color: 'text-purple-600'
  }
};

export default function ModeSelector({
  mode,
  onModeChange,
  compact = false,
  disabled = false
}: ModeSelectorProps) {
  // 单一模式，只显示当前模式标识
  return (
    <div className="mode-selector">
      <div
        className={`
          flex items-center gap-1 px-2 py-2
          rounded-md border border-gray-300
          bg-gray-800
          ${disabled ? 'opacity-50' : ''}
        `}
        title="Planning 模式"
      >
        <span className="text-sm text-gray-300">📋</span>
        <span className="text-xs text-gray-400">Planning</span>
      </div>
    </div>
  );
}

// 导出配置供其他组件使用
export { MODE_CONFIG };
