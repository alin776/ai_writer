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
    // 开发环境使用 MockAdapter，生产环境使用 ApiAdapter
    const useMock = import.meta.env.MODE !== 'production' || import.meta.env.VITE_USE_MOCK === 'true';

    this.adapter = useMock ? new MockAdapter() : new ApiAdapter();

    console.log(`[DataService] 使用 ${useMock ? 'Mock' : 'Real API'} 数据源`);
  }

  // ==================== 认证相关 ====================

  /**
   * 登录
   * @param credentials 登录凭证
   * @returns Promise<AuthResponse>
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    return this.adapter.post('/auth/login', credentials);
  }

  /**
   * 注册
   * @param data 注册数据
   * @returns Promise<AuthResponse>
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    return this.adapter.post('/auth/register', data);
  }

  /**
   * 获取当前用户信息
   * @returns Promise<User>
   */
  async getCurrentUser(): Promise<User> {
    return this.adapter.get('/auth/me');
  }

  /**
   * 登出
   */
  async logout(): Promise<void> {
    localStorage.removeItem('token');
  }

  // ==================== 作品相关 ====================

  /**
   * 获取所有作品
   * @returns Promise<Work[]>
   */
  async getWorks(): Promise<Work[]> {
    return this.adapter.get('/works');
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
    return this.adapter.get(`/works/${workId}/chapters`);
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
    return this.adapter.get(`/works/${workId}/characters`);
  }

  /**
   * 创建角色
   * @param character 角色数据
   * @returns Promise<Character>
   */
  async createCharacter(character: Partial<Character>): Promise<Character> {
    return this.adapter.post('/characters', character);
  }

  /**
   * 更新角色
   * @param id 角色ID
   * @param character 更新的数据
   * @returns Promise<Character>
   */
  async updateCharacter(id: string, character: Partial<Character>): Promise<Character> {
    return this.adapter.put(`/characters/${id}`, character);
  }

  /**
   * 获取作品的所有地点
   * @param workId 作品ID
   * @returns Promise<Location[]>
   */
  async getLocations(workId: string): Promise<Location[]> {
    return this.adapter.get(`/works/${workId}/locations`);
  }

  /**
   * 创建地点
   * @param location 地点数据
   * @returns Promise<Location>
   */
  async createLocation(location: Partial<Location>): Promise<Location> {
    return this.adapter.post('/locations', location);
  }

  /**
   * 更新地点
   * @param id 地点ID
   * @param location 更新的数据
   * @returns Promise<Location>
   */
  async updateLocation(id: string, location: Partial<Location>): Promise<Location> {
    return this.adapter.put(`/locations/${id}`, location);
  }

  /**
   * 删除地点
   * @param id 地点ID
   * @returns Promise<void>
   */
  async deleteLocation(id: string): Promise<void> {
    return this.adapter.delete(`/locations/${id}`);
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
    return this.adapter.get(`/works/${workId}/settings`);
  }

  /**
   * 创建设定
   * @param setting 设定数据
   * @returns Promise<Setting>
   */
  async createSetting(setting: Partial<Setting>): Promise<Setting> {
    return this.adapter.post('/settings', setting);
  }

  /**
   * 更新设定
   * @param id 设定ID
   * @param setting 更新的数据
   * @returns Promise<Setting>
   */
  async updateSetting(id: string, setting: Partial<Setting>): Promise<Setting> {
    return this.adapter.put(`/settings/${id}`, setting);
  }

  /**
   * 删除设定
   * @param id 设定ID
   * @returns Promise<void>
   */
  async deleteSetting(id: string): Promise<void> {
    return this.adapter.delete(`/settings/${id}`);
  }

  /**
   * 获取作品的世界观数据
   * @param workId 作品ID
   * @returns Promise<WorldData>
   */
  async getWorldData(workId: string): Promise<WorldData> {
    const [characters, locations, settings] = await Promise.all([
      this.getCharacters(workId),
      this.getLocations(workId),
      this.getSettings(workId),
    ]);
    return { characters, locations, settings };
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
