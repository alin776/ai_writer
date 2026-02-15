/**
 * Agent type definitions for frontend request/response and execution flow data.
 */

import { z } from 'zod';


export interface AgentChatRequest {
  message: string;
  mode?: 'planning' | 'react';
  tool_policy?: 'auto' | 'no_tool' | 'cache_only';
  work_id?: string;
  chapter_id?: string;
  conversation_id?: string;
  enable_reflection?: boolean;
  context?: {
    chapter_context?: string;
    text?: string;
    current_content?: string;
    knowledge_doc_ids?: string[];
    knowledge_tags?: string[];
    use_optimization?: boolean;
    selected_text?: string;
    selected_text_html?: string;
    selection_position?: {
      from: number;
      to: number;
    };
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
  editor_action?: EditorAction;
}

export interface EditorAction {
  type: 'modify' | 'continue' | 'insert' | 'none';
  original_text?: string;
  new_text?: string;
  new_text_html?: string;
  position?: {
    from: number;
    to: number;
  };
  requires_confirmation?: boolean;
  description?: string;
  before_anchor?: string;
  after_anchor?: string;
  node_id?: string;
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


export interface Message {
  role: 'user' | 'agent';
  content: string;
  agentSteps?: AgentStep[];
  metadata?: AgentMetadata;
  timestamp: string;
  flowItems?: FlowItem[];
  tasksSnapshot?: TaskSnapshot[];
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


export type AgentActivityType = 'intent_analysis' | 'thinking' | 'tool_execution' | 'generating';

export type ActivityStatus = 'active' | 'completed' | 'failed';

export interface ActivityItem {
  id: string;
  type: AgentActivityType;
  description: string;
  timestamp: string;
  status: ActivityStatus;
  node?: string;
  tool?: string;
  details?: Record<string, any>;
  elapsedTime?: number;
}

export interface ProgressEvent {
  type: 'progress';
  step: 'intent_analysis' | 'thinking' | 'tool_execution' | 'generating';
  description: string;
  node?: string;
  details?: Record<string, any>;
  timestamp: string;
}

export interface ToolCallEvent {
  tool: string;
  args: any;
  timestamp: string;
}


export interface ProgressData {
  progress: number;
  eta: number | null;
  eta_display: string;
  eta_confidence: 'low' | 'medium' | 'high';
  current_step: number;
  total_steps: number;
  step_description: string;
  elapsed: number;
  current_node?: string;
  current_node_display?: string | null;
  current_node_description?: string | null;
}

export interface EnhancedProgressEvent extends ProgressEvent {
  progress?: number;
  eta?: number | null;
  eta_display?: string;
  eta_confidence?: 'low' | 'medium' | 'high';
  current_step?: number;
  total_steps?: number;
  step_description?: string;
  elapsed?: number;
}


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

export const EnhancedProgressEventSchema = z.object({
  type: z.literal('progress'),
  step: z.enum(['intent_analysis', 'thinking', 'tool_execution', 'generating']),
  description: z.string(),
  node: z.string().optional(),
  details: z.record(z.string(), z.any()).optional(),
  timestamp: z.string(),
  progress: z.number().min(0).max(100).optional(),
  eta: z.number().nullable().optional(),
  eta_display: z.string().optional(),
  eta_confidence: z.enum(['low', 'medium', 'high']).optional(),
  current_step: z.number().int().positive().optional(),
  total_steps: z.number().int().positive().optional(),
  step_description: z.string().optional(),
  elapsed: z.number().nonnegative().optional()
});


export type FlowItemType = 'text' | 'tool' | 'content' | 'step' | 'output' | 'agent_header' | 'completion' | 'summarization' | 'revision' | 'explore_round' | 'explore_summary' | 'operate';


export interface KnowledgeItem {
  name: string;
  tag?: string;
  similarity?: number;
  link?: string;
}

export interface KnowledgeFlowData {
  title: string;
  icon: string;            // "BookOpen" | "FileText" | "Search"
  items: KnowledgeItem[];
}

export interface StepFlowData {
  stepId: number;
  title: string;
  status: 'running' | 'done' | 'error';
  description?: string;
  knowledge?: KnowledgeFlowData[];
  toolCall?: {
    icon: string;          // "Wrench"
    name: string;          // "get_worldview_summary"
  };
  revision?: RevisionFlowData;
  revisionItemId?: string;
}

export interface OutputFlowData {
  intro?: string;
  introHighlight?: string;
  title: string;
  content: string;
  isApplicable?: boolean;
}

export interface AgentHeaderFlowData {
  name?: string;
  badge?: string;
}

export interface CompletionFlowData {
  text?: string;
}

export interface SummarizationFlowData {
  status: 'running' | 'done';
  reason?: string;
  taskClassification: {
    inputTasks: Array<{ tool: string; description: string }>;
    outputTasks: Array<{ tool: string; description: string }>;
    displayTasks: Array<{ tool: string; description: string }>;
  };
  contextStats: {
    originalLength: number;
    compressedLength: number;
    mode: string;
  };
}

export interface TextFlowData {
  content: string;
}

export interface ToolFlowData {
  taskId: number;
  icon: string;
  title: string;
  description: string;
  status: 'running' | 'done' | 'error';
}


/**
 * Agentic budget data
 */
export interface BudgetFlowData {
  budget?: {
    max_steps?: number;
    used_steps?: number;
    max_cost?: number;
    used_cost?: number;
    max_time_ms?: number;
  };
}

/**
 * Agentic decision data
 */
export interface DecisionFlowData {
  status?: 'running' | 'done' | 'error' | string;
  goal?: string;
  reason?: string;
  candidates?: Array<{
    id?: string;
    identifier?: string;
    title?: string;
  }>;
  decision?: {
    id?: string;
    identifier?: string;
    reason?: string;
    risk?: string;
  };
}

/**
 * Agentic reflection data
 */
export interface ReflectFlowData {
  summary?: string;
  nextAction?: string;
  stopReason?: string;
}
export interface ContentFlowData {
  content: string;
}


export type RevisionType = 'append' | 'replace' | 'insert' | 'create' | 'rename';

export type RevisionStatus = 'pending' | 'accepted' | 'discarded';

export interface RewriteVersion {
  style_name: string;
  reason: string;
  content: string;
}

export interface RevisionFlowData {
  revisionType: RevisionType;
  status: RevisionStatus;
  statusUpdatedAt?: string;
  requestId?: string;
  chapterId?: string;
  chapterTitle?: string;
  contentPreview?: string;
  oldTitle?: string;
  newTitle?: string;
  versions?: RewriteVersion[];
  originalContent?: string;
  newContent?: string;
  editorPosition?: { from: number; to: number };
  selectedVersion?: number;
}


export interface ExploreToolCall {
  type: 'Search' | 'Locate' | 'ReadRaw' | 'ReadParagraph' | 'ListChapters' | 'ListParagraphs' | 'Worldview';
  value: string;
  highlight?: string;
}

export interface ExploreEvidenceItem {
  chapter?: number;
  paragraph?: number;
  text: string;
  chapterOrder?: number;
  chapterTitle?: string;
  paragraphIndex?: number;
}

export interface ExploreRoundFlowData {
  stepId: number;
  roundIdx: number;
  title: string;
  reason?: string;
  toolCalls: ExploreToolCall[];
  hitCount: number;
  missingItems: string[];
  statusText: string;
  evidences: ExploreEvidenceItem[];
  reviewStatus: string;
  status: 'running' | 'done';
}

export interface ExploreStats {
  worldview: number;
  chapters: string;    // "1-4"
  evidences: number;
  coverage: string;
}

export interface ExploreSummaryFlowData {
  stepId: number;
  totalRounds: number;
  summary: string;
  nextAction: string;
  nextTool?: string;
  sufficient?: boolean;
  coverage?: string;
  stats: ExploreStats;
}

export interface ExploreRound {
  id: string;
  title?: string;
  reason?: string;
  query?: string;
  search?: {
    query?: string;
    results?: any[];
  };
  locate?: {
    chapterOrder?: number;
    chapterTitle?: string;
    paragraphIndex?: number;
  };
  readRaw?: {
    chapterOrder?: number;
    chapterTitle?: string;
  };
  readSegment?: {
    chapterOrder?: number;
    chapterTitle?: string;
    paragraphIndex?: number;
  };
  review?: {
    status: 'pass' | 'insufficient' | 'pending';
  };
  evidence?: ExploreEvidenceItem[];
}

export interface ExploreFlowData {
  rounds: ExploreRound[];
}


export type OperateOperationType = 'append' | 'replace' | 'insert' | 'content' | 'create' | 'title';

export type OperateLocateMethod = 'direct' | 'text_match' | 'semantic' | 'none' | 'fallback' | 'failed';

export type OperatePhaseStatus = 'pending' | 'running' | 'done' | 'skipped';

export interface OperateTag {
  label: string;
  value: string;
  icon?: string;
  variant?: 'default' | 'success' | 'warning' | 'info';
}

export interface OperatePhaseData {
  phase: 1 | 2 | 3;
  title: string;
  status: OperatePhaseStatus;
  tags: OperateTag[];
}

export interface OperateFlowData {
  stepId: number;
  operation: OperateOperationType;
  phases: OperatePhaseData[];
  status: 'running' | 'done' | 'error';
  locateMethod?: OperateLocateMethod;  // direct | text_match | semantic | none | fallback
  locateTarget?: string;
  targetOperation?: string;
  toolUsed?: string;
  chapterId?: string;
  chapterTitle?: string;
  requiresConfirmation?: boolean;
  revisionId?: string;
  requestId?: string;
}

export interface FlowItem {
  id: string;
  type: FlowItemType;
  data: TextFlowData | ToolFlowData | ContentFlowData | StepFlowData | OutputFlowData | AgentHeaderFlowData | CompletionFlowData | SummarizationFlowData | RevisionFlowData | ExploreRoundFlowData | ExploreSummaryFlowData | ExploreFlowData | OperateFlowData;
  timestamp: string;
}

export interface EnhancedTaskStartEvent {
  task_id: number;
  description: string;
  tool?: string;
  params?: Record<string, any>;
  explanation?: string;
  icon?: string;
  tool_title?: string;
  tool_description?: string;
}


export interface PendingRevision {
  id: string;
  requestId: string;
  chapterId: string;
  chapterTitle: string;
  revisionType: RevisionType;
  content: string;
  originalContent?: string;
  contentPreview: string;
  position?: { from: number; to: number };
  operation?: string;
  editorAction?: EditorAction;
  status: 'pending' | 'accepted' | 'rejected';
  createdAt: number;
  messageId?: string;
  flowItemId?: string;
}

export interface RevisionSession {
  sessionId: string;
  conversationId: string;
  revisions: PendingRevision[];
  status: 'in_progress' | 'completed';
  pendingCount: number;
  acceptedCount: number;
  rejectedCount: number;
  startTime: number;
  endTime?: number;
}


