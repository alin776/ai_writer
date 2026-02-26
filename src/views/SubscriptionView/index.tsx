/**
 * 订阅视图 - 敬请期待页面（与首页统一磨砂暗色风格）
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Clock, Infinity, Cpu, Crown } from 'lucide-react';
import { ImageWithFallback } from '@/components/figma/ImageWithFallback';
import { IMAGES } from '../HomeView/constants';

const features = [
  {
    icon: Infinity,
    title: '无限创作',
    desc: '解锁无限 AI 写作次数，让创作不受限制',
    iconColor: 'text-sky-400',
    containerClass: 'bg-sky-500/10 border-sky-500/20',
    accentColor: 'from-sky-500/20 to-sky-500/0',
  },
  {
    icon: Cpu,
    title: '高级模型',
    desc: '访问最先进的 AI 模型，提升创作质量',
    iconColor: 'text-emerald-400',
    containerClass: 'bg-emerald-500/10 border-emerald-500/20',
    accentColor: 'from-emerald-500/20 to-emerald-500/0',
  },
  {
    icon: Crown,
    title: '专属功能',
    desc: '享受会员专属功能和优先支持服务',
    iconColor: 'text-violet-400',
    containerClass: 'bg-violet-500/10 border-violet-500/20',
    accentColor: 'from-violet-500/20 to-violet-500/0',
  },
];

const frostedGradient = 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.5) 50%, rgba(148,163,184,0.6) 100%)';
const cardBg = 'linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)';

const SubscriptionView: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#0f172a] relative overflow-hidden">
      {/* 背景图 */}
      <div className="absolute inset-0">
        <ImageWithFallback
          src={IMAGES.shelf}
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-[#0f172a]/60" />
      </div>

      {/* 装饰大字水印 */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none select-none">
        <span className="text-[8rem] lg:text-[14rem] leading-none tracking-tighter font-black text-white/[0.03]">
          PREMIUM
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
        <div className="max-w-6xl mx-auto px-6 lg:px-12 pt-12 pb-24">
          {/* 标题 */}
          <div className="text-center mb-16">
            <h1 className="font-serif text-4xl sm:text-5xl lg:text-6xl font-bold mb-6">
              <span
                className="bg-clip-text text-transparent"
                style={{
                  backgroundImage: frostedGradient,
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  filter: 'drop-shadow(0 0 30px rgba(255,255,255,0.08))',
                }}
              >
                会员订阅
              </span>
            </h1>

            {/* 敬请期待徽章 */}
            <div
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full backdrop-blur-md border border-white/[0.1] mb-6"
              style={{ background: cardBg }}
            >
              <Clock className="w-4 h-4 text-sky-400" />
              <span className="text-sm text-white/60 font-medium">敬请期待</span>
            </div>

            <p className="text-white/40 max-w-xl mx-auto leading-relaxed">
              我们正在精心打造会员订阅服务，为您带来更强大的 AI 写作体验。
              即将推出多种订阅计划，满足您的不同需求。
            </p>
          </div>

          {/* 三列特性卡片 */}
          <div className="grid md:grid-cols-3 gap-6 lg:gap-8">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <div
                  key={feature.title}
                  className="group relative rounded-2xl p-7 lg:p-8
                             backdrop-blur-md border border-white/[0.08]
                             transition-all duration-300 overflow-hidden
                             hover:border-white/[0.15]"
                  style={{ background: cardBg }}
                >
                  {/* hover 顶部渐变光 */}
                  <div
                    className={`absolute top-0 left-0 right-0 h-32 bg-gradient-to-b ${feature.accentColor} opacity-0 group-hover:opacity-100 transition-opacity duration-500`}
                  />

                  <div className="relative">
                    <div
                      className={`w-14 h-14 rounded-xl flex items-center justify-center mb-5 border ${feature.containerClass}`}
                    >
                      <Icon className={`w-7 h-7 ${feature.iconColor}`} strokeWidth={1.8} />
                    </div>

                    <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                    <p className="text-white/50 leading-relaxed text-[15px]">{feature.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubscriptionView;
