// src/views/HumanizeHistoryView/index.tsx

import React, { useEffect, useState } from 'react';
import HumanizeService from '@/services/HumanizeService';
import type { HumanizeSession, HumanizeHistoryResponse } from '@/types/humanize';
import { formatRelativeTime } from '@/utils/formatDate';
import { TrendingDown, Loader2, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const PAGE_SIZE = 20;

export const HumanizeHistoryView: React.FC = () => {
  const [history, setHistory] = useState<HumanizeHistoryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const data = await HumanizeService.getHistory(1, PAGE_SIZE);
        setHistory(data);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-6 py-6">
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={() => navigate('/humanize')}
          className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="w-4 h-4" />
          返回 AI去痕
        </button>
        <h1 className="text-xl font-semibold text-gray-900">历史记录</h1>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-48 text-gray-500">
          <Loader2 className="w-5 h-5 animate-spin mr-2" />
          加载中...
        </div>
      ) : history && history.items.length > 0 ? (
        <div className="space-y-3">
          {history.items.map((session: HumanizeSession) => (
            <div
              key={session.id}
              className="p-4 bg-white border border-gray-200 rounded-lg shadow-sm flex justify-between items-center cursor-pointer hover:border-blue-200"
              onClick={() => navigate(`/humanize/history/${session.id}`)}
            >
              <div>
                <div className="flex items-center gap-2 text-sm text-gray-700">
                  <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700">
                    {session.intensity === 'light' ? '轻度' : session.intensity === 'medium' ? '中度' : '强度'}
                  </span>
                  <span className="text-gray-500">{formatRelativeTime(session.created_at)}</span>
                </div>
                <div className="flex items-center gap-2 text-xs text-gray-600 mt-1">
                  <TrendingDown className="w-3 h-3" />
                  改进 {session.improvement.toFixed(0)} 分
                </div>
                {session.detail?.original_preview && (
                  <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                    {session.detail.original_preview}
                  </p>
                )}
              </div>
              <span className="text-sm text-blue-600">查看详情</span>
            </div>
          ))}
        </div>
      ) : (
        <div className="h-48 flex items-center justify-center text-gray-400">暂无历史记录</div>
      )}
    </div>
  );
};

export default HumanizeHistoryView;
