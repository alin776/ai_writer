/**
 * Agent 会话数据压缩工具 v2
 * 修复版本：正确匹配数据结构，确保类型安全
 */

import type {
  Message,
  FlowItem,
  ExploreRoundFlowData,
  ToolFlowData,
  ContentFlowData,
} from '@/types/agent';

interface CompressionStats {
  originalSize: number;
  compressedSize: number;
  ratio: number;
  itemsRemoved: number;
}

/**
 * 压缩 flowItems 数据
 *
 * @param flowItems 要压缩的 flowItems
 * @param isCurrentSession 是否是当前会话
 * @returns 压缩后的 flowItems
 */
export function compressFlowItems(
  flowItems: FlowItem[] | undefined,
  isCurrentSession: boolean
): FlowItem[] | undefined {
  if (!flowItems || flowItems.length === 0) return flowItems;

  // 对于非当前会话，完全移除 flowItems（最激进的压缩）
  if (!isCurrentSession) {
    return undefined;
  }

  // 对于当前会话，选择性压缩
  return flowItems.map((item) => {
    const compressed = { ...item };

    switch (item.type) {
      case 'explore_round': {
        const data = item.data as ExploreRoundFlowData;

        // ✅ 修复：正确压缩 evidences（这是占用空间最大的部分）
        compressed.data = {
          ...data,
          // 只保留前 5 个证据片段
          evidences: data.evidences?.slice(0, 5) || [],
          // toolCalls 保持不变（占用空间小，且UI需要显示）
        } as ExploreRoundFlowData;
        break;
      }

      case 'tool': {
        const data = item.data as ToolFlowData;

        // 压缩长输出
        if (data.output && typeof data.output === 'string' && data.output.length > 1000) {
          compressed.data = {
            ...data,
            output: data.output.substring(0, 1000) + '\n\n...(已截断，完整内容请查看当前会话)',
          } as ToolFlowData;
        }
        break;
      }

      case 'content': {
        const data = item.data as ContentFlowData;

        // 压缩长文本
        if (data.content && data.content.length > 2000) {
          compressed.data = {
            ...data,
            content: data.content.substring(0, 2000) + '\n\n...(已截断，完整内容请查看当前会话)',
          } as ContentFlowData;
        }
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
 * 压缩单条消息
 *
 * @param message 要压缩的消息
 * @param isCurrentSession 是否是当前会话
 * @returns 压缩后的消息
 */
export function compressMessage(
  message: Message,
  isCurrentSession: boolean
): Message {
  const compressed = { ...message };

  // 压缩策略：
  // - 当前会话：保留 flowItems，只压缩长内容
  // - 历史会话：完全移除 flowItems，节省 90% 空间

  if (!isCurrentSession) {
    // 历史会话：移除 flowItems 和 tasksSnapshot
    compressed.flowItems = undefined;
    compressed.tasksSnapshot = undefined;

    // 保留 content 和 agentSteps 的摘要
    if (compressed.agentSteps) {
      compressed.agentSteps = compressed.agentSteps.map((step) => ({
        ...step,
        // 移除详细的 raw 数据
        raw: undefined,
      }));
    }
  } else {
    // 当前会话：压缩 flowItems
    compressed.flowItems = compressFlowItems(message.flowItems, true);
  }

  // 压缩长消息内容（无论当前还是历史会话）
  if (compressed.content && compressed.content.length > 10000) {
    compressed.content = compressed.content.substring(0, 10000) + '\n\n...(内容过长已截断)';
  }

  return compressed;
}

/**
 * 批量压缩会话消息
 *
 * @param messages 消息列表
 * @param isCurrentSession 是否是当前会话
 * @returns 压缩后的消息列表
 */
export function compressSessionMessages(
  messages: Message[],
  isCurrentSession: boolean
): Message[] {
  return messages.map((msg) => compressMessage(msg, isCurrentSession));
}

/**
 * 计算数据大小（字节）
 */
function calculateSize(data: any): number {
  try {
    return new Blob([JSON.stringify(data)]).size;
  } catch {
    return 0;
  }
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
    ratio: originalSize > 0 ? compressedSize / originalSize : 1,
    itemsRemoved: originalItems - compressedItems,
  };
}

/**
 * 自动压缩策略
 * 根据存储使用情况自动选择压缩级别
 *
 * @param messages 消息列表
 * @param storageUsagePercent 存储使用率（0-100）
 * @param isCurrentSession 是否是当前会话
 * @returns 压缩后的消息列表
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

  // 使用率 50-80%: 轻度压缩（只压缩 flowItems）
  if (storageUsagePercent < 80) {
    if (isCurrentSession) {
      return messages.map((msg) => ({
        ...msg,
        flowItems: compressFlowItems(msg.flowItems, true),
      }));
    }
    return messages;
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
    autoCompress: autoCompressMessages,
  };
}
