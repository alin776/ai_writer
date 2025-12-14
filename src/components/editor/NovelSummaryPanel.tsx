/**
 * 小说概括面板组件
 * 提供"小说概括"和"当前章节概括"两个选项
 */
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Button, Loading } from '../common';
import { DataService } from '@/services/DataService';
import { BookOpen, FileText, RefreshCw } from 'lucide-react';
import styles from './NovelSummaryPanel.module.css';

interface NovelSummaryPanelProps {
  workId: string;
  currentChapterId?: string;
  onToast: (type: 'success' | 'error' | 'warning' | 'info', message: string) => void;
}

type TabType = 'novel' | 'chapter';

const NovelSummaryPanel: React.FC<NovelSummaryPanelProps> = ({
  workId,
  currentChapterId,
  onToast
}) => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<TabType>('novel');
  const [novelSummary, setNovelSummary] = useState<string>('');
  const [chapterSummary, setChapterSummary] = useState<string>('');
  const [isLoadingNovel, setIsLoadingNovel] = useState(false);
  const [isLoadingChapter, setIsLoadingChapter] = useState(false);

  /**
   * 加载小说概括
   */
  const loadNovelSummary = async () => {
    try {
      setIsLoadingNovel(true);
      const result = await DataService.getAnalysisResult(workId);
      
      if (result && result.macroResults) {
        // 提取纯文本概括，移除多余的标题
        const summary = extractSummary(result.macroResults);
        setNovelSummary(summary);
      } else {
        setNovelSummary(t('editor.novelSummary.noSummaryAnalyze'));
      }
    } catch (error: any) {
      const is404 = error?.status === 404 || error?.response?.status === 404;
      if (is404) {
        setNovelSummary(t('editor.novelSummary.noSummaryAnalyze'));
      } else {
        console.error('Failed to load novel summary:', error);
        onToast('error', t('editor.novelSummary.loadNovelFailed'));
      }
    } finally {
      setIsLoadingNovel(false);
    }
  };

  /**
   * 加载当前章节概括
   */
  const loadChapterSummary = async () => {
    if (!currentChapterId) {
      setChapterSummary(t('editor.novelSummary.selectChapterFirst'));
      return;
    }

    try {
      setIsLoadingChapter(true);

      // 获取章节详情
      const chapter = await DataService.getChapter(currentChapterId);

      if (!chapter || !chapter.content) {
        setChapterSummary(t('editor.novelSummary.chapterEmpty'));
        return;
      }

      // 调用AI总结章节
      const summary = await DataService.summarizeChapter(chapter.content);
      setChapterSummary(summary);
    } catch (error: any) {
      console.error('Failed to load chapter summary:', error);
      setChapterSummary(t('editor.novelSummary.loadFailedRetry'));
      onToast('error', t('editor.novelSummary.loadChapterFailed'));
    } finally {
      setIsLoadingChapter(false);
    }
  };

  /**
   * 提取纯文本概括（去除标题和说明）
   */
  const extractSummary = (text: string): string => {
    if (!text) return '';
    
    // 简单处理：返回完整文本
    // 如果需要进一步处理，可以在这里添加逻辑
    return text.trim();
  };

  /**
   * 初始加载
   */
  useEffect(() => {
    if (activeTab === 'novel') {
      loadNovelSummary();
    }
  }, [activeTab, workId]);

  /**
   * 当切换到章节概括或章节ID变化时加载
   */
  useEffect(() => {
    if (activeTab === 'chapter') {
      loadChapterSummary();
    }
  }, [activeTab, currentChapterId]);

  /**
   * 渲染内容
   */
  const renderContent = () => {
    if (activeTab === 'novel') {
      if (isLoadingNovel) {
        return (
          <div className={styles.loadingContainer}>
            <Loading />
            <p>{t('editor.novelSummary.loadingNovelSummary')}</p>
          </div>
        );
      }

      return (
        <div className={styles.summaryContent}>
          {novelSummary || t('editor.novelSummary.noNovelSummary')}
        </div>
      );
    }

    // 章节概括
    if (isLoadingChapter) {
      return (
        <div className={styles.loadingContainer}>
          <Loading />
          <p>{t('editor.novelSummary.generatingChapterSummary')}</p>
        </div>
      );
    }

    return (
      <div className={styles.summaryContent}>
        {chapterSummary || t('editor.novelSummary.selectChapterFirst')}
      </div>
    );
  };

  return (
    <div className={styles.container}>
      {/* 标签切换 */}
      <div className={styles.tabs}>
        <button
          className={`${styles.tab} ${activeTab === 'novel' ? styles.active : ''}`}
          onClick={() => setActiveTab('novel')}
        >
          <BookOpen size={16} />
          <span>{t('editor.novelSummary.novelSummary')}</span>
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'chapter' ? styles.active : ''}`}
          onClick={() => setActiveTab('chapter')}
        >
          <FileText size={16} />
          <span>{t('editor.novelSummary.currentChapterSummary')}</span>
        </button>
      </div>

      {/* 刷新按钮 */}
      <div className={styles.actions}>
        <Button
          onClick={activeTab === 'novel' ? loadNovelSummary : loadChapterSummary}
          variant="outline"
          size="sm"
          disabled={isLoadingNovel || isLoadingChapter}
        >
          <RefreshCw size={16} className={isLoadingNovel || isLoadingChapter ? styles.spinning : ''} />
          <span>{t('editor.novelSummary.refresh')}</span>
        </Button>
      </div>

      {/* 内容区域 */}
      <div className={styles.content}>
        {renderContent()}
      </div>
    </div>
  );
};

export default NovelSummaryPanel;
