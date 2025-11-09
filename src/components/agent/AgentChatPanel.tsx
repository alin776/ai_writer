/**
 * Agent智能助手 - 主对话面板组件
 *
 * 功能特性:
 * - 支持4个核心场景 (写作/规划/分析/卡文)
 * - 显示Agent思考过程
 * - 建议操作按钮
 * - Markdown渲染
 * - 历史记录管理
 */

import React, { useState, useRef, useEffect } from 'react';
import { useAgentChat } from '@/hooks/useAgentChat';
import AgentMessage from './AgentMessage';
import ChatInput from './ChatInput';
import SuggestedActions from './SuggestedActions';
import ThinkingIndicator from './ThinkingIndicator';
import TaskListPanel from './TaskListPanel';
import ModeSelector, { type AgentMode } from './ModeSelector';

interface AgentChatPanelProps {
  workId?: string;
  chapterId?: string;
  initialMessage?: string;
  className?: string;
}

export default function AgentChatPanel({
  workId,
  chapterId,
  initialMessage,
  className = ''
}: AgentChatPanelProps) {
  const {
    messages,
    sendMessage,
    sendMessageStream,
    isLoading,
    suggestedActions,
    tasks,
    currentTaskId,
    clearMessages
  } = useAgentChat();

  const [conversationId, setConversationId] = useState<string | null>(null);
  const [mode, setMode] = useState<AgentMode>('planning'); // Agent执行模式：planning(默认) 或 react
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 始终使用流式响应
  const useStreaming = true;

  // 自动滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // 发送初始消息
  useEffect(() => {
    if (initialMessage && messages.length === 0) {
      handleSendMessage(initialMessage);
    }
  }, [initialMessage]);

  const handleSendMessage = async (message: string, context?: any) => {
    const request = {
      message,
      mode,  // 传递当前选择的执行模式
      work_id: workId,
      chapter_id: chapterId,
      conversation_id: conversationId || undefined,  // 将 null 转换为 undefined
      context
    };

    if (useStreaming) {
      // 使用流式响应
      await sendMessageStream(request);
    } else {
      // 使用普通响应
      const response = await sendMessage(request);
      if (response?.conversation_id) {
        setConversationId(response.conversation_id);
      }
    }
  };

  const handleClearChat = () => {
    if (confirm('确定要清空对话历史吗？')) {
      clearMessages();
      setConversationId(null);
    }
  };

  return (
    <div className={`agent-chat-panel flex flex-col h-full bg-white rounded-lg shadow-lg ${className}`}>
      {/* 头部 */}
      <div className="chat-header px-4 py-3 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div>
              <h2 className="text-sm font-bold text-gray-800 flex items-center gap-2">
                <span className="text-base">🤖</span>
                AI写作助手
              </h2>
              <p className="text-xs text-gray-600 mt-0.5">
                智能规划 · 写作辅助 · 文本分析 · 创意激发
              </p>
            </div>

            {/* 模式选择器 */}
            <div className="ml-2">
              <ModeSelector
                mode={mode}
                onModeChange={setMode}
                disabled={isLoading}
              />
            </div>
          </div>

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

      {/* 消息列表 */}
      <div className="messages flex-1 overflow-y-auto px-4 py-3 space-y-4">
        {/* 任务清单面板 */}
        {tasks.length > 0 && (
          <TaskListPanel tasks={tasks} currentTaskId={currentTaskId} />
        )}

        {messages.length === 0 && (
          <div className="empty-state text-center py-8">
            <div className="text-4xl mb-3">💡</div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">
              你好！我是你的AI写作助手
            </h3>
            <p className="text-xs text-gray-500 mb-4">
              我可以帮你完成以下任务：
            </p>
            <div className="grid grid-cols-2 gap-3 max-w-2xl mx-auto text-left">
              <div className="p-3 bg-blue-50 rounded-lg">
                <div className="text-lg mb-1">✍️</div>
                <div className="text-xs font-semibold text-gray-700">创作辅助</div>
                <div className="text-xs text-gray-600">续写章节、扩写内容</div>
              </div>
              <div className="p-3 bg-purple-50 rounded-lg">
                <div className="text-lg mb-1">📋</div>
                <div className="text-xs font-semibold text-gray-700">规划设计</div>
                <div className="text-xs text-gray-600">世界观、大纲、人物</div>
              </div>
              <div className="p-3 bg-green-50 rounded-lg">
                <div className="text-lg mb-1">🔍</div>
                <div className="text-xs font-semibold text-gray-700">文本分析</div>
                <div className="text-xs text-gray-600">诊断问题、改进建议</div>
              </div>
              <div className="p-3 bg-orange-50 rounded-lg">
                <div className="text-lg mb-1">💫</div>
                <div className="text-xs font-semibold text-gray-700">创意激发</div>
                <div className="text-xs text-gray-600">卡文求助、方向建议</div>
              </div>
            </div>
          </div>
        )}

        {messages.map((msg, index) => (
          <AgentMessage
            key={index}
            message={msg}
            isLatest={index === messages.length - 1}
          />
        ))}

        {isLoading && <ThinkingIndicator />}

        <div ref={messagesEndRef} />
      </div>

      {/* 建议操作 */}
      {suggestedActions.length > 0 && !isLoading && (
        <div className="px-4 py-2 border-t border-gray-100 bg-gray-50">
          <SuggestedActions
            actions={suggestedActions}
            onActionClick={handleSendMessage}
          />
        </div>
      )}

      {/* 输入框 */}
      <div className="px-4 py-3 border-t border-gray-200">
        <ChatInput
          onSend={handleSendMessage}
          disabled={isLoading}
          placeholder="试试：帮我写第三章..."
        />
      </div>

      {/* 快捷操作按钮 */}
      {messages.length === 0 && (
        <div className="px-4 pb-3 pt-1">
          <div className="text-xs text-gray-500 mb-1.5">快捷开始：</div>
          <div className="flex flex-wrap gap-1.5">
            <button
              onClick={() => handleSendMessage("帮我写第三章")}
              className="px-2 py-1 text-xs bg-white border border-gray-300 rounded-full hover:bg-gray-50 transition-colors"
            >
              📝 帮我写第三章
            </button>
            <button
              onClick={() => handleSendMessage("我想写一部玄幻小说")}
              className="px-2 py-1 text-xs bg-white border border-gray-300 rounded-full hover:bg-gray-50 transition-colors"
            >
              🌟 规划玄幻小说
            </button>
            <button
              onClick={() => handleSendMessage("我卡文了")}
              className="px-2 py-1 text-xs bg-white border border-gray-300 rounded-full hover:bg-gray-50 transition-colors"
            >
              💭 我卡文了
            </button>
            <button
              onClick={() => handleSendMessage("分析这段文字哪里不好")}
              className="px-2 py-1 text-xs bg-white border border-gray-300 rounded-full hover:bg-gray-50 transition-colors"
            >
              🔍 文本分析
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
