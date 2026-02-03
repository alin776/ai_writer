import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import AdminSidebar from './AdminSidebar';

/**
 * AdminLayout 组件 - 管理后台布局
 *
 * 功能：
 * - 检查用户是否为管理员
 * - 非管理员重定向到作品页
 * - 管理员显示管理后台布局（AdminSidebar + 内容区域）
 */
export const AdminLayout: React.FC = () => {
  const { user } = useAuthStore();

  /**
   * 权限检查：只有管理员可以访问
   */
  if (!user?.isAdmin) {
    return <Navigate to="/works" replace />;
  }

  /**
   * 管理员布局
   */
  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      {/* 主要内容区域 */}
      <div className="flex flex-1 overflow-hidden">
        {/* 管理后台侧边栏 */}
        <AdminSidebar />

        {/* 内容区域 */}
        <main className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900">
          <div className="container mx-auto">
            {/* 使用 Outlet 渲染子路由 */}
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;
