import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Input } from '../../components/ui/input';
import { Button } from '../../components/ui/button';
import { ImageWithFallback } from '../../components/common/ImageWithFallback';
import { BookOpen, Feather, Sparkles, ArrowLeft, CheckCircle, Mail, Eye, EyeOff } from 'lucide-react';
import { ApiAdapter } from '@/services/ApiAdapter';

// 创建API实例
const api = new ApiAdapter();

/**
 * ForgotPasswordView 组件 - 忘记密码页面
 * 两步流程：1. 发送验证码 2. 重置密码
 */
const ForgotPasswordView: React.FC = () => {
  const navigate = useNavigate();

  // 当前步骤：'email' | 'reset'
  const [step, setStep] = useState<'email' | 'reset'>('email');

  const [emailForm, setEmailForm] = useState({ email: '' });
  const [resetForm, setResetForm] = useState({
    email: '',
    code: '',
    newPassword: '',
    confirmPassword: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  /**
   * 发送验证码
   */
  const handleSendCode = async (e: React.FormEvent) => {
    e.preventDefault();

    // 验证邮箱
    if (!emailForm.email) {
      setErrors({ email: '请输入邮箱地址' });
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailForm.email)) {
      setErrors({ email: '请输入有效的邮箱地址' });
      return;
    }

    setIsLoading(true);
    setErrors({});

    try {
      await api.post('/auth/forgot-password', {
        email: emailForm.email
      });

      // 发送成功，进入重置步骤
      setResetForm({ ...resetForm, email: emailForm.email });
      setStep('reset');

      // 开始倒计时（60秒）
      setCountdown(60);
      const timer = setInterval(() => {
        setCountdown(prev => {
          if (prev <= 1) {
            clearInterval(timer);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } catch (error: any) {
      const errorMessage = error?.response?.data?.detail || error?.message || '发送验证码失败，请稍后重试';
      setErrors({ submit: errorMessage });
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * 重新发送验证码
   */
  const handleResendCode = async () => {
    if (countdown > 0) return;

    setIsLoading(true);
    setErrors({});

    try {
      await api.post('/auth/forgot-password', {
        email: resetForm.email
      });

      // 重新开始倒计时
      setCountdown(60);
      const timer = setInterval(() => {
        setCountdown(prev => {
          if (prev <= 1) {
            clearInterval(timer);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } catch (error: any) {
      const errorMessage = error?.response?.data?.detail || error?.message || '发送验证码失败，请稍后重试';
      setErrors({ submit: errorMessage });
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * 重置密码表单验证
   */
  const validateResetForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!resetForm.code) {
      newErrors.code = '请输入验证码';
    } else if (resetForm.code.length !== 6) {
      newErrors.code = '验证码为6位数字';
    }

    if (!resetForm.newPassword) {
      newErrors.newPassword = '请输入新密码';
    } else if (resetForm.newPassword.length < 8) {
      newErrors.newPassword = '密码长度至少为 8 位';
    } else if (resetForm.newPassword.length > 20) {
      newErrors.newPassword = '密码长度不能超过 20 位';
    } else {
      // 验证密码复杂度
      const hasLetter = /[a-zA-Z]/.test(resetForm.newPassword);
      const hasNumber = /\d/.test(resetForm.newPassword);
      const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(resetForm.newPassword);
      if (!hasLetter || !hasNumber || !hasSpecial) {
        newErrors.newPassword = '密码必须包含字母、数字、特殊符号三种字符';
      }
    }

    if (!resetForm.confirmPassword) {
      newErrors.confirmPassword = '请确认新密码';
    } else if (resetForm.newPassword !== resetForm.confirmPassword) {
      newErrors.confirmPassword = '两次输入的密码不一致';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * 重置密码
   */
  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateResetForm()) return;

    setIsLoading(true);
    setErrors({});

    try {
      await api.post('/auth/reset-password', {
        email: resetForm.email,
        code: resetForm.code,
        new_password: resetForm.newPassword
      });

      // 重置成功，跳转到登录页
      navigate('/login', {
        state: {
          message: '密码重置成功！请使用新密码登录。',
          username: ''
        }
      });
    } catch (error: any) {
      const errorMessage = error?.response?.data?.detail || error?.message || '密码重置失败，请稍后重试';
      setErrors({ submit: errorMessage });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex relative overflow-hidden">
      {/* 左侧图片区域（与 AuthView 保持一致） */}
      <div className="hidden lg:flex lg:w-[45%] relative bg-gray-900">
        <ImageWithFallback
          src="https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1200&q=80"
          alt="Background"
          className="w-full h-full object-cover"
        />

        <div className="absolute bottom-0 left-0 right-0 h-[30%] bg-gradient-to-t from-black/50 to-transparent"></div>

        <div className="absolute right-0 top-0 bottom-0 w-16">
          <svg className="absolute right-0 w-16 h-full" preserveAspectRatio="none" viewBox="0 0 100 100">
            <path d="M0,0 Q50,50 0,100 L100,100 L100,0 Z" fill="white" />
          </svg>
        </div>

        <div className="absolute top-20 left-12 animate-float">
          <Feather className="w-8 h-8 text-white/30" />
        </div>
        <div className="absolute top-1/3 right-24 animate-float" style={{ animationDelay: '1s' }}>
          <BookOpen className="w-10 h-10 text-white/20" />
        </div>
        <div className="absolute bottom-32 left-20 animate-float" style={{ animationDelay: '2s' }}>
          <Sparkles className="w-6 h-6 text-white/25" />
        </div>

        <div className="absolute inset-0 flex flex-col justify-between p-12 z-10">
          <div className="flex items-center gap-3 animate-fade-in">
            <div className="w-12 h-12 bg-black/30 backdrop-blur-md rounded-xl flex items-center justify-center border border-white/20 shadow-lg">
              <BookOpen className="w-6 h-6 text-white drop-shadow-lg" />
            </div>
            <span className="text-white tracking-wide drop-shadow-lg">文枢AI</span>
          </div>

          <div className="space-y-6 animate-fade-in-up">
            <div className="space-y-4">
              <h2 className="text-white leading-tight drop-shadow-lg text-4xl font-bold">
                重置您的密码
              </h2>
              <p className="text-white drop-shadow-lg text-xl">
                找回账户访问权限
              </p>
            </div>
          </div>

          <div className="border-l-2 border-white/40 pl-4 animate-fade-in text-white italic bg-black/30 backdrop-blur-md rounded-lg px-4 py-3 text-[16px] max-w-[85%]">
            <span className="drop-shadow">"安全永远是第一位的"</span>
          </div>
        </div>
      </div>

      {/* 右侧表单区域 */}
      <div className="w-full lg:w-[55%] flex items-center justify-center p-8 lg:p-12 bg-white relative">
        <div className="absolute top-0 right-0 w-72 h-72 bg-gray-100/40 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-gray-50/30 rounded-full blur-3xl"></div>

        <div className="w-full max-w-md relative z-10 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
          {/* 移动端Logo */}
          <div className="lg:hidden flex items-center gap-3 mb-8">
            <div className="w-12 h-12 bg-gray-900 rounded-xl flex items-center justify-center">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <span className="text-gray-800 tracking-wide">文枢AI</span>
          </div>

          {/* 返回登录链接 */}
          <Link
            to="/login"
            className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors mb-8 group"
          >
            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
            <span>返回登录</span>
          </Link>

          {/* 步骤1: 输入邮箱 */}
          {step === 'email' && (
            <div>
              <div className="mb-10">
                <h1 className="text-gray-900 mb-2 text-3xl font-bold">
                  忘记密码？
                </h1>
                <p className="text-gray-600">请输入您的邮箱地址，我们将发送验证码到您的邮箱</p>
              </div>

              <form onSubmit={handleSendCode} className="space-y-5">
                <div className="space-y-2">
                  <Input
                    id="email"
                    type="email"
                    placeholder="请输入邮箱地址"
                    className="h-12 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 text-gray-900"
                    value={emailForm.email}
                    onChange={(e) => {
                      setEmailForm({ email: e.target.value });
                      if (errors.email) setErrors({ ...errors, email: '' });
                    }}
                  />
                  {errors.email && <span className="text-sm text-red-500">{errors.email}</span>}
                </div>

                {errors.submit && (
                  <div className="text-sm text-red-500 text-center">
                    {errors.submit}
                  </div>
                )}

                <Button
                  type="submit"
                  disabled={isLoading}
                  className="w-full h-12 bg-gray-900 hover:bg-gray-800 text-white shadow-lg shadow-gray-900/20 transition-all duration-200 hover:shadow-xl hover:shadow-gray-900/30 hover:scale-[1.02]"
                >
                  {isLoading ? '发送中...' : '发送验证码'}
                </Button>
              </form>
            </div>
          )}

          {/* 步骤2: 重置密码 */}
          {step === 'reset' && (
            <div>
              <div className="mb-10">
                <h1 className="text-gray-900 mb-2 text-3xl font-bold">
                  重置密码
                </h1>
                <div className="flex items-center gap-2 text-gray-600">
                  <Mail className="w-4 h-4" />
                  <span className="text-sm">验证码已发送到 {resetForm.email}</span>
                </div>
              </div>

              <form onSubmit={handleResetPassword} className="space-y-5">
                <div className="space-y-2">
                  <div className="flex gap-2">
                    <Input
                      id="code"
                      type="text"
                      placeholder="请输入6位验证码"
                      maxLength={6}
                      className="h-12 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 font-mono text-center text-lg tracking-wider text-gray-900"
                      value={resetForm.code}
                      onChange={(e) => {
                        setResetForm({ ...resetForm, code: e.target.value.replace(/\D/g, '') });
                        if (errors.code) setErrors({ ...errors, code: '' });
                      }}
                    />
                    <Button
                      type="button"
                      variant="outline"
                      onClick={handleResendCode}
                      disabled={countdown > 0 || isLoading}
                      className="h-12 px-6 whitespace-nowrap border-gray-200 hover:border-gray-900"
                    >
                      {countdown > 0 ? `${countdown}秒` : '重新发送'}
                    </Button>
                  </div>
                  {errors.code && <span className="text-sm text-red-500">{errors.code}</span>}
                </div>

                <div className="space-y-2">
                  <div className="relative">
                    <Input
                      id="newPassword"
                      type={showNewPassword ? "text" : "password"}
                      placeholder="请输入新密码（8-20位，含字母、数字、特殊符号）"
                      className="h-12 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 text-gray-900 pr-10"
                      value={resetForm.newPassword}
                      onChange={(e) => {
                        setResetForm({ ...resetForm, newPassword: e.target.value });
                        if (errors.newPassword) setErrors({ ...errors, newPassword: '' });
                      }}
                    />
                    <button
                      type="button"
                      onClick={() => setShowNewPassword(!showNewPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
                    >
                      {showNewPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                  {errors.newPassword && <span className="text-sm text-red-500">{errors.newPassword}</span>}
                </div>

                <div className="space-y-2">
                  <div className="relative">
                    <Input
                      id="confirmPassword"
                      type={showConfirmPassword ? "text" : "password"}
                      placeholder="再次输入新密码"
                      className="h-12 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 text-gray-900 pr-10"
                      value={resetForm.confirmPassword}
                      onChange={(e) => {
                        setResetForm({ ...resetForm, confirmPassword: e.target.value });
                        if (errors.confirmPassword) setErrors({ ...errors, confirmPassword: '' });
                      }}
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
                    >
                      {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                  {errors.confirmPassword && <span className="text-sm text-red-500">{errors.confirmPassword}</span>}
                </div>

                {errors.submit && (
                  <div className="text-sm text-red-500 text-center">
                    {errors.submit}
                  </div>
                )}

                <Button
                  type="submit"
                  disabled={isLoading}
                  className="w-full h-12 bg-gray-900 hover:bg-gray-800 text-white shadow-lg shadow-gray-900/20 transition-all duration-200 hover:shadow-xl hover:shadow-gray-900/30 hover:scale-[1.02]"
                >
                  {isLoading ? '重置中...' : '重置密码'}
                </Button>
              </form>
            </div>
          )}

          <div className="mt-10 text-center">
            <p className="text-sm text-gray-500">
              © 2025 文枢AI · 让创作更简单
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ForgotPasswordView;
