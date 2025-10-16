import React, { useEffect } from 'react';
import { createPortal } from 'react-dom';
import { useGlobalStore, type Toast as ToastType } from '../../store/globalStore';
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react';

/**
 * 单个 Toast 项组件 Props 接口
 */
interface ToastItemProps {
  /**
   * Toast 数据
   */
  toast: ToastType;

  /**
   * 关闭回调
   */
  onClose: (id: string) => void;
}

/**
 * 单个 Toast 项组件
 */
const ToastItem: React.FC<ToastItemProps> = ({ toast, onClose }) => {
  /**
   * 获取 Toast 图标
   */
  const getIcon = () => {
    const iconProps = { className: 'w-5 h-5', strokeWidth: 2 };

    switch (toast.type) {
      case 'success':
        return <CheckCircle {...iconProps} />;
      case 'error':
        return <XCircle {...iconProps} />;
      case 'warning':
        return <AlertCircle {...iconProps} />;
      case 'info':
        return <Info {...iconProps} />;
      default:
        return <Info {...iconProps} />;
    }
  };

  /**
   * 获取 Toast 样式
   */
  const getStyles = (): string => {
    const baseStyles = 'flex items-start gap-3 p-4 rounded-lg shadow-lg min-w-[300px] max-w-md animate-slideInRight';

    const typeStyles = {
      success: 'bg-green-50 text-green-800 border border-green-200',
      error: 'bg-red-50 text-red-800 border border-red-200',
      warning: 'bg-yellow-50 text-yellow-800 border border-yellow-200',
      info: 'bg-blue-50 text-blue-800 border border-blue-200',
    };

    return `${baseStyles} ${typeStyles[toast.type]}`;
  };

  /**
   * 获取图标颜色
   */
  const getIconColor = (): string => {
    const colors = {
      success: 'text-green-600',
      error: 'text-red-600',
      warning: 'text-yellow-600',
      info: 'text-blue-600',
    };

    return colors[toast.type];
  };

  /**
   * 自动关闭
   */
  useEffect(() => {
    if (toast.duration && toast.duration > 0) {
      const timer = setTimeout(() => {
        onClose(toast.id);
      }, toast.duration);

      return () => clearTimeout(timer);
    }
  }, [toast.id, toast.duration, onClose]);

  return (
    <div className={getStyles()} role="alert">
      {/* 图标 */}
      <div className={`flex-shrink-0 ${getIconColor()}`}>
        {getIcon()}
      </div>

      {/* 消息内容 */}
      <div className="flex-1 pt-0.5">
        <p className="text-sm font-medium leading-relaxed">{toast.message}</p>
      </div>

      {/* 关闭按钮 */}
      <button
        type="button"
        onClick={() => onClose(toast.id)}
        className="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded"
        aria-label="关闭"
      >
        <X className="w-4 h-4" strokeWidth={2} />
      </button>
    </div>
  );
};

/**
 * Toast 容器组件
 *
 * 功能：
 * - 支持 success, error, warning, info 四种类型
 * - 自动消失（可配置时长）
 * - 使用 lucide-react 图标
 * - 与 globalStore 集成
 * - 支持多个 Toast 同时显示
 * - 使用 Portal 渲染到 body
 * - 带滑入动画效果
 * - 支持手动关闭
 *
 * @example
 * ```tsx
 * // 在 App 组件中使用
 * function App() {
 *   return (
 *     <>
 *       <Toast />
 *       <YourAppContent />
 *     </>
 *   );
 * }
 *
 * // 在其他组件中调用
 * const { showToast } = useGlobalStore();
 * showToast('success', '操作成功！');
 * ```
 */
const Toast: React.FC = () => {
  const toasts = useGlobalStore((state) => state.toasts);
  const hideToast = useGlobalStore((state) => state.hideToast);

  if (toasts.length === 0) {
    return null;
  }

  /**
   * 渲染 Toast 容器
   */
  const toastContainer = (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-3 pointer-events-none">
      <div className="flex flex-col gap-3 pointer-events-auto">
        {toasts.map((toast) => (
          <ToastItem key={toast.id} toast={toast} onClose={hideToast} />
        ))}
      </div>
    </div>
  );

  // 使用 Portal 渲染到 body
  return createPortal(toastContainer, document.body);
};

export default Toast;
