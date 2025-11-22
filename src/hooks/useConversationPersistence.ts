/**
 * useConversationPersistence - 对话持久化管理Hook
 *
 * 功能:
 * - 保存对话到localStorage
 * - 恢复历史对话
 * - 管理多个对话会话
 * - 自动保存/加载
 */

import { useEffect, useCallback, useState } from 'react';
import type { Message } from '@/types/agent';

interface ConversationSession {
  id: string;
  conversationId: string;  // 后端的conversation_id
  messages: Message[];
  createdAt: string;
  updatedAt: string;
  title: string;  // 对话标题（从第一条用户消息生成）
  mode?: 'planning' | 'react';
  workId?: string;
  chapterId?: string;
}

interface UseConversationPersistenceOptions {
  sessionId?: string;  // 当前会话ID，如果为空则创建新会话
  autoSave?: boolean;  // 是否自动保存（默认true）
  maxSessions?: number;  // 最多保留多少个会话（默认10）
  workId?: string;  // 🆕 作品ID（用于会话隔离）
  chapterId?: string;  // 🆕 章节ID（用于会话隔离）
  contextKey?: string;  // 🆕 自定义上下文键（优先级高于workId+chapterId）
}

interface UseConversationPersistenceReturn {
  // 当前会话
  currentSession: ConversationSession | null;
  sessionId: string;

  // 会话管理
  saveSession: (messages: Message[], conversationId?: string, metadata?: Partial<ConversationSession>) => void;
  loadSession: (sessionId: string) => ConversationSession | null;
  deleteSession: (sessionId: string) => void;
  clearCurrentSession: () => void;

  // 会话列表
  getAllSessions: () => ConversationSession[];
  createNewSession: (metadata?: Partial<ConversationSession>) => string;

  // 标题管理
  updateSessionTitle: (sessionId: string, title: string) => void;
}

const STORAGE_KEY_PREFIX = 'agent_conversation_';
const SESSIONS_LIST_KEY = 'agent_conversation_sessions';
const CONTEXT_SESSION_MAP_KEY = 'agent_context_session_map';  // 🆕 上下文到会话ID的映射
const DEFAULT_MAX_SESSIONS = 10;

/**
 * 生成会话ID
 */
function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * 🆕 生成上下文键
 */
function generateContextKey(workId?: string, chapterId?: string): string | null {
  if (chapterId) return `chapter_${chapterId}`;
  if (workId) return `work_${workId}`;
  return null;
}

/**
 * 从消息生成标题（取第一条用户消息的前30个字符）
 */
function generateTitleFromMessages(messages: Message[]): string {
  const firstUserMessage = messages.find(m => m.role === 'user');
  if (!firstUserMessage) return '新对话';

  const content = firstUserMessage.content.trim();
  if (content.length <= 30) return content;
  return content.substring(0, 30) + '...';
}

/**
 * 对话持久化Hook
 */
