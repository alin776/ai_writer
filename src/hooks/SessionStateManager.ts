/**
 * SessionStateManager - 多会话状态管理器
 *
 * 核心功能:
 * - 每个会话维护独立的状态（messages, activities, tasks等）
 * - 每个会话维护独立的SSE连接（fetch reader）
 * - 切换会话时不中断后台会话的响应
 * - 限制同时激活的SSE连接数量，防止内存泄漏
 * - 后台会话自动保存到localStorage
 */

import type { Message, ActivityItem, ProgressData } from '@/types/agent';

// 任务接口
interface Task {
  task_id: number;
  description: string;
  tool?: string;
  estimated_time?: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  elapsed_time?: number;
  progress_status?: string;  // Multi-Agent 内部进度状态
}

// 会话状态接口
export interface SessionState {
  sessionId: string;
  conversationId?: string;
  messages: Message[];
  activities: ActivityItem[];
  tasks: Task[];
  progressData: ProgressData | null;
  isLoading: boolean;
  error: string | null;
  suggestedActions: string[];
  currentTaskId: number | null;
  pendingApproval: any | null;

  // SSE连接管理
  reader: ReadableStreamDefaultReader<Uint8Array> | null;
  abortController: AbortController | null;

  // 元数据
  createdAt: number;
  lastActiveAt: number;
  mode?: 'plan' | 'agent';
}

// 状态变更监听器
type StateChangeListener = (sessionId: string, state: SessionState) => void;

const MAX_ACTIVE_CONNECTIONS = 3;  // 最多同时保持3个SSE连接
const MAX_SESSIONS_IN_MEMORY = 10;  // 最多在内存中保存10个会话
const AUTO_DISCONNECT_DELAY = 60000;  // 60秒后自动断开非活跃会话的连接

export class SessionStateManager {
  private sessions: Map<string, SessionState> = new Map();
  private listeners: Set<StateChangeListener> = new Set();
  private autoDisconnectTimers: Map<string, NodeJS.Timeout> = new Map();
  private currentActiveSessionId: string | null = null;  // 当前显示的会话ID

  /**
   * 创建新会话状态
   */
  createSession(sessionId: string, initialData?: Partial<SessionState>): SessionState {
    const now = Date.now();

    const state: SessionState = {
      sessionId,
      conversationId: initialData?.conversationId,
      messages: initialData?.messages || [],
      activities: initialData?.activities || [],
      tasks: initialData?.tasks || [],
      progressData: initialData?.progressData || null,
      isLoading: false,
      error: null,
      suggestedActions: [],
      currentTaskId: null,
      pendingApproval: null,
      reader: null,
      abortController: null,
      createdAt: now,
      lastActiveAt: now,
      mode: initialData?.mode || 'plan'
    };

    this.sessions.set(sessionId, state);
    console.log(`[SessionManager] 创建会话: ${sessionId}`, state);

    // 检查并强制内存限制
    this.enforceMemoryLimit();

    return state;
  }

  /**
   * 设置当前活跃会话（用于判断是否触发UI更新）
   */
  setActiveSession(sessionId: string): void {
    this.currentActiveSessionId = sessionId;

    // 更新该会话的最后活跃时间
    const session = this.sessions.get(sessionId);
    if (session) {
      session.lastActiveAt = Date.now();
    }

    console.log(`[SessionManager] 设置活跃会话: ${sessionId}`);
  }

  /**
   * 获取当前活跃会话ID
   */
  getActiveSessionId(): string | null {
    return this.currentActiveSessionId;
  }

  /**
   * 检查是否是当前活跃会话
   */
  isActiveSession(sessionId: string): boolean {
    return this.currentActiveSessionId === sessionId;
  }

  /**
   * 获取会话状态
   */
  getSession(sessionId: string): SessionState | undefined {
    return this.sessions.get(sessionId);
  }

  /**
   * 获取或创建会话
   */
  getOrCreateSession(sessionId: string, initialData?: Partial<SessionState>): SessionState {
    let session = this.sessions.get(sessionId);
    if (!session) {
      session = this.createSession(sessionId, initialData);
    }
    return session;
  }

  /**
   * 更新会话状态（部分更新）
   */
  updateSession(sessionId: string, updates: Partial<SessionState>): void {
    const session = this.sessions.get(sessionId);
    if (!session) {
      console.warn(`[SessionManager] 会话不存在: ${sessionId}`);
      return;
    }

    Object.assign(session, updates);
    session.lastActiveAt = Date.now();

    // 通知监听器
    this.notifyListeners(sessionId, session);
  }

  /**
   * 开始SSE连接
   */
  startStreaming(
    sessionId: string,
    reader: ReadableStreamDefaultReader<Uint8Array>,
    abortController: AbortController
  ): void {
    const session = this.sessions.get(sessionId);
    if (!session) {
      console.warn(`[SessionManager] 会话不存在: ${sessionId}`);
      return;
    }

    // 清除之前的连接（如果有）
    this.disconnectSession(sessionId);

    session.reader = reader;
    session.abortController = abortController;
    session.isLoading = true;
    session.lastActiveAt = Date.now();

    console.log(`[SessionManager] 开始SSE连接: ${sessionId}`);

    // 检查并限制连接数量
    this.enforceConnectionLimit();
  }

