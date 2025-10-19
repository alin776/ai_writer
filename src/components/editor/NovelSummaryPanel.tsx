/**
 * 小说概括面板组件
 * 提供"小说概括"和"当前章节概括"两个选项
 */
import React, { useState, useEffect } from 'react';
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
        setNovelSummary('暂无小说概括，请先进行分析');
      }
    } catch (error: any) {
      const is404 = error?.status === 404 || error?.response?.status === 404;
      if (is404) {
        setNovelSummary('暂无小说概括，请先进行分析');
      } else {
        console.error('加载小说概括失败:', error);
        onToast('error', '加载小说概括失败');
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
      setChapterSummary('请先选择一个章节');
      return;
    }

    try {
      setIsLoadingChapter(true);
      
      // 获取章节详情
      const chapter = await DataService.getChapter(currentChapterId);
      
      if (!chapter || !chapter.content) {
        setChapterSummary('章节内容为空');
        return;
      }

      // 调用AI总结章节
      const summary = await DataService.summarizeChapter(chapter.content);
      setChapterSummary(summary);
    } catch (error: any) {
      console.error('加载章节概括失败:', error);
      setChapterSummary('加载失败，请重试');
      onToast('error', '加载章节概括失败');
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
            <p>加载小说概括中...</p>
          </div>
        );
      }

      return (
        <div className={styles.summaryContent}>
          {novelSummary || '暂无小说概括'}
        </div>
      );
    }

    // 章节概括
    if (isLoadingChapter) {
      return (
        <div className={styles.loadingContainer}>
          <Loading />
          <p>生成章节概括中...</p>
        </div>
      );
    }

    return (
      <div className={styles.summaryContent}>
        {chapterSummary || '请先选择一个章节'}
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
          <span>小说概括</span>
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'chapter' ? styles.active : ''}`}
          onClick={() => setActiveTab('chapter')}
        >
          <FileText size={16} />
          <span>当前章节概括</span>
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
          <span>刷新</span>
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
