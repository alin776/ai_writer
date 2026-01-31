import { useQuery, UseQueryOptions } from '@tanstack/react-query';
import { DataService } from '@/services/DataService';
import { queryKeys } from '../queryKeys';
import type { AnalysisStatusResponse } from '@/types';

/**
 * 获取分析状态的 Hook（支持自动轮询）
 * 
 * 特点：
 * - 当状态为 'processing' 时，每2秒自动轮询
 * - 完成或失败后自动停止轮询
 * - 支持手动刷新
 * 
 * 使用示例：
 * ```tsx
 * const { data: status, isLoading } = useAnalysisStatus(workId);
 * 
 * if (status?.status === 'processing') {
 *   return <Progress value={status.progress} />;
 * }
 * ```
 * 
 * @param workId - 作品 ID
 * @param options - React Query 配置选项
 * @returns Query result
 */
export const useAnalysisStatus = (
  workId: string | undefined,
  options?: Omit<UseQueryOptions<AnalysisStatusResponse, Error>, 'queryKey' | 'queryFn'>
) => {
  return useQuery<AnalysisStatusResponse, Error>({
    queryKey: queryKeys.analysis.status(workId || ''),
    queryFn: async () => {
      if (!workId) throw new Error('Work ID is required');
      return await DataService.getAnalysisStatus(workId);
    },
    enabled: !!workId,
    
    // 智能轮询：仅在处理中时轮询
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (status === 'processing') {
        return 2000;
      }
      return false;
    },

    // 确保数据总是最新的
    staleTime: 0,
    gcTime: 1 * 60 * 1000, // 1分钟

    // 窗口聚焦时不刷新（避免打断用户）
    refetchOnWindowFocus: false,

    ...options,
  });
};

/**
 * 使用示例（完整流程）：
 * 
 * ```tsx
 * const NovelAnalysisPanel = ({ workId }) => {
 *   const startAnalysis = useStartAnalysis();
 *   const { data: status, refetch } = useAnalysisStatus(workId);
 *   
 *   const handleStart = async () => {
 *     await startAnalysis.mutateAsync(workId);
 *     // mutation 成功后会自动触发 status 刷新
 *   };
 *   
 *   // 根据状态显示不同 UI
 *   if (!status) {
 *     return <Button onClick={handleStart}>开始分析</Button>;
 *   }
 *   
 *   if (status.status === 'processing') {
 *     return (
 *       <div>
 *         <Progress value={status.progress} />
 *         <p>正在分析... {status.progress}%</p>
 *       </div>
 *     );
 *   }
 *   
 *   if (status.status === 'completed') {
 *     return <AnalysisResult workId={workId} />;
 *   }
 *   
 *   return <Error message={status.error} />;
 * };
 * ```
 */
