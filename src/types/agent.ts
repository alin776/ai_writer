/**
 * Agent系统 - TypeScript类型定义
 */

import { z } from 'zod';

// ==================== 基础类型 ====================

export interface AgentChatRequest {
  message: string;
  mode?: 'planning' | 'react';  // Agent执行模式：planning(先规划再执行) 或 react(边思考边执行)
  work_id?: string;
  chapter_id?: string;
  conversation_id?: string;
  enable_reflection?: boolean;  // 启用 DeepAgent 反思模式
  context?: {
    chapter_context?: string;
    text?: string;
    current_content?: string;
    /** 知识库文档ID列表，用于@引用指定文档 */
    knowledge_doc_ids?: string[];
    /** @deprecated 已弃用，请使用 knowledge_doc_ids。此字段将在后续版本移除 */
    knowledge_tags?: string[];
    use_optimization?: boolean;
    [key: string]: any;
  };
}

export interface AgentChatResponse {
  response: string;
  conversation_id: string;
  agent_steps: AgentStep[];
  suggested_actions: string[];
  metadata: AgentMetadata;
}

export interface AgentStep {
  step: string;
  result: string;
  usage?: TokenUsage;
}

export interface TokenUsage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

export interface AgentMetadata {
  intent: AgentIntent;
  memory_quality: string;
  timestamp: string;
}

export type AgentIntent = 'writing' | 'planning' | 'analysis' | 'stuck' | 'general';
export interface HistorySessionItem {
  sessionId: string;
  title: string;
  messageCount: number;
  updatedAt: string;
  archivedAt?: string | null;
  lastMessagePreview?: string;
  conversationId?: string;
  workId?: string;
  chapterId?: string;
  titleLocked?: boolean;
}

// ==================== 会话管理 ====================

export interface AgentSession {
  session_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  archived_at?: string | null;
  message_count?: number;
  conversation_id?: string;
  work_id?: string;
  chapter_id?: string;
}

export interface CreateAgentSessionResponse {
  session_id: string;
  title?: string;
  conversation_id?: string;
  created_at?: string;
}

// ==================== 计划管理 ====================

export interface PlanCreationRequest {
  goal: string;
  genre?: string;
  work_id?: string;
  context?: Record<string, any>;
}

export interface PlanResponse {
  plan_id: string;
  goal: string;
  tasks: PlanTask[];
  status: PlanStatus;
  progress: number;
}

export interface PlanTask {
  task_id: string;
  description: string;
  status: TaskStatus;
  depends_on: string[];
  result?: any;
  error?: string;
}

export type PlanStatus = 'pending' | 'in_progress' | 'completed' | 'failed';
export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'failed' | 'skipped';

// ==================== 人机协同 (HITL) ====================

export interface ApprovalResponse {
  request_id: string;
  title: string;
  description: string;
  proposed_action: Record<string, any>;
  alternatives: Array<Record<string, any>>;
  status: ApprovalStatus;
  created_at: string;
  timeout_at?: string;
}

export interface ApprovalActionRequest {
  action: 'approve' | 'reject' | 'modify';
  modifications?: Record<string, any>;
  feedback?: string;
}

export type ApprovalStatus = 'pending' | 'approved' | 'rejected' | 'timeout';

// ==================== 记忆系统 ====================

export interface MemoryContext {
  success: boolean;
  data: MemoryData;
}

export interface MemoryData {
  user_preferences: UserPreferences;
  user_profile: UserProfile;
  writing_style?: WritingStyle;
}

export interface UserPreferences {
  preferred_genres: string[];
  writing_style: string;
  tone_preference: string;
  length_preference: string;
  complexity_level: string;
  [key: string]: any;
}

export interface UserProfile {
  skill_level: SkillLevel;
  total_sessions: number;
  total_works: number;
  favorite_operations: string[];
  interaction_mode: InteractionMode;
  [key: string]: any;
}

export interface WritingStyle {
  vocabulary_richness: number;
  avg_sentence_length: number;
  common_phrases: string[];
  tone_patterns: string[];
  [key: string]: any;
}

export type SkillLevel = 'beginner' | 'intermediate' | 'advanced' | 'expert';
export type InteractionMode = 'autonomous' | 'guided' | 'manual';

// ==================== UI组件类型 ====================

export interface Message {
  role: 'user' | 'agent';
  content: string;
  agentSteps?: AgentStep[];
  metadata?: AgentMetadata;
  timestamp: string;
}

export interface ChatInputProps {
  onSend: (message: string, context?: any) => void;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
  mode: 'plan' | 'agent';
  onModeChange: (mode: 'plan' | 'agent') => void;
  isLoading?: boolean;
  onStop?: () => void;
}

export interface AgentMessageProps {
  message: Message;
  isLatest?: boolean;
}

