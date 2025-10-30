/**
 * useAgentChat - Agent对话数据管理Hook
 *
 * 功能:
 * - 消息状态管理
 * - API调用封装
 * - 错误处理
 * - 加载状态
 */

import { useState, useCallback } from 'react';
import { agentApi } from '@/services/agentApi';
import type { AgentChatRequest, AgentChatResponse } from '@/types/agent';

interface Message {
  role: 'user' | 'agent';
  content: string;
  agentSteps?: any[];
  metadata?: any;
  timestamp: string;
}

interface UseAgentChatReturn {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  suggestedActions: string[];
  sendMessage: (request: AgentChatRequest) => Promise<AgentChatResponse | null>;
  clearMessages: () => void;
  retryLastMessage: () => Promise<void>;
}

export function useAgentChat(): UseAgentChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [suggestedActions, setSuggestedActions] = useState<string[]>([]);
  const [lastRequest, setLastRequest] = useState<AgentChatRequest | null>(null);

  const sendMessage = useCallback(
    async (request: AgentChatRequest): Promise<AgentChatResponse | null> => {
      try {
        setIsLoading(true);
        setError(null);
        setLastRequest(request);

        // 添加用户消息
        const userMessage: Message = {
          role: 'user',
          content: request.message,
          timestamp: new Date().toISOString()
        };
        setMessages((prev) => [...prev, userMessage]);

        // 调用API
        const response = await agentApi.chat(request);

        // 添加Agent回复
        const agentMessage: Message = {
          role: 'agent',
          content: response.response,
          agentSteps: response.agent_steps,
          metadata: response.metadata,
          timestamp: new Date().toISOString()
        };
        setMessages((prev) => [...prev, agentMessage]);

        // 更新建议操作
        setSuggestedActions(response.suggested_actions || []);

        return response;
      } catch (err: any) {
        const errorMessage = err.response?.data?.detail || err.message || '未知错误';
        setError(errorMessage);

        // 添加错误消息
        const errorAgentMessage: Message = {
          role: 'agent',
          content: `❌ 抱歉，遇到了问题：${errorMessage}\n\n请稍后重试，或联系管理员。`,
          timestamp: new Date().toISOString()
        };
        setMessages((prev) => [...prev, errorAgentMessage]);

        console.error('Agent chat error:', err);
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    setSuggestedActions([]);
    setError(null);
    setLastRequest(null);
  }, []);

  const retryLastMessage = useCallback(async () => {
    if (!lastRequest) return;

    // 移除最后两条消息（用户消息 + Agent错误消息）
    setMessages((prev) => prev.slice(0, -2));

    // 重新发送
    await sendMessage(lastRequest);
  }, [lastRequest, sendMessage]);

  return {
    messages,
    isLoading,
    error,
    suggestedActions,
    sendMessage,
    clearMessages,
    retryLastMessage
  };
}
