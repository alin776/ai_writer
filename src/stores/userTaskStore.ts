/**
 * 用户任务状态管理
 */
import { create } from 'zustand';
import { TaskListResponse, UserTaskWithTemplate } from '../types/userTask';
import { getMyTasks } from '../api/userTasks';

interface UserTaskState {
  tasks: UserTaskWithTemplate[];
  total: number;
  completedCount: number;
  totalCreditsEarned: number;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchTasks: () => Promise<void>;
  refreshTasks: () => Promise<void>;
  clearError: () => void;
}

export const useUserTaskStore = create<UserTaskState>((set) => ({
  tasks: [],
  total: 0,
  completedCount: 0,
  totalCreditsEarned: 0,
  isLoading: false,
  error: null,

  fetchTasks: async () => {
    set({ isLoading: true, error: null });
    try {
      const data: TaskListResponse = await getMyTasks();
      set({
        tasks: data.tasks,
        total: data.total,
        completedCount: data.completed_count,
        totalCreditsEarned: data.total_credits_earned,
        isLoading: false,
      });
    } catch (error: any) {
      console.error('获取任务列表失败:', error);
      console.error('错误详情:', error.response?.data);

      let errorMessage = '获取任务列表失败';
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          // Pydantic验证错误
          errorMessage = error.response.data.detail.map((err: any) =>
            `${err.loc?.join('.')}: ${err.msg}`
          ).join(', ');
        } else {
          errorMessage = error.response.data.detail;
        }
      }

      set({
        error: errorMessage,
        isLoading: false,
      });
    }
  },

  refreshTasks: async () => {
    // 静默刷新，不显示loading
    try {
      const data: TaskListResponse = await getMyTasks();
      set({
        tasks: data.tasks,
        total: data.total,
        completedCount: data.completed_count,
        totalCreditsEarned: data.total_credits_earned,
      });
    } catch (error: any) {
      console.error('刷新任务失败:', error);
    }
  },

  clearError: () => set({ error: null }),
}));
