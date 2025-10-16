import React, { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import Header from './Header';
import Sidebar from './Sidebar';
import Loading from '../common/Loading';

/**
 * AuthLayout 组件 - 需要认证的页面布局
 *
 * 功能：
 * - 检查用户登录状态
 * - 未登录用户重定向到登录页
 * - 已登录用户显示完整布局（Header + Sidebar + 内容区域）
 * - 使用 Outlet 渲染子路由内容
 */
export const AuthLayout: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuthStore();
  const [isChecking, setIsChecking] = React.useState(true);

  /**
   * 检查认证状态
   */
  useEffect(() => {
    // 模拟认证检查过程
    const checkAuth = async () => {
      // 给一个短暂的延迟，避免闪烁
      await new Promise((resolve) => setTimeout(resolve, 100));

      if (!isAuthenticated || !user) {
        // 未登录，重定向到登录页
        navigate('/login', { replace: true });
      } else {
        // 已登录，显示布局
        setIsChecking(false);
      }
    };

    checkAuth();
  }, [isAuthenticated, user, navigate]);

  /**
   * 正在检查认证状态时显示加载中
   */
  if (isChecking) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <Loading size="lg" text="加载中..." />
      </div>
    );
  }

  /**
   * 已认证，显示完整布局
   */
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* 顶部导航栏 */}
      <Header />

      {/* 主要内容区域 */}
      <div className="flex flex-1 overflow-hidden">
        {/* 侧边栏 */}
        <Sidebar />

        {/* 内容区域 */}
        <main className="flex-1 overflow-y-auto">
          <div className="container mx-auto p-6">
            {/* 使用 Outlet 渲染子路由 */}
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default AuthLayout;
