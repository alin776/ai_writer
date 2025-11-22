/**
 * useAgentChat - Agent对话数据管理Hook
 *
 * 功能:
 * - 消息状态管理
 * - API调用封装
 * - 错误处理
 * - 加载状态
 * - 对话持久化（localStorage）
 */

import { useState, useCallback, useEffect } from 'react';
import { agentApi } from '@/services/agentApi';
import { useConversationPersistence } from './useConversationPersistence';
import type { AgentChatRequest, AgentChatResponse, ActivityItem, ProgressData } from '@/types/agent';

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

interface UseAgentChatOptions {
  workId?: string;  // 🆕 作品ID（用于会话隔离）
  chapterId?: string;  // 🆕 章节ID（用于会话隔离）
}

interface UseAgentChatReturn {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  suggestedActions: string[];
  tasks: Task[];
  currentTaskId: number | null;
  activities: ActivityItem[];  // ✅ 活动流
  progressData: ProgressData | null;  // ✅ 进度数据
  sendMessage: (request: AgentChatRequest) => Promise<AgentChatResponse | null>;
  sendMessageStream: (request: AgentChatRequest) => Promise<void>;
  clearMessages: () => void;
  retryLastMessage: () => Promise<void>;

  // 🆕 对话历史管理
  sessionId: string;
  conversationId: string | undefined;
  loadHistorySession: (sessionId: string) => void;
  getAllHistorySessions: () => any[];
  createNewConversation: () => void;
}

