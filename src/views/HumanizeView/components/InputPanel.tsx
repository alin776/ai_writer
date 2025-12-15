// src/views/HumanizeView/components/InputPanel.tsx

import React from 'react';
import Button from '@/components/common/Button';
import { Wand2, Loader2, AlertCircle } from 'lucide-react';
import type { HumanizeIntensity, HumanizeStage } from '@/types/humanize';

interface InputPanelProps {
  inputText: string;
  intensity: HumanizeIntensity;
  isProcessing: boolean;
  currentStage: HumanizeStage;
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
  const trimmedLength = inputText.trim().length;  // 使用trim后的长度进行判断
  const maxLength = 5000;
  const minLength = 10;
  const isOverLimit = inputLength > maxLength;
  const isBelowMin = trimmedLength > 0 && trimmedLength < minLength;  // 使用trimmedLength

  return (
    <div className="h-full flex flex-col bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm min-h-[520px] max-h-[520px]">
      {/* 标题栏 */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">原文输入</h3>
        <span className={`text-xs font-mono ${isOverLimit ? 'text-red-600 dark:text-red-400' : 'text-gray-500 dark:text-gray-400'}`}>
          {inputLength.toLocaleString()} / {maxLength.toLocaleString()}
        </span>
      </div>

      {/* 文本输入区 */}
      <div className="flex-1 p-4 overflow-hidden flex flex-col">
        <textarea
          value={inputText}
          onChange={(e) => onInputChange(e.target.value)}
          placeholder="粘贴或输入需要去除AI痕迹的文本...&#10;&#10;支持最多5,000字符"
          className="flex-1 resize-none text-sm border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={isProcessing}
        />
        {isBelowMin && (
          <p className="mt-2 text-xs text-red-600 dark:text-red-400">请输入至少 10 个字符</p>
        )}
      </div>

      {/* 强度选择 */}
      <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700">
        <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
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
                  ? 'bg-blue-600 dark:bg-blue-500 text-white shadow-sm'
                  : 'bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600'
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
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
          {intensity === 'light' && '仅去除明显AI套话，保持原文风格'}
          {intensity === 'medium' && '平衡自然度与内容保留，推荐使用'}
          {intensity === 'strong' && '深度重构句式，最大化自然度'}
        </p>
      </div>

      {/* 处理状态 */}
      {isProcessing && (
        <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-blue-50 dark:bg-blue-900/30">
          <div className="flex items-center gap-2 text-sm text-blue-700 dark:text-blue-300">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>
              {currentStage === 'detecting' && '正在检测AI痕迹...'}
              {currentStage === 'detected' && '检测完成，准备改写...'}
              {currentStage === 'rewriting' && '正在智能改写...'}
              {currentStage === 'verifying' && '正在验证效果...'}
            </span>
          </div>
          {detectionScore !== null && (
            <div className="mt-2 text-xs text-blue-600 dark:text-blue-400">
              AI特征分数: <span className="font-mono font-semibold">{detectionScore}/100</span>
            </div>
          )}
        </div>
      )}

      {/* 错误提示 */}
      {error && (
        <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-red-50 dark:bg-red-900/30">
          <div className="flex items-start gap-2">
            <AlertCircle className="w-4 h-4 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
          </div>
        </div>
      )}

      {/* 操作按钮 */}
      <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700">
        <Button
          onClick={onRewrite}
          disabled={isProcessing || !inputText.trim() || isOverLimit || isBelowMin}
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
