import { useCallback, useEffect, useState } from 'react';
import type { Message } from '@/types/agent';
import { compressSessionMessages } from '@/utils/sessionCompression_v2';

export interface ConversationSession {
  id: string;
  conversationId: string;
  messages: Message[];
  createdAt: string;
  updatedAt: string;
  title: string;
  mode?: 'plan' | 'chat';
  workId?: string;
  chapterId?: string;
}

interface UseConversationPersistenceOptions {
  sessionId?: string;
  autoSave?: boolean;
  maxSessions?: number;
  workId?: string;
  chapterId?: string;
  contextKey?: string;
  useBackend?: boolean; // true 时优先使用后端会话创建/列表
}

interface UseConversationPersistenceReturn {
  currentSession: ConversationSession | null;
  sessionId: string;
  saveSession: (messages: Message[], conversationId?: string, metadata?: Partial<ConversationSession>) => void;
  loadSession: (sessionId: string) => ConversationSession | null;
  deleteSession: (sessionId: string) => void;
  clearCurrentSession: () => void;
  getAllSessions: () => ConversationSession[];
  createNewSession: (metadata?: Partial<ConversationSession>) => Promise<string>;
  getSessionsOrder: () => string[];
  updateSessionsOrder: (order: string[]) => void;
  insertSessionAfter: (newSessionId: string, afterSessionId: string) => void;
  updateSessionTitle: (sessionId: string, title: string) => void;
}

const STORAGE_KEY_PREFIX = 'agent_conversation_';
const SESSIONS_LIST_KEY = 'agent_conversation_sessions';
const SESSIONS_ORDER_KEY = 'agent_sessions_order';
const CONTEXT_SESSION_MAP_KEY = 'agent_context_session_map';
const DEFAULT_MAX_SESSIONS = 5; // 先改为 5，观察效果后再决定是否进一步减少
const DEFAULT_TITLE = '新会话';

function normalizeMode(mode?: string): 'plan' | 'chat' {
  return mode === 'plan' ? 'plan' : 'chat';
}

