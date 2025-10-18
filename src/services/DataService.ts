/**
 * 数据服务统一接口
 *
 * 所有组件必须通过此服务访问数据，禁止直接导入 Mock 数据
 * 通过适配器模式实现 Mock 和真实 API 的无缝切换
 *
 * 未来 API 替换步骤：
 * 1. 实现 ApiAdapter.ts（已预留）
 * 2. 修改下方构造函数中的环境判断逻辑
 * 3. 在 .env.production 中配置 VITE_API_BASE_URL
 * 4. 无需修改任何组件代码
 */
import { MockAdapter } from './MockAdapter';
import { ApiAdapter } from './ApiAdapter';
import type { IDataAdapter } from './IDataAdapter';
import type {
  Work,
  Chapter,
  User,
  AIModel,
  Item,
  AuthResponse,
  TokenResponse,
  LoginCredentials,
  RegisterData,
  CreateWorkData,
  CreateChapterData,
  AIContinueRequest,
  AIContinueResponse,
  AIPolishRequest,
  AISummaryRequest,
  CostMetric,
} from '@/types';
import type { WorldData, Setting, Character, Location } from '@/types/novel';

class DataServiceClass {
  private adapter: IDataAdapter;

  constructor() {
    // 根据环境变量决定使用 Mock 还是真实 API
    // VITE_USE_MOCK=false 时使用真实 API
    // VITE_USE_MOCK=true 时使用 Mock 数据
    const useMock = import.meta.env.VITE_USE_MOCK === 'true';

    this.adapter = useMock ? new MockAdapter() : new ApiAdapter();

    console.log(`[DataService] 使用 ${useMock ? 'Mock' : 'Real API'} 数据源`);
    console.log(`[DataService] VITE_USE_MOCK = ${import.meta.env.VITE_USE_MOCK}`);
    console.log(`[DataService] VITE_API_BASE_URL = ${import.meta.env.VITE_API_BASE_URL}`);
  }

  // ==================== 认证相关 ====================

