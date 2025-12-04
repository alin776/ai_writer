/**
 * HistoryPanel - 历史会话面板组件
 *
 * 功能:
 * - 显示历史会话列表（包括已归档的）
 * - 从后端获取历史会话
 * - 恢复历史会话
 */

import React, { useState, useEffect, useCallback } from 'react';
import { agentApi } from '@/services/agentApi';
import type { HistorySessionItem } from '@/types/agent';

interface HistoryPanelProps {
  workId?: string;
  chapterId?: string;
  onClose: () => void;
  onRestore: (sessionId: string) => Promise<void>;
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

  // 加载历史会话列表（使用useCallback避免useEffect依赖警告）
  const loadHistorySessions = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await agentApi.getHistorySessions({
        workId,
        chapterId,
        limit: 50,
        includeArchived: true,  // 包括已归档的会话
      });

      setSessions(response.sessions);
      console.log('[HistoryPanel] 加载历史会话成功:', response.sessions.length, '个会话');
    } catch (err: any) {
      console.error('[HistoryPanel] 加载历史会话失败:', err);
      setError(err.response?.data?.detail || err.message || '加载失败');
    } finally {
      setIsLoading(false);
    }
  }, [workId, chapterId]);

  useEffect(() => {
    loadHistorySessions();
  }, [loadHistorySessions]);

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
    if (diffDays < 30) return `${diffDays}天前`;

    return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' });
  };

  // 恢复会话
  const handleRestore = async (sessionId: string) => {
    if (restoringSessionId) return;

    setRestoringSessionId(sessionId);
    try {
      await onRestore(sessionId);
      onClose();  // 恢复成功后关闭面板
    } catch (err: any) {
      console.error('[HistoryPanel] 恢复会话失败:', err);
      alert(`恢复失败: ${err.message}`);
    } finally {
      setRestoringSessionId(null);
    }
  };

  return (
    <>
      {/* 遮罩层 */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={onClose}
      />

      {/* 面板内容 */}
      <div className={`fixed right-0 top-0 bottom-0 w-full sm:w-96 bg-gray-900 text-white shadow-2xl z-50 flex flex-col ${className}`}>
        {/* 头部 */}
        <div className="px-4 py-3 border-b border-gray-700 bg-gray-800">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold">历史会话</h3>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white text-xl transition-colors"
            >
              ✕
            </button>
          </div>
          <p className="text-xs text-gray-400 mt-1">
            从后端恢复已归档的会话
          </p>
        </div>

        {/* 内容区域 */}
        <div className="flex-1 overflow-y-auto">
          {isLoading && (
            <div className="flex items-center justify-center h-full">
              <div className="text-gray-400 text-sm">
                <div className="animate-spin text-2xl mb-2">⭕</div>
                <p>加载中...</p>
              </div>
            </div>
          )}

          {error && (
            <div className="px-4 py-8 text-center">
              <div className="text-red-400 text-4xl mb-2">⚠️</div>
              <p className="text-red-400 text-sm">{error}</p>
              <button
                onClick={loadHistorySessions}
                className="mt-4 px-3 py-1 bg-gray-800 text-white text-sm rounded hover:bg-gray-700 transition-colors"
              >
                重试
              </button>
            </div>
          )}

          {!isLoading && !error && sessions.length === 0 && (
            <div className="px-4 py-8 text-center text-gray-500 text-sm">
              <div className="text-4xl mb-2">📝</div>
              <p>暂无历史会话</p>
              <p className="text-xs mt-1">已归档的会话会显示在这里</p>
            </div>
          )}

          {!isLoading && !error && sessions.length > 0 && (
            <div className="space-y-1 p-2">
              {sessions.map((session) => (
                <div
                  key={session.sessionId}
                  className="p-3 bg-gray-800 rounded-lg hover:bg-gray-750 transition-all border border-gray-700 hover:border-gray-600"
                >
                  {/* 标题和时间 */}
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-medium text-white truncate">
                        {session.title}
                      </h4>
                      <div className="flex items-center gap-3 text-xs text-gray-400 mt-1">
                        <span>{session.messageCount} 条消息</span>
                        <span>•</span>
                        <span>{formatTime(session.updatedAt)}</span>
                      </div>
                    </div>

                    {session.archivedAt && (
                      <span className="text-xs bg-yellow-500/20 text-yellow-400 px-2 py-0.5 rounded">
                        已归档
                      </span>
                    )}
                  </div>

                  {/* 最后消息预览 */}
                  {session.lastMessagePreview && (
                    <p className="text-xs text-gray-500 line-clamp-2 mb-2">
                      {session.lastMessagePreview}
                    </p>
                  )}

                  {/* 操作按钮 */}
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleRestore(session.sessionId)}
                      disabled={restoringSessionId !== null}
                      className="flex-1 px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {restoringSessionId === session.sessionId ? (
                        <span className="flex items-center justify-center gap-2">
                          <span className="animate-spin">⭕</span>
                          恢复中...
                        </span>
                      ) : (
                        '恢复会话'
                      )}
                    </button>
                    <div className="text-xs text-gray-500">
                      ID: {session.conversationId?.slice(0, 8)}...
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 底部提示 */}
        <div className="px-4 py-2 border-t border-gray-700 bg-gray-800">
          <p className="text-xs text-gray-400 text-center">
            历史会话保存在后端 Redis 中（30天）
          </p>
        </div>
      </div>
    </>
  );
}
