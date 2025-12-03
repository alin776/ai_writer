import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, FileText, Check, AlertCircle } from 'lucide-react';
import { Loading } from '../../components/common';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import { useEditorStore } from '../../store/editorStore';
import NovelEditor from '../../components/editor/NovelEditor';
import AgentChatPanel from '../../components/agent/AgentChatPanel';
import { WorldviewPanel } from '../../components/editor/WorldviewPanel';
import NovelAnalysisPanel from '../../components/editor/NovelAnalysisPanel';
import SessionTabBar from '../../components/editor/SessionTabBar';
import type { Chapter } from '../../types';
import type { WorldData } from '../../types/novel';
import styles from './EditorView.module.css';

/**
 * EditorView 组件 - 编辑器页面
 *
 * 极简美学：
 * - 绝对专注：无边框干扰的编辑区域
 * - 纯净背景：白色或极浅灰
 * - 高对比度：确保可读性
 * - 扁平化工具栏：图标为主
 *
 * 新增功能：
 * - 左侧导航栏控制右侧面板（世界观/概括/AI）
 * - AI智能助手完整集成
 */
const EditorView: React.FC = () => {
  const { chapterId } = useParams<{ chapterId?: string }>();
  const navigate = useNavigate();
  const { showToast } = useGlobalStore();
  const { setCurrentChapter, rightSidebarType, setRightSidebarType, closeRightSidebar } = useEditorStore();

  const [chapter, setChapter] = useState<Chapter | null>(null);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'error' | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [worldData, setWorldData] = useState<WorldData>({
    characters: [],
    locations: [],
    settings: [],
  });

  /**
   * 默认打开 agent 面板
   */
  useEffect(() => {
    if (chapterId) {
      setRightSidebarType('agent');
    }
  }, [chapterId, setRightSidebarType]);

  /**
   * 加载章节数据和世界观数据
   */
  useEffect(() => {
    const loadData = async () => {
      if (!chapterId) {
        // 没有章节ID，清空编辑器
        setChapter(null);
        setTitle('');
        setContent('');
        setCurrentChapter(null);
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        setError(null);
        const data = await DataService.getChapter(chapterId);
        setChapter(data);
        setTitle(data.title);
        setContent(data.content);
        setCurrentChapter(data);

        // 加载世界观数据
        try {
          const worldDataFromServer = await DataService.getWorldData(data.workId);
          setWorldData(worldDataFromServer);
        } catch (worldErr) {
          console.error('加载世界观数据失败:', worldErr);
          // 世界观数据加载失败不影响编辑器使用
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : '加载章节失败';
        setError(message);
        showToast('error', message);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [chapterId, setCurrentChapter, showToast]);

  /**
   * 计算字数
   */
  const wordCount = content.replace(/\s/g, '').length;

  /**
   * 处理保存
   */
  const handleSave = async () => {
    if (!chapterId || !chapter) {
      showToast('warning', '没有可保存的章节');
      return;
    }

    try {
      setIsSaving(true);
      setSaveStatus('saving');
      await DataService.updateChapter(chapterId, {
        title,
        content,
        wordCount,
      });
      setSaveStatus('saved');
      showToast('success', '保存成功');

      // 3秒后清除保存状态
      setTimeout(() => setSaveStatus(null), 3000);
    } catch (err) {
      const message = err instanceof Error ? err.message : '保存失败';
      setSaveStatus('error');
      showToast('error', message);
    } finally {
      setIsSaving(false);
    }
  };

  /**
   * 获取保存状态文本和图标
   */
  const getSaveStatusDisplay = () => {
    if (!saveStatus) return null;

    const displays = {
      saving: { text: '保存中...', icon: <FileText className="w-3 h-3" />, className: styles.saving },
      saved: { text: '已保存', icon: <Check className="w-3 h-3" />, className: styles.saved },
      error: { text: '保存失败', icon: <AlertCircle className="w-3 h-3" />, className: styles.error },
    };

    return displays[saveStatus];
  };

  if (isLoading) {
    return (
      <div className={styles.loadingContainer}>
        <Loading />
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.errorContainer}>
        <div className={styles.errorContent}>
          <p className={styles.errorMessage}>{error}</p>
          <button className={`${styles.toolbarButton} ${styles.primary}`} onClick={() => navigate('/works')}>
            返回作品列表
          </button>
        </div>
      </div>
    );
  }

  const saveStatusDisplay = getSaveStatusDisplay();

  return (
    <div className={styles.page}>
      <div className={styles.container}>
        {/* 工具栏 - 极简扁平化 */}
        <div className={styles.toolbar}>
          <div className={styles.toolbarLeft}>
            <button className={styles.backButton} onClick={() => navigate('/works')}>
              <ArrowLeft className="w-4 h-4" />
              <span>返回</span>
            </button>
          </div>

          <div className={styles.toolbarRight}>
            <button
              className={`${styles.toolbarButton} ${styles.primary}`}
              onClick={handleSave}
              disabled={isSaving}
              title="保存"
            >
              <Save className="w-4 h-4" />
              <span>{isSaving ? '保存中...' : '保存'}</span>
            </button>
          </div>
        </div>

        {/* 编辑器主体 */}
        <div className={styles.editor}>
          <div className={styles.editorMain}>
            <div className={styles.editorContent}>
              {/* 标题输入 - 绝对专注，无边框 */}
              <textarea
                placeholder="章节标题"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className={styles.titleInput}
                rows={1}
                onInput={(e) => {
                  const target = e.target as HTMLTextAreaElement;
                  target.style.height = 'auto';
                  target.style.height = target.scrollHeight + 'px';
                }}
              />

              {/* Novel 富文本编辑器 */}
              <NovelEditor
                content={content}
                onSave={(html, json) => {
                  setContent(html);
                  console.log('Editor JSON:', json);
                }}
                placeholder="开始写作..."
                autoSave={true}
                autoSaveInterval={3000}
              />
            </div>
          </div>

          {/* 右侧面板 - 方案B：替换整个面板内容 */}
          {rightSidebarType && chapter && (
            <div className={styles.sidebar}>
              {/* 会话标签栏 */}
              <SessionTabBar />

              {/* 面板内容区域 */}
              <div className={styles.sidebarContent} style={{ padding: 0, height: 'calc(100% - 40px)' }}>
                {rightSidebarType === 'worldview' && (
                  <WorldviewPanel
                    workId={chapter.workId}
                    worldData={worldData}
                  />
                )}

                {rightSidebarType === 'summary' && (
                  <NovelAnalysisPanel
                    workId={chapter.workId}
                    currentChapterId={chapter.id}
                    onToast={showToast}
                  />
                )}

                {rightSidebarType === 'agent' && (
                  <AgentChatPanel
                    workId={chapter.workId}
                    chapterId={chapter.id}
                    className="h-full"
                  />
                )}
              </div>
            </div>
          )}
        </div>

        {/* 状态栏 */}
        <div className={styles.statusBar}>
          <div className={styles.statusLeft}>
            <div className={styles.wordCount}>
              <FileText className="w-3 h-3" />
              <span>字数: {wordCount.toLocaleString()}</span>
            </div>
          </div>

          <div className={styles.statusRight}>
            {saveStatusDisplay && (
              <div className={`${styles.saveStatus} ${saveStatusDisplay.className}`}>
                {saveStatusDisplay.icon}
                <span>{saveStatusDisplay.text}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EditorView;
