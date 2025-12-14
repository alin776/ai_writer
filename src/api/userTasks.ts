/**
 * 任务奖励系统API
 */
import axios from 'axios';
import { TaskListResponse, TaskTemplate, TaskTemplateUpdate } from '../types/userTask';

const API_BASE_URL = import.meta.env.DEV ? '/api/v1' : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1');

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器 - 添加token
api.interceptors.request.use(
  (config) => {
    // 从Zustand persist存储中读取token
    const authStorage = localStorage.getItem('auth-storage');
    if (authStorage) {
      try {
        const authState = JSON.parse(authStorage);
        const token = authState.state?.token;
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      } catch (error) {
        console.error('Failed to parse auth storage:', error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * 获取当前用户的所有任务
 */
export const getMyTasks = async (): Promise<TaskListResponse> => {
  const response = await api.get('/tasks/user/my-tasks');
  return response.data;
};

/**
 * 手动更新任务进度（测试用）
 */
export const updateTaskProgress = async (
  taskKey: string,
  progressIncrement: number = 1
): Promise<void> => {
  await api.post(`/tasks/user/progress/${taskKey}`, null, {
    params: { progress_increment: progressIncrement },
  });
};

/**
 * 获取所有任务模板（管理员）
 */
export const getAllTemplates = async (): Promise<TaskTemplate[]> => {
  const response = await api.get('/tasks/admin/templates');
  return response.data;
};

/**
 * 更新任务模板（管理员）
 */
export const updateTemplate = async (
  templateId: string,
  updateData: TaskTemplateUpdate
): Promise<TaskTemplate> => {
  const response = await api.patch(`/tasks/admin/templates/${templateId}`, updateData);
  return response.data;
};
