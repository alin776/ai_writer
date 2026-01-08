
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { agentApi } from '@/services/agentApi';
import { useConversationPersistence } from './useConversationPersistence';
import { getGlobalSessionManager } from '@/contexts/SessionContext';
import type { SessionState } from './SessionStateManager';
import type { AgentChatRequest, AgentChatResponse, ActivityItem, ProgressData, FlowItem, ToolFlowData, StepFlowData, TaskSnapshot, SummarizationFlowData, RevisionFlowData, RevisionStatus } from '@/types/agent';
import TypewriterWorker from '@/workers/typewriterWorker?worker';

// 清理任务描述中的 UUID（兜底过滤）
const cleanTaskDescription = (description: string): string => {
  if (!description) return description;
  return description
    .replace(/work_id[:\s]*[a-f0-9-]{8,36}/gi, '当前作品')
    .replace(/chapter_id[:\s]*[a-f0-9-]{8,36}/gi, '当前章节')
    .replace(/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}/gi, '');
};

interface Message {
  role: 'user' | 'agent';
  content: string;
  agentSteps?: any[];
  metadata?: any;
  timestamp: string;
  flowItems?: FlowItem[];  // v5.1: 执行轨迹绑定到消息
  tasksSnapshot?: TaskSnapshot[]; // v6.2: 任务列表快照（用于历史执行轨迹）
}

