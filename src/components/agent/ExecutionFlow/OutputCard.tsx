/**
 * OutputCard - 最终输出卡片组件
 * 显示续写内容
 *
 * 优化：使用 React.memo + useMemo 减少流式输出时的重复渲染
 */

import { Loader2 } from 'lucide-react';
import React, { useState, useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { OutputFlowData } from '@/types/agent';
import { ContentPreviewModal } from './ContentPreviewModal';

interface OutputCardProps extends OutputFlowData {
  onCopy?: () => void;
  onApply?: () => void;
  onAddToKnowledge?: () => void;
}

/**
 * 优化的 Markdown 渲染组件
 * 使用 React.memo 避免父组件更新时的不必要重渲染
 */
const MemoizedMarkdown = React.memo(({ content }: { content: string }) => {
  // 缓存 remarkPlugins 数组，避免每次渲染都创建新数组
  const plugins = useMemo(() => [remarkGfm], []);

  return (
    <ReactMarkdown remarkPlugins={plugins}>
      {content}
    </ReactMarkdown>
  );
}, (prevProps, nextProps) => {
  // 自定义比较：只有内容变化时才重新渲染
  return prevProps.content === nextProps.content;
});

MemoizedMarkdown.displayName = 'MemoizedMarkdown';

function OutputCardInner({
  intro,
  introHighlight,
  title,
  content,
  isApplicable,
  onCopy,
  onApply,
  onAddToKnowledge
}: OutputCardProps) {
  const [previewOpen, setPreviewOpen] = useState(false);

  const toNumber = (value: string) => {
    const cleaned = value.trim();
    if (!cleaned) return null;
    if (/^\d+$/.test(cleaned)) return parseInt(cleaned, 10);
    const map: Record<string, number> = {
      '零': 0,
      '一': 1,
      '二': 2,
      '两': 2,
      '三': 3,
      '四': 4,
      '五': 5,
      '六': 6,
      '七': 7,
      '八': 8,
      '九': 9,
      '十': 10
    };
    if (cleaned === '十') return 10;
    if (cleaned.includes('十')) {
      const parts = cleaned.split('十');
      const tens = parts[0] ? (map[parts[0]] ?? 0) : 1;
      const ones = parts[1] ? (map[parts[1]] ?? 0) : 0;
      return tens * 10 + ones;
    }
    const single = map[cleaned];
    if (single === undefined) return null;
    return single;
  };

  // Normalize common numbered prefixes to Markdown ordered lists.
  const isYearish = (value: string) => {
    const trimmed = value.trim();
    if (!/^(19|20)\d{2}$/.test(trimmed)) return false;
    const year = parseInt(trimmed, 10);
    if (year < 1900 || year > 2100) return false;
    return true;
  };

  const isNoticeLine = (text: string) => {
    if (!text) return false;
    const haystack = text.trim();
    return /(公告|编号|版本|通知|更新|修订|说明|通告|第[一二三四五六七八九十]+号)/.test(haystack);
  };

  const shouldPreserveIndent = (trimmed: string) => {
    if (!trimmed) return false;
    if (/^#{1,6}\s/.test(trimmed)) return true; // headings
    if (/^>/.test(trimmed)) return true; // blockquote
    if (/^[-*+]\s/.test(trimmed)) return true; // unordered list
    if (/^\d+[.)]\s/.test(trimmed)) return true; // ordered list
    if (/^\|/.test(trimmed)) return true; // tables
    if (/^(\*{3,}|-{3,}|_{3,})$/.test(trimmed)) return true; // hr
    return false;
  };

  const stripLeadingIndent = (line: string) => {
    if (!line) return line;
    const trimmed = line.trimStart();
    if (shouldPreserveIndent(trimmed)) return line;
    return line.replace(/^[\s\u00a0\u2000-\u200b\u202f\u205f\u3000\uFEFF]+/, '');
  };

  const fix = (line: string) => {
    const bracketed = line.match(/^(\s*)[（(]\s*([0-9]+)\s*[）)]\s*(.+)$/);
    if (bracketed) {
      if (isYearish(bracketed[2]) || isNoticeLine(bracketed[3])) return line;
      return `${bracketed[1]}${bracketed[2]}. ${bracketed[3]}`;
    }

    const numbered = line.match(/^(\s*)([0-9]+|[一二三四五六七八九十两]+)\s*[、\.．\)\]）:：]\s*(.+)$/);
    if (!numbered) return line;
    const value = toNumber(numbered[2]);
    if (value === null) return line;
    if (isYearish(String(value)) || isNoticeLine(numbered[3])) return line;
    if (/^\s*[0-9]+\s*[\.．]\s*[0-9]/.test(line)) return line;
    return `${numbered[1]}${value}. ${numbered[3]}`;
  };

  const normalize = (value: string) => {
    const lines = value.split(/\r?\n/);
    const result = lines.reduce(
      (state, line) => {
        const trimmed = line.trim();
        const isFence = trimmed.startsWith('```');
        if (isFence) {
          return { inCode: !state.inCode, lines: [...state.lines, line] };
        }
        if (state.inCode) {
          return { inCode: true, lines: [...state.lines, line] };
        }
        const fixed = fix(line);
        return { inCode: false, lines: [...state.lines, stripLeadingIndent(fixed)] };
      },
      { inCode: false, lines: [] as string[] }
    );
    return result.lines.join('\n');
  };

  // 渲染介绍文字，支持高亮
  const renderIntro = () => {
    if (!intro) return null;
    if (!introHighlight) {
      return <span>{intro}</span>;
    }
    // 将 {highlight} 替换为加粗的高亮文字
    const parts = intro.split('{highlight}');
    if (parts.length === 1) {
      return <span>{intro}</span>;
    }
    return (
      <>
        {parts[0]}
        <strong className="text-gray-900 dark:text-white">{introHighlight}</strong>
        {parts[1]}
      </>
    );
  };

  return (
    <div className="mt-2">
      {/* 输出介绍 */}
      {intro && (
        <div className="text-[14px] text-gray-600 dark:text-[#ccc] mb-3 leading-[1.7]">
          {renderIntro()}
        </div>
      )}

      {/* 内容区域 - 直接显示，无容器 */}
      <div className="mt-2">
        {!content ? (
          <div className="flex items-center gap-2 text-[13px] text-gray-400 dark:text-slate-500">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>正在生成...</span>
          </div>
        ) : (
          <div className="text-[14px] text-gray-600 dark:text-slate-300 leading-[1.8] [&_p]:mb-2.5 [&_p]:indent-0 [&_h1]:text-lg [&_h1]:font-bold [&_h1]:mb-3 [&_h2]:text-base [&_h2]:font-semibold [&_h2]:mb-2 [&_h3]:text-[15px] [&_h3]:font-medium [&_h3]:mb-2 [&_h4]:text-[14px] [&_h4]:font-medium [&_h4]:mb-2 [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:pl-5 [&_table]:w-full [&_table]:border-collapse [&_table]:my-3 [&_th]:border [&_th]:border-gray-300 [&_th]:dark:border-slate-600 [&_th]:px-3 [&_th]:py-2 [&_th]:bg-gray-100 [&_th]:dark:bg-slate-700 [&_td]:border [&_td]:border-gray-300 [&_td]:dark:border-slate-600 [&_td]:px-3 [&_td]:py-2">
            <MemoizedMarkdown content={normalize(content)} />
          </div>
        )}
      </div>

      {/* 预览弹窗 */}
      <ContentPreviewModal
        isOpen={previewOpen}
        onClose={() => setPreviewOpen(false)}
        title={title}
        content={content}
        onAddToKnowledge={onAddToKnowledge}
      />
    </div>
  );
}

/**
 * 导出的 OutputCard 组件
 * 使用 React.memo 包裹，只有 props 变化时才重新渲染
 */
export const OutputCard = React.memo(OutputCardInner, (prevProps, nextProps) => {
  // 优化比较：只比较关键 props
  return (
    prevProps.content === nextProps.content &&
    prevProps.intro === nextProps.intro &&
    prevProps.introHighlight === nextProps.introHighlight &&
    prevProps.title === nextProps.title
  );
});

OutputCard.displayName = 'OutputCard';
