/**
 * ContentPreviewModal - 内容预览弹窗组件
 * 参考 Manus UI 风格，支持 Markdown 渲染、下载、复制等功能
 * 支持浅色/暗色模式
 */

import { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { X, Download, Copy, Check, BookPlus, Maximize2, Minimize2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface ContentPreviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  content: string;
  onAddToKnowledge?: () => void;
}

// 文件格式配置
const FILE_FORMATS = [
  { key: 'txt', label: 'TXT', color: '#64748b' },
  { key: 'md', label: 'Markdown', color: '#3b82f6' },
] as const;

type FileFormat = typeof FILE_FORMATS[number]['key'];

export function ContentPreviewModal({
  isOpen,
  onClose,
  title,
  content,
  onAddToKnowledge,
}: ContentPreviewModalProps) {
  const [copied, setCopied] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  // ESC 关闭
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleEsc);
    return () => document.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  // 锁定 body 滚动
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  // 复制内容
  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // 下载内容
  const handleDownload = async (format: FileFormat) => {
    const formatConfig: Record<FileFormat, { ext: string; mime: string }> = {
      txt: { ext: '.txt', mime: 'text/plain' },
      md: { ext: '.md', mime: 'text/markdown' },
    };

    const config = formatConfig[format];

    const blob = new Blob([content], { type: config.mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title}${config.ext}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (!isOpen) return null;

  const modalContent = (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 dark:bg-black/60"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div
        className={`
          bg-white dark:bg-slate-800 flex flex-col shadow-2xl
          ${isFullscreen
            ? 'fixed inset-0 rounded-none'
            : 'w-full max-w-[960px] max-h-[90vh] rounded-xl mx-4'
          }
        `}
      >
        {/* 顶部工具栏 */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-gray-200 dark:border-slate-700 flex-shrink-0">
          {/* 左侧：文档图标 + 标题 */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-blue-500 rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
              </svg>
            </div>
            <div>
              <h2 className="text-[15px] font-semibold text-gray-900 dark:text-slate-100">{title}</h2>
              <span className="text-xs text-gray-500 dark:text-slate-500">预览模式</span>
            </div>
          </div>

          {/* 右侧：操作按钮 */}
          <div className="flex items-center gap-1">
            {/* 下载 - 下拉菜单 */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button
                  className="w-9 h-9 flex items-center justify-center rounded-lg text-gray-500 dark:text-slate-500 hover:bg-gray-100 dark:hover:bg-slate-700 hover:text-gray-700 dark:hover:text-slate-300 transition-colors"
                  title="下载"
                >
                  <Download size={18} />
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="min-w-[130px] bg-white dark:bg-slate-800 border-gray-200 dark:border-slate-700 rounded-xl p-1.5">
                {FILE_FORMATS.map((format) => (
                  <DropdownMenuItem
                    key={format.key}
                    onClick={() => handleDownload(format.key)}
                    className="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-gray-700 dark:text-slate-200 hover:bg-gray-100 dark:hover:bg-slate-700 cursor-pointer"
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
              </DropdownMenuContent>
            </DropdownMenu>

            {/* 复制 */}
            <button
              onClick={handleCopy}
              className="w-9 h-9 flex items-center justify-center rounded-lg text-gray-500 dark:text-slate-500 hover:bg-gray-100 dark:hover:bg-slate-700 hover:text-gray-700 dark:hover:text-slate-300 transition-colors"
              title={copied ? '已复制' : '复制'}
            >
              {copied ? <Check size={18} /> : <Copy size={18} />}
            </button>

            {/* 添加到知识库 */}
            {onAddToKnowledge && (
              <button
                onClick={onAddToKnowledge}
                className="w-9 h-9 flex items-center justify-center rounded-lg text-gray-500 dark:text-slate-500 hover:bg-gray-100 dark:hover:bg-slate-700 hover:text-gray-700 dark:hover:text-slate-300 transition-colors"
                title="添加到知识库"
              >
                <BookPlus size={18} />
              </button>
            )}

            {/* 分隔线 */}
            <div className="w-px h-6 bg-gray-200 dark:bg-slate-700 mx-2" />

            {/* 全屏 */}
            <button
              onClick={() => setIsFullscreen(!isFullscreen)}
              className="w-9 h-9 flex items-center justify-center rounded-lg text-gray-500 dark:text-slate-500 hover:bg-gray-100 dark:hover:bg-slate-700 hover:text-gray-700 dark:hover:text-slate-300 transition-colors"
              title={isFullscreen ? '退出全屏' : '全屏'}
            >
              {isFullscreen ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
            </button>

            {/* 关闭 */}
            <button
              onClick={onClose}
              className="w-9 h-9 flex items-center justify-center rounded-lg text-gray-500 dark:text-slate-500 hover:bg-gray-100 dark:hover:bg-slate-700 hover:text-gray-700 dark:hover:text-slate-300 transition-colors"
              title="关闭"
            >
              <X size={18} />
            </button>
          </div>
        </div>

        {/* 内容区域 */}
        <div className="flex-1 overflow-y-auto py-8 custom-scrollbar-preview">
          <div className="max-w-[800px] mx-auto px-12">
            <div className="prose-preview">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {content}
              </ReactMarkdown>
            </div>
          </div>
        </div>
      </div>

      {/* 自定义滚动条和 Markdown 样式 */}
      <style>{`
        .custom-scrollbar-preview::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar-preview::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar-preview::-webkit-scrollbar-thumb {
          background: #d1d5db;
          border-radius: 3px;
        }
        .custom-scrollbar-preview::-webkit-scrollbar-thumb:hover {
          background: #9ca3af;
        }
        .dark .custom-scrollbar-preview::-webkit-scrollbar-thumb {
          background: #475569;
        }
        .dark .custom-scrollbar-preview::-webkit-scrollbar-thumb:hover {
          background: #64748b;
        }

        /* Markdown 样式 - 浅色模式 */
        .prose-preview {
          font-size: 15px;
          line-height: 1.8;
          color: #374151;
        }
        .prose-preview h1 {
          font-size: 28px;
          font-weight: 700;
          color: #111827;
          margin-bottom: 24px;
        }
        .prose-preview h2 {
          font-size: 20px;
          font-weight: 600;
          color: #1f2937;
          margin: 28px 0 16px;
        }
        .prose-preview h3 {
          font-size: 17px;
          font-weight: 600;
          color: #1f2937;
          margin: 24px 0 12px;
        }
        .prose-preview p {
          margin-bottom: 16px;
        }
        .prose-preview ul, .prose-preview ol {
          margin: 16px 0;
          padding-left: 24px;
        }
        .prose-preview li {
          margin-bottom: 8px;
        }
        .prose-preview strong {
          color: #111827;
          font-weight: 600;
        }
        .prose-preview code {
          background: #f3f4f6;
          padding: 2px 6px;
          border-radius: 4px;
          font-size: 13px;
        }
        .prose-preview pre {
          background: #f9fafb;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          padding: 16px;
          overflow-x: auto;
          margin: 16px 0;
        }
        .prose-preview pre code {
          background: transparent;
          padding: 0;
        }
        .prose-preview blockquote {
          border-left: 3px solid #3b82f6;
          padding-left: 16px;
          margin: 16px 0;
          color: #6b7280;
        }
        .prose-preview table {
          width: 100%;
          border-collapse: collapse;
          margin: 16px 0;
        }
        .prose-preview th, .prose-preview td {
          border: 1px solid #e5e7eb;
          padding: 8px 12px;
          text-align: left;
        }
        .prose-preview th {
          background: #f9fafb;
          font-weight: 600;
        }

        /* Markdown 样式 - 暗色模式 */
        .dark .prose-preview {
          color: #cbd5e1;
        }
        .dark .prose-preview h1 {
          color: #f1f5f9;
        }
        .dark .prose-preview h2 {
          color: #e2e8f0;
        }
        .dark .prose-preview h3 {
          color: #e2e8f0;
        }
        .dark .prose-preview strong {
          color: #f1f5f9;
        }
        .dark .prose-preview code {
          background: #334155;
        }
        .dark .prose-preview pre {
          background: #1e293b;
          border-color: #334155;
        }
        .dark .prose-preview blockquote {
          color: #94a3b8;
        }
        .dark .prose-preview th, .dark .prose-preview td {
          border-color: #334155;
        }
        .dark .prose-preview th {
          background: #1e293b;
        }
      `}</style>
    </div>
  );

  return createPortal(modalContent, document.body);
}
