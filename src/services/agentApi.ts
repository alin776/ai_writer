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
  Skill,
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
    const streamUrl = `${streamBase}/api/v1/agent/v2/chat/stream`;

    // ✅ 真正的流式输出：直接传递后端返回的内容，不再拆分和模拟
    // 后端现在会以小块（5字符）的粒度发送内容，前端直接展示即可

    const doFetch = async (authToken: string | null): Promise<Response | null> => {
      const resp = await fetch(streamUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': authToken ? `Bearer ${authToken}` : '',
        },
        body: JSON.stringify(finalRequest),
        signal: options?.signal,
      });
      return resp;
    };

    // 断线重连状态（需在 try/catch 外声明）
    let receivedDone = false;
    let receivedError = false;
    let doneMetadata: any = null;
    let doneActions: string[] = [];
    let lastEventId = 0;
    let conversationId = '';
    let handleLine: (line: string) => void = () => {};

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
        let detail = '';
        try {
          const body = await response?.json();
          detail = typeof body?.detail === 'string' ? body.detail : '';
        } catch { /* body 不可读则忽略 */ }
        throw new Error(detail || `HTTP error! status: ${response?.status ?? 'unknown'}`);
      }

      // 从响应头提取 conversation_id（断线重连的关键：流断开前可能还没收到 done 事件）
      const headerConvId = response.headers.get('X-Conversation-Id');
      if (headerConvId) {
        conversationId = headerConvId;
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      callbacks.onReader?.(reader, options?.controller);

      let buffer = '';

      handleLine = (line: string) => {
        // 追踪 SSE id 字段
        if (line.startsWith('id: ')) {
          const parsed = parseInt(line.substring(4).trim(), 10);
          if (!isNaN(parsed)) {
            lastEventId = parsed;
          }
          return;
        }
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
              conversationId = data.conversation_id || conversationId;
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
                conversationId = data.conversation_id;
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
              // 从首个 SSE 事件中提取 conversation_id（断线重连的关键来源）
              if (data.conversation_id) {
                conversationId = data.conversation_id;
              }
              callbacks.onFlowEvent?.({ type: 'agent_header', data: data.data, timestamp: data.timestamp });
              break;
            case 'text':
              callbacks.onFlowEvent?.({ type: 'text', data: data.data, timestamp: data.timestamp });
              break;
            case 'step_start':
              callbacks.onFlowEvent?.({ type: 'step_start', stepId: data.step_id, title: data.title, description: data.description, toolName: data.tool_name, toolInput: data.tool_input, status: data.status, timestamp: data.timestamp, parentStepId: data.parent_step_id, isTask: data.is_task, isMemory: data.is_memory });
              break;
            case 'skill_loaded':
              callbacks.onFlowEvent?.({ type: 'skill_loaded', skillName: data.skill_name, timestamp: data.timestamp });
              break;
            case 'skill_switched':
              callbacks.onFlowEvent?.({ type: 'skill_switched', skillName: data.skill_name, timestamp: data.timestamp });
              break;
            case 'step_complete':
              callbacks.onFlowEvent?.({ type: 'step_complete', stepId: data.step_id, description: data.description, toolName: data.tool_name, toolCall: data.tool_call, status: data.status, error: data.error, timestamp: data.timestamp, parentStepId: data.parent_step_id, isTask: data.is_task, isMemory: data.is_memory, childToolCount: data.child_tool_count });
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

      // 断线重连：非主动中断 + 有 conversationId + 收到过事件 → 尝试恢复
      if (!isAbort && conversationId && lastEventId > 0 && !receivedDone) {
        console.log(`[AgentApi] 尝试断线重连: conversationId=${conversationId}, lastEventId=${lastEventId}`);
        try {
          await this._resumeStream(conversationId, lastEventId, handleLine, streamBase, options);
          // 重连成功，检查是否收到了 done
          if (!receivedDone && !receivedError && !options?.signal?.aborted) {
            callbacks.onDone?.(doneMetadata || {}, doneActions || []);
          }
          return; // 重连成功，正常返回
        } catch (resumeError: any) {
          console.error('[AgentApi] 重连失败:', resumeError);
        }
      }

      // 如果是主动停止/中断，直接静默结束
      if (!isAbort) {
        callbacks.onError?.(error.message || 'Stream connection failed');
      }
      throw error;
    }
  }

  /**
   * SSE 断线重连：调用恢复端点，从断点续传事件
   */
  private async _resumeStream(
    conversationId: string,
    lastEventId: number,
    handleLine: (line: string) => void,
    streamBase: string,
    options?: { signal?: AbortSignal; controller?: AbortController }
  ): Promise<void> {
    const maxRetries = 3;

    const shouldAttemptResume = (
      attempt: number,
      maxRetries: number,
      lastError: Error | null
    ): { shouldRetry: boolean; delayMs: number } => {
      // 超过最大重试次数，放弃
      if (attempt >= maxRetries) return { shouldRetry: false, delayMs: 0 };

      // 4xx 业务错误不重试（认证失败、资源不存在等）
      // 匹配 "HTTP error! status: NNN" / "Resume HTTP error: NNN" 等格式
      if (lastError?.message) {
        const statusMatch = lastError.message.match(/HTTP error[!:\s]+(?:status[:\s]+)?(\d{3})/i);
        if (statusMatch) {
          const code = parseInt(statusMatch[1], 10);
          if (code >= 400 && code < 500) return { shouldRetry: false, delayMs: 0 };
        }
      }

      // 首次重连立即尝试，不等待
      if (attempt === 0) return { shouldRetry: true, delayMs: 0 };

      // 后续重试：指数退避 1s → 2s → 4s，加 ±30% 随机抖动防惊群
      const baseDelay = 1000 * Math.pow(2, attempt - 1);
      const jitter = baseDelay * 0.3 * (Math.random() * 2 - 1);
      const delayMs = Math.round(baseDelay + jitter);

      return { shouldRetry: true, delayMs };
    };

    const token = await this.ensureValidToken();

    let lastError: Error | null = null;
    for (let attempt = 0; attempt < maxRetries; attempt++) {
      const decision = shouldAttemptResume(attempt, maxRetries, lastError);
      if (!decision.shouldRetry) break;

      if (decision.delayMs > 0) {
        await new Promise(resolve => setTimeout(resolve, decision.delayMs));
      }

      // 每次重试使用最新的 lastEventId（handleLine 可能已更新）
      const resumeUrl = `${streamBase}/api/v1/agent/v2/chat/stream/resume/${conversationId}?last_event_id=${lastEventId}`;

      try {
        const resp = await fetch(resumeUrl, {
          method: 'GET',
          headers: {
            'Authorization': token ? `Bearer ${token}` : '',
          },
          signal: options?.signal,
        });

        if (!resp.ok) throw new Error(`Resume HTTP error: ${resp.status}`);

        const reader = resp.body?.getReader();
        if (!reader) throw new Error('Resume response body not readable');

        const decoder = new TextDecoder();
        let resumeBuffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          resumeBuffer += decoder.decode(value, { stream: true });
          const lines = resumeBuffer.split('\n');
          resumeBuffer = lines.pop() || '';

          for (const line of lines) {
            handleLine(line);
          }
        }

        resumeBuffer += decoder.decode();
        if (resumeBuffer.trim()) {
          for (const line of resumeBuffer.split('\n')) {
            handleLine(line);
          }
        }

        console.log('[AgentApi] 断线重连成功');
        return; // 成功
      } catch (retryError: any) {
        lastError = retryError;
        const nextDecision = shouldAttemptResume(attempt + 1, maxRetries, retryError);
        if (!nextDecision.shouldRetry) throw retryError;
        console.warn(`[AgentApi] 重连第 ${attempt + 1} 次失败，${nextDecision.delayMs}ms 后重试`);
      }
    }

    throw new Error('断线重连: 所有重试均失败');
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
  /**
   * 获取可用 Agent Skills 列表
   */
  async getSkills(): Promise<Skill[]> {
    const response = await this.client.get('/skills');
    return response.data;
  }

  /**
   * 切换 Skill 启用/禁用状态
   */
  async toggleSkill(skillName: string): Promise<{ skill_name: string; enabled: boolean }> {
    const response = await this.client.post(`/skills/${encodeURIComponent(skillName)}/toggle`);
    return response.data;
  }

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
