import { motion } from 'motion/react';
import { ArrowRight } from 'lucide-react';
import { ImageWithFallback } from '@/components/figma/ImageWithFallback';
import { IMAGES } from '../constants';
import { useReducedMotion } from '../useReducedMotion';

interface Screen5CTAProps {
  isActive: boolean;
  onNavigateToAuth: () => void;
}

export default function Screen5CTA({ isActive, onNavigateToAuth }: Screen5CTAProps) {
  const reduced = useReducedMotion();

  return (
    <section className="relative h-screen flex flex-col items-center justify-center overflow-hidden bg-black px-6">
      {/* ① 背景图 */}
      <div className="absolute inset-0">
        <ImageWithFallback
          src={IMAGES.desk}
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/70" />
      </div>

      {/* ② 径向渐变叠加 */}
      <div
        className="absolute inset-0"
        style={{
          background: 'radial-gradient(ellipse 80% 60% at 50% 40%, rgba(14,165,233,0.1) 0%, transparent 70%)',
        }}
      />

      {/* ③ 装饰大字水印 */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center pointer-events-none select-none"
        initial={reduced ? { opacity: 0 } : { scale: 2.5, opacity: 0 }}
        animate={isActive ? (reduced ? { opacity: 1 } : { scale: 1, opacity: 1 }) : (reduced ? { opacity: 0 } : { scale: 2.5, opacity: 0 })}
        transition={reduced ? { duration: 0 } : { duration: 1.6, ease: [0.22, 1, 0.36, 1] }}
      >
        <span className="text-[12rem] lg:text-[20rem] leading-none tracking-tighter font-black text-white/[0.03]">
          GO
        </span>
      </motion.div>

      {/* ④ 内容层 */}
      <div className="relative z-10 max-w-4xl mx-auto text-center">
        {/* 标题 */}
        <motion.h2
          className="font-shufa text-4xl sm:text-5xl lg:text-6xl font-bold text-center mb-6"
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
            开始你的 Vibe Writing
          </span>
        </motion.h2>

        {/* 按钮 */}
        <motion.div
          initial={{ opacity: 0, y: reduced ? 0 : 20 }}
          animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: reduced ? 0 : 20 }}
          transition={reduced ? { duration: 0 } : { duration: 0.6, delay: 1.0 }}
        >
          <button
            onClick={onNavigateToAuth}
            className="group relative h-14 px-12 rounded-xl text-lg font-medium
                       backdrop-blur-md border border-white/[0.15] cursor-pointer
                       hover:border-white/[0.25] transition-all duration-300 overflow-hidden"
            style={{
              background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.04) 100%)',
            }}
          >
            <span className="relative z-10 flex items-center gap-2 text-white">
              免费开始创作 <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
            </span>
            {/* hover 光晕 */}
            <div className="absolute inset-0 bg-gradient-to-r from-sky-500/20 to-emerald-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          </button>
        </motion.div>
      </div>

      {/* ⑤ 底部版权 */}
      <motion.div
        className="absolute bottom-8 left-1/2 -translate-x-1/2 w-full max-w-4xl px-6"
        initial={{ opacity: 0 }}
        animate={isActive ? { opacity: 1 } : { opacity: 0 }}
        transition={reduced ? { duration: 0 } : { duration: 0.6, delay: 1.4 }}
      >
        <div className="border-t border-white/[0.06] pt-6 text-center">
          <p className="text-xs text-white/20">© 2026 文枢AI</p>
        </div>
      </motion.div>
    </section>
  );
}
