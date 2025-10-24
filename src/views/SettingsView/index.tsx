import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Settings, User, Bell, Shield, Save, Moon, Sun, Monitor, Smartphone, Tablet } from 'lucide-react';
import { Card, Button, Input } from '../../components/common';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import InputDialog from '../../components/common/InputDialog';
import { ToastContainer } from '../../components/ui/Toast';
import { useAuthStore } from '../../store/authStore';
import { DataService } from '../../services/DataService';
import { useToast } from '../../hooks/useToast';
import { useTheme } from '../../hooks/useTheme';
import type { NotificationSettings, UserPreferences, UserSession } from '@/types';

const notificationDefaults: NotificationSettings = {
  emailNotifications: true,
  browserNotifications: false,
  newChapter: true,
  comments: true,
  mentions: true,
  systemUpdates: false,
};

const preferenceDefaults: UserPreferences = {
  theme: 'light',
  language: 'zh-CN',
  fontSize: 'medium',
  autoSave: true,
  autoSaveInterval: 30,
};

/**
 * 设置分类类型
 */
type SettingTab = 'profile' | 'notifications' | 'security' | 'preferences';

/**
 * SettingsView 组件 - 设置页面
 */
const SettingsView: React.FC = () => {
  const { user, setUser, logout } = useAuthStore();
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [activeTab, setActiveTab] = useState<SettingTab>('profile');
  const [isSaving, setIsSaving] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [isDeletingAccount, setIsDeletingAccount] = useState(false);
  const [isUploadingAvatar, setIsUploadingAvatar] = useState(false);
  const { success: showSuccess, error: showError, info: showInfo, messages, close } = useToast();
  const { applyTheme } = useTheme(user?.preferences?.theme);

  // 个人信息表单
  const [profileForm, setProfileForm] = useState({
    username: user?.username || '',
    email: user?.email || '',
    fullName: user?.fullName || '',
    bio: user?.bio || '',
    website: '', // 注意：后端暂不支持website字段
  });

  // 通知设置
  const [notificationSettings, setNotificationSettings] = useState<NotificationSettings>({
    ...notificationDefaults,
  });

  // 安全设置
  const [securityForm, setSecurityForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  // 偏好设置
  const [preferences, setPreferences] = useState<UserPreferences>({
    ...preferenceDefaults,
  });
  const [sessions, setSessions] = useState<UserSession[]>([]);
  const [isSessionsLoading, setIsSessionsLoading] = useState(true);
  const [sessionActionId, setSessionActionId] = useState<string | null>(null);
  const [isLoggingOutOthers, setIsLoggingOutOthers] = useState(false);
  const [logoutTarget, setLogoutTarget] = useState<UserSession | null>(null);
  const [showLogoutOthersConfirm, setShowLogoutOthersConfirm] = useState(false);
  const [showDeleteAccountDialog, setShowDeleteAccountDialog] = useState(false);

  const handleThemeSelect = (nextTheme: UserPreferences['theme']) => {
    setPreferences({ ...preferences, theme: nextTheme });
    applyTheme(nextTheme, { persist: false });
  };

  const loadSessions = useCallback(
    async (showError: boolean = true) => {
      setIsSessionsLoading(true);
      try {
        const result = await DataService.getSessions();
        setSessions(result);
      } catch (error: any) {
        console.error('加载会话失败:', error);
        setSessions([]);
        if (showError) {
          showError(error?.message || '获取会话信息失败，请稍后重试');
        }
      } finally {
        setIsSessionsLoading(false);
      }
    },
    [showError]
  );

  const handleRefreshSessions = async () => {
    await loadSessions();
  };

  const handleLogoutSession = async (session: UserSession) => {
    if (session.isCurrent) {
      showInfo('当前设备无需在此处退出');
      return;
    }

    setLogoutTarget(session);
  };

  const handleLogoutOtherSessions = async () => {
    setShowLogoutOthersConfirm(true);
  };

  const resolveDeviceIcon = (type: UserSession['deviceType']) => {
    switch (type) {
      case 'desktop':
        return <Monitor className="w-6 h-6 text-blue-500" />;
      case 'mobile':
        return <Smartphone className="w-6 h-6 text-green-500" />;
      case 'tablet':
        return <Tablet className="w-6 h-6 text-purple-500" />;
      default:
        return <Shield className="w-6 h-6 text-gray-400" />;
    }
  };

  const formatTimestamp = (value?: string) => {
    if (!value) return '未知时间';
    try {
      return new Date(value).toLocaleString();
    } catch {
      return value;
    }
  };

  useEffect(() => {
    if (user) {
      setProfileForm({
        username: user.username || '',
        email: user.email || '',
        fullName: user.fullName || '',
        bio: user.bio || '',
        website: '',
      });
      if (user.notificationSettings) {
        setNotificationSettings({
          ...notificationDefaults,
          ...user.notificationSettings,
        });
      }
      if (user.preferences) {
        setPreferences({
          ...preferenceDefaults,
          ...user.preferences,
        });
      }
    }
  }, [user]);

  useEffect(() => {
    const loadSettings = async () => {
      setIsInitializing(true);
      try {
        const [userResponse, notificationResponse, preferenceResponse] = await Promise.all([
          DataService.getCurrentUser(),
          DataService.getNotificationSettings(),
          DataService.getPreferences(),
        ]);
        setUser(userResponse);
        setNotificationSettings({
          ...notificationDefaults,
          ...notificationResponse,
        });
        setPreferences({
          ...preferenceDefaults,
          ...preferenceResponse,
        });
      } catch (error: any) {
        console.error('加载设置失败:', error);
        showError(error?.message || '加载设置失败，请稍后重试');
      } finally {
        setIsInitializing(false);
      }
    };

    loadSettings();
    loadSessions(false);
  }, [loadSessions, setUser, showError]);

  // 标签页配置
  const tabs = [
    { id: 'profile' as const, label: '个人信息', icon: User },
    { id: 'notifications' as const, label: '通知设置', icon: Bell },
    { id: 'security' as const, label: '安全设置', icon: Shield },
    { id: 'preferences' as const, label: '偏好设置', icon: Settings },
  ];

  // 保存设置
  const handleSave = async () => {
    setIsSaving(true);
    try {
      if (activeTab === 'profile') {
        const updatedUser = await DataService.updateUserProfile({
          username: profileForm.username,
          email: profileForm.email,
          fullName: profileForm.fullName,
          bio: profileForm.bio,
          // website: profileForm.website, // 后端暂不支持
        });
        // 更新本地状态
        setUser(updatedUser);
        showSuccess('个人信息已保存');
      } else if (activeTab === 'notifications') {
        const updatedSettings = await DataService.updateNotificationSettings(notificationSettings);
        setNotificationSettings({
          ...notificationDefaults,
          ...updatedSettings,
        });
        if (user) {
          setUser({
            ...user,
            notificationSettings: updatedSettings,
          });
        }
        showSuccess('通知设置已保存');
      } else if (activeTab === 'preferences') {
        const updatedPreferences = await DataService.updatePreferences(preferences);
        setPreferences({
          ...preferenceDefaults,
          ...updatedPreferences,
        });
        if (user) {
          setUser({
            ...user,
            preferences: updatedPreferences,
          });
        }
        if (updatedPreferences?.theme) {
          applyTheme(updatedPreferences.theme, { persist: true });
        }
        showSuccess('偏好设置已保存');
      } else {
        showInfo('请使用下方操作管理安全设置');
      }
    } catch (error: any) {
      console.error('保存设置失败:', error);
      showError(error.message || '保存失败，请稍后重试');
    } finally {
      setIsSaving(false);
    }
  };

  // 取消修改
  const handleCancel = () => {
    if (activeTab === 'profile') {
      // 重置个人信息表单
      setProfileForm({
        username: user?.username || '',
        email: user?.email || '',
        fullName: user?.fullName || '',
        bio: user?.bio || '',
        website: '',
      });
      showInfo('已取消修改');
    } else if (activeTab === 'notifications') {
      // 重置通知设置
      setNotificationSettings(user?.notificationSettings || notificationDefaults);
      showInfo('已取消修改');
    } else if (activeTab === 'preferences') {
      // 重置偏好设置
      const originalPreferences = user?.preferences || preferenceDefaults;
      setPreferences(originalPreferences);
      // 恢复主题
      if (originalPreferences?.theme) {
        applyTheme(originalPreferences.theme, { persist: false });
      }
      showInfo('已取消修改');
    }
  };

  const handleAvatarSelect = () => {
    fileInputRef.current?.click();
  };

  const handleAvatarChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      showError('仅支持 JPG、PNG、WebP 格式的图片');
      event.target.value = '';
      return;
    }

    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      showError('文件过大，请选择 10MB 以下的图片');
      event.target.value = '';
      return;
    }

    setIsUploadingAvatar(true);
    try {
      const avatarUrl = await DataService.uploadAvatar(file);
      if (user) {
        setUser({
          ...user,
          avatar: avatarUrl,
        });
      } else {
        const refreshedUser = await DataService.getCurrentUser();
        setUser(refreshedUser);
      }
      showSuccess('头像已更新');
    } catch (error: any) {
      console.error('上传头像失败:', error);
      showError(error?.message || '上传头像失败，请稍后重试');
    } finally {
      setIsUploadingAvatar(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleChangePassword = async () => {
    if (!securityForm.currentPassword || !securityForm.newPassword || !securityForm.confirmPassword) {
      showError('请完整填写密码信息');
      return;
    }

    if (securityForm.newPassword !== securityForm.confirmPassword) {
      showError('新密码与确认密码不一致');
      return;
    }

    if (securityForm.newPassword.length < 6) {
      showError('新密码长度至少为 6 位');
      return;
    }

    setIsChangingPassword(true);
    try {
      const message = await DataService.changePassword(
        securityForm.currentPassword,
        securityForm.newPassword
      );
      showSuccess(message || '密码已更新');
      setSecurityForm({
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      });
    } catch (error: any) {
      console.error('修改密码失败:', error);
      showError(error?.message || '修改密码失败，请稍后重试');
    } finally {
      setIsChangingPassword(false);
    }
  };

  const handleDeleteAccount = async () => {
    setShowDeleteAccountDialog(true);
  };

  // 渲染个人信息设置
  const renderProfileSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">个人信息</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-700 mb-2">用户名</label>
            <Input
              value={profileForm.username}
              onChange={(e) => setProfileForm({ ...profileForm, username: e.target.value })}
              placeholder="输入用户名"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-700 mb-2">邮箱</label>
            <Input
              type="email"
              value={profileForm.email}
              onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })}
              placeholder="输入邮箱地址"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-700 mb-2">真实姓名</label>
            <Input
              value={profileForm.fullName}
              onChange={(e) => setProfileForm({ ...profileForm, fullName: e.target.value })}
              placeholder="输入真实姓名（可选）"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-700 mb-2">个人简介</label>
            <textarea
              value={profileForm.bio}
              onChange={(e) => setProfileForm({ ...profileForm, bio: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent bg-white dark:bg-white text-gray-900 dark:text-gray-900 placeholder-gray-400"
              rows={4}
              placeholder="介绍一下自己..."
            />
          </div>
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">头像</h3>
        <div className="flex items-center space-x-4">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/png,image/jpeg,image/webp"
            className="hidden"
            onChange={handleAvatarChange}
          />
          <div className="w-20 h-20 bg-blue-100 dark:bg-blue-900/40 rounded-full flex items-center justify-center overflow-hidden">
            {user?.avatar ? (
              <img src={user.avatar} alt="用户头像" className="w-full h-full object-cover" />
            ) : (
              <span className="text-2xl font-bold text-blue-600">
                {user?.username ? user.username[0].toUpperCase() : 'U'}
              </span>
            )}
          </div>
          <div>
            <Button
              variant="outline"
              size="sm"
              onClick={handleAvatarSelect}
              disabled={isUploadingAvatar}
            >
              {isUploadingAvatar ? '上传中...' : '上传新头像'}
            </Button>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">支持 JPG、PNG、WebP 格式，10MB 以内</p>
          </div>
        </div>
      </div>
    </div>
  );

  // 渲染通知设置
  const renderNotificationSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">通知渠道</h3>
        <div className="space-y-4">
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer bg-white">
            <div>
              <p className="font-medium text-gray-900">邮件通知</p>
              <p className="text-sm text-gray-600">通过邮件接收通知</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.emailNotifications}
              onChange={(e) =>
                setNotificationSettings({ ...notificationSettings, emailNotifications: e.target.checked })
              }
              className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
          </label>
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer bg-white">
            <div>
              <p className="font-medium text-gray-900">浏览器通知</p>
              <p className="text-sm text-gray-600">通过浏览器推送通知</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.browserNotifications}
              onChange={(e) =>
                setNotificationSettings({ ...notificationSettings, browserNotifications: e.target.checked })
              }
              className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
          </label>
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">通知类型</h3>
        <div className="space-y-4">
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer bg-white">
            <div>
              <p className="font-medium text-gray-900">新章节发布</p>
              <p className="text-sm text-gray-600">关注的作者发布新章节时通知我</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.newChapter}
              onChange={(e) => setNotificationSettings({ ...notificationSettings, newChapter: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
          </label>
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer bg-white">
            <div>
              <p className="font-medium text-gray-900">评论回复</p>
              <p className="text-sm text-gray-600">有人回复我的评论时通知我</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.comments}
              onChange={(e) => setNotificationSettings({ ...notificationSettings, comments: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
          </label>
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer bg-white">
            <div>
              <p className="font-medium text-gray-900">@提及</p>
              <p className="text-sm text-gray-600">有人@我时通知我</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.mentions}
              onChange={(e) => setNotificationSettings({ ...notificationSettings, mentions: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
          </label>
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer bg-white">
            <div>
              <p className="font-medium text-gray-900">系统更新</p>
              <p className="text-sm text-gray-600">系统有重要更新时通知我</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.systemUpdates}
              onChange={(e) => setNotificationSettings({ ...notificationSettings, systemUpdates: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
          </label>
        </div>
      </div>
    </div>
  );

  // 渲染安全设置
  const renderSecuritySettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">修改密码</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-700 mb-2">当前密码</label>
            <Input
              type="password"
              value={securityForm.currentPassword}
              onChange={(e) => setSecurityForm({ ...securityForm, currentPassword: e.target.value })}
              placeholder="输入当前密码"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-700 mb-2">新密码</label>
            <Input
              type="password"
              value={securityForm.newPassword}
              onChange={(e) => setSecurityForm({ ...securityForm, newPassword: e.target.value })}
              placeholder="输入新密码"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-700 mb-2">确认新密码</label>
            <Input
              type="password"
              value={securityForm.confirmPassword}
              onChange={(e) => setSecurityForm({ ...securityForm, confirmPassword: e.target.value })}
              placeholder="再次输入新密码"
            />
          </div>
          <Button
            variant="secondary"
            onClick={handleChangePassword}
            disabled={isChangingPassword}
          >
            {isChangingPassword ? '更新中...' : '更新密码'}
          </Button>
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">登录会话</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">查看并管理所有已登录设备</p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="gray-outline" size="sm" onClick={handleRefreshSessions} disabled={isSessionsLoading}>
              {isSessionsLoading ? '加载中...' : '刷新'}
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={handleLogoutOtherSessions}
              disabled={isLoggingOutOthers || isSessionsLoading || sessions.length <= 1}
            >
              {isLoggingOutOthers ? '处理中...' : '退出其他设备'}
            </Button>
          </div>
        </div>
        {isSessionsLoading ? (
          <div className="mt-4 p-4 text-center text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 rounded-lg">
            正在加载会话信息...
          </div>
        ) : sessions.length === 0 ? (
          <div className="mt-4 p-4 text-center text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 rounded-lg">
            暂无其他登录设备
          </div>
        ) : (
          <div className="mt-4 space-y-3">
            {sessions.map((session) => (
              <div
                key={session.id}
                className="flex items-start justify-between gap-4 p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800"
              >
                <div className="flex items-start gap-3">
                  <div className="mt-1">
                    {resolveDeviceIcon(session.deviceType)}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="font-medium text-gray-900 dark:text-gray-100">
                        {session.deviceName || '未知设备'}
                      </p>
                      {session.isCurrent && (
                        <span className="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-200 rounded-full">
                          当前设备
                        </span>
                      )}
                      {!session.isActive && (
                        <span className="px-2 py-0.5 text-xs font-medium bg-gray-200 text-gray-600 dark:bg-gray-700 dark:text-gray-300 rounded-full">
                          已退出
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {(session.browser || '未知浏览器')}{session.browserVersion ? ` · ${session.browserVersion}` : ''}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {session.operatingSystem ? `系统: ${session.operatingSystem}` : '系统: 未知'}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {session.ipAddress ? `IP: ${session.ipAddress}` : 'IP: 未知'}
                      {session.location ? ` · 位置: ${session.location}` : ''}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      最近活动: {formatTimestamp(session.lastActiveAt)}
                    </p>
                  </div>
                </div>
                {!session.isCurrent && session.isActive && (
                  <Button
                    variant="gray-outline"
                    size="sm"
                    onClick={() => handleLogoutSession(session)}
                    disabled={sessionActionId === session.id}
                  >
                    {sessionActionId === session.id ? '处理中...' : '退出'}
                  </Button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">危险操作</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">删除账号后将无法恢复，请谨慎操作</p>
        <Button
          variant="danger"
          onClick={handleDeleteAccount}
          disabled={isDeletingAccount}
        >
          {isDeletingAccount ? '删除中...' : '删除账号'}
        </Button>
      </div>
    </div>
  );

  // 渲染偏好设置
  const renderPreferencesSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">外观</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-700 mb-3">主题</label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { value: 'light', label: '浅色', icon: Sun },
                { value: 'dark', label: '深色', icon: Moon },
                { value: 'auto', label: '自动', icon: Settings },
              ].map((theme) => {
                const Icon = theme.icon;
                return (
                  <button
                    key={theme.value}
                    onClick={() => handleThemeSelect(theme.value as UserPreferences['theme'])}
                    className={`flex flex-col items-center justify-center p-4 border-2 rounded-lg transition-all ${
                      preferences.theme === theme.value
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="w-6 h-6 mb-2" />
                    <span className="text-sm font-medium text-gray-900">{theme.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-700 mb-3">字体大小</label>
            <div className="flex items-center space-x-2">
              {['small', 'medium', 'large'].map((size) => (
                <button
                  key={size}
                  onClick={() => setPreferences({ ...preferences, fontSize: size as any })}
                  className={`px-4 py-2 border-2 rounded-lg transition-colors ${
                    preferences.fontSize === size
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50 text-gray-700'
                  }`}
                >
                  {size === 'small' ? '小' : size === 'medium' ? '中' : '大'}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">语言和地区</h3>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-700 mb-2">界面语言</label>
          <select
            value={preferences.language}
            onChange={(e) => setPreferences({ ...preferences, language: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-200 focus:border-blue-300 bg-white text-gray-900 [&>option:checked]:bg-blue-50 [&>option:checked]:text-blue-700"
          >
            <option value="zh-CN">简体中文</option>
            <option value="zh-TW">繁体中文</option>
            <option value="en-US">English</option>
          </select>
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">编辑器</h3>
        <div className="space-y-4">
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer bg-white">
            <div>
              <p className="font-medium text-gray-900">自动保存</p>
              <p className="text-sm text-gray-600">在编辑时自动保存内容</p>
            </div>
            <input
              type="checkbox"
              checked={preferences.autoSave}
              onChange={(e) => setPreferences({ ...preferences, autoSave: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
          </label>
          {preferences.autoSave && (
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-700 mb-2">自动保存间隔（秒）</label>
              <Input
                type="number"
                value={preferences.autoSaveInterval}
                onChange={(e) => setPreferences({ ...preferences, autoSaveInterval: parseInt(e.target.value) })}
                min={10}
                max={300}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );

  const confirmLogoutSession = async () => {
    if (!logoutTarget) return;
    setSessionActionId(logoutTarget.id);
    try {
      await DataService.logoutSession(logoutTarget.id);
      showSuccess('已退出指定设备');
      await loadSessions();
    } catch (error: any) {
      console.error('退出会话失败:', error);
      showError(error?.message || '退出失败，请稍后重试');
    } finally {
      setSessionActionId(null);
      setLogoutTarget(null);
    }
  };

  const confirmLogoutOtherSessions = async () => {
    setShowLogoutOthersConfirm(false);
    setIsLoggingOutOthers(true);
    try {
      await DataService.logoutOtherSessions();
      showSuccess('已退出其他设备');
      await loadSessions();
    } catch (error: any) {
      console.error('退出其他设备失败:', error);
      showError(error?.message || '退出其他设备失败，请稍后重试');
    } finally {
      setIsLoggingOutOthers(false);
    }
  };

  const confirmDeleteAccount = async (values: Record<string, string>) => {
    if (isDeletingAccount) {
      return;
    }
    const password = values.password?.trim();
    if (!password) {
      showError('请输入密码后再确认删除');
      return;
    }

    setIsDeletingAccount(true);
    try {
      await DataService.deleteAccount(password);
      showSuccess('账号已删除');
      logout();
      window.location.href = '/';
    } catch (error: any) {
      console.error('删除账号失败:', error);
      showError(error?.message || '删除账号失败，请稍后重试');
    } finally {
      setIsDeletingAccount(false);
    }
  };

  return (
    <>
    <div className="space-y-6">
      {/* 页面标题 */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">设置</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">管理您的账号和应用偏好</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* 左侧标签栏 */}
        <Card className="lg:col-span-1 !bg-white dark:!bg-white shadow-none border-gray-100">
          <div className="p-4">
            <nav className="space-y-1">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                      activeTab === tab.id
                        ? 'bg-blue-50 text-blue-700'
                        : 'text-gray-900 hover:bg-gray-100 hover:text-gray-900'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>
        </Card>

        {/* 右侧内容区 */}
        <Card className="lg:col-span-3 !bg-white dark:!bg-white shadow-none border-gray-100">
          <div className="p-6">
            {isInitializing ? (
            <div className="py-16 text-center text-gray-500 dark:text-gray-400">正在加载设置...</div>
            ) : (
              <>
                {activeTab === 'profile' && renderProfileSettings()}
                {activeTab === 'notifications' && renderNotificationSettings()}
                {activeTab === 'security' && renderSecuritySettings()}
                {activeTab === 'preferences' && renderPreferencesSettings()}
              </>
            )}

            {/* 保存按钮区域 - 仅在非安全设置标签页显示 */}
            {activeTab !== 'security' ? (
              <div className="border-t border-gray-200 mt-6 pt-6">
                <div className="flex items-center justify-end space-x-3">
                  <Button variant="outline" onClick={handleCancel} disabled={isSaving}>
                    取消
                  </Button>
                  <Button variant="primary" onClick={handleSave} disabled={isSaving || isInitializing}>
                    <Save className="w-4 h-4 mr-2" />
                    {isSaving ? '保存中...' : '保存更改'}
                  </Button>
                </div>
              </div>
            ) : (
              // 安全设置页 - 保持相同高度的底部留白
              <div className="mt-6 pt-6"></div>
            )}
          </div>
        </Card>
      </div>
    </div>

      <ConfirmDialog
        isOpen={!!logoutTarget}
        title="退出该登录设备？"
        message={`确定要退出「${logoutTarget?.deviceName || logoutTarget?.deviceType || '未知设备'}」吗？退出后需重新登录。`}
        confirmText="确认退出"
        cancelText="取消"
        variant="warning"
        onConfirm={confirmLogoutSession}
        onCancel={() => setLogoutTarget(null)}
      />

      <ConfirmDialog
        isOpen={showLogoutOthersConfirm}
        title="退出其他设备？"
        message="此操作将登出除当前设备外的所有会话，需要重新登录才能使用。是否继续？"
        confirmText="退出其他设备"
        cancelText="暂不退出"
        variant="warning"
        onConfirm={confirmLogoutOtherSessions}
        onCancel={() => setShowLogoutOthersConfirm(false)}
      />

      <InputDialog
        isOpen={showDeleteAccountDialog}
        onClose={() => setShowDeleteAccountDialog(false)}
        onConfirm={confirmDeleteAccount}
        title="确认删除账号"
        confirmText={isDeletingAccount ? '删除中...' : '确认删除'}
        cancelText="取消"
        fields={[
          {
            name: 'password',
            label: '当前密码',
            placeholder: '请输入密码以确认删除',
            required: true,
            type: 'password',
          },
        ]}
      />

      {/* Toast 通知容器 */}
      <ToastContainer messages={messages} onClose={close} />
    </>
  );
};

export default SettingsView;
