/**
 * DiffViewer - 行级差异视图组件
 * 行级 diff + 行内字符高亮 + 折叠未变区域，类似 VS Code diff
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

interface DiffSpan {
  type: 'equal' | 'del' | 'add';
  text: string;
}

interface DiffLine {
  type: 'add' | 'del' | 'ctx';
  lineNo: number | null;   // 目标文件行号（del 行用原始行号）
  content: string;
  /** 行内字符级高亮（配对的 del/add 行才有） */
  spans?: DiffSpan[];
}

/**
 * 行级 diff：先用 diff_linesToChars_ 把每行当原子单位，再为配对行添加字符级高亮
 */
function computeLineDiffs(original: string, modified: string): DiffLine[] {
  const dmp = new diff_match_patch();

  // Phase 1: 行级 diff（每行作为一个原子单位比较）
  const a = dmp.diff_linesToChars_(original, modified);
  const diffs = dmp.diff_main(a.chars1, a.chars2, false);
  dmp.diff_charsToLines_(diffs, a.lineArray);

  // Phase 2: 转换为 DiffLine 数组
  const lines: DiffLine[] = [];
  let oldLineNo = 1;
  let newLineNo = 1;

  for (const [op, text] of diffs) {
    // diff_linesToChars_ 保留行尾 \n，split 后末尾会有空串
    const splitLines = text.split('\n');
    if (splitLines.length > 0 && splitLines[splitLines.length - 1] === '') {
      splitLines.pop();
    }

    for (const lineText of splitLines) {
      if (op === DIFF_EQUAL) {
        lines.push({ type: 'ctx', lineNo: newLineNo, content: lineText });
        oldLineNo++;
        newLineNo++;
      } else if (op === DIFF_DELETE) {
        lines.push({ type: 'del', lineNo: oldLineNo, content: lineText });
        oldLineNo++;
      } else if (op === DIFF_INSERT) {
        lines.push({ type: 'add', lineNo: newLineNo, content: lineText });
        newLineNo++;
      }
    }
  }

  // Phase 3: 为配对的 del/add 行添加行内字符级高亮
  let i = 0;
  while (i < lines.length) {
    // 找连续 del 块
    const delStart = i;
    while (i < lines.length && lines[i].type === 'del') i++;
    const delEnd = i;

    // 找紧接着的连续 add 块
    const addStart = i;
    while (i < lines.length && lines[i].type === 'add') i++;
    const addEnd = i;

    const delCount = delEnd - delStart;
    const addCount = addEnd - addStart;

    // 配对行：逐行计算字符级差异
    if (delCount > 0 && addCount > 0) {
      const pairCount = Math.min(delCount, addCount);
      for (let j = 0; j < pairCount; j++) {
        const delLine = lines[delStart + j];
        const addLine = lines[addStart + j];
        const charDiffs = dmp.diff_main(delLine.content, addLine.content);
        dmp.diff_cleanupSemantic(charDiffs);

        delLine.spans = charDiffs
          .filter(([op]) => op !== DIFF_INSERT)
          .map(([op, text]) => ({
            type: op === DIFF_DELETE ? 'del' as const : 'equal' as const,
            text,
          }));

        addLine.spans = charDiffs
          .filter(([op]) => op !== DIFF_DELETE)
          .map(([op, text]) => ({
            type: op === DIFF_INSERT ? 'add' as const : 'equal' as const,
            text,
          }));
      }
    }

    // 没有 del 也没有 add 时（纯 ctx）前进
    if (delCount === 0 && addCount === 0) i++;
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
                // 行内高亮样式（标注具体改了哪些字符）
                let hlClass = '';

                if (line.type === 'add') {
                  bgClass = inline ? 'bg-green-50 dark:bg-green-500/10' : 'bg-green-500/10';
                  prefix = '+';
                  textClass = inline ? 'text-green-800 dark:text-green-300' : 'text-green-300';
                  lineNoClass = inline ? 'text-green-600/50 dark:text-green-800' : 'text-green-800';
                  hlClass = inline ? 'bg-green-200/70 dark:bg-green-500/30 rounded-sm' : 'bg-green-500/30 rounded-sm';
                } else if (line.type === 'del') {
                  bgClass = inline ? 'bg-red-50 dark:bg-red-500/10' : 'bg-red-500/10';
                  prefix = '-';
                  textClass = inline ? 'text-red-800 dark:text-red-300' : 'text-red-300';
                  lineNoClass = inline ? 'text-red-600/50 dark:text-red-800' : 'text-red-800';
                  hlClass = inline ? 'bg-red-200/70 dark:bg-red-500/30 rounded-sm' : 'bg-red-500/30 rounded-sm';
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
                      {line.spans
                        ? line.spans.map((span, si) => {
                            const isHL = span.type === line.type; // del-in-del or add-in-add
                            return (
                              <span key={si} className={isHL ? hlClass : ''}>
                                {span.text.replace(/\t/g, '\u3000\u3000')}
                              </span>
                            );
                          })
                        : line.content.replace(/\t/g, '\u3000\u3000')
                      }
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
