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
  Plus,
  Save,
  MoreHorizontal,
  Clock
} from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import { DataService } from '@/services/DataService';
import { useNavigate } from 'react-router-dom';
import Button from '@/components/common/Button';
import { GlobalSearch } from '@/components/search/GlobalSearch';

const Header: React.FC = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [lastSaved] = useState<Date>(new Date());
  const [showSearch, setShowSearch] = useState(false);

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
    if (path.includes('/editor')) return '写作中';
    if (path.includes('/admin/dashboard')) return '数据面板';
    if (path.includes('/admin/users')) return '用户管理';
    if (path.includes('/admin/ai-models')) return 'AI 模型';
    if (path.includes('/admin/cost')) return '成本监控';
    if (path.includes('/settings')) return '系统设置';
    return 'AI Writer';
  };

  // 判断是否在编辑器页面
  const isEditorPage = location.pathname.includes('/editor');

  // 判断是否在作品列表页
  const isWorksPage = location.pathname === '/works';

  return (
    <header className="bg-white border-b border-gray-200 h-14 flex items-center px-4 sticky top-0 z-40">
      <div className="flex items-center justify-between w-full max-w-full">
        {/* 左侧内容 - 根据页面类型动态显示 */}
        <div className="flex items-center space-x-3 min-w-0">
          {/* 编辑器页面：返回按钮 + 作品/章节信息 */}
          {isEditorPage ? (
            <>
              <button
                onClick={() => navigate('/works')}
                className="p-1.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded transition-colors"
                title="返回作品列表"
              >
                <ArrowLeft className="w-4 h-4" />
              </button>
              <div className="min-w-0">
                <h1 className="text-sm font-semibold text-gray-900 truncate">当前作品名称</h1>
                <div className="flex items-center space-x-2 text-xs text-gray-500">
                  <Clock className="w-3 h-3" />
                  <span>{lastSaved.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })} 已保存</span>
                </div>
              </div>
            </>
          ) : (
            /* 其他页面：显示页面标题 */
            <h1 className="text-base font-semibold text-gray-900">{getPageTitle()}</h1>
          )}
        </div>

        {/* 右侧操作区 - 根据页面类型动态显示 */}
        <div className="flex items-center space-x-2">
          {/* 编辑器页面的特殊操作 */}
          {isEditorPage && (
            <>
              <button className="px-3 py-1.5 text-xs font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded transition-colors">
                导出
              </button>
              <button className="px-3 py-1.5 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded transition-colors shadow-sm">
                AI 续写
              </button>
              <button className="p-1.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded transition-colors">
                <MoreHorizontal className="w-4 h-4" />
              </button>
              <div className="h-4 w-px bg-gray-200 mx-1"></div>
            </>
          )}

          {/* 作品列表页：新建作品按钮 */}
          {isWorksPage && (
            <>
              <button
                className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded transition-colors shadow-sm"
                onClick={() => alert('创建新作品功能')}
              >
                <Plus className="w-3.5 h-3.5" />
                <span>新建作品</span>
              </button>
              <div className="h-4 w-px bg-gray-200 mx-1"></div>
            </>
          )}

          {/* 通用操作：搜索和通知 */}
          <button 
            className="p-1.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded transition-colors"
            onClick={() => setShowSearch(true)}
            title="搜索 (Cmd+K)"
          >
            <Search className="w-4 h-4" />
          </button>

          <button className="relative p-1.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded transition-colors">
            <Bell className="w-4 h-4" />
            <span className="absolute top-1 right-1 w-1.5 h-1.5 bg-blue-600 rounded-full"></span>
          </button>

          {/* 分隔线 */}
          <div className="h-4 w-px bg-gray-200 mx-1"></div>

          {/* 用户菜单 */}
          {user && (
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-2 px-2 py-1 hover:bg-gray-100 rounded transition-colors"
              >
                <div className="w-7 h-7 bg-gray-900 rounded-full flex items-center justify-center">
                  <span className="text-xs font-medium text-white">
                    {user.username ? user.username[0].toUpperCase() : 'U'}
                  </span>
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

                  <div className="absolute right-0 mt-1.5 w-48 bg-white rounded border border-gray-200 py-1 z-50 shadow-sm">
                    <div className="px-3 py-2 border-b border-gray-100">
                      <p className="text-xs font-semibold text-gray-900">{user.username}</p>
                      <p className="text-xs text-gray-500 mt-0.5">{user.email}</p>
                    </div>

                    <div className="py-1">
                      <Link
                        to="/settings"
                        className="flex items-center space-x-2 px-3 py-1.5 text-xs text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors"
                        onClick={() => setShowUserMenu(false)}
                      >
                        <User className="w-3.5 h-3.5" />
                        <span>个人设置</span>
                      </Link>

                      {user.isAdmin && (
                        <Link
                          to="/admin/dashboard"
                          className="flex items-center space-x-2 px-3 py-1.5 text-xs text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors"
                          onClick={() => setShowUserMenu(false)}
                        >
                          <Menu className="w-3.5 h-3.5" />
                          <span>管理后台</span>
                        </Link>
                      )}
                    </div>

                    <div className="pt-1 border-t border-gray-100">
                      <button
                        onClick={handleLogout}
                        className="flex items-center space-x-2 px-3 py-1.5 text-xs text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors w-full text-left"
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
