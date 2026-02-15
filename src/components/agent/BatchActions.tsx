/**
 * BatchActions — 批量审批操作面板
 *
 * 在 Agent 响应结束后显示，列出所有文件变更。
 * 支持全部接受/拒绝 + 单个接受/拒绝。
 */
import React, { useState, useEffect, useCallback } from 'react';
import { CheckCheck, XCircle, RefreshCw } from 'lucide-react';
import { changesApi, type FileChange } from '../../services/changesApi';
import FileChangeCard from './FileChangeCard';

interface BatchActionsProps {
  conversationId: string;
  onAllAccepted?: () => void;
  onAllRejected?: () => void;
  onRefreshChapters?: () => void;
}

const BatchActions: React.FC<BatchActionsProps> = ({
  conversationId,
  onAllAccepted,
  onAllRejected,
  onRefreshChapters,
}) => {
  const [changes, setChanges] = useState<FileChange[]>([]);
  const [loading, setLoading] = useState(true);
  const [acting, setActing] = useState(false);

  // 加载变更列表，返回新列表长度（避免闭包陈旧问题）
  const loadChanges = useCallback(async (): Promise<number> => {
    try {
      setLoading(true);
      const res = await changesApi.list(conversationId);
      const list = res.changes || [];
      setChanges(list);
      return list.length;
    } catch (err) {
      console.error('[BatchActions] 加载变更失败:', err);
      setChanges([]);
      return 0;
    } finally {
      setLoading(false);
    }
  }, [conversationId]);

  useEffect(() => {
    loadChanges();
  }, [loadChanges]);

  // 全部接受
  const handleAcceptAll = async () => {
    setActing(true);
    try {
      await changesApi.acceptAll(conversationId);
      setChanges([]);
      onAllAccepted?.();
      onRefreshChapters?.();
    } catch (err) {
      console.error('[BatchActions] 全部接受失败:', err);
    } finally {
      setActing(false);
    }
  };

  // 全部拒绝
  const handleRejectAll = async () => {
    setActing(true);
    try {
      await changesApi.rejectAll(conversationId);
      setChanges([]);
      onAllRejected?.();
      onRefreshChapters?.();
    } catch (err) {
      console.error('[BatchActions] 全部拒绝失败:', err);
    } finally {
      setActing(false);
    }
  };

  // 单个接受：调用 API 后重新拉取列表（后端会重新编号 index，本地过滤不安全）
  const handleAcceptOne = async (index: number) => {
    setActing(true);
    try {
      await changesApi.acceptOne(conversationId, index);
      const remaining = await loadChanges();
      if (remaining === 0) onRefreshChapters?.();
    } catch (err) {
      console.error('[BatchActions] 单个接受失败:', err);
    } finally {
      setActing(false);
    }
  };

  // 单个拒绝
  const handleRejectOne = async (index: number) => {
    setActing(true);
    try {
      await changesApi.rejectOne(conversationId, index);
      const remaining = await loadChanges();
      if (remaining === 0) onRefreshChapters?.();
    } catch (err) {
      console.error('[BatchActions] 单个拒绝失败:', err);
    } finally {
      setActing(false);
    }
  };

  // 点击卡片 → 触发 diff 视图
  const handleCardClick = (index: number) => {
    const change = changes[index];
    if (change) {
      window.dispatchEvent(new CustomEvent('editor-show-diff', {
        detail: {
          original: '',
          modified: change.content || change.diff || '',
          path: change.path,
        }
      }));
    }
  };

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 text-xs text-zinc-400">
        <RefreshCw className="h-3 w-3 animate-spin" />
        加载变更...
      </div>
    );
  }

  if (changes.length === 0) return null;

  return (
    <div className="mt-3 rounded-xl border border-zinc-200 dark:border-slate-700 overflow-hidden">
      {/* 标题栏 */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-zinc-50 dark:bg-slate-800 border-b border-zinc-200 dark:border-slate-700">
        <span className="text-sm font-medium text-zinc-700 dark:text-slate-200">
          文件变更 ({changes.length})
        </span>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleRejectAll}
            disabled={acting}
            className="flex items-center gap-1 px-2.5 py-1 text-xs rounded-md border border-red-200 text-red-600 hover:bg-red-50 disabled:opacity-50 dark:border-red-800 dark:hover:bg-red-900/30"
          >
            <XCircle className="h-3 w-3" />
            全部拒绝
          </button>
          <button
            type="button"
            onClick={handleAcceptAll}
            disabled={acting}
            className="flex items-center gap-1 px-2.5 py-1 text-xs rounded-md bg-green-600 text-white hover:bg-green-700 disabled:opacity-50"
          >
            <CheckCheck className="h-3 w-3" />
            全部接受
          </button>
        </div>
      </div>

      {/* 变更列表 */}
      <div className="p-2 space-y-1 max-h-[300px] overflow-y-auto">
        {changes.map((change, index) => (
          <FileChangeCard
            key={`${change.path}-${index}`}
            path={change.path}
            op={change.op}
            index={index}
            onAccept={handleAcceptOne}
            onReject={handleRejectOne}
            onClick={handleCardClick}
          />
        ))}
      </div>
    </div>
  );
};

export default BatchActions;
