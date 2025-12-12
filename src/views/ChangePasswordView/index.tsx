import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Lock, AlertCircle, Eye, EyeOff } from 'lucide-react';
import { Card, Button } from '../../components/common';
import { ToastContainer } from '../../components/ui/Toast';
import { DataService } from '../../services/DataService';
import { useToast } from '../../hooks/useToast';

/**
 * ChangePasswordView 组件 - 独立的修改密码页面
 */
const ChangePasswordView: React.FC = () => {
  const navigate = useNavigate();
  const { success: showSuccess, error: showError, messages, close } = useToast();

  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [securityForm, setSecurityForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  // 密码可见性状态
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleBack = () => {
    navigate('/settings', { state: { activeTab: 'security' } });
  };

  const handleReset = () => {
    setSecurityForm({
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
    });
    setShowCurrentPassword(false);
    setShowNewPassword(false);
    setShowConfirmPassword(false);
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

    if (securityForm.newPassword.length < 8) {
      showError('新密码长度至少为 8 位');
      return;
    }

    // 验证密码复杂度：必须包含字母、数字、特殊符号
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
      // 延迟返回，让用户看到成功提示
      setTimeout(() => {
        navigate('/settings', { state: { activeTab: 'security' } });
      }, 1500);
    } catch (error: any) {
      console.error('修改密码失败:', error);
      showError(error?.message || '修改密码失败，请稍后重试');
    } finally {
      setIsChangingPassword(false);
    }
  };

  // 密码输入框样式（隐藏浏览器自带按钮）
  const passwordInputClassName = "block w-full px-3 py-2 pr-10 border rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-0 transition-all duration-200 bg-white dark:bg-gray-900 border-gray-300 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-700 dark:focus:border-blue-400 dark:focus:ring-blue-400 hover:border-gray-400 dark:hover:border-gray-500 [&::-ms-reveal]:hidden [&::-ms-clear]:hidden";

  return (
    <>
      <div className="space-y-6">
        {/* 返回按钮 */}
        <button
          onClick={handleBack}
          className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>返回设置</span>
        </button>

        {/* 页面标题 */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">修改密码</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">更新您的登录密码</p>
        </div>

        {/* 密码修改表单 */}
        <Card className="!bg-white dark:!bg-gray-900 shadow-none border-gray-100 dark:border-gray-800">
          <div className="p-6 space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">密码设置</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">请输入您的当前密码和新密码</p>
            </div>

            {/* 密码要求提示 */}
            <div className="flex items-start gap-3 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
              <AlertCircle className="w-5 h-5 text-blue-500 dark:text-blue-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-blue-800 dark:text-blue-200">密码要求</p>
                <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                  密码长度8-20位，必须包含字母、数字、特殊符号等三种字符
                </p>
              </div>
            </div>

            {/* 表单字段 */}
            <div className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  当前密码 <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <input
                    type={showCurrentPassword ? 'text' : 'password'}
                    value={securityForm.currentPassword}
                    onChange={(e) => setSecurityForm({ ...securityForm, currentPassword: e.target.value })}
                    placeholder="请输入当前密码"
                    className={passwordInputClassName}
                  />
                  <button
                    type="button"
                    onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors"
                    tabIndex={-1}
                  >
                    {showCurrentPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  新密码 <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <input
                    type={showNewPassword ? 'text' : 'password'}
                    value={securityForm.newPassword}
                    onChange={(e) => setSecurityForm({ ...securityForm, newPassword: e.target.value })}
                    placeholder="请输入新密码"
                    className={passwordInputClassName}
                  />
                  <button
                    type="button"
                    onClick={() => setShowNewPassword(!showNewPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors"
                    tabIndex={-1}
                  >
                    {showNewPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  确认新密码 <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <input
                    type={showConfirmPassword ? 'text' : 'password'}
                    value={securityForm.confirmPassword}
                    onChange={(e) => setSecurityForm({ ...securityForm, confirmPassword: e.target.value })}
                    placeholder="请再次输入新密码"
                    className={passwordInputClassName}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors"
                    tabIndex={-1}
                  >
                    {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
            </div>

            {/* 操作按钮 */}
            <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
              <Button
                variant="outline"
                onClick={handleReset}
                disabled={isChangingPassword}
              >
                重置
              </Button>
              <Button
                variant="secondary"
                onClick={handleChangePassword}
                disabled={isChangingPassword}
              >
                <Lock className="w-4 h-4 mr-2" />
                {isChangingPassword ? '更新中...' : '更新密码'}
              </Button>
            </div>
          </div>
        </Card>
      </div>

      {/* Toast 通知容器 */}
      <ToastContainer messages={messages} onClose={close} />
    </>
  );
};

export default ChangePasswordView;
