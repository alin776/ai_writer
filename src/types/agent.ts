/**
 * Agent绯荤粺 - TypeScript绫诲瀷瀹氫箟
 */

import { z } from 'zod';

// ==================== 鍩虹绫诲瀷 ====================

export interface AgentChatRequest {
  message: string;
  mode?: 'planning' | 'react';  // Agent鎵ц妯″紡锛歱lanning(鍏堣鍒掑啀鎵ц) 鎴?react(杈规€濊€冭竟鎵ц)
  tool_policy?: 'auto' | 'no_tool' | 'cache_only';
  work_id?: string;
  chapter_id?: string;
  conversation_id?: string;
  enable_reflection?: boolean;  // 鍚敤 DeepAgent 鍙嶆€濇ā寮?
  context?: {
    chapter_context?: string;
    text?: string;
    current_content?: string;
    /** 鐭ヨ瘑搴撴枃妗D鍒楄〃锛岀敤浜嶡寮曠敤鎸囧畾鏂囨。 */
    knowledge_doc_ids?: string[];
    /** @deprecated 宸插純鐢紝璇蜂娇鐢?knowledge_doc_ids銆傛瀛楁灏嗗湪鍚庣画鐗堟湰绉婚櫎 */
    knowledge_tags?: string[];
    use_optimization?: boolean;
    /** 缂栬緫鍣ㄩ€変腑鐨勬枃瀛楋紙绾枃鏈級 */
    selected_text?: string;
    /** 缂栬緫鍣ㄩ€変腑鐨勬枃瀛楋紙淇濈暀HTML鏍煎紡锛?*/
    selected_text_html?: string;
    /** 閫変腑鏂囧瓧鍦ㄧ紪杈戝櫒涓殑浣嶇疆 */
    selection_position?: {
      from: number;
      to: number;
    };
    /** 鍓嶇缁撴瀯鎬у畾浣嶇粨鏋滐紙鐢ㄤ簬 locate_content 蹇€熻矾寰勶級 */
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
  /** 缂栬緫鍣ㄦ搷浣滄寚浠わ紙鐢ㄤ簬淇敼/缁啓锛?*/
  editor_action?: EditorAction;
}

/** 缂栬緫鍣ㄦ搷浣滅被鍨?*/
export interface EditorAction {
  /** 鎿嶄綔绫诲瀷锛歮odify(淇敼) | continue(缁啓) | insert(鎻掑叆) | none(鏃犳搷浣? */
  type: 'modify' | 'continue' | 'insert' | 'none';
  /** 鍘熷鏂囧瓧锛堜粎 modify 鏃舵湁鍊硷級 */
  original_text?: string;
  /** 鏂版枃瀛楋紙淇敼鍚?缁啓/鎻掑叆鐨勫唴瀹癸級 */
  new_text?: string;
  /** 鏂版枃瀛楋紙HTML鏍煎紡锛?*/
  new_text_html?: string;
  /** 鎻掑叆浣嶇疆锛堜粎 insert 鏃舵湁鍊硷級 */
  position?: {
    from: number;
    to: number;
  };
  /** 鏄惁闇€瑕佺敤鎴风‘璁?*/
  requires_confirmation?: boolean;
  /** 鎿嶄綔鎻忚堪 */
  description?: string;
  /** 閿氱偣瀹氫綅锛氫慨鏀圭偣鍓嶇殑鏂囨湰锛?0-50瀛楋級锛岀敤浜庝綅缃け鏁堟椂閲嶆柊瀹氫綅 */
  before_anchor?: string;
  /** 閿氱偣瀹氫綅锛氫慨鏀圭偣鍚庣殑鏂囨湰锛?0-50瀛楋級锛岀敤浜庝綅缃け鏁堟椂閲嶆柊瀹氫綅 */
  after_anchor?: string;
  /** 馃啎 鑺傜偣 ID锛堟渶楂樹紭鍏堢骇瀹氫綅锛屾潵鑷?UniqueID 鎵╁睍锛?*/
  node_id?: string;
  /** 馃啎 娈佃惤绱㈠紩锛堝彲鐢ㄤ簬浠?getAllNodes() 鑾峰彇 node_id锛?*/
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

// ==================== 浼氳瘽绠＄悊 ====================

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

// ==================== 璁″垝绠＄悊 ====================

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

// ==================== 浜烘満鍗忓悓 (HITL) ====================

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

// ==================== 璁板繂绯荤粺 ====================

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

// ==================== UI缁勪欢绫诲瀷 ====================

export interface Message {
  role: 'user' | 'agent';
  content: string;
  agentSteps?: AgentStep[];
  metadata?: AgentMetadata;
  timestamp: string;
  flowItems?: FlowItem[];  // v5.1: 鎵ц杞ㄨ抗缁戝畾鍒版秷鎭?
  tasksSnapshot?: TaskSnapshot[]; // v6.2: 浠诲姟鍒楄〃蹇収锛堢敤浜庡巻鍙叉墽琛岃建杩癸級
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

// ==================== API鍝嶅簲绫诲瀷 ====================

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

// ==================== ActivityStream 娲诲姩娴?====================

/**
 * Agent 娲诲姩绫诲瀷锛堢敤浜?ReAct 妯″紡鐨勫疄鏃惰繘搴﹀睍绀猴級
 * 娉ㄦ剰锛氫笌 activity.ts 涓殑 ActivityType 鏋氫妇涓嶅悓锛岃繖鏄?Agent 涓撶敤鐨勬椿鍔ㄧ被鍨?
 */
export type AgentActivityType = 'intent_analysis' | 'thinking' | 'tool_execution' | 'generating';

/**
 * 娲诲姩鐘舵€?
 */
export type ActivityStatus = 'active' | 'completed' | 'failed';

/**
 * 娲诲姩椤?
 * 鐢ㄤ簬ReAct妯″紡鐨勫疄鏃惰繘搴﹀睍绀?
 */
export interface ActivityItem {
  id: string;
  type: AgentActivityType;
  description: string;
  timestamp: string;
  status: ActivityStatus;
  node?: string;  // LangGraph鑺傜偣鍚?
  tool?: string;  // 宸ュ叿鍚嶏紙濡傛灉鏄伐鍏疯皟鐢級
  details?: Record<string, any>;  // 棰濆淇℃伅
  elapsedTime?: number;  // 鎵ц鏃堕棿锛堢锛?
}

/**
 * 杩涘害浜嬩欢锛堜粠鍚庣鎺ユ敹锛?
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
 * 宸ュ叿璋冪敤浜嬩欢锛堜粠鍚庣鎺ユ敹锛?
 */
export interface ToolCallEvent {
  tool: string;
  args: any;
  timestamp: string;
}

// ==================== ProgressTracker 杩涘害杩借釜 ====================

/**
 * 杩涘害淇℃伅锛堜粠鍚庣SSE浜嬩欢鎺ユ敹锛?
 * 鐢盤rogressTracker鐢熸垚鐨勫畬鏁磋繘搴︽暟鎹?
 */
export interface ProgressData {
  progress: number;              // 杩涘害鐧惧垎姣?(0-100)
  eta: number | null;            // 棰勪及鍓╀綑鏃堕棿锛堢锛?
  eta_display: string;           // ETA鍙嬪ソ鏄剧ず锛堝"2鍒嗛挓"銆?鍗冲皢瀹屾垚"锛?
  eta_confidence: 'low' | 'medium' | 'high';  // ETA缃俊搴?
  current_step: number;          // 褰撳墠绗嚑姝ワ紙浠?寮€濮嬶級
  total_steps: number;           // 鎬绘鏁?
  step_description: string;      // 姝ラ鎻忚堪锛堝"绗?/5姝?锛?
  elapsed: number;               // 宸茬敤鏃堕棿锛堢锛?
  current_node?: string;         // 褰撳墠鑺傜偣鍚嶏紙LangGraph鍐呴儴鍚嶇О锛?
  current_node_display?: string | null; // 褰撳墠鑺傜偣鍙嬪ソ鍚嶇О锛堝"馃 鎰忓浘鍒嗘瀽"锛?
  current_node_description?: string | null; // 褰撳墠鑺傜偣鎻忚堪锛堝"姝ｅ湪鍒嗘瀽鎮ㄧ殑闇€姹?.."锛?
}

/**
 * 澧炲己鐨勮繘搴︿簨浠讹紙鍖呭惈ProgressTracker鏁版嵁锛?
 * 鎵╁睍ProgressEvent锛屾坊鍔犺繘搴﹁拷韪俊鎭?
 */
export interface EnhancedProgressEvent extends ProgressEvent {
  // ProgressTracker鎻愪緵鐨勫瓧娈?
  progress?: number;
  eta?: number | null;
  eta_display?: string;
  eta_confidence?: 'low' | 'medium' | 'high';
  current_step?: number;
  total_steps?: number;
  step_description?: string;
  elapsed?: number;
}

// ==================== Zod楠岃瘉Schema ====================

/**
 * ProgressData鐨刏od楠岃瘉Schema
 * 鉁?鐢ㄤ簬杩愯鏃舵暟鎹獙璇侊紝纭繚鍚庣杩斿洖鐨勬暟鎹鍚堥鏈?
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
 * ActivityItem鐨刏od楠岃瘉Schema
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
 * EnhancedProgressEvent鐨刏od楠岃瘉Schema
 */
export const EnhancedProgressEventSchema = z.object({
  type: z.literal('progress'),
  step: z.enum(['intent_analysis', 'thinking', 'tool_execution', 'generating']),
  description: z.string(),
  node: z.string().optional(),
  details: z.record(z.string(), z.any()).optional(),
  timestamp: z.string(),
  // ProgressTracker瀛楁
  progress: z.number().min(0).max(100).optional(),
  eta: z.number().nullable().optional(),
  eta_display: z.string().optional(),
  eta_confidence: z.enum(['low', 'medium', 'high']).optional(),
  current_step: z.number().int().positive().optional(),
  total_steps: z.number().int().positive().optional(),
  step_description: z.string().optional(),
  elapsed: z.number().nonnegative().optional()
});

// ==================== ExecutionFlow 鎵ц杞ㄨ抗 (v5.0) ====================

/**
 * 鎵ц杞ㄨ抗椤圭被鍨?
 */
export type FlowItemType = 'text' | 'tool' | 'content' | 'step' | 'output' | 'agent_header' | 'completion' | 'summarization' | 'revision' | 'explore_round' | 'explore_summary' | 'operate';

// ==================== 鐭ヨ瘑璋冨彇鐩稿叧绫诲瀷 (v6.0) ====================

/**
 * 鐭ヨ瘑椤?
 */
export interface KnowledgeItem {
  name: string;            // "鏋楅€?- 涓昏"
  tag?: string;            // "浜虹墿" | "鍦扮偣" | "璁惧畾" | "瑙勮寖"
  similarity?: number;     // 0.89 (妫€绱㈢粨鏋滅敤)
  link?: string;           // 鐐瑰嚮璺宠浆閾炬帴
}

/**
 * 鐭ヨ瘑璋冨彇鏁版嵁
 */
export interface KnowledgeFlowData {
  title: string;           // "涓栫晫瑙傚凡鍔犺浇(5)"
  icon: string;            // "BookOpen" | "FileText" | "Search"
  items: KnowledgeItem[];
}

/**
 * 鎵ц姝ラ鏁版嵁
 */
export interface StepFlowData {
  stepId: number;
  title: string;           // "鑾峰彇涓栫晫瑙傝瀹?
  status: 'running' | 'done' | 'error';
  description?: string;    // 姝ラ鎻忚堪
  knowledge?: KnowledgeFlowData[];  // 鐭ヨ瘑璋冨彇鍒楄〃
  toolCall?: {
    icon: string;          // "Wrench"
    name: string;          // "get_worldview_summary"
  };
  revision?: RevisionFlowData;  // 鍐呭祵鐨勪慨璁㈣兌鍥婏紙v7.3锛?
  revisionItemId?: string;      // 鍏宠仈鐨?FlowItem ID锛堢敤浜庡洖璋冿級
}

/**
 * 鏈€缁堣緭鍑烘暟鎹?
 */
export interface OutputFlowData {
  intro?: string;          // "绗簲绔犲凡缁啓瀹屾垚锛佹湰绔犱富瑕佽杩?.."
  introHighlight?: string; // "鏋楅€稿紑濮嬪闂ㄤ慨鐐? (鍔犵矖閮ㄥ垎)
  title: string;           // "绗簲绔狅細澶栭棬鍒濅慨"
  content: string;         // 绔犺妭鍐呭 (鏀寔Markdown)
  isApplicable?: boolean;  // 鏄惁鍙簲鐢ㄥ埌缂栬緫鍣紙鏄剧ず"搴旂敤鍒扮珷鑺?鎸夐挳锛?
}

/**
 * Agent澶撮儴鏁版嵁
 */
export interface AgentHeaderFlowData {
  name?: string;           // "鏂囨灑AI"
  badge?: string;          // 鍙€夋爣绛?
}

/**
 * 瀹屾垚鐘舵€佹暟鎹?
 */
export interface CompletionFlowData {
  text?: string;           // "浠诲姟宸插畬鎴?
}

/**
 * AI鏁村悎鍒嗘瀽鏁版嵁 (Summarization)
 */
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

/**
 * AI 璇存槑鏂囧瓧鏁版嵁
 */
export interface TextFlowData {
  content: string;
}

/**
 * 宸ュ叿鍗＄墖鏁版嵁
 */
export interface ToolFlowData {
  taskId: number;
  icon: string;           // Lucide 鍥炬爣鍚?
  title: string;          // 宸ュ叿鏍囬
  description: string;    // 宸ュ叿鎻忚堪
  status: 'running' | 'done' | 'error';
}

/**
 * 娴佸紡鍐呭鏁版嵁
 */

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

// ==================== 淇鍗＄墖绫诲瀷 (v7.0) ====================

/**
 * 淇绫诲瀷
 */
export type RevisionType = 'append' | 'replace' | 'insert' | 'create' | 'rename';

/**
 * 淇鐘舵€?
 */
export type RevisionStatus = 'pending' | 'accepted' | 'discarded';

/**
 * 鏀瑰啓鐗堟湰
 */
export interface RewriteVersion {
  style_name: string;
  reason: string;
  content: string;
}

/**
 * 淇鍗＄墖鏁版嵁
 */
export interface RevisionFlowData {
  revisionType: RevisionType;
  status: RevisionStatus;
  statusUpdatedAt?: string;    // 鐘舵€佹洿鏂版椂闂达紙鐢ㄤ簬鈥滃凡鎾ら攢璁板綍鈥濊拷婧級
  requestId?: string;
  chapterId?: string;
  chapterTitle?: string;
  contentPreview?: string;      // 鍐呭棰勮锛堝墠50瀛楋級
  oldTitle?: string;            // 鍘熸爣棰橈紙rename 绫诲瀷锛?
  newTitle?: string;            // 鏂版爣棰橈紙rename 绫诲瀷锛?
  versions?: RewriteVersion[];  // 鏀瑰啓鐗堟湰锛坮eplace 绫诲瀷锛?
  // v7.2: 鎾ら攢/閲嶅仛鏀寔
  originalContent?: string;     // 鍘熷鍐呭蹇収锛堢敤浜庢挙閿€锛?
  newContent?: string;          // 鏂板唴瀹瑰揩鐓э紙鐢ㄤ簬閲嶅仛锛?
  editorPosition?: { from: number; to: number };  // 缂栬緫鍣ㄤ綅缃?
  selectedVersion?: number;     // 閫夋嫨鐨勬敼鍐欑増鏈储寮?
}

// ==================== Explore 鎺㈢储杞ㄨ抗绫诲瀷 (v9.0) ====================

/**
 * Explore 宸ュ叿璋冪敤鏍囩
 */
export interface ExploreToolCall {
  type: 'Search' | 'Locate' | 'ReadRaw' | 'ReadParagraph' | 'ListChapters' | 'ListParagraphs' | 'Worldview';
  value: string;
  highlight?: string;  // Search 绫诲瀷鐨勯珮浜叧閿瘝
}

/**
 * Explore 璇佹嵁椤?
 */
export interface ExploreEvidenceItem {
  chapter?: number;
  paragraph?: number;
  text: string;
  chapterOrder?: number;
  chapterTitle?: string;
  paragraphIndex?: number;
}

/**
 * Explore 杞鏁版嵁锛堟祦浜嬩欢锛?
 */
export interface ExploreRoundFlowData {
  stepId: number;
  roundIdx: number;
  title: string;
  reason?: string;  // AI 鐢熸垚鐨勫喅绛栫悊鐢憋紙瀹屾暣锛?
  toolCalls: ExploreToolCall[];
  hitCount: number;
  missingItems: string[];
  statusText: string;
  evidences: ExploreEvidenceItem[];
  reviewStatus: string;  // "瑕嗙洊涓嶈冻" | "琛ラ綈瑕佺偣" | "閫氳繃"
  status: 'running' | 'done';
}

/**
 * Explore 缁熻鏁版嵁
 */
export interface ExploreStats {
  worldview: number;
  chapters: string;    // "1-4"
  evidences: number;
  coverage: string;    // "鍏呰冻/瑕嗙洊涓嶈冻/鏈煡"
}

/**
 * Explore 鎬荤粨鏁版嵁锛堟祦浜嬩欢锛?
 */
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

/**
 * ExploreCard 缁勪欢浣跨敤鐨勮疆娆℃暟鎹紙鍏煎鏃х増锛?
 */
export interface ExploreRound {
  id: string;
  title?: string;
  reason?: string;  // AI 鐢熸垚鐨勫喅绛栫悊鐢憋紙瀹屾暣锛?
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

/**
 * ExploreCard 缁勪欢浣跨敤鐨勬暟鎹紙鍏煎鏃х増锛?
 */
export interface ExploreFlowData {
  rounds: ExploreRound[];
}

// ==================== Operate 鎿嶄綔杞ㄨ抗绫诲瀷 (v10.0) ====================

/**
 * Operate 鎿嶄綔绫诲瀷
 */
export type OperateOperationType = 'append' | 'replace' | 'insert' | 'content' | 'create' | 'title';

/**
 * Operate 瀹氫綅鏂瑰紡
 */
export type OperateLocateMethod = 'direct' | 'text_match' | 'semantic' | 'none' | 'fallback' | 'failed';

/**
 * Operate 闃舵鐘舵€?
 */
export type OperatePhaseStatus = 'pending' | 'running' | 'done' | 'skipped';

/**
 * Operate 鏍囩
 */
export interface OperateTag {
  label: string;      // 鏍囩鍚嶏細杈撳叆銆佸伐鍏枫€佹柟寮忋€佷綅缃€佹搷浣溿€佺姸鎬?
  value: string;      // 鏄剧ず鍊硷紙宸茶浆鎹负鐢ㄦ埛鍙嬪ソ鍚嶇О锛?
  icon?: string;      // Lucide 鍥炬爣鍚?
  variant?: 'default' | 'success' | 'warning' | 'info';
}

/**
 * Operate 闃舵鏁版嵁
 */
export interface OperatePhaseData {
  phase: 1 | 2 | 3;
  title: string;
  status: OperatePhaseStatus;
  tags: OperateTag[];
}

/**
 * Operate 杞ㄨ抗鏁版嵁锛堟祦浜嬩欢锛?
 */
export interface OperateFlowData {
  stepId: number;
  operation: OperateOperationType;     // 鍘熷鎿嶄綔绫诲瀷
  phases: OperatePhaseData[];          // 涓夐樁娈垫暟鎹?
  status: 'running' | 'done' | 'error';
  // 瀹氫綅缁撴灉锛堥樁娈?锛?
  locateMethod?: OperateLocateMethod;  // direct | text_match | semantic | none | fallback
  locateTarget?: string;               // "绗簲绔?路 绗?娈?
  // 鎵ц缁撴灉锛堥樁娈?锛?
  targetOperation?: string;            // 瀹為檯鎵ц鐨勬搷浣滐紙濡?content 鈫?replace_all锛?
  toolUsed?: string;                   // 浣跨敤鐨勫伐鍏?
  chapterId?: string;
  chapterTitle?: string;
  requiresConfirmation?: boolean;
  revisionId?: string;
  requestId?: string;
}

/**
 * 鎵ц杞ㄨ抗椤?
 */
export interface FlowItem {
  id: string;
  type: FlowItemType;
  data: TextFlowData | ToolFlowData | ContentFlowData | StepFlowData | OutputFlowData | AgentHeaderFlowData | CompletionFlowData | SummarizationFlowData | RevisionFlowData | ExploreRoundFlowData | ExploreSummaryFlowData | ExploreFlowData | OperateFlowData;
  timestamp: string;
}

/**
 * 澧炲己鐗堜换鍔″紑濮嬩簨浠讹紙鍚庣 v5.0 鍙戦€侊級
 */
export interface EnhancedTaskStartEvent {
  task_id: number;
  description: string;
  tool?: string;
  params?: Record<string, any>;
  // v5.0 澧炲己瀛楁
  explanation?: string;      // AI 璇存槑鏂囧瓧
  icon?: string;             // Lucide 鍥炬爣鍚?
  tool_title?: string;       // 宸ュ叿鏍囬
  tool_description?: string; // 宸ュ叿鎻忚堪
}

// ==================== 闈為樆濉炲紡淇 (v7.5) ====================

/**
 * 寰呭鐞嗕慨璁?
 */
export interface PendingRevision {
  id: string;                    // 鍓嶇鐢熸垚鐨勫敮涓€ID
  requestId: string;             // 鍚庣鐨剅equest_id
  chapterId: string;
  chapterTitle: string;
  revisionType: RevisionType;
  content: string;               // 瀹屾暣鍐呭
  originalContent?: string;      // 鍘熷唴瀹癸紙replace绫诲瀷闇€瑕侊級
  contentPreview: string;        // 鍐呭棰勮锛堝墠50瀛楋級
  position?: { from: number; to: number };
  operation?: string;            // 鎿嶄綔绫诲瀷
  editorAction?: EditorAction;   // 缂栬緫鍣ㄦ搷浣滀俊鎭?
  status: 'pending' | 'accepted' | 'rejected';
  createdAt: number;
  messageId?: string;            // 鍏宠仈鐨勬秷鎭疘D
  flowItemId?: string;           // 鍏宠仈鐨凢lowItem ID
}

/**
 * 淇浼氳瘽
 */
export interface RevisionSession {
  sessionId: string;             // 瀵瑰簲涓€娆gent鎵ц
  conversationId: string;        // 瀵硅瘽ID
  revisions: PendingRevision[];  // 淇鍒楄〃
  status: 'in_progress' | 'completed';
  pendingCount: number;          // 寰呯‘璁ゆ暟閲?
  acceptedCount: number;         // 宸查噰绾虫暟閲?
  rejectedCount: number;         // 宸插純鐢ㄦ暟閲?
  startTime: number;
  endTime?: number;
}



