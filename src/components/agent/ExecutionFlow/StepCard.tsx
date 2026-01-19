/**
 * StepCard - 执行步骤卡片组件
 * 可折叠，显示状态图标、知识调取、工具调用、内嵌修订胶囊
 */

import { useState, type ReactNode } from 'react';
import { Check, Loader2, ChevronUp, ChevronDown, Wrench } from 'lucide-react';
import type { StepFlowData } from '@/types/agent';
import { KnowledgeContainer } from './KnowledgeContainer';
import { RevisionCard } from './RevisionCard';

interface StepCardProps extends StepFlowData {
  defaultExpanded?: boolean;
  children?: ReactNode;
  // v7.3: 修订回调（从 ExecutionFlow 传入）
  onAcceptRevision?: (selectedVersion?: number) => void;
  onDiscardRevision?: () => void;
  onUndoRevision?: () => void;
  onRedoRevision?: () => void;
  onJumpRevision?: () => void;
}

export function StepCard({
  title,
  status,
  description,
  knowledge,
  toolCall,
  children,
  revision,
  defaultExpanded = true,
  onAcceptRevision,
  onDiscardRevision,
  onUndoRevision,
  onRedoRevision,
  onJumpRevision
}: StepCardProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);
  const showToolCall = toolCall && toolCall.name !== 'explore_content';

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
          ) : status === 'done' ? (
            <Check size={12} className="text-gray-500" />
          ) : (
            <span className="w-2 h-2 rounded-full bg-red-500" />
          )}
        </div>

        {/* 标题区域 */}
        <div className="flex items-center gap-1.5">
          <span className="text-[14px] font-medium text-gray-900 dark:text-white">{title}</span>
          <span className="text-gray-400 dark:text-slate-600 text-[10px]">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>

        <div className="flex-1" />
      </div>

      {/* 步骤内容 */}
      {expanded && (
        <div className="ml-[26px] pt-1">
          {/* 知识调取 */}
          {knowledge && knowledge.length > 0 && (
            <div className="mb-2">
              {knowledge.map((k, index) => (
                <KnowledgeContainer key={index} {...k} />
              ))}
            </div>
          )}

          {/* 步骤描述 */}
          {description && (
            <div className="text-[13px] text-gray-500 dark:text-slate-300 my-2 leading-[1.6]">
              {description}
            </div>
          )}

          {/* 工具调用标签 */}
          {showToolCall && (
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-full my-2">
              <span className="text-gray-400 dark:text-slate-500">
                <Wrench size={12} />
              </span>
              <span className="text-[13px] text-gray-500 dark:text-slate-400">调用工具</span>
              <span className="font-mono text-[12px] text-gray-600 dark:text-slate-300">
                {toolCall.name}
              </span>
            </div>
          )}

          {children && (
            <div className="mt-2">
              {children}
            </div>
          )}

          {/* v7.3: 内嵌修订胶囊 */}
          {revision && (
            <div className="mt-2">
              <RevisionCard
                {...revision}
                onAccept={onAcceptRevision}
                onDiscard={onDiscardRevision}
                onUndo={onUndoRevision}
                onRedo={onRedoRevision}
                onJump={onJumpRevision}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
