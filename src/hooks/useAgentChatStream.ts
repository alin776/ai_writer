/**
 * Agent Chat Stream Hook
 *
 * 提供ReAct流式对话功能，支持实时进度显示
 */

import { useState, useCallback, useRef } from 'react';
import { agentApi } from '@/services/agentApi';
import type { AgentChatRequest } from '@/types/agent';

// 进度详情类型
export interface ProgressDetails {
  intent?: string;
  tools?: string[];
  [key: string]: any;  // 允许扩展
}

// 进度事件类型
export interface ProgressEvent {
  type: 'progress';
  step: 'intent_analysis' | 'thinking' | 'tool_execution';
  description: string;
  node?: string;
  details?: ProgressDetails;
  timestamp: string;
}

// 工具调用事件类型
export interface ToolCallEvent {
  tool: string;
  args: any;
  timestamp: string;
}

// Hook返回类型
export interface UseAgentChatStreamReturn {
  // 状态
  loading: boolean;
  error: Error | null;
  conversationId: string | null;

  // 实时进度
  currentProgress: ProgressEvent | null;
  progressHistory: ProgressEvent[];
  toolCalls: ToolCallEvent[];

  // 内容
  content: string;

  // 结果
  result: any | null;

  // 方法
  sendMessage: (message: string, options?: Partial<AgentChatRequest>) => Promise<void>;
  clearError: () => void;
  reset: () => void;
}

// Hook配置
export interface UseAgentChatStreamOptions {
  onProgress?: (progress: ProgressEvent) => void;
  onToolCall?: (toolCall: ToolCallEvent) => void;
  onContent?: (content: string) => void;
  onComplete?: (result: any) => void;
  onError?: (error: Error) => void;
}

/**
 * useAgentChatStream Hook
 *
 * 使用ReAct模式的流式Agent对话
 */
export function useAgentChatStream(
  options?: UseAgentChatStreamOptions
): UseAgentChatStreamReturn {
  // 状态
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);

  // 进度状态
  const [currentProgress, setCurrentProgress] = useState<ProgressEvent | null>(null);
  const [progressHistory, setProgressHistory] = useState<ProgressEvent[]>([]);
  const [toolCalls, setToolCalls] = useState<ToolCallEvent[]>([]);

  // 内容和结果
  const [content, setContent] = useState('');
  const [result, setResult] = useState<any | null>(null);

  // 用于取消请求（如果需要）
  const abortControllerRef = useRef<AbortController | null>(null);

  /**
   * 清除错误
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  /**
   * 重置所有状态
   */
  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
    setConversationId(null);
    setCurrentProgress(null);
    setProgressHistory([]);
    setToolCalls([]);
    setContent('');
    setResult(null);
  }, []);

  /**
   * 发送消息
   */
  const sendMessage = useCallback(
    async (message: string, requestOptions?: Partial<AgentChatRequest>) => {
      setLoading(true);
      setError(null);
      setCurrentProgress(null);
      setProgressHistory([]);
      setToolCalls([]);
      setContent('');
      setResult(null);

      try {
        // 准备请求
        const request: AgentChatRequest = {
          message,
          conversation_id: conversationId || undefined,
          ...requestOptions,
        };

        // 调用API
        await agentApi.chatReactStream(request, {
          onStart: (convId) => {
            setConversationId(convId);
          },

          onProgress: (progress) => {
            const progressEvent: ProgressEvent = {
              type: 'progress',
              step: progress.step,
              description: progress.description,
              node: progress.node,
              details: progress.details,
              timestamp: progress.timestamp,
            };

            setCurrentProgress(progressEvent);
            // 限制进度历史最多保留100条，避免内存占用过大
            setProgressHistory((prev) => {
              const newHistory = [...prev, progressEvent];
              return newHistory.length > 100 ? newHistory.slice(-100) : newHistory;
            });

            // 触发外部回调
            options?.onProgress?.(progressEvent);
          },

          onToolCall: (toolCall) => {
            const toolCallEvent: ToolCallEvent = {
              tool: toolCall.tool,
              args: toolCall.args,
              timestamp: toolCall.timestamp,
            };

            setToolCalls((prev) => [...prev, toolCallEvent]);

            // 触发外部回调
            options?.onToolCall?.(toolCallEvent);
          },

          onContent: (chunk) => {
            setContent((prev) => prev + chunk);

            // 触发外部回调
            options?.onContent?.(chunk);
          },

          onDone: (data) => {
            setResult(data);
            setCurrentProgress(null);

            // 触发外部回调
            options?.onComplete?.(data);
          },

          onError: (errorMsg) => {
            const err = new Error(errorMsg);
            setError(err);

            // 触发外部回调
            options?.onError?.(err);
          },
        });

      } catch (err) {
        const error = err instanceof Error ? err : new Error('Agent请求失败');
        setError(error);
        options?.onError?.(error);
      } finally {
        setLoading(false);
      }
    },
    [conversationId, options]
  );

  return {
    // 状态
    loading,
    error,
    conversationId,

    // 进度
    currentProgress,
    progressHistory,
    toolCalls,

    // 内容
    content,

    // 结果
    result,

    // 方法
    sendMessage,
    clearError,
    reset,
  };
}
