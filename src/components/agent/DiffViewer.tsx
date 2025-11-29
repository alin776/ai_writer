/**
 * Diff差异视图组件 - 显示文本变更差异
 */
import React, { useMemo } from 'react';
import { diff_match_patch, DIFF_DELETE, DIFF_INSERT, DIFF_EQUAL } from 'diff-match-patch';

interface DiffViewerProps {
  original: string;
  modified: string;
  showLineNumbers?: boolean;
  maxHeight?: number;
  className?: string;
}

export const DiffViewer: React.FC<DiffViewerProps> = ({
  original,
  modified,
  showLineNumbers = false,
  maxHeight = 400,
  className = ''
}) => {
  const dmp = useMemo(() => new diff_match_patch(), []);

  // ✅ P0-6修复：添加空值保护，避免diff_main收到null
  const safeOriginal = original ?? '';
  const safeModified = modified ?? '';

  const diffs = useMemo(() => {
    const rawDiffs = dmp.diff_main(safeOriginal, safeModified);
    dmp.diff_cleanupSemantic(rawDiffs);
    return rawDiffs;
  }, [safeOriginal, safeModified, dmp]);

  // 计算统计信息
  const stats = useMemo(() => {
    let added = 0, removed = 0;
    diffs.forEach(([op, text]) => {
      if (op === DIFF_INSERT) added += text.length;
      if (op === DIFF_DELETE) removed += text.length;
    });
    return { added, removed };
  }, [diffs]);

  return (
    <div className={`diff-viewer border border-gray-200 rounded-lg overflow-hidden ${className}`}>
      {/* 统计栏 */}
      <div className="diff-stats px-3 py-2 bg-gray-50 border-b border-gray-200 text-xs flex items-center gap-3">
        <span className="text-green-600 font-medium">+{stats.added}字</span>
        <span className="text-gray-400">|</span>
        <span className="text-red-600 font-medium">-{stats.removed}字</span>
      </div>

      {/* 差异内容 */}
      <div
        className="diff-content p-3 overflow-y-auto text-sm leading-relaxed"
        style={{ maxHeight }}
      >
        {diffs.map(([op, text], index) => {
          let className = '';
          if (op === DIFF_INSERT) {
            className = 'bg-green-100 text-green-800';
          } else if (op === DIFF_DELETE) {
            className = 'bg-red-100 text-red-800 line-through';
          }

          return (
            <span key={index} className={className}>
              {text}
            </span>
          );
        })}
      </div>
    </div>
  );
};

export default DiffViewer;