  /**
   * 停止SSE连接
   */
  disconnectSession(sessionId: string): void {
    const session = this.sessions.get(sessionId);
    if (!session) return;

    // 关闭reader
    if (session.reader) {
      try {
        session.reader.cancel();
      } catch (error) {
        console.warn(`[SessionManager] 关闭reader失败:`, error);
      }
      session.reader = null;
    }

    // 中断请求
    if (session.abortController) {
      try {
        session.abortController.abort();
      } catch (error) {
        console.warn(`[SessionManager] 中断请求失败:`, error);
      }
      session.abortController = null;
    }

    session.isLoading = false;

    console.log(`[SessionManager] 断开SSE连接: ${sessionId}`);

    // 清除自动断开定时器
    this.clearAutoDisconnectTimer(sessionId);
  }

  /**
   * 强制限制活跃连接数量
   * 当超过MAX_ACTIVE_CONNECTIONS时，断开最久未使用的连接
   */
  private enforceConnectionLimit(): void {
    const activeSessions = Array.from(this.sessions.entries())
      .filter(([_, state]) => state.reader !== null)
      .sort((a, b) => a[1].lastActiveAt - b[1].lastActiveAt);

    if (activeSessions.length > MAX_ACTIVE_CONNECTIONS) {
      const excess = activeSessions.length - MAX_ACTIVE_CONNECTIONS;
      console.warn(`[SessionManager] 超过连接数限制，关闭${excess}个最旧的连接`);

      for (let i = 0; i < excess; i++) {
        const [sessionId, _] = activeSessions[i];
        this.disconnectSession(sessionId);
      }
    }
  }

  /**
   * 强制限制内存中的会话数量
   * 当超过MAX_SESSIONS_IN_MEMORY时，删除最久未使用的会话（但不删除当前活跃会话）
   */
  private enforceMemoryLimit(): void {
    if (this.sessions.size <= MAX_SESSIONS_IN_MEMORY) {
      return;
    }

    // 按最后活跃时间排序（最旧的在前）
    const sortedSessions = Array.from(this.sessions.entries())
      .filter(([id, _]) => id !== this.currentActiveSessionId)  // 排除当前活跃会话
      .sort((a, b) => a[1].lastActiveAt - b[1].lastActiveAt);

    const excess = this.sessions.size - MAX_SESSIONS_IN_MEMORY;

    for (let i = 0; i < excess && i < sortedSessions.length; i++) {
      const [sessionId, _] = sortedSessions[i];
      console.log(`[SessionManager] 内存限制，删除会话: ${sessionId}`);
      this.deleteSession(sessionId);
    }
  }

  /**
   * 设置自动断开定时器
   * 非活跃会话在一段时间后自动断开SSE连接
   */
  scheduleAutoDisconnect(sessionId: string, currentActiveSessionId: string): void {
    // 如果是当前活跃会话，不设置定时器
    if (sessionId === currentActiveSessionId) {
      this.clearAutoDisconnectTimer(sessionId);
      return;
    }

    // 清除旧定时器
    this.clearAutoDisconnectTimer(sessionId);

    // 设置新定时器
    const timer = setTimeout(() => {
      console.log(`[SessionManager] 自动断开非活跃会话: ${sessionId}`);
      this.disconnectSession(sessionId);
    }, AUTO_DISCONNECT_DELAY);

    this.autoDisconnectTimers.set(sessionId, timer);
  }

  /**
   * 清除自动断开定时器
   */
  private clearAutoDisconnectTimer(sessionId: string): void {
    const timer = this.autoDisconnectTimers.get(sessionId);
    if (timer) {
      clearTimeout(timer);
      this.autoDisconnectTimers.delete(sessionId);
    }
  }

  /**
   * 删除会话
   */
  deleteSession(sessionId: string): void {
    // 先断开连接
    this.disconnectSession(sessionId);

    // 删除状态
    this.sessions.delete(sessionId);

    console.log(`[SessionManager] 删除会话: ${sessionId}`);
  }

  /**
   * 获取所有会话ID
   */
  getAllSessionIds(): string[] {
    return Array.from(this.sessions.keys());
  }

  /**
   * 获取活跃连接数量
   */
  getActiveConnectionCount(): number {
    return Array.from(this.sessions.values())
      .filter(state => state.reader !== null).length;
  }

  /**
   * 注册状态变更监听器
   */
  addListener(listener: StateChangeListener): () => void {
    this.listeners.add(listener);

    // 返回取消监听的函数
    return () => {
      this.listeners.delete(listener);
    };
  }

  /**
   * 通知所有监听器
   */
  private notifyListeners(sessionId: string, state: SessionState): void {
    this.listeners.forEach(listener => {
      try {
        listener(sessionId, state);
      } catch (error) {
        console.error('[SessionManager] 监听器执行失败:', error);
      }
    });
  }

  /**
   * 清理所有会话
   */
  dispose(): void {
    // 断开所有连接
    this.sessions.forEach((_, sessionId) => {
      this.disconnectSession(sessionId);
    });

    // 清空所有状态
    this.sessions.clear();
    this.listeners.clear();

    console.log('[SessionManager] dispose all sessions');
  }
}
