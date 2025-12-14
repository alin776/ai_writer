import React, { useState, useEffect } from 'react';
import { Search, Plus, Trash2, Copy, CheckCircle2, Gift, Coins, TrendingUp, DollarSign, FileDown } from 'lucide-react';
import { Button, Card, Input, Loading } from '../../components/common';
import { AdminCreditsService, type RedeemCodeInfo } from '../../services/AdminCreditsService';
import { useGlobalStore } from '../../store/globalStore';
import { formatDate } from '../../utils/formatDate';

interface CreditStats {
  totalUsers: number;
  totalBalance: number;
  totalRecharged: number;
  totalConsumed: number;
  totalGifted: number;
  totalTransactions: number;
}

const defaultStats: CreditStats = {
  totalUsers: 0,
  totalBalance: 0,
  totalRecharged: 0,
  totalConsumed: 0,
  totalGifted: 0,
  totalTransactions: 0,
};

/**
 * AdminCreditsView 组件 - 积分管理页面
 *
 * 功能：
 * - 批量生成兑换码
 * - 查询兑换码列表
 * - 删除兑换码
 * - 赠送积分给用户
 * - 查看积分统计
 */
const AdminCreditsView: React.FC = () => {
  const [codes, setCodes] = useState<RedeemCodeInfo[]>([]);
  const [stats, setStats] = useState<CreditStats | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [usedFilter, setUsedFilter] = useState<'all' | 'used' | 'unused'>('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [showGiftModal, setShowGiftModal] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [gifting, setGifting] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [copiedCode, setCopiedCode] = useState<string | null>(null);

  // 生成兑换码表单
  const [generateForm, setGenerateForm] = useState({
    count: 1,
    credits: 100,
    validDays: 0, // 0表示无限期
    remark: '',
  });

  // 赠送积分表单
  const [giftForm, setGiftForm] = useState({
    userId: '',
    credits: 100,
    reason: '',
  });

  const { showToast } = useGlobalStore();

  /**
   * 加载数据
   */
  const loadData = async () => {
    try {
      setIsLoading(true);
      const [codesResponse, statsResponse] = await Promise.all([
        AdminCreditsService.listCodes({
          page: 1,
          page_size: 100,
          is_used: usedFilter === 'all' ? undefined : usedFilter === 'used',
          search: searchQuery.trim() || undefined,
        }),
        AdminCreditsService.getStats(),
      ]);

      let filteredCodes = codesResponse.items || [];
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase();
        filteredCodes = filteredCodes.filter(
          (code) =>
            code.code.toLowerCase().includes(query) ||
            code.remark?.toLowerCase().includes(query)
        );
      }

      setCodes(filteredCodes);
      const normalizedStats: CreditStats = { ...defaultStats, ...(statsResponse || {}) };
      setStats(normalizedStats);
    } catch (err) {
      const message = err instanceof Error ? err.message : '加载数据失败';
      showToast('error', message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [usedFilter, searchQuery]);

  /**
   * 批量生成兑换码
   */
  const handleGenerate = async () => {
    if (generateForm.count < 1 || generateForm.count > 100) {
      showToast('error', '生成数量必须在1-100之间');
      return;
    }

    if (generateForm.credits < 1) {
      showToast('error', '积分数必须大于0');
      return;
    }

    try {
      setGenerating(true);
      const request: any = {
        count: generateForm.count,
        credits: generateForm.credits,
      };

      if (generateForm.validDays > 0) {
        request.expires_days = generateForm.validDays;
      }

      if (generateForm.remark.trim()) {
        request.remark = generateForm.remark.trim();
      }

      const response = await AdminCreditsService.generateCodes(request);
      showToast('success', `成功生成 ${response.codes.length} 个兑换码`);
      setShowGenerateModal(false);
      setGenerateForm({ count: 1, credits: 100, validDays: 0, remark: '' });
      loadData();
    } catch (err) {
      const message = err instanceof Error ? err.message : '生成兑换码失败';
      showToast('error', message);
    } finally {
      setGenerating(false);
    }
  };

  /**
   * 赠送积分
   */
  const handleGift = async () => {
    if (!giftForm.userId.trim()) {
      showToast('error', '请输入用户ID');
      return;
    }

    if (giftForm.credits < 1) {
      showToast('error', '积分数必须大于0');
      return;
    }

    if (!giftForm.reason.trim()) {
      showToast('error', '请输入赠送原因');
      return;
    }

    try {
      setGifting(true);
      await AdminCreditsService.giftCredits({
        user_id: giftForm.userId.trim(),
        amount: giftForm.credits,
        description: giftForm.reason.trim(),
      });
      showToast('success', '积分赠送成功');
      setShowGiftModal(false);
      setGiftForm({ userId: '', credits: 100, reason: '' });
      loadData();
    } catch (err) {
      const message = err instanceof Error ? err.message : '赠送积分失败';
      showToast('error', message);
    } finally {
      setGifting(false);
    }
  };

  /**
   * 删除兑换码
   */
  const handleDelete = async (id: string, code: string) => {
    if (!confirm(`确定要删除兑换码 ${code} 吗？`)) {
      return;
    }

    try {
      setDeletingId(id);
      await AdminCreditsService.deleteCode(id);
      showToast('success', '兑换码已删除');
      loadData();
    } catch (err) {
      const message = err instanceof Error ? err.message : '删除失败';
      showToast('error', message);
    } finally {
      setDeletingId(null);
    }
  };

  /**
   * 复制兑换码
   */
  const handleCopy = async (code: string) => {
    try {
      await navigator.clipboard.writeText(code);
      setCopiedCode(code);
      showToast('success', '已复制到剪贴板');
      setTimeout(() => setCopiedCode(null), 2000);
    } catch (err) {
      showToast('error', '复制失败');
    }
  };

  /**
   * 批量复制当前列表兑换码
   */
  const handleCopyAll = async () => {
    if (!codes.length) {
      showToast('warning', '暂无可复制的兑换码');
      return;
    }
    const lines = codes.map((code) => code.code).join('\n');
    try {
      await navigator.clipboard.writeText(lines);
      showToast('success', '已复制当前列表的兑换码');
    } catch (err) {
      showToast('error', '批量复制失败');
    }
  };

  /**
   * 导出当前列表兑换码为 CSV
   */
  const handleExportCsv = () => {
    if (!codes.length) {
      showToast('warning', '暂无可导出的兑换码');
      return;
    }
    const header = ['code', 'credits', 'expiresAt', 'isUsed', 'remark'];
    const escape = (val: string | number | null | undefined) => {
      const str = val === null || val === undefined ? '' : String(val);
      return `"${str.replace(/"/g, '""')}"`;
    };
    const rows = codes.map((code) => [
      escape(code.code),
      escape(code.credits),
      escape(code.expiresAt || '无限期'),
      escape(code.isUsed ? '已使用' : '未使用'),
      escape(code.remark || ''),
    ]);
    const csv = [header.map(escape).join(','), ...rows.map((r) => r.join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `redeem_codes_${Date.now()}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    showToast('success', '已导出 CSV');
  };

  if (isLoading && !stats) {
    return <Loading />;
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">积分管理</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">管理兑换码和用户积分</p>
        </div>
        <div className="flex gap-3">
          <Button onClick={() => setShowGiftModal(true)} variant="outline" icon={<Gift className="w-4 h-4" />}>
            赠送积分
          </Button>
          <Button onClick={() => setShowGenerateModal(true)} icon={<Plus className="w-4 h-4" />}>
            生成兑换码
          </Button>
        </div>
      </div>

      {/* 统计卡片 */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card background="blue">
            <div className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">积分用户数</p>
                  <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">{stats.totalUsers.toLocaleString()}</p>
                </div>
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center">
                  <Coins className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
              </div>
            </div>
          </Card>

          <Card background="blue">
            <div className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">总余额</p>
                  <p className="mt-2 text-3xl font-bold text-green-600 dark:text-green-400">{stats.totalBalance.toLocaleString()}</p>
                </div>
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900/50 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-green-600 dark:text-green-400" />
                </div>
              </div>
            </div>
          </Card>

          <Card background="blue">
            <div className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">累计充值</p>
                  <p className="mt-2 text-3xl font-bold text-purple-600 dark:text-purple-400">{stats.totalRecharged.toLocaleString()}</p>
                </div>
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/50 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                </div>
              </div>
            </div>
          </Card>

          <Card background="blue">
            <div className="p-6">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">累计消费</p>
              <p className="mt-2 text-2xl font-bold text-gray-900 dark:text-white">{stats.totalConsumed.toLocaleString()}</p>
            </div>
          </Card>

          <Card background="blue">
            <div className="p-6">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">累计赠送</p>
              <p className="mt-2 text-2xl font-bold text-gray-900 dark:text-white">{stats.totalGifted.toLocaleString()}</p>
            </div>
          </Card>

          <Card background="blue">
            <div className="p-6">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">交易总数</p>
              <p className="mt-2 text-2xl font-bold text-gray-900 dark:text-white">{stats.totalTransactions.toLocaleString()}</p>
            </div>
          </Card>
        </div>
      )}

      {/* 兑换码列表 */}
      <Card background="blue">
        <div className="p-6 space-y-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <Input
                placeholder="搜索兑换码或备注..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                icon={<Search className="w-5 h-5 text-gray-400 dark:text-gray-500" />}
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setUsedFilter('all')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  usedFilter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                全部
              </button>
              <button
                onClick={() => setUsedFilter('unused')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  usedFilter === 'unused' ? 'bg-green-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                未使用
              </button>
              <button
                onClick={() => setUsedFilter('used')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  usedFilter === 'used' ? 'bg-gray-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                已使用
              </button>
              <button
                onClick={handleCopyAll}
                className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                title="一键复制当前列表兑换码"
              >
                复制全部
              </button>
              <button
                onClick={handleExportCsv}
                className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center space-x-1"
                title="导出当前列表为 CSV"
              >
                <FileDown className="w-4 h-4" />
                <span>导出CSV</span>
              </button>
            </div>
          </div>

          {/* 兑换码表格 */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-gray-100">兑换码</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-gray-100">积分</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-gray-100">状态</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-gray-100">使用者</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-gray-100">使用时间</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-gray-100">过期时间</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-gray-100">备注</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-gray-900 dark:text-gray-100">操作</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {codes.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
                      {searchQuery || usedFilter !== 'all' ? '没有找到匹配的兑换码' : '暂无兑换码'}
                    </td>
                  </tr>
                ) : (
                  codes.map((code) => (
                    <tr key={code.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-4 py-3 text-sm">
                        <div className="flex items-center space-x-2">
                          <code className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded font-mono text-blue-600 dark:text-blue-400">
                            {code.code}
                          </code>
                          <button
                            onClick={() => handleCopy(code.code)}
                            className="p-1 text-gray-400 dark:text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                            title="复制兑换码"
                          >
                            {copiedCode === code.code ? (
                              <CheckCircle2 className="w-4 h-4 text-green-600 dark:text-green-400" />
                            ) : (
                              <Copy className="w-4 h-4" />
                            )}
                          </button>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-gray-100">{code.credits}</td>
                      <td className="px-4 py-3 text-sm">
                        {code.isUsed ? (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                            已使用
                          </span>
                        ) : (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300">
                            未使用
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                        {code.usedBy ? (
                          <code className="text-xs">{code.usedBy.slice(0, 8)}...</code>
                        ) : (
                          '-'
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                        {code.usedAt ? formatDate(code.usedAt) : '-'}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                        {code.expiresAt ? formatDate(code.expiresAt) : '无限期'}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                        {code.remark || '-'}
                      </td>
                      <td className="px-4 py-3 text-sm text-right">
                        <button
                          onClick={() => handleDelete(code.id, code.code)}
                          disabled={deletingId === code.id || code.isUsed}
                          className="p-1.5 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                          title={code.isUsed ? '已使用的兑换码不能删除' : '删除兑换码'}
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </Card>

      {/* 生成兑换码模态框 */}
      {showGenerateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <Card background="blue" className="w-full max-w-md mx-4">
            <div className="p-6 space-y-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">批量生成兑换码</h3>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  生成数量 (1-100)
                </label>
                <Input
                  type="number"
                  min="1"
                  max="100"
                  value={generateForm.count}
                  onChange={(e) => setGenerateForm({ ...generateForm, count: parseInt(e.target.value) || 1 })}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  每个兑换码的积分数
                </label>
                <Input
                  type="number"
                  min="1"
                  value={generateForm.credits}
                  onChange={(e) => setGenerateForm({ ...generateForm, credits: parseInt(e.target.value) || 100 })}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  有效期 (天，0表示无限期)
                </label>
                <Input
                  type="number"
                  min="0"
                  value={generateForm.validDays}
                  onChange={(e) => setGenerateForm({ ...generateForm, validDays: parseInt(e.target.value) || 0 })}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  备注 (可选)
                </label>
                <Input
                  placeholder="备注信息"
                  value={generateForm.remark}
                  onChange={(e) => setGenerateForm({ ...generateForm, remark: e.target.value })}
                />
              </div>

              <div className="flex gap-3 pt-4">
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => {
                    setShowGenerateModal(false);
                    setGenerateForm({ count: 1, credits: 100, validDays: 0, remark: '' });
                  }}
                  disabled={generating}
                >
                  取消
                </Button>
                <Button className="flex-1" onClick={handleGenerate} disabled={generating}>
                  {generating ? '生成中...' : '生成'}
                </Button>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* 赠送积分模态框 */}
      {showGiftModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <Card background="blue" className="w-full max-w-md mx-4">
            <div className="p-6 space-y-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">赠送积分</h3>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  用户ID
                </label>
                <Input
                  placeholder="请输入用户ID"
                  value={giftForm.userId}
                  onChange={(e) => setGiftForm({ ...giftForm, userId: e.target.value })}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  积分数量
                </label>
                <Input
                  type="number"
                  min="1"
                  value={giftForm.credits}
                  onChange={(e) => setGiftForm({ ...giftForm, credits: parseInt(e.target.value) || 100 })}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  赠送原因
                </label>
                <Input
                  placeholder="请输入赠送原因"
                  value={giftForm.reason}
                  onChange={(e) => setGiftForm({ ...giftForm, reason: e.target.value })}
                />
              </div>

              <div className="flex gap-3 pt-4">
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => {
                    setShowGiftModal(false);
                    setGiftForm({ userId: '', credits: 100, reason: '' });
                  }}
                  disabled={gifting}
                >
                  取消
                </Button>
                <Button className="flex-1" onClick={handleGift} disabled={gifting}>
                  {gifting ? '赠送中...' : '赠送'}
                </Button>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};

export default AdminCreditsView;
