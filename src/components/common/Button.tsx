import React from 'react';

/**
 * 按钮变体类型
 */
export type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'outline' | 'ghost';

/**
 * 按钮尺寸类型
 */
export type ButtonSize = 'sm' | 'md' | 'lg';

/**
 * 按钮组件 Props 接口
 */
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * 按钮变体样式
   * @default 'primary'
   */
  variant?: ButtonVariant;

  /**
   * 按钮尺寸
   * @default 'md'
   */
  size?: ButtonSize;

  /**
   * 是否处于加载状态
   * @default false
   */
  loading?: boolean;

  /**
   * 是否处于加载状态 (loading 的别名)
   * @default false
   */
  isLoading?: boolean;

  /**
   * 是否禁用
   * @default false
   */
  disabled?: boolean;

  /**
   * 图标元素
   */
  icon?: React.ReactNode;

  /**
   * 按钮内容
   */
  children: React.ReactNode;

  /**
   * 自定义类名
   */
  className?: string;

  /**
   * 完整宽度
   * @default false
   */
  fullWidth?: boolean;
}

/**
 * 按钮组件
 *
 * 功能：
 * - 支持多种变体样式 (primary, secondary, danger, outline, ghost)
 * - 支持多种尺寸 (sm, md, lg)
 * - 支持 loading 和 disabled 状态
 * - 使用 Tailwind CSS 进行样式设计
 * - 完全支持原生 button 属性
 *
 * @example
 * ```tsx
 * <Button variant="primary" size="md" onClick={handleClick}>
 *   点击我
 * </Button>
 *
 * <Button variant="danger" loading disabled>
 *   加载中...
 * </Button>
 * ```
 */
const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  isLoading = false,
  disabled = false,
  icon,
  children,
  className = '',
  fullWidth = false,
  ...props
}) => {
  // 统一 loading 状态：isLoading 优先，其次是 loading
  const isButtonLoading = isLoading || loading;
  /**
   * 获取按钮变体样式
   */
  const getVariantStyles = (): string => {
    const variants: Record<ButtonVariant, string> = {
      primary: 'bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800 focus:ring-blue-500',
      secondary: 'bg-gray-600 text-white hover:bg-gray-700 active:bg-gray-800 focus:ring-gray-500',
      danger: 'bg-red-600 text-white hover:bg-red-700 active:bg-red-800 focus:ring-red-500',
      outline: 'bg-transparent border-2 border-blue-600 text-blue-600 hover:bg-blue-50 active:bg-blue-100 focus:ring-blue-500',
      ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 active:bg-gray-200 focus:ring-gray-500',
    };

    return variants[variant];
  };

  /**
   * 获取按钮尺寸样式
   */
  const getSizeStyles = (): string => {
    const sizes: Record<ButtonSize, string> = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg',
    };

    return sizes[size];
  };

  /**
   * 获取禁用状态样式
   */
  const getDisabledStyles = (): string => {
    if (disabled || isButtonLoading) {
      return 'opacity-50 cursor-not-allowed';
    }
    return 'cursor-pointer';
  };

  /**
   * 获取宽度样式
   */
  const getWidthStyles = (): string => {
    return fullWidth ? 'w-full' : '';
  };

  /**
   * 基础样式
   */
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';

  /**
   * 组合所有样式
   */
  const buttonStyles = [
    baseStyles,
    getVariantStyles(),
    getSizeStyles(),
    getDisabledStyles(),
    getWidthStyles(),
    className,
  ].join(' ');

  return (
    <button
      type="button"
      className={buttonStyles}
      disabled={disabled || isButtonLoading}
      {...props}
    >
      {isButtonLoading && (
        <svg
          className="animate-spin -ml-1 mr-2 h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
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
      )}
      {!isButtonLoading && icon && <span className="mr-2">{icon}</span>}
      {children}
    </button>
  );
};

export default Button;
