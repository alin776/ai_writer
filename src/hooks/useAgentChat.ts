
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { agentApi } from '@/services/agentApi';
import { changesApi } from '@/services/changesApi';
import { DataService } from '@/services/DataService';
import { useConversationPersistence } from './useConversationPersistence';
import { getGlobalSessionManager } from '@/contexts/SessionContext';
import type { SessionState } from './SessionStateManager';
import type { AgentChatRequest, AgentChatResponse, FlowItem, ToolFlowData, StepFlowData, SummarizationFlowData, RevisionFlowData, RevisionStatus } from '@/types/agent';
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
  flowItems?: FlowItem[];
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
  action_type: 'edit' | 'rewrite' | 'insert' | 'create' | 'rename';
  apply_state?: 'pending' | 'applied' | 'rejected' | 'failed';
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
    (messagesToSave: Message[], conversation?: string, mode?: 'plan' | 'chat') => {
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
    (messagesToSave: Message[], conversation?: string, mode?: 'plan' | 'chat', force: boolean = false) => {
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
      // 从最后一条 agent 消息恢复状态
      const lastAgentMessage = [...persisted.messages].reverse().find(m => m.role === 'agent');

      sessionManager.updateSession(sessionId, {
        messages: persisted.messages as Message[],
        conversationId: persisted.conversationId || undefined,
        mode: persisted.mode || 'plan',
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
      // request.mode 仅支持 planning，转换为前端 UI 模式
      const uiMode = 'plan' as const;
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
          flowItems: [{  // v5.1: 预填 agent_header，让 logo 和 Thinking... 同时出现
            id: `flow-${Date.now()}-header`,
            type: 'agent_header',
            data: { name: '文枢AI', badge: '' },
            timestamp: now,
          }]
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
            // 🆕 planning 模式也需要处理审批请求
            onApprovalRequest: (approvalReq: any) => {
              const editorAction = approvalReq.editor_action;
              const pendingData = {
                request_id: approvalReq.request_id,
                action_type: approvalReq.action_type,
                apply_state: approvalReq.apply_state || 'pending',
                operation: approvalReq.operation,
                original_content: approvalReq.original_content,
                new_content: approvalReq.new_content,
                description: approvalReq.description,
                versions: approvalReq.versions,
                editor_action: editorAction,
                work_id: approvalReq.work_id,
                chapter_id: approvalReq.chapter_id,
                chapter_title: approvalReq.chapter_title,
                new_title: approvalReq.new_title,
                old_title: approvalReq.old_title,
                order: approvalReq.order,
                content: approvalReq.content
              };

              sessionManager.updateSession(sessionId, {
                pendingApproval: pendingData
              });

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
            },
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
                  // 替换已有的 agent_header（预填或重复推送），避免出现两个 logo
                  const hasExisting = currentFlowItems.some(fi => fi.type === 'agent_header');
                  currentFlowItems = hasExisting
                    ? currentFlowItems.map(fi => fi.type === 'agent_header' ? item : fi)
                    : [...currentFlowItems, item];
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
                    description: event.description,
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
                          // step_complete 的完成摘要优先，回退到 step_start 的 AI 意图描述
                          const finalDescription = cleanTaskDescription(eventDescription) || stepData.description;
                          return {
                            ...item,
                            data: { ...stepData, status: 'done' as const, description: finalDescription, toolCall: eventToolCall }
                          };
                        }
                        return item;
                      });

                      // 更新消息的 flowItems
                      const updated = [...currentMessages];
                      updated[agentMessageIndex] = {
                        ...targetMessage,
                        flowItems: latestFlowItems,
                      };
                      sessionManager.updateSession(sessionId, { messages: updated });
                    }, delayMs);
                    pendingTaskTimersRef.current.set(timerKey, timerId);
                  } else {
                    // 立即更新：直接修改 currentFlowItems，让后续代码统一更新
                    currentFlowItems = currentFlowItems.map(item => {
                      if (item.type === 'step' && (item.data as StepFlowData).stepId === stepId) {
                        const stepData = item.data as StepFlowData;
                        // step_complete 的完成摘要优先，回退到 step_start 的 AI 意图描述
                        const finalDescription = cleanTaskDescription(eventDescription) || stepData.description;
                        return {
                          ...item,
                          data: { ...stepData, status: 'done' as const, description: finalDescription, toolCall: eventToolCall }
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
                  // 章节级替换（operation=content/replace_all）不走段落修订标记，避免定位失败
                  const revisionOperation = (revisionData as any)?.operation;
                  const isChapterReplace = revisionOperation === 'content' || revisionOperation === 'replace_all';
                  if (!isChapterReplace && (revisionData.content || revisionData.editorAction)) {
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
                  // 检测是否包含表格（Markdown 表格语法：| xxx | xxx |）
                  const hasTable = /\|[^|]+\|[^|]+\|/.test(content);
                  // 检测是否包含代码块
                  const hasCodeBlock = /```[\s\S]*/.test(content);
                  // 检测是否在表格中间（最后 200 字符包含 | 但没有完整的行结束）
                  const recentContent = content.slice(-200);
                  const isInTableRow = recentContent.includes('|') && !recentContent.endsWith('\n');

                  if (hasTable || isInTableRow) return 200;  // 表格：200 字符更新一次
                  if (hasCodeBlock) return 150;              // 代码块：150 字符更新一次
                  return 50;                                 // 普通文本：50 字符更新一次
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

                // ✅ 流结束时：立即完成所有 pending 的步骤卡片（避免 running 状态残留）
                if (pendingTaskTimersRef.current.size > 0) {
                  const pendingKeys = Array.from(pendingTaskTimersRef.current.keys());

                  // 清理所有 timers
                  pendingTaskTimersRef.current.forEach((timerId) => clearTimeout(timerId));
                  pendingTaskTimersRef.current.clear();

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
                }

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
                    flowItems: finalFlowItems,
                  };
                }

                sessionManager.updateSession(sessionId, {
                  messages: updated,
                  suggestedActions: actions || [],
                  isLoading: false,
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
            timestamp: new Date().toISOString(),
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
      conversationId: undefined,
      pendingApproval: null
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
        pendingApproval: null,
        // 兼容旧数据：统一为 plan 模式
        mode: 'plan'
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
      const isChapterReplace =
        pending.operation === 'content' || pending.operation === 'replace_all';

      try {
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

          // 章节级整章替换不走段落修订采纳事件，避免触发旧稿保存覆盖
          if (!isChapterReplace) {
            // 派发"确认采纳"事件，让编辑器应用修改（移除标记，保留新内容）
            window.dispatchEvent(
              new CustomEvent('agent-accept-revision', {
                detail: { request_id: pending.request_id, chapter_id: pending.chapter_id }
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
          window.dispatchEvent(
            new CustomEvent('agent-discard-revision', {
              detail: { request_id: pending.request_id, chapter_id: pending.chapter_id }
            })
          );
          console.log('[useAgentChat] ❌ 派发弃用事件');

          // 🆕 章节操作弃用时：派发撤销事件
          const targetWorkId = (pending as any).work_id || workId;
          if (targetWorkId && ['create', 'rename', 'delete'].includes(pending.action_type || '')) {
            window.dispatchEvent(
              new CustomEvent('agent-chapter-revert', {
                detail: {
                  action_type: pending.action_type,
                  request_id: pending.request_id,
                  work_id: targetWorkId,
                  chapter_id: (pending as any).chapter_id
                }
              })
            );
            console.log('[useAgentChat] 🔄 派发章节撤销事件:', pending.action_type);
          }
        }

        const approvalResponse = await agentApi.submitApprovalResponse({
          request_id: pending.request_id,
          approved,
          selected_version: selectedVersion
        });
        const isApplied = approvalResponse.apply_state === 'applied';

        // 章节级替换在审批成功后回读后端章节内容，避免本地草稿与后端状态不一致
        if (approved && isChapterReplace) {
          if (!isApplied) {
            console.warn('[useAgentChat] 章节级审批未落库，跳过本地替换:', approvalResponse);
          } else {
            let replacement = pending.new_content;
            if (pending.chapter_id) {
              try {
                const latestChapter = await DataService.getChapter(pending.chapter_id);
                if (latestChapter?.content) {
                  replacement = latestChapter.content;
                }
              } catch (readErr) {
                console.warn('[useAgentChat] 回读章节最新内容失败，回退到 pending 内容:', readErr);
              }
            }
            if (!replacement) {
              console.warn('[useAgentChat] 章节级替换缺少可用内容，跳过本地替换');
            } else {
              window.dispatchEvent(
                new CustomEvent('agent-replace-text', {
                  detail: {
                    replacement,
                    skipRevision: true,
                    forceReplaceAll: true,
                    chapterId: pending.chapter_id
                  }
                })
              );
              console.log('[useAgentChat] ✅ 章节级替换已在审批成功后同步到编辑器');
            }
          }
        }

        // 🆕 章节操作采纳后派发确认事件，通知 WorkDetailView 刷新列表
        const targetWorkId = (pending as any).work_id || workId;
        if (
          approved &&
          isApplied &&
          targetWorkId &&
          ['create', 'rename', 'delete'].includes(pending.action_type || '')
        ) {
          window.dispatchEvent(
            new CustomEvent('agent-chapter-confirm', {
              detail: { work_id: targetWorkId }
            })
          );
          console.log('[useAgentChat] ✅ 派发章节确认事件，刷新列表');
        }

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
    [sessionId, sessionManager, workId]
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

  // v8.0 → v3.3: 使用 V2 Changes API 检查待审批变更
  const [hasOperations, setHasOperations] = useState(false);

  useEffect(() => {
    const checkOperations = async () => {
      if (!sessionState.conversationId) {
        setHasOperations(false);
        return;
      }
      try {
        const result = await changesApi.list(sessionState.conversationId);
        setHasOperations(result.changes && result.changes.length > 0);
      } catch {
        setHasOperations(false);
      }
    };
    if (!sessionState.isLoading && sessionState.conversationId) {
      checkOperations();
    }
  }, [sessionState.isLoading, sessionState.conversationId]);

  // v3.3: 采纳所有操作 — 使用 V2 Changes API
  const acceptAllOperations = useCallback(async () => {
    if (!sessionState.conversationId) return;
    try {
      await changesApi.acceptAll(sessionState.conversationId);
      setHasOperations(false);

      window.dispatchEvent(new CustomEvent('agent-accept-all-revisions', {
        detail: { conversationId: sessionState.conversationId }
      }));
    } catch (error) {
      console.error('[useAgentChat] 采纳操作失败:', error);
    }
  }, [sessionState.conversationId]);

  // v3.3: 回滚所有操作 — 使用 V2 Changes API
  const rollbackAllOperations = useCallback(async () => {
    if (!sessionState.conversationId) return;
    try {
      await changesApi.rejectAll(sessionState.conversationId);
      setHasOperations(false);

      window.dispatchEvent(new CustomEvent('agent-discard-all-revisions', {
        detail: { conversationId: sessionState.conversationId }
      }));
      window.dispatchEvent(new CustomEvent('agent-operations-rollback', {
        detail: { conversationId: sessionState.conversationId }
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
