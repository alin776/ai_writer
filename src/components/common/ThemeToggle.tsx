/**
 * 主题切换按钮组件
 * 支持 View Transitions API 实现从按钮位置向外扩散的动画效果
 */
import React, { useRef } from 'react';
import { Sun, Moon } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useTheme, type ThemePreference } from '@/hooks/useTheme';
import { useAuthStore } from '@/store/authStore';
import { DataService } from '@/services/DataService';

interface ThemeToggleProps {
  className?: string;
}

const ThemeToggle: React.FC<ThemeToggleProps> = ({ className = '' }) => {
  const { effectiveTheme, applyTheme } = useTheme();
  const { user, setUser } = useAuthStore();
  const { t } = useTranslation();
  const buttonRef = useRef<HTMLButtonElement>(null);

  const toggleTheme = async () => {
    const newTheme: ThemePreference = effectiveTheme === 'dark' ? 'light' : 'dark';

    // 检查浏览器是否支持 View Transitions API
    if (!document.startViewTransition) {
      applyTheme(newTheme);
      saveThemeToBackend(newTheme);
      return;
    }

    // 获取按钮位置，用于计算动画起点
    const button = buttonRef.current;
    if (!button) {
      applyTheme(newTheme);
      saveThemeToBackend(newTheme);
      return;
    }

    const rect = button.getBoundingClientRect();
    const x = rect.left + rect.width / 2;
    const y = rect.top + rect.height / 2;

    // 计算需要覆盖整个屏幕的最大半径
    const endRadius = Math.hypot(
      Math.max(x, window.innerWidth - x),
      Math.max(y, window.innerHeight - y)
    );

    // 设置 CSS 变量，供动画使用
    document.documentElement.style.setProperty('--theme-toggle-x', `${x}px`);
    document.documentElement.style.setProperty('--theme-toggle-y', `${y}px`);
    document.documentElement.style.setProperty('--theme-toggle-radius', `${endRadius}px`);

    // 使用 View Transitions API
    const transition = document.startViewTransition(() => {
      applyTheme(newTheme);
    });

    // 等待动画完成后保存到后端
    await transition.finished;
    saveThemeToBackend(newTheme);
  };

  // 保存主题到后端并更新 authStore
  const saveThemeToBackend = async (theme: ThemePreference) => {
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
        theme,
      });

      // 更新 authStore 中的用户偏好
      setUser({
        ...user,
        preferences: updatedPreferences,
      });
    } catch (error) {
      console.error('保存主题设置失败:', error);
    }
  };

  const isDark = effectiveTheme === 'dark';
  const themeLabel = isDark
    ? t('settings.preferences.appearance.light')
    : t('settings.preferences.appearance.dark');

  return (
    <button
      ref={buttonRef}
      onClick={toggleTheme}
      className={`relative p-1.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800 rounded transition-colors ${className}`}
      title={themeLabel}
      aria-label={themeLabel}
    >
      <div className="relative w-4 h-4">
        {/* 太阳图标 */}
        <Sun
          className={`absolute inset-0 w-4 h-4 transition-all duration-300 ${
            isDark
              ? 'opacity-0 rotate-90 scale-0'
              : 'opacity-100 rotate-0 scale-100'
          }`}
        />
        {/* 月亮图标 */}
        <Moon
          className={`absolute inset-0 w-4 h-4 transition-all duration-300 ${
            isDark
              ? 'opacity-100 rotate-0 scale-100'
              : 'opacity-0 -rotate-90 scale-0'
          }`}
        />
      </div>
    </button>
  );
};

export default ThemeToggle;
