/**
 * 个人知识库 API 服务
 */

import axios, { AxiosInstance } from 'axios';

interface KnowledgeItem {
  id: string;
  title: string;
  content?: string;
  category?: string;
  source_type: 'manual' | 'book_analysis' | 'ai_generated' | 'imported' | 'text' | 'file' | 'url';
  file_type?: string;
  tags: string[];
  created_at: string;
  updated_at: string;
  chunk_count?: number;
  summary?: string;
  view_count?: number;
  reference_count?: number;
  extra_data?: Record<string, any>;
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
  top_k?: number;
  tags?: string[];
  category?: string;
  work_id?: string;
}

interface SearchResult {
  item: KnowledgeItem;
  relevance_score: number;
  highlight: string;
}

class KnowledgeApiService {
  private client: AxiosInstance;

  constructor() {
    const rawBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    const baseURL = import.meta.env.DEV ? '/api/v1' : rawBase;

    this.client = axios.create({
      baseURL: `${baseURL}/knowledge`,
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
   * @param params 查询参数
   * @param signal 可选的 AbortSignal，用于取消请求
   */
  async getList(params?: {
    search?: string;
    tags?: string[];
    page?: number;
    pageSize?: number;
    limit?: number;
    skip?: number;
    category?: string;
  }, signal?: AbortSignal): Promise<KnowledgeListResponse> {
    const page = params?.page ?? 1;
    const pageSize = params?.pageSize ?? params?.limit ?? 20;
    const skip = params?.skip ?? (page - 1) * pageSize;
    const limit = params?.limit ?? pageSize;
    // 使用空路径，避免带尾随斜杠触发 307 重定向导致 Authorization 可能丢失
    const response = await this.client.get<KnowledgeListResponse>('', {
      params: {
        search: params?.search,
        category: params?.category,
        tags: params?.tags?.length ? params.tags.join(',') : undefined,
        skip,
        limit,
      },
      signal,
    });
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
    const response = await this.client.post<KnowledgeItem>('', data);
    return response.data;
  }

  /**
   * 上传文件
   */
  async upload(file: File, metadata: { title: string; category: string; tags?: string[]; source_reference?: string }): Promise<KnowledgeItem> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', metadata.title);
    formData.append('category', metadata.category);
    if (metadata.source_reference) {
      formData.append('source_reference', metadata.source_reference);
    }
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
    const response = await this.client.post<{ results: SearchResult[] }>('/search', request);
    return response.data.results || [];
  }

  /**
   * 获取所有标签
   */
  async getTags(): Promise<string[]> {
    try {
      const response = await this.client.get<string[]>('/tags');
      return response.data || [];
    } catch (error: any) {
      if (error?.response?.status === 404) {
        return [];
      }
      // 静默处理网络错误，避免 UI 报红
      if (error?.message?.includes('Network Error')) {
        return [];
      }
      return [];
    }
  }

  /**
   * 获取知识库文档列表（id + title），用于@引用选择
   */
  async getDocTitles(): Promise<{ id: string; title: string }[]> {
    try {
      const response = await this.client.get<{ id: string; title: string }[]>('/titles');
      return response.data || [];
    } catch (error: any) {
      if (error?.response?.status === 404) {
        return [];
      }
      if (error?.message?.includes('Network Error')) {
        return [];
      }
      return [];
    }
  }
}

export const knowledgeApi = new KnowledgeApiService();
export type { KnowledgeItem, KnowledgeListResponse, SearchResult };
