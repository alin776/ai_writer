/**
 * ModeSelector - Agent模式选择器
 *
 * 支持两种模式（与后端完全对齐）：
 * - Planning: 先规划再执行（planning模式）
 * - ReAct: 边思考边执行（react模式）
 *
 * 参考：VS Code Copilot 的模式切换设计
 */

import React from 'react';

export type AgentMode = 'planning' | 'react';

interface ModeSelectorProps {
  mode: AgentMode;
  onModeChange: (mode: AgentMode) => void;
  compact?: boolean;  // 紧凑模式（只显示图标和名称）
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
    description: '先规划再执行，任务分解',
    color: 'text-purple-600'
  },
  'react': {
    label: 'ReAct',
    icon: '⚡',
    description: '边思考边执行，实时推理',
    color: 'text-green-600'
  }
};

export default function ModeSelector({
  mode,
  onModeChange,
  compact = false,
  disabled = false
}: ModeSelectorProps) {
  const [isOpen, setIsOpen] = React.useState(false);

  const handleModeClick = (newMode: AgentMode) => {
    onModeChange(newMode);
    setIsOpen(false);
  };

  return (
    <div className="mode-selector relative">
      {/* 触发按钮 - 简洁图标风格 */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={disabled}
        className={`
          flex items-center gap-1 px-2 py-2
          rounded-md border border-gray-300
          bg-gray-800 hover:bg-gray-700
          transition-colors
          ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
          ${isOpen ? 'bg-gray-700' : ''}
        `}
        title="切换模式"
      >
        <span className="text-sm text-gray-300">∞</span>
        <span className={`text-gray-400 text-[10px] transition-transform ${isOpen ? 'rotate-180' : ''}`}>
          ▼
        </span>
      </button>

      {/* 下拉菜单 - 向上弹出 */}
      {isOpen && (
        <>
          {/* 遮罩层 */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />

          {/* 菜单内容 - 深色主题 */}
          <div className="absolute left-0 bottom-full mb-1 z-20 w-48 bg-gray-800 rounded-md shadow-xl border border-gray-700 overflow-hidden">
            {/* Planning模式 */}
            <button
              onClick={() => handleModeClick('planning')}
              className={`
                w-full flex items-center justify-between px-3 py-2
                hover:bg-gray-700 transition-colors
                text-left
                ${mode === 'planning' ? 'bg-gray-700' : ''}
              `}
            >
              <div className="flex items-center gap-2">
                <span className="text-base">{MODE_CONFIG.planning.icon}</span>
                <span className="text-sm text-gray-200">
                  {MODE_CONFIG.planning.label}
                </span>
              </div>
              <div className="flex items-center gap-1">
                {mode === 'planning' && (
                  <span className="text-blue-400 text-sm">✓</span>
                )}
                <span className="text-gray-400 text-xs">默认</span>
              </div>
            </button>

            {/* ReAct模式 */}
            <button
              onClick={() => handleModeClick('react')}
              className={`
                w-full flex items-center justify-between px-3 py-2
                hover:bg-gray-700 transition-colors
                text-left
                ${mode === 'react' ? 'bg-gray-700' : ''}
              `}
            >
              <div className="flex items-center gap-2">
                <span className="text-base">{MODE_CONFIG.react.icon}</span>
                <span className="text-sm text-gray-200">
                  {MODE_CONFIG.react.label}
                </span>
              </div>
              {mode === 'react' && (
                <span className="text-blue-400 text-sm">✓</span>
              )}
            </button>
          </div>
        </>
      )}
    </div>
  );
}

// 导出配置供其他组件使用
export { MODE_CONFIG };
