/**
 * 智能排版对话框组件
 */
import React, { useState, useCallback } from 'react';
import { Editor } from '@tiptap/react';
import {
  X,
  Wand2,
  AlignLeft,
  Space,
  RemoveFormatting,
  Check,
  AlertCircle,
} from 'lucide-react';

interface SmartFormatDialogProps {
  editor: Editor;
  isOpen: boolean;
  onClose: () => void;
}

interface FormatOption {
  id: string;
  label: string;
  description: string;
  icon: React.ReactNode;
  enabled: boolean;
}

const SmartFormatDialog: React.FC<SmartFormatDialogProps> = ({
  editor,
  isOpen,
  onClose,
}) => {
  const [options, setOptions] = useState<FormatOption[]>([
    {
      id: 'removeExtraSpaces',
      label: '清理多余空格',
      description: '删除段落中多余的连续空格，保留单个空格',
      icon: <Space className="w-4 h-4" />,
      enabled: true,
    },
    {
      id: 'removeLeadingSpaces',
      label: '清理段首空格',
      description: '删除段落开头的空格（首行缩进由样式控制）',
      icon: <AlignLeft className="w-4 h-4" />,
      enabled: true,
    },
    {
      id: 'removeExtraLines',
      label: '删除空行',
      description: '删除文档中所有的空行',
      icon: <RemoveFormatting className="w-4 h-4" />,
      enabled: true,
    },
    {
      id: 'trimParagraphs',
      label: '清理段尾空格',
      description: '删除段落末尾的多余空格',
      icon: <AlignLeft className="w-4 h-4" />,
      enabled: true,
    },
  ]);

  const [result, setResult] = useState<{
    show: boolean;
    changes: number;
    details: string[];
  }>({ show: false, changes: 0, details: [] });

  const [isProcessing, setIsProcessing] = useState(false);

  const toggleOption = (id: string) => {
    setOptions(prev =>
      prev.map(opt =>
        opt.id === id ? { ...opt, enabled: !opt.enabled } : opt
      )
    );
  };

  const applyFormat = useCallback(() => {
    setIsProcessing(true);
    setResult({ show: false, changes: 0, details: [] });

    const enabledOptions = options.filter(opt => opt.enabled).map(opt => opt.id);
    if (enabledOptions.length === 0) {
      setIsProcessing(false);
      return;
    }

    // 获取当前 HTML 内容
    let html = editor.getHTML();
    const originalHtml = html;
    const details: string[] = [];
    let totalChanges = 0;

    // 解析 HTML
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const paragraphs = doc.body.querySelectorAll('p');

    // 1. 清理多余空格
    if (enabledOptions.includes('removeExtraSpaces')) {
      let spaceChanges = 0;
      paragraphs.forEach(p => {
        const original = p.innerHTML;
        // 将多个连续空格替换为单个空格（保留 &nbsp;）
        p.innerHTML = p.innerHTML
          .replace(/  +/g, ' ')  // 多个普通空格 -> 单个空格
          .replace(/(&nbsp;)+/g, '&nbsp;')  // 多个 &nbsp; -> 单个
          .replace(/(&nbsp; )+/g, '&nbsp;')  // &nbsp; 和空格的组合
          .replace(/( &nbsp;)+/g, '&nbsp;');
        if (p.innerHTML !== original) spaceChanges++;
      });
      if (spaceChanges > 0) {
        details.push(`清理了 ${spaceChanges} 处多余空格`);
        totalChanges += spaceChanges;
      }
    }

    // 2. 清理段首空格
    if (enabledOptions.includes('removeLeadingSpaces')) {
      let leadingChanges = 0;
      paragraphs.forEach(p => {
        const original = p.innerHTML;
        // 移除段落开头的空格和 &nbsp;
        p.innerHTML = p.innerHTML
          .replace(/^(&nbsp;|[\s\u3000])+/, '')  // 移除开头的空格、全角空格和 &nbsp;
          .replace(/^(<[^>]+>)(&nbsp;|[\s\u3000])+/g, '$1');  // 处理标签后的空格
        if (p.innerHTML !== original) leadingChanges++;
      });
      if (leadingChanges > 0) {
        details.push(`清理了 ${leadingChanges} 处段首空格`);
        totalChanges += leadingChanges;
      }
    }

    // 3. 清理段尾空格
    if (enabledOptions.includes('trimParagraphs')) {
      let trailingChanges = 0;
      paragraphs.forEach(p => {
        const original = p.innerHTML;
        // 移除段落末尾的空格和 &nbsp;
        p.innerHTML = p.innerHTML
          .replace(/(&nbsp;|[\s\u3000])+$/, '')  // 移除末尾的空格
          .replace(/(&nbsp;|[\s\u3000])+(<\/[^>]+>)$/g, '$2');  // 处理标签前的空格
        if (p.innerHTML !== original) trailingChanges++;
      });
      if (trailingChanges > 0) {
        details.push(`清理了 ${trailingChanges} 处段尾空格`);
        totalChanges += trailingChanges;
      }
    }

    // 4. 删除空行
    if (enabledOptions.includes('removeExtraLines')) {
      // 获取处理后的 HTML
      html = doc.body.innerHTML;

      // 统计并删除所有空段落
      const emptyParagraphPattern = /<p><\/p>|<p>\s*<\/p>|<p>&nbsp;<\/p>|<p><br\s*\/?><\/p>/gi;
      const emptyMatches = html.match(emptyParagraphPattern);

      if (emptyMatches && emptyMatches.length > 0) {
        // 直接删除所有空段落
        const lineChanges = emptyMatches.length;
        html = html.replace(emptyParagraphPattern, '');

        if (lineChanges > 0) {
          details.push(`删除了 ${lineChanges} 处空行`);
          totalChanges += lineChanges;
        }
      }
    } else {
      html = doc.body.innerHTML;
    }

    // 如果有变化，更新编辑器内容
    if (html !== originalHtml && totalChanges > 0) {
      editor.commands.setContent(html);
    }

    setResult({
      show: true,
      changes: totalChanges,
      details,
    });
    setIsProcessing(false);
  }, [editor, options]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* 背景遮罩 */}
      <div
        className="absolute inset-0 bg-black/20 dark:bg-black/40"
        onClick={onClose}
      />

      {/* 对话框 */}
      <div className="relative bg-white dark:bg-slate-800 rounded-xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
        {/* 标题栏 */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-100 dark:border-slate-700">
          <h3 className="text-sm font-semibold text-zinc-800 dark:text-slate-200 flex items-center gap-2">
            <Wand2 className="w-4 h-4 text-blue-500" />
            智能排版
          </h3>
          <button
            onClick={onClose}
            className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-slate-700 transition-colors"
          >
            <X className="w-4 h-4 text-zinc-500 dark:text-slate-400" />
          </button>
        </div>

        {/* 内容区域 */}
        <div className="p-4 space-y-4">
          {/* 说明 */}
          <div className="flex items-start gap-2 px-3 py-2 bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800 rounded-lg">
            <AlertCircle className="w-4 h-4 text-blue-500 dark:text-blue-400 mt-0.5 shrink-0" />
            <p className="text-xs text-blue-700 dark:text-blue-300">
              智能排版可以自动清理文本中的格式问题，让文章更加整洁规范。首行缩进由编辑器样式统一控制。
            </p>
          </div>

          {/* 选项列表 */}
          <div className="space-y-2">
            {options.map(option => (
              <label
                key={option.id}
                className={`flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-all ${
                  option.enabled
                    ? 'border-blue-200 dark:border-blue-700 bg-blue-50/50 dark:bg-blue-900/20'
                    : 'border-zinc-200 dark:border-slate-600 hover:border-zinc-300 dark:hover:border-slate-500'
                }`}
              >
                <input
                  type="checkbox"
                  checked={option.enabled}
                  onChange={() => toggleOption(option.id)}
                  className="w-4 h-4 mt-0.5 rounded border-zinc-300 dark:border-slate-600 text-blue-500 focus:ring-blue-500/50"
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-zinc-500 dark:text-slate-400">
                      {option.icon}
                    </span>
                    <span className="text-sm font-medium text-zinc-800 dark:text-slate-200">
                      {option.label}
                    </span>
                  </div>
                  <p className="text-xs text-zinc-500 dark:text-slate-400 mt-1">
                    {option.description}
                  </p>
                </div>
              </label>
            ))}
          </div>

          {/* 结果提示 */}
          {result.show && (
            <div
              className={`flex items-start gap-2 px-3 py-2 rounded-xl border ${
                result.changes > 0
                  ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
                  : 'bg-zinc-50 dark:bg-slate-700/50 border-zinc-200 dark:border-slate-600'
              }`}
            >
              {result.changes > 0 ? (
                <Check className="w-4 h-4 text-green-600 dark:text-green-400 mt-0.5 shrink-0" />
              ) : (
                <AlertCircle className="w-4 h-4 text-zinc-500 dark:text-slate-400 mt-0.5 shrink-0" />
              )}
              <div className="text-xs">
                {result.changes > 0 ? (
                  <>
                    <p className="font-medium text-green-700 dark:text-green-400">
                      排版完成，共处理 {result.changes} 处
                    </p>
                    <ul className="mt-1 space-y-0.5 text-green-600 dark:text-green-400">
                      {result.details.map((detail, index) => (
                        <li key={index}>• {detail}</li>
                      ))}
                    </ul>
                  </>
                ) : (
                  <p className="text-zinc-600 dark:text-slate-400">
                    文档格式良好，无需调整
                  </p>
                )}
              </div>
            </div>
          )}
        </div>

        {/* 底部操作栏 */}
        <div className="flex items-center justify-end gap-2 px-4 py-3 border-t border-zinc-100 dark:border-slate-700 bg-zinc-50 dark:bg-slate-800/50">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm text-zinc-600 dark:text-slate-400 hover:bg-zinc-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
          >
            关闭
          </button>
          <button
            onClick={applyFormat}
            disabled={isProcessing || options.every(opt => !opt.enabled)}
            className="px-4 py-2 text-sm bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isProcessing ? (
              <>
                <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                处理中...
              </>
            ) : (
              <>
                <Wand2 className="w-4 h-4" />
                应用排版
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SmartFormatDialog;
