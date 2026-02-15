import React, { useEffect, useMemo, useState } from 'react';

interface ConversationSession {
  id: string;
  title: string;
  updatedAt: string;
  messages: any[];
  conversationId?: string;
  mode?: 'plan' | 'agent';  // 更新为新的模式命名
}

interface SessionTabsProps {
  sessions: ConversationSession[];
  activeSessionId: string;
  onSwitchSession: (sessionId: string) => void;
  onCreateSession: () => Promise<string>;
  onCloseSession: (sessionId: string) => void;
  onOpenHistory: () => void;
  onShowToast?: (type: 'success' | 'error' | 'warning' | 'info', message: string) => void;
  onInsertSessionAfter?: (newSessionId: string, afterSessionId: string) => void;
  className?: string;
}

export default function SessionTabs({
  sessions,
  activeSessionId,
  onSwitchSession,
  onCreateSession,
  onCloseSession,
  onOpenHistory,
  onShowToast,
  onInsertSessionAfter,
  className = ''
}: SessionTabsProps) {
  const [isCreating, setIsCreating] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearch, setShowSearch] = useState(false);

  useEffect(() => {
    const matchingSession = sessions.find((s) => s.id === activeSessionId);
    console.log('[SessionTabs] activeSessionId changed:', activeSessionId, matchingSession?.title);
  }, [activeSessionId, sessions]);

  const filteredSessions = useMemo(() => {
    if (!searchQuery.trim()) {
      return sessions;
    }

    const query = searchQuery.toLowerCase();
    return sessions.filter((s) => {
      if (s.title.toLowerCase().includes(query)) {
        return true;
      }
      const messagesToCheck = s.messages?.slice(0, 10) || [];
      return messagesToCheck.some((m) => m.content?.toLowerCase().includes(query));
    });
  }, [sessions, searchQuery]);

  const getSessionIcon = (session: ConversationSession) => {
    if (session.mode === 'agent') return '⚡';  // Agent 模式 (DeepAgent)
    if (session.mode === 'plan') return '📋';   // Plan 模式
    if (!session.messages || session.messages.length === 0) return '💬';
    return '📝';
  };

  const handleCloseSession = (e: React.MouseEvent, sessionId: string) => {
    e.stopPropagation();

    if (sessions.length <= 1) {
      onShowToast?.('warning', '至少需要保留一个会话');
      return;
    }

    if (sessionId === activeSessionId) {
      const currentIndex = sessions.findIndex((s) => s.id === sessionId);
      const nextSession = sessions[currentIndex + 1] || sessions[currentIndex - 1];
      if (nextSession) {
        onSwitchSession(nextSession.id);
      }
    }

    onCloseSession(sessionId);
  };

  const MAX_SESSIONS = 30;

  const handleCreateSession = async () => {
    if (isCreating) return;

    if (sessions.length >= MAX_SESSIONS) {
      onShowToast?.('warning', `会话数量已达上限（${MAX_SESSIONS}）`);
      return;
    }

    setIsCreating(true);
    try {
      const newSessionId = await onCreateSession();

      // onCreateSession already handles ordering; onInsertSessionAfter is kept for compatibility.
      if (onInsertSessionAfter && activeSessionId) {
        onInsertSessionAfter(newSessionId, activeSessionId);
      }
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className={`session-tabs flex items-center gap-2 px-4 py-2 bg-gray-900 border-b border-gray-700 ${className}`}>
      <button
        onClick={onOpenHistory}
        className="flex items-center justify-center w-8 h-8 text-gray-400 hover:text-white hover:bg-gray-800 rounded transition-colors"
        title="查看历史会话"
      >
        <span className="text-lg">🕘</span>
      </button>

      {sessions.length >= 5 && (
        <button
          onClick={() => setShowSearch(!showSearch)}
          className={`flex items-center justify-center w-8 h-8 rounded transition-colors ${
            showSearch ? 'text-blue-400 bg-gray-800' : 'text-gray-400 hover:text-white hover:bg-gray-800'
          }`}
          title="搜索会话"
        >
          <span className="text-sm">🔍</span>
        </button>
      )}

      {showSearch && (
        <div className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="搜索会话..."
            className="w-32 h-7 px-2 text-xs bg-gray-800 text-white border border-gray-600 rounded focus:outline-none focus:border-blue-500"
            autoFocus
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-1 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
            >
              ×
            </button>
          )}
        </div>
      )}

      <div className="w-px h-6 bg-gray-700" />

      <div className="flex-1 flex items-center gap-1 overflow-x-auto scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-gray-900">
        {searchQuery && filteredSessions.length === 0 && (
          <span className="text-xs text-gray-500 px-2">未找到匹配的会话</span>
        )}
        {filteredSessions.map((session) => {
          const isActive = session.id === activeSessionId;

          return (
            <div
              key={session.id}
              onClick={() => onSwitchSession(session.id)}
              className={`session-tab flex items-center gap-2 px-3 py-1.5 rounded-t-lg cursor-pointer transition-all min-w-[120px] max-w-[200px] ${
                isActive
                  ? 'bg-blue-600 text-white border-b-2 border-blue-400 shadow-lg shadow-blue-500/30 font-medium'
                  : 'bg-gray-800/50 text-gray-400 hover:bg-gray-700 hover:text-white border-b-2 border-transparent'
              }`}
            >
              <span
                className="text-xs flex-shrink-0"
                title={session.mode === 'agent' ? 'Agent 模式 (DeepAgent)' : session.mode === 'plan' ? 'Plan 模式' : '对话'}
              >
                {getSessionIcon(session)}
              </span>

              <span className="flex-1 text-sm truncate" title={session.title}>
                {session.title}
              </span>

              {session.messages && session.messages.length > 0 && (
                <span
                  className="text-[10px] px-1.5 py-0.5 rounded-full bg-gray-700/50 text-gray-400 flex-shrink-0"
                  title={`${session.messages.length} 条消息`}
                >
                  {session.messages.length}
                </span>
              )}

              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onOpenHistory();
                }}
                className="flex items-center justify-center w-5 h-5 rounded transition-all hover:bg-gray-700 text-gray-300 hover:text-white"
                title="历史会话"
              >
                <span className="text-sm">…</span>
              </button>
            </div>
          );
        })}
      </div>

      <div className="w-px h-6 bg-gray-700" />

      <button
        onClick={handleCreateSession}
        disabled={isCreating}
        className="flex items-center justify-center w-8 h-8 text-gray-400 hover:text-white hover:bg-gray-800 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        title="新建会话"
      >
        {isCreating ? <span className="text-sm animate-spin">⏳</span> : <span className="text-xl">+</span>}
      </button>
    </div>
  );
}
