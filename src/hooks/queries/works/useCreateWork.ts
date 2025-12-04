import { useMutation, useQueryClient, UseMutationOptions } from '@tanstack/react-query';
import { DataService } from '@/services/DataService';
import { queryKeys } from '../queryKeys';
import { useGlobalStore } from '@/store/globalStore';
import type { CreateWorkData, Work } from '@/types';

/**
 * 创建作品的 Hook
 * 
 * 使用示例：
 * ```tsx
 * const createWork = useCreateWork();
 * 
 * const handleCreate = async () => {
 *   try {
 *     const newWork = await createWork.mutateAsync({
 *       title: '新作品',
 *       description: '描述'
 *     });
 *     navigate(`/works/${newWork.id}`);
 *   } catch (error) {
 *     // 错误已自动显示 toast
 *   }
 * };
 * 
 * // 或者使用回调
 * createWork.mutate(workData, {
 *   onSuccess: (work) => navigate(`/works/${work.id}`)
 * });
 * ```
 * 
 * @param options - React Query mutation 配置选项
 * @returns Mutation result
 */
export const useCreateWork = (
  options?: UseMutationOptions<Work, Error, CreateWorkData>
) => {
  const queryClient = useQueryClient();
  const { showToast } = useGlobalStore();

  return useMutation<Work, Error, CreateWorkData>({
    mutationFn: async (workData: CreateWorkData) => {
      return await DataService.createWork(workData);
    },

    onSuccess: (newWork, variables, context) => {
      // 1. 失效作品列表缓存（触发自动刷新）
      queryClient.invalidateQueries({ queryKey: queryKeys.works.lists() });

      // 2. 预填充新作品的详情缓存（优化性能）
      queryClient.setQueryData(queryKeys.works.detail(newWork.id), newWork);

      // 3. 显示成功提示
      showToast('success', '作品创建成功');

      // 4. 调用用户自定义的 onSuccess
      if (options?.onSuccess) {
        options.onSuccess(newWork, variables, context, undefined as any);
      }
    },

    onError: (error, variables, context) => {
      // 显示错误提示
      const message = error instanceof Error ? error.message : '创建作品失败';
      showToast('error', message);

      // 调用用户自定义的 onError
      if (options?.onError) {
        options.onError(error, variables, context, undefined as any);
      }
    },

    ...options,
  });
};
