import React from 'react';
import { useTranslation } from 'react-i18next';

/**
 * 加载指示器尺寸类型
 */
export type LoadingSize = 'sm' | 'md' | 'lg' | 'xl';

/**
 * 加载指示器组件 Props 接口
 */
export interface LoadingProps {
  /**
   * 加载指示器尺寸
   * @default 'md'
   */
  size?: LoadingSize;

  /**
   * 是否显示全屏遮罩
   * @default false
   */
  fullscreen?: boolean;

  /**
   * 加载提示文本
   */
  text?: string;

  /**
   * 自定义类名
   */
  className?: string;

  /**
   * 加载指示器颜色
   * @default 'blue'
   */
  color?: 'blue' | 'white' | 'gray' | 'red' | 'green';
}

/**
 * 加载指示器组件
 *
 * 功能：
 * - 支持多种尺寸 (sm, md, lg, xl)
 * - 旋转动画效果
 * - 支持全屏遮罩模式
 * - 支持加载提示文本
 * - 支持多种颜色
 * - 使用 Tailwind CSS 进行样式设计
 *
 * @example
 * ```tsx
 * // 基础用法
 * <Loading size="md" />
 *
 * // 全屏遮罩模式
 * <Loading fullscreen text="加载中..." />
 *
 * // 自定义颜色
 * <Loading color="white" size="lg" />
 * ```
 */
const Loading: React.FC<LoadingProps> = ({
  size = 'md',
  fullscreen = false,
  text,
  className = '',
  color = 'blue',
}) => {
  const { t } = useTranslation();
  /**
   * 获取加载指示器尺寸样式
   */
  const getSizeStyles = (): string => {
    const sizes: Record<LoadingSize, string> = {
      sm: 'h-4 w-4',
      md: 'h-8 w-8',
      lg: 'h-12 w-12',
      xl: 'h-16 w-16',
    };

    return sizes[size];
  };

  /**
   * 获取文本尺寸样式
   */
  const getTextSizeStyles = (): string => {
    const textSizes: Record<LoadingSize, string> = {
      sm: 'text-sm',
      md: 'text-base',
      lg: 'text-lg',
      xl: 'text-xl',
    };

    return textSizes[size];
  };

  /**
   * 获取颜色样式
   */
  const getColorStyles = (): string => {
    const colors = {
      blue: 'text-blue-600',
      white: 'text-white',
      gray: 'text-gray-600',
      red: 'text-red-600',
      green: 'text-green-600',
    };

    return colors[color];
  };

  /**
   * 渲染加载指示器
   */
  const renderSpinner = () => (
    <svg
      className={`animate-spin ${getSizeStyles()} ${getColorStyles()} ${className}`}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      role="status"
      aria-label={t('common.loading')}
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  );

  /**
   * 全屏模式
   */
  if (fullscreen) {
    return (
      <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm animate-fadeIn">
        <div className="flex flex-col items-center gap-4">
          {renderSpinner()}
          {text && (
            <p className={`${getTextSizeStyles()} font-medium ${fullscreen ? 'text-white' : 'text-gray-700'}`}>
              {text}
            </p>
          )}
        </div>
      </div>
    );
  }

  /**
   * 内联模式
   */
  return (
    <div className="flex flex-col items-center justify-center gap-2">
      {renderSpinner()}
      {text && (
        <p className={`${getTextSizeStyles()} font-medium text-gray-700`}>
          {text}
        </p>
      )}
    </div>
  );
};

export default Loading;
