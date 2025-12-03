import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  BookOpen,
  PenTool,
  Settings,
  ChevronLeft,
  ChevronRight,
  LayoutDashboard,
  Users,
  Cpu,
  DollarSign,
  Sparkles,
  Library,
  Wallet,
  BarChart3,
  Gift,
  ChevronDown,
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import clsx from 'clsx';

/**
 * 导航菜单项接口
 */
interface NavItem {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  path: string;
  roles?: string[]; // 允许访问的角色，不设置则所有角色都能访问
}

/**
 * 主导航菜单配置
 */
const mainNavItems: NavItem[] = [
  {
    id: 'works',
    label: '作品管理',
    icon: BookOpen,
    path: '/works',
  },
  {
    id: 'knowledge',
    label: '知识库',
    icon: Library,
    path: '/knowledge',
  },
];

/**
 * 我的服务导航菜单配置
 */
const serviceNavItems: NavItem[] = [
  {
    id: 'credits',
    label: '我的积分',
    icon: Wallet,
    path: '/service/credits',
  },
  {
    id: 'usage',
    label: '使用记录',
    icon: BarChart3,
    path: '/service/usage',
  },
  {
    id: 'obtain',
    label: '获取积分',
    icon: Gift,
    path: '/service/obtain',
  },
];

/**
 * 管理员导航菜单配置
 */
const adminNavItems: NavItem[] = [
  {
    id: 'dashboard',
    label: '数据面板',
    icon: LayoutDashboard,
    path: '/admin/dashboard',
    roles: ['admin'],
  },
  {
    id: 'users',
    label: '用户管理',
    icon: Users,
    path: '/admin/users',
    roles: ['admin'],
  },
  {
    id: 'ai-models',
    label: 'AI 模型',
    icon: Cpu,
    path: '/admin/ai-models',
    roles: ['admin'],
  },
  {
    id: 'cost',
    label: '成本监控',
    icon: DollarSign,
    path: '/admin/cost',
    roles: ['admin'],
  },
];

/**
 * Sidebar 组件 - 侧边栏导航
 *
 * 功能：
 * - 显示主要导航菜单
 * - 显示管理员菜单（仅管理员可见）
 * - 支持收起/展开
 * - 高亮当前激活的菜单项
 * - 响应式设计
 */
