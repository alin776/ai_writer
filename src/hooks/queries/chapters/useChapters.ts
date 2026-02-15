import { useQuery, UseQueryOptions } from '@tanstack/react-query';
import { DataService } from '@/services/DataService';
import { queryKeys } from '../queryKeys';
import { queryOptions } from '@/config/queryClient';
import type { Chapter } from '@/types';

/**
 * 获取作品章节列表的 Hook
 * 
 * 使用示例：
 * ```tsx
 * const { data: chapters, isLoading } = useChapters(workId);
 * ```
 * 
 * @param workId - 作品 ID
 * @param options - React Query 配置选项
 * @returns Query result
 */
export const useChapters = (
  workId: string | undefined,
  options?: Omit<UseQueryOptions<Chapter[], Error>, 'queryKey' | 'queryFn'>
) => {
  return useQuery<Chapter[], Error>({
    queryKey: queryKeys.chapters.list(workId!),
    queryFn: async () => {
      if (!workId) throw new Error('Work ID is required');
      return await DataService.getChapters(workId);
    },
    enabled: !!workId,
    ...queryOptions.static,
    ...options,
  });
};
