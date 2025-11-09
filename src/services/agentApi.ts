/**
 * Agent API 服务封装
 *
 * 提供所有Agent相关的API调用方法
 */

import axios, { AxiosInstance } from 'axios';
import type {
  AgentChatRequest,
  AgentChatResponse,
  PlanCreationRequest,
  PlanResponse,
  ApprovalResponse,
  ApprovalActionRequest
} from '../types/agent';

class AgentApiService {
  private client: AxiosInstance;

  constructor() {
    // 使用本地后端API基础URL，而不是OpenAI代理URL
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace('/api/v1', '') || 'http://localhost:8000';

    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api/v1/agent`,
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 180000 // 180秒超时（3分钟），适配长文本生成
    });

    // 请求拦截器 - 添加Token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // 响应拦截器 - 统一错误处理
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token过期，跳转登录
          this.handleUnauthorized();
        }
        return Promise.reject(error);
      }
    );
  }

  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      // 从 Zustand persist 存储中读取 token（与 ApiAdapter、AIService 保持一致）
      const authStorage = localStorage.getItem('auth-storage');
      if (authStorage) {
        try {
          const authState = JSON.parse(authStorage);
          return authState.state?.token || null;
        } catch (error) {
          console.error('[AgentApi] Failed to parse auth storage:', error);
          return null;
        }
      }
    }
    return null;
  }

  private handleUnauthorized(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth-storage');
      window.location.href = '/login';
    }
  }

  /**
   * Agent对话
   */
  async chat(request: AgentChatRequest): Promise<AgentChatResponse> {
    const response = await this.client.post<AgentChatResponse>('/chat', request);
    return response.data;
  }

  /**
   * Agent对话 - 流式响应（SSE）with Planning + Execution
   *
   * @param request 对话请求
   * @param callbacks 回调函数集合
   */
  async chatStream(
    request: AgentChatRequest,
    callbacks: {
      // 共同回调
      onStart?: (conversationId: string) => void;
      onContent?: (chunk: string) => void;
      onStep?: (step: any) => void;
      onDone?: (metadata: any, suggestedActions: string[]) => void;
      onError?: (error: string) => void;
      // Planning 模式回调
      onPlan?: (plan: any) => void;
      onTaskStart?: (task: any) => void;
      onTaskProgress?: (progress: any) => void;
      onTaskDone?: (taskDone: any) => void;
      // React 模式回调（新增）
      onProgress?: (progress: any) => void;
      onToolCall?: (toolCall: any) => void;
    }
  ): Promise<void> {
    const token = this.getToken();
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace('/api/v1', '') || 'http://localhost:8000';
    const url = `${API_BASE_URL}/api/v1/agent/chat/stream`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        // 解码数据块
        buffer += decoder.decode(value, { stream: true });

        // 处理缓冲区中的所有完整事件
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // 保留不完整的行

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.substring(6));

              switch (data.type) {
                // 共同事件
                case 'start':
                  callbacks.onStart?.(data.conversation_id);
                  break;
                case 'content':
                  // 处理两种格式的 content
                  const content = typeof data.data === 'string'
                    ? data.data
                    : data.data?.content || data.data;
                  callbacks.onContent?.(content);
                  break;
                case 'step':
                  callbacks.onStep?.(data.data);
                  break;
                case 'done':
                  callbacks.onDone?.(data.metadata, data.suggested_actions);
                  break;
                case 'error':
                  callbacks.onError?.(data.error);
                  break;

                // Planning 模式事件
                case 'plan':
                  callbacks.onPlan?.(data.data);
                  break;
                case 'task_start':
                  callbacks.onTaskStart?.(data.data);
                  break;
                case 'task_progress':
                  callbacks.onTaskProgress?.(data.data);
                  break;
                case 'task_done':
                  callbacks.onTaskDone?.(data.data);
                  break;

                // React 模式事件（新增）
                case 'progress':
                  console.log('🟢 [API] 收到 progress 事件:', data.data);
                  callbacks.onProgress?.(data.data);
                  break;
                case 'tool_call':
                  console.log('🟢 [API] 收到 tool_call 事件:', data.data);
                  callbacks.onToolCall?.(data.data);
                  break;
              }
            } catch (error) {
              console.error('[AgentApi] Failed to parse SSE data:', error);
            }
          }
        }
      }
    } catch (error: any) {
      console.error('[AgentApi] Stream error:', error);
      callbacks.onError?.(error.message || 'Stream connection failed');
      throw error;
    }
  }


  /**
   * 创建执行计划
   */
  async createPlan(request: PlanCreationRequest): Promise<PlanResponse> {
    const response = await this.client.post<PlanResponse>('/plans', request);
    return response.data;
  }

  /**
   * 查询计划状态
   */
  async getPlan(planId: string): Promise<PlanResponse> {
    const response = await this.client.get<PlanResponse>(`/plans/${planId}`);
    return response.data;
  }

  /**
   * 获取待批准请求列表
   */
  async getPendingApprovals(): Promise<ApprovalResponse[]> {
    const response = await this.client.get<ApprovalResponse[]>('/approvals/pending');
    return response.data;
  }

  /**
   * 批准请求
   */
  async approveRequest(
    requestId: string,
    action: ApprovalActionRequest
  ): Promise<any> {
    const response = await this.client.post(
      `/approvals/${requestId}/approve`,
      action
    );
    return response.data;
  }

  /**
   * 拒绝请求
   */
  async rejectRequest(
    requestId: string,
    action: ApprovalActionRequest
  ): Promise<any> {
    const response = await this.client.post(
      `/approvals/${requestId}/reject`,
      action
    );
    return response.data;
  }

  /**
   * 获取用户记忆上下文
   */
  async getMemoryContext(): Promise<any> {
    const response = await this.client.get('/memory/context');
    return response.data;
  }

  /**
   * 更新用户偏好
   */
  async updatePreferences(preferences: any): Promise<any> {
    const response = await this.client.put('/memory/context', preferences);
    return response.data;
  }
}

// 导出单例
export const agentApi = new AgentApiService();

// 也导出类型，方便其他地方使用
export type { AgentApiService };
