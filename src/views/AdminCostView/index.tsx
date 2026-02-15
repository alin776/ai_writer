import React, { useState, useEffect } from 'react';
import { DollarSign, TrendingUp, Cpu, AlertCircle, Download, Calendar } from 'lucide-react';
import { Card, Button } from '../../components/common';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, PieChart, Pie, Cell } from 'recharts';
import { DataService } from '@/services/DataService';
import { formatUsdToCny } from '@/utils/currency';
import type { CostMetrics } from '@/types';

/**
 * AdminCostView 组件 - 成本监控页面
 */
const AdminCostView: React.FC = () => {
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d'>('7d');
  const [metrics, setMetrics] = useState<CostMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 深色模式动态检测
  const [isDarkMode, setIsDarkMode] = useState(
    document.documentElement.classList.contains('dark')
  );

  // 监听主题切换
  useEffect(() => {
    const observer = new MutationObserver(() => {
      setIsDarkMode(document.documentElement.classList.contains('dark'));
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class'],
    });

    return () => observer.disconnect();
  }, []);

  // 加载成本指标数据
  const loadCostMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await DataService.getCostMetrics();
      setMetrics(data);
    } catch (err: any) {
      console.error('Failed to load cost metrics:', err);
      setError(err.message || '加载成本数据失败');
    } finally {
      setLoading(false);
    }
  };

  // 组件挂载时加载数据
  useEffect(() => {
    loadCostMetrics();
  }, []);

  // 加载状态
  if (loading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">成本监控</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">查看和分析 AI 使用成本</p>
        </div>
        <Card>
          <div className="p-12 text-center">
            <DollarSign className="w-16 h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600 animate-pulse" />
            <p className="text-gray-500 dark:text-gray-400">加载中...</p>
          </div>
        </Card>
      </div>
    );
  }

  // 错误状态
  if (error || !metrics) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">成本监控</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">查看和分析 AI 使用成本</p>
        </div>
        <Card>
          <div className="p-12 text-center">
            <AlertCircle className="w-16 h-16 mx-auto mb-4 text-red-400 dark:text-red-500" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">加载失败</h3>
            <p className="text-gray-500 dark:text-gray-400 mb-4">{error || '无法加载成本数据'}</p>
            <Button onClick={loadCostMetrics}>重试</Button>
          </div>
        </Card>
      </div>
    );
  }

  // 成本统计卡片数据（基于真实数据）
  const costStats = [
    {
      label: '今日成本',
      value: formatUsdToCny(metrics.todayCost),
      change: metrics.yesterdayCost > 0
        ? `${((metrics.todayCost - metrics.yesterdayCost) / metrics.yesterdayCost * 100).toFixed(1)}%`
        : 'N/A',
      icon: DollarSign,
      bgColor: 'bg-blue-100',
      iconColor: 'text-blue-600',
      description: `${metrics.todayCalls} 次调用`,
    },
    {
      label: '本月成本',
      value: formatUsdToCny(metrics.thisMonthCost),
      change: metrics.lastMonthCost > 0
        ? `${((metrics.thisMonthCost - metrics.lastMonthCost) / metrics.lastMonthCost * 100).toFixed(1)}%`
        : 'N/A',
      icon: Cpu,
      bgColor: 'bg-blue-100',
      iconColor: 'text-blue-600',
      description: `${metrics.thisMonthCalls} 次调用`,
    },
    {
      label: '平均每次成本',
      value: metrics.thisMonthCalls > 0
        ? formatUsdToCny(metrics.thisMonthCost / metrics.thisMonthCalls)
        : '¥0.00',
      change: '-',
      icon: TrendingUp,
      bgColor: 'bg-blue-100',
      iconColor: 'text-blue-600',
      description: '本月平均',
    },
    {
      label: '昨日成本',
      value: formatUsdToCny(metrics.yesterdayCost),
      change: '-',
      icon: AlertCircle,
      bgColor: 'bg-blue-100',
      iconColor: 'text-blue-600',
      description: '对比参考',
    },
  ];

  // 成本趋势数据（根据选择的时间范围截取）
  const rangeDays = timeRange === '7d' ? 7 : timeRange === '30d' ? 30 : 90;
  const costTrendData = metrics.dailyCosts
    .slice(-rangeDays)
    .map(item => ({
      date: item.date.slice(5), // 只显示 MM-DD
      cost: parseFloat((item.cost * 7.19).toFixed(4)), // 转换为人民币，保留4位小数
    }));

  // 模型成本分布
  const modelCostData = metrics.topModels.map((model, index) => {
    const colors = ['#3B82F6', '#10B981', '#8B5CF6', '#F59E0B', '#EF4444'];
    return {
      name: model.modelName,
      value: parseFloat((model.totalCost * 7.19).toFixed(4)), // 转换为人民币，保留4位小数
      color: colors[index % colors.length],
    };
  });

  // 用户成本排行 Top 5
  const topUsers = metrics.topUsers.slice(0, 5).map(user => {
    const maxCost = Math.max(...metrics.topUsers.map(u => u.totalCost));
    return {
      userId: user.userId,
      calls: user.totalCalls,
      cost: parseFloat((user.totalCost * 7.19).toFixed(4)), // 转换为人民币，保留4位小数
      percentage: maxCost > 0 ? Math.round((user.totalCost / maxCost) * 100) : 0,
    };
  });

  // 模型详细使用（基于 topModels 数据）
  const modelDetails = metrics.topModels.map(model => ({
    name: model.modelName,
    calls: model.totalCalls,
    totalTokens: 0, // 后端暂未返回 Token 总数
    cost: parseFloat((model.totalCost * 7.19).toFixed(4)), // 转换为人民币，保留4位小数
    avgCost: model.totalCalls > 0
      ? parseFloat(((model.totalCost * 7.19) / model.totalCalls).toFixed(4))
      : 0,
    trend: '-', // 趋势数据需要历史对比，暂不实现
  }));

  return (
    <div className="space-y-6">
      {/* 页面标题和操作栏 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">成本监控</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">实时监控 AI 调用成本和使用情况</p>
        </div>
          <div className="flex items-center space-x-3">
            {/* 时间范围选择 */}
            <div className="flex items-center bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden">
              {(['7d', '30d', '90d'] as const).map((range) => (
                <button
                  key={range}
                onClick={() => setTimeRange(range)}
                className={`px-4 py-2 text-sm font-medium transition-colors ${
                  timeRange === range
                    ? 'bg-blue-600 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                }`}
                >
                  {range === '7d' ? '最近7天' : range === '30d' ? '最近30天' : '最近90天'}
                </button>
              ))}
            </div>
            <Button variant="outline" size="sm" disabled title="后端暂未开放自定义日期">
              <Calendar className="w-4 h-4 mr-2" />
              自定义日期
            </Button>
            <Button variant="outline" size="sm" disabled title="导出报告功能待实现">
              <Download className="w-4 h-4 mr-2" />
              导出报告
            </Button>
          </div>
        </div>

      {/* 成本统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {costStats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.label} background="blue" className="hover:shadow-lg transition-shadow">
              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{stat.label}</p>
                    <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">{stat.value}</p>
                    <div className="mt-2 flex items-center text-sm">
                      <span className="text-green-600 dark:text-green-400 font-medium">{stat.change}</span>
                      <span className="ml-1 text-gray-500 dark:text-gray-400">{stat.description}</span>
                    </div>
                  </div>
                  <div className={`w-12 h-12 ${stat.bgColor} dark:bg-blue-900/50 rounded-lg flex items-center justify-center flex-shrink-0`}>
                    <Icon className={`w-6 h-6 ${stat.iconColor} dark:text-blue-400`} />
                  </div>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* 图表区域 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 成本趋势 - 占2列 */}
        <Card background="blue" className="lg:col-span-2">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">成本趋势</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">最近7天每日成本变化</p>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={costTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke={isDarkMode ? "#374151" : "#E5E7EB"} />
                <XAxis dataKey="date" stroke={isDarkMode ? "#9CA3AF" : "#6B7280"} style={{ fontSize: '12px' }} />
                <YAxis
                  stroke={isDarkMode ? "#9CA3AF" : "#6B7280"}
                  style={{ fontSize: '12px' }}
                  tickFormatter={(value) => `¥${value.toFixed(4)}`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: isDarkMode ? '#1F2937' : '#ffffff',
                    border: `1px solid ${isDarkMode ? '#374151' : '#E5E7EB'}`,
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                    color: isDarkMode ? '#F3F4F6' : '#111827',
                  }}
                  labelStyle={{
                    color: isDarkMode ? '#F3F4F6' : '#111827',
                  }}
                  formatter={(value: number) => [`¥${value.toFixed(4)}`, '成本']}
                />
                <Legend
                  wrapperStyle={{
                    color: isDarkMode ? '#D1D5DB' : '#6B7280',
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="cost"
                  stroke="#3B82F6"
                  strokeWidth={3}
                  dot={{ fill: '#3B82F6', r: 6, strokeWidth: 2, stroke: '#fff' }}
                  activeDot={{ r: 8, strokeWidth: 2 }}
                  name="成本 (¥)"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* 模型成本分布 */}
        <Card background="blue">
          <div className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">模型成本分布</h3>
            {modelCostData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={modelCostData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={false}
                    outerRadius={90}
                    innerRadius={40}
                    fill="#8884d8"
                    dataKey="value"
                    paddingAngle={2}
                  >
                    {modelCostData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: isDarkMode ? '#1F2937' : '#ffffff',
                      border: `1px solid ${isDarkMode ? '#374151' : '#E5E7EB'}`,
                      borderRadius: '8px',
                      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                      color: isDarkMode ? '#F3F4F6' : '#111827',
                    }}
                    labelStyle={{
                      color: isDarkMode ? '#F3F4F6' : '#111827',
                    }}
                    formatter={(value: number) => [`¥${value.toFixed(4)}`, '成本']}
                  />
                  <Legend
                    verticalAlign="bottom"
                    height={36}
                    formatter={(value, entry: any) => {
                      const percent = entry.payload?.percent || 0;
                      return `${value} (${(percent * 100).toFixed(1)}%)`;
                    }}
                    wrapperStyle={{
                      color: isDarkMode ? '#D1D5DB' : '#6B7280',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-[300px] text-gray-400 dark:text-gray-500">
                <p>暂无数据</p>
              </div>
            )}
          </div>
        </Card>
      </div>

      {/* 模型详细使用情况 */}
      <Card background="blue">
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">模型详细使用</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-900 dark:text-gray-100">模型名称</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-900 dark:text-gray-100">调用次数</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-900 dark:text-gray-100">总 Token 数</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-900 dark:text-gray-100">总成本</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-900 dark:text-gray-100">平均成本</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-900 dark:text-gray-100">趋势</th>
                </tr>
              </thead>
              <tbody>
                {modelDetails.map((model, index) => (
                  <tr key={index} className="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="py-4 px-4 text-sm font-medium text-gray-900 dark:text-gray-100">{model.name}</td>
                    <td className="py-4 px-4 text-sm text-right text-gray-700 dark:text-gray-300">{model.calls.toLocaleString()}</td>
                    <td className="py-4 px-4 text-sm text-right text-gray-700 dark:text-gray-300">
                      {model.totalTokens > 0 ? model.totalTokens.toLocaleString() : '-'}
                    </td>
                    <td className="py-4 px-4 text-sm text-right font-medium text-gray-900 dark:text-gray-100">¥{model.cost}</td>
                    <td className="py-4 px-4 text-sm text-right text-gray-700 dark:text-gray-300">¥{model.avgCost}</td>
                    <td className="py-4 px-4 text-sm text-right">
                      <span className="text-green-600 dark:text-green-400 font-medium">{model.trend}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </Card>

      {/* 用户成本排行 */}
      <Card background="blue">
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">用户成本排行 TOP 5</h3>
          <div className="space-y-4">
            {topUsers.map((user, index) => (
              <div key={user.userId} className="flex items-center space-x-4">
                <div className="flex-shrink-0 w-8 text-center">
                  <span className="text-lg font-bold text-gray-400 dark:text-gray-500">#{index + 1}</span>
                </div>
                <div className="flex-shrink-0 w-10 h-10 bg-blue-100 dark:bg-blue-900/50 rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-blue-600 dark:text-blue-400">{(index + 1)}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">{user.userId.slice(0, 8)}...</p>
                    <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">¥{user.cost.toFixed(4)}</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-blue-600 dark:bg-blue-500 h-2 rounded-full"
                        style={{ width: `${user.percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-500 dark:text-gray-400">{user.calls} 次</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </Card>
    </div>
  );
};

export default AdminCostView;
