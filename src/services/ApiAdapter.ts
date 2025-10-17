/**
 * 真实 API 适配器（预留）
 *
 * 用于生产环境，调用真实的后端 API
 * 使用 Axios 进行 HTTP 请求
 */
import axios, { AxiosInstance } from 'axios';
import type { IDataAdapter } from './IDataAdapter';

export class ApiAdapter implements IDataAdapter {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 请求拦截器：添加 Token
    this.axiosInstance.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // 响应拦截器：处理错误
    this.axiosInstance.interceptors.response.use(
      (response) => response.data,
      (error) => {
        if (error.response) {
          // 服务器返回错误状态码
          const { status, data, config } = error.response;
          const url = config?.url || '';

          // 世界观相关的404错误静默处理（功能未实现，暂时忽略）
          const isWorldviewNotFound = status === 404 && (
            url.includes('/characters') ||
            url.includes('/locations') ||
            url.includes('/settings')
          );

          if (isWorldviewNotFound) {
            // 只在开发模式下显示警告
            if (import.meta.env.DEV) {
              console.warn(`[API] 世界观API未实现: ${url}`);
            }
            // 返回空数组，不中断应用
            return Promise.resolve([]);
          }

          // 非世界观错误，正常打印
          console.error('API Error:', error);

          switch (status) {
            case 401:
              // 未授权，清除 token 并跳转登录
              localStorage.removeItem('token');
              window.location.href = '/login';
              break;
            case 403:
              // 无权限
              console.error('无权限访问');
              break;
            case 404:
              // 资源不存在
              console.error('资源不存在:', url);
              break;
            case 500:
              // 服务器错误
              console.error('服务器错误');
              break;
            default:
              console.error('请求错误:', data?.message || error.message);
          }

          return Promise.reject(data || error);
        } else if (error.request) {
          // 请求已发送但没有收到响应
          console.error('网络错误，请检查网络连接');
          return Promise.reject(new Error('网络错误'));
        } else {
          // 其他错误
          console.error('请求配置错误:', error.message);
          return Promise.reject(error);
        }
      }
    );
  }

  /**
   * GET 请求
   */
  async get<T>(url: string, params?: any): Promise<T> {
    return this.axiosInstance.get(url, { params });
  }

  /**
   * POST 请求
   */
  async post<T>(url: string, data?: any): Promise<T> {
    // 特殊处理登录接口，使用 FormData
    if (url === '/auth/login') {
      const formData = new URLSearchParams();
      formData.append('username', data.username);
      formData.append('password', data.password);
      
      return this.axiosInstance.post(url, formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
    }
    
    return this.axiosInstance.post(url, data);
  }

  /**
   * PUT 请求
   */
  async put<T>(url: string, data?: any): Promise<T> {
    return this.axiosInstance.put(url, data);
  }

  /**
   * DELETE 请求
   */
  async delete<T>(url: string): Promise<T> {
    return this.axiosInstance.delete(url);
  }
}
