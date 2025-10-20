import { useQuery, UseQueryOptions } from '@tanstack/react-query';
import { DataService } from '@/services/DataService';
import { queryKeys } from '../queryKeys';
import { queryOptions } from '@/config/queryClient';
import type { Work } from '@/types';

/**
 * 获取作品列表的 Hook
 * 
 * 使用示例：
 * ```tsx
 * const { data: works, isLoading, error, refetch } = useWorks();
 * 
 * if (isLoading) return <Loading />;
 * if (error) return <Error message={error.message} />;
 * return <WorkList works={works} />;
 * ```
 * 
 * @param options - React Query 配置选项
 * @returns Query result
 */
export const useWorks = (
  options?: Omit<UseQueryOptions<Work[], Error>, 'queryKey' | 'queryFn'>
) => {
  return useQuery<Work[], Error>({
    queryKey: queryKeys.works.lists(),
    queryFn: async () => {
      const works = await DataService.getWorks();
      return works;
    },
    // 使用静态数据配置（作品列表变化不频繁）
    ...queryOptions.static,
    // 允许用户覆盖配置
    ...options,
  });
};

/**
 * 使用示例（带筛选）：
 * 
 * ```tsx
 * // 未来如果需要支持筛选
 * const useWorks = (filters?: WorkFilters) => {
 *   return useQuery({
 *     queryKey: queryKeys.works.list(filters),
 *     queryFn: () => DataService.getWorks(filters),
 *     ...queryOptions.static,
 *   });
 * };
 * ```
 */
