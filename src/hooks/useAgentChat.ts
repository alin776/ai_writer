
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { agentApi } from '@/services/agentApi';
import { useConversationPersistence } from './useConversationPersistence';
import { getGlobalSessionManager } from '@/contexts/SessionContext';
import type { SessionState } from './SessionStateManager';
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
  progress_status?: string;  // Multi-Agent 内部进度状态
}

interface UseAgentChatOptions {
  workId?: string;
  chapterId?: string;
  sessionId?: string;
}

export interface EditorAction {
  type: 'modify' | 'continue' | 'insert' | 'none';
  original_text?: string;
  new_text?: string;
  new_text_html?: string;
  position?: { from: number; to: number };
  requires_confirmation?: boolean;
  description?: string;
}

export interface ApprovalRequest {
  request_id: string;
  action_type: 'edit' | 'rewrite' | 'insert';
  operation?: string;
  original_content?: string;
  new_content?: string;
  description?: string;
  versions?: Array<{
    style?: string;
    style_name: string;
    reason?: string;
    content?: string;
  }>;
  chapter_id?: string;
  // 🆕 InlineAI 编辑器操作
  editor_action?: EditorAction;
}

interface UseAgentChatReturn {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  suggestedActions: string[];
  tasks: Task[];
  currentTaskId: number | null;
  activities: ActivityItem[];
  progressData: ProgressData | null;
  sendMessage: (request: AgentChatRequest) => Promise<AgentChatResponse | null>;
  sendMessageStream: (request: AgentChatRequest) => Promise<void>;
  clearMessages: () => void;
  retryLastMessage: () => Promise<void>;
  sessionId: string;
  conversationId: string | undefined;
  loadHistorySession: (sessionId: string) => void;
  getAllHistorySessions: () => any[];
  createNewConversation: () => Promise<void>;
  pendingApproval: ApprovalRequest | null;
  submitApproval: (approved: boolean, selectedVersion?: number) => Promise<void>;
  stopStreaming: () => void;
}

