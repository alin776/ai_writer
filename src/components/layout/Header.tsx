/**
 * 顶部导航栏组件
 */
import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Bell,
  Search,
  ArrowLeft,
  MoreHorizontal,
  Clock
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { GlobalSearch } from '@/components/search/GlobalSearch';
import { useNotificationStore } from '@/store/notificationStore';
import NotificationDropdown from '@/components/notifications/NotificationDropdown';
import ThemeToggle from '@/components/common/ThemeToggle';
import { toLocaleTime } from '@/utils/dateFormat';
import type { LanguageCode } from '@/i18n';

const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t, i18n } = useTranslation();
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

  // 获取当前页面标题
  const getPageTitle = () => {
    const path = location.pathname;

    // 创作模块
    if (path.includes('/works') && path !== '/works') return t('header.pages.workDetail');
    if (path === '/works') return '作品管理';
    if (path.includes('/knowledge')) return '知识库';
    if (path.includes('/channels')) return '频道';

    // 图书馆模块
    if (path.includes('/library/novel-square')) return '小说广场';
    if (path.includes('/library/my-bookshelf')) return '我的书架';

    // 我的服务模块
    if (path.includes('/tasks')) return '任务中心';
    if (path.includes('/service/credits')) return '我的积分';
    if (path.includes('/service/usage')) return '使用记录';
    if (path.includes('/service/obtain')) return '获取积分';

    // 底部导航
    if (path.includes('/user/')) return '个人主页';
    if (path.includes('/notifications')) return '通知中心';
    if (path.includes('/settings')) return '系统设置';

    // 管理员模块
    if (path.includes('/admin/dashboard')) return t('header.pages.dashboard');
    if (path.includes('/admin/users')) return t('header.pages.users');
    if (path.includes('/admin/ai-models')) return t('header.pages.aiModels');
    if (path.includes('/admin/cost')) return t('header.pages.cost');
    if (path.includes('/admin/notifications')) return '通知管理';
    if (path.includes('/admin/tasks')) return '任务配置';

    // 编辑器
    if (path.includes('/editor')) return t('header.pages.editor');

    return t('app.name');
  };

  // 判断是否在编辑器页面
  const isEditorPage = location.pathname.includes('/editor');

  return (
    <header className="bg-white dark:bg-slate-900 border-b border-gray-200 dark:border-slate-700 h-11 flex items-center px-4 sticky top-0 z-40">
      <div className="flex items-center justify-between w-full max-w-full">
        {/* 左侧内容 - 根据页面类型动态显示 */}
        <div className="flex items-center space-x-3 min-w-0">
          {/* 编辑器页面：返回按钮 + 作品/章节信息 */}
          {isEditorPage ? (
            <>
              <button
                onClick={() => navigate('/works')}
                className="p-1.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800 rounded transition-colors"
                title={t('header.actions.backToWorks')}
              >
                <ArrowLeft className="w-4 h-4" />
              </button>
              <div className="min-w-0">
                <h1 className="text-sm font-semibold text-gray-900 dark:text-slate-100 truncate">{t('header.pages.workDetail')}</h1>
                <div className="flex items-center space-x-2 text-xs text-gray-500 dark:text-slate-400">
                  <Clock className="w-3 h-3" />
                  <span>{toLocaleTime(lastSaved, i18n.language as LanguageCode)} {t('header.actions.saved')}</span>
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
                {t('header.actions.export')}
              </button>
              <button className="px-3 py-1.5 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-500 rounded transition-colors shadow-sm">
                {t('header.actions.aiContinue')}
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
            title={t('header.actions.searchShortcut')}
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
        </div>
      </div>

      {/* 全局搜索对话框 */}
      <GlobalSearch isOpen={showSearch} onClose={() => setShowSearch(false)} />
    </header>
  );
};

export default Header;
