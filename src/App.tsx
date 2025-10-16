import React from 'react';
import { RouterProvider } from 'react-router-dom';
import { router } from './router';

/**
 * App 组件 - 应用根组件
 *
 * 功能：
 * - 提供路由配置
 * - 全局状态管理
 */
const App: React.FC = () => {
  return <RouterProvider router={router} />;
};

export default App;