export function useAgentChat(options: UseAgentChatOptions = {}): UseAgentChatReturn {
  const { workId, chapterId } = options;
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [suggestedActions, setSuggestedActions] = useState<string[]>([]);
  const [lastRequest, setLastRequest] = useState<AgentChatRequest | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [currentTaskId, setCurrentTaskId] = useState<number | null>(null);
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const [activities, setActivities] = useState<ActivityItem[]>([]);  // ✅ 活动流状态
  const [progressData, setProgressData] = useState<ProgressData | null>(null);  // ✅ 进度数据状态

  // 用于记录活动开始时间（计算耗时）
  const [activityStartTimes] = useState<Map<string, number>>(new Map());

  // 🆕 对话持久化（传递workId和chapterId进行会话隔离）
  const persistence = useConversationPersistence({
    autoSave: true,
    maxSessions: 20,  // 最多保留20个历史会话
    workId,  // 🆕 传递作品ID
    chapterId  // 🆕 传递章节ID
  });

  // 🆕 初始化：从localStorage恢复历史对话
  useEffect(() => {
    const session = persistence.currentSession;
    if (session && session.messages.length > 0) {
      console.log(`[useAgentChat] 恢复历史会话 ${session.id}:`, session.messages.length, '条消息');
      setMessages(session.messages);
      setConversationId(session.conversationId || undefined);
    } else {
      // 空会话或null（新章节），清空消息
      console.log(`[useAgentChat] 新会话，清空消息`);
      setMessages([]);
      setConversationId(undefined);
    }
  }, [persistence.sessionId, persistence.currentSession]);  // 🔧 同时监听sessionId和currentSession

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

        // 🆕 自动保存对话
        persistence.saveSession([...messages, userMessage, agentMessage], response.conversation_id);

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

        // ✅ 重置活动流状态和进度数据
        setActivities([]);
        setProgressData(null);
        activityStartTimes.clear();

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

        // ✅ 调用流式API（传递保存的conversation_id）
        const mode = request.mode || 'planning'; // 默认 planning 模式

        await agentApi.chatStream(
          {
            ...request,
            conversation_id: conversationId // 传递保存的conversation_id
          },
          {
            // 共同回调
            onStart: (convId) => {
              setConversationId(convId); // ✅ 保存conversation_id到状态
              console.log('[Stream] Started, conversation_id:', convId, 'mode:', mode);
            },

          // Planning 模式回调
          ...(mode === 'planning' ? {
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
          }
          } : {}),

          // React 模式回调（新增）
          ...(mode === 'react' ? {
            onProgress: (progress) => {
              // ✅ 保存完整的进度数据（用于ProgressBar显示）
              setProgressData({
                progress: progress.progress || 0,
                eta: progress.eta ?? null,
                eta_display: progress.eta_display || '计算中...',
                eta_confidence: progress.eta_confidence || 'low',
                current_step: progress.current_step || 1,
                total_steps: progress.total_steps || 1,
                step_description: progress.step_description || '',
                elapsed: progress.elapsed || 0,
                current_node: progress.node,
                current_node_display: progress.current_node_display,
                current_node_description: progress.description
              });

              // 转换为 ActivityItem 并添加到活动流
              const activityId = `${progress.node || progress.step}_${Date.now()}`;
              const activity: ActivityItem = {
                id: activityId,
                type: progress.step as any,  // 'intent_analysis' | 'thinking' | 'tool_execution' | 'generating'
                description: progress.description,
                timestamp: progress.timestamp,
                status: 'active',
                node: progress.node,
                details: progress.details
              };

              // 记录活动开始时间
              activityStartTimes.set(activityId, Date.now());

              // 添加到活动流
              setActivities(prev => [...prev, activity]);
            },
            onActivityComplete: (activity) => {
              // ✅ 新增：处理活动完成事件
              console.log('[React] Activity完成:', activity.step, `(${activity.elapsed_time}s)`);

              setActivities(prev => {
                // ✅ 修复：查找最后一个同类型的active活动（更准确）
                let updated = false;
                const newActivities = prev.map((a, index) => {
                  // 只更新最后一个同类型的active活动
                  if (!updated && a.type === activity.step && a.status === 'active') {
                    // 检查是否是最后一个
                    const isLast = !prev.slice(index + 1).some(
                      x => x.type === activity.step && x.status === 'active'
                    );

                    if (isLast) {
                      updated = true;
                      const startTime = activityStartTimes.get(a.id);
                      const elapsedTime = activity.elapsed_time ||
                        (startTime ? (Date.now() - startTime) / 1000 : 0);

                      // 清理时间记录
                      activityStartTimes.delete(a.id);

                      return {
                        ...a,
                        status: 'completed' as const,
                        elapsedTime
                      };
                    }
                  }
                  return a;
                });

                return newActivities;
              });
            },
            onToolCall: (toolCall) => {
              console.log('[Stream] 工具调用:', toolCall);

              // 将工具调用记录到 agentSteps 中
              agentSteps.push({
                step: `调用工具: ${toolCall.tool || '未知'}`,
                result: JSON.stringify(toolCall.args || {})
              });

              // ✅ 标记对应的活动为完成（如果有 tool_execution 活动）
              setActivities(prev =>
                prev.map(a => {
                  // 查找最近的tool_execution活动
                  if (a.type === 'tool_execution' && a.status === 'active') {
                    const startTime = activityStartTimes.get(a.id);
                    const elapsedTime = startTime ? (Date.now() - startTime) / 1000 : 0;

                    return {
                      ...a,
                      status: 'completed' as const,
                      tool: toolCall.tool,
                      elapsedTime
                    };
                  }
                  return a;
                })
              );
            }
          } : {}),

          // 共同回调
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

            // ✅ 标记所有活动为完成
            setActivities(prev =>
              prev.map(a => {
                if (a.status === 'active') {
                  const startTime = activityStartTimes.get(a.id);
                  const elapsedTime = startTime ? (Date.now() - startTime) / 1000 : 0;

                  return {
                    ...a,
                    status: 'completed' as const,
                    elapsedTime
                  };
                }
                return a;
              })
            );

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

              // 🆕 自动保存对话（在消息更新后）
              persistence.saveSession(newMessages, conversationId);

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
    [messages.length, conversationId] // ✅ 添加conversationId依赖
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    setSuggestedActions([]);
    setError(null);
    setLastRequest(null);
    setTasks([]);
    setCurrentTaskId(null);
    setConversationId(undefined);
    setActivities([]);  // ✅ 清空活动流
    setProgressData(null);  // ✅ 清空进度数据
    activityStartTimes.clear();

    // 🆕 清空当前会话并创建新会话
    persistence.clearCurrentSession();
  }, [activityStartTimes, persistence]);

  const retryLastMessage = useCallback(async () => {
    if (!lastRequest) return;

    // 移除最后两条消息（用户消息 + Agent错误消息）
    setMessages((prev) => prev.slice(0, -2));

    // 重新发送（使用流式）
    await sendMessageStream(lastRequest);
  }, [lastRequest, sendMessageStream]);

  // 🆕 加载历史会话
  const loadHistorySession = useCallback((sessionId: string) => {
    const session = persistence.loadSession(sessionId);
    if (!session) {
      console.warn(`[useAgentChat] 会话 ${sessionId} 不存在`);
      return;
    }

    console.log(`[useAgentChat] 加载历史会话 ${sessionId}:`, session.messages.length, '条消息');

    // 重置所有状态
    setMessages(session.messages);
    setConversationId(session.conversationId || undefined);
    setSuggestedActions([]);
    setError(null);
    setTasks([]);
    setCurrentTaskId(null);
    setActivities([]);
    setProgressData(null);
    activityStartTimes.clear();
  }, [persistence, activityStartTimes]);

  // 🆕 获取所有历史会话
  const getAllHistorySessions = useCallback(() => {
    return persistence.getAllSessions();
  }, [persistence]);

  // 🆕 创建新对话
  const createNewConversation = useCallback(() => {
    console.log('[useAgentChat] 创建新对话');

    // 重置所有状态
    setMessages([]);
    setConversationId(undefined);
    setSuggestedActions([]);
    setError(null);
    setTasks([]);
    setCurrentTaskId(null);
    setActivities([]);
    setProgressData(null);
    activityStartTimes.clear();

    // 创建新会话
    persistence.createNewSession();
  }, [persistence, activityStartTimes]);

  return {
    messages,
    isLoading,
    error,
    suggestedActions,
    tasks,
    currentTaskId,
    activities,  // ✅ 返回活动流
    progressData,  // ✅ 返回进度数据
    sendMessage,
    sendMessageStream,
    clearMessages,
    retryLastMessage,

    // 🆕 对话历史管理
    sessionId: persistence.sessionId,
    conversationId,
    loadHistorySession,
    getAllHistorySessions,
    createNewConversation
  };
}
