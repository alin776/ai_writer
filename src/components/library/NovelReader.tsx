import { useState, useEffect, useRef } from 'react';
import {
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  Menu,
  Settings,
  BookOpen,
  Loader2,
  Search,
  X,
} from 'lucide-react';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import { useTheme } from '../../hooks/useTheme';
import { useWorkNavStore } from '../../store/workNavStore';

interface NovelReaderProps {
  workId: string;
  chapterId?: string;
  onBack: () => void;
  initialChapters?: ChapterListItem[];  // 从 NovelDetail 传入的章节列表，避免重复调用 API
  novelTitle?: string;  // 小说名称，显示在顶部导航栏
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

export function NovelReader({ workId, chapterId, onBack, initialChapters, novelTitle }: NovelReaderProps) {
  const { error: showError } = useGlobalStore();
  const { effectiveTheme } = useTheme();
  const isDarkMode = effectiveTheme === 'dark';
  const { setLastChapter } = useWorkNavStore();

  const [currentChapter, setCurrentChapter] = useState<Chapter | null>(null);
  const [chapters, setChapters] = useState<ChapterListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showChapterList, setShowChapterList] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [chapterSearchQuery, setChapterSearchQuery] = useState('');

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

  // 防止 StrictMode 双重渲染导致的重复调用
  const hasLoadedChaptersRef = useRef<string | null>(null);
  const loadedChapterIdRef = useRef<string | null>(null);
  // 防止章节快速切换时重复加载
  const loadingChapterRef = useRef<string | null>(null);

  // 加载章节列表
  useEffect(() => {
    // 如果传入了初始章节列表，直接使用，不调用 API（避免重复增加浏览量）
    if (initialChapters && initialChapters.length > 0) {
      setChapters(initialChapters);
      hasLoadedChaptersRef.current = workId;
      return;
    }

    // 如果 workId 变化了，需要重置标记
    if (hasLoadedChaptersRef.current && hasLoadedChaptersRef.current !== workId) {
      hasLoadedChaptersRef.current = null;
    }

    // 如果已经加载过当前作品的章节列表，则跳过
    if (hasLoadedChaptersRef.current === workId) {
      return;
    }

    const loadChapters = async () => {
      try {
        // 标记为已加载
        hasLoadedChaptersRef.current = workId;
        const response = await DataService.getPublishedNovelDetail(workId);
        setChapters(response?.chapters || []);
      } catch (error) {
        console.error('加载章节列表失败:', error);
        showError('加载章节列表失败');
        // 加载失败时重置标记，允许重试
        hasLoadedChaptersRef.current = null;
      }
    };
    loadChapters();
  }, [workId, initialChapters]);

  // 加载章节内容
  const loadChapter = async (targetChapterId: string) => {
    // 防止重复加载同一章节（用户快速点击翻页时）
    if (loadingChapterRef.current === targetChapterId) {
      return;
    }

    try {
      loadingChapterRef.current = targetChapterId;
      setLoading(true);
      const chapterData = await DataService.getPublishedChapterContent(workId, targetChapterId);
      setCurrentChapter(chapterData);
      loadedChapterIdRef.current = targetChapterId;

      // 保存章节ID到本地存储，用于返回时恢复阅读位置
      setLastChapter(workId, targetChapterId);

      // 保存阅读进度到后端
      await DataService.updateReadingProgress(workId, targetChapterId, 0).catch(() => {
        // 静默失败，不影响阅读体验
      });
    } catch (error) {
      console.error('加载章节失败:', error);
      showError('加载章节失败');
    } finally {
      setLoading(false);
      loadingChapterRef.current = null;
    }
  };

