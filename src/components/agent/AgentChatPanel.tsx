import { useEffect, useRef, useState } from 'react';
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
}

function TabContent({ workId, chapterId, sessionId, initialMessage, onTitleChange }: TabContentProps) {
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

  const [mode, setMode] = useState<AgentMode>('planning');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (initialMessage && messages.length === 0) {
      handleSendMessage(initialMessage);
    }
  }, [initialMessage, messages.length]);

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

  const handleSendMessage = async (message: string, context?: any) => {
    const request = {
      message,
      mode,
      work_id: workId,
      chapter_id: chapterId,
      context
    };

    await sendMessageStream(request);
  };

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

      {mode === 'react' && activities.length > 0 && (
        <div className="activity-stream-container px-4 py-2 border-b border-gray-200 bg-gray-50 transition-all duration-300">
          <ActivityStream activities={activities} progressData={progressData} />
        </div>
      )}

      {mode === 'planning' && tasks.length > 0 && (
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
