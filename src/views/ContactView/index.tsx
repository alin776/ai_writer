/**
 * 联系我们视图 — 与首页统一磨砂暗色风格
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Mail, MessageSquare, Send } from 'lucide-react';
import { ImageWithFallback } from '@/components/figma/ImageWithFallback';
import { IMAGES } from '../HomeView/constants';
import { sendContactMessage } from '@/api/contact';

const frostedGradient =
  'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.5) 50%, rgba(148,163,184,0.6) 100%)';
const cardBg =
  'linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)';
const inputBg =
  'linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%)';

const ContactView: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const response = await sendContactMessage(formData);

      if (response.success) {
        setSubmitted(true);

        // 3秒后重置表单
        setTimeout(() => {
          setSubmitted(false);
          setFormData({ name: '', email: '', subject: '', message: '' });
        }, 3000);
      } else {
        setError(response.detail || '发送失败，请稍后重试');
      }
    } catch (err: any) {
      console.error('发送联系消息失败:', err);
      setError(
        err.response?.data?.detail ||
          err.message ||
          '发送失败，请稍后重试或直接发送邮件联系我们'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  // TODO(human): 实现提交成功后的反馈 UI
  // 返回一段 JSX，用磨砂玻璃风格展示"消息已发送"状态
  // 可用的设计元素：cardBg, border-white/[0.08], backdrop-blur-md, text-white 等
  const renderSuccessState = () => {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <p className="text-white/60">消息已发送</p>
      </div>
    );
  };

  const inputClasses =
    'w-full px-4 py-3 backdrop-blur-md border border-white/[0.08] rounded-xl text-white placeholder-white/30 focus:outline-none focus:border-white/[0.2] transition-all';

  return (
    <div className="min-h-screen bg-[#0f172a] relative overflow-hidden">
      {/* 背景图 */}
      <div className="fixed inset-0">
        <ImageWithFallback
          src={IMAGES.desk}
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-[#0f172a]/60" />
      </div>

      {/* 装饰大字水印 */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none select-none">
        <span className="text-[6rem] lg:text-[12rem] leading-none tracking-tighter font-black text-white/[0.03]">
          CONTACT
        </span>
      </div>

      {/* 内容层 */}
      <div className="relative z-10">
        {/* 导航栏 */}
        <div className="max-w-7xl mx-auto px-6 lg:px-12 py-5">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-white/50 hover:text-white transition-colors cursor-pointer"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>返回首页</span>
          </button>
        </div>

        {/* 主内容 */}
        <div className="max-w-6xl mx-auto px-6 lg:px-12 pt-8 pb-24">
          {/* 标题 */}
          <div className="text-center mb-14">
            <h1 className="font-serif text-4xl sm:text-5xl lg:text-6xl font-bold mb-5">
              <span
                className="bg-clip-text text-transparent"
                style={{
                  backgroundImage: frostedGradient,
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  filter: 'drop-shadow(0 0 30px rgba(255,255,255,0.08))',
                }}
              >
                联系我们
              </span>
            </h1>
            <p className="text-white/40 max-w-xl mx-auto leading-relaxed">
              有任何问题或建议？我们随时为您服务
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 lg:gap-10">
            {/* 左侧：联系表单 */}
            <div
              className="rounded-2xl p-7 lg:p-8 backdrop-blur-md border border-white/[0.08]"
              style={{ background: cardBg }}
            >
              <h2 className="text-xl font-semibold text-white mb-6">
                发送消息
              </h2>

              {submitted ? (
                renderSuccessState()
              ) : (
                <form onSubmit={handleSubmit} className="space-y-5">
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className={inputClasses}
                    style={{ background: inputBg }}
                    placeholder="请输入您的姓名"
                  />

                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className={inputClasses}
                    style={{ background: inputBg }}
                    placeholder="请输入您的邮箱"
                  />

                  <input
                    type="text"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    required
                    className={inputClasses}
                    style={{ background: inputBg }}
                    placeholder="您想咨询什么？"
                  />

                  <textarea
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    rows={5}
                    className={`${inputClasses} resize-none`}
                    style={{ background: inputBg }}
                    placeholder="请详细描述您的问题或建议..."
                  />

                  {/* 错误提示 */}
                  {error && (
                    <div className="border border-red-500/20 rounded-xl p-4 text-red-400 text-sm backdrop-blur-md bg-red-500/5">
                      {error}
                    </div>
                  )}

                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="group relative w-full h-12 rounded-xl text-base font-medium
                               backdrop-blur-md border border-white/[0.15] cursor-pointer
                               hover:border-white/[0.25] transition-all duration-300 overflow-hidden
                               disabled:opacity-50 disabled:cursor-not-allowed"
                    style={{
                      background:
                        'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.04) 100%)',
                    }}
                  >
                    <span className="relative z-10 flex items-center justify-center gap-2 text-white">
                      {isSubmitting ? (
                        <>
                          <div className="w-4 h-4 border-2 border-white/50 border-t-transparent rounded-full animate-spin" />
                          发送中...
                        </>
                      ) : (
                        <>
                          <Send className="w-4 h-4" />
                          发送消息
                        </>
                      )}
                    </span>
                    {/* hover 光晕 */}
                    <div className="absolute inset-0 bg-gradient-to-r from-sky-500/20 to-emerald-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  </button>
                </form>
              )}
            </div>

            {/* 右侧：联系方式 + 社区 */}
            <div className="space-y-6">
              {/* 联系方式卡片 */}
              <div
                className="rounded-2xl p-7 lg:p-8 backdrop-blur-md border border-white/[0.08]"
                style={{ background: cardBg }}
              >
                <h2 className="text-xl font-semibold text-white mb-6">
                  联系方式
                </h2>
                <div className="space-y-5">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-xl flex items-center justify-center border bg-sky-500/10 border-sky-500/20 flex-shrink-0">
                      <Mail className="w-5 h-5 text-sky-400" />
                    </div>
                    <div>
                      <h3 className="font-medium text-white mb-1">邮箱</h3>
                      <p className="text-white/50 text-[15px]">
                        contact@wenshuai.online
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-xl flex items-center justify-center border bg-emerald-500/10 border-emerald-500/20 flex-shrink-0">
                      <MessageSquare className="w-5 h-5 text-emerald-400" />
                    </div>
                    <div>
                      <h3 className="font-medium text-white mb-1">在线客服</h3>
                      <p className="text-white/50 text-[15px]">
                        工作日 9:00 - 18:00
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* 社区卡片 */}
              <div
                className="rounded-2xl p-7 lg:p-8 backdrop-blur-md border border-white/[0.08]"
                style={{ background: cardBg }}
              >
                <h3 className="text-xl font-semibold text-white mb-2">
                  加入我们的社区
                </h3>
                <p className="text-white/40 text-[15px] mb-6 leading-relaxed">
                  关注我们的社交媒体，获取最新资讯和写作技巧
                </p>
                <div className="flex gap-4">
                  {/* 微信 */}
                  <div className="relative group">
                    <button className="w-12 h-12 rounded-xl flex items-center justify-center border border-emerald-500/20 bg-emerald-500/10 hover:bg-emerald-500/20 transition-all cursor-pointer">
                      <svg
                        className="w-6 h-6 text-emerald-400"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                      >
                        <path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 01.213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 00.167-.054l1.903-1.114a.864.864 0 01.717-.098 10.16 10.16 0 002.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348zM5.785 5.991c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 01-1.162 1.178A1.17 1.17 0 014.623 7.17c0-.651.52-1.18 1.162-1.18zm5.813 0c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 01-1.162 1.178 1.17 1.17 0 01-1.162-1.178c0-.651.52-1.18 1.162-1.18zm5.34 2.867c-1.797-.052-3.746.512-5.28 1.786-1.72 1.428-2.687 3.72-1.78 6.22.942 2.453 3.666 4.229 6.884 4.229.826 0 1.622-.12 2.361-.336a.722.722 0 01.598.082l1.584.926a.272.272 0 00.14.045c.134 0 .24-.11.24-.245 0-.06-.023-.12-.038-.177l-.327-1.233a.582.582 0 01-.023-.156.49.49 0 01.201-.398C23.024 18.48 24 16.82 24 14.98c0-3.21-2.931-5.837-6.656-6.088V8.89c-.135-.01-.269-.03-.407-.032zm-2.53 3.274c.535 0 .969.44.969.982a.976.976 0 01-.969.983.976.976 0 01-.969-.983c0-.542.434-.982.97-.982zm4.844 0c.535 0 .969.44.969.982a.976.976 0 01-.969.983.976.976 0 01-.969-.983c0-.542.434-.982.969-.982z" />
                      </svg>
                    </button>
                    {/* 悬停显示的二维码 */}
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-3 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
                      <div
                        className="rounded-xl p-4 backdrop-blur-md border border-white/[0.1]"
                        style={{ background: 'rgba(15, 23, 42, 0.95)' }}
                      >
                        <img
                          src="/images/qrcode/wechat.png"
                          alt="微信二维码"
                          className="w-52 h-52 object-contain rounded-lg"
                        />
                        <p className="text-center text-white/50 text-sm mt-2 whitespace-nowrap">
                          扫码添加微信
                        </p>
                      </div>
                      <div className="absolute left-1/2 -translate-x-1/2 -bottom-2 w-0 h-0 border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent border-t-[rgba(15,23,42,0.95)]" />
                    </div>
                  </div>

                  {/* QQ */}
                  <div className="relative group">
                    <button className="w-12 h-12 rounded-xl flex items-center justify-center border border-sky-500/20 bg-sky-500/10 hover:bg-sky-500/20 transition-all cursor-pointer">
                      <svg
                        className="w-6 h-6 text-sky-400"
                        viewBox="0 0 1024 1024"
                        fill="currentColor"
                      >
                        <path d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm210.5 612.4c-11.5 1.4-44.9-52.7-44.9-52.7 0 31.3-16.2 72.2-51.1 101.8 16.9 5.2 54.9 19.2 45.9 34.4-7.3 12.3-125.6 7.9-160.4 4-34.8 3.9-153.1 8.3-160.4-4-9-15.2 28.9-29.2 45.8-34.4-34.9-29.5-51.1-70.4-51.1-101.8 0 0-33.4 54.1-44.9 52.7-5.4-.7-12.4-29.6 9.4-99.7 10.3-33 22-60.5 40.2-105.8-3.1-116.9 45.3-215 160.4-215 113.9 0 162.5 98.1 160.4 215 18.1 45.2 29.9 72.8 40.2 105.8 21.7 70.1 14.6 99.1 9.3 99.7z" />
                      </svg>
                    </button>
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-3 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
                      <div
                        className="rounded-xl p-4 backdrop-blur-md border border-white/[0.1]"
                        style={{ background: 'rgba(15, 23, 42, 0.95)' }}
                      >
                        <img
                          src="/images/qrcode/qq.jpg"
                          alt="QQ二维码"
                          className="w-52 h-52 object-contain rounded-lg"
                        />
                        <p className="text-center text-white/50 text-sm mt-2 whitespace-nowrap">
                          扫码加入QQ群
                        </p>
                      </div>
                      <div className="absolute left-1/2 -translate-x-1/2 -bottom-2 w-0 h-0 border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent border-t-[rgba(15,23,42,0.95)]" />
                    </div>
                  </div>

                  {/* 小红书 */}
                  <div className="relative group">
                    <button className="w-12 h-12 rounded-xl flex items-center justify-center border border-red-500/20 bg-red-500/10 hover:bg-red-500/20 transition-all cursor-pointer overflow-hidden">
                      <img
                        src="/images/qrcode/xhsLogo.png"
                        alt="小红书"
                        className="w-full h-full object-cover"
                      />
                    </button>
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-3 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
                      <div
                        className="rounded-xl p-4 backdrop-blur-md border border-white/[0.1]"
                        style={{ background: 'rgba(15, 23, 42, 0.95)' }}
                      >
                        <img
                          src="/images/qrcode/xiaohongshu.png"
                          alt="小红书二维码"
                          className="w-52 h-52 object-contain rounded-lg"
                        />
                        <p className="text-center text-white/50 text-sm mt-2 whitespace-nowrap">
                          扫码关注小红书
                        </p>
                      </div>
                      <div className="absolute left-1/2 -translate-x-1/2 -bottom-2 w-0 h-0 border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent border-t-[rgba(15,23,42,0.95)]" />
                    </div>
                  </div>

                  {/* B站 */}
                  <button
                    onClick={() =>
                      window.open(
                        'https://space.bilibili.com/3546898017291150?spm_id_from=333.337.0.0',
                        '_blank'
                      )
                    }
                    className="w-12 h-12 rounded-xl flex items-center justify-center border border-pink-500/20 bg-pink-500/10 hover:bg-pink-500/20 transition-all cursor-pointer"
                  >
                    <svg
                      className="w-6 h-6 text-pink-400"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path d="M17.813 4.653h.854c1.51.054 2.769.578 3.773 1.574 1.004.995 1.524 2.249 1.56 3.76v7.36c-.036 1.51-.556 2.769-1.56 3.773s-2.262 1.524-3.773 1.56H5.333c-1.51-.036-2.769-.556-3.773-1.56S.036 18.858 0 17.347v-7.36c.036-1.511.556-2.765 1.56-3.76 1.004-.996 2.262-1.52 3.773-1.574h.774l-1.174-1.12a1.234 1.234 0 01-.373-.906c0-.356.124-.659.373-.907l.027-.027c.267-.249.573-.373.92-.373.347 0 .653.124.92.373L9.653 4.44c.071.071.134.142.187.213h4.267a.836.836 0 01.16-.213l2.853-2.747c.267-.249.573-.373.92-.373.347 0 .662.151.929.4.267.249.391.551.391.907 0 .355-.124.657-.373.906zM5.333 7.24c-.746.018-1.373.276-1.88.773-.506.498-.769 1.13-.787 1.894v7.52c.018.764.281 1.395.787 1.893.507.498 1.134.756 1.88.773h13.334c.746-.017 1.373-.275 1.88-.773.506-.498.769-1.129.787-1.893v-7.52c-.018-.764-.281-1.396-.787-1.894-.507-.497-1.134-.755-1.88-.773zM8 11.107c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c.017-.391.15-.711.4-.96.249-.249.56-.373.933-.373zm8 0c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c.017-.391.15-.711.4-.96.249-.249.56-.373.933-.373z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactView;
