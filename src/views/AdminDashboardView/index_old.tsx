import React, { useEffect, useState } from 'react';
import { Users, BookOpen, Cpu, DollarSign, TrendingUp, TrendingDown, ArrowUpRight } from 'lucide-react';
import { Card } from '../../components/common';
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

/**
 * AdminDashboardView 组件 - 管理员仪表板
 *
 * 功能：
 * - 显示系统统计数据
 * - 显示使用趋势图表
 * - 快速访问管理功能
 */
const AdminDashboardView: React.FC = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 模拟数据加载
    const timer = setTimeout(() => setLoading(false), 500);
    return () => clearTimeout(timer);
  }, []);

  // 统计数据配置 - 修复动态颜色类名问题
  const stats = [
    {
      label: '总用户数',
      value: '1,234',
      change: '+12.5%',
      trend: 'up' as const,
      icon: Users,
      bgColor: 'bg-blue-100',
      iconColor: 'text-blue-600',
      trendColor: 'text-green-600',
    },
    {
      label: '总作品数',
      value: '5,678',
      change: '+8.2%',
      trend: 'up' as const,
      icon: BookOpen,
      bgColor: 'bg-green-100',
      iconColor: 'text-green-600',
      trendColor: 'text-green-600',
    },
    {
      label: 'AI 调用次数',
      value: '12,345',
      change: '+23.1%',
      trend: 'up' as const,
      icon: Cpu,
      bgColor: 'bg-purple-100',
      iconColor: 'text-purple-600',
      trendColor: 'text-green-600',
    },
    {
      label: '总成本',
      value: '¥1,234',
      change: '-5.3%',
      trend: 'down' as const,
      icon: DollarSign,
      bgColor: 'bg-orange-100',
      iconColor: 'text-orange-600',
      trendColor: 'text-red-600',
    },
  ];

  // 用户增长趋势数据
  const userGrowthData = [
    { date: '1月', users: 820, works: 1200 },
    { date: '2月', users: 890, works: 1400 },
    { date: '3月', users: 950, works: 1650 },
    { date: '4月', users: 1020, works: 1900 },
    { date: '5月', users: 1100, works: 2150 },
    { date: '6月', users: 1180, works: 2400 },
    { date: '7月', users: 1234, works: 2678 },
  ];

  // AI 调用统计数据
  const aiUsageData = [
    { model: 'GPT-4', calls: 5234, cost: 456 },
    { model: 'GPT-3.5', calls: 4123, cost: 234 },
    { model: 'Claude', calls: 2988, cost: 344 },
  ];

  // 最近活动
  const recentActivities = [
    { user: '张三', action: '创建了新作品', work: '《星际漫游》', time: '5分钟前' },
    { user: '李四', action: '完成了章节', work: '《时空之门》第3章', time: '15分钟前' },
    { user: '王五', action: '使用 AI 续写', work: '《未来世界》', time: '30分钟前' },
    { user: '赵六', action: '发布了作品', work: '《末日求生》', time: '1小时前' },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">数据面板</h1>
        <p className="mt-2 text-gray-600">系统运营数据总览</p>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          const TrendIcon = stat.trend === 'up' ? TrendingUp : TrendingDown;
          return (
            <Card key={stat.label} className="hover:shadow-lg transition-shadow">
              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                    <p className="mt-2 text-3xl font-bold text-gray-900">{stat.value}</p>
                    <div className={`mt-2 flex items-center text-sm ${stat.trendColor}`}>
                      <TrendIcon className="w-4 h-4 mr-1" />
                      <span className="font-medium">{stat.change}</span>
                      <span className="ml-1 text-gray-500">vs 上月</span>
                    </div>
                  </div>
                  <div className={`w-12 h-12 ${stat.bgColor} rounded-lg flex items-center justify-center flex-shrink-0`}>
                    <Icon className={`w-6 h-6 ${stat.iconColor}`} />
                  </div>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* 图表区域 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 用户与作品增长趋势 */}
        <Card>
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">增长趋势</h3>
              <button className="text-sm text-blue-600 hover:text-blue-700 flex items-center">
                查看详情
                <ArrowUpRight className="w-4 h-4 ml-1" />
              </button>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={userGrowthData}>
                <defs>
                  <linearGradient id="colorUsers" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorWorks" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis dataKey="date" stroke="#6B7280" style={{ fontSize: '12px' }} />
                <YAxis stroke="#6B7280" style={{ fontSize: '12px' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    border: '1px solid #E5E7EB',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                  }}
                />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="users"
                  stroke="#3B82F6"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorUsers)"
                  name="用户数"
                />
                <Area
                  type="monotone"
                  dataKey="works"
                  stroke="#10B981"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorWorks)"
                  name="作品数"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* AI 模型使用统计 */}
        <Card>
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">AI 模型使用</h3>
              <button className="text-sm text-blue-600 hover:text-blue-700 flex items-center">
                查看详情
                <ArrowUpRight className="w-4 h-4 ml-1" />
              </button>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={aiUsageData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis dataKey="model" stroke="#6B7280" style={{ fontSize: '12px' }} />
                <YAxis stroke="#6B7280" style={{ fontSize: '12px' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    border: '1px solid #E5E7EB',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                  }}
                />
                <Legend />
                <Bar dataKey="calls" fill="#8B5CF6" name="调用次数" radius={[8, 8, 0, 0]} />
                <Bar dataKey="cost" fill="#F59E0B" name="成本 (¥)" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {/* 最近活动 */}
      <Card>
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">最近活动</h3>
          <div className="space-y-4">
            {recentActivities.map((activity, index) => (
              <div key={index} className="flex items-start space-x-3 pb-4 border-b border-gray-100 last:border-0 last:pb-0">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-sm font-medium text-blue-600">{activity.user[0]}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900">
                    <span className="font-medium">{activity.user}</span> {activity.action}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">{activity.work}</p>
                </div>
                <span className="text-xs text-gray-500 flex-shrink-0">{activity.time}</span>
              </div>
            ))}
          </div>
        </div>
      </Card>
    </div>
  );
};

export default AdminDashboardView;
