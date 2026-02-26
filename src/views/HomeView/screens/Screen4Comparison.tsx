import { motion } from 'motion/react';
import { X, Check, Sparkles } from 'lucide-react';
import { ImageWithFallback } from '@/components/figma/ImageWithFallback';
import { IMAGES } from '../constants';
import { useReducedMotion } from '../useReducedMotion';

interface Screen4ComparisonProps {
  isActive: boolean;
}

interface ComparisonRow {
  label: string;
  traditional: string;
  vibe: string;
}

const rows: ComparisonRow[] = [
  {
    label: '创作模式',
    traditional: '逐段补全，写到后面才发现前后矛盾',
    vibe: 'Agent 先读完设定和大纲，再规划、再落笔',
  },
  {
    label: '世界观记忆',
    traditional: '每次对话都要重新解释你的设定',
    vibe: '知识库记住角色关系和力量体系，跨章保持一致',
  },
  {
    label: '文风适配',
    traditional: '千篇一律，换个提示词还是同一种腔调',
    vibe: '学习你的文风和叙事节奏，生成专属故事',
  },
  {
    label: '质量把控',
    traditional: '产出即终稿，错误直接混入正文',
    vibe: '内建修订卡片，逐章 diff 审核、一键接受或打回',
  },
];

export default function Screen4Comparison({ isActive }: Screen4ComparisonProps) {
  const reduced = useReducedMotion();

  return (
    <section className="relative h-screen flex flex-col items-center justify-center overflow-hidden bg-[#0a0f1a] px-6">
      {/* ① 背景图 */}
      <div className="absolute inset-0">
        <ImageWithFallback
          src={IMAGES.desk}
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/50" />
      </div>

      {/* ② 装饰大字水印 */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center pointer-events-none select-none"
        initial={reduced ? { opacity: 0 } : { scale: 2, opacity: 0 }}
        animate={isActive ? (reduced ? { opacity: 1 } : { scale: 1, opacity: 1 }) : (reduced ? { opacity: 0 } : { scale: 2, opacity: 0 })}
        transition={reduced ? { duration: 0 } : { duration: 1.4, ease: [0.22, 1, 0.36, 1] }}
      >
        <span className="text-[10rem] lg:text-[16rem] leading-none tracking-tighter font-black text-white/[0.03]">
          VS
        </span>
      </motion.div>

      {/* ③ 内容层 */}
      <div className="relative z-10 max-w-6xl w-full">
        {/* 标题 */}
        <motion.div
          className="text-center mb-10 lg:mb-14"
          initial={{ opacity: 0, y: reduced ? 0 : 20 }}
          animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: reduced ? 0 : 20 }}
          transition={reduced ? { duration: 0 } : { duration: 0.8, delay: 0.3 }}
        >
          <h2 className="font-serif text-4xl sm:text-5xl lg:text-6xl font-bold">
            <span
              className="bg-clip-text text-transparent"
              style={{
                backgroundImage: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.5) 50%, rgba(148,163,184,0.6) 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                filter: 'drop-shadow(0 0 30px rgba(255,255,255,0.08))',
              }}
            >
              为什么选择 Vibe Writing？
            </span>
          </h2>
        </motion.div>

        {/* 逐行对比卡片 */}
        <div className="space-y-4">
          {rows.map((row, i) => (
            <motion.div
              key={row.label}
              className="grid md:grid-cols-2 gap-4 items-stretch"
              initial={{ opacity: 0, y: reduced ? 0 : 16 }}
              animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: reduced ? 0 : 16 }}
              transition={reduced ? { duration: 0 } : { duration: 0.5, delay: 0.5 + i * 0.12 }}
            >
              {/* 左：传统 */}
              <div className="rounded-xl p-4 lg:p-5 backdrop-blur-md border border-white/[0.06]"
                style={{ background: 'linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%)' }}
              >
                <div className="flex items-start gap-3">
                  <div className="mt-0.5 flex-shrink-0 w-5 h-5 rounded-full bg-red-500/10 flex items-center justify-center">
                    <X className="w-3 h-3 text-red-400/70" strokeWidth={2.5} />
                  </div>
                  <span className="text-white/35 leading-relaxed text-[15px]">{row.traditional}</span>
                </div>
              </div>

              {/* 右：Vibe */}
              <div className="rounded-xl p-4 lg:p-5 backdrop-blur-md border border-sky-500/[0.15]"
                style={{ background: 'linear-gradient(135deg, rgba(14,165,233,0.06) 0%, rgba(16,185,129,0.03) 100%)' }}
              >
                <div className="flex items-start gap-3">
                  <div className="mt-0.5 flex-shrink-0 w-5 h-5 rounded-full bg-emerald-500/15 flex items-center justify-center">
                    <Check className="w-3 h-3 text-emerald-400" strokeWidth={2.5} />
                  </div>
                  <span className="text-white/80 leading-relaxed text-[15px]">{row.vibe}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
