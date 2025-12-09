/**
 * Agent API 服务封装
 *
 * 提供所有Agent相关的API调用方法
 */

import axios, { AxiosInstance } from 'axios';
import type {
  AgentChatRequest,
  AgentChatResponse,
  PlanCreationRequest,
  PlanResponse,
  ApprovalResponse,
  ApprovalActionRequest,
  HistorySessionItem
} from '../types/agent';

class AgentApiService {
  private client: AxiosInstance;

  constructor() {
    // 使用本地后端API基础URL，而不是OpenAI代理URL
    const rawBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    // 无条件使用相对路径，让 Vite 代理接管，避免跨域/重定向
    const baseURL = import.meta.env.DEV ? '/api/v1' : rawBase;

    this.client = axios.create({
      baseURL: `${baseURL}/agent`,
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 180000 // 180秒超时（3分钟），适配长文本生成
    });

    // 请求拦截器 - 添加Token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // 响应拦截器 - 统一错误处理
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token过期，跳转登录
          this.handleUnauthorized();
        }
        return Promise.reject(error);
      }
    );
  }

  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      // 从 Zustand persist 存储中读取 token（与 ApiAdapter、AIService 保持一致）
      const authStorage = localStorage.getItem('auth-storage');
      if (authStorage) {
        try {
          const authState = JSON.parse(authStorage);
          return authState.state?.token || null;
        } catch (error) {
          console.error('[AgentApi] Failed to parse auth storage:', error);
          return null;
        }
      }
    }
    return null;
  }

  private handleUnauthorized(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth-storage');
      window.location.href = '/login';
    }
  }

  private normalizeHistorySession(session: any): HistorySessionItem | null {
    if (!session) return null;

    const conversationId =
      session.conversation_id ??
      session.conversationId ??
      session.conversationid ??
      session.conversationID;

    const sessionId =
      session.session_id ??
      session.sessionId ??
      session.id ??
      conversationId ??
      '';

    const messageCount =
      typeof session.message_count === 'number'
        ? session.message_count
        : typeof session.messageCount === 'number'
          ? session.messageCount
          : Array.isArray(session.messages)
            ? session.messages.length
            : 0;

    const updatedAt =
      session.updated_at ||
      session.updatedAt ||
      session.last_message_at ||
      session.lastMessageAt ||
      session.created_at ||
      session.createdAt ||
      new Date().toISOString();

    const lastMessagePreview =
      session.last_message_preview ??
      session.lastMessagePreview ??
      (Array.isArray(session.messages) && session.messages.length > 0
        ? session.messages[session.messages.length - 1]?.content?.slice(0, 80)
        : '');

    return {
      sessionId: sessionId || 'unknown-session',
      title: session.title || '历史会话',
      messageCount,
      updatedAt,
      archivedAt: session.archived_at ?? session.archivedAt ?? null,
      lastMessagePreview,
      conversationId: conversationId || undefined,
      workId: session.work_id ?? session.workId,
      chapterId: session.chapter_id ?? session.chapterId,
      titleLocked: session.title_locked ?? session.titleLocked ?? false,
    };
  }

  /**
   * Agent对话
   */
  async chat(request: AgentChatRequest): Promise<AgentChatResponse> {
    const response = await this.client.post<AgentChatResponse>('/chat', request);
    return response.data;
  }

  /**
   * Agent对话 - 流式响应（SSE）with Planning + Execution
   *
   * @param request 对话请求
   * @param callbacks 回调函数集合
   */

  async chatStream(
    request: AgentChatRequest,
    callbacks: {
      // ????
      onStart?: (conversationId: string) => void;
      onContent?: (chunk: string) => void;
      onStep?: (step: any) => void;
      onDone?: (metadata: any, suggestedActions: string[]) => void;
      onError?: (error: string) => void;
      // Planning ????
      onPlan?: (plan: any) => void;
      onTaskStart?: (task: any) => void;
      onTaskProgress?: (progress: any) => void;
      onTaskDone?: (taskDone: any) => void;
      // React ????
      onProgress?: (progress: any) => void;
      onToolCall?: (toolCall: any) => void;
      onActivityComplete?: (activity: any) => void;
      onApprovalRequest?: (approvalReq: any) => void;
      onReader?: (reader: ReadableStreamDefaultReader<Uint8Array>, controller?: AbortController) => void;
    },
    options?: {
      signal?: AbortSignal;
      controller?: AbortController;
    }
  ): Promise<void> {
    const token = this.getToken();
    const rawBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    const defaultBase = rawBase.replace(/\/api\/v1\/?$/, '');
    const streamBaseRaw =
      import.meta.env.VITE_AGENT_STREAM_BASE_URL ||
      (import.meta.env.DEV ? '' : defaultBase);
    const streamBase = streamBaseRaw
      .replace(/\/api\/v1\/?$/, '')
      .replace(/\/$/, '');
    const url = `${streamBase}/api/v1/agent/chat/stream`;

    // 🔍 调试日志：追踪实际发送到后端的 payload
    console.log('===== agentApi.chatStream 发送请求 =====');
    console.log('1. URL:', url);
    console.log('2. request 完整内容:', request);
    console.log('3. request.context:', request.context);
    console.log('4. request.context?.selected_text:', request.context?.selected_text);
    console.log('5. request.context?.selection_position:', request.context?.selection_position);
    console.log('6. request.context?.instruction_context:', request.context?.instruction_context);
    console.log('==========================================');

    // 将后端返回的内容细粒度拆分为逐字符小块，保证前端能触发逐字流式动画
    const contentQueue: string[] = [];
    let contentTimer: ReturnType<typeof setTimeout> | null = null;
    const flushContentQueue = () => {
      if (!contentQueue.length) {
        contentTimer = null;
        return;
      }
      const piece = contentQueue.shift();
      if (piece !== undefined) {
        callbacks.onContent?.(piece);
      }
      contentTimer = setTimeout(flushContentQueue, 0);
    };
    const enqueueContent = (text: string | undefined | null) => {
      if (!text) return;
      for (const ch of text) {
        contentQueue.push(ch);
      }
      if (!contentTimer) {
        contentTimer = setTimeout(flushContentQueue, 0);
      }
    };
    const flushRemainingContentSync = () => {
      if (contentTimer) {
        clearTimeout(contentTimer);
        contentTimer = null;
      }
      while (contentQueue.length) {
        const piece = contentQueue.shift();
        if (piece !== undefined) {
          callbacks.onContent?.(piece);
        }
      }
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        },
        body: JSON.stringify(request),
        signal: options?.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      callbacks.onReader?.(reader, options?.controller);

      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.substring(6));

              switch (data.type) {
                // ????
                case 'start':
                  callbacks.onStart?.(data.conversation_id);
                  break;
                case 'content':
                  const content = typeof data.data === 'string'
                    ? data.data
                    : data.data?.content || data.data;
                  enqueueContent(content);
                  break;
                case 'step':
                  callbacks.onStep?.(data.data);
                  break;
                case 'done':
                  flushRemainingContentSync();
                  callbacks.onDone?.(data.metadata, data.suggested_actions);
                  break;
                case 'error':
                  flushRemainingContentSync();
                  callbacks.onError?.(data.error);
                  break;

                // Planning ????
                case 'plan':
                  callbacks.onPlan?.(data.data);
                  break;
                case 'task_start':
                  callbacks.onTaskStart?.(data.data);
                  break;
                case 'task_progress':
                  callbacks.onTaskProgress?.(data.data);
                  break;
                case 'task_done':
                  callbacks.onTaskDone?.(data.data);
                  break;

                // React ????
                case 'progress':
                  callbacks.onProgress?.(data.data);
                  break;
                case 'tool_call':
                  callbacks.onToolCall?.(data.data);
                  break;
                case 'activity_complete':
                  callbacks.onActivityComplete?.(data.data);
                  break;
                case 'approval_request':
                  callbacks.onApprovalRequest?.(data.data);
                  break;
              }
            } catch (error) {
              console.error('[AgentApi] Failed to parse SSE data:', error);
            }
          }
        }
      }
    } catch (error: any) {
      console.error('[AgentApi] Stream error:', error);
      flushRemainingContentSync();
      callbacks.onError?.(error.message || 'Stream connection failed');
      throw error;
    } finally {
      // 防止定时器泄漏
      if (contentTimer) {
        clearTimeout(contentTimer);
      }
    }
  }
  async createSession(payload: { title?: string; work_id?: string; chapter_id?: string }): Promise<{ session_id: string; title?: string; conversation_id?: string; created_at?: string }> {
    const response = await this.client.post('/sessions', payload);
    return response.data;
  }

  /**
   * 获取会话列表（真实后端）
   */
  async getSessions(params: { work_id?: string; chapter_id?: string; limit?: number } = {}): Promise<{ sessions: any[] }> {
    const response = await this.client.get('/sessions', { params });
    return response.data;
  }

  /**
   * 更新会话标题
   */
  async updateSessionTitle(sessionId: string, title: string, titleLocked: boolean = true): Promise<any> {
    const response = await this.client.patch(`/sessions/${sessionId}`, { title, title_locked: titleLocked });
    return response.data;
  }

  /**
   * 删除会话
   */
  async deleteSession(sessionId: string): Promise<void> {
    await this.client.delete(`/sessions/${sessionId}`);
  }

  /**
   * 获取会话消息列表
   */
  async getSessionMessages(
    sessionId: string,
    params: { limit?: number; offset?: number; order?: 'asc' | 'desc' } = {}
  ): Promise<any[]> {
    const response = await this.client.get(`/sessions/${sessionId}/messages`, { params });
    return response.data;
  }

  /**
   * 获取单个会话详情（含消息，如果后端支持）
   */
  async getSessionDetail(sessionId: string): Promise<any> {
    const response = await this.client.get(`/sessions/${sessionId}`);
    return response.data;
  }

  /**
   * 获取历史会话列表（先调后端，失败再本地兜底）
   */
  async getHistorySessions(params: { workId?: string; chapterId?: string; limit?: number } = {}) {
    // 优先尝试真实后端
    try {
      const resp = await this.getSessions({
        work_id: params.workId,
        chapter_id: params.chapterId,
        limit: params.limit,
      });
      const sessions = Array.isArray(resp?.sessions)
        ? resp.sessions
          .map((s) => this.normalizeHistorySession(s))
          .filter((s): s is HistorySessionItem => Boolean(s))
        : [];
      return { sessions };
    } catch (err) {
      console.warn('[AgentApi] getSessions failed, fallback to local cache:', err);
    }

    // 本地兜底：读取 useConversationPersistence 写入的 localStorage
    if (typeof window === 'undefined') {
      return { sessions: [] };
    }

    const {
      workId,
      chapterId,
      limit = 50,
    } = params;

    const STORAGE_KEY_PREFIX = 'agent_conversation_';
    const SESSIONS_LIST_KEY = 'agent_conversation_sessions';

    const loadSessionIds = (): string[] => {
      try {
        const stored = localStorage.getItem(SESSIONS_LIST_KEY);
        return stored ? JSON.parse(stored) : [];
      } catch {
        return [];
      }
    };

    const loadSession = (sessionId: string) => {
      try {
        const stored = localStorage.getItem(`${STORAGE_KEY_PREFIX}${sessionId}`);
        return stored ? JSON.parse(stored) : null;
      } catch {
        return null;
      }
    };

    const sessionIds = loadSessionIds();
    const sessions = sessionIds
      .map((id) => loadSession(id))
      .filter(Boolean)
      .map((s) => this.normalizeHistorySession(s))
      .filter((s): s is HistorySessionItem => Boolean(s))
      .filter((s) => {
        if (workId && s.workId && s.workId !== workId) return false;
        if (chapterId && s.chapterId && s.chapterId !== chapterId) return false;
        return true;
      })
      .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
      .slice(0, limit);

    return { sessions };
  }


  /**
   * 创建执行计划
   */
  async createPlan(request: PlanCreationRequest): Promise<PlanResponse> {
    const response = await this.client.post<PlanResponse>('/plans', request);
    return response.data;
  }

  /**
   * 查询计划状态
   */
  async getPlan(planId: string): Promise<PlanResponse> {
    const response = await this.client.get<PlanResponse>(`/plans/${planId}`);
    return response.data;
  }

  /**
   * 获取待批准请求列表
   */
  async getPendingApprovals(): Promise<ApprovalResponse[]> {
    const response = await this.client.get<ApprovalResponse[]>('/approvals/pending');
    return response.data;
  }

  /**
   * 批准请求
   */
  async approveRequest(
    requestId: string,
    action: ApprovalActionRequest
  ): Promise<any> {
    const response = await this.client.post(
      `/approvals/${requestId}/approve`,
      action
    );
    return response.data;
  }

  /**
   * 拒绝请求
   */
  async rejectRequest(
    requestId: string,
    action: ApprovalActionRequest
  ): Promise<any> {
    const response = await this.client.post(
      `/approvals/${requestId}/reject`,
      action
    );
    return response.data;
  }

  /**
   * 获取用户记忆上下文
   */
  async getMemoryContext(): Promise<any> {
    const response = await this.client.get('/memory/context');
    return response.data;
  }

  /**
   * 更新用户偏好
   */
  async updatePreferences(preferences: any): Promise<any> {
    const response = await this.client.put('/memory/context', preferences);
    return response.data;
  }

  /**
   * 提交编辑器确认响应
   *
   * @param request 确认响应请求
   */
  async submitApprovalResponse(request: {
    request_id: string;
    approved: boolean;
    selected_version?: number;
    reason?: string;
  }): Promise<{ success: boolean; request_id: string }> {
    const response = await this.client.post('/chat/approval-response', request);
    return response.data;
  }
}

// 导出单例
export const agentApi = new AgentApiService();

// 也导出类型，方便其他地方使用
export type { AgentApiService };
