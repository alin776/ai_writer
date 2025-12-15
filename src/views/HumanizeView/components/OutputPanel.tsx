// src/views/HumanizeView/components/OutputPanel.tsx

import React, { useRef, useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark, oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';
import Button from '@/components/common/Button';
import { Check, X, Copy, Sparkles, History } from 'lucide-react';
import type { HumanizeStage } from '@/types/humanize';

interface OutputPanelProps {
  outputText: string;
  isProcessing: boolean;
  currentStage: HumanizeStage;
  improvement: number | null;
  processingTime: number | null;
  tokensUsed: number | null;
  sessionId: string | null;
  skipped?: boolean;
  onFeedback: (accepted: boolean) => void;
  renderComplete?: boolean;
  isTyping?: boolean; // 打字机是否正在输出
  isHistoryCollapsed?: boolean;
  onExpandHistory?: () => void;
}

export const OutputPanel: React.FC<OutputPanelProps> = ({
  outputText,
  isProcessing,
  currentStage,
  improvement,
  processingTime,
  tokensUsed,
  sessionId,
  skipped,
  onFeedback,
  renderComplete,
  isTyping,
  isHistoryCollapsed,
  onExpandHistory,
}) => {
  const outputRef = useRef<HTMLDivElement>(null);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [copied, setCopied] = useState(false);

  // 监听深色模式变化
  useEffect(() => {
    const checkDarkMode = () => {
      setIsDarkMode(document.documentElement.classList.contains('dark'));
    };

    // 初始检查
    checkDarkMode();

    // 监听 class 变化
    const observer = new MutationObserver(checkDarkMode);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class'],
    });

    return () => observer.disconnect();
  }, []);

  // 自动滚动到底部
  useEffect(() => {
    if (outputRef.current && outputText) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [outputText]);

  // 复制到剪贴板
  const handleCopy = async () => {
    if (!outputText) return;
    try {
      await navigator.clipboard.writeText(outputText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000); // 2秒后恢复
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const hasResult = !!outputText && renderComplete && !skipped;

  return (
    <div className="h-full w-full flex flex-col bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden">
      {/* 标题栏 */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">改写结果</h3>
        <div className="flex items-center gap-2">
          {outputText && (
            <button
              onClick={handleCopy}
              className={`p-1.5 rounded transition-colors ${
                copied
                  ? 'text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/30'
                  : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
              title={copied ? '已复制' : '复制'}
            >
              {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
            </button>
          )}
          {isHistoryCollapsed && onExpandHistory && (
            <button
              onClick={onExpandHistory}
              className="inline-flex items-center gap-1 px-2 py-1 text-xs text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 border border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 rounded transition-colors"
              title="展开历史记录"
            >
              <History className="w-3.5 h-3.5" />
              <span>历史</span>
            </button>
          )}
        </div>
      </div>

      {/* 输出区域 */}
      <div className="flex-1 p-4 overflow-hidden flex flex-col">
        {outputText ? (
          <div
            ref={outputRef}
            className="flex-1 overflow-y-auto text-sm text-gray-700 dark:text-gray-300 leading-relaxed bg-gray-50 dark:bg-gray-700 rounded-md p-3 border border-gray-200 dark:border-gray-600"
          >
            {/* Markdown 渲染 */}
            <div className="prose prose-sm dark:prose-invert max-w-none prose-p:my-2 prose-headings:my-3 prose-ul:my-2 prose-ol:my-2 prose-li:my-0.5 prose-pre:my-2 prose-code:text-blue-600 dark:prose-code:text-blue-400 prose-code:bg-gray-100 dark:prose-code:bg-gray-800 prose-code:px-1 prose-code:py-0.5 prose-code:rounded prose-code:before:content-none prose-code:after:content-none">
              <ReactMarkdown
                components={{
                  // 代码块高亮 - 根据深浅色模式切换样式
                  code({ className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || '');
                    const isInline = !match;
                    return !isInline && match ? (
                      <SyntaxHighlighter
                        style={isDarkMode ? oneDark : oneLight}
                        language={match[1]}
                        PreTag="div"
                        customStyle={{
                          margin: '0.5rem 0',
                          borderRadius: '0.375rem',
                          fontSize: '0.8125rem',
                        }}
                      >
                        {String(children).replace(/\n$/, '')}
                      </SyntaxHighlighter>
                    ) : (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  },
                  // 段落 - 使用正常换行，避免过多空白
                  p({ children }) {
                    return <p className="whitespace-normal break-words">{children}</p>;
                  },
                }}
              >
                {outputText}
              </ReactMarkdown>
            </div>
            {/* 打字机光标 */}
            {(isTyping || (isProcessing && currentStage === 'rewriting')) && (
              <span className="inline-block w-0.5 h-4 bg-blue-600 dark:bg-blue-400 animate-pulse ml-0.5 align-middle" />
            )}
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-gray-400 dark:text-gray-500">
            <div className="text-center">
              <Sparkles className="w-12 h-12 mx-auto mb-3 opacity-30" />
              <p className="text-sm">改写结果将在这里显示</p>
            </div>
          </div>
        )}
      </div>

      {currentStage === 'done' && skipped && (
        <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-yellow-50 dark:bg-yellow-900/30 text-sm text-yellow-800 dark:text-yellow-300">
          文本AI特征较低，未执行改写，已返回原文。
        </div>
      )}

      {/* 改进结果 */}
      {hasResult && improvement !== null && (
        <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-green-50 dark:bg-green-900/30">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-green-600 dark:bg-green-500 rounded-full flex items-center justify-center">
                <Check className="w-3.5 h-3.5 text-white" />
              </div>
              <span className="text-sm font-medium text-green-700 dark:text-green-300">改写完成</span>
            </div>
            {processingTime && (
              <span className="text-xs text-green-600 dark:text-green-400 font-mono">
                {processingTime.toFixed(1)}s
              </span>
            )}
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span className="text-green-600 dark:text-green-400">改进幅度:</span>
              <span className="ml-1 font-semibold text-green-700 dark:text-green-300">
                {Math.abs(improvement).toFixed(0)}分
              </span>
            </div>
            {tokensUsed && (
              <div>
                <span className="text-green-600 dark:text-green-400">Token消耗:</span>
                <span className="ml-1 font-semibold text-green-700 dark:text-green-300 font-mono">
                  {tokensUsed.toLocaleString()}
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* 反馈按钮 */}
      {hasResult && sessionId && (
        <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700">
          <div className="flex gap-2">
            <Button
              onClick={() => onFeedback(true)}
              variant="primary"
              size="md"
              fullWidth
            >
              <Check className="w-4 h-4 mr-1.5" />
              接受结果
            </Button>
            <Button
              onClick={() => onFeedback(false)}
              variant="outline"
              size="md"
              fullWidth
            >
              <X className="w-4 h-4 mr-1.5" />
              拒绝
            </Button>
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center mt-2">
            您的反馈将帮助我们改进算法
          </p>
        </div>
      )}
    </div>
  );
};
