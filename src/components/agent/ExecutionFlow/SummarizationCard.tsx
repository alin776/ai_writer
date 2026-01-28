/**
 * SummarizationCard - AI整合分析卡片组件
 * 显示任务分类和上下文处理信息
 */

import { useState } from 'react';
import { Check, Loader2, ChevronUp, ChevronDown, Wrench } from 'lucide-react';
import type { SummarizationFlowData } from '@/types/agent';

interface SummarizationCardProps extends SummarizationFlowData {
  defaultExpanded?: boolean;
}

export function SummarizationCard({
  status,
  reason,
  defaultExpanded = true
}: SummarizationCardProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);
  // 保留接口字段但不展示详细胶囊

  return (
    <div className="mb-3">
      {/* 步骤头部 */}
      <div
        className="flex items-center gap-2 py-1.5 cursor-pointer select-none"
        onClick={() => setExpanded(!expanded)}
      >
        {/* 状态图标 */}
        <div className="w-[18px] h-[18px] flex items-center justify-center">
          {status === 'running' ? (
            <Loader2 size={12} className="text-blue-500 animate-spin" />
          ) : (
            <Check size={12} className="text-gray-500" />
          )}
        </div>

        {/* 标题区域 */}
        <div className="flex items-center gap-1.5">
          <span className="text-[14px] font-medium text-gray-900 dark:text-white">AI整合分析</span>
          <span className="text-gray-400 dark:text-slate-600 text-[10px]">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>

        <div className="flex-1" />
      </div>

      {/* 步骤内容 */}
      {expanded && (
        <div className="ml-[26px] pt-1">
          {reason && (
            <div className="mb-2 text-[13px] text-gray-600 dark:text-slate-300 leading-[1.6]">
              {reason}
            </div>
          )}
          {/* 工具调用标签 */}
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-full my-2">
            <span className="text-gray-400 dark:text-slate-500">
              <Wrench size={12} />
            </span>
            <span className="text-[13px] text-gray-500 dark:text-slate-400">调用工具</span>
            <span className="font-mono text-[12px] text-gray-600 dark:text-slate-300">
              response_builder.summarize
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
