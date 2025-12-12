import React from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AuthLayout, AdminLayout, ProtectedRoute } from '../components/layout';
import { ErrorBoundary } from '../components/common';

const HomeView = React.lazy(() => import('../views/HomeView'));
const AuthView = React.lazy(() => import('../views/AuthView'));
const WorksView = React.lazy(() => import('../views/WorksView'));
const CreateWorkView = React.lazy(() => import('../views/CreateWorkView'));
const WorkDetailView = React.lazy(() => import('../views/WorkDetailView'));
const WorldviewGraphFullscreen = React.lazy(() => import('../views/WorldviewGraphFullscreen'));
const HumanizeView = React.lazy(() => import('../views/HumanizeView'));
const HumanizeHistoryView = React.lazy(() => import('../views/HumanizeHistoryView'));
const HumanizeSessionDetail = React.lazy(() => import('../views/HumanizeHistoryView/SessionDetail'));
const ServiceCreditsView = React.lazy(() => import('../views/ServiceCreditsView'));
const ServiceUsageView = React.lazy(() => import('../views/ServiceUsageView'));
const ServiceObtainView = React.lazy(() => import('../views/ServiceObtainView'));
const AdminDashboardView = React.lazy(() => import('../views/AdminDashboardView'));
const AdminUsersView = React.lazy(() => import('../views/AdminUsersView'));
const AdminAIModelsView = React.lazy(() => import('../views/AdminAIModelsView'));
const AdminCostView = React.lazy(() => import('../views/AdminCostView'));
const AdminInvitationsView = React.lazy(() => import('../views/AdminInvitationsView'));
const AdminCreditsView = React.lazy(() => import('../views/AdminCreditsView'));
const AdminNotificationsView = React.lazy(() => import('../views/AdminNotificationsView'));
const SettingsView = React.lazy(() => import('../views/SettingsView'));
const ChangePasswordView = React.lazy(() => import('../views/ChangePasswordView'));
const ChangeEmailView = React.lazy(() => import('../views/ChangeEmailView'));
const ForgotPasswordView = React.lazy(() => import('../views/ForgotPasswordView'));
const KnowledgeView = React.lazy(() => import('../views/KnowledgeView'));
const NotificationCenter = React.lazy(() => import('../pages/NotificationCenter'));
const NotFoundView = React.lazy(() => import('../views/NotFoundView'));

const LoadingFallback: React.FC = () => (
  <div className="flex items-center justify-center min-h-screen bg-gray-50">
    <div className="flex flex-col items-center space-y-4">
      <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      <p className="text-gray-600">加载中...</p>
    </div>
  </div>
);

const SuspenseWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <React.Suspense fallback={<LoadingFallback />}>{children}</React.Suspense>
);

export const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <SuspenseWrapper>
        <HomeView />
      </SuspenseWrapper>
    ),
  },
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
    path: '/forgot-password',
    element: (
      <SuspenseWrapper>
        <ForgotPasswordView />
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
  {
    element: <AuthLayout />,
    children: [
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
      {
        path: '/settings',
        element: (
          <SuspenseWrapper>
            <SettingsView />
          </SuspenseWrapper>
        ),
      },
      {
        path: '/settings/change-password',
        element: (
          <SuspenseWrapper>
            <ChangePasswordView />
          </SuspenseWrapper>
        ),
      },
      {
        path: '/settings/change-email',
        element: (
          <SuspenseWrapper>
            <ChangeEmailView />
          </SuspenseWrapper>
        ),
      },
      {
        path: '/knowledge',
        element: (
          <SuspenseWrapper>
            <KnowledgeView />
          </SuspenseWrapper>
        ),
      },
      {
        path: '/humanize',
        element: (
          <SuspenseWrapper>
            <HumanizeView />
          </SuspenseWrapper>
        ),
      },
      {
        path: '/humanize/history',
        element: (
          <SuspenseWrapper>
            <HumanizeHistoryView />
          </SuspenseWrapper>
        ),
      },
      {
        path: '/humanize/history/:sessionId',
        element: (
          <SuspenseWrapper>
            <HumanizeSessionDetail />
          </SuspenseWrapper>
        ),
      },
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
      {
        path: '/notifications',
        element: (
          <SuspenseWrapper>
            <NotificationCenter />
          </SuspenseWrapper>
        ),
      },
    ],
  },
  {
    element: <AdminLayout />,
    children: [
      {
        path: '/admin',
        children: [
          { index: true, element: <Navigate to="/admin/dashboard" replace /> },
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
          {
            path: 'notifications',
            element: (
              <SuspenseWrapper>
                <AdminNotificationsView />
              </SuspenseWrapper>
            ),
          },
        ],
      },
    ],
  },
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
