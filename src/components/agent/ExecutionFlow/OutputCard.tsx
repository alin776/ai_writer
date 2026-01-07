/**
 * OutputCard - 最终输出卡片组件
 * 显示续写内容，带复制/应用按钮
 */

import { Copy, Check, ChevronDown, ChevronUp, Loader2 } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { OutputFlowData } from '@/types/agent';

interface OutputCardProps extends OutputFlowData {
  onCopy?: () => void;
  onApply?: () => void;
}

export function OutputCard({
  intro,
  introHighlight,
  title,
  content,
  isApplicable,
  onCopy,
  onApply
}: OutputCardProps) {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);

  // 内容变化时自动滚动到底部
  useEffect(() => {
    if (contentRef.current) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }
  }, [content]);

  const handleCopy = () => {
    // 复制纯文本内容
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
    onCopy?.();
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

      {/* 内容卡片 */}
      <div className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[10px] mt-4 overflow-hidden">
        {/* 标题栏 */}
        <div className="group flex items-center justify-between px-3 py-1 border-b border-gray-200 dark:border-slate-700">
          <span className="text-[13px] font-medium text-gray-900 dark:text-white">{title}</span>
          <div className="flex gap-1.5">
            <button
              onClick={() => setExpanded(!expanded)}
              className="p-1.5 text-gray-400 dark:text-slate-500 rounded hover:bg-gray-100 dark:hover:bg-slate-700 hover:text-gray-600 dark:hover:text-slate-300 transition-colors"
              title={expanded ? '收缩' : '展开'}
            >
              {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>
            <button
              onClick={handleCopy}
              className="p-1.5 text-gray-400 dark:text-slate-500 rounded hover:bg-gray-100 dark:hover:bg-slate-700 hover:text-gray-600 dark:hover:text-slate-300 transition-colors"
              title={copied ? '已复制' : '复制'}
            >
              {copied ? <Check size={14} /> : <Copy size={14} />}
            </button>
            {isApplicable && onApply && (
              <button
                onClick={onApply}
                className="text-[11px] px-2.5 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
              >
                应用到章节
              </button>
            )}
          </div>
        </div>

        {/* 内容区域 - 使用固定高度避免影响外层滚动 */}
        <div
          ref={contentRef}
          className={`px-4 py-4 overflow-y-auto custom-scrollbar transition-all overscroll-contain ${expanded ? 'h-[350px]' : 'h-[100px]'}`}
        >
          {!content ? (
            <div className="flex items-center gap-2 text-[13px] text-gray-400 dark:text-slate-500">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>正在生成...</span>
            </div>
          ) : (
            <div className="text-[14px] text-gray-600 dark:text-[#bbb] leading-[1.8] [&_p]:mb-2.5 [&_p]:indent-8 [&_h1]:text-lg [&_h1]:font-bold [&_h1]:mb-3 [&_h2]:text-base [&_h2]:font-semibold [&_h2]:mb-2 [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:pl-5 [&_table]:w-full [&_table]:border-collapse [&_th]:border [&_th]:border-gray-300 [&_th]:dark:border-slate-600 [&_th]:px-3 [&_th]:py-2 [&_th]:bg-gray-100 [&_th]:dark:bg-slate-700 [&_td]:border [&_td]:border-gray-300 [&_td]:dark:border-slate-600 [&_td]:px-3 [&_td]:py-2">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {content}
              </ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
