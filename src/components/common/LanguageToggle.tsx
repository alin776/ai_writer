/**
 * 语言切换组件
 * 提供一个地球图标按钮，点击后显示语言选择下拉菜单
 */
import React, { useState, useRef, useEffect } from 'react';
import { Globe, Check } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useLanguage } from '@/hooks/useLanguage';
import { languages, type LanguageCode } from '@/i18n';
import { useAuthStore } from '@/store/authStore';
import { DataService } from '@/services/DataService';

interface LanguageToggleProps {
  className?: string;
}

const LanguageToggle: React.FC<LanguageToggleProps> = ({ className = '' }) => {
  const { language, changeLanguage } = useLanguage();
  const { t } = useTranslation();
  const { user, setUser } = useAuthStore();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // 点击外部关闭下拉菜单
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  // 保存语言到后端
  const saveLanguageToBackend = async (lang: LanguageCode) => {
    if (!user) return;

    try {
      const currentPreferences = user.preferences || {
        theme: 'light',
        language: 'zh-CN',
        fontSize: 'medium' as const,
        autoSave: true,
        autoSaveInterval: 30,
        aiAutoComplete: false,
      };

      const updatedPreferences = await DataService.updatePreferences({
        ...currentPreferences,
        language: lang,
      });

      // 更新 authStore 中的用户偏好
      setUser({
        ...user,
        preferences: updatedPreferences,
      });
    } catch (error) {
      console.error('保存语言设置失败:', error);
    }
  };

  const handleLanguageChange = (lang: LanguageCode) => {
    changeLanguage(lang);
    saveLanguageToBackend(lang);
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`relative p-1.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800 rounded transition-colors ${className}`}
        title={t('header.actions.switchLanguage', '切换语言')}
        aria-label={t('header.actions.switchLanguage', '切换语言')}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
      >
        <Globe className="w-4 h-4" />
      </button>

      {/* 语言选择下拉菜单 */}
      {isOpen && (
        <>
          {/* 遮罩层 */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />

          {/* 下拉菜单 */}
          <div className="absolute right-0 mt-1.5 w-36 bg-white dark:bg-slate-900 rounded border border-gray-200 dark:border-slate-700 py-1 z-50 shadow-lg">
            {languages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => handleLanguageChange(lang.code)}
                className={`flex items-center justify-between w-full px-3 py-2 text-sm transition-colors ${
                  language === lang.code
                    ? 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20'
                    : 'text-gray-700 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-slate-800'
                }`}
                role="option"
                aria-selected={language === lang.code}
              >
                <span>{lang.nativeName}</span>
                {language === lang.code && (
                  <Check className="w-4 h-4" />
                )}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default LanguageToggle;
