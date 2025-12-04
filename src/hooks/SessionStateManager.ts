/**
 * SessionStateManager - 澶氫細璇濈姸鎬佺鐞嗗櫒
 *
 * 鏍稿績鍔熻兘:
 * - 姣忎釜浼氳瘽缁存姢鐙珛鐨勭姸鎬侊紙messages, activities, tasks绛夛級
 * - 姣忎釜浼氳瘽缁存姢鐙珛鐨凷SE杩炴帴锛坒etch reader锛?
 * - 鍒囨崲浼氳瘽鏃朵笉涓柇鍚庡彴浼氳瘽鐨勫搷搴?
 * - 闄愬埗鍚屾椂婵€娲荤殑SSE杩炴帴鏁伴噺锛岄槻姝㈠唴瀛樻硠婕?
 * - 鍚庡彴浼氳瘽鑷姩淇濆瓨鍒發ocalStorage
 */

import type { Message, ActivityItem, ProgressData } from '@/types/agent';

// 浠诲姟鎺ュ彛
interface Task {
  task_id: number;
  description: string;
  tool?: string;
  estimated_time?: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  elapsed_time?: number;
}

// 浼氳瘽鐘舵€佹帴鍙?
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

  // SSE杩炴帴绠＄悊
  reader: ReadableStreamDefaultReader<Uint8Array> | null;
  abortController: AbortController | null;

  // 鍏冩暟鎹?
  createdAt: number;
  lastActiveAt: number;
  mode?: 'planning' | 'react';
}

// 鐘舵€佸彉鏇寸洃鍚櫒
type StateChangeListener = (sessionId: string, state: SessionState) => void;

const MAX_ACTIVE_CONNECTIONS = 3;  // 鏈€澶氬悓鏃朵繚鎸?涓猄SE杩炴帴
const MAX_SESSIONS_IN_MEMORY = 10;  // 鏈€澶氬湪鍐呭瓨涓繚瀛?0涓細璇?
const AUTO_DISCONNECT_DELAY = 60000;  // 60绉掑悗鑷姩鏂紑闈炴椿璺冧細璇濈殑杩炴帴

export class SessionStateManager {
  private sessions: Map<string, SessionState> = new Map();
  private listeners: Set<StateChangeListener> = new Set();
  private autoDisconnectTimers: Map<string, NodeJS.Timeout> = new Map();
  private currentActiveSessionId: string | null = null;  // 褰撳墠鏄剧ず鐨勪細璇滻D

  /**
   * 鍒涘缓鏂颁細璇濈姸鎬?
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
      mode: initialData?.mode || 'planning'
    };

    this.sessions.set(sessionId, state);
    console.log(`[SessionManager] 鍒涘缓浼氳瘽: ${sessionId}`, state);

    // 妫€鏌ュ苟寮哄埗鍐呭瓨闄愬埗
    this.enforceMemoryLimit();

    return state;
  }

  /**
   * 璁剧疆褰撳墠娲昏穬浼氳瘽锛堢敤浜庡垽鏂槸鍚﹁Е鍙慤I鏇存柊锛?
   */
  setActiveSession(sessionId: string): void {
    this.currentActiveSessionId = sessionId;

    // 鏇存柊璇ヤ細璇濈殑鏈€鍚庢椿璺冩椂闂?
    const session = this.sessions.get(sessionId);
    if (session) {
      session.lastActiveAt = Date.now();
    }

    console.log(`[SessionManager] 璁剧疆娲昏穬浼氳瘽: ${sessionId}`);
  }

  /**
   * 鑾峰彇褰撳墠娲昏穬浼氳瘽ID
   */
  getActiveSessionId(): string | null {
    return this.currentActiveSessionId;
  }

  /**
   * 妫€鏌ユ槸鍚︽槸褰撳墠娲昏穬浼氳瘽
   */
  isActiveSession(sessionId: string): boolean {
    return this.currentActiveSessionId === sessionId;
  }

  /**
   * 鑾峰彇浼氳瘽鐘舵€?
   */
  getSession(sessionId: string): SessionState | undefined {
    return this.sessions.get(sessionId);
  }

