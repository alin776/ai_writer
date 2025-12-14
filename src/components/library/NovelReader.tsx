import { useState, useEffect } from 'react';
import {
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  Menu,
  Settings,
  BookOpen,
  Loader2,
} from 'lucide-react';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import { useTheme } from '../../hooks/useTheme';

interface NovelReaderProps {
  workId: string;
  chapterId?: string;
  onBack: () => void;
}

interface Chapter {
  id: string;
  title: string;
  order: number;
  content: string;
  wordCount: number;
  publishedAt: string;
}

interface ChapterListItem {
  id: string;
  title: string;
  order: number;
  wordCount: number;
  viewCount: number;
  publishedAt: string;
}

export function NovelReader({ workId, chapterId, onBack }: NovelReaderProps) {
  const { error: showError } = useGlobalStore();
  const { effectiveTheme } = useTheme();
  const isDarkMode = effectiveTheme === 'dark';

  const [currentChapter, setCurrentChapter] = useState<Chapter | null>(null);
  const [chapters, setChapters] = useState<ChapterListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showChapterList, setShowChapterList] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  // 阅读设置
  const [fontSize, setFontSize] = useState(18);
  const [lineHeight, setLineHeight] = useState(1.8);

  // 预设主题
  const themes = [
    { name: '护眼', bg: '#faf8f3', text: '#333333', darkBg: '#2a2a2a', darkText: '#d4d4d4' },
    { name: '夜间', bg: '#1a1a1a', text: '#e0e0e0', darkBg: '#0d0d0d', darkText: '#e8e8e8' },
    { name: '纯白', bg: '#ffffff', text: '#000000', darkBg: '#1f1f1f', darkText: '#ffffff' },
    { name: '羊皮纸', bg: '#f4ecd8', text: '#5c4a2a', darkBg: '#3a3428', darkText: '#d4c4a8' },
  ];

  // 根据深色模式自动选择主题
  const [selectedThemeIndex, setSelectedThemeIndex] = useState(0);
  const currentTheme = themes[selectedThemeIndex];
  const backgroundColor = isDarkMode ? currentTheme.darkBg : currentTheme.bg;
  const textColor = isDarkMode ? currentTheme.darkText : currentTheme.text;

  // 加载章节列表
  useEffect(() => {
    const loadChapters = async () => {
      try {
        const response = await DataService.getPublishedNovelDetail(workId);
        setChapters(response?.chapters || []);
      } catch (error) {
        console.error('加载章节列表失败:', error);
        showError('加载章节列表失败');
      }
    };
    loadChapters();
  }, [workId]);

  // 加载章节内容
  const loadChapter = async (targetChapterId: string) => {
    try {
      setLoading(true);
      const chapterData = await DataService.getPublishedChapterContent(workId, targetChapterId);
      setCurrentChapter(chapterData);

      // 保存阅读进度
      await DataService.updateReadingProgress(workId, targetChapterId, 0).catch(() => {
        // 静默失败，不影响阅读体验
      });
    } catch (error) {
      console.error('加载章节失败:', error);
      showError('加载章节失败');
    } finally {
      setLoading(false);
    }
  };

  // 初始加载
  useEffect(() => {
    if (chapters.length > 0) {
      const targetId = chapterId || chapters[0]?.id;
      if (targetId) {
        loadChapter(targetId);
      }
    }
  }, [chapters, chapterId]);

  // 上一章
  const handlePrevChapter = () => {
    if (!currentChapter) return;
    const currentIndex = chapters.findIndex((c) => c.id === currentChapter.id);
    if (currentIndex > 0) {
      loadChapter(chapters[currentIndex - 1].id);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  // 下一章
  const handleNextChapter = () => {
    if (!currentChapter) return;
    const currentIndex = chapters.findIndex((c) => c.id === currentChapter.id);
    if (currentIndex < chapters.length - 1) {
      loadChapter(chapters[currentIndex + 1].id);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  // 跳转到指定章节
  const handleSelectChapter = (chapterId: string) => {
    loadChapter(chapterId);
    setShowChapterList(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // 应用主题
  const applyTheme = (index: number) => {
    setSelectedThemeIndex(index);
  };

  const currentIndex = currentChapter ? chapters.findIndex((c) => c.id === currentChapter.id) : -1;
  const hasPrev = currentIndex > 0;
  const hasNext = currentIndex < chapters.length - 1;

  return (
    <div className="min-h-screen" style={{ backgroundColor }}>
      {/* 顶部导航栏 */}
      <div className="sticky top-0 z-10 bg-white dark:bg-slate-900 border-b border-gray-200 dark:border-slate-700 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span className="text-sm">返回</span>
          </button>

          <div className="flex-1 mx-4 text-center">
            <h1 className="text-sm font-medium text-gray-900 dark:text-white truncate">
              {currentChapter?.title || '加载中...'}
            </h1>
            <p className="text-xs text-gray-500 dark:text-slate-400">
              {currentIndex >= 0 ? `${currentIndex + 1}/${chapters.length}` : ''}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowChapterList(!showChapterList)}
              className="p-2 text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              title="章节列表"
            >
              <Menu className="w-5 h-5" />
            </button>
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              title="阅读设置"
            >
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* 章节列表侧边栏 */}
      {showChapterList && (
        <div className="fixed inset-0 z-20 flex">
          <div
            className="flex-1 bg-black/20"
            onClick={() => setShowChapterList(false)}
          ></div>
          <div className="w-80 bg-white dark:bg-slate-900 shadow-xl overflow-y-auto">
            <div className="p-4 border-b border-gray-200 dark:border-slate-700">
              <h2 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <BookOpen className="w-5 h-5" />
                章节目录
              </h2>
              <p className="text-sm text-gray-500 dark:text-slate-400 mt-1">
                共 {chapters.length} 章
              </p>
            </div>
            <div className="divide-y divide-gray-200 dark:divide-slate-700">
              {chapters.map((chapter) => (
                <button
                  key={chapter.id}
                  onClick={() => handleSelectChapter(chapter.id)}
                  className={`w-full text-left px-4 py-3 hover:bg-gray-50 dark:hover:bg-slate-800 transition-colors ${
                    currentChapter?.id === chapter.id
                      ? 'bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-600'
                      : ''
                  }`}
                >
                  <div className="font-medium text-gray-900 dark:text-white text-sm">
                    第 {chapter.order} 章
                  </div>
                  <div className="text-sm text-gray-600 dark:text-slate-400 mt-1 truncate">
                    {chapter.title}
                  </div>
                  <div className="text-xs text-gray-400 dark:text-slate-500 mt-1">
                    {chapter.wordCount} 字
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 阅读设置面板 */}
      {showSettings && (
        <div className="fixed inset-0 z-20 flex items-center justify-center bg-black/50">
          <div className="bg-white dark:bg-slate-900 rounded-lg shadow-xl w-full max-w-md mx-4 p-6">
            <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
              阅读设置
            </h2>

            {/* 字体大小 */}
            <div className="mb-6">
              <label className="text-sm text-gray-700 dark:text-slate-300 mb-2 block">
                字体大小: {fontSize}px
              </label>
              <input
                type="range"
                min="14"
                max="28"
                step="2"
                value={fontSize}
                onChange={(e) => setFontSize(Number(e.target.value))}
                className="w-full"
              />
            </div>

            {/* 行高 */}
            <div className="mb-6">
              <label className="text-sm text-gray-700 dark:text-slate-300 mb-2 block">
                行高: {lineHeight}
              </label>
              <input
                type="range"
                min="1.2"
                max="2.5"
                step="0.1"
                value={lineHeight}
                onChange={(e) => setLineHeight(Number(e.target.value))}
                className="w-full"
              />
            </div>

            {/* 主题 */}
            <div className="mb-6">
              <label className="text-sm text-gray-700 dark:text-slate-300 mb-2 block">
                阅读主题
              </label>
              <div className="grid grid-cols-4 gap-2">
                {themes.map((theme, index) => (
                  <button
                    key={theme.name}
                    onClick={() => applyTheme(index)}
                    className="px-3 py-2 text-sm rounded border-2 transition-all"
                    style={{
                      backgroundColor: isDarkMode ? theme.darkBg : theme.bg,
                      color: isDarkMode ? theme.darkText : theme.text,
                      borderColor:
                        selectedThemeIndex === index
                          ? '#3b82f6'
                          : 'transparent',
                    }}
                  >
                    {theme.name}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={() => setShowSettings(false)}
              className="w-full px-4 py-2 bg-black dark:bg-slate-700 text-white rounded hover:bg-gray-800 dark:hover:bg-slate-600 transition-colors"
            >
              关闭
            </button>
          </div>
        </div>
      )}

      {/* 阅读内容区域 */}
      <div className="max-w-4xl mx-auto px-6 py-8">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin mb-4" style={{ color: textColor }} />
            <p style={{ color: textColor }}>加载中...</p>
          </div>
        ) : currentChapter ? (
          <>
            {/* 章节标题 */}
            <div className="mb-8 text-center">
              <h1
                className="text-2xl font-bold mb-2"
                style={{ color: textColor }}
              >
                {currentChapter.title}
              </h1>
              <div className="text-sm opacity-60" style={{ color: textColor }}>
                第 {currentChapter.order} 章 · {currentChapter.wordCount} 字
              </div>
            </div>

            {/* 章节内容 */}
            <div
              className="prose prose-lg max-w-none mb-12"
              style={{
                fontSize: `${fontSize}px`,
                lineHeight: lineHeight,
                color: textColor,
              }}
            >
              <style>
                {`
                  .chapter-content p {
                    margin-bottom: 1.5em;
                    text-indent: 2em;
                    text-align: justify;
                  }
                  .chapter-content p:first-child {
                    margin-top: 0;
                  }
                `}
              </style>
              <div
                className="chapter-content"
                dangerouslySetInnerHTML={{ __html: currentChapter.content }}
              />
            </div>

            {/* 底部翻页按钮 */}
            <div className="flex items-center justify-between gap-4 py-8 border-t border-gray-200 dark:border-slate-700">
              <button
                onClick={handlePrevChapter}
                disabled={!hasPrev}
                className="flex items-center gap-2 px-6 py-3 bg-white dark:bg-slate-800 rounded-lg transition-colors disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-slate-700"
                style={{ color: textColor }}
              >
                <ChevronLeft className="w-5 h-5" />
                <span>上一章</span>
              </button>

              <button
                onClick={() => setShowChapterList(true)}
                className="px-6 py-3 bg-white dark:bg-slate-800 rounded-lg hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors"
                style={{ color: textColor }}
              >
                目录
              </button>

              <button
                onClick={handleNextChapter}
                disabled={!hasNext}
                className="flex items-center gap-2 px-6 py-3 bg-white dark:bg-slate-800 rounded-lg transition-colors disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-slate-700"
                style={{ color: textColor }}
              >
                <span>下一章</span>
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </>
        ) : (
          <div className="text-center py-20" style={{ color: textColor }}>
            <p>章节加载失败</p>
          </div>
        )}
      </div>
    </div>
  );
}
