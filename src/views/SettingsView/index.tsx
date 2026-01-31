import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Settings, User, Bell, Shield, Save, Moon, Sun, Monitor, Smartphone, Tablet, Mail, Lock, ChevronRight, Clock, X, Pencil, Search, ArrowLeft, AlertCircle, Eye, EyeOff } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Card, Button, Input, ImageCropper } from '../../components/common';
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
  aiAutoComplete: false, // 默认关闭，避免意外消耗积分
};

/**
 * 设置分类类型
 */
type SettingTab = 'profile' | 'notifications' | 'security' | 'preferences' | 'changeEmail' | 'changePassword';

/**
 * SettingsView 组件 - 设置页面
 */
const SettingsView: React.FC = () => {
  const { user, setUser, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const bioTextareaRef = useRef<HTMLTextAreaElement | null>(null);
  // 标记表单是否已从 user 数据初始化，避免后续 user 更新时覆盖用户编辑
  const formInitializedRef = useRef(false);

  // 支持从修改密码页面返回时恢复到安全设置标签
  const initialTab = (location.state as { activeTab?: SettingTab })?.activeTab || 'profile';
  const [activeTab, setActiveTab] = useState<SettingTab>(initialTab);
  const [isSaving, setIsSaving] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const [isDeletingAccount, setIsDeletingAccount] = useState(false);
  const [isUploadingAvatar, setIsUploadingAvatar] = useState(false);
  const [isCropperOpen, setIsCropperOpen] = useState(false);
  const [selectedImageSrc, setSelectedImageSrc] = useState<string>('');
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

  // 修改邮箱相关状态
  const [newEmail, setNewEmail] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [isSendingCode, setIsSendingCode] = useState(false);
  const [isVerifyingEmail, setIsVerifyingEmail] = useState(false);
  const [codeSent, setCodeSent] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const countdownTimerRef = useRef<NodeJS.Timeout | null>(null);

  // 修改密码相关状态
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [securityForm, setSecurityForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // 清理倒计时
  useEffect(() => {
    return () => {
      if (countdownTimerRef.current) {
        clearInterval(countdownTimerRef.current);
      }
    };
  }, []);

  // 邮箱格式验证
  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  // 发送验证码
  const handleSendCode = async () => {
    if (!newEmail.trim()) {
      showError('请输入新邮箱地址');
      return;
    }
    if (!validateEmail(newEmail)) {
      showError('请输入有效的邮箱地址');
      return;
    }
    if (newEmail === user?.email) {
      showError('新邮箱不能与当前邮箱相同');
      return;
    }

    setIsSendingCode(true);
    try {
      await DataService.sendEmailVerificationCode(newEmail);
      showSuccess('验证码已发送到新邮箱，请查收');
      setCodeSent(true);
      if (countdownTimerRef.current) {
        clearInterval(countdownTimerRef.current);
      }
      setCountdown(60);
      countdownTimerRef.current = setInterval(() => {
        setCountdown((prev) => {
          if (prev <= 1) {
            if (countdownTimerRef.current) {
              clearInterval(countdownTimerRef.current);
              countdownTimerRef.current = null;
            }
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } catch (error: any) {
      showError(error?.detail || error?.message || '发送验证码失败，请稍后重试');
    } finally {
      setIsSendingCode(false);
    }
  };

  // 验证并更新邮箱
  const handleVerifyAndUpdateEmail = async () => {
    if (!newEmail.trim()) {
      showError('请输入新邮箱地址');
      return;
    }
    if (!verificationCode.trim()) {
      showError('请输入验证码');
      return;
    }

    setIsVerifyingEmail(true);
    try {
      const updatedUser = await DataService.verifyAndUpdateEmail(newEmail, verificationCode);
      setUser(updatedUser);
      showSuccess('邮箱修改成功');
      // 重置状态并返回安全设置
      setNewEmail('');
      setVerificationCode('');
      setCodeSent(false);
      setCountdown(0);
      setTimeout(() => setActiveTab('security'), 1000);
    } catch (error: any) {
      showError(error?.detail || error?.message || '验证失败，请检查验证码是否正确');
    } finally {
      setIsVerifyingEmail(false);
    }
  };

  // 重置邮箱表单
  const handleResetEmailForm = () => {
    setNewEmail('');
    setVerificationCode('');
    setCodeSent(false);
    setCountdown(0);
    if (countdownTimerRef.current) {
      clearInterval(countdownTimerRef.current);
      countdownTimerRef.current = null;
    }
  };

  // 修改密码
  const handleChangePassword = async () => {
    if (!securityForm.currentPassword || !securityForm.newPassword || !securityForm.confirmPassword) {
      showError('请完整填写密码信息');
      return;
    }
    if (securityForm.newPassword !== securityForm.confirmPassword) {
      showError('新密码与确认密码不一致');
      return;
    }
    if (securityForm.newPassword.length < 8) {
      showError('新密码长度至少为 8 位');
      return;
    }
    const hasLetter = /[a-zA-Z]/.test(securityForm.newPassword);
    const hasNumber = /\d/.test(securityForm.newPassword);
    const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(securityForm.newPassword);
    if (!hasLetter || !hasNumber || !hasSpecial) {
      showError('密码必须包含字母、数字、特殊符号三种字符');
      return;
    }
    if (securityForm.newPassword.length > 20) {
      showError('密码长度不能超过 20 位');
      return;
    }

    setIsChangingPassword(true);
    try {
      const message = await DataService.changePassword(securityForm.currentPassword, securityForm.newPassword);
      showSuccess(message || '密码已更新');
      // 重置表单并返回安全设置
      setSecurityForm({ currentPassword: '', newPassword: '', confirmPassword: '' });
      setShowCurrentPassword(false);
      setShowNewPassword(false);
      setShowConfirmPassword(false);
      setTimeout(() => setActiveTab('security'), 1000);
    } catch (error: any) {
      showError(error?.detail || error?.message || '密码修改失败');
    } finally {
      setIsChangingPassword(false);
    }
  };

  // 重置密码表单
  const handleResetPasswordForm = () => {
    setSecurityForm({ currentPassword: '', newPassword: '', confirmPassword: '' });
    setShowCurrentPassword(false);
    setShowNewPassword(false);
    setShowConfirmPassword(false);
  };

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

  // 只在页面首次加载时从服务器数据初始化表单（在 loadSettings 中处理）
  // 后续的 user 更新（如头像上传）不会触发表单重置
  useEffect(() => {
    // 仅初始化通知设置和偏好设置（这些不是用户正在编辑的表单字段）
    if (user) {
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
        // 只在页面首次加载时初始化 profileForm，避免后续 user 更新时覆盖用户正在编辑的内容
        setProfileForm({
          username: userResponse?.username || '',
          bio: userResponse?.bio || '',
        });
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

    // Read file and open cropper
    const reader = new FileReader();
    reader.onload = () => {
      setSelectedImageSrc(reader.result as string);
      setIsCropperOpen(true);
    };
    reader.readAsDataURL(file);

    // Clear input for re-selection of the same file
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleCropSave = async (croppedBlob: Blob) => {
    setIsCropperOpen(false);
    setIsUploadingAvatar(true);

    try {
      // Convert blob to File for upload
      const file = new File([croppedBlob], 'avatar.png', { type: 'image/png' });
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
      setSelectedImageSrc('');
    }
  };

  const handleCropperClose = () => {
    setIsCropperOpen(false);
    setSelectedImageSrc('');
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
            <Input
              value={profileForm.username}
              onChange={(e) => setProfileForm({ ...profileForm, username: e.target.value })}
              placeholder={t('settings.profile.usernamePlaceholder')}
            />
          </div>
          <div>
            <textarea
              ref={bioTextareaRef}
              value={profileForm.bio}
              onChange={(e) => {
                setProfileForm({ ...profileForm, bio: e.target.value });
                // 自动调整高度
                e.target.style.height = 'auto';
                e.target.style.height = `${Math.min(e.target.scrollHeight, 200)}px`;
              }}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-0 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-blue-500 dark:focus:border-blue-400 hover:border-gray-400 dark:hover:border-gray-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 resize-none overflow-y-auto transition-all duration-200"
              rows={3}
              style={{ maxHeight: '200px' }}
              placeholder={t('settings.profile.bioPlaceholder')}
            />
          </div>
        </div>
      </div>

      <div className="pt-6">
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

      <div className="pt-6">
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
            onClick={() => setActiveTab('changeEmail')}
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
            onClick={() => setActiveTab('changePassword')}
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

      <div className="pt-6">
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

      <div className="pt-6">
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

      <div className="pt-6">
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

  // 渲染修改邮箱页面
  const renderChangeEmailSettings = () => {
    const inputClassName = "block w-full px-3 py-2 border rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-0 transition-all duration-200 bg-white dark:bg-gray-900 border-gray-300 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-700 dark:focus:border-blue-400 dark:focus:ring-blue-400 hover:border-gray-400 dark:hover:border-gray-500";
    const disabledInputClassName = "block w-full px-3 py-2 border rounded-lg text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 border-gray-200 dark:border-gray-700 cursor-not-allowed";

    return (
      <div className="space-y-6">
        {/* 返回按钮 */}
        <button
          onClick={() => { handleResetEmailForm(); setActiveTab('security'); }}
          className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>返回安全设置</span>
        </button>

        {/* 注意提示 */}
        <div className="flex items-start gap-3 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
          <AlertCircle className="w-5 h-5 text-blue-500 dark:text-blue-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-blue-800 dark:text-blue-200">注意</p>
            <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
              修改邮箱后，您可以使用新邮箱或用户名登录。
            </p>
          </div>
        </div>

        {/* 表单字段 */}
        <div className="space-y-5">
          <div>
            <input type="email" value={user?.email || ''} disabled className={disabledInputClassName} />
          </div>

          <div>
            <input
              type="email"
              value={newEmail}
              onChange={(e) => setNewEmail(e.target.value)}
              placeholder="请输入新的邮箱地址"
              disabled={codeSent}
              className={codeSent ? disabledInputClassName : inputClassName}
            />
          </div>

          <div>
            <div className="relative">
              <input
                type="text"
                inputMode="numeric"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, ''))}
                placeholder="请输入6位验证码"
                maxLength={6}
                disabled={!codeSent}
                className={`${codeSent ? inputClassName : disabledInputClassName} pr-28`}
              />
              <button
                type="button"
                onClick={handleSendCode}
                disabled={isSendingCode || (codeSent && countdown > 0) || !newEmail.trim() || !validateEmail(newEmail)}
                className="absolute right-1 top-1/2 -translate-y-1/2 px-3 py-1.5 text-sm font-medium rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed bg-blue-500 hover:bg-blue-600 text-white disabled:bg-gray-300 dark:disabled:bg-gray-600"
              >
                {isSendingCode ? '发送中...' : (countdown > 0 ? `${countdown}s` : (codeSent ? '重新发送' : '发送验证码'))}
              </button>
            </div>
          </div>
        </div>

        {/* 操作按钮 */}
        <div className="flex items-center justify-end gap-3 pt-4">
          <Button variant="outline" onClick={handleResetEmailForm} disabled={isSendingCode || isVerifyingEmail}>
            重置
          </Button>
          <Button variant="secondary" onClick={handleVerifyAndUpdateEmail} disabled={isVerifyingEmail || !verificationCode.trim() || !codeSent}>
            <Mail className="w-4 h-4 mr-2" />
            {isVerifyingEmail ? '验证中...' : '确认修改'}
          </Button>
        </div>
      </div>
    );
  };

  // 渲染修改密码页面
  const renderChangePasswordSettings = () => {
    const inputClassName = "block w-full px-3 py-2 border rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-0 transition-all duration-200 bg-white dark:bg-gray-900 border-gray-300 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-700 dark:focus:border-blue-400 dark:focus:ring-blue-400 hover:border-gray-400 dark:hover:border-gray-500";

    return (
      <div className="space-y-6">
        {/* 返回按钮 */}
        <button
          onClick={() => { handleResetPasswordForm(); setActiveTab('security'); }}
          className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>返回安全设置</span>
        </button>

        {/* 密码要求提示 */}
        <div className="flex items-start gap-3 p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg">
          <AlertCircle className="w-5 h-5 text-amber-500 dark:text-amber-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-amber-800 dark:text-amber-200">密码要求</p>
            <ul className="text-sm text-amber-700 dark:text-amber-300 mt-1 list-disc list-inside">
              <li>长度 8-20 位</li>
              <li>必须包含字母、数字、特殊符号</li>
            </ul>
          </div>
        </div>

        {/* 表单字段 */}
        <div className="space-y-5">
          <div>
            <div className="relative">
              <input
                type={showCurrentPassword ? 'text' : 'password'}
                value={securityForm.currentPassword}
                onChange={(e) => setSecurityForm({ ...securityForm, currentPassword: e.target.value })}
                placeholder="请输入当前密码"
                className={`${inputClassName} pr-10`}
              />
              <button
                type="button"
                onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showCurrentPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <div>
            <div className="relative">
              <input
                type={showNewPassword ? 'text' : 'password'}
                value={securityForm.newPassword}
                onChange={(e) => setSecurityForm({ ...securityForm, newPassword: e.target.value })}
                placeholder="请输入新密码"
                className={`${inputClassName} pr-10`}
              />
              <button
                type="button"
                onClick={() => setShowNewPassword(!showNewPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showNewPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <div>
            <div className="relative">
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                value={securityForm.confirmPassword}
                onChange={(e) => setSecurityForm({ ...securityForm, confirmPassword: e.target.value })}
                placeholder="请再次输入新密码"
                className={`${inputClassName} pr-10`}
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </div>

        {/* 操作按钮 */}
        <div className="flex items-center justify-end gap-3 pt-4">
          <Button variant="outline" onClick={handleResetPasswordForm} disabled={isChangingPassword}>
            重置
          </Button>
          <Button variant="secondary" onClick={handleChangePassword} disabled={isChangingPassword}>
            <Lock className="w-4 h-4 mr-2" />
            {isChangingPassword ? '修改中...' : '确认修改'}
          </Button>
        </div>
      </div>
    );
  };

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
    <div className="h-full flex bg-gray-50 dark:bg-gray-900 overflow-hidden">
      {/* 左侧导航栏 - Discord 风格 */}
      <div className="flex-shrink-0 w-60 bg-white dark:bg-gray-900 flex flex-col overflow-hidden border-r border-gray-200 dark:border-gray-700">
        {/* 用户信息区域 */}
        <div className="px-3 pt-4 pb-2 flex items-center">
          <div className="flex items-center gap-3 px-3 py-2 bg-gray-100 dark:bg-gray-800 rounded-lg shadow-sm w-full">
            <div className="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900/40 flex items-center justify-center overflow-hidden flex-shrink-0">
              {user?.avatar ? (
                <img src={user.avatar} alt={user?.username} className="w-full h-full object-cover" />
              ) : (
                <span className="text-lg font-bold text-blue-600 dark:text-blue-400">
                  {user?.username ? user.username[0].toUpperCase() : 'U'}
                </span>
              )}
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-semibold text-gray-900 dark:text-gray-100 truncate text-base">
                {user?.username || t('common.unknown')}
              </p>
            </div>
          </div>
        </div>

        {/* 导航菜单 */}
        <div className="flex-1 overflow-y-auto px-2 py-3 pb-4">
          <nav className="space-y-0.5">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-md transition-colors text-left ${
                    activeTab === tab.id
                      ? 'bg-gray-300/60 dark:bg-gray-700/60 text-gray-900 dark:text-gray-100'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200/60 dark:hover:bg-gray-700/40 hover:text-gray-900 dark:hover:text-gray-100'
                  }`}
                >
                  <Icon className="w-5 h-5 flex-shrink-0" />
                  <span className="text-sm font-medium">{t(tab.labelKey)}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* 右侧内容区 */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden bg-white dark:bg-gray-900">
        {/* 顶部标题栏 */}
        <div className="h-12 flex-shrink-0 flex items-center justify-between px-10 border-b border-gray-200 dark:border-gray-700">
          <h1 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
            {activeTab === 'changeEmail'
              ? '邮箱设置'
              : activeTab === 'changePassword'
                ? '修改密码'
                : t(tabs.find(tab => tab.id === activeTab)?.labelKey || 'settings.tabs.profile')}
          </h1>
          <button
            onClick={() => navigate(-1)}
            className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 dark:text-gray-400 transition-colors"
            title={t('common.close')}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 内容区域 - 可滚动 */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-3xl mx-auto px-10 py-6">
            {isInitializing ? (
              <div className="py-16 text-center text-gray-500 dark:text-gray-400">{t('settings.messages.loadingSettings')}</div>
            ) : (
              <>
                {activeTab === 'profile' && renderProfileSettings()}
                {activeTab === 'notifications' && renderNotificationSettings()}
                {activeTab === 'security' && renderSecuritySettings()}
                {activeTab === 'preferences' && renderPreferencesSettings()}
                {activeTab === 'changeEmail' && renderChangeEmailSettings()}
                {activeTab === 'changePassword' && renderChangePasswordSettings()}
              </>
            )}

            {/* 保存按钮区域 - 仅在基础设置标签页显示 */}
            {['profile', 'notifications', 'preferences'].includes(activeTab) ? (
              <div className="mt-8 pt-6">
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
              <div className="mt-8 pt-6"></div>
            )}
          </div>
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

      {/* 头像裁剪器 */}
      <ImageCropper
        isOpen={isCropperOpen}
        imageSrc={selectedImageSrc}
        onClose={handleCropperClose}
        onSave={handleCropSave}
        aspect={1}
        cropShape="round"
      />

      {/* Toast 通知容器 */}
      <ToastContainer messages={messages} onClose={close} />
    </>
  );
};

export default SettingsView;
