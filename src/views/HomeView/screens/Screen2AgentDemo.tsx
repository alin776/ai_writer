import { motion } from 'motion/react';
import { useAgentDemoTimeline } from '../agent-demo/useAgentDemoTimeline';
import AgentDemoPlayer from '../agent-demo/AgentDemoPlayer';
import { ImageWithFallback } from '@/components/figma/ImageWithFallback';
import { IMAGES } from '../constants';
import { useReducedMotion } from '../useReducedMotion';
import styles from '../VibingHomePage.module.css';

interface Screen2AgentDemoProps {
  isActive: boolean;
}

export default function Screen2AgentDemo({ isActive }: Screen2AgentDemoProps) {
  const { visibleSteps, checkedIndices, phase } = useAgentDemoTimeline(isActive);
  const reduced = useReducedMotion();

  return (
    <section className="relative h-screen flex flex-col items-center justify-center overflow-hidden bg-black">
      {/* ① 背景图 desk + 60% 遮罩 */}
      <div className="absolute inset-0">
        <ImageWithFallback
          src={IMAGES.desk}
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/60" />
      </div>

      {/* ② 装饰大字水印 */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center pointer-events-none select-none"
        initial={reduced ? { opacity: 0 } : { scale: 1.8, opacity: 0 }}
        animate={isActive ? (reduced ? { opacity: 1 } : { scale: 1, opacity: 1 }) : (reduced ? { opacity: 0 } : { scale: 1.8, opacity: 0 })}
        transition={reduced ? { duration: 0 } : { duration: 1.4, ease: [0.22, 1, 0.36, 1] }}
      >
        <span className="text-[10rem] lg:text-[16rem] leading-none tracking-tighter font-black text-white/[0.03]">
          AGENT
        </span>
      </motion.div>

      {/* ③ 内容层 */}
      <div className="relative z-10 flex flex-col items-center w-full max-w-5xl px-4">
        {/* 标题 — 磨砂渐变 */}
        <motion.h2
          className="font-serif text-3xl sm:text-4xl lg:text-5xl font-bold mb-10"
          initial={{ opacity: 0, y: reduced ? 0 : 20 }}
          animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: reduced ? 0 : 20 }}
          transition={reduced ? { duration: 0 } : { duration: 0.6, delay: 0.2 }}
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
            Agent 实时执行流
          </span>
        </motion.h2>

        {/* Demo 卡片容器 */}
        <motion.div
          className="w-full"
          initial={{ opacity: 0, y: reduced ? 0 : 30 }}
          animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: reduced ? 0 : 30 }}
          transition={reduced ? { duration: 0 } : { duration: 0.7, delay: 0.5 }}
        >
          <div
            className={`backdrop-blur-md border border-white/[0.08] rounded-2xl overflow-hidden ${styles.shadowGlow}`}
            style={{
              background: 'linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)',
              opacity: phase === 'fading' ? 0 : 1,
              transition: phase === 'fading' ? (reduced ? 'none' : 'opacity 800ms ease-out') : 'none',
            }}
          >
            {/* 终端标题栏 */}
            <div className="flex items-center px-4 py-3 border-b border-white/[0.06]">
              <div className="flex gap-2">
                <span className="w-3 h-3 rounded-full bg-[#ff5f57]" />
                <span className="w-3 h-3 rounded-full bg-[#febc2e]" />
                <span className="w-3 h-3 rounded-full bg-[#28c840]" />
              </div>
              <span className="ml-4 text-xs text-white/30 font-mono">agent-execution.log</span>
            </div>
            <AgentDemoPlayer visibleSteps={visibleSteps} checkedIndices={checkedIndices} />
          </div>
        </motion.div>
      </div>
    </section>
  );
}
