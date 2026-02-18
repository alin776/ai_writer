/**
 * Agent API 服务封装
 *
 * 提供所有Agent相关的API调用方法
 */

import axios, { AxiosInstance } from 'axios';
import { useAuthStore } from '@/store/authStore';
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
  public readonly client: AxiosInstance;

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

  /**
   * 获取有效的 token，如果快过期则先刷新
   * 复用 ApiAdapter 的刷新逻辑，保持一致性
   */
  private async ensureValidToken(): Promise<string | null> {
    const { tokenExpiresAt, refreshToken } = useAuthStore.getState();

    // token 还有 30 秒以上有效期，直接用
    if (tokenExpiresAt && Date.now() < tokenExpiresAt - 30_000) {
      return this.getToken();
    }

    // token 快过期或已过期，尝试刷新
    if (refreshToken) {
      try {
        const newToken = await this.refreshAccessToken();
        if (newToken) return newToken;
      } catch (e) {
        console.error('[AgentApi] Token refresh failed:', e);
      }
    }

    // 刷新失败，返回当前 token（可能已过期，但让后端决定）
    return this.getToken();
  }

  /**
   * 使用 refresh token 获取新的 access token
   */
  private refreshPromise: Promise<string | null> | null = null;

  private async refreshAccessToken(): Promise<string | null> {
    // 防抖：多个并发请求只刷新一次
    if (this.refreshPromise) return this.refreshPromise;

    this.refreshPromise = (async () => {
      const { refreshToken, login, user, logout } = useAuthStore.getState();
      if (!refreshToken) return null;

      try {
        const baseURL = import.meta.env.DEV ? '/api/v1' : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1');
        const resp = await fetch(`${baseURL}/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });

        if (!resp.ok) {
          // 401/403 表示 refresh token 无效，需要重新登录
          if (resp.status === 401 || resp.status === 403) {
            logout();
            localStorage.removeItem('auth-storage');
          }
          throw new Error(`Refresh failed: ${resp.status}`);
        }

        const data = await resp.json();
        const newAccessToken = data.access_token || data.accessToken;
        const newRefreshToken = data.refresh_token || data.refreshToken || refreshToken;
        const expiresAt = data.expires_at || data.expiresAt;
        const refreshExpiresAt = data.refresh_expires_at || data.refreshExpiresAt;

        if (!newAccessToken) return null;

        const tokenExpiresAt = expiresAt ? expiresAt * 1000 : null;
        const refreshTokenExpiresAt = refreshExpiresAt ? refreshExpiresAt * 1000 : null;

        if (user) {
          login(user, newAccessToken, newRefreshToken, tokenExpiresAt, refreshTokenExpiresAt);
        }

        return newAccessToken;
      } catch (error) {
        console.error('[AgentApi] refreshAccessToken error:', error);
        // logout 已在上面 401/403 分支处理，此处仅返回 null
        return null;
      } finally {
        this.refreshPromise = null;
      }
    })();

    return this.refreshPromise;
  }

  private handleUnauthorized(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth-storage');
      window.location.href = '/login';
    }
  }

  private withToolPolicy(request: AgentChatRequest): AgentChatRequest {
    if (request.tool_policy !== undefined) {
      return request;
    }

    const contextPolicy = request.context?.tool_policy;
    if (contextPolicy !== undefined) {
      return { ...request, tool_policy: contextPolicy };
    }

    return { ...request, tool_policy: 'auto' };
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
    const finalRequest = this.withToolPolicy(request);
    const response = await this.client.post<AgentChatResponse>('/chat', finalRequest);
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
      // 审批/执行轨迹回调
      onApprovalRequest?: (approvalReq: any) => void;
      onFlowEvent?: (event: any) => void;  // 执行轨迹事件 (v6.0)
      onReader?: (reader: ReadableStreamDefaultReader<Uint8Array>, controller?: AbortController) => void;
    },
    options?: {
      signal?: AbortSignal;
      controller?: AbortController;
    }
  ): Promise<void> {
    const finalRequest = this.withToolPolicy(request);
    // ✅ 修复：发请求前检查 token 有效性，必要时自动刷新
    const token = await this.ensureValidToken();
    const rawBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    const defaultBase = rawBase.replace(/\/api\/v1\/?$/, '');
    const streamBaseRaw =
      import.meta.env.VITE_AGENT_STREAM_BASE_URL ||
      (import.meta.env.DEV ? '' : defaultBase);
    const streamBase = streamBaseRaw
      .replace(/\/api\/v1\/?$/, '')
      .replace(/\/$/, '');
    const streamUrls = [
      `${streamBase}/api/v1/agent/v2/chat/stream`,
      `${streamBase}/api/v1/agent/chat/stream`,
    ];

    // ✅ 真正的流式输出：直接传递后端返回的内容，不再拆分和模拟
    // 后端现在会以小块（5字符）的粒度发送内容，前端直接展示即可

    const doFetch = async (authToken: string | null): Promise<Response | null> => {
      let response: Response | null = null;
      for (let idx = 0; idx < streamUrls.length; idx += 1) {
        const candidate = streamUrls[idx];
        const resp = await fetch(candidate, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': authToken ? `Bearer ${authToken}` : '',
          },
          body: JSON.stringify(finalRequest),
          signal: options?.signal,
        });

        // 新后端走 /v2，若目标服务仍是旧版本，则 404 后自动回退。
        if (resp.status === 404 && idx < streamUrls.length - 1) {
          continue;
        }

        response = resp;
        break;
      }
      return response;
    };

    try {
      let response = await doFetch(token);

      // ✅ 修复：401 时自动刷新 token 并重试一次
      if (response?.status === 401) {
        const refreshedToken = await this.refreshAccessToken();
        if (refreshedToken) {
          response = await doFetch(refreshedToken);
        }
      }

      if (!response || !response.ok) {
        throw new Error(`HTTP error! status: ${response?.status ?? 'unknown'}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      callbacks.onReader?.(reader, options?.controller);

      let buffer = '';
      let receivedDone = false;
      let receivedError = false;
      let doneMetadata: any = null;
      let doneActions: string[] = [];

      const handleLine = (line: string) => {
        if (!line.startsWith('data: ')) {
          return;
        }
        const jsonStr = line.substring(6);
        if (!jsonStr.trim()) return;
        try {
          const data = JSON.parse(jsonStr);

          switch (data.type) {
            // ????
            case 'start':
              callbacks.onStart?.(data.conversation_id);
              break;
            case 'content': {
              const raw = typeof data.data === 'string'
                ? data.data
                : data.data?.content;
              const content = typeof raw === 'string' ? raw : '';
              callbacks.onContent?.(content);
              break;
            }
            case 'step':
              callbacks.onStep?.(data.data);
              break;
            case 'done':
              receivedDone = true;
              if (data.conversation_id) {
                callbacks.onStart?.(data.conversation_id);
              }
              doneMetadata = data.metadata;
              doneActions = Array.isArray(data.suggested_actions) ? data.suggested_actions : [];
              callbacks.onDone?.(doneMetadata, doneActions);
              break;
            case 'error':
              receivedError = true;
              callbacks.onError?.(data.error);
              break;

            case 'approval_request':
              callbacks.onApprovalRequest?.(data.data);
              break;

            // 执行轨迹事件 (v6.0)
            case 'agent_header':
              callbacks.onFlowEvent?.({ type: 'agent_header', data: data.data, timestamp: data.timestamp });
              break;
            case 'text':
              callbacks.onFlowEvent?.({ type: 'text', data: data.data, timestamp: data.timestamp });
              break;
            case 'step_start':
              callbacks.onFlowEvent?.({ type: 'step_start', stepId: data.step_id, title: data.title, description: data.description, toolName: data.tool_name, toolInput: data.tool_input, status: data.status, timestamp: data.timestamp });
              break;
            case 'knowledge_loaded':
              // V1 遗留，忽略
              break;
            case 'step_complete':
              callbacks.onFlowEvent?.({ type: 'step_complete', stepId: data.step_id, description: data.description, toolName: data.tool_name, toolCall: data.tool_call, status: data.status, timestamp: data.timestamp });
              break;
            case 'output_ready':
              callbacks.onFlowEvent?.({ type: 'output_ready', title: data.title, content: data.content, intro: data.intro, introHighlight: data.intro_highlight, isApplicable: data.is_applicable, timestamp: data.timestamp });
              break;
            case 'completion':
              callbacks.onFlowEvent?.({ type: 'completion', data: data.data, timestamp: data.timestamp });
              break;
            case 'revision': {
              // 兼容后端两种结构：直接 revision 事件 / 包裹在 data 中的 flow_event
              const payload = data.data as any;
              const revisionEvent =
                payload && payload.type === 'revision' && payload.data ? payload : null;
              const revisionData = revisionEvent ? revisionEvent.data : (payload?.data ?? payload);
              const timestamp = revisionEvent?.timestamp ?? payload?.timestamp ?? data.timestamp;
              callbacks.onFlowEvent?.({ type: 'revision', data: revisionData, stepId: data.step_id, timestamp });
              break;
            }
            case 'summarization_start':
              // V1 遗留，忽略
              break;
            case 'summarization_complete':
              // V1 遗留，忽略
              break;

            // Explore 探索事件 — V1 遗留，忽略
            case 'explore_round':
              break;
            case 'explore_summary':
              break;
          }
        } catch (error) {
          console.error('[AgentApi] Failed to parse SSE data:', error);
        }
      };

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          handleLine(line);
        }
      }

      buffer += decoder.decode();
      if (buffer.trim()) {
        const lines = buffer.split('\n');
        for (const line of lines) {
          handleLine(line);
        }
      }
      if (!receivedDone && !receivedError && !options?.signal?.aborted) {
        callbacks.onDone?.(doneMetadata || {}, doneActions || []);
      }
    } catch (error: any) {
      const isAbort =
        error?.name === 'AbortError' ||
        error?.message?.toLowerCase?.().includes('abort') ||
        options?.signal?.aborted;

      console.error('[AgentApi] Stream error:', error);

      // 如果是主动停止/中断，直接静默结束
      if (!isAbort) {
        callbacks.onError?.(error.message || 'Stream connection failed');
      }
      throw error;
    }
  }
  async createSession(payload: { title?: string; work_id?: string; chapter_id?: string; conversation_id?: string }): Promise<{ session_id: string; title?: string; conversation_id?: string; created_at?: string }> {
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
        if (workId && s.workId !== workId) return false;
        if (chapterId && s.chapterId !== chapterId) return false;
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
      `/approvals/${requestId}/action`,
      { ...action, action: 'approve' }
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
      `/approvals/${requestId}/action`,
      { ...action, action: 'reject' }
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
  }): Promise<{
    success: boolean;
    request_id: string;
    action: 'accepted' | 'rejected';
    apply_state: 'pending' | 'applied' | 'rejected' | 'failed';
  }> {
    const response = await this.client.post('/chat/approval-response', request);
    return response.data;
  }

}

// 导出单例
export const agentApi = new AgentApiService();

// 也导出类型，方便其他地方使用
export type { AgentApiService };
