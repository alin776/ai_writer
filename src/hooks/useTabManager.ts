import { useCallback, useEffect, useState } from 'react';
import { agentApi } from '@/services/agentApi';
import {
  Tab,
  addTabToChapter,
  deleteTab,
  getChapterActiveTab,
  getChapterTabs,
  insertTabAfter,
  loadTab,
  migrateChapterTabs,
  removeTabFromChapter,
  rebuildChapterTabsFromSessions,
  recoverChapterTabsFromStorage,
  saveChapterActiveTab,
  saveTab
} from '@/utils/tabStorage';

interface UseTabManagerReturn {
  tabs: Tab[];
  activeTabId: string;
  isReady: boolean;
  createTab: (afterTabId?: string) => Promise<Tab>;
  closeTab: (tabId: string) => void;
  switchTab: (tabId: string) => void;
  updateTabTitle: (tabId: string, title: string) => void;
  replaceTabSession: (tabId: string, sessionId: string, title?: string, conversationId?: string) => void;
  attachSessionTab: (sessionId: string, title?: string, conversationId?: string) => Tab;
}

const DEFAULT_TITLE = '新会话';

/**
 * Manage per-chapter chat tabs with localStorage persistence.
 */
export function useTabManager(chapterId: string, workId?: string): UseTabManagerReturn {
  const resolvedChapterId = chapterId || '';
  // fs-N 格式的 chapterId 跨作品重复，加 workId 前缀做存储隔离
  // UUID 格式天然唯一，无需前缀，保持向后兼容
  const storageChapterId =
    workId && resolvedChapterId.startsWith('fs-')
      ? `${workId}:${resolvedChapterId}`
      : resolvedChapterId;
  const isReady = Boolean(resolvedChapterId);
  const [tabs, setTabs] = useState<Tab[]>([]);
  const [activeTabId, setActiveTabId] = useState<string>('');

  const createNewTab = useCallback(async (): Promise<Tab> => {
    if (!isReady) {
      throw new Error('[TabManager] chapterId not ready');
    }
    const timestamp = Date.now();
    const random = Math.random().toString(36).slice(2, 9);
    const now = new Date().toISOString();

    let sessionId = `session_${timestamp}_${random}`;
    let conversationId: string | undefined;
    let title = DEFAULT_TITLE;
    let createdAt = now;

    try {
      const resp = await agentApi.createSession({
        title: DEFAULT_TITLE,
        work_id: workId,
        chapter_id: undefined,  // 会话与作品绑定，不绑章节
        conversation_id: sessionId
      });
      sessionId = resp.session_id || sessionId;
      conversationId = resp.conversation_id;
      title = resp.title || title;
      createdAt = resp.created_at || now;
    } catch (error) {
      console.warn('[TabManager] createSession failed, fallback to local tab only:', error);
    }

    const newTab: Tab = {
      id: `tab_${timestamp}_${random}`,
      chapterId: storageChapterId,
      title,
      sessionId,
      conversationId: conversationId || sessionId,
      createdAt,
      updatedAt: createdAt
    };

    saveTab(newTab);
    addTabToChapter(storageChapterId, newTab.id);
    return newTab;
  }, [isReady, resolvedChapterId, storageChapterId, workId]);

  // Load tabs for the chapter and bootstrap a first tab when empty.
  useEffect(() => {
    let mounted = true;

    const bootstrap = async () => {
      if (!isReady) {
        if (!mounted) return;
        setTabs([]);
        setActiveTabId('');
        return;
      }
      let chapterTabs = getChapterTabs(storageChapterId);

      if (chapterTabs.length === 0) {
        const recovered = recoverChapterTabsFromStorage(storageChapterId);
        if (recovered.length > 0) {
          chapterTabs = recovered;
        }
      }

      if (chapterTabs.length === 0 && workId) {
        const migrated = migrateChapterTabs(workId, storageChapterId);
        if (migrated.length > 0) {
          chapterTabs = migrated;
        }
      }

      if (chapterTabs.length === 0) {
        const rebuilt = rebuildChapterTabsFromSessions(storageChapterId);
        if (rebuilt.length > 0) {
          chapterTabs = rebuilt;
        }
      }

      if (chapterTabs.length === 0) {
        const newTab = await createNewTab();
        if (!mounted) return;
        setTabs([newTab]);
        setActiveTabId(newTab.id);
        saveChapterActiveTab(storageChapterId, newTab.id);
        return;
      }

      if (!mounted) return;
      setTabs(chapterTabs);
      const storedActiveId = getChapterActiveTab(storageChapterId);
      const fallbackId = chapterTabs[0].id;
      const activeId =
        storedActiveId && chapterTabs.some((t) => t.id === storedActiveId) ? storedActiveId : fallbackId;
      setActiveTabId(activeId);
      if (activeId !== storedActiveId) {
        saveChapterActiveTab(storageChapterId, activeId);
      }
    };

    bootstrap();
    return () => {
      mounted = false;
    };
  }, [isReady, storageChapterId, workId, createNewTab]);

  const createTab = useCallback(
    async (afterTabId?: string): Promise<Tab> => {
      if (!isReady) {
        throw new Error('[TabManager] chapterId not ready');
      }
      const newTab = await createNewTab();

      if (afterTabId) {
        insertTabAfter(storageChapterId, newTab.id, afterTabId);
        setTabs(getChapterTabs(storageChapterId));
      } else {
        setTabs((prev) => [...prev, newTab]);
      }

      setActiveTabId(newTab.id);
      saveChapterActiveTab(storageChapterId, newTab.id);
      return newTab;
    },
    [createNewTab, isReady, storageChapterId]
  );

  const refreshTabsFromStorage = useCallback(() => {
    if (!isReady) {
      setTabs([]);
      setActiveTabId('');
      return;
    }
    const storedTabs = getChapterTabs(storageChapterId);
    setTabs(storedTabs);
    const storedActiveId = getChapterActiveTab(storageChapterId);
    if (storedActiveId && storedTabs.some((t) => t.id === storedActiveId)) {
      setActiveTabId(storedActiveId);
    } else if (storedTabs.length > 0) {
      setActiveTabId(storedTabs[0].id);
      saveChapterActiveTab(storageChapterId, storedTabs[0].id);
    }
  }, [isReady, storageChapterId]);

  const closeTab = useCallback(
    (tabId: string) => {
      if (tabs.length <= 1) {
        console.warn('[TabManager] at least one tab must remain');
        return;
      }

      deleteTab(tabId);
      removeTabFromChapter(storageChapterId, tabId);

      if (tabId === activeTabId) {
        const index = tabs.findIndex((t) => t.id === tabId);
        const nextTab = tabs[index + 1] || tabs[index - 1];
        if (nextTab) {
          setActiveTabId(nextTab.id);
          saveChapterActiveTab(storageChapterId, nextTab.id);
        }
      }

      setTabs((prev) => prev.filter((t) => t.id !== tabId));
    },
    [activeTabId, storageChapterId, tabs]
  );

  const switchTab = useCallback(
    (tabId: string) => {
      setActiveTabId(tabId);
      saveChapterActiveTab(storageChapterId, tabId);
    },
    [storageChapterId]
  );

  const updateTabTitle = useCallback((tabId: string, title: string) => {
    const tab = loadTab(tabId);
    if (!tab) return;

    const updatedTab: Tab = {
      ...tab,
      title,
      updatedAt: new Date().toISOString()
    };

    saveTab(updatedTab);
    setTabs((prev) => prev.map((t) => (t.id === tabId ? updatedTab : t)));
  }, []);

  const replaceTabSession = useCallback(
    (tabId: string, newSessionId: string, title?: string, conversationId?: string) => {
      const tab = loadTab(tabId);
      if (!tab) return;

      const updatedTab: Tab = {
        ...tab,
        sessionId: newSessionId,
        conversationId: conversationId || tab.conversationId || newSessionId,
        title: title || tab.title,
        updatedAt: new Date().toISOString()
      };

      saveTab(updatedTab);
      setTabs((prev) => prev.map((t) => (t.id === tabId ? updatedTab : t)));
    },
    []
  );

  const attachSessionTab = useCallback(
    (sessionId: string, title?: string, conversationId?: string): Tab => {
      const existing = tabs.find((t) => t.sessionId === sessionId);
      if (existing) {
        setActiveTabId(existing.id);
        saveChapterActiveTab(storageChapterId, existing.id);
        return existing;
      }

      const now = new Date().toISOString();
      const newTab: Tab = {
        id: `tab_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
        chapterId: storageChapterId,
        title: title || DEFAULT_TITLE,
        sessionId,
        conversationId: conversationId || sessionId,
        createdAt: now,
        updatedAt: now
      };

      saveTab(newTab);
      addTabToChapter(storageChapterId, newTab.id);
      setTabs((prev) => [...prev, newTab]);
      setActiveTabId(newTab.id);
      saveChapterActiveTab(storageChapterId, newTab.id);
      return newTab;
    },
    [storageChapterId, tabs]
  );

  useEffect(() => {
    const handleTabUpdated = () => refreshTabsFromStorage();
    window.addEventListener('agent-tab-updated', handleTabUpdated);
    window.addEventListener('agent-tab-deleted', handleTabUpdated);
    return () => {
      window.removeEventListener('agent-tab-updated', handleTabUpdated);
      window.removeEventListener('agent-tab-deleted', handleTabUpdated);
    };
  }, [refreshTabsFromStorage]);

  return {
    tabs,
    activeTabId,
    isReady,
    createTab,
    closeTab,
    switchTab,
    updateTabTitle,
    replaceTabSession,
    attachSessionTab
  };
}
