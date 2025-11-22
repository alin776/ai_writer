/**
 * 个人知识库 API 服务
 */

import axios, { AxiosInstance } from 'axios';

interface KnowledgeItem {
  id: string;
  title: string;
  content?: string;
  source_type: 'text' | 'file' | 'url';
  file_type?: string;
  tags: string[];
  created_at: string;
  updated_at: string;
  chunk_count?: number;
}

interface KnowledgeListResponse {
  items: KnowledgeItem[];
  total: number;
  page: number;
  page_size: number;
}

interface CreateKnowledgeRequest {
  title: string;
  content: string;
  category: string;
  tags?: string[];
}

interface UpdateKnowledgeRequest {
  title?: string;
  content?: string;
  category?: string;
  tags?: string[];
}

interface SearchRequest {
  query: string;
  limit?: number;
  tags?: string[];
}

interface SearchResult {
  id: string;
  title: string;
  content: string;
  score: number;
  tags: string[];
}

class KnowledgeApiService {
  private client: AxiosInstance;

  constructor() {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace('/api/v1', '') || 'http://localhost:8000';

    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api/v1/knowledge`,
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 60000
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

    // 响应拦截器
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.handleUnauthorized();
        }
        return Promise.reject(error);
      }
    );
  }

  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      const authStorage = localStorage.getItem('auth-storage');
      if (authStorage) {
        try {
          const authState = JSON.parse(authStorage);
          return authState.state?.token || null;
        } catch {
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
   * 获取知识列表
   */
  async getList(params?: {
    search?: string;
    tags?: string[];
    page?: number;
    page_size?: number;
  }): Promise<KnowledgeListResponse> {
    const response = await this.client.get<KnowledgeListResponse>('/', { params });
    return response.data;
  }

  /**
   * 获取单个知识详情
   */
  async getById(id: string): Promise<KnowledgeItem> {
    const response = await this.client.get<KnowledgeItem>(`/${id}`);
    return response.data;
  }

  /**
   * 创建文本知识
   */
  async create(data: CreateKnowledgeRequest): Promise<KnowledgeItem> {
    const response = await this.client.post<KnowledgeItem>('/', data);
    return response.data;
  }

  /**
   * 上传文件
   */
  async upload(file: File, metadata: { title: string; category: string; tags?: string[] }): Promise<KnowledgeItem> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', metadata.title);
    formData.append('category', metadata.category);
    if (metadata.tags) {
      formData.append('tags', JSON.stringify(metadata.tags));
    }

    const response = await this.client.post<KnowledgeItem>('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  }

  /**
   * 更新知识
   */
  async update(id: string, data: UpdateKnowledgeRequest): Promise<KnowledgeItem> {
    const response = await this.client.put<KnowledgeItem>(`/${id}`, data);
    return response.data;
  }

  /**
   * 删除知识
   */
  async delete(id: string): Promise<void> {
    await this.client.delete(`/${id}`);
  }

  /**
   * 语义搜索
   */
  async search(request: SearchRequest): Promise<SearchResult[]> {
    const response = await this.client.post<SearchResult[]>('/search', request);
    return response.data;
  }

  /**
   * 获取所有标签
   */
  async getTags(): Promise<string[]> {
    const response = await this.client.get<string[]>('/tags');
    return response.data;
  }
}

export const knowledgeApi = new KnowledgeApiService();
export type { KnowledgeItem, KnowledgeListResponse, SearchResult };
