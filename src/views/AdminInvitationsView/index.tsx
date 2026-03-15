import React, { useState, useEffect } from 'react';
import { Search, Plus, Trash2, Copy, CheckCircle2, AlertCircle, Gift, Ticket } from 'lucide-react';
import { ADMIN_STYLES } from '../../styles/adminStyles';
import {
  AdminInvitationsService,
  type AdminInvitationInfo,
  type AdminInvitationStats,
} from '../../services/AdminInvitationsService';
import { useGlobalStore } from '../../store/globalStore';
import { formatDate, formatShortDate } from '../../utils/formatDate';

/**
 * AdminInvitationsView 组件 - 邀请码管理页面
 *
 * 功能：
 * - 生成邀请码
 * - 查询邀请码列表
 * - 删除未使用的邀请码
 * - 显示统计信息
 */
const AdminInvitationsView: React.FC = () => {
  const [invitations, setInvitations] = useState<AdminInvitationInfo[]>([]);
  const [stats, setStats] = useState<AdminInvitationStats>({ totalCodes: 0, activeCodes: 0, expiredCodes: 0, exhaustedCodes: 0, totalUsages: 0, totalActivated: 0, totalRewards: 0 });
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'expired' | 'exhausted'>('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [copiedCode, setCopiedCode] = useState<string | null>(null);

  // 生成表单
  const [generateForm, setGenerateForm] = useState({
    customCode: '',
    maxUsageCount: 1,
    validDays: 30,
    remark: '',
  });

  const { showToast } = useGlobalStore();

  /**
   * 加载邀请码列表
   */
  const loadInvitations = async () => {
    try {
      setIsLoading(true);
      const params: any = { page: 1, pageSize: 100 };
      if (statusFilter !== 'all') {
        params.status = statusFilter;
      }
      if (searchQuery.trim()) {
        params.search = searchQuery.trim();
      }

      const response = await AdminInvitationsService.list(params);
      setInvitations(response.items || []);
      setStats(response.stats || { totalCodes: 0, activeCodes: 0, expiredCodes: 0, exhaustedCodes: 0 });
    } catch (err) {
      const message = err instanceof Error ? err.message : '加载邀请码失败';
      showToast('error', message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadInvitations();
  }, [statusFilter, searchQuery]);

  /**
   * 生成邀请码
   */
  const handleGenerate = async () => {
    if (generateForm.customCode && (generateForm.customCode.length < 3 || generateForm.customCode.length > 8)) {
      showToast('error', '自定义邀请码长度必须在3-8位之间');
      return;
    }

    if (generateForm.maxUsageCount < 1 || generateForm.maxUsageCount > 100) {
      showToast('error', '最大使用次数必须在1-100之间');
      return;
    }

    if (generateForm.validDays < 1 || generateForm.validDays > 365) {
      showToast('error', '有效期必须在1-365天之间');
      return;
    }

    try {
      setGenerating(true);
      const request: any = {
        maxUses: generateForm.maxUsageCount,
        expiresDays: generateForm.validDays,
      };

      if (generateForm.customCode.trim()) {
        request.custom_code = generateForm.customCode.trim();
      }

      if (generateForm.remark.trim()) {
        request.remark = generateForm.remark.trim();
      }

      const response = await AdminInvitationsService.generate(request);
      showToast('success', `邀请码生成成功: ${response.code}`);
      setShowGenerateModal(false);
      setGenerateForm({ customCode: '', maxUsageCount: 1, validDays: 30, remark: '' });
      loadInvitations();
    } catch (err) {
      const message = err instanceof Error ? err.message : '生成邀请码失败';
      showToast('error', message);
    } finally {
      setGenerating(false);
    }
  };

  /**
   * 删除邀请码
   */
  const handleDelete = async (id: string, code: string) => {
    if (!confirm(`确定要删除邀请码 ${code} 吗？`)) {
      return;
    }

    try {
      setDeletingId(id);
      await AdminInvitationsService.delete(id);
      showToast('success', '邀请码已删除');
      loadInvitations();
    } catch (err) {
      const message = err instanceof Error ? err.message : '删除失败';
      showToast('error', message);
    } finally {
      setDeletingId(null);
    }
  };

  /**
   * 构造可直接访问注册页的邀请链接
   */
  const buildInviteLink = (code: string) => {
    const origin = typeof window !== 'undefined' ? window.location.origin : '';
    return origin ? `${origin}/register?code=${code}` : code;
  };

  /**
   * 复制邀请码链接
   */
  const handleCopy = async (code: string) => {
    try {
      const link = buildInviteLink(code);
      await navigator.clipboard.writeText(link);
      setCopiedCode(code);
      showToast('success', '已复制邀请链接');
      setTimeout(() => setCopiedCode(null), 2000);
    } catch (err) {
      showToast('error', '复制失败');
    }
  };

  /**
   * 获取状态显示
   */
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'active':
        return <span className="px-2 py-1 rounded text-xs font-medium bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300">有效</span>;
      case 'expired':
        return <span className="px-2 py-1 rounded text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">已过期</span>;
      case 'exhausted':
        return <span className="px-2 py-1 rounded text-xs font-medium bg-orange-100 dark:bg-orange-900/50 text-orange-700 dark:text-orange-300">已用完</span>;
      default:
        return <span className="px-2 py-1 rounded text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">未知</span>;
    }
  };

  if (isLoading && invitations.length === 0) {
    return (
      <div className={ADMIN_STYLES.page}>
        <div className={ADMIN_STYLES.loadingContainer}>
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={ADMIN_STYLES.page}>
      <div className={ADMIN_STYLES.stickyHeader}>
        {/* 页面标题 */}
        <div className="flex items-center justify-between">
          <div className={ADMIN_STYLES.titleSection}>
            <h1 className={ADMIN_STYLES.title}><Ticket className={ADMIN_STYLES.titleIcon} />邀请码管理</h1>
            <p className={ADMIN_STYLES.subtitle}>生成和管理系统邀请码</p>
          </div>
          <button onClick={() => setShowGenerateModal(true)} className={ADMIN_STYLES.btnPrimary + ' flex items-center gap-2'}>
            <Plus className="w-4 h-4" />生成邀请码
          </button>
        </div>

        {/* 统计卡片 */}
        <div className={ADMIN_STYLES.filterCard}>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div><p className={ADMIN_STYLES.statLabel}>总数</p><p className={ADMIN_STYLES.statValue}>{stats.totalCodes}</p></div>
            <div><p className={ADMIN_STYLES.statLabel}>有效</p><p className="text-2xl font-bold text-green-600 dark:text-green-400">{stats.activeCodes}</p></div>
            <div><p className={ADMIN_STYLES.statLabel}>已过期</p><p className="text-2xl font-bold text-gray-600 dark:text-gray-400">{stats.expiredCodes}</p></div>
            <div><p className={ADMIN_STYLES.statLabel}>已用完</p><p className="text-2xl font-bold text-orange-600 dark:text-orange-400">{stats.exhaustedCodes}</p></div>
          </div>
        </div>
      </div>

      {/* 搜索筛选 + 邀请码表格 */}
      <div className={ADMIN_STYLES.tableContainer}>
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 dark:text-gray-500" />
              <input
                placeholder="搜索邀请码或备注..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className={ADMIN_STYLES.searchInput}
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setStatusFilter('all')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  statusFilter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                全部
              </button>
              <button
                onClick={() => setStatusFilter('active')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  statusFilter === 'active' ? 'bg-green-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                有效
              </button>
              <button
                onClick={() => setStatusFilter('expired')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  statusFilter === 'expired' ? 'bg-gray-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                已过期
              </button>
              <button
                onClick={() => setStatusFilter('exhausted')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  statusFilter === 'exhausted' ? 'bg-orange-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                已用完
              </button>
            </div>
          </div>
        </div>

        {/* 邀请码表格 */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className={ADMIN_STYLES.tableHead}>
              <tr>
                <th className={ADMIN_STYLES.th}>邀请码</th>
                <th className={ADMIN_STYLES.th}>使用次数</th>
                <th className={ADMIN_STYLES.th}>状态</th>
                <th className={ADMIN_STYLES.th}>过期时间</th>
                <th className={ADMIN_STYLES.th}>备注</th>
                <th className={ADMIN_STYLES.th}>创建时间</th>
                <th className={ADMIN_STYLES.thRight}>操作</th>
              </tr>
            </thead>
            <tbody className={ADMIN_STYLES.tbody}>
                {invitations.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
                      {searchQuery || statusFilter !== 'all' ? '没有找到匹配的邀请码' : '暂无邀请码'}
                    </td>
                  </tr>
                ) : (
                  invitations.map((invitation) => (
                    <tr key={invitation.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-4 py-3 text-sm">
                        <div className="flex items-center space-x-2">
                          <code className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded font-mono text-blue-600 dark:text-blue-400">
                            {invitation.code}
                          </code>
                          <button
                            onClick={() => handleCopy(invitation.code)}
                            className="p-1 text-gray-400 dark:text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                            title="复制邀请链接"
                          >
                            {copiedCode === invitation.code ? (
                              <CheckCircle2 className="w-4 h-4 text-green-600 dark:text-green-400" />
                            ) : (
                              <Copy className="w-4 h-4" />
                            )}
                          </button>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                        {invitation.usedCount} / {invitation.maxUses}
                      </td>
                      <td className="px-4 py-3 text-sm">{getStatusBadge(invitation.status)}</td>
                      <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                        {invitation.expiresAt ? formatShortDate(invitation.expiresAt) : '无限期'}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                        {invitation.remark || '-'}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                        {formatDate(invitation.createdAt)}
                      </td>
                      <td className="px-4 py-3 text-sm text-right">
                        <button
                          onClick={() => handleDelete(invitation.id, invitation.code)}
                          disabled={deletingId === invitation.id || invitation.usedCount > 0}
                          className="p-1.5 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                          title={invitation.usedCount > 0 ? '已使用的邀请码不能删除' : '删除邀请码'}
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

      {/* 生成邀请码模态框 */}
      {showGenerateModal && (
        <div className={ADMIN_STYLES.modalOverlay}>
          <div className={ADMIN_STYLES.modalContainer + ' max-w-md'}>
            <div className="p-6 space-y-4">
              <h3 className={ADMIN_STYLES.modalTitle}>生成邀请码</h3>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  自定义邀请码 (可选，3-8位)
                </label>
                <input
                  placeholder="留空则自动生成"
                  value={generateForm.customCode}
                  onChange={(e) => setGenerateForm({ ...generateForm, customCode: e.target.value })}
                  className={ADMIN_STYLES.modalInput}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  最大使用次数 (1-100)
                </label>
                <input
                  type="number"
                  min={1}
                  max={100}
                  value={generateForm.maxUsageCount}
                  onChange={(e) => setGenerateForm({ ...generateForm, maxUsageCount: parseInt(e.target.value) || 1 })}
                  className={ADMIN_STYLES.modalInput}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  有效期 (天，1-365)
                </label>
                <input
                  type="number"
                  min={1}
                  max={365}
                  value={generateForm.validDays}
                  onChange={(e) => setGenerateForm({ ...generateForm, validDays: parseInt(e.target.value) || 30 })}
                  className={ADMIN_STYLES.modalInput}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  备注 (可选)
                </label>
                <input
                  placeholder="备注信息"
                  value={generateForm.remark}
                  onChange={(e) => setGenerateForm({ ...generateForm, remark: e.target.value })}
                  className={ADMIN_STYLES.modalInput}
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  className={ADMIN_STYLES.btnSecondary + ' flex-1'}
                  onClick={() => {
                    setShowGenerateModal(false);
                    setGenerateForm({ customCode: '', maxUsageCount: 1, validDays: 30, remark: '' });
                  }}
                  disabled={generating}
                >
                  取消
                </button>
                <button className={ADMIN_STYLES.btnPrimary + ' flex-1'} onClick={handleGenerate} disabled={generating}>
                  {generating ? '生成中...' : '生成'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminInvitationsView;
