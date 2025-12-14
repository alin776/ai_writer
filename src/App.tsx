import React, { Suspense, useEffect } from 'react';
import { RouterProvider } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { router } from './router';
import Toast from './components/common/Toast';
import { useAuthStore } from './store/authStore';
import { useTheme } from './hooks/useTheme';
import './i18n';

const LoadingFallback: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      <div className="flex flex-col items-center space-y-4">
        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-gray-600 dark:text-gray-300">{t('common.loading')}</p>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  const { user } = useAuthStore();
  const { i18n } = useTranslation();
  const userTheme = user?.preferences?.theme;
  const userLanguage = user?.preferences?.language;
  const { applyTheme } = useTheme(userTheme);

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
