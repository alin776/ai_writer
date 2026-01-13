/**
 * ExecutionFlow - 执行轨迹可视化组件 (v7.1)
 *
 * 显示 AI 说明文字 + 执行步骤 + 工具卡片 + 最终输出 + 修订卡片
 * 支持知识调取容器、可折叠步骤、输出卡片、修订胶囊、批量修订管理
 */

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
  onAddToKnowledge?: (title: string, content: string) => void;
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
  onAddToKnowledge,
  onAcceptRevision,
  onDiscardRevision,
  onAcceptAllRevisions,
  onDiscardAllRevisions,
  onUndoRevision,
  onRedoRevision
}: ExecutionFlowProps) {
  if (!items || items.length === 0) {
    return null;
  }

  return (
    <div>
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
          case 'step': {
            const stepData = item.data as StepFlowData;
            // v7.4: 使用 item.id 作为 fallback，确保回调函数始终有效
            const revisionId = stepData.revisionItemId || item.id;
            return (
              <StepCard
                key={item.id}
                {...stepData}
                // v7.3: 传递修订回调给 StepCard（用于内嵌的 RevisionCard）
                onAcceptRevision={stepData.revision ? (selectedVersion) => onAcceptRevision?.(revisionId, (stepData.revision as any)?.requestId, selectedVersion) : undefined}
                onDiscardRevision={stepData.revision ? () => onDiscardRevision?.(revisionId, (stepData.revision as any)?.requestId) : undefined}
                onUndoRevision={stepData.revision ? () => onUndoRevision?.(revisionId) : undefined}
                onRedoRevision={stepData.revision ? () => onRedoRevision?.(revisionId) : undefined}
              />
            );
          }
          case 'output':
            return (
              <OutputCard
                key={item.id}
                {...(item.data as OutputFlowData)}
                onApply={onApplyContent ? () => onApplyContent((item.data as OutputFlowData).content) : undefined}
                onAddToKnowledge={onAddToKnowledge ? () => onAddToKnowledge(
                  (item.data as OutputFlowData).title,
                  (item.data as OutputFlowData).content
                ) : undefined}
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
