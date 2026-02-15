import React, { useEffect } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import Sidebar from './Sidebar';
import Loading from '../common/Loading';
import { useNotificationWebSocket } from '../../hooks/useNotificationWebSocket';
import NotificationModal from '../notifications/NotificationModal';

/**
 * AuthLayout 组件 - 需要认证的页面布局
 *
 * 功能：
 * - 检查用户登录状态
 * - 未登录用户重定向到登录页
 * - 已登录用户显示完整布局（Header + Sidebar + 内容区域）
 * - 使用 Outlet 渲染子路由内容
 * - 根据路由条件渲染是否添加 padding
 */
export const AuthLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, user, hasHydrated } = useAuthStore();
  const [isChecking, setIsChecking] = React.useState(true);

  // 启用通知 WebSocket 和弹窗
  const { showModal, modalNotification, closeModal } = useNotificationWebSocket();

  // 检查是否是需要全屏显示的页面（不需要 padding）
  const isFullWidthPage = location.pathname === '/works' ||
                          location.pathname.startsWith('/works/') ||
                          location.pathname.startsWith('/editor/') ||
                          location.pathname.startsWith('/worldview/') ||
                          location.pathname.startsWith('/worldview-graph/') ||
                          location.pathname.startsWith('/humanize') ||
                          location.pathname.startsWith('/knowledge') ||
                          location.pathname.startsWith('/library') ||
                          location.pathname.startsWith('/notifications') ||
                          location.pathname.startsWith('/settings') ||
                          location.pathname.startsWith('/channels') ||
                          location.pathname.startsWith('/user/');

  /**
   * 检查认证状态
   */
  useEffect(() => {
    if (!hasHydrated) return;

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
  }, [hasHydrated, isAuthenticated, user, navigate]);

  /**
   * 正在检查认证状态时显示加载中
   */
  if (!hasHydrated || isChecking) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-white dark:bg-gray-950">
        <Loading size="lg" text="加载中..." />
      </div>
    );
  }

  /**
   * 已认证，显示完整布局
   */
  return (
    <div className="flex flex-col h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      {/* 主要内容区域 */}
      <div className="flex flex-1 overflow-hidden">
        {/* 侧边栏 */}
        <Sidebar />

        {/* 内容区域 */}
        <main className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900">
          {isFullWidthPage ? (
            /* 全屏页面：不添加 container 和 padding */
            <Outlet />
          ) : (
            /* 普通页面：添加 container 和 padding */
            <div className="container mx-auto py-6 px-4">
              <Outlet />
            </div>
          )}
        </main>
      </div>

      {/* 通知弹窗 */}
      {showModal && modalNotification && (
        <NotificationModal
          notification={modalNotification}
          onClose={closeModal}
        />
      )}
    </div>
  );
};

export default AuthLayout;
