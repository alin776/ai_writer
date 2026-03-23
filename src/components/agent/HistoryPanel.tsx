/**
 * HistoryPanel - 历史会话抽屉
 *
 * 功能:
 * - 展示历史会话列表
 * - 从后端获取历史会话
 * - 恢复历史会话
 */

import React, { useState, useEffect, useCallback } from 'react';
import { formatUserError } from '@/utils/formatUserError';
import { agentApi } from '@/services/agentApi';
import type { HistorySessionItem } from '@/types/agent';
import { getChapterTabs, saveTab, deleteTab, removeTabFromChapter } from '@/utils/tabStorage';
import { Pencil, Trash2 } from 'lucide-react';

interface HistoryPanelProps {
  workId?: string;
  chapterId?: string;
  onClose: () => void;
  onRestore: (session: HistorySessionItem) => Promise<void>;
  className?: string;
}

export default function HistoryPanel({
  workId,
  chapterId,
  onClose,
  onRestore,
  className = ''
}: HistoryPanelProps) {
  const [sessions, setSessions] = useState<HistorySessionItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [restoringSessionId, setRestoringSessionId] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState<string>('');

  const loadHistorySessions = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    const resolveLocalSession = (ids: Array<string | undefined>) => {
      if (typeof window === 'undefined') return null;
      for (const id of ids.filter((v): v is string => Boolean(v))) {
        try {
          const stored = localStorage.getItem(`agent_conversation_${id}`);
          if (stored) {
            return JSON.parse(stored);
          }
        } catch (error) {
          console.warn('[HistoryPanel] 读取本地缓存失败:', error);
        }
      }
      return null;
    };

    const getTabTitle = (sessionId: string) => {
      try {
        const chapterKey = chapterId || workId || 'work';
        const tabs = getChapterTabs(chapterKey);
        const matched = tabs.find((t) => t.sessionId === sessionId);
        return matched?.title;
      } catch (error) {
        console.warn('[HistoryPanel] 读取标签页标题失败:', error);
        return undefined;
      }
    };

    try {
      const response = await agentApi.getHistorySessions({
        workId,
        chapterId,
        limit: 100
      });

      const enriched = response.sessions
        .map((s) => {
          const local = resolveLocalSession([s.sessionId, s.conversationId]);
          const tabTitle = getTabTitle(s.sessionId);
          const localMessages = Array.isArray(local?.messages) ? local.messages : [];
          const backendCount = typeof s.messageCount === 'number' ? s.messageCount : 0;
          const messageCount = Math.max(backendCount, localMessages.length);
          const lastPreview =
            local?.lastMessagePreview ||
            (localMessages.length > 0 ? localMessages[localMessages.length - 1]?.content?.slice(0, 80) : s.lastMessagePreview);

          return {
            ...s,
            title: tabTitle || local?.title || s.title || '历史会话',
            messageCount,
            lastMessagePreview: lastPreview,
            updatedAt: local?.updatedAt || s.updatedAt,
            conversationId: local?.conversationId || s.conversationId,
            titleLocked: s.titleLocked ?? local?.titleLocked ?? false,
          } as HistorySessionItem;
        })
        .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime());

      setSessions(enriched);
      console.log('[HistoryPanel] 加载历史会话成功:', enriched.length);
    } catch (err: any) {
      console.error('[HistoryPanel] 加载历史会话失败:', err);
      setError(formatUserError(err.response?.data?.detail || err.message));
    } finally {
      setIsLoading(false);
    }
  }, [workId, chapterId]);

  useEffect(() => {
    loadHistorySessions();
  }, [loadHistorySessions]);

  const formatTime = (isoString: string) => {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return '刚刚';
    if (diffMins < 60) return `${diffMins} 分钟前`;
    if (diffHours < 24) return `${diffHours} 小时前`;
    if (diffDays < 7) return `${diffDays} 天前`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} 周前`;

    return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' });
  };

  const applyRename = async (session: HistorySessionItem, newTitle: string) => {
    const trimmed = newTitle.trim();
    if (!trimmed) return;

    setSessions((prev) =>
      prev.map((s) => (s.sessionId === session.sessionId ? { ...s, title: trimmed } : s))
    );

    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(`agent_session_title_locked_${session.sessionId}`, '1');
      } catch {
        /* ignore */
      }
    }

    try {
      await agentApi.updateSessionTitle(session.sessionId, trimmed);
    } catch (error) {
      // 尝试用 conversationId 兜底
      if (session.conversationId) {
        try {
          await agentApi.updateSessionTitle(session.conversationId, trimmed);
        } catch (err) {
          console.warn('[HistoryPanel] 后端重命名失败，已仅本地更新:', err);
        }
      } else {
        console.warn('[HistoryPanel] 后端重命名失败，已仅本地更新:', error);
      }
    }

    if (typeof window !== 'undefined') {
      try {
        const stored = localStorage.getItem(`agent_conversation_${session.sessionId}`);
        if (stored) {
          const parsed = JSON.parse(stored);
          parsed.title = trimmed;
          localStorage.setItem(`agent_conversation_${session.sessionId}`, JSON.stringify(parsed));
        }
      } catch (error) {
        console.warn('[HistoryPanel] 重命名本地会话失败:', error);
      }

      if (session.titleLocked) {
        try {
          localStorage.setItem(`agent_session_title_locked_${session.sessionId}`, '1');
        } catch {/* ignore */}
      }

      // 更新当前章节下的标签标题（如果存在对应 tab）
      const chapterKey = chapterId || workId || 'work';
      const tabs = getChapterTabs(chapterKey);
      tabs
        .filter((t) => t.sessionId === session.sessionId)
        .forEach((t) => {
          const updated = { ...t, title: trimmed, updatedAt: new Date().toISOString() };
          saveTab(updated);
        });

      // 通知 Tab 管理器刷新
      window.dispatchEvent(
        new CustomEvent('agent-tab-updated', {
          detail: { sessionId: session.sessionId }
        })
      );
    }
  };
  const handleRename = (session: HistorySessionItem) => {
    setEditingId(session.sessionId);
    setEditingTitle(session.title || '');
  };

  const commitEditing = async (session: HistorySessionItem) => {
    await applyRename(session, editingTitle || session.title || '');
    setEditingId(null);
    setEditingTitle('');
  };

  const handleDelete = async (session: HistorySessionItem) => {
    setSessions((prev) => prev.filter((s) => s.sessionId !== session.sessionId));

    if (typeof window !== 'undefined') {
      try {
        await agentApi.deleteSession(session.sessionId);
        localStorage.removeItem(`agent_conversation_${session.sessionId}`);
        const listKey = 'agent_conversation_sessions';
        const storedList = localStorage.getItem(listKey);
        const ids: string[] = storedList ? JSON.parse(storedList) : [];
        const updatedIds = ids.filter((id) => id !== session.sessionId);
        localStorage.setItem(listKey, JSON.stringify(updatedIds));
        localStorage.removeItem(`agent_session_title_locked_${session.sessionId}`);

        const chapterKey = chapterId || workId || 'work';
        const tabs = getChapterTabs(chapterKey).filter((t) => t.sessionId === session.sessionId);
        tabs.forEach((t) => {
          deleteTab(t.id);
          removeTabFromChapter(chapterKey, t.id);
        });
      } catch (error) {
        console.warn('[HistoryPanel] 删除会话失败:', error);
      }

      window.dispatchEvent(
        new CustomEvent('agent-tab-deleted', {
          detail: { sessionId: session.sessionId }
        })
      );
    }
  };

  const getDisplayId = (session: HistorySessionItem) => {
    const id = session.conversationId || session.sessionId;
    return id ? id.slice(0, 8) : 'N/A';
  };

  const handleRestore = async (session: HistorySessionItem) => {
    if (restoringSessionId) return;
    setRestoringSessionId(session.sessionId);
    try {
      await onRestore(session);
      onClose();
    } catch (err: any) {
      console.error('[HistoryPanel] 恢复会话失败:', err);
      setError(formatUserError(err.message));
    } finally {
      setRestoringSessionId(null);
    }
  };

  return (
    <>
      <div className="fixed inset-0 bg-black/30 dark:bg-black/50 z-40" onClick={onClose} />

      <div
        className={`fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] sm:w-[480px] min-h-[500px] max-h-[85vh] bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-2xl shadow-2xl z-50 flex flex-col overflow-hidden ${className}`}
      >
        <div className="px-4 py-3 bg-white/95 dark:bg-slate-800/95 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-semibold text-gray-900 dark:text-white">历史会话</h3>
            </div>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 dark:text-slate-400 dark:hover:text-slate-200 text-xl leading-none"
              aria-label="关闭历史会话"
            >
              ×
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto bg-white dark:bg-slate-800">
          {isLoading && (
            <div className="flex flex-col items-center justify-center h-full text-sm text-gray-500 dark:text-slate-400">
              <div className="h-5 w-5 border-2 border-gray-300 dark:border-slate-600 border-t-blue-500 dark:border-t-blue-400 rounded-full animate-spin mb-3" />
              <p>加载中...</p>
            </div>
          )}

          {error && (
            <div className="px-4 py-8 text-center">
              <p className="text-sm text-red-500 dark:text-red-400 mb-3">{error}</p>
              <button
                onClick={loadHistorySessions}
                className="px-3 py-1.5 bg-blue-600 dark:bg-blue-500 text-white text-xs rounded-md hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors"
              >
                重试
              </button>
            </div>
          )}

          {!isLoading && !error && sessions.length === 0 && (
            <div className="px-4 py-10 text-center text-gray-500 dark:text-slate-400 text-sm">
              <div className="text-3xl mb-2">🗂️</div>
              <p className="font-medium text-gray-700 dark:text-slate-300">暂无历史会话</p>
            </div>
          )}

          {!isLoading && !error && sessions.length > 0 && (
            <div className="space-y-1 p-2">
              {sessions.map((session) => (
                <div
                  key={session.sessionId || session.conversationId || session.title}
                  onClick={() => handleRestore(session)}
                  className="rounded-lg border border-gray-100 dark:border-slate-700 bg-white dark:bg-slate-700/50 hover:bg-gray-50 dark:hover:bg-slate-700 shadow-sm hover:shadow-md transition-all px-3 py-2 cursor-pointer group"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      {editingId === session.sessionId ? (
                        <input
                          autoFocus
                          value={editingTitle}
                          onChange={(e) => setEditingTitle(e.target.value)}
                          onClick={(e) => e.stopPropagation()}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                              e.preventDefault();
                              commitEditing(session);
                            }
                            if (e.key === 'Escape') {
                              e.stopPropagation();
                              setEditingId(null);
                              setEditingTitle('');
                            }
                          }}
                          onBlur={() => commitEditing(session)}
                          className="w-full text-sm font-medium text-gray-900 dark:text-white bg-white dark:bg-slate-600 border border-blue-200 dark:border-blue-500 rounded px-1 py-0.5 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        />
                      ) : (
                        <h4 className="text-sm font-medium text-gray-900 dark:text-white truncate">{session.title}</h4>
                      )}
                      <p className="text-[11px] text-gray-500 dark:text-slate-400 mt-0.5">{formatTime(session.updatedAt)}</p>
                    </div>
                    <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleRename(session);
                        }}
                        className="p-1 rounded-md hover:bg-gray-100 dark:hover:bg-slate-600 text-gray-500 dark:text-slate-400"
                        aria-label="重命名会话"
                      >
                        <Pencil className="w-4 h-4" />
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(session);
                        }}
                        className="p-1 rounded-md hover:bg-gray-100 dark:hover:bg-slate-600 text-gray-500 dark:text-slate-400"
                        aria-label="删除会话"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  {session.lastMessagePreview && (
                    <p className="text-[12px] text-gray-600 dark:text-slate-300 line-clamp-2 mt-1 leading-relaxed">
                      {session.lastMessagePreview}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="px-4 py-3 bg-white dark:bg-slate-800">
          <p className="text-[11px] text-gray-500 dark:text-slate-500 text-center">历史会话存储 30 天</p>
        </div>
      </div>
    </>
  );
}