  // 初始加载
  useEffect(() => {
    if (chapters.length > 0) {
      const targetId = chapterId || chapters[0]?.id;
      // 防止重复加载同一章节
      if (targetId && loadedChapterIdRef.current !== targetId) {
        loadedChapterIdRef.current = targetId;
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
              {novelTitle || '小说阅读'}
            </h1>
            <p className="text-xs text-gray-500 dark:text-slate-400">
              {currentIndex >= 0 ? `第${currentIndex + 1}章 / 共${chapters.length}章` : '加载中...'}
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
        <>
          {/* 遮罩层 - 从顶部导航栏下方开始 */}
          <div
            className="fixed inset-0 top-[52px] z-20 bg-black/30 backdrop-blur-sm"
            onClick={() => setShowChapterList(false)}
          />
          {/* 章节列表面板 */}
          <div className="fixed top-[52px] right-0 bottom-0 w-80 z-30 bg-white dark:bg-slate-900 shadow-2xl flex flex-col border-l border-gray-200 dark:border-slate-700">
            {/* 头部 */}
            <div className="flex-shrink-0 p-4 border-b border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-800/50">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-base font-bold text-gray-900 dark:text-white flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-blue-500" />
                  章节目录
                </h2>
                <button
                  onClick={() => setShowChapterList(false)}
                  className="p-1 text-gray-400 hover:text-gray-600 dark:text-slate-500 dark:hover:text-slate-300 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              {/* 搜索框 */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="搜索章节..."
                  value={chapterSearchQuery}
                  onChange={(e) => setChapterSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-8 py-2 text-sm bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 focus:outline-none focus:border-gray-400 dark:focus:border-slate-600 text-gray-900 dark:text-white placeholder-gray-400 transition-colors"
                />
                {chapterSearchQuery && (
                  <button
                    onClick={() => setChapterSearchQuery('')}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-slate-300 transition-colors"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
              {/* 当前阅读位置提示 */}
              <div className="flex items-center justify-between mt-3">
                {currentChapter && (
                  <p className="text-xs text-blue-600 dark:text-blue-400">
                    当前：第 {currentChapter.order} 章
                  </p>
                )}
                <span className="text-xs text-gray-500 dark:text-slate-400 bg-gray-100 dark:bg-slate-800 px-2 py-0.5 border border-gray-200 dark:border-slate-700">
                  共 {chapters.length} 章
                </span>
              </div>
            </div>
            {/* 章节列表 - 可滚动区域 */}
            <div className="flex-1 overflow-y-auto">
              {(() => {
                const filteredChapters = chapters.filter((chapter) =>
                  chapterSearchQuery
                    ? chapter.title.toLowerCase().includes(chapterSearchQuery.toLowerCase()) ||
                      chapter.order.toString().includes(chapterSearchQuery)
                    : true
                );

                if (filteredChapters.length === 0) {
                  return (
                    <div className="flex flex-col items-center justify-center py-12 text-gray-400 dark:text-slate-500">
                      <Search className="w-8 h-8 mb-2" />
                      <p className="text-sm">未找到匹配的章节</p>
                    </div>
                  );
                }

                return (
                  <div className="divide-y divide-gray-200 dark:divide-slate-700">
                    {filteredChapters.map((chapter) => {
                      const isCurrentChapter = currentChapter?.id === chapter.id;
                      return (
                        <button
                          key={chapter.id}
                          onClick={() => handleSelectChapter(chapter.id)}
                          className={`w-full text-left px-4 py-3 transition-colors ${
                            isCurrentChapter
                              ? 'bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-600'
                              : 'hover:bg-gray-100 dark:hover:bg-slate-800'
                          }`}
                        >
                          <div className="flex items-center gap-2">
                            <span className={`text-xs font-medium px-1.5 py-0.5 rounded ${
                              isCurrentChapter
                                ? 'bg-blue-500 text-white'
                                : 'bg-gray-200 dark:bg-slate-700 text-gray-600 dark:text-slate-400'
                            }`}>
                              {chapter.order}
                            </span>
                            <span className={`text-sm truncate flex-1 ${
                              isCurrentChapter
                                ? 'text-blue-700 dark:text-blue-300 font-medium'
                                : 'text-gray-700 dark:text-slate-300'
                            }`}>
                              {chapter.title}
                            </span>
                          </div>
                          <div className="flex items-center justify-between mt-1.5 pl-7">
                            <span className="text-xs text-gray-400 dark:text-slate-500">
                              {chapter.wordCount.toLocaleString()} 字
                            </span>
                            {isCurrentChapter && (
                              <span className="text-xs text-blue-500 dark:text-blue-400 font-medium">
                                阅读中
                              </span>
                            )}
                          </div>
                        </button>
                      );
                    })}
                  </div>
                );
              })()}
            </div>
          </div>
        </>
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
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm text-gray-700 dark:text-slate-300">
                  字体大小
                </label>
                <span className="text-sm text-gray-900 dark:text-white font-medium">{fontSize}px</span>
              </div>
              <input
                type="range"
                min={14}
                max={28}
                step={2}
                value={fontSize}
                onChange={(e) => setFontSize(Number(e.target.value))}
                className="w-full h-2 bg-gray-200 dark:bg-slate-600 rounded-lg appearance-none cursor-pointer accent-blue-500"
              />
              <div className="flex justify-between text-xs text-gray-500 dark:text-slate-400 mt-1">
                <span>14px</span>
                <span>28px</span>
              </div>
            </div>

            {/* 行高 */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm text-gray-700 dark:text-slate-300">
                  行高
                </label>
                <span className="text-sm text-gray-900 dark:text-white font-medium">{lineHeight}</span>
              </div>
              <input
                type="range"
                min={1.2}
                max={2.5}
                step={0.1}
                value={lineHeight}
                onChange={(e) => setLineHeight(Number(e.target.value))}
                className="w-full h-2 bg-gray-200 dark:bg-slate-600 rounded-lg appearance-none cursor-pointer accent-blue-500"
              />
              <div className="flex justify-between text-xs text-gray-500 dark:text-slate-400 mt-1">
                <span>1.2</span>
                <span>2.5</span>
              </div>
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
            <div className="max-w-none mb-12">
              <style>
                {`
                  .chapter-content {
                    font-size: ${fontSize}px;
                    line-height: ${lineHeight};
                    color: ${textColor};
                  }
                  .chapter-content p,
                  .chapter-content div,
                  .chapter-content span {
                    font-size: ${fontSize}px;
                    line-height: ${lineHeight};
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
            <div className="flex items-center justify-center gap-6 py-8 border-t border-gray-200 dark:border-slate-700">
              <button
                onClick={handlePrevChapter}
                disabled={!hasPrev}
                className="p-3 bg-white dark:bg-slate-800 rounded-full transition-colors disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-slate-700"
                style={{ color: textColor }}
                title="上一章"
              >
                <ChevronLeft className="w-6 h-6" />
              </button>

              <button
                onClick={handleNextChapter}
                disabled={!hasNext}
                className="p-3 bg-white dark:bg-slate-800 rounded-full transition-colors disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-slate-700"
                style={{ color: textColor }}
                title="下一章"
              >
                <ChevronRight className="w-6 h-6" />
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
