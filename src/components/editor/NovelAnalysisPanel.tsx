/**
 * 小说概括面板组件
 * 提供"小说概括"和"当前章节概括"两个选项
 */
import React, { useState, useEffect } from 'react';
import { Button, Loading } from '../common';
import { DataService } from '@/services/DataService';
import {
  NovelAnalysisStatus,
  AnalysisStage,
  AnalysisStatusResponse,
  AnalysisResultResponse,
} from '@/types';
import { BookOpen, FileText, RefreshCw, PlayCircle, Download } from 'lucide-react';
import styles from './NovelAnalysisPanel.module.css';

interface NovelAnalysisPanelProps {
  workId: string;
  currentChapterId?: string;
  onToast: (type: 'success' | 'error' | 'warning' | 'info', message: string) => void;
}

type TabType = 'novel' | 'chapter';

const NovelAnalysisPanel: React.FC<NovelAnalysisPanelProps> = ({ 
  workId, 
  currentChapterId,
  onToast 
}) => {
  // 标签切换状态
  const [activeTab, setActiveTab] = useState<TabType>('novel');
  
  // 小说概括
  const [novelSummary, setNovelSummary] = useState<string>('');
  const [isLoadingNovel, setIsLoadingNovel] = useState(false);
  
  // 章节概括
  const [chapterSummary, setChapterSummary] = useState<string>('');
  const [isLoadingChapter, setIsLoadingChapter] = useState(false);
  
  // 保留原有状态（用于显示分析按钮）
  const [hasAnalysis, setHasAnalysis] = useState(false);
  
  // 世界观提取状态
  const [isExtractingWorldview, setIsExtractingWorldview] = useState(false);

  /**
   * 加载小说概括
   */
  const loadNovelSummary = async () => {
    try {
      setIsLoadingNovel(true);
      const result = await DataService.getAnalysisResult(workId);
      
      console.log('[NovelAnalysisPanel] 分析结果:', result);
      console.log('[NovelAnalysisPanel] macroResults:', result?.macroResults);
      console.log('[NovelAnalysisPanel] 结果字段:', Object.keys(result || {}));
      
      if (result && result.macroResults) {
        console.log('[NovelAnalysisPanel] 设置概括内容, 长度:', result.macroResults.length);
        setNovelSummary(result.macroResults);
        setHasAnalysis(true);
      } else {
        console.log('[NovelAnalysisPanel] 没有macroResults字段');
        setNovelSummary('暂无小说概括，请先点击下方"生成概括"按钮');
        setHasAnalysis(false);
      }
    } catch (error: any) {
      const is404 = error?.status === 404 || error?.response?.status === 404;
      if (is404) {
        setNovelSummary('暂无小说概括，请先点击下方"生成概括"按钮');
        setHasAnalysis(false);
      } else {
        console.error('加载小说概括失败:', error);
        onToast('error', '加载小说概括失败');
      }
    } finally {
      setIsLoadingNovel(false);
    }
  };

  /**
   * 加载/生成当前章节概括
   */
  const loadChapterSummary = async (forceRegenerate: boolean = false) => {
    if (!currentChapterId) {
      setChapterSummary('请先选择一个章节');
      onToast('warning', '请先选择一个章节');
      return;
    }

    try {
      setIsLoadingChapter(true);
      
      // 先获取章节详情，检查是否已有概括
      const chapter = await DataService.getChapter(currentChapterId);
      
      if (!chapter) {
        setChapterSummary('章节不存在');
        onToast('error', '章节不存在');
        return;
      }

      if (!chapter.content || chapter.content.trim().length === 0) {
        setChapterSummary('章节内容为空，无法生成概括');
        onToast('warning', '章节内容为空');
        return;
      }

      // 如果已有概括且不强制重新生成，直接显示
      if (chapter.summary && !forceRegenerate) {
        console.log('[NovelAnalysisPanel] 使用已有概括');
        setChapterSummary(chapter.summary);
        return;
      }

      // 如果没有概括且不强制生成，显示提示
      if (!chapter.summary && !forceRegenerate) {
        console.log('[NovelAnalysisPanel] 没有概括，显示提示');
        setChapterSummary('该章节还没有生成概括，请点击"生成概括"按钮');
        return;
      }

      // 调用新接口生成并保存概括
      console.log('[NovelAnalysisPanel] 准备生成概括，chapter_id:', currentChapterId);
      const summary = await DataService.generateChapterSummary(currentChapterId, forceRegenerate);
      console.log('[NovelAnalysisPanel] 概括生成成功:', summary);
      
      setChapterSummary(summary || '生成概括失败');
      if (summary) {
        onToast('success', '剧情概括生成成功');
      }
    } catch (error: any) {
      console.error('[NovelAnalysisPanel] 生成章节概括失败:', error);
      console.error('[NovelAnalysisPanel] 错误详情:', {
        message: error.message,
        detail: error.detail,
        status: error.status,
        fullError: error
      });
      setChapterSummary('生成失败，请重试');
      onToast('error', '生成章节概括失败');
    } finally {
      setIsLoadingChapter(false);
    }
  };

  /**
   * 生成小说概括
   */
  const handleGenerateSummary = async () => {
    if (!workId) {
      onToast('warning', '请先选择一个作品');
      return;
    }

    try {
      setIsLoadingNovel(true);
      
      console.log('[NovelAnalysisPanel] 开始生成小说概括, workId:', workId);
      
      // 先启动分析任务
      await DataService.startNovelAnalysis(workId);
      
      onToast('success', '小说分析已启动，请稍等片刻...');
      
      // 轮询检查分析状态（最多等待20分钟，适应长文本分析）
      const maxAttempts = 240; // 240次 * 5秒 = 20分钟（1小时后端超时 / 3 = 足够缓冲）
      let attempts = 0;
      let lastProgress = 0;
      let noProgressCount = 0;
      
      const checkStatus = async (): Promise<boolean> => {
        try {
          const status = await DataService.getAnalysisStatus(workId);
          
          if (status.status === 'completed') {
            // 分析完成，加载结果
            await loadNovelSummary();
            onToast('success', '小说概括生成完成！');
            return true;
          } else if (status.status === 'failed') {
            onToast('error', status.errorMessage || '分析失败');
            return true;
          }
          
          // 检测进度停滞（可能后端卡住了）
          const currentProgress = status.progress?.analyzedChapters || 0;
          if (currentProgress === lastProgress) {
            noProgressCount++;
            if (noProgressCount >= 30) {  // 30次无进度 = 2.5分钟停滞
              console.warn('[压测优化] 检测到分析进度停滞，可能遇到问题');
              onToast('warning', '分析进度似乎停滞，请稍后检查或刷新页面');
            }
          } else {
            lastProgress = currentProgress;
            noProgressCount = 0;
          }
          
          // 显示进度信息（开发模式）
          if (status.progress) {
            const progressPercent = (status.progress.analyzedChapters / status.progress.totalChapters * 100).toFixed(1);
            console.log(
              `[分析进度] ${status.progress.analyzedChapters}/${status.progress.totalChapters} 章 ` +
              `(${progressPercent}%) - ${status.currentStage}`
            );
          }
          
          // 继续等待
          return false;
        } catch (error) {
          console.error('检查分析状态失败:', error);
          return false;
        }
      };
      
      const pollInterval = setInterval(async () => {
        attempts++;
        
        const done = await checkStatus();
        
        if (done || attempts >= maxAttempts) {
          clearInterval(pollInterval);
          setIsLoadingNovel(false);
          
          if (!done) {
            const waitedMinutes = Math.floor(attempts * 5 / 60);
            onToast(
              'warning', 
              `分析超时（已等待${waitedMinutes}分钟），请稍后刷新查看结果或检查后端日志`
            );
            console.error(
              `[压测优化] 分析轮询超时: 已轮询${attempts}次（${waitedMinutes}分钟），` +
              `超过最大限制${maxAttempts}次`
            );
          }
        }
      }, 5000); // 每5秒检查一次（长文本分析需要更多时间）
      
    } catch (error: any) {
      console.error('[NovelAnalysisPanel] 生成小说概括失败:', error);
      
      let errorMessage = '生成概括失败';
      if (error?.detail) {
        errorMessage = error.detail;
      } else if (error?.message) {
        errorMessage = error.message;
      }
      
      if (errorMessage.includes('no chapters')) {
        errorMessage = '该作品还没有章节，无法生成概括';
      }
      
      onToast('error', errorMessage);
      setIsLoadingNovel(false);
    }
  };

  /**
   * 从分析结果提取世界观数据
   */
  const handleExtractWorldview = async () => {
    if (!workId) {
      onToast('warning', '请先选择一个作品');
      return;
    }

    try {
      setIsExtractingWorldview(true);
      
      console.log('[NovelAnalysisPanel] 开始提取世界观数据, workId:', workId);
      
      const result = await DataService.extractWorldviewFromAnalysis(workId, {
        extractCharacters: true,
        extractLocations: true,
        extractSettings: true
      });
      
      console.log('[NovelAnalysisPanel] 世界观提取结果:', result);
      
      // 构建提示消息
      const messages = [];
      if (result.characters.created > 0 || result.characters.updated > 0) {
        messages.push(`角色: 创建${result.characters.created}个, 更新${result.characters.updated}个`);
      }
      if (result.locations.created > 0 || result.locations.updated > 0) {
        messages.push(`地点: 创建${result.locations.created}个, 更新${result.locations.updated}个`);
      }
      if (result.settings.created > 0 || result.settings.updated > 0) {
        messages.push(`设定: 创建${result.settings.created}个, 更新${result.settings.updated}个`);
      }
      
      if (messages.length > 0) {
        onToast('success', `世界观提取完成！${messages.join(' | ')}`);
      } else {
        onToast('info', '没有提取到新数据（可能已经提取过了）');
      }
      
    } catch (error: any) {
      console.error('[NovelAnalysisPanel] 提取世界观失败:', error);
      
      let errorMessage = '提取世界观失败';
      if (error?.detail) {
        errorMessage = error.detail;
      } else if (error?.message) {
        errorMessage = error.message;
      }
      
      if (errorMessage.includes('No analysis found')) {
        errorMessage = '请先运行小说分析后再提取';
      } else if (errorMessage.includes('not completed')) {
        errorMessage = '小说分析尚未完成，请稍后再试';
      }
      
      onToast('error', errorMessage);
    } finally {
      setIsExtractingWorldview(false);
    }
  };

  /**
   * 初始加载和标签切换时加载数据
   */
  useEffect(() => {
    if (activeTab === 'novel') {
      loadNovelSummary();
    } else if (activeTab === 'chapter' && currentChapterId) {
      // 切换到章节概括时，自动检查并加载已有概括（不生成新的）
      loadChapterSummary(false);
    }
  }, [activeTab, workId, currentChapterId]);

  /**
   * 智能分段：按标题或大段落拆分内容
   */
  const parseReportIntoSections = (report: string) => {
    const sections: Array<{ title: string; content: string }> = [];

    // 方式1：尝试按 Markdown 标题拆分 (##, ###, 或 **)
    const markdownSections = report.split(/\n(?=#{2,3}\s+|(?:\*{2}|【).+?(?:\*{2}|】))/);
    
    if (markdownSections.length > 1) {
      // 成功按标题拆分
      markdownSections.forEach(section => {
        if (!section.trim()) return;
        
        // 提取标题
        const titleMatch = section.match(/^(?:#{2,3}\s+|(?:\*{2}|【))(.+?)(?:\*{2}|】)?(?:\n|$)/);
        if (titleMatch) {
          const title = titleMatch[1].trim();
          const content = section.replace(/^(?:#{2,3}\s+|(?:\*{2}|【)).+?(?:\*{2}|】)?(?:\n|$)/, '').trim();
          if (content) {
            sections.push({ title, content });
          }
        } else {
          // 没有明确标题，使用第一行作为标题
          const lines = section.trim().split('\n');
          const title = lines[0].trim();
          const content = lines.slice(1).join('\n').trim();
          if (title && content) {
            sections.push({ title, content });
          }
        }
      });
    }

    // 方式2：如果没有找到标题，按大段落拆分（空行分隔）
    if (sections.length === 0) {
      const paragraphs = report.split(/\n\s*\n/).filter(p => p.trim().length > 50);
      
      paragraphs.forEach((para, index) => {
        const lines = para.trim().split('\n');
        const firstLine = lines[0].trim();
        
        // 如果第一行比较短（可能是标题）
        if (firstLine.length < 30 && lines.length > 1) {
          sections.push({
            title: firstLine,
            content: lines.slice(1).join('\n').trim()
          });
        } else {
          // 使用序号作为标题
          sections.push({
            title: `第 ${index + 1} 部分`,
            content: para.trim()
          });
        }
      });
    }

    // 如果还是没有分段成功，按固定长度分段
    if (sections.length === 0 && report.length > 500) {
      const chunkSize = 800;
      const chunks = Math.ceil(report.length / chunkSize);
      
      for (let i = 0; i < chunks; i++) {
        const start = i * chunkSize;
        const end = Math.min(start + chunkSize, report.length);
        const chunk = report.substring(start, end);
        
        // 尝试在句号处截断
        const lastPeriod = chunk.lastIndexOf('。');
        const content = lastPeriod > 0 && lastPeriod > chunkSize * 0.7 
          ? chunk.substring(0, lastPeriod + 1)
          : chunk;
        
        sections.push({
          title: `第 ${i + 1} 段`,
          content: content.trim()
        });
      }
    }

    // 如果仍然为空，返回整体
    if (sections.length === 0) {
      sections.push({
        title: '小说概括',
        content: report.trim()
      });
    }

    return sections;
  };

  /**
   * 渲染小说概括（智能分段展示）
   */
  const renderNovelSummary = () => {
    if (!novelSummary || novelSummary.includes('暂无小说概括') || novelSummary.includes('生成概括')) {
      return (
        <div className={styles.emptyState}>
          <p>{novelSummary || '暂无小说概括'}</p>
        </div>
      );
    }

    const sections = parseReportIntoSections(novelSummary);
    
    return (
      <div className={styles.reportContainer}>
        {sections.map((section, index) => (
          <div key={index} className={styles.reportSection}>
            <h3 className={styles.reportTitle}>
              {section.title}
            </h3>
            <div className={styles.reportContent}>
              {section.content}
            </div>
          </div>
        ))}
      </div>
    );
  };

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

      return renderNovelSummary();
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

      {/* 操作按钮 */}
      <div className={styles.actions}>
        {activeTab === 'novel' ? (
          <>
            <Button
              onClick={loadNovelSummary}
              variant="outline"
              size="sm"
              disabled={isLoadingNovel}
            >
              <RefreshCw size={16} className={isLoadingNovel ? styles.spinning : ''} />
              <span>刷新</span>
            </Button>

            <Button
              onClick={handleGenerateSummary}
              size="sm"
              disabled={isLoadingNovel}
            >
              <PlayCircle size={16} className={isLoadingNovel ? styles.spinning : ''} />
              <span>{isLoadingNovel ? '生成中...' : (hasAnalysis ? '重新生成' : '生成概括')}</span>
            </Button>

            {hasAnalysis && (
              <Button
                onClick={handleExtractWorldview}
                variant="outline"
                size="sm"
                disabled={isExtractingWorldview}
                title="从小说分析结果中自动提取角色、地点和设定信息到世界观标签"
              >
                <Download size={16} className={isExtractingWorldview ? styles.spinning : ''} />
                <span>{isExtractingWorldview ? '提取中...' : '提取世界观'}</span>
              </Button>
            )}
          </>
        ) : (
          <Button
            onClick={() => loadChapterSummary(true)}
            size="sm"
            disabled={isLoadingChapter || !currentChapterId}
          >
            <PlayCircle size={16} className={isLoadingChapter ? styles.spinning : ''} />
            <span>生成概括</span>
          </Button>
        )}
      </div>

      {/* 内容区域 */}
      <div className={styles.content}>
        {renderContent()}
      </div>
    </div>
  );
};

export default NovelAnalysisPanel;
