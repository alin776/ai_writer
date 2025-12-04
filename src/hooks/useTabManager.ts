import { useCallback, useEffect, useState } from 'react';
import {
  Tab,
  addTabToChapter,
  deleteTab,
  getChapterActiveTab,
  getChapterTabs,
  insertTabAfter,
  loadTab,
  removeTabFromChapter,
  saveChapterActiveTab,
  saveTab
} from '@/utils/tabStorage';

interface UseTabManagerReturn {
  tabs: Tab[];
  activeTabId: string;
  createTab: (afterTabId?: string) => Tab;
  closeTab: (tabId: string) => void;
  switchTab: (tabId: string) => void;
  updateTabTitle: (tabId: string, title: string) => void;
}

const DEFAULT_TITLE = '新会话';

/**
 * Manage per-chapter chat tabs with localStorage persistence.
 */
export function useTabManager(chapterId: string): UseTabManagerReturn {
  const resolvedChapterId = chapterId || 'default';
  const [tabs, setTabs] = useState<Tab[]>([]);
  const [activeTabId, setActiveTabId] = useState<string>('');

  const createNewTab = useCallback((): Tab => {
    const timestamp = Date.now();
    const random = Math.random().toString(36).slice(2, 9);
    const newTab: Tab = {
      id: `tab_${timestamp}_${random}`,
      chapterId: resolvedChapterId,
      title: DEFAULT_TITLE,
      sessionId: `session_${timestamp}_${random}`,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    saveTab(newTab);
    addTabToChapter(resolvedChapterId, newTab.id);
    return newTab;
  }, [resolvedChapterId]);

  // Load tabs for the chapter and bootstrap a first tab when empty.
  useEffect(() => {
    const chapterTabs = getChapterTabs(resolvedChapterId);

    if (chapterTabs.length === 0) {
      const newTab = createNewTab();
      setTabs([newTab]);
      setActiveTabId(newTab.id);
      saveChapterActiveTab(resolvedChapterId, newTab.id);
      return;
    }

    setTabs(chapterTabs);
    const storedActiveId = getChapterActiveTab(resolvedChapterId);
    const fallbackId = chapterTabs[0].id;
    const activeId =
      storedActiveId && chapterTabs.some((t) => t.id === storedActiveId) ? storedActiveId : fallbackId;
    setActiveTabId(activeId);
    if (activeId !== storedActiveId) {
      saveChapterActiveTab(resolvedChapterId, activeId);
    }
  }, [resolvedChapterId, createNewTab]);

  const createTab = useCallback(
    (afterTabId?: string): Tab => {
      const newTab = createNewTab();

      if (afterTabId) {
        insertTabAfter(resolvedChapterId, newTab.id, afterTabId);
        setTabs(getChapterTabs(resolvedChapterId));
      } else {
        setTabs((prev) => [...prev, newTab]);
      }

      setActiveTabId(newTab.id);
      saveChapterActiveTab(resolvedChapterId, newTab.id);
      return newTab;
    },
    [createNewTab, resolvedChapterId]
  );

  const closeTab = useCallback(
    (tabId: string) => {
      if (tabs.length <= 1) {
        console.warn('[TabManager] at least one tab must remain');
        return;
      }

      deleteTab(tabId);
      removeTabFromChapter(resolvedChapterId, tabId);

      if (tabId === activeTabId) {
        const index = tabs.findIndex((t) => t.id === tabId);
        const nextTab = tabs[index + 1] || tabs[index - 1];
        if (nextTab) {
          setActiveTabId(nextTab.id);
          saveChapterActiveTab(resolvedChapterId, nextTab.id);
        }
      }

      setTabs((prev) => prev.filter((t) => t.id !== tabId));
    },
    [activeTabId, resolvedChapterId, tabs]
  );

  const switchTab = useCallback(
    (tabId: string) => {
      setActiveTabId(tabId);
      saveChapterActiveTab(resolvedChapterId, tabId);
    },
    [resolvedChapterId]
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

  return {
    tabs,
    activeTabId,
    createTab,
    closeTab,
    switchTab,
    updateTabTitle
  };
}
