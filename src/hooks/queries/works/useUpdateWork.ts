import { useMutation, useQueryClient, UseMutationOptions } from '@tanstack/react-query';
import { DataService } from '@/services/DataService';
import { queryKeys } from '../queryKeys';
import { useGlobalStore } from '@/store/globalStore';
import type { Work } from '@/types';

interface UpdateWorkVariables {
  id: string;
  data: Partial<Work>;
}

/**
 * 更新作品的 Hook
 * 
 * 使用示例：
 * ```tsx
 * const updateWork = useUpdateWork();
 * 
 * const handleUpdate = async () => {
 *   await updateWork.mutateAsync({
 *     id: workId,
 *     data: { title: '新标题' }
 *   });
 * };
 * ```
 * 
 * @param options - React Query mutation 配置选项
 * @returns Mutation result
 */
export const useUpdateWork = (
  options?: UseMutationOptions<Work, Error, UpdateWorkVariables>
) => {
  const queryClient = useQueryClient();
  const { showToast } = useGlobalStore();

  return useMutation<Work, Error, UpdateWorkVariables>({
    mutationFn: async ({ id, data }: UpdateWorkVariables) => {
      return await DataService.updateWork(id, data);
    },

    // 乐观更新
    onMutate: async ({ id, data }) => {
      // 1. 取消正在进行的查询，避免冲突
      await queryClient.cancelQueries({ queryKey: queryKeys.works.detail(id) });

      // 2. 保存旧数据（用于回滚）
      const previousWork = queryClient.getQueryData<Work>(queryKeys.works.detail(id));

      // 3. 乐观更新缓存
      if (previousWork) {
        queryClient.setQueryData<Work>(queryKeys.works.detail(id), {
          ...previousWork,
          ...data,
          updatedAt: new Date().toISOString(),
        });
      }

      // 返回上下文（用于回滚）
      return { previousWork };
    },

    onSuccess: (updatedWork, variables, context) => {
      // 1. 更新详情缓存
      queryClient.setQueryData(queryKeys.works.detail(updatedWork.id), updatedWork);

      // 2. 失效作品列表缓存（因为列表中也显示了作品信息）
      queryClient.invalidateQueries({ queryKey: queryKeys.works.lists() });

      // 3. 显示成功提示
      showToast('success', '作品更新成功');

      // 4. 调用用户自定义的 onSuccess
      if (options?.onSuccess) {
        options.onSuccess(updatedWork, variables, context, undefined as any);
      }
    },

    onError: (error, variables, context) => {
      // 回滚乐观更新
      if (context && (context as any).previousWork) {
        queryClient.setQueryData(
          queryKeys.works.detail(variables.id),
          (context as any).previousWork
        );
      }

      // 显示错误提示
      const message = error instanceof Error ? error.message : '更新作品失败';
      showToast('error', message);

      // 调用用户自定义的 onError
      if (options?.onError) {
        options.onError(error, variables, context, undefined as any);
      }
    },

    ...options,
  });
};
