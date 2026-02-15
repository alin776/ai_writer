import { useCallback, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { LANGUAGE_STORAGE_KEY, type LanguageCode } from '../i18n';

const LANGUAGE_CHANGE_EVENT = 'language-preference-change';

/**
 * 获取存储的语言偏好
 */
export const getStoredLanguage = (): LanguageCode => {
  if (typeof window === 'undefined') return 'zh-CN';
  const stored = window.localStorage.getItem(LANGUAGE_STORAGE_KEY) as LanguageCode | null;
  return stored ?? 'zh-CN';
};

/**
 * 获取浏览器语言
 */
const getBrowserLanguage = (): LanguageCode => {
  if (typeof navigator === 'undefined') return 'zh-CN';

  const browserLang = navigator.language;

  if (browserLang.startsWith('zh')) {
    // 区分简体和繁体
    if (browserLang === 'zh-TW' || browserLang === 'zh-HK' || browserLang === 'zh-Hant') {
      return 'zh-TW';
    }
    return 'zh-CN';
  }

  if (browserLang.startsWith('en')) {
    return 'en-US';
  }

  // 默认简体中文
  return 'zh-CN';
};

interface UseLanguageOptions {
  /** 初始语言（优先级：传入值 > localStorage > 浏览器语言） */
  initialLanguage?: LanguageCode;
  /** 是否持久化到 localStorage */
  persist?: boolean;
}

interface UseLanguageReturn {
  /** 当前语言代码 */
  language: LanguageCode;
  /** 切换语言 */
  changeLanguage: (lang: LanguageCode) => void;
  /** 翻译函数 */
  t: (key: string, options?: Record<string, unknown>) => string;
}

/**
 * 语言管理 Hook
 *
 * @example
 * ```tsx
 * const { language, changeLanguage, t } = useLanguage();
 *
 * // 切换语言
 * changeLanguage('en-US');
 *
 * // 使用翻译
 * <h1>{t('settings.title')}</h1>
 * ```
 */
export function useLanguage(options: UseLanguageOptions = {}): UseLanguageReturn {
  const { initialLanguage, persist = true } = options;
  const { i18n, t } = useTranslation();

  // 确定初始语言
  const resolvedInitial = (): LanguageCode => {
    if (initialLanguage) return initialLanguage;

    const stored = getStoredLanguage();
    if (stored) return stored;

    return getBrowserLanguage();
  };

  const [language, setLanguage] = useState<LanguageCode>(resolvedInitial);

  // 切换语言
  const changeLanguage = useCallback(
    (lang: LanguageCode) => {
      setLanguage(lang);
      i18n.changeLanguage(lang);

      if (persist && typeof window !== 'undefined') {
        window.localStorage.setItem(LANGUAGE_STORAGE_KEY, lang);

        // 触发自定义事件，让其他 useLanguage 实例同步状态
        window.dispatchEvent(
          new CustomEvent(LANGUAGE_CHANGE_EVENT, {
            detail: { language: lang },
          })
        );
      }
    },
    [i18n, persist]
  );

  // 监听语言变化事件，实现跨组件同步
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleLanguageChange = (event: CustomEvent<{ language: LanguageCode }>) => {
      const { language: newLang } = event.detail;
      setLanguage(newLang);
    };

    window.addEventListener(LANGUAGE_CHANGE_EVENT, handleLanguageChange as EventListener);

    return () => {
      window.removeEventListener(LANGUAGE_CHANGE_EVENT, handleLanguageChange as EventListener);
    };
  }, []);

  // 初始化时同步 i18n 语言
  useEffect(() => {
    const initial = resolvedInitial();
    if (i18n.language !== initial) {
      i18n.changeLanguage(initial);
    }
  }, []);

  // 监听 i18n 语言变化
  useEffect(() => {
    const handleI18nChange = (lng: string) => {
      setLanguage(lng as LanguageCode);
    };

    i18n.on('languageChanged', handleI18nChange);

    return () => {
      i18n.off('languageChanged', handleI18nChange);
    };
  }, [i18n]);

  return {
    language,
    changeLanguage,
    t,
  };
}

export default useLanguage;
