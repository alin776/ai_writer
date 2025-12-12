/**
 * 顶部导航栏组件
 */
import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LogOut,
  User,
  Bell,
  Search,
  Menu,
  ChevronDown,
  ArrowLeft,
  Save,
  MoreHorizontal,
  Clock
} from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import { DataService } from '@/services/DataService';
import { useNavigate } from 'react-router-dom';
import Button from '@/components/common/Button';
import { GlobalSearch } from '@/components/search/GlobalSearch';
import { useNotificationStore } from '@/store/notificationStore';
import NotificationDropdown from '@/components/notifications/NotificationDropdown';
import ThemeToggle from '@/components/common/ThemeToggle';

const Header: React.FC = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [lastSaved] = useState<Date>(new Date());
  const [showSearch, setShowSearch] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const unreadCount = useNotificationStore((state) => state.unreadCount);

  // 监听 Cmd+K / Ctrl+K 快捷键打开搜索
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setShowSearch(true);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleLogout = async () => {
    await DataService.logout();
    logout();
    navigate('/login');
  };

  // 获取当前页面标题
  const getPageTitle = () => {
    const path = location.pathname;
    if (path.includes('/works') && path !== '/works') return '作品详情';
    if (path === '/works') return '我的作品';
    if (path.includes('/editor')) return '创作中';
    if (path.includes('/admin/dashboard')) return '数据面板';
    if (path.includes('/admin/users')) return '用户管理';
    if (path.includes('/admin/ai-models')) return 'AI 模型';
    if (path.includes('/admin/cost')) return '成本监控';
    if (path.includes('/settings')) return '系统设置';
    return '文枢AI';
  };

  // 判断是否在编辑器页面
  const isEditorPage = location.pathname.includes('/editor');

  return (
    <header className="bg-white dark:bg-slate-900 border-b border-gray-200 dark:border-slate-700 h-14 flex items-center px-4 sticky top-0 z-40">
      <div className="flex items-center justify-between w-full max-w-full">
        {/* 左侧内容 - 根据页面类型动态显示 */}
        <div className="flex items-center space-x-3 min-w-0">
          {/* 编辑器页面：返回按钮 + 作品/章节信息 */}
          {isEditorPage ? (
            <>
              <button
                onClick={() => navigate('/works')}
                className="p-1.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800 rounded transition-colors"
                title="返回作品列表"
              >
                <ArrowLeft className="w-4 h-4" />
              </button>
              <div className="min-w-0">
                <h1 className="text-sm font-semibold text-gray-900 dark:text-slate-100 truncate">当前作品名称</h1>
                <div className="flex items-center space-x-2 text-xs text-gray-500 dark:text-slate-400">
                  <Clock className="w-3 h-3" />
                  <span>{lastSaved.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })} 已保存</span>
                </div>
              </div>
            </>
          ) : (
            /* 其他页面：显示页面标题 */
            <h1 className="text-base font-semibold text-gray-900 dark:text-slate-100">{getPageTitle()}</h1>
          )}
        </div>

        {/* 右侧操作区 - 根据页面类型动态显示 */}
        <div className="flex items-center space-x-2">
          {/* 编辑器页面的特殊操作 */}
          {isEditorPage && (
            <>
              <button className="px-3 py-1.5 text-xs font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800 rounded transition-colors">
                导出
              </button>
              <button className="px-3 py-1.5 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-500 rounded transition-colors shadow-sm">
                AI 续写
              </button>
              <button className="p-1.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800 rounded transition-colors">
                <MoreHorizontal className="w-4 h-4" />
              </button>
              <div className="h-4 w-px bg-gray-200 dark:bg-slate-700 mx-1"></div>
            </>
          )}

          {/* 通用操作：搜索和通知 */}
          <button
            className="p-1.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800 rounded transition-colors"
            onClick={() => setShowSearch(true)}
            title="搜索 (Cmd+K)"
          >
            <Search className="w-4 h-4" />
          </button>

          {/* 通知铃铛 */}
          <div className="relative">
            <button
              className="relative p-1.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800 rounded transition-colors"
              onClick={() => setShowNotifications(!showNotifications)}
            >
              <Bell className="w-4 h-4" />
              {unreadCount > 0 && (
                <span className="absolute -top-0.5 -right-0.5 flex items-center justify-center min-w-[18px] h-[18px] px-1 text-[10px] font-bold text-white bg-red-500 rounded-full">
                  {unreadCount > 99 ? '99+' : unreadCount}
                </span>
              )}
            </button>

            {/* 通知下拉列表 */}
            {showNotifications && (
              <>
                <div
                  className="fixed inset-0 z-40"
                  onClick={() => setShowNotifications(false)}
                ></div>
                <div className="absolute right-0 mt-1.5 z-50">
                  <NotificationDropdown onClose={() => setShowNotifications(false)} />
                </div>
              </>
            )}
          </div>

          {/* 主题切换按钮 */}
          <ThemeToggle />

          {/* 分隔线 */}
          <div className="h-4 w-px bg-gray-200 dark:bg-slate-700 mx-1"></div>

          {/* 用户菜单 */}
          {user && (
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-2 px-2 py-1 text-gray-900 dark:text-slate-100 hover:bg-gray-100 dark:hover:bg-slate-800 rounded transition-colors"
              >
                <div className="w-7 h-7 bg-gray-900 dark:bg-slate-700 rounded-full flex items-center justify-center overflow-hidden">
                  {user.avatar ? (
                    <img src={user.avatar} alt="用户头像" className="w-full h-full object-cover" />
                  ) : (
                    <span className="text-xs font-medium text-white">
                      {user.username ? user.username[0].toUpperCase() : 'U'}
                    </span>
                  )}
                </div>
                <ChevronDown className="w-3 h-3 text-gray-500" />
              </button>

              {/* 用户下拉菜单 */}
              {showUserMenu && (
                <>
                  <div
                    className="fixed inset-0 z-40"
                    onClick={() => setShowUserMenu(false)}
                  ></div>

                  <div className="absolute right-0 mt-1.5 w-48 bg-white dark:bg-slate-900 rounded border border-gray-200 dark:border-slate-700 py-1 z-50 shadow-sm">
                    <div className="px-3 py-2 border-b border-gray-100 dark:border-slate-700">
                      <p className="text-xs font-semibold text-gray-900 dark:text-slate-100">{user.username}</p>
                      <p className="text-xs text-gray-500 dark:text-slate-400 mt-0.5">{user.email}</p>
                    </div>

                    <div className="py-1">
                      <Link
                        to="/settings"
                        className="flex items-center space-x-2 px-3 py-1.5 text-xs text-gray-700 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-slate-800 hover:text-gray-900 dark:hover:text-slate-100 transition-colors"
                        onClick={() => setShowUserMenu(false)}
                      >
                        <User className="w-3.5 h-3.5" />
                        <span>个人设置</span>
                      </Link>

                      {user.isAdmin && (
                        <Link
                          to="/admin/dashboard"
                          className="flex items-center space-x-2 px-3 py-1.5 text-xs text-gray-700 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-slate-800 hover:text-gray-900 dark:hover:text-slate-100 transition-colors"
                          onClick={() => setShowUserMenu(false)}
                        >
                          <Menu className="w-3.5 h-3.5" />
                          <span>管理后台</span>
                        </Link>
                      )}
                    </div>

                    <div className="pt-1 border-t border-gray-100 dark:border-slate-700">
                      <button
                        onClick={handleLogout}
                        className="flex items-center space-x-2 px-3 py-1.5 text-xs text-gray-700 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-slate-800 hover:text-gray-900 dark:hover:text-slate-100 transition-colors w-full text-left"
                      >
                        <LogOut className="w-3.5 h-3.5" />
                        <span>退出登录</span>
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>

      {/* 全局搜索对话框 */}
      <GlobalSearch isOpen={showSearch} onClose={() => setShowSearch(false)} />
    </header>
  );
};

export default Header;
