/**
 * 小说分析系统类型定义
 */

/**
 * 分析状态枚举
 */
export enum NovelAnalysisStatus {
  PENDING = 'pending',      // 等待中
  PROCESSING = 'processing', // 分析中
  COMPLETED = 'completed',   // 已完成
  FAILED = 'failed'          // 失败
}

/**
 * 分析阶段枚举
 */
export enum AnalysisStage {
  MICRO = 'micro_analysis',   // 微观分析阶段
  MACRO = 'macro_analysis'    // 宏观分析阶段
}

/**
 * 分析进度信息
 */
export interface AnalysisProgress {
  status: NovelAnalysisStatus;
  stage: AnalysisStage | null;
  total_chapters: number;
  analyzed_chapters: number;
  progress_percentage: number;
  error_message?: string;
}

/**
 * 实体信息（角色、物品、地点）
 */
export interface EntityInfo {
  type: string;           // 类型：character/item/location
  name: string;           // 名称
  description: string;    // 描述
}

/**
 * 详细事件
 */
export interface DetailedEvent {
  time_context: string;           // 时间上下文
  action_summary: string;         // 动作摘要
  entities_involved: EntityInfo[]; // 涉及的实体
}

/**
 * 微观分析结果（单章）
 */
export interface MicroAnalysisResult {
  chapter_theme: string;           // 章节主题
  detailed_events: DetailedEvent[]; // 详细事件列表
}

/**
 * 分析状态响应
 */
export interface AnalysisStatusResponse {
  workId: string;
  status: NovelAnalysisStatus;
  stage: AnalysisStage | null;
  totalChapters: number;
  analyzedChapters: number;
  progressPercentage: number;
  createdAt: string;
  updatedAt: string;
  errorMessage?: string;
}

/**
 * 分析结果响应
 */
export interface AnalysisResultResponse {
  workId: string;
  status: NovelAnalysisStatus;
  microResults: MicroAnalysisResult[] | null; // 微观分析结果列表
  macroResults: string | null;                // 宏观分析报告（完整文本）
  completedAt: string | null;
}

/**
 * 触发分析请求响应
 */
export interface StartAnalysisResponse {
  message: string;
  work_id: string;
  analysis_id: string;
  status: NovelAnalysisStatus;
}
