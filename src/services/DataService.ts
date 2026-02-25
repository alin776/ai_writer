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
  Item,
  TokenResponse,
  LoginCredentials,
  RegisterData,
  CreateWorkData,
  CreateChapterData,
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
import type { ChapterRevision } from '@/types/revision';
import type { SearchResponse } from '@/types/search';
import type { WorldData, Setting, Character, Location, WorldviewChanges, ApplyChangesResult, WorldviewScanProgress } from '@/types/novel';
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
import type { WorkListResponse } from '@/types';

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
   * 更新用户在线状态
   * @param status 在线状态 (online, idle, dnd, offline)
   * @returns Promise<User>
   */
  async updateOnlineStatus(status: 'online' | 'idle' | 'dnd' | 'offline'): Promise<User> {
    return this.adapter.put('/users/me/status', { status });
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

  /**
   * 发送邮箱验证码
   * @param newEmail 新邮箱地址
   * @returns Promise<string> 提示消息
   */
  async sendEmailVerificationCode(newEmail: string): Promise<string> {
    const response = await this.adapter.post<{ detail: string }>('/users/me/send-email-code', {
      newEmail,
    });
    return response.detail;
  }

  /**
   * 验证并更新邮箱
   * @param newEmail 新邮箱地址
   * @param code 验证码
   * @returns Promise<User> 更新后的用户信息
   */
  async verifyAndUpdateEmail(newEmail: string, code: string): Promise<User> {
    return this.adapter.post<User>('/users/me/verify-and-update-email', {
      newEmail,
      code,
    });
  }

  // ==================== 作品相关 ====================

  /**
   * 获取所有作品
   * @returns Promise<WorkListResponse>
   */
  async getWorks(): Promise<WorkListResponse> {
    // 后端返回分页格式：{ total, page, page_size, items }
    const response = await this.adapter.get<WorkListResponse>('/works', { skip: 0, limit: 100 });
    return response;
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

  /**
   * 上传作品封面
   * @param workId 作品ID
   * @param file 封面图片文件
   * @returns Promise<string> 返回封面URL
   */
  async uploadWorkCover(workId: string, file: File): Promise<string> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.adapter.post<{ coverUrl: string }>(`/works/${workId}/cover`, formData);
    return response.coverUrl;
  }

  /**
   * 发布作品到小说广场
   * @param workId 作品ID
   * @param chapterNums 要发布的章节序号列表
   * @returns Promise<{ message: string; work_id: string; is_published: boolean }>
   */
  async publishWork(workId: string, chapterNums: number[]): Promise<{ message: string; work_id: string; is_published: boolean }> {
    return this.adapter.post(`/works/${workId}/publish`, { chapter_nums: chapterNums });
  }

  /**
   * 取消发布作品
   * @param workId 作品ID
   * @returns Promise<{ message: string; work_id: string; is_published: boolean }>
   */
  async unpublishWork(workId: string): Promise<{ message: string; work_id: string; is_published: boolean }> {
    return this.adapter.post(`/works/${workId}/unpublish`, {});
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
   * 获取章节待处理修订
   * @param chapterId 章节ID
   * @param status 修订状态（默认 pending）
   * @returns Promise<ChapterRevision[]>
   */
  async getChapterRevisions(chapterId: string, status: 'pending' = 'pending'): Promise<ChapterRevision[]> {
    return this.adapter.get(`/chapters/${chapterId}/revisions?status=${status}`);
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

  /**
   * 生成章节剧情概括（会自动保存到数据库）
   * @param chapterId 章节ID
   * @param regenerate 是否强制重新生成
   * @returns Promise<string> 章节概括
   */
  async generateChapterSummary(chapterId: string, regenerate: boolean = false): Promise<string> {
    const response = await this.adapter.post<{ summary: string }>(
      `/chapters/${chapterId}/summary?regenerate=${regenerate}`,
      {}
    );
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

  /**
   * 更新用户称号（管理员）
   * @param id 用户ID
   * @param honor 新称号（空字符串或 null 清除称号）
   * @returns Promise<{ message: string }>
   */
  async updateUserHonor(id: string, honor: string | null): Promise<{ message: string }> {
    return this.adapter.patch(`/admin/users/${id}/honor`, { honor });
  }

  // ==================== 管理员频道管理 ====================

  /**
   * 获取所有频道列表（管理员）
   * @param params 查询参数
   * @returns Promise<{ total: number; channels: Channel[] }>
   */
  async getAdminChannels(params?: {
    skip?: number;
    limit?: number;
    channel_type?: string;
    channel_status?: string;
    search?: string;
  }): Promise<{ total: number; channels: any[] }> {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.channel_type) queryParams.append('channel_type', params.channel_type);
    if (params?.channel_status) queryParams.append('channel_status', params.channel_status);
    if (params?.search) queryParams.append('search', params.search);

    const queryString = queryParams.toString();
    return this.adapter.get(`/admin/channels${queryString ? `?${queryString}` : ''}`);
  }

  /**
   * 更新频道状态（管理员）
   * @param channelId 频道ID
   * @param status 新状态 (active/warning/locked)
   * @returns Promise<{ message: string; channel: any }>
   */
  async updateChannelStatus(channelId: string, status: string): Promise<{ message: string; channel: any }> {
    return this.adapter.patch(`/admin/channels/${channelId}/status?new_status=${status}`);
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
    return this.adapter.post('/relationships/', relationship);
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

  /**
   * AI 生成关系标签和描述
   * @param data AI生成请求数据
   * @returns Promise<{ label: string; description: string }>
   */
  async aiGenerateRelationship(data: {
    workId: string;
    userInput: string;
    source: { id: string; name: string; type: string; description?: string };
    target: { id: string; name: string; type: string; description?: string };
    relationshipType: string;
    direction: 'one-way' | 'two-way';
  }): Promise<{ label: string; description: string }> {
    return this.adapter.post('/relationships/ai-generate', {
      work_id: data.workId,
      user_input: data.userInput,
      source: {
        id: data.source.id,
        name: data.source.name,
        type: data.source.type,
        description: data.source.description || null
      },
      target: {
        id: data.target.id,
        name: data.target.name,
        type: data.target.type,
        description: data.target.description || null
      },
      relationship_type: data.relationshipType,
      direction: data.direction
    });
  }

  /**
   * AI 生成实体信息（角色/地点/设定）
   * @param data AI生成请求数据
   * @returns Promise<{ name?: string; role?: string; description: string }>
   */
  async aiGenerateEntity(data: {
    workId: string;
    userInput: string;
    entityType: 'character' | 'location' | 'setting';
    entityName: string;
    entityRole?: string;
  }): Promise<{ name?: string; role?: string; description: string }> {
    return this.adapter.post('/worldview/ai-generate-entity', {
      work_id: data.workId,
      user_input: data.userInput,
      entity_type: data.entityType,
      entity_name: data.entityName,
      entity_role: data.entityRole || null
    });
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
    formData.append('include_guidelines', String(options.includeGuidelines));
    if (options.genre) {
      formData.append('genre', options.genre);
    }

    if (options.workId) {
      formData.append('work_id', options.workId);
    }

    return this.adapter.post('/works/import', formData);
  }

  /**
   * 获取世界观扫描进度（导入解析）
   * @param workId 作品ID
   */
  async getWorldviewScanProgress(workId: string): Promise<WorldviewScanProgress> {
    return this.adapter.get(`/works/${workId}/worldview/scan-progress`);
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

  // ========== 图书馆相关API ==========

  /**
   * 获取推荐作品列表(用于轮播图)
   */
  async getFeaturedNovels(): Promise<any> {
    return this.adapter.get('/library/featured');
  }

  /**
   * 获取小说广场的已发布作品列表
   */
  async getPublishedNovels(params?: {
    skip?: number;
    limit?: number;
    genre?: string;
    search?: string;
    sortBy?: 'latest' | 'popular' | 'words';
  }): Promise<any> {
    const queryParams = new URLSearchParams();
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.genre) queryParams.append('genre', params.genre);
    if (params?.search) queryParams.append('search', params.search);
    if (params?.sortBy) queryParams.append('sort_by', params.sortBy);

    return this.adapter.get(`/library/novels${queryParams.toString() ? `?${queryParams.toString()}` : ''}`);
  }

  /**
   * 获取已发布作品的详情
   */
  async getPublishedNovelDetail(workId: string): Promise<any> {
    return this.adapter.get(`/library/novels/${workId}`);
  }

  /**
   * 获取已发布章节的内容
   */
  async getPublishedChapterContent(workId: string, chapterId: string): Promise<any> {
    return this.adapter.get(`/library/novels/${workId}/chapters/${chapterId}`);
  }

  /**
   * 获取已发布小说的章节列表
   */
  async getNovelChapters(workId: string): Promise<any> {
    return this.adapter.get(`/library/novels/${workId}/chapters`);
  }

  // ========== 评论相关API ==========

  /**
   * 获取作品的评论列表
   */
  async getWorkComments(workId: string, params?: { skip?: number; limit?: number; sortBy?: 'newest' | 'most_liked' }): Promise<any> {
    const queryParams = new URLSearchParams();
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.sortBy) queryParams.append('sort_by', params.sortBy);

    return this.adapter.get(`/comments/works/${workId}/comments${queryParams.toString() ? `?${queryParams.toString()}` : ''}`);
  }

  /**
   * 发表评论
   */
  async createComment(workId: string, data: { content: string; parentId?: string; replyToUserId?: string }): Promise<any> {
    return this.adapter.post(`/comments/works/${workId}/comments`, {
      content: data.content,
      parent_id: data.parentId,
      reply_to_user_id: data.replyToUserId,
    });
  }

  /**
   * 更新评论
   */
  async updateComment(commentId: string, content: string): Promise<any> {
    return this.adapter.put(`/comments/comments/${commentId}`, { content });
  }

  /**
   * 删除评论
   */
  async deleteComment(commentId: string): Promise<void> {
    return this.adapter.delete(`/comments/comments/${commentId}`);
  }

  /**
   * 点赞评论
   */
  async likeComment(commentId: string): Promise<any> {
    return this.adapter.post(`/comments/comments/${commentId}/like`, {});
  }

  /**
   * 取消点赞评论
   */
  async unlikeComment(commentId: string): Promise<any> {
    return this.adapter.delete(`/comments/comments/${commentId}/like`);
  }

  /**
   * 踩评论
   */
  async dislikeComment(commentId: string): Promise<any> {
    return this.adapter.post(`/comments/comments/${commentId}/dislike`, {});
  }

  /**
   * 取消踩评论
   */
  async undislikeComment(commentId: string): Promise<any> {
    return this.adapter.delete(`/comments/comments/${commentId}/dislike`);
  }

  // ========== 书架相关API ==========

  /**
   * 获取我的书架
   */
  async getBookshelf(): Promise<any> {
    return this.adapter.get('/library/bookshelf');
  }

  /**
   * 将作品加入书架
   * @returns { message, workId, alreadyExists } - alreadyExists 为 true 时表示作品已在书架中
   */
  async addToBookshelf(workId: string): Promise<{ message: string; workId: string; alreadyExists: boolean }> {
    return this.adapter.post(`/library/bookshelf/${workId}`, {});
  }

  /**
   * 从书架移除作品
   */
  async removeFromBookshelf(workId: string): Promise<void> {
    return this.adapter.delete(`/library/bookshelf/${workId}`);
  }

  /**
   * 检查作品是否在书架中
   * 注意：ApiAdapter 会自动将 snake_case 转换为 camelCase
   */
  async checkInBookshelf(workId: string): Promise<{ workId: string; inBookshelf: boolean }> {
    return this.adapter.get(`/library/bookshelf/check/${workId}`);
  }

  /**
   * 获取作品的书友圈频道信息
   */
  async getWorkChannel(workId: string): Promise<{
    workId: string;
    hasChannel: boolean;
    channelId: string | null;
    channelName: string | null;
    channelStatus: 'active' | 'warning' | 'locked' | null;
    isMember: boolean;
  }> {
    return this.adapter.get(`/library/works/${workId}/channel`);
  }

  /**
   * 更新阅读进度
   */
  async updateReadingProgress(workId: string, chapterId: string, position: number = 0): Promise<any> {
    return this.adapter.put(`/library/bookshelf/${workId}/progress`, {
      chapter_id: chapterId,
      position,
    });
  }

  // ========== 评分相关API ==========

  /**
   * 为作品评分(如果已评分则更新)
   */
  async rateWork(workId: string, rating: number): Promise<any> {
    return this.adapter.post(`/ratings/works/${workId}/rating`, { rating });
  }

  /**
   * 获取作品评分统计
   */
  async getWorkRatingStats(workId: string): Promise<any> {
    return this.adapter.get(`/ratings/works/${workId}/rating/stats`);
  }

  /**
   * 删除作品评分
   */
  async deleteWorkRating(workId: string): Promise<void> {
    return this.adapter.delete(`/ratings/works/${workId}/rating`);
  }

  // ========== 举报相关API ==========

  /**
   * 举报评论
   */
  async reportComment(commentId: string, reason: string, description?: string): Promise<any> {
    return this.adapter.post(`/comments/comments/${commentId}/report`, {
      reason,
      description,
    });
  }

  /**
   * 举报作品
   */
  async reportWork(workId: string, reason: string, description?: string): Promise<any> {
    return this.adapter.post(`/library/works/${workId}/report`, {
      reason,
      description,
    });
  }

  // ========== 管理员 - 小说管理API ==========

  /**
   * 获取所有作品列表（管理员）
   */
  async adminGetAllWorks(params?: {
    skip?: number;
    limit?: number;
    search?: string;
    genre?: string;
    status?: string;
    isPublished?: boolean;
  }): Promise<any> {
    return this.adapter.get('/admin/works/works', params);
  }

  /**
   * 切换作品发布状态（管理员）
   */
  async adminToggleWorkPublish(workId: string, isPublished: boolean): Promise<any> {
    return this.adapter.put(`/admin/works/works/${workId}/publish`, {
      is_published: isPublished,
    });
  }

  /**
   * 切换作品推荐状态（管理员）
   */
  async adminToggleWorkFeatured(workId: string, isFeatured: boolean): Promise<any> {
    return this.adapter.put(`/admin/works/works/${workId}/feature`, {
      is_featured: isFeatured,
    });
  }

  /**
   * 删除作品（管理员）
   */
  async adminDeleteWork(workId: string): Promise<void> {
    return this.adapter.delete(`/admin/works/works/${workId}`);
  }

  // ==================== 举报管理 API ====================

  /**
   * 获取举报统计概览
   */
  async getReportsSummary(): Promise<any> {
    return this.adapter.get('/admin/reports/summary');
  }

  /**
   * 获取消息举报列表
   */
  async getMessageReports(status?: string): Promise<any> {
    return this.adapter.get('/admin/reports/messages', status ? { status } : undefined);
  }

  /**
   * 获取评论举报列表
   */
  async getCommentReports(isProcessed?: boolean): Promise<any> {
    return this.adapter.get('/admin/reports/comments', isProcessed !== undefined ? { is_processed: isProcessed } : undefined);
  }

  /**
   * 获取小说举报列表
   */
  async getWorkReports(status?: string): Promise<any> {
    return this.adapter.get('/admin/reports/works', status ? { status } : undefined);
  }

  /**
   * 处理消息举报
   */
  async processMessageReport(reportId: string, action: string, adminNote?: string): Promise<any> {
    return this.adapter.patch(`/admin/reports/messages/${reportId}`, { action, admin_note: adminNote });
  }

  /**
   * 处理评论举报
   */
  async processCommentReport(reportId: string, action: string, adminNote?: string): Promise<any> {
    return this.adapter.patch(`/admin/reports/comments/${reportId}`, { action, admin_note: adminNote });
  }

  /**
   * 处理小说举报
   */
  async processWorkReport(reportId: string, action: string, adminNote?: string): Promise<any> {
    return this.adapter.patch(`/admin/reports/works/${reportId}`, { action, admin_note: adminNote });
  }

  // ==================== AI生成世界观 ====================

  /**
   * 🆕 方案C：基于故事梗概生成完整世界观设定（24个字段，含标题和简介）
   * @param request 包含story_concept的请求对象
   * @returns Promise<any> 返回生成的24个字段（包括title和description）
   */
  async generateAIGuidelines(request: { storyConcept: string }): Promise<any> {
    return this.adapter.post('/worldview/ai-guidelines/generate', {
      story_concept: request.storyConcept
    });
  }

  // ==================== 世界观同步相关 ====================

  /**
   * 从单个章节提取世界观变化（方案A）
   * @param workId 作品ID
   * @param chapterId 章节ID
   * @param chapterContent 章节内容（可选，不传则从数据库读取）
   * @returns Promise<WorldviewChanges>
   */
  async extractWorldviewChanges(
    workId: string,
    chapterId: string,
    chapterContent?: string
  ): Promise<WorldviewChanges> {
    return this.adapter.post(`/worldview/works/${workId}/worldview/extract-changes`, {
      chapter_id: chapterId,
      chapter_content: chapterContent
    });
  }

  /**
   * 批量扫描章节提取世界观变化（方案C）
   * @param workId 作品ID
   * @param startChapter 起始章节号
   * @param endChapter 结束章节号（可选）
   * @param limit 最多扫描章节数
   * @returns Promise<WorldviewChanges>
   */
  async scanWorldviewChanges(
    workId: string,
    startChapter: number = 1,
    endChapter?: number,
    limit: number = 10
  ): Promise<WorldviewChanges> {
    return this.adapter.post(`/worldview/works/${workId}/worldview/scan-changes`, {
      start_chapter: startChapter,
      end_chapter: endChapter,
      limit
    });
  }

  /**
   * 应用世界观变化到卡片
   * @param workId 作品ID
   * @param changes 变化数据
   * @param selectedItems 选择性应用的项目
   * @returns Promise<ApplyChangesResult>
   */
  async applyWorldviewChanges(
    workId: string,
    changes: WorldviewChanges,
    selectedItems?: {
      new_characters?: string[];
      new_locations?: string[];
      new_settings?: string[];
      relationship_changes?: string[];
    }
  ): Promise<ApplyChangesResult> {
    return this.adapter.post(`/worldview/works/${workId}/worldview/apply-changes`, {
      changes,
      selected_items: selectedItems
    });
  }

  /**
   * 手动将世界观卡片同步到 knowledge/*.md
   * @param workId 作品ID
   */
  async syncWorldviewCardsToKnowledge(workId: string): Promise<{
    status: string;
    updatedFiles: string[];
    charactersCount: number;
    locationsCount: number;
    settingsCount: number;
  }> {
    return this.adapter.post(`/worldview/works/${workId}/knowledge/sync`, {});
  }

  /**
   * 手动将知识文件同步到世界观卡片（knowledge -> cards）
   * @param workId 作品ID
   * @param touchedPaths 指定同步的 knowledge 文件路径（可选）
   */
  async syncKnowledgeToWorldviewCards(
    workId: string,
    touchedPaths?: string[],
  ): Promise<{
    status: string;
    created: { characters: number; locations: number; settings: number };
    updated: { characters: number; locations: number; settings: number };
    deleted: { characters: number; locations: number; settings: number };
    mirroredFiles: string[];
    hasDbChanges: boolean;
    parsedCounts: { characters: number; locations: number; settings: number };
    checkedFiles: string[];
    missingFiles: string[];
    syncMode: string;
  }> {
    return this.adapter.post(`/worldview/works/${workId}/knowledge/sync-to-worldview`, {
      touched_paths: touchedPaths,
    });
  }
}

// 导出单例
export const DataService = new DataServiceClass();
