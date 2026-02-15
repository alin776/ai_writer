/**
 * 标签页 localStorage 操作工具
 */

export interface Tab {
  id: string;
  chapterId: string;
  title: string;
  sessionId: string;
  conversationId?: string;
  createdAt: string;
  updatedAt: string;
}

const TAB_PREFIX = 'agent_tab_';
const CHAPTER_TABS_MAP_KEY = 'chapter_tabs_map';
const CHAPTER_ACTIVE_TAB_KEY = 'chapter_active_tab';
const SESSION_KEY_PREFIX = 'agent_conversation_';
const SESSIONS_LIST_KEY = 'agent_conversation_sessions';
const CONTEXT_SESSION_MAP_KEY = 'agent_context_session_map';
const DEFAULT_TAB_TITLE = '新会话';

interface ConversationSessionSnapshot {
  id: string;
  conversationId?: string;
  title?: string;
  createdAt?: string;
  updatedAt?: string;
  chapterId?: string;
}

function isQuotaExceeded(error: unknown): boolean {
  if (!error || typeof error !== 'object') return false;
  const name = (error as { name?: string }).name;
  return name === 'QuotaExceededError' || name === 'NS_ERROR_DOM_QUOTA_REACHED';
}

function emitStorageQuotaEvent(message: string): void {
  if (typeof window === 'undefined') return;
  window.dispatchEvent(
    new CustomEvent('storage-quota-exceeded', {
      detail: { store: 'agent-tab', message }
    })
  );
}

function cleanupOldConversationSessions(keepCount: number = 5): void {
  try {
    const stored = localStorage.getItem(SESSIONS_LIST_KEY);
    if (!stored) return;
    const sessions: string[] = JSON.parse(stored);
    if (sessions.length <= keepCount) return;

    const toDelete = sessions.slice(keepCount);
    toDelete.forEach((sessionId) => {
      localStorage.removeItem(`${SESSION_KEY_PREFIX}${sessionId}`);
    });
    localStorage.setItem(SESSIONS_LIST_KEY, JSON.stringify(sessions.slice(0, keepCount)));
  } catch (error) {
    console.error('[TabStorage] Failed to cleanup old sessions:', error);
  }
}

function safeSetItem(key: string, value: string): boolean {
  if (typeof window === 'undefined') return false;
  try {
    localStorage.setItem(key, value);
    return true;
  } catch (error) {
    if (isQuotaExceeded(error)) {
      console.warn('[TabStorage] localStorage quota exceeded, cleanup and retry:', key);
      cleanupOldConversationSessions();
      try {
        localStorage.setItem(key, value);
        return true;
      } catch (retryError) {
        console.error('[TabStorage] localStorage quota still exceeded:', retryError);
        emitStorageQuotaEvent('存储空间不足，会话标签无法保存，请清理浏览器缓存或减少历史会话。');
        return false;
      }
    }
    console.error('[TabStorage] Failed to save:', error);
    return false;
  }
}

/**
 * 保存标签页数据
 */
export function saveTab(tab: Tab): void {
  try {
    safeSetItem(`${TAB_PREFIX}${tab.id}`, JSON.stringify(tab));
  } catch (error) {
    console.error('[TabStorage] Failed to save tab:', error);
  }
}

/**
 * 加载标签页数据
 */
export function loadTab(tabId: string): Tab | null {
  try {
    const stored = localStorage.getItem(`${TAB_PREFIX}${tabId}`);
    return stored ? JSON.parse(stored) : null;
  } catch (error) {
    console.error('[TabStorage] Failed to load tab:', error);
    return null;
  }
}

/**
 * 删除标签页数据
 */
export function deleteTab(tabId: string): void {
  try {
    localStorage.removeItem(`${TAB_PREFIX}${tabId}`);
  } catch (error) {
    console.error('[TabStorage] Failed to delete tab:', error);
  }
}

/**
 * 获取章节的所有标签页ID
 */
function dedupeIds(ids: string[]): string[] {
  const seen = new Set<string>();
  return ids.filter((id) => {
    if (seen.has(id)) return false;
    seen.add(id);
    return true;
  });
}

export function getChapterTabIds(chapterId: string): string[] {
  try {
    const stored = localStorage.getItem(CHAPTER_TABS_MAP_KEY);
    const map: Record<string, string[]> = stored ? JSON.parse(stored) : {};
    const ids = map[chapterId] || [];
    const uniqueIds = dedupeIds(ids);

    // 清理遗留的重复 ID，避免一次关闭移除多个标签
    if (uniqueIds.length !== ids.length) {
      map[chapterId] = uniqueIds;
      safeSetItem(CHAPTER_TABS_MAP_KEY, JSON.stringify(map));
    }

    return uniqueIds;
  } catch (error) {
    console.error('[TabStorage] Failed to get chapter tabs:', error);
    return [];
  }
}

