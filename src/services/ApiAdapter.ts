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
        // 统一错误处理
        console.error('API Error:', error);

        if (error.response) {
          // 服务器返回错误状态码
          const { status, data } = error.response;

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
              console.error('资源不存在');
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
