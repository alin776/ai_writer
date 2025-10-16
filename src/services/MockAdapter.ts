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
} from '@/types';

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

    // 用户认证
    if (url === '/auth/me') {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('未登录');
      }
      return mockUsers[0] as T;
    }

    // 作品列表
    if (url === '/works') {
      return mockWorks as T;
    }

    // 单个作品
    if (url.startsWith('/works/') && !url.includes('/chapters') && !url.includes('/characters') && !url.includes('/locations') && !url.includes('/items') && !url.includes('/settings')) {
      const id = url.split('/')[2];
      const work = mockWorks.find((w) => w.id === id);
      if (!work) throw new Error('作品不存在');
      return work as T;
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

    throw new Error(`Mock route not implemented: ${url}`);
  }

  /**
   * POST 请求实现
   */
  async post<T>(url: string, data?: any): Promise<T> {
    await this.delay();

    // 登录
    if (url === '/auth/login') {
      const { email, password } = data as LoginCredentials;
      const user = mockUsers.find((u) => u.email === email);
      if (!user || password !== '123456') {
        throw new Error('邮箱或密码错误');
      }
      const response: AuthResponse = {
        user,
        token: 'mock-jwt-token-' + Date.now(),
      };
      return response as T;
    }

    // 注册
    if (url === '/auth/register') {
      const registerData = data as RegisterData;
      const newUser: User = {
        id: 'user-' + Date.now(),
        name: registerData.name,
        email: registerData.email,
        role: 'user',
        registrationDate: new Date().toISOString(),
        status: 'active',
        dailyAiQuota: 100,
        usedAiQuota: 0,
      };
      const response: AuthResponse = {
        user: newUser,
        token: 'mock-jwt-token-' + Date.now(),
      };
      return response as T;
    }

    // 创建作品
    if (url === '/works') {
      const workData = data as CreateWorkData;
      const newWork: Work = {
        id: 'work-' + Date.now(),
        ...workData,
        authorId: mockUsers[0].id,
        totalWords: 0,
        chapterCount: 0,
        status: 'draft',
        createTime: new Date().toISOString(),
        updateTime: new Date().toISOString(),
      };
      mockWorks.push(newWork);
      return newWork as T;
    }

    // 创建章节
    if (url === '/chapters') {
      const chapterData = data as CreateChapterData;
      const newChapter: Chapter = {
        id: 'chapter-' + Date.now(),
        ...chapterData,
        content: chapterData.content || '',
        wordCount: 0,
        status: 'draft',
        order: mockChapters.filter((c) => c.workId === chapterData.workId).length + 1,
        createTime: new Date().toISOString(),
        updateTime: new Date().toISOString(),
      };
      mockChapters.push(newChapter);
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

    // 更新作品
    if (url.startsWith('/works/')) {
      const id = url.split('/')[2];
      const index = mockWorks.findIndex((w) => w.id === id);
      if (index === -1) throw new Error('作品不存在');
      mockWorks[index] = { ...mockWorks[index], ...data, updateTime: new Date().toISOString() };
      return mockWorks[index] as T;
    }

    // 更新章节
    if (url.startsWith('/chapters/')) {
      const id = url.split('/')[2];
      const index = mockChapters.findIndex((c) => c.id === id);
      if (index === -1) throw new Error('章节不存在');
      const updatedChapter = {
        ...mockChapters[index],
        ...data,
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
      mockUsers[index] = { ...mockUsers[index], ...data };
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
  async delete<T>(url: string): Promise<T> {
    await this.delay();

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

    throw new Error(`Mock DELETE route not implemented: ${url}`);
  }
}
