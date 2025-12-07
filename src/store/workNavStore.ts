import { create } from 'zustand';

interface WorkNavState {
  lastWorkId: string | null;
  lastWorkTitle: string | null;
  lastWorkPath: string | null;
  setLastWork: (workId: string, title?: string | null) => void;
  clearLastWork: () => void;
}

/**
 * 保存最近访问的作品详情，用于侧边栏动态导航。
 */
export const useWorkNavStore = create<WorkNavState>((set) => ({
  lastWorkId: null,
  lastWorkTitle: null,
  lastWorkPath: null,
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
}));