function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`;
}

function generateContextKey(workId?: string, chapterId?: string): string | null {
  if (workId) return `work_${workId}`;
  if (chapterId) return `chapter_${chapterId}`;
  return null;
}

function generateTitleFromMessages(messages: Message[]): string {
  const firstUserMessage = messages.find((m) => m.role === 'user');
  if (!firstUserMessage) return DEFAULT_TITLE;

  const content = firstUserMessage.content.trim();
  return content.length <= 30 ? content : `${content.substring(0, 30)}...`;
}

export function useConversationPersistence(
  options: UseConversationPersistenceOptions = {}
): UseConversationPersistenceReturn {
  const {
    sessionId: initialSessionId,
    maxSessions = DEFAULT_MAX_SESSIONS,
    workId,
    chapterId,
    contextKey: customContextKey,
    useBackend = false
  } = options;

  const contextKey = customContextKey || generateContextKey(workId, chapterId);

  const getOrCreateSessionId = useCallback((): string => {
    if (initialSessionId) return initialSessionId;

    if (contextKey) {
      try {
        const mapStr = localStorage.getItem(CONTEXT_SESSION_MAP_KEY);
        const map: Record<string, string> = mapStr ? JSON.parse(mapStr) : {};
        const mappedId = map[contextKey];
        if (mappedId && localStorage.getItem(`${STORAGE_KEY_PREFIX}${mappedId}`)) {
          return mappedId;
        }
      } catch (error) {
        console.error('[Persistence] Failed to read context map:', error);
      }
    }

    return generateSessionId();
  }, [contextKey, initialSessionId]);

  const [sessionId, setSessionId] = useState<string>(getOrCreateSessionId());
  const [currentSession, setCurrentSession] = useState<ConversationSession | null>(null);

  const getSessionsList = useCallback((): string[] => {
    try {
      const stored = localStorage.getItem(SESSIONS_LIST_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('[Persistence] Failed to load sessions list:', error);
      return [];
    }
  }, []);

  const updateSessionsList = useCallback(
    (sessionIds: string[]) => {
      try {
        const limited = sessionIds.slice(0, maxSessions);
        localStorage.setItem(SESSIONS_LIST_KEY, JSON.stringify(limited));
      } catch (error) {
        console.error('[Persistence] Failed to update sessions list:', error);
      }
    },
    [maxSessions]
  );

  const loadSession = useCallback((targetSessionId: string): ConversationSession | null => {
    try {
      const stored = localStorage.getItem(`${STORAGE_KEY_PREFIX}${targetSessionId}`);
      if (!stored) return null;

      const session = JSON.parse(stored) as ConversationSession;
      return session;
    } catch (error) {
      console.error(`[Persistence] Failed to load session ${targetSessionId}:`, error);
      return null;
    }
  }, []);

  const saveSession = useCallback(
    (messages: Message[], conversationId?: string, metadata?: Partial<ConversationSession>) => {
      try {
        const now = new Date().toISOString();
        const existing = currentSession;

        // 轻量压缩：保留当前会话结构，压缩大字段（flowItems/长文本）
        const messagesToPersist = compressSessionMessages(messages, true);

        const session: ConversationSession = {
          id: sessionId,
          conversationId: conversationId || existing?.conversationId || '',
          messages: messagesToPersist,
          createdAt: existing?.createdAt || now,
          updatedAt: now,
          title: metadata?.title || existing?.title || generateTitleFromMessages(messages),
          mode: normalizeMode(metadata?.mode ?? existing?.mode),
          workId: metadata?.workId ?? existing?.workId,
          chapterId: metadata?.chapterId ?? existing?.chapterId
        };

        localStorage.setItem(`${STORAGE_KEY_PREFIX}${sessionId}`, JSON.stringify(session));
        setCurrentSession(session);

        if (contextKey) {
          try {
            const mapStr = localStorage.getItem(CONTEXT_SESSION_MAP_KEY);
            const map: Record<string, string> = mapStr ? JSON.parse(mapStr) : {};
            map[contextKey] = sessionId;
            localStorage.setItem(CONTEXT_SESSION_MAP_KEY, JSON.stringify(map));
          } catch (error) {
            console.error('[Persistence] Failed to save context map:', error);
          }
        }

        const sessions = getSessionsList();
        const updatedSessions = [sessionId, ...sessions.filter((id) => id !== sessionId)];
        updateSessionsList(updatedSessions);
      } catch (error) {
        console.error('[Persistence] Failed to save session:', error);
      }
    },
    [contextKey, currentSession, getSessionsList, sessionId, updateSessionsList]
  );

  const deleteSession = useCallback(
    (targetSessionId: string) => {
      try {
        localStorage.removeItem(`${STORAGE_KEY_PREFIX}${targetSessionId}`);
        const sessions = getSessionsList();
        const updatedSessions = sessions.filter((id) => id !== targetSessionId);
        updateSessionsList(updatedSessions);
      } catch (error) {
        console.error(`[Persistence] Failed to delete session ${targetSessionId}:`, error);
      }
    },
    [getSessionsList, updateSessionsList]
  );

  const clearCurrentSession = useCallback(() => {
    deleteSession(sessionId);
    const newSessionId = generateSessionId();
    setSessionId(newSessionId);
    setCurrentSession(null);
  }, [deleteSession, sessionId]);

  const getAllSessions = useCallback((): ConversationSession[] => {
    const sessionIds = getSessionsList();
    const sessions: ConversationSession[] = [];

    for (const id of sessionIds) {
      const session = loadSession(id);
      if (session) sessions.push(session);
    }

    return sessions.sort(
      (a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
    );
  }, [getSessionsList, loadSession]);

  const createNewSession = useCallback(
    async (metadata?: Partial<ConversationSession>): Promise<string> => {
      // 后端模式：创建真实会话并用返回的 session_id
      if (useBackend) {
        try {
          const resp = await import('@/services/agentApi').then(m => m.agentApi.createSession({
            title: metadata?.title,
            work_id: metadata?.workId || workId,
            chapter_id: metadata?.chapterId || chapterId,
            conversation_id: initialSessionId || undefined
          }));
          const newId = resp.session_id;
          setSessionId(newId);
          setCurrentSession(null);
          const now = new Date().toISOString();
          localStorage.setItem(
            `${STORAGE_KEY_PREFIX}${newId}`,
            JSON.stringify({
              id: newId,
              conversationId: resp.conversation_id || '',
              messages: [],
              createdAt: resp.created_at || now,
              updatedAt: resp.created_at || now,
              title: resp.title || metadata?.title || DEFAULT_TITLE,
              workId: metadata?.workId || workId,
              chapterId: metadata?.chapterId || chapterId
            } as ConversationSession)
          );
          const sessions = getSessionsList();
          updateSessionsList([newId, ...sessions]);
          return newId;
        } catch (error) {
          console.warn('[Persistence] createSession failed, fallback to local mode:', error);
        }
      }

      // 本地模式
      const newSessionId = generateSessionId();
      setSessionId(newSessionId);
      setCurrentSession(null);

      if (metadata || useBackend) {
        localStorage.setItem(
          `${STORAGE_KEY_PREFIX}${newSessionId}`,
          JSON.stringify({
            id: newSessionId,
            conversationId: '',
            messages: [],
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            title: metadata?.title || DEFAULT_TITLE,
            mode: normalizeMode(metadata?.mode),
            workId: metadata?.workId || workId,
            chapterId: metadata?.chapterId || chapterId
          } as ConversationSession)
        );
      }

      const sessions = getSessionsList();
      updateSessionsList([newSessionId, ...sessions]);
      return newSessionId;
    },
    [chapterId, getSessionsList, updateSessionsList, useBackend, workId]
  );

  const updateSessionTitle = useCallback(
    (targetSessionId: string, title: string) => {
      const session = loadSession(targetSessionId);
      if (!session) return;

      const updated: ConversationSession = { ...session, title, updatedAt: new Date().toISOString() };
      localStorage.setItem(`${STORAGE_KEY_PREFIX}${targetSessionId}`, JSON.stringify(updated));

      if (targetSessionId === sessionId) {
        setCurrentSession(updated);
      }
    },
    [loadSession, sessionId]
  );

  const getSessionsOrder = useCallback((): string[] => {
    try {
      const stored = localStorage.getItem(SESSIONS_ORDER_KEY);
      if (!stored) return [];

      const order: string[] = JSON.parse(stored);
      const validSessions = new Set(getAllSessions().map((s) => s.id));
      const validOrder = order.filter((id) => validSessions.has(id));
      const missing = Array.from(validSessions).filter((id) => !validOrder.includes(id));
      const finalOrder = [...validOrder, ...missing];

      if (JSON.stringify(order) !== JSON.stringify(finalOrder)) {
        localStorage.setItem(SESSIONS_ORDER_KEY, JSON.stringify(finalOrder));
      }

      return finalOrder;
    } catch (error) {
      console.error('[Persistence] Failed to load sessions order:', error);
      return [];
    }
  }, [getAllSessions]);

  const updateSessionsOrder = useCallback((order: string[]) => {
    try {
      localStorage.setItem(SESSIONS_ORDER_KEY, JSON.stringify(order));
    } catch (error) {
      console.error('[Persistence] Failed to update sessions order:', error);
    }
  }, []);

  const insertSessionAfter = useCallback(
    (newSessionId: string, afterSessionId: string) => {
      const order = getSessionsOrder();
      const index = order.indexOf(afterSessionId);
      if (index === -1) {
        order.push(newSessionId);
      } else {
        order.splice(index + 1, 0, newSessionId);
      }
      updateSessionsOrder(order);
    },
    [getSessionsOrder, updateSessionsOrder]
  );

  useEffect(() => {
    const newSessionId = getOrCreateSessionId();
    setSessionId((prev) => (prev !== newSessionId ? newSessionId : prev));
  }, [getOrCreateSessionId]);

  useEffect(() => {
    const session = loadSession(sessionId);
    if (session) {
      setCurrentSession(session);
    } else {
      setCurrentSession(null);
    }
  }, [sessionId, loadSession]);

  return {
    currentSession,
    sessionId,
    saveSession,
    loadSession,
    deleteSession,
    clearCurrentSession,
    getAllSessions,
    createNewSession,
    getSessionsOrder,
    updateSessionsOrder,
    insertSessionAfter,
    updateSessionTitle
  };
}
