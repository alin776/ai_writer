import { create } from 'zustand';
import { persist } from 'zustand/middleware';

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
          lastChapterMap: {
            ...state.lastChapterMap,
            [workId]: chapterId,
          },
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
        set({ novelSquareBrowseState: browseState });
      },
      clearNovelSquareBrowseState: () => {
        set({ novelSquareBrowseState: null });
      },
      setBookshelfStatus: (workId, inBookshelf) => {
        set((state) => ({
          bookshelfMap: {
            ...state.bookshelfMap,
            [workId]: inBookshelf,
          },
        }));
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
    }),
    {
      name: 'work-nav-storage', // localStorage 的 key
      partialize: (state) => ({
        // 持久化章节记录、阅读状态、浏览状态和书架状态
        lastChapterMap: state.lastChapterMap,
        novelSquareReadingState: state.novelSquareReadingState,
        bookshelfReadingState: state.bookshelfReadingState,
        novelSquareBrowseState: state.novelSquareBrowseState,
        bookshelfMap: state.bookshelfMap,
      }),
    }
  )
);
