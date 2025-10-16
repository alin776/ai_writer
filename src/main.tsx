import React, { Suspense } from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { router } from './router';
import Toast from './components/common/Toast';
import './styles/globals.css';

/**
 * 应用入口文件
 *
 * 功能：
 * - 导入 React 和 ReactDOM
 * - 导入全局样式 globals.css
 * - 使用 RouterProvider 渲染路由
 * - 使用 Suspense 包裹懒加载组件
 * - 添加 Toast 组件
 */

/**
 * Loading 组件
 * 在懒加载组件加载时显示
 */
const LoadingFallback: React.FC = () => (
  <div className="flex items-center justify-center min-h-screen bg-gray-50">
    <div className="flex flex-col items-center space-y-4">
      <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      <p className="text-gray-600">加载中...</p>
    </div>
  </div>
);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Suspense fallback={<LoadingFallback />}>
      <RouterProvider router={router} />
      <Toast />
    </Suspense>
  </React.StrictMode>
);
