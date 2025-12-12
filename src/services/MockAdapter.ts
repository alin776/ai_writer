/**
 * Mock 数据适配器
 *
 * 模拟真实 API 请求，返回 Mock 数据
 * 包含网络延迟模拟和简单的 CRUD 操作
 */
import type { IDataAdapter } from './IDataAdapter';
import {
  mockWorks,
  mockChapters,
  mockUsers,
  mockAIModels,
  mockCharacters,
  mockLocations,
  mockItems,
  mockSettings,
  mockCostMetrics
} from '@/mock';
import type {
  Work,
  Chapter,
  User,
  AuthResponse,
  LoginCredentials,
  RegisterData,
  CreateWorkData,
  CreateChapterData,
  UserSession,
} from '@/types';
import type { WorkStatus } from '@/types';

type WorkGuidelines = Record<string, any>;
type AdminStatistics = {
  users?: { total?: number; change?: string };
  works?: { total?: number; change?: string };
  aiCalls?: { total?: number; change?: string };
  cost?: { total?: number; change?: string };
};
type UsersGrowthPoint = { date: string; count?: number; total?: number };
type AIUsagePoint = { date: string; calls: number; cost: number };
type RecentActivity = { id: string; type: string; message: string; createdAt: string };

const defaultNotificationSettings = {
  emailNotifications: true,
  browserNotifications: false,
  newChapter: true,
  comments: true,
  mentions: true,
  systemUpdates: false,
};

const defaultPreferences = {
  theme: 'light' as const,
  language: 'zh-CN' as const,
  autoSave: true,
  autoSaveInterval: 30,
};

let cachedNotificationSettings = { ...defaultNotificationSettings };
let cachedPreferences = { ...defaultPreferences };
let cachedAvatarUrl = 'https://api.dicebear.com/7.x/avataaars/svg?seed=mock';
let cachedGuidelines: Record<string, any> = {};
let cachedAIGuidelines: Record<string, any> = {};
let cachedSessions: UserSession[] = [
  {
    id: 'session-current',
    deviceType: 'desktop',
    deviceName: 'Windows 桌面端',
    browser: 'Chrome',
    browserVersion: '121.0',
    operatingSystem: 'Windows 11',
    ipAddress: '222.132.58.45',
    location: '北京',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString(),
    lastActiveAt: new Date().toISOString(),
    isActive: true,
    isCurrent: true,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
  },
  {
    id: 'session-mobile',
    deviceType: 'mobile',
    deviceName: 'iPhone 15',
    browser: 'Safari',
    browserVersion: '17.0',
    operatingSystem: 'iOS 17',
    ipAddress: '120.55.32.10',
    location: '上海',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    lastActiveAt: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
    isActive: true,
    isCurrent: false,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)...',
  },
  {
    id: 'session-tablet',
    deviceType: 'tablet',
    deviceName: 'iPad Pro',
    browser: 'Safari',
    browserVersion: '16.6',
    operatingSystem: 'iPadOS 16',
    ipAddress: '58.34.190.9',
    location: '广州',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString(),
    lastActiveAt: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(),
    isActive: true,
    isCurrent: false,
    userAgent: 'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X)...',
  },
];

