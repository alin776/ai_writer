/**
 * ProgressBar - Agent进度条组件
 *
 * 显示Agent执行的实时进度信息，包括：
 * - 进度条（0-100%）
 * - ETA倒计时
 * - 步骤计数（第X/Y步）
 * - 当前节点描述
 *
 * 设计：简约专业，灵感来自VSCode和Linear
 */

import React, { memo } from 'react';
import { Clock, TrendingUp } from 'lucide-react';
import type { ProgressData } from '@/types/agent';
import styles from './ProgressBar.module.css';  // ✅ 导入CSS Module

interface ProgressBarProps {
  progress: number;              // 0-100
  eta?: number | null;
  etaDisplay?: string;
  etaConfidence?: 'low' | 'medium' | 'high';
  currentStep?: number;
  totalSteps?: number;
  stepDescription?: string;
  currentNodeDescription?: string | null;
  className?: string;
}

/**
 * 获取ETA置信度颜色（提取到组件外部，避免重复创建）
 */
const getConfidenceColor = (confidence?: string): string => {
  switch (confidence) {
    case 'high':
      return 'text-green-600';
    case 'medium':
      return 'text-yellow-600';
    case 'low':
      return 'text-gray-500';
    default:
      return 'text-gray-500';
  }
};

/**
 * ProgressBar组件（使用memo优化性能）
 */
const ProgressBar = memo(function ProgressBar({
  progress,
  eta,
  etaDisplay,
  etaConfidence,
  currentStep,
  totalSteps,
  stepDescription,
  currentNodeDescription,
  className = '',
}: ProgressBarProps) {
  // 确保进度在0-100范围内
  const clampedProgress = Math.min(Math.max(progress, 0), 100);

  // 判断是否接近完成
  const isNearComplete = clampedProgress >= 95;

  return (
    <div className={`progress-bar-container ${className}`}>
      {/* 顶部信息行 */}
      <div className="flex items-center justify-between mb-2 text-sm">
        {/* 左侧：当前节点描述或步骤描述 */}
        <div className="flex items-center gap-2">
          {currentNodeDescription && (
            <span className="text-gray-700 font-medium">
              {currentNodeDescription}
            </span>
          )}
          {stepDescription && (
            <span className="text-gray-500 text-xs">
              {stepDescription}
            </span>
          )}
        </div>

        {/* 右侧：ETA和进度百分比 */}
        <div className="flex items-center gap-3">
          {/* ETA */}
          {etaDisplay && !isNearComplete && (
            <div className={`flex items-center gap-1 text-xs ${getConfidenceColor(etaConfidence)}`}>
              <Clock size={12} />
              <span>{etaDisplay}</span>
            </div>
          )}

          {/* 进度百分比 */}
          <div className="flex items-center gap-1 text-xs font-medium text-blue-600">
            <TrendingUp size={12} />
            <span>{clampedProgress.toFixed(0)}%</span>
          </div>
        </div>
      </div>

      {/* 进度条 - ✅ 添加ARIA可访问性属性 */}
      <div
        className="relative w-full h-2 bg-gray-200 rounded-full overflow-hidden"
        role="progressbar"
        aria-valuenow={clampedProgress}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-live="polite"
        aria-label={currentNodeDescription || stepDescription || "Agent执行进度"}
        aria-valuetext={`${clampedProgress.toFixed(0)}%, ${etaDisplay || '计算中'}`}
      >
        {/* 填充条 */}
        <div
          className={`
            absolute top-0 left-0 h-full rounded-full
            ${styles.progressFill}
            ${isNearComplete ? styles.progressFillComplete : styles.progressFillActive}
          `}
          style={{ width: `${clampedProgress}%` }}
        >
          {/* 动画光效 */}
          {clampedProgress > 0 && clampedProgress < 100 && (
            <div
              className={`absolute top-0 right-0 bottom-0 w-20 bg-gradient-to-r from-transparent to-white opacity-30 ${styles.shimmer}`}
            />
          )}
        </div>

        {/* 完成时的脉冲效果 */}
        {clampedProgress >= 100 && (
          <div className={`absolute top-0 left-0 w-full h-full bg-green-500 ${styles.pulse}`} />
        )}
      </div>

      {/* 底部提示（可选） */}
      {isNearComplete && clampedProgress < 100 && (
        <div className="mt-1 text-xs text-green-600 text-center">
          即将完成...
        </div>
      )}
      {clampedProgress >= 100 && (
        <div className="mt-1 text-xs text-green-600 text-center font-medium">
          ✓ 完成
        </div>
      )}
    </div>
  );
}, (prevProps, nextProps) => {
  // 自定义比较逻辑：只有这些关键属性变化时才重新渲染
  return (
    prevProps.progress === nextProps.progress &&
    prevProps.etaDisplay === nextProps.etaDisplay &&
    prevProps.etaConfidence === nextProps.etaConfidence &&
    prevProps.stepDescription === nextProps.stepDescription &&
    prevProps.currentNodeDescription === nextProps.currentNodeDescription
  );
});

// 默认导出
export default ProgressBar;

/**
 * ProgressBarCompact - 紧凑版进度条（使用memo优化）
 *
 * 只显示进度条和百分比，适合空间有限的场景
 */
export const ProgressBarCompact = memo(function ProgressBarCompact({
  progress,
  className = '',
}: {
  progress: number;
  className?: string;
}) {
  const clampedProgress = Math.min(Math.max(progress, 0), 100);

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      {/* 进度条 - ✅ 添加ARIA可访问性属性 */}
      <div
        className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden"
        role="progressbar"
        aria-valuenow={clampedProgress}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-live="polite"
        aria-label="执行进度"
        aria-valuetext={`${clampedProgress.toFixed(0)}%`}
      >
        <div
          className={`h-full bg-blue-500 rounded-full ${styles.compactFill}`}
          style={{ width: `${clampedProgress}%` }}
        />
      </div>

      {/* 百分比 */}
      <span className="text-xs text-gray-600 font-medium min-w-[40px] text-right">
        {clampedProgress.toFixed(0)}%
      </span>
    </div>
  );
}, (prevProps, nextProps) => prevProps.progress === nextProps.progress);
