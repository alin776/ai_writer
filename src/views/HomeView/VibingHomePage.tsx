import { useState, useEffect, useCallback } from 'react';
import { motion } from 'motion/react';
import Screen1Brand from './screens/Screen1Brand';
import Screen2AgentDemo from './screens/Screen2AgentDemo';
import Screen3Pillars from './screens/Screen3Pillars';
import Screen4Comparison from './screens/Screen4Comparison';
import Screen5CTA from './screens/Screen5CTA';
import { IMAGES } from './constants';
import { useReducedMotion } from './useReducedMotion';

interface VibingHomePageProps {
  onNavigateToAuth: () => void;
  onNavigateToSubscription: () => void;
  onNavigateToContact: () => void;
}

const TOTAL_SCREENS = 5;

// 每屏对应的 ARIA 名称
const SCREEN_LABELS = ['品牌介绍', 'Agent 演示', '核心能力', '方案对比', '开始使用'];

// 每屏需要的图片 keys
const SCREEN_IMAGE_KEYS: (keyof typeof IMAGES)[][] = [
  ['shelf'],               // Screen1
  ['desk'],                // Screen2
  ['shelf'],               // Screen3
  ['desk'],                // Screen4
  ['desk'],                // Screen5
];

// 屏幕背景色映射：所有屏均为深色
const isDarkScreen = (_index: number) => true;