export function useAgentChat(options: UseAgentChatOptions = {}): UseAgentChatReturn {
  const { workId, chapterId, sessionId: externalSessionId } = options;
  const useBackendSessions = import.meta.env.VITE_USE_MOCK !== 'true';
  const MAX_HUMANIZE_CHARS = 5000;

  const activityStartTimes = useRef<Map<string, number>>(new Map());
  const lastRequestRef = useRef<AgentChatRequest | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const lastPersistRef = useRef<number>(0);
  const lastUpdateRef = useRef<number>(0);
  const stopRequestedRef = useRef<boolean>(false);

  // ✅ 打字机效果：缓冲队列和定时器
  const typewriterQueueRef = useRef<string[]>([]);
  const typewriterTimerRef = useRef<number | null>(null);
  const TYPEWRITER_SPEED = 10; // 每个字符显示间隔（毫秒），10ms约100字/秒

  const persistence = useConversationPersistence({
    sessionId: externalSessionId,
    autoSave: true,
    maxSessions: 20,
    workId,
    chapterId,
    useBackend: useBackendSessions
  });
  const sessionId = persistence.sessionId;

  const sessionManager = useMemo(() => getGlobalSessionManager(), []);
  const [sessionState, setSessionState] = useState<SessionState>(() =>
    sessionManager.getOrCreateSession(sessionId, { mode: 'plan' })
  );

  const persistMessages = useCallback(
    (messagesToSave: Message[], conversation?: string, mode?: 'plan' | 'agent') => {
      persistence.saveSession(messagesToSave, conversation, {
        mode,
        workId,
        chapterId
      });
    },
    [chapterId, persistence, workId]
  );

  const persistMessagesThrottled = useCallback(
    (messagesToSave: Message[], conversation?: string, mode?: 'plan' | 'agent', force: boolean = false) => {
      const now = Date.now();
      if (!force && now - lastPersistRef.current < 500) {
        return;
      }
      lastPersistRef.current = now;
      persistMessages(messagesToSave, conversation, mode);
    },
    [persistMessages]
  );

  const refreshSessionSnapshot = useCallback(() => {
    const snapshot = sessionManager.getOrCreateSession(sessionId, { mode: 'plan' });
    setSessionState({ ...snapshot });
  }, [sessionId, sessionManager]);

  useEffect(() => {
    const persisted = persistence.loadSession(sessionId);
    if (persisted) {
      sessionManager.updateSession(sessionId, {
        messages: persisted.messages as Message[],
        conversationId: persisted.conversationId || undefined,
        mode: persisted.mode || 'plan'
      });
    }
    refreshSessionSnapshot();

    sessionManager.setActiveSession(sessionId);
    const unsubscribe = sessionManager.addListener((id, state) => {
      if (id === sessionId) {
        setSessionState({ ...state });
      }
    });

    return () => {
      unsubscribe();
    };
  }, [persistence.loadSession, refreshSessionSnapshot, sessionId, sessionManager]);

  const sendMessage = useCallback(
    async (request: AgentChatRequest): Promise<AgentChatResponse | null> => {
      const now = new Date().toISOString();
      const userMessage: Message = {
        role: 'user',
        content: request.message,
        timestamp: now
      };

      const current = sessionManager.getOrCreateSession(sessionId);
      const withUser = [...current.messages, userMessage];
      lastRequestRef.current = request;

      sessionManager.updateSession(sessionId, {
        messages: withUser,
        isLoading: true,
        error: null,
        suggestedActions: [],
        pendingApproval: null
      });
      persistMessages(withUser, current.conversationId, current.mode);

      try {
        const response = await agentApi.chat(request);

        const agentMessage: Message = {
          role: 'agent',
          content: response.response,
          agentSteps: response.agent_steps,
          metadata: response.metadata,
          timestamp: new Date().toISOString()
        };
        const updated = [...withUser, agentMessage];

        sessionManager.updateSession(sessionId, {
          messages: updated,
          conversationId: response.conversation_id,
          suggestedActions: response.suggested_actions || [],
          isLoading: false
        });
        persistMessages(updated, response.conversation_id, current.mode);

        return response;
      } catch (err: any) {
        const errorMessage = err.response?.data?.detail || err.message || '????';
        const errorAgentMessage: Message = {
          role: 'agent',
          content:
            'Sorry, something went wrong: ' +
            errorMessage +
            '\\n\\nPlease try again later or contact support.',
          timestamp: new Date().toISOString()
        };
        const updated = [...withUser, errorAgentMessage];
        sessionManager.updateSession(sessionId, {
          messages: updated,
          error: errorMessage,
          isLoading: false
        });
        persistMessages(updated, current.conversationId, current.mode);
        return null;
      }
    },
    [persistMessages, sessionId, sessionManager]
  );

  const sendMessageStream = useCallback(
    async (request: AgentChatRequest): Promise<void> => {
      // 防止在加载中被重复触发（例如 StrictMode 双调用或多次点击）
      const loadingSnap = sessionManager.getSession(sessionId);
      if (loadingSnap?.isLoading) {
        console.warn('[useAgentChat] stream already in progress, skip duplicate trigger');
        return;
      }

      // 如果开启 @optimization：补齐文本后走 Agent 接口（不写 humanize 历史）
      if (request.context?.use_optimization) {
        const current = sessionManager.getOrCreateSession(sessionId);
        let text =
          (request.context.current_content as string | undefined)?.trim() ||
          (request.context.text as string | undefined)?.trim() ||
          '';
        if (!text) {
          const history = [...current.messages].reverse();
          const lastAgent = history.find((m) => m.role === 'agent' && m.content?.trim());
          const lastUser = history.find((m) => m.role === 'user' && m.content?.trim());
          text = (lastAgent?.content || lastUser?.content || '').trim();
        }
        if (text && text.length > MAX_HUMANIZE_CHARS) {
          text = text.slice(0, MAX_HUMANIZE_CHARS);
        }
        request.context = {
          ...request.context,
          text,
          current_content: text
        };
      }

      stopRequestedRef.current = false;
      // request.mode 是发送给后端的模式（'planning'），转换为前端 UI 模式
      const backendMode = request.mode || 'planning';
      const uiMode: 'plan' | 'agent' = request.enable_reflection ? 'agent' : 'plan';
      const now = new Date().toISOString();
      const userMessage: Message = {
        role: 'user',
        content: request.message,
        timestamp: now
      };

      const current = sessionManager.getOrCreateSession(sessionId);
      const baseMessages: Message[] = [
        ...current.messages,
        userMessage,
        {
          role: 'agent',
          content: '',
          agentSteps: [],
          timestamp: now
        }
      ];
      const agentMessageIndex = baseMessages.length - 1;
      let streamingContent = '';
      let agentSteps: any[] = [];
      let streamConversationId: string | undefined = current.conversationId;
      const abortController = new AbortController();
      abortControllerRef.current?.abort();
      abortControllerRef.current = abortController;
      lastPersistRef.current = 0;

      // ✅ 清理打字机队列（确保每次新请求时队列干净）
      if (typewriterTimerRef.current !== null) {
        clearInterval(typewriterTimerRef.current);
        typewriterTimerRef.current = null;
      }
      typewriterQueueRef.current = [];

      const taskStartTimes = new Map<number, number>();
      activityStartTimes.current.clear();
      lastRequestRef.current = request;

      // Ensure backend session exists when using real API
      if (!streamConversationId && useBackendSessions) {
        try {
          const resp = await agentApi.createSession({
            title: '新会话',
            work_id: workId,
            chapter_id: chapterId
          });
          streamConversationId = resp.conversation_id || resp.session_id || streamConversationId;
          sessionManager.updateSession(sessionId, { conversationId: streamConversationId });
        } catch (error) {
          console.warn('[useAgentChat] create backend session failed:', error);
        }
      }

      sessionManager.updateSession(sessionId, {
        messages: baseMessages,
        isLoading: true,
        error: null,
        suggestedActions: [],
        tasks: [],
        currentTaskId: null,
        activities: [],
        progressData: null,
        pendingApproval: null,
        mode: uiMode
      });
      persistMessages(baseMessages, streamConversationId, uiMode);

      try {
        await agentApi.chatStream(
          { ...request, conversation_id: streamConversationId },
          {
            onReader: (reader) => {
              sessionManager.startStreaming(sessionId, reader, abortController);
            },
            onStart: (convId) => {
              streamConversationId = convId;
              sessionManager.updateSession(sessionId, { conversationId: convId });
            },
            ...(backendMode === 'planning'
              ? {
                  onPlan: (plan: any) => {
                    // 获取当前任务列表，用于保留已完成任务的状态
                    const currentTasks = sessionManager.getSession(sessionId)?.tasks || [];
                    const currentTaskMap = new Map(currentTasks.map(t => [t.task_id, t]));
                    const isUpdate = plan.is_update === true;

                    const updatedTasks: Task[] = plan.tasks.map((t: any) => {
                      const existing = currentTaskMap.get(t.task_id);

                      // 重规划时：保留已完成任务的状态
                      if (isUpdate && existing && existing.status === 'completed') {
                        return existing;
                      }

                      // 保留正在运行任务的状态
                      if (existing && existing.status === 'running') {
                        return { ...existing, description: t.description };
                      }

                      return {
                        task_id: t.task_id,
                        description: t.description,
                        tool: t.tool,
                        estimated_time: t.estimated_time,
                        status: t.status || 'pending',
                      };
                    });

                    sessionManager.updateSession(sessionId, { tasks: updatedTasks });
                  },
                  onTaskStart: (task: any) => {
                    taskStartTimes.set(task.task_id, Date.now());
                    sessionManager.updateSession(sessionId, {
                      currentTaskId: task.task_id,
                      tasks: (sessionManager.getSession(sessionId)?.tasks || []).map((t) =>
                        t.task_id === task.task_id ? { ...t, status: 'running' } : t
                      )
                    });
                  },
                  onTaskDone: (taskDone: any) => {
                    const startTime = taskStartTimes.get(taskDone.task_id);
                    let elapsedTime = taskDone.elapsed_time || 0;
                    if (startTime && elapsedTime === 0) {
                      elapsedTime = (Date.now() - startTime) / 1000;
                    }
                    sessionManager.updateSession(sessionId, {
                      tasks: (sessionManager.getSession(sessionId)?.tasks || []).map((t) =>
                        t.task_id === taskDone.task_id
                          ? { ...t, status: 'completed', elapsed_time: elapsedTime, progress_status: undefined }
                          : t
                      ),
                      currentTaskId: null
                    });
                    taskStartTimes.delete(taskDone.task_id);
                  },
                  onTaskProgress: (progress: any) => {
                    // 更新任务的进度状态（用于 Multi-Agent 内部进度）
                    const taskId = progress.task_id;
                    const status = progress.status;
                    if (taskId !== undefined && status) {
                      sessionManager.updateSession(sessionId, {
                        tasks: (sessionManager.getSession(sessionId)?.tasks || []).map((t) =>
                          t.task_id === taskId ? { ...t, progress_status: status } : t
                        )
                      });
                    }
                  }
                }
              : {}),
            ...(backendMode === 'react'
              ? {
                  onProgress: (progress: any) => {
                    const progressState: ProgressData = {
                      progress: progress.progress || 0,
                      eta: progress.eta ?? null,
                      eta_display: progress.eta_display || '',
                      eta_confidence: progress.eta_confidence || 'low',
                      current_step: progress.current_step || 1,
                      total_steps: progress.total_steps || 1,
                      step_description: progress.step_description || '',
                      elapsed: progress.elapsed || 0,
                      current_node: progress.node,
                      current_node_display: progress.current_node_display,
                      current_node_description: progress.description
                    };

                    const activityId =
                      String(progress.node || progress.step) + '_' + Date.now();
                    const activity: ActivityItem = {
                      id: activityId,
                      type: progress.step,
                      description: progress.description,
                      timestamp: progress.timestamp,
                      status: 'active',
                      node: progress.node,
                      details: progress.details
                    };

                    activityStartTimes.current.set(activityId, Date.now());
                    sessionManager.updateSession(sessionId, {
                      progressData: progressState,
                      activities: [
                        ...(sessionManager.getSession(sessionId)?.activities || []),
                        activity
                      ]
                    });
                  },
                  onActivityComplete: (activity: any) => {
                    sessionManager.updateSession(sessionId, {
                      activities: (sessionManager.getSession(sessionId)?.activities || []).map(
                        (a) => {
                          if (a.type === activity.step && a.status === 'active') {
                            const startTime = activityStartTimes.current.get(a.id);
                            const elapsedTime =
                              activity.elapsed_time ||
                              (startTime ? (Date.now() - startTime) / 1000 : 0);
                            activityStartTimes.current.delete(a.id);
                            return { ...a, status: 'completed', elapsedTime };
                          }
                          return a;
                        }
                      )
                    });
                  },
                  onToolCall: (toolCall: any) => {
                    agentSteps.push({
                      step: 'Call tool: ' + (toolCall.tool || 'unknown'),
                      result: JSON.stringify(toolCall.args || {})
                    });

                    sessionManager.updateSession(sessionId, {
                      activities: (sessionManager.getSession(sessionId)?.activities || []).map(
                        (a) => {
                          if (a.type === 'tool_execution' && a.status === 'active') {
                            const startTime = activityStartTimes.current.get(a.id);
                            const elapsedTime = startTime ? (Date.now() - startTime) / 1000 : 0;
                            return { ...a, status: 'completed', tool: toolCall.tool, elapsedTime };
                          }
                          return a;
                        }
                      )
                    });
                  },
                  onApprovalRequest: (approvalReq: any) => {
                    sessionManager.updateSession(sessionId, {
                      pendingApproval: {
                        request_id: approvalReq.request_id,
                        action_type: approvalReq.action_type,
                        operation: approvalReq.operation,
                        original_content: approvalReq.original_content,
                        new_content: approvalReq.new_content,
                        description: approvalReq.description,
                        versions: approvalReq.versions,
                        // 🆕 InlineAI: 包含 editor_action
                        editor_action: approvalReq.editor_action
                      }
                    });
                  }
                }
              : {}),
            onContent: (chunk) => {
              if (stopRequestedRef.current) return; // 已请求停止时丢弃后续流内容

              // ✅ 打字机效果：将chunk中的每个字符加入队列
              for (const char of chunk) {
                typewriterQueueRef.current.push(char);
              }

              // 启动打字机定时器（如果未启动）
              if (typewriterTimerRef.current === null) {
                const processQueue = () => {
                  if (stopRequestedRef.current || typewriterQueueRef.current.length === 0) {
                    if (typewriterTimerRef.current !== null) {
                      clearInterval(typewriterTimerRef.current);
                      typewriterTimerRef.current = null;
                    }
                    return;
                  }

                  // 从队列取出一个字符
                  const char = typewriterQueueRef.current.shift();
                  if (char) {
                    streamingContent += char;

                    // 更新UI
                    const currentSession = sessionManager.getSession(sessionId);
                    const currentMessages = currentSession?.messages || baseMessages;
                    const updated = [...currentMessages];
                    const target = updated[agentMessageIndex];
                    if (target) {
                      updated[agentMessageIndex] = {
                        ...target,
                        content: streamingContent,
                        agentSteps
                      };
                      sessionManager.updateSession(sessionId, { messages: updated });
                    }
                  }
                };

                typewriterTimerRef.current = window.setInterval(processQueue, TYPEWRITER_SPEED);
              }
            },
            onStep: (step) => {
              agentSteps.push(step);
            },
            onDone: (metadata, actions) => {
              // ✅ 打字机效果：等待队列清空后再完成
              const finishStream = () => {
                // 清空队列中剩余的所有字符
                while (typewriterQueueRef.current.length > 0) {
                  const char = typewriterQueueRef.current.shift();
                  if (char) streamingContent += char;
                }

                // 清理定时器
                if (typewriterTimerRef.current !== null) {
                  clearInterval(typewriterTimerRef.current);
                  typewriterTimerRef.current = null;
                }

                const currentSession = sessionManager.getSession(sessionId);
                const currentMessages = currentSession?.messages || baseMessages;
                const updated = [...currentMessages];
                const target = updated[agentMessageIndex];
                if (target) {
                  updated[agentMessageIndex] = {
                    ...target,
                    content: streamingContent,
                    agentSteps,
                    metadata
                  };
                }

                sessionManager.updateSession(sessionId, {
                  messages: updated,
                  suggestedActions: actions || [],
                  isLoading: false,
                  progressData: null,
                  activities: (currentSession?.activities || []).map((a) =>
                    a.status === 'active' ? { ...a, status: 'completed' } : a
                  )
                });
                persistMessagesThrottled(updated, streamConversationId, uiMode, true);
                sessionManager.disconnectSession(sessionId);
                abortControllerRef.current = null;
              };

              // 如果队列为空，直接完成；否则等待队列清空
              if (typewriterQueueRef.current.length === 0) {
                finishStream();
              } else {
                // 等待打字机效果完成
                const waitForQueue = setInterval(() => {
                  if (typewriterQueueRef.current.length === 0) {
                    clearInterval(waitForQueue);
                    finishStream();
                  }
                }, 50);
              }
            },
            onError: (errorMsg) => {
              const errorMessage = errorMsg || '未知错误';
              const currentSession = sessionManager.getSession(sessionId);
              const currentMessages = currentSession?.messages || baseMessages;
              const updated = [...currentMessages];
              const isAbort =
                stopRequestedRef.current ||
                errorMessage.toLowerCase().includes('abort') ||
                errorMessage.toLowerCase().includes('cancel');
              if (updated[agentMessageIndex]) {
                updated[agentMessageIndex] = {
                  role: 'agent',
                  content: isAbort
                    ? '对话已停止。'
                    : '抱歉，遇到了问题：' + errorMessage + '\\n\\n请稍后重试，或联系管理员。',
                  timestamp: new Date().toISOString()
                };
              } else if (isAbort) {
                // fallback: push a single stop message if placeholder missing
                updated.push({
                  role: 'agent',
                  content: '对话已停止。',
                  timestamp: new Date().toISOString()
                });
              }
              sessionManager.updateSession(sessionId, {
                messages: updated,
                error: isAbort ? null : errorMessage,
                isLoading: false
              });
              persistMessagesThrottled(updated, streamConversationId, uiMode, true);
              sessionManager.disconnectSession(sessionId);
              abortControllerRef.current = null;
            }
          },
          {
            signal: abortController.signal,
            controller: abortController
          }
        );
      } catch (err: any) {
        const errorMessage = err.message || '未知错误';
        const isAbort = stopRequestedRef.current || errorMessage.toLowerCase().includes('abort');
        const currentSession = sessionManager.getSession(sessionId);
        const currentMessages = currentSession?.messages || [];
        const updated = [...currentMessages];
        if (updated.length > 0 && updated[updated.length - 1].role === 'agent') {
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            content: isAbort
              ? '对话已停止。'
              : '抱歉，遇到了问题：' + errorMessage + '\\n\\n请稍后重试，或联系管理员。',
            timestamp: new Date().toISOString()
          };
        } else if (isAbort) {
          updated.push({
            role: 'agent',
            content: '对话已停止。',
            timestamp: new Date().toISOString()
          });
        }
        sessionManager.updateSession(sessionId, {
          messages: updated,
          error: isAbort ? null : errorMessage,
          isLoading: false
        });
        if (isAbort) {
          persistMessagesThrottled(updated, currentSession?.conversationId, currentSession?.mode, true);
        }
        sessionManager.disconnectSession(sessionId);
        abortControllerRef.current = null;
      }
    },
    [persistMessages, persistMessagesThrottled, sessionId, sessionManager]
  );

  const clearMessages = useCallback(() => {
    sessionManager.updateSession(sessionId, {
      messages: [],
      suggestedActions: [],
      error: null,
      isLoading: false,
      tasks: [],
      currentTaskId: null,
      conversationId: undefined,
      activities: [],
      progressData: null,
      pendingApproval: null
    });
    activityStartTimes.current.clear();
    abortControllerRef.current = null;
    lastPersistRef.current = 0;

    // ✅ 清理打字机定时器和队列
    if (typewriterTimerRef.current !== null) {
      clearInterval(typewriterTimerRef.current);
      typewriterTimerRef.current = null;
    }
    typewriterQueueRef.current = [];

    persistence.clearCurrentSession();
    refreshSessionSnapshot();
  }, [persistence, refreshSessionSnapshot, sessionId, sessionManager]);

  const retryLastMessage = useCallback(async () => {
    if (!lastRequestRef.current) return;
    await sendMessageStream(lastRequestRef.current);
  }, [sendMessageStream]);

  const stopStreaming = useCallback(() => {
    stopRequestedRef.current = true;

    // ✅ 清理打字机定时器和队列
    if (typewriterTimerRef.current !== null) {
      clearInterval(typewriterTimerRef.current);
      typewriterTimerRef.current = null;
    }
    typewriterQueueRef.current = [];

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    const snap = sessionManager.getSession(sessionId);
    if (snap?.messages) {
      persistMessagesThrottled(snap.messages as Message[], snap.conversationId, snap.mode, true);
    }
    sessionManager.disconnectSession(sessionId);
    sessionManager.updateSession(sessionId, { isLoading: false });
  }, [persistMessagesThrottled, sessionId, sessionManager]);

  const loadHistorySession = useCallback(
    (targetSessionId: string) => {
      const session = persistence.loadSession(targetSessionId);
      if (!session || session.id !== targetSessionId) {
        console.warn(
          `[useAgentChat] session ${targetSessionId} does not exist or ID mismatch`
        );
        sessionManager.updateSession(sessionId, {
          messages: [],
          conversationId: undefined,
          suggestedActions: [],
          error: null,
          tasks: [],
          currentTaskId: null,
          activities: [],
          progressData: null,
          pendingApproval: null
        });
        activityStartTimes.current.clear();
        return;
      }

      sessionManager.updateSession(sessionId, {
        messages: session.messages as Message[],
        conversationId: session.conversationId || undefined,
        suggestedActions: [],
        error: null,
        tasks: [],
        currentTaskId: null,
        activities: [],
        progressData: null,
        pendingApproval: null,
        // 兼容旧数据：将可能存在的 'planning'/'react' 转换为 'plan'/'agent'
        mode: (session.mode as string) === 'react' || session.mode === 'agent' ? 'agent' : 'plan'
      });
      activityStartTimes.current.clear();
      refreshSessionSnapshot();
    },
    [persistence, refreshSessionSnapshot, sessionId, sessionManager]
  );

  const getAllHistorySessions = useCallback(() => {
    return persistence.getAllSessions();
  }, [persistence]);

  const createNewConversation = useCallback(async () => {
    activityStartTimes.current.clear();
    await persistence.createNewSession();
  }, [persistence]);

  const submitApproval = useCallback(
    async (approved: boolean, selectedVersion?: number) => {
      const pending = sessionManager.getSession(sessionId)?.pendingApproval as ApprovalRequest | null;
      if (!pending) {
        console.warn('[useAgentChat] no pending approval request');
        return;
      }

      try {
        if (approved) {
          // 处理 rewrite 类型（改写，有多个版本选择）
          if (pending.action_type === 'rewrite' && selectedVersion !== undefined) {
            const versions = pending.versions;
            if (versions && versions[selectedVersion]) {
              const selectedContent = versions[selectedVersion].content;
              const originalContent = pending.original_content;
              const editorAction = pending.editor_action;

              // 🆕 WPS修订模式: 触发显示修订标记事件（而非直接替换）
              window.dispatchEvent(
                new CustomEvent('agent-show-revision', {
                  detail: {
                    type: 'modify',
                    original: originalContent,
                    replacement: selectedContent,
                    position: editorAction?.position,
                    revisionId: `rev-${pending.request_id}-${Date.now()}`
                  }
                })
              );
            }
          }
          // 处理 continue 类型（续写）
          else if (pending.editor_action?.type === 'continue') {
            const newContent = pending.new_content;
            const editorAction = pending.editor_action;

            window.dispatchEvent(
              new CustomEvent('agent-show-revision', {
                detail: {
                  type: 'continue',
                  replacement: newContent,
                  position: editorAction?.position,
                  revisionId: `rev-${pending.request_id}-${Date.now()}`
                }
              })
            );
          }
          // 🆕 处理 edit 类型（编辑）
          else if (pending.action_type === 'edit') {
            const newContent = pending.new_content;
            const originalContent = pending.original_content;
            const editorAction = pending.editor_action;

            window.dispatchEvent(
              new CustomEvent('agent-show-revision', {
                detail: {
                  type: editorAction?.type === 'continue' ? 'continue' : 'modify',
                  original: originalContent,
                  replacement: newContent,
                  position: editorAction?.position,
                  revisionId: `rev-${pending.request_id}-${Date.now()}`
                }
              })
            );
          }
          // 🆕 处理 insert 类型（插入）
          else if (pending.action_type === 'insert') {
            const newContent = pending.new_content;
            const editorAction = pending.editor_action;

            window.dispatchEvent(
              new CustomEvent('agent-show-revision', {
                detail: {
                  type: 'continue',
                  replacement: newContent,
                  position: editorAction?.position,
                  revisionId: `rev-${pending.request_id}-${Date.now()}`
                }
              })
            );
          }
        }

        await agentApi.submitApprovalResponse({
          request_id: pending.request_id,
          approved,
          selected_version: selectedVersion
        });

        // 🆕 无论批准还是拒绝，都清理 pendingApproval 状态
        sessionManager.updateSession(sessionId, { pendingApproval: null });
      } catch (err: any) {
        console.error('[useAgentChat] submit approval failed:', err);
        sessionManager.updateSession(sessionId, {
          error: err.response?.data?.detail || err.message || 'Approval failed',
          pendingApproval: null  // 🆕 错误时也清理状态
        });
      }
    },
    [sessionId, sessionManager]
  );

  return {
    messages: sessionState.messages as Message[],
    isLoading: sessionState.isLoading,
    error: sessionState.error,
    suggestedActions: sessionState.suggestedActions,
    tasks: (sessionState.tasks || []) as Task[],
    currentTaskId: sessionState.currentTaskId,
    activities: (sessionState.activities || []) as ActivityItem[],
    progressData: sessionState.progressData,
    sendMessage,
    sendMessageStream,
    clearMessages,
    retryLastMessage,
    sessionId: persistence.sessionId,
    conversationId: sessionState.conversationId,
    loadHistorySession,
    getAllHistorySessions,
    createNewConversation,
    pendingApproval: sessionState.pendingApproval as ApprovalRequest | null,
    submitApproval,
    stopStreaming
  };
}
