/**
 * RevisionCard - Cursor 风格紧凑文件卡片
 * 单行显示：[图标] 章节名.md  +N -M  [✓] [×]
 */

import { useState } from 'react';
import {
  FilePlus, FileEdit, FilePlus2, FileInput, FileType,
  Check, X
} from 'lucide-react';
import type { RevisionFlowData } from '@/types/agent';

interface RevisionCardProps extends RevisionFlowData {
  onAccept?: (selectedVersion?: number) => void;
  onDiscard?: () => void;
  onUndo?: () => void;
  onJump?: () => void;
  // 后端 event_translator 额外传入的字段（未在 RevisionFlowData 中声明）
  path?: string;        // 文件路径，如 "chapters/03-玉佩之谜.md"
  oldString?: string;   // 原始文本（replace 类型）
  newString?: string;   // 新文本（create/replace 类型）
  addLines?: number;    // 后端估算的新增行数
  delLines?: number;    // 后端估算的删除行数
}

// 图标映射（统一使用 text-slate-500 灰色，与 preview HTML 一致）
const iconMap = {
  create:  FilePlus,
  replace: FileEdit,
  append:  FilePlus2,
  insert:  FileInput,
  rename:  FileType,
} as const;

export function RevisionCard({
  revisionType,
  status,
  chapterTitle,
  oldTitle,
  newTitle,
  newContent,
  originalContent,
  versions,
  path,
  oldString,
  newString,
  addLines,
  delLines,
  onAccept,
  onDiscard,
  onJump,
}: RevisionCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [selectedVersion, setSelectedVersion] = useState(0);

  // 图标（统一灰色）
  const Icon = iconMap[revisionType] || iconMap.replace;

  // 文件名：路径已自带标题（chapters/06-考核之日.md），直接使用
  const cleanPath = path?.replace(/^\/+/, '');
  const displayName = revisionType === 'rename'
    ? `${oldTitle || '?'} → ${newTitle || '?'}`
    : cleanPath || `chapters/??-${chapterTitle || newTitle || '未命名'}.md`;

  // diff 行数：优先用后端 addLines/delLines，fallback 按实际换行符统计
  const countLines = (s: string | undefined) => s ? s.split('\n').length : null;
  const addCount = addLines || countLines(newString) || countLines(newContent);
  const delCount = delLines || countLines(oldString)
    || (revisionType === 'replace' && originalContent ? countLines(originalContent) : null);

  // replace 多版本：点击卡片时展开版本选择
  const hasVersions = revisionType === 'replace' && versions && versions.length > 1;

  const handleCardClick = () => {
    if (hasVersions && status === 'pending') {
      setExpanded(!expanded);
    } else {
      onJump?.();
    }
  };

  return (
    <div className="my-1">
      {/* 主行 */}
      <div
        className="flex items-center gap-2 px-2.5 py-1.5 bg-[#192438] rounded-lg cursor-pointer hover:bg-slate-800 transition-colors text-[13px]"
        onClick={handleCardClick}
      >
        {/* 操作图标 — 统一灰色 */}
        <Icon className="h-3.5 w-3.5 flex-shrink-0 text-slate-500" />

        {/* 文件名 */}
        <span className="text-slate-200 truncate flex-1">{displayName}</span>

        {/* diff 统计 */}
        {addCount != null && <span className="text-green-400 text-xs flex-shrink-0">+{addCount}</span>}
        {delCount != null && <span className="text-red-400 text-xs flex-shrink-0">-{delCount}</span>}

        {/* 操作按钮 / 状态图标 */}
        {status === 'pending' ? (
          <div className="flex gap-1 ml-auto flex-shrink-0">
            <button
              title="采纳"
              className="w-[22px] h-[22px] flex items-center justify-center rounded text-green-400 hover:bg-green-500/10 transition-colors"
              onClick={(e) => { e.stopPropagation(); onAccept?.(hasVersions ? selectedVersion : undefined); }}
            >
              <Check size={13} />
            </button>
            <button
              title="弃用"
              className="w-[22px] h-[22px] flex items-center justify-center rounded text-red-400 hover:bg-red-500/10 transition-colors"
              onClick={(e) => { e.stopPropagation(); onDiscard?.(); }}
            >
              <X size={13} />
            </button>
          </div>
        ) : status === 'accepted' ? (
          <Check size={13} className="text-green-400 ml-auto flex-shrink-0" />
        ) : (
          <X size={13} className="text-slate-500 ml-auto flex-shrink-0" />
        )}
      </div>

      {/* 多版本展开区（仅 replace + 多版本 + pending） */}
      {expanded && hasVersions && versions && (
        <div className="ml-6 mt-1 space-y-1">
          {versions.map((v, idx) => (
            <label
              key={idx}
              className={`flex items-center gap-2 px-2.5 py-1.5 rounded-lg cursor-pointer text-[12px] transition-colors ${
                selectedVersion === idx
                  ? 'bg-blue-900/20 text-blue-300'
                  : 'bg-[#192438] text-slate-400 hover:bg-slate-800'
              }`}
            >
              <input
                type="radio"
                name="version"
                checked={selectedVersion === idx}
                onChange={() => setSelectedVersion(idx)}
                className="w-3 h-3 text-blue-500"
              />
              <span className="font-medium text-slate-200">{v.style_name}</span>
              <span className="truncate">{v.reason}</span>
            </label>
          ))}
        </div>
      )}
    </div>
  );
}
