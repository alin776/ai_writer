import React, { forwardRef } from 'react';

/**
 * 输入框类型
 */
export type InputType = 'text' | 'email' | 'password' | 'number' | 'tel' | 'url';

/**
 * 输入框组件 Props 接口
 */
export interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  /**
   * 输入框类型
   * @default 'text'
   */
  type?: InputType;

  /**
   * 标签文本
   */
  label?: string;

  /**
   * 错误提示信息
   */
  error?: string;

  /**
   * 帮助文本
   */
  helperText?: string;

  /**
   * 是否必填
   * @default false
   */
  required?: boolean;

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
   * 输入框值（受控组件）
   */
  value?: string | number;

  /**
   * 值变化回调
   */
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;

  /**
   * 自定义类名
   */
  className?: string;

  /**
   * 容器自定义类名
   */
  containerClassName?: string;

  /**
   * 完整宽度
   * @default true
   */
  fullWidth?: boolean;
}

/**
 * 输入框组件
 *
 * 功能：
 * - 支持多种输入类型 (text, email, password, number, tel, url)
 * - 支持错误提示和帮助文本
 * - 支持 label 和 placeholder
 * - 完整的受控组件实现
 * - 支持必填标识
 * - 使用 Tailwind CSS 进行样式设计
 * - 使用 forwardRef 支持 ref 转发
 *
 * @example
 * ```tsx
 * <Input
 *   label="邮箱"
 *   type="email"
 *   placeholder="请输入邮箱"
 *   value={email}
 *   onChange={(e) => setEmail(e.target.value)}
 *   error={emailError}
 *   required
 * />
 * ```
 */
const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      type = 'text',
      label,
      error,
      helperText,
      required = false,
      disabled = false,
      icon,
      value,
      onChange,
      className = '',
      containerClassName = '',
      fullWidth = true,
      placeholder,
      ...props
    },
    ref
  ) => {
    /**
     * 输入框 ID（用于 label 关联）
     */
    const inputId = React.useId();

    /**
     * 获取输入框样式
     */
    const getInputStyles = (): string => {
      const baseStyles =
        'block px-3 py-2 border rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-0 transition-all duration-200 bg-white dark:bg-gray-900 dark:[&::-ms-reveal]:invert dark:[&::-ms-reveal]:brightness-200';

      // 错误状态样式
      const errorStyles = error
        ? 'border-red-500 focus:border-red-500 focus:ring-red-500 dark:border-red-400 dark:focus:border-red-400 dark:focus:ring-red-400'
        : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:focus:border-blue-400 dark:focus:ring-blue-400';

      // 禁用状态样式
      const disabledStyles = disabled
        ? 'bg-gray-100 cursor-not-allowed opacity-60 dark:bg-gray-800 dark:text-gray-500 dark:border-gray-700'
        : 'bg-white hover:border-gray-400 dark:bg-gray-900 dark:border-gray-700 dark:hover:border-gray-500';

      // 宽度样式
      const widthStyles = fullWidth ? 'w-full' : '';

      return [baseStyles, errorStyles, disabledStyles, widthStyles, className].join(' ');
    };

    /**
     * 获取容器样式
     */
    const getContainerStyles = (): string => {
      const widthStyles = fullWidth ? 'w-full' : '';
      return [widthStyles, containerClassName].join(' ');
    };

    return (
      <div className={getContainerStyles()}>
        {/* 标签 */}
        {label && (
          <label
            htmlFor={inputId}
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >
            {label}
            {required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}

        {/* 输入框容器 */}
        <div className="relative">
          {/* 图标 */}
          {icon && (
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              {icon}
            </div>
          )}

          {/* 输入框 */}
          <input
            ref={ref}
            id={inputId}
            type={type}
            value={value}
            onChange={onChange}
            disabled={disabled}
            placeholder={placeholder}
            className={`${getInputStyles()} ${icon ? 'pl-10' : ''}`}
            aria-invalid={!!error}
            aria-describedby={error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined}
            {...props}
          />
        </div>

        {/* 错误提示 */}
        {error && (
          <p
            id={`${inputId}-error`}
            className="mt-1 text-sm text-red-600 flex items-center"
            role="alert"
          >
            <svg
              className="w-4 h-4 mr-1"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                clipRule="evenodd"
              />
            </svg>
            {error}
          </p>
        )}

        {/* 帮助文本 */}
        {!error && helperText && (
          <p
            id={`${inputId}-helper`}
            className="mt-1 text-sm text-gray-500"
          >
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
