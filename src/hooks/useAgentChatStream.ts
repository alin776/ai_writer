/**
 * Agent Chat Stream Hook
 *
 * 提供Planning流式对话功能，支持实时进度显示
 */

import { useState, useCallback, useRef } from 'react';
import { agentApi } from '@/services/agentApi';
import type { AgentChatRequest, EnhancedProgressEvent, ProgressData, ActivityItem, AgentActivityType, ActivityStatus, FlowItem, StepFlowData, SummarizationFlowData } from '@/types/agent';
import { ProgressDataSchema, EnhancedProgressEventSchema } from '@/types/agent';  // ✅ 导入Zod Schema

// 进度详情类型
export interface ProgressDetails {
  intent?: string;
  tools?: string[];
  [key: string]: any;  // 允许扩展
}

// 进度事件类型（保留用于向后兼容）
export interface ProgressEvent {
  type: 'progress';
  step: 'intent_analysis' | 'thinking' | 'tool_execution';
  description: string;
  node?: string;
  details?: ProgressDetails;
  timestamp: string;
  // ✅ 新增：ProgressTracker字段（可选）
  progress?: number;
  eta?: number | null;
  eta_display?: string;
  eta_confidence?: 'low' | 'medium' | 'high';
  current_step?: number;
  total_steps?: number;
  step_description?: string;
  elapsed?: number;
}

// 工具调用事件类型
export interface ToolCallEvent {
  tool: string;
  args: any;
  timestamp: string;
}

// Hook返回类型
export interface UseAgentChatStreamReturn {
  // 状态
  loading: boolean;
  error: Error | null;
  conversationId: string | null;

  // 实时进度
  currentProgress: ProgressEvent | null;
  progressHistory: ProgressEvent[];
  toolCalls: ToolCallEvent[];

  // ✅ 新增：进度数据（from ProgressTracker）
  progressData: ProgressData | null;

  // ✅ 新增：活动流
  activities: ActivityItem[];

  // ✅ 新增：执行轨迹 (v6.0)
  flowItems: FlowItem[];

  // 内容
  content: string;

  // 结果
  result: any | null;

  // 方法
  sendMessage: (message: string, options?: Partial<AgentChatRequest>) => Promise<void>;
  clearError: () => void;
  reset: () => void;
}

// Hook配置
export interface UseAgentChatStreamOptions {
  onProgress?: (progress: ProgressEvent) => void;
  onToolCall?: (toolCall: ToolCallEvent) => void;
  onContent?: (content: string) => void;
  onComplete?: (result: any) => void;
  onError?: (error: Error) => void;
  onFlowEvent?: (event: any) => void;  // 执行轨迹事件 (v6.0)
}

/**
 * useAgentChatStream Hook
 *
 * 使用Planning模式的流式Agent对话
 */
