/**
 * ModeSelector - Agent 模式选择器
 *
 * 支持两种模式（与后端完全对齐）：
 * - Planning: 先规划再执行（planning 模式）
 * - ReAct: 边思考边执行（react 模式）
 *
 * 参考 Cursor 风格的胶囊按钮
 */

import React from 'react';
import { Check, ChevronDown, Sparkles, Workflow } from 'lucide-react';

export type AgentMode = 'planning' | 'react';

interface ModeSelectorProps {
  mode: AgentMode;
  onModeChange: (mode: AgentMode) => void;
  compact?: boolean; // 紧凑模式（只显示图标和名称）
  disabled?: boolean;
  className?: string;
}

interface ModeConfig {
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  description: string;
  badgeClass: string;
}

const MODE_CONFIG: Record<AgentMode, ModeConfig> = {
  planning: {
    label: 'Plan',
    icon: Workflow,
    description: '先规划再执行，任务分解',
    badgeClass: 'bg-primary-50 text-primary-700 ring-1 ring-primary-100',
  },
  react: {
    label: 'Agent',
    icon: Sparkles,
    description: '边思考边执行，实时推理',
    badgeClass: 'bg-emerald-50 text-emerald-700 ring-1 ring-emerald-100',
  },
};

export default function ModeSelector({
  mode,
  onModeChange,
  compact = false,
  disabled = false,
  className = '',
}: ModeSelectorProps) {
  const [isOpen, setIsOpen] = React.useState(false);

  const handleModeClick = (newMode: AgentMode) => {
    onModeChange(newMode);
    setIsOpen(false);
  };

  const CurrentIcon = MODE_CONFIG[mode].icon;

  return (
    <div className={`mode-selector relative ${className}`}>
      {/* 触发按钮 - 胶囊样式 */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={disabled}
        className={`
          inline-flex items-center gap-2 rounded-full
          border text-sm font-medium transition-all shadow-sm
          ${compact ? 'px-2.5 py-1.5 h-9' : 'px-3.5 py-2.5 h-11'}
          ${isOpen ? 'border-primary-200 bg-primary-50/80' : 'border-gray-200 bg-white/90 hover:border-primary-200 hover:bg-primary-50/70'}
          ${disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'}
        `}
        title="切换模式"
        aria-haspopup="menu"
        aria-expanded={isOpen}
      >
        <span
          className={`flex items-center justify-center ${compact ? 'w-6.5 h-6.5' : 'w-8 h-8'} rounded-full ${MODE_CONFIG[mode].badgeClass}`}
        >
          <CurrentIcon className={`${compact ? 'w-3.5 h-3.5' : 'w-4 h-4'} text-current`} />
        </span>
        <span className="text-gray-900">{MODE_CONFIG[mode].label}</span>
        <ChevronDown className={`w-4 h-4 text-gray-500 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* 下拉菜单 - 向上弹出 */}
      {isOpen && (
        <>
          {/* 遮罩层 */}
          <div className="fixed inset-0 z-10" onClick={() => setIsOpen(false)} />

          {/* 菜单内容 - 轻量明亮主题 */}
          <div className="absolute left-0 bottom-full mb-2 z-20 w-64 rounded-xl border border-gray-200 bg-white shadow-xl overflow-hidden">
            <div className="p-1">
              {(['planning', 'react'] as AgentMode[]).map((item) => {
                const ItemIcon = MODE_CONFIG[item].icon;
                const isActive = mode === item;

                return (
                  <button
                    key={item}
                    onClick={() => handleModeClick(item)}
                    className={`
                      w-full flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg transition-colors
                      ${isActive ? 'bg-primary-50 border border-primary-100' : 'hover:bg-gray-50'}
                    `}
                  >
                    <div className="flex items-center gap-3 text-left">
                      <div className={`flex items-center justify-center w-9 h-9 rounded-full ${MODE_CONFIG[item].badgeClass}`}>
                        <ItemIcon className="w-4 h-4 text-current" />
                      </div>
                      <div className="flex flex-col">
                        <span className="text-sm font-medium text-gray-900">{MODE_CONFIG[item].label}</span>
                        <span className="text-xs text-gray-500">{MODE_CONFIG[item].description}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-gray-500">
                      {item === 'planning' && <span className="text-gray-400">默认</span>}
                      {isActive && <Check className="w-4 h-4 text-primary-600" />}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

// 导出配置供其他组件使用
export { MODE_CONFIG };
