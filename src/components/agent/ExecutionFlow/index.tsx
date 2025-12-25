/**
 * ExecutionFlow - 执行轨迹可视化组件 (v5.0)
 *
 * 显示 AI 说明文字 + 工具卡片交织的执行轨迹
 * 样式复用 ActivityStream 风格
 */

import type { FlowItem, TextFlowData, ToolFlowData, ContentFlowData } from '@/types/agent';
import { TextBlock } from './TextBlock';
import { ToolCard } from './ToolCard';
import { ContentBlock } from './ContentBlock';

interface ExecutionFlowProps {
  items: FlowItem[];
}

export function ExecutionFlow({ items }: ExecutionFlowProps) {
  if (!items || items.length === 0) {
    return null;
  }

  return (
    <div>
      {items.map((item) => {
        switch (item.type) {
          case 'text':
            return (
              <TextBlock
                key={item.id}
                content={(item.data as TextFlowData).content}
              />
            );
          case 'tool':
            return (
              <ToolCard
                key={item.id}
                {...(item.data as ToolFlowData)}
              />
            );
          case 'content':
            return (
              <ContentBlock
                key={item.id}
                content={(item.data as ContentFlowData).content}
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
