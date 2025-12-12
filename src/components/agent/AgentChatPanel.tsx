import { useCallback, useEffect, useRef, useState } from 'react';
import { useAgentChat } from '@/hooks/useAgentChat';
import { useTabManager } from '@/hooks/useTabManager';
import SessionTabs from './SessionTabs';
import AgentMessage from './AgentMessage';
import ChatInput from './ChatInput';
import SuggestedActions from './SuggestedActions';
import ThinkingIndicator from './ThinkingIndicator';
import TaskListPanel from './TaskListPanel';
import ActivityStream from './ActivityStream';
import { type AgentMode } from './ModeSelector';
import type { AgentChatRequest } from '@/types/agent';

import type { Tab } from '@/utils/tabStorage';

interface AgentChatPanelProps {
  workId?: string;
  chapterId?: string;
  initialMessage?: string;
  className?: string;
  tabs?: Tab[];
  activeTabId?: string;
  onCreateTab?: (afterTabId?: string) => Promise<Tab>;
  onCloseTab?: (tabId: string) => void;
  onSwitchTab?: (tabId: string) => void;
  onUpdateTabTitle?: (tabId: string, title: string) => void;
}

export default function AgentChatPanel({
  workId,
  chapterId,
  initialMessage,
  className = '',
  tabs: controlledTabs,
  activeTabId: controlledActiveTabId,
  onCreateTab,
  onCloseTab,
  onSwitchTab,
  onUpdateTabTitle
}: AgentChatPanelProps) {
  const [selectionContext, setSelectionContext] = useState<{
    selected_text?: string;
    selected_text_html?: string;
    selection_position?: { from: number; to: number };
  } | null>(null);

  useEffect(() => {
    console.log('[AgentChatPanel] mounted', { workId, chapterId, className });
  }, [workId, chapterId, className]);
  const {
    tabs,
    activeTabId,
    createTab,
    closeTab,
    switchTab,
    updateTabTitle
  } = useTabManager(chapterId || 'default', workId);

  const tabsToUse = controlledTabs ?? tabs;
  const activeTabIdToUse = controlledActiveTabId ?? activeTabId;
  const renderInternalTabs = !controlledTabs;

  // 全局：消费 InlineAI intent 队列并监听 intent 事件（与 tab 活动状态无关）
  useEffect(() => {
    const intentQueue: any[] = (window as any).__inlineAIIntentQueue__ || [];
    if (intentQueue.length > 0) {
      const last = intentQueue[intentQueue.length - 1];
      console.log('[AgentChatPanel] intentQueue consumed (global):', last);
      setSelectionContext(last || null);
      (window as any).__inlineAIIntentQueue__ = [];
    }

    (window as any).__agentInlineIntent__ = (ctx?: {
      selected_text?: string;
      selected_text_html?: string;
      selection_position?: { from: number; to: number };
    }) => {
      setSelectionContext(ctx || null);
    };

    const handleInlineAIIntent = (event: CustomEvent<{
      selected_text?: string;
      selected_text_html?: string;
      selection_position?: { from: number; to: number };
    }>) => {
      console.log('[AgentChatPanel] 收到 InlineAI intent (global):', event.detail);
      setSelectionContext(event.detail || null);
    };

    window.addEventListener('inline-ai-intent', handleInlineAIIntent as EventListener);
    return () => {
      window.removeEventListener('inline-ai-intent', handleInlineAIIntent as EventListener);
      delete (window as any).__agentInlineIntent__;
    };
  }, []);

  // 兜底：若 selectionContext 为空且队列中有新意图，取最新一条
  useEffect(() => {
    if (selectionContext) return;
    const q: any[] = (window as any).__inlineAIIntentQueue__ || [];
    if (q.length > 0) {
      const last = q[q.length - 1];
      console.log('[AgentChatPanel] fallback intentQueue hit:', last);
      setSelectionContext(last || null);
      (window as any).__inlineAIIntentQueue__ = [];
    }
  }, [selectionContext]);

  // Debug: track selectionContext changes
  useEffect(() => {
    if (selectionContext) {
      console.log('[AgentChatPanel] selectionContext ->', selectionContext);
    } else {
      console.log('[AgentChatPanel] selectionContext cleared');
    }
  }, [selectionContext]);

  // Create a new tab to the right of the current active tab.
  const handleCreateTab = async (): Promise<string> => {
    const create = onCreateTab ?? createTab;
    const baseId = activeTabIdToUse;
    const newTab = await create(baseId);
    return newTab.id;
  };

  return (
    <div className={`agent-chat-panel flex flex-col h-full bg-white rounded-lg shadow-lg ${className}`}>
      {renderInternalTabs && (
        <SessionTabs
          sessions={tabsToUse.map((tab) => ({
            id: tab.id,
            title: tab.title,
            updatedAt: tab.updatedAt,
            messages: [],
            conversationId: tab.conversationId || ''
          }))}
          activeSessionId={activeTabIdToUse}
          onSwitchSession={onSwitchTab ?? switchTab}
          onCreateSession={handleCreateTab}
          onCloseSession={onCloseTab ?? closeTab}
          onOpenHistory={() => {}}
          onShowToast={(type, message) => console.log(`[Toast/${type}]`, message)}
        />
      )}

      {tabsToUse.map((tab) => (
        <div
          key={tab.id}
          style={{
            display: tab.id === activeTabIdToUse ? 'flex' : 'none',
            flexDirection: 'column',
            flex: 1
          }}
        >
          <TabContent
            workId={workId}
            chapterId={chapterId}
            sessionId={tab.sessionId}
            initialMessage={initialMessage}
            onTitleChange={(title) => (onUpdateTabTitle ?? updateTabTitle)(tab.id, title)}
            isActive={tab.id === activeTabIdToUse}
            selectionContext={selectionContext}
            onClearSelection={() => setSelectionContext(null)}
          />
        </div>
      ))}
    </div>
  );
}

