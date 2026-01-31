import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

const MAX_LAST_CHAPTER_ENTRIES = 200;
const MAX_BOOKSHELF_ENTRIES = 200;

const trimRecord = <T>(
  record: Record<string, T>,
  maxEntries: number,
  isValid: (entry: [string, T]) => boolean
) => {
  const entries = Object.entries(record).filter(isValid);
  if (entries.length <= maxEntries) {
    return Object.fromEntries(entries) as Record<string, T>;
  }
  return Object.fromEntries(entries.slice(entries.length - maxEntries)) as Record<string, T>;
};

const updateBoundedRecord = <T>(
  record: Record<string, T>,
  key: string,
  value: T,
  maxEntries: number,
  isValid: (entry: [string, T]) => boolean
) => {
  const next = { ...record };
  if (key in next) {
    delete next[key];
  }
  next[key] = value;
  return trimRecord(next, maxEntries, isValid);
};

const isQuotaExceeded = (error: unknown) => {
  if (!error || typeof error !== 'object') return false;
  const name = (error as { name?: string }).name;
  return name === 'QuotaExceededError' || name === 'NS_ERROR_DOM_QUOTA_REACHED';
};

const safeStorage = {
  getItem: (name: string) => localStorage.getItem(name),
  setItem: (name: string, value: string) => {
    try {
      localStorage.setItem(name, value);
    } catch (error) {
      if (isQuotaExceeded(error)) {
        try {
          localStorage.removeItem(name);
          localStorage.setItem(name, value);
          return;
        } catch (retryError) {
          console.error('[workNavStore] localStorage 配额不足，已跳过写入:', retryError);
          return;
        }
      }
      console.error('[workNavStore] localStorage 写入失败:', error);
    }
  },
  removeItem: (name: string) => localStorage.removeItem(name),
};

// 阅读状态（用于从阅读器返回时恢复）
interface ReadingState {
  novelId: string;
  isReading: boolean;  // 是否在阅读器中
}

// 小说广场浏览状态（用于保持分页和筛选）
interface NovelSquareBrowseState {
  page: number;
  category: string;
  status: string;
  sort: string;
  searchQuery: string;
}

// 验证浏览状态是否有效
const isValidBrowseState = (state: any): state is NovelSquareBrowseState => {
  if (!state || typeof state !== 'object') return false;
  return (
    typeof state.page === 'number' &&
    state.page >= 1 &&
    typeof state.category === 'string' &&
    typeof state.status === 'string' &&
    typeof state.sort === 'string' &&
    typeof state.searchQuery === 'string'
  );
};

// 验证阅读状态是否有效
const isValidReadingState = (state: any): state is ReadingState => {
  if (!state || typeof state !== 'object') return false;
  return (
    typeof state.novelId === 'string' &&
    state.novelId.length > 0 &&
    typeof state.isReading === 'boolean'
  );
};

interface WorkNavState {
  lastWorkId: string | null;
  lastWorkTitle: string | null;
  lastWorkPath: string | null;
  // 存储每个作品的最后阅读章节ID { workId: chapterId }
  lastChapterMap: Record<string, string>;
  // 小说广场的阅读状态（独立）
  novelSquareReadingState: ReadingState | null;
  // 我的书架的阅读状态（独立）
  bookshelfReadingState: ReadingState | null;
  // 小说广场的浏览状态（页码、筛选等）
  novelSquareBrowseState: NovelSquareBrowseState | null;
  // 存储用户书架状态 { workId: boolean } - 用于持久化红心状态
  bookshelfMap: Record<string, boolean>;
  // 标记持久化是否完成（用于等待 hydration）
  hasHydrated: boolean;
  setLastWork: (workId: string, title?: string | null) => void;
  clearLastWork: () => void;
  // 保存某个作品的最后阅读章节
  setLastChapter: (workId: string, chapterId: string) => void;
  // 获取某个作品的最后阅读章节
  getLastChapter: (workId: string) => string | null;
  // 清除某个作品的阅读记录
  clearLastChapter: (workId: string) => void;
  // 设置小说广场阅读状态
  setNovelSquareReadingState: (novelId: string, isReading: boolean) => void;
  // 清除小说广场阅读状态
  clearNovelSquareReadingState: () => void;
  // 设置书架阅读状态
  setBookshelfReadingState: (novelId: string, isReading: boolean) => void;
  // 清除书架阅读状态
  clearBookshelfReadingState: () => void;
  // 设置小说广场浏览状态
  setNovelSquareBrowseState: (state: NovelSquareBrowseState) => void;
  // 清除小说广场浏览状态
  clearNovelSquareBrowseState: () => void;
  // 设置书架状态（加入/移出书架）
  setBookshelfStatus: (workId: string, inBookshelf: boolean) => void;
  // 获取书架状态
  getBookshelfStatus: (workId: string) => boolean;
  // 清除书架状态（用于从书架移除时）
  removeFromBookshelfMap: (workId: string) => void;
  // 设置持久化完成标记
  setHasHydrated: (value: boolean) => void;
}

/**
 * 保存最近访问的作品详情，用于侧边栏动态导航。
 * 同时保存每个作品的最后阅读章节，用于返回时恢复阅读位置。
 * 小说广场和我的书架的阅读状态独立管理。
 */
