import { QueryClient } from '@tanstack/react-query';

/**
 * React Query Client 配置
 * 
 * 配置说明：
 * - staleTime: 数据被认为"新鲜"的时间，在此期间不会重新请求
 * - gcTime: 数据在缓存中保留的时间，超时后会被垃圾回收
 * - retry: 请求失败后的重试次数
 * - refetchOnWindowFocus: 窗口聚焦时是否自动刷新
 * - refetchOnReconnect: 网络重连时是否自动刷新
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // 数据新鲜时间：5分钟
      // 5分钟内再次访问会直接使用缓存，不发请求
      staleTime: 5 * 60 * 1000,

      // 缓存时间：30分钟
      // 超过30分钟未使用的数据会被清理
      gcTime: 30 * 60 * 1000,

      // 失败重试1次
      retry: 1,

      // 窗口聚焦时不自动刷新（避免频繁请求）
      refetchOnWindowFocus: false,

      // 网络重连时自动刷新
      refetchOnReconnect: true,

    },
    mutations: {
      // Mutation 失败不重试（由用户手动重试）
      retry: false,
    },
  },
});

/**
 * 针对不同数据类型的自定义配置
 */
export const queryOptions = {
  /**
   * 静态数据配置（如：作品列表、章节列表）
   * 这些数据变化不频繁，可以长时间缓存
   */
  static: {
    staleTime: 10 * 60 * 1000,  // 10分钟
    gcTime: 60 * 60 * 1000,  // 1小时
  },

  /**
   * 动态数据配置（如：章节内容、世界观数据）
   * 这些数据可能被其他用户修改，需要较短的缓存时间
   */
  dynamic: {
    staleTime: 2 * 60 * 1000,   // 2分钟
    gcTime: 10 * 60 * 1000,  // 10分钟
  },

  /**
   * 实时数据配置（如：分析状态、AI处理状态）
   * 这些数据需要频繁更新
   */
  realtime: {
    staleTime: 0,               // 立即过期
    gcTime: 1 * 60 * 1000,   // 1分钟
    refetchInterval: 3000,      // 每3秒自动刷新
  },

  /**
   * 编辑中数据配置
   * 用户正在编辑时，禁用自动刷新
   */
  editing: {
    staleTime: Infinity,        // 永不过期
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
  },
};
