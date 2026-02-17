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
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

// 执行轨迹内 Markdown 的紧凑样式（比 AIPanel 更紧凑）
const markdownComponents = {
  p({ children }: any) {
    return <p className="mb-1 last:mb-0">{children}</p>;
  },
  h1({ children }: any) {
    return <h1 className="text-base font-bold mb-1 mt-2 first:mt-0">{children}</h1>;
  },
  h2({ children }: any) {
    return <h2 className="text-base font-semibold mb-1 mt-2 first:mt-0">{children}</h2>;
  },
  h3({ children }: any) {
    return <h3 className="text-sm font-medium mb-1 mt-1.5 first:mt-0">{children}</h3>;
  },
  ul({ children }: any) {
    return <ul className="list-disc list-outside pl-5 mb-1 space-y-0.5">{children}</ul>;
  },
  ol({ children }: any) {
    return <ol className="list-decimal list-outside pl-5 mb-1 space-y-0.5">{children}</ol>;
  },
  li({ children }: any) {
    return <li>{children}</li>;
  },
  strong({ children }: any) {
    return <strong className="font-semibold">{children}</strong>;
  },
  blockquote({ children }: any) {
    return <blockquote className="border-l-2 border-gray-300 dark:border-gray-600 pl-2 my-1 text-gray-500 dark:text-gray-400">{children}</blockquote>;
  },
  code({ inline, children, ...props }: any) {
    return inline
      ? <code className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded text-sm font-mono" {...props}>{children}</code>
      : <pre className="bg-gray-100 dark:bg-gray-800 p-2 rounded text-sm font-mono overflow-x-auto my-1" {...props}><code>{children}</code></pre>;
  },
  hr() {
    return <hr className="my-1.5 border-gray-200 dark:border-gray-700" />;
  },
};

interface ExecutionFlowProps {
  items: FlowItem[];
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
                <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
                  {textContent}
                </ReactMarkdown>
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
    </div>
  );
}

export default ExecutionFlow;
