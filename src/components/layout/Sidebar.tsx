import React, { useMemo, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  BookOpen,
  Settings,
  ChevronLeft,
  LayoutDashboard,
  Users,
  Cpu,
  DollarSign,
  Library,
  Wallet,
  BarChart3,
  Gift,
  ChevronDown,
  Wand2,
  Bell,
  Trophy,
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import clsx from 'clsx';

interface NavItem {
  id: string;
  labelKey: string;
  icon: React.ComponentType<{ className?: string }>;
  path: string;
  tooltip?: string;
  roles?: string[];
}

const mainNavItemsConfig: NavItem[] = [
  { id: 'works', labelKey: 'sidebar.nav.works', icon: BookOpen, path: '/works' },
  { id: 'knowledge', labelKey: 'sidebar.nav.knowledge', icon: Library, path: '/knowledge' },
  { id: 'humanize', labelKey: 'sidebar.nav.humanize', icon: Wand2, path: '/humanize' },
];

const serviceNavItemsConfig: NavItem[] = [
  { id: 'tasks', labelKey: 'sidebar.nav.tasks', icon: Trophy, path: '/tasks' },
  { id: 'credits', labelKey: 'sidebar.nav.credits', icon: Wallet, path: '/service/credits' },
  { id: 'usage', labelKey: 'sidebar.nav.usage', icon: BarChart3, path: '/service/usage' },
  { id: 'obtain', labelKey: 'sidebar.nav.obtain', icon: Gift, path: '/service/obtain' },
];

const adminNavItemsConfig: NavItem[] = [
  { id: 'dashboard', labelKey: 'sidebar.nav.dashboard', icon: LayoutDashboard, path: '/admin/dashboard', roles: ['admin'] },
  { id: 'users', labelKey: 'sidebar.nav.users', icon: Users, path: '/admin/users', roles: ['admin'] },
  { id: 'ai-models', labelKey: 'sidebar.nav.aiModels', icon: Cpu, path: '/admin/ai-models', roles: ['admin'] },
  { id: 'cost', labelKey: 'sidebar.nav.cost', icon: DollarSign, path: '/admin/cost', roles: ['admin'] },
  { id: 'notifications-admin', labelKey: 'sidebar.nav.notificationsAdmin', icon: Bell, path: '/admin/notifications', roles: ['admin'] },
  { id: 'tasks-admin', labelKey: 'sidebar.nav.tasksAdmin', icon: Trophy, path: '/admin/tasks', roles: ['admin'] },
];

export const Sidebar: React.FC = () => {
  const location = useLocation();
  const { user } = useAuthStore();
  const { t } = useTranslation();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isServiceExpanded, setIsServiceExpanded] = useState(true);

  const isWorkDetail = location.pathname.startsWith('/works/') && location.pathname !== '/works';

  const dynamicMainNavItems = useMemo(() => {
    return mainNavItemsConfig.map(item =>
      item.id === 'works'
        ? { ...item, labelKey: isWorkDetail ? 'sidebar.nav.workDetail' : 'sidebar.nav.works' }
        : item
    );
  }, [isWorkDetail]);

  const isActive = (path: string) => location.pathname === path || location.pathname.startsWith(`${path}/`);
  const hasPermission = (item: NavItem) => !item.roles?.length || item.roles.includes(user?.role || '');

  const bottomNavItems: NavItem[] = [
    { id: 'notifications', labelKey: 'sidebar.nav.notifications', icon: Bell, path: '/notifications' },
    { id: 'settings', labelKey: 'sidebar.nav.settings', icon: Settings, path: '/settings' },
  ];

  const renderNavItem = (item: NavItem) => {
    if (!hasPermission(item)) return null;
    const Icon = item.icon;
    const active = isActive(item.path);
    const label = t(item.labelKey);
    const tooltip = item.tooltip || label;

    return (
      <Link
        key={item.id}
        to={item.path}
        className={clsx(
          'group relative flex items-center px-3 py-2 rounded transition-all duration-200 !text-gray-900 dark:!text-white',
          active
            ? 'bg-blue-50 dark:bg-blue-900/30'
            : 'hover:bg-gray-100 dark:hover:bg-slate-800',
          isCollapsed ? 'justify-center' : 'space-x-3'
        )}
        title={isCollapsed ? tooltip : undefined}
      >
        {active && <div className="absolute left-0 top-1 bottom-1 w-1 bg-blue-600 dark:bg-blue-400 rounded-r"></div>}
        <Icon className={clsx('flex-shrink-0', isCollapsed ? 'w-5 h-5' : 'w-4 h-4', 'text-gray-900 dark:text-white')} />
        {!isCollapsed && <span className="text-sm font-medium">{label}</span>}
        {isCollapsed && (
          <div className="absolute left-full ml-2 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50">
            {tooltip}
          </div>
        )}
      </Link>
    );
  };

  return (
    <aside
      className={clsx(
        'bg-gray-50 dark:bg-slate-900 border-r border-gray-200 dark:border-slate-700 transition-all duration-300 flex flex-col',
        isCollapsed ? 'w-20' : 'w-64'
      )}
    >
      <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200 dark:border-slate-700">
        {!isCollapsed ? (
          <>
            <Link to="/works" className="flex items-center space-x-2.5 group min-w-0">
              <div className="w-10 h-10 bg-gray-900 dark:bg-slate-800 rounded-lg flex items-center justify-center flex-shrink-0">
                <img src="/logo-icon.svg" alt="文枢AI" style={{ width: '28px', height: '28px', filter: 'brightness(0) invert(1)' }} />
              </div>
              <div className="min-w-0">
                <h2 className="text-sm font-semibold text-gray-900 dark:text-slate-100 leading-tight">{t('app.name')}</h2>
                <p className="text-xs text-gray-500 dark:text-slate-400 leading-tight">{t('app.slogan')}</p>
              </div>
            </Link>
            <button
              onClick={() => setIsCollapsed(true)}
              className="flex-shrink-0 p-1 text-gray-400 hover:text-gray-700 hover:bg-gray-100 dark:text-slate-500 dark:hover:text-slate-200 dark:hover:bg-slate-800 rounded transition-all"
              title={t('sidebar.collapse')}
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
          </>
        ) : (
          <button onClick={() => setIsCollapsed(false)} className="w-full flex justify-center" title={t('sidebar.expand')}>
            <div className="w-12 h-12 bg-gray-900 dark:bg-slate-800 rounded-lg flex items-center justify-center hover:bg-gray-800 dark:hover:bg-slate-700 transition-all">
              <img src="/logo-icon.svg" alt="文枢AI" style={{ width: '32px', height: '32px', filter: 'brightness(0) invert(1)' }} />
            </div>
          </button>
        )}
      </div>

      <nav className="flex-1 px-3 py-4 overflow-y-auto">
        <div className="space-y-0.5">
          {!isCollapsed && (
            <div className="px-3 py-2 text-xs font-medium text-gray-400 dark:text-slate-500 uppercase tracking-wider">{t('sidebar.sections.create')}</div>
          )}
          {dynamicMainNavItems.map(renderNavItem)}
        </div>

        <div className="mt-6 space-y-0.5">
          <button
            onClick={() => setIsServiceExpanded(!isServiceExpanded)}
            className={clsx(
              'w-full flex items-center justify-between px-3 py-2 text-xs font-medium text-gray-900 dark:text-slate-200 uppercase tracking-wider hover:text-gray-700 dark:hover:text-slate-100 transition-colors',
              isCollapsed && 'justify-center'
            )}
          >
            {!isCollapsed && <span>{t('sidebar.sections.myServices')}</span>}
            <ChevronDown className={clsx('w-4 h-4 transition-transform', !isServiceExpanded && '-rotate-90')} />
          </button>
          {isServiceExpanded && serviceNavItemsConfig.map(renderNavItem)}
        </div>

        {user?.role === 'admin' && (
          <div className="mt-6 space-y-0.5">
            {!isCollapsed && (
              <div className="px-3 py-2 text-xs font-medium text-gray-400 dark:text-slate-500 uppercase tracking-wider">{t('sidebar.sections.admin')}</div>
            )}
            {adminNavItemsConfig.map(renderNavItem)}
          </div>
        )}

        <div className="mt-6 pt-6 border-t border-gray-200 dark:border-slate-700 space-y-0.5">
          {bottomNavItems.map(renderNavItem)}
        </div>
      </nav>

      <div className="p-3 border-t border-gray-200 dark:border-slate-700">
        {!isCollapsed ? (
          <div className="flex items-center space-x-2.5 p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded transition-colors cursor-pointer">
            <div className="w-8 h-8 bg-gray-900 dark:bg-slate-700 rounded-full flex items-center justify-center flex-shrink-0">
              <span className="text-xs font-medium text-white">
                {user?.username ? user.username[0].toUpperCase() : 'U'}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-gray-700 dark:text-slate-200 truncate leading-tight">
                {user?.username || t('common.user')}
              </p>
              <p className="text-xs text-gray-500 dark:text-slate-400 leading-tight">
                {user?.role === 'admin' ? t('sidebar.roles.admin') : t('sidebar.roles.creator')}
              </p>
            </div>
            <Settings className="w-3.5 h-3.5 text-gray-500 hover:text-gray-700 dark:text-slate-400 dark:hover:text-slate-200 flex-shrink-0 transition-colors" />
          </div>
        ) : (
          <div className="flex justify-center">
            <div className="w-9 h-9 bg-gray-900 dark:bg-slate-700 rounded-full flex items-center justify-center hover:bg-gray-800 dark:hover:bg-slate-600 transition-colors cursor-pointer">
              <span className="text-xs font-medium text-white">
                {user?.username ? user.username[0].toUpperCase() : 'U'}
              </span>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