export function useConversationPersistence(
  options: UseConversationPersistenceOptions = {}
): UseConversationPersistenceReturn {
  const {
    sessionId: initialSessionId,
    autoSave = true,
    maxSessions = DEFAULT_MAX_SESSIONS,
    workId,
    chapterId,
    contextKey: customContextKey
  } = options;

  // 🆕 计算上下文键
  const contextKey = customContextKey || generateContextKey(workId, chapterId);

  // 🆕 根据上下文键查找或创建会话ID
  const getOrCreateSessionId = useCallback((): string => {
    if (initialSessionId) return initialSessionId;

    if (contextKey) {
      // 从映射表中查找已有的会话ID
      try {
        const mapStr = localStorage.getItem(CONTEXT_SESSION_MAP_KEY);
        const map: Record<string, string> = mapStr ? JSON.parse(mapStr) : {};

        if (map[contextKey]) {
          // 验证会话是否存在
          const session = localStorage.getItem(`${STORAGE_KEY_PREFIX}${map[contextKey]}`);
          if (session) {
            console.log(`[Persistence] 找到${contextKey}的会话:`, map[contextKey]);
            return map[contextKey];
          }
        }
      } catch (error) {
        console.error('[Persistence] Failed to load context map:', error);
      }
    }

    // 创建新会话ID
    return generateSessionId();
  }, [initialSessionId, contextKey]);

  // 当前会话ID（使用useState以便能触发更新）
  const [sessionId, setSessionId] = useState<string>(getOrCreateSessionId());
  const [currentSession, setCurrentSession] = useState<ConversationSession | null>(null);

  /**
   * 🆕 监听contextKey变化，切换会话
   */
  useEffect(() => {
    const newSessionId = getOrCreateSessionId();
    setSessionId(prev => {
      if (prev !== newSessionId) {
        console.log(`[Persistence] 上下文变化，切换会话: ${prev} -> ${newSessionId}`);
        return newSessionId;
      }
      return prev;
    });
  }, [contextKey, getOrCreateSessionId]); // 只监听contextKey和函数变化

  /**
   * 获取所有会话ID列表
   */
  const getSessionsList = useCallback((): string[] => {
    try {
      const stored = localStorage.getItem(SESSIONS_LIST_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('[Persistence] Failed to load sessions list:', error);
      return [];
    }
  }, []);

  /**
   * 更新会话列表
   */
  const updateSessionsList = useCallback((sessionIds: string[]) => {
    try {
      // 限制会话数量
      const limited = sessionIds.slice(0, maxSessions);
      localStorage.setItem(SESSIONS_LIST_KEY, JSON.stringify(limited));
    } catch (error) {
      console.error('[Persistence] Failed to update sessions list:', error);
    }
  }, [maxSessions]);

  /**
   * 从localStorage加载会话
   */
  const loadSession = useCallback((sessionId: string): ConversationSession | null => {
    try {
      const stored = localStorage.getItem(`${STORAGE_KEY_PREFIX}${sessionId}`);
      if (!stored) return null;

      const session = JSON.parse(stored) as ConversationSession;
      console.log(`[Persistence] Loaded session ${sessionId}:`, session.messages.length, 'messages');
      return session;
    } catch (error) {
      console.error(`[Persistence] Failed to load session ${sessionId}:`, error);
      return null;
    }
  }, []);

  /**
   * 保存会话到localStorage
   */
  const saveSession = useCallback((
    messages: Message[],
    conversationId?: string,
    metadata?: Partial<ConversationSession>
  ) => {
    try {
      const now = new Date().toISOString();

      // 创建或更新会话
      const session: ConversationSession = {
        id: sessionId,
        conversationId: conversationId || currentSession?.conversationId || '',
        messages,
        createdAt: currentSession?.createdAt || now,
        updatedAt: now,
        title: metadata?.title || currentSession?.title || generateTitleFromMessages(messages),
        mode: metadata?.mode || currentSession?.mode,
        workId: metadata?.workId || currentSession?.workId,
        chapterId: metadata?.chapterId || currentSession?.chapterId,
      };

      // 保存会话数据
      localStorage.setItem(`${STORAGE_KEY_PREFIX}${sessionId}`, JSON.stringify(session));
      setCurrentSession(session);  // 🔧 使用setState

      // 🆕 保存上下文到会话ID的映射
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

      // 更新会话列表（将当前会话移到最前面）
      const sessions = getSessionsList();
      const updatedSessions = [
        sessionId,
        ...sessions.filter(id => id !== sessionId)
      ];
      updateSessionsList(updatedSessions);

      console.log(`[Persistence] Saved session ${sessionId}${contextKey ? ` [${contextKey}]` : ''}:`, messages.length, 'messages');
    } catch (error) {
      console.error('[Persistence] Failed to save session:', error);

      // 如果是存储空间不足错误，尝试清理旧会话
      if (error instanceof DOMException && error.name === 'QuotaExceededError') {
        console.warn('[Persistence] Storage quota exceeded, cleaning old sessions...');
        const sessions = getSessionsList();
        if (sessions.length > 0) {
          // 删除最旧的会话
          const oldestSession = sessions[sessions.length - 1];
          deleteSession(oldestSession);
          // 重试保存
          saveSession(messages, conversationId, metadata);
        }
      }
    }
  }, [getSessionsList, updateSessionsList]);

  /**
   * 删除会话
   */
  const deleteSession = useCallback((sessionId: string) => {
    try {
      localStorage.removeItem(`${STORAGE_KEY_PREFIX}${sessionId}`);

      // 从会话列表中移除
      const sessions = getSessionsList();
      const updatedSessions = sessions.filter(id => id !== sessionId);
      updateSessionsList(updatedSessions);

      console.log(`[Persistence] Deleted session ${sessionId}`);
    } catch (error) {
      console.error(`[Persistence] Failed to delete session ${sessionId}:`, error);
    }
  }, [getSessionsList, updateSessionsList]);

  /**
   * 清空当前会话（但不删除）
   */
  const clearCurrentSession = useCallback(() => {
    deleteSession(sessionId);

    // 创建新会话
    const newSessionId = generateSessionId();
    setSessionId(newSessionId);  // 🔧 使用setState
    setCurrentSession(null);  // 🔧 使用setState

    console.log(`[Persistence] Cleared session ${sessionId}, new session: ${newSessionId}`);
  }, [deleteSession, sessionId]);

  /**
   * 获取所有会话（按时间倒序）
   */
  const getAllSessions = useCallback((): ConversationSession[] => {
    const sessionIds = getSessionsList();
    const sessions: ConversationSession[] = [];

    for (const sessionId of sessionIds) {
      const session = loadSession(sessionId);
      if (session) {
        sessions.push(session);
      }
    }

    // 按更新时间倒序排序
    return sessions.sort((a, b) =>
      new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
    );
  }, [getSessionsList, loadSession]);

  /**
   * 创建新会话
   */
  const createNewSession = useCallback((metadata?: Partial<ConversationSession>): string => {
    const newSessionId = generateSessionId();
    setSessionId(newSessionId);  // 🔧 使用setState
    setCurrentSession(null);  // 🔧 使用setState

    // 如果提供了元数据，保存空会话
    if (metadata) {
      saveSession([], undefined, metadata);
    }

    console.log(`[Persistence] Created new session: ${newSessionId}`);
    return newSessionId;
  }, [saveSession]);

  /**
   * 更新会话标题
   */
  const updateSessionTitle = useCallback((targetSessionId: string, title: string) => {
    const session = loadSession(targetSessionId);
    if (!session) return;

    session.title = title;
    session.updatedAt = new Date().toISOString();

    localStorage.setItem(`${STORAGE_KEY_PREFIX}${targetSessionId}`, JSON.stringify(session));

    if (targetSessionId === sessionId) {
      setCurrentSession(session);  // 🔧 使用setState
    }

    console.log(`[Persistence] Updated session title: ${targetSessionId} -> ${title}`);
  }, [loadSession, sessionId]);

  /**
   * 初始化：加载当前会话
   */
  useEffect(() => {
    const session = loadSession(sessionId);

    if (session) {
      setCurrentSession(session);  // 🔧 使用setState
      console.log(`[Persistence] Restored session ${sessionId}:`, session.messages.length, 'messages');
    } else {
      setCurrentSession(null);  // 🔧 使用setState
      console.log(`[Persistence] Starting new session: ${sessionId}`);
    }
  }, [sessionId, loadSession]);  // 🔧 添加sessionId依赖，以便切换章节时重新加载

  return {
    currentSession,  // 🔧 直接返回state
    sessionId,  // 🔧 直接返回state
    saveSession,
    loadSession,
    deleteSession,
    clearCurrentSession,
    getAllSessions,
    createNewSession,
    updateSessionTitle,
  };
}
