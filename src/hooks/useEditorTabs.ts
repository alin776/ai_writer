/**
 * useEditorTabs — 编辑器多标签页状态管理
 *
 * 管理打开的章节标签、激活标签、切换/关闭，并通过 localStorage 持久化。
 */
import { useState, useCallback, useEffect, useRef } from 'react';

export interface EditorTab {
  id: string;       // chapterId
  title: string;    // 章节标题
  order: number;    // 章节序号
}

interface ChapterLike {
  id: string;
  title: string;
  order: number;
}

const STORAGE_PREFIX = 'editor_tabs_';

function loadTabs(workId: string): { tabs: EditorTab[]; activeId: string | null } {
  try {
    const raw = localStorage.getItem(STORAGE_PREFIX + workId);
    if (!raw) return { tabs: [], activeId: null };
    const parsed = JSON.parse(raw);
    return {
      tabs: Array.isArray(parsed.tabs) ? parsed.tabs : [],
      activeId: parsed.activeId ?? null,
    };
  } catch {
    return { tabs: [], activeId: null };
  }
}

function saveTabs(workId: string, tabs: EditorTab[], activeId: string | null) {
  try {
    localStorage.setItem(STORAGE_PREFIX + workId, JSON.stringify({ tabs, activeId }));
  } catch { /* quota exceeded, silently ignore */ }
}

export function useEditorTabs(workId: string, chapters: ChapterLike[]) {
  const [openTabs, setOpenTabs] = useState<EditorTab[]>([]);
  const [activeTabId, setActiveTabId] = useState<string | null>(null);
  const initializedRef = useRef(false);

  // 初始化：从 localStorage 恢复标签
  useEffect(() => {
    if (!workId) return;
    const { tabs, activeId } = loadTabs(workId);
    if (tabs.length > 0) {
      setOpenTabs(tabs);
      setActiveTabId(activeId);
    }
    initializedRef.current = true;
  }, [workId]);

  // 持久化：tabs 或 activeTabId 变化时保存
  useEffect(() => {
    if (!workId || !initializedRef.current) return;
    saveTabs(workId, openTabs, activeTabId);
  }, [workId, openTabs, activeTabId]);

  // 监听 chapters 变化，移除已删除章节的标签
  useEffect(() => {
    if (!initializedRef.current || chapters.length === 0) return;
    const chapterIds = new Set(chapters.map(c => c.id));
    setOpenTabs(prev => {
      const filtered = prev.filter(tab => chapterIds.has(tab.id));
      if (filtered.length === prev.length) return prev; // 无变化
      return filtered;
    });
    setActiveTabId(prev => {
      if (prev && !chapterIds.has(prev)) {
        // 激活标签被删除，切换到最后一个标签
        return null; // 将在 openTab 时重新设定
      }
      return prev;
    });
  }, [chapters]);

  // 打开标签（如已存在则切换）
  const openTab = useCallback((chapter: ChapterLike) => {
    setOpenTabs(prev => {
      const exists = prev.find(t => t.id === chapter.id);
      if (exists) return prev;
      return [...prev, { id: chapter.id, title: chapter.title, order: chapter.order }];
    });
    setActiveTabId(chapter.id);
  }, []);

  // 关闭标签
  const closeTab = useCallback((tabId: string) => {
    setOpenTabs(prev => {
      const idx = prev.findIndex(t => t.id === tabId);
      if (idx === -1) return prev;
      const next = prev.filter(t => t.id !== tabId);
      // 如果关闭的是激活标签，切换到相邻标签
      setActiveTabId(current => {
        if (current !== tabId) return current;
        if (next.length === 0) return null;
        // 优先切换到右侧标签，否则左侧
        const newIdx = Math.min(idx, next.length - 1);
        return next[newIdx].id;
      });
      return next;
    });
  }, []);

  // 切换标签
  const switchTab = useCallback((tabId: string) => {
    setActiveTabId(tabId);
  }, []);

  // 更新标签标题（章节重命名时调用）
  const updateTabTitle = useCallback((chapterId: string, newTitle: string, newOrder?: number) => {
    setOpenTabs(prev =>
      prev.map(tab =>
        tab.id === chapterId
          ? { ...tab, title: newTitle, order: newOrder ?? tab.order }
          : tab
      )
    );
  }, []);

  return {
    openTabs,
    activeTabId,
    openTab,
    closeTab,
    switchTab,
    updateTabTitle,
  };
}
