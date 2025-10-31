import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { DataService } from '../../services/DataService';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Button } from '../../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { ImageWithFallback } from '../../components/common/ImageWithFallback';
import { BookOpen, Feather, Sparkles, ChevronRight, CheckCircle } from 'lucide-react';

/**
 * AuthView 组件 - 统一的登录/注册页面
 * 基于 Figma 设计，左右分栏布局，使用 Tab 切换
 */
const AuthView: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuthStore();

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
    password: '',
    confirmPassword: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState(registerSuccess?.message || '');

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

  // 清除成功消息（5秒后）
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => {
        setSuccessMessage('');
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  /**
   * 登录表单验证
   */
  const validateLogin = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!loginForm.username) {
      newErrors.username = '请输入用户名';
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

    if (!registerForm.password) {
      newErrors.password = '请输入密码';
    } else if (registerForm.password.length < 6) {
      newErrors.password = '密码至少需要 6 个字符';
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
   * 处理登录
   */
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateLogin()) return;

    setIsLoading(true);

    try {
      // 第一步：获取 Token
      const tokenResponse = await DataService.login({
        username: loginForm.username,
        password: loginForm.password,
      });

      console.log('[AuthView] Token response:', tokenResponse);

      // 登录成功 - authStore 会自动持久化 token
      login(null as any, tokenResponse.accessToken);  // 先存token，再获取用户信息

      // 第二步：获取用户信息
      const user = await DataService.getCurrentUser();
      console.log('[AuthView] User info:', user);

      // 更新用户信息
      login(user, tokenResponse.accessToken);
      navigate('/works');
    } catch (error) {
      setErrors({ submit: '登录失败，请检查用户名和密码' });
    } finally {
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
        password: registerForm.password,
      });

      // 注册成功，切换到登录 Tab 并显示成功消息
      setSuccessMessage('注册成功！请使用您的账号登录。');
      setLoginForm({ username: registerForm.username, password: '' });
      setActiveTab('login');

      // 清空注册表单
      setRegisterForm({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      });
    } catch (error) {
      setErrors({ submit: '注册失败，请稍后重试' });
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
              <BookOpen className="w-6 h-6 text-white drop-shadow-lg" />
            </div>
            <span className="text-white tracking-wide drop-shadow-lg">AI Writer</span>
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
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <span className="text-gray-800 tracking-wide">AI Writer</span>
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
              <TabsTrigger value="login" className="data-[state=active]:bg-gray-900 data-[state=active]:text-white">
                登录
              </TabsTrigger>
              <TabsTrigger value="register" className="data-[state=active]:bg-gray-900 data-[state=active]:text-white">
                注册
              </TabsTrigger>
            </TabsList>

            {/* 登录表单 */}
            <TabsContent value="login" className="space-y-6">
              <form onSubmit={handleLogin} className="space-y-5">
                <div className="space-y-2 group">
                  <Label htmlFor="login-username" className="text-gray-700">用户名</Label>
                  <Input
                    id="login-username"
                    type="text"
                    placeholder="请输入用户名"
                    className="h-12 bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200"
                    value={loginForm.username}
                    onChange={(e) => {
                      setLoginForm({ ...loginForm, username: e.target.value });
                      if (errors.username) setErrors({ ...errors, username: '' });
                    }}
                  />
                  {errors.username && <span className="text-sm text-red-500">{errors.username}</span>}
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="login-password" className="text-gray-700">密码</Label>
                    <a href="#" className="text-sm text-gray-700 hover:text-gray-900 transition-colors flex items-center gap-1 group">
                      忘记密码
                      <ChevronRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
                    </a>
                  </div>
                  <Input
                    id="login-password"
                    type="password"
                    placeholder="请输入密码"
                    className="h-12 bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200"
                    value={loginForm.password}
                    onChange={(e) => {
                      setLoginForm({ ...loginForm, password: e.target.value });
                      if (errors.password) setErrors({ ...errors, password: '' });
                    }}
                  />
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
                  <Label htmlFor="register-username" className="text-gray-700">用户名</Label>
                  <Input
                    id="register-username"
                    type="text"
                    placeholder="设置你的用户名"
                    className="h-11 bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200"
                    value={registerForm.username}
                    onChange={(e) => {
                      setRegisterForm({ ...registerForm, username: e.target.value });
                      if (errors.username) setErrors({ ...errors, username: '' });
                    }}
                  />
                  {errors.username && <span className="text-sm text-red-500">{errors.username}</span>}
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="register-email" className="text-gray-700">邮箱地址</Label>
                  <Input
                    id="register-email"
                    type="email"
                    placeholder="your@email.com"
                    className="h-11 bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200"
                    value={registerForm.email}
                    onChange={(e) => {
                      setRegisterForm({ ...registerForm, email: e.target.value });
                      if (errors.email) setErrors({ ...errors, email: '' });
                    }}
                  />
                  {errors.email && <span className="text-sm text-red-500">{errors.email}</span>}
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="register-password" className="text-gray-700">密码</Label>
                  <Input
                    id="register-password"
                    type="password"
                    placeholder="至少6个字符"
                    className="h-11 bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200"
                    value={registerForm.password}
                    onChange={(e) => {
                      setRegisterForm({ ...registerForm, password: e.target.value });
                      if (errors.password) setErrors({ ...errors, password: '' });
                    }}
                  />
                  {errors.password && <span className="text-sm text-red-500">{errors.password}</span>}
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="register-confirm-password" className="text-gray-700">确认密码</Label>
                  <Input
                    id="register-confirm-password"
                    type="password"
                    placeholder="再次输入密码"
                    className="h-11 bg-white border-gray-200 focus:border-gray-900 focus:ring-gray-900/20 transition-all duration-200"
                    value={registerForm.confirmPassword}
                    onChange={(e) => {
                      setRegisterForm({ ...registerForm, confirmPassword: e.target.value });
                      if (errors.confirmPassword) setErrors({ ...errors, confirmPassword: '' });
                    }}
                  />
                  {errors.confirmPassword && <span className="text-sm text-red-500">{errors.confirmPassword}</span>}
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
                    <a href="#" className="text-gray-900 hover:text-gray-700 mx-1 underline underline-offset-2">
                      服务条款
                    </a>
                    和
                    <a href="#" className="text-gray-900 hover:text-gray-700 mx-1 underline underline-offset-2">
                      隐私政策
                    </a>
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
              © 2025 AI Writer · 让创作更简单
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthView;
