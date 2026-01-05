import { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { DataService } from '../../services/DataService';

interface FeaturedNovel {
  id: string;
  title: string;
  description: string;
  cover: string;
}

interface FeaturedCarouselProps {
  onViewDetail?: (workId: string) => void;
}

export function FeaturedCarousel({ onViewDetail }: FeaturedCarouselProps = {}) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [featuredNovels, setFeaturedNovels] = useState<FeaturedNovel[]>([]);
  const [loading, setLoading] = useState(true);

  // 默认封面图片 - 使用本地图片确保国内可访问
  const DEFAULT_COVER_IMAGE = '/default-cover.jpg';

  // 获取默认封面
  const getDefaultCover = (): string => {
    return DEFAULT_COVER_IMAGE;
  };

  // 加载推荐作品
  useEffect(() => {
    const loadFeaturedNovels = async () => {
      try {
        const response = await DataService.getFeaturedNovels();
        const novels = response.map((work: any) => ({
          id: work.id,
          title: work.title,
          description: work.description || '暂无简介',
          cover: work.coverImage || getDefaultCover(),
        }));
        setFeaturedNovels(novels);
      } catch (error) {
        console.error('加载推荐作品失败:', error);
        // 失败时使用空数组
        setFeaturedNovels([]);
      } finally {
        setLoading(false);
      }
    };

    loadFeaturedNovels();
  }, []);

  // 如果没有推荐作品,不显示轮播图
  if (loading || featuredNovels.length === 0) {
    return null;
  }

  const handlePrev = () => {
    setCurrentIndex((prev) => (prev === 0 ? featuredNovels.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setCurrentIndex((prev) => (prev === featuredNovels.length - 1 ? 0 : prev + 1));
  };

  const getItemStyle = (index: number) => {
    const total = featuredNovels.length;
    let position = index - currentIndex;

    if (position < -Math.floor(total / 2)) {
      position += total;
    } else if (position > Math.floor(total / 2)) {
      position -= total;
    }

    const positions: { [key: number]: any } = {
      '-2': { scale: 0.85, opacity: 0.8, zIndex: 3, display: 'block' },
      '-1': { scale: 0.9, opacity: 0.9, zIndex: 4, display: 'block' },
      '0': { scale: 1, opacity: 1, zIndex: 5, display: 'block' },
      '1': { scale: 0.9, opacity: 0.9, zIndex: 4, display: 'block' },
      '2': { scale: 0.85, opacity: 0.8, zIndex: 3, display: 'block' },
    };

    return positions[position] || { right: '-300px', scale: 0.5, opacity: 0, zIndex: 1, display: 'none' };
  };

  const currentNovel = featuredNovels[currentIndex];

  return (
    <div className="bg-white dark:bg-slate-900">
      <div className="max-w-6xl mx-auto px-6 py-8">
        <h2 className="mb-6 text-gray-900 dark:text-white">
          编辑推荐
        </h2>

        <div className="flex items-center gap-8">
          <button
            onClick={handlePrev}
            className="flex-shrink-0 w-10 h-10 flex items-center justify-center text-gray-400 dark:text-slate-500 hover:text-gray-600 dark:hover:text-slate-300 transition-colors"
            aria-label="上一个"
          >
            <ChevronLeft className="w-6 h-6" />
          </button>

          <div className="flex-1 flex items-center gap-8">
            <div className="relative w-[600px] h-[352px] overflow-visible">
              {featuredNovels.map((novel, index) => {
                const style = getItemStyle(index);

                const baseWidth = 186;
                let rightPosition: string;
                const total = featuredNovels.length;
                let position = index - currentIndex;

                if (position < -Math.floor(total / 2)) {
                  position += total;
                } else if (position > Math.floor(total / 2)) {
                  position -= total;
                }

                // 50%重叠布局: 每张图片间隔为baseWidth * 0.5
                const centerOffset = 300;
                if (position === -2) {
                  rightPosition = `${centerOffset + baseWidth * 0.5 * 2}px`;
                } else if (position === -1) {
                  rightPosition = `${centerOffset + baseWidth * 0.5}px`;
                } else if (position === 0) {
                  rightPosition = `${centerOffset}px`;
                } else if (position === 1) {
                  rightPosition = `${centerOffset - baseWidth * 0.5}px`;
                } else if (position === 2) {
                  rightPosition = `${centerOffset - baseWidth * 0.5 * 2}px`;
                } else {
                  rightPosition = '-300px';
                }

                const imgWidth = 186 * style.scale;
                const imgHeight = 248 * style.scale;

                return (
                  <div
                    key={novel.id}
                    className="absolute transition-all duration-500 ease-in-out overflow-hidden shadow-lg rounded-xl"
                    style={{
                      right: rightPosition,
                      width: `${imgWidth}px`,
                      height: `${imgHeight}px`,
                      top: `${(352 - imgHeight) / 2}px`,
                      opacity: style.opacity,
                      zIndex: style.zIndex,
                      display: style.display,
                    }}
                  >
                    <img
                      src={novel.cover}
                      alt={novel.title}
                      style={{ width: `${imgWidth}px`, height: `${imgHeight}px`, objectFit: 'cover' }}
                    />
                  </div>
                );
              })}
            </div>

            <div className="flex-1">
              <h3 className="mb-4 text-gray-900 dark:text-white">{currentNovel.title}</h3>
              <p className="text-gray-600 dark:text-slate-400 mb-6 leading-relaxed">{currentNovel.description}</p>
              <button
                onClick={() => onViewDetail?.(currentNovel.id)}
                className="px-8 py-2 bg-red-600 text-white hover:bg-red-700 transition-colors rounded-lg"
              >
                书籍详情
              </button>
            </div>
          </div>

          <button
            onClick={handleNext}
            className="flex-shrink-0 w-10 h-10 flex items-center justify-center text-gray-400 dark:text-slate-500 hover:text-gray-600 dark:hover:text-slate-300 transition-colors"
            aria-label="下一个"
          >
            <ChevronRight className="w-6 h-6" />
          </button>
        </div>

        <div className="flex items-center justify-center gap-2 mt-6">
          {featuredNovels.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentIndex(index)}
              className={`w-2 h-2 rounded-full transition-all ${
                index === currentIndex ? 'bg-red-600 w-6' : 'bg-gray-300 dark:bg-slate-600 hover:bg-gray-400 dark:hover:bg-slate-500'
              }`}
              aria-label={`跳转到第 ${index + 1} 个`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
