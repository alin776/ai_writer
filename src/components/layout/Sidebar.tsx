import React, { useMemo, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
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
  BookMarked,
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import clsx from 'clsx';

interface NavItem {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  path: string;
  tooltip?: string;
  roles?: string[];
}

const mainNavItems: NavItem[] = [
  { id: 'works', label: '作品管理', icon: BookOpen, path: '/works' },
  { id: 'knowledge', label: '知识库', icon: Library, path: '/knowledge' },
  { id: 'humanize', label: 'AI去痕', icon: Wand2, path: '/humanize' },
];

const libraryNavItems: NavItem[] = [
  { id: 'novel-square', label: '小说广场', icon: BookMarked, path: '/library/novel-square' },
  { id: 'my-bookshelf', label: '我的书架', icon: BookOpen, path: '/library/my-bookshelf' },
];

const serviceNavItems: NavItem[] = [
  { id: 'tasks', label: '任务中心', icon: Trophy, path: '/tasks' },
  { id: 'credits', label: '我的积分', icon: Wallet, path: '/service/credits' },
  { id: 'usage', label: '使用记录', icon: BarChart3, path: '/service/usage' },
  { id: 'obtain', label: '获取积分', icon: Gift, path: '/service/obtain' },
];

// 管理员导航项
const adminNavItems: NavItem[] = [
  { id: 'dashboard', label: '数据面板', icon: LayoutDashboard, path: '/admin/dashboard', roles: ['admin'] },
  { id: 'users', label: '用户管理', icon: Users, path: '/admin/users', roles: ['admin'] },
  { id: 'ai-models', label: 'AI 模型', icon: Cpu, path: '/admin/ai-models', roles: ['admin'] },
  { id: 'cost', label: '成本监控', icon: DollarSign, path: '/admin/cost', roles: ['admin'] },
  { id: 'notifications-admin', label: '通知管理', icon: Bell, path: '/admin/notifications', roles: ['admin'] },
  { id: 'tasks-admin', label: '任务配置', icon: Trophy, path: '/admin/tasks', roles: ['admin'] },
];

export const Sidebar: React.FC = () => {
  const location = useLocation();
  const { user } = useAuthStore();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isLibraryExpanded, setIsLibraryExpanded] = useState(true);
  const [isServiceExpanded, setIsServiceExpanded] = useState(true);

  const isWorkDetail = location.pathname.startsWith('/works/') && location.pathname !== '/works';

  const dynamicMainNavItems: NavItem[] = useMemo(() => {
    return mainNavItems.map(item =>
      item.id === 'works'
        ? { ...item, label: isWorkDetail ? '作品详情' : '作品管理' }
        : item
    );
  }, [isWorkDetail]);

  const isActive = (path: string) => location.pathname === path || location.pathname.startsWith(`${path}/`);
  const hasPermission = (item: NavItem) => !item.roles?.length || item.roles.includes(user?.role || '');

  const bottomNavItems: NavItem[] = [
    { id: 'notifications', label: '通知中心', icon: Bell, path: '/notifications' },
    { id: 'settings', label: '系统设置', icon: Settings, path: '/settings' },
  ];

  const renderNavItem = (item: NavItem) => {
    if (!hasPermission(item)) return null;
    const Icon = item.icon;
    const active = isActive(item.path);
    const tooltip = item.tooltip || item.label;

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
        {!isCollapsed && <span className="text-sm font-medium">{item.label}</span>}
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
                <h2 className="text-sm font-semibold text-gray-900 dark:text-slate-100 leading-tight">文枢AI</h2>
                <p className="text-xs text-gray-500 dark:text-slate-400 leading-tight">智能创作助手</p>
              </div>
            </Link>
            <button
              onClick={() => setIsCollapsed(true)}
              className="flex-shrink-0 p-1 text-gray-400 hover:text-gray-700 hover:bg-gray-100 dark:text-slate-500 dark:hover:text-slate-200 dark:hover:bg-slate-800 rounded transition-all"
              title="收起侧边栏"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
          </>
        ) : (
          <button onClick={() => setIsCollapsed(false)} className="w-full flex justify-center" title="展开侧边栏">
            <div className="w-12 h-12 bg-gray-900 dark:bg-slate-800 rounded-lg flex items-center justify-center hover:bg-gray-800 dark:hover:bg-slate-700 transition-all">
              <img src="/logo-icon.svg" alt="文枢AI" style={{ width: '32px', height: '32px', filter: 'brightness(0) invert(1)' }} />
            </div>
          </button>
        )}
      </div>

      <nav className="flex-1 px-3 py-4 overflow-y-auto">
        <div className="space-y-0.5">
          {!isCollapsed && (
            <div className="px-3 py-2 text-xs font-medium text-gray-400 dark:text-slate-500 uppercase tracking-wider">创作</div>
          )}
          {dynamicMainNavItems.map(renderNavItem)}
        </div>

        <div className="mt-6 space-y-0.5">
          <button
            onClick={() => setIsLibraryExpanded(!isLibraryExpanded)}
            className={clsx(
              'w-full flex items-center justify-between px-3 py-2 text-xs font-medium text-gray-900 dark:text-slate-200 uppercase tracking-wider hover:text-gray-700 dark:hover:text-slate-100 transition-colors',
              isCollapsed && 'justify-center'
            )}
          >
            {!isCollapsed && <span>图书馆</span>}
            <ChevronDown className={clsx('w-4 h-4 transition-transform', !isLibraryExpanded && '-rotate-90')} />
          </button>
          {isLibraryExpanded && libraryNavItems.map(renderNavItem)}
        </div>

        <div className="mt-6 space-y-0.5">
          <button
            onClick={() => setIsServiceExpanded(!isServiceExpanded)}
            className={clsx(
              'w-full flex items-center justify-between px-3 py-2 text-xs font-medium text-gray-900 dark:text-slate-200 uppercase tracking-wider hover:text-gray-700 dark:hover:text-slate-100 transition-colors',
              isCollapsed && 'justify-center'
            )}
          >
            {!isCollapsed && <span>我的服务</span>}
            <ChevronDown className={clsx('w-4 h-4 transition-transform', !isServiceExpanded && '-rotate-90')} />
          </button>
          {isServiceExpanded && serviceNavItems.map(renderNavItem)}
        </div>

        {user?.role === 'admin' && (
          <div className="mt-6 space-y-0.5">
            {!isCollapsed && (
              <div className="px-3 py-2 text-xs font-medium text-gray-400 dark:text-slate-500 uppercase tracking-wider">管理</div>
            )}
            {adminNavItems.map(renderNavItem)}
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
                {user?.username || '用户'}
              </p>
              <p className="text-xs text-gray-500 dark:text-slate-400 leading-tight">
                {user?.role === 'admin' ? '管理员' : '创作者'}
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













