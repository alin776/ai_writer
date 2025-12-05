/**
 * 真实 API 适配器（预留�? *
 * 用于生产环境，调用真实的后端 API
 * 使用 Axios 进行 HTTP 请求
 */
import axios, { AxiosInstance } from 'axios';
import { useAuthStore } from '@/store/authStore';
import type { IDataAdapter } from './IDataAdapter';

export class ApiAdapter implements IDataAdapter {
  private axiosInstance: AxiosInstance;
  private refreshPromise: Promise<string | null> | null = null;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',
      timeout: 180000, // 180秒超时（3分钟），适配AI长文本生�?
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 请求拦截器：添加 Token
    this.axiosInstance.interceptors.request.use(
      (config) => {
        // 登录/注册无需附带 Authorization，避免预检导致�?CORS 异常
        const url = config.url || '';
        const skipAuthHeader = url.includes('/auth/login') || url.includes('/auth/register') || url.includes('/auth/refresh');
        if (skipAuthHeader) {
          return config;
        }

        // �?Zustand persist 存储中读�?token
        const authStorage = localStorage.getItem('auth-storage');
        if (authStorage) {
          try {
            const authState = JSON.parse(authStorage);
            console.log('[ApiAdapter] Auth storage:', authState);
            
            const token = authState.state?.token;
            console.log('[ApiAdapter] Token:', token);
            
            if (token) {
              config.headers.Authorization = `Bearer ${token}`;
              console.log('[ApiAdapter] Authorization header set');
            } else {
              console.warn('[ApiAdapter] No token found in auth storage');
            }
          } catch (error) {
            console.error('[ApiAdapter] Failed to parse auth storage:', error);
          }
        } else {
          console.warn('[ApiAdapter] No auth-storage in localStorage');
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // 响应拦截器：处理错误和数据转�?
    this.axiosInstance.interceptors.response.use(
      (response) => {
        const url = response.config.url || '';
        console.log('[ApiAdapter] Response SUCCESS:', url);
        console.log('[ApiAdapter] Response data type:', typeof response.data);
        console.log('[ApiAdapter] Response data (raw):', response.data);
        console.log('[ApiAdapter] Response status:', response.status);
        
        // 在这里统一进行 snake_case �?camelCase 的转�?
        const camelCaseData = this.convertKeysToCamelCase(response.data);
        console.log('[ApiAdapter] Response data (camelCase):', camelCaseData);
        
        return { ...response, data: camelCaseData };
      },
      async (error) => {
        console.error('[ApiAdapter] Error:', error);
        console.error('[ApiAdapter] Error details:', {
          hasResponse: !!error.response,
          hasRequest: !!error.request,
          message: error.message,
          response: error.response,
          responseData: error.response?.data,
          status: error.response?.status
        });
        if (error.response) {
          // 服务器返回错误状态码
          const { status, data, config } = error.response;
          const url = config?.url || '';

          // 401 时尝试用 refresh token 续期，再重放原请求
          if (status === 401 && config && !url.includes('/auth/login') && !url.includes('/auth/register') && !url.includes('/auth/refresh')) {
            const originalRequest: any = config;
            if (!originalRequest._retry) {
              originalRequest._retry = true;
              try {
                const newAccessToken = await this.handleRefreshToken();
                if (newAccessToken) {
                  originalRequest.headers = originalRequest.headers || {};
                  originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                  return this.axiosInstance.request(originalRequest);
                }
              } catch (refreshError) {
                console.error('[ApiAdapter] Refresh token failed:', refreshError);
              }
            }
          }

          // 世界观相关的404错误静默处理（功能未实现，暂时忽略）
          const isWorldviewNotFound = status === 404 && (
            url.includes('/characters') ||
            url.includes('/locations') ||
            url.includes('/settings')
          );

          if (isWorldviewNotFound) {
            // 只在开发模式下显示警告
            if (import.meta.env.DEV) {
              console.warn(`[API] 世界观API未实�? ${url}`);
            }
            // 返回空数组，不中断应�?
            return Promise.resolve([]);
          }

          // 特殊处理：guidelines相关�?04是正常情况（可能还未创建�?
          const isGuidelinesNotFound = status === 404 && 
            (url.includes('/guidelines') || url.includes('/ai-guidelines'));
          
          if (isGuidelinesNotFound) {
            // 静默处理 guidelines �?04，这是正常情�?
            console.debug('Guidelines不存在（尚未创建�?', url);
          } else {
            // 其他错误正常打印
            console.error('API Error:', error);
          }

          switch (status) {
            case 401:
              // 未授权，清除 token 并跳转登�?
              localStorage.removeItem('auth-storage');
              window.location.href = '/login';
              break;
            case 403:
              // 无权限
              console.error('无权限访问');
              break;
            case 404:
              // 资源不存在- 静默处理，由调用方决定如何处理
              if (!isGuidelinesNotFound) {
                console.debug('资源不存在', url);
              }
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
   * 使用刷新令牌获取新的 access token，并更新全局状态
   */
  private async handleRefreshToken(): Promise<string | null> {
    if (this.refreshPromise) {
      return this.refreshPromise;
    }

    this.refreshPromise = (async () => {
      const { refreshToken, setToken, setRefreshToken, logout } = useAuthStore.getState();
      if (!refreshToken) {
        return null;
      }

      try {
        const response = await this.axiosInstance.post('/auth/refresh', {
          refresh_token: refreshToken,
        }, {
          headers: { 'Content-Type': 'application/json' },
        });

        const data: any = (response as any)?.data ?? response;
        const newAccessToken = data?.accessToken || data?.access_token;
        const newRefreshToken = data?.refreshToken || data?.refresh_token || refreshToken;

        if (!newAccessToken) {
          return null;
        }

        setToken(newAccessToken);
        setRefreshToken(newRefreshToken);
        return newAccessToken;
      } catch (error) {
        console.error('[ApiAdapter] Failed to refresh token:', error);
        logout();
        localStorage.removeItem('auth-storage');
        return null;
      } finally {
        this.refreshPromise = null;
      }
    })();

    return this.refreshPromise;
  }

  /**
   * 将snake_case转换为camelCase
   */
  private toCamelCase(str: string): string {
    return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
  }

  /**
   * 递归转换对象的键名从snake_case到camelCase
   */
  private convertKeysToCamelCase(obj: any): any {
    if (obj === null || obj === undefined) return obj;
    if (typeof obj !== 'object') return obj;
    if (obj instanceof Date) return obj;
    if (Array.isArray(obj)) return obj.map(item => this.convertKeysToCamelCase(item));

    const result: any = {};
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        const camelKey = this.toCamelCase(key);
        result[camelKey] = this.convertKeysToCamelCase(obj[key]);
      }
    }
    return result;
  }

  /**
   * 将camelCase转换为snake_case
   */
  private toSnakeCase(str: string): string {
    return str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
  }

  /**
   * 递归转换对象的键名从camelCase到snake_case
   */
  private convertKeysToSnakeCase(obj: any): any {
    if (obj === null || obj === undefined) return obj;
    if (typeof obj !== 'object') return obj;
    if (obj instanceof Date) return obj;
    if (Array.isArray(obj)) return obj.map(item => this.convertKeysToSnakeCase(item));

    const result: any = {};
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        const snakeKey = this.toSnakeCase(key);
        result[snakeKey] = this.convertKeysToSnakeCase(obj[key]);
      }
    }
    return result;
  }

  /**
   * GET 请求
   */
  async get<T>(url: string, params?: any): Promise<T> {
    const response = await this.axiosInstance.get(url, { params });
    return (response as any)?.data ?? (response as any as T);
  }

  /**
   * POST 请求
   */
  async post<T>(url: string, data?: any): Promise<T> {
    console.log('[ApiAdapter.post] URL:', url);
    console.log('[ApiAdapter.post] 请求数据:', data);
    
    // 特殊处理登录接口，使�?FormData
    if (url === '/auth/login') {
      const formData = new URLSearchParams();
      formData.append('username', data.username);
      formData.append('password', data.password);
      
      // 响应拦截器已经处理了 camelCase 转换
      const response = await this.axiosInstance.post(url, formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      return (response as any)?.data ?? (response as any as T);
    }

    // FormData 直接透传，避免键名转换破�?multipart 结构
    if (data instanceof FormData) {
      const response = await this.axiosInstance.post(url, data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return (response as any)?.data ?? (response as any as T);
    }
    
    // 将请求体�?camelCase 转换�?snake_case
    const snakeCaseData = this.convertKeysToSnakeCase(data);
    console.log('[ApiAdapter.post] 转换后的数据 (snake_case):', snakeCaseData);
    
    // 响应拦截器已经处理了 camelCase 转换，直接返�?
    const response = await this.axiosInstance.post(url, snakeCaseData);
    console.log('[ApiAdapter.post] 收到响应 (已转camelCase):', response);
    
    return (response as any)?.data ?? (response as any as T);
  }

  /**
   * PUT 请求
   */
  async put<T>(url: string, data?: any): Promise<T> {
    // 将请求体�?camelCase 转换�?snake_case
    const snakeCaseData = this.convertKeysToSnakeCase(data);
    // 响应拦截器已经处理了 camelCase 转换
    const response = await this.axiosInstance.put(url, snakeCaseData);
    return (response as any)?.data ?? (response as any as T);
  }

  /**
   * DELETE 请求
   */
  async delete<T>(url: string, data?: any): Promise<T> {
    let payload = data;
    if (payload && !(payload instanceof FormData)) {
      payload = this.convertKeysToSnakeCase(payload);
    }
    const response = await this.axiosInstance.delete(url, payload ? { data: payload } : undefined);
    return (response as any)?.data ?? (response as any as T);
  }

  /**
   * PATCH 请求
   */
  async patch<T>(url: string, data?: any): Promise<T> {
    console.log('[ApiAdapter.patch] URL:', url);
    console.log('[ApiAdapter.patch] 请求数据:', data);
    
    // 将请求体�?camelCase 转换�?snake_case
    const snakeCaseData = this.convertKeysToSnakeCase(data);
    console.log('[ApiAdapter.patch] 转换后的数据 (snake_case):', snakeCaseData);
    
    // 响应拦截器已经处理了 camelCase 转换，直接返�?
    const response = await this.axiosInstance.patch(url, snakeCaseData);
    console.log('[ApiAdapter.patch] 收到响应 (已转camelCase):', response);
    
    return (response as any)?.data ?? (response as any as T);
  }
}

