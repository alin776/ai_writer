import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Settings, User, Bell, Shield, Save, Moon, Sun, Monitor, Smartphone, Tablet, Mail, Lock, ChevronRight, Clock } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Card, Button, Input } from '../../components/common';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import InputDialog from '../../components/common/InputDialog';
import { ToastContainer } from '../../components/ui/Toast';
import { useAuthStore } from '../../store/authStore';
import { DataService } from '../../services/DataService';
import { useToast } from '../../hooks/useToast';
import { useTheme } from '../../hooks/useTheme';
import { languages, type LanguageCode } from '../../i18n';
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
  aiAutoComplete: false, // 默认关闭，避免意外消耗积分
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
  const navigate = useNavigate();
  const location = useLocation();
  const { t, i18n } = useTranslation();
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const bioTextareaRef = useRef<HTMLTextAreaElement | null>(null);

  // 支持从修改密码页面返回时恢复到安全设置标签
  const initialTab = (location.state as { activeTab?: SettingTab })?.activeTab || 'profile';
  const [activeTab, setActiveTab] = useState<SettingTab>(initialTab);
  const [isSaving, setIsSaving] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const [isDeletingAccount, setIsDeletingAccount] = useState(false);
  const [isUploadingAvatar, setIsUploadingAvatar] = useState(false);
  const { success: showSuccess, error: showError, info: showInfo, messages, close } = useToast();
  const { applyTheme } = useTheme(user?.preferences?.theme);

  // 个人信息表单
  const [profileForm, setProfileForm] = useState({
    username: user?.username || '',
    bio: user?.bio || '',
  });

  // 通知设置
  const [notificationSettings, setNotificationSettings] = useState<NotificationSettings>({
    ...notificationDefaults,
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

  const handleLanguageSelect = (nextLanguage: LanguageCode) => {
    setPreferences({ ...preferences, language: nextLanguage });
    // 立即应用语言变更
    i18n.changeLanguage(nextLanguage);
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
        // 保持静默，错误提示已通过 useToast 处理
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
      showInfo(t('settings.messages.currentDeviceInfo'));
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
    if (!value) return t('date.unknownTime');
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
        bio: user.bio || '',
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

  // 自动调整 bio textarea 高度
  useEffect(() => {
    if (bioTextareaRef.current && profileForm.bio) {
      bioTextareaRef.current.style.height = 'auto';
      bioTextareaRef.current.style.height = `${bioTextareaRef.current.scrollHeight}px`;
    }
  }, [profileForm.bio]);

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
        showError(error?.message || t('settings.messages.loadError'));
      } finally {
        setIsInitializing(false);
      }
    };

    loadSettings();
    loadSessions(false);
  }, [loadSessions, setUser, showError]);

  // 标签页配置
  const tabs = [
    { id: 'profile' as const, labelKey: 'settings.tabs.profile', icon: User },
    { id: 'notifications' as const, labelKey: 'settings.tabs.notifications', icon: Bell },
    { id: 'security' as const, labelKey: 'settings.tabs.security', icon: Shield },
    { id: 'preferences' as const, labelKey: 'settings.tabs.preferences', icon: Settings },
  ];

  // 保存设置
  const handleSave = async () => {
    setIsSaving(true);
    try {
      if (activeTab === 'profile') {
        const updatedUser = await DataService.updateUserProfile({
          username: profileForm.username,
          bio: profileForm.bio,
        });
        // 更新本地状态
        setUser(updatedUser);
        showSuccess(t('settings.messages.profileSaved'));
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
        showSuccess(t('settings.messages.notificationsSaved'));
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
        showSuccess(t('settings.messages.preferencesSaved'));
      } else {
        showInfo(t('settings.messages.useSecurityActions'));
      }
    } catch (error: any) {
      console.error('保存设置失败:', error);
      showError(error.message || t('settings.messages.saveError'));
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
        bio: user?.bio || '',
      });
      showInfo(t('settings.actions.cancelChanges'));
    } else if (activeTab === 'notifications') {
      // 重置通知设置
      setNotificationSettings(user?.notificationSettings || notificationDefaults);
      showInfo(t('settings.actions.cancelChanges'));
    } else if (activeTab === 'preferences') {
      // 重置偏好设置
      const originalPreferences = user?.preferences || preferenceDefaults;
      setPreferences(originalPreferences);
      // 恢复主题
      if (originalPreferences?.theme) {
        applyTheme(originalPreferences.theme, { persist: false });
      }
      showInfo(t('settings.actions.cancelChanges'));
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
      showError(t('settings.profile.avatarError.format'));
      event.target.value = '';
      return;
    }

    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      showError(t('settings.profile.avatarError.size'));
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
      showSuccess(t('settings.messages.avatarUpdated'));
    } catch (error: any) {
      console.error('上传头像失败:', error);
      showError(error?.message || t('settings.messages.avatarError'));
    } finally {
      setIsUploadingAvatar(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleDeleteAccount = async () => {
    setShowDeleteAccountDialog(true);
  };

  // 渲染个人信息设置
  const renderProfileSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('settings.profile.title')}</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{t('settings.profile.username')}</label>
            <Input
              value={profileForm.username}
              onChange={(e) => setProfileForm({ ...profileForm, username: e.target.value })}
              placeholder={t('settings.profile.usernamePlaceholder')}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{t('settings.profile.bio')}</label>
            <textarea
              ref={bioTextareaRef}
              value={profileForm.bio}
              onChange={(e) => {
                setProfileForm({ ...profileForm, bio: e.target.value });
                // 自动调整高度
                e.target.style.height = 'auto';
                e.target.style.height = `${e.target.scrollHeight}px`;
              }}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-0 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-blue-500 dark:focus:border-blue-400 hover:border-gray-400 dark:hover:border-gray-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 resize-none overflow-hidden transition-all duration-200"
              rows={2}
              placeholder={t('settings.profile.bioPlaceholder')}
            />
          </div>
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('settings.profile.avatar')}</h3>
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
              <img src={user.avatar} alt={t('settings.profile.avatar')} className="w-full h-full object-cover" />
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
              {isUploadingAvatar ? t('common.uploading') : t('settings.profile.uploadAvatar')}
            </Button>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">{t('settings.profile.avatarHint')}</p>
          </div>
        </div>
      </div>
    </div>
  );

  // 渲染通知设置
  const renderNotificationSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('settings.notifications.channels.title')}</h3>
        <div className="space-y-4">
          <label className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/60 cursor-pointer bg-white dark:bg-gray-900 transition-colors">
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">{t('settings.notifications.channels.email')}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('settings.notifications.channels.emailDesc')}</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.emailNotifications}
              onChange={(e) =>
                setNotificationSettings({ ...notificationSettings, emailNotifications: e.target.checked })
              }
              className="w-5 h-5 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 dark:focus:ring-blue-400 dark:bg-gray-900"
            />
          </label>
          <label className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/60 cursor-pointer bg-white dark:bg-gray-900 transition-colors">
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">{t('settings.notifications.channels.browser')}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('settings.notifications.channels.browserDesc')}</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.browserNotifications}
              onChange={(e) =>
                setNotificationSettings({ ...notificationSettings, browserNotifications: e.target.checked })
              }
              className="w-5 h-5 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 dark:focus:ring-blue-400 dark:bg-gray-900"
            />
          </label>
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('settings.notifications.types.title')}</h3>
        <div className="space-y-4">
          <label className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/60 cursor-pointer bg-white dark:bg-gray-900 transition-colors">
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">{t('settings.notifications.types.newChapter')}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('settings.notifications.types.newChapterDesc')}</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.newChapter}
              onChange={(e) => setNotificationSettings({ ...notificationSettings, newChapter: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 dark:focus:ring-blue-400 dark:bg-gray-900"
            />
          </label>
          <label className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/60 cursor-pointer bg-white dark:bg-gray-900 transition-colors">
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">{t('settings.notifications.types.comments')}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('settings.notifications.types.commentsDesc')}</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.comments}
              onChange={(e) => setNotificationSettings({ ...notificationSettings, comments: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 dark:focus:ring-blue-400 dark:bg-gray-900"
            />
          </label>
          <label className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/60 cursor-pointer bg-white dark:bg-gray-900 transition-colors">
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">{t('settings.notifications.types.mentions')}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('settings.notifications.types.mentionsDesc')}</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.mentions}
              onChange={(e) => setNotificationSettings({ ...notificationSettings, mentions: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 dark:focus:ring-blue-400 dark:bg-gray-900"
            />
          </label>
          <label className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/60 cursor-pointer bg-white dark:bg-gray-900 transition-colors">
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">{t('settings.notifications.types.systemUpdates')}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('settings.notifications.types.systemUpdatesDesc')}</p>
            </div>
            <input
              type="checkbox"
              checked={notificationSettings.systemUpdates}
              onChange={(e) => setNotificationSettings({ ...notificationSettings, systemUpdates: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 dark:focus:ring-blue-400 dark:bg-gray-900"
            />
          </label>
        </div>
      </div>
    </div>
  );

  // 渲染安全设置
  const renderSecuritySettings = () => {
    const { refreshTokenExpiresAt } = useAuthStore.getState();

    // 格式化过期时间
    const formatExpiryDate = (timestamp: number | null) => {
      if (!timestamp) return '未知';
      const date = new Date(timestamp);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    };

    // 计算剩余天数
    const getDaysLeft = (timestamp: number | null) => {
      if (!timestamp) return null;
      const now = Date.now();
      const timeLeft = timestamp - now;
      if (timeLeft <= 0) return 0;
      return Math.ceil(timeLeft / (24 * 60 * 60 * 1000));
    };

    const daysLeft = getDaysLeft(refreshTokenExpiresAt);

    return (
      <div className="space-y-6">
      {/* 账户安全 */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">{t('settings.security.account.title')}</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">{t('settings.security.account.subtitle')}</p>
        <div className="space-y-3">
          {/* 邮箱地址 */}
          <button
            onClick={() => navigate('/settings/change-email')}
            className="w-full flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors cursor-pointer text-left"
          >
            <div className="flex items-center gap-4">
              <div className="flex items-center justify-center w-10 h-10 bg-gray-100 dark:bg-gray-700 rounded-lg">
                <Mail className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              </div>
              <div>
                <p className="font-medium text-gray-900 dark:text-gray-100">{t('settings.security.account.email')}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">{user?.email || t('common.notSet')}</p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
              <span className="text-sm">{t('common.edit')}</span>
              <ChevronRight className="w-5 h-5" />
            </div>
          </button>

          {/* 登录密码 */}
          <button
            onClick={() => navigate('/settings/change-password')}
            className="w-full flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors cursor-pointer text-left"
          >
            <div className="flex items-center gap-4">
              <div className="flex items-center justify-center w-10 h-10 bg-gray-100 dark:bg-gray-700 rounded-lg">
                <Lock className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              </div>
              <div>
                <p className="font-medium text-gray-900 dark:text-gray-100">{t('settings.security.account.password')}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">{t('settings.security.account.passwordDesc')}</p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
              <span className="text-sm">{t('common.edit')}</span>
              <ChevronRight className="w-5 h-5" />
            </div>
          </button>

          {/* 登录有效期 */}
          <div className="w-full flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800/50">
            <div className="flex items-center gap-4">
              <div className="flex items-center justify-center w-10 h-10 bg-gray-100 dark:bg-gray-700 rounded-lg">
                <Clock className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              </div>
              <div>
                <p className="font-medium text-gray-900 dark:text-gray-100">登录有效期</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {refreshTokenExpiresAt ? (
                    <>
                      有效期至 {formatExpiryDate(refreshTokenExpiresAt)}
                      {daysLeft !== null && daysLeft > 0 && (
                        <span className={`ml-2 ${daysLeft <= 1 ? 'text-orange-500 font-medium' : ''}`}>
                          (剩余 {daysLeft} 天)
                        </span>
                      )}
                      {daysLeft === 0 && (
                        <span className="ml-2 text-orange-500 font-medium">(即将过期)</span>
                      )}
                    </>
                  ) : (
                    '未知'
                  )}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{t('settings.security.sessions.title')}</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{t('settings.security.sessions.subtitle')}</p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="gray-outline" size="sm" onClick={handleRefreshSessions} disabled={isSessionsLoading}>
              {isSessionsLoading ? t('common.loading') : t('common.refresh')}
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={handleLogoutOtherSessions}
              disabled={isLoggingOutOthers || isSessionsLoading || sessions.length <= 1}
            >
              {isLoggingOutOthers ? t('common.processing') : t('settings.security.sessions.logoutOthers')}
            </Button>
          </div>
        </div>
        {isSessionsLoading ? (
          <div className="mt-4 p-4 text-center text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 rounded-lg">
            {t('settings.security.sessions.loadingInfo')}
          </div>
        ) : sessions.length === 0 ? (
          <div className="mt-4 p-4 text-center text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 rounded-lg">
            {t('settings.security.sessions.noOtherDevices')}
          </div>
        ) : (
          <div className="mt-4 space-y-3 max-h-[400px] overflow-y-auto pr-2">
            {sessions.map((session) => (
              <div
                key={session.id}
                className="flex items-start justify-between gap-4 p-4 border-2 border-blue-200 dark:border-blue-900 rounded-lg bg-blue-50 dark:bg-blue-900/20 hover:bg-blue-100 dark:hover:bg-blue-900/35 transition-colors"
              >
                <div className="flex items-start gap-3">
                  <div className="mt-1">
                    {resolveDeviceIcon(session.deviceType)}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="font-medium text-gray-900 dark:text-gray-100">
                        {session.deviceName || t('settings.security.sessions.unknownDevice')}
                      </p>
                      {session.isCurrent && (
                        <span className="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full">
                          {t('settings.security.sessions.currentDevice')}
                        </span>
                      )}
                      {!session.isActive && (
                        <span className="px-2 py-0.5 text-xs font-medium bg-gray-200 dark:bg-gray-800 text-gray-600 dark:text-gray-300 rounded-full">
                          {t('settings.security.sessions.loggedOut')}
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-800 dark:text-gray-200 mt-1">
                      {(session.browser || t('settings.security.sessions.unknownBrowser'))}{session.browserVersion ? ` · ${session.browserVersion}` : ''}
                    </p>
                    <p className="text-xs text-gray-700 dark:text-gray-400 mt-1">
                      {session.operatingSystem ? `${t('settings.security.sessions.system')}: ${session.operatingSystem}` : `${t('settings.security.sessions.system')}: ${t('common.unknown')}`}
                    </p>
                    <p className="text-xs text-gray-700 dark:text-gray-400 mt-1">
                      {session.ipAddress ? `${t('settings.security.sessions.ip')}: ${session.ipAddress}` : `${t('settings.security.sessions.ip')}: ${t('common.unknown')}`}
                      {session.location ? ` · ${t('settings.security.sessions.location')}: ${session.location}` : ''}
                    </p>
                    <p className="text-xs text-gray-700 dark:text-gray-400 mt-1">
                      {t('settings.security.sessions.lastActive')}: {formatTimestamp(session.lastActiveAt)}
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
                    {sessionActionId === session.id ? t('common.processing') : t('settings.security.sessions.logout')}
                  </Button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">{t('settings.security.danger.title')}</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">{t('settings.security.danger.subtitle')}</p>
        <Button
          variant="danger"
          onClick={handleDeleteAccount}
          disabled={isDeletingAccount}
        >
          {isDeletingAccount ? t('common.deleting') : t('settings.security.danger.deleteAccount')}
        </Button>
      </div>
    </div>
    );
  };

  // 渲染偏好设置
  const renderPreferencesSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('settings.preferences.appearance.title')}</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">{t('settings.preferences.appearance.theme')}</label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { value: 'light', labelKey: 'settings.preferences.appearance.light', icon: Sun },
                { value: 'dark', labelKey: 'settings.preferences.appearance.dark', icon: Moon },
                { value: 'auto', labelKey: 'settings.preferences.appearance.auto', icon: Settings },
              ].map((theme) => {
                const Icon = theme.icon;
                return (
                  <button
                    key={theme.value}
                    onClick={() => handleThemeSelect(theme.value as UserPreferences['theme'])}
                    className={`flex flex-col items-center justify-center p-4 border-2 rounded-lg transition-all ${
                      preferences.theme === theme.value
                        ? 'border-blue-500 bg-blue-50 dark:border-blue-500 dark:bg-blue-900/30'
                        : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50 dark:border-gray-700 dark:hover:border-gray-500 dark:hover:bg-gray-800'
                    }`}
                  >
                    <Icon className={`w-6 h-6 mb-2 ${
                      preferences.theme === theme.value
                        ? 'text-blue-600 dark:text-blue-400'
                        : 'text-gray-500 dark:text-gray-400'
                    }`} />
                    <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{t(theme.labelKey)}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('settings.preferences.language.title')}</h3>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{t('settings.preferences.language.label')}</label>
          <select
            value={preferences.language}
            onChange={(e) => handleLanguageSelect(e.target.value as LanguageCode)}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-400 focus:border-blue-300 dark:focus:border-blue-400 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 [&>option:checked]:bg-blue-50 [&>option:checked]:text-blue-700 dark:[&>option:checked]:bg-blue-900/40 dark:[&>option:checked]:text-blue-100"
          >
            {languages.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.nativeName}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('settings.preferences.editor.title')}</h3>
        <div className="space-y-4">
          <label className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/60 cursor-pointer bg-white dark:bg-gray-900 transition-colors">
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">{t('settings.preferences.editor.autoSave')}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('settings.preferences.editor.autoSaveDesc')}</p>
            </div>
            <input
              type="checkbox"
              checked={preferences.autoSave}
              onChange={(e) => setPreferences({ ...preferences, autoSave: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 dark:focus:ring-blue-400 dark:bg-gray-900"
            />
          </label>
          {preferences.autoSave && (
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{t('settings.preferences.editor.autoSaveInterval')}</label>
              <Input
                type="number"
                value={preferences.autoSaveInterval}
                onChange={(e) => setPreferences({ ...preferences, autoSaveInterval: parseInt(e.target.value) })}
                min={10}
                max={300}
              />
            </div>
          )}
          <label className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/60 cursor-pointer bg-white dark:bg-gray-900 transition-colors">
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">{t('settings.preferences.editor.aiAutoComplete')}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('settings.preferences.editor.aiAutoCompleteDesc')}</p>
              <p className="text-xs text-orange-500 mt-1">{t('settings.preferences.editor.aiAutoCompleteWarning')}</p>
            </div>
            <input
              type="checkbox"
              checked={preferences.aiAutoComplete}
              onChange={(e) => setPreferences({ ...preferences, aiAutoComplete: e.target.checked })}
              className="w-5 h-5 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 dark:focus:ring-blue-400 dark:bg-gray-900"
            />
          </label>
        </div>
      </div>
    </div>
  );

  const confirmLogoutSession = async () => {
    if (!logoutTarget) return;
    setSessionActionId(logoutTarget.id);
    try {
      await DataService.logoutSession(logoutTarget.id);
      showSuccess(t('settings.messages.sessionLoggedOut'));
      await loadSessions();
    } catch (error: any) {
      console.error('退出会话失败?', error);
      showError(error?.message || t('settings.messages.sessionLogoutError'));
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
      showSuccess(t('settings.messages.othersLoggedOut'));
      await loadSessions();
    } catch (error: any) {
      console.error('退出其他设备失败?', error);
      showError(error?.message || t('settings.messages.othersLogoutError'));
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
      showError(t('settings.messages.passwordRequired'));
      return;
    }

    setIsDeletingAccount(true);
    try {
      await DataService.deleteAccount(password);
      showSuccess(t('settings.messages.accountDeleted'));
      logout();
      window.location.href = '/';
    } catch (error: any) {
      console.error('删除账户失败:', error);
      showError(error?.message || t('settings.messages.accountDeleteError'));
    } finally {
      setIsDeletingAccount(false);
    }
  };

  return (
    <>
    <div className="h-full flex flex-col bg-gray-50 dark:bg-gray-900 overflow-hidden">
      {/* 固定页眉 */}
      <div className="flex-shrink-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{t("settings.title")}</h1>
        <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">{t("settings.subtitle")}</p>
      </div>

      {/* 内容区 - 左侧固定，右侧滚动 */}
      <div className="flex-1 min-h-0 flex overflow-hidden p-6 gap-6">
        {/* 左侧标签栏 - 固定 */}
        <div className="flex-shrink-0 w-64">
          <Card className="!bg-white dark:!bg-gray-900 shadow-none border-gray-100 dark:border-gray-800 sticky top-6">
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
                          ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/40 dark:text-blue-100'
                          : 'text-gray-900 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-100 dark:hover:bg-gray-800 dark:hover:text-gray-50'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span className="font-medium">{t(tab.labelKey)}</span>
                    </button>
                  );
                })}
              </nav>
            </div>
          </Card>
        </div>

        {/* 右侧内容区 - 可滚动 */}
        <div className="flex-1 min-h-0 min-w-0 overflow-auto">
          <Card className="!bg-white dark:!bg-gray-900 shadow-none border-gray-100 dark:border-gray-800">
            <div className="p-6">
            {isInitializing ? (
            <div className="py-16 text-center text-gray-500 dark:text-gray-400">{t('settings.messages.loadingSettings')}</div>
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
              <div className="border-t border-gray-200 dark:border-gray-800 mt-6 pt-6">
                <div className="flex items-center justify-end space-x-3">
                  <Button variant="outline" onClick={handleCancel} disabled={isSaving}>
                    {t('common.cancel')}
                  </Button>
                  <Button variant="primary" onClick={handleSave} disabled={isSaving || isInitializing}>
                    <Save className="w-4 h-4 mr-2" />
                    {isSaving ? t('common.saving') : t('settings.actions.saveChanges')}
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
    </div>

      <ConfirmDialog
        isOpen={!!logoutTarget}
        title={t('settings.security.dialogs.logoutDevice.title')}
        message={t('settings.security.dialogs.logoutDevice.message', { device: logoutTarget?.deviceName || logoutTarget?.deviceType || t('settings.security.sessions.unknownDevice') })}
        confirmText={t('settings.security.dialogs.logoutDevice.confirm')}
        cancelText={t('common.cancel')}
        variant="warning"
        onConfirm={confirmLogoutSession}
        onCancel={() => setLogoutTarget(null)}
      />

      <ConfirmDialog
        isOpen={showLogoutOthersConfirm}
        title={t('settings.security.dialogs.logoutOthers.title')}
        message={t('settings.security.dialogs.logoutOthers.message')}
        confirmText={t('settings.security.dialogs.logoutOthers.confirm')}
        cancelText={t('settings.security.dialogs.logoutOthers.cancel')}
        variant="warning"
        onConfirm={confirmLogoutOtherSessions}
        onCancel={() => setShowLogoutOthersConfirm(false)}
      />

      <InputDialog
        isOpen={showDeleteAccountDialog}
        onClose={() => setShowDeleteAccountDialog(false)}
        onConfirm={confirmDeleteAccount}
        title={t('settings.security.dialogs.deleteAccount.title')}
        confirmText={isDeletingAccount ? t('common.deleting') : t('settings.security.dialogs.deleteAccount.confirm')}
        cancelText={t('common.cancel')}
        fields={[
          {
            name: 'password',
            label: t('settings.security.dialogs.deleteAccount.passwordLabel'),
            placeholder: t('settings.security.dialogs.deleteAccount.passwordPlaceholder'),
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
