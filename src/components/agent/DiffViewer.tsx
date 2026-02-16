/**
 * DiffViewer - 行级差异视图组件
 * 红绿行 + 行号 + 折叠未变区域，类似 VS Code diff
 */
import React, { useMemo, useState } from 'react';
import { diff_match_patch, DIFF_DELETE, DIFF_INSERT, DIFF_EQUAL } from 'diff-match-patch';

interface DiffViewerProps {
  original: string;
  modified: string;
  /** 未变区域折叠时显示的上下文行数 */
  contextLines?: number;
  maxHeight?: number;
  className?: string;
  /** 内联模式：去掉边框/圆角，融入编辑器 */
  inline?: boolean;
}

interface DiffLine {
  type: 'add' | 'del' | 'ctx';
  lineNo: number | null;   // 目标文件行号（del 行用原始行号）
  content: string;
}

/**
 * 将 diff-match-patch 的字符级结果转换为行级 DiffLine 数组
 */
function computeLineDiffs(original: string, modified: string): DiffLine[] {
  const dmp = new diff_match_patch();
  const rawDiffs = dmp.diff_main(original, modified);
  dmp.diff_cleanupSemantic(rawDiffs);

  // 先拼成带标记的行
  const lines: DiffLine[] = [];
  let oldLineNo = 1;
  let newLineNo = 1;

  for (const [op, text] of rawDiffs) {
    const segments = text.split('\n');
    for (let i = 0; i < segments.length; i++) {
      const seg = segments[i];
      const isLast = i === segments.length - 1;

      if (op === DIFF_EQUAL) {
        if (seg || !isLast) {
          lines.push({ type: 'ctx', lineNo: newLineNo, content: seg });
        }
        if (!isLast) { oldLineNo++; newLineNo++; }
      } else if (op === DIFF_DELETE) {
        if (seg || !isLast) {
          lines.push({ type: 'del', lineNo: oldLineNo, content: seg });
        }
        if (!isLast) { oldLineNo++; }
      } else if (op === DIFF_INSERT) {
        if (seg || !isLast) {
          lines.push({ type: 'add', lineNo: newLineNo, content: seg });
        }
        if (!isLast) { newLineNo++; }
      }
    }
  }
  return lines;
}

/**
 * 将连续的 ctx 行分组，中间超过 contextLines*2 行的折叠
 */
interface DiffBlock {
  type: 'lines' | 'fold';
  lines: DiffLine[];
  foldCount?: number;
}

function groupWithFolds(lines: DiffLine[], contextLines: number): DiffBlock[] {
  // 标记哪些行需要展示（changed 行以及周围 contextLines 行）
  const show = new Array(lines.length).fill(false);
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].type !== 'ctx') {
      const start = Math.max(0, i - contextLines);
      const end = Math.min(lines.length - 1, i + contextLines);
      for (let j = start; j <= end; j++) show[j] = true;
    }
  }

  const blocks: DiffBlock[] = [];
  let i = 0;
  while (i < lines.length) {
    if (show[i]) {
      // 收集连续可见行
      const group: DiffLine[] = [];
      while (i < lines.length && show[i]) {
        group.push(lines[i]);
        i++;
      }
      blocks.push({ type: 'lines', lines: group });
    } else {
      // 收集连续隐藏行（全是 ctx）
      const group: DiffLine[] = [];
      while (i < lines.length && !show[i]) {
        group.push(lines[i]);
        i++;
      }
      blocks.push({ type: 'fold', lines: group, foldCount: group.length });
    }
  }
  return blocks;
}

export const DiffViewer: React.FC<DiffViewerProps> = ({
  original,
  modified,
  contextLines = 3,
  maxHeight,
  className = '',
  inline = false,
}) => {
  const safeOriginal = original ?? '';
  const safeModified = modified ?? '';

  const lines = useMemo(() => computeLineDiffs(safeOriginal, safeModified), [safeOriginal, safeModified]);
  const blocks = useMemo(() => groupWithFolds(lines, contextLines), [lines, contextLines]);

  // 折叠展开状态
  const [expandedFolds, setExpandedFolds] = useState<Set<number>>(new Set());
  const toggleFold = (idx: number) => {
    setExpandedFolds(prev => {
      const next = new Set(prev);
      next.has(idx) ? next.delete(idx) : next.add(idx);
      return next;
    });
  };

  const containerClass = inline
    ? `diff-viewer bg-white dark:bg-slate-900 ${className}`
    : `diff-viewer border border-slate-700 rounded-lg overflow-hidden bg-[#0d1117] ${className}`;

  const foldClass = inline
    ? 'px-4 py-1 text-center text-xs text-zinc-400 dark:text-slate-500 bg-zinc-50 dark:bg-slate-800/30 border-y border-zinc-100 dark:border-slate-800 cursor-pointer hover:bg-zinc-100 dark:hover:bg-slate-800 select-none'
    : 'px-3 py-1 text-center text-xs text-slate-500 bg-[#161b22] border-y border-slate-800 cursor-pointer hover:bg-slate-800 select-none';

  return (
    <div className={containerClass}>
      {/* 差异内容 */}
      <div
        className={inline ? "font-mono text-[13px] leading-[1.6]" : "overflow-y-auto font-mono text-[13px] leading-[1.6]"}
        style={maxHeight ? { maxHeight } : undefined}
      >
        {blocks.map((block, blockIdx) => {
          if (block.type === 'fold' && !expandedFolds.has(blockIdx)) {
            return (
              <div
                key={blockIdx}
                className={foldClass}
                onClick={() => toggleFold(blockIdx)}
              >
                ··· {block.foldCount} 行未变 ···
              </div>
            );
          }

          // 走到这里：要么是 lines 块，要么是已展开的 fold 块
          return (
            <React.Fragment key={blockIdx}>
              {block.lines.map((line, lineIdx) => {
                let bgClass = '';
                let prefix = ' ';
                let textClass = inline ? 'text-zinc-700 dark:text-slate-300' : 'text-slate-300';
                let lineNoClass = inline ? 'text-zinc-400 dark:text-slate-600' : 'text-slate-600';

                if (line.type === 'add') {
                  bgClass = inline ? 'bg-green-50 dark:bg-green-500/10' : 'bg-green-500/10';
                  prefix = '+';
                  textClass = inline ? 'text-green-800 dark:text-green-300' : 'text-green-300';
                  lineNoClass = inline ? 'text-green-600/50 dark:text-green-800' : 'text-green-800';
                } else if (line.type === 'del') {
                  bgClass = inline ? 'bg-red-50 dark:bg-red-500/10' : 'bg-red-500/10';
                  prefix = '-';
                  textClass = inline ? 'text-red-800 dark:text-red-300' : 'text-red-300';
                  lineNoClass = inline ? 'text-red-600/50 dark:text-red-800' : 'text-red-800';
                }

                return (
                  <div key={`${blockIdx}-${lineIdx}`} className={`flex ${bgClass}`}>
                    <span className={`w-10 flex-shrink-0 text-right pr-2 select-none ${lineNoClass}`}>
                      {line.lineNo ?? ''}
                    </span>
                    <span className={`w-4 flex-shrink-0 text-center select-none ${textClass}`}>
                      {prefix}
                    </span>
                    <span className={`flex-1 pr-3 whitespace-pre-wrap break-all ${textClass}`}>
                      {line.content}
                    </span>
                  </div>
                );
              })}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

export default DiffViewer;
