import { motion } from 'motion/react';
import { Bot, Puzzle, MessagesSquare, type LucideIcon } from 'lucide-react';
import { ImageWithFallback } from '@/components/figma/ImageWithFallback';
import { IMAGES } from '../constants';
import { useReducedMotion } from '../useReducedMotion';

interface Screen3PillarsProps {
  isActive: boolean;
}

interface PillarData {
  icon: LucideIcon;
  title: string;
  desc: string;
  highlights: string[];
  iconColor: string;
  accentColor: string;
  containerClass: string;
}

const pillars: PillarData[] = [
  {
    icon: Bot,
    title: 'Agent 智能创作',
    desc: 'Agent 理解你的故事，规划、探索、落笔',
    highlights: ['自动规划章节结构', '上下文感知写作', '多轮迭代优化'],
    iconColor: 'text-sky-400',
    accentColor: 'from-sky-500/20 to-sky-500/0',
    containerClass: 'bg-sky-500/10 border-sky-500/20',
  },
  {
    icon: Puzzle,
    title: 'Skills 技能扩展',
    desc: '从角色一致性到世界观构建，可自定义技能',
    highlights: ['角色性格一致性', '世界观逻辑校验', '自定义创作技能'],
    iconColor: 'text-emerald-400',
    accentColor: 'from-emerald-500/20 to-emerald-500/0',
    containerClass: 'bg-emerald-500/10 border-emerald-500/20',
  },
  {
    icon: MessagesSquare,
    title: 'Channels 创作社区',
    desc: '和创作者交流灵感、分享作品、互相启发',
    highlights: ['创作者实时交流', '作品互评与启发', '灵感素材共享'],
    iconColor: 'text-violet-400',
    accentColor: 'from-violet-500/20 to-violet-500/0',
    containerClass: 'bg-violet-500/10 border-violet-500/20',
  },
];

export default function Screen3Pillars({ isActive }: Screen3PillarsProps) {
  const reduced = useReducedMotion();

  return (
    <section className="relative h-screen flex flex-col items-center justify-center overflow-hidden bg-[#0f172a] px-6">
      {/* ① 背景图 */}
      <div className="absolute inset-0">
        <ImageWithFallback
          src={IMAGES.shelf}
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-[#0f172a]/50" />
      </div>

      {/* ② 装饰大字水印 */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center pointer-events-none select-none"
        initial={reduced ? { opacity: 0 } : { scale: 2, opacity: 0 }}
        animate={isActive ? (reduced ? { opacity: 1 } : { scale: 1, opacity: 1 }) : (reduced ? { opacity: 0 } : { scale: 2, opacity: 0 })}
        transition={reduced ? { duration: 0 } : { duration: 1.4, ease: [0.22, 1, 0.36, 1] }}
      >
        <span className="text-[10rem] lg:text-[16rem] leading-none tracking-tighter font-black text-white/[0.03]">
          ECOSYSTEM
        </span>
      </motion.div>

      {/* ③ 内容层 */}
      <div className="relative z-10 max-w-6xl w-full">
        {/* 标题 — 磨砂渐变 */}
        <motion.h2
          className="font-serif text-3xl sm:text-4xl lg:text-5xl font-bold text-center mb-14"
          initial={{ opacity: 0, y: reduced ? 0 : 30 }}
          animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: reduced ? 0 : 30 }}
          transition={reduced ? { duration: 0 } : { duration: 0.8, delay: 0.4 }}
        >
          <span
            className="bg-clip-text text-transparent"
            style={{
              backgroundImage: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.5) 50%, rgba(148,163,184,0.6) 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              filter: 'drop-shadow(0 0 30px rgba(255,255,255,0.08))',
            }}
          >
            不只是 AI 写作，是完整的创作生态
          </span>
        </motion.h2>

        {/* 三列卡片 */}
        <div className="grid md:grid-cols-3 gap-6 lg:gap-8">
          {pillars.map((pillar, index) => {
            const Icon = pillar.icon;

            return (
              <motion.div
                key={pillar.title}
                className="group relative rounded-2xl p-7 lg:p-8 cursor-pointer
                           backdrop-blur-md border border-white/[0.08]
                           transition-all duration-300 overflow-hidden
                           hover:border-white/[0.15]"
                style={{
                  background: 'linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)',
                }}
                initial={{ opacity: 0, y: reduced ? 0 : 40 }}
                animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: reduced ? 0 : 40 }}
                transition={reduced ? { duration: 0 } : { duration: 0.6, delay: 0.6 + index * 0.15 }}
              >
                {/* 顶部渐变光 — hover 时增强 */}
                <div
                  className={`absolute top-0 left-0 right-0 h-32 bg-gradient-to-b ${pillar.accentColor} opacity-0 group-hover:opacity-100 transition-opacity duration-500`}
                />

                <div className="relative">
                  {/* 图标容器 */}
                  <div
                    className={`w-14 h-14 rounded-xl flex items-center justify-center mb-5 border ${pillar.containerClass}`}
                  >
                    <Icon className={`w-7 h-7 ${pillar.iconColor}`} strokeWidth={1.8} />
                  </div>

                  <h3 className="text-xl font-semibold text-white mb-2">{pillar.title}</h3>
                  <p className="text-white/50 leading-relaxed text-[15px] mb-5">{pillar.desc}</p>

                  {/* 特性列表 */}
                  <div className="space-y-2.5">
                    {pillar.highlights.map((h, i) => (
                      <div key={i} className="flex items-center gap-2">
                        <span className={`w-1 h-1 rounded-full flex-shrink-0 ${pillar.iconColor.replace('text-', 'bg-')}`} />
                        <span className="text-white/40 text-sm">{h}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
