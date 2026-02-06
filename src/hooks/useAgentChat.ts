
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
  /** 锚点定位：修改点前的文本（30-50字） */
  before_anchor?: string;
  /** 锚点定位：修改点后的文本（30-50字） */
  after_anchor?: string;
  /** 🆕 节点 ID（最高优先级定位） */
  node_id?: string;
  /** 🆕 段落索引（可用于从 getAllNodes() 获取 node_id） */
  paragraph_index?: number;
}

export interface ApprovalRequest {
  request_id: string;
  action_type: 'edit' | 'rewrite' | 'insert' | 'create' | 'rename' | 'continue' | 'update_content' | 'delete';
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
  work_id?: string;
  conversation_id?: string;
  // 🆕 InlineAI 编辑器操作
  editor_action?: EditorAction;
}

interface UseAgentChatReturn {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  suggestedActions: string[];
  tasks: Task[];
  currentTaskId: number | string | null;
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
  // v8.0: 批量操作管理
  hasOperations: boolean;  // 是否有待确认的操作
  acceptAllOperations: () => Promise<void>;  // 采纳所有操作
  rollbackAllOperations: () => Promise<void>;  // 回滚所有操作
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
    let cancelled = false;
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
    } else if (useBackendSessions) {
      (async () => {
        try {
          const backendMessages = await agentApi.getSessionMessages(sessionId, { order: 'asc', limit: 200 });
          if (cancelled || backendMessages.length === 0) return;

          const mapped = backendMessages.map((m: any) => ({
            role: (m.role === 'assistant' ? 'agent' : m.role) as Message['role'],
            content: m.content,
            metadata: m.metadata,
            timestamp: m.created_at || new Date().toISOString()
          }));

          sessionManager.updateSession(sessionId, {
            messages: mapped as Message[],
            conversationId: sessionId,
            mode: 'plan'
          });
          saveSessionRef.current(mapped as Message[], sessionId, { mode: 'plan', workId, chapterId });
          refreshSessionSnapshot();
        } catch (error) {
          console.warn('[useAgentChat] Failed to hydrate session from backend:', error);
        }
      })();
    }
    refreshSessionSnapshot();

    sessionManager.setActiveSession(sessionId);
    const unsubscribe = sessionManager.addListener((id, state) => {
      if (id === sessionId) {
        setSessionState({ ...state });
      }
    });

    return () => {
      cancelled = true;
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
  }, [chapterId, loadSession, refreshSessionSnapshot, sessionId, sessionManager, useBackendSessions, workId]);

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
            chapter_id: chapterId,
            conversation_id: sessionId
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
        const normalizeTaskId = (id: any) => {
          if (id === null || id === undefined) return id;
          if (typeof id === 'number') return id;
          const asNumber = Number(id);
          return Number.isNaN(asNumber) ? id : asNumber;
        };

        const normalizeTaskStatus = (status?: string) => {
          if (!status) return 'pending';
          if (status === 'in_progress') return 'running';
          return status;
        };

        const getTaskDescription = (task: any) =>
          cleanTaskDescription(task?.description ?? task?.title ?? '');

        const applyPlanUpdate = (plan: any, forceUpdate: boolean = false) => {
          const currentTasks = sessionManager.getSession(sessionId)?.tasks || [];
          const currentTaskMap = new Map(
            currentTasks.map(t => [normalizeTaskId(t.task_id), t])
          );
          const isUpdate = forceUpdate || plan?.is_update === true;
          const sourceTasks = Array.isArray(plan?.tasks) ? plan.tasks : [];

          const updatedTasks: Task[] = sourceTasks.map((t: any) => {
            const taskId = normalizeTaskId(t.task_id);
            const existing = currentTaskMap.get(taskId);

            // 重规划时：保留已完成任务的状态
            if (isUpdate && existing && existing.status === 'completed') {
              return existing;
            }

            // 保留正在运行任务的状态
            if (existing && existing.status === 'running') {
              return { ...existing, description: getTaskDescription(t) };
            }

            return {
              task_id: taskId,
              description: getTaskDescription(t),
              tool: t.tool,
              estimated_time: t.estimated_time,
              status: normalizeTaskStatus(t.status) as Task['status'],
            };
          });

          sessionManager.updateSession(sessionId, { tasks: updatedTasks });
        };

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
                    applyPlanUpdate(plan);
                  },
                  onPlanUpdate: (plan: any) => {
                    applyPlanUpdate(plan, true);
                  },
                  onTaskStart: (task: any) => {
                    const taskId = normalizeTaskId(task.task_id);
                    taskStartTimes.set(taskId, Date.now());

                    // v6.0: flowItems 由 onFlowEvent 的 step_start 处理，这里只更新任务状态
                    const updatedTasks = (sessionManager.getSession(sessionId)?.tasks || []).map((t) =>
                      normalizeTaskId(t.task_id) === taskId ? { ...t, status: 'running' as const } : t
                    );
                    sessionManager.updateSession(sessionId, {
                      currentTaskId: taskId,
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
                    const taskId = normalizeTaskId(taskDone.task_id);
                    const startTime = taskStartTimes.get(taskId);
                    let elapsedTime = taskDone.elapsed_time || 0;
                    if (startTime && elapsedTime === 0) {
                      elapsedTime = (Date.now() - startTime) / 1000;
                    }
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
                          normalizeTaskId(t.task_id) === taskId
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
                    // 更新任务的进度状态（仅字符串）
                    const taskId = normalizeTaskId(progress.task_id);
                    const status = progress.status;
                    if (taskId !== undefined && typeof status === 'string' && status) {
                      sessionManager.updateSession(sessionId, {
                        tasks: (sessionManager.getSession(sessionId)?.tasks || []).map((t) =>
                          normalizeTaskId(t.task_id) === taskId ? { ...t, progress_status: status } : t
                        )
                      });
                    }
                  },
                  onThinking: (thinking: any) => {
                    const summary = typeof thinking === 'string'
                      ? thinking
                      : (thinking?.summary ?? thinking?.content ?? thinking?.text ?? '');
                    const nextStep = thinking?.next_step ? `下一步：${thinking.next_step}` : '';
                    const description = [summary, nextStep].filter(Boolean).join(' ');
                    if (!description) return;
                    const activity: ActivityItem = {
                      id: `thinking-${Date.now()}`,
                      type: 'thinking',
                      description,
                      timestamp: new Date().toISOString(),
                      status: 'completed'
                    };
                    sessionManager.updateSession(sessionId, {
                      activities: [
                        ...(sessionManager.getSession(sessionId)?.activities || []),
                        activity
                      ]
                    });
                  },
                  // 🆕 planning 模式也需要处理审批请求
                  onApprovalRequest: (approvalReq: any) => {
                    const editorAction = approvalReq.editor_action;
                    const pendingData = {
                      request_id: approvalReq.request_id,
                      action_type: approvalReq.action_type,
                      operation: approvalReq.operation,
                      original_content: approvalReq.original_content,
                      new_content: approvalReq.new_content,
                      description: approvalReq.description,
                      versions: approvalReq.versions,
                      editor_action: editorAction,
                      work_id: approvalReq.work_id,
                      conversation_id: approvalReq.conversation_id,
                      chapter_id: approvalReq.chapter_id,
                      chapter_title: approvalReq.chapter_title,
                      new_title: approvalReq.new_title,
                      old_title: approvalReq.old_title,
                      order: approvalReq.order,
                      content: approvalReq.content
                    };

                    const chapterBoundActions = ['edit', 'rewrite', 'insert', 'continue', 'update_content'];
                    const chapterMismatch = Boolean(
                      chapterId &&
                      approvalReq.chapter_id &&
                      chapterBoundActions.includes(approvalReq.action_type) &&
                      approvalReq.chapter_id !== chapterId
                    );
                    if (!chapterMismatch) {
                      sessionManager.updateSession(sessionId, {
                        pendingApproval: pendingData
                      });
                    } else {
                      console.warn('[useAgentChat] 忽略跨章节 pendingApproval (planning)', {
                        requestId: approvalReq.request_id,
                        currentChapterId: chapterId,
                        targetChapterId: approvalReq.chapter_id
                      });
                    }

                    // 🆕 章节操作的乐观更新（立即在目录中显示）
                    const actionType = approvalReq.action_type;
                    const targetWorkId = approvalReq.work_id || workId;

                    if (targetWorkId && ['create', 'rename', 'delete'].includes(actionType)) {
                      window.dispatchEvent(
                        new CustomEvent('agent-chapter-preview', {
                          detail: {
                            action_type: actionType,
                            request_id: approvalReq.request_id,
                            work_id: targetWorkId,
                            chapter_id: approvalReq.chapter_id,
                            chapter_title: approvalReq.chapter_title,
                            new_title: approvalReq.new_title,
                            old_title: approvalReq.old_title,
                            content: approvalReq.content,
                            order: approvalReq.order
                          }
                        })
                      );
                      console.log('[useAgentChat] 🆕 派发章节预览事件 (planning):', actionType, approvalReq.chapter_title);
                    }

                    // 注意：修订显示由 revision 流事件统一派发，避免重复插入
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
                    const editorAction = approvalReq.editor_action;
                    const pendingData = {
                      request_id: approvalReq.request_id,
                      action_type: approvalReq.action_type,
                      operation: approvalReq.operation,
                      original_content: approvalReq.original_content,
                      new_content: approvalReq.new_content,
                      description: approvalReq.description,
                      versions: approvalReq.versions,
                      // 🆕 InlineAI: 包含 editor_action
                      editor_action: editorAction,
                      // 🆕 章节操作相关字段
                      work_id: approvalReq.work_id,
                      conversation_id: approvalReq.conversation_id,
                      chapter_id: approvalReq.chapter_id,
                      chapter_title: approvalReq.chapter_title,
                      new_title: approvalReq.new_title,
                      old_title: approvalReq.old_title,
                      order: approvalReq.order,
                      content: approvalReq.content
                    };

                    const chapterBoundActions = ['edit', 'rewrite', 'insert', 'continue', 'update_content'];
                    const chapterMismatch = Boolean(
                      chapterId &&
                      approvalReq.chapter_id &&
                      chapterBoundActions.includes(approvalReq.action_type) &&
                      approvalReq.chapter_id !== chapterId
                    );
                    if (!chapterMismatch) {
                      sessionManager.updateSession(sessionId, {
                        pendingApproval: pendingData
                      });
                    } else {
                      console.warn('[useAgentChat] 忽略跨章节 pendingApproval (react)', {
                        requestId: approvalReq.request_id,
                        currentChapterId: chapterId,
                        targetChapterId: approvalReq.chapter_id
                      });
                    }

                    // 🆕 章节操作的乐观更新（立即在目录中显示）
                    const actionType = approvalReq.action_type;
                    const targetWorkId = approvalReq.work_id || workId;

                    if (targetWorkId && ['create', 'rename', 'delete'].includes(actionType)) {
                      // 派发事件通知 WorkDetailView 进行乐观更新
                      window.dispatchEvent(
                        new CustomEvent('agent-chapter-preview', {
                          detail: {
                            action_type: actionType,
                            request_id: approvalReq.request_id,
                            work_id: targetWorkId,
                            chapter_id: approvalReq.chapter_id,
                            chapter_title: approvalReq.chapter_title,
                            new_title: approvalReq.new_title,
                            old_title: approvalReq.old_title,
                            content: approvalReq.content,
                            order: approvalReq.order
                          }
                        })
                      );
                      console.log('[useAgentChat] 🆕 派发章节预览事件:', actionType, approvalReq.chapter_title);
                    }

                    // 🆕 立即派发事件到编辑器，显示修订标记（红删绿增）
                    // v8.4: 修复 - 补充派发 agent-show-revision 事件（之前是占位符代码）
                    if (editorAction || approvalReq.new_content) {
                      // 映射 operation 到编辑器操作类型
                      let editorType: 'modify' | 'continue' | 'insert' = 'modify';
                      if (approvalReq.operation === 'append') {
                        editorType = 'continue';
                      } else if (approvalReq.operation === 'insert') {
                        editorType = 'insert';
                      }

                      const position = editorAction?.position || approvalReq.position;

                      window.dispatchEvent(new CustomEvent('agent-show-revision', {
                        detail: {
                          revisionId: approvalReq.request_id,
                          requestId: approvalReq.request_id,
                          chapterId: approvalReq.chapter_id,
                          type: editorType,
                          replacement: approvalReq.new_content,
                          original: approvalReq.original_content,
                          position: position,
                          beforeAnchor: editorAction?.before_anchor,
                          afterAnchor: editorAction?.after_anchor,
                          nodeId: editorAction?.node_id,
                          paragraphIndex: editorAction?.paragraph_index,
                        }
                      }));
                      console.log('[useAgentChat] 🆕 派发修订事件到编辑器:', editorType, approvalReq.request_id);
                    }

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
                      reason: event.reason,
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
                // Explore 探索事件 (2026-01-17)
                case 'explore_round': {
                  const item: FlowItem = {
                    id: `flow-${Date.now()}-explore-round-${event.roundIdx}`,
                    type: 'explore_round',
                    data: {
                      stepId: event.stepId,
                      roundIdx: event.roundIdx,
                      title: event.title,
                      reason: event.reason,  // AI 决策理由（完整）
                      toolCalls: event.toolCalls,
                      hitCount: event.hitCount,
                      missingItems: event.missingItems,
                      statusText: event.statusText,
                      evidences: event.evidences,
                      reviewStatus: event.reviewStatus,
                      status: event.status,
                    },
                    timestamp,
                  };
                  currentFlowItems = [...currentFlowItems, item];
                  break;
                }
                case 'explore_summary': {
                  const item: FlowItem = {
                    id: `flow-${Date.now()}-explore-summary`,
                    type: 'explore_summary',
                    data: {
                      stepId: event.stepId,
                      totalRounds: event.totalRounds,
                      summary: event.summary,
                      nextAction: event.nextAction,
                      nextTool: event.nextTool,
                      sufficient: event.sufficient,
                      coverage: event.coverage,
                      stats: event.stats,
                    },
                    timestamp,
                  };
                  currentFlowItems = [...currentFlowItems, item];
                  break;
                }
                case 'revision': {
                  // v7.5: 非阻塞式修订 - 嵌入到最后一个 step 中 + 派发事件到编辑器
                  const revisionItemId = `flow-${Date.now()}-revision`;
                  const revisionData = event.data;

                  // 查找最后一个 step 类型的 FlowItem
                  const lastStepIndex = [...currentFlowItems].reverse().findIndex(item => item.type === 'step');

                  if (lastStepIndex !== -1) {
                    // 计算正确的索引（因为我们是从后往前找的）
                    const actualIndex = currentFlowItems.length - 1 - lastStepIndex;
                    // 将 revision 嵌入到 step 中
                    currentFlowItems = currentFlowItems.map((item, index) => {
                      if (index === actualIndex && item.type === 'step') {
                        const stepData = item.data as StepFlowData;
                        return {
                          ...item,
                          data: {
                            ...stepData,
                            revision: revisionData,
                            revisionItemId: revisionItemId
                          }
                        };
                      }
                      return item;
                    });
                  } else {
                    // 如果没有找到 step，则作为独立的 FlowItem 添加（兜底）
                    const item: FlowItem = {
                      id: revisionItemId,
                      type: 'revision',
                      data: revisionData,
                      timestamp,
                    };
                    currentFlowItems = [...currentFlowItems, item];
                  }

                  // v7.5: 派发事件到编辑器显示修订标记
                  if (revisionData.content || revisionData.editorAction) {
                    const editorAction = revisionData.editorAction;
                    const position = editorAction?.position || revisionData.position;

                    // 映射 revisionType 到编辑器操作类型
                    let editorType: 'modify' | 'continue' | 'insert' = 'modify';
                    if (revisionData.revisionType === 'append' || revisionData.operation === 'append') {
                      editorType = 'continue';
                    } else if (revisionData.revisionType === 'insert' || revisionData.operation === 'insert') {
                      editorType = 'insert';
                    }

                    window.dispatchEvent(new CustomEvent('agent-show-revision', {
                      detail: {
                        revisionId: revisionItemId,
                        requestId: revisionData.requestId,
                        chapterId: revisionData.chapterId,
                        type: editorType,
                        replacement: revisionData.content,  // NovelEditor 期望 replacement
                        original: revisionData.originalContent,
                        position: position,
                        beforeAnchor: editorAction?.before_anchor,
                        afterAnchor: editorAction?.after_anchor,
                        nodeId: editorAction?.node_id,
                        paragraphIndex: editorAction?.paragraph_index,
                      }
                    }));
                  }
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
                // V3.4.1 优化：批量更新计数器
                let charsSinceLastUpdate = 0;

                // ✅ 内容感知的动态批量大小：表格/代码块使用更大的批量，减少渲染次数
                const getDynamicBatchSize = (content: string): number => {
                  // 检测是否在表格中间（最后 200 字符包含 | 但没有完整的行结束）
                  const recentContent = content.slice(-200);
                  const isInTableRow = recentContent.includes('|') && !recentContent.endsWith('\n');

                  // 检测是否包含代码块（只检查标记存在，避免贪心匹配）
                  const hasCodeBlock = content.includes('```');

                  if (isInTableRow) return 200;   // 表格行中：200 字符更新一次
                  if (hasCodeBlock) return 150;   // 代码块：150 字符更新一次
                  return 50;                      // 普通文本：50 字符更新一次
                };

                const processQueue = () => {
                  if (stopRequestedRef.current || typewriterQueueRef.current.length === 0) {
                    // 队列空了，先刷新剩余内容到 UI，然后停止 Worker
                    if (charsSinceLastUpdate > 0) {
                      // 最后一次更新 UI
                      const currentSession = sessionManager.getSession(sessionId);
                      const currentMessages = currentSession?.messages || baseMessages;
                      const updated = [...currentMessages];
                      const target = updated[agentMessageIndex];
                      if (target) {
                        const existingFlowItems = (target as Message).flowItems || [];
                        const updatedFlowItems = existingFlowItems.map(item => {
                          if (item.type === 'output') {
                            return { ...item, data: { ...item.data, content: streamingContent } };
                          }
                          return item;
                        });
                        updated[agentMessageIndex] = {
                          ...target,
                          content: streamingContent,
                          agentSteps,
                          flowItems: updatedFlowItems
                        };
                        sessionManager.updateSession(sessionId, { messages: updated });
                      }
                      charsSinceLastUpdate = 0;
                    }
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
                    charsSinceLastUpdate++;

                    // ✅ 使用动态批量大小：根据内容类型调整更新频率
                    const currentBatchSize = getDynamicBatchSize(streamingContent);
                    if (charsSinceLastUpdate >= currentBatchSize) {
                      const currentSession = sessionManager.getSession(sessionId);
                      const currentMessages = currentSession?.messages || baseMessages;
                      const updated = [...currentMessages];
                      const target = updated[agentMessageIndex];
                      if (target) {
                        // v6.8: 同步更新 flowItems 中 output 类型项的 content
                        const existingFlowItems = (target as Message).flowItems || [];
                        const updatedFlowItems = existingFlowItems.map(item => {
                          if (item.type === 'output') {
                            return { ...item, data: { ...item.data, content: streamingContent } };
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
                      charsSinceLastUpdate = 0;
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
                // V3.4.1 修复：使用 join 一次性合并，避免 O(n²) 的 shift 循环
                if (typewriterQueueRef.current.length > 0) {
                  streamingContent += typewriterQueueRef.current.join('');
                  typewriterQueueRef.current = [];
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
              // V3.4.1 修复：对于长内容（超过 5000 字符），直接完成，不等待打字机效果
              const queueLength = typewriterQueueRef.current.length;
              if (queueLength === 0) {
                finishStream();
              } else if (queueLength > 5000) {
                // 长内容：直接跳过打字机效果，立即完成
                console.log(`[useAgentChat] 长内容（${queueLength}字符），跳过打字机效果直接完成`);
                finishStream();
              } else {
                // 等待打字机效果完成
                const waitForQueue = setInterval(() => {
                  // 如果 Worker 已停止但队列不为空，直接完成（避免死锁）
                  if (typewriterWorkerRef.current === null && typewriterQueueRef.current.length > 0) {
                    clearInterval(waitForQueue);
                    finishStream();
                    return;
                  }
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
        const chapterBoundActions = new Set<ApprovalRequest['action_type']>([
          'edit', 'rewrite', 'insert', 'continue', 'update_content'
        ]);
        const currentChapterId = chapterId;
        const targetChapterId = pending.chapter_id;
        const resolvedTargetChapterId = targetChapterId || currentChapterId;
        const chapterMismatch = Boolean(
          currentChapterId &&
          targetChapterId &&
          chapterBoundActions.has(pending.action_type) &&
          currentChapterId !== targetChapterId
        );
        if (chapterMismatch && targetChapterId) {
          console.warn('[useAgentChat] chapter mismatch when submit approval', {
            requestId: pending.request_id,
            currentChapterId,
            targetChapterId,
            actionType: pending.action_type
          });
          if (targetChapterId) {
            window.dispatchEvent(
              new CustomEvent('agent-jump-revision', {
                detail: {
                  workId: pending.work_id || workId,
                  chapterId: targetChapterId,
                  requestId: pending.request_id,
                  revisionId: pending.request_id,
                }
              })
            );
          }
        }

        if (approved) {
          // 🆕 采纳时：修订标记已经显示，现在派发"确认采纳"事件
          // 对于 rewrite 类型，如果用户选择了不同版本，需要更新显示
          if (pending.action_type === 'rewrite' && selectedVersion !== undefined && selectedVersion > 0) {
            const versions = pending.versions;
            if (versions && versions[selectedVersion]) {
              const selectedContent = versions[selectedVersion].content;
              const editorAction = pending.editor_action;

              // 用户选择了非默认版本，需要更新编辑器中的修订内容
              window.dispatchEvent(
                new CustomEvent('agent-update-revision', {
                  detail: {
                    replacement: selectedContent,
                    position: editorAction?.position
                  }
                })
              );
            }
          }

          // 派发"确认采纳"事件，让编辑器应用修改（移除标记，保留新内容）
          if (!chapterMismatch) {
            window.dispatchEvent(
              new CustomEvent('agent-accept-revision', {
                detail: { request_id: pending.request_id, chapter_id: resolvedTargetChapterId }
              })
            );
            console.log('[useAgentChat] ✅ 派发采纳事件');
          }

          // 🆕 处理 create/rename 类型（不触发编辑器修订，直接提交审批）
          if (pending.action_type === 'create' || pending.action_type === 'rename') {
            // 无需触发 editor 修订标记
          }
        } else {
          // v7.6: 弃用时：派发弃用事件，移除修订标记，恢复原文
          if (!chapterMismatch) {
            window.dispatchEvent(
              new CustomEvent('agent-discard-revision', {
                detail: { request_id: pending.request_id, chapter_id: resolvedTargetChapterId }
              })
            );
            console.log('[useAgentChat] ❌ 派发弃用事件');
          }

          // 🆕 章节操作弃用时：派发撤销事件
          const targetWorkId = pending.work_id || workId;
          if (targetWorkId && ['create', 'rename', 'delete'].includes(pending.action_type || '')) {
            window.dispatchEvent(
              new CustomEvent('agent-chapter-revert', {
                detail: {
                  action_type: pending.action_type,
                  request_id: pending.request_id,
                  work_id: targetWorkId,
                  chapter_id: targetChapterId
                }
              })
            );
            console.log('[useAgentChat] 🔄 派发章节撤销事件:', pending.action_type);
          }
        }

        const currentConversationId =
          sessionManager.getSession(sessionId)?.conversationId || pending.conversation_id;
        await agentApi.submitApprovalResponse({
          request_id: pending.request_id,
          approved,
          selected_version: selectedVersion,
          chapter_id: resolvedTargetChapterId,
          work_id: pending.work_id || workId,
          conversation_id: currentConversationId
        });

        // 🆕 采纳后派发确认事件，通知 WorkDetailView 刷新列表（覆盖跨章节内容修订）
        const targetWorkId = pending.work_id || workId;
        if (approved && targetWorkId) {
          window.dispatchEvent(
            new CustomEvent('agent-chapter-confirm', {
              detail: { work_id: targetWorkId }
            })
          );
          if (chapterMismatch && targetChapterId) {
            window.dispatchEvent(
              new CustomEvent('agent-jump-revision', {
                detail: {
                  workId: pending.work_id || workId,
                  chapterId: targetChapterId,
                  requestId: pending.request_id,
                  revisionId: pending.request_id,
                }
              })
            );
          }
          console.log('[useAgentChat] ✅ 派发章节确认事件，刷新列表');
        }

        // 🆕 无论批准还是拒绝，都清理 pendingApproval 状态
        sessionManager.updateSession(sessionId, { pendingApproval: null });
      } catch (err: any) {
        console.error('[useAgentChat] submit approval failed:', err);
        const statusCode = err?.response?.status;
        const detail = err?.response?.data?.detail || err.message || 'Approval failed';
        const isRecoverableConflict = statusCode === 409;
        if (isRecoverableConflict) {
          if (pending.chapter_id) {
            window.dispatchEvent(
              new CustomEvent('agent-jump-revision', {
                detail: {
                  workId: pending.work_id || workId,
                  chapterId: pending.chapter_id,
                  requestId: pending.request_id,
                  revisionId: pending.request_id,
                }
              })
            );
          }
          sessionManager.updateSession(sessionId, {
            error: `${detail} 已为你定位到目标章节，请再次点击采纳。`,
            pendingApproval: pending
          });
          return;
        }
        sessionManager.updateSession(sessionId, {
          error: detail,
          pendingApproval: null  // 🆕 错误时也清理状态
        });
      }
    },
    [chapterId, sessionId, sessionManager, workId]
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
          // v7.3: 处理嵌入在 step 中的 revision
          if (item.type === 'step') {
            const stepData = item.data as StepFlowData;
            // v7.4: 支持 revisionItemId 或 item.id 匹配
            if ((stepData.revisionItemId === itemId || item.id === itemId) && stepData.revision) {
              return {
                ...item,
                data: {
                  ...stepData,
                  revision: {
                    ...stepData.revision,
                    status,
                    ...(snapshot || {})
                  }
                }
              };
            }
          }

          // 处理独立的 revision（兜底）
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

      // 查找该修订的数据（支持嵌入在 step 中的 revision）
      let revisionData: RevisionFlowData | null = null;
      for (const msg of currentMessages) {
        if (!msg.flowItems) continue;
        for (const item of msg.flowItems as FlowItem[]) {
          // v7.3: 检查嵌入在 step 中的 revision
          if (item.type === 'step') {
            const stepData = item.data as StepFlowData;
            // v7.4: 支持 revisionItemId 或 item.id 匹配
            if ((stepData.revisionItemId === itemId || item.id === itemId) && stepData.revision) {
              revisionData = stepData.revision;
              break;
            }
          }
          // 检查独立的 revision
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

      // 查找该修订的数据（支持嵌入在 step 中的 revision）
      let revisionData: RevisionFlowData | null = null;
      for (const msg of currentMessages) {
        if (!msg.flowItems) continue;
        for (const item of msg.flowItems as FlowItem[]) {
          // v7.3: 检查嵌入在 step 中的 revision
          if (item.type === 'step') {
            const stepData = item.data as StepFlowData;
            // v7.4: 支持 revisionItemId 或 item.id 匹配
            if ((stepData.revisionItemId === itemId || item.id === itemId) && stepData.revision) {
              revisionData = stepData.revision;
              break;
            }
          }
          // 检查独立的 revision
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

  // v8.0: 批量操作管理 - 检查是否有待确认的操作
  const [hasOperations, setHasOperations] = useState(false);

  // 检查操作日志
  useEffect(() => {
    const checkOperations = async () => {
      if (!sessionState.conversationId) {
        setHasOperations(false);
        return;
      }
      try {
        const result = await agentApi.getOperations(sessionState.conversationId);
        setHasOperations(result.operations && result.operations.length > 0);
      } catch {
        setHasOperations(false);
      }
    };
    // 只在 isLoading 变为 false 时检查（即流式响应结束后）
    if (!sessionState.isLoading && sessionState.conversationId) {
      checkOperations();
    }
  }, [sessionState.isLoading, sessionState.conversationId]);

  // v8.0: 采纳所有操作
  const acceptAllOperations = useCallback(async () => {
    console.log('[useAgentChat] acceptAllOperations 被调用, conversationId:', sessionState.conversationId);
    if (!sessionState.conversationId) {
      console.warn('[useAgentChat] acceptAllOperations: conversationId 为空，操作取消');
      return;
    }
    try {
      console.log('[useAgentChat] 正在调用 API acceptOperations...');
      await agentApi.acceptOperations(sessionState.conversationId);
      setHasOperations(false);
      console.log('[useAgentChat] 所有操作已采纳');

      // v8.1: 派发采纳事件到编辑器，清除修订标记并保留新内容
      window.dispatchEvent(new CustomEvent('agent-accept-all-revisions', {
        detail: { conversationId: sessionState.conversationId }
      }));
      console.log('[useAgentChat] ✅ 派发采纳事件到编辑器');
    } catch (error) {
      console.error('[useAgentChat] 采纳操作失败:', error);
    }
  }, [sessionState.conversationId]);

  // v8.0: 回滚所有操作
  const rollbackAllOperations = useCallback(async () => {
    console.log('[useAgentChat] rollbackAllOperations 被调用, conversationId:', sessionState.conversationId);
    if (!sessionState.conversationId) {
      console.warn('[useAgentChat] rollbackAllOperations: conversationId 为空，操作取消');
      return;
    }
    try {
      console.log('[useAgentChat] 正在调用 API rollbackOperations...');
      const result = await agentApi.rollbackOperations(sessionState.conversationId);
      setHasOperations(false);
      console.log(`[useAgentChat] 已回滚 ${result.rolled_back} 个操作`);

      // v8.1: 派发撤销事件到编辑器，清除修订标记并恢复原文
      window.dispatchEvent(new CustomEvent('agent-discard-all-revisions', {
        detail: { conversationId: sessionState.conversationId, rolledBack: result.rolled_back }
      }));
      console.log('[useAgentChat] ❌ 派发撤销事件到编辑器');

      // 触发刷新事件，通知编辑器重新加载数据
      window.dispatchEvent(new CustomEvent('agent-operations-rollback', {
        detail: { conversationId: sessionState.conversationId, rolledBack: result.rolled_back }
      }));
    } catch (error) {
      console.error('[useAgentChat] 回滚操作失败:', error);
    }
  }, [sessionState.conversationId]);

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
    stopStreaming,
    // v8.0: 批量操作管理
    hasOperations,
    acceptAllOperations,
    rollbackAllOperations
  };
}
