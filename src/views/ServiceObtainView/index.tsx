import React, { useEffect, useState } from 'react';
import { Card, Button, Input } from '../../components/common';
import { useCreditsStore } from '../../store/creditsStore';
import { useInvitationsStore } from '../../store/invitationsStore';
import { useGlobalStore } from '../../store/globalStore';
import { Gift, Users, Award, Clock, Copy, ChevronDown, ChevronUp } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';

const ServiceObtainView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'redeem' | 'invite'>('redeem');
  const [redeemCode, setRedeemCode] = useState('');
  const [isRedeeming, setIsRedeeming] = useState(false);
  const [expandedCodes, setExpandedCodes] = useState<Set<string>>(new Set());
  const [showGenerateDialog, setShowGenerateDialog] = useState(false);
  // 前端固定为 3 次，与后端校验保持一致
  const [generateParams] = useState({ maxUses: 3, expiresDays: 60 });
  const [isGenerating, setIsGenerating] = useState(false);

  const { redeem } = useCreditsStore();
  const { stats, myCodes, isLoading, fetchStats, fetchMyCodes, generateCode } = useInvitationsStore();
  const { showToast } = useGlobalStore();

  useEffect(() => {
    fetchStats();
    fetchMyCodes();
  }, [fetchStats, fetchMyCodes]);

  const handleRedeem = async () => {
    if (redeemCode.length !== 12) {
      showToast('error', '兑换码必须是12位字符');
      return;
    }

    setIsRedeeming(true);
    try {
      const result = await redeem(redeemCode);
      showToast('success', `兑换成功！获得 ${result.credits.toFixed(2)} 积分`);
      setRedeemCode('');
    } catch (error: any) {
      // 后端返回 { detail: "错误信息" }
      showToast('error', error?.detail || error?.message || '兑换失败');
    } finally {
      setIsRedeeming(false);
    }
  };

  const handleCopyInviteLink = async (code: string) => {
    try {
      const inviteLink = `${window.location.origin}/auth?invitation_code=${code}`;
      await navigator.clipboard.writeText(inviteLink);
      showToast('success', '邀请链接已复制到剪贴板');
    } catch (error) {
      showToast('error', '复制失败，请手动复制');
    }
  };

  const toggleCodeExpanded = (code: string) => {
    const newExpanded = new Set(expandedCodes);
    if (newExpanded.has(code)) {
      newExpanded.delete(code);
    } else {
      newExpanded.add(code);
    }
    setExpandedCodes(newExpanded);
  };

  const handleGenerateCode = async () => {
    setIsGenerating(true);
    try {
      await generateCode(generateParams.maxUses, generateParams.expiresDays);
      showToast('success', '邀请码生成成功！');
      setShowGenerateDialog(false);
      fetchMyCodes();
      fetchStats();
    } catch (error: any) {
      showToast('error', error?.detail || error?.message || '生成失败');
    } finally {
      setIsGenerating(false);
    }
  };

  const canGenerateMore = stats ? stats.remainingQuota > 0 : false;

  return (
    <div className="h-full overflow-y-auto overflow-x-hidden bg-gray-50 dark:bg-gray-900">
      <div className="w-[1152px] mx-auto p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">获取积分</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">通过兑换码或邀请好友获取积分</p>
        </div>

        <div className="flex space-x-2 border-b border-gray-200 dark:border-gray-700">
          <button
            onClick={() => setActiveTab('redeem')}
            className={`px-4 py-2 text-sm font-medium transition-colors ${
              activeTab === 'redeem'
                ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }`}
          >
            兑换码
          </button>
          <button
            onClick={() => setActiveTab('invite')}
            className={`px-4 py-2 text-sm font-medium transition-colors ${
              activeTab === 'invite'
                ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }`}
          >
            邀请好友
          </button>
        </div>

        {activeTab === 'redeem' ? (
          <Card padding="lg">
            <div className="space-y-6">
              <div className="flex items-center space-x-2">
                <Gift className="w-5 h-5 text-amber-600 dark:text-amber-500" />
                <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">兑换积分</h2>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    输入12位兑换码
                  </label>
                  <Input
                    value={redeemCode}
                    onChange={(e) => setRedeemCode(e.target.value.toUpperCase())}
                    placeholder="请输入兑换码"
                    maxLength={12}
                    className="font-mono"
                  />
                  <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                    兑换码长度为12位，输入时会自动转换为大写
                  </p>
                </div>

                <Button
                  onClick={handleRedeem}
                  disabled={redeemCode.length !== 12 || isRedeeming}
                  className="w-full"
                >
                  {isRedeeming ? '兑换中...' : '兑换'}
                </Button>
              </div>

              <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg">
                <h3 className="text-sm font-medium text-blue-900 dark:text-blue-300 mb-2">说明</h3>
                <ul className="text-sm text-blue-800 dark:text-blue-400 space-y-1 list-disc list-inside">
                  <li>每个兑换码只能使用一次</li>
                  <li>兑换码可能有使用期限，请及时兑换</li>
                  <li>兑换成功后，积分将立即到账</li>
                </ul>
              </div>
            </div>
          </Card>
        ) : (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card padding="md">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">邀请总数</span>
                  <Users className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="mt-2 text-2xl font-bold text-gray-900 dark:text-gray-100">
                  {stats?.totalInvitations || 0}
                </div>
              </Card>

              <Card padding="md">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">激活数</span>
                  <Award className="w-4 h-4 text-green-600 dark:text-green-400" />
                </div>
                <div className="mt-2 text-2xl font-bold text-gray-900 dark:text-gray-100">
                  {stats?.totalActivated || 0}
                </div>
              </Card>

              <Card padding="md">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">获得奖励</span>
                  <Gift className="w-4 h-4 text-amber-600 dark:text-amber-500" />
                </div>
                <div className="mt-2 text-2xl font-bold text-amber-600 dark:text-amber-500">
                  {stats?.totalRewards.toFixed(2) || '0.00'}
                </div>
              </Card>

              <Card padding="md">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">剩余配额</span>
                  <Clock className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                </div>
                <div className="mt-2 text-2xl font-bold text-purple-600 dark:text-purple-400">
                  {stats?.remainingQuota || 0}
                </div>
              </Card>
            </div>

            <Card padding="lg">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">我的邀请码</h2>
                  <Button
                    onClick={() => setShowGenerateDialog(true)}
                    disabled={!canGenerateMore || isLoading}
                    size="sm"
                  >
                    生成新邀请码
                  </Button>
                </div>

                {isLoading && myCodes.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">加载中...</div>
                ) : myCodes.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    暂无邀请码，点击上方按钮生成
                  </div>
                ) : (
                  <div className="space-y-3">
                    {myCodes.map((codeDetail) => {
                      const isExpanded = expandedCodes.has(codeDetail.code);
                      const isExpired = codeDetail.expiresAt
                        ? new Date(codeDetail.expiresAt) < new Date()
                        : false;

                      return (
                        <div
                          key={codeDetail.id}
                          className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
                        >
                          <div className="p-4 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                            <div className="flex items-center justify-between">
                              <div className="flex items-center space-x-3">
                                <code className="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded font-mono text-sm font-medium text-gray-900 dark:text-gray-100">
                                  {codeDetail.code}
                                </code>
                                {isExpired && (
                                  <span className="px-2 py-0.5 bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300 text-xs rounded">
                                    已过期
                                  </span>
                                )}
                              </div>

                              <div className="flex items-center space-x-2">
                                <span className="text-sm text-gray-600 dark:text-gray-400">
                                  {codeDetail.usedCount} / {codeDetail.maxUses || '∞'}
                                </span>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => handleCopyInviteLink(codeDetail.code)}
                                  title="复制邀请链接"
                                >
                                  <Copy className="w-4 h-4" />
                                </Button>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => toggleCodeExpanded(codeDetail.code)}
                                >
                                  {isExpanded ? (
                                    <ChevronUp className="w-4 h-4" />
                                  ) : (
                                    <ChevronDown className="w-4 h-4" />
                                  )}
                                </Button>
                              </div>
                            </div>

                            <div className="mt-2 flex items-center space-x-4 text-xs text-gray-500">
                              <span>
                                创建时间:{' '}
                                {formatDistanceToNow(new Date(codeDetail.createdAt), {
                                  addSuffix: true,
                                  locale: zhCN,
                                })}
                              </span>
                              {codeDetail.expiresAt && (
                                <span>
                                  过期时间:{' '}
                                  {formatDistanceToNow(new Date(codeDetail.expiresAt), {
                                    addSuffix: true,
                                    locale: zhCN,
                                  })}
                                </span>
                              )}
                            </div>
                          </div>

                          {isExpanded && codeDetail.invitees && (
                            <div className="px-4 py-3 bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
                              <h4 className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
                                被邀请人 ({codeDetail.invitees.length})
                              </h4>
                              {codeDetail.invitees.length === 0 ? (
                                <p className="text-xs text-gray-500 dark:text-gray-400">暂无被邀请人</p>
                              ) : (
                                <div className="space-y-2">
                                  {codeDetail.invitees.map((invitee, idx) => (
                                    <div
                                      key={idx}
                                      className="flex items-center justify-between text-xs"
                                    >
                                      <span className="text-gray-700 dark:text-gray-300">{invitee.username}</span>
                                      <div className="flex items-center space-x-2">
                                        <span
                                          className={`px-2 py-0.5 rounded ${
                                            invitee.status === 'active'
                                              ? 'bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300'
                                              : 'bg-orange-100 dark:bg-orange-900/50 text-orange-700 dark:text-orange-300'
                                          }`}
                                        >
                                          {invitee.status === 'active' ? '已激活' : '待激活'}
                                        </span>
                                        <span className="text-gray-500">
                                          {formatDistanceToNow(new Date(invitee.registeredAt), {
                                            addSuffix: true,
                                            locale: zhCN,
                                          })}
                                        </span>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </Card>
          </div>
        )}

        {showGenerateDialog && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card padding="lg" className="w-full max-w-md">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">生成邀请码</h3>

              <div className="space-y-4">
                <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg">
                  <h4 className="text-sm font-medium text-blue-900 dark:text-blue-300 mb-2">邀请码规则</h4>
                  <ul className="text-sm text-blue-800 dark:text-blue-400 space-y-1 list-disc list-inside">
                    <li>每个邀请码最多使用 3 次</li>
                    <li>有效期固定为 60 天（2个月）</li>
                    <li>邀请好友注册后，满足激活条件即可获得奖励</li>
                  </ul>
                </div>

                <div className="flex space-x-3 pt-4">
                  <Button
                    variant="outline"
                    onClick={() => setShowGenerateDialog(false)}
                    className="flex-1"
                    disabled={isGenerating}
                  >
                    取消
                  </Button>
                  <Button onClick={handleGenerateCode} className="flex-1" disabled={isGenerating}>
                    {isGenerating ? '生成中...' : '生成邀请码'}
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default ServiceObtainView;
