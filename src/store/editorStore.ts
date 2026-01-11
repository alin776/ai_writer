import { create } from 'zustand';
import type { Chapter } from '@/types';
import { countWordsInHtml } from '@/utils/wordCount';

/**
 * 右侧面板类型
 */
export type RightSidebarType = 'worldview' | 'agent' | null;

/**
 * 编辑器状态接口
 */
interface EditorState {
  // 状态
  currentChapter: Chapter | null;
  isSaving: boolean;
  isAiSidebarOpen: boolean; // 已废弃，保留以兼容旧代码
  rightSidebarType: RightSidebarType; // 右侧面板类型
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
   * 设置右侧面板类型
   * @param type 面板类型
   */
  setRightSidebarType: (type: RightSidebarType) => void;

  /**
   * 切换右侧面板
   * @param type 面板类型
   * 如果未打开则打开，如果已打开相同面板则保持，如果打开其他面板则切换
   */
  toggleRightSidebar: (type: RightSidebarType) => void;

  /**
   * 关闭右侧面板
   */
  closeRightSidebar: () => void;

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
  isAiSidebarOpen: false, // 已废弃
  rightSidebarType: null, // 右侧面板默认关闭
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

  // 设置右侧面板类型
  setRightSidebarType: (type: RightSidebarType) => {
    set({ rightSidebarType: type });
  },

  // 切换右侧面板
  toggleRightSidebar: (type: RightSidebarType) => {
    set((state) => {
      // 如果点击的是当前已打开的面板，关闭它
      if (state.rightSidebarType === type) {
        return { rightSidebarType: null };
      }
      // 否则切换到新面板（或打开面板）
      return { rightSidebarType: type };
    });
  },

  // 关闭右侧面板
  closeRightSidebar: () => {
    set({ rightSidebarType: null });
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

      // 使用统一的字数统计算法（与后端一致）
      const wordCount = countWordsInHtml(content);

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
      rightSidebarType: null, // 重置右侧面板
      lastSavedAt: null,
      isDirty: false,
    });
  },
}));
