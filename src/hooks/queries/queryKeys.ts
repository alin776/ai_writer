/**
 * React Query Keys 统一管理
 * 
 * 为什么需要统一管理 Query Keys？
 * 1. 避免拼写错误
 * 2. 方便批量失效缓存
 * 3. 易于维护和重构
 * 4. 支持 TypeScript 类型推导
 * 
 * Query Key 设计原则：
 * - 从通用到具体：['works'] -> ['work', id] -> ['work', id, 'chapters']
 * - 便于模式匹配：invalidateQueries({ queryKey: ['works'] }) 会失效所有相关查询
 */

export const queryKeys = {
  // ==================== 认证相关 ====================
  auth: {
    all: ['auth'] as const,
    currentUser: () => [...queryKeys.auth.all, 'currentUser'] as const,
  },

  // ==================== 作品相关 ====================
  works: {
    all: ['works'] as const,
    lists: () => [...queryKeys.works.all, 'list'] as const,
    list: (filters?: Record<string, any>) => 
      [...queryKeys.works.lists(), filters] as const,
    details: () => [...queryKeys.works.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.works.details(), id] as const,
  },

  // ==================== 章节相关 ====================
  chapters: {
    all: ['chapters'] as const,
    lists: () => [...queryKeys.chapters.all, 'list'] as const,
    list: (workId: string) => 
      [...queryKeys.chapters.lists(), workId] as const,
    details: () => [...queryKeys.chapters.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.chapters.details(), id] as const,
    summary: (id: string) => 
      [...queryKeys.chapters.detail(id), 'summary'] as const,
  },

  // ==================== 世界观相关 ====================
  worldview: {
    all: ['worldview'] as const,
    
    // 完整世界观数据
    worldData: (workId: string) => 
      [...queryKeys.worldview.all, 'worldData', workId] as const,
    
    // 角色
    characters: {
      all: () => [...queryKeys.worldview.all, 'characters'] as const,
      list: (workId: string) => 
        [...queryKeys.worldview.characters.all(), workId] as const,
      detail: (id: string) => 
        [...queryKeys.worldview.characters.all(), 'detail', id] as const,
    },
    
    // 地点
    locations: {
      all: () => [...queryKeys.worldview.all, 'locations'] as const,
      list: (workId: string) => 
        [...queryKeys.worldview.locations.all(), workId] as const,
      detail: (id: string) => 
        [...queryKeys.worldview.locations.all(), 'detail', id] as const,
    },
    
    // 设定
    settings: {
      all: () => [...queryKeys.worldview.all, 'settings'] as const,
      list: (workId: string) => 
        [...queryKeys.worldview.settings.all(), workId] as const,
      detail: (id: string) => 
        [...queryKeys.worldview.settings.all(), 'detail', id] as const,
    },
    
    // 作品规范
    guidelines: (workId: string) => 
      [...queryKeys.worldview.all, 'guidelines', workId] as const,
    
    // AI创作规范
    aiGuidelines: (workId: string) => 
      [...queryKeys.worldview.all, 'aiGuidelines', workId] as const,
  },

  // ==================== 分析相关 ====================
  analysis: {
    all: ['analysis'] as const,
    status: (workId: string) => 
      [...queryKeys.analysis.all, 'status', workId] as const,
    result: (workId: string) => 
      [...queryKeys.analysis.all, 'result', workId] as const,
  },

  // ==================== 管理后台相关 ====================
  admin: {
    all: ['admin'] as const,
    
    // 统计数据
    statistics: () => [...queryKeys.admin.all, 'statistics'] as const,
    
    // 用户管理
    users: {
      all: () => [...queryKeys.admin.all, 'users'] as const,
      list: (filters?: Record<string, any>) => 
        [...queryKeys.admin.users.all(), 'list', filters] as const,
      detail: (id: string) => 
        [...queryKeys.admin.users.all(), 'detail', id] as const,
    },
    
    // AI模型管理
    aiModels: {
      all: () => [...queryKeys.admin.all, 'aiModels'] as const,
      list: () => [...queryKeys.admin.aiModels.all(), 'list'] as const,
      detail: (id: string) => 
        [...queryKeys.admin.aiModels.all(), 'detail', id] as const,
    },
    
    // 成本统计
    costs: {
      all: () => [...queryKeys.admin.all, 'costs'] as const,
      metrics: (dateRange?: { start: string; end: string }) => 
        [...queryKeys.admin.costs.all(), 'metrics', dateRange] as const,
    },
  },
} as const;

/**
 * 辅助函数：批量失效相关缓存
 */
export const invalidateWorkRelated = (workId: string) => {
  return [
    queryKeys.works.detail(workId),
    queryKeys.chapters.list(workId),
    queryKeys.worldview.worldData(workId),
    queryKeys.worldview.characters.list(workId),
    queryKeys.worldview.locations.list(workId),
    queryKeys.worldview.settings.list(workId),
  ];
};
