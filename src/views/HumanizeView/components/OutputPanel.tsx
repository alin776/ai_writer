// src/views/HumanizeView/components/OutputPanel.tsx

import React, { useRef, useEffect } from 'react';
import Button from '@/components/common/Button';
import { Check, X, Copy, RotateCcw, Sparkles } from 'lucide-react';

interface OutputPanelProps {
  outputText: string;
  isProcessing: boolean;
  currentStage: string;
  improvement: number | null;
  processingTime: number | null;
  tokensUsed: number | null;
  sessionId: string | null;
  onFeedback: (accepted: boolean) => void;
  onApplyToInput: () => void;
}

export const OutputPanel: React.FC<OutputPanelProps> = ({
  outputText,
  isProcessing,
  currentStage,
  improvement,
  processingTime,
  tokensUsed,
  sessionId,
  onFeedback,
  onApplyToInput,
}) => {
  const outputRef = useRef<HTMLDivElement>(null);

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
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const hasResult = outputText && currentStage === 'done';

  return (
    <div className="h-full flex flex-col bg-white rounded-lg border border-gray-200 shadow-sm">
      {/* 标题栏 */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
        <h3 className="text-sm font-semibold text-gray-900">改写结果</h3>
        {outputText && (
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="p-1.5 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded transition-colors"
              title="复制"
            >
              <Copy className="w-4 h-4" />
            </button>
            <button
              onClick={onApplyToInput}
              className="p-1.5 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded transition-colors"
              title="应用到输入区"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>

      {/* 输出区域 */}
      <div className="flex-1 p-4 overflow-hidden flex flex-col">
        {outputText ? (
          <div
            ref={outputRef}
            className="flex-1 overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap bg-gray-50 rounded-md p-3 border border-gray-200"
          >
            {outputText}
            {isProcessing && currentStage === 'rewriting' && (
              <span className="inline-block w-0.5 h-4 bg-blue-600 animate-pulse ml-0.5" />
            )}
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <Sparkles className="w-12 h-12 mx-auto mb-3 opacity-30" />
              <p className="text-sm">改写结果将在这里显示</p>
            </div>
          </div>
        )}
      </div>

      {/* 改进结果 */}
      {hasResult && improvement !== null && (
        <div className="px-4 py-3 border-t border-gray-200 bg-green-50">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-green-600 rounded-full flex items-center justify-center">
                <Check className="w-3.5 h-3.5 text-white" />
              </div>
              <span className="text-sm font-medium text-green-700">改写完成</span>
            </div>
            {processingTime && (
              <span className="text-xs text-green-600 font-mono">
                {processingTime.toFixed(1)}s
              </span>
            )}
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span className="text-green-600">改进幅度:</span>
              <span className="ml-1 font-semibold text-green-700">
                {Math.abs(improvement).toFixed(0)}分
              </span>
            </div>
            {tokensUsed && (
              <div>
                <span className="text-green-600">Token消耗:</span>
                <span className="ml-1 font-semibold text-green-700 font-mono">
                  {tokensUsed.toLocaleString()}
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* 反馈按钮 */}
      {hasResult && sessionId && (
        <div className="px-4 py-3 border-t border-gray-200">
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
          <p className="text-xs text-gray-500 text-center mt-2">
            您的反馈将帮助我们改进算法
          </p>
        </div>
      )}
    </div>
  );
};
