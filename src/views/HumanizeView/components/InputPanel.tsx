// src/views/HumanizeView/components/InputPanel.tsx

import React from 'react';
import Button from '@/components/common/Button';
import { Wand2, Loader2, AlertCircle } from 'lucide-react';
import type { HumanizeIntensity } from '@/types/humanize';

interface InputPanelProps {
  inputText: string;
  intensity: HumanizeIntensity;
  isProcessing: boolean;
  currentStage: string;
  detectionScore: number | null;
  error: string | null;
  onInputChange: (text: string) => void;
  onIntensityChange: (intensity: HumanizeIntensity) => void;
  onRewrite: () => void;
}

export const InputPanel: React.FC<InputPanelProps> = ({
  inputText,
  intensity,
  isProcessing,
  currentStage,
  detectionScore,
  error,
  onInputChange,
  onIntensityChange,
  onRewrite,
}) => {
  const inputLength = inputText.length;
  const maxLength = 50000;
  const isOverLimit = inputLength > maxLength;

  return (
    <div className="h-full flex flex-col bg-white rounded-lg border border-gray-200 shadow-sm min-h-[520px] max-h-[520px]">
      {/* 标题栏 */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
        <h3 className="text-sm font-semibold text-gray-900">原文输入</h3>
        <span className={`text-xs font-mono ${isOverLimit ? 'text-red-600' : 'text-gray-500'}`}>
          {inputLength.toLocaleString()} / {maxLength.toLocaleString()}
        </span>
      </div>

      {/* 文本输入区 */}
      <div className="flex-1 p-4 overflow-hidden flex flex-col">
        <textarea
          value={inputText}
          onChange={(e) => onInputChange(e.target.value)}
          placeholder="粘贴或输入需要去除AI痕迹的文本...&#10;&#10;支持最多50,000字符"
          className="flex-1 resize-none text-sm border border-gray-200 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={isProcessing}
        />
      </div>

      {/* 强度选择 */}
      <div className="px-4 py-3 border-t border-gray-200">
        <label className="block text-xs font-medium text-gray-700 mb-2">
          改写强度
        </label>
        <div className="grid grid-cols-3 gap-2">
          {(['light', 'medium', 'strong'] as HumanizeIntensity[]).map((level) => (
            <button
              key={level}
              onClick={() => onIntensityChange(level)}
              disabled={isProcessing}
              className={`px-3 py-2 rounded-md text-xs font-medium transition-all ${
                intensity === level
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
              } ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {level === 'light' && '轻度'}
              {level === 'medium' && '中度'}
              {level === 'strong' && '强度'}
              <span className="block text-xs opacity-75 mt-0.5">
                {level === 'light' && '~5%'}
                {level === 'medium' && '~20%'}
                {level === 'strong' && '~40%'}
              </span>
            </button>
          ))}
        </div>
        <p className="text-xs text-gray-500 mt-2">
          {intensity === 'light' && '仅去除明显AI套话，保持原文风格'}
          {intensity === 'medium' && '平衡自然度与内容保留，推荐使用'}
          {intensity === 'strong' && '深度重构句式，最大化自然度'}
        </p>
      </div>

      {/* 处理状态 */}
      {isProcessing && (
        <div className="px-4 py-3 border-t border-gray-200 bg-blue-50">
          <div className="flex items-center gap-2 text-sm text-blue-700">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>
              {currentStage === 'detecting' && '正在检测AI痕迹...'}
              {currentStage === 'rewriting' && '正在智能改写...'}
              {currentStage === 'verifying' && '正在验证效果...'}
            </span>
          </div>
          {detectionScore !== null && (
            <div className="mt-2 text-xs text-blue-600">
              AI特征分数: <span className="font-mono font-semibold">{detectionScore}/100</span>
            </div>
          )}
        </div>
      )}

      {/* 错误提示 */}
      {error && (
        <div className="px-4 py-3 border-t border-gray-200 bg-red-50">
          <div className="flex items-start gap-2">
            <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      )}

      {/* 操作按钮 */}
      <div className="px-4 py-3 border-t border-gray-200">
        <Button
          onClick={onRewrite}
          disabled={isProcessing || !inputText.trim() || isOverLimit}
          fullWidth
          variant="primary"
          size="md"
        >
          {isProcessing ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              处理中...
            </>
          ) : (
            <>
              <Wand2 className="w-4 h-4 mr-2" />
              开始去痕
            </>
          )}
        </Button>
      </div>
    </div>
  );
};