export class MockAdapter implements IDataAdapter {
  /**
   * 模拟网络延迟
   * @param ms 延迟毫秒数
   */
  private async delay(ms: number = 500): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  /**
   * GET 请求实现
   */
  async get<T>(url: string): Promise<T> {
    await this.delay();

    // 管理后台统计
    if (url === '/admin/statistics') {
      const statistics: AdminStatistics = {
        users: { total: mockUsers.length, change: '+0%' },
        works: { total: mockWorks.length, change: '+0%' },
        aiCalls: { total: 1024, change: '+8%' },
        cost: { total: 123.45, change: '+5%' },
      };
      return statistics as T;
    }

    // 用户增长趋势
    if (url.startsWith('/admin/users-growth')) {
      const data: UsersGrowthPoint[] = Array.from({ length: 7 }).map((_, idx) => ({
        date: new Date(Date.now() - (6 - idx) * 86400000).toISOString().slice(0, 10),
        count: Math.max(1, mockUsers.length - (6 - idx)),
      }));
      return { data } as T;
    }

    // AI 使用统计
    if (url === '/admin/ai-usage') {
      const data: AIUsagePoint[] = Array.from({ length: 7 }).map((_, idx) => ({
        date: new Date(Date.now() - (6 - idx) * 86400000).toISOString().slice(0, 10),
        calls: 200 + idx * 10,
        cost: 5 + idx * 0.5,
      }));
      return { data } as T;
    }

    // 最近活动
    if (url.startsWith('/admin/recent-activities')) {
      const data: RecentActivity[] = [
        { id: 'act-1', type: 'work', message: '新建作品《梦境之海》', createdAt: new Date().toISOString() },
        { id: 'act-2', type: 'user', message: '用户 alice 完成注册', createdAt: new Date(Date.now() - 3600000).toISOString() },
      ];
      return data as T;
    }

    // 世界观规范
    if (url.match(/\/worldview\/works\/.+\/guidelines$/)) {
      const workId = url.split('/')[3];
      return (cachedGuidelines[workId] ?? null) as T;
    }
    if (url.match(/\/worldview\/works\/.+\/ai-guidelines$/)) {
      const workId = url.split('/')[3];
      return (cachedAIGuidelines[workId] ?? null) as T;
    }

    if (url === '/users/me/notification-settings') {
      return { ...cachedNotificationSettings } as T;
    }

    if (url === '/users/me/preferences') {
      return { ...cachedPreferences } as T;
    }

    if (url === '/users/me') {
      const base = mockUsers[0] || {
        id: 'user-1',
        username: 'mockuser',
        email: 'mock@example.com',
        role: 'admin',
        isActive: true,
        isAdmin: true,
        isVerified: true,
      };
      const now = new Date().toISOString();
      return {
        id: base.id,
        username: base.username,
        name: base.name || 'Mock User',
        email: base.email,
        fullName: base.fullName || base.name || 'Mock User',
        avatar: base.avatar,
        bio: base.bio,
        notificationSettings: { ...cachedNotificationSettings },
        preferences: { ...cachedPreferences },
        isActive: true,
        isAdmin: base.role === 'admin',
        isVerified: true,
        createdAt: base.createdAt || now,
        updatedAt: base.updatedAt || now,
      } as T;
    }

    if (url === '/users/me/sessions') {
      return cachedSessions.map((session) => ({ ...session })) as T;
    }

    // 用户认证
    if (url === '/auth/me') {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('未登录');
      }
      const base = mockUsers[0] || {};
      return {
        id: base.id || 'user-1',
        username: base.username || 'mockuser',
        name: base.name || '张三',
        email: base.email || 'mock@example.com',
        role: base.role || 'user',
        avatar: base.avatar,
        isActive: true,
        isAdmin: base.role === 'admin',
        isVerified: true,
        createdAt: base.createdAt || new Date().toISOString(),
        updatedAt: base.updatedAt || new Date().toISOString(),
      } as T;
    }

    // 作品列表
    if (url === '/works') {
      const normalizedWorks = mockWorks.map((w) => ({
        totalChapters: w.totalChapters ?? w.chapterCount ?? 0,
        viewCount: w.viewCount ?? 0,
        createdAt: w.createdAt ?? w.createTime ?? new Date().toISOString(),
        updatedAt: w.updatedAt ?? w.updateTime ?? new Date().toISOString(),
        ...w,
      }));

      const totalWords = normalizedWorks.reduce((sum, work) => sum + (work.totalWords || 0), 0);
      const writingCount = normalizedWorks.filter((work) => work.status === 'writing').length;
      const weekStart = Date.now() - 7 * 24 * 60 * 60 * 1000;
      const weekNewWords = mockChapters
        .filter((c) => {
          const updated = new Date(c.updatedAt ?? c.updateTime ?? c.lastSaveTime ?? c.createTime ?? 0).getTime();
          return updated >= weekStart;
        })
        .reduce((sum, c) => sum + (c.wordCount || 0), 0);

      return {
        total: normalizedWorks.length,
        page: 1,
        pageSize: normalizedWorks.length,
        items: normalizedWorks,
        summary: {
          totalWords,
          writingCount,
          weeklyNewWords: weekNewWords,
        },
      } as T;
    }

