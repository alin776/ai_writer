/**
 * 认证服务
 * 专门处理登录、注册等认证相关的 API 调用
 */
import axios, { AxiosInstance } from 'axios';
import type { LoginCredentials, RegisterData, AuthResponse, User } from '@/types';

class AuthServiceClass {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 请求拦截器：添加 Token
    this.axiosInstance.interceptors.request.use(
      (config) => {
        const authStorage = localStorage.getItem('auth-storage');
        if (authStorage) {
          try {
            const { state } = JSON.parse(authStorage);
            if (state?.token) {
              config.headers.Authorization = `Bearer ${state.token}`;
            }
          } catch (e) {
            console.error('Failed to parse auth storage:', e);
          }
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // 响应拦截器：统一错误处理
    this.axiosInstance.interceptors.response.use(
      (response) => response.data,
      (error) => {
        if (error.response) {
          const { status, data } = error.response;
          const errorMessage = data?.detail || data?.message || '请求失败';

          console.error(`API Error [${status}]:`, errorMessage);
          return Promise.reject(new Error(errorMessage));
        }
        return Promise.reject(error);
      }
    );
  }

  /**
   * 用户登录
   * 后端使用 OAuth2PasswordRequestForm，需要使用 application/x-www-form-urlencoded 格式
   */
  async login(credentials: LoginCredentials): Promise<{ user: User; token: string }> {
    try {
      // 后端登录 API 使用 OAuth2PasswordRequestForm
      // 需要使用 application/x-www-form-urlencoded 格式
      const formData = new URLSearchParams();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);

      const response = await this.axiosInstance.post<AuthResponse>('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      // 后端现在直接返回 user 和 token
      const { access_token, user } = response;

      // 添加兼容字段
      const enrichedUser = this.enrichUser(user);

      return {
        user: enrichedUser,
        token: access_token,
      };
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  }

  /**
   * 用户注册
   */
  async register(data: RegisterData): Promise<{ user: User; token: string }> {
    try {
      // 后端注册 API 现在直接返回用户信息和 token
      const response = await this.axiosInstance.post<AuthResponse>('/auth/register', data);

      const { access_token, user } = response;

      // 添加兼容字段
      const enrichedUser = this.enrichUser(user);

      return {
        user: enrichedUser,
        token: access_token,
      };
    } catch (error) {
      console.error('Register failed:', error);
      throw error;
    }
  }

  /**
   * 添加兼容字段，便于前端使用
   */
  private enrichUser(user: User): User {
    return {
      ...user,
      name: user.full_name || user.username,
      role: user.is_admin ? 'admin' : 'user',
      registrationDate: user.created_at,
      status: user.is_active ? 'active' : 'disabled',
    };
  }

  /**
   * 获取当前用户信息
   */
  async getCurrentUser(): Promise<User> {
    try {
      const user = await this.axiosInstance.get<User>('/auth/me');
      return this.enrichUser(user);
    } catch (error) {
      console.error('Get current user failed:', error);
      throw error;
    }
  }

  /**
   * 刷新 Token
   */
  async refreshToken(refreshToken: string): Promise<string> {
    try {
      const response = await this.axiosInstance.post<AuthResponse>('/auth/refresh', {
        refresh_token: refreshToken,
      });

      return response.access_token;
    } catch (error) {
      console.error('Refresh token failed:', error);
      throw error;
    }
  }

  /**
   * 登出
   */
  async logout(): Promise<void> {
    localStorage.removeItem('auth-storage');
  }
}

// 导出单例
export const AuthService = new AuthServiceClass();
