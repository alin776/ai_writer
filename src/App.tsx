import React, { Suspense, useEffect } from 'react';
import { RouterProvider } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { router } from './router';
import Toast from './components/common/Toast';
import { useAuthStore } from './store/authStore';
import { useGlobalStore } from './store/globalStore';
import { useTheme } from './hooks/useTheme';
import { useTokenExpiryWarning } from './hooks/useTokenExpiryWarning';
import './i18n';

// 导入存储调试工具（开发模式）
if (import.meta.env.DEV) {
  import('./utils/storageDebug');
}

const LoadingFallback: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      <div className="flex flex-col items-center space-y-4">
        <div className="w-16 h-16 bg-gray-900 dark:bg-gray-800 rounded-full flex items-center justify-center">
          <img src="/logo-icon.svg" alt="文枢AI" style={{ width: '48px', height: '48px', filter: 'brightness(0) invert(1)' }} />
        </div>
        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-gray-600 dark:text-gray-300">{t('common.loading')}</p>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  const { user } = useAuthStore();
  const { error: showErrorToast } = useGlobalStore();
  const { i18n } = useTranslation();
  const userTheme = user?.preferences?.theme;
  const userLanguage = user?.preferences?.language;
  const { applyTheme } = useTheme(userTheme);

  // 启用 token 过期提醒
  useTokenExpiryWarning();

  // 监听 localStorage 配额超限事件
  useEffect(() => {
    const handleStorageQuotaExceeded = (event: Event) => {
      const customEvent = event as CustomEvent<{ store: string; message: string }>;
      const { store, message } = customEvent.detail;

      if (store === 'auth') {
        showErrorToast(
          '存储空间不足：认证信息无法保存，刷新页面可能需要重新登录。请清理浏览器缓存后重试。',
          8000
        );
      }
    };

    window.addEventListener('storage-quota-exceeded', handleStorageQuotaExceeded);
    return () => {
      window.removeEventListener('storage-quota-exceeded', handleStorageQuotaExceeded);
    };
  }, [showErrorToast]);

  // 应用用户主题
  useEffect(() => {
    if (userTheme) {
      applyTheme(userTheme);
    }
  }, [applyTheme, userTheme]);

  // 应用用户语言
  useEffect(() => {
    if (userLanguage && i18n.language !== userLanguage) {
      i18n.changeLanguage(userLanguage);
    }
  }, [i18n, userLanguage]);

  return (
    <Suspense fallback={<LoadingFallback />}>
      <RouterProvider router={router} />
      <Toast />
    </Suspense>
  );
};

export default App;
