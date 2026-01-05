import React, { useState } from 'react';
import { ArrowLeft, BookOpen, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

interface CreateWorkChoiceProps {
  onSelect: (mode: 'manual' | 'ai') => void;
  onBack: () => void;
}

interface InkDrop {
  id: number;
  x: number;
  y: number;
}

/**
 * CreateWorkChoice 组件 - 选择创建模式
 *
 * 两个选项：
 * 1. 已有剧情想法和世界观思路 - 手动填写
 * 2. 需要AI创建世界观和思路 - AI辅助
 *
 * 采用中国水墨风格设计，对联式布局
 */
const CreateWorkChoice: React.FC<CreateWorkChoiceProps> = ({ onSelect, onBack }) => {
  const [selectedMode, setSelectedMode] = useState<'manual' | 'ai' | null>(null);
  const [inkDrops, setInkDrops] = useState<InkDrop[]>([]);

  const handleModeClick = (mode: 'manual' | 'ai', event: React.MouseEvent<HTMLButtonElement>) => {
    setSelectedMode(mode);

    // 获取点击位置
    const rect = event.currentTarget.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const newDrop: InkDrop = {
      id: Date.now(),
      x,
      y,
    };

    setInkDrops(prev => [...prev, newDrop]);

    // 2秒后移除墨滴
    setTimeout(() => {
      setInkDrops(prev => prev.filter(drop => drop.id !== newDrop.id));
    }, 2000);
  };

  const handleConfirm = () => {
    if (selectedMode) {
      onSelect(selectedMode);
    }
  };

  return (
    <div className="h-screen bg-[#faf8f5] dark:bg-slate-900 flex relative overflow-hidden">
      {/* SVG 滤镜定义 - 创建不规则墨滴效果 */}
      <svg className="absolute w-0 h-0">
        <defs>
          <filter id="inkFilter">
            {/* 创建湍流噪声 */}
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.03"
              numOctaves="4"
              result="turbulence"
            />
            {/* 位移映射使边缘不规则 */}
            <feDisplacementMap
              in="SourceGraphic"
              in2="turbulence"
              scale="15"
              xChannelSelector="R"
              yChannelSelector="G"
              result="displacement"
            />
            {/* 高斯模糊模拟晕染 */}
            <feGaussianBlur in="displacement" stdDeviation="3" result="blur" />
            {/* 合成 */}
            <feComposite in="blur" in2="SourceGraphic" operator="atop" />
          </filter>

          <filter id="inkFilterLight">
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.02"
              numOctaves="3"
              result="turbulence"
            />
            <feDisplacementMap
              in="SourceGraphic"
              in2="turbulence"
              scale="20"
              xChannelSelector="R"
              yChannelSelector="G"
              result="displacement"
            />
            <feGaussianBlur in="displacement" stdDeviation="6" result="blur" />
            <feComposite in="blur" in2="SourceGraphic" operator="atop" />
          </filter>
        </defs>
      </svg>

      {/* 背景墨迹渐变 */}
      <div className="absolute inset-0 opacity-[0.02] dark:opacity-[0.05]">
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-radial from-gray-900 dark:from-gray-100 to-transparent blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-gradient-radial from-gray-900 dark:from-gray-100 to-transparent blur-3xl"></div>
      </div>

      <div className="w-full relative z-10 h-full overflow-y-auto overflow-x-hidden">
        {/* 返回按钮 - 卷轴轴头样式 */}
        <button
          onClick={onBack}
          className="absolute left-8 top-8 w-10 h-10 rounded-full border-2 border-gray-300 dark:border-gray-600 bg-[#faf8f5] dark:bg-slate-800 flex items-center justify-center hover:border-gray-600 dark:hover:border-gray-400 transition-colors group"
        >
          <ArrowLeft className="w-4 h-4 text-gray-400 group-hover:text-gray-800 dark:group-hover:text-gray-200 transition-colors" />
        </button>

        {/* 标题 - 书法式排版 */}
        <div className="text-center mb-12 pt-12">
          <div className="inline-block relative">
            <h1 className="text-5xl text-gray-800 dark:text-gray-100 tracking-[0.5em] mb-4" style={{ fontFamily: "'HYShangWeiShouShuW', 'Ma Shan Zheng', cursive" }}>
              开始创作
            </h1>
          </div>
          <p className="text-gray-500 dark:text-gray-400 mt-4">选择适合你的创作方式</p>
        </div>

        {/* 对联式选项 */}
        <div className="grid grid-cols-2 gap-0 mb-8">
          {/* 左侧：清晰思路 */}
          <motion.button
            onClick={(e) => handleModeClick('manual', e)}
            className={`relative py-12 px-8 min-h-[320px] transition-all duration-500 overflow-hidden rounded-2xl ${
              selectedMode === 'manual'
                ? ''
                : selectedMode === 'ai'
                ? 'opacity-40'
                : 'hover:bg-white/20 dark:hover:bg-white/5'
            }`}
            whileTap={{ scale: 0.98 }}
          >
            {/* 背景山水图片 */}
            {selectedMode === 'manual' && (
              <motion.div
                initial={{ opacity: 0, scale: 1.2 }}
                animate={{ opacity: 1, scale: 1.5 }}
                transition={{ duration: 0.8 }}
                className="absolute inset-0 z-0"
                style={{
                  backgroundImage: 'url(/images/mountain-bg.png)',
                  backgroundSize: 'contain',
                  backgroundPosition: 'center',
                  backgroundRepeat: 'no-repeat',
                  opacity: 0.15,
                }}
              />
            )}

            {/* 墨滴扩散动画 */}
            <AnimatePresence>
              {inkDrops
                .filter((_, index, arr) => index >= arr.length - 1 && selectedMode === 'manual')
                .map((drop) => (
                  <div key={drop.id} className="absolute inset-0 pointer-events-none">
                    {/* 外层 - 最淡的晕染 */}
                    <motion.div
                      className="absolute rounded-full bg-gray-900/5 dark:bg-gray-100/5"
                      style={{
                        left: drop.x,
                        top: drop.y,
                        filter: 'url(#inkFilterLight)',
                      }}
                      initial={{ width: 0, height: 0, x: '-50%', y: '-50%' }}
                      animate={{
                        width: 400,
                        height: 400,
                        opacity: [0.3, 0.1, 0]
                      }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 1.8, ease: [0.4, 0, 0.2, 1] }}
                    />
                    {/* 中层 */}
                    <motion.div
                      className="absolute rounded-full bg-gray-900/8 dark:bg-gray-100/8"
                      style={{
                        left: drop.x,
                        top: drop.y,
                        filter: 'url(#inkFilter)',
                      }}
                      initial={{ width: 0, height: 0, x: '-50%', y: '-50%' }}
                      animate={{
                        width: 250,
                        height: 250,
                        opacity: [0.5, 0.2, 0]
                      }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 1.5, ease: [0.4, 0, 0.2, 1] }}
                    />
                    {/* 核心 - 最浓 */}
                    <motion.div
                      className="absolute rounded-full bg-gray-900/12 dark:bg-gray-100/12"
                      style={{
                        left: drop.x,
                        top: drop.y,
                        filter: 'url(#inkFilter)',
                      }}
                      initial={{ width: 0, height: 0, x: '-50%', y: '-50%' }}
                      animate={{
                        width: 120,
                        height: 120,
                        opacity: [0.7, 0.3, 0]
                      }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 1.2, ease: [0.4, 0, 0.2, 1] }}
                    />
                  </div>
                ))}
            </AnimatePresence>
            <motion.div
              className="space-y-6 relative z-10"
              animate={{
                x: selectedMode === 'manual' ? -80 : 0
              }}
              transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
            >
              {/* 图标 */}
              <div className="flex justify-center">
                <BookOpen className="w-12 h-12 text-gray-700 dark:text-gray-300 stroke-[1.5]" />
              </div>

              {/* 标题 */}
              <div className="text-center">
                <h2 className="text-2xl text-gray-800 dark:text-gray-100 mb-3 tracking-wide">已有清晰思路</h2>
                <div className="w-12 h-px bg-gray-300 dark:bg-gray-600 mx-auto"></div>
              </div>

              {/* 描述 - 竖排诗意 */}
              <div className="text-center space-y-2 text-gray-600 dark:text-gray-400">
                <p className="leading-loose">胸有成竹</p>
                <p className="leading-loose">一气呵成</p>
              </div>

              {/* 特点 */}
              <div className="flex justify-center gap-6 text-sm text-gray-400 dark:text-gray-500">
                <span>快速</span>
                <span>·</span>
                <span>自主</span>
              </div>
            </motion.div>

            {/* 选中标记 */}
            {selectedMode === 'manual' && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                className="absolute top-4 right-4 w-6 h-6 rounded-full bg-gray-800 dark:bg-gray-200 flex items-center justify-center"
              >
                <div className="w-2 h-2 bg-white dark:bg-slate-800 rounded-full"></div>
              </motion.div>
            )}
          </motion.button>

          {/* 中间分隔线 */}
          <div className="absolute left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-gray-300 dark:via-gray-600 to-transparent"></div>

          {/* 右侧：AI 协作 */}
          <motion.button
            onClick={(e) => handleModeClick('ai', e)}
            className={`relative py-12 px-8 min-h-[320px] transition-all duration-500 overflow-hidden rounded-2xl ${
              selectedMode === 'ai'
                ? ''
                : selectedMode === 'manual'
                ? 'opacity-40'
                : 'hover:bg-white/20 dark:hover:bg-white/5'
            }`}
            whileTap={{ scale: 0.98 }}
          >
            {/* 背景山水图片 */}
            {selectedMode === 'ai' && (
              <motion.div
                initial={{ opacity: 0, scale: 1.2 }}
                animate={{ opacity: 1, scale: 1.5 }}
                transition={{ duration: 0.8 }}
                className="absolute inset-0 z-0"
                style={{
                  backgroundImage: 'url(/images/waterfall-bg.png)',
                  backgroundSize: 'contain',
                  backgroundPosition: 'center',
                  backgroundRepeat: 'no-repeat',
                  opacity: 0.15,
                }}
              />
            )}

            {/* 墨滴扩散动画 */}
            <AnimatePresence>
              {inkDrops
                .filter((_, index, arr) => index >= arr.length - 1 && selectedMode === 'ai')
                .map((drop) => (
                  <div key={drop.id} className="absolute inset-0 pointer-events-none">
                    {/* 外层 - 最淡的晕染 */}
                    <motion.div
                      className="absolute rounded-full bg-gray-900/5 dark:bg-gray-100/5"
                      style={{
                        left: drop.x,
                        top: drop.y,
                        filter: 'url(#inkFilterLight)',
                      }}
                      initial={{ width: 0, height: 0, x: '-50%', y: '-50%' }}
                      animate={{
                        width: 400,
                        height: 400,
                        opacity: [0.3, 0.1, 0]
                      }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 1.8, ease: [0.4, 0, 0.2, 1] }}
                    />
                    {/* 中层 */}
                    <motion.div
                      className="absolute rounded-full bg-gray-900/8 dark:bg-gray-100/8"
                      style={{
                        left: drop.x,
                        top: drop.y,
                        filter: 'url(#inkFilter)',
                      }}
                      initial={{ width: 0, height: 0, x: '-50%', y: '-50%' }}
                      animate={{
                        width: 250,
                        height: 250,
                        opacity: [0.5, 0.2, 0]
                      }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 1.5, ease: [0.4, 0, 0.2, 1] }}
                    />
                    {/* 核心 - 最浓 */}
                    <motion.div
                      className="absolute rounded-full bg-gray-900/12 dark:bg-gray-100/12"
                      style={{
                        left: drop.x,
                        top: drop.y,
                        filter: 'url(#inkFilter)',
                      }}
                      initial={{ width: 0, height: 0, x: '-50%', y: '-50%' }}
                      animate={{
                        width: 120,
                        height: 120,
                        opacity: [0.7, 0.3, 0]
                      }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 1.2, ease: [0.4, 0, 0.2, 1] }}
                    />
                  </div>
                ))}
            </AnimatePresence>
            <motion.div
              className="space-y-6 relative z-10"
              animate={{
                x: selectedMode === 'ai' ? 80 : 0
              }}
              transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
            >
              {/* 图标 */}
              <div className="flex justify-center">
                <Sparkles className="w-12 h-12 text-gray-700 dark:text-gray-300 stroke-[1.5]" />
              </div>

              {/* 标题 */}
              <div className="text-center">
                <h2 className="text-2xl text-gray-800 dark:text-gray-100 mb-3 tracking-wide">需要AI协作构建</h2>
                <div className="w-12 h-px bg-gray-300 dark:bg-gray-600 mx-auto"></div>
              </div>

              {/* 描述 - 竖排诗意 */}
              <div className="text-center space-y-2 text-gray-600 dark:text-gray-400">
                <p className="leading-loose">抽丝剥茧</p>
                <p className="leading-loose">渐入佳境</p>
              </div>

              {/* 特点 */}
              <div className="flex justify-center gap-6 text-sm text-gray-400 dark:text-gray-500">
                <span>引导</span>
                <span>·</span>
                <span>灵活</span>
              </div>
            </motion.div>

            {/* 选中标记 */}
            {selectedMode === 'ai' && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                className="absolute top-4 right-4 w-6 h-6 rounded-full bg-gray-800 dark:bg-gray-200 flex items-center justify-center"
              >
                <div className="w-2 h-2 bg-white dark:bg-slate-800 rounded-full"></div>
              </motion.div>
            )}
          </motion.button>
        </div>

        {/* 画卷展开内容区域 */}
        {selectedMode && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            transition={{ duration: 0.6, ease: [0.4, 0, 0.2, 1] }}
            className="overflow-hidden"
          >
            <motion.div
              initial={{ y: -20 }}
              animate={{ y: 0 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="py-6"
            >
              {/* 详细说明 */}
              <div className="max-w-2xl mx-auto text-center space-y-4">

                {/* 进入按钮 */}
                <motion.button
                  onClick={handleConfirm}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-16 py-4 border-2 border-gray-800 dark:border-gray-200 text-gray-800 dark:text-gray-200 hover:bg-gray-800 hover:text-white dark:hover:bg-gray-200 dark:hover:text-slate-900 transition-all duration-300 rounded-xl"
                >
                  进入创作
                </motion.button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default CreateWorkChoice;