  /**
   * 鑾峰彇鎴栧垱寤轰細璇?
   */
  getOrCreateSession(sessionId: string, initialData?: Partial<SessionState>): SessionState {
    let session = this.sessions.get(sessionId);
    if (!session) {
      session = this.createSession(sessionId, initialData);
    }
    return session;
  }

  /**
   * 鏇存柊浼氳瘽鐘舵€侊紙閮ㄥ垎鏇存柊锛?
   */
  updateSession(sessionId: string, updates: Partial<SessionState>): void {
    const session = this.sessions.get(sessionId);
    if (!session) {
      console.warn(`[SessionManager] 浼氳瘽涓嶅瓨鍦? ${sessionId}`);
      return;
    }

    Object.assign(session, updates);
    session.lastActiveAt = Date.now();

    // 閫氱煡鐩戝惉鍣?
    this.notifyListeners(sessionId, session);
  }

  /**
   * 寮€濮婼SE杩炴帴
   */
  startStreaming(
    sessionId: string,
    reader: ReadableStreamDefaultReader<Uint8Array>,
    abortController: AbortController
  ): void {
    const session = this.sessions.get(sessionId);
    if (!session) {
      console.warn(`[SessionManager] 浼氳瘽涓嶅瓨鍦? ${sessionId}`);
      return;
    }

    // 娓呴櫎涔嬪墠鐨勮繛鎺ワ紙濡傛灉鏈夛級
    this.disconnectSession(sessionId);

    session.reader = reader;
    session.abortController = abortController;
    session.isLoading = true;
    session.lastActiveAt = Date.now();

    console.log(`[SessionManager] 寮€濮婼SE杩炴帴: ${sessionId}`);

    // 妫€鏌ュ苟闄愬埗杩炴帴鏁伴噺
    this.enforceConnectionLimit();
  }

  /**
   * 鍋滄SSE杩炴帴
   */
  disconnectSession(sessionId: string): void {
    const session = this.sessions.get(sessionId);
    if (!session) return;

    // 鍏抽棴reader
    if (session.reader) {
      try {
        session.reader.cancel();
      } catch (error) {
        console.warn(`[SessionManager] 鍏抽棴reader澶辫触:`, error);
      }
      session.reader = null;
    }

    // 涓璇锋眰
    if (session.abortController) {
      try {
        session.abortController.abort();
      } catch (error) {
        console.warn(`[SessionManager] 涓璇锋眰澶辫触:`, error);
      }
      session.abortController = null;
    }

    session.isLoading = false;

    console.log(`[SessionManager] 鏂紑SSE杩炴帴: ${sessionId}`);

    // 娓呴櫎鑷姩鏂紑瀹氭椂鍣?
    this.clearAutoDisconnectTimer(sessionId);
  }

  /**
   * 寮哄埗闄愬埗娲昏穬杩炴帴鏁伴噺
   * 褰撹秴杩嘙AX_ACTIVE_CONNECTIONS鏃讹紝鏂紑鏈€涔呮湭浣跨敤鐨勮繛鎺?
   */
  private enforceConnectionLimit(): void {
    const activeSessions = Array.from(this.sessions.entries())
      .filter(([_, state]) => state.reader !== null)
      .sort((a, b) => a[1].lastActiveAt - b[1].lastActiveAt);

    if (activeSessions.length > MAX_ACTIVE_CONNECTIONS) {
      const excess = activeSessions.length - MAX_ACTIVE_CONNECTIONS;
      console.warn(`[SessionManager] 瓒呰繃杩炴帴鏁伴檺鍒讹紝鍏抽棴${excess}涓渶鏃х殑杩炴帴`);

      for (let i = 0; i < excess; i++) {
        const [sessionId, _] = activeSessions[i];
        this.disconnectSession(sessionId);
      }
    }
  }

