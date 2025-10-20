import React, { useEffect, useState } from 'react';
import { Users, BookOpen, Cpu, DollarSign, TrendingUp, TrendingDown, ArrowUpRight } from 'lucide-react';
import { Card } from '../../components/common';
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';

/**
 * AdminDashboardView 组件 - 管理员仪表板
 *
 * 功能：
 * - 显示系统统计数据（真实数据）
 * - 显示使用趋势图表
 * - 快速访问管理功能
 */
const AdminDashboardView: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [statistics, setStatistics] = useState<any>(null);
  const [growthData, setGrowthData] = useState<any[]>([]);
  const [aiUsageData, setAiUsageData] = useState<any[]>([]);
  const { showToast } = useGlobalStore();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      // 并行加载所有数据
      const [stats, growth, aiUsage] = await Promise.all([
        DataService.getAdminStatistics(),
        DataService.getUsersGrowth(7),
        DataService.getAIUsage(),
      ]);

      setStatistics(stats);
      setGrowthData(growth.data || []);
      setAiUsageData(aiUsage.data || []);
    } catch (error) {
      console.error('加载管理后台数据失败:', error);
      showToast('error', '加载数据失败');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!statistics) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <p className="text-gray-500">暂无数据</p>
      </div>
    );
  }

  // 统计数据配置（使用可选链和默认值避免错误）
  const aiCalls = statistics.aiCalls || statistics.ai_calls || { total: 0, change: '+0%' };
  const cost = statistics.cost || { total: 0, change: '+0%' };
  
  const stats = [
    {
      label: '总用户数',
      value: (statistics.users?.total || 0).toLocaleString(),
      change: statistics.users?.change || '+0%',
      trend: (statistics.users?.change || '+0%').startsWith('+') ? 'up' as const : 'down' as const,
      icon: Users,
      bgColor: 'bg-blue-100',
      iconColor: 'text-blue-600',
      trendColor: (statistics.users?.change || '+0%').startsWith('+') ? 'text-green-600' : 'text-red-600',
    },
    {
      label: '总作品数',
      value: (statistics.works?.total || 0).toLocaleString(),
      change: statistics.works?.change || '+0%',
      trend: (statistics.works?.change || '+0%').startsWith('+') ? 'up' as const : 'down' as const,
      icon: BookOpen,
      bgColor: 'bg-green-100',
      iconColor: 'text-green-600',
      trendColor: (statistics.works?.change || '+0%').startsWith('+') ? 'text-green-600' : 'text-red-600',
    },
    {
      label: 'AI 调用次数',
      value: (aiCalls.total || 0).toLocaleString(),
      change: aiCalls.change || '+0%',
      trend: (aiCalls.change || '+0%').startsWith('+') ? 'up' as const : 'down' as const,
      icon: Cpu,
      bgColor: 'bg-purple-100',
      iconColor: 'text-purple-600',
      trendColor: (aiCalls.change || '+0%').startsWith('+') ? 'text-green-600' : 'text-red-600',
    },
    {
      label: '总成本',
      value: `¥${(cost.total || 0).toLocaleString()}`,
      change: cost.change || '+0%',
      trend: (cost.change || '+0%').startsWith('+') ? 'up' as const : 'down' as const,
      icon: DollarSign,
      bgColor: 'bg-orange-100',
      iconColor: 'text-orange-600',
      trendColor: (cost.change || '+0%').startsWith('-') ? 'text-green-600' : 'text-red-600',
    },
  ];

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
              <button 
                className="text-sm text-blue-600 hover:text-blue-700 flex items-center"
                onClick={loadData}
              >
                刷新
                <ArrowUpRight className="w-4 h-4 ml-1" />
              </button>
            </div>
            
            {growthData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={growthData}>
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
            ) : (
              <div className="flex items-center justify-center h-[300px] text-gray-500">
                暂无增长数据
              </div>
            )}
          </div>
        </Card>

        {/* AI 模型使用统计 */}
        <Card>
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">AI 模型使用</h3>
              <button 
                className="text-sm text-blue-600 hover:text-blue-700 flex items-center"
                onClick={loadData}
              >
                刷新
                <ArrowUpRight className="w-4 h-4 ml-1" />
              </button>
            </div>
            
            {aiUsageData.length > 0 ? (
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
            ) : (
              <div className="flex items-center justify-center h-[300px] text-gray-500">
                暂无 AI 使用数据
              </div>
            )}
          </div>
        </Card>
      </div>

      {/* 额外信息卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <div className="p-6">
            <h4 className="text-sm font-medium text-gray-600 mb-2">总章节数</h4>
            <p className="text-2xl font-bold text-gray-900">
              {(statistics.chapters?.total || 0).toLocaleString()}
            </p>
          </div>
        </Card>
        
        <Card>
          <div className="p-6">
            <h4 className="text-sm font-medium text-gray-600 mb-2">总字数</h4>
            <p className="text-2xl font-bold text-gray-900">
              {(statistics.words?.total || 0).toLocaleString()}
            </p>
          </div>
        </Card>
        
        <Card>
          <div className="p-6">
            <h4 className="text-sm font-medium text-gray-600 mb-2">平均作品字数</h4>
            <p className="text-2xl font-bold text-gray-900">
              {(statistics.works?.total || 0) > 0 
                ? Math.round((statistics.words?.total || 0) / (statistics.works?.total || 1)).toLocaleString()
                : '0'
              }
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default AdminDashboardView;
