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
    <div className="mt-2 first:mt-0">
      {/* 输出介绍 */}
      {intro && (
        <div className="text-[14px] mb-3 leading-[1.7]">
          {renderIntro()}
        </div>
      )}

      {/* 内容区域 - 直接显示，无容器 */}
      <div className="mt-2 overflow-hidden">
        {!content ? (
          <div className="flex items-center gap-2 text-[13px] text-gray-400 dark:text-slate-500">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>正在生成...</span>
          </div>
        ) : (
          <div className="text-[14px] leading-[1.8] [&_pre]:overflow-x-auto [&_pre]:rounded-lg [&_pre]:p-3 [&_pre]:bg-gray-100 [&_pre]:dark:bg-slate-800 [&_p]:mb-2.5 [&_p]:indent-8 [&_h1]:text-lg [&_h1]:font-bold [&_h1]:mb-3 [&_h2]:text-base [&_h2]:font-semibold [&_h2]:mb-2 [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:pl-5 [&_table]:w-full [&_table]:border-collapse [&_th]:border [&_th]:border-gray-300 [&_th]:dark:border-slate-600 [&_th]:px-3 [&_th]:py-2 [&_th]:bg-gray-100 [&_th]:dark:bg-slate-700 [&_td]:border [&_td]:border-gray-300 [&_td]:dark:border-slate-600 [&_td]:px-3 [&_td]:py-2">
            <MemoizedMarkdown content={content} />
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