export function useAgentChatStream(
  options?: UseAgentChatStreamOptions
): UseAgentChatStreamReturn {
  // 状态
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);

  // 进度状态
  const [currentProgress, setCurrentProgress] = useState<ProgressEvent | null>(null);
  const [progressHistory, setProgressHistory] = useState<ProgressEvent[]>([]);
  const [toolCalls, setToolCalls] = useState<ToolCallEvent[]>([]);

  // ✅ 新增：进度数据状态
  const [progressData, setProgressData] = useState<ProgressData | null>(null);

  // ✅ 新增：活动流状态
  const [activities, setActivities] = useState<ActivityItem[]>([]);

  // ✅ 新增：执行轨迹状态 (v6.0)
  const [flowItems, setFlowItems] = useState<FlowItem[]>([]);
  const stepDataRef = useRef<Map<number, StepFlowData>>(new Map());  // 步骤数据缓存

  // 内容和结果
  const [content, setContent] = useState('');
  const [result, setResult] = useState<any | null>(null);

  // 用于取消请求（如果需要）
  const abortControllerRef = useRef<AbortController | null>(null);

  /**
   * ✅ 新增：将ProgressEvent转换为ActivityItem
   *
   * 使用全局计数器确保ID唯一性
   */
  let activityIdCounter = 0;  // 全局计数器

  const progressEventToActivity = useCallback((event: ProgressEvent): ActivityItem => {
    // 将step映射到AgentActivityType
    const stepToTypeMap: Record<string, AgentActivityType> = {
      'intent_analysis': 'intent_analysis',
      'thinking': 'thinking',
      'tool_execution': 'tool_execution',
      'generating': 'generating',  // ✅ 新增：补充generating类型（P1任务15）
    };

    const activityType = stepToTypeMap[event.step] || 'thinking';

    // 根据进度判断状态
    let status: ActivityStatus = 'active';
    if (event.progress !== undefined) {
      if (event.progress >= 100) {
        status = 'completed';
      }
    }

    // ✅ 改进：使用全局计数器 + 时间戳 + 随机字符串确保唯一性
    const uniqueId = `activity-${++activityIdCounter}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    return {
      id: uniqueId,
      type: activityType,
      description: event.description,
      timestamp: event.timestamp,
      status,
      node: event.node,
      details: event.details,
      elapsedTime: event.elapsed,
    };
  }, []);

  /**
   * 清除错误
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  /**
   * 重置所有状态
   */
  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
    setConversationId(null);
    setCurrentProgress(null);
    setProgressHistory([]);
    setToolCalls([]);
    setProgressData(null);  // ✅ 重置progressData
    setActivities([]);  // ✅ 重置activities
    setFlowItems([]);  // ✅ 重置flowItems
    stepDataRef.current.clear();  // ✅ 重置步骤缓存
    setContent('');
    setResult(null);
  }, []);

  /**
   * 发送消息
   */
  const sendMessage = useCallback(
    async (message: string, requestOptions?: Partial<AgentChatRequest>) => {
      setLoading(true);
      setError(null);
      setCurrentProgress(null);
      setProgressHistory([]);
      setToolCalls([]);
      setProgressData(null);  // ✅ 重置progressData
      setActivities([]);  // ✅ 重置activities
      setFlowItems([]);  // ✅ 重置flowItems
      stepDataRef.current.clear();  // ✅ 重置步骤缓存
      setContent('');
      setResult(null);

      try {
        // 准备请求
        const request: AgentChatRequest = {
          message,
          mode: 'planning',  // 使用 Planning 模式
          conversation_id: conversationId || undefined,
          ...requestOptions,
        };

        // 调用API（使用统一的 chatStream，通过 mode 参数区分）
        await agentApi.chatStream(request, {
          onStart: (convId) => {
            setConversationId(convId);
          },

          onProgress: (progress) => {
            const progressEvent: ProgressEvent = {
              type: 'progress',
              step: progress.step,
              description: progress.description,
              node: progress.node,
              details: progress.details,
              timestamp: progress.timestamp,
              // ✅ 新增：提取ProgressTracker字段
              progress: progress.progress,
              eta: progress.eta,
              eta_display: progress.eta_display,
              eta_confidence: progress.eta_confidence,
              current_step: progress.current_step,
              total_steps: progress.total_steps,
              step_description: progress.step_description,
              elapsed: progress.elapsed,
            };

            setCurrentProgress(progressEvent);

            // ✅ 新增：提取并存储ProgressData（使用Zod验证）
            if (progress.progress !== undefined) {
              const newProgressData: ProgressData = {
                progress: progress.progress,
                eta: progress.eta ?? null,
                eta_display: progress.eta_display ?? '计算中...',
                eta_confidence: progress.eta_confidence ?? 'low',
                current_step: progress.current_step ?? 1,
                total_steps: progress.total_steps ?? 1,
                step_description: progress.step_description ?? '',
                elapsed: progress.elapsed ?? 0,
                current_node: progress.node,
                current_node_display: progress.current_node_display,
                current_node_description: progress.current_node_description,
              };

              // ✅ 使用Zod验证数据（safeParse不会抛异常）
              const validationResult = ProgressDataSchema.safeParse(newProgressData);
              if (validationResult.success) {
                setProgressData(validationResult.data);
              } else {
                if (process.env.NODE_ENV === 'development') {
                  console.error('[useAgentChatStream] ProgressData验证失败:', validationResult.error);
                }
                // 降级：仍然设置数据，但记录警告
                setProgressData(newProgressData);
              }
            }

            // ✅ 新增：更新活动流（追加模式）
            const newActivity = progressEventToActivity(progressEvent);
            setActivities((prev) => {
              // 直接追加，不去重
              const newList = [...prev, newActivity];

              // 限制最多保留50条（防止无限增长）
              if (newList.length > 50) {
                return newList.slice(-50);
              }

              return newList;
            });

            // 限制进度历史最多保留100条，避免内存占用过大
            setProgressHistory((prev) => {
              const newHistory = [...prev, progressEvent];
              return newHistory.length > 100 ? newHistory.slice(-100) : newHistory;
            });

            // 触发外部回调
            options?.onProgress?.(progressEvent);
          },

          onToolCall: (toolCall) => {
            const toolCallEvent: ToolCallEvent = {
              tool: toolCall.tool,
              args: toolCall.args,
              timestamp: toolCall.timestamp,
            };

            setToolCalls((prev) => [...prev, toolCallEvent]);

            // 触发外部回调
            options?.onToolCall?.(toolCallEvent);
          },

          onContent: (chunk) => {
            setContent((prev) => prev + chunk);

            // 触发外部回调
            options?.onContent?.(chunk);
          },

          onDone: (data) => {
            setResult(data);
            setCurrentProgress(null);
            setProgressData(null);  // ✅ 完成时清空progressData

            // ✅ 新增：只将active状态的activities标记为completed
            setActivities((prev) =>
              prev.map(a =>
                a.status === 'active'
                  ? { ...a, status: 'completed' as ActivityStatus }
                  : a  // 保持completed和failed状态不变
              )
            );

            // 触发外部回调
            options?.onComplete?.(data);
          },

          onError: (errorMsg) => {
            const err = new Error(errorMsg);
            setError(err);

            // 触发外部回调
            options?.onError?.(err);
          },

          // ✅ 新增：执行轨迹事件处理 (v6.0)
          onFlowEvent: (event) => {
            const timestamp = event.timestamp || new Date().toISOString();

            switch (event.type) {
              case 'agent_header': {
                const item: FlowItem = {
                  id: `flow-${Date.now()}-header`,
                  type: 'agent_header',
                  data: { name: event.data?.name, badge: event.data?.badge },
                  timestamp,
                };
                setFlowItems((prev) => [...prev, item]);
                break;
              }
              case 'text': {
                const item: FlowItem = {
                  id: `flow-${Date.now()}-text`,
                  type: 'text',
                  data: { content: event.data?.content || '' },
                  timestamp,
                };
                setFlowItems((prev) => [...prev, item]);
                break;
              }
              case 'step_start': {
                const stepData: StepFlowData = {
                  stepId: event.stepId,
                  title: event.title,
                  status: 'running',
                };
                stepDataRef.current.set(event.stepId, stepData);
                const item: FlowItem = {
                  id: `flow-${Date.now()}-step-${event.stepId}`,
                  type: 'step',
                  data: stepData,
                  timestamp,
                };
                setFlowItems((prev) => [...prev, item]);
                break;
              }
              case 'knowledge_loaded': {
                const stepData = stepDataRef.current.get(event.stepId);
                if (stepData) {
                  const knowledge = { title: event.title, icon: event.icon, items: event.items || [] };
                  stepData.knowledge = [...(stepData.knowledge || []), knowledge];
                  setFlowItems((prev) =>
                    prev.map((item) =>
                      item.type === 'step' && (item.data as StepFlowData).stepId === event.stepId
                        ? { ...item, data: { ...stepData } }
                        : item
                    )
                  );
                }
                break;
              }
              case 'step_complete': {
                const stepData = stepDataRef.current.get(event.stepId);
                if (stepData) {
                  stepData.status = 'done';
                  stepData.description = event.description;
                  stepData.toolCall = event.toolCall;
                  setFlowItems((prev) =>
                    prev.map((item) =>
                      item.type === 'step' && (item.data as StepFlowData).stepId === event.stepId
                        ? { ...item, data: { ...stepData } }
                        : item
                    )
                  );
                }
                break;
              }
              case 'output_ready': {
                const item: FlowItem = {
                  id: `flow-${Date.now()}-output`,
                  type: 'output',
                  data: {
                    title: event.title,
                    content: event.content,
                    intro: event.intro,
                    introHighlight: event.introHighlight,
                    isApplicable: event.is_applicable,
                  },
                  timestamp,
                };
                setFlowItems((prev) => [...prev, item]);
                break;
              }
              case 'completion': {
                const item: FlowItem = {
                  id: `flow-${Date.now()}-completion`,
                  type: 'completion',
                  data: { text: event.data?.text },
                  timestamp,
                };
                setFlowItems((prev) => [...prev, item]);
                break;
              }
              case 'summarization_start': {
                console.log('[useAgentChatStream] Processing summarization_start event:', event);
                const item: FlowItem = {
                  id: `flow-${Date.now()}-summarization`,
                  type: 'summarization',
                  data: {
                    status: 'running',
                    taskClassification: {
                      inputTasks: event.task_classification?.input_tasks || [],
                      outputTasks: event.task_classification?.output_tasks || [],
                      displayTasks: event.task_classification?.display_tasks || [],
                    },
                    contextStats: {
                      originalLength: event.context_stats?.original_length || 0,
                      compressedLength: event.context_stats?.compressed_length || 0,
                      mode: event.context_stats?.mode || '流式生成',
                    },
                  },
                  timestamp,
                };
                console.log('[useAgentChatStream] Created summarization FlowItem:', item);
                setFlowItems((prev) => [...prev, item]);
                break;
              }
              case 'summarization_complete': {
                setFlowItems((prev) =>
                  prev.map((item): FlowItem =>
                    item.type === 'summarization'
                      ? { ...item, data: { ...(item.data as SummarizationFlowData), status: 'done' } }
                      : item
                  )
                );
                break;
              }
              // Explore 探索事件 (2026-01-17)
              case 'explore_round': {
                const item: FlowItem = {
                  id: `flow-${Date.now()}-explore-round-${event.roundIdx}`,
                  type: 'explore_round',
                  data: {
                    stepId: event.stepId,
                    roundIdx: event.roundIdx,
                    title: event.title,
                    toolCalls: event.toolCalls,
                    hitCount: event.hitCount,
                    missingItems: event.missingItems,
                    statusText: event.statusText,
                    evidences: event.evidences,
                    reviewStatus: event.reviewStatus,
                    status: event.status,
                  },
                  timestamp,
                };
                setFlowItems((prev) => [...prev, item]);
                break;
              }
              case 'explore_summary': {
                const item: FlowItem = {
                  id: `flow-${Date.now()}-explore-summary`,
                  type: 'explore_summary',
                  data: {
                    stepId: event.stepId,
                    totalRounds: event.totalRounds,
                    summary: event.summary,
                    nextAction: event.nextAction,
                    nextTool: event.nextTool,
                    sufficient: event.sufficient,
                    coverage: event.coverage,
                    stats: event.stats,
                  },
                  timestamp,
                };
                setFlowItems((prev) => [...prev, item]);
                break;
              }
              case 'revision': {
                // v7.0: 修订请求事件
                const item: FlowItem = {
                  id: `flow-${Date.now()}-revision`,
                  type: 'revision',
                  data: event.data,
                  timestamp,
                };
                setFlowItems((prev) => [...prev, item]);
                break;
              }
            }

            // 触发外部回调
            options?.onFlowEvent?.(event);
          },
        });

      } catch (err) {
        const error = err instanceof Error ? err : new Error('Agent请求失败');
        setError(error);
        options?.onError?.(error);
      } finally {
        setLoading(false);
      }
    },
    [conversationId, options, progressEventToActivity]  // ✅ 添加progressEventToActivity依赖
  );

  return {
    // 状态
    loading,
    error,
    conversationId,

    // 进度
    currentProgress,
    progressHistory,
    toolCalls,
    progressData,  // ✅ 返回progressData
    activities,  // ✅ 返回activities
    flowItems,  // ✅ 返回flowItems (v6.0)

    // 内容
    content,

    // 结果
    result,

    // 方法
    sendMessage,
    clearError,
    reset,
  };
}
