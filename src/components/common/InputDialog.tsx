/**
 * InputDialog - 输入对话框组件
 * 用于替代原生的 prompt，提供更专业的输入体验
 */
import React, { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { X } from 'lucide-react';

interface InputField {
  name: string;
  label: string;
  placeholder?: string;
  required?: boolean;
  defaultValue?: string;
  type?: 'text' | 'textarea' | 'password';
  rows?: number;
}

interface InputDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (values: Record<string, string>) => void;
  title: string;
  fields: InputField[];
  confirmText?: string;
  cancelText?: string;
}

const InputDialog: React.FC<InputDialogProps> = ({
  isOpen,
  onClose,
  onConfirm,
  title,
  fields,
  confirmText,
  cancelText,
}) => {
  const { t } = useTranslation();
  const actualConfirmText = confirmText || t('common.confirm');
  const actualCancelText = cancelText || t('common.cancel');

  const [values, setValues] = useState<Record<string, string>>({});
  const firstInputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null);

  // 初始化表单值
  useEffect(() => {
    if (isOpen) {
      const initialValues: Record<string, string> = {};
      fields.forEach((field) => {
        initialValues[field.name] = field.defaultValue || '';
      });
      setValues(initialValues);

      // 聚焦第一个输入框
      setTimeout(() => {
        firstInputRef.current?.focus();
      }, 100);
    }
  }, [isOpen, fields]);

  const handleChange = (name: string, value: string) => {
    setValues((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // 验证必填字段
    for (const field of fields) {
      if (field.required && !values[field.name]?.trim()) {
        return;
      }
    }

    onConfirm(values);
    onClose();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* 遮罩层 */}
      <div
        className="absolute inset-0 bg-black/50 dark:bg-black/60 backdrop-blur-sm animate-fadeIn"
        onClick={onClose}
      />

      {/* 对话框 */}
      <div
        className="relative bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 rounded-lg shadow-2xl w-full max-w-md mx-4 animate-scaleIn border border-gray-200 dark:border-gray-700"
        onKeyDown={handleKeyDown}
      >
        {/* 头部 */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{title}</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 表单内容 */}
        <form onSubmit={handleSubmit} className="px-6 py-4">
          <div className="space-y-4">
            {fields.map((field, index) => (
              <div key={field.name}>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  {field.label}
                  {field.required && <span className="text-red-500 ml-1">*</span>}
                </label>
                {field.type === 'textarea' ? (
                  <textarea
                    ref={index === 0 ? (firstInputRef as React.RefObject<HTMLTextAreaElement>) : undefined}
                    value={values[field.name] || ''}
                    onChange={(e) => handleChange(field.name, e.target.value)}
                    placeholder={field.placeholder}
                    rows={field.rows || 3}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-all resize-none bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
                    required={field.required}
                  />
                ) : (
                  <input
                    ref={index === 0 ? (firstInputRef as React.RefObject<HTMLInputElement>) : undefined}
                    type={field.type === 'password' ? 'password' : 'text'}
                    value={values[field.name] || ''}
                    onChange={(e) => handleChange(field.name, e.target.value)}
                    placeholder={field.placeholder}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-all bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 dark:[&::-ms-reveal]:invert dark:[&::-ms-reveal]:brightness-200"
                    required={field.required}
                  />
                )}
              </div>
            ))}
          </div>

          {/* 底部按钮 */}
          <div className="flex justify-end gap-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              {actualCancelText}
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 dark:bg-blue-500 rounded-lg hover:bg-blue-700 dark:hover:bg-blue-400 transition-colors shadow-sm hover:shadow-md"
            >
              {actualConfirmText}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default InputDialog;
