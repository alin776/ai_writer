/**
 * ExecutionFlow - 执行轨迹可视化组件 (v7.1)
 *
 * 显示 AI 说明文字 + 执行步骤 + 工具卡片 + 最终输出 + 修订卡片
 * 支持知识调取容器、可折叠步骤、输出卡片、修订胶囊、批量修订管理
 */

import { useMemo } from 'react';
import { CheckCheck, XCircle } from 'lucide-react';
import type { FlowItem, TextFlowData, ToolFlowData, ContentFlowData, StepFlowData, OutputFlowData, AgentHeaderFlowData, CompletionFlowData, SummarizationFlowData, RevisionFlowData } from '@/types/agent';
import { TextBlock } from './TextBlock';
import { ToolCard } from './ToolCard';
import { ContentBlock } from './ContentBlock';
import { StepCard } from './StepCard';
import { OutputCard } from './OutputCard';
import { AgentHeader } from './AgentHeader';
import { CompletionStatus } from './CompletionStatus';
import { SummarizationCard } from './SummarizationCard';
import { RevisionCard } from './RevisionCard';

interface ExecutionFlowProps {
  items: FlowItem[];
  onApplyContent?: (content: string) => void;
  onAcceptRevision?: (itemId: string, requestId: string | undefined, selectedVersion?: number) => void;
  onDiscardRevision?: (itemId: string, requestId: string | undefined) => void;
  onAcceptAllRevisions?: (itemIds: string[]) => void;
  onDiscardAllRevisions?: (itemIds: string[]) => void;
  // v7.2: 撤销/重做回调
  onUndoRevision?: (itemId: string) => void;
  onRedoRevision?: (itemId: string) => void;
}

export function ExecutionFlow({
  items,
  onApplyContent,
  onAcceptRevision,
  onDiscardRevision,
  onAcceptAllRevisions,
  onDiscardAllRevisions,
  onUndoRevision,
  onRedoRevision
}: ExecutionFlowProps) {
  // 统计 pending 状态的修订
  const pendingRevisions = useMemo(() => {
    return items.filter(
      item => item.type === 'revision' && (item.data as RevisionFlowData).status === 'pending'
    );
  }, [items]);

  const pendingCount = pendingRevisions.length;

  if (!items || items.length === 0) {
    return null;
  }

  return (
    <div>
      {/* 批量操作栏：当有多个 pending 修订时显示 */}
      {pendingCount > 1 && (
        <div className="flex items-center gap-2 mb-3 px-2 py-1.5 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg">
          <span className="text-[12px] text-amber-600 dark:text-amber-400">
            {pendingCount} 项待确认修订
          </span>
          <div className="flex gap-1.5 ml-auto">
            <button
              onClick={() => onDiscardAllRevisions?.(pendingRevisions.map(r => r.id))}
              className="flex items-center gap-1 px-2 py-0.5 text-[11px] text-gray-500 dark:text-slate-400 bg-gray-100 dark:bg-slate-700 rounded-full hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors"
            >
              <XCircle size={11} />
              全部弃用
            </button>
            <button
              onClick={() => onAcceptAllRevisions?.(pendingRevisions.map(r => r.id))}
              className="flex items-center gap-1 px-2 py-0.5 text-[11px] text-white bg-blue-500 rounded-full hover:bg-blue-600 transition-colors"
            >
              <CheckCheck size={11} />
              全部采纳
            </button>
          </div>
        </div>
      )}

      {items.map((item) => {
        switch (item.type) {
          case 'text':
            // 不渲染 TextBlock，只保留 StepCard
            return null;
          case 'tool':
            // 不渲染 ToolCard，只保留 StepCard
            return null;
          case 'content':
            return (
              <ContentBlock
                key={item.id}
                content={(item.data as ContentFlowData).content}
              />
            );
          case 'step':
            return (
              <StepCard
                key={item.id}
                {...(item.data as StepFlowData)}
              />
            );
          case 'output':
            return (
              <OutputCard
                key={item.id}
                {...(item.data as OutputFlowData)}
                onApply={onApplyContent ? () => onApplyContent((item.data as OutputFlowData).content) : undefined}
              />
            );
          case 'agent_header':
            return (
              <AgentHeader
                key={item.id}
                {...(item.data as AgentHeaderFlowData)}
              />
            );
          case 'completion':
            return (
              <CompletionStatus
                key={item.id}
                {...(item.data as CompletionFlowData)}
              />
            );
          case 'summarization':
            return (
              <SummarizationCard
                key={item.id}
                {...(item.data as SummarizationFlowData)}
              />
            );
          case 'revision': {
            const revisionData = item.data as RevisionFlowData;
            return (
              <RevisionCard
                key={item.id}
                {...revisionData}
                onAccept={(selectedVersion) => onAcceptRevision?.(item.id, revisionData.requestId, selectedVersion)}
                onDiscard={() => onDiscardRevision?.(item.id, revisionData.requestId)}
                onUndo={() => onUndoRevision?.(item.id)}
                onRedo={() => onRedoRevision?.(item.id)}
              />
            );
          }
          default:
            return null;
        }
      })}
    </div>
  );
}

export default ExecutionFlow;
