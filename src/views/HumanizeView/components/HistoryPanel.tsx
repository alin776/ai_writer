// src/views/HumanizeView/components/HistoryPanel.tsx

import React, { useState, useEffect } from 'react';
import { Clock, TrendingDown, ChevronRight } from 'lucide-react';
import HumanizeService from '@/services/HumanizeService';
import type { HumanizeSession } from '@/types/humanize';
import { formatDate } from '@/utils/formatDate';

interface HistoryPanelProps {
  refreshKey: number;
  onOpenFullHistory: () => void;
  onSelectSession: (sessionId: string) => void;
  onCollapse?: () => void; // 新增：收起回调
}

export const HistoryPanel: React.FC<HistoryPanelProps> = ({
  refreshKey,
  onOpenFullHistory,
  onSelectSession,
  onCollapse,
}) => {
  const [sessions, setSessions] = useState<HumanizeSession[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // 加载历史记录
  useEffect(() => {
    const loadHistory = async () => {
      try {
        setIsLoading(true);
        const historyData = await HumanizeService.getHistory(1, 10);
        setSessions(historyData.items || []);
      } catch (err) {
        console.error('Failed to load history:', err);
      } finally {
        setIsLoading(false);
      }
    };
    loadHistory();
  }, [refreshKey]);

  return (
    <div className="h-full w-full flex flex-col bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden">
      {/* 标题栏 */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">历史记录</h3>
        {onCollapse && (
          <button
            onClick={onCollapse}
            className="p-1 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
            title="收起历史记录"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* 历史列表 */}
      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="flex items-center justify-center h-32">
            <div className="text-sm text-gray-400 dark:text-gray-500">加载中...</div>
          </div>
        ) : sessions.length === 0 ? (
          <div className="flex items-center justify-center h-32">
            <div className="text-center text-gray-400 dark:text-gray-500">
              <Clock className="w-8 h-8 mx-auto mb-2 opacity-30" />
              <p className="text-sm">暂无历史记录</p>
            </div>
          </div>
        ) : (
          <div className="divide-y divide-gray-100 dark:divide-gray-700">
            {sessions.map((session) => (
              <div
                key={session.id}
                className="p-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors cursor-pointer"
                onClick={() => session.id && onSelectSession(session.id)}
              >
                <div className="flex items-start justify-between mb-1.5">
                  <span className={`text-xs px-1.5 py-0.5 rounded font-medium ${
                    session.intensity === 'light' ? 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300' :
                    session.intensity === 'medium' ? 'bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300' :
                    'bg-orange-100 dark:bg-orange-900/50 text-orange-700 dark:text-orange-300'
                  }`}>
                    {session.intensity === 'light' && '轻度'}
                    {session.intensity === 'medium' && '中度'}
                    {session.intensity === 'strong' && '强度'}
                  </span>
                  {session.user_accepted !== null && (
                    <span className={`text-xs ${
                      session.user_accepted ? 'text-green-600 dark:text-green-400' : 'text-gray-400 dark:text-gray-500'
                    }`}>
                      {session.user_accepted ? '已接受' : '已拒绝'}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-400 mb-1">
                  <TrendingDown className="w-3 h-3" />
                  <span>改进 {session.improvement.toFixed(0)}分</span>
                </div>
                <div className="text-xs text-gray-400 dark:text-gray-500">
                  {formatDate(session.created_at)}
                </div>
                {session.detail && (
                  <div className="mt-1.5 text-xs text-gray-500 dark:text-gray-400 line-clamp-2">
                    {session.detail.original_preview}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 查看更多 */}
      <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700">
        <button
          onClick={onOpenFullHistory}
          className="w-full text-sm text-[#5865f2] hover:text-[#4752c4] font-medium"
        >
          查看全部历史
        </button>
      </div>
    </div>
  );
};
