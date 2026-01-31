/**
 * Agent 会话数据压缩工具
 * 用于减少 localStorage 存储占用
 */

import type { Message } from '@/types/agent';
import type { FlowItem } from '@/types/agent';

interface CompressionStats {
  originalSize: number;
  compressedSize: number;
  ratio: number;
  itemsRemoved: number;
}

/**
 * 压缩 flowItems 数据
 * 策略：
 * 1. 移除 Explore 工具的详细检索结果（保留摘要）
 * 2. 移除工具调用的详细参数（保留关键信息）
 * 3. 压缩长文本内容
 * 4. 移除冗余的 metadata
 */
export function compressFlowItems(flowItems: FlowItem[] | undefined): FlowItem[] | undefined {
  if (!flowItems || flowItems.length === 0) return flowItems;

  return flowItems.map((item) => {
    const compressed = { ...item };

    switch (item.type) {
      case 'explore_round': {
        const data = item.data as any;
        // 保留摘要，移除详细的检索结果
        if (data.results && Array.isArray(data.results)) {
          compressed.data = {
            ...data,
            results: data.results.slice(0, 3).map((r: any) => ({
              title: r.title,
              score: r.score,
              // 移除 content 字段（通常很长）
            })),
            _compressed: true,
          };
        }
        break;
      }

      case 'tool': {
        const data = item.data as any;
        // 压缩工具参数
        if (data.params) {
          const compressedParams: any = {};
          // 只保留关键参数
          const keepKeys = ['query', 'type', 'limit', 'filter'];
          keepKeys.forEach((key) => {
            if (data.params[key] !== undefined) {
              compressedParams[key] = data.params[key];
            }
          });
          compressed.data = {
            ...data,
            params: compressedParams,
            _compressed: true,
          };
        }

        // 压缩输出结果
        if (data.output && typeof data.output === 'string') {
          if (data.output.length > 500) {
            compressed.data = {
              ...compressed.data,
              output: data.output.substring(0, 500) + '... (已截断)',
              _compressed: true,
            };
          }
        }
        break;
      }

      case 'content': {
        const data = item.data as any;
        // 压缩长文本内容
        if (data.content && typeof data.content === 'string') {
          if (data.content.length > 1000) {
            compressed.data = {
              ...data,
              content: data.content.substring(0, 1000) + '... (已截断)',
              _compressed: true,
            };
          }
        }
        break;
      }

      case 'step': {
        const data = item.data as any;
        // 移除详细的步骤数据，只保留摘要
        compressed.data = {
          title: data.title,
          status: data.status,
          stepId: data.stepId,
          _compressed: true,
        };
        break;
      }

      default:
        // 其他类型保持不变
        break;
    }

    return compressed;
  });
}

/**
 * 压缩消息数据（用于历史会话）
 * 对于非当前会话，可以更激进地压缩
 */
export function compressMessage(message: Message, isCurrentSession: boolean): Message {
  const compressed = { ...message };

  // 对于历史会话，移除 flowItems
  if (!isCurrentSession) {
    compressed.flowItems = undefined;
    // 也可以移除 agentSteps 中的详细数据
    if (compressed.agentSteps) {
      compressed.agentSteps = compressed.agentSteps.map((step) => ({
        ...step,
        // 移除详细的 raw 数据
        raw: undefined,
      }));
    }
  } else {
    // 对于当前会话，压缩 flowItems
    compressed.flowItems = compressFlowItems(message.flowItems);
  }

  // 压缩长消息内容
  if (compressed.content && compressed.content.length > 10000) {
    compressed.content = compressed.content.substring(0, 10000) + '\n\n... (内容过长已截断)';
  }

  return compressed;
}

/**
 * 批量压缩会话消息
 */
export function compressSessionMessages(
  messages: Message[],
  currentSessionId: string,
  sessionId: string
): Message[] {
  const isCurrentSession = currentSessionId === sessionId;
  return messages.map((msg) => compressMessage(msg, isCurrentSession));
}

/**
 * 计算数据大小（字节）
 */
function calculateSize(data: any): number {
  return new Blob([JSON.stringify(data)]).size;
}

/**
 * 分析压缩效果
 */
export function analyzeCompression(
  original: Message[],
  compressed: Message[]
): CompressionStats {
  const originalSize = calculateSize(original);
  const compressedSize = calculateSize(compressed);

  // 计算移除的 flowItems 数量
  const originalItems = original.reduce(
    (sum, msg) => sum + (msg.flowItems?.length || 0),
    0
  );
  const compressedItems = compressed.reduce(
    (sum, msg) => sum + (msg.flowItems?.length || 0),
    0
  );

  return {
    originalSize,
    compressedSize,
    ratio: compressedSize / originalSize,
    itemsRemoved: originalItems - compressedItems,
  };
}

/**
 * 自动压缩策略
 * 根据存储使用情况自动选择压缩级别
 */
export function autoCompressMessages(
  messages: Message[],
  storageUsagePercent: number,
  isCurrentSession: boolean
): Message[] {
  // 使用率 < 50%: 不压缩
  if (storageUsagePercent < 50) {
    return messages;
  }

  // 使用率 50-80%: 轻度压缩（压缩 flowItems）
  if (storageUsagePercent < 80) {
    return messages.map((msg) => ({
      ...msg,
      flowItems: compressFlowItems(msg.flowItems),
    }));
  }

  // 使用率 > 80%: 重度压缩（移除历史会话的 flowItems）
  return messages.map((msg) => compressMessage(msg, isCurrentSession));
}

/**
 * 在开发模式下暴露到全局
 */
if (import.meta.env.DEV) {
  (window as any).sessionCompression = {
    compress: compressSessionMessages,
    analyze: analyzeCompression,
    compressFlowItems,
  };
}
