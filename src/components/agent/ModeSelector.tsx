/**
 * ModeSelector - Agent 模式选择器
 *
 * 支持两种模式：
 * - Plan: 纯规划执行（planning + enable_reflection=false）
 * - Agent: 规划 + DeepAgent 反思（planning + enable_reflection=true）
 *
 * 参考 Cursor 风格的胶囊按钮
 */

import React from 'react';
import { Check, ChevronDown, Sparkles, Workflow } from 'lucide-react';

export type AgentMode = 'plan' | 'agent';

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
  badgeClassDark: string;
}

const MODE_CONFIG: Record<AgentMode, ModeConfig> = {
  plan: {
    label: 'Plan',
    icon: Workflow,
    description: '规划执行，任务列表固定',
    badgeClass: 'bg-primary-50 text-primary-700 ring-1 ring-primary-100',
    badgeClassDark: 'dark:bg-blue-900/50 dark:text-blue-300 dark:ring-blue-800',
  },
  agent: {
    label: 'Agent',
    icon: Sparkles,
    description: 'DeepAgent 反思，可动态调整',
    badgeClass: 'bg-emerald-50 text-emerald-700 ring-1 ring-emerald-100',
    badgeClassDark: 'dark:bg-emerald-900/50 dark:text-emerald-300 dark:ring-emerald-800',
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
          inline-flex items-center gap-1.5 rounded-full
          border text-xs font-medium transition-all shadow-sm
          ${compact ? 'px-2 py-1 h-7' : 'px-2.5 py-1.5 h-8'}
          ${isOpen
            ? 'border-primary-200 bg-primary-50/80 dark:border-blue-700 dark:bg-blue-900/30'
            : 'border-gray-200 bg-white/90 hover:border-primary-200 hover:bg-primary-50/70 dark:border-slate-600 dark:bg-slate-700 dark:hover:border-blue-600 dark:hover:bg-slate-600'}
          ${disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'}
        `}
        title="切换模式"
        aria-haspopup="menu"
        aria-expanded={isOpen}
      >
        <span
          className={`flex items-center justify-center ${compact ? 'w-5 h-5' : 'w-5.5 h-5.5'} rounded-full ${MODE_CONFIG[mode].badgeClass} ${MODE_CONFIG[mode].badgeClassDark}`}
        >
          <CurrentIcon className={`${compact ? 'w-3 h-3' : 'w-3 h-3'} text-current`} />
        </span>
        <span className="text-gray-900 dark:text-slate-100">{MODE_CONFIG[mode].label}</span>
        <ChevronDown className={`w-3 h-3 text-gray-500 dark:text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* 下拉菜单 - 向上弹出 */}
      {isOpen && (
        <>
          {/* 遮罩层 */}
          <div className="fixed inset-0 z-10" onClick={() => setIsOpen(false)} />

          {/* 菜单内容 - 支持深色模式 */}
          <div className="absolute left-0 bottom-full mb-2 z-20 w-64 rounded-xl border border-gray-200 bg-white shadow-xl overflow-hidden dark:border-slate-600 dark:bg-slate-800">
            <div className="p-1">
              {(['plan', 'agent'] as AgentMode[]).map((item) => {
                const ItemIcon = MODE_CONFIG[item].icon;
                const isActive = mode === item;

                return (
                  <button
                    key={item}
                    onClick={() => handleModeClick(item)}
                    className={`
                      w-full flex items-center justify-between gap-2.5 px-2.5 py-2 rounded-lg transition-colors
                      ${isActive
                        ? 'bg-primary-50 border border-primary-100 dark:bg-blue-900/30 dark:border-blue-800'
                        : 'hover:bg-gray-50 dark:hover:bg-slate-700'}
                    `}
                  >
                    <div className="flex items-center gap-2.5 text-left">
                      <div className={`flex items-center justify-center w-7 h-7 rounded-full ${MODE_CONFIG[item].badgeClass} ${MODE_CONFIG[item].badgeClassDark}`}>
                        <ItemIcon className="w-3.5 h-3.5 text-current" />
                      </div>
                      <div className="flex flex-col">
                        <span className="text-xs font-medium text-gray-900 dark:text-slate-100">{MODE_CONFIG[item].label}</span>
                        <span className="text-[11px] text-gray-500 dark:text-slate-400 leading-tight">{MODE_CONFIG[item].description}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-1.5 text-[11px] text-gray-500 dark:text-slate-400">
                      {item === 'plan' && <span className="text-gray-400 dark:text-slate-500">默认</span>}
                      {isActive && <Check className="w-3.5 h-3.5 text-primary-600 dark:text-blue-400" />}
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
