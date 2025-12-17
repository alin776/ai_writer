import { create } from 'zustand';

/**
 * 会话草稿数据结构
 */
export interface SessionDraft {
  inputValue: string;
  selectedDocs: Array<{ id: string; title: string }>;
  optimizationSelected: boolean;
  selectionContext: {
    selected_text?: string;
    selected_text_html?: string;
    selection_position?: { from: number; to: number };
  } | null;
}

/**
 * 草稿状态管理接口
 * 按 sessionId 存储，每个会话有独立的草稿
 */
interface ChatDraftState {
  // 按 sessionId 存储的草稿数据
  drafts: Record<string, SessionDraft>;

  /**
   * 保存草稿（支持部分更新）
   * @param sessionId 会话ID
   * @param draft 草稿数据（部分字段）
   */
  saveDraft: (sessionId: string, draft: Partial<SessionDraft>) => void;

  /**
   * 获取草稿
   * @param sessionId 会话ID
   * @returns 草稿数据，不存在则返回 null
   */
  getDraft: (sessionId: string) => SessionDraft | null;

  /**
   * 清除草稿（发送消息后调用）
   * @param sessionId 会话ID
   */
  clearDraft: (sessionId: string) => void;

  /**
   * 清除所有草稿
   */
  clearAllDrafts: () => void;
}

/**
 * 默认草稿值
 */
const DEFAULT_DRAFT: SessionDraft = {
  inputValue: '',
  selectedDocs: [],
  optimizationSelected: false,
  selectionContext: null,
};

/**
 * 聊天草稿状态管理 Store
 * 用于在章节切换时保留用户的输入状态
 * 按 sessionId 存储，因为每个会话是唯一的
 * 注意：不使用 persist 中间件，仅保留当前会话
 */
export const useChatDraftStore = create<ChatDraftState>((set, get) => ({
  drafts: {},

  saveDraft: (sessionId: string, draft: Partial<SessionDraft>) => {
    if (!sessionId) return;

    set((state) => {
      const existing = state.drafts[sessionId] || { ...DEFAULT_DRAFT };
      return {
        drafts: {
          ...state.drafts,
          [sessionId]: {
            ...existing,
            ...draft,
          },
        },
      };
    });
  },

  getDraft: (sessionId: string) => {
    if (!sessionId) return null;
    return get().drafts[sessionId] || null;
  },

  clearDraft: (sessionId: string) => {
    if (!sessionId) return;

    set((state) => {
      const { [sessionId]: _, ...rest } = state.drafts;
      return { drafts: rest };
    });
  },

  clearAllDrafts: () => {
    set({ drafts: {} });
  },
}));