    // 单个作品
    if (url.startsWith('/works/') && !url.includes('/chapters') && !url.includes('/characters') && !url.includes('/locations') && !url.includes('/items') && !url.includes('/settings')) {
      const id = url.split('/')[2];
      const work = mockWorks.find((w) => w.id === id);
      if (!work) throw new Error('作品不存在');
      return {
        totalChapters: work.totalChapters ?? (work as any).chapterCount ?? 0,
        viewCount: work.viewCount ?? 0,
        createdAt: (work as any).createdAt ?? (work as any).createTime ?? new Date().toISOString(),
        updatedAt: (work as any).updatedAt ?? (work as any).updateTime ?? new Date().toISOString(),
        ...work,
      } as T;
    }

    // 作品的章节列表
    if (url.match(/\/works\/.*\/chapters$/)) {
      const workId = url.split('/')[2];
      const chapters = mockChapters.filter((c) => c.workId === workId);
      return chapters as T;
    }

    // 单个章节
    if (url.match(/\/chapters\/.+$/)) {
      const id = url.split('/')[2];
      const chapter = mockChapters.find((c) => c.id === id);
      if (!chapter) throw new Error('章节不存在');
      return chapter as T;
    }

    // 用户列表
    if (url === '/users') {
      return mockUsers as T;
    }

    // AI 模型列表
    if (url === '/ai-models') {
      return mockAIModels as T;
    }

    // 世界观数据 - 角色
    if (url.match(/\/works\/.*\/characters$/)) {
      const workId = url.split('/')[2];
      const characters = mockCharacters.filter((c) => c.workId === workId);
      return characters as T;
    }

    // 世界观数据 - 地点
    if (url.match(/\/works\/.*\/locations$/)) {
      const workId = url.split('/')[2];
      const locations = mockLocations.filter((l) => l.workId === workId);
      return locations as T;
    }

    // 世界观数据 - 道具
    if (url.match(/\/works\/.*\/items$/)) {
      const workId = url.split('/')[2];
      const items = mockItems.filter((i) => i.workId === workId);
      return items as T;
    }

    // 世界观数据 - 设定
    if (url.match(/\/works\/.*\/settings$/)) {
      const workId = url.split('/')[2];
      const settings = mockSettings.filter((s) => s.workId === workId);
      return settings as T;
    }

    // 成本统计
    if (url === '/cost-metrics') {
      return mockCostMetrics as T;
    }

    // 关系、时间线、分组等返回空集合以兼容 UI
    if (url.match(/\/relationships\/work\/.+/)) {
      return { items: [] } as T;
    }
    if (url.match(/\/timeline\/work\/.+\/chapter-anchors/)) {
      return [] as T;
    }
    if (url.match(/\/timeline\/work\/.+/)) {
      return { items: [] } as T;
    }
    if (url.match(/\/timeline\/.+/)) {
      return {} as T;
    }
    if (url.match(/\/groups\/work\/.+/)) {
      return [] as T;
    }
    if (url.match(/\/groups\/.+/)) {
      return {} as T;
    }

