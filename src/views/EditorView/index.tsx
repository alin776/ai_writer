import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, Wand2, FileText, Check, AlertCircle } from 'lucide-react';
import { Loading } from '../../components/common';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import { useEditorStore } from '../../store/editorStore';
import NovelEditor from '../../components/editor/NovelEditor';
import type { Chapter } from '../../types';
import styles from './EditorView.module.css';

/**
 * EditorView 组件 - 编辑器页面
 *
 * 极简美学：
 * - 绝对专注：无边框干扰的编辑区域
 * - 纯净背景：白色或极浅灰
 * - 高对比度：确保可读性
 * - 扁平化工具栏：图标为主
 */
const EditorView: React.FC = () => {
  const { chapterId } = useParams<{ chapterId?: string }>();
  const navigate = useNavigate();
  const { showToast } = useGlobalStore();
  const { setCurrentChapter } = useEditorStore();

  const [chapter, setChapter] = useState<Chapter | null>(null);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'error' | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showSidebar, setShowSidebar] = useState(false);

  /**
   * 加载章节数据
   */
  useEffect(() => {
    const loadChapter = async () => {
      if (!chapterId) {
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
      } catch (err) {
        const message = err instanceof Error ? err.message : '加载章节失败';
        setError(message);
        showToast('error', message);
      } finally {
        setIsLoading(false);
      }
    };

    loadChapter();
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
   * 处理 AI 辅助
   */
  const handleAIAssist = () => {
    setShowSidebar(!showSidebar);
    showToast('info', 'AI 辅助功能待实现');
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
              className={`${styles.toolbarButton} ${styles.outline}`}
              onClick={handleAIAssist}
              title="AI 辅助"
            >
              <Wand2 className="w-4 h-4" />
              <span>AI 辅助</span>
            </button>
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
                  // 可以选择保存 JSON 格式用于未来的高级功能
                  console.log('Editor JSON:', json);
                }}
                placeholder="开始写作..."
                autoSave={true}
                autoSaveInterval={3000}
              />
            </div>
          </div>

          {/* AI 辅助侧边栏 */}
          {showSidebar && (
            <div className={styles.sidebar}>
              <div className={styles.sidebarHeader}>
                <h3 className={styles.sidebarTitle}>AI 辅助</h3>
              </div>
              <div className={styles.sidebarContent}>
                <div className={styles.sidebarPlaceholder}>AI 辅助功能待实现</div>
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
