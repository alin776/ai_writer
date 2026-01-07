import React, { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { cn } from '@/lib/utils';

interface TooltipProps {
  content: string;
  children: React.ReactNode;
  position?: 'top' | 'bottom' | 'left' | 'right';
  delay?: number;
  className?: string;
}

export function Tooltip({
  content,
  children,
  position = 'top',
  delay = 100,
  className
}: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [coords, setCoords] = useState<{ x: number; y: number } | null>(null);
  const triggerRef = useRef<HTMLDivElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  const showTooltip = () => {
    timeoutRef.current = setTimeout(() => {
      setIsVisible(true);
    }, delay);
  };

  const hideTooltip = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setIsVisible(false);
    setCoords(null);
  };

  // 计算位置
  useEffect(() => {
    if (isVisible && triggerRef.current) {
      const updatePosition = () => {
        if (!triggerRef.current || !tooltipRef.current) return;

        const triggerRect = triggerRef.current.getBoundingClientRect();
        const tooltipRect = tooltipRef.current.getBoundingClientRect();

        let x = 0, y = 0;

        switch (position) {
          case 'top':
            x = triggerRect.left + triggerRect.width / 2 - tooltipRect.width / 2;
            y = triggerRect.top - tooltipRect.height - 8;
            break;
          case 'bottom':
            x = triggerRect.left + triggerRect.width / 2 - tooltipRect.width / 2;
            y = triggerRect.bottom + 8;
            break;
          case 'left':
            x = triggerRect.left - tooltipRect.width - 8;
            y = triggerRect.top + triggerRect.height / 2 - tooltipRect.height / 2;
            break;
          case 'right':
            x = triggerRect.right + 8;
            y = triggerRect.top + triggerRect.height / 2 - tooltipRect.height / 2;
            break;
        }

        // 边界检测
        x = Math.max(8, Math.min(x, window.innerWidth - tooltipRect.width - 8));
        y = Math.max(8, Math.min(y, window.innerHeight - tooltipRect.height - 8));

        setCoords({ x, y });
      };

      // 使用 requestAnimationFrame 确保 DOM 已更新
      requestAnimationFrame(updatePosition);
    }
  }, [isVisible, position]);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  // 不在服务端渲染
  if (typeof window === 'undefined') {
    return <>{children}</>;
  }

  const tooltipElement = isVisible ? (
    <div
      ref={tooltipRef}
      role="tooltip"
      className={cn(
        "fixed z-[9999] px-3 py-1.5 text-sm font-medium rounded-md shadow-lg pointer-events-none whitespace-nowrap",
        // 使用项目的 CSS 变量系统，支持深浅色模式
        "bg-gray-900 text-white dark:bg-gray-100 dark:text-gray-900",
        // 过渡动画
        "transition-opacity duration-150",
        coords ? "opacity-100" : "opacity-0"
      )}
      style={{
        left: coords?.x ?? -9999,
        top: coords?.y ?? -9999,
      }}
    >
      {content}
      {/* 箭头 - 使用相同的颜色 */}
      <div
        className={cn(
          "absolute w-2 h-2 rotate-45",
          "bg-gray-900 dark:bg-gray-100",
          position === 'top' && "bottom-[-4px] left-1/2 -translate-x-1/2",
          position === 'bottom' && "top-[-4px] left-1/2 -translate-x-1/2",
          position === 'left' && "right-[-4px] top-1/2 -translate-y-1/2",
          position === 'right' && "left-[-4px] top-1/2 -translate-y-1/2"
        )}
      />
    </div>
  ) : null;

  return (
    <>
      <div
        ref={triggerRef}
        onMouseEnter={showTooltip}
        onMouseLeave={hideTooltip}
        className={cn("inline-flex", className)}
      >
        {children}
      </div>
      {tooltipElement && createPortal(tooltipElement, document.body)}
    </>
  );
}
