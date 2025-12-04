// src/views/HumanizeHistoryView/SessionDetail.tsx

import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import HumanizeService from '@/services/HumanizeService';
import type { HumanizeSession } from '@/types/humanize';
import { formatRelativeTime, formatFullDate } from '@/utils/formatDate';
import { ArrowLeft, TrendingDown, Loader2, Copy } from 'lucide-react';

export const HumanizeSessionDetail: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const [session, setSession] = useState<HumanizeSession | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isOriginalExpanded, setIsOriginalExpanded] = useState(false);
  const [isHumanizedExpanded, setIsHumanizedExpanded] = useState(false);
  const [copyMessage, setCopyMessage] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      if (!sessionId) return;
      try {
        setLoading(true);
        const data = await HumanizeService.getSession(sessionId);
        setSession(data);
      } catch (e: any) {
        setError(e?.message || '加载详情失败');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [sessionId]);

  const handleCopy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopyMessage('已复制');
      setTimeout(() => setCopyMessage(null), 1500);
    } catch (e) {
      setCopyMessage('复制失败');
      setTimeout(() => setCopyMessage(null), 1500);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-6 py-6 space-y-4">
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/humanize/history')}
          className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="w-4 h-4" />
          返回历史列表
        </button>
        <h1 className="text-xl font-semibold text-gray-900">历史详情</h1>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-48 text-gray-500">
          <Loader2 className="w-5 h-5 animate-spin mr-2" />
          加载中...
        </div>
      ) : error ? (
        <div className="text-red-600 text-sm">{error}</div>
      ) : session ? (
        <div className="space-y-4">
          <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-sm flex items-center gap-3">
            <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 text-sm">
              {session.intensity === 'light' ? '轻度' : session.intensity === 'medium' ? '中度' : '强度'}
            </span>
            <div className="text-sm text-gray-600 flex items-center gap-2">
              <TrendingDown className="w-4 h-4" />
              改进 {session.improvement.toFixed(0)} 分
            </div>
            <div className="text-xs text-gray-500">
              {formatRelativeTime(session.created_at)} · {formatFullDate(session.created_at)}
            </div>
          </div>

          {session.detail?.original_preview && (
            <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-sm space-y-2">
              <div className="flex items-center justify-between">
                <h2 className="text-sm font-semibold text-gray-800">原文片段</h2>
                <div className="flex items-center gap-2 text-xs">
                  <button
                    onClick={() => setIsOriginalExpanded((v) => !v)}
                    className="text-blue-600 hover:text-blue-700"
                  >
                    {isOriginalExpanded ? '收起' : '展开'}
                  </button>
                  <button
                    onClick={() => handleCopy(session.detail.original_preview || '')}
                    className="flex items-center gap-1 text-gray-600 hover:text-gray-900"
                  >
                    <Copy className="w-4 h-4" />
                    复制
                  </button>
                </div>
              </div>
              <p
                className={`text-sm text-gray-700 whitespace-pre-wrap ${
                  isOriginalExpanded ? '' : 'line-clamp-5'
                }`}
              >
                {session.detail.original_preview}
              </p>
            </div>
          )}

          {session.detail?.humanized_preview && (
            <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-sm space-y-2">
              <div className="flex items-center justify-between">
                <h2 className="text-sm font-semibold text-gray-800">改写后片段</h2>
                <div className="flex items-center gap-2 text-xs">
                  <button
                    onClick={() => setIsHumanizedExpanded((v) => !v)}
                    className="text-blue-600 hover:text-blue-700"
                  >
                    {isHumanizedExpanded ? '收起' : '展开'}
                  </button>
                  <button
                    onClick={() => handleCopy(session.detail.humanized_preview || '')}
                    className="flex items-center gap-1 text-gray-600 hover:text-gray-900"
                  >
                    <Copy className="w-4 h-4" />
                    复制
                  </button>
                </div>
              </div>
              <p
                className={`text-sm text-gray-700 whitespace-pre-wrap ${
                  isHumanizedExpanded ? '' : 'line-clamp-5'
                }`}
              >
                {session.detail.humanized_preview}
              </p>
            </div>
          )}

          {copyMessage && <div className="text-xs text-green-600">{copyMessage}</div>}
        </div>
      ) : (
        <div className="text-sm text-gray-500">未找到该会话</div>
      )}
    </div>
  );
};

export default HumanizeSessionDetail;
