import React, { useState } from 'react';
import { Settings, User, Bell, Shield, Save, Moon, Sun, Globe, Keyboard } from 'lucide-react';
import { Card, Button, Input } from '../../components/common';
import { useAuthStore } from '../../store/authStore';

/**
 * 设置分类类型
 */
type SettingTab = 'profile' | 'notifications' | 'security' | 'preferences';

/**
 * SettingsView 组件 - 设置页面
 */
const SettingsView: React.FC = () => {
  const { user } = useAuthStore();
  const [activeTab, setActiveTab] = useState<SettingTab>('profile');
  const [isSaving, setIsSaving] = useState(false);

  // 个人信息表单
  const [profileForm, setProfileForm] = useState({
    username: user?.username || '',
    email: user?.email || '',
    bio: '热爱创作的小说作者',
    website: '',
  });

  // 通知设置
  const [notificationSettings, setNotificationSettings] = useState({
    emailNotifications: true,
    browserNotifications: false,
    newChapter: true,
    comments: true,
    mentions: true,
    systemUpdates: false,
  });

  // 安全设置
  const [securityForm, setSecurityForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  // 偏好设置
  const [preferences, setPreferences] = useState({
    theme: 'light' as 'light' | 'dark' | 'auto',
    language: 'zh-CN',
    fontSize: 'medium' as 'small' | 'medium' | 'large',
    autoSave: true,
    autoSaveInterval: 30,
  });

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
    // TODO: 调用 API 保存设置
    setTimeout(() => {
      setIsSaving(false);
      alert('设置已保存');
    }, 1000);
  };

  // 渲染个人信息设置
  const renderProfileSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">个人信息</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">用户名</label>
            <Input
              value={profileForm.username}
              onChange={(e) => setProfileForm({ ...profileForm, username: e.target.value })}
              placeholder="输入用户名"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
            <Input
              type="email"
              value={profileForm.email}
              onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })}
              placeholder="输入邮箱地址"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">个人简介</label>
            <textarea
              value={profileForm.bio}
              onChange={(e) => setProfileForm({ ...profileForm, bio: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={4}
              placeholder="介绍一下自己..."
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">个人网站</label>
            <Input
              type="url"
              value={profileForm.website}
              onChange={(e) => setProfileForm({ ...profileForm, website: e.target.value })}
              placeholder="https://example.com"
            />
          </div>
        </div>
      </div>

      <div className="border-t border-gray-200 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">头像</h3>
        <div className="flex items-center space-x-4">
          <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center">
            <span className="text-2xl font-bold text-blue-600">
              {user?.username ? user.username[0].toUpperCase() : 'U'}
            </span>
          </div>
          <div>
            <Button variant="outline" size="sm">
              上传新头像
            </Button>
            <p className="text-sm text-gray-500 mt-2">支持 JPG、PNG 格式，不超过 2MB</p>
          </div>
        </div>
      </div>
    </div>
  );

  // 渲染通知设置
  const renderNotificationSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">通知渠道</h3>
        <div className="space-y-4">
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
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
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
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

      <div className="border-t border-gray-200 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">通知类型</h3>
        <div className="space-y-4">
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
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
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
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
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
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
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
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
        <h3 className="text-lg font-semibold text-gray-900 mb-4">修改密码</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">当前密码</label>
            <Input
              type="password"
              value={securityForm.currentPassword}
              onChange={(e) => setSecurityForm({ ...securityForm, currentPassword: e.target.value })}
              placeholder="输入当前密码"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">新密码</label>
            <Input
              type="password"
              value={securityForm.newPassword}
              onChange={(e) => setSecurityForm({ ...securityForm, newPassword: e.target.value })}
              placeholder="输入新密码"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">确认新密码</label>
            <Input
              type="password"
              value={securityForm.confirmPassword}
              onChange={(e) => setSecurityForm({ ...securityForm, confirmPassword: e.target.value })}
              placeholder="再次输入新密码"
            />
          </div>
          <Button variant="outline">更新密码</Button>
        </div>
      </div>

      <div className="border-t border-gray-200 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">登录会话</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <p className="font-medium text-gray-900">当前设备</p>
              <p className="text-sm text-gray-600">Windows • Chrome • 北京</p>
              <p className="text-xs text-gray-500 mt-1">最后活动: 刚刚</p>
            </div>
            <span className="px-3 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">当前</span>
          </div>
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div>
              <p className="font-medium text-gray-900">移动设备</p>
              <p className="text-sm text-gray-600">iPhone • Safari • 上海</p>
              <p className="text-xs text-gray-500 mt-1">最后活动: 2小时前</p>
            </div>
            <Button variant="outline" size="sm">
              退出登录
            </Button>
          </div>
        </div>
      </div>

      <div className="border-t border-gray-200 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">危险操作</h3>
        <p className="text-sm text-gray-600 mb-4">删除账号后将无法恢复，请谨慎操作</p>
        <Button variant="outline">删除账号</Button>
      </div>
    </div>
  );

  // 渲染偏好设置
  const renderPreferencesSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">外观</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">主题</label>
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
                    onClick={() => setPreferences({ ...preferences, theme: theme.value as any })}
                    className={`flex flex-col items-center justify-center p-4 border-2 rounded-lg transition-all ${
                      preferences.theme === theme.value
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="w-6 h-6 mb-2" />
                    <span className="text-sm font-medium">{theme.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">字体大小</label>
            <div className="flex items-center space-x-2">
              {['small', 'medium', 'large'].map((size) => (
                <button
                  key={size}
                  onClick={() => setPreferences({ ...preferences, fontSize: size as any })}
                  className={`px-4 py-2 border rounded-lg transition-colors ${
                    preferences.fontSize === size
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  {size === 'small' ? '小' : size === 'medium' ? '中' : '大'}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-gray-200 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">语言和地区</h3>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">界面语言</label>
          <select
            value={preferences.language}
            onChange={(e) => setPreferences({ ...preferences, language: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="zh-CN">简体中文</option>
            <option value="zh-TW">繁体中文</option>
            <option value="en-US">English</option>
          </select>
        </div>
      </div>

      <div className="border-t border-gray-200 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">编辑器</h3>
        <div className="space-y-4">
          <label className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
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
              <label className="block text-sm font-medium text-gray-700 mb-2">自动保存间隔（秒）</label>
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

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">设置</h1>
        <p className="mt-2 text-gray-600">管理您的账号和应用偏好</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* 左侧标签栏 */}
        <Card className="lg:col-span-1">
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
                        : 'text-gray-700 hover:bg-gray-50'
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
        <Card className="lg:col-span-3">
          <div className="p-6">
            {activeTab === 'profile' && renderProfileSettings()}
            {activeTab === 'notifications' && renderNotificationSettings()}
            {activeTab === 'security' && renderSecuritySettings()}
            {activeTab === 'preferences' && renderPreferencesSettings()}

            {/* 保存按钮 */}
            <div className="border-t border-gray-200 mt-6 pt-6">
              <div className="flex items-center justify-end space-x-3">
                <Button variant="outline">取消</Button>
                <Button variant="primary" onClick={handleSave} disabled={isSaving}>
                  <Save className="w-4 h-4 mr-2" />
                  {isSaving ? '保存中...' : '保存更改'}
                </Button>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default SettingsView;
