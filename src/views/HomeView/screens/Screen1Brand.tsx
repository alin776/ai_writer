import { motion } from 'motion/react';
import { ChevronDown } from 'lucide-react';
import { ImageWithFallback } from '@/components/figma/ImageWithFallback';
import { IMAGES } from '../constants';
import { useReducedMotion } from '../useReducedMotion';
import styles from '../VibingHomePage.module.css';

interface Screen1BrandProps {
  isActive: boolean;
}

export default function Screen1Brand({ isActive }: Screen1BrandProps) {
  const reduced = useReducedMotion();

  return (
    <section className="relative h-screen flex flex-col items-center justify-center overflow-hidden bg-black">
      {/* ① 背景图 shelf + 40% 遮罩 */}
      <motion.div
        className="absolute inset-0"
        initial={{ opacity: 0 }}
        animate={isActive ? { opacity: 1 } : { opacity: 0 }}
        transition={reduced ? { duration: 0 } : { duration: 1.2 }}
      >
        <ImageWithFallback
          src={IMAGES.shelf}
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/40" />
      </motion.div>

      {/* ② 径向渐变 */}
      <div
        className="absolute inset-0"
        style={{
          background: 'radial-gradient(ellipse 80% 60% at 50% 40%, rgba(14,165,233,0.08) 0%, transparent 70%)',
        }}
      />

      {/* ③ 噪点纹理 */}
      <div className={`absolute inset-0 ${styles.noiseOverlay}`} />

      {/* ④ 浮动粒子 */}
      {!reduced &&
        [
          { w: 120, h: 120, top: '15%', left: '10%' },
          { w: 80, h: 80, top: '60%', left: '80%' },
          { w: 60, h: 60, top: '30%', left: '70%' },
          { w: 100, h: 100, top: '75%', left: '20%' },
          { w: 50, h: 50, top: '45%', left: '50%' },
        ].map((p, i) => (
          <div
            key={i}
            className={styles.particle}
            style={{ width: p.w, height: p.h, top: p.top, left: p.left }}
          />
        ))}

      {/* ⑤ 装饰大字水印 */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center pointer-events-none select-none"
        initial={reduced ? { opacity: 0 } : { scale: 1.5, opacity: 0 }}
        animate={isActive ? (reduced ? { opacity: 1 } : { scale: 1, opacity: 1 }) : (reduced ? { opacity: 0 } : { scale: 1.5, opacity: 0 })}
        transition={reduced ? { duration: 0 } : { duration: 1.4, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}
      >
        <span className="text-[8rem] lg:text-[16rem] leading-none tracking-tighter font-black text-white/[0.03]">
          VIBE
        </span>
      </motion.div>

      {/* ⑥ 主标题 — 磨砂渐变 */}
      <motion.h1
        className="relative z-10 font-serif font-bold text-center select-none
                   text-[4rem] sm:text-[6rem] md:text-[8rem] lg:text-[12rem] leading-none tracking-tight"
        initial={reduced ? { opacity: 0 } : { scale: 1.3, opacity: 0 }}
        animate={isActive ? (reduced ? { opacity: 1 } : { scale: 1, opacity: 1 }) : (reduced ? { opacity: 0 } : { scale: 1.3, opacity: 0 })}
        transition={reduced ? { duration: 0 } : { duration: 1.2, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
      >
        <span
          className="bg-clip-text text-transparent"
          style={{
            backgroundImage: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.6) 50%, rgba(148,163,184,0.6) 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            filter: 'drop-shadow(0 0 40px rgba(255,255,255,0.1))',
          }}
        >
          VIBE WRITING
        </span>
      </motion.h1>

      {/* ⑦ 副标题 */}
      <motion.p
        className="relative z-10 font-shufa text-white/70 text-center mt-4
                   text-xl sm:text-2xl lg:text-3xl"
        initial={{ opacity: 0, y: reduced ? 0 : 20 }}
        animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: reduced ? 0 : 20 }}
        transition={reduced ? { duration: 0 } : { duration: 0.8, delay: 0.7, ease: 'easeOut' }}
      >
        你负责灵魂，Agent 负责落笔
      </motion.p>

      {/* ⑧ 底部滚动指示 */}
      <motion.div
        className="absolute bottom-12 left-1/2 -translate-x-1/2 z-20 flex flex-col items-center gap-2"
        initial={{ opacity: 0 }}
        animate={isActive ? { opacity: 1 } : { opacity: 0 }}
        transition={reduced ? { duration: 0 } : { duration: 0.8, delay: 1.1 }}
      >
        <motion.div
          animate={reduced ? {} : { y: [0, 8, 0] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
        >
          <ChevronDown className="w-5 h-5 text-white/40" />
        </motion.div>
      </motion.div>
    </section>
  );
}
