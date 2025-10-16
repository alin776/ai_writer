import { create } from 'zustand';
import type { Chapter } from '@/types';

/**
 * 编辑器状态接口
 */
interface EditorState {
  // 状态
  currentChapter: Chapter | null;
  isSaving: boolean;
  isAiSidebarOpen: boolean;
  lastSavedAt: Date | null;
  isDirty: boolean; // 是否有未保存的更改

  // 方法
  /**
   * 设置当前编辑的章节
   * @param chapter 章节信息
   */
  setCurrentChapter: (chapter: Chapter | null) => void;

  /**
   * 设置保存状态
   * @param isSaving 是否正在保存
   */
  setIsSaving: (isSaving: boolean) => void;

  /**
   * 切换 AI 侧边栏显示状态
   */
  toggleAiSidebar: () => void;

  /**
   * 设置 AI 侧边栏显示状态
   * @param isOpen 是否打开
   */
  setAiSidebarOpen: (isOpen: boolean) => void;

  /**
   * 更新最后保存时间
   */
  updateLastSavedAt: () => void;

  /**
   * 设置内容是否已修改
   * @param isDirty 是否有未保存的更改
   */
  setDirty: (isDirty: boolean) => void;

  /**
   * 更新章节内容（不保存到服务器）
   * @param content 新内容
   */
  updateChapterContent: (content: string) => void;

  /**
   * 重置编辑器状态
   */
  reset: () => void;
}

/**
 * 编辑器状态管理 Store
 * 管理编辑器相关的所有状态
 */
export const useEditorStore = create<EditorState>((set) => ({
  // 初始状态
  currentChapter: null,
  isSaving: false,
  isAiSidebarOpen: false,
  lastSavedAt: null,
  isDirty: false,

  // 设置当前章节
  setCurrentChapter: (chapter: Chapter | null) => {
    set({
      currentChapter: chapter,
      isDirty: false,
      lastSavedAt: null,
    });
  },

  // 设置保存状态
  setIsSaving: (isSaving: boolean) => {
    set({ isSaving });
  },

  // 切换 AI 侧边栏
  toggleAiSidebar: () => {
    set((state) => ({
      isAiSidebarOpen: !state.isAiSidebarOpen,
    }));
  },

  // 设置 AI 侧边栏状态
  setAiSidebarOpen: (isOpen: boolean) => {
    set({ isAiSidebarOpen: isOpen });
  },

  // 更新最后保存时间
  updateLastSavedAt: () => {
    set({
      lastSavedAt: new Date(),
      isDirty: false,
    });
  },

  // 设置修改状态
  setDirty: (isDirty: boolean) => {
    set({ isDirty });
  },

  // 更新章节内容
  updateChapterContent: (content: string) => {
    set((state) => {
      if (!state.currentChapter) return state;

      // 计算字数（移除空格和标点符号）
      const wordCount = content.replace(/[\s\p{P}]/gu, '').length;

      return {
        currentChapter: {
          ...state.currentChapter,
          content,
          wordCount,
          updateTime: new Date().toISOString(),
        },
        isDirty: true,
      };
    });
  },

  // 重置编辑器
  reset: () => {
    set({
      currentChapter: null,
      isSaving: false,
      isAiSidebarOpen: false,
      lastSavedAt: null,
      isDirty: false,
    });
  },
}));
