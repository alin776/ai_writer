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
  AnalysisStatusResponse,
  AnalysisResultResponse,
  StartAnalysisResponse,
  NotificationSettings,
  UserPreferences,
  UserSession,
  AICallLog,
  AICallLogPaginatedResponse,
  AICallLogStats,
  CostMetrics,
} from '@/types';
import type { SearchResponse } from '@/types/search';
import type { WorldData, Setting, Character, Location } from '@/types/novel';
import type {
  ExportOptions,
  ExportResponse,
  ImportOptions,
  ImportPreviewResponse,
  ImportResponse
} from '@/types/export';
import type {
  TimelineEvent,
  CreateTimelineEventData,
  UpdateTimelineEventData,
  ChapterAnchor
} from '@/types/timeline';
import type {
  Relationship,
  CreateRelationshipData,
  UpdateRelationshipData
} from '@/types/relationship';
import type {
  EntityGroup,
  CreateEntityGroupData,
  UpdateEntityGroupData,
  GroupMember,
  CreateGroupMemberData
} from '@/types/group';

type WorkGuidelines = Record<string, unknown>;
type AdminStatistics = {
  users?: { total?: number; change?: string };
  works?: { total?: number; change?: string };
  aiCalls?: { total?: number; change?: string };
  ai_calls?: { total?: number; change?: string };
  cost?: { total?: number; change?: string };
  [key: string]: any;
};
type UsersGrowthPoint = { date: string; count?: number; total?: number };
type UsersGrowthResponse = { data?: UsersGrowthPoint[] } | UsersGrowthPoint[];
type AIUsagePoint = { date: string; calls: number; cost: number };
type AIUsageResponse = { data?: AIUsagePoint[] } | AIUsagePoint[];
type RecentActivity = { id?: string; type?: string; message?: string; createdAt?: string; [key: string]: any };

class DataServiceClass {
  private adapter: IDataAdapter;

  // P2修复: 请求去重 - 防止同一章节短时间内多次更新
  private pendingChapterUpdates: Map<string, Promise<Chapter>> = new Map();

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

  /**
   * 更新当前用户信息
   * @param data 更新数据
   * @returns Promise<User>
   */
  async updateUserProfile(data: {
    username?: string;
    email?: string;
    fullName?: string;
    bio?: string;
    website?: string;
  }): Promise<User> {
    return this.adapter.put('/users/me', data);
  }

  /**
   * 获取通知设置
   * @returns Promise<NotificationSettings>
   */
  async getNotificationSettings(): Promise<NotificationSettings> {
    return this.adapter.get('/users/me/notification-settings');
  }

  /**
   * 更新通知设置
   * @param settings 通知配置
   * @returns Promise<NotificationSettings>
   */
  async updateNotificationSettings(settings: NotificationSettings): Promise<NotificationSettings> {
    return this.adapter.put('/users/me/notification-settings', settings);
  }

  /**
   * 获取偏好设置
   * @returns Promise<UserPreferences>
   */
  async getPreferences(): Promise<UserPreferences> {
    return this.adapter.get('/users/me/preferences');
  }

  /**
   * 更新偏好设置
   * @param preferences 偏好配置
   * @returns Promise<UserPreferences>
   */
  async updatePreferences(preferences: UserPreferences): Promise<UserPreferences> {
    return this.adapter.put('/users/me/preferences', preferences);
  }

  /**
   * 修改密码
   * @param currentPassword 当前密码
   * @param newPassword 新密码
   * @returns Promise<string> 提示消息
   */
  async changePassword(currentPassword: string, newPassword: string): Promise<string> {
    const response = await this.adapter.post<{ detail: string }>('/users/me/change-password', {
      currentPassword,
      newPassword,
    });
    return response.detail;
  }

  /**
   * 删除账号
   * @param password 密码确认
   */
  async deleteAccount(password: string): Promise<void> {
    await this.adapter.delete('/users/me', { password });
  }

