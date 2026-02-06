/**
 * BudgetCard - Agentic 预算卡片
 */

import type { BudgetFlowData } from '@/types/agent';

interface BudgetCardProps extends BudgetFlowData {}

export function BudgetCard({ budget }: BudgetCardProps) {
  const maxSteps = budget?.max_steps ?? 0;
  const usedSteps = budget?.used_steps ?? 0;
  const maxCost = budget?.max_cost ?? 0;
  const usedCost = budget?.used_cost ?? 0;
  const maxTimeMs = budget?.max_time_ms ?? 0;

  return (
    <div className="mb-3 ml-[26px] text-[12px] text-gray-500 dark:text-slate-400">
      <div className="inline-flex items-center gap-2 px-2.5 py-1 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-full">
        <span>预算</span>
        <span className="font-mono">步数 {usedSteps}/{maxSteps || '-'}</span>
        <span className="font-mono">成本 {usedCost}/{maxCost || '-'}</span>
        <span className="font-mono">时限 {Math.round(maxTimeMs / 1000)}s</span>
      </div>
    </div>
  );
}