export interface SuggestedActionsProps {
  actions: string[];
  onActionClick: (action: string) => void;
}

// ==================== API响应类型 ====================

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

// ==================== ActivityStream 活动流 ====================

/**
 * 活动类型
 */
export type ActivityType = 'intent_analysis' | 'thinking' | 'tool_execution' | 'generating';

/**
 * 活动状态
 */
export type ActivityStatus = 'active' | 'completed' | 'failed';

/**
 * 活动项
 * 用于ReAct模式的实时进度展示
 */
export interface ActivityItem {
  id: string;
  type: ActivityType;
  description: string;
  timestamp: string;
  status: ActivityStatus;
  node?: string;  // LangGraph节点名
  tool?: string;  // 工具名（如果是工具调用）
  details?: Record<string, any>;  // 额外信息
  elapsedTime?: number;  // 执行时间（秒）
}

/**
 * 进度事件（从后端接收）
 */
export interface ProgressEvent {
  type: 'progress';
  step: 'intent_analysis' | 'thinking' | 'tool_execution' | 'generating';
  description: string;
  node?: string;
  details?: Record<string, any>;
  timestamp: string;
}

/**
 * 工具调用事件（从后端接收）
 */
export interface ToolCallEvent {
  tool: string;
  args: any;
  timestamp: string;
}

// ==================== ProgressTracker 进度追踪 ====================

/**
 * 进度信息（从后端SSE事件接收）
 * 由ProgressTracker生成的完整进度数据
 */
export interface ProgressData {
  progress: number;              // 进度百分比 (0-100)
  eta: number | null;            // 预估剩余时间（秒）
  eta_display: string;           // ETA友好显示（如"2分钟"、"即将完成"）
  eta_confidence: 'low' | 'medium' | 'high';  // ETA置信度
  current_step: number;          // 当前第几步（从1开始）
  total_steps: number;           // 总步数
  step_description: string;      // 步骤描述（如"第2/5步"）
  elapsed: number;               // 已用时间（秒）
  current_node?: string;         // 当前节点名（LangGraph内部名称）
  current_node_display?: string | null; // 当前节点友好名称（如"🧠 意图分析"）
  current_node_description?: string | null; // 当前节点描述（如"正在分析您的需求..."）
}

/**
 * 增强的进度事件（包含ProgressTracker数据）
 * 扩展ProgressEvent，添加进度追踪信息
 */
export interface EnhancedProgressEvent extends ProgressEvent {
  // ProgressTracker提供的字段
  progress?: number;
  eta?: number | null;
  eta_display?: string;
  eta_confidence?: 'low' | 'medium' | 'high';
  current_step?: number;
  total_steps?: number;
  step_description?: string;
  elapsed?: number;
}

// ==================== Zod验证Schema ====================

/**
 * ProgressData的Zod验证Schema
 * ✅ 用于运行时数据验证，确保后端返回的数据符合预期
 */
export const ProgressDataSchema = z.object({
  progress: z.number().min(0).max(100),
  eta: z.number().nullable(),
  eta_display: z.string(),
  eta_confidence: z.enum(['low', 'medium', 'high']),
  current_step: z.number().int().positive(),
  total_steps: z.number().int().positive(),
  step_description: z.string(),
  elapsed: z.number().nonnegative(),
  current_node: z.string().optional(),
  current_node_display: z.string().nullable().optional(),
  current_node_description: z.string().nullable().optional()
});

/**
 * ActivityItem的Zod验证Schema
 */
export const ActivityItemSchema = z.object({
  id: z.string(),
  type: z.enum(['intent_analysis', 'thinking', 'tool_execution', 'generating']),
  description: z.string(),
  timestamp: z.string(),
  status: z.enum(['active', 'completed', 'failed']),
  node: z.string().optional(),
  tool: z.string().optional(),
  details: z.record(z.string(), z.any()).optional(),
  elapsedTime: z.number().optional()
});

/**
 * EnhancedProgressEvent的Zod验证Schema
 */
export const EnhancedProgressEventSchema = z.object({
  type: z.literal('progress'),
  step: z.enum(['intent_analysis', 'thinking', 'tool_execution', 'generating']),
  description: z.string(),
  node: z.string().optional(),
  details: z.record(z.string(), z.any()).optional(),
  timestamp: z.string(),
  // ProgressTracker字段
  progress: z.number().min(0).max(100).optional(),
  eta: z.number().nullable().optional(),
  eta_display: z.string().optional(),
  eta_confidence: z.enum(['low', 'medium', 'high']).optional(),
  current_step: z.number().int().positive().optional(),
  total_steps: z.number().int().positive().optional(),
  step_description: z.string().optional(),
  elapsed: z.number().nonnegative().optional()
});

