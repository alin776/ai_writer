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
 * 用户接口（后端 snake_case 格式）
 */
export interface User {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
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
 */
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

/**
 * 认证响应（注册后返回）
 */
export interface AuthResponse {
  user: User;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// ==================== 作品相关类型 ====================

/**
 * 作品状态
 */
export type WorkStatus = 'draft' | 'writing' | 'completed' | 'archived';

/**
 * 作品接口（后端 snake_case 格式）
 */
export interface Work {
  id: string;
  title: string;
  description: string;
  author_id: string;
  total_words: number;
  total_chapters: number;
  created_at: string;
  updated_at: string;
}

/**
 * 创建作品数据
 */
export interface CreateWorkData {
  title: string;
  description: string;
}

// ==================== 章节相关类型 ====================

/**
 * 章节状态
 */
export type ChapterStatus = 'draft' | 'published';

/**
 * 章节接口（后端 snake_case 格式）
 */
export interface Chapter {
  id: string;
  work_id: string;
  title: string;
  content: string;
  word_count: number;
  is_published: boolean;
  order: number;
  created_at: string;
  updated_at: string;
}

/**
 * 创建章节数据
 */
export interface CreateChapterData {
  work_id: string;
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
