/**
 * API 基础地址
 * 根据环境变量自动切换
 */
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api';

/**
 * API 端点配置
 */
export const API_ENDPOINTS = {
  // 认证相关
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    PROFILE: '/auth/profile',
  },

  // 小说相关
  NOVELS: {
    LIST: '/novels',
    DETAIL: (id: string) => `/novels/${id}`,
    CREATE: '/novels',
    UPDATE: (id: string) => `/novels/${id}`,
    DELETE: (id: string) => `/novels/${id}`,
    STATS: (id: string) => `/novels/${id}/stats`,
  },

  // 章节相关
  CHAPTERS: {
    LIST: (novelId: string) => `/novels/${novelId}/chapters`,
    DETAIL: (novelId: string, chapterId: string) => `/novels/${novelId}/chapters/${chapterId}`,
    CREATE: (novelId: string) => `/novels/${novelId}/chapters`,
    UPDATE: (novelId: string, chapterId: string) => `/novels/${novelId}/chapters/${chapterId}`,
    DELETE: (novelId: string, chapterId: string) => `/novels/${novelId}/chapters/${chapterId}`,
  },

  // AI 相关
  AI: {
    GENERATE: '/ai/generate',
    CONTINUE: '/ai/continue',
    OPTIMIZE: '/ai/optimize',
    OUTLINE: '/ai/outline',
    CHARACTER: '/ai/character',
  },

  // 用户相关
  USER: {
    PROFILE: '/user/profile',
    UPDATE_PROFILE: '/user/profile',
    CHANGE_PASSWORD: '/user/password',
    SETTINGS: '/user/settings',
  },
} as const;

/**
 * 存储键名
 */
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth-storage',
  THEME: 'theme',
  EDITOR_SETTINGS: 'editor-settings',
  RECENT_NOVELS: 'recent-novels',
} as const;

/**
 * 分页默认配置
 */
export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
} as const;

/**
 * 编辑器默认配置
 */
export const EDITOR_CONFIG = {
  AUTO_SAVE_INTERVAL: 30000, // 自动保存间隔（毫秒）
  MIN_WORD_COUNT: 0, // 最小字数
  MAX_WORD_COUNT: 100000, // 最大字数
  DEFAULT_FONT_SIZE: 16, // 默认字体大小
  DEFAULT_LINE_HEIGHT: 1.8, // 默认行高
} as const;

/**
 * AI 配置
 */
export const AI_CONFIG = {
  MAX_GENERATE_LENGTH: 2000, // AI 生成最大长度
  MIN_PROMPT_LENGTH: 10, // 提示词最小长度
  MAX_PROMPT_LENGTH: 500, // 提示词最大长度
  DEFAULT_TEMPERATURE: 0.8, // 默认温度
  DEFAULT_TOP_P: 0.9, // 默认 top_p
} as const;

/**
 * 小说类型
 */
export const NOVEL_GENRES = [
  '玄幻',
  '奇幻',
  '武侠',
  '仙侠',
  '都市',
  '历史',
  '军事',
  '科幻',
  '游戏',
  '体育',
  '悬疑',
  '灵异',
  '二次元',
  '轻小说',
] as const;

/**
 * 小说状态
 */
export const NOVEL_STATUS = {
  DRAFT: 'draft', // 草稿
  ONGOING: 'ongoing', // 连载中
  COMPLETED: 'completed', // 已完结
  PAUSED: 'paused', // 暂停
} as const;

/**
 * 小说状态标签
 */
export const NOVEL_STATUS_LABELS: Record<string, string> = {
  [NOVEL_STATUS.DRAFT]: '草稿',
  [NOVEL_STATUS.ONGOING]: '连载中',
  [NOVEL_STATUS.COMPLETED]: '已完结',
  [NOVEL_STATUS.PAUSED]: '暂停',
} as const;

/**
 * Toast 消息默认持续时间（毫秒）
 */
export const TOAST_DURATION = {
  SUCCESS: 3000,
  ERROR: 5000,
  WARNING: 4000,
  INFO: 3000,
} as const;

/**
 * 文件上传配置
 */
export const UPLOAD_CONFIG = {
  MAX_FILE_SIZE: 5 * 1024 * 1024, // 5MB
  ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
  ALLOWED_DOCUMENT_TYPES: ['application/pdf', 'text/plain', 'application/msword'],
} as const;

/**
 * 路由路径
 */
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  NOVELS: '/novels',
  NOVEL_DETAIL: (id: string) => `/novels/${id}`,
  EDITOR: (novelId: string, chapterId: string) => `/editor/${novelId}/${chapterId}`,
  PROFILE: '/profile',
  SETTINGS: '/settings',
} as const;

/**
 * 正则表达式
 */
export const REGEX = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PASSWORD: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/, // 至少8位，包含大小写字母和数字
  USERNAME: /^[a-zA-Z0-9_]{3,20}$/, // 3-20位，字母、数字、下划线
  PHONE: /^1[3-9]\d{9}$/, // 中国手机号
} as const;

/**
 * 错误消息
 */
export const ERROR_MESSAGES = {
  NETWORK_ERROR: '网络连接失败，请检查网络设置',
  SERVER_ERROR: '服务器错误，请稍后重试',
  AUTH_FAILED: '认证失败，请重新登录',
  UNAUTHORIZED: '您没有权限执行此操作',
  NOT_FOUND: '请求的资源不存在',
  VALIDATION_ERROR: '数据验证失败',
  UNKNOWN_ERROR: '未知错误，请联系管理员',
} as const;
