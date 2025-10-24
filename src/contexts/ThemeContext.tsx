import React, { createContext, useContext, useEffect, useState, useCallback, ReactNode } from 'react';

export type ThemePreference = 'light' | 'dark' | 'auto';
type ThemeMode = 'light' | 'dark';

interface ApplyThemeOptions {
  persist?: boolean;
}

interface ThemeContextValue {
  preference: ThemePreference;
  effectiveTheme: ThemeMode;
  applyTheme: (theme: ThemePreference, options?: ApplyThemeOptions) => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

const STORAGE_KEY = 'novelaide-theme-preference';
const DARK_MEDIA_QUERY = '(prefers-color-scheme: dark)';

const getSystemTheme = (): ThemeMode => {
  if (typeof window === 'undefined') return 'light';
  return window.matchMedia(DARK_MEDIA_QUERY).matches ? 'dark' : 'light';
};

const applyThemeClass = (theme: ThemeMode) => {
  if (typeof document === 'undefined') return;

  // Tailwind dark mode: 只需要切换 'dark' 类
  // 深色模式: 添加 'dark' 类
  // 浅色模式: 移除 'dark' 类
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
    // 同时强制设置 body 背景色
    document.body.style.backgroundColor = '';  // 让 CSS 变量生效
  } else {
    document.documentElement.classList.remove('dark');
    // 强制移除可能残留的内联样式
    document.body.style.backgroundColor = '';
  }

  // 强制浏览器重绘
  void document.documentElement.offsetHeight;

  console.log('[applyThemeClass] DOM 更新:', {
    theme,
    htmlClasses: document.documentElement.className,
    bodyBgColor: window.getComputedStyle(document.body).backgroundColor,
  });
};

export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // 从 localStorage 读取初始主题
  const getInitialTheme = (): ThemePreference => {
    if (typeof window === 'undefined') return 'light';
    const stored = window.localStorage.getItem(STORAGE_KEY) as ThemePreference | null;
    return stored ?? 'light';
  };

  const [preference, setPreference] = useState<ThemePreference>(getInitialTheme);
  const [effectiveTheme, setEffectiveTheme] = useState<ThemeMode>(() => {
    const initial = getInitialTheme();
    return initial === 'auto' ? getSystemTheme() : initial;
  });

  // 应用主题函数
  const applyTheme = useCallback((nextPreference: ThemePreference, options: ApplyThemeOptions = {}) => {
    const { persist = true } = options;

    setPreference(nextPreference);

    // 计算实际要应用的主题
    const targetTheme = nextPreference === 'auto' ? getSystemTheme() : nextPreference;
    setEffectiveTheme(targetTheme);

    // 立即应用到 DOM
    applyThemeClass(targetTheme);

    // 持久化到 localStorage
    if (persist && typeof window !== 'undefined') {
      window.localStorage.setItem(STORAGE_KEY, nextPreference);
    }

    console.log('[ThemeProvider] 主题已切换:', {
      preference: nextPreference,
      effectiveTheme: targetTheme,
      persist,
    });
  }, []);

  // 初始化时应用主题
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const initialTheme = preference === 'auto' ? getSystemTheme() : preference;
    applyThemeClass(initialTheme);

    console.log('[ThemeProvider] 初始化主题:', {
      preference,
      effectiveTheme: initialTheme,
    });
  }, []); // 只在挂载时执行一次

  // 监听系统主题变化
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const mediaQuery = window.matchMedia(DARK_MEDIA_QUERY);
    const handleSystemThemeChange = (event: MediaQueryListEvent) => {
      if (preference === 'auto') {
        const nextTheme = event.matches ? 'dark' : 'light';
        setEffectiveTheme(nextTheme);
        applyThemeClass(nextTheme);

        console.log('[ThemeProvider] 系统主题变化:', nextTheme);
      }
    };

    mediaQuery.addEventListener('change', handleSystemThemeChange);
    return () => {
      mediaQuery.removeEventListener('change', handleSystemThemeChange);
    };
  }, [preference]);

  return (
    <ThemeContext.Provider value={{ preference, effectiveTheme, applyTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
