/**
 * InputDialog - 杈撳叆瀵硅瘽妗嗙粍浠?
 * 鐢ㄤ簬鏇夸唬鍘熺敓鐨?prompt锛屾彁渚涙洿涓撲笟鐨勮緭鍏ヤ綋楠?
 */
import React, { useState, useEffect, useRef } from 'react';
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
  confirmText = '纭畾',
  cancelText = '鍙栨秷',
}) => {
  const [values, setValues] = useState<Record<string, string>>({});
  const firstInputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null);

  // 鍒濆鍖栬〃鍗曞€?
  useEffect(() => {
    if (isOpen) {
      const initialValues: Record<string, string> = {};
      fields.forEach((field) => {
        initialValues[field.name] = field.defaultValue || '';
      });
      setValues(initialValues);

      // 鑱氱劍绗竴涓緭鍏ユ
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

    // 楠岃瘉蹇呭～瀛楁
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
      {/* 閬僵灞?*/}
      <div
        className="absolute inset-0 bg-black/50 dark:bg-black/60 backdrop-blur-sm animate-fadeIn"
        onClick={onClose}
      />

      {/* 瀵硅瘽妗?*/}
      <div
        className="relative bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 rounded-lg shadow-2xl w-full max-w-md mx-4 animate-scaleIn border border-gray-200 dark:border-gray-700"
        onKeyDown={handleKeyDown}
      >
        {/* 澶撮儴 */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{title}</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 琛ㄥ崟鍐呭 */}
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
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-all bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
                    required={field.required}
                  />
                )}
              </div>
            ))}
          </div>

          {/* 搴曢儴鎸夐挳 */}
          <div className="flex justify-end gap-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              {cancelText}
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 dark:bg-blue-500 rounded-lg hover:bg-blue-700 dark:hover:bg-blue-400 transition-colors shadow-sm hover:shadow-md"
            >
              {confirmText}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default InputDialog;