export const useWorkNavStore = create<WorkNavState>()(
  persist(
    (set, get) => ({
      lastWorkId: null,
      lastWorkTitle: null,
      lastWorkPath: null,
      lastChapterMap: {},
      novelSquareReadingState: null,
      bookshelfReadingState: null,
      novelSquareBrowseState: null,
      bookshelfMap: {},
      hasHydrated: false,
      setLastWork: (workId, title = null) => {
        set({
          lastWorkId: workId,
          lastWorkTitle: title,
          lastWorkPath: workId ? `/works/${workId}` : null,
        });
      },
      clearLastWork: () =>
        set({
          lastWorkId: null,
          lastWorkTitle: null,
          lastWorkPath: null,
        }),
      setLastChapter: (workId, chapterId) => {
        set((state) => ({
          lastChapterMap: updateBoundedRecord(
            state.lastChapterMap,
            workId,
            chapterId,
            MAX_LAST_CHAPTER_ENTRIES,
            ([key, value]) => typeof key === 'string' && typeof value === 'string' && value.length > 0
          ),
        }));
      },
      getLastChapter: (workId) => {
        return get().lastChapterMap[workId] || null;
      },
      clearLastChapter: (workId) => {
        set((state) => {
          const newMap = { ...state.lastChapterMap };
          delete newMap[workId];
          return { lastChapterMap: newMap };
        });
      },
      setNovelSquareReadingState: (novelId, isReading) => {
        set({
          novelSquareReadingState: { novelId, isReading },
        });
      },
      clearNovelSquareReadingState: () => {
        set({ novelSquareReadingState: null });
      },
      setBookshelfReadingState: (novelId, isReading) => {
        set({
          bookshelfReadingState: { novelId, isReading },
        });
      },
      clearBookshelfReadingState: () => {
        set({ bookshelfReadingState: null });
      },
      setNovelSquareBrowseState: (browseState) => {
        console.log('[workNavStore] 保存浏览状态:', JSON.stringify(browseState));
        set({ novelSquareBrowseState: browseState });
      },
      clearNovelSquareBrowseState: () => {
        set({ novelSquareBrowseState: null });
      },
      setBookshelfStatus: (workId, inBookshelf) => {
        set((state) => {
          if (!inBookshelf) {
            const next = { ...state.bookshelfMap };
            delete next[workId];
            return { bookshelfMap: next };
          }
          return {
            bookshelfMap: updateBoundedRecord(
              state.bookshelfMap,
              workId,
              inBookshelf,
              MAX_BOOKSHELF_ENTRIES,
              ([key, value]) => typeof key === 'string' && typeof value === 'boolean'
            ),
          };
        });
      },
      getBookshelfStatus: (workId) => {
        return get().bookshelfMap[workId] || false;
      },
      removeFromBookshelfMap: (workId) => {
        set((state) => {
          const newMap = { ...state.bookshelfMap };
          delete newMap[workId];
          return { bookshelfMap: newMap };
        });
      },
      setHasHydrated: (value) => {
        set({ hasHydrated: value });
      },
    }),
    {
      name: 'work-nav-storage', // localStorage 的 key
      storage: createJSONStorage(() => safeStorage),
      partialize: (state) => ({
        // 持久化章节记录、阅读状态、浏览状态和书架状态
        lastChapterMap: trimRecord(
          state.lastChapterMap,
          MAX_LAST_CHAPTER_ENTRIES,
          ([key, value]) => typeof key === 'string' && typeof value === 'string' && value.length > 0
        ),
        novelSquareReadingState: state.novelSquareReadingState,
        bookshelfReadingState: state.bookshelfReadingState,
        novelSquareBrowseState: state.novelSquareBrowseState,
        bookshelfMap: trimRecord(
          state.bookshelfMap,
          MAX_BOOKSHELF_ENTRIES,
          ([key, value]) => typeof key === 'string' && typeof value === 'boolean'
        ),
      }),
      // 合并时验证数据有效性，避免损坏的数据导致问题
      merge: (persistedState: any, currentState) => {
        const merged = { ...currentState };

        if (persistedState && typeof persistedState === 'object') {
          // 验证并合并章节记录
          if (persistedState.lastChapterMap && typeof persistedState.lastChapterMap === 'object') {
            merged.lastChapterMap = trimRecord(
              persistedState.lastChapterMap,
              MAX_LAST_CHAPTER_ENTRIES,
              ([key, value]) => typeof key === 'string' && typeof value === 'string' && value.length > 0
            );
          }

          // 验证并合并阅读状态
          if (isValidReadingState(persistedState.novelSquareReadingState)) {
            merged.novelSquareReadingState = persistedState.novelSquareReadingState;
          }
          if (isValidReadingState(persistedState.bookshelfReadingState)) {
            merged.bookshelfReadingState = persistedState.bookshelfReadingState;
          }

          // 验证并合并浏览状态
          if (isValidBrowseState(persistedState.novelSquareBrowseState)) {
            merged.novelSquareBrowseState = persistedState.novelSquareBrowseState;
          }

          // 验证并合并书架状态
          if (persistedState.bookshelfMap && typeof persistedState.bookshelfMap === 'object') {
            merged.bookshelfMap = trimRecord(
              persistedState.bookshelfMap,
              MAX_BOOKSHELF_ENTRIES,
              ([key, value]) => typeof key === 'string' && typeof value === 'boolean'
            );
          }
        }

        return merged as WorkNavState;
      },
      // rehydration 完成后设置标记
      onRehydrateStorage: () => {
        console.log('[workNavStore] 开始 rehydration...');
        return (state, error) => {
          if (error) {
            console.error('[workNavStore] rehydration 失败:', error);
          } else {
            console.log('[workNavStore] rehydration 完成，novelSquareBrowseState:', JSON.stringify(state?.novelSquareBrowseState));
          }
          state?.setHasHydrated?.(true);
        };
      },
    }
  )
);
