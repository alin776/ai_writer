/**
 * 管理员通知管理页面
 *
 * 功能:
 * - 创建和发送通知
 * - 查看所有通知列表
 * - 编辑和删除通知
 * - 查看通知统计数据
 */

import React, { useState, useEffect } from 'react';
import {
  Plus,
  Send,
  Edit,
  Trash2,
  Eye,
  Users,
  Bell,
  TrendingUp,
  Calendar,
  Filter,
  Search,
  Save,
  X,
  Image as ImageIcon,
  AlertCircle,
} from 'lucide-react';
import { ApiAdapter } from '../services/ApiAdapter';
import type {
  NotificationCreate,
  NotificationResponse,
  NotificationStats,
} from '../types/notification';
import {
  NotificationPriority,
  NotificationCategory,
  NotificationType,
} from '../types/notification';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';

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

  // 表单状态
  const [formData, setFormData] = useState<Partial<NotificationCreate>>({
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
    bannerColor: '',
    showOnce: false,
  });

  // 加载通知列表
  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const response = await api.get<{
        total: number;
        page: number;
        pageSize: number;
        items: NotificationResponse[];
      }>('/notifications/admin/notifications', {
        params: {
          page: 1,
          pageSize: 50,
        }
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
    setLoading(true);

    try {
      if (editingNotification) {
        // 更新通知
        await api.put(`/notifications/admin/notifications/${editingNotification.id}`, formData);
      } else {
        // 创建新通知
        await api.post('/notifications/admin/notifications', formData);
      }

      // 重新加载列表
      await fetchNotifications();

      // 关闭弹窗并重置表单
      setShowCreateModal(false);
      setEditingNotification(null);
      resetForm();
    } catch (error) {
      console.error('保存通知失败:', error);
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
      bannerColor: '',
      showOnce: false,
    });
  };

  // 处理图片上传
  const handleCoverUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // 验证文件类型
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
    if (!allowedTypes.includes(file.type)) {
      alert('仅支持 JPG/PNG/WebP/GIF 图片文件');
      return;
    }

    // 验证文件大小 (10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('文件过大，请选择 10MB 以下的图片');
      return;
    }

    setUploadingCover(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post<{ coverUrl: string }>(
        '/notifications/admin/notifications/upload-cover',
        formData
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
    setEditingNotification(notification);
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
      bannerColor: notification.bannerColor || '',
      showOnce: notification.showOnce,
      validFrom: notification.validFrom || undefined,
      validUntil: notification.validUntil || undefined,
    });
    setShowCreateModal(true);
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
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* 页面头部 */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                通知管理
              </h1>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                创建和管理系统通知、公告和活动
              </p>
            </div>
            <button
              onClick={() => {
                resetForm();
                setEditingNotification(null);
                setShowCreateModal(true);
              }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-4 h-4" />
              创建通知
            </button>
          </div>

          {/* 筛选和搜索 */}
          <div className="mt-4 flex items-center gap-3">
            <div className="flex items-center gap-1 bg-gray-100 dark:bg-gray-700 rounded-lg p-0.5">
              <button
                onClick={() => setFilterStatus('all')}
                className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                  filterStatus === 'all'
                    ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm'
                    : 'text-gray-600 dark:text-gray-300'
                }`}
              >
                全部
              </button>
              <button
                onClick={() => setFilterStatus('published')}
                className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                  filterStatus === 'published'
                    ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm'
                    : 'text-gray-600 dark:text-gray-300'
                }`}
              >
                已发布
              </button>
              <button
                onClick={() => setFilterStatus('draft')}
                className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                  filterStatus === 'draft'
                    ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm'
                    : 'text-gray-600 dark:text-gray-300'
                }`}
              >
                草稿
              </button>
            </div>

            <div className="flex-1 max-w-md">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="搜索通知标题..."
                  className="w-full pl-10 pr-4 py-2 text-sm bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 通知列表 */}
      <div className="p-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
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
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {filteredNotifications.map((notification) => (
                <div
                  key={notification.id}
                  className="p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-sm font-medium text-gray-900 dark:text-white">
                          {notification.title}
                        </h3>
                        <span
                          className={`inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-full ${
                            notification.priority === NotificationPriority.URGENT
                              ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                              : notification.priority === NotificationPriority.IMPORTANT
                              ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
                              : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                          }`}
                        >
                          {notification.priority === NotificationPriority.URGENT
                            ? '紧急'
                            : notification.priority === NotificationPriority.IMPORTANT
                            ? '重要'
                            : '普通'}
                        </span>
                        <span
                          className={`inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-full ${
                            notification.status === 'published'
                              ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                              : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                          }`}
                        >
                          {notification.status === 'published' ? '已发布' : '草稿'}
                        </span>
                      </div>
                      {notification.content && (
                        <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2 mb-2">
                          {notification.content}
                        </p>
                      )}
                      <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
                        <span>
                          目标: {notification.targetUsers === 'all' ? '全部用户' : '自定义'}
                        </span>
                        <span>
                          展示: {notification.displayType.includes('modal') ? '弹窗+' : ''}
                          {notification.displayType.includes('notification') ? '通知' : ''}
                        </span>
                        <span>
                          创建于{' '}
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
                          className="p-2 text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20 rounded-lg transition-colors"
                          title="发布"
                        >
                          <Send className="w-4 h-4" />
                        </button>
                      )}
                      <button
                        onClick={() => handleEdit(notification)}
                        className="p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
                        title="编辑"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(notification.id)}
                        className="p-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
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

      {/* 创建/编辑通知弹窗 */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                {editingNotification ? '编辑通知' : '创建通知'}
              </h2>
              <button
                onClick={() => {
                  setShowCreateModal(false);
                  setEditingNotification(null);
                  resetForm();
                }}
                className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              {/* 标题 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  标题 *
                </label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                  placeholder="输入通知标题"
                />
              </div>

              {/* 内容 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  内容
                </label>
                <textarea
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  rows={4}
                  className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 resize-none"
                  placeholder="输入通知内容（可选）"
                />
              </div>

              {/* 类型和优先级 */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    类型 *
                  </label>
                  <select
                    required
                    value={formData.type}
                    onChange={(e) =>
                      setFormData({ ...formData, type: e.target.value as NotificationType })
                    }
                    className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                  >
                    <option value={NotificationType.ANNOUNCEMENT}>公告</option>
                    <option value={NotificationType.FEATURE}>新功能</option>
                    <option value={NotificationType.EVENT}>活动</option>
                    <option value={NotificationType.MAINTENANCE}>维护通知</option>
                    <option value={NotificationType.MILESTONE}>里程碑</option>
                    <option value={NotificationType.SMART_REMINDER}>智能提醒</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
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
                    className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                  >
                    <option value={NotificationPriority.NORMAL}>普通</option>
                    <option value={NotificationPriority.IMPORTANT}>重要</option>
                    <option value={NotificationPriority.URGENT}>紧急</option>
                  </select>
                </div>
              </div>

              {/* 展示方式 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  展示方式 *
                </label>
                <div className="space-y-2">
                  <label className="inline-flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.displayType?.includes('notification')}
                      onChange={(e) => {
                        const newTypes = e.target.checked
                          ? [...(formData.displayType || []), 'notification']
                          : (formData.displayType || []).filter((t) => t !== 'notification');
                        setFormData({ ...formData, displayType: newTypes });
                      }}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                      通知铃铛
                    </span>
                  </label>
                  <label className="inline-flex items-center ml-4">
                    <input
                      type="checkbox"
                      checked={formData.displayType?.includes('modal')}
                      onChange={(e) => {
                        const newTypes = e.target.checked
                          ? [...(formData.displayType || []), 'modal']
                          : (formData.displayType || []).filter((t) => t !== 'modal');
                        setFormData({ ...formData, displayType: newTypes });
                      }}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                      弹窗提醒
                    </span>
                  </label>
                </div>
              </div>

              {/* 目标用户 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  目标用户 *
                </label>
                <select
                  required
                  value={formData.targetUsers}
                  onChange={(e) => setFormData({ ...formData, targetUsers: e.target.value })}
                  className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">全部用户</option>
                  <option value="active">活跃用户</option>
                  <option value="inactive">不活跃用户</option>
                </select>
              </div>

              {/* 封面图片上传 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  封面图片
                </label>
                <div className="flex items-center gap-3">
                  <label className="flex items-center gap-2 px-4 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors">
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
                        className="w-16 h-16 object-cover rounded border border-gray-200"
                      />
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, coverImageUrl: '' })}
                        className="text-red-600 hover:text-red-700 text-sm"
                      >
                        删除
                      </button>
                    </div>
                  )}
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  支持 JPG/PNG/WebP/GIF，最大 10MB
                </p>
              </div>

              {/* 行动按钮 */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    按钮文本
                  </label>
                  <input
                    type="text"
                    value={formData.actionButton?.text || ''}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        actionButton: {
                          text: e.target.value,
                          url: formData.actionButton?.url || '',
                        },
                      })
                    }
                    className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                    placeholder="查看详情"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    按钮链接
                  </label>
                  <input
                    type="text"
                    value={formData.actionButton?.url || ''}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        actionButton: {
                          text: formData.actionButton?.text || '',
                          url: e.target.value,
                        },
                      })
                    }
                    className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                    placeholder="/works"
                  />
                </div>
              </div>

              {/* 活动时间（仅活动类型显示） */}
              {formData.type === NotificationType.EVENT && (
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
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
                      className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
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
                      className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
              )}

              {/* 发布类型 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  发布方式 *
                </label>
                <select
                  required
                  value={formData.publishType}
                  onChange={(e) => setFormData({ ...formData, publishType: e.target.value })}
                  className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                >
                  <option value="immediate">立即发布</option>
                  <option value="draft">保存为草稿</option>
                </select>
              </div>

              {/* 提交按钮 */}
              <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateModal(false);
                    setEditingNotification(null);
                    resetForm();
                  }}
                  className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                >
                  取消
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? (
                    <>加载中...</>
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
