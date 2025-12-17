import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Button } from '../ui/button';
import { Play, RefreshCw, Download, Loader2 } from 'lucide-react';
import { DataService } from '../../services/DataService';

interface SummaryPanelProps {
  workId: string;
  currentChapterId?: string;
  onToast: (type: 'success' | 'error' | 'warning' | 'info', message: string) => void;
}

export function SummaryPanel({ workId, currentChapterId, onToast }: SummaryPanelProps) {
  const { t } = useTranslation();
  const [summaryTab, setSummaryTab] = React.useState<'novel' | 'chapter'>('novel');

  // 小说概括状态
  const [novelSummary, setNovelSummary] = useState<string>('');
  const [isLoadingNovel, setIsLoadingNovel] = useState(false);

  // 章节概括状态
  const [chapterSummary, setChapterSummary] = useState<string>('');
  const [isLoadingChapter, setIsLoadingChapter] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  // 加载作品概括（通过获取所有章节的概括汇总）
  const loadNovelSummary = async () => {
    if (!workId) return;

    setIsLoadingNovel(true);
    try {
      // 获取所有章节
      const chapters = await DataService.getChapters(workId);

      // 收集所有章节概括
      const summaries = chapters
        .filter(ch => ch.summary)
        .map((ch, idx) => `${t('editor.summary.chapterNum', { num: idx + 1 })}${ch.summary}`)
        .join('\n\n');

      if (summaries) {
        setNovelSummary(summaries);
      } else {
        setNovelSummary(t('editor.summary.noChapterSummary'));
      }
    } catch (error) {
      console.error('Failed to load novel summary:', error);
      onToast('error', t('editor.summary.loadNovelFailed'));
      setNovelSummary(t('editor.summary.loadFailed'));
    } finally {
      setIsLoadingNovel(false);
    }
  };

  // 加载章节概括
  const loadChapterSummary = async () => {
    if (!currentChapterId) return;

    setIsLoadingChapter(true);
    try {
      const chapter = await DataService.getChapter(currentChapterId);
      setChapterSummary(chapter.summary || t('editor.summary.noSummaryClickGenerate'));
    } catch (error) {
      console.error('Failed to load chapter summary:', error);
      onToast('error', t('editor.summary.loadChapterFailed'));
      setChapterSummary(t('editor.summary.loadFailed'));
    } finally {
      setIsLoadingChapter(false);
    }
  };

  // 生成/重新生成章节概括
  const generateChapterSummary = async (regenerate: boolean = false) => {
    if (!currentChapterId) return;

    setIsGenerating(true);
    try {
      const summary = await DataService.generateChapterSummary(currentChapterId, regenerate);
      setChapterSummary(summary);
      onToast('success', regenerate ? t('editor.summary.regenerateSuccess') : t('editor.summary.generateSuccess'));

      // 如果在小说概括标签，也刷新小说概括
      if (summaryTab === 'novel') {
        loadNovelSummary();
      }
    } catch (error) {
      console.error('Failed to generate chapter summary:', error);
      onToast('error', t('editor.summary.generateFailed'));
    } finally {
      setIsGenerating(false);
    }
  };

  // 获取世界观（批量生成所有章节概括）
  const handleGetWorldview = async () => {
    if (!workId) return;

    setIsLoadingNovel(true);
    try {
      const chapters = await DataService.getChapters(workId);
      const chaptersWithoutSummary = chapters.filter(ch => !ch.summary);

      if (chaptersWithoutSummary.length === 0) {
        onToast('info', t('editor.summary.allChaptersHaveSummary'));
        loadNovelSummary();
        return;
      }

      onToast('info', t('editor.summary.startGenerating', { count: chaptersWithoutSummary.length }));

      // 批量生成概括
      for (const chapter of chaptersWithoutSummary) {
        await DataService.generateChapterSummary(chapter.id, false);
      }

      onToast('success', t('editor.summary.allChaptersComplete'));
      loadNovelSummary();
    } catch (error) {
      console.error('Failed to get worldview:', error);
      onToast('error', t('editor.summary.getWorldviewFailed'));
    } finally {
      setIsLoadingNovel(false);
    }
  };

  // 切换标签时加载数据
  useEffect(() => {
    if (summaryTab === 'novel') {
      loadNovelSummary();
    } else if (summaryTab === 'chapter' && currentChapterId) {
      loadChapterSummary();
    }
  }, [summaryTab, currentChapterId]);

  return (
    <div className="flex flex-col h-full bg-white dark:bg-slate-900">
      {/* 子标签 - 简约设计 */}
      <div className="flex items-center gap-1.5 px-3 py-2 border-b border-zinc-100 dark:border-zinc-700 bg-zinc-50 dark:bg-slate-800">
        <button
          onClick={() => setSummaryTab('novel')}
          className={`px-2.5 py-1 rounded-md text-[11px] transition-all duration-200 ${
            summaryTab === 'novel'
              ? 'bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900'
              : 'text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-zinc-100'
          }`}
        >
          {t('editor.summary.novelSummary')}
        </button>
        <button
          onClick={() => setSummaryTab('chapter')}
          className={`px-2.5 py-1 rounded-md text-[11px] transition-all duration-200 ${
            summaryTab === 'chapter'
              ? 'bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900'
              : 'text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-zinc-100'
          }`}
        >
          {t('editor.summary.currentChapter')}
        </button>
      </div>

      {/* 内容区域 */}
      <div className="flex-1 flex flex-col p-3 overflow-y-auto custom-scrollbar bg-white dark:bg-slate-900">
        {summaryTab === 'novel' && (
          <>
            {/* 概括内容 */}
            <div className="flex-1 p-3 rounded-lg bg-zinc-50/70 border border-zinc-100 mb-2.5 overflow-y-auto custom-scrollbar dark:bg-zinc-800/70 dark:border-zinc-700">
              {isLoadingNovel ? (
                <div className="flex items-center justify-center h-full">
                  <Loader2 className="h-5 w-5 animate-spin text-zinc-400 dark:text-zinc-500" />
                </div>
              ) : (
                <p className="text-[11px] text-zinc-600 leading-[1.7] whitespace-pre-wrap dark:text-zinc-300">
                  {novelSummary || t('editor.summary.noNovelSummary')}
                </p>
              )}
            </div>

            {/* 操作按钮 - 重新布局 */}
            <div className="space-y-1.5">
              <Button
                size="sm"
                onClick={() => loadNovelSummary()}
                disabled={isLoadingNovel}
                className="w-full h-8 text-[11px] bg-zinc-100 hover:bg-zinc-200 text-zinc-700 transition-all border border-zinc-200 dark:bg-zinc-800 dark:hover:bg-zinc-700 dark:text-zinc-300 dark:border-zinc-600"
              >
                {isLoadingNovel ? (
                  <Loader2 className="h-3.5 w-3.5 mr-1.5 animate-spin" />
                ) : (
                  <Play className="h-3.5 w-3.5 mr-1.5" />
                )}
                {t('editor.summary.regenerate')}
              </Button>
              <div className="flex gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => loadNovelSummary()}
                  disabled={isLoadingNovel}
                  className="flex-1 h-7 text-[11px] text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100 transition-all dark:text-zinc-400 dark:hover:text-zinc-100 dark:hover:bg-zinc-800"
                >
                  <RefreshCw className="h-3 w-3 mr-1" />
                  {t('editor.summary.refresh')}
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleGetWorldview}
                  disabled={isLoadingNovel}
                  className="flex-1 h-7 text-[11px] text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100 transition-all dark:text-zinc-400 dark:hover:text-zinc-100 dark:hover:bg-zinc-800"
                >
                  {isLoadingNovel ? (
                    <Loader2 className="h-3 w-3 mr-1 animate-spin" />
                  ) : (
                    <Download className="h-3 w-3 mr-1" />
                  )}
                  {t('editor.summary.getWorldview')}
                </Button>
              </div>
            </div>
          </>
        )}

        {summaryTab === 'chapter' && (
          <>
            {/* 概括内容 */}
            <div className="flex-1 p-3 rounded-lg bg-zinc-50/70 border border-zinc-100 mb-2.5 overflow-y-auto custom-scrollbar dark:bg-zinc-800/70 dark:border-zinc-700">
              {isLoadingChapter ? (
                <div className="flex items-center justify-center h-full">
                  <Loader2 className="h-5 w-5 animate-spin text-zinc-400 dark:text-zinc-500" />
                </div>
              ) : (
                <p className="text-[11px] text-zinc-600 leading-[1.7] whitespace-pre-wrap dark:text-zinc-300">
                  {currentChapterId
                    ? chapterSummary || t('editor.summary.noSummaryClickGenerate')
                    : t('editor.summary.selectChapterToView')}
                </p>
              )}
            </div>

            {/* 生成按钮 */}
            <div className="space-y-1.5">
              <Button
                size="sm"
                onClick={() => generateChapterSummary(false)}
                disabled={!currentChapterId || isGenerating || isLoadingChapter}
                className="w-full h-8 text-[11px] bg-zinc-100 hover:bg-zinc-200 text-zinc-700 transition-all border border-zinc-200 dark:bg-zinc-800 dark:hover:bg-zinc-700 dark:text-zinc-300 dark:border-zinc-600"
              >
                {isGenerating ? (
                  <Loader2 className="h-3.5 w-3.5 mr-1.5 animate-spin" />
                ) : (
                  <Play className="h-3.5 w-3.5 mr-1.5" />
                )}
                {t('editor.summary.generateSummary')}
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => generateChapterSummary(true)}
                disabled={!currentChapterId || isGenerating || isLoadingChapter || !chapterSummary}
                className="w-full h-7 text-[11px] text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100 transition-all dark:text-zinc-400 dark:hover:text-zinc-100 dark:hover:bg-zinc-800"
              >
                <RefreshCw className="h-3 w-3 mr-1" />
                {t('editor.summary.regenerate')}
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
