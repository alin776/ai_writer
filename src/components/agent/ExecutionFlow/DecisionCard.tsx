/**
 * DecisionCard - Agentic 决策卡片
 */

import { useState } from 'react';
import { Check, Loader2, ChevronUp, ChevronDown } from 'lucide-react';
import type { DecisionFlowData } from '@/types/agent';

interface DecisionCardProps extends DecisionFlowData {
  defaultExpanded?: boolean;
}

export function DecisionCard({
  status,
  goal,
  reason,
  candidates = [],
  decision,
  defaultExpanded = true
}: DecisionCardProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);
  const decisionId = decision?.id || decision?.identifier;
  const decisionReason = decision?.reason;
  const decisionRisk = decision?.risk;

  return (
    <div className="mb-3">
      <div
        className="flex items-center gap-2 py-1.5 cursor-pointer select-none"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="w-[18px] h-[18px] flex items-center justify-center">
          {status === 'running' ? (
            <Loader2 size={12} className="text-blue-500 animate-spin" />
          ) : (
            <Check size={12} className="text-gray-500" />
          )}
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-[14px] font-medium text-gray-900 dark:text-white">策略决策</span>
          <span className="text-gray-400 dark:text-slate-600 text-[10px]">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>
        <div className="flex-1" />
      </div>

      {expanded && (
        <div className="ml-[26px] pt-1 text-[13px] text-gray-600 dark:text-slate-300 leading-[1.6] space-y-1">
          <div>目标：{goal}</div>
          {reason && <div>原因：{reason}</div>}
          {decisionId && (
            <div>
              已选策略：{decisionId}
              {decisionRisk ? `（风险: ${decisionRisk}）` : ''}
            </div>
          )}
          {decisionReason && <div>裁决理由：{decisionReason}</div>}
          {candidates.length > 0 && (
            <div>
              候选策略：{candidates.map((c: any) => c.title || c.id || c.identifier).filter(Boolean).join(' / ')}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

