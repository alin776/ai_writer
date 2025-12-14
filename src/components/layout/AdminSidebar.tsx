import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, Cpu, DollarSign, ArrowLeft, Gift, Coins, Bell, Trophy } from 'lucide-react';

const AdminSidebar: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  const menuItems = [
    {
      path: '/admin/dashboard',
      icon: LayoutDashboard,
      label: '数据面板',
      description: '系统统计概览',
    },
    {
      path: '/admin/users',
      icon: Users,
      label: '用户管理',
      description: '管理系统用户',
    },
    {
      path: '/admin/invitations',
      icon: Gift,
      label: '邀请码管理',
      description: '生成和管理邀请码',
    },
    {
      path: '/admin/credits',
      icon: Coins,
      label: '积分管理',
      description: '管理兑换码和积分',
    },
    {
      path: '/admin/tasks',
      icon: Trophy,
      label: '任务配置',
      description: '管理任务奖励系统',
    },
    {
      path: '/admin/ai-models',
      icon: Cpu,
      label: 'AI 模型',
      description: '配置AI模型',
    },
    {
      path: '/admin/cost',
      icon: DollarSign,
      label: '成本监控',
      description: '查看使用成本',
    },
    {
      path: '/admin/notifications',
      icon: Bell,
      label: '通知管理',
      description: '发送系统通知',
    },
  ];

  return (
    <aside className="w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col">
      <div className="p-4 border-b border-gray-200 dark:border-gray-800">
        <Link
          to="/works"
          className="flex items-center space-x-2 text-sm text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-gray-100 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>返回作品管理</span>
        </Link>
      </div>

      <div className="px-4 py-3 border-b border-gray-100 dark:border-gray-800">
        <h2 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
          管理后台
        </h2>
      </div>

      <nav className="flex-1 overflow-y-auto p-3 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`
                flex items-start space-x-3 px-3 py-2.5 rounded-lg transition-colors
                ${
                  active
                    ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-100'
                    : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900 dark:text-gray-200 dark:hover:bg-gray-800 dark:hover:text-gray-100'
                }
              `}
            >
              <Icon
                className={`w-5 h-5 flex-shrink-0 mt-0.5 ${
                  active ? 'text-blue-600 dark:text-blue-300' : 'text-gray-400 dark:text-gray-500'
                }`}
              />
              <div className="flex-1 min-w-0">
                <div className={`text-sm font-medium ${active ? 'text-blue-700' : 'text-gray-900 dark:text-gray-100'}`}>
                  {item.label}
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{item.description}</div>
              </div>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-800">
        <div className="flex items-start space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full flex-shrink-0 mt-1.5"></div>
          <div>
            <p className="text-xs font-medium text-gray-900 dark:text-gray-100">管理员模式</p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">具有完整系统权限</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default AdminSidebar;













