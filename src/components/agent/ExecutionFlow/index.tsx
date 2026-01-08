/**
 * ExecutionFlow - 执行轨迹可视化组件 (v6.0)
 *
 * 显示 AI 说明文字 + 执行步骤 + 工具卡片 + 最终输出
 * 支持知识调取容器、可折叠步骤、输出卡片
 */

import type { FlowItem, TextFlowData, ToolFlowData, ContentFlowData, StepFlowData, OutputFlowData, AgentHeaderFlowData, CompletionFlowData, SummarizationFlowData } from '@/types/agent';
import { TextBlock } from './TextBlock';
import { ToolCard } from './ToolCard';
import { ContentBlock } from './ContentBlock';
import { StepCard } from './StepCard';
import { OutputCard } from './OutputCard';
import { AgentHeader } from './AgentHeader';
import { CompletionStatus } from './CompletionStatus';
import { SummarizationCard } from './SummarizationCard';

interface ExecutionFlowProps {
  items: FlowItem[];
  onApplyContent?: (content: string) => void;
}

export function ExecutionFlow({ items, onApplyContent }: ExecutionFlowProps) {
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
          default:
            return null;
        }
      })}
    </div>
  );
}

export default ExecutionFlow;
