import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { DataService } from '../../services/DataService';
import { Input } from '../../components/ui/input';
import { Button } from '../../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { ImageWithFallback } from '../../components/common/ImageWithFallback';
import { BookOpen, Feather, Sparkles, ChevronRight, CheckCircle, Eye, EyeOff } from 'lucide-react';
import { ApiAdapter } from '@/services/ApiAdapter';

// 创建API实例
const api = new ApiAdapter();

/**
 * AuthView 组件 - 统一的登录/注册页面
 * 基于 Figma 设计，左右分栏布局，使用 Tab 切换
 */
const AuthView: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated } = useAuthStore();
  const useMock = import.meta.env.VITE_USE_MOCK === 'true';

  // 获取注册页面传递的状态
  const registerSuccess = location.state as { message?: string; username?: string } | null;

  // 默认 Tab，如果来自注册成功则显示登录
  const [activeTab, setActiveTab] = useState<'login' | 'register'>('login');

  const [loginForm, setLoginForm] = useState({
    username: registerSuccess?.username || '',
    password: ''
  });

  const [registerForm, setRegisterForm] = useState({
    username: '',
    email: '',
    emailVerificationCode: '',
    password: '',
    confirmPassword: '',
    invitationCode: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [isSendingCode, setIsSendingCode] = useState(false);
  const [successMessage, setSuccessMessage] = useState(registerSuccess?.message || '');
  const loginInFlight = useRef(false);
  const [emailVerificationCountdown, setEmailVerificationCountdown] = useState(0);
  const [isEmailVerified, setIsEmailVerified] = useState(false);
  const [showLoginPassword, setShowLoginPassword] = useState(false);
  const [showRegisterPassword, setShowRegisterPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // 打字机效果
  const [typewriterText, setTypewriterText] = useState('');
  const fullText = '开启你的创作之旅';

  useEffect(() => {
    let index = 0;
    const timer = setInterval(() => {
      if (index <= fullText.length) {
        setTypewriterText(fullText.slice(0, index));
        index++;
      } else {
        clearInterval(timer);
      }
    }, 150);

    return () => clearInterval(timer);
  }, []);

  // 从URL参数读取邀请码
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const code = params.get('invitation_code') || params.get('code');
    if (code) {
      setRegisterForm(prev => ({ ...prev, invitationCode: code.toUpperCase() }));
      setActiveTab('register');
    }
  }, [location.search]);

  // 清除成功消息（5秒后）
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => {
        setSuccessMessage('');
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  // Mock 模式下自动登录，避免阻塞在登录页
  useEffect(() => {
    if (!useMock || isAuthenticated) return;

    const run = async () => {
      setIsLoading(true);
      try {
        const tokenResponse = await DataService.login({
          username: 'mock@example.com',
          password: '123456',
        });
        const user = await DataService.getCurrentUser();
        const token =
          (tokenResponse as any)?.accessToken ||
          (tokenResponse as any)?.access_token ||
          'mock-token';
        const refreshToken =
          (tokenResponse as any)?.refreshToken ||
          (tokenResponse as any)?.refresh_token ||
          null;
        login(user, token, refreshToken);
        navigate('/works', { replace: true });
      } catch (error) {
        console.error('[AuthView] Mock 自动登录失败', error);
        setErrors({ submit: 'Mock 自动登录失败，请手动输入 mock@example.com / 123456 重试' });
      } finally {
        setIsLoading(false);
      }
    };

    run();
  }, [useMock, isAuthenticated, login, navigate]);

  /**
   * 登录表单验证
   */
  const validateLogin = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!loginForm.username) {
      newErrors.username = '请输入邮箱或用户名';
    }

    if (!loginForm.password) {
      newErrors.password = '请输入密码';
    } else if (loginForm.password.length < 6) {
      newErrors.password = '密码至少需要 6 个字符';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * 注册表单验证
   */
  const validateRegister = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!registerForm.username) {
      newErrors.username = '请输入用户名';
    } else if (registerForm.username.length < 3) {
      newErrors.username = '用户名至少需要 3 个字符';
    }

    if (!registerForm.email) {
      newErrors.email = '请输入邮箱地址';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.email)) {
      newErrors.email = '请输入有效的邮箱地址';
    }

    if (!registerForm.emailVerificationCode) {
      newErrors.emailVerificationCode = '请输入邮箱验证码';
    } else if (registerForm.emailVerificationCode.length !== 6) {
      newErrors.emailVerificationCode = '验证码为6位数字';
    }

    if (!registerForm.invitationCode) {
      newErrors.invitationCode = '请输入邀请码';
    } else if (registerForm.invitationCode.length !== 8) {
      newErrors.invitationCode = '邀请码必须是 8 位字符';
    }

    if (!registerForm.password) {
      newErrors.password = '请输入密码';
    } else if (registerForm.password.length < 8) {
      newErrors.password = '密码长度至少为 8 位';
    } else if (registerForm.password.length > 20) {
      newErrors.password = '密码长度不能超过 20 位';
    } else {
      // 验证密码复杂度
      const hasLetter = /[a-zA-Z]/.test(registerForm.password);
      const hasNumber = /\d/.test(registerForm.password);
      const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(registerForm.password);
      if (!hasLetter || !hasNumber || !hasSpecial) {
        newErrors.password = '密码必须包含字母、数字、特殊符号三种字符';
      }
    }

    if (!registerForm.confirmPassword) {
      newErrors.confirmPassword = '请确认密码';
    } else if (registerForm.password !== registerForm.confirmPassword) {
      newErrors.confirmPassword = '两次输入的密码不一致';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * 发送邮箱验证码
   */
  const handleSendEmailVerification = async () => {
    // 验证邮箱格式
    if (!registerForm.email) {
      setErrors({ ...errors, email: '请输入邮箱地址' });
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.email)) {
      setErrors({ ...errors, email: '请输入有效的邮箱地址' });
      return;
    }

    if (emailVerificationCountdown > 0) return;

    setIsSendingCode(true);
    setErrors({});

    try {
      await api.post('/auth/send-email-verification', {
        email: registerForm.email
      });

      // 开始倒计时
      setEmailVerificationCountdown(60);
      const timer = setInterval(() => {
        setEmailVerificationCountdown(prev => {
          if (prev <= 1) {
            clearInterval(timer);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      setSuccessMessage('验证码已发送到您的邮箱');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error: any) {
      const errorMessage = error?.response?.data?.detail || error?.message || '发送验证码失败';
      setErrors({ email: errorMessage });
    } finally {
      setIsSendingCode(false);
    }
  };

  /**
   * 验证邮箱验证码
   */
  const handleVerifyEmailCode = async (code?: string) => {
    const verificationCode = (code ?? registerForm.emailVerificationCode).trim();
    if (!verificationCode) {
      setErrors({ ...errors, emailVerificationCode: '请输入验证码' });
      return;
    }

    if (verificationCode.length !== 6) {
      setErrors({ ...errors, emailVerificationCode: '验证码为6位数字' });
      return;
    }

    setIsSendingCode(true);
    setErrors({});

    try {
      await api.post('/auth/verify-email', {
        email: registerForm.email,
        code: verificationCode
      });

      setIsEmailVerified(true);
      setSuccessMessage('邮箱验证成功');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error: any) {
      const errorMessage = error?.response?.data?.detail || error?.message || '验证码错误';
      setErrors({ emailVerificationCode: errorMessage });
    } finally {
      setIsSendingCode(false);
    }
  };

  /**
   * 处理登录
   */
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    // 避免重复提交导致二次请求
    if (isLoading || loginInFlight.current) return;
    loginInFlight.current = true;

    if (!validateLogin()) return;

    setIsLoading(true);

    try {
      // 第一步：获取 Token
      const tokenResponse = await DataService.login({
        username: loginForm.username,
        password: loginForm.password,
      });

      console.log('[AuthView] Token response:', tokenResponse);
      const accessToken =
        (tokenResponse as any)?.accessToken ||
        (tokenResponse as any)?.access_token ||
        (tokenResponse as any)?.token ||
        '';
      const refreshToken =
        (tokenResponse as any)?.refreshToken ||
        (tokenResponse as any)?.refresh_token ||
        null;
      if (!accessToken) {
        throw new Error('Missing access token');
      }

      // 登录成功 - authStore 会自动持久化 token
      login(null as any, accessToken, refreshToken);  // 先存token，再获取用户信息

      // 第二步：获取用户信息
      const user = await DataService.getCurrentUser();
      console.log('[AuthView] User info:', user);

      // 更新用户信息
      login(user, accessToken, refreshToken);
      navigate('/works');
    } catch (error: any) {
      const errorMessage = error?.response?.data?.detail || error?.message || '登录失败，请检查用户名和密码';
      setErrors({ submit: errorMessage });
    } finally {
      loginInFlight.current = false;
      setIsLoading(false);
    }
  };

  /**
   * 处理注册
   */
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateRegister()) return;

    setIsLoading(true);

    try {
      // 调用 DataService 注册
      await DataService.register({
        username: registerForm.username,
        email: registerForm.email,
        email_verification_code: registerForm.emailVerificationCode,
        password: registerForm.password,
        invitation_code: registerForm.invitationCode
      });

      // 注册成功，切换到登录 Tab 并显示成功消息
      setSuccessMessage('注册成功！请使用您的账号登录。');
      setLoginForm({ username: registerForm.username, password: '' });
      setActiveTab('login');

      // 清空注册表单
      setRegisterForm({
        username: '',
        email: '',
        emailVerificationCode: '',
        password: '',
        confirmPassword: '',
        invitationCode: ''
      });
      setIsEmailVerified(false);
      setEmailVerificationCountdown(0);
    } catch (error: any) {
      const errorMessage = error?.response?.data?.detail || error?.message || '注册失败，请稍后重试';
      setErrors({ submit: errorMessage });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex relative overflow-hidden">
      {/* 左侧图片区域 */}
      <div className="hidden lg:flex lg:w-[45%] relative bg-gray-900">
        <ImageWithFallback
          src="https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1200&q=80"
          alt="Background"
          className="w-full h-full object-cover"
        />

        {/* 底部渐变遮罩，只覆盖底部30% */}
        <div className="absolute bottom-0 left-0 right-0 h-[30%] bg-gradient-to-t from-black/50 to-transparent"></div>

        {/* 曲线边缘 */}
        <div className="absolute right-0 top-0 bottom-0 w-16">
          <svg className="absolute right-0 w-16 h-full" preserveAspectRatio="none" viewBox="0 0 100 100">
            <path d="M0,0 Q50,50 0,100 L100,100 L100,0 Z" fill="white" />
          </svg>
        </div>

        {/* 浮动装饰元素 */}
        <div className="absolute top-20 left-12 animate-float">
          <Feather className="w-8 h-8 text-white/30" />
        </div>
        <div className="absolute top-1/3 right-24 animate-float" style={{ animationDelay: '1s' }}>
          <BookOpen className="w-10 h-10 text-white/20" />
        </div>
        <div className="absolute bottom-32 left-20 animate-float" style={{ animationDelay: '2s' }}>
          <Sparkles className="w-6 h-6 text-white/25" />
        </div>

        {/* 左侧内容 */}
        <div className="absolute inset-0 flex flex-col justify-between p-12 z-10">
          {/* Logo */}
          <div className="flex items-center gap-3 animate-fade-in">
            <div className="w-12 h-12 bg-black/30 backdrop-blur-md rounded-xl flex items-center justify-center border border-white/20 shadow-lg">
              <img src="/logo.svg" alt="文枢AI" style={{ width: '48px', height: '48px', filter: 'brightness(0) invert(1)' }} />
            </div>
            <span className="text-white tracking-wide drop-shadow-lg">文枢AI</span>
          </div>

          {/* 中间文字 */}
          <div className="space-y-6 animate-fade-in-up">
            <div className="space-y-4">
              <h2 className="text-white leading-tight drop-shadow-lg text-4xl font-bold">
                AI辅助小说创作平台
              </h2>
              <div className="h-8 flex items-center">
                <p className="text-white drop-shadow-lg text-xl">
                  {typewriterText}
                  <span className="inline-block w-0.5 h-5 bg-white ml-1 animate-pulse"></span>
                </p>
              </div>
            </div>

            <div className="flex gap-8 text-white">
              <div className="flex items-center gap-2 bg-black/20 backdrop-blur-sm px-3 py-2 rounded-lg">
                <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
                  <Sparkles className="w-4 h-4" />
                </div>
                <span className="text-sm drop-shadow">AI智能辅助</span>
              </div>
              <div className="flex items-center gap-2 bg-black/20 backdrop-blur-sm px-3 py-2 rounded-lg">
                <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
                  <Feather className="w-4 h-4" />
                </div>
                <span className="text-sm drop-shadow">自由创作</span>
              </div>
            </div>
          </div>

          {/* 底部引用 */}
          <div className="border-l-2 border-white/40 pl-4 animate-fade-in text-white italic bg-black/30 backdrop-blur-md rounded-lg px-4 py-3 text-[16px] max-w-[85%]">
            <span className="drop-shadow">"写作是对孤独的一种征服"</span>
            <span className="block mt-1 not-italic text-sm text-white/80 drop-shadow">— 雨果</span>
          </div>
        </div>
      </div>

      {/* 右侧表单区域 */}
      <div className="w-full lg:w-[55%] flex items-center justify-center p-8 lg:p-12 bg-white relative">
        {/* 装饰性背景元素 */}
        <div className="absolute top-0 right-0 w-72 h-72 bg-gray-100/40 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-gray-50/30 rounded-full blur-3xl"></div>

        <div className="w-full max-w-md relative z-10 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
          {/* 移动端Logo */}
          <div className="lg:hidden flex items-center gap-3 mb-8">
            <div className="w-12 h-12 bg-gray-900 rounded-xl flex items-center justify-center">
              <img src="/logo.svg" alt="文枢AI" style={{ width: '48px', height: '48px', filter: 'brightness(0) invert(1)' }} />
            </div>
            <span className="text-gray-800 tracking-wide">文枢AI</span>
          </div>

          <div className="mb-10">
            <h1 className="text-gray-900 mb-2 text-3xl font-bold">
              欢迎回来
            </h1>
            <p className="text-gray-600">继续你的创作故事</p>
          </div>

          {/* 注册成功提示 */}
          {successMessage && (
            <div className="flex items-center gap-2 px-4 py-3 mb-6 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
              <CheckCircle size={18} />
              <span>{successMessage}</span>
            </div>
          )}

          <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as 'login' | 'register')} className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-8 bg-white shadow-sm border border-gray-200">
              <TabsTrigger value="login" className="data-[state=active]:!bg-gray-900 data-[state=active]:text-white">
                登录
              </TabsTrigger>
              <TabsTrigger value="register" className="data-[state=active]:!bg-gray-900 data-[state=active]:text-white">
                注册
              </TabsTrigger>
            </TabsList>

            {/* 登录表单 */}
            <TabsContent value="login" className="space-y-6">
              <form onSubmit={handleLogin} className="space-y-5">
                <div className="space-y-2 group">
                  <Input
                    id="login-username"
                    type="text"
                    placeholder="请输入邮箱或用户名"
                    className="h-12 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 text-gray-900"
                    value={loginForm.username}
                    onChange={(e) => {
                      setLoginForm({ ...loginForm, username: e.target.value });
                      if (errors.username) setErrors({ ...errors, username: '' });
                    }}
                  />
                  {errors.username && <span className="text-sm text-red-500">{errors.username}</span>}
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-end mb-1">
                    <Link to="/forgot-password" className="text-sm text-gray-700 hover:text-gray-900 transition-colors flex items-center gap-1 group">
                      忘记密码
                      <ChevronRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
                    </Link>
                  </div>
                  <div className="relative">
                    <Input
                      id="login-password"
                      type={showLoginPassword ? "text" : "password"}
                      placeholder="请输入密码"
                      className="h-12 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 text-gray-900 pr-10"
                      value={loginForm.password}
                      onChange={(e) => {
                        setLoginForm({ ...loginForm, password: e.target.value });
                        if (errors.password) setErrors({ ...errors, password: '' });
                      }}
                    />
                    <button
                      type="button"
                      onClick={() => setShowLoginPassword(!showLoginPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
                    >
                      {showLoginPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                  {errors.password && <span className="text-sm text-red-500">{errors.password}</span>}
                </div>

                <div className="flex items-center">
                  <input
                    id="remember-me"
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-gray-900 focus:ring-gray-900 cursor-pointer"
                  />
                  <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700 cursor-pointer">
                    记住登录状态
                  </label>
                </div>

                {/* 提交错误提示 */}
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
                  {isLoading ? '登录中...' : '登录账户'}
                </Button>
              </form>
            </TabsContent>

            {/* 注册表单 */}
            <TabsContent value="register" className="space-y-4">
              <form onSubmit={handleRegister} className="space-y-3">
                <div className="space-y-1.5">
                  <Input
                    id="register-username"
                    type="text"
                    placeholder="设置你的用户名"
                    className="h-11 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 text-gray-900"
                    value={registerForm.username}
                    onChange={(e) => {
                      setRegisterForm({ ...registerForm, username: e.target.value });
                      if (errors.username) setErrors({ ...errors, username: '' });
                    }}
                  />
                  {errors.username && <span className="text-sm text-red-500">{errors.username}</span>}
                </div>

                <div className="space-y-1.5">
                  <Input
                    id="register-email"
                    type="email"
                    placeholder="请输入邮箱"
                    className="h-11 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 text-gray-900"
                    value={registerForm.email}
                    onChange={(e) => {
                      setRegisterForm({ ...registerForm, email: e.target.value });
                      if (errors.email) setErrors({ ...errors, email: '' });
                      setIsEmailVerified(false); // 邮箱改变后重置验证状态
                    }}
                  />
                  {errors.email && <span className="text-sm text-red-500">{errors.email}</span>}
                </div>

                <div className="space-y-1.5">
                  <div className="flex gap-2">
                    <Input
                      id="register-email-code"
                      type="text"
                      placeholder="请输入6位验证码"
                      maxLength={6}
                      className="h-11 flex-1 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 font-mono text-gray-900"
                      value={registerForm.emailVerificationCode}
                      onChange={(e) => {
                        const code = e.target.value.replace(/\D/g, '');
                        setRegisterForm({ ...registerForm, emailVerificationCode: code });
                        if (errors.emailVerificationCode) setErrors({ ...errors, emailVerificationCode: '' });

                        // 当输入6位验证码时，自动验证
                        if (code.length === 6) {
                          void handleVerifyEmailCode(code);
                        }
                      }}
                      disabled={!registerForm.email || isEmailVerified}
                    />
                    {!isEmailVerified ? (
                      <Button
                        type="button"
                        onClick={handleSendEmailVerification}
                        disabled={!registerForm.email || emailVerificationCountdown > 0 || isSendingCode}
                        className="h-11 px-6 whitespace-nowrap bg-gray-900 hover:bg-gray-800 text-white shadow-lg shadow-gray-900/20 transition-all duration-200"
                      >
                        {emailVerificationCountdown > 0 ? `${emailVerificationCountdown}秒` : (isSendingCode ? '发送中...' : '发送验证码')}
                      </Button>
                    ) : (
                      <div className="h-11 px-6 flex items-center bg-green-50 border border-green-200 rounded-md text-green-700 text-sm whitespace-nowrap">
                        <CheckCircle className="w-4 h-4 mr-2" />
                        已验证
                      </div>
                    )}
                  </div>
                  {errors.emailVerificationCode && <span className="text-sm text-red-500">{errors.emailVerificationCode}</span>}
                </div>

                <div className="space-y-1.5">
                  <div className="relative">
                    <Input
                      id="register-password"
                      type={showRegisterPassword ? "text" : "password"}
                      placeholder="8-20位，含字母、数字、特殊符号"
                      className="h-11 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 text-gray-900 pr-10"
                      value={registerForm.password}
                      onChange={(e) => {
                        setRegisterForm({ ...registerForm, password: e.target.value });
                        if (errors.password) setErrors({ ...errors, password: '' });
                      }}
                    />
                    <button
                      type="button"
                      onClick={() => setShowRegisterPassword(!showRegisterPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
                    >
                      {showRegisterPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                  {errors.password && <span className="text-sm text-red-500">{errors.password}</span>}
                </div>

                <div className="space-y-1.5">
                  <div className="relative">
                    <Input
                      id="register-confirm-password"
                      type={showConfirmPassword ? "text" : "password"}
                      placeholder="再次输入密码"
                      className="h-11 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 text-gray-900 pr-10"
                      value={registerForm.confirmPassword}
                      onChange={(e) => {
                        setRegisterForm({ ...registerForm, confirmPassword: e.target.value });
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

                <div className="space-y-1.5">
                  <Input
                    id="register-invitation-code"
                    type="text"
                    placeholder="请输入8位邀请码"
                    maxLength={8}
                    className="h-11 !bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200 font-mono uppercase text-gray-900"
                    value={registerForm.invitationCode}
                    onChange={(e) => {
                      setRegisterForm({ ...registerForm, invitationCode: e.target.value.toUpperCase() });
                      if (errors.invitationCode) setErrors({ ...errors, invitationCode: '' });
                    }}
                  />
                  {errors.invitationCode && <span className="text-sm text-red-500">{errors.invitationCode}</span>}
                </div>

                <div className="flex items-start pt-2">
                  <input
                    id="terms"
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-gray-900 focus:ring-gray-900 mt-0.5 cursor-pointer"
                    required
                  />
                  <label htmlFor="terms" className="ml-2 block text-sm text-gray-700 cursor-pointer">
                    我已阅读并同意
                    <Link to="/terms" target="_blank" className="text-gray-900 hover:text-gray-700 mx-1 underline underline-offset-2">
                      服务条款
                    </Link>
                    和
                    <Link to="/privacy" target="_blank" className="text-gray-900 hover:text-gray-700 mx-1 underline underline-offset-2">
                      隐私政策
                    </Link>
                  </label>
                </div>

                {/* 提交错误提示 */}
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
                  {isLoading ? '注册中...' : '创建账户'}
                </Button>
              </form>
            </TabsContent>
          </Tabs>

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

export default AuthView;
