/**
 * 管理员通知管理页面 - 简约黑白设计
 *
 * 功能:
 * - 创建和发送通知
 * - 活动通知支持完整的奖励配置
 * - 查看所有通知列表
 * - 编辑和删除通知
 */

import React, { useState, useEffect } from 'react';
import {
  Plus,
  Send,
  Edit,
  Trash2,
  Bell,
  Search,
  Save,
  X,
  Image as ImageIcon,
  Gift,
  Trophy,
  Award,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import { ApiAdapter } from '../services/ApiAdapter';
import type {
  NotificationCreate,
  NotificationResponse,
} from '../types/notification';
import {
  NotificationPriority,
  NotificationCategory,
  NotificationType,
} from '../types/notification';
import {
  ActivityType,
  RewardType,
  type Reward,
  type ActivityRules,
  type InvitationRules,
  type CompetitionRules,
} from '../types/activity';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';

// 扩展通知创建接口以包含活动规则
interface ActivityNotificationCreate extends NotificationCreate {
  activity_type?: ActivityType | null;
  activity_rules?: ActivityRules | null;
}

const AdminNotificationsView: React.FC = () => {
  const api = new ApiAdapter();

  // 状态管理
  const [notifications, setNotifications] = useState<NotificationResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingNotification, setEditingNotification] = useState<NotificationResponse | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'published' | 'draft'>('all');
  const [uploadingCover, setUploadingCover] = useState(false);
  const [showRewardsConfig, setShowRewardsConfig] = useState(false);

  // 表单状态
  const [formData, setFormData] = useState<ActivityNotificationCreate>({
    title: '',
    content: '',
    category: NotificationCategory.ANNOUNCEMENT,
    type: NotificationType.ANNOUNCEMENT,
    priority: NotificationPriority.NORMAL,
    displayType: ['notification'],
    publishType: 'immediate',
    targetUsers: 'all',
    actionButton: undefined,
    coverImageUrl: '',
    showOnce: false,
    activity_type: null,
    activity_rules: null,
  });

  // 加载通知列表
  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const response = await api.get<{
        total: number;
        items: NotificationResponse[];
      }>('/notifications/admin/notifications', {
        params: { page: 1, pageSize: 50 }
      });
      setNotifications(response.items || []);
    } catch (error) {
      console.error('加载通知失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  // 处理表单提交
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // 验证展示方式至少选择一种
    if (formData.displayType.length === 0) {
      alert('请至少选择一种展示方式');
      return;
    }

    setLoading(true);

    try {
      // 准备提交的数据
      const submitData: any = { ...formData };

      // 如果是活动类型，必须包含活动配置
      if (formData.type === NotificationType.EVENT) {
        if (!formData.activity_type || !formData.activity_rules) {
          alert('活动类型通知必须配置活动信息');
          setLoading(false);
          return;
        }

        // 确保活动配置存在且正确
        submitData.activity_type = formData.activity_type;
        submitData.activity_rules = formData.activity_rules;

        console.log('📤 活动配置数据:', {
          activity_type: submitData.activity_type,
          activity_rules: submitData.activity_rules
        });
      } else {
        // 非活动类型，清除活动字段
        submitData.activity_type = null;
        submitData.activity_rules = null;
      }

      console.log('📤 最终提交数据:', JSON.stringify(submitData, null, 2));

      let response;
      if (editingNotification) {
        console.log(`📝 更新通知 ID: ${editingNotification.id}`);
        response = await api.put(`/notifications/admin/notifications/${editingNotification.id}`, submitData);
        console.log('📥 更新响应:', response);
      } else {
        console.log('📝 创建新通知');
        response = await api.post('/notifications/admin/notifications', submitData);
        console.log('📥 创建响应:', response);
      }

      await fetchNotifications();
      setShowCreateModal(false);
      setEditingNotification(null);
      resetForm();

      alert('保存成功！');
    } catch (error) {
      console.error('❌ 保存通知失败:', error);
      alert('保存失败,请检查表单数据');
    } finally {
      setLoading(false);
    }
  };

  // 删除通知
  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除这条通知吗?')) return;

    try {
      await api.delete(`/notifications/admin/notifications/${id}`);
      await fetchNotifications();
    } catch (error) {
      console.error('删除失败:', error);
    }
  };

  // 发布通知
  const handlePublish = async (id: string) => {
    try {
      await api.post(`/notifications/admin/notifications/${id}/publish`);
      await fetchNotifications();
    } catch (error) {
      console.error('发布失败:', error);
    }
  };

  // 重置表单
  const resetForm = () => {
    setFormData({
      title: '',
      content: '',
      category: NotificationCategory.ANNOUNCEMENT,
      type: NotificationType.ANNOUNCEMENT,
      priority: NotificationPriority.NORMAL,
      displayType: ['notification'],
      publishType: 'immediate',
      targetUsers: 'all',
      actionButton: undefined,
      coverImageUrl: '',
      showOnce: false,
      activity_type: null,
      activity_rules: null,
    });
    setShowRewardsConfig(false);
  };

  // 处理图片上传
  const handleCoverUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
    if (!allowedTypes.includes(file.type)) {
      alert('仅支持 JPG/PNG/WebP/GIF 图片文件');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      alert('文件过大，请选择 10MB 以下的图片');
      return;
    }

    setUploadingCover(true);
    try {
      const formDataUpload = new FormData();
      formDataUpload.append('file', file);

      const response = await api.post<{ coverUrl: string }>(
        '/notifications/admin/notifications/upload-cover',
        formDataUpload
      );

      setFormData(prev => ({ ...prev, coverImageUrl: response.coverUrl }));
    } catch (error) {
      console.error('图片上传失败:', error);
      alert('图片上传失败，请重试');
    } finally {
      setUploadingCover(false);
    }
  };

  // 开始编辑
  const handleEdit = (notification: NotificationResponse) => {
    console.log('\n' + '='.repeat(80));
    console.log('📝 开始编辑通知');
    console.log('='.repeat(80));
    console.log('通知ID:', notification.id);
    console.log('通知类型:', notification.type);
    console.log('activity_type:', notification.activity_type);
    console.log('activity_rules:', notification.activity_rules);
    console.log('='.repeat(80) + '\n');

    setEditingNotification(notification);

    // 检查是否是活动类型
    const isEventType = notification.type === NotificationType.EVENT;
    const hasActivityConfig = isEventType &&
                              !!notification.activity_type &&
                              !!notification.activity_rules;

    // 准备活动规则数据
    let activityRules = notification.activity_rules;
    if (activityRules && notification.activity_type) {
      // 确保 activity_rules 包含 type 字段
      if (!activityRules.type) {
        activityRules = { ...activityRules, type: notification.activity_type };
      }
    }

    // 设置表单数据
    setFormData({
      title: notification.title,
      content: notification.content || '',
      category: notification.category,
      type: notification.type,
      priority: notification.priority,
      displayType: notification.displayType,
      publishType: 'immediate',
      targetUsers: notification.targetUsers,
      actionButton: notification.actionButton,
      coverImageUrl: notification.coverImageUrl || '',
      showOnce: notification.showOnce,
      validFrom: notification.validFrom || undefined,
      validUntil: notification.validUntil || undefined,
      activity_type: notification.activity_type,
      activity_rules: activityRules,
    });

    console.log('📝 表单数据已设置:', {
      activity_type: notification.activity_type,
      activity_rules: activityRules,
      hasActivityConfig
    });

    // 如果有活动配置，显示活动配置区域
    if (hasActivityConfig) {
      setShowRewardsConfig(true);
      console.log('✅ 展开活动配置区域');
    } else {
      setShowRewardsConfig(false);
      console.log('⚠️  没有活动配置，不展开配置区域');
    }

    setShowCreateModal(true);
  };

  // 初始化邀请活动规则
  const initInvitationRules = (): InvitationRules => ({
    type: ActivityType.INVITATION,
    inviterRewards: [{
      type: RewardType.POINTS,
      name: '邀请者奖励',
      amount: 500
    }],
    inviteeRewards: [{
      type: RewardType.POINTS,
      name: '被邀请者奖励',
      amount: 300
    }],
    requirementForInvitee: '完成首次任务'
  });

  // 初始化比赛活动规则
  const initCompetitionRules = (): CompetitionRules => ({
    type: ActivityType.COMPETITION,
    rankRewards: [{
      rankRange: [1, 1],
      description: '一等奖',
      rewards: [{
        type: RewardType.POINTS,
        name: '积分奖励',
        amount: 10000
      }]
    }],
    scoringCriteria: '作品质量（40%）+ 创新性（30%）+ 完成度（30%）',
  });

  // 初始化积分活动规则
  const initPointsRules = () => ({
    type: ActivityType.POINTS as const,
    pointsMultiplier: 2,  // 双倍积分
    bonusPoints: 100,     // 额外赠送100积分
    tasks: [{
      taskId: 'task1',
      description: '完成每日任务',
      pointsReward: 50
    }]
  });

  // 处理活动类型变化
  const handleActivityTypeChange = (type: ActivityType) => {
    let rules: ActivityRules | undefined;

    switch (type) {
      case ActivityType.INVITATION:
        rules = initInvitationRules();
        break;
      case ActivityType.COMPETITION:
        rules = initCompetitionRules();
        break;
      case ActivityType.POINTS:
        rules = initPointsRules();
        break;
      default:
        // 其他类型暂时使用基础结构
        rules = { type } as any;
        break;
    }

    setFormData(prev => ({
      ...prev,
      activity_type: type,
      activity_rules: rules
    }));

    console.log('🎯 切换活动类型:', { type, rules });
  };

  // 添加奖励
  const addReward = (path: 'inviterRewards' | 'inviteeRewards' | string) => {
    const newReward: Reward = {
      type: RewardType.POINTS,
      name: '奖励',
      amount: 100
    };

    setFormData(prev => {
      if (!prev.activity_rules) return prev;

      const rules = { ...prev.activity_rules };

      // 只要有 activity_rules 且当前活动类型是邀请活动，就允许添加
      if (prev.activity_type === ActivityType.INVITATION && (path === 'inviterRewards' || path === 'inviteeRewards')) {
        return {
          ...prev,
          activity_rules: {
            ...rules,
            [path]: [...(rules[path as keyof typeof rules] as Reward[]), newReward]
          }
        };
      }

      return prev;
    });
  };

  // 更新奖励
  const updateReward = (
    path: 'inviterRewards' | 'inviteeRewards',
    index: number,
    field: string,
    value: any
  ) => {
    setFormData(prev => {
      // 只检查是否有 activity_rules 和是否是邀请活动类型
      if (!prev.activity_rules || prev.activity_type !== ActivityType.INVITATION) return prev;

      const rules = { ...prev.activity_rules };
      const rewards = [...rules[path]];
      rewards[index] = { ...rewards[index], [field]: value };

      return {
        ...prev,
        activity_rules: {
          ...rules,
          [path]: rewards
        }
      };
    });
  };

  // 删除奖励
  const removeReward = (path: 'inviterRewards' | 'inviteeRewards', index: number) => {
    setFormData(prev => {
      // 只检查是否有 activity_rules 和是否是邀请活动类型
      if (!prev.activity_rules || prev.activity_type !== ActivityType.INVITATION) return prev;

      const rules = { ...prev.activity_rules };
      const rewards = [...rules[path]];
      rewards.splice(index, 1);

      return {
        ...prev,
        activity_rules: {
          ...rules,
          [path]: rewards
        }
      };
    });
  };

  // 筛选通知
  const filteredNotifications = notifications.filter((n) => {
    if (searchQuery && !n.title.toLowerCase().includes(searchQuery.toLowerCase())) {
      return false;
    }
    if (filterStatus === 'published' && n.status !== 'published') return false;
    if (filterStatus === 'draft' && n.status !== 'draft') return false;
    return true;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 页面头部 - 简约黑白风格 */}
      <div className="bg-white border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl text-black">通知管理</h1>
              <p className="mt-1 text-sm text-gray-500">
                创建和管理系统通知、公告和活动
              </p>
            </div>
            <button
              onClick={() => {
                resetForm();
                setEditingNotification(null);
                setShowCreateModal(true);
              }}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-black text-white text-sm rounded-full hover:bg-gray-800 transition-colors"
            >
              <Plus className="w-4 h-4" />
              创建通知
            </button>
          </div>

          {/* 筛选和搜索 */}
          <div className="mt-6 flex items-center gap-3">
            <div className="flex items-center gap-2">
              {(['all', 'published', 'draft'] as const).map((status) => (
                <button
                  key={status}
                  onClick={() => setFilterStatus(status)}
                  className={`px-4 py-2 text-sm rounded-full transition-all ${
                    filterStatus === status
                      ? 'bg-black text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  {status === 'all' ? '全部' : status === 'published' ? '已发布' : '草稿'}
                </button>
              ))}
            </div>

            <div className="flex-1 max-w-md">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="搜索通知标题..."
                  className="w-full pl-10 pr-4 py-2 text-sm bg-white border border-gray-200 rounded-full focus:outline-none focus:border-black"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 通知列表 */}
      <div className="max-w-7xl mx-auto px-8 py-6">
        <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-sm text-gray-500">加载中...</div>
            </div>
          ) : filteredNotifications.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12">
              <Bell className="w-12 h-12 text-gray-300 mb-3" />
              <p className="text-sm text-gray-500">暂无通知</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-100">
              {filteredNotifications.map((notification) => (
                <div
                  key={notification.id}
                  className="p-6 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="text-sm font-medium text-black">
                          {notification.title}
                        </h3>
                        <span
                          className={`inline-flex items-center px-2 py-0.5 text-xs rounded-full ${
                            notification.priority === NotificationPriority.URGENT
                              ? 'bg-red-50 text-red-600'
                              : notification.priority === NotificationPriority.IMPORTANT
                              ? 'bg-amber-50 text-amber-600'
                              : 'bg-gray-100 text-gray-600'
                          }`}
                        >
                          {notification.priority === NotificationPriority.URGENT
                            ? '紧急'
                            : notification.priority === NotificationPriority.IMPORTANT
                            ? '重要'
                            : '普通'}
                        </span>
                        <span
                          className={`inline-flex items-center px-2 py-0.5 text-xs rounded-full ${
                            notification.status === 'published'
                              ? 'bg-green-50 text-green-600'
                              : 'bg-gray-100 text-gray-600'
                          }`}
                        >
                          {notification.status === 'published' ? '已发布' : '草稿'}
                        </span>
                      </div>
                      {notification.content && (
                        <p className="text-xs text-gray-600 line-clamp-2 mb-2">
                          {notification.content}
                        </p>
                      )}
                      <div className="flex items-center gap-4 text-xs text-gray-500">
                        <span>
                          {notification.targetUsers === 'all' ? '全部用户' : '自定义'}
                        </span>
                        <span>
                          {formatDistanceToNow(new Date(notification.createdAt), {
                            addSuffix: true,
                            locale: zhCN,
                          })}
                        </span>
                      </div>
                    </div>

                    {/* 操作按钮 */}
                    <div className="flex items-center gap-2">
                      {notification.status === 'draft' && (
                        <button
                          onClick={() => handlePublish(notification.id)}
                          className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                          title="发布"
                        >
                          <Send className="w-4 h-4" />
                        </button>
                      )}
                      <button
                        onClick={() => handleEdit(notification)}
                        className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                        title="编辑"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(notification.id)}
                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="删除"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* 创建/编辑通知弹窗 - 简约黑白风格 */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/20 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            {/* 弹窗头部 */}
            <div className="sticky top-0 bg-white border-b border-gray-100 px-8 py-6 flex items-center justify-between">
              <h2 className="text-lg font-medium text-black">
                {editingNotification ? '编辑通知' : '创建通知'}
              </h2>
              <button
                onClick={() => {
                  setShowCreateModal(false);
                  setEditingNotification(null);
                  resetForm();
                }}
                className="p-2 text-gray-400 hover:text-black rounded-lg hover:bg-gray-100 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-8 space-y-6">
              {/* 基础信息 */}
              <div className="space-y-4">
                <h3 className="text-sm font-medium text-black">基础信息</h3>

                {/* 标题 */}
                <div>
                  <label className="block text-xs text-gray-600 mb-2">
                    标题 *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-white text-black focus:outline-none focus:border-black"
                    placeholder="输入通知标题"
                  />
                </div>

                {/* 内容 */}
                <div>
                  <label className="block text-xs text-gray-600 mb-2">
                    内容描述
                  </label>
                  <textarea
                    value={formData.content}
                    onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                    rows={4}
                    className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-white text-black focus:outline-none focus:border-black resize-none"
                    placeholder="输入通知内容（可选）"
                  />
                </div>

                {/* 类型和优先级 */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs text-gray-600 mb-2">
                      通知类型 *
                    </label>
                    <select
                      required
                      value={formData.type}
                      onChange={(e) => {
                        const newType = e.target.value as NotificationType;
                        setFormData({ ...formData, type: newType });
                        // 如果选择活动类型，显示活动配置
                        if (newType === NotificationType.EVENT) {
                          setShowRewardsConfig(true);
                        } else {
                          setShowRewardsConfig(false);
                          setFormData(prev => ({
                            ...prev,
                            activity_type: null,
                            activity_rules: null
                          }));
                        }
                      }}
                      className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-white text-black focus:outline-none focus:border-black"
                    >
                      <option value={NotificationType.ANNOUNCEMENT}>公告</option>
                      <option value={NotificationType.FEATURE}>新功能</option>
                      <option value={NotificationType.EVENT}>活动</option>
                      <option value={NotificationType.MAINTENANCE}>维护通知</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs text-gray-600 mb-2">
                      优先级 *
                    </label>
                    <select
                      required
                      value={formData.priority}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          priority: e.target.value as NotificationPriority,
                        })
                      }
                      className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-white text-black focus:outline-none focus:border-black"
                    >
                      <option value={NotificationPriority.NORMAL}>普通</option>
                      <option value={NotificationPriority.IMPORTANT}>重要</option>
                      <option value={NotificationPriority.URGENT}>紧急</option>
                    </select>
                  </div>
                </div>

                {/* 封面图片 */}
                <div>
                  <label className="block text-xs text-gray-600 mb-2">
                    封面图片
                  </label>
                  <div className="flex items-center gap-3">
                    <label className="flex items-center gap-2 px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-white text-gray-700 cursor-pointer hover:bg-gray-50 transition-colors">
                      <ImageIcon className="w-4 h-4" />
                      <span>{uploadingCover ? '上传中...' : '选择图片'}</span>
                      <input
                        type="file"
                        accept="image/jpeg,image/png,image/webp,image/gif"
                        onChange={handleCoverUpload}
                        disabled={uploadingCover}
                        className="hidden"
                      />
                    </label>
                    {formData.coverImageUrl && (
                      <div className="flex items-center gap-2">
                        <img
                          src={formData.coverImageUrl}
                          alt="封面预览"
                          className="w-16 h-16 object-cover rounded-xl border border-gray-200"
                        />
                        <button
                          type="button"
                          onClick={() => setFormData({ ...formData, coverImageUrl: '' })}
                          className="text-red-600 hover:text-red-700 text-xs"
                        >
                          删除
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* 活动配置（仅活动类型显示） */}
              {formData.type === NotificationType.EVENT && (
                <div className="space-y-4 pt-6 border-t border-gray-100">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-medium text-black">活动配置</h3>
                    <button
                      type="button"
                      onClick={() => setShowRewardsConfig(!showRewardsConfig)}
                      className="flex items-center gap-1 text-xs text-gray-600 hover:text-black"
                    >
                      {showRewardsConfig ? (
                        <>
                          <ChevronUp className="w-4 h-4" />
                          收起
                        </>
                      ) : (
                        <>
                          <ChevronDown className="w-4 h-4" />
                          展开配置
                        </>
                      )}
                    </button>
                  </div>

                  {showRewardsConfig && (
                    <>
                      {/* 活动类型选择 */}
                      <div>
                        <label className="block text-xs text-gray-600 mb-2">
                          活动类型 *
                        </label>
                        <div className="grid grid-cols-3 gap-3">
                          {[
                            { type: ActivityType.INVITATION, label: '邀请活动', icon: Gift },
                            { type: ActivityType.COMPETITION, label: '比赛活动', icon: Trophy },
                            { type: ActivityType.POINTS, label: '积分活动', icon: Award },
                          ].map(({ type, label, icon: Icon }) => (
                            <button
                              key={type}
                              type="button"
                              onClick={() => handleActivityTypeChange(type)}
                              className={`flex items-center justify-center gap-2 px-4 py-3 text-sm border rounded-xl transition-all ${
                                formData.activity_type === type
                                  ? 'border-black bg-black text-white'
                                  : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                              }`}
                            >
                              <Icon className="w-4 h-4" />
                              {label}
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* 邀请活动配置 */}
                      {formData.activity_type === ActivityType.INVITATION &&
                        formData.activity_rules && (
                          <div className="space-y-4 p-4 bg-gray-50 rounded-xl">
                            <h4 className="text-xs font-medium text-black">邀请奖励配置</h4>

                            {/* 邀请者奖励 */}
                            <div>
                              <div className="flex items-center justify-between mb-2">
                                <label className="text-xs text-gray-600">邀请者奖励</label>
                                <button
                                  type="button"
                                  onClick={() => addReward('inviterRewards')}
                                  className="text-xs text-black hover:underline"
                                >
                                  + 添加奖励
                                </button>
                              </div>
                              <div className="space-y-2">
                                {formData.activity_rules.inviterRewards.map((reward, index) => (
                                  <div key={index} className="flex items-center gap-2 p-3 bg-white rounded-lg border border-gray-200">
                                    <select
                                      value={reward.type}
                                      onChange={(e) => updateReward('inviterRewards', index, 'type', e.target.value)}
                                      className="px-3 py-1.5 text-xs border border-gray-200 rounded-lg"
                                    >
                                      <option value={RewardType.POINTS}>积分</option>
                                      <option value={RewardType.VIP}>会员</option>
                                      <option value={RewardType.BADGE}>徽章</option>
                                    </select>
                                    {reward.type === RewardType.POINTS && (
                                      <input
                                        type="number"
                                        value={reward.amount}
                                        onChange={(e) => updateReward('inviterRewards', index, 'amount', parseInt(e.target.value))}
                                        className="w-24 px-3 py-1.5 text-xs border border-gray-200 rounded-lg"
                                        placeholder="数量"
                                      />
                                    )}
                                    <input
                                      type="text"
                                      value={reward.name}
                                      onChange={(e) => updateReward('inviterRewards', index, 'name', e.target.value)}
                                      className="flex-1 px-3 py-1.5 text-xs border border-gray-200 rounded-lg"
                                      placeholder="奖励名称"
                                    />
                                    <button
                                      type="button"
                                      onClick={() => removeReward('inviterRewards', index)}
                                      className="p-1.5 text-red-600 hover:bg-red-50 rounded-lg"
                                    >
                                      <X className="w-4 h-4" />
                                    </button>
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* 被邀请者奖励 */}
                            <div>
                              <div className="flex items-center justify-between mb-2">
                                <label className="text-xs text-gray-600">被邀请者奖励</label>
                                <button
                                  type="button"
                                  onClick={() => addReward('inviteeRewards')}
                                  className="text-xs text-black hover:underline"
                                >
                                  + 添加奖励
                                </button>
                              </div>
                              <div className="space-y-2">
                                {formData.activity_rules.inviteeRewards.map((reward, index) => (
                                  <div key={index} className="flex items-center gap-2 p-3 bg-white rounded-lg border border-gray-200">
                                    <select
                                      value={reward.type}
                                      onChange={(e) => updateReward('inviteeRewards', index, 'type', e.target.value)}
                                      className="px-3 py-1.5 text-xs border border-gray-200 rounded-lg"
                                    >
                                      <option value={RewardType.POINTS}>积分</option>
                                      <option value={RewardType.VIP}>会员</option>
                                      <option value={RewardType.BADGE}>徽章</option>
                                    </select>
                                    {reward.type === RewardType.POINTS && (
                                      <input
                                        type="number"
                                        value={reward.amount}
                                        onChange={(e) => updateReward('inviteeRewards', index, 'amount', parseInt(e.target.value))}
                                        className="w-24 px-3 py-1.5 text-xs border border-gray-200 rounded-lg"
                                        placeholder="数量"
                                      />
                                    )}
                                    <input
                                      type="text"
                                      value={reward.name}
                                      onChange={(e) => updateReward('inviteeRewards', index, 'name', e.target.value)}
                                      className="flex-1 px-3 py-1.5 text-xs border border-gray-200 rounded-lg"
                                      placeholder="奖励名称"
                                    />
                                    <button
                                      type="button"
                                      onClick={() => removeReward('inviteeRewards', index)}
                                      className="p-1.5 text-red-600 hover:bg-red-50 rounded-lg"
                                    >
                                      <X className="w-4 h-4" />
                                    </button>
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* 完成条件 */}
                            <div>
                              <label className="block text-xs text-gray-600 mb-2">
                                被邀请者完成条件
                              </label>
                              <input
                                type="text"
                                value={formData.activity_rules.requirementForInvitee || ''}
                                onChange={(e) => setFormData(prev => ({
                                  ...prev,
                                  activity_rules: prev.activity_rules && prev.activity_type === ActivityType.INVITATION
                                    ? { ...prev.activity_rules, requirementForInvitee: e.target.value }
                                    : prev.activity_rules
                                }))}
                                className="w-full px-3 py-2 text-xs border border-gray-200 rounded-lg"
                                placeholder="例如：完成首次任务"
                              />
                            </div>
                          </div>
                        )}

                      {/* 比赛活动配置 */}
                      {formData.activity_type === ActivityType.COMPETITION &&
                        formData.activity_rules && (
                          <div className="space-y-4 p-4 bg-gray-50 rounded-xl">
                            <h4 className="text-xs font-medium text-black">比赛奖励配置</h4>
                            <div>
                              <label className="block text-xs text-gray-600 mb-2">
                                评分标准
                              </label>
                              <input
                                type="text"
                                value={formData.activity_rules.scoringCriteria}
                                onChange={(e) => setFormData(prev => ({
                                  ...prev,
                                  activity_rules: prev.activity_rules && prev.activity_type === ActivityType.COMPETITION
                                    ? { ...prev.activity_rules, scoringCriteria: e.target.value }
                                    : prev.activity_rules
                                }))}
                                className="w-full px-3 py-2 text-xs border border-gray-200 rounded-lg"
                                placeholder="例如：作品质量（40%）+ 创新性（30%）"
                              />
                            </div>
                            <p className="text-xs text-gray-500">
                              💡 提示：比赛活动的排名奖励配置较复杂，建议在后续版本中添加
                            </p>
                          </div>
                        )}

                      {/* 活动时间 */}
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-xs text-gray-600 mb-2">
                            活动开始时间
                          </label>
                          <input
                            type="datetime-local"
                            value={
                              formData.validFrom
                                ? new Date(new Date(formData.validFrom).getTime() - new Date().getTimezoneOffset() * 60000)
                                    .toISOString()
                                    .slice(0, 16)
                                : ''
                            }
                            onChange={(e) => setFormData({ ...formData, validFrom: e.target.value })}
                            className="w-full px-3 py-2 text-xs border border-gray-200 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-gray-600 mb-2">
                            活动结束时间
                          </label>
                          <input
                            type="datetime-local"
                            value={
                              formData.validUntil
                                ? new Date(new Date(formData.validUntil).getTime() - new Date().getTimezoneOffset() * 60000)
                                    .toISOString()
                                    .slice(0, 16)
                                : ''
                            }
                            onChange={(e) => setFormData({ ...formData, validUntil: e.target.value })}
                            className="w-full px-3 py-2 text-xs border border-gray-200 rounded-lg"
                          />
                        </div>
                      </div>
                    </>
                  )}
                </div>
              )}

              {/* 其他设置 */}
              <div className="space-y-4 pt-6 border-t border-gray-100">
                <h3 className="text-sm font-medium text-black">其他设置</h3>

                {/* 展示方式 */}
                <div>
                  <label className="block text-xs text-gray-600 mb-2">
                    展示方式 *
                  </label>
                  <div className="space-y-2">
                    <label className="flex items-center gap-2 p-3 border border-gray-200 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors">
                      <input
                        type="checkbox"
                        checked={formData.displayType.includes('notification')}
                        onChange={(e) => {
                          const types = e.target.checked
                            ? [...formData.displayType, 'notification']
                            : formData.displayType.filter(t => t !== 'notification');
                          setFormData({ ...formData, displayType: types });
                        }}
                        className="w-4 h-4 text-black border-gray-300 rounded focus:ring-black"
                      />
                      <div className="flex-1">
                        <div className="text-xs font-medium text-black">通知铃铛</div>
                        <div className="text-xs text-gray-500">在顶部通知铃铛中显示</div>
                      </div>
                    </label>
                    <label className="flex items-center gap-2 p-3 border border-gray-200 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors">
                      <input
                        type="checkbox"
                        checked={formData.displayType.includes('modal')}
                        onChange={(e) => {
                          const types = e.target.checked
                            ? [...formData.displayType, 'modal']
                            : formData.displayType.filter(t => t !== 'modal');
                          setFormData({ ...formData, displayType: types });
                        }}
                        className="w-4 h-4 text-black border-gray-300 rounded focus:ring-black"
                      />
                      <div className="flex-1">
                        <div className="text-xs font-medium text-black">弹窗提醒</div>
                        <div className="text-xs text-gray-500">用户登录时自动弹出（仅显示一次）</div>
                      </div>
                    </label>
                  </div>
                  {formData.displayType.length === 0 && (
                    <p className="text-xs text-red-600 mt-1">至少选择一种展示方式</p>
                  )}
                </div>

                {/* 目标用户 */}
                <div>
                  <label className="block text-xs text-gray-600 mb-2">
                    目标用户 *
                  </label>
                  <select
                    required
                    value={formData.targetUsers}
                    onChange={(e) => setFormData({ ...formData, targetUsers: e.target.value })}
                    className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-white text-black focus:outline-none focus:border-black"
                  >
                    <option value="all">全部用户</option>
                    <option value="active">活跃用户</option>
                    <option value="inactive">不活跃用户</option>
                  </select>
                </div>

                {/* 发布类型 */}
                <div>
                  <label className="block text-xs text-gray-600 mb-2">
                    发布方式 *
                  </label>
                  <select
                    required
                    value={formData.publishType}
                    onChange={(e) => setFormData({ ...formData, publishType: e.target.value })}
                    className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-white text-black focus:outline-none focus:border-black"
                  >
                    <option value="immediate">立即发布</option>
                    <option value="draft">保存为草稿</option>
                  </select>
                </div>
              </div>

              {/* 提交按钮 */}
              <div className="flex items-center justify-end gap-3 pt-6 border-t border-gray-100">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateModal(false);
                    setEditingNotification(null);
                    resetForm();
                  }}
                  className="px-5 py-2.5 text-sm text-gray-700 hover:bg-gray-100 rounded-full transition-colors"
                >
                  取消
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="inline-flex items-center gap-2 px-5 py-2.5 bg-black text-white text-sm rounded-full hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? (
                    '保存中...'
                  ) : (
                    <>
                      <Save className="w-4 h-4" />
                      {editingNotification ? '保存修改' : '创建通知'}
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminNotificationsView;
