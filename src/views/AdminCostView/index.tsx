import React, { useState } from 'react';
import { DollarSign, TrendingUp, Cpu, AlertCircle, Download, Calendar } from 'lucide-react';
import { Card, Button } from '../../components/common';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, PieChart, Pie, Cell } from 'recharts';

/**
 * AdminCostView 组件 - 成本监控页面
 */
const AdminCostView: React.FC = () => {
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d'>('7d');

  // 成本趋势数据
  const costTrendData = [
    { date: '10-09', cost: 124, calls: 1234 },
    { date: '10-10', cost: 156, calls: 1456 },
    { date: '10-11', cost: 143, calls: 1324 },
    { date: '10-12', cost: 189, calls: 1678 },
    { date: '10-13', cost: 167, calls: 1523 },
    { date: '10-14', cost: 198, calls: 1789 },
    { date: '10-15', cost: 234, calls: 2134 },
  ];

  // 模型成本分布
  const modelCostData = [
    { name: 'GPT-4', value: 456, color: '#3B82F6' },
    { name: 'GPT-3.5', value: 234, color: '#10B981' },
    { name: 'Claude', value: 344, color: '#8B5CF6' },
    { name: 'DALL-E', value: 200, color: '#F59E0B' },
  ];

  // 成本统计
  const costStats = [
    {
      label: '总成本',
      value: '¥1,234',
      change: '+15.2%',
      icon: DollarSign,
      bgColor: 'bg-blue-100',
      iconColor: 'text-blue-600',
      description: '本月累计',
    },
    {
      label: 'AI 调用次数',
      value: '12,345',
      change: '+23.1%',
      icon: Cpu,
      bgColor: 'bg-green-100',
      iconColor: 'text-green-600',
      description: '本月累计',
    },
    {
      label: '平均每次成本',
      value: '¥0.10',
      change: '-5.3%',
      icon: TrendingUp,
      bgColor: 'bg-purple-100',
      iconColor: 'text-purple-600',
      description: '优化后降低',
    },
    {
      label: '预计月度成本',
      value: '¥2,468',
      change: '+12.8%',
      icon: AlertCircle,
      bgColor: 'bg-orange-100',
      iconColor: 'text-orange-600',
      description: '基于当前趋势',
    },
  ];

  // 用户成本排行
  const topUsers = [
    { name: '张三', calls: 2345, cost: 234.5, percentage: 19 },
    { name: '李四', calls: 1987, cost: 198.7, percentage: 16 },
    { name: '王五', calls: 1654, cost: 165.4, percentage: 13 },
    { name: '赵六', calls: 1432, cost: 143.2, percentage: 12 },
    { name: '钱七', calls: 1234, cost: 123.4, percentage: 10 },
  ];

  // 模型详细使用
  const modelDetails = [
    {
      name: 'GPT-4',
      calls: 5234,
      totalTokens: 2345678,
      cost: 456.78,
      avgCost: 0.087,
      trend: '+12%',
    },
    {
      name: 'GPT-3.5 Turbo',
      calls: 4123,
      totalTokens: 1876543,
      cost: 234.56,
      avgCost: 0.057,
      trend: '+8%',
    },
    {
      name: 'Claude 2',
      calls: 2988,
      totalTokens: 1234567,
      cost: 344.23,
      avgCost: 0.115,
      trend: '+15%',
    },
    {
      name: 'DALL-E 3',
      calls: 1567,
      totalTokens: 0,
      cost: 200.12,
      avgCost: 0.128,
      trend: '+5%',
    },
  ];

  return (
    <div className="space-y-6">
      {/* 页面标题和操作栏 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">成本监控</h1>
          <p className="mt-2 text-gray-600">实时监控 AI 调用成本和使用情况</p>
        </div>
        <div className="flex items-center space-x-3">
          {/* 时间范围选择 */}
          <div className="flex items-center bg-white border border-gray-300 rounded-lg overflow-hidden">
            {(['7d', '30d', '90d'] as const).map((range) => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-4 py-2 text-sm font-medium transition-colors ${
                  timeRange === range
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                {range === '7d' ? '最近7天' : range === '30d' ? '最近30天' : '最近90天'}
              </button>
            ))}
          </div>
          <Button variant="outline" size="sm">
            <Calendar className="w-4 h-4 mr-2" />
            自定义日期
          </Button>
          <Button variant="outline" size="sm">
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
            <Card key={stat.label} className="hover:shadow-lg transition-shadow">
              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                    <p className="mt-2 text-3xl font-bold text-gray-900">{stat.value}</p>
                    <div className="mt-2 flex items-center text-sm">
                      <span className="text-green-600 font-medium">{stat.change}</span>
                      <span className="ml-1 text-gray-500">{stat.description}</span>
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
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 成本趋势 - 占2列 */}
        <Card className="lg:col-span-2">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">成本趋势</h3>
                <p className="text-sm text-gray-600 mt-1">每日成本和调用次数变化</p>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={costTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis dataKey="date" stroke="#6B7280" style={{ fontSize: '12px' }} />
                <YAxis yAxisId="left" stroke="#6B7280" style={{ fontSize: '12px' }} />
                <YAxis yAxisId="right" orientation="right" stroke="#6B7280" style={{ fontSize: '12px' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    border: '1px solid #E5E7EB',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                  }}
                />
                <Legend />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="cost"
                  stroke="#3B82F6"
                  strokeWidth={2}
                  dot={{ fill: '#3B82F6', r: 4 }}
                  activeDot={{ r: 6 }}
                  name="成本 (¥)"
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="calls"
                  stroke="#10B981"
                  strokeWidth={2}
                  dot={{ fill: '#10B981', r: 4 }}
                  activeDot={{ r: 6 }}
                  name="调用次数"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* 模型成本分布 */}
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">模型成本分布</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={modelCostData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {modelCostData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    border: '1px solid #E5E7EB',
                    borderRadius: '8px',
                  }}
                  formatter={(value: number) => `¥${value}`}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {/* 模型详细使用情况 */}
      <Card>
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">模型详细使用</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-900">模型名称</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-900">调用次数</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-900">总 Token 数</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-900">总成本</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-900">平均成本</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-900">趋势</th>
                </tr>
              </thead>
              <tbody>
                {modelDetails.map((model, index) => (
                  <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-4 px-4 text-sm font-medium text-gray-900">{model.name}</td>
                    <td className="py-4 px-4 text-sm text-right text-gray-700">{model.calls.toLocaleString()}</td>
                    <td className="py-4 px-4 text-sm text-right text-gray-700">
                      {model.totalTokens > 0 ? model.totalTokens.toLocaleString() : '-'}
                    </td>
                    <td className="py-4 px-4 text-sm text-right font-medium text-gray-900">¥{model.cost}</td>
                    <td className="py-4 px-4 text-sm text-right text-gray-700">¥{model.avgCost}</td>
                    <td className="py-4 px-4 text-sm text-right">
                      <span className="text-green-600 font-medium">{model.trend}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </Card>

      {/* 用户成本排行 */}
      <Card>
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">用户成本排行 TOP 5</h3>
          <div className="space-y-4">
            {topUsers.map((user, index) => (
              <div key={index} className="flex items-center space-x-4">
                <div className="flex-shrink-0 w-8 text-center">
                  <span className="text-lg font-bold text-gray-400">#{index + 1}</span>
                </div>
                <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-blue-600">{user.name[0]}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-sm font-medium text-gray-900">{user.name}</p>
                    <p className="text-sm font-semibold text-gray-900">¥{user.cost}</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${user.percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-500">{user.calls} 次</span>
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