/**
 * 获取章节的所有标签页
 */
export function getChapterTabs(chapterId: string): Tab[] {
  const tabIds = getChapterTabIds(chapterId);
  return tabIds.map(id => loadTab(id)).filter(Boolean) as Tab[];
}

/**
 * 迁移章节分组的 tab（从 legacyKey -> chapterId）
 * 仅在 chapterId 的 tab 为空时使用，避免覆盖正常数据。
 */
export function migrateChapterTabs(legacyKey: string, chapterId: string): Tab[] {
  if (!legacyKey || legacyKey === chapterId) return [];

  try {
    const stored = localStorage.getItem(CHAPTER_TABS_MAP_KEY);
    const map: Record<string, string[]> = stored ? JSON.parse(stored) : {};
    const legacyIds = map[legacyKey] || [];
    if (legacyIds.length === 0) return [];

    const existing = new Set(map[chapterId] || []);
    const mergedIds = [...existing, ...legacyIds.filter((id) => !existing.has(id))];
    map[chapterId] = mergedIds;
    delete map[legacyKey];
    safeSetItem(CHAPTER_TABS_MAP_KEY, JSON.stringify(map));

    const activeStored = localStorage.getItem(CHAPTER_ACTIVE_TAB_KEY);
    const activeMap: Record<string, string> = activeStored ? JSON.parse(activeStored) : {};
    if (!activeMap[chapterId] && activeMap[legacyKey]) {
      activeMap[chapterId] = activeMap[legacyKey];
    }
    delete activeMap[legacyKey];
    safeSetItem(CHAPTER_ACTIVE_TAB_KEY, JSON.stringify(activeMap));

    return mergedIds.map((id) => loadTab(id)).filter(Boolean) as Tab[];
  } catch (error) {
    console.error('[TabStorage] Failed to migrate chapter tabs:', error);
    return [];
  }
}

function loadConversationSession(sessionId: string): ConversationSessionSnapshot | null {
  try {
    const stored = localStorage.getItem(`${SESSION_KEY_PREFIX}${sessionId}`);
    if (!stored) return null;
    const session = JSON.parse(stored) as ConversationSessionSnapshot;
    if (!session?.id) return null;
    return session;
  } catch (error) {
    console.error('[TabStorage] Failed to load conversation session:', error);
    return null;
  }
}

function getStoredTabsByChapter(chapterId: string): Tab[] {
  if (typeof window === 'undefined') return [];
  const tabs: Tab[] = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (!key || !key.startsWith(TAB_PREFIX)) continue;
    try {
      const raw = localStorage.getItem(key);
      if (!raw) continue;
      const tab = JSON.parse(raw) as Tab;
      if (tab?.chapterId === chapterId) {
        tabs.push(tab);
      }
    } catch (error) {
      console.warn('[TabStorage] Failed to parse tab:', key, error);
    }
  }
  const unique = new Map<string, Tab>();
  tabs.forEach((tab) => unique.set(tab.id, tab));
  return Array.from(unique.values());
}

function sortByUpdatedAtDesc<T extends { updatedAt?: string; createdAt?: string }>(items: T[]): T[] {
  return [...items].sort((a, b) => {
    const aTime = new Date(a.updatedAt || a.createdAt || 0).getTime();
    const bTime = new Date(b.updatedAt || b.createdAt || 0).getTime();
    return bTime - aTime;
  });
}

export function recoverChapterTabsFromStorage(chapterId: string): Tab[] {
  if (!chapterId) return [];
  try {
    const storedTabs = sortByUpdatedAtDesc(getStoredTabsByChapter(chapterId));
    if (storedTabs.length === 0) return [];

    const stored = localStorage.getItem(CHAPTER_TABS_MAP_KEY);
    const map: Record<string, string[]> = stored ? JSON.parse(stored) : {};
    map[chapterId] = dedupeIds(storedTabs.map((t) => t.id));
    safeSetItem(CHAPTER_TABS_MAP_KEY, JSON.stringify(map));

    const activeStored = localStorage.getItem(CHAPTER_ACTIVE_TAB_KEY);
    const activeMap: Record<string, string> = activeStored ? JSON.parse(activeStored) : {};
    const hasValidActive = activeMap[chapterId] && storedTabs.some((t) => t.id === activeMap[chapterId]);
    if (!hasValidActive) {
      activeMap[chapterId] = storedTabs[0].id;
      safeSetItem(CHAPTER_ACTIVE_TAB_KEY, JSON.stringify(activeMap));
    }

    return storedTabs;
  } catch (error) {
    console.error('[TabStorage] Failed to recover chapter tabs:', error);
    return [];
  }
}