  /**
   * 寮哄埗闄愬埗鍐呭瓨涓殑浼氳瘽鏁伴噺
   * 褰撹秴杩嘙AX_SESSIONS_IN_MEMORY鏃讹紝鍒犻櫎鏈€涔呮湭浣跨敤鐨勪細璇濓紙浣嗕笉鍒犻櫎褰撳墠娲昏穬浼氳瘽锛?
   */
  private enforceMemoryLimit(): void {
    if (this.sessions.size <= MAX_SESSIONS_IN_MEMORY) {
      return;
    }

    // 鎸夋渶鍚庢椿璺冩椂闂存帓搴忥紙鏈€鏃х殑鍦ㄥ墠锛?
    const sortedSessions = Array.from(this.sessions.entries())
      .filter(([id, _]) => id !== this.currentActiveSessionId)  // 鎺掗櫎褰撳墠娲昏穬浼氳瘽
      .sort((a, b) => a[1].lastActiveAt - b[1].lastActiveAt);

    const excess = this.sessions.size - MAX_SESSIONS_IN_MEMORY;

    for (let i = 0; i < excess && i < sortedSessions.length; i++) {
      const [sessionId, _] = sortedSessions[i];
      console.log(`[SessionManager] 鍐呭瓨闄愬埗锛屽垹闄や細璇? ${sessionId}`);
      this.deleteSession(sessionId);
    }
  }

  /**
   * 璁剧疆鑷姩鏂紑瀹氭椂鍣?
   * 闈炴椿璺冧細璇濆湪涓€娈垫椂闂村悗鑷姩鏂紑SSE杩炴帴
   */
  scheduleAutoDisconnect(sessionId: string, currentActiveSessionId: string): void {
    // 濡傛灉鏄綋鍓嶆椿璺冧細璇濓紝涓嶈缃畾鏃跺櫒
    if (sessionId === currentActiveSessionId) {
      this.clearAutoDisconnectTimer(sessionId);
      return;
    }

    // 娓呴櫎鏃у畾鏃跺櫒
    this.clearAutoDisconnectTimer(sessionId);

    // 璁剧疆鏂板畾鏃跺櫒
    const timer = setTimeout(() => {
      console.log(`[SessionManager] 鑷姩鏂紑闈炴椿璺冧細璇? ${sessionId}`);
      this.disconnectSession(sessionId);
    }, AUTO_DISCONNECT_DELAY);

    this.autoDisconnectTimers.set(sessionId, timer);
  }

  /**
   * 娓呴櫎鑷姩鏂紑瀹氭椂鍣?
   */
  private clearAutoDisconnectTimer(sessionId: string): void {
    const timer = this.autoDisconnectTimers.get(sessionId);
    if (timer) {
      clearTimeout(timer);
      this.autoDisconnectTimers.delete(sessionId);
    }
  }

  /**
   * 鍒犻櫎浼氳瘽
   */
  deleteSession(sessionId: string): void {
    // 鍏堟柇寮€杩炴帴
    this.disconnectSession(sessionId);

    // 鍒犻櫎鐘舵€?
    this.sessions.delete(sessionId);

    console.log(`[SessionManager] 鍒犻櫎浼氳瘽: ${sessionId}`);
  }

  /**
   * 鑾峰彇鎵€鏈変細璇滻D
   */
  getAllSessionIds(): string[] {
    return Array.from(this.sessions.keys());
  }

  /**
   * 鑾峰彇娲昏穬杩炴帴鏁伴噺
   */
  getActiveConnectionCount(): number {
    return Array.from(this.sessions.values())
      .filter(state => state.reader !== null).length;
  }

  /**
   * 娉ㄥ唽鐘舵€佸彉鏇寸洃鍚櫒
   */
  addListener(listener: StateChangeListener): () => void {
    this.listeners.add(listener);

    // 杩斿洖鍙栨秷鐩戝惉鐨勫嚱鏁?
    return () => {
      this.listeners.delete(listener);
    };
  }

  /**
   * 閫氱煡鎵€鏈夌洃鍚櫒
   */
  private notifyListeners(sessionId: string, state: SessionState): void {
    this.listeners.forEach(listener => {
      try {
        listener(sessionId, state);
      } catch (error) {
        console.error('[SessionManager] 鐩戝惉鍣ㄦ墽琛屽け璐?', error);
      }
    });
  }

  /**
   * 娓呯悊鎵€鏈変細璇?
   */
  dispose(): void {
    // 鏂紑鎵€鏈夎繛鎺?
    this.sessions.forEach((_, sessionId) => {
      this.disconnectSession(sessionId);
    });

    // 娓呯┖鎵€鏈夌姸鎬?
    this.sessions.clear();
    this.listeners.clear();

    console.log('[SessionManager] dispose all sessions');
  }
}