  /**
   * 上传头像
   * @param file 头像文件
   * @returns Promise<string> 头像地址
   */
  async uploadAvatar(file: File): Promise<string> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await this.adapter.post<{ avatarUrl: string }>('/users/me/avatar', formData);
    return response.avatarUrl;
  }

  /**
   * 获取当前用户的活跃会话列表
   * @returns Promise<UserSession[]>
   */
  async getSessions(): Promise<UserSession[]> {
    return this.adapter.get('/users/me/sessions');
  }

  /**
   * 注销指定会话
   * @param sessionId 会话 ID
   */
  async logoutSession(sessionId: string): Promise<void> {
    await this.adapter.delete(`/users/me/sessions/${sessionId}`);
  }

  /**
   * 注销除当前会话外的所有会话
   */
  async logoutOtherSessions(): Promise<void> {
    await this.adapter.post('/users/me/sessions/logout-others');
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
   *
   * P2修复: 添加请求去重，防止同一章节短时间内多次更新
   */
  async updateChapter(id: string, chapter: Partial<Chapter>): Promise<Chapter> {
    // 如果同一章节已有pending请求，等待它完成后再发送新请求
    const pendingRequest = this.pendingChapterUpdates.get(id);
    if (pendingRequest) {
      console.log(`[DataService] 章节 ${id} 已有pending请求，等待完成...`);
      try {
        await pendingRequest;
      } catch {
        // 忽略之前请求的错误
      }
    }

    // 创建新请求
    const request = this.adapter.put<Chapter>(`/chapters/${id}`, chapter);
    this.pendingChapterUpdates.set(id, request);

    try {
      const result = await request;
      return result;
    } finally {
      // 请求完成后清除
      this.pendingChapterUpdates.delete(id);
    }
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
   * AI 剧情概括（返回JSON对象）- 已废弃，请使用 generateChapterSummary
   * @deprecated
   * @param request 概括请求
   * @returns Promise<string>
   */
  async aiSummarize(request: AISummaryRequest): Promise<string> {
    console.log('[DataService.aiSummarize] 请求参数:', request);
    const response = await this.adapter.post<{ summary: string }>('/ai/summarize', request);
    console.log('[DataService.aiSummarize] 响应数据:', response);
    return response.summary;
  }

  /**
   * 生成章节剧情概括（会自动保存到数据库）
   * @param chapterId 章节ID
   * @param regenerate 是否强制重新生成
   * @returns Promise<string> 章节概括
   */
  async generateChapterSummary(chapterId: string, regenerate: boolean = false): Promise<string> {
    console.log('[DataService.generateChapterSummary] chapterId:', chapterId, 'regenerate:', regenerate);
    const response = await this.adapter.post<{ summary: string }>(
      `/chapters/${chapterId}/summary?regenerate=${regenerate}`,
      {}
    );
    console.log('[DataService.generateChapterSummary] 响应数据:', response);
    return response.summary;
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
  async getGuidelines(workId: string): Promise<WorkGuidelines | null> {
    try {
      const result = await this.adapter.get<WorkGuidelines | null>(`/worldview/works/${workId}/guidelines`);
      return result ?? null;
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
  async saveGuidelines(workId: string, guidelines: WorkGuidelines): Promise<WorkGuidelines> {
    return this.adapter.post<WorkGuidelines>(`/worldview/works/${workId}/guidelines`, guidelines);
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
  async getAIGuidelines(workId: string): Promise<WorkGuidelines | null> {
    try {
      // ApiAdapter 已经自动将 snake_case 转换为 camelCase，直接返回
      const data = await this.adapter.get<WorkGuidelines | null>(`/worldview/works/${workId}/ai-guidelines`);
      return data ?? null;
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
  async saveAIGuidelines(workId: string, guidelines: WorkGuidelines): Promise<WorkGuidelines> {
    // ApiAdapter 会自动处理字段名转换，直接发送 camelCase 数据
    // 后端会接收到 snake_case（由 Pydantic 自动处理）
    return this.adapter.post<WorkGuidelines>(`/worldview/works/${workId}/ai-guidelines`, guidelines);
  }

  /**
   * 创建或更新AI规范（别名方法）
   * @param workId 作品ID
   * @param guidelines AI规范数据（31个字段）
   */
  async createOrUpdateAIGuidelines(workId: string, guidelines: WorkGuidelines): Promise<WorkGuidelines> {
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
      guidelines: guidelines ?? undefined,
      aiGuidelines: aiGuidelines ?? undefined
    };
  }

  // ==================== 用户管理相关 ====================

  /**
   * 获取所有用户
   * @returns Promise<User[]>
   */
  async getUsers(): Promise<User[]> {
    const response = await this.adapter.get<User[] | { items: User[]; total?: number }>('/users');
    return Array.isArray(response) ? response : (response.items || []);
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

  /**
   * 封禁用户
   * @param id 用户ID
   * @returns Promise<void>
   */
  async banUser(id: string): Promise<void> {
    return this.adapter.patch(`/admin/users/${id}/ban`);
  }

  /**
   * 解封用户
   * @param id 用户ID
   * @returns Promise<void>
   */
  async unbanUser(id: string): Promise<void> {
    return this.adapter.patch(`/admin/users/${id}/unban`);
  }

  /**
   * 切换用户管理员角色
   * @param id 用户ID
   * @returns Promise<void>
   */
  async toggleAdminRole(id: string): Promise<void> {
    return this.adapter.patch(`/admin/users/${id}/toggle-admin`);
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

  // ==================== 成本统计（旧版，已废弃） ====================

  /**
   * 获取成本统计数据（旧版，已废弃）
   * @deprecated 请使用 AI 日志部分的 getCostMetrics() 方法
   * @returns Promise<CostMetric[]>
   */
  async getOldCostMetrics(): Promise<CostMetric[]> {
    return this.adapter.get('/cost-metrics');
  }

  // ==================== 管理后台统计 ====================

  /**
   * 获取系统统计数据
   * @returns Promise<AdminStatistics>
   */
  async getAdminStatistics(): Promise<AdminStatistics> {
    return this.adapter.get('/admin/statistics');
  }

  /**
   * 获取用户增长趋势
   * @param days 统计天数（默认7天）
   * @returns Promise<any>
   */
  async getUsersGrowth(days: number = 7): Promise<UsersGrowthResponse> {
    return this.adapter.get(`/admin/users-growth?days=${days}`);
  }

  /**
   * 获取 AI 使用统计
   * @returns Promise<any>
   */
  async getAIUsage(): Promise<AIUsageResponse> {
    return this.adapter.get('/admin/ai-usage');
  }

  /**
   * 获取最近活动
   * @param limit 返回记录数量（默认10条）
   * @returns Promise<any>
   */
  async getRecentActivities(limit: number = 10): Promise<RecentActivity[]> {
    return this.adapter.get(`/admin/recent-activities?limit=${limit}`);
  }

  // ==================== 小说分析相关方法 ====================

  /**
   * 触发小说分析
   * @param workId 作品ID
   * @returns Promise<StartAnalysisResponse>
   */
  async startNovelAnalysis(workId: string): Promise<StartAnalysisResponse> {
    return this.adapter.post(`/analysis/works/${workId}/start`, {});
  }

  /**
   * 查询分析状态
   * @param workId 作品ID
   * @returns Promise<AnalysisStatusResponse>
   */
  async getAnalysisStatus(workId: string): Promise<AnalysisStatusResponse> {
    return this.adapter.get(`/analysis/works/${workId}/status`);
  }

  /**
   * 获取分析结果
   * @param workId 作品ID
   * @returns Promise<AnalysisResultResponse>
   */
  async getAnalysisResult(workId: string): Promise<AnalysisResultResponse> {
    return this.adapter.get(`/analysis/works/${workId}/result`);
  }

  /**
   * 删除分析数据
   * @param workId 作品ID
   * @returns Promise<void>
   */
  async deleteAnalysis(workId: string): Promise<void> {
    return this.adapter.delete(`/analysis/works/${workId}`);
  }

  /**
   * 从分析结果提取世界观数据
   * @param workId 作品ID
   * @param options 提取选项
   * @returns Promise<{characters: {created: number, updated: number}, locations: {created: number, updated: number}, settings: {created: number, updated: number}}>
   */
  async extractWorldviewFromAnalysis(
    workId: string,
    options?: {
      extractCharacters?: boolean;
      extractLocations?: boolean;
      extractSettings?: boolean;
    }
  ): Promise<{
    characters: { created: number; updated: number };
    locations: { created: number; updated: number };
    settings: { created: number; updated: number };
  }> {
    const params = new URLSearchParams();
    if (options?.extractCharacters !== undefined) {
      params.append('extract_characters', String(options.extractCharacters));
    }
    if (options?.extractLocations !== undefined) {
      params.append('extract_locations', String(options.extractLocations));
    }
    if (options?.extractSettings !== undefined) {
      params.append('extract_settings', String(options.extractSettings));
    }
    
    const url = `/analysis/works/${workId}/extract-worldview${params.toString() ? `?${params.toString()}` : ''}`;
    return this.adapter.post(url, {});
  }

  // ==================== 搜索相关 ====================

  /**
   * 全局搜索
   * @param query 搜索关键词
   * @param type 搜索类型（可选）
   * @param workId 限定作品ID（可选）
   * @param limit 每类最大结果数
   * @returns Promise<SearchResponse>
   */
  async globalSearch(
    query: string,
    type?: string,
    workId?: string,
    limit: number = 10
  ): Promise<SearchResponse> {
    const params = new URLSearchParams({ q: query, limit: limit.toString() });
    if (type) params.append('type', type);
    if (workId) params.append('work_id', workId);

    return this.adapter.get(`/search?${params.toString()}`);
  }

  // ==================== 导出相关 ====================

  /**
   * 导出作品
   * @param workId 作品ID
   * @param options 导出选项
   * @returns Promise<ExportResponse>
   */
  async exportWork(workId: string, options: ExportOptions): Promise<ExportResponse> {
    return this.adapter.post(`/works/${workId}/export`, options);
  }

  /**
   * 下载导出的文件（返回下载URL）
   * @param fileId 文件ID
   * @returns 下载URL
   */
  getDownloadUrl(fileId: string): string {
    // baseUrl已经包含/api/v1（来自.env的VITE_API_BASE_URL），所以直接拼接/downloads
    const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    return `${baseUrl}/downloads/${fileId}`;
  }

  /**
   * 删除导出的临时文件
   * @param fileId 文件ID
   */
  async deleteExportFile(fileId: string): Promise<void> {
    return this.adapter.delete(`/downloads/${fileId}`);
  }

  // ==================== 关系管理相关 ====================

  /**
   * 获取作品的所有关系
   * @param workId 作品ID
   * @returns Promise<Relationship[]>
   */
  async getRelationships(workId: string): Promise<Relationship[]> {
    const response = await this.adapter.get<{ items: Relationship[]; total: number }>(`/relationships/work/${workId}`);
    return response.items || [];
  }

  /**
   * 创建关系
   * @param relationship 关系数据
   * @returns Promise<any>
   */
  async createRelationship(relationship: CreateRelationshipData): Promise<Relationship> {
    return this.adapter.post('/relationships', relationship);
  }

  /**
   * 更新关系
   * @param id 关系ID
   * @param relationship 更新的数据
   * @returns Promise<any>
   */
  async updateRelationship(id: string, relationship: UpdateRelationshipData): Promise<Relationship> {
    return this.adapter.put(`/relationships/${id}`, relationship);
  }

  /**
   * 删除关系
   * @param id 关系ID
   * @returns Promise<void>
   */
  async deleteRelationship(id: string): Promise<void> {
    return this.adapter.delete(`/relationships/${id}`);
  }

  // ==================== 导入相关 ====================

  /**
   * 预览导入数据
   * @param file 文件对象
   * @param format 文件格式
   * @returns Promise<ImportPreviewResponse>
   */
  async previewImport(file: File, format: string): Promise<ImportPreviewResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('format', format);
    
    return this.adapter.post('/works/import/preview', formData);
  }

  /**
   * 导入作品
   * @param file 文件对象
   * @param options 导入选项
   * @returns Promise<ImportResponse>
   */
  async importWork(file: File, options: ImportOptions): Promise<ImportResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('format', options.format);
    formData.append('create_new', String(options.createNew));
    formData.append('include_worldview', String(options.includeWorldview));
    formData.append('include_guidelines', String(options.includeGuidelines));
    
    if (options.workId) {
      formData.append('work_id', options.workId);
    }
    
    return this.adapter.post('/works/import', formData);
  }

  // ==================== 时间线相关方法 ====================

  /**
   * 创建时间线事件
   * @param eventData 事件数据
   * @returns Promise<TimelineEvent>
   */
  async createTimelineEvent(eventData: CreateTimelineEventData): Promise<TimelineEvent> {
    return this.adapter.post('/timeline/', eventData);
  }

  /**
   * 获取时间线事件详情
   * @param eventId 事件ID
   * @returns Promise<TimelineEvent>
   */
  async getTimelineEvent(eventId: string): Promise<TimelineEvent> {
    return this.adapter.get(`/timeline/${eventId}`);
  }

  /**
   * 获取作品的所有时间线事件
   * @param workId 作品ID
   * @returns Promise<TimelineEvent[]>
   */
  async getTimelineEvents(workId: string): Promise<TimelineEvent[]> {
    const response = await this.adapter.get<{ items?: TimelineEvent[] }>(`/timeline/work/${workId}`);
    return response?.items || [];
  }

  /**
   * 更新时间线事件
   * @param eventId 事件ID
   * @param eventData 更新数据
   * @returns Promise<TimelineEvent>
   */
  async updateTimelineEvent(eventId: string, eventData: UpdateTimelineEventData): Promise<TimelineEvent> {
    return this.adapter.put(`/timeline/${eventId}`, eventData);
  }

  /**
   * 删除时间线事件
   * @param eventId 事件ID
   * @returns Promise<void>
   */
  async deleteTimelineEvent(eventId: string): Promise<void> {
    return this.adapter.delete(`/timeline/${eventId}`);
  }

  /**
   * 获取作品的章节锚点列表
   * @param workId 作品ID
   * @returns Promise<ChapterAnchor[]>
   */
  async getChapterAnchors(workId: string): Promise<ChapterAnchor[]> {
    return this.adapter.get(`/timeline/work/${workId}/chapter-anchors`);
  }

  // ==================== 实体分组管理 ====================

  /**
   * 创建实体分组
   * @param groupData 分组数据
   * @returns Promise<EntityGroup>
   */
  async createGroup(groupData: CreateEntityGroupData): Promise<EntityGroup> {
    return this.adapter.post('/groups/', groupData);
  }

  /**
   * 获取分组详情
   * @param groupId 分组ID
   * @returns Promise<EntityGroup>
   */
  async getGroup(groupId: string): Promise<EntityGroup> {
    return this.adapter.get(`/groups/${groupId}`);
  }

  /**
   * 获取作品的所有分组
   * @param workId 作品ID
   * @returns Promise<EntityGroup[]>
   */
  async getWorkGroups(workId: string): Promise<EntityGroup[]> {
    return this.adapter.get(`/groups/work/${workId}`);
  }

  /**
   * 更新分组信息
   * @param groupId 分组ID
   * @param groupData 更新数据
   * @returns Promise<EntityGroup>
   */
  async updateGroup(groupId: string, groupData: UpdateEntityGroupData): Promise<EntityGroup> {
    return this.adapter.put(`/groups/${groupId}`, groupData);
  }

  /**
   * 删除分组
   * @param groupId 分组ID
   * @returns Promise<void>
   */
  async deleteGroup(groupId: string): Promise<void> {
    return this.adapter.delete(`/groups/${groupId}`);
  }

  /**
   * 批量添加分组成员
   * @param groupId 分组ID
   * @param members 成员列表
   * @returns Promise<GroupMember[]>
   */
  async addGroupMembers(groupId: string, members: CreateGroupMemberData[]): Promise<GroupMember[]> {
    return this.adapter.post(`/groups/${groupId}/members`, { members });
  }

  /**
   * 移除分组成员
   * @param groupId 分组ID
   * @param memberId 成员ID
   * @returns Promise<void>
   */
  async removeGroupMember(groupId: string, memberId: string): Promise<void> {
    return this.adapter.delete(`/groups/${groupId}/members/${memberId}`);
  }

  /**
   * 批量移除分组成员
   * @param groupId 分组ID
   * @param memberIds 成员ID列表
   * @returns Promise<void>
   */
  async batchRemoveGroupMembers(groupId: string, memberIds: string[]): Promise<void> {
    return this.adapter.post(`/groups/${groupId}/members/batch-remove`, { memberIds });
  }

  // ==================== AI调用日志相关 ====================

  /**
   * 获取当前用户的AI调用日志（分页）
   * @param params 查询参数
   * @returns Promise<AICallLogPaginatedResponse>
   */
  async getMyAILogs(params?: {
    skip?: number;
    limit?: number;
    startDate?: string;
    endDate?: string;
  }): Promise<AICallLogPaginatedResponse> {
    const queryParams = new URLSearchParams();
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.startDate) queryParams.append('start_date', params.startDate);
    if (params?.endDate) queryParams.append('end_date', params.endDate);

    const url = `/ai-logs/me${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
    return this.adapter.get(url);
  }

  /**
   * 获取当前用户的AI使用统计
   * @param days 统计天数（默认30天）
   * @returns Promise<AICallLogStats>
   */
  async getMyAIStats(days: number = 30): Promise<AICallLogStats> {
    return this.adapter.get(`/ai-logs/me/stats?days=${days}`);
  }

  /**
   * 获取所有用户的AI使用统计（仅管理员）
   * @param days 统计天数（默认30天）
   * @returns Promise<AICallLogStats>
   */
  async getAllAIStats(days: number = 30): Promise<AICallLogStats> {
    return this.adapter.get(`/ai-logs/admin/stats?days=${days}`);
  }

  /**
   * 获取成本指标（仅管理员）- 核心方法
   * @returns Promise<CostMetrics>
   */
  async getCostMetrics(): Promise<CostMetrics> {
    return this.adapter.get('/ai-logs/admin/cost-metrics');
  }

  /**
   * 获取指定用户的AI调用日志（仅管理员）
   * @param userId 用户ID
   * @param params 查询参数
   * @returns Promise<AICallLog[]>
   */
  async getUserAILogs(userId: string, params?: {
    skip?: number;
    limit?: number;
    startDate?: string;
    endDate?: string;
  }): Promise<AICallLog[]> {
    const queryParams = new URLSearchParams();
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.startDate) queryParams.append('start_date', params.startDate);
    if (params?.endDate) queryParams.append('end_date', params.endDate);

    const url = `/ai-logs/admin/user/${userId}/logs${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
    return this.adapter.get(url);
  }

  /**
   * 获取指定用户的AI使用统计（仅管理员）
   * @param userId 用户ID
   * @param days 统计天数（默认30天）
   * @returns Promise<AICallLogStats>
   */
  async getUserAIStats(userId: string, days: number = 30): Promise<AICallLogStats> {
    return this.adapter.get(`/ai-logs/admin/user/${userId}/stats?days=${days}`);
  }
}

// 导出单例
export const DataService = new DataServiceClass();