  /**
   * 登录
   * @param credentials 登录凭证
   * @returns Promise<TokenResponse>
   */
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    return this.adapter.post('/auth/login', credentials);
  }

  /**
   * 注册
   * @param data 注册数据
   * @returns Promise<User>
   */
  async register(data: RegisterData): Promise<User> {
    return this.adapter.post('/auth/register', data);
  }

  /**
   * 获取当前用户信息
   * @returns Promise<User>
   */
  async getCurrentUser(): Promise<User> {
    return this.adapter.get('/users/me');
  }

  /**
   * 登出
   */
  async logout(): Promise<void> {
    localStorage.removeItem('auth-storage');
  }

  // ==================== 作品相关 ====================

  /**
   * 获取所有作品
   * @returns Promise<Work[]>
   */
  async getWorks(): Promise<Work[]> {
    // 后端返回分页格式：{ total, page, page_size, items }
    const response = await this.adapter.get<{ items: Work[]; total: number }>('/works');
    return response.items || [];
  }

  /**
   * 获取单个作品详情
   * @param id 作品ID
   * @returns Promise<Work>
   */
  async getWork(id: string): Promise<Work> {
    return this.adapter.get(`/works/${id}`);
  }

  /**
   * 创建作品
   * @param work 作品数据
   * @returns Promise<Work>
   */
  async createWork(work: CreateWorkData): Promise<Work> {
    return this.adapter.post('/works', work);
  }

  /**
   * 更新作品
   * @param id 作品ID
   * @param work 更新的数据
   * @returns Promise<Work>
   */
  async updateWork(id: string, work: Partial<Work>): Promise<Work> {
    return this.adapter.put(`/works/${id}`, work);
  }

  /**
   * 删除作品
   * @param id 作品ID
   * @returns Promise<void>
   */
  async deleteWork(id: string): Promise<void> {
    return this.adapter.delete(`/works/${id}`);
  }

  // ==================== 章节相关 ====================

  /**
   * 获取作品的所有章节
   * @param workId 作品ID
   * @returns Promise<Chapter[]>
   */
  async getChapters(workId: string): Promise<Chapter[]> {
    const response = await this.adapter.get<Chapter[] | { items: Chapter[] }>(`/chapters/work/${workId}`);
    return Array.isArray(response) ? response : (response.items || []);
  }

  /**
   * 获取单个章节
   * @param id 章节ID
   * @returns Promise<Chapter>
   */
  async getChapter(id: string): Promise<Chapter> {
    return this.adapter.get(`/chapters/${id}`);
  }

  /**
   * 创建章节
   * @param chapter 章节数据
   * @returns Promise<Chapter>
   */
  async createChapter(chapter: CreateChapterData): Promise<Chapter> {
    return this.adapter.post('/chapters', chapter);
  }

  /**
   * 更新章节
   * @param id 章节ID
   * @param chapter 更新的数据
   * @returns Promise<Chapter>
   */
  async updateChapter(id: string, chapter: Partial<Chapter>): Promise<Chapter> {
    return this.adapter.put(`/chapters/${id}`, chapter);
  }

  /**
   * 删除章节
   * @param id 章节ID
   * @returns Promise<void>
   */
  async deleteChapter(id: string): Promise<void> {
    return this.adapter.delete(`/chapters/${id}`);
  }

  /**
   * 重新排序章节
   * @param workId 作品ID
   * @param chapterIds 章节ID列表（按新顺序）
   * @returns Promise<void>
   */
  async reorderChapters(workId: string, chapterIds: string[]): Promise<void> {
    return this.adapter.post('/chapters/reorder', {
      work_id: workId,
      chapter_ids: chapterIds
    });
  }

  // ==================== AI 相关 ====================

  /**
   * AI 续写
   * @param request 续写请求
   * @returns Promise<AIContinueResponse>
   */
  async aiContinue(request: AIContinueRequest): Promise<AIContinueResponse> {
    return this.adapter.post('/ai/continue', request);
  }

  /**
   * AI 润色
   * @param request 润色请求
   * @returns Promise<string>
   */
  async aiPolish(request: AIPolishRequest): Promise<string> {
    const response = await this.adapter.post<{ result: string }>('/ai/polish', request);
    return response.result;
  }

  /**
   * AI 摘要
   * @param request 摘要请求
   * @returns Promise<string>
   */
  async aiSummary(request: AISummaryRequest): Promise<string> {
    const response = await this.adapter.post<{ result: string }>('/ai/summary', request);
    return response.result;
  }

  // ==================== 世界观相关 ====================

  /**
   * 获取作品的所有角色
   * @param workId 作品ID
   * @returns Promise<Character[]>
   */
  async getCharacters(workId: string): Promise<Character[]> {
    return this.adapter.get(`/worldview/works/${workId}/characters`);
  }

  /**
   * 创建角色
   * @param character 角色数据
   * @returns Promise<Character>
   */
  async createCharacter(character: Partial<Character>): Promise<Character> {
    return this.adapter.post('/worldview/characters', character);
  }

  /**
   * 更新角色
   * @param id 角色ID
   * @param character 更新的数据
   * @returns Promise<Character>
   */
  async updateCharacter(id: string, character: Partial<Character>): Promise<Character> {
    return this.adapter.put(`/worldview/characters/${id}`, character);
  }

  /**
   * 删除角色
   * @param id 角色ID
   * @returns Promise<void>
   */
  async deleteCharacter(id: string): Promise<void> {
    return this.adapter.delete(`/worldview/characters/${id}`);
  }

  /**
   * 获取作品的所有地点
   * @param workId 作品ID
   * @returns Promise<Location[]>
   */
  async getLocations(workId: string): Promise<Location[]> {
    return this.adapter.get(`/worldview/works/${workId}/locations`);
  }

  /**
   * 创建地点
   * @param location 地点数据
   * @returns Promise<Location>
   */
  async createLocation(location: Partial<Location>): Promise<Location> {
    return this.adapter.post('/worldview/locations', location);
  }

  /**
   * 更新地点
   * @param id 地点ID
   * @param location 更新的数据
   * @returns Promise<Location>
   */
  async updateLocation(id: string, location: Partial<Location>): Promise<Location> {
    return this.adapter.put(`/worldview/locations/${id}`, location);
  }

  /**
   * 删除地点
   * @param id 地点ID
   * @returns Promise<void>
   */
  async deleteLocation(id: string): Promise<void> {
    return this.adapter.delete(`/worldview/locations/${id}`);
  }

  /**
   * 获取作品的所有道具
   * @param workId 作品ID
   * @returns Promise<Item[]>
   */
  async getItems(workId: string): Promise<Item[]> {
    return this.adapter.get(`/works/${workId}/items`);
  }

  /**
   * 获取作品的所有设定
   * @param workId 作品ID
   * @returns Promise<Setting[]>
   */
  async getSettings(workId: string): Promise<Setting[]> {
    return this.adapter.get(`/worldview/works/${workId}/settings`);
  }

  /**
   * 创建设定
   * @param setting 设定数据
   * @returns Promise<Setting>
   */
  async createSetting(setting: Partial<Setting>): Promise<Setting> {
    return this.adapter.post('/worldview/settings', setting);
  }

  /**
   * 更新设定
   * @param id 设定ID
   * @param setting 更新的数据
   * @returns Promise<Setting>
   */
  async updateSetting(id: string, setting: Partial<Setting>): Promise<Setting> {
    return this.adapter.put(`/worldview/settings/${id}`, setting);
  }

  /**
   * 删除设定
   * @param id 设定ID
   * @returns Promise<void>
   */
  async deleteSetting(id: string): Promise<void> {
    return this.adapter.delete(`/worldview/settings/${id}`);
  }

  /**
   * 获取作品规范
   * @param workId 作品ID
   * @returns Promise<WorkGuidelines | null>
   */
  async getGuidelines(workId: string): Promise<any | null> {
    try {
      const result = await this.adapter.get(`/worldview/works/${workId}/guidelines`);
      return result;
    } catch (error: any) {
      // 404说明还没创建规范，返回null（不要抛出异常影响其他数据）
      // error 可能是 {detail: 'Guidelines not found'} 或标准 axios 错误
      return null;
    }
  }

  /**
   * 创建或更新作品规范
   * @param workId 作品ID
   * @param guidelines 规范数据
   * @returns Promise<any>
   */
  async saveGuidelines(workId: string, guidelines: any): Promise<any> {
    return this.adapter.post(`/worldview/works/${workId}/guidelines`, guidelines);
  }

  /**
   * 删除作品规范
   * @param workId 作品ID
   * @returns Promise<void>
   */
  async deleteGuidelines(workId: string): Promise<void> {
    return this.adapter.delete(`/worldview/works/${workId}/guidelines`);
  }

  /**
   * 获取AI创作规范
   * @param workId 作品ID
   * @returns Promise<any | null>
   */
  async getAIGuidelines(workId: string): Promise<any | null> {
    try {
      // ApiAdapter 已经自动将 snake_case 转换为 camelCase，直接返回
      const data = await this.adapter.get(`/worldview/works/${workId}/ai-guidelines`);
      return data || null;
    } catch (error: any) {
      if (error?.response?.status === 404 || error?.status === 404) {
        return null;
      }
      throw error;
    }
  }

  /**
   * 创建或更新AI创作规范
   * @param workId 作品ID
   * @param guidelines AI规范数据（camelCase）
   * @returns Promise<any>
   */
  async saveAIGuidelines(workId: string, guidelines: any): Promise<any> {
    // ApiAdapter 会自动处理字段名转换，直接发送 camelCase 数据
    // 后端会接收到 snake_case（由 Pydantic 自动处理）
    return this.adapter.post(`/worldview/works/${workId}/ai-guidelines`, guidelines);
  }

  /**
   * 创建或更新AI规范（别名方法）
   * @param workId 作品ID
   * @param guidelines AI规范数据（31个字段）
   */
  async createOrUpdateAIGuidelines(workId: string, guidelines: any): Promise<any> {
    return this.saveAIGuidelines(workId, guidelines);
  }

  /**
   * 删除AI创作规范
   * @param workId 作品ID
   * @returns Promise<void>
   */
  async deleteAIGuidelines(workId: string): Promise<void> {
    return this.adapter.delete(`/worldview/works/${workId}/ai-guidelines`);
  }

  /**
   * 获取作品的世界观数据
   * @param workId 作品ID
   * @returns Promise<WorldData>
   */
  async getWorldData(workId: string): Promise<WorldData> {
    const [characters, locations, settings, guidelines, aiGuidelines] = await Promise.all([
      this.getCharacters(workId),
      this.getLocations(workId),
      this.getSettings(workId),
      this.getGuidelines(workId),
      this.getAIGuidelines(workId),
    ]);
    
    return { 
      characters, 
      locations, 
      settings, 
      guidelines: guidelines || undefined,
      aiGuidelines: aiGuidelines || undefined
    };
  }

  // ==================== 用户管理相关 ====================

  /**
   * 获取所有用户
   * @returns Promise<User[]>
   */
  async getUsers(): Promise<User[]> {
    return this.adapter.get('/users');
  }

  /**
   * 更新用户
   * @param id 用户ID
   * @param user 更新的数据
   * @returns Promise<User>
   */
  async updateUser(id: string, user: Partial<User>): Promise<User> {
    return this.adapter.put(`/users/${id}`, user);
  }

  // ==================== AI 模型管理 ====================

  /**
   * 获取所有 AI 模型
   * @returns Promise<AIModel[]>
   */
  async getAIModels(): Promise<AIModel[]> {
    return this.adapter.get('/ai-models');
  }

  /**
   * 创建 AI 模型
   * @param model 模型数据
   * @returns Promise<AIModel>
   */
  async createAIModel(model: Partial<AIModel>): Promise<AIModel> {
    return this.adapter.post('/ai-models', model);
  }

  /**
   * 更新 AI 模型
   * @param id 模型ID
   * @param model 更新的数据
   * @returns Promise<AIModel>
   */
  async updateAIModel(id: string, model: Partial<AIModel>): Promise<AIModel> {
    return this.adapter.put(`/ai-models/${id}`, model);
  }

  /**
   * 删除 AI 模型
   * @param id 模型ID
   * @returns Promise<void>
   */
  async deleteAIModel(id: string): Promise<void> {
    return this.adapter.delete(`/ai-models/${id}`);
  }

  // ==================== 成本统计 ====================

  /**
   * 获取成本统计数据
   * @returns Promise<CostMetric[]>
   */
  async getCostMetrics(): Promise<CostMetric[]> {
    return this.adapter.get('/cost-metrics');
  }
}

// 导出单例
export const DataService = new DataServiceClass();