export function rebuildChapterTabsFromSessions(chapterId: string): Tab[] {
  if (!chapterId) return [];

  try {
    const candidates = new Map<string, ConversationSessionSnapshot>();
    const mapStr = localStorage.getItem(CONTEXT_SESSION_MAP_KEY);
    const contextMap: Record<string, string> = mapStr ? JSON.parse(mapStr) : {};
    const contextId = contextMap[`chapter_${chapterId}`];
    if (contextId) {
      const session = loadConversationSession(contextId);
      if (session) candidates.set(session.id, session);
    }

    const listStr = localStorage.getItem(SESSIONS_LIST_KEY);
    const listIds: string[] = listStr ? JSON.parse(listStr) : [];
    listIds.forEach((id) => {
      if (candidates.has(id)) return;
      const session = loadConversationSession(id);
      if (session) candidates.set(id, session);
    });

    const matched = sortByUpdatedAtDesc(
      Array.from(candidates.values()).filter((session) => session.chapterId === chapterId)
    );
    if (matched.length === 0) return [];

    const session = matched[0];
    const now = new Date().toISOString();
    const createdAt = session.createdAt || session.updatedAt || now;
    const updatedAt = session.updatedAt || createdAt;
    const tab: Tab = {
      id: `tab_recover_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
      chapterId,
      title: session.title || DEFAULT_TAB_TITLE,
      sessionId: session.id,
      conversationId: session.conversationId || session.id,
      createdAt,
      updatedAt
    };

    saveTab(tab);
    addTabToChapter(chapterId, tab.id);
    saveChapterActiveTab(chapterId, tab.id);
    return [tab];
  } catch (error) {
    console.error('[TabStorage] Failed to rebuild tabs from sessions:', error);
    return [];
  }
}

/**
 * 添加标签页到章节
 */
export function addTabToChapter(chapterId: string, tabId: string): void {
  try {
    const stored = localStorage.getItem(CHAPTER_TABS_MAP_KEY);
    const map: Record<string, string[]> = stored ? JSON.parse(stored) : {};

    if (!map[chapterId]) {
      map[chapterId] = [];
    }

    if (!map[chapterId].includes(tabId)) {
      map[chapterId].push(tabId);
    }

    safeSetItem(CHAPTER_TABS_MAP_KEY, JSON.stringify(map));
  } catch (error) {
    console.error('[TabStorage] Failed to add tab to chapter:', error);
  }
}

/**
 * 在指定标签页后插入新标签页
 */
export function insertTabAfter(chapterId: string, newTabId: string, afterTabId: string): void {
  try {
    const stored = localStorage.getItem(CHAPTER_TABS_MAP_KEY);
    const map: Record<string, string[]> = stored ? JSON.parse(stored) : {};

    if (!map[chapterId]) {
      map[chapterId] = [];
    }

    // 先去重，避免重复插入同一个 tabId
    map[chapterId] = map[chapterId].filter((id) => id !== newTabId);

    const index = map[chapterId].indexOf(afterTabId);
    if (index === -1) {
      map[chapterId].push(newTabId);
    } else {
      map[chapterId].splice(index + 1, 0, newTabId);
    }

    safeSetItem(CHAPTER_TABS_MAP_KEY, JSON.stringify(map));
  } catch (error) {
    console.error('[TabStorage] Failed to insert tab:', error);
  }
}

/**
 * 从章节移除标签页
 */
export function removeTabFromChapter(chapterId: string, tabId: string): void {
  try {
    const stored = localStorage.getItem(CHAPTER_TABS_MAP_KEY);
    const map: Record<string, string[]> = stored ? JSON.parse(stored) : {};

    if (map[chapterId]) {
      map[chapterId] = map[chapterId].filter(id => id !== tabId);
    }

    safeSetItem(CHAPTER_TABS_MAP_KEY, JSON.stringify(map));
  } catch (error) {
    console.error('[TabStorage] Failed to remove tab from chapter:', error);
  }
}

/**
 * 获取章节的激活标签页ID
 */
export function getChapterActiveTab(chapterId: string): string | null {
  try {
    const stored = localStorage.getItem(CHAPTER_ACTIVE_TAB_KEY);
    const map: Record<string, string> = stored ? JSON.parse(stored) : {};
    return map[chapterId] || null;
  } catch (error) {
    console.error('[TabStorage] Failed to get active tab:', error);
    return null;
  }
}

/**
 * 保存章节的激活标签页ID
 */
export function saveChapterActiveTab(chapterId: string, tabId: string): void {
  try {
    const stored = localStorage.getItem(CHAPTER_ACTIVE_TAB_KEY);
    const map: Record<string, string> = stored ? JSON.parse(stored) : {};
    map[chapterId] = tabId;
    safeSetItem(CHAPTER_ACTIVE_TAB_KEY, JSON.stringify(map));
  } catch (error) {
    console.error('[TabStorage] Failed to save active tab:', error);
  }
}
