// src/types/humanize.ts

/**
 * AI去痕迹类型定义
 *
 * 包含:
 * - 改写强度类型
 * - AI检测结果
 * - 改写验证结果
 * - 会话记录
 * - 用户画像
 * - SSE事件类型
 */

// ==================== 基础类型 ====================

/**
 * 改写强度类型
 * - light: 轻度改写 (~5%改动)
 * - medium: 中度改写 (~20%改动)
 * - strong: 强度改写 (~40%改动)
 */
export type HumanizeIntensity = 'light' | 'medium' | 'strong';

// ==================== AI检测相关 ====================

/**
 * 单维度评分
 */
export interface DimensionScore {
  /** 分数 (0-100) */
  score: number;
  /** 维度说明 */
  description: string;
  /** 检测到的问题列表 */
  issues: string[];
}

/**
 * AI特征检测结果
 */
export interface AIDetectionResult {
  /** 总体AI特征分数 (0-100，分数越高越像AI) */
  overall_score: number;

  /** 七维度评分详情 */
  dimensions: Record<string, DimensionScore>;

  /** 检测到的AI痕迹列表 */
  detected_patterns: string[];

  /** 是否需要去痕迹 */
  needs_humanization: boolean;
}

// ==================== 改写验证相关 ====================

/**
 * 改写效果验证结果
 */
export interface HumanizeVerification {
  /** 改写前AI特征分数 */
  score_before: number;

  /** 改写后AI特征分数 */
  score_after: number;

  /** 改进幅度 (score_before - score_after) */
  improvement: number;

  /** 是否成功降低AI痕迹 */
  success: boolean;

  /** 改进项列表 */
  improvements: string[];

  /** 遗留问题列表 */
  remaining_issues: string[];
}

// ==================== 会话记录相关 ====================

/**
 * 会话详情 (7天后过期)
 */
export interface HumanizeSessionDetail {
  /** 改写前七维度评分 */
  dimensions_before: Record<string, any>;

  /** 改写后七维度评分 */
  dimensions_after: Record<string, any>;

  /** 检测到的AI痕迹列表 */
  detected_patterns: string[];

  /** 原文预览 (前200字) */
  original_preview?: string;

  /** 改写后预览 (前200字) */
  humanized_preview?: string;
  original_full?: string;
  humanized_full?: string;

  /** 过期时间 */
  expires_at: string;
}

/**
 * 去痕迹会话记录
 */
export interface HumanizeSession {
  /** 会话ID (跳过时为null) */
  id: string | null;

  /** 用户ID */
  user_id: string;

  /** AI功能类型 */
  ai_function: string;

  /** 改写前AI特征分数 */
  score_before: number;

  /** 改写后AI特征分数 */
  score_after: number;

  /** 改进幅度 */
  improvement: number;

  /** 改写强度 */
  intensity: HumanizeIntensity;

  /** 用户是否接受 (null=未反馈, true=接受, false=拒绝) */
  user_accepted: boolean | null;

  /** 处理耗时 (秒) */
  processing_time: number;

  /** 消耗Token数 */
  tokens_used: number;

  /** 成本 (美元) */
  cost: number;

  /** 创建时间 */
  created_at: string;

  /** 会话详情 (可能为空，如果已过期) */
  detail?: HumanizeSessionDetail;

  /** 是否跳过改写（检测分低于阈值） */
  skipped?: boolean;
}

/**
 * 历史记录响应 (分页)
 */
export interface HumanizeHistoryResponse {
  /** 总记录数 */
  total: number;

  /** 会话列表 */
  items: HumanizeSession[];

  /** 当前页码 */
  page: number;

  /** 每页数量 */
  page_size: number;
}

/**
 * 统计数据响应
 */
export interface HumanizeStatsResponse {
  /** 总使用次数 */
  total_uses: number;

  /** 平均改进幅度 */
  avg_improvement: number;

  /** 接受率 */
  accept_rate: number;

  /** 总Token消耗 */
  total_tokens: number;

  /** 总成本 */
  total_cost: number;

  /** 最常用功能 */
  most_used_function: string | null;
}

// ==================== SSE流式事件 ====================

/**
 * 流式事件类型
 */
export interface HumanizeStreamEvent {
  /** 事件类型 */
  type: 'chunk' | 'progress' | 'done' | 'error' | 'info';

  /** 文本片段 (type=chunk时) */
  content?: string;

  /** 当前阶段 (type=progress时) */
  stage?: 'detecting' | 'detected' | 'rewriting' | 'verifying';

  /** 提示信息 (type=progress/info/error时) */
  message?: string;

  /** 检测分数 (type=progress, stage=detected时) */
  score?: number;

  /** 会话ID (type=done时) */
  session_id?: string;

  /** 改进幅度 (type=done时) */
  improvement?: number;

  /** 处理耗时 (type=done时) */
  processing_time?: number;

  /** Token消耗 (type=done时) */
  tokens_used?: number;

  /** 是否跳过改写 (type=done时) */
  skipped?: boolean;
}

// ==================== 用户画像相关 ====================

/**
 * 显示模式
 */
export type DisplayMode = 'detailed' | 'simplified' | 'silent';

/**
 * 用户画像
 */
export interface UserProfile {
  /** 画像ID */
  id: string;

  /** 用户ID */
  user_id: string;

  /** 全局开关 */
  humanize_enabled_global: boolean;

  /** 分功能开关 */
  humanize_enabled_by_function: Record<string, boolean>;

  /** 偏好强度 */
  preferred_intensity: HumanizeIntensity | null;

  /** 偏好速度优于质量 */
  preferred_speed_over_quality: boolean;

  /** 显示模式 */
  display_mode: DisplayMode;

  /** 总使用次数 */
  total_uses: number;

  /** 平均文本长度 */
  avg_text_length: number | null;

  /** 最常用功能 */
  most_used_function: string | null;

  /** 是否小说作者 */
  is_novel_writer: boolean;

  /** 总接受次数 */
  total_accepted: number;

  /** 总拒绝次数 */
  total_rejected: number;

  /** 接受率 */
  accept_rate: number;

  /** 创建时间 */
  created_at: string;

  /** 更新时间 */
  updated_at: string;
}

/**
 * 用户画像更新请求
 */
export interface UserProfileUpdateRequest {
  /** 全局开关 */
  humanize_enabled_global?: boolean;

  /** 分功能开关 */
  humanize_enabled_by_function?: Record<string, boolean>;

  /** 偏好强度 */
  preferred_intensity?: HumanizeIntensity | null;

  /** 显示模式 */
  display_mode?: DisplayMode;
}

// ==================== 请求类型 ====================

/**
 * 去痕迹请求
 */
export interface HumanizeRequest {
  /** 待去痕迹的文本 */
  text: string;

  /** 改写强度 */
  intensity: HumanizeIntensity;

  /** AI功能类型 */
  ai_function?: string;
}

/**
 * 用户反馈请求
 */
export interface UserFeedbackRequest {
  /** 会话ID */
  session_id: string;

  /** 是否接受结果 */
  accepted: boolean;
}
