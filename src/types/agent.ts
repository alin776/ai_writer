/**
 * Agent系统 - TypeScript类型定义
 */

import { z } from 'zod';

// ==================== 基础类型 ====================

/** Agent Skill 定义（后端 GET /skills 返回） */
export interface Skill {
  name: string;
  description: string;
  group: string;
  allowed_tools?: string[];
  content?: string;
  enabled?: boolean;
}

export interface AgentChatRequest {
  message: string;
  mode?: 'planning';  // Agent执行模式：planning(先规划再执行)
  tool_policy?: 'auto' | 'no_tool' | 'cache_only';
  work_id?: string;
  chapter_id?: string;
  conversation_id?: string;
  /** 知识库文件路径列表，V2 后端顶层字段 */
  knowledge_files?: string[];
  /** 用户在编辑器中选中的引用文本 */
  quoted_text?: string;
  /** 用户主动选择的 Skill 名称（如 chapter-review） */
  skill?: string;
  context?: {
    chapter_context?: string;
    text?: string;
    current_content?: string;
    /** 编辑器选中的文字（纯文本） */
    selected_text?: string;
    /** 编辑器选中的文字（保留HTML格式） */
    selected_text_html?: string;
    /** 选中文字在编辑器中的位置 */
    selection_position?: {
      from: number;
      to: number;
    };
    /** 前端结构性定位结果（用于 locate_content 快速路径） */
    locate_node_id?: string;
    locate_paragraph_index?: number;
    locate_method?: string;
    locate_original_text?: string;
    locate_before_anchor?: string;
    locate_after_anchor?: string;
    nodes_info?: string;
    [key: string]: any;
  };
}

export interface AgentChatResponse {
  response: string;
  conversation_id: string;
  agent_steps: AgentStep[];
  suggested_actions: string[];
  metadata: AgentMetadata;
  /** 编辑器操作指令（用于修改/续写） */
  editor_action?: EditorAction;
}

/** 编辑器操作类型 */
export interface EditorAction {
  /** 操作类型：modify(修改) | continue(续写) | insert(插入) | none(无操作) */
  type: 'modify' | 'continue' | 'insert' | 'none';
  /** 原始文字（仅 modify 时有值） */
  original_text?: string;
  /** 新文字（修改后/续写/插入的内容） */
  new_text?: string;
  /** 新文字（HTML格式） */
  new_text_html?: string;
  /** 插入位置（仅 insert 时有值） */
  position?: {
    from: number;
    to: number;
  };
  /** 是否需要用户确认 */
  requires_confirmation?: boolean;
  /** 操作描述 */
  description?: string;
  /** 锚点定位：修改点前的文本（30-50字），用于位置失效时重新定位 */
  before_anchor?: string;
  /** 锚点定位：修改点后的文本（30-50字），用于位置失效时重新定位 */
  after_anchor?: string;
  /** 🆕 节点 ID（最高优先级定位，来自 UniqueID 扩展） */
  node_id?: string;
  /** 🆕 段落索引（可用于从 getAllNodes() 获取 node_id） */
  paragraph_index?: number;
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
  task_id: number | string;
  description: string;
  status: TaskStatus;
  depends_on: string[];
  result?: any;
  error?: string;
}

export type PlanStatus = 'pending' | 'running' | 'completed' | 'failed';
export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'skipped';

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
  flowItems?: FlowItem[];  // v5.1: 执行轨迹绑定到消息
  tasksSnapshot?: TaskSnapshot[]; // v6.2: 任务列表快照（用于历史执行轨迹）
}

export interface TaskSnapshot {
  task_id: number | string;
  description: string;
  tool?: string;
  estimated_time?: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'skipped';
  elapsed_time?: number;
  progress_status?: string;
}

