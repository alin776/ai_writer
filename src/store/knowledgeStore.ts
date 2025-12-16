import { create } from 'zustand';
import type { KnowledgeItem } from '@/services/knowledgeApi';

// 扩展类型以支持组件使用
type KnowledgeItemExtended = KnowledgeItem & {
  category?: string;
};

interface KnowledgeState {
  // 缓存的数据
  items: KnowledgeItemExtended[];
  // 上次加载的参数（用于判断是否需要重新加载）
  lastSearchQuery: string;
  lastTagFilter: string;
  // 缓存时间戳
  cacheTimestamp: number;
  // 缓存有效期（5分钟）
  cacheMaxAge: number;

  // 方法
  setItems: (items: KnowledgeItemExtended[], searchQuery: string, tagFilter: string) => void;
  getItems: () => KnowledgeItemExtended[];
  shouldRefetch: (searchQuery: string, tagFilter: string) => boolean;
  invalidateCache: () => void;
}

/**
 * 知识库内存缓存 Store
 * 不使用 persist，纯内存缓存，避免 localStorage 的同步阻塞问题
 */
export const useKnowledgeStore = create<KnowledgeState>()((set, get) => ({
  items: [],
  lastSearchQuery: '',
  lastTagFilter: '',
  cacheTimestamp: 0,
  cacheMaxAge: 5 * 60 * 1000, // 5分钟

  setItems: (items, searchQuery, tagFilter) => {
    set({
      items,
      lastSearchQuery: searchQuery,
      lastTagFilter: tagFilter,
      cacheTimestamp: Date.now(),
    });
  },

  getItems: () => get().items,

  shouldRefetch: (searchQuery, tagFilter) => {
    const state = get();
    const now = Date.now();

    // 缓存过期
    if (now - state.cacheTimestamp > state.cacheMaxAge) {
      return true;
    }

    // 查询参数变化
    if (state.lastSearchQuery !== searchQuery || state.lastTagFilter !== tagFilter) {
      return true;
    }

    // 缓存为空
    if (state.items.length === 0 && state.cacheTimestamp === 0) {
      return true;
    }

    return false;
  },

  invalidateCache: () => {
    set({
      items: [],
      cacheTimestamp: 0,
      lastSearchQuery: '',
      lastTagFilter: '',
    });
  },
}));
