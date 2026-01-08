/**
 * OutputCard - 最终输出卡片组件
 * 显示续写内容，带更多操作（预览/复制/下载）/应用按钮
 */

import { MoreHorizontal, ChevronDown, ChevronUp, Loader2, Eye, Copy, Download } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { OutputFlowData } from '@/types/agent';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSub,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
} from '@/components/ui/dropdown-menu';
import { ContentPreviewModal } from './ContentPreviewModal';

interface OutputCardProps extends OutputFlowData {
  onCopy?: () => void;
  onApply?: () => void;
  onAddToKnowledge?: () => void;
}

// 文件格式配置
const FILE_FORMATS = [
  { key: 'txt', label: 'TXT', color: '#64748b' },
  { key: 'md', label: 'Markdown', color: '#3b82f6' },
  { key: 'pdf', label: 'PDF', color: '#ef4444' },
  { key: 'docx', label: 'DOCX', color: '#2563eb' },
] as const;

type FileFormat = typeof FILE_FORMATS[number]['key'];

export function OutputCard({
  intro,
  introHighlight,
  title,
  content,
  isApplicable,
  onCopy,
  onApply,
  onAddToKnowledge
}: OutputCardProps) {
  const [expanded, setExpanded] = useState(true);  // 默认展开
  const [previewOpen, setPreviewOpen] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);

  // 内容变化时自动滚动到底部
  useEffect(() => {
    if (contentRef.current) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }
  }, [content]);

  // 复制内容
  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    onCopy?.();
  };

  // 下载内容
  const handleDownload = (format: FileFormat) => {
    const formatConfig: Record<FileFormat, { ext: string; mime: string }> = {
      txt: { ext: '.txt', mime: 'text/plain' },
      md: { ext: '.md', mime: 'text/markdown' },
      pdf: { ext: '.pdf', mime: 'application/pdf' },
      docx: { ext: '.docx', mime: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' },
    };

    const config = formatConfig[format];

    // PDF 和 DOCX 需要后端支持
    if (format === 'pdf' || format === 'docx') {
      // TODO: 调用后端 API 进行格式转换
      console.log(`${format.toUpperCase()} 格式需要后端支持`);
      return;
    }

    const blob = new Blob([content], { type: config.mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title}${config.ext}`;
    a.click();
    URL.revokeObjectURL(url);
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
      <div className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[10px] mt-4">
        {/* 标题栏 */}
        <div className="group flex items-center justify-between px-3 py-1 border-b border-gray-200 dark:border-slate-700">
          <span className="text-[13px] font-medium text-gray-900 dark:text-white">{title}</span>
          <div className="flex gap-1.5">
            {/* 展开/收缩按钮 */}
            <button
              onClick={() => setExpanded(!expanded)}
              className="p-1.5 text-gray-400 dark:text-slate-500 rounded hover:bg-gray-100 dark:hover:bg-slate-700 hover:text-gray-600 dark:hover:text-slate-300 transition-colors"
              title={expanded ? '收缩' : '展开'}
            >
              {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>

            {/* 更多按钮 - 下拉菜单 */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button
                  className="p-1.5 text-gray-400 dark:text-slate-500 rounded hover:bg-gray-100 dark:hover:bg-slate-700 hover:text-gray-600 dark:hover:text-slate-300 transition-colors"
                  title="更多操作"
                >
                  <MoreHorizontal size={14} />
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent
                align="end"
                className="min-w-[140px] bg-white dark:bg-slate-800 border-gray-200 dark:border-slate-700 rounded-xl p-1.5"
              >
                {/* 预览 */}
                <DropdownMenuItem
                  onClick={() => setPreviewOpen(true)}
                  className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-lg text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-slate-700 cursor-pointer"
                >
                  <Eye size={16} className="text-gray-500 dark:text-gray-400" />
                  预览
                </DropdownMenuItem>

                {/* 复制 */}
                <DropdownMenuItem
                  onClick={handleCopy}
                  className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-lg text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-slate-700 cursor-pointer"
                >
                  <Copy size={16} className="text-gray-500 dark:text-gray-400" />
                  复制
                </DropdownMenuItem>

                {/* 下载 - 子菜单 */}
                <DropdownMenuSub>
                  <DropdownMenuSubTrigger className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-lg text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-slate-700 cursor-pointer data-[state=open]:bg-gray-100 dark:data-[state=open]:bg-slate-700">
                    <Download size={16} className="text-gray-500 dark:text-gray-400" />
                    下载
                  </DropdownMenuSubTrigger>
                  <DropdownMenuSubContent className="min-w-[130px] bg-white dark:bg-slate-800 border-gray-200 dark:border-slate-700 rounded-xl p-1.5">
                    {FILE_FORMATS.map((format) => (
                      <DropdownMenuItem
                        key={format.key}
                        onClick={() => handleDownload(format.key)}
                        className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-lg text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-slate-700 cursor-pointer"
                      >
                        <span
                          className="w-[18px] h-[18px] flex items-center justify-center text-[10px] font-semibold text-white rounded"
                          style={{ backgroundColor: format.color }}
                        >
                          {format.label[0]}
                        </span>
                        {format.label}
                      </DropdownMenuItem>
                    ))}
                  </DropdownMenuSubContent>
                </DropdownMenuSub>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* 应用到章节按钮 */}
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
