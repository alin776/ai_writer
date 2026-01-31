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

/**
 * 保存标签页数据
 */
export function saveTab(tab: Tab): void {
  try {
    localStorage.setItem(`${TAB_PREFIX}${tab.id}`, JSON.stringify(tab));
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
      localStorage.setItem(CHAPTER_TABS_MAP_KEY, JSON.stringify(map));
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

    localStorage.setItem(CHAPTER_TABS_MAP_KEY, JSON.stringify(map));
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

    localStorage.setItem(CHAPTER_TABS_MAP_KEY, JSON.stringify(map));
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

    localStorage.setItem(CHAPTER_TABS_MAP_KEY, JSON.stringify(map));
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
    localStorage.setItem(CHAPTER_ACTIVE_TAB_KEY, JSON.stringify(map));
  } catch (error) {
    console.error('[TabStorage] Failed to save active tab:', error);
  }
}
