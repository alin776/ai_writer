import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import zhCN from './locales/zh-CN.json';
import zhTW from './locales/zh-TW.json';
import enUS from './locales/en-US.json';

export type LanguageCode = 'zh-CN' | 'zh-TW' | 'en-US';

export const LANGUAGE_STORAGE_KEY = 'novelaide-language';

export const languages: { code: LanguageCode; name: string; nativeName: string }[] = [
  { code: 'zh-CN', name: 'Simplified Chinese', nativeName: '简体中文' },
  { code: 'zh-TW', name: 'Traditional Chinese', nativeName: '繁體中文' },
  { code: 'en-US', name: 'English', nativeName: 'English' },
];

const resources = {
  'zh-CN': { translation: zhCN },
  'zh-TW': { translation: zhTW },
  'en-US': { translation: enUS },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'zh-CN',
    debug: import.meta.env.DEV,

    detection: {
      order: ['localStorage', 'navigator'],
      lookupLocalStorage: LANGUAGE_STORAGE_KEY,
      caches: ['localStorage'],
    },

    interpolation: {
      escapeValue: false,
    },

    react: {
      useSuspense: false,
    },
  });

export default i18n;