    throw new Error(`Mock route not implemented: ${url}`);
  }

  /**
   * POST 请求实现
   */
  async post<T>(url: string, data?: any): Promise<T> {
    await this.delay();

    // 登录
    if (url === '/auth/login') {
      const { email, password, username } = data as LoginCredentials & { email?: string };
      const user =
        mockUsers.find((u) => u.email === email || u.username === username) ||
        (username === 'mockuser' || email === 'mock@example.com'
          ? {
              id: 'user-mock',
              name: 'Mock User',
              username: 'mockuser',
              email: 'mock@example.com',
              role: 'admin',
              avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=mockuser',
              registrationDate: new Date().toISOString(),
              status: 'active',
            }
          : null);
      if (!user || password !== '123456') {
        throw new Error('邮箱或密码错误');
      }
      const response: AuthResponse = {
        user,
        accessToken: 'mock-jwt-token-' + Date.now(),
        tokenType: 'bearer',
      };
      return response as T;
    }

    // 注册
    if (url === '/auth/register') {
      const registerData = data as RegisterData & { name?: string };
      const newUser: any = {
        id: 'user-' + Date.now(),
        name: registerData.name,
        username: registerData.username,
        email: registerData.email,
        role: 'user',
        isActive: true,
        isAdmin: false,
        isVerified: false,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      const response: any = {
        user: newUser as User,
        accessToken: 'mock-jwt-token-' + Date.now(),
        tokenType: 'bearer',
      };
      return response as T;
    }

    // 创建作品
    if (url === '/works') {
      const workData = data as Partial<CreateWorkData>;
      const newWork: Work = {
        id: 'work-' + Date.now(),
        title: workData.title || '新作品',
        description: workData.description || '',
        authorId: mockUsers[0]?.id || 'user-1',
        totalWords: 0,
        totalChapters: 0,
        viewCount: 0,
        status: (workData.status as WorkStatus) || 'draft',
        genre: workData.genre || 'other',
        coverImage: workData.cover_image,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      mockWorks.push(newWork as Work);
      return newWork as T;
    }

    // 创建章节
    if (url === '/chapters') {
      const chapterData = data as Partial<CreateChapterData> & { workId?: string; summary?: string };
      const workId = chapterData.workId || chapterData.work_id || 'work-unknown';
      const newChapter: Chapter = {
        id: 'chapter-' + Date.now(),
        workId,
        title: chapterData.title || '新章节',
        content: chapterData.content || '',
        summary: chapterData.summary || '',
        wordCount: 0,
        viewCount: 0,
        isPublished: false,
        status: 'draft',
        order: mockChapters.filter((c) => c.workId === workId).length + 1,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        publishedAt: null,
      };
      mockChapters.push(newChapter as Chapter);
      return newChapter as T;
    }

    // AI 续写
    if (url === '/ai/continue') {
      await this.delay(1500); // AI 响应较慢
      return {
        suggestions: [
          '这是 AI 生成的续写内容示例...',
          '另一个可能的续写方向...',
        ],
        tokensUsed: 150,
        cost: 0.003,
      } as T;
    }

    if (url === '/users/me/change-password') {
      if (data?.currentPassword !== '123456') {
        throw new Error('当前密码错误');
      }
      return { detail: '密码修改成功' } as T;
    }

    if (url === '/users/me/avatar') {
      cachedAvatarUrl = data?.get?.('file')
        ? `${cachedAvatarUrl}?t=${Date.now()}`
        : cachedAvatarUrl;
      return { avatarUrl: cachedAvatarUrl } as T;
    }

    // 保存世界观规范
    if (url.match(/\/worldview\/works\/.+\/guidelines$/)) {
      const workId = url.split('/')[3];
      cachedGuidelines[workId] = data as WorkGuidelines;
      return cachedGuidelines[workId] as T;
    }
    if (url.match(/\/worldview\/works\/.+\/ai-guidelines$/)) {
      const workId = url.split('/')[3];
      cachedAIGuidelines[workId] = data as WorkGuidelines;
      return cachedAIGuidelines[workId] as T;
    }

    if (url === '/users/me/sessions/logout-others') {
      cachedSessions = cachedSessions.map((session) =>
        session.isCurrent
          ? session
          : { ...session, isActive: false }
      );
      cachedSessions = cachedSessions.filter((session) => session.isCurrent);
      return { detail: '已退出其他设备' } as T;
    }

    // AI 润色
    if (url === '/ai/polish') {
      await this.delay(1000);
      return {
        result: '这是润色后的文本...',
        tokensUsed: 100,
        cost: 0.002,
      } as T;
    }

    // 创建角色
    if (url === '/characters') {
      const newCharacter: any = {
        id: 'character-' + Date.now(),
        ...data,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      mockCharacters.push(newCharacter);
      return newCharacter as T;
    }

    // 创建地点
    if (url === '/locations') {
      const newLocation: any = {
        id: 'location-' + Date.now(),
        ...data,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      mockLocations.push(newLocation);
      return newLocation as T;
    }

    // 创建设定
    if (url === '/settings') {
      const newSetting: any = {
        id: 'setting-' + Date.now(),
        ...data,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      mockSettings.push(newSetting);
      return newSetting as T;
    }

    throw new Error(`Mock POST route not implemented: ${url}`);
  }

  /**
   * PUT 请求实现
   */
  async put<T>(url: string, data?: any): Promise<T> {
    await this.delay();

    if (url === '/users/me/notification-settings') {
      cachedNotificationSettings = { ...cachedNotificationSettings, ...data };
      return { ...cachedNotificationSettings } as T;
    }

    if (url === '/users/me/preferences') {
      cachedPreferences = { ...cachedPreferences, ...data };
      return { ...cachedPreferences } as T;
    }

    if (url === '/users/me') {
      cachedAvatarUrl = data?.avatar ?? cachedAvatarUrl;
      return {
        id: 'user-1',
        username: data?.username ?? 'mock-user',
        email: data?.email ?? 'mock@example.com',
        fullName: data?.fullName,
        avatar: cachedAvatarUrl,
        bio: data?.bio,
        notificationSettings: { ...cachedNotificationSettings },
        preferences: { ...cachedPreferences },
        isActive: true,
        isAdmin: true,
        isVerified: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      } as T;
    }

    // 更新作品
    if (url.startsWith('/works/')) {
      const id = url.split('/')[2];
      const index = mockWorks.findIndex((w) => w.id === id);
      if (index === -1) throw new Error('作品不存在');
      mockWorks[index] = { ...mockWorks[index], ...(data as Partial<Work>), updateTime: new Date().toISOString() } as any;
      return mockWorks[index] as T;
    }

    // 更新章节
    if (url.startsWith('/chapters/')) {
      const id = url.split('/')[2];
      const index = mockChapters.findIndex((c) => c.id === id);
      if (index === -1) throw new Error('章节不存在');
      const updatedChapter: Chapter = {
        ...mockChapters[index],
        ...(data as Partial<Chapter>),
        updateTime: new Date().toISOString(),
        lastSaveTime: new Date().toISOString(),
      };
      mockChapters[index] = updatedChapter;
      return updatedChapter as T;
    }

    // 更新用户
    if (url.startsWith('/users/')) {
      const id = url.split('/')[2];
      const index = mockUsers.findIndex((u) => u.id === id);
      if (index === -1) throw new Error('用户不存在');
      mockUsers[index] = { ...mockUsers[index], ...(data as Partial<User>) };
      return mockUsers[index] as T;
    }

    // 更新设定
    if (url.startsWith('/settings/')) {
      const id = url.split('/')[2];
      const index = mockSettings.findIndex((s) => s.id === id);
      if (index === -1) throw new Error('设定不存在');
      mockSettings[index] = {
        ...mockSettings[index],
        ...data,
        updatedAt: new Date(),
      };
      return mockSettings[index] as T;
    }

    throw new Error(`Mock PUT route not implemented: ${url}`);
  }

  /**
   * DELETE 请求实现
   */
  async delete<T>(url: string, _data?: any): Promise<T> {
    await this.delay();

    if (url.startsWith('/users/me/sessions/')) {
      const sessionId = url.split('/').pop();
      if (!sessionId) {
        throw new Error('未指定会话 ID');
      }
      const session = cachedSessions.find((item) => item.id === sessionId);
      if (!session) {
        throw new Error('会话不存在');
      }
      if (session.isCurrent) {
        throw new Error('无法在当前设备退出当前会话');
      }
      cachedSessions = cachedSessions.filter((item) => item.id !== sessionId);
      return { detail: '会话已退出' } as T;
    }

    if (url === '/users/me') {
      cachedNotificationSettings = { ...defaultNotificationSettings };
      cachedPreferences = { ...defaultPreferences };
      return { detail: '账号已删除' } as unknown as T;
    }

    // 删除作品
    if (url.startsWith('/works/')) {
      const id = url.split('/')[2];
      const index = mockWorks.findIndex((w) => w.id === id);
      if (index === -1) throw new Error('作品不存在');
      mockWorks.splice(index, 1);
      return { success: true } as T;
    }

    // 删除章节
    if (url.startsWith('/chapters/')) {
      const id = url.split('/')[2];
      const index = mockChapters.findIndex((c) => c.id === id);
      if (index === -1) throw new Error('章节不存在');
      mockChapters.splice(index, 1);
      return { success: true } as T;
    }

    // 删除设定
    if (url.startsWith('/settings/')) {
      const id = url.split('/')[2];
      const index = mockSettings.findIndex((s) => s.id === id);
      if (index === -1) throw new Error('设定不存在');
      mockSettings.splice(index, 1);
      return { success: true } as T;
    }

    // 删除世界观规范
    if (url.match(/\/worldview\/works\/.+\/guidelines$/)) {
      const workId = url.split('/')[3];
      delete cachedGuidelines[workId];
      return { success: true } as unknown as T;
    }
    if (url.match(/\/worldview\/works\/.+\/ai-guidelines$/)) {
      const workId = url.split('/')[3];
      delete cachedAIGuidelines[workId];
      return { success: true } as unknown as T;
    }

    throw new Error(`Mock DELETE route not implemented: ${url}`);
  }

  /**
   * PATCH 请求实现
   */
  async patch<T>(url: string, data?: any): Promise<T> {
    await this.delay();

    // 封禁用户
    if (url.match(/\/admin\/users\/.+\/ban$/)) {
      const id = url.split('/')[3];
      const index = mockUsers.findIndex((u) => u.id === id);
      if (index === -1) throw new Error('用户不存在');
      mockUsers[index] = { ...mockUsers[index], status: 'banned' };
      return { message: '用户已封禁', user: mockUsers[index] } as T;
    }

    // 解封用户
    if (url.match(/\/admin\/users\/.+\/unban$/)) {
      const id = url.split('/')[3];
      const index = mockUsers.findIndex((u) => u.id === id);
      if (index === -1) throw new Error('用户不存在');
      mockUsers[index] = { ...mockUsers[index], status: 'active' };
      return { message: '用户已解封', user: mockUsers[index] } as T;
    }

    // 切换管理员角色
    if (url.match(/\/admin\/users\/.+\/toggle-admin$/)) {
      const id = url.split('/')[3];
      const index = mockUsers.findIndex((u) => u.id === id);
      if (index === -1) throw new Error('用户不存在');
      const isAdmin = mockUsers[index].role === 'admin';
      mockUsers[index] = {
        ...mockUsers[index],
        role: isAdmin ? 'user' : 'admin',
      };
      return {
        message: isAdmin ? '已取消管理员权限' : '已设置为管理员',
        user: mockUsers[index],
      } as T;
    }

    throw new Error(`Mock PATCH route not implemented: ${url}`);
  }
}
