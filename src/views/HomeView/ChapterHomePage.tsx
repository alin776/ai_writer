import { useState, useEffect } from "react";
import { motion, useMotionValue, useSpring } from "motion/react";
import { Button } from "@/components/ui/button";
import { ImageWithFallback } from "@/components/figma/ImageWithFallback";
import { BookOpen, ArrowRight, Zap, Users, Pencil, Sparkles, Shield, Target, ChevronDown } from "lucide-react";

export default function ChapterHomePage({ onNavigateToAuth, onNavigateToSubscription, onNavigateToContact }: {
  onNavigateToAuth: () => void;
  onNavigateToSubscription: () => void;
  onNavigateToContact: () => void;
}) {
  const [activeChapter, setActiveChapter] = useState(0);
  const [isScrolling, setIsScrolling] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [imagesLoaded, setImagesLoaded] = useState(false);
  const totalChapters = 5;

  // 鼠标位置追踪
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  const smoothMouseX = useSpring(mouseX, { stiffness: 50, damping: 20 });
  const smoothMouseY = useSpring(mouseY, { stiffness: 50, damping: 20 });

  // 图片预加载
  useEffect(() => {
    const imagesToPreload = [
      "https://images.unsplash.com/photo-1643050079091-1d4a51e07ba0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsaWJyYXJ5JTIwYm9va3MlMjBzaGVsZnxlbnwxfHx8fDE3NjUzNDY2NDd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
      "https://images.unsplash.com/photo-1760840414854-36cd365d14f1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxvcGVuJTIwYm9vayUyMHBhZ2VzJTIwbGlnaHR8ZW58MXx8fHwxNzY1Mzc2MTcxfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
      "https://images.unsplash.com/photo-1763098844247-141e76ea20fb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3cml0aW5nJTIwZGVzayUyMGF0bW9zcGhlcmljfGVufDF8fHx8MTc2NTM3NjE3MXww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
      "https://images.unsplash.com/reserve/LJIZlzHgQ7WPSh5KVTCB_Typewriter.jpg?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aW50YWdlJTIwdHlwZXdyaXRlcnxlbnwxfHx8fDE3NjUzMzM2NDB8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
      "https://images.unsplash.com/photo-1661001032128-507b57ffd046?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwYXBlciUyMHRleHR1cmUlMjBhYnN0cmFjdHxlbnwxfHx8fDE3NjUzNzYxNzZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
    ];

    let loadedCount = 0;
    const totalImages = imagesToPreload.length;

    imagesToPreload.forEach(src => {
      const img = new Image();
      img.src = src;
      img.onload = () => {
        loadedCount++;
        if (loadedCount === totalImages) {
          setImagesLoaded(true);
          setTimeout(() => setIsLoading(false), 800);
        }
      };
      img.onerror = () => {
        loadedCount++;
        if (loadedCount === totalImages) {
          setImagesLoaded(true);
          setTimeout(() => setIsLoading(false), 800);
        }
      };
    });
  }, []);

  // 鼠标移动监听
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      mouseX.set(e.clientX);
      mouseY.set(e.clientY);
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [mouseX, mouseY]);

  // 滚轮劫持
  useEffect(() => {
    let touchStartY = 0;

    const handleWheel = (e: WheelEvent) => {
      if (isScrolling || isLoading) return;
      e.preventDefault();

      if (e.deltaY > 0 && activeChapter < totalChapters - 1) {
        setIsScrolling(true);
        setActiveChapter(prev => prev + 1);
        setTimeout(() => setIsScrolling(false), 1200);
      } else if (e.deltaY < 0 && activeChapter > 0) {
        setIsScrolling(true);
        setActiveChapter(prev => prev - 1);
        setTimeout(() => setIsScrolling(false), 1200);
      }
    };

    const handleTouchStart = (e: TouchEvent) => {
      touchStartY = e.touches[0].clientY;
    };

    const handleTouchEnd = (e: TouchEvent) => {
      if (isScrolling || isLoading) return;
      const touchEndY = e.changedTouches[0].clientY;
      const diff = touchStartY - touchEndY;

      if (Math.abs(diff) > 50) {
        if (diff > 0 && activeChapter < totalChapters - 1) {
          setIsScrolling(true);
          setActiveChapter(prev => prev + 1);
          setTimeout(() => setIsScrolling(false), 1200);
        } else if (diff < 0 && activeChapter > 0) {
          setIsScrolling(true);
          setActiveChapter(prev => prev - 1);
          setTimeout(() => setIsScrolling(false), 1200);
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
  }, [activeChapter, isScrolling, totalChapters, isLoading]);

  // 判断当前章节背景颜色
  const isDarkBackground = activeChapter === 0 || activeChapter === 1 || activeChapter === 3 || activeChapter === 4;

  // 加载动画
  if (isLoading) {
    return (
      <div className="fixed inset-0 bg-black flex items-center justify-center z-[100]">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <motion.div
            className="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-4"
            animate={{
              scale: [1, 1.1, 1],
              rotate: [0, 180, 360]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            <img src="/logo-icon.svg" alt="文枢AI" className="w-8 h-8" />
          </motion.div>
          <motion.p
            className="text-white text-sm tracking-widest"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            文枢AI
          </motion.p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="h-screen overflow-hidden bg-black">
      {/* 导航栏 - 根据背景色改变 */}
      <motion.nav
        className="fixed top-0 left-0 right-0 z-50"
        animate={{
          backgroundColor: 'transparent',
        }}
        transition={{ duration: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-6 lg:px-12">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <motion.div
                className="w-12 h-12 rounded-full flex items-center justify-center"
                animate={{
                  backgroundColor: isDarkBackground ? '#ffffff' : '#000000',
                }}
                transition={{ duration: 0.5 }}
              >
                <img
                  src="/logo-icon.svg"
                  alt="文枢AI"
                  className="w-9 h-9"
                  style={{
                    filter: isDarkBackground ? 'none' : 'brightness(0) invert(1)'
                  }}
                />
              </motion.div>
              <motion.span
                className="text-base tracking-wider font-medium"
                animate={{
                  color: isDarkBackground ? '#ffffff' : '#000000',
                }}
                transition={{ duration: 0.5 }}
              >
                文枢AI
              </motion.span>
            </div>

            <div className="hidden md:flex items-center gap-8">
              {['首页', '订阅', '联系我们'].map((item, index) => (
                <motion.button
                  key={item}
                  onClick={() => {
                    if (index === 0 && !isScrolling) {
                      setIsScrolling(true);
                      setActiveChapter(0);
                      setTimeout(() => setIsScrolling(false), 1200);
                    } else if (index === 1) {
                      onNavigateToSubscription();
                    } else if (index === 2) {
                      onNavigateToContact();
                    }
                  }}
                  className="text-sm tracking-wide transition-colors"
                  animate={{
                    color: isDarkBackground ? '#ffffff' : '#000000',
                  }}
                  whileHover={{
                    color: isDarkBackground ? '#9ca3af' : '#6b7280',
                  }}
                  transition={{ duration: 0.5 }}
                >
                  {item}
                </motion.button>
              ))}
            </div>

            <RippleButton
              onClick={onNavigateToAuth}
              isDark={isDarkBackground}
            >
              登录
            </RippleButton>
          </div>
        </div>
      </motion.nav>

      {/* 章节指示器 */}
      <div className="fixed right-6 top-1/2 -translate-y-1/2 z-40 hidden lg:flex flex-col gap-3">
        {[0, 1, 2, 3, 4].map((index) => (
          <button
            key={index}
            onClick={() => {
              if (!isScrolling) {
                setIsScrolling(true);
                setActiveChapter(index);
                setTimeout(() => setIsScrolling(false), 1200);
              }
            }}
            className="group flex items-center gap-2"
          >
            <span className="text-[10px] text-white/40 group-hover:text-white/80 transition-colors opacity-0 group-hover:opacity-100 whitespace-nowrap">
              {['01', '02', '03', '04', '05'][index]}
            </span>
            <div
              className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                activeChapter === index
                  ? 'bg-white w-6'
                  : 'bg-white/30 hover:bg-white/60'
              }`}
            />
          </button>
        ))}
      </div>

      {/* 章节容器 */}
      <div
        className="h-screen transition-transform duration-1200 ease-in-out"
        style={{ transform: `translateY(-${activeChapter * 100}vh)` }}
      >
        <Chapter0 onNavigateToAuth={onNavigateToAuth} isActive={activeChapter === 0} mouseX={smoothMouseX} mouseY={smoothMouseY} />
        <Chapter1 isActive={activeChapter === 1} mouseX={smoothMouseX} mouseY={smoothMouseY} />
        <Chapter2 isActive={activeChapter === 2} mouseX={smoothMouseX} mouseY={smoothMouseY} />
        <Chapter3 isActive={activeChapter === 3} mouseX={smoothMouseX} mouseY={smoothMouseY} />
        <Chapter4 onNavigateToAuth={onNavigateToAuth} isActive={activeChapter === 4} mouseX={smoothMouseX} mouseY={smoothMouseY} />
      </div>
    </div>
  );
}

// 第0幕：全屏背景图 + 遮罩文字效果
function Chapter0({ onNavigateToAuth, isActive, mouseX, mouseY }: { onNavigateToAuth: () => void; isActive: boolean; mouseX: any; mouseY: any }) {
  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden bg-black">
      {/* 背景大图（固定） */}
      <div className="absolute inset-0">
        <ImageWithFallback
          src="https://images.unsplash.com/photo-1643050079091-1d4a51e07ba0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsaWJyYXJ5JTIwYm9va3MlMjBzaGVsZnxlbnwxfHx8fDE3NjUzNDY2NDd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/40"></div>
      </div>

      {/* 大标题作为遮罩 - 由远及近 */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center"
        initial={{ scale: 1.5, opacity: 0 }}
        animate={isActive ? { scale: 1, opacity: 1 } : { scale: 1.5, opacity: 0 }}
        transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
      >
        <h1
          className="text-[12rem] lg:text-[16rem] leading-none tracking-tighter select-none"
          style={{
            background: 'url(https://images.unsplash.com/photo-1760840414854-36cd365d14f1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxvcGVuJTIwYm9vayUyMHBhZ2VzJTIwbGlnaHR8ZW58MXx8fHwxNzY1Mzc2MTcxfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontWeight: 900
          }}
        >
          AI
        </h1>
      </motion.div>

      {/* 内容层 - 依次进入 */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-12 w-full">
        <div className="max-w-2xl">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
            transition={{ duration: 0.8, delay: 0.6 }}
          >
            <div className="inline-block px-3 py-1 bg-white/10 backdrop-blur-md text-[10px] tracking-widest text-white mb-4 rounded">
              AI-POWERED WRITING
            </div>
          </motion.div>

          <motion.h2
            className="text-4xl lg:text-5xl text-white leading-tight mb-4"
            initial={{ opacity: 0, y: 30 }}
            animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            创作新纪元
          </motion.h2>

          <motion.p
            className="text-base text-white/70 mb-8 leading-relaxed max-w-lg"
            initial={{ opacity: 0, y: 30 }}
            animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
            transition={{ duration: 0.8, delay: 1 }}
          >
            融合人工智能的力量，让小说创作突破想象边界
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
            transition={{ duration: 0.8, delay: 1.2 }}
          >
            <Button
              onClick={onNavigateToAuth}
              className="bg-white hover:bg-gray-200 text-black h-11 px-8"
            >
              开始创作 <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </motion.div>
        </div>
      </div>

      {/* 底部滚动提示 */}
      <motion.div
        className="absolute bottom-12 left-1/2 -translate-x-1/2 z-20 flex flex-col items-center gap-2"
        initial={{ opacity: 0, y: -20 }}
        animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: -20 }}
        transition={{ duration: 0.8, delay: 1.6 }}
      >
        <span className="text-xs text-white/60 tracking-widest">向下滚动</span>
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
        >
          <ChevronDown className="w-5 h-5 text-white/60" />
        </motion.div>
      </motion.div>
    </section>
  );
}

// 第1幕：文字遮罩效果 + 视差
function Chapter1({ isActive, mouseX, mouseY }: { isActive: boolean; mouseX: any; mouseY: any }) {
  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden bg-black">
      {/* 背景图片 */}
      <div className="absolute inset-0">
        <ImageWithFallback
          src="https://images.unsplash.com/photo-1763098844247-141e76ea20fb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3cml0aW5nJTIwZGVzayUyMGF0bW9zcGhlcmljfGVufDF8fHx8MTc2NTM3NjE3MXww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/50"></div>
      </div>

      {/* 大标题作为遮罩 - 由远及近 */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center"
        initial={{ scale: 1.8, opacity: 0 }}
        animate={isActive ? { scale: 1, opacity: 1 } : { scale: 1.8, opacity: 0 }}
        transition={{ duration: 1.4, ease: [0.22, 1, 0.36, 1] }}
      >
        <h2
          className="text-[14rem] lg:text-[20rem] leading-none tracking-tighter select-none"
          style={{
            background: 'url(https://images.unsplash.com/reserve/LJIZlzHgQ7WPSh5KVTCB_Typewriter.jpg?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aW50YWdlJTIwdHlwZXdyaXRlcnxlbnwxfHx8fDE3NjUzMzM2NDB8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontWeight: 900
          }}
        >
          创作
        </h2>
      </motion.div>

      {/* 内容层 - 依次进入 */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-12 w-full">
        <div className="grid lg:grid-cols-2 gap-12">
          {/* 左侧 */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={isActive ? { opacity: 1, x: 0 } : { opacity: 0, x: -50 }}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            <h3 className="text-3xl lg:text-4xl text-white mb-4">突破创作瓶颈</h3>
            <p className="text-base text-white/70 leading-relaxed">
              我们的 AI 深度理解你的写作风格，在灵感枯竭时提供精准建议，让创作过程流畅自然。
            </p>
          </motion.div>

          {/* 右侧数据卡片 */}
          <motion.div
            className="flex gap-4"
            initial={{ opacity: 0, x: 50 }}
            animate={isActive ? { opacity: 1, x: 0 } : { opacity: 0, x: 50 }}
            transition={{ duration: 0.8, delay: 1 }}
          >
            <div className="flex-1 bg-white/10 border border-white/20 p-6 rounded-2xl">
              <div className="text-4xl text-white mb-2">10k+</div>
              <div className="text-sm text-white/60">活跃创作者</div>
            </div>
            <div className="flex-1 bg-white/10 border border-white/20 p-6 rounded-2xl">
              <div className="text-4xl text-white mb-2">50M+</div>
              <div className="text-sm text-white/60">创作字数</div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

// 第2幕：分屏视差效果
function Chapter2({ isActive, mouseX, mouseY }: { isActive: boolean; mouseX: any; mouseY: any }) {
  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden bg-white">
      {/* 背景图（右侧） */}
      <motion.div
        className="absolute right-0 top-0 bottom-0 w-1/2 lg:w-2/5"
        initial={{ x: '100%' }}
        animate={isActive ? { x: 0 } : { x: '100%' }}
        transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1], delay: 0.6 }}
      >
        <ImageWithFallback
          src="https://images.unsplash.com/photo-1760840414854-36cd365d14f1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxvcGVuJTIwYm9vayUyMHBhZ2VzJTIwbGlnaHR8ZW58MXx8fHwxNzY1Mzc2MTcxfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
          alt="Books"
          className="w-full h-full object-cover"
        />
      </motion.div>

      {/* 大标题作为遮罩 - 由远及近 */}
      <motion.div
        className="absolute left-12 lg:left-24"
        initial={{ scale: 2, opacity: 0 }}
        animate={isActive ? { scale: 1, opacity: 1 } : { scale: 2, opacity: 0 }}
        transition={{ duration: 1.4, ease: [0.22, 1, 0.36, 1] }}
      >
        <h2
          className="text-[10rem] lg:text-[14rem] leading-none tracking-tighter select-none"
          style={{
            background: 'url(https://images.unsplash.com/photo-1661001032128-507b57ffd046?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwYXBlciUyMHRleHR1cmUlMjBhYnN0cmFjdHxlbnwxfHx8fDE3NjUzNzYxNzZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontWeight: 900
          }}
        >
          智能
        </h2>
      </motion.div>

      {/* 内容层 */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-12 w-full">
        <div className="max-w-xl">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
            transition={{ duration: 0.8, delay: 1 }}
            className="space-y-6"
          >
            <div className="bg-white/90 backdrop-blur-sm border-2 border-gray-900 p-6 rounded-2xl">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-gray-900 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Target className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">灵感枯竭</h3>
                  <p className="text-sm text-gray-600">AI 帮你打破思维定式，提供多角度创作建议</p>
                </div>
              </div>
            </div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
              transition={{ duration: 0.8, delay: 1.2 }}
              className="bg-white/90 backdrop-blur-sm border border-gray-200 p-6 rounded-2xl"
            >
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Shield className="w-6 h-6 text-gray-900" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">细节遗漏</h3>
                  <p className="text-sm text-gray-600">智能管理角色设定和世界观，确保前后一致</p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
              transition={{ duration: 0.8, delay: 1.4 }}
              className="bg-white/90 backdrop-blur-sm border border-gray-200 p-6 rounded-2xl"
            >
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Pencil className="w-6 h-6 text-gray-900" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">文字打磨</h3>
                  <p className="text-sm text-gray-600">实时纠错和优化建议，让表达更精准</p>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

// 第3幕：网格视差效果
function Chapter3({ isActive, mouseX, mouseY }: { isActive: boolean; mouseX: any; mouseY: any }) {
  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden bg-black">
      {/* 背景图 */}
      <div className="absolute inset-0">
        <ImageWithFallback
          src="https://images.unsplash.com/reserve/LJIZlzHgQ7WPSh5KVTCB_Typewriter.jpg?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aW50YWdlJTIwdHlwZXdyaXRlcnxlbnwxfHx8fDE3NjUzMzM2NDB8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/70"></div>
      </div>

      {/* 大标题作为遮罩 - 由远及近 */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center"
        initial={{ scale: 2.5, opacity: 0 }}
        animate={isActive ? { scale: 1, opacity: 1 } : { scale: 2.5, opacity: 0 }}
        transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1] }}
      >
        <h2
          className="text-[12rem] lg:text-[18rem] leading-none tracking-tighter select-none"
          style={{
            background: 'url(https://images.unsplash.com/photo-1661001032128-507b57ffd046?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwYXBlciUyMHRleHR1cmUlMjBhYnN0cmFjdHxlbnwxfHx8fDE3NjUzNzYxNzZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontWeight: 900
          }}
        >
          功能
        </h2>
      </motion.div>

      {/* 内容层 - 网格卡片 */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-12 w-full">
        <div className="grid md:grid-cols-3 gap-4">
          {[
            { icon: Zap, title: "智能续写", desc: "深度学习写作风格" },
            { icon: Users, title: "角色管理", desc: "记录人物关系网络" },
            { icon: Sparkles, title: "灵感激发", desc: "提供多元化建议" },
            { icon: BookOpen, title: "大纲构建", desc: "规划故事结构" },
            { icon: Pencil, title: "精准纠错", desc: "语法和表达优化" },
            { icon: Shield, title: "版本管理", desc: "自动保存历史" }
          ].map((feature, index) => (
            <motion.div
              key={index}
              className={`p-6 rounded-2xl backdrop-blur-md border transition-all cursor-pointer ${
                index === 0
                  ? 'bg-white text-black border-white'
                  : 'bg-white/5 text-white border-white/10 hover:bg-white/10'
              }`}
              initial={{ y: 60, opacity: 0 }}
              animate={isActive ? { y: 0, opacity: 1 } : { y: 60, opacity: 0 }}
              transition={{ duration: 0.7, delay: 0.8 + index * 0.1 }}
              whileHover={{ scale: 1.05 }}
            >
              <feature.icon className={`w-8 h-8 mb-4 ${index === 0 ? 'text-black' : 'text-white'}`} />
              <h3 className="text-lg mb-2">{feature.title}</h3>
              <p className={`text-sm ${index === 0 ? 'text-gray-600' : 'text-gray-400'}`}>{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

// 第4幕：CTA + 背景纹理
function Chapter4({ onNavigateToAuth, isActive, mouseX, mouseY }: { onNavigateToAuth: () => void; isActive: boolean; mouseX: any; mouseY: any }) {
  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden bg-black">
      {/* 背景纹理 */}
      <div className="absolute inset-0">
        <ImageWithFallback
          src="https://images.unsplash.com/photo-1763098844247-141e76ea20fb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3cml0aW5nJTIwZGVzayUyMGF0bW9zcGhlcmljfGVufDF8fHx8MTc2NTM3NjE3MXww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/80"></div>
      </div>

      {/* 大标题作为遮罩 - 由远及近 */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center pointer-events-none"
        initial={{ scale: 3, opacity: 0 }}
        animate={isActive ? { scale: 1, opacity: 0.15 } : { scale: 3, opacity: 0 }}
        transition={{ duration: 1.6, ease: [0.22, 1, 0.36, 1] }}
      >
        <h2
          className="text-[18rem] lg:text-[24rem] leading-none tracking-tighter select-none"
          style={{
            background: 'url(https://images.unsplash.com/photo-1760840414854-36cd365d14f1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxvcGVuJTIwYm9vayUyMHBhZ2VzJTIwbGlnaHR8ZW58MXx8fHwxNzY1Mzc2MTcxfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontWeight: 900
          }}
        >
          GO
        </h2>
      </motion.div>

      <div className="relative z-10 max-w-4xl mx-auto px-6 lg:px-12 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
          transition={{ duration: 0.8, delay: 0.8 }}
        >
          <h3 className="text-5xl lg:text-6xl text-white mb-6 leading-tight">
            开启你的创作之旅
          </h3>
        </motion.div>

        <motion.p
          className="text-lg text-gray-400 mb-10 max-w-2xl mx-auto"
          initial={{ opacity: 0, y: 30 }}
          animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
          transition={{ duration: 0.8, delay: 1 }}
        >
          加入数千位创作者，让 AI 成为你的写作伙伴
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isActive ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
          transition={{ duration: 0.8, delay: 1.2 }}
        >
          <Button
            onClick={onNavigateToAuth}
            className="h-12 px-10 bg-white hover:bg-gray-200 text-black"
          >
            免费注册 <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </motion.div>

        <motion.div
          className="mt-20 pt-8 border-t border-white/10"
          initial={{ opacity: 0 }}
          animate={isActive ? { opacity: 1 } : { opacity: 0 }}
          transition={{ duration: 0.8, delay: 1.4 }}
        >
          <p className="text-xs text-gray-600">© 2025 文枢AI</p>
        </motion.div>
      </div>
    </section>
  );
}

// 水波纹按钮组件
function RippleButton({ onClick, isDark, children }: { onClick: () => void; isDark: boolean; children: React.ReactNode }) {
  const [ripples, setRipples] = useState<{ x: number; y: number; id: number }[]>([]);

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const newRipple = { x, y, id: Date.now() };
    setRipples(prev => [...prev, newRipple]);

    setTimeout(() => {
      setRipples(prev => prev.filter(r => r.id !== newRipple.id));
    }, 600);

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
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      {children}
      {ripples.map(ripple => (
        <motion.span
          key={ripple.id}
          className="absolute pointer-events-none rounded-full"
          style={{
            top: ripple.y,
            left: ripple.x,
            backgroundColor: isDark ? 'rgba(255, 255, 255, 0.5)' : 'rgba(0, 0, 0, 0.5)',
          }}
          initial={{ width: 0, height: 0, x: '-50%', y: '-50%' }}
          animate={{ width: 200, height: 200, opacity: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
      ))}
    </motion.button>
  );
}
