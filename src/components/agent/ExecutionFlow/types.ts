/**
 * ExecutionFlow 类型定义
 */

export type FlowItemType = 'text' | 'tool' | 'content';

export interface TextFlowItem {
  type: 'text';
  id: string;
  content: string;
  node?: string;
  timestamp: string;
}

export interface ToolFlowItem {
  type: 'tool';
  id: string;
  tool_name: string;
  icon: string;
  title: string;
  description: string;
  status: 'running' | 'done' | 'error';
  timestamp: string;
}

export interface ContentFlowItem {
  type: 'content';
  id: string;
  content: string;
  timestamp: string;
}

export type FlowItem = TextFlowItem | ToolFlowItem | ContentFlowItem;

export interface ExecutionFlowProps {
  items: FlowItem[];
  className?: string;
}

export interface TextBlockProps {
  content: string;
}

export interface ToolCardProps {
  icon: string;
  title: string;
  description: string;
  status: 'running' | 'done' | 'error';
}

export interface ContentBlockProps {
  content: string;
}
