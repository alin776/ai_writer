import { useQuery, UseQueryOptions } from '@tanstack/react-query';
import { DataService } from '@/services/DataService';
import { queryKeys } from '../queryKeys';
import { queryOptions } from '@/config/queryClient';
import type { Work } from '@/types';

/**
 * 获取单个作品详情的 Hook
 * 
 * 使用示例：
 * ```tsx
 * const { data: work, isLoading, error } = useWork(workId);
 * 
 * // 编辑中禁用自动刷新
 * const { data: work } = useWork(workId, { 
 *   enabled: !isEditing,
 *   ...queryOptions.editing 
 * });
 * ```
 * 
 * @param workId - 作品 ID
 * @param options - React Query 配置选项
 * @returns Query result
 */
export const useWork = (
  workId: string | undefined,
  options?: Omit<UseQueryOptions<Work, Error>, 'queryKey' | 'queryFn'>
) => {
  return useQuery<Work, Error>({
    queryKey: queryKeys.works.detail(workId!),
    queryFn: async () => {
      if (!workId) throw new Error('Work ID is required');
      return await DataService.getWork(workId);
    },
    // 只有 workId 存在时才执行查询
    enabled: !!workId,
    // 使用动态数据配置
    ...queryOptions.dynamic,
    // 允许用户覆盖配置
    ...options,
  });
};
