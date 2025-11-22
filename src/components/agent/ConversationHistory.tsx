/**
 * ConversationHistory - 对话历史侧边栏组件
 *
 * 功能:
 * - 显示历史对话列表
 * - 切换对话
 * - 删除对话
 * - 创建新对话
 */

import React, { useState, useEffect } from 'react';

interface Message {
  role: 'user' | 'agent';
  content: string;
  timestamp: string;
  [key: string]: any;
}

interface ConversationSession {
  id: string;
  title: string;
  updatedAt: string;
  messages: Message[];
  conversationId?: string;
}

interface ConversationHistoryProps {
  currentSessionId: string;
  onLoadSession: (sessionId: string) => void;
  onCreateNew: () => void;
  getAllSessions: () => ConversationSession[];
  className?: string;
}

export default function ConversationHistory({
  currentSessionId,
  onLoadSession,
  onCreateNew,
  getAllSessions,
  className = ''
}: ConversationHistoryProps) {
  const [sessions, setSessions] = useState<ConversationSession[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  // 加载会话列表
  const refreshSessions = () => {
    const allSessions = getAllSessions();
    setSessions(allSessions);
  };

  useEffect(() => {
    refreshSessions();
  }, [currentSessionId]);

  // 格式化时间
  const formatTime = (isoString: string) => {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return '刚刚';
    if (diffMins < 60) return `${diffMins}分钟前`;
    if (diffHours < 24) return `${diffHours}小时前`;
    if (diffDays < 7) return `${diffDays}天前`;

    return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' });
  };

  const handleLoadSession = (sessionId: string) => {
    if (sessionId === currentSessionId) return;
    onLoadSession(sessionId);
    setIsOpen(false);
  };

  const handleCreateNew = () => {
    onCreateNew();
    setIsOpen(false);
    refreshSessions();
  };

  const handleDeleteSession = (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();

    if (!confirm('确定要删除这个对话吗？')) return;

    // 从localStorage删除
    localStorage.removeItem(`agent_conversation_${sessionId}`);

    // 从会话列表中移除
    const sessionsList = JSON.parse(localStorage.getItem('agent_conversation_sessions') || '[]');
    const updated = sessionsList.filter((id: string) => id !== sessionId);
    localStorage.setItem('agent_conversation_sessions', JSON.stringify(updated));

    // 如果删除的是当前会话，创建新会话
    if (sessionId === currentSessionId) {
      onCreateNew();
    }

    refreshSessions();
  };

  return (
    <>
      {/* 触发按钮 */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`p-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded transition-colors relative ${className}`}
        title="对话历史"
      >
        📚 历史
        {sessions.length > 0 && (
          <span className="absolute -top-1 -right-1 bg-blue-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center">
            {sessions.length > 9 ? '9+' : sessions.length}
          </span>
        )}
      </button>

      {/* 侧边栏 */}
      {isOpen && (
        <>
          {/* 遮罩层 */}
          <div
            className="fixed inset-0 bg-black bg-opacity-30 z-40"
            onClick={() => setIsOpen(false)}
          />

          {/* 侧边栏内容 */}
          <div className="fixed right-0 top-0 bottom-0 w-80 bg-white shadow-2xl z-50 flex flex-col">
            {/* 头部 */}
            <div className="px-4 py-3 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-gray-800">对话历史</h3>
                <button
                  onClick={() => setIsOpen(false)}
                  className="text-gray-500 hover:text-gray-700 text-lg"
                >
                  ✕
                </button>
              </div>
            </div>

            {/* 新建对话按钮 */}
            <div className="px-4 py-3 border-b border-gray-200">
              <button
                onClick={handleCreateNew}
                className="w-full px-3 py-2 bg-blue-500 text-white text-sm font-medium rounded-lg hover:bg-blue-600 transition-colors flex items-center justify-center gap-2"
              >
                <span className="text-lg">➕</span>
                新建对话
              </button>
            </div>

            {/* 会话列表 */}
            <div className="flex-1 overflow-y-auto">
              {sessions.length === 0 ? (
                <div className="px-4 py-8 text-center text-gray-500 text-sm">
                  <div className="text-4xl mb-2">📝</div>
                  <p>暂无历史对话</p>
                  <p className="text-xs mt-1">开始新对话后会自动保存</p>
                </div>
              ) : (
                <div className="space-y-1 p-2">
                  {sessions.map((session) => (
                    <div
                      key={session.id}
                      onClick={() => handleLoadSession(session.id)}
                      className={`
                        group px-3 py-2.5 rounded-lg cursor-pointer transition-all
                        ${session.id === currentSessionId
                          ? 'bg-blue-50 border border-blue-200'
                          : 'hover:bg-gray-50 border border-transparent'
                        }
                      `}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <h4 className={`
                              text-sm font-medium truncate
                              ${session.id === currentSessionId ? 'text-blue-700' : 'text-gray-800'}
                            `}>
                              {session.title}
                            </h4>
                            {session.id === currentSessionId && (
                              <span className="text-xs bg-blue-500 text-white px-1.5 py-0.5 rounded">
                                当前
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-3 text-xs text-gray-500">
                            <span>{session.messages.length} 条消息</span>
                            <span>•</span>
                            <span>{formatTime(session.updatedAt)}</span>
                          </div>
                        </div>

                        {/* 删除按钮 */}
                        <button
                          onClick={(e) => handleDeleteSession(session.id, e)}
                          className="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded transition-all"
                          title="删除对话"
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* 底部提示 */}
            <div className="px-4 py-2 border-t border-gray-200 bg-gray-50">
              <p className="text-xs text-gray-500 text-center">
                对话会自动保存到本地
              </p>
            </div>
          </div>
        </>
      )}
    </>
  );
}