export const Sidebar: React.FC = () => {
  const location = useLocation();
  const { user } = useAuthStore();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isServiceExpanded, setIsServiceExpanded] = useState(true);

  /**
   * 检查菜单项是否激活
   */
  const isActive = (path: string): boolean => {
    return location.pathname === path || location.pathname.startsWith(`${path}/`);
  };

  /**
   * 检查用户是否有权限访问菜单项
   */
  const hasPermission = (item: NavItem): boolean => {
    if (!item.roles || item.roles.length === 0) return true;
    return item.roles.includes(user?.role || '');
  };

  /**
   * 渲染导航菜单项
   */
  const renderNavItem = (item: NavItem) => {
    if (!hasPermission(item)) return null;

    const Icon = item.icon;
    const active = isActive(item.path);

    return (
      <Link
        key={item.id}
        to={item.path}
        className={clsx(
          'group relative flex items-center px-3 py-2 rounded transition-all duration-200',
          active
            ? 'bg-blue-50 text-blue-600'
            : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900',
          isCollapsed ? 'justify-center' : 'space-x-3'
        )}
        title={isCollapsed ? item.label : undefined}
      >
        {/* 左侧激活状态指示条 - 高亮色强调 */}
        {active && (
          <div className="absolute left-0 top-1 bottom-1 w-1 bg-blue-600 rounded-r"></div>
        )}

        <Icon className={clsx('flex-shrink-0', isCollapsed ? 'w-5 h-5' : 'w-4 h-4')} />
        {!isCollapsed && <span className="text-sm font-medium">{item.label}</span>}

        {/* 折叠状态的悬停提示 */}
        {isCollapsed && (
          <div className="absolute left-full ml-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50">
            {item.label}
          </div>
        )}
      </Link>
    );
  };

  return (
    <aside
      className={clsx(
        'bg-gray-50 border-r border-gray-200 transition-all duration-300 flex flex-col',
        isCollapsed ? 'w-20' : 'w-64'
      )}
    >
      {/* 侧边栏头部 - Logo 和收起/展开按钮 */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200">
        {!isCollapsed ? (
          <>
            <Link to="/works" className="flex items-center space-x-2.5 group min-w-0">
              <div className="w-7 h-7 bg-gray-900 rounded-sm flex items-center justify-center flex-shrink-0">
                <Sparkles className="w-3.5 h-3.5 text-white" />
              </div>
              <div className="min-w-0">
                <h2 className="text-sm font-semibold text-gray-900 leading-tight">AI Writer</h2>
                <p className="text-xs text-gray-500 leading-tight">智能创作</p>
              </div>
            </Link>
            <button
              onClick={() => setIsCollapsed(true)}
              className="flex-shrink-0 p-1 text-gray-400 hover:text-gray-700 hover:bg-gray-100 rounded transition-all"
              title="收起侧边栏"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
          </>
        ) : (
          <button
            onClick={() => setIsCollapsed(false)}
            className="w-full flex justify-center"
            title="展开侧边栏"
          >
            <div className="w-9 h-9 bg-gray-900 rounded-sm flex items-center justify-center hover:bg-gray-800 transition-all">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
          </button>
        )}
      </div>

      {/* 侧边栏内容 */}
      <nav className="flex-1 px-3 py-4 overflow-y-auto">
        {/* 主要导航 */}
        <div className="space-y-0.5">
          {!isCollapsed && (
            <div className="px-3 py-2 text-xs font-medium text-gray-400 uppercase tracking-wider">
              创作
            </div>
          )}
          {mainNavItems.map(renderNavItem)}
        </div>

        {/* 我的服务导航 - 可折叠 */}
        <div className="mt-6 space-y-0.5">
          {/* 菜单组标题 - 可点击折叠 */}
          <button
            onClick={() => setIsServiceExpanded(!isServiceExpanded)}
            className={clsx(
              'w-full flex items-center justify-between px-3 py-2 text-xs font-medium text-gray-400 uppercase tracking-wider hover:text-gray-600 transition-colors',
              isCollapsed && 'justify-center'
            )}
          >
            {!isCollapsed && <span>我的服务</span>}
            <ChevronDown
              className={clsx(
                'w-4 h-4 transition-transform',
                !isServiceExpanded && '-rotate-90'
              )}
            />
          </button>
          {/* 子菜单项 */}
          {isServiceExpanded && serviceNavItems.map(renderNavItem)}
        </div>

        {/* 管理员导航 - 仅管理员可见 */}
        {user?.role === 'admin' && (
          <div className="mt-6 space-y-0.5">
            {!isCollapsed && (
              <div className="px-3 py-2 text-xs font-medium text-gray-400 uppercase tracking-wider">
                管理
              </div>
            )}
            {adminNavItems.map(renderNavItem)}
          </div>
        )}

        {/* 设置导航 */}
        <div className="mt-6 pt-6 border-t border-gray-200 space-y-0.5">
          {renderNavItem({
            id: 'settings',
            label: '系统设置',
            icon: Settings,
            path: '/settings',
          })}
        </div>
      </nav>

      {/* 侧边栏底部 - 用户信息 */}
      <div className="p-3 border-t border-gray-200">
        {!isCollapsed ? (
          <div className="flex items-center space-x-2.5 p-2 hover:bg-gray-100 rounded transition-colors cursor-pointer">
            <div className="w-8 h-8 bg-gray-900 rounded-full flex items-center justify-center flex-shrink-0">
              <span className="text-xs font-medium text-white">
                {user?.username ? user.username[0].toUpperCase() : 'U'}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-gray-700 truncate leading-tight">
                {user?.username || '用户'}
              </p>
              <p className="text-xs text-gray-500 leading-tight">
                {user?.role === 'admin' ? '管理员' : '创作者'}
              </p>
            </div>
            <Settings className="w-3.5 h-3.5 text-gray-500 hover:text-gray-700 flex-shrink-0 transition-colors" />
          </div>
        ) : (
          <div className="flex justify-center">
            <div className="w-9 h-9 bg-gray-900 rounded-full flex items-center justify-center hover:bg-gray-800 transition-colors cursor-pointer">
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
