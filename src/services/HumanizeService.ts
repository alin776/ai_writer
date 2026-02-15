// src/services/HumanizeService.ts

import axios, { AxiosInstance } from 'axios';
import type {
  HumanizeIntensity,
  HumanizeSession,
  HumanizeHistoryResponse,
  HumanizeStatsResponse,
  UserProfile,
  UserProfileUpdateRequest,
  HumanizeStreamEvent
} from '@/types/humanize';

/**
 * HumanizeService - AI去痕迹API服务
 *
 * 功能:
 * - 用户画像管理
 * - 去痕迹改写 (流式/非流式)
 * - 历史记录查询
 * - 统计数据获取
 * - 用户反馈提交
 */
class HumanizeService {
  private api: AxiosInstance;

  /**
   * 从持久化存储中读取 token
   * 优先从 Zustand 持久化的 auth-storage 读取，兼容旧的 localStorage 'token' 键
   */
  private getToken(): string | null {
    const authStorage = localStorage.getItem('auth-storage');
    if (authStorage) {
      try {
        const authState = JSON.parse(authStorage);
        const token = authState.state?.token;
        if (token) return token as string;
      } catch (error) {
        console.error('[HumanizeService] Failed to parse auth storage', error);
      }
    }
    return localStorage.getItem('token');
  }

  constructor() {
    // 创建Axios实例
    this.api = axios.create({
      // 默认指向后端 /api/v1 前缀，避免遗漏版本号导致 404
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
      timeout: 60000, // 60秒超时
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 添加请求拦截器 - 自动添加token
    this.api.interceptors.request.use((config) => {
      const token = this.getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // 添加响应拦截器 - 统一错误处理
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token过期，清除本地存储并跳转登录
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // ==================== 用户画像相关 ====================

  /**
   * 获取用户画像
   * @returns 用户画像数据
   */
  async getUserProfile(): Promise<UserProfile> {
    const { data } = await this.api.get<UserProfile>('/humanize/profile');
    return data;
  }

  /**
   * 更新用户画像设置
   * @param settings 更新的设置项
   * @returns 更新后的用户画像
   */
  async updateUserProfile(
    settings: UserProfileUpdateRequest
  ): Promise<UserProfile> {
    const { data } = await this.api.put<UserProfile>(
      '/humanize/profile/settings',
      settings
    );
    return data;
  }

  // ==================== 去痕迹改写相关 ====================

  /**
   * 非流式去痕迹化（用于测试或特殊场景）
   *
   * @param text 待去痕迹的文本
   * @param intensity 改写强度
   * @param ai_function AI功能类型
   * @returns 完整的会话记录
   */
  async rewrite(
    text: string,
    intensity: HumanizeIntensity = 'medium',
    ai_function: string = 'rewrite'
  ): Promise<HumanizeSession> {
    const { data } = await this.api.post<HumanizeSession>('/humanize/rewrite', {
      text,
      intensity,
      ai_function,
    });
    return data;
  }

  /**
   * 流式去痕迹化（推荐使用）
   *
   * 使用SSE (Server-Sent Events) 协议实时接收改写内容
   *
   * @param text 待去痕迹的文本
   * @param intensity 改写强度
   * @param ai_function AI功能类型
   * @param onChunk 事件回调函数
   *
   * @example
   * ```typescript
   * await HumanizeService.rewriteStream(
   *   text,
   *   'medium',
   *   'rewrite',
   *   (event) => {
   *     if (event.type === 'chunk') {
   *       console.log('Received:', event.content);
   *     }
   *   }
   * );
   * ```
   */
  async rewriteStream(
    text: string,
    intensity: HumanizeIntensity = 'medium',
    ai_function: string = 'rewrite',
    onChunk: (event: HumanizeStreamEvent) => void,
    signal?: AbortSignal
  ): Promise<void> {
    const token = this.getToken();
    const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

    // 使用Fetch API进行SSE请求
    const response = await fetch(
      `${baseURL}/humanize/rewrite/stream`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        },
        signal,
        body: JSON.stringify({
          text,
          intensity,
          ai_function,
        }),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 读取流式响应
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) {
      throw new Error('No response body');
    }

    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        // 解码数据
        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;

        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        // 解析SSE格式（逐行，容错半包）
        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed.startsWith('data:')) continue;
          try {
            const payload = trimmed.slice(5).trim();
            const event: HumanizeStreamEvent = JSON.parse(payload);
            onChunk(event);
          } catch (e) {
            console.warn('Failed to parse SSE data:', trimmed, e);
          }
        }
      }

      // 处理剩余缓冲
      const tail = buffer.trim();
      if (tail.startsWith('data:')) {
        try {
          const payload = tail.slice(5).trim();
          const event: HumanizeStreamEvent = JSON.parse(payload);
          onChunk(event);
        } catch (e) {
          console.warn('Failed to parse trailing SSE data:', tail, e);
        }
      }
    } finally {
      reader.releaseLock();
    }
  }

  // ==================== 历史记录相关 ====================

  /**
   * 获取历史记录 (分页)
   *
   * @param page 页码 (从1开始)
   * @param pageSize 每页数量
   * @returns 分页的历史记录
   */
  async getHistory(
    page: number = 1,
    pageSize: number = 20
  ): Promise<HumanizeHistoryResponse> {
    const { data } = await this.api.get<HumanizeHistoryResponse>(
      '/humanize/history',
      {
        params: { page, page_size: pageSize },
      }
    );
    return data;
  }

  /**
   * 获取单条会话详情
   *
   * @param sessionId 会话ID
   * @returns 会话详情
   */
  async getSession(sessionId: string): Promise<HumanizeSession> {
    const { data } = await this.api.get<HumanizeSession>(
      `/humanize/history/${sessionId}`
    );
    return data;
  }

  // ==================== 统计数据相关 ====================

  /**
   * 获取统计数据
   *
   * @returns 统计数据（总使用次数、接受率、平均改进等）
   */
  async getStats(): Promise<HumanizeStatsResponse> {
    const { data } = await this.api.get<HumanizeStatsResponse>('/humanize/stats');
    return data;
  }

  // ==================== 用户反馈相关 ====================

  /**
   * 提交用户反馈
   *
   * @param sessionId 会话ID
   * @param accepted 是否接受结果
   */
  async submitFeedback(sessionId: string, accepted: boolean): Promise<void> {
    await this.api.post('/humanize/feedback', {
      session_id: sessionId,
      accepted,
    });
  }
}

// 导出单例
export default new HumanizeService();