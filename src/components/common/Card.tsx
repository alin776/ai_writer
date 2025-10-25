import React from 'react';

/**
 * 卡片组件 Props 接口
 */
export interface CardProps {
  /**
   * 卡片内容
   */
  children: React.ReactNode;

  /**
   * 是否启用 hover 效果
   * @default false
   */
  hoverable?: boolean;

  /**
   * 是否显示阴影
   * @default true
   */
  shadow?: boolean;

  /**
   * 阴影大小
   * @default 'md'
   */
  shadowSize?: 'sm' | 'md' | 'lg' | 'xl' | 'none';

  /**
   * 内边距大小
   * @default 'md'
   */
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';

  /**
   * 圆角大小
   * @default 'lg'
   */
  rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | 'full';

  /**
   * 是否显示边框
   * @default true
   */
  bordered?: boolean;

  /**
   * 背景颜色
   * @default 'white'
   */
  background?: 'white' | 'gray' | 'transparent' | 'blue';

  /**
   * 点击事件
   */
  onClick?: () => void;

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
 * 卡片组件
 *
 * 功能：
 * - 基础卡片容器
 * - 支持 hover 效果（悬停时阴影加深）
 * - 支持不同的阴影大小
 * - 支持不同的内边距和圆角
 * - 支持边框显示/隐藏
 * - 支持不同背景颜色
 * - 支持点击事件
 * - 使用 Tailwind CSS 进行样式设计
 *
 * @example
 * ```tsx
 * <Card hoverable shadow padding="lg">
 *   <h3>卡片标题</h3>
 *   <p>卡片内容...</p>
 * </Card>
 *
 * <Card onClick={handleClick} hoverable>
 *   点击我
 * </Card>
 * ```
 */
const Card: React.FC<CardProps> = ({
  children,
  hoverable = false,
  shadow = true,
  shadowSize = 'md',
  padding = 'md',
  rounded = 'lg',
  bordered = true,
  background = 'white',
  onClick,
  className = '',
  fullWidth = false,
}) => {
  /**
   * 获取阴影样式
   */
  const getShadowStyles = (): string => {
    if (!shadow) return '';

    const shadows = {
      none: '',
      sm: 'shadow-sm',
      md: 'shadow-md',
      lg: 'shadow-lg',
      xl: 'shadow-xl',
    };

    const hoverShadows = {
      none: '',
      sm: 'hover:shadow-md',
      md: 'hover:shadow-lg',
      lg: 'hover:shadow-xl',
      xl: 'hover:shadow-2xl',
    };

    return hoverable
      ? `${shadows[shadowSize]} ${hoverShadows[shadowSize]}`
      : shadows[shadowSize];
  };

  /**
   * 获取内边距样式
   */
  const getPaddingStyles = (): string => {
    const paddings = {
      none: 'p-0',
      sm: 'p-3',
      md: 'p-4',
      lg: 'p-6',
      xl: 'p-8',
    };

    return paddings[padding];
  };

  /**
   * 获取圆角样式
   */
  const getRoundedStyles = (): string => {
    const roundeds = {
      none: 'rounded-none',
      sm: 'rounded-sm',
      md: 'rounded-md',
      lg: 'rounded-lg',
      xl: 'rounded-xl',
      full: 'rounded-full',
    };

    return roundeds[rounded];
  };

  /**
   * 获取边框样式
   */
  const getBorderStyles = (): string => {
    return bordered ? 'border border-gray-200 dark:border-gray-700' : '';
  };

  /**
   * 获取背景样式
   */
  const getBackgroundStyles = (): string => {
    const backgrounds = {
      white: 'bg-white dark:bg-gray-800',
      gray: 'bg-gray-50 dark:bg-gray-800/70',
      transparent: 'bg-transparent',
      blue: 'bg-blue-50 dark:bg-blue-900/20',
    };

    return backgrounds[background];
  };

  /**
   * 获取交互样式
   */
  const getInteractiveStyles = (): string => {
    if (onClick) {
      return 'cursor-pointer transition-all duration-200';
    }
    return hoverable ? 'transition-all duration-200' : '';
  };

  /**
   * 获取宽度样式
   */
  const getWidthStyles = (): string => {
    return fullWidth ? 'w-full' : '';
  };

  /**
   * Hover 变换效果
   */
  const getHoverTransform = (): string => {
    return hoverable ? 'hover:-translate-y-1' : '';
  };

  /**
   * 组合所有样式
   */
  const cardStyles = [
    'block',
    getBackgroundStyles(),
    getBorderStyles(),
    getRoundedStyles(),
    getPaddingStyles(),
    getShadowStyles(),
    getInteractiveStyles(),
    getHoverTransform(),
    getWidthStyles(),
    className,
  ]
    .filter(Boolean)
    .join(' ');

  /**
   * 渲染卡片
   */
  const cardElement = (
    <div className={cardStyles} onClick={onClick} role={onClick ? 'button' : undefined} tabIndex={onClick ? 0 : undefined}>
      {children}
    </div>
  );

  return cardElement;
};

/**
 * 卡片头部组件
 */
export interface CardHeaderProps {
  children: React.ReactNode;
  className?: string;
}

export const CardHeader: React.FC<CardHeaderProps> = ({ children, className = '' }) => {
  return (
    <div className={`border-b border-gray-200 dark:border-gray-700 pb-3 mb-3 ${className}`}>
      {children}
    </div>
  );
};

/**
 * 卡片内容组件
 */
export interface CardContentProps {
  children: React.ReactNode;
  className?: string;
}

export const CardContent: React.FC<CardContentProps> = ({ children, className = '' }) => {
  return <div className={className}>{children}</div>;
};

/**
 * 卡片底部组件
 */
export interface CardFooterProps {
  children: React.ReactNode;
  className?: string;
}

export const CardFooter: React.FC<CardFooterProps> = ({ children, className = '' }) => {
  return (
    <div className={`border-t border-gray-200 dark:border-gray-700 pt-3 mt-3 ${className}`}>
      {children}
    </div>
  );
};

export default Card;
