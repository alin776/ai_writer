/**
 * OutputCard - 最终输出卡片组件
 * 显示续写内容，带复制/应用按钮
 */

import { Copy, Check } from 'lucide-react';
import { useState } from 'react';
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
  onCopy,
  onApply
}: OutputCardProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    // 复制纯文本内容
    const textContent = content.replace(/<[^>]*>/g, '');
    navigator.clipboard.writeText(textContent);
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
        <div className="flex items-center justify-between px-3.5 py-2.5 border-b border-gray-200 dark:border-slate-700">
          <span className="text-[13px] font-medium text-gray-900 dark:text-white">{title}</span>
          <div className="flex gap-2">
            <button
              onClick={handleCopy}
              className="text-[11px] px-2.5 py-1 bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-slate-300 rounded hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors flex items-center gap-1"
            >
              {copied ? <Check size={12} /> : <Copy size={12} />}
              {copied ? '已复制' : '复制'}
            </button>
            {onApply && (
              <button
                onClick={onApply}
                className="text-[11px] px-2.5 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
              >
                应用到章节
              </button>
            )}
          </div>
        </div>

        {/* 内容区域 */}
        <div className="px-4 py-4 max-h-[350px] overflow-y-auto">
          <div
            className="text-[14px] text-gray-600 dark:text-[#bbb] leading-[1.8] [&_p]:mb-2.5 [&_p]:indent-8 [&_.highlight]:text-blue-500 dark:[&_.highlight]:text-[#5c9eff] [&_.highlight]:font-medium"
            dangerouslySetInnerHTML={{ __html: content }}
          />
        </div>
      </div>
    </div>
  );
}
