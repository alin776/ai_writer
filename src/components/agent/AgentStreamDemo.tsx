/**
 * Agent Stream Demo - ReAct流式对话测试组件
 *
 * 用于测试和演示ReAct流式对话功能
 */

import React, { useState } from 'react';
import { useAgentChatStream } from '@/hooks/useAgentChatStream';
import ProgressIndicator from './ProgressIndicator';

export default function AgentStreamDemo() {
  const [message, setMessage] = useState('');
  const [workId, setWorkId] = useState('');
  const [chapterId, setChapterId] = useState('');

  const {
    loading,
    error,
    conversationId,
    currentProgress,
    progressHistory,
    toolCalls,
    content,
    result,
    sendMessage,
    clearError,
    reset,
  } = useAgentChatStream({
    onProgress: (progress) => {
      console.log('[Demo] Progress:', progress);
    },
    onToolCall: (toolCall) => {
      console.log('[Demo] Tool call:', toolCall);
    },
    onContent: (chunk) => {
      console.log('[Demo] Content chunk:', chunk);
    },
    onComplete: (data) => {
      console.log('[Demo] Complete:', data);
    },
    onError: (err) => {
      console.error('[Demo] Error:', err);
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    await sendMessage(message, {
      work_id: workId || undefined,
      chapter_id: chapterId || undefined,
    });
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* 标题 */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          Agent ReAct 流式对话测试
        </h1>
        <p className="text-sm text-gray-600 mt-1">
          测试新的ReAct模式流式响应功能
        </p>
      </div>

      {/* 输入表单 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* 消息输入 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              消息
            </label>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="输入你的消息..."
              disabled={loading}
            />
          </div>

          {/* 可选参数 */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Work ID (可选)
              </label>
              <input
                type="text"
                value={workId}
                onChange={(e) => setWorkId(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="作品ID"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Chapter ID (可选)
              </label>
              <input
                type="text"
                value={chapterId}
                onChange={(e) => setChapterId(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="章节ID"
                disabled={loading}
              />
            </div>
          </div>

          {/* 按钮 */}
          <div className="flex gap-2">
            <button
              type="submit"
              disabled={loading || !message.trim()}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? '发送中...' : '发送消息'}
            </button>
            <button
              type="button"
              onClick={reset}
              disabled={loading}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:bg-gray-100 disabled:cursor-not-allowed transition-colors"
            >
              重置
            </button>
          </div>
        </form>
      </div>

      {/* 会话ID显示 */}
      {conversationId && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-6">
          <p className="text-sm text-blue-700">
            <strong>会话ID:</strong> {conversationId}
          </p>
        </div>
      )}

      {/* 错误显示 */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-6">
          <div className="flex items-start justify-between">
            <p className="text-sm text-red-700">
              <strong>错误:</strong> {error.message}
            </p>
            <button
              onClick={clearError}
              className="text-red-500 hover:text-red-700"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* 进度显示 */}
      {(loading || currentProgress) && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">
            实时进度
          </h2>
          <ProgressIndicator
            currentProgress={currentProgress}
            toolCalls={toolCalls}
          />
        </div>
      )}

      {/* 内容显示 */}
      {content && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">
            生成内容
          </h2>
          <div className="prose max-w-none">
            <div className="whitespace-pre-wrap text-gray-700">{content}</div>
          </div>
        </div>
      )}

      {/* 最终结果 */}
      {result && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">
            最终结果
          </h2>
          <div className="space-y-3">
            {/* 响应文本 */}
            {result.response && (
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-1">
                  响应:
                </h3>
                <div className="bg-gray-50 rounded-lg p-3 text-sm text-gray-700 whitespace-pre-wrap">
                  {result.response}
                </div>
              </div>
            )}

            {/* 元数据 */}
            {result.metadata && (
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-1">
                  元数据:
                </h3>
                <pre className="bg-gray-50 rounded-lg p-3 text-xs text-gray-600 overflow-auto">
                  {JSON.stringify(result.metadata, null, 2)}
                </pre>
              </div>
            )}

            {/* 建议操作 */}
            {result.suggested_actions && result.suggested_actions.length > 0 && (
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-1">
                  建议操作:
                </h3>
                <div className="flex flex-wrap gap-2">
                  {result.suggested_actions.map((action: string, index: number) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                    >
                      {action}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* 进度历史 */}
      {progressHistory.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">
            进度历史 ({progressHistory.length})
          </h2>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {progressHistory.map((progress, index) => (
              <div
                key={index}
                className="text-sm bg-gray-50 rounded-lg p-3 border border-gray-200"
              >
                <div className="flex items-center justify-between">
                  <span className="font-medium text-gray-700">
                    {progress.description}
                  </span>
                  <span className="text-xs text-gray-500">
                    {new Date(progress.timestamp).toLocaleTimeString('zh-CN')}
                  </span>
                </div>
                {progress.details && (
                  <div className="mt-1 text-xs text-gray-600">
                    {JSON.stringify(progress.details)}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
