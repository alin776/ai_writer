import { useState, useEffect, useRef, useCallback } from 'react';
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
  MessageCircle,
} from 'lucide-react';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import { useTheme } from '../../hooks/useTheme';
import { useWorkNavStore } from '../../store/workNavStore';
import { useContentParser, ParsedParagraph } from '../../hooks/useContentParser';
import { CommentBadge } from './CommentBadge';
import { ReaderContextMenu } from './ReaderContextMenu';
import { ChapterCommentPanel } from './ChapterCommentPanel';
import { chapterCommentApi, CommentLocationStats } from '../../services/chapterCommentApi';

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
  const [contentWidth, setContentWidth] = useState(720); // 内容宽度，单位 px

  // 评论相关状态
  const [showCommentPanel, setShowCommentPanel] = useState(false);
  const [commentStats, setCommentStats] = useState<CommentLocationStats | null>(null);
  const [commentFilter, setCommentFilter] = useState<{
    type: 'all' | 'paragraph' | 'sentence';
    paragraphIndex?: number;
    sentenceIndex?: number;
    quotedText?: string;
  }>({ type: 'all' });

  // 右键菜单状态
  const [contextMenu, setContextMenu] = useState<{
    show: boolean;
    x: number;
    y: number;
    paragraphIndex: number;
    sentenceIndex?: number;
    selectedText: string;
    quotedText: string;
  } | null>(null);

  // 高亮句子状态
  const [highlightedSentence, setHighlightedSentence] = useState<{
    paragraphIndex: number;
    sentenceIndex: number;
  } | null>(null);

  // 预设主题 - 第一个改为渐变暖色
  const themes = [
    { name: '暖阳', bg: 'linear-gradient(to bottom right, #fffbeb, #fff7ed, #fff1f2)', text: '#1f2937', darkBg: '#2a2a2a', darkText: '#d4d4d4', isGradient: true },
    { name: '夜间', bg: '#1a1a1a', text: '#e0e0e0', darkBg: '#0d0d0d', darkText: '#e8e8e8', isGradient: false },
    { name: '纯白', bg: '#ffffff', text: '#1f2937', darkBg: '#1f1f1f', darkText: '#ffffff', isGradient: false },
    { name: '羊皮纸', bg: '#f4ecd8', text: '#1f2937', darkBg: '#3a3428', darkText: '#d4c4a8', isGradient: false },
  ];

  // 根据深色模式自动选择主题
  const [selectedThemeIndex, setSelectedThemeIndex] = useState(0);
  const currentTheme = themes[selectedThemeIndex];
  const isGradientBg = !isDarkMode && currentTheme.isGradient;
  const backgroundColor = isDarkMode ? currentTheme.darkBg : (isGradientBg ? '#fffbeb' : currentTheme.bg);
  const backgroundStyle = isDarkMode
    ? { backgroundColor: currentTheme.darkBg }
    : (isGradientBg ? { background: currentTheme.bg } : { backgroundColor: currentTheme.bg });
  const textColor = isDarkMode ? currentTheme.darkText : currentTheme.text;

  // 解析章节内容为结构化段落和句子
  const { paragraphs: parsedParagraphs } = useContentParser(
    currentChapter?.content || '',
    commentStats
  );

  // 加载评论统计
  const loadCommentStats = useCallback(async (chapterId: string) => {
    try {
      const stats = await chapterCommentApi.getStats(chapterId);
      setCommentStats(stats);
    } catch (err) {
      console.error('加载评论统计失败:', err);
    }
  }, []);

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

      // 加载评论统计
      loadCommentStats(targetChapterId);
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

  // 右键菜单处理
  const handleContextMenu = (
    e: React.MouseEvent,
    paragraphIndex: number,
    sentenceIndex?: number,
    sentenceText?: string
  ) => {
    e.preventDefault();
    e.stopPropagation();

    const selection = window.getSelection();
    const selectedText = selection?.toString().trim() || '';

    // 高亮当前句子
    if (sentenceIndex !== undefined) {
      setHighlightedSentence({ paragraphIndex, sentenceIndex });
    }

    setContextMenu({
      show: true,
      x: e.clientX,
      y: e.clientY,
      paragraphIndex,
      sentenceIndex,
      selectedText,
      quotedText: sentenceText || '',
    });
  };

  // 关闭右键菜单
  const closeContextMenu = () => {
    setContextMenu(null);
    setHighlightedSentence(null);
  };

  // 复制文本
  const handleCopy = () => {
    if (contextMenu?.selectedText) {
      navigator.clipboard.writeText(contextMenu.selectedText);
    }
  };

  // 评论句子
  const handleCommentSentence = () => {
    if (contextMenu && contextMenu.sentenceIndex !== undefined) {
      setCommentFilter({
        type: 'sentence',
        paragraphIndex: contextMenu.paragraphIndex,
        sentenceIndex: contextMenu.sentenceIndex,
        quotedText: contextMenu.quotedText,
      });
      setShowCommentPanel(true);
    }
  };

  // 评论段落
  const handleCommentParagraph = () => {
    if (contextMenu) {
      // 获取段落文本
      const paragraph = parsedParagraphs[contextMenu.paragraphIndex];
      const paragraphText = paragraph?.sentences.map(s => s.text).join('') || '';
      setCommentFilter({
        type: 'paragraph',
        paragraphIndex: contextMenu.paragraphIndex,
        quotedText: paragraphText,
      });
      setShowCommentPanel(true);
    }
  };

  // 点击评论标记
  const handleBadgeClick = (paragraphIndex: number, sentenceIndex?: number, quotedText?: string) => {
    if (sentenceIndex !== undefined) {
      setCommentFilter({
        type: 'sentence',
        paragraphIndex,
        sentenceIndex,
        quotedText,
      });
    } else {
      // 获取段落文本
      const paragraph = parsedParagraphs[paragraphIndex];
      const paragraphText = paragraph?.sentences.map(s => s.text).join('') || '';
      setCommentFilter({
        type: 'paragraph',
        paragraphIndex,
        quotedText: paragraphText,
      });
    }
    setShowCommentPanel(true);
  };

  // 打开全部评论
  const openAllComments = () => {
    setCommentFilter({ type: 'all' });
    setShowCommentPanel(true);
  };

  // 更新评论统计
  const handleStatsUpdate = (stats: CommentLocationStats) => {
    setCommentStats(stats);
  };

  // 渲染段落内容
  const renderParagraphContent = (paragraph: ParsedParagraph) => {
    // 获取段落评论数
    const paragraphCommentCount = commentStats?.paragraphs[String(paragraph.index)] || 0;

    return (
      <div
        key={paragraph.index}
        data-paragraph-index={paragraph.index}
        className="relative group"
        style={{
          marginBottom: '1.5em',
          textIndent: '2em',
          textAlign: 'justify',
        }}
        onContextMenu={(e) => handleContextMenu(e, paragraph.index)}
      >
        {paragraph.sentences.map((sentence, sIndex) => {
          const isHighlighted =
            highlightedSentence?.paragraphIndex === paragraph.index &&
            highlightedSentence?.sentenceIndex === sIndex;

          // 获取句子评论数
          const sentenceKey = `${paragraph.index}-${sIndex}`;
          const sentenceCommentCount = commentStats?.sentences[sentenceKey] || 0;

          return (
            <span
              key={sIndex}
              data-paragraph-index={paragraph.index}
              data-sentence-index={sIndex}
              className={`${isHighlighted ? 'bg-yellow-200 dark:bg-yellow-800/50' : ''}`}
              onContextMenu={(e) => handleContextMenu(e, paragraph.index, sIndex, sentence.text)}
            >
              {sentence.text}
              {sentenceCommentCount > 0 && (
                <CommentBadge
                  count={sentenceCommentCount}
                  size="sm"
                  onClick={() => handleBadgeClick(paragraph.index, sIndex, sentence.text)}
                />
              )}
            </span>
          );
        })}

        {/* 段落末尾的评论标记（仅段落级别的评论） */}
        {paragraphCommentCount > 0 && (
          <CommentBadge
            count={paragraphCommentCount}
            size="md"
            className="absolute -right-2 -top-4"
            onClick={() => handleBadgeClick(paragraph.index)}
          />
        )}
      </div>
    );
  };

  const currentIndex = currentChapter ? chapters.findIndex((c) => c.id === currentChapter.id) : -1;
  const hasPrev = currentIndex > 0;
  const hasNext = currentIndex < chapters.length - 1;

  // 计算是否有侧边面板打开
  const hasSidePanel = showChapterList || showCommentPanel;

  return (
    <div className="min-h-screen flex" style={backgroundStyle}>
      {/* 主内容区域 - 面板打开时收缩 */}
      <div
        className={`flex-1 min-w-0 transition-all duration-300 ease-in-out ${
          hasSidePanel ? 'mr-96' : 'mr-0'
        }`}
      >
      {/* 顶部导航栏 - 透明背景 */}
      <div className="sticky top-0 z-10">
        <div className="px-8 py-4 flex items-center justify-between">
          <button
            onClick={onBack}
            className="flex items-center gap-2 transition-colors hover:opacity-70"
            style={{ color: textColor }}
          >
            <ArrowLeft className="w-5 h-5" />
            <span className="text-sm">返回</span>
          </button>

          <div className="flex items-center gap-6">
            <button
              onClick={openAllComments}
              className="p-2 transition-colors hover:opacity-70 relative"
              style={{ color: textColor }}
              title="章节评论"
            >
              <MessageCircle className="w-5 h-5" />
              {commentStats && commentStats.total > 0 && (
                <span className="absolute -top-0.5 -right-0.5 min-w-[16px] h-4 px-1 bg-blue-500 text-white text-[10px] font-medium rounded-full flex items-center justify-center">
                  {commentStats.total > 99 ? '99+' : commentStats.total}
                </span>
              )}
            </button>
            <button
              onClick={() => setShowChapterList(!showChapterList)}
              className="p-2 transition-colors hover:opacity-70"
              style={{ color: textColor }}
              title="章节列表"
            >
              <Menu className="w-5 h-5" />
            </button>
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 transition-colors hover:opacity-70"
              style={{ color: textColor }}
              title="阅读设置"
            >
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* 阅读内容区域 */}
      <div className="mx-auto px-6 py-8" style={{ maxWidth: `${contentWidth}px` }}>
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
                className="text-3xl font-bold mb-2"
                style={{ color: textColor }}
              >
                {currentChapter.title}
              </h1>
              <div className="text-xs opacity-60" style={{ color: textColor }}>
                第 {currentChapter.order} 章 · {currentChapter.wordCount} 字
              </div>
            </div>

            {/* 章节内容 */}
            <div
              className="max-w-none mb-12 chapter-content"
              style={{
                fontSize: `${fontSize}px`,
                lineHeight: lineHeight,
                color: textColor,
                fontWeight: 500,
              }}
              onContextMenu={(e) => {
                const target = e.target as HTMLElement;
                if (!target.dataset.paragraphIndex) {
                  e.preventDefault();
                }
              }}
            >
              {parsedParagraphs.length > 0 ? (
                parsedParagraphs.map(paragraph => renderParagraphContent(paragraph))
              ) : (
                <div dangerouslySetInnerHTML={{ __html: currentChapter.content }} />
              )}
            </div>

            {/* 底部翻页按钮 */}
            <div
              className="flex items-center justify-center gap-6 py-8 border-t"
              style={{ borderColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)' }}
            >
              <button
                onClick={handlePrevChapter}
                disabled={!hasPrev}
                className="p-3 rounded-full transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                style={{
                  backgroundColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)',
                  color: textColor,
                }}
                title="上一章"
              >
                <ChevronLeft className="w-6 h-6" />
              </button>

              <button
                onClick={handleNextChapter}
                disabled={!hasNext}
                className="p-3 rounded-full transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                style={{
                  backgroundColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)',
                  color: textColor,
                }}
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

      {/* 主内容区域结束 */}
      </div>

      {/* 右侧面板区域 - 章节列表或评论面板 */}
      <div
        className={`fixed top-[52px] right-0 bottom-0 w-96 z-20 transition-transform duration-300 ease-in-out ${
          hasSidePanel ? 'translate-x-0' : 'translate-x-full'
        }`}
        style={{ backgroundColor }}
      >
        {/* 章节列表面板 */}
        {showChapterList && (
          <div
            className="h-full flex flex-col border-l transition-colors"
            style={{
              borderColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)',
              backgroundColor: isDarkMode ? 'rgba(0,0,0,0.3)' : 'rgba(255,255,255,0.85)',
              backdropFilter: 'blur(12px)',
            }}
          >
            {/* 头部 */}
            <div
              className="flex-shrink-0 p-4 border-b"
              style={{
                borderColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)',
                backgroundColor: isDarkMode ? 'rgba(0,0,0,0.2)' : 'rgba(255,255,255,0.5)',
              }}
            >
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-base font-bold flex items-center gap-2" style={{ color: textColor }}>
                  <BookOpen className="w-4 h-4 text-blue-500" />
                  章节目录
                </h2>
                <button
                  onClick={() => setShowChapterList(false)}
                  className="p-1.5 rounded-full transition-colors hover:bg-black/10 dark:hover:bg-white/10"
                  style={{ color: textColor }}
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              {/* 搜索框 */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 opacity-50" style={{ color: textColor }} />
                <input
                  type="text"
                  placeholder="搜索章节..."
                  value={chapterSearchQuery}
                  onChange={(e) => setChapterSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-8 py-2 text-sm rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
                  style={{
                    backgroundColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)',
                    borderColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
                    color: textColor,
                  }}
                />
                {chapterSearchQuery && (
                  <button
                    onClick={() => setChapterSearchQuery('')}
                    className="absolute right-3 top-1/2 -translate-y-1/2 opacity-50 hover:opacity-100 transition-opacity"
                    style={{ color: textColor }}
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
              {/* 当前阅读位置提示 */}
              <div className="flex items-center justify-between mt-3">
                {currentChapter && (
                  <p className="text-xs text-blue-500">
                    当前：第 {currentChapter.order} 章
                  </p>
                )}
                <span
                  className="text-xs px-2 py-0.5 rounded-full"
                  style={{
                    backgroundColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)',
                    color: textColor,
                    opacity: 0.7,
                  }}
                >
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
                    <div className="flex flex-col items-center justify-center py-12 opacity-50" style={{ color: textColor }}>
                      <Search className="w-8 h-8 mb-2" />
                      <p className="text-sm">未找到匹配的章节</p>
                    </div>
                  );
                }

                return (
                  <div>
                    {filteredChapters.map((chapter) => {
                      const isCurrentChapter = currentChapter?.id === chapter.id;
                      return (
                        <button
                          key={chapter.id}
                          onClick={() => handleSelectChapter(chapter.id)}
                          className={`w-full text-left px-4 py-3 transition-all border-b ${
                            isCurrentChapter
                              ? 'border-l-4 border-l-blue-500'
                              : 'border-l-4 border-l-transparent hover:border-l-blue-300'
                          }`}
                          style={{
                            backgroundColor: isCurrentChapter
                              ? (isDarkMode ? 'rgba(59,130,246,0.15)' : 'rgba(59,130,246,0.1)')
                              : 'transparent',
                            borderBottomColor: isDarkMode ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)',
                          }}
                        >
                          <div className="flex items-center gap-2">
                            <span
                              className="text-xs font-medium px-1.5 py-0.5 rounded"
                              style={{
                                backgroundColor: isCurrentChapter
                                  ? '#3b82f6'
                                  : (isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)'),
                                color: isCurrentChapter ? '#fff' : textColor,
                                opacity: isCurrentChapter ? 1 : 0.7,
                              }}
                            >
                              {chapter.order}
                            </span>
                            <span
                              className={`text-sm truncate flex-1 ${isCurrentChapter ? 'font-medium' : ''}`}
                              style={{
                                color: isCurrentChapter ? '#3b82f6' : textColor,
                              }}
                            >
                              {chapter.title}
                            </span>
                          </div>
                          <div className="flex items-center justify-between mt-1.5 pl-7">
                            <span className="text-xs opacity-50" style={{ color: textColor }}>
                              {chapter.wordCount.toLocaleString()} 字
                            </span>
                            {isCurrentChapter && (
                              <span className="text-xs text-blue-500 font-medium">
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
        )}

        {/* 评论面板 - 集成到右侧面板区域 */}
        {currentChapter && showCommentPanel && (
          <ChapterCommentPanel
            chapterId={currentChapter.id}
            isOpen={showCommentPanel}
            onClose={() => setShowCommentPanel(false)}
            filter={commentFilter}
            onStatsUpdate={handleStatsUpdate}
            themeColors={{
              backgroundColor,
              textColor,
              isDarkMode,
            }}
          />
        )}
      </div>

      {/* 阅读设置面板 - 使用固定定位的模态框 */}
      {showSettings && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div
            className="rounded-2xl shadow-2xl w-full max-w-md mx-4 p-6"
            style={{
              backgroundColor: isDarkMode ? 'rgba(30,30,30,0.95)' : 'rgba(255,255,255,0.95)',
              backdropFilter: 'blur(12px)',
            }}
          >
            <h2 className="text-lg font-bold mb-4" style={{ color: textColor }}>
              阅读设置
            </h2>

            {/* 字体大小 */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm" style={{ color: textColor, opacity: 0.8 }}>
                  字体大小
                </label>
                <span className="text-sm font-medium" style={{ color: textColor }}>{fontSize}px</span>
              </div>
              <input
                type="range"
                min={14}
                max={28}
                step={2}
                value={fontSize}
                onChange={(e) => setFontSize(Number(e.target.value))}
                className="w-full h-2 rounded-lg appearance-none cursor-pointer accent-blue-500"
                style={{
                  backgroundColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
                }}
              />
              <div className="flex justify-between text-xs mt-1" style={{ color: textColor, opacity: 0.5 }}>
                <span>14px</span>
                <span>28px</span>
              </div>
            </div>

            {/* 行高 */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm" style={{ color: textColor, opacity: 0.8 }}>
                  行高
                </label>
                <span className="text-sm font-medium" style={{ color: textColor }}>{lineHeight}</span>
              </div>
              <input
                type="range"
                min={1.2}
                max={2.5}
                step={0.1}
                value={lineHeight}
                onChange={(e) => setLineHeight(Number(e.target.value))}
                className="w-full h-2 rounded-lg appearance-none cursor-pointer accent-blue-500"
                style={{
                  backgroundColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
                }}
              />
              <div className="flex justify-between text-xs mt-1" style={{ color: textColor, opacity: 0.5 }}>
                <span>1.2</span>
                <span>2.5</span>
              </div>
            </div>

            {/* 内容宽度 */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm" style={{ color: textColor, opacity: 0.8 }}>
                  内容宽度
                </label>
                <span className="text-sm font-medium" style={{ color: textColor }}>{contentWidth}px</span>
              </div>
              <input
                type="range"
                min={480}
                max={1200}
                step={40}
                value={contentWidth}
                onChange={(e) => setContentWidth(Number(e.target.value))}
                className="w-full h-2 rounded-lg appearance-none cursor-pointer accent-blue-500"
                style={{
                  backgroundColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
                }}
              />
              <div className="flex justify-between text-xs mt-1" style={{ color: textColor, opacity: 0.5 }}>
                <span>窄</span>
                <span>宽</span>
              </div>
            </div>

            {/* 主题 */}
            <div className="mb-6">
              <label className="text-sm mb-3 block" style={{ color: textColor, opacity: 0.8 }}>
                阅读主题
              </label>
              <div className="grid grid-cols-4 gap-3">
                {themes.map((theme, index) => (
                  <button
                    key={theme.name}
                    onClick={() => applyTheme(index)}
                    className="px-3 py-2.5 text-sm rounded-lg border-2 transition-all shadow-sm"
                    style={{
                      ...(isDarkMode
                        ? { backgroundColor: theme.darkBg }
                        : (theme.isGradient ? { background: theme.bg } : { backgroundColor: theme.bg })),
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
              className="w-full px-4 py-2.5 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium"
            >
              完成
            </button>
          </div>
        </div>
      )}

      {/* 右键菜单 */}
      {contextMenu?.show && (
        <ReaderContextMenu
          x={contextMenu.x}
          y={contextMenu.y}
          selectedText={contextMenu.selectedText}
          paragraphIndex={contextMenu.paragraphIndex}
          sentenceIndex={contextMenu.sentenceIndex}
          onClose={closeContextMenu}
          onCopy={handleCopy}
          onCommentSentence={handleCommentSentence}
          onCommentParagraph={handleCommentParagraph}
        />
      )}
    </div>
  );
}
