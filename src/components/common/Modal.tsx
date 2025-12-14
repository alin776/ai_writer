import React, { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';

/**
 * 模态框组件 Props 接口
 */
export interface ModalProps {
  /**
   * 是否显示模态框
   */
  isOpen: boolean;

  /**
   * 关闭模态框回调
   */
  onClose: () => void;

  /**
   * 模态框标题
   */
  title?: string;

  /**
   * 模态框内容
   */
  children: React.ReactNode;

  /**
   * 底部按钮区域
   */
  footer?: React.ReactNode;

  /**
   * 点击遮罩层是否关闭
   * @default true
   */
  closeOnOverlayClick?: boolean;

  /**
   * 按 ESC 键是否关闭
   * @default true
   */
  closeOnEsc?: boolean;

  /**
   * 模态框尺寸
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';

  /**
   * 是否显示关闭按钮
   * @default true
   */
  showCloseButton?: boolean;

  /**
   * 自定义类名
   */
  className?: string;
}

/**
 * 模态框组件
 *
 * 功能：
 * - 支持标题、内容、底部按钮区域
 * - 支持点击遮罩层关闭
 * - 支持按 ESC 键关闭
 * - 带淡入淡出动画效果
 * - 使用 Portal 渲染到 body
 * - 支持多种尺寸
 * - 自动管理 body 滚动锁定
 *
 * @example
 * ```tsx
 * <Modal
 *   isOpen={isOpen}
 *   onClose={() => setIsOpen(false)}
 *   title="确认删除"
 *   footer={
 *     <>
 *       <Button variant="secondary" onClick={() => setIsOpen(false)}>取消</Button>
 *       <Button variant="danger" onClick={handleDelete}>删除</Button>
 *     </>
 *   }
 * >
 *   <p>确定要删除这个项目吗？</p>
 * </Modal>
 * ```
 */
const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
  closeOnOverlayClick = true,
  closeOnEsc = true,
  size = 'md',
  showCloseButton = true,
  className = '',
}) => {
  const { t } = useTranslation();
  const modalRef = useRef<HTMLDivElement>(null);

  /**
   * 获取模态框尺寸样式
   */
  const getSizeStyles = (): string => {
    const sizes = {
      sm: 'max-w-sm',
      md: 'max-w-md',
      lg: 'max-w-lg',
      xl: 'max-w-xl',
      full: 'max-w-full mx-4',
    };

    return sizes[size];
  };

  /**
   * 处理遮罩层点击
   */
  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (closeOnOverlayClick && e.target === e.currentTarget) {
      onClose();
    }
  };

  /**
   * 处理 ESC 键按下
   */
  useEffect(() => {
    const handleEscKey = (e: KeyboardEvent) => {
      if (closeOnEsc && e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscKey);
    }

    return () => {
      document.removeEventListener('keydown', handleEscKey);
    };
  }, [isOpen, closeOnEsc, onClose]);

  /**
   * 管理 body 滚动锁定
   */
  useEffect(() => {
    if (isOpen) {
      // 锁定 body 滚动
      document.body.style.overflow = 'hidden';
    } else {
      // 恢复 body 滚动
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  /**
   * 聚焦管理
   */
  useEffect(() => {
    if (isOpen && modalRef.current) {
      modalRef.current.focus();
    }
  }, [isOpen]);

  if (!isOpen) {
    return null;
  }

  /**
   * 渲染模态框内容
   */
  const modalContent = (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fadeIn"
      onClick={handleOverlayClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby={title ? 'modal-title' : undefined}
    >
      {/* 遮罩层 */}
      <div className="fixed inset-0 bg-gray-900/20 transition-opacity" />

      {/* 模态框容器 */}
      <div
        ref={modalRef}
        className={`relative bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 rounded-lg shadow-xl w-full border border-gray-200 dark:border-gray-700 ${getSizeStyles()} animate-scaleIn ${className}`}
        tabIndex={-1}
      >
        {/* 头部 */}
        {(title || showCloseButton) && (
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            {title && (
              <h3
                id="modal-title"
                className="text-lg font-semibold text-gray-900 dark:text-gray-100"
              >
                {title}
              </h3>
            )}
            {showCloseButton && (
              <button
                type="button"
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 rounded-lg p-1"
                aria-label={t('common.close')}
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            )}
          </div>
        )}

        {/* 内容区域 */}
        <div className="px-6 py-4 max-h-[calc(100vh-200px)] overflow-y-auto">
          {children}
        </div>

        {/* 底部按钮区域 */}
        {footer && (
          <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-b-lg">
            {footer}
          </div>
        )}
      </div>
    </div>
  );

  // 使用 Portal 渲染到 body
  return createPortal(modalContent, document.body);
};

export default Modal;
