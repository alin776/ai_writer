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

interface Task {
  task_id: number;
  description: string;
  tool?: string;
  estimated_time?: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  elapsed_time?: number;
}

interface UseAgentChatReturn {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  suggestedActions: string[];
  tasks: Task[];
  currentTaskId: number | null;
  sendMessage: (request: AgentChatRequest) => Promise<AgentChatResponse | null>;
  sendMessageStream: (request: AgentChatRequest) => Promise<void>;
  clearMessages: () => void;
  retryLastMessage: () => Promise<void>;
}

export function useAgentChat(): UseAgentChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [suggestedActions, setSuggestedActions] = useState<string[]>([]);
  const [lastRequest, setLastRequest] = useState<AgentChatRequest | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [currentTaskId, setCurrentTaskId] = useState<number | null>(null);

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

  const sendMessageStream = useCallback(
    async (request: AgentChatRequest): Promise<void> => {
      try {
        setIsLoading(true);
        setError(null);
        setLastRequest(request);

        // 重置任务状态
        setTasks([]);
        setCurrentTaskId(null);

        // 添加用户消息
        const userMessage: Message = {
          role: 'user',
          content: request.message,
          timestamp: new Date().toISOString()
        };
        setMessages((prev) => [...prev, userMessage]);

        // 创建一个空的Agent消息，用于实时更新
        let streamingContent = '';
        let agentSteps: any[] = [];
        let conversationId = '';

        const agentMessageIndex = messages.length + 1;

        // 添加空的Agent消息占位
        setMessages((prev) => [
          ...prev,
          {
            role: 'agent',
            content: '',
            agentSteps: [],
            timestamp: new Date().toISOString()
          }
        ]);

        // 用于记录每个任务的开始时间
        const taskStartTimes = new Map<number, number>();

        // 调用流式API
        await agentApi.chatStream(request, {
          onStart: (convId) => {
            conversationId = convId;
            console.log('[Stream] Started, conversation_id:', convId);
          },
          onPlan: (plan) => {
            // 初始化任务列表
            const initialTasks: Task[] = plan.tasks.map((t: any) => ({
              task_id: t.task_id,
              description: t.description,
              tool: t.tool,
              estimated_time: t.estimated_time,
              status: 'pending' as const,
              elapsed_time: undefined
            }));
            setTasks(initialTasks);
            console.log('[Stream] 规划生成:', initialTasks.length, '个任务');
          },
          onTaskStart: (task) => {
            // 记录任务开始时间
            taskStartTimes.set(task.task_id, Date.now());

            // 标记任务为运行中
            setCurrentTaskId(task.task_id);
            setTasks((prev) =>
              prev.map((t) =>
                t.task_id === task.task_id
                  ? { ...t, status: 'running' as const }
                  : t
              )
            );
            console.log('[Stream] 任务开始:', task.description);
          },
          onTaskProgress: (progress) => {
            console.log('[Stream] 任务进度:', progress);
          },
          onTaskDone: (taskDone) => {
            // 计算实际执行时间（前端计算）
            const startTime = taskStartTimes.get(taskDone.task_id);
            let elapsedTime = taskDone.elapsed_time || 0;

            if (startTime && elapsedTime === 0) {
              // 如果后端没有提供时间（为0），则使用前端计算的时间
              elapsedTime = (Date.now() - startTime) / 1000; // 转换为秒
            }

            // 标记任务完成
            setTasks((prev) =>
              prev.map((t) =>
                t.task_id === taskDone.task_id
                  ? {
                      ...t,
                      status: 'completed' as const,
                      elapsed_time: elapsedTime
                    }
                  : t
              )
            );
            setCurrentTaskId(null);

            // 清理已完成任务的开始时间记录
            taskStartTimes.delete(taskDone.task_id);

            console.log('[Stream] 任务完成:', taskDone.description, `(${elapsedTime.toFixed(1)}s)`);
          },
          onContent: (chunk) => {
            // 累积内容
            streamingContent += chunk;

            // 更新Agent消息
            setMessages((prev) => {
              const newMessages = [...prev];
              newMessages[agentMessageIndex] = {
                role: 'agent',
                content: streamingContent,
                agentSteps,
                timestamp: new Date().toISOString()
              };
              return newMessages;
            });
          },
          onStep: (step) => {
            agentSteps.push(step);
            console.log('[Stream] Agent step:', step);
          },
          onDone: (metadata, actions) => {
            console.log('[Stream] Done');
            setSuggestedActions(actions || []);

            // 最终更新消息，添加metadata
            setMessages((prev) => {
              const newMessages = [...prev];
              newMessages[agentMessageIndex] = {
                role: 'agent',
                content: streamingContent,
                agentSteps,
                metadata,
                timestamp: new Date().toISOString()
              };
              return newMessages;
            });
          },
          onError: (errorMsg) => {
            console.error('[Stream] Error:', errorMsg);
            setError(errorMsg);

            // 更新为错误消息
            setMessages((prev) => {
              const newMessages = [...prev];
              newMessages[agentMessageIndex] = {
                role: 'agent',
                content: `❌ 抱歉，遇到了问题：${errorMsg}\n\n请稍后重试，或联系管理员。`,
                timestamp: new Date().toISOString()
              };
              return newMessages;
            });
          }
        });
      } catch (err: any) {
        const errorMessage = err.message || '未知错误';
        setError(errorMessage);
        console.error('Agent chat stream error:', err);
      } finally {
        setIsLoading(false);
      }
    },
    [messages.length]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    setSuggestedActions([]);
    setError(null);
    setLastRequest(null);
    setTasks([]);
    setCurrentTaskId(null);
  }, []);

  const retryLastMessage = useCallback(async () => {
    if (!lastRequest) return;

    // 移除最后两条消息（用户消息 + Agent错误消息）
    setMessages((prev) => prev.slice(0, -2));

    // 重新发送（使用流式）
    await sendMessageStream(lastRequest);
  }, [lastRequest, sendMessageStream]);

  return {
    messages,
    isLoading,
    error,
    suggestedActions,
    tasks,
    currentTaskId,
    sendMessage,
    sendMessageStream,
    clearMessages,
    retryLastMessage
  };
}