type Task = TaskSnapshot;

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
  action_type: 'edit' | 'rewrite' | 'insert' | 'create' | 'rename';
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
  flowItems: FlowItem[];  // v5.0: 执行轨迹项
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
  updateRevisionStatus: (itemId: string, status: RevisionStatus, snapshot?: {
    originalContent?: string;
    newContent?: string;
    editorPosition?: { from: number; to: number };
    selectedVersion?: number;
  }) => void;
  acceptAllRevisions: (itemIds: string[]) => void;
  discardAllRevisions: (itemIds: string[]) => void;
  undoRevision: (itemId: string) => void;      // v7.2
  redoRevision: (itemId: string) => void;      // v7.2
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

  // ✅ 打字机效果：缓冲队列和 Web Worker（后台标签页不会被节流）
  const typewriterQueueRef = useRef<string[]>([]);
  const typewriterWorkerRef = useRef<Worker | null>(null);
  const processQueueRef = useRef<(() => void) | null>(null);
  const TYPEWRITER_SPEED = 10; // 每个字符显示间隔（毫秒），10ms约100字/秒

  // ✅ 用于在页面不可见时快速清空队列的回调引用
  const flushQueueCallbackRef = useRef<(() => void) | null>(null);

  // ✅ 最小显示时间：跟踪 pending 的 setTimeout，以便清理
  // v6.7: 使用字符串 key 支持 step 和 task 的 timer（如 "step-1", "task-1"）
  const pendingTaskTimersRef = useRef<Map<string, ReturnType<typeof setTimeout>>>(new Map());

  const {
    sessionId: persistedSessionId,
    saveSession,
    loadSession,
    clearCurrentSession,
    getAllSessions,
    createNewSession
  } = useConversationPersistence({
    sessionId: externalSessionId,
    autoSave: true,
    maxSessions: 20,
    workId,
    chapterId,
    useBackend: useBackendSessions
  });
  const sessionId = persistedSessionId;
  const saveSessionRef = useRef(saveSession);

  const sessionManager = useMemo(() => getGlobalSessionManager(), []);
  const [sessionState, setSessionState] = useState<SessionState>(() =>
    sessionManager.getOrCreateSession(sessionId, { mode: 'plan' })
  );

  useEffect(() => {
    saveSessionRef.current = saveSession;
  }, [saveSession]);

  const persistMessages = useCallback(
    (messagesToSave: Message[], conversation?: string, mode?: 'plan' | 'agent') => {
      // DEBUG: 检查保存时消息是否包含 flowItems
      if (process.env.NODE_ENV === 'development') {
        console.log(`[useAgentChat] Saving ${messagesToSave.length} messages`);
        messagesToSave.forEach((msg, idx) => {
          if (msg.role === 'agent') {
            console.log(`[useAgentChat] Saving message ${idx} flowItems:`, (msg as any).flowItems?.length || 0);
          }
        });
      }
      saveSession(messagesToSave, conversation, {
        mode,
        workId,
        chapterId
      });
    },
    [chapterId, saveSession, workId]
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
    // 先确保会话存在，再更新数据
    sessionManager.getOrCreateSession(sessionId, { mode: 'plan' });

    const persisted = loadSession(sessionId);
    if (persisted) {
      // DEBUG: 检查从 localStorage 加载的消息是否包含 flowItems
      if (process.env.NODE_ENV === 'development') {
        console.log(`[useAgentChat] Loading session ${sessionId}, messages:`, persisted.messages.length);
        persisted.messages.forEach((msg, idx) => {
          if (msg.role === 'agent') {
            console.log(`[useAgentChat] Message ${idx} flowItems:`, (msg as any).flowItems?.length || 0);
          }
        });
      }
      // 从最后一条 agent 消息恢复 tasks
      const lastAgentMessage = [...persisted.messages].reverse().find(m => m.role === 'agent');
      const restoredTasks = (lastAgentMessage as any)?.tasksSnapshot || [];

      sessionManager.updateSession(sessionId, {
        messages: persisted.messages as Message[],
        conversationId: persisted.conversationId || undefined,
        mode: persisted.mode || 'plan',
        tasks: restoredTasks  // 恢复任务列表
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
      // 组件卸载时强制持久化当前状态，确保切换章节时数据不丢失
      const currentSession = sessionManager.getSession(sessionId);
      if (currentSession?.messages && currentSession.messages.length > 0) {
        saveSessionRef.current(
          currentSession.messages as Message[],
          currentSession.conversationId,
          { mode: currentSession.mode }
        );
      }
    };
  }, [loadSession, refreshSessionSnapshot, sessionId, sessionManager]);

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
          timestamp: now,
          flowItems: []  // v5.1: 执行轨迹绑定到消息
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

      // ✅ 清理打字机 Worker（确保每次新请求时队列干净）
      if (typewriterWorkerRef.current) {
        typewriterWorkerRef.current.postMessage({ type: 'stop' });
        typewriterWorkerRef.current.terminate();
        typewriterWorkerRef.current = null;
      }
      typewriterQueueRef.current = [];

      // ✅ 清理上一次请求的 pending 任务定时器
      pendingTaskTimersRef.current.forEach((timerId) => clearTimeout(timerId));
      pendingTaskTimersRef.current.clear();

      const taskStartTimes = new Map<number, number>();
      const stepStartTimes = new Map<number, number>();  // v6.7: 记录 step 开始时间，用于同步延迟
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
              // v5.1: flowItems 现在绑定到消息，不再全局清空
              sessionManager.updateSession(sessionId, {
                conversationId: convId
              });
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
                        return { ...existing, description: cleanTaskDescription(t.description) };
                      }

                      return {
                        task_id: t.task_id,
                        description: cleanTaskDescription(t.description),
                        tool: t.tool,
                        estimated_time: t.estimated_time,
                        status: t.status || 'pending',
                      };
                    });

                    sessionManager.updateSession(sessionId, { tasks: updatedTasks });
                  },
                  onTaskStart: (task: any) => {
                    taskStartTimes.set(task.task_id, Date.now());

                    // v6.0: flowItems 由 onFlowEvent 的 step_start 处理，这里只更新任务状态
                    const updatedTasks = (sessionManager.getSession(sessionId)?.tasks || []).map((t) =>
                      t.task_id === task.task_id ? { ...t, status: 'running' as const } : t
                    );
                    sessionManager.updateSession(sessionId, {
                      currentTaskId: task.task_id,
                      tasks: updatedTasks
                    });

                    // 保存 running 状态的任务快照，确保切换章节时不丢失
                    const currentSession = sessionManager.getSession(sessionId);
                    const currentMessages = currentSession?.messages || baseMessages;
                    const updated = [...currentMessages];
                    if (updated[agentMessageIndex]) {
                      updated[agentMessageIndex] = {
                        ...updated[agentMessageIndex],
                        tasksSnapshot: updatedTasks.map(t => ({ ...t }))
                      };
                      sessionManager.updateSession(sessionId, { messages: updated });
                      persistMessagesThrottled(updated, streamConversationId, uiMode, false);
                    }
                  },
                  onTaskDone: (taskDone: any) => {
                    const startTime = taskStartTimes.get(taskDone.task_id);
                    let elapsedTime = taskDone.elapsed_time || 0;
                    if (startTime && elapsedTime === 0) {
                      elapsedTime = (Date.now() - startTime) / 1000;
                    }
                    const taskId = taskDone.task_id;
                    const timerKey = `task-${taskId}`;

                    // v6.7: 确保 running 状态至少显示 500ms，提升用户体验
                    const MIN_RUNNING_DISPLAY_MS = 500;
                    const elapsedMs = startTime ? Date.now() - startTime : MIN_RUNNING_DISPLAY_MS;
                    const delayMs = Math.max(0, MIN_RUNNING_DISPLAY_MS - elapsedMs);

                    const updateTaskCompleted = () => {
                      pendingTaskTimersRef.current.delete(timerKey);
                      // v6.0: flowItems 由 onFlowEvent 的 step_complete 处理，这里只更新任务状态
                      sessionManager.updateSession(sessionId, {
                        tasks: (sessionManager.getSession(sessionId)?.tasks || []).map((t) =>
                          t.task_id === taskId
                            ? { ...t, status: 'completed', elapsed_time: elapsedTime, progress_status: undefined }
                            : t
                        ),
                        currentTaskId: sessionManager.getSession(sessionId)?.currentTaskId === taskId ? null : sessionManager.getSession(sessionId)?.currentTaskId
                      });
                      taskStartTimes.delete(taskId);
                    };

                    if (delayMs > 0) {
                      const timerId = setTimeout(updateTaskCompleted, delayMs);
                      pendingTaskTimersRef.current.set(timerKey, timerId);
                    } else {
                      updateTaskCompleted();
                    }
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
            // v6.0: 执行轨迹事件处理（所有模式通用）
            onFlowEvent: (event: any) => {
              const timestamp = event.timestamp || new Date().toISOString();
              const currentSession = sessionManager.getSession(sessionId);
              const currentMessages = currentSession?.messages || baseMessages;
              const targetMessage = currentMessages[agentMessageIndex] as Message;
              let currentFlowItems = targetMessage?.flowItems || [];

              switch (event.type) {
                case 'agent_header': {
                  const item: FlowItem = {
                    id: `flow-${Date.now()}-header`,
                    type: 'agent_header',
                    data: { name: event.data?.name, badge: event.data?.badge },
                    timestamp,
                  };
                  currentFlowItems = [...currentFlowItems, item];
                  break;
                }
                case 'text': {
                  const item: FlowItem = {
                    id: `flow-${Date.now()}-text`,
                    type: 'text',
                    data: { content: event.data?.content || '' },
                    timestamp,
                  };
                  currentFlowItems = [...currentFlowItems, item];
                  break;
                }
                case 'step_start': {
                  stepStartTimes.set(event.stepId, Date.now());  // v6.7: 记录开始时间
                  const stepData: StepFlowData = {
                    stepId: event.stepId,
                    title: cleanTaskDescription(event.title),
                    status: 'running',
                  };
                  const item: FlowItem = {
                    id: `flow-${Date.now()}-step-${event.stepId}`,
                    type: 'step',
                    data: stepData,
                    timestamp,
                  };
                  currentFlowItems = [...currentFlowItems, item];
                  break;
                }
                case 'knowledge_loaded': {
                  currentFlowItems = currentFlowItems.map(item => {
                    if (item.type === 'step' && (item.data as StepFlowData).stepId === event.stepId) {
                      const stepData = item.data as StepFlowData;
                      const knowledge = { title: event.title, icon: event.icon, items: event.items || [] };
                      return {
                        ...item,
                        data: { ...stepData, knowledge: [...(stepData.knowledge || []), knowledge] }
                      };
                    }
                    return item;
                  });
                  break;
                }
                case 'step_complete': {
                  // v6.7: 确保 running 状态至少显示 500ms，与 TaskList 同步
                  const MIN_RUNNING_DISPLAY_MS = 500;
                  const stepId = event.stepId;
                  const timerKey = `step-${stepId}`;
                  const startTime = stepStartTimes.get(stepId);
                  const elapsedMs = startTime ? Date.now() - startTime : MIN_RUNNING_DISPLAY_MS;
                  const delayMs = Math.max(0, MIN_RUNNING_DISPLAY_MS - elapsedMs);

                  // 保存事件数据，供延迟回调使用
                  const eventDescription = event.description;
                  const eventToolCall = event.toolCall;

                  if (delayMs > 0) {
                    // 延迟更新：使用 setTimeout，在回调中从消息获取最新 flowItems
                    const timerId = setTimeout(() => {
                      pendingTaskTimersRef.current.delete(timerKey);
                      stepStartTimes.delete(stepId);

                      // 从消息中获取最新的 flowItems（而不是使用闭包中的旧值）
                      const currentSession = sessionManager.getSession(sessionId);
                      const currentMessages = currentSession?.messages || [];
                      const targetMessage = currentMessages[agentMessageIndex] as Message | undefined;
                      if (!targetMessage) return;

                      const latestFlowItems = (targetMessage.flowItems || []).map(item => {
                        if (item.type === 'step' && (item.data as StepFlowData).stepId === stepId) {
                          const stepData = item.data as StepFlowData;
                          return {
                            ...item,
                            data: { ...stepData, status: 'done' as const, description: cleanTaskDescription(eventDescription), toolCall: eventToolCall }
                          };
                        }
                        return item;
                      });

                      // 更新消息的 flowItems
                      const updated = [...currentMessages];
                      updated[agentMessageIndex] = {
                        ...targetMessage,
                        flowItems: latestFlowItems,
                        tasksSnapshot: (currentSession?.tasks || []).map((task) => ({ ...task }))
                      };
                      sessionManager.updateSession(sessionId, { messages: updated });
                    }, delayMs);
                    pendingTaskTimersRef.current.set(timerKey, timerId);
                  } else {
                    // 立即更新：直接修改 currentFlowItems，让后续代码统一更新
                    currentFlowItems = currentFlowItems.map(item => {
                      if (item.type === 'step' && (item.data as StepFlowData).stepId === stepId) {
                        const stepData = item.data as StepFlowData;
                        return {
                          ...item,
                          data: { ...stepData, status: 'done' as const, description: cleanTaskDescription(eventDescription), toolCall: eventToolCall }
                        };
                      }
                      return item;
                    });
                    stepStartTimes.delete(stepId);
                  }
                  break;
                }
                case 'output_ready': {
                  const item: FlowItem = {
                    id: `flow-${Date.now()}-output`,
                    type: 'output',
                    data: {
                      title: event.title,
                      content: event.content,
                      intro: event.intro,
                      introHighlight: event.introHighlight,
                      isApplicable: event.isApplicable,  // v6.8: 添加 isApplicable 字段
                    },
                    timestamp,
                  };
                  currentFlowItems = [...currentFlowItems, item];
                  break;
                }
                case 'completion': {
                  const item: FlowItem = {
                    id: `flow-${Date.now()}-completion`,
                    type: 'completion',
                    data: { text: event.data?.text },
                    timestamp,
                  };
                  currentFlowItems = [...currentFlowItems, item];
                  break;
                }
                case 'summarization_start': {
                  const item: FlowItem = {
                    id: `flow-${Date.now()}-summarization`,
                    type: 'summarization',
                    data: {
                      status: 'running',
                      taskClassification: {
                        inputTasks: event.task_classification?.input_tasks || [],
                        outputTasks: event.task_classification?.output_tasks || [],
                        displayTasks: event.task_classification?.display_tasks || [],
                      },
                      contextStats: {
                        originalLength: event.context_stats?.original_length || 0,
                        compressedLength: event.context_stats?.compressed_length || 0,
                        mode: event.context_stats?.mode || '流式生成',
                      },
                    },
                    timestamp,
                  };
                  currentFlowItems = [...currentFlowItems, item];
                  break;
                }
                case 'summarization_complete': {
                  currentFlowItems = currentFlowItems.map((item): FlowItem =>
                    item.type === 'summarization'
                      ? { ...item, data: { ...(item.data as SummarizationFlowData), status: 'done' } }
                      : item
                  );
                  break;
                }
                case 'revision': {
                  // v7.0: 修订请求事件
                  const item: FlowItem = {
                    id: `flow-${Date.now()}-revision`,
                    type: 'revision',
                    data: event.data,
                    timestamp,
                  };
                  currentFlowItems = [...currentFlowItems, item];
                  break;
                }
              }

              // 更新消息的flowItems
              const updated = [...currentMessages];
              const tasksSnapshot = (currentSession?.tasks || []).map((task) => ({ ...task }));
              if (updated[agentMessageIndex]) {
                // v6.8: 合并 flowItems，保留 output 类型项已有的 content（避免被覆盖）
                const existingFlowItems = (updated[agentMessageIndex] as Message).flowItems || [];
                const mergedFlowItems = currentFlowItems.map(item => {
                  if (item.type === 'output') {
                    // 查找已有的 output item，保留其 content
                    const existingOutput = existingFlowItems.find(
                      e => e.type === 'output' && e.id === item.id
                    );
                    if (existingOutput && (existingOutput.data as any).content) {
                      return {
                        ...item,
                        data: { ...item.data, content: (existingOutput.data as any).content }
                      };
                    }
                  }
                  return item;
                });

                updated[agentMessageIndex] = {
                  ...updated[agentMessageIndex],
                  flowItems: mergedFlowItems,
                  tasksSnapshot  // 保存任务列表快照，确保切换章节时不丢失
                };
                sessionManager.updateSession(sessionId, { messages: updated });
                // 节流持久化，确保切换章节时 flowItems 不丢失
                persistMessagesThrottled(updated, streamConversationId, uiMode, false);
              }
            },
            onContent: (chunk) => {
              if (stopRequestedRef.current) return; // 已请求停止时丢弃后续流内容

              // ✅ 打字机效果：将chunk中的每个字符加入队列
              for (const char of chunk) {
                typewriterQueueRef.current.push(char);
              }

              // 启动打字机 Worker（如果未启动）
              if (typewriterWorkerRef.current === null) {
                const processQueue = () => {
                  if (stopRequestedRef.current || typewriterQueueRef.current.length === 0) {
                    // 队列空了，停止 Worker
                    if (typewriterWorkerRef.current) {
                      typewriterWorkerRef.current.postMessage({ type: 'stop' });
                      typewriterWorkerRef.current.terminate();
                      typewriterWorkerRef.current = null;
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
                      // v6.8: 同步更新 flowItems 中 output 类型项的 content
                      const existingFlowItems = (target as Message).flowItems || [];
                      const updatedFlowItems = existingFlowItems.map(item => {
                        if (item.type === 'output') {
                          return {
                            ...item,
                            data: { ...item.data, content: streamingContent }
                          };
                        }
                        return item;
                      });

                      updated[agentMessageIndex] = {
                        ...target,
                        content: streamingContent,
                        agentSteps,
                        flowItems: updatedFlowItems  // v6.8: 更新 flowItems
                      };
                      sessionManager.updateSession(sessionId, { messages: updated });
                      // 节流持久化内容，确保切换章节时不丢失
                      persistMessagesThrottled(updated, streamConversationId, uiMode, false);
                    }
                  }
                };

                // 保存 processQueue 引用，供 Worker 消息处理使用
                processQueueRef.current = processQueue;

                // 创建 Worker 并启动
                const worker = new TypewriterWorker();
                worker.onmessage = () => {
                  processQueueRef.current?.();
                };
                worker.postMessage({ type: 'start', speed: TYPEWRITER_SPEED });
                typewriterWorkerRef.current = worker;
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

                // 清理 Worker
                if (typewriterWorkerRef.current) {
                  typewriterWorkerRef.current.postMessage({ type: 'stop' });
                  typewriterWorkerRef.current.terminate();
                  typewriterWorkerRef.current = null;
                }

                // v5.1: 获取当前消息的 flowItems
                const currentSession = sessionManager.getSession(sessionId);
                const currentMessages = currentSession?.messages || baseMessages;
                const targetMessage = currentMessages[agentMessageIndex] as Message;
                let currentFlowItems = targetMessage?.flowItems || [];
                let finalTasks = currentSession?.tasks || [];

                // ✅ 流结束时：立即完成所有 pending 的任务卡片（避免 running 状态残留）
                if (pendingTaskTimersRef.current.size > 0) {
                  const pendingKeys = Array.from(pendingTaskTimersRef.current.keys());

                  // 清理所有 timers
                  pendingTaskTimersRef.current.forEach((timerId) => clearTimeout(timerId));
                  pendingTaskTimersRef.current.clear();

                  // v6.7: 更新所有 pending step 的状态为 done
                  // 注意：stepId 可能是数字或字符串，需要同时支持
                  const pendingStepIds = pendingKeys
                    .filter(k => k.startsWith('step-'))
                    .map(k => k.replace('step-', ''));
                  if (pendingStepIds.length > 0) {
                    currentFlowItems = currentFlowItems.map(item => {
                      if (item.type === 'step') {
                        const stepIdStr = String((item.data as StepFlowData).stepId);
                        if (pendingStepIds.includes(stepIdStr)) {
                          return {
                            ...item,
                            data: { ...(item.data as StepFlowData), status: 'done' as const }
                          };
                        }
                      }
                      return item;
                    });
                  }

                  // v6.7: 更新所有 pending task 的状态为 completed
                  // 注意：task_id 可能是数字或字符串（UUID），需要同时支持
                  const pendingTaskIds = pendingKeys
                    .filter(k => k.startsWith('task-'))
                    .map(k => k.replace('task-', ''));
                  if (pendingTaskIds.length > 0) {
                    finalTasks = finalTasks.map(t => {
                      const taskIdStr = String(t.task_id);
                      return pendingTaskIds.includes(taskIdStr)
                        ? { ...t, status: 'completed' as const }
                        : t;
                    });
                  }
                }

                const tasksSnapshot = finalTasks.map((task) => ({ ...task }));

                // v6.8: 同步更新 flowItems 中 output 类型项的 content
                const finalFlowItems = currentFlowItems.map(item => {
                  if (item.type === 'output') {
                    return {
                      ...item,
                      data: { ...item.data, content: streamingContent }
                    };
                  }
                  return item;
                });

                const updated = [...currentMessages];
                const target = updated[agentMessageIndex];
                if (target) {
                  updated[agentMessageIndex] = {
                    ...target,
                    content: streamingContent,
                    agentSteps,
                    metadata,
                    flowItems: finalFlowItems,  // v6.8: 使用更新后的 flowItems
                    tasksSnapshot  // v6.2: 保存任务列表快照
                  };
                }

                sessionManager.updateSession(sessionId, {
                  messages: updated,
                  tasks: finalTasks,  // v6.7: 更新 tasks 状态
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
              const tasksSnapshot = (currentSession?.tasks || []).map((task) => ({ ...task }));
              const updated = [...currentMessages];
              const isAbort =
                stopRequestedRef.current ||
                errorMessage.toLowerCase().includes('abort') ||
                errorMessage.toLowerCase().includes('cancel');
              if (updated[agentMessageIndex]) {
                // v5.1: 保留 flowItems
                const existingFlowItems = (updated[agentMessageIndex] as Message).flowItems || [];
                updated[agentMessageIndex] = {
                  role: 'agent',
                  content: isAbort
                    ? '对话已停止。'
                    : '抱歉，遇到了问题：' + errorMessage + '\\n\\n请稍后重试，或联系管理员。',
                  timestamp: new Date().toISOString(),
                  flowItems: existingFlowItems,  // v5.1: 保留执行轨迹
                  tasksSnapshot  // v6.2: 保存任务列表快照
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
        const tasksSnapshot = (currentSession?.tasks || []).map((task) => ({ ...task }));
        if (updated.length > 0 && updated[updated.length - 1].role === 'agent') {
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            content: isAbort
              ? '对话已停止。'
              : '抱歉，遇到了问题：' + errorMessage + '\\n\\n请稍后重试，或联系管理员。',
            timestamp: new Date().toISOString(),
            tasksSnapshot
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
      pendingApproval: null,
      flowItems: []  // v5.0: 清空执行轨迹
    });
    activityStartTimes.current.clear();
    abortControllerRef.current = null;
    lastPersistRef.current = 0;

    // ✅ 清理打字机 Worker 和队列
    if (typewriterWorkerRef.current) {
      typewriterWorkerRef.current.postMessage({ type: 'stop' });
      typewriterWorkerRef.current.terminate();
      typewriterWorkerRef.current = null;
    }
    typewriterQueueRef.current = [];

    // ✅ 清理所有 pending 的任务完成定时器
    pendingTaskTimersRef.current.forEach((timerId) => clearTimeout(timerId));
    pendingTaskTimersRef.current.clear();

    clearCurrentSession();
    refreshSessionSnapshot();
  }, [clearCurrentSession, refreshSessionSnapshot, sessionId, sessionManager]);

  const retryLastMessage = useCallback(async () => {
    if (!lastRequestRef.current) return;
    await sendMessageStream(lastRequestRef.current);
  }, [sendMessageStream]);

  const stopStreaming = useCallback(() => {
    stopRequestedRef.current = true;

    // ✅ 清理打字机 Worker 和队列
    if (typewriterWorkerRef.current) {
      typewriterWorkerRef.current.postMessage({ type: 'stop' });
      typewriterWorkerRef.current.terminate();
      typewriterWorkerRef.current = null;
    }
    typewriterQueueRef.current = [];

    // ✅ 清理所有 pending 的任务完成定时器
    pendingTaskTimersRef.current.forEach((timerId) => clearTimeout(timerId));
    pendingTaskTimersRef.current.clear();

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
      const session = loadSession(targetSessionId);
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
    [loadSession, refreshSessionSnapshot, sessionId, sessionManager]
  );

  const getAllHistorySessions = useCallback(() => {
    return getAllSessions();
  }, [getAllSessions]);

  const createNewConversation = useCallback(async () => {
    activityStartTimes.current.clear();
    await createNewSession();
  }, [createNewSession]);

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
            const resolvedType =
              editorAction?.type === 'continue' || pending.operation === 'append'
                ? 'continue'
                : editorAction?.type === 'insert' || pending.operation === 'insert'
                  ? 'insert'
                  : 'modify';

            window.dispatchEvent(
              new CustomEvent('agent-show-revision', {
                detail: {
                  type: resolvedType,
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
                  type: 'insert',
                  replacement: newContent,
                  position: editorAction?.position,
                  revisionId: `rev-${pending.request_id}-${Date.now()}`
                }
              })
            );
          }
          // 🆕 处理 create/rename 类型（不触发编辑器修订，直接提交审批）
          else if (pending.action_type === 'create' || pending.action_type === 'rename') {
            // 无需触发 editor 修订标记
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

  // v7.0: 更新 revision 状态
  const updateRevisionStatus = useCallback(
    (itemId: string, status: RevisionStatus, snapshot?: {
      originalContent?: string;
      newContent?: string;
      editorPosition?: { from: number; to: number };
      selectedVersion?: number;
    }) => {
      const currentSession = sessionManager.getSession(sessionId);
      const currentMessages = currentSession?.messages || [];

      // 遍历所有消息，找到包含该 revision 的消息并更新
      const updated = currentMessages.map((msg: Message) => {
        if (!msg.flowItems) return msg;

        const updatedFlowItems = msg.flowItems.map((item: FlowItem) => {
          if (item.id === itemId && item.type === 'revision') {
            return {
              ...item,
              data: {
                ...(item.data as RevisionFlowData),
                status,
                // v7.2: 保存快照数据用于撤销/重做
                ...(snapshot || {})
              }
            };
          }
          return item;
        });

        return { ...msg, flowItems: updatedFlowItems };
      });

      sessionManager.updateSession(sessionId, { messages: updated });

      // v7.1: 持久化修订状态，确保刷新后不丢失
      persistMessages(updated, currentSession?.conversationId, currentSession?.mode);
    },
    [sessionId, sessionManager, persistMessages]
  );

  // v7.2: 撤销修订（恢复原始内容）
  const undoRevision = useCallback(
    (itemId: string) => {
      const currentSession = sessionManager.getSession(sessionId);
      const currentMessages = currentSession?.messages || [];

      // 查找该修订的数据
      let revisionData: RevisionFlowData | null = null;
      for (const msg of currentMessages) {
        if (!msg.flowItems) continue;
        for (const item of msg.flowItems as FlowItem[]) {
          if (item.id === itemId && item.type === 'revision') {
            revisionData = item.data as RevisionFlowData;
            break;
          }
        }
        if (revisionData) break;
      }

      if (!revisionData) {
        console.warn('[useAgentChat] revision not found for undo:', itemId);
        return;
      }

      // 派发撤销事件到编辑器
      if (revisionData.originalContent !== undefined || revisionData.revisionType === 'append' || revisionData.revisionType === 'insert') {
        window.dispatchEvent(
          new CustomEvent('agent-undo-revision', {
            detail: {
              itemId,
              revisionType: revisionData.revisionType,
              originalContent: revisionData.originalContent,
              newContent: revisionData.newContent,
              position: revisionData.editorPosition
            }
          })
        );
      }

      // 更新状态为 pending（允许重新采纳）
      updateRevisionStatus(itemId, 'pending');
    },
    [sessionId, sessionManager, updateRevisionStatus]
  );

  // v7.2: 重做修订（重新应用新内容）
  const redoRevision = useCallback(
    (itemId: string) => {
      const currentSession = sessionManager.getSession(sessionId);
      const currentMessages = currentSession?.messages || [];

      // 查找该修订的数据
      let revisionData: RevisionFlowData | null = null;
      for (const msg of currentMessages) {
        if (!msg.flowItems) continue;
        for (const item of msg.flowItems as FlowItem[]) {
          if (item.id === itemId && item.type === 'revision') {
            revisionData = item.data as RevisionFlowData;
            break;
          }
        }
        if (revisionData) break;
      }

      if (!revisionData) {
        console.warn('[useAgentChat] revision not found for redo:', itemId);
        return;
      }

      // 派发重做事件到编辑器
      if (revisionData.newContent !== undefined) {
        const revisionType = revisionData.revisionType;
        const editorType =
          revisionType === 'append' ? 'continue' :
          revisionType === 'insert' ? 'insert' : 'modify';

        window.dispatchEvent(
          new CustomEvent('agent-show-revision', {
            detail: {
              type: editorType,
              original: revisionData.originalContent,
              replacement: revisionData.newContent,
              position: revisionData.editorPosition,
              revisionId: `redo-${itemId}-${Date.now()}`
            }
          })
        );
      }

      // 更新状态为 accepted
      updateRevisionStatus(itemId, 'accepted');
    },
    [sessionId, sessionManager, updateRevisionStatus]
  );

  // v7.1: 批量采纳所有修订
  const acceptAllRevisions = useCallback(
    (itemIds: string[]) => {
      itemIds.forEach(id => updateRevisionStatus(id, 'accepted'));
    },
    [updateRevisionStatus]
  );

  // v7.1: 批量弃用所有修订
  const discardAllRevisions = useCallback(
    (itemIds: string[]) => {
      itemIds.forEach(id => updateRevisionStatus(id, 'discarded'));
    },
    [updateRevisionStatus]
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
    flowItems: (sessionState.flowItems || []) as FlowItem[],  // v5.0: 执行轨迹项
    sendMessage,
    sendMessageStream,
    clearMessages,
    retryLastMessage,
    sessionId: persistedSessionId,
    conversationId: sessionState.conversationId,
    loadHistorySession,
    getAllHistorySessions,
    createNewConversation,
    pendingApproval: sessionState.pendingApproval as ApprovalRequest | null,
    submitApproval,
    updateRevisionStatus,
    acceptAllRevisions,
    discardAllRevisions,
    undoRevision,      // v7.2
    redoRevision,      // v7.2
    stopStreaming
  };
}
