/**
 * RevisionCard - 修订胶囊组件
 * 显示修订操作，支持采纳/弃用/撤销/重做
 */

import { useState } from 'react';
import { FilePen, Check, X, ChevronDown, ChevronUp, Undo2, Redo2 } from 'lucide-react';
import type { RevisionFlowData } from '@/types/agent';

interface RevisionCardProps extends RevisionFlowData {
  onAccept?: (selectedVersion?: number) => void;
  onDiscard?: () => void;
  onUndo?: () => void;   // v7.2: 撤销回调
  onRedo?: () => void;   // v7.2: 重做回调
}

export function RevisionCard({
  revisionType,
  status,
  chapterTitle,
  contentPreview,
  oldTitle,
  newTitle,
  versions,
  onAccept,
  onDiscard,
  onUndo,
  onRedo
}: RevisionCardProps) {
  // v7.1: 已处理的修订默认收起，pending 状态默认展开
  const [expanded, setExpanded] = useState(status === 'pending');
  const [selectedVersion, setSelectedVersion] = useState(0);

  // 获取修订类型的显示文本
  const getRevisionTitle = () => {
    const titles: Record<string, string> = {
      append: '章节续写',
      replace: '文本改写',
      insert: '内容插入',
      create: '新建章节',
      rename: '修改标题'
    };
    return titles[revisionType] || '章节修订';
  };

  // 状态标签样式
  const statusStyles: Record<string, string> = {
    pending: 'bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400',
    accepted: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400',
    discarded: 'bg-gray-100 dark:bg-slate-700 text-gray-500 dark:text-slate-400'
  };

  const statusText: Record<string, string> = {
    pending: '待确认',
    accepted: '已采纳',
    discarded: '已弃用'
  };

  return (
    <div className={`inline-block bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 mb-3 ${
      expanded ? 'rounded-xl px-3 py-2' : 'rounded-full px-2.5 py-1'
    }`}>
      {/* 头部 */}
      <div
        className="flex items-center gap-1.5 cursor-pointer select-none"
        onClick={() => setExpanded(!expanded)}
      >
        <span className="text-gray-500">
          <FilePen size={12} />
        </span>
        <span className="text-[13px] text-gray-500">{getRevisionTitle()}</span>
        {/* v7.1: 收起状态下显示章节标题或新标题作为简要说明 */}
        {!expanded && (chapterTitle || newTitle) && (
          <span className="text-[12px] text-gray-400 dark:text-slate-500 truncate max-w-[120px]">
            · {chapterTitle || newTitle}
          </span>
        )}
        <span className="text-gray-400 dark:text-gray-600 text-[9px] ml-0.5">
          {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
        </span>
        <span className={`text-[10px] px-1.5 py-0.5 rounded-full ml-auto ${statusStyles[status]}`}>
          {statusText[status]}
        </span>
      </div>

      {/* 内容区域 */}
      {expanded && (
        <div className="pt-2">
          {/* 章节信息 */}
          {chapterTitle && (
            <div className="mb-2">
              <span className="text-[13px] text-blue-500 dark:text-[#5c9eff] underline underline-offset-2 cursor-pointer hover:text-blue-600">
                {chapterTitle}
              </span>
            </div>
          )}

          {/* 根据类型显示不同内容 */}
          {revisionType === 'rename' ? (
            // 修改标题
            <div className="space-y-1 mb-3">
              <div className="flex items-center gap-2 text-[13px]">
                <span className="text-gray-500 min-w-[50px]">原标题</span>
                <span className="text-gray-400 line-through">{oldTitle}</span>
              </div>
              <div className="flex items-center gap-2 text-[13px]">
                <span className="text-gray-500 min-w-[50px]">新标题</span>
                <span className="text-emerald-600 dark:text-emerald-400">{newTitle}</span>
              </div>
            </div>
          ) : revisionType === 'replace' && versions && versions.length > 0 ? (
            // 改写 - 多版本选择
            <div className="space-y-1.5 mb-3">
              {versions.map((v, idx) => (
                <label
                  key={idx}
                  className={`flex items-center gap-2 p-2 rounded-lg cursor-pointer transition-colors ${
                    selectedVersion === idx
                      ? 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800'
                      : 'bg-gray-50 dark:bg-slate-700/50 border border-transparent hover:bg-gray-100 dark:hover:bg-slate-700'
                  }`}
                >
                  <input
                    type="radio"
                    name="version"
                    checked={selectedVersion === idx}
                    onChange={() => setSelectedVersion(idx)}
                    className="w-3.5 h-3.5 text-blue-500"
                  />
                  <span className="text-[13px] text-gray-900 dark:text-white font-medium">{v.style_name}</span>
                  <span className="text-[12px] text-gray-500 dark:text-slate-400">{v.reason}</span>
                </label>
              ))}
            </div>
          ) : (
            // 其他类型 - 内容预览
            contentPreview && (
              <div className="bg-gray-50 dark:bg-slate-700/50 rounded-lg p-2.5 mb-3">
                <div className="text-[11px] text-gray-400 dark:text-slate-500 mb-1">
                  {revisionType === 'create' ? '章节内容预览' : '新增内容预览'}
                </div>
                <div className="text-[13px] text-gray-600 dark:text-slate-300 leading-[1.6] line-clamp-2">
                  "{contentPreview}..."
                </div>
              </div>
            )
          )}

          {/* 操作按钮 */}
          {status === 'pending' ? (
            <div className="flex gap-2">
              <button
                onClick={(e) => { e.stopPropagation(); onDiscard?.(); }}
                className="flex items-center gap-1 px-2.5 py-1 text-[12px] text-gray-500 dark:text-slate-400 bg-gray-100 dark:bg-slate-700 rounded-full hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors"
              >
                <X size={12} />
                弃用
              </button>
              <button
                onClick={(e) => { e.stopPropagation(); onAccept?.(versions ? selectedVersion : undefined); }}
                className="flex items-center gap-1 px-2.5 py-1 text-[12px] text-green-700 bg-green-50 border border-green-200 rounded-full hover:bg-green-100 dark:bg-green-900/30 dark:hover:bg-green-900/50 dark:text-green-400 dark:border-green-800 transition-colors"
              >
                <Check size={12} />
                采纳
              </button>
            </div>
          ) : status === 'accepted' ? (
            // v7.2: 已采纳状态 - 显示撤销按钮（create/rename 类型不支持撤销）
            <div className="flex items-center gap-2">
              <span className="flex items-center gap-1 text-[12px] text-emerald-600 dark:text-emerald-400">
                <Check size={12} />
                修订已采纳
              </span>
              {onUndo && revisionType !== 'create' && revisionType !== 'rename' && (
                <button
                  onClick={(e) => { e.stopPropagation(); onUndo(); }}
                  className="flex items-center gap-1 px-2 py-0.5 text-[11px] text-gray-500 dark:text-slate-400 bg-gray-100 dark:bg-slate-700 rounded-full hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors"
                >
                  <Undo2 size={10} />
                  撤销
                </button>
              )}
            </div>
          ) : (
            // v7.2: 已弃用状态 - 显示重做按钮（create/rename 类型不支持重做）
            <div className="flex items-center gap-2">
              <span className="flex items-center gap-1 text-[12px] text-gray-500">
                <X size={12} />
                修订已弃用
              </span>
              {onRedo && revisionType !== 'create' && revisionType !== 'rename' && (
                <button
                  onClick={(e) => { e.stopPropagation(); onRedo(); }}
                  className="flex items-center gap-1 px-2 py-0.5 text-[11px] text-gray-500 dark:text-slate-400 bg-gray-100 dark:bg-slate-700 rounded-full hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors"
                >
                  <Redo2 size={10} />
                  重做
                </button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