interface TabContentProps {
  workId?: string;
  chapterId?: string;
  sessionId: string;
  initialMessage?: string;
  onTitleChange?: (title: string) => void;
  /** 是否为当前活动标签页（只有活动标签才处理 InlineAI 事件） */
  isActive?: boolean;
  selectionContext?: {
    selected_text?: string;
    selected_text_html?: string;
    selection_position?: { from: number; to: number };
  } | null;
  onClearSelection?: () => void;
}

function TabContent({
  workId,
  chapterId,
  sessionId,
  initialMessage,
  onTitleChange,
  isActive = true,
  selectionContext,
  onClearSelection,
}: TabContentProps) {
  const {
    messages,
    sendMessageStream,
    isLoading,
    suggestedActions,
    tasks,
    currentTaskId,
    activities,
    progressData,
    clearMessages,
    stopStreaming
  } = useAgentChat({ workId, chapterId, sessionId });

  const [mode, setMode] = useState<AgentMode>('plan');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  // 🆕 提前定义 handleSendMessage，确保所有 useEffect 都能使用
  const handleSendMessage = useCallback(async (message: string, context?: any) => {
    // 🔍 调试日志：追踪 context 发送
    console.log('===== AgentChatPanel handleSendMessage =====');
    console.log('1. message:', message);
    console.log('2. context 完整内容:', context);
    console.log('3. context.selected_text:', context?.selected_text);
    console.log('4. context.selection_position:', context?.selection_position);
    console.log('=============================================');

    // Agent 模式 = Planning + DeepAgent 反思（可动态调整任务）
    const enableDeepAgent = mode === 'agent';

    const backendMode: AgentChatRequest['mode'] = enableDeepAgent ? 'react' : 'planning';
    const request: AgentChatRequest = {
      message,
      mode: backendMode,
      work_id: workId,
      chapter_id: chapterId,
      context,
      enable_reflection: enableDeepAgent,
    };

    console.log('[AgentChatPanel] 📤 发送请求:', JSON.stringify(request, null, 2));

    await sendMessageStream(request);
  }, [mode, workId, chapterId, sendMessageStream]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (initialMessage && messages.length === 0) {
      handleSendMessage(initialMessage);
    }
  }, [initialMessage, messages.length, handleSendMessage]);

  // 全局去重集合，确保跨组件只处理一次 inline-ai 消息
  const getInlineAIProcessedSet = useCallback((): Set<string> => {
    if (typeof window === 'undefined') return new Set<string>();
    if (!(window as any).__inlineAIProcessed__) {
      (window as any).__inlineAIProcessed__ = new Set<string>();
    }
    return (window as any).__inlineAIProcessed__ as Set<string>;
  }, []);

  // 🆕 合并：队列消费 + 全局回调 + 事件监听（共享去重 Set）（只有活动标签页才处理）
  useEffect(() => {
    // 非活动标签页不设置监听器
    if (!isActive) {
      console.log('[AgentChatPanel] TabContent 非活动，跳过 InlineAI 监听设置, sessionId:', sessionId);
      return;
    }

    console.log('[AgentChatPanel] TabContent mounted (活动标签页), sessionId:', sessionId);

    // 共享去重 Set（跨组件全局复用）
    const consumed = getInlineAIProcessedSet();

    // 1. 先消费队列中的遗留消息
    const queue: any[] = (window as any).__inlineAIQueueFlushed__ || (window as any).__inlineAIQueue__ || [];
    queue.forEach((item) => {
      const rid = item?.requestId || JSON.stringify(item);
      if (!consumed.has(rid)) {
        consumed.add(rid);
        console.log('[AgentChatPanel] consuming queued inline-ai payload', item);

        const ctx = item.context || item.ctx || {};
        const enrichedContext = {
          ...ctx,
          chapter_context: ctx.selected_text
            ? `【选中的文字】\n${ctx.selected_text}\n\n【用户指令】\n${item.message || item.msg}`
            : undefined,
        };
        handleSendMessage(item.message || item.msg || '', enrichedContext);
      }
    });
    (window as any).__inlineAIQueueFlushed__ = [];
    (window as any).__inlineAIQueue__ = [];

    // 2. 暴露全局回调
    (window as any).__agentInlineSend__ = (msg: string, ctx?: any, requestId?: string) => {
      const rid = requestId || `inline-${Date.now()}-${Math.random().toString(16).slice(2)}`;
      if (consumed.has(rid)) {
        console.log('[AgentChatPanel] __agentInlineSend__ 消息已处理，跳过:', rid);
        return;
      }
      consumed.add(rid);
      console.log('[AgentChatPanel] __agentInlineSend__ invoked', { msg, ctx, rid });

      const enrichedContext = {
        ...ctx,
        chapter_context: ctx?.selected_text
          ? `【选中的文字】\n${ctx.selected_text}\n\n【用户指令】\n${msg}`
          : undefined,
      };
      handleSendMessage(msg, enrichedContext);
    };

    // 3. 监听 inline-ai-send 事件（共享去重 Set）
    const handleInlineAIMessage = (event: CustomEvent<{
      message: string;
      context: {
        selected_text?: string;
        selected_text_html?: string;
        selection_position?: { from: number; to: number };
        knowledge_doc_ids?: string[];
      };
      requestId?: string;
    }>) => {
      const { message, context, requestId } = event.detail;
      console.log('[AgentChatPanel] 收到 InlineAI 消息:', { message, context, requestId });

      // 去重检查
      const rid = requestId || `inline-${Date.now()}`;
      if (consumed.has(rid)) {
        console.log('[AgentChatPanel] 消息已处理，跳过:', rid);
        return;
      }
      consumed.add(rid);

      // 构建带选中文字上下文的请求
      const enrichedContext = {
        ...context,
        chapter_context: context.selected_text
          ? `【选中的文字】\n${context.selected_text}\n\n【用户指令】\n${message}`
          : undefined,
      };

      handleSendMessage(message, enrichedContext);
    };

    window.addEventListener('inline-ai-send', handleInlineAIMessage as EventListener);

    return () => {
      window.removeEventListener('inline-ai-send', handleInlineAIMessage as EventListener);
      delete (window as any).__agentInlineSend__;
      console.log('[AgentChatPanel] 卸载 InlineAI 事件监听');
    };
  }, [handleSendMessage, sessionId, isActive, getInlineAIProcessedSet]);

  // Update tab title using the first user message.
  useEffect(() => {
    if (messages.length > 0 && onTitleChange) {
      const firstUserMessage = messages.find((m) => m.role === 'user');
      if (firstUserMessage) {
        const content = firstUserMessage.content.trim();
        const title = content.length <= 30 ? content : `${content.substring(0, 30)}...`;
        onTitleChange(title);
      }
    }
  }, [messages, onTitleChange]);

  const handleClearChat = () => {
    if (confirm('Clear this conversation and start a new one?')) {
      clearMessages();
    }
  };

  return (
    <>
      <div className="chat-header px-4 py-3 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div>
              <h2 className="text-sm font-bold text-gray-800 flex items-center gap-2">AI 写作助手</h2>
              <p className="text-xs text-gray-600 mt-0.5">规划 · 写作辅助 · 文本分析 · 创意激发</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {messages.length > 0 && (
              <button
                onClick={handleClearChat}
                className="px-2 py-1 text-xs text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded transition-colors"
              >
                清空对话
              </button>
            )}
          </div>
        </div>
      </div>

      {tasks.length > 0 && (
        <div className="px-4 py-2 border-b border-gray-200 bg-gray-50">
          <TaskListPanel tasks={tasks} currentTaskId={currentTaskId} />
        </div>
      )}

      <div className="messages flex-1 overflow-y-auto px-4 py-3 space-y-4">
        {messages.length === 0 && (
          <div className="empty-state text-center py-8">
            <div className="text-4xl mb-3">💡</div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">你好，我是你的 AI 写作助手</h3>
            <p className="text-xs text-gray-500 mb-4">我可以帮你完成下面的任务：</p>
            <div className="grid grid-cols-2 gap-3 max-w-2xl mx-auto text-left">
              <div className="p-3 bg-blue-50 rounded-lg">
                <div className="text-lg mb-1">✍️</div>
                <div className="text-xs font-semibold text-gray-700">创作辅助</div>
                <div className="text-xs text-gray-600">续写章节、扩写内容</div>
              </div>
              <div className="p-3 bg-purple-50 rounded-lg">
                <div className="text-lg mb-1">📓</div>
                <div className="text-xs font-semibold text-gray-700">规划设计</div>
                <div className="text-xs text-gray-600">世界观、大纲、人物</div>
              </div>
              <div className="p-3 bg-green-50 rounded-lg">
                <div className="text-lg mb-1">🔍</div>
                <div className="text-xs font-semibold text-gray-700">文本分析</div>
                <div className="text-xs text-gray-600">诊断问题、改进建议</div>
              </div>
              <div className="p-3 bg-orange-50 rounded-lg">
                <div className="text-lg mb-1">💡</div>
                <div className="text-xs font-semibold text-gray-700">创意激发</div>
                <div className="text-xs text-gray-600">卡文求助、方向建议</div>
              </div>
            </div>
          </div>
        )}

        {messages.map((msg, index) => (
          <AgentMessage key={index} message={msg} isLatest={index === messages.length - 1} />
        ))}

        {isLoading && <ThinkingIndicator />}

        <div ref={messagesEndRef} />
      </div>

      {suggestedActions.length > 0 && !isLoading && (
        <div className="px-4 py-2 border-t border-gray-100 bg-gray-50">
          <SuggestedActions actions={suggestedActions} onActionClick={handleSendMessage} />
        </div>
      )}

      <div className="px-4 py-3 border-t border-gray-200">
        <ChatInput
          onSend={handleSendMessage}
          disabled={isLoading}
          placeholder="试试：帮我写第三章..."
          mode={mode}
          onModeChange={setMode}
          isLoading={isLoading}
          onStop={stopStreaming}
          selectionContext={selectionContext || undefined}
          onClearSelection={onClearSelection}
        />
      </div>

      {messages.length === 0 && (
        <div className="px-4 pb-3 pt-1">
          <div className="text-xs text-gray-500 mb-1.5">快速开始：</div>
          <div className="flex flex-wrap gap-1.5">
            <button
              onClick={() => handleSendMessage('帮我写第三章')}
              className="px-2 py-1 text-xs bg-white border border-gray-300 rounded-full hover:bg-gray-50 transition-colors"
            >
              📖 帮我写第三章
            </button>
            <button
              onClick={() => handleSendMessage('我想写一部玄幻小说')}
              className="px-2 py-1 text-xs bg-white border border-gray-300 rounded-full hover:bg-gray-50 transition-colors"
            >
              🌟 规划玄幻小说
            </button>
            <button
              onClick={() => handleSendMessage('我卡文了')}
              className="px-2 py-1 text-xs bg-white border border-gray-300 rounded-full hover:bg-gray-50 transition-colors"
            >
              💭 我卡文了
            </button>
            <button
              onClick={() => handleSendMessage('分析这段文字哪里不好')}
              className="px-2 py-1 text-xs bg-white border border-gray-300 rounded-full hover:bg-gray-50 transition-colors"
            >
              🔍 文本分析
            </button>
          </div>
        </div>
      )}
    </>
  );
}
