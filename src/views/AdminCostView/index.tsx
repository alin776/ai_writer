import React, { useState, useEffect } from 'react';
import { DollarSign, TrendingUp, Cpu, AlertCircle, Calendar, Download } from 'lucide-react';
import { ADMIN_STYLES } from '../../styles/adminStyles';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, PieChart, Pie, Cell } from 'recharts';
import { DataService } from '@/services/DataService';
import { formatUsd } from '@/utils/currency';
import type { CostMetrics } from '@/types';

/**
 * AdminCostView 组件 - 成本监控页面（增强版）
 */
const AdminCostView: React.FC = () => {
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d'>('7d');
  const [metrics, setMetrics] = useState<CostMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [isDarkMode, setIsDarkMode] = useState(
    document.documentElement.classList.contains('dark')
  );

  useEffect(() => {
    const observer = new MutationObserver(() => {
      setIsDarkMode(document.documentElement.classList.contains('dark'));
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    return () => observer.disconnect();
  }, []);

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

  useEffect(() => {
    loadCostMetrics();
  }, []);

  if (loading) {
    return (
      <div className={ADMIN_STYLES.page}>
        <div className={ADMIN_STYLES.stickyHeader}>
          <div className={ADMIN_STYLES.titleSection}>
            <h1 className={ADMIN_STYLES.title}><DollarSign className={ADMIN_STYLES.titleIcon} />成本监控</h1>
            <p className={ADMIN_STYLES.subtitle}>实时监控 AI 调用成本和使用情况</p>
          </div>
        </div>
        <div className={ADMIN_STYLES.loadingContainer}>
          <div className="text-center">
            <DollarSign className="w-16 h-16 text-gray-300 dark:text-gray-600 animate-pulse mb-4 mx-auto" />
            <p className={ADMIN_STYLES.loadingText}>加载中...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !metrics) {
    return (
      <div className={ADMIN_STYLES.page}>
        <div className={ADMIN_STYLES.stickyHeader}>
          <div className={ADMIN_STYLES.titleSection}>
            <h1 className={ADMIN_STYLES.title}><DollarSign className={ADMIN_STYLES.titleIcon} />成本监控</h1>
            <p className={ADMIN_STYLES.subtitle}>实时监控 AI 调用成本和使用情况</p>
          </div>
        </div>
        <div className={ADMIN_STYLES.tableContainer}>
          <div className="p-12 text-center">
            <AlertCircle className="w-16 h-16 mx-auto mb-4 text-red-400 dark:text-red-500" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">加载失败</h3>
            <p className="text-gray-500 dark:text-gray-400 mb-4">{error || '无法加载成本数据'}</p>
            <button onClick={loadCostMetrics} className={ADMIN_STYLES.btnPrimary}>重试</button>
          </div>
        </div>
      </div>
    );
  }

  // 成本统计卡片
  const costStats = [
    {
      label: '今日成本',
      value: formatUsd(metrics.todayCost),
      change: metrics.yesterdayCost > 0
        ? `${((metrics.todayCost - metrics.yesterdayCost) / metrics.yesterdayCost * 100).toFixed(1)}%`
        : 'N/A',
      icon: DollarSign,
      description: `${metrics.todayCalls} 次调用`,
    },
    {
      label: '本月成本',
      value: formatUsd(metrics.thisMonthCost),
      change: metrics.lastMonthCost > 0
        ? `${((metrics.thisMonthCost - metrics.lastMonthCost) / metrics.lastMonthCost * 100).toFixed(1)}%`
        : 'N/A',
      icon: Cpu,
      description: `${metrics.thisMonthCalls} 次调用`,
    },
    {
      label: '平均每次成本',
      value: metrics.thisMonthCalls > 0
        ? formatUsd(metrics.thisMonthCost / metrics.thisMonthCalls)
        : '$0.00',
      change: '-',
      icon: TrendingUp,
      description: '本月平均',
    },
    {
      label: '昨日成本',
      value: formatUsd(metrics.yesterdayCost),
      change: '-',
      icon: AlertCircle,
      description: '对比参考',
    },
  ];

  // 成本趋势数据
  const rangeDays = timeRange === '7d' ? 7 : timeRange === '30d' ? 30 : 90;
  const costTrendData = metrics.dailyCosts
    .slice(-rangeDays)
    .map(item => ({
      date: item.date.slice(5),
      cost: parseFloat((item.cost).toFixed(4)),
    }));

  // Token 构成数据（环形图）
  const allInput = metrics.topModels.reduce((s, m) => s + (m.totalInputTokens ?? 0), 0);
  const allOutput = metrics.topModels.reduce((s, m) => s + (m.totalOutputTokens ?? 0), 0);
  const allCacheRead = metrics.topModels.reduce((s, m) => s + (m.totalCacheRead ?? 0), 0);
  const allReasoning = metrics.topModels.reduce((s, m) => s + (m.totalReasoning ?? 0), 0);
  const pureInput = Math.max(allInput - allCacheRead, 0);
  const pureOutput = Math.max(allOutput - allReasoning, 0);

  const tokenCompositionData = [
    { name: 'New Input', value: pureInput, color: '#3B82F6' },
    { name: 'Cache Read', value: allCacheRead, color: '#10B981' },
    { name: 'Output', value: pureOutput, color: '#F59E0B' },
    { name: 'Reasoning', value: allReasoning, color: '#8B5CF6' },
  ].filter(d => d.value > 0);

  // 用户排行
  const topUsers = metrics.topUsers.slice(0, 5).map(user => {
    const maxCost = Math.max(...metrics.topUsers.map(u => u.totalCost));
    return {
      userId: user.userId,
      username: user.username,
      calls: user.totalCalls,
      cost: parseFloat((user.totalCost).toFixed(4)),
      percentage: maxCost > 0 ? Math.round((user.totalCost / maxCost) * 100) : 0,
      totalInputTokens: user.totalInputTokens ?? 0,
      totalOutputTokens: user.totalOutputTokens ?? 0,
      totalCacheRead: user.totalCacheRead ?? 0,
    };
  });

  // 模型详细使用
  const modelDetails = metrics.topModels.map(model => ({
    name: model.modelName,
    calls: model.totalCalls,
    inputTokens: model.totalInputTokens ?? 0,
    outputTokens: model.totalOutputTokens ?? 0,
    cacheRead: model.totalCacheRead ?? 0,
    cacheCreation: model.totalCacheCreation ?? 0,
    reasoning: model.totalReasoning ?? 0,
    cost: parseFloat((model.totalCost).toFixed(4)),
    avgCost: model.totalCalls > 0
      ? parseFloat((model.totalCost / model.totalCalls).toFixed(4))
      : 0,
  }));

  return (
    <div className={ADMIN_STYLES.page}>
      {/* 页面标题和操作栏 */}
      <div className={ADMIN_STYLES.stickyHeader}>
        <div className={ADMIN_STYLES.titleSection}>
          <div className="flex items-center justify-between">
            <div>
              <h1 className={ADMIN_STYLES.title}><DollarSign className={ADMIN_STYLES.titleIcon} />成本监控</h1>
              <p className={ADMIN_STYLES.subtitle}>实时监控 AI 调用成本和使用情况</p>
            </div>
            <div className="flex items-center space-x-3">
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
              <button className={ADMIN_STYLES.btnSecondary + ' text-sm flex items-center gap-2'} disabled title="后端暂未开放自定义日期">
                <Calendar className="w-4 h-4" />
                自定义日期
              </button>
              <button className={ADMIN_STYLES.btnSecondary + ' text-sm flex items-center gap-2'} disabled title="导出报告功能待实现">
                <Download className="w-4 h-4" />
                导出报告
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 成本统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {costStats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.label} className={ADMIN_STYLES.tableContainer + ' hover:shadow-lg transition-shadow'}>
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
                  <div className="w-12 h-12 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Icon className="w-6 h-6 text-gray-600 dark:text-gray-400" />
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* 图表区域 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        {/* 成本趋势 */}
        <div className={ADMIN_STYLES.tableContainer + ' lg:col-span-2'}>
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">成本趋势</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">每日成本变化</p>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={costTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke={isDarkMode ? "#374151" : "#E5E7EB"} />
                <XAxis dataKey="date" stroke={isDarkMode ? "#9CA3AF" : "#6B7280"} style={{ fontSize: '12px' }} />
                <YAxis stroke={isDarkMode ? "#9CA3AF" : "#6B7280"} style={{ fontSize: '12px' }} tickFormatter={(v) => `$${v.toFixed(4)}`} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: isDarkMode ? '#1F2937' : '#ffffff',
                    border: `1px solid ${isDarkMode ? '#374151' : '#E5E7EB'}`,
                    borderRadius: '8px',
                    color: isDarkMode ? '#F3F4F6' : '#111827',
                  }}
                  formatter={(value: number) => [`$${value.toFixed(4)}`, '成本']}
                />
                <Legend wrapperStyle={{ color: isDarkMode ? '#D1D5DB' : '#6B7280' }} />
                <Line type="monotone" dataKey="cost" stroke="#3B82F6" strokeWidth={3} dot={{ fill: '#3B82F6', r: 6, strokeWidth: 2, stroke: '#fff' }} activeDot={{ r: 8, strokeWidth: 2 }} name="成本 ($)" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Token 构成（替代纯成本分布） */}
        <div className={ADMIN_STYLES.tableContainer}>
          <div className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Token 构成</h3>
            {tokenCompositionData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={tokenCompositionData}
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
                    {tokenCompositionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: isDarkMode ? '#1F2937' : '#ffffff',
                      border: `1px solid ${isDarkMode ? '#374151' : '#E5E7EB'}`,
                      borderRadius: '8px',
                      color: isDarkMode ? '#F3F4F6' : '#111827',
                    }}
                    formatter={(value: number) => [value.toLocaleString(), 'Tokens']}
                  />
                  <Legend
                    verticalAlign="bottom"
                    height={36}
                    formatter={(value, entry: any) => {
                      const percent = entry.payload?.percent || 0;
                      return `${value} (${(percent * 100).toFixed(1)}%)`;
                    }}
                    wrapperStyle={{ color: isDarkMode ? '#D1D5DB' : '#6B7280' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-[300px] text-gray-400 dark:text-gray-500">
                <p>暂无数据</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 模型详细使用 — 增强版 */}
      <div className={ADMIN_STYLES.tableContainer + ' mt-6'}>
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">模型详细使用</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className={ADMIN_STYLES.tableHead}>
                <tr>
                  <th className={ADMIN_STYLES.th}>模型</th>
                  <th className={ADMIN_STYLES.thRight}>调用次数</th>
                  <th className={ADMIN_STYLES.thRight}>Input Tokens</th>
                  <th className={ADMIN_STYLES.thRight}>Output Tokens</th>
                  <th className={ADMIN_STYLES.thRight}>Cache Read</th>
                  <th className={ADMIN_STYLES.thRight}>Reasoning</th>
                  <th className={ADMIN_STYLES.thRight}>总成本</th>
                  <th className={ADMIN_STYLES.thRight}>平均成本</th>
                </tr>
              </thead>
              <tbody className={ADMIN_STYLES.tbody}>
                {modelDetails.map((model, index) => (
                  <tr key={index} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                    <td className="py-4 px-4 text-sm font-medium text-gray-900 dark:text-gray-100">{model.name}</td>
                    <td className="py-4 px-4 text-sm text-right text-gray-700 dark:text-gray-300">{model.calls.toLocaleString()}</td>
                    <td className="py-4 px-4 text-sm text-right text-gray-700 dark:text-gray-300">{model.inputTokens.toLocaleString()}</td>
                    <td className="py-4 px-4 text-sm text-right text-gray-700 dark:text-gray-300">{model.outputTokens.toLocaleString()}</td>
                    <td className="py-4 px-4 text-sm text-right text-green-600 dark:text-green-400">{model.cacheRead > 0 ? model.cacheRead.toLocaleString() : '-'}</td>
                    <td className="py-4 px-4 text-sm text-right text-purple-600 dark:text-purple-400">{model.reasoning > 0 ? model.reasoning.toLocaleString() : '-'}</td>
                    <td className="py-4 px-4 text-sm text-right font-medium text-gray-900 dark:text-gray-100">${model.cost}</td>
                    <td className="py-4 px-4 text-sm text-right text-gray-700 dark:text-gray-300">${model.avgCost}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* 用户成本排行 — 增强版 */}
      <div className={ADMIN_STYLES.tableContainer + ' mt-6'}>
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">用户成本排行 TOP 5</h3>
          <div className="space-y-4">
            {topUsers.map((user, index) => (
              <div key={user.userId} className="flex items-center space-x-4">
                <div className="flex-shrink-0 w-8 text-center">
                  <span className="text-lg font-bold text-gray-400 dark:text-gray-500">#{index + 1}</span>
                </div>
                <div className="flex-shrink-0 w-10 h-10 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-gray-600 dark:text-gray-400">{user.username.charAt(0).toUpperCase()}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">{user.username}</p>
                    <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">${user.cost.toFixed(4)}</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div className="bg-blue-600 dark:bg-blue-500 h-2 rounded-full" style={{ width: `${user.percentage}%` }} />
                    </div>
                    <span className="text-xs text-gray-500 dark:text-gray-400 whitespace-nowrap">
                      {user.calls} 次 · In:{(user.totalInputTokens / 1000).toFixed(0)}k · Out:{(user.totalOutputTokens / 1000).toFixed(0)}k
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminCostView;