export interface ChatInputProps {
  onSend: (message: string, context?: any) => void;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
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
 * Agent 活动类型（用于实时进度展示）
 * 注意：与 activity.ts 中的 ActivityType 枚举不同，这是 Agent 专用的活动类型
 */
export type AgentActivityType = 'intent_analysis' | 'thinking' | 'tool_execution' | 'generating';

/**
 * 活动状态
 */
export type ActivityStatus = 'active' | 'completed' | 'failed';

/**
 * 活动项
 * 用于实时进度展示
 */
export interface ActivityItem {
  id: string;
  type: AgentActivityType;
  description: string;
  timestamp: string;
  status: ActivityStatus;
  node?: string;  // LangGraph节点名
  tool?: string;  // 工具名（如果是工具调用）
  details?: Record<string, any>;  // 额外信息
  elapsedTime?: number;  // 执行时间（秒）
}

// ==================== ExecutionFlow 执行轨迹 (v5.0) ====================

/**
 * 执行轨迹项类型
 */
export type FlowItemType = 'text' | 'step' | 'output' | 'agent_header' | 'completion' | 'revision' | 'operate' | 'todo';

// ==================== 知识调取相关类型 (v6.0) ====================

/**
 * 知识项
 */
export interface KnowledgeItem {
  name: string;            // "林逸 - 主角"
  tag?: string;            // "人物" | "地点" | "设定" | "规范"
  similarity?: number;     // 0.89 (检索结果用)
  link?: string;           // 点击跳转链接
}

/**
 * 知识调取数据
 */
export interface KnowledgeFlowData {
  title: string;           // "世界观已加载(5)"
  icon: string;            // "BookOpen" | "FileText" | "Search"
  items: KnowledgeItem[];
}

/**
 * 执行步骤数据
 */
export interface StepFlowData {
  stepId: number;
  title: string;           // "获取世界观设定"
  status: 'running' | 'done' | 'error';
  description?: string;    // 步骤描述
  toolName?: string;       // 原始工具名（如 "read_file"）
  toolInput?: any;         // 原始工具输入参数
  knowledge?: KnowledgeFlowData[];  // 知识调取列表
  toolCall?: {
    icon: string;          // "Wrench"
    name: string;          // "get_worldview_summary"
  };
  revision?: RevisionFlowData;  // 内嵌的修订胶囊（v7.3）
  revisionItemId?: string;      // 关联的 FlowItem ID（用于回调）
  // ── 子 Agent 嵌套字段 ──
  parentStepId?: number;           // 非空 = 这是子步骤
  isTask?: boolean;                // true = task 工具调用
  isMemory?: boolean;              // true = knowledge/ 写入（Memory Updated 展示）
  childSteps?: ChildStepData[];    // 子步骤列表（仅 task 步骤有）
  childToolCount?: number;         // 后端返回的子工具总数
}

/** 子步骤数据（轻量，只保留展示所需字段） */
export interface ChildStepData {
  stepId: number;
  title: string;
  status: 'running' | 'done';
  toolName?: string;
  toolInput?: any;
}

/**
 * 最终输出数据
 */
export interface OutputFlowData {
  intro?: string;          // "第五章已续写完成！本章主要讲述..."
  introHighlight?: string; // "林逸开始外门修炼" (加粗部分)
  title: string;           // "第五章：外门初修"
  content: string;         // 章节内容 (支持Markdown)
  isApplicable?: boolean;  // 是否可应用到编辑器（显示"应用到章节"按钮）
}

/**
 * Agent头部数据
 */
export interface AgentHeaderFlowData {
  name?: string;           // "文枢AI"
  badge?: string;          // 可选标签
}

/**
 * 完成状态数据
 */
export interface CompletionFlowData {
  text?: string;           // "任务已完成"
  memory_count?: number;   // knowledge/ 写入次数（已自动落盘）
}

/**
 * AI 说明文字数据
 */
export interface TextFlowData {
  content: string;
}

// ==================== 修订卡片类型 (v7.0) ====================

/**
 * 修订类型
 */
export type RevisionType = 'append' | 'replace' | 'insert' | 'create' | 'rename';

/**
 * 修订状态
 */
export type RevisionStatus = 'pending' | 'accepted' | 'discarded';

/**
 * 改写版本
 */
export interface RewriteVersion {
  style_name: string;
  reason: string;
  content: string;
}

/**
 * 修订卡片数据
 */
export interface RevisionFlowData {
  revisionType: RevisionType;
  status: RevisionStatus;
  operation?: string;
  requestId?: string;
  chapterId?: string;
  chapterTitle?: string;
  contentPreview?: string;      // 内容预览（前50字）
  oldTitle?: string;            // 原标题（rename 类型）
  newTitle?: string;            // 新标题（rename 类型）
  versions?: RewriteVersion[];  // 改写版本（replace 类型）
  index?: number;               // buffer 操作索引（用于 changesApi 单条操作）
  indices?: number[];            // 所有 buffer 索引（同 path 累加时保留所有）
  path?: string;                 // 文件路径（用于多文件去重/累加）
  addLines?: number;             // 新增行数
  delLines?: number;             // 删除行数
  // v7.2: 撤销/重做支持
  originalContent?: string;     // 原始内容快照（用于撤销）
  newContent?: string;          // 新内容快照（用于重做）
  oldString?: string;           // 原始文本片段（edit 操作，来自后端）
  newString?: string;           // 新文本片段（edit/write 操作，来自后端）
  diffPairs?: Array<{ oldString: string; newString: string }>;  // 同 path 累加时保留所有 diff 对（用于 session 恢复重放）
  editorPosition?: { from: number; to: number };  // 编辑器位置
  selectedVersion?: number;     // 选择的改写版本索引
}

// ==================== Operate 操作轨迹类型 (v10.0) ====================

/**
 * Operate 操作类型
 */
export type OperateOperationType = 'append' | 'replace' | 'insert' | 'content' | 'create' | 'title';

/**
 * Operate 定位方式
 */
export type OperateLocateMethod = 'direct' | 'text_match' | 'semantic' | 'none' | 'fallback' | 'failed';

/**
 * Operate 阶段状态
 */
export type OperatePhaseStatus = 'pending' | 'running' | 'done' | 'skipped';

/**
 * Operate 标签
 */
export interface OperateTag {
  label: string;      // 标签名：输入、工具、方式、位置、操作、状态
  value: string;      // 显示值（已转换为用户友好名称）
  icon?: string;      // Lucide 图标名
  variant?: 'default' | 'success' | 'warning' | 'info';
}

/**
 * Operate 阶段数据
 */
export interface OperatePhaseData {
  phase: 1 | 2 | 3;
  title: string;
  status: OperatePhaseStatus;
  tags: OperateTag[];
}

/**
 * Operate 轨迹数据（流事件）
 */
export interface OperateFlowData {
  stepId: number;
  operation: OperateOperationType;     // 原始操作类型
  phases: OperatePhaseData[];          // 三阶段数据
  status: 'running' | 'done' | 'error';
  // 定位结果（阶段2）
  locateMethod?: OperateLocateMethod;  // direct | text_match | semantic | none | fallback
  locateTarget?: string;               // "第五章 · 第2段"
  // 执行结果（阶段3）
  targetOperation?: string;            // 实际执行的操作（如 content → replace_all）
  toolUsed?: string;                   // 使用的工具
  chapterId?: string;
  chapterTitle?: string;
  requiresConfirmation?: boolean;
  revisionId?: string;
  requestId?: string;
}

// ==================== Todo 类型 (Claude Code 风格) ====================

/**
 * Todo 项
 */
export interface TodoItem {
  description: string;
  status: 'pending' | 'in_progress' | 'completed';
}

/**
 * TodoList 数据（write_todos 工具输出）
 */
export interface TodoFlowData {
  todos: TodoItem[];
  currentTask?: string;  // 当前执行的任务描述
}

/**
 * 执行轨迹项
 */
export interface FlowItem {
  id: string;
  type: FlowItemType;
  data: TextFlowData | StepFlowData | OutputFlowData | AgentHeaderFlowData | CompletionFlowData | RevisionFlowData | OperateFlowData | TodoFlowData;
  timestamp: string;
}

/**
 * 增强版任务开始事件（后端 v5.0 发送）
 */
export interface EnhancedTaskStartEvent {
  task_id: number;
  description: string;
  tool?: string;
  params?: Record<string, any>;
  // v5.0 增强字段
  explanation?: string;      // AI 说明文字
  icon?: string;             // Lucide 图标名
  tool_title?: string;       // 工具标题
  tool_description?: string; // 工具描述
}

// ==================== 非阻塞式修订 (v7.5) ====================

/**
 * 待处理修订
 */
export interface PendingRevision {
  id: string;                    // 前端生成的唯一ID
  requestId: string;             // 后端的request_id
  chapterId: string;
  chapterTitle: string;
  revisionType: RevisionType;
  content: string;               // 完整内容
  originalContent?: string;      // 原内容（replace类型需要）
  contentPreview: string;        // 内容预览（前50字）
  position?: { from: number; to: number };
  operation?: string;            // 操作类型
  editorAction?: EditorAction;   // 编辑器操作信息
  status: 'pending' | 'accepted' | 'rejected';
  createdAt: number;
  messageId?: string;            // 关联的消息ID
  flowItemId?: string;           // 关联的FlowItem ID
}

/**
 * 修订会话
 */
export interface RevisionSession {
  sessionId: string;             // 对应一次Agent执行
  conversationId: string;        // 对话ID
  revisions: PendingRevision[];  // 修订列表
  status: 'in_progress' | 'completed';
  pendingCount: number;          // 待确认数量
  acceptedCount: number;         // 已采纳数量
  rejectedCount: number;         // 已弃用数量
  startTime: number;
  endTime?: number;
}