export default function VibingHomePage({
  onNavigateToAuth,
  onNavigateToSubscription,
  onNavigateToContact,
}: VibingHomePageProps) {
  const [activeScreen, setActiveScreen] = useState(0);
  const [isScrolling, setIsScrolling] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [loadedScreens, setLoadedScreens] = useState<Set<number>>(new Set([0]));
  const reduced = useReducedMotion();

  const isDark = isDarkScreen(activeScreen);

  // ─── 图片渐进加载：首屏仅加载 shelf，其余按 activeScreen 渐进 ───
  useEffect(() => {
    // 首屏：仅加载 Screen1 所需图片
    const firstScreenUrls = SCREEN_IMAGE_KEYS[0].map((key) => IMAGES[key]);
    let loadedCount = 0;

    firstScreenUrls.forEach((src) => {
      const img = new Image();
      img.src = src;
      const onDone = () => {
        loadedCount++;
        if (loadedCount === firstScreenUrls.length) {
          setTimeout(() => setIsLoading(false), 800);
        }
      };
      img.onload = onDone;
      img.onerror = onDone;
    });
  }, []);

  // 当 activeScreen 变化时，预加载当前屏和相邻屏图片
  useEffect(() => {
    const screensToLoad = [activeScreen - 1, activeScreen, activeScreen + 1].filter(
      (s) => s >= 0 && s < TOTAL_SCREENS && !loadedScreens.has(s)
    );

    if (screensToLoad.length === 0) return;

    const newLoaded = new Set(loadedScreens);
    screensToLoad.forEach((screenIdx) => {
      newLoaded.add(screenIdx);
      SCREEN_IMAGE_KEYS[screenIdx].forEach((key) => {
        const img = new Image();
        img.src = IMAGES[key];
      });
    });
    setLoadedScreens(newLoaded);
  }, [activeScreen]); // eslint-disable-line react-hooks/exhaustive-deps

  // ─── 屏幕切换逻辑 ───
  const goToScreen = useCallback(
    (index: number) => {
      if (isScrolling || index < 0 || index >= TOTAL_SCREENS) return;
      setIsScrolling(true);
      setActiveScreen(index);
      setTimeout(() => setIsScrolling(false), reduced ? 100 : 1200);
    },
    [isScrolling, reduced]
  );

  // ─── 滚轮劫持 ───
  useEffect(() => {
    let touchStartY = 0;

    const handleWheel = (e: WheelEvent) => {
      if (isScrolling || isLoading) return;
      e.preventDefault();

      if (e.deltaY > 0 && activeScreen < TOTAL_SCREENS - 1) {
        goToScreen(activeScreen + 1);
      } else if (e.deltaY < 0 && activeScreen > 0) {
        goToScreen(activeScreen - 1);
      }
    };

    const handleTouchStart = (e: TouchEvent) => {
      touchStartY = e.touches[0].clientY;
    };

    const handleTouchEnd = (e: TouchEvent) => {
      if (isScrolling || isLoading) return;
      const diff = touchStartY - e.changedTouches[0].clientY;

      if (Math.abs(diff) > 50) {
        if (diff > 0 && activeScreen < TOTAL_SCREENS - 1) {
          goToScreen(activeScreen + 1);
        } else if (diff < 0 && activeScreen > 0) {
          goToScreen(activeScreen - 1);
        }
      }
    };

    window.addEventListener('wheel', handleWheel, { passive: false });
    window.addEventListener('touchstart', handleTouchStart, { passive: true });
    window.addEventListener('touchend', handleTouchEnd, { passive: true });

    return () => {
      window.removeEventListener('wheel', handleWheel);
      window.removeEventListener('touchstart', handleTouchStart);
      window.removeEventListener('touchend', handleTouchEnd);
    };
  }, [activeScreen, isScrolling, isLoading, goToScreen]);

  // ─── 键盘导航 ───
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (isScrolling || isLoading) return;

      switch (e.key) {
        case 'ArrowDown':
        case 'ArrowRight':
          e.preventDefault();
          goToScreen(activeScreen + 1);
          break;
        case 'ArrowUp':
        case 'ArrowLeft':
          e.preventDefault();
          goToScreen(activeScreen - 1);
          break;
        case 'Home':
          e.preventDefault();
          goToScreen(0);
          break;
        case 'End':
          e.preventDefault();
          goToScreen(TOTAL_SCREENS - 1);
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [activeScreen, isScrolling, isLoading, goToScreen]);

  // ─── Loading 动画 ───
  if (isLoading) {
    return (
      <div className="fixed inset-0 bg-black flex items-center justify-center z-[100]">
        <motion.div
          initial={{ opacity: 0, scale: reduced ? 1 : 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={reduced ? { duration: 0 } : { duration: 0.6 }}
          className="text-center"
        >
          <motion.div
            className="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-4"
            animate={reduced ? {} : { scale: [1, 1.1, 1], rotate: [0, 180, 360] }}
            transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
          >
            <img src="/logo-icon.svg" alt="文枢AI" className="w-8 h-8" />
          </motion.div>
          <motion.p
            className="text-white text-sm tracking-widest"
            initial={{ opacity: 0 }}
            animate={reduced ? { opacity: 1 } : { opacity: [0.5, 1, 0.5] }}
            transition={reduced ? { duration: 0 } : { duration: 1.5, repeat: Infinity }}
          >
            文枢AI
          </motion.p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="h-screen overflow-hidden bg-[#0f172a]" role="main">
      {/* ─── 浮动导航栏 ─── */}
      <motion.nav
        className="fixed top-4 left-4 right-4 z-50 rounded-2xl backdrop-blur-md"
        animate={{
          backgroundColor: isDark
            ? 'rgba(0, 0, 0, 0.3)'
            : 'rgba(255, 255, 255, 0.7)',
        }}
        transition={{ duration: 0.5 }}
        aria-label="主导航"
      >
        <div className="max-w-7xl mx-auto px-6 lg:px-12">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <motion.div
                className="w-12 h-12 rounded-full flex items-center justify-center"
                animate={{ backgroundColor: isDark ? '#ffffff' : '#000000' }}
                transition={{ duration: 0.5 }}
              >
                <img
                  src="/logo-icon.svg"
                  alt="文枢AI"
                  className="w-9 h-9"
                  style={{ filter: isDark ? 'none' : 'brightness(0) invert(1)' }}
                />
              </motion.div>
              <motion.span
                className="text-base tracking-wider font-medium"
                animate={{ color: isDark ? '#ffffff' : '#000000' }}
                transition={{ duration: 0.5 }}
              >
                文枢AI
              </motion.span>
            </div>

            {/* 导航链接 */}
            <div className="hidden md:flex items-center gap-8">
              {['首页', '订阅', '联系我们'].map((item, index) => (
                <motion.button
                  key={item}
                  onClick={() => {
                    if (index === 0) goToScreen(0);
                    else if (index === 1) onNavigateToSubscription();
                    else if (index === 2) onNavigateToContact();
                  }}
                  className="text-sm tracking-wide transition-colors"
                  animate={{ color: isDark ? '#ffffff' : '#000000' }}
                  whileHover={{ color: isDark ? '#9ca3af' : '#6b7280' }}
                  transition={{ duration: 0.5 }}
                >
                  {item}
                </motion.button>
              ))}
            </div>

            {/* 登录按钮 */}
            <RippleButton onClick={onNavigateToAuth} isDark={isDark} reduced={reduced}>
              登录
            </RippleButton>
          </div>
        </div>
      </motion.nav>

      {/* ─── 侧边章节指示器（桌面端） ─── */}
      <div className="fixed right-6 top-1/2 -translate-y-1/2 z-40 hidden lg:flex flex-col gap-3">
        {Array.from({ length: TOTAL_SCREENS }).map((_, index) => (
          <button
            key={index}
            onClick={() => goToScreen(index)}
            className="group flex items-center gap-2"
            aria-label={`跳转到第 ${index + 1} 屏：${SCREEN_LABELS[index]}`}
          >
            <motion.span
              className="text-[10px] transition-colors opacity-0 group-hover:opacity-100 whitespace-nowrap"
              animate={{ color: isDark ? 'rgba(255,255,255,0.4)' : 'rgba(0,0,0,0.4)' }}
            >
              {String(index + 1).padStart(2, '0')}
            </motion.span>
            <motion.div
              className="h-1.5 rounded-full transition-all duration-300"
              animate={
                activeScreen === index
                  ? {
                      width: 24,
                      backgroundColor: isDark ? '#ffffff' : '#111827',
                    }
                  : {
                      width: 6,
                      backgroundColor: isDark ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.2)',
                    }
              }
              whileHover={
                activeScreen !== index
                  ? { scale: 1.5, backgroundColor: isDark ? 'rgba(255,255,255,0.6)' : 'rgba(0,0,0,0.5)' }
                  : {}
              }
              transition={{ duration: 0.3 }}
            />
          </button>
        ))}
      </div>

      {/* ─── 移动端底部指示器 ─── */}
      <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-40 flex lg:hidden gap-2">
        {Array.from({ length: TOTAL_SCREENS }).map((_, index) => (
          <button
            key={index}
            onClick={() => goToScreen(index)}
            aria-label={`跳转到第 ${index + 1} 屏：${SCREEN_LABELS[index]}`}
            className="p-1"
          >
            <motion.div
              className="rounded-full transition-all duration-300"
              animate={
                activeScreen === index
                  ? {
                      width: 24,
                      height: 8,
                      backgroundColor: isDark ? '#ffffff' : '#111827',
                    }
                  : {
                      width: 8,
                      height: 8,
                      backgroundColor: isDark ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.2)',
                    }
              }
              transition={{ duration: 0.3 }}
            />
          </button>
        ))}
      </div>

      {/* ─── 五屏容器 ─── */}
      <div
        className="h-screen transition-transform ease-in-out"
        style={{
          transform: `translateY(-${activeScreen * 100}vh)`,
          transitionDuration: reduced ? '0ms' : '1200ms',
        }}
      >
        <Screen1Brand isActive={activeScreen === 0} />
        <Screen2AgentDemo isActive={activeScreen === 1} />
        <Screen3Pillars isActive={activeScreen === 2} />
        <Screen4Comparison isActive={activeScreen === 3} />
        <Screen5CTA isActive={activeScreen === 4} onNavigateToAuth={onNavigateToAuth} />
      </div>
    </div>
  );
}

// ─── 水波纹按钮 ───
function RippleButton({
  onClick,
  isDark,
  reduced,
  children,
}: {
  onClick: () => void;
  isDark: boolean;
  reduced: boolean;
  children: React.ReactNode;
}) {
  const [ripples, setRipples] = useState<{ x: number; y: number; id: number }[]>([]);

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const newRipple = { x, y, id: Date.now() };
    if (!reduced) {
      setRipples((prev) => [...prev, newRipple]);
      setTimeout(() => {
        setRipples((prev) => prev.filter((r) => r.id !== newRipple.id));
      }, 600);
    }
    onClick();
  };

  return (
    <motion.button
      onClick={handleClick}
      className={`relative overflow-hidden h-10 px-6 text-sm font-medium border rounded transition-all duration-300 ${
        isDark
          ? 'border-white text-white hover:bg-white hover:text-black'
          : 'border-black text-black hover:bg-black hover:text-white'
      }`}
      whileHover={reduced ? {} : { y: -2, boxShadow: '0 4px 12px rgba(0,0,0,0.15)' }}
      whileTap={{ scale: 0.95 }}
    >
      {children}
      {ripples.map((ripple) => (
        <motion.span
          key={ripple.id}
          className="absolute pointer-events-none rounded-full"
          style={{
            top: ripple.y,
            left: ripple.x,
            backgroundColor: isDark ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.5)',
          }}
          initial={{ width: 0, height: 0, x: '-50%', y: '-50%' }}
          animate={{ width: 200, height: 200, opacity: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
      ))}
    </motion.button>
  );
}
