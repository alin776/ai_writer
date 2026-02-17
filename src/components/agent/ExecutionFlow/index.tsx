/**
 * ExecutionFlow - 执行轨迹可视化组件 (V2 - Claude Code 风格)
 *
 * 线性对话流：工具调用压缩为单行 ToolLine，文本内联，
 * 仅保留 RevisionCard 和审批按钮。
 */

import type { FlowItem, StepFlowData, OutputFlowData, RevisionFlowData, CompletionFlowData, TodoFlowData, TextFlowData } from '@/types/agent';
import { ToolLine } from './ToolLine';
import { TodoBlock } from './TodoBlock';
import { OutputCard } from './OutputCard';
import { RevisionCard } from './RevisionCard';
import { Streamdown } from 'streamdown';
import { code } from '@streamdown/code';
import { cjk } from '@streamdown/cjk';

interface ExecutionFlowProps {
  items: FlowItem[];
  isStreaming?: boolean;
  onApplyContent?: (content: string) => void;
  onAddToKnowledge?: (title: string, content: string) => void;
  onAcceptRevision?: (itemId: string, requestId: string | undefined, selectedVersion?: number) => void;
  onDiscardRevision?: (itemId: string, requestId: string | undefined) => void;
  onJumpRevision?: (itemId: string, requestId: string | undefined) => void;
  onAcceptAllRevisions?: (itemIds: string[]) => void;
  onDiscardAllRevisions?: (itemIds: string[]) => void;
  onUndoRevision?: (itemId: string) => void;
}

export function ExecutionFlow({
  items,
  isStreaming,
  onApplyContent,
  onAddToKnowledge,
  onAcceptRevision,
  onDiscardRevision,
  onJumpRevision,
  onAcceptAllRevisions,
  onDiscardAllRevisions,
  onUndoRevision
}: ExecutionFlowProps) {
  if (!items || items.length === 0) {
    return null;
  }

  return (
    <div className="space-y-1">
      {items.map((item) => {
        switch (item.type) {
          case 'step': {
            const stepData = item.data as StepFlowData;
            const revisionId = stepData.revisionItemId || item.id;
            return (
              <ToolLine key={item.id} {...stepData}>
                {/* 内嵌的 RevisionCard */}
                {stepData.revision && (
                  <RevisionCard
                    {...stepData.revision}
                    onAccept={(selectedVersion) => onAcceptRevision?.(revisionId, (stepData.revision as any)?.requestId, selectedVersion)}
                    onDiscard={() => onDiscardRevision?.(revisionId, (stepData.revision as any)?.requestId)}
                    onUndo={() => onUndoRevision?.(revisionId)}
                    onJump={() => onJumpRevision?.(revisionId, (stepData.revision as any)?.requestId)}
                  />
                )}
              </ToolLine>
            );
          }

          case 'todo': {
            const todoData = item.data as TodoFlowData;
            return <TodoBlock key={item.id} {...todoData} />;
          }

          case 'text': {
            const textData = item.data as TextFlowData;
            if (!textData.content) return null;
            // 防御：LLM chunk.content 可能是对象（如工具调用中间态），确保只渲染字符串
            const textContent = typeof textData.content === 'string' ? textData.content : String(textData.content);
            return (
              <div key={item.id} className="text-base text-gray-700 dark:text-gray-300 leading-relaxed">
                <Streamdown mode="static" plugins={{ code, cjk }}>
                  {textContent}
                </Streamdown>
              </div>
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

          case 'revision': {
            const revisionData = item.data as RevisionFlowData;
            return (
              <RevisionCard
                key={item.id}
                {...revisionData}
                onAccept={(selectedVersion) => onAcceptRevision?.(item.id, revisionData.requestId, selectedVersion)}
                onDiscard={() => onDiscardRevision?.(item.id, revisionData.requestId)}
                onUndo={() => onUndoRevision?.(item.id)}
                onJump={() => onJumpRevision?.(item.id, revisionData.requestId)}
              />
            );
          }

          case 'completion': {
            const completionData = item.data as CompletionFlowData;
            return (
              <div key={item.id} className="flex items-center gap-2 py-1 text-base font-mono text-emerald-600 dark:text-emerald-400">
                <span>✓</span>
                <span>{completionData.text || '任务已完成'}</span>
              </div>
            );
          }

          case 'agent_header':
            // 极简：不渲染独立 header，由 AIPanel 控制
            return null;

          // V1 遗留类型 — 兼容旧消息，不报错
          case 'summarization':
          case 'explore_round':
          case 'explore_summary':
          case 'operate':
          case 'tool':
          case 'content':
          default:
            return null;
        }
      })}

      {/* Thinking 指示器：仅在「静默期」显示
          - isStreaming: Agent 仍在运行
          - 最后一项不是 completion（任务未完成）
          - 最后一项不是 text（LLM 不在输出文字）
          - 没有正在执行的工具（running 状态的 step）
       */}
      {isStreaming
        && items[items.length - 1]?.type !== 'completion'
        && items[items.length - 1]?.type !== 'text'
        && !items.some(i => i.type === 'step' && (i.data as StepFlowData).status === 'running')
        && (
        <div className="flex items-center gap-2 py-0.5 text-base font-mono text-gray-500 dark:text-gray-400">
          <span className="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse flex-shrink-0" />
          <span>Working...</span>
        </div>
      )}
    </div>
  );
}

export default ExecutionFlow;
