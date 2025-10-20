/**
 * AI 写作平台 - TypeScript 类型定义
 *
 * 所有核心数据结构的类型定义，确保强类型化
 */

// ==================== 用户相关类型 ====================

/**
 * 用户角色
 */
export type UserRole = 'admin' | 'user';

/**
 * 用户接口
 * 注意：后端返回snake_case，ApiAdapter会自动转换为camelCase
 */
export interface User {
  id: string;
  username: string;
  email: string;
  fullName?: string;      // 后端: full_name
  avatar?: string;
  bio?: string;
  isActive: boolean;      // 后端: is_active
  isAdmin: boolean;       // 后端: is_admin
  isVerified: boolean;    // 后端: is_verified
  createdAt: string;      // 后端: created_at
  updatedAt: string;      // 后端: updated_at
  lastLoginAt?: string;   // 后端: last_login_at
}

/**
 * 登录凭证
 */
export interface LoginCredentials {
  username: string;
  password: string;
}

/**
 * 注册数据
 */
export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

/**
 * Token 响应（登录后返回）
 * 注意：后端返回snake_case，ApiAdapter会自动转换为camelCase
 */
export interface TokenResponse {
  accessToken: string;  // 后端: access_token
  tokenType: string;     // 后端: token_type
}

/**
 * 认证响应（注册后返回）
 * 注意：后端返回snake_case，ApiAdapter会自动转换为camelCase
 */
export interface AuthResponse {
  user: User;
  accessToken: string;   // 后端: access_token
  tokenType: string;     // 后端: token_type
}

// ==================== 作品相关类型 ====================

/**
 * 作品状态
 */
export type WorkStatus = 'draft' | 'writing' | 'completed' | 'abandoned';

/**
 * 作品类型
 */
export type WorkGenre = 'fantasy' | 'urban' | 'romance' | 'scifi' | 'wuxia' | 'game' | 'history' | 'military' | 'other';

/**
 * 作品接口
 * 注意：后端返回snake_case，ApiAdapter会自动转换为camelCase
 */
export interface Work {
  id: string;
  title: string;
  description?: string;
  authorId: string;        // 后端: author_id
  genre: WorkGenre;
  status: WorkStatus;
  coverImage?: string;     // 后端: cover_image
  totalWords: number;      // 后端: total_words
  totalChapters: number;   // 后端: total_chapters
  viewCount: number;       // 后端: view_count
  createdAt: string;       // 后端: created_at
  updatedAt: string;       // 后端: updated_at
  publishedAt?: string;    // 后端: published_at
}

/**
 * 创建作品数据
 */
export interface CreateWorkData {
  title: string;
  description?: string; // 可选，与后端一致
  genre?: WorkGenre;
  status?: WorkStatus;
  cover_image?: string;
}

// ==================== 章节相关类型 ====================

/**
 * 章节状态
 */
export type ChapterStatus = 'draft' | 'published';

/**
 * 章节接口
 * 注意：后端返回snake_case，ApiAdapter会自动转换为camelCase
 */
export interface Chapter {
  id: string;
  workId: string;            // 后端: work_id
  title: string;
  content: string;
  summary?: string | null;   // 后端: summary - 章节剧情概括
  wordCount: number;         // 后端: word_count
  viewCount: number;         // 后端: view_count
  isPublished: boolean;      // 后端: is_published
  order: number;
  publishedAt: string | null; // 后端: published_at
  createdAt: string;         // 后端: created_at
  updatedAt: string;         // 后端: updated_at
}

/**
 * 创建章节数据（发送到后端时使用snake_case）
 */
export interface CreateChapterData {
  work_id: string;  // 后端需要snake_case
  title: string;
  content?: string;
  order?: number;
}

// ==================== AI 相关类型 ====================

/**
 * AI 模型状态
 */
export type AIModelStatus = 'active' | 'inactive' | 'maintenance';

/**
 * AI 模型类型
 */
export type AIModelType = 'gpt-4' | 'gpt-3.5-turbo' | 'claude-3' | 'claude-2' | 'custom';

/**
 * AI 模型接口
 */
export interface AIModel {
  id: string;
  name: string;
  type: AIModelType;
  provider: string;
  apiKey: string;
  apiEndpoint?: string;
  usageLimit: number;
  usedCount: number;
  costPerRequest: number;
  status: AIModelStatus;
  description?: string;
  createTime: string;
}

/**
 * AI 配置
 */
export interface AIConfig {
  tone: 'formal' | 'casual' | 'humorous' | 'serious';
  length: number;
  temperature: number;
  model: string;
}

/**
 * AI 续写请求
 */
export interface AIContinueRequest {
  chapterId: string;
  content: string;
  config: AIConfig;
}

/**
 * AI 续写响应
 */
export interface AIContinueResponse {
  suggestions: string[];
  tokensUsed: number;
  cost: number;
}

/**
 * AI 润色请求
 */
export interface AIPolishRequest {
  text: string;
  config: Partial<AIConfig>;
}

/**
 * AI 摘要请求
 */
export interface AISummaryRequest {
  content: string;
  maxLength: number;
}

// ==================== 世界观相关类型 ====================

/**
 * 角色接口
 */
export interface Character {
  id: string;
  workId: string;
  name: string;
  description: string;
  avatar?: string;
  age?: number;
  gender?: 'male' | 'female' | 'other';
  personality?: string;
  background?: string;
  relationships?: string[];
  createTime: string;
  updateTime: string;
}

/**
 * 地点接口
 */
export interface Location {
  id: string;
  workId: string;
  name: string;
  description: string;
  image?: string;
  type?: 'city' | 'building' | 'nature' | 'other';
  createTime: string;
  updateTime: string;
}

/**
 * 道具接口
 */
export interface Item {
  id: string;
  workId: string;
  name: string;
  description: string;
  image?: string;
  type?: 'weapon' | 'tool' | 'treasure' | 'other';
  createTime: string;
  updateTime: string;
}

/**
 * 世界观数据
 */
export interface WorldData {
  characters: Character[];
  locations: Location[];
  items: Item[];
}

// ==================== 成本监控相关类型 ====================

/**
 * 成本指标
 */
export interface CostMetric {
  date: string;
  totalCalls: number;
  totalCost: number;
  model: string;
}

/**
 * 使用统计
 */
export interface UsageStats {
  totalWorks: number;
  totalChapters: number;
  totalWords: number;
  totalAICalls: number;
  totalCost: number;
  dailyMetrics: CostMetric[];
}

// ==================== 通用类型 ====================

/**
 * API 响应包装
 */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

/**
 * 分页参数
 */
export interface PaginationParams {
  page: number;
  pageSize: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

/**
 * 分页响应
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

/**
 * 搜索参数
 */
export interface SearchParams extends PaginationParams {
  keyword?: string;
  filters?: Record<string, any>;
}

/**
 * Loading 状态
 */
export interface LoadingState {
  isLoading: boolean;
  error: string | null;
}

/**
 * Toast 消息类型
 */
export type ToastType = 'success' | 'error' | 'warning' | 'info';

/**
 * Toast 消息
 */
export interface ToastMessage {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}

// ==================== 小说分析相关类型 ====================
export * from './novel_analysis';

// ==================== 搜索相关类型 ====================
export * from './search';

// ==================== 导入导出相关类型 ====================
export * from './export';
