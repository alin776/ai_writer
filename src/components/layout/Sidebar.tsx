import React, { useMemo, useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { Link, useLocation, useNavigate } from 'react-router-dom';
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
  MessageCircle,
  User,
  CheckCheck,
  ExternalLink,
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { useWorkNavStore } from '../../store/workNavStore';
import { useNotificationStore } from '../../store/notificationStore';
import { channelApi } from '@/services/channelApi';
import clsx from 'clsx';
import UserCardPopover from './UserCardPopover';
import NotificationItem from '../notifications/NotificationItem';

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
  { id: 'channels', label: '频道', icon: MessageCircle, path: '/channels' },
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
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const { lastWorkPath } = useWorkNavStore();
  const {
    notifications,
    unreadCount: notificationUnreadCount,
    isLoading: notificationLoading,
    fetchNotifications,
    markAllAsRead,
  } = useNotificationStore();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isLibraryExpanded, setIsLibraryExpanded] = useState(true);
  const [isServiceExpanded, setIsServiceExpanded] = useState(true);
  const [isUserCardOpen, setIsUserCardOpen] = useState(false);
  const [isQRCodeOpen, setIsQRCodeOpen] = useState(false);
  const [hasChannelMention, setHasChannelMention] = useState(false); // 频道是否有@提醒
  const [channelUnreadCount, setChannelUnreadCount] = useState(0); // 频道未读消息总数
  const [isNavScrolled, setIsNavScrolled] = useState(false); // 导航区域是否滚动
  const [isNotificationHovered, setIsNotificationHovered] = useState(false); // 通知中心悬浮状态
  const notificationHoverRef = useRef<HTMLDivElement>(null);
  const userMenuRef = useRef<HTMLDivElement>(null);

  // 获取频道未读状态
  useEffect(() => {
    const fetchChannelUnread = async () => {
      try {
        const summary = await channelApi.getUnreadSummary();
        // 检查是否有任何频道有@提醒
        const hasMention = summary.channels.some(ch => ch.mentionCount > 0);
        setHasChannelMention(hasMention);
        // 计算未读消息总数
        const totalUnread = summary.channels.reduce((sum, ch) => sum + ch.unreadCount, 0);
        setChannelUnreadCount(totalUnread);
      } catch (error) {
        // 未登录或接口错误时忽略
      }
    };

    // 只有登录用户才获取
    if (user) {
      fetchChannelUnread();
      // 每30秒刷新一次
      const interval = setInterval(fetchChannelUnread, 30000);
      return () => clearInterval(interval);
    }
  }, [user, location.pathname]); // 路径变化时也刷新（可能标记了已读）

  // 点击外部关闭菜单 - 由 UserCardPopover 内部处理
  // useEffect 保留用于其他可能的外部点击处理
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      // 如果用户卡片打开，让 UserCardPopover 自己处理关闭逻辑
      if (isUserCardOpen) return;
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isUserCardOpen]);

  // 悬浮通知中心时加载通知
  useEffect(() => {
    if (isNotificationHovered && isCollapsed) {
      fetchNotifications({ isRead: false });
    }
  }, [isNotificationHovered, isCollapsed, fetchNotifications]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // 检测当前是否在作品详情页
  const isWorkDetail = location.pathname.startsWith('/works/') && location.pathname !== '/works';

  // 判断是否应该显示"作品详情"：当前在作品详情页 或 有最近访问的作品记录且不在作品管理列表页
  const shouldShowWorkDetail = isWorkDetail || (lastWorkPath && location.pathname !== '/works');

  const dynamicMainNavItems: NavItem[] = useMemo(() => {
    return mainNavItems.map(item =>
      item.id === 'works'
        ? {
            ...item,
            label: shouldShowWorkDetail ? '作品详情' : '作品管理',
            path: shouldShowWorkDetail && lastWorkPath ? lastWorkPath : '/works'
          }
        : item
    );
  }, [shouldShowWorkDetail, lastWorkPath]);

  const isActive = (path: string) => location.pathname === path || location.pathname.startsWith(`${path}/`);
  const hasPermission = (item: NavItem) => !item.roles?.length || item.roles.includes(user?.role || '');

  const bottomNavItems: NavItem[] = useMemo(() => [
    { id: 'profile', label: '个人主页', icon: User, path: user ? `/user/${user.id}` : '/login' },
    { id: 'notifications', label: '通知中心', icon: Bell, path: '/notifications' },
    { id: 'settings', label: '系统设置', icon: Settings, path: '/settings' },
  ], [user]);

  // 导航项渲染函数
  const renderNavItem = (item: NavItem) => {
    if (!hasPermission(item)) return null;
    const Icon = item.icon;
    const active = isActive(item.path);
    const tooltip = item.tooltip || item.label;
    const isChannelItem = item.id === 'channels';
    const showMentionDot = isChannelItem && hasChannelMention;
    const showUnreadBadge = isChannelItem && !hasChannelMention && channelUnreadCount > 0;

    return (
      <Link
        key={item.id}
        to={item.path}
        className={clsx(
          'group relative flex items-center px-3 py-2 rounded-lg transition-all duration-200 !text-gray-900 dark:!text-white',
          active
            ? 'bg-blue-50 dark:bg-blue-900/30'
            : 'hover:bg-gray-100 dark:hover:bg-slate-800',
          isCollapsed ? 'justify-center' : 'space-x-3'
        )}
        title={isCollapsed ? tooltip : undefined}
      >
        <div className="relative flex-shrink-0">
          <Icon className={clsx(isCollapsed ? 'w-5 h-5' : 'w-4 h-4', 'text-gray-900 dark:text-white')} />
          {/* 频道@提醒红点 - 优先级最高 */}
          {showMentionDot && (
            <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          )}
        </div>
        {!isCollapsed && (
          <>
            <span className="text-sm font-medium flex-1">{item.label}</span>
            {/* 频道未读消息数量徽章 */}
            {showUnreadBadge && (
              <span className="text-xs bg-gray-900 dark:bg-zinc-600 text-white rounded-full h-5 min-w-5 px-1.5 flex items-center justify-center">
                {channelUnreadCount > 99 ? '99+' : channelUnreadCount}
              </span>
            )}
          </>
        )}
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
        'relative z-10 bg-gray-50 dark:bg-slate-900 border-r border-gray-200 dark:border-slate-700 transition-all duration-300 flex flex-col overflow-hidden',
        isCollapsed ? 'w-16' : 'w-64'
      )}
    >
      <div className={clsx(
        "h-16 flex items-center justify-between border-b transition-colors",
        isCollapsed ? "px-3" : "px-4",
        isNavScrolled ? "border-gray-200 dark:border-slate-700" : "border-transparent"
      )}>
        {!isCollapsed ? (
          <>
            <Link to="/works" className="flex items-center space-x-2.5 group min-w-0">
              <div className="w-10 h-10 bg-gray-900 dark:bg-slate-800 rounded-full flex items-center justify-center flex-shrink-0">
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
            <div className="w-10 h-10 bg-gray-900 dark:bg-slate-800 rounded-full flex items-center justify-center hover:bg-gray-800 dark:hover:bg-slate-700 transition-all">
              <img src="/logo-icon.svg" alt="文枢AI" style={{ width: '28px', height: '28px', filter: 'brightness(0) invert(1)' }} />
            </div>
          </button>
        )}
      </div>

      <nav
        className="flex-1 px-3 py-4 overflow-y-auto overflow-x-hidden sidebar-scrollbar"
        onScroll={(e) => setIsNavScrolled(e.currentTarget.scrollTop > 0)}
      >
        <div className="space-y-0.5">
          {!isCollapsed && (
            <div className="px-3 py-2 text-xs font-medium text-gray-900 dark:text-slate-200 uppercase tracking-wider">创作</div>
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
            {!isCollapsed && <span>社区</span>}
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
          {bottomNavItems.map((item) => {
            // 通知中心特殊处理
            if (item.id === 'notifications') {
              const Icon = item.icon;
              const active = isActive(item.path);
              const tooltip = item.label;
              const hasUnread = notificationUnreadCount > 0;

              return (
                <div
                  key={item.id}
                  ref={notificationHoverRef}
                  className="relative"
                  onMouseEnter={() => setIsNotificationHovered(true)}
                  onMouseLeave={() => setIsNotificationHovered(false)}
                >
                  <Link
                    to={item.path}
                    className={clsx(
                      'group relative flex items-center px-3 py-2 rounded-lg transition-all duration-200 !text-gray-900 dark:!text-white',
                      active
                        ? 'bg-blue-50 dark:bg-blue-900/30'
                        : 'hover:bg-gray-100 dark:hover:bg-slate-800',
                      isCollapsed ? 'justify-center' : 'space-x-3'
                    )}
                    title={isCollapsed && !isNotificationHovered ? tooltip : undefined}
                  >
                    <div className="relative flex-shrink-0">
                      <Icon className={clsx(isCollapsed ? 'w-5 h-5' : 'w-4 h-4', 'text-gray-900 dark:text-white')} />
                      {/* 未读通知红点 */}
                      {hasUnread && (
                        <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                      )}
                    </div>
                    {!isCollapsed && (
                      <>
                        <span className="text-sm font-medium flex-1">{item.label}</span>
                        {/* 未读数量徽章 */}
                        {hasUnread && (
                          <span className="text-xs bg-red-500 text-white rounded-full h-5 min-w-5 px-1.5 flex items-center justify-center">
                            {notificationUnreadCount > 99 ? '99+' : notificationUnreadCount}
                          </span>
                        )}
                      </>
                    )}
                  </Link>

                  {/* 收缩状态下悬浮显示通知列表 - 使用 Portal 避免被裁剪 */}
                  {isCollapsed && isNotificationHovered && createPortal(
                    <div
                      className="fixed w-80 bg-white dark:bg-slate-900 rounded-lg shadow-xl border border-gray-200 dark:border-slate-700 z-[100]"
                      style={(() => {
                        if (!notificationHoverRef.current) return { left: 72, top: 0 };
                        const rect = notificationHoverRef.current.getBoundingClientRect();
                        const popupHeight = 400; // 弹窗预估高度
                        const viewportHeight = window.innerHeight;
                        let top = rect.top;
                        // 如果弹窗会超出屏幕底部，向上调整
                        if (top + popupHeight > viewportHeight - 16) {
                          top = viewportHeight - popupHeight - 16;
                        }
                        // 确保不超出屏幕顶部
                        if (top < 16) top = 16;
                        return { left: rect.right + 8, top };
                      })()}
                      onMouseEnter={() => setIsNotificationHovered(true)}
                      onMouseLeave={() => setIsNotificationHovered(false)}
                    >
                      {/* 通知列表 */}
                      <div className="max-h-80 overflow-y-auto">
                        {notificationLoading ? (
                          <div className="flex items-center justify-center py-8">
                            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                          </div>
                        ) : notifications.length === 0 ? (
                          <div className="flex flex-col items-center justify-center py-8 text-gray-500 dark:text-gray-400">
                            <Bell className="w-8 h-8 mb-2 opacity-50" />
                            <p className="text-sm">暂无通知</p>
                          </div>
                        ) : (
                          <div className="divide-y divide-gray-100 dark:divide-gray-800">
                            {notifications.slice(0, 5).map((notification) => (
                              <NotificationItem
                                key={notification.id}
                                notification={notification}
                                onClose={() => setIsNotificationHovered(false)}
                              />
                            ))}
                          </div>
                        )}
                      </div>

                      {/* 底部 - 查看全部 */}
                      <div className="px-4 py-2 border-t border-gray-200 dark:border-slate-700">
                        <Link
                          to="/notifications"
                          onClick={() => setIsNotificationHovered(false)}
                          className="flex items-center justify-center gap-2 w-full px-3 py-1.5 text-xs font-medium text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
                        >
                          查看全部通知
                          <ExternalLink className="w-3 h-3" />
                        </Link>
                      </div>
                    </div>,
                    document.body
                  )}
                </div>
              );
            }
            return renderNavItem(item);
          })}
        </div>
      </nav>

      <div className="p-3 relative" ref={userMenuRef}>
        {/* 用户明信片弹窗 */}
        <UserCardPopover
          isOpen={isUserCardOpen}
          onClose={() => setIsUserCardOpen(false)}
        />

        {!isCollapsed ? (
          <div
            className="flex items-center p-2 rounded-lg border border-transparent hover:border-gray-200 dark:hover:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-800 transition-colors cursor-pointer"
          >
            <div
              onClick={() => setIsUserCardOpen(!isUserCardOpen)}
              className="flex items-center space-x-2.5 flex-1 min-w-0"
            >
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0 overflow-hidden">
                {user?.avatar ? (
                  <img src={user.avatar} alt={user.username} className="w-full h-full object-cover" />
                ) : (
                  <span className="text-xs font-medium text-white">
                    {user?.username ? user.username[0].toUpperCase() : 'U'}
                  </span>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                  {user?.username || '用户'}
                </p>
                <p className="text-xs text-gray-500 dark:text-slate-400 truncate">
                  {user?.isAdmin ? '管理员账户' : '个人账户'}
                </p>
              </div>
            </div>
            {/* 星球图标 - 悬浮显示二维码 */}
            <div
              className="relative ml-2"
              onMouseEnter={() => setIsQRCodeOpen(true)}
              onMouseLeave={() => setIsQRCodeOpen(false)}
              onClick={(e) => e.stopPropagation()}
            >
              <svg
                className="w-6 h-6 text-gray-500 hover:text-gray-700 dark:text-slate-400 dark:hover:text-slate-200 flex-shrink-0 transition-colors cursor-pointer"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="12" cy="12" r="5" />
                <ellipse cx="12" cy="12" rx="11" ry="4" transform="rotate(-20 12 12)" />
                <circle cx="19" cy="8" r="1" fill="currentColor" stroke="none" />
                <circle cx="6" cy="5" r="0.5" fill="currentColor" stroke="none" />
                <circle cx="18" cy="17" r="0.5" fill="currentColor" stroke="none" />
              </svg>
              {/* 二维码弹出框 */}
              {isQRCodeOpen && (
                <div className="fixed bottom-24 left-72 bg-white dark:bg-slate-800 rounded-xl shadow-2xl border border-gray-200 dark:border-slate-700 p-4 z-[100]">
                  {/* 内测群 */}
                  <div className="text-center">
                    <div className="rounded-lg overflow-hidden w-52 h-52 bg-white flex items-center justify-center">
                      <img
                        src="/images/qrcode/qq.jpg"
                        alt="内测群二维码"
                        className="max-w-full max-h-full object-contain"
                      />
                    </div>
                    <p className="mt-3 text-sm font-medium text-blue-500 dark:text-blue-400">内测群</p>
                    <p className="text-xs text-gray-500 dark:text-slate-400 mt-1">反馈、分享作品、参与活动赢会员</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="flex justify-center">
            <div
              onClick={() => setIsUserCardOpen(!isUserCardOpen)}
              className="w-9 h-9 bg-blue-600 rounded-full flex items-center justify-center hover:bg-blue-700 transition-colors cursor-pointer overflow-hidden"
            >
              {user?.avatar ? (
                <img src={user.avatar} alt={user.username} className="w-full h-full object-cover" />
              ) : (
                <span className="text-xs font-medium text-white">
                  {user?.username ? user.username[0].toUpperCase() : 'U'}
                </span>
              )}
            </div>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;













