import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Mail, AlertCircle } from 'lucide-react';
import { Card, Button } from '../../components/common';
import { ToastContainer } from '../../components/ui/Toast';
import { DataService } from '../../services/DataService';
import { useToast } from '../../hooks/useToast';
import { useAuthStore } from '../../store/authStore';

/**
 * ChangeEmailView 组件 - 独立的修改邮箱页面
 */
const ChangeEmailView: React.FC = () => {
  const navigate = useNavigate();
  const { user, setUser } = useAuthStore();
  const { success: showSuccess, error: showError, messages, close } = useToast();

  const [newEmail, setNewEmail] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [isSendingCode, setIsSendingCode] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [codeSent, setCodeSent] = useState(false);
  const [countdown, setCountdown] = useState(0);

  // 用于清理倒计时的 ref
  const countdownTimerRef = useRef<NodeJS.Timeout | null>(null);

  // 组件卸载时清理倒计时
  useEffect(() => {
    return () => {
      if (countdownTimerRef.current) {
        clearInterval(countdownTimerRef.current);
      }
    };
  }, []);

  const handleBack = () => {
    navigate('/settings', { state: { activeTab: 'security' } });
  };

  const handleReset = () => {
    setNewEmail('');
    setVerificationCode('');
    setCodeSent(false);
    setCountdown(0);
    if (countdownTimerRef.current) {
      clearInterval(countdownTimerRef.current);
      countdownTimerRef.current = null;
    }
  };

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

      // 清理之前的倒计时
      if (countdownTimerRef.current) {
        clearInterval(countdownTimerRef.current);
      }

      // 开始倒计时
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
      console.error('发送验证码失败:', error);
      // 后端返回格式为 { detail: "xxx" }
      showError(error?.detail || error?.message || '发送验证码失败，请稍后重试');
    } finally {
      setIsSendingCode(false);
    }
  };

  // 验证并更新邮箱
  const handleVerifyAndUpdate = async () => {
    if (!newEmail.trim()) {
      showError('请输入新邮箱地址');
      return;
    }

    if (!verificationCode.trim()) {
      showError('请输入验证码');
      return;
    }

    setIsVerifying(true);
    try {
      const updatedUser = await DataService.verifyAndUpdateEmail(newEmail, verificationCode);
      setUser(updatedUser);
      showSuccess('邮箱修改成功');

      // 延迟返回，让用户看到成功提示
      setTimeout(() => {
        navigate('/settings', { state: { activeTab: 'security' } });
      }, 1500);
    } catch (error: any) {
      console.error('验证邮箱失败:', error);
      // 后端返回格式为 { detail: "xxx" }
      showError(error?.detail || error?.message || '验证失败，请检查验证码是否正确');
    } finally {
      setIsVerifying(false);
    }
  };

  const inputClassName = "block w-full px-3 py-2 border rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-0 transition-all duration-200 bg-white dark:bg-gray-900 border-gray-300 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-700 dark:focus:border-blue-400 dark:focus:ring-blue-400 hover:border-gray-400 dark:hover:border-gray-500";

  const disabledInputClassName = "block w-full px-3 py-2 border rounded-lg text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 border-gray-200 dark:border-gray-700 cursor-not-allowed";

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
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">修改邮箱</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">更新您的邮箱地址</p>
        </div>

        {/* 邮箱修改表单 */}
        <Card className="!bg-white dark:!bg-gray-900 shadow-none border-gray-100 dark:border-gray-800">
          <div className="p-6 space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">邮箱设置</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">输入新邮箱地址</p>
            </div>

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
              {/* 当前邮箱 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  当前邮箱
                </label>
                <input
                  type="email"
                  value={user?.email || ''}
                  disabled
                  className={disabledInputClassName}
                />
              </div>

              {/* 新邮箱 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  新邮箱 <span className="text-red-500">*</span>
                </label>
                <input
                  type="email"
                  value={newEmail}
                  onChange={(e) => setNewEmail(e.target.value)}
                  placeholder="请输入新的邮箱地址"
                  disabled={codeSent}
                  className={codeSent ? disabledInputClassName : inputClassName}
                />
                {codeSent && (
                  <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                    如需更改邮箱地址，请点击"重置"按钮
                  </p>
                )}
              </div>

              {/* 验证码输入 - 带内嵌发送按钮 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  验证码 <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <input
                    type="text"
                    inputMode="numeric"
                    pattern="[0-9]*"
                    value={verificationCode}
                    onChange={(e) => {
                      // 只允许输入数字
                      const value = e.target.value.replace(/\D/g, '');
                      setVerificationCode(value);
                    }}
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
            <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
              <Button
                variant="outline"
                onClick={handleReset}
                disabled={isSendingCode || isVerifying}
              >
                重置
              </Button>

              <Button
                variant="secondary"
                onClick={handleVerifyAndUpdate}
                disabled={isVerifying || !verificationCode.trim() || !codeSent}
              >
                <Mail className="w-4 h-4 mr-2" />
                {isVerifying ? '验证中...' : '确认修改'}
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

export default ChangeEmailView;
