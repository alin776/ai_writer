/**
 * Agent系统 - TypeScript类型定义
 */

// ==================== 基础类型 ====================

export interface AgentChatRequest {
  message: string;
  work_id?: string;
  chapter_id?: string;
  conversation_id?: string;
  context?: {
    chapter_context?: string;
    text?: string;
    current_content?: string;
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
