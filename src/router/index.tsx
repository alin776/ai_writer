import React from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AuthLayout, AdminLayout, ProtectedRoute } from '../components/layout';
import { ErrorBoundary } from '../components/common';

/**
 * 路由配置文件
 *
 * 使用 react-router-dom v7 的 createBrowserRouter
 * 配置应用的所有路由规则
 */

/**
 * 懒加载视图组件
 * 使用 React.lazy 进行代码分割，优化初始加载性能
 */
const HomeView = React.lazy(() => import('../views/HomeView'));
const AuthView = React.lazy(() => import('../views/AuthView'));
const WorksView = React.lazy(() => import('../views/WorksView'));
const CreateWorkView = React.lazy(() => import('../views/CreateWorkView'));
const WorkDetailView = React.lazy(() => import('../views/WorkDetailView'));
const WorldviewGraphFullscreen = React.lazy(() => import('../views/WorldviewGraphFullscreen'));
const EditorView = React.lazy(() => import('../views/EditorView'));
const AdminDashboardView = React.lazy(() => import('../views/AdminDashboardView'));
const AdminUsersView = React.lazy(() => import('../views/AdminUsersView'));
const AdminAIModelsView = React.lazy(() => import('../views/AdminAIModelsView'));
const AdminCostView = React.lazy(() => import('../views/AdminCostView'));
const AdminInvitationsView = React.lazy(() => import('../views/AdminInvitationsView'));
const AdminCreditsView = React.lazy(() => import('../views/AdminCreditsView'));
const SettingsView = React.lazy(() => import('../views/SettingsView'));
const KnowledgeView = React.lazy(() => import('../views/KnowledgeView'));
const ServiceCreditsView = React.lazy(() => import('../views/ServiceCreditsView'));
const ServiceUsageView = React.lazy(() => import('../views/ServiceUsageView'));
const ServiceObtainView = React.lazy(() => import('../views/ServiceObtainView'));
const NotFoundView = React.lazy(() => import('../views/NotFoundView'));

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

/**
 * Suspense 包装组件
 * 为懒加载组件提供加载状态
 */
const SuspenseWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <React.Suspense fallback={<LoadingFallback />}>{children}</React.Suspense>
);

/**
 * 路由配置
 */
export const router = createBrowserRouter([
  /**
   * 首页（公开）
   */
  {
    path: '/',
    element: (
      <SuspenseWrapper>
        <HomeView />
      </SuspenseWrapper>
    ),
  },

  /**
   * 公开路由（无需认证）
   */
  {
    path: '/login',
    element: (
      <SuspenseWrapper>
        <AuthView />
      </SuspenseWrapper>
    ),
  },
  {
    path: '/register',
    element: (
      <SuspenseWrapper>
        <AuthView />
      </SuspenseWrapper>
    ),
  },
  {
    path: '/auth',
    element: (
      <SuspenseWrapper>
        <AuthView />
      </SuspenseWrapper>
    ),
  },

  /**
   * 创建作品路由（需要认证但无布局）
   * 独立路由，不显示侧边栏和顶部导航栏
   */
  {
    path: '/works/create',
    element: (
      <ProtectedRoute>
        <SuspenseWrapper>
          <CreateWorkView />
        </SuspenseWrapper>
      </ProtectedRoute>
    ),
  },

  /**
   * 需要认证的路由
   * 使用 AuthLayout 进行保护
   */
  {
    element: <AuthLayout />,
    children: [
      /**
       * 作品相关路由
       */
      {
        path: '/works',
        element: (
          <SuspenseWrapper>
            <WorksView />
          </SuspenseWrapper>
        ),
      },
      {
        path: '/works/:workId',
        element: (
          <SuspenseWrapper>
            <WorkDetailView />
          </SuspenseWrapper>
        ),
      },
      {
        path: '/worldview/:workId',
        element: (
          <SuspenseWrapper>
            <WorldviewGraphFullscreen />
          </SuspenseWrapper>
        ),
      },

      /**
       * 编辑器路由
       */
      {
        path: '/editor',
        element: (
          <SuspenseWrapper>
            <EditorView />
          </SuspenseWrapper>
        ),
      },
      {
        path: '/editor/:chapterId',
        element: (
          <SuspenseWrapper>
            <EditorView />
          </SuspenseWrapper>
        ),
      },

      /**
       * 设置路由
       */
      {
        path: '/settings',
        element: (
          <SuspenseWrapper>
            <SettingsView />
          </SuspenseWrapper>
        ),
      },

      /**
       * 知识库路由
       */
      {
        path: '/knowledge',
        element: (
          <SuspenseWrapper>
            <KnowledgeView />
          </SuspenseWrapper>
        ),
      },

      /**
       * 我的服务路由
       */
      {
        path: '/service/credits',
        element: (
          <SuspenseWrapper>
            <ServiceCreditsView />
          </SuspenseWrapper>
        ),
      },
      {
        path: '/service/usage',
        element: (
          <SuspenseWrapper>
            <ServiceUsageView />
          </SuspenseWrapper>
        ),
      },
      {
        path: '/service/obtain',
        element: (
          <SuspenseWrapper>
            <ServiceObtainView />
          </SuspenseWrapper>
        ),
      },
    ],
  },

  /**
   * 管理后台路由（独立布局）
   * 需要 admin 权限，使用 AdminLayout 守卫
   */
  {
    element: <AdminLayout />,
    children: [
      {
        path: '/admin',
        children: [
          {
            index: true,
            element: <Navigate to="/admin/dashboard" replace />,
          },
          {
            path: 'dashboard',
            element: (
              <SuspenseWrapper>
                <AdminDashboardView />
              </SuspenseWrapper>
            ),
          },
          {
            path: 'users',
            element: (
              <SuspenseWrapper>
                <AdminUsersView />
              </SuspenseWrapper>
            ),
          },
          {
            path: 'ai-models',
            element: (
              <SuspenseWrapper>
                <AdminAIModelsView />
              </SuspenseWrapper>
            ),
          },
          {
            path: 'cost',
            element: (
              <SuspenseWrapper>
                <AdminCostView />
              </SuspenseWrapper>
            ),
          },
          {
            path: 'invitations',
            element: (
              <ErrorBoundary>
                <SuspenseWrapper>
                  <AdminInvitationsView />
                </SuspenseWrapper>
              </ErrorBoundary>
            ),
          },
          {
            path: 'credits',
            element: (
              <ErrorBoundary>
                <SuspenseWrapper>
                  <AdminCreditsView />
                </SuspenseWrapper>
              </ErrorBoundary>
            ),
          },
        ],
      },
    ],
  },

  /**
   * 404 页面
   * 匹配所有未定义的路由
   */
  {
    path: '*',
    element: (
      <SuspenseWrapper>
        <NotFoundView />
      </SuspenseWrapper>
    ),
  },
]);

export default router;
