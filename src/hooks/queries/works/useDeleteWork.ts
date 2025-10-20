import { useMutation, useQueryClient, UseMutationOptions } from '@tanstack/react-query';
import { DataService } from '@/services/DataService';
import { queryKeys, invalidateWorkRelated } from '../queryKeys';
import { useGlobalStore } from '@/store/globalStore';
import type { Work } from '@/types';

/**
 * 删除作品的 Hook
 * 
 * 使用示例：
 * ```tsx
 * const deleteWork = useDeleteWork();
 * 
 * const handleDelete = async (work: Work) => {
 *   const confirmed = await confirm({ title: '确认删除？' });
 *   if (!confirmed) return;
 *   
 *   await deleteWork.mutateAsync(work.id);
 *   navigate('/works');
 * };
 * ```
 * 
 * @param options - React Query mutation 配置选项
 * @returns Mutation result
 */
export const useDeleteWork = (
  options?: UseMutationOptions<void, Error, string>
) => {
  const queryClient = useQueryClient();
  const { showToast } = useGlobalStore();

  return useMutation<void, Error, string>({
    mutationFn: async (workId: string) => {
      return await DataService.deleteWork(workId);
    },

    // 乐观更新
    onMutate: async (deletedId) => {
      // 1. 取消正在进行的查询
      await queryClient.cancelQueries({ queryKey: queryKeys.works.lists() });

      // 2. 保存旧数据（用于回滚）
      const previousWorks = queryClient.getQueryData<Work[]>(queryKeys.works.lists());

      // 3. 乐观更新：从列表中移除
      if (previousWorks) {
        queryClient.setQueryData<Work[]>(
          queryKeys.works.lists(),
          previousWorks.filter((work) => work.id !== deletedId)
        );
      }

      // 返回上下文（用于回滚）
      return { previousWorks };
    },

    onSuccess: (_, deletedId, context) => {
      // 1. 移除详情缓存
      queryClient.removeQueries({ queryKey: queryKeys.works.detail(deletedId) });

      // 2. 失效相关缓存（章节、世界观等）
      invalidateWorkRelated(deletedId).forEach((key) => {
        queryClient.removeQueries({ queryKey: key });
      });

      // 3. 确保列表数据是最新的（防止乐观更新失败）
      queryClient.invalidateQueries({ queryKey: queryKeys.works.lists() });

      // 4. 显示成功提示
      showToast('success', '作品已删除');

      // 5. 调用用户自定义的 onSuccess
      options?.onSuccess?.(undefined, deletedId, context);
    },

    onError: (error, deletedId, context) => {
      // 回滚乐观更新
      if (context?.previousWorks) {
        queryClient.setQueryData(queryKeys.works.lists(), context.previousWorks);
      }

      // 显示错误提示
      const message = error instanceof Error ? error.message : '删除作品失败';
      showToast('error', message);

      // 调用用户自定义的 onError
      options?.onError?.(error, deletedId, context);
    },

    ...options,
  });
};
