import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import Loading from '../common/Loading';

/**
 * ProtectedRoute 组件 - 认证保护（无布局）
 *
 * 功能：
 * - 检查用户登录状态
 * - 未登录用户重定向到登录页
 * - 已登录用户直接渲染子组件（无Header和Sidebar）
 */
interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const navigate = useNavigate();
  const { isAuthenticated, user, login, hasHydrated } = useAuthStore();
  const [isChecking, setIsChecking] = React.useState(true);
  const useMock = import.meta.env.VITE_USE_MOCK === 'true';

  /**
   * 检查认证状态
   */
  useEffect(() => {
    if (!hasHydrated) return;

    const checkAuth = async () => {
      // 给一个短暂的延迟，避免闪烁
      await new Promise((resolve) => setTimeout(resolve, 100));

      if (!isAuthenticated || !user) {
        if (useMock) {
          // Mock 模式下自动登录一个本地用户，避免卡在登录页
          const now = new Date().toISOString();
          login(
            {
              id: 'mock-user',
              username: 'mockuser',
              name: 'Mock User',
              email: 'mock@example.com',
              isActive: true,
              isAdmin: true,
              isVerified: true,
              createdAt: now,
              updatedAt: now,
            },
            'mock-token'
          );
          setIsChecking(false);
          return;
        }
        // 未登录，重定向到登录页
        navigate('/login', { replace: true });
      } else {
        // 已登录，显示内容
        setIsChecking(false);
      }
    };

    checkAuth();
  }, [hasHydrated, isAuthenticated, user, navigate, useMock, login]);

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
   * 已认证，直接渲染子组件
   */
  return <>{children}</>;
};

export default ProtectedRoute;
