import React, { Suspense, useEffect } from 'react';
import { RouterProvider } from 'react-router-dom';
import { router } from './router';
import Toast from './components/common/Toast';
import { useAuthStore } from './store/authStore';
import { useTheme } from './hooks/useTheme';
import { useTokenExpiryWarning } from './hooks/useTokenExpiryWarning';

const LoadingFallback: React.FC = () => (
  <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
    <div className="flex flex-col items-center space-y-4">
      <div className="w-16 h-16 bg-gray-900 dark:bg-gray-800 rounded-xl flex items-center justify-center">
        <img src="/logo-icon.svg" alt="文枢AI" style={{ width: '48px', height: '48px', filter: 'brightness(0) invert(1)' }} />
      </div>
      <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      <p className="text-gray-600 dark:text-gray-300">加载中...</p>
    </div>
  </div>
);

const App: React.FC = () => {
  const { user } = useAuthStore();
  const userTheme = user?.preferences?.theme;
  const { applyTheme } = useTheme(userTheme);

  // 启用 token 过期提醒
  useTokenExpiryWarning();

  useEffect(() => {
    if (userTheme) {
      applyTheme(userTheme);
    }
  }, [applyTheme, userTheme]);

  return (
    <Suspense fallback={<LoadingFallback />}>
      <RouterProvider router={router} />
      <Toast />
    </Suspense>
  );
};

export default App;
