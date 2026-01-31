import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useParams, Link, useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ArrowLeft, Edit, Trash2, Plus, BookOpen, BarChart3, BookMarked, Download, MessageSquare, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button, Card, Loading } from '../../components/common';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import ExportDialog from '../../components/export/ExportDialog';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '../../components/ui/alert-dialog';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import { useAuthStore } from '../../store/authStore';
import type { Work, Chapter, CreateChapterData } from '../../types';
import type { Chapter as NovelChapter, WorldData, Character, Location, Setting, WorkGuidelines } from '../../types/novel';
import { formatDate } from '../../utils/formatDate';
import NovelEditor from '../../components/editor/NovelEditor';
import { WorldviewPanel } from '../../components/editor/WorldviewPanel';
import { AIPanel } from '../../components/editor/AIPanel';
import SessionTabBar from '../../components/editor/SessionTabBar';
import { useEditorStore } from '../../store/editorStore';
import { useWorkNavStore } from '../../store/workNavStore';
import { useConfirm } from '../../hooks/useConfirm';
import { useTabManager } from '../../hooks/useTabManager';
import HistoryPanel from '../../components/agent/HistoryPanel';
import type { HistorySessionItem } from '@/types/agent';
import { agentApi } from '@/services/agentApi';
import styles from './WorkDetailView.module.css';

/**
 * WorkDetailView 组件 - 作品详情页面
 *
 * 功能：
 * - 显示作品详细信息
 * - 显示章节列表
 * - 使用路由参数获取 workId
 * - 使用 DataService 获取数据
 */
const WorkDetailView: React.FC = () => {
  const { workId } = useParams<{ workId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();
  const { showToast } = useGlobalStore();
  const { user, setUser } = useAuthStore();
  const { confirmState, confirm, closeConfirm } = useConfirm();
  const { rightSidebarType, setRightSidebarType } = useEditorStore();
  const setLastWork = useWorkNavStore((state) => state.setLastWork);
  const clearLastWork = useWorkNavStore((state) => state.clearLastWork);
  const autoExtractFromImportRef = useRef(false);
  const autoExtractWorkIdRef = useRef<string | undefined>(undefined);
  // 检测是否从新建或导入进入（用于设置初始收起状态）
  const isFromCreateOrImport = Boolean(
    (location.state as Record<string, any> | null)?.fromCreate ||
    (location.state as Record<string, any> | null)?.autoExtractWorldview
  );

  if (workId && autoExtractWorkIdRef.current !== workId) {
    autoExtractFromImportRef.current = Boolean(
      (location.state as Record<string, any> | null)?.autoExtractWorldview
    );
    autoExtractWorkIdRef.current = workId;
  }
  // 获取章节记忆功能
  const setLastChapter = useWorkNavStore((state) => state.setLastChapter);
  const getLastChapter = useWorkNavStore((state) => state.getLastChapter);

  // AI 自动补全开关
  const aiAutoCompleteEnabled = user?.preferences?.aiAutoComplete ?? false;

  const handleToggleAIAutoComplete = useCallback(async () => {
    if (!user) return;

    const newValue = !aiAutoCompleteEnabled;
    const currentPreferences = user.preferences || {
      theme: 'light' as const,
      language: 'zh-CN' as const,
      fontSize: 'medium' as const,
      autoSave: true,
      autoSaveInterval: 30,
      aiAutoComplete: false,
    };

    const newPreferences = {
      ...currentPreferences,
      aiAutoComplete: newValue,
    };

    try {
      setUser({ ...user, preferences: newPreferences });
      await DataService.updatePreferences(newPreferences);
      showToast('success', newValue ? t('workDetail.toast.aiAutoCompleteEnabled') : t('workDetail.toast.aiAutoCompleteDisabled'));
    } catch (error) {
      setUser({ ...user, preferences: currentPreferences });
      showToast('error', t('workDetail.toast.updateSettingsFailed'));
    }
  }, [user, aiAutoCompleteEnabled, setUser, showToast]);

  const [work, setWork] = useState<Work | null>(null);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 编辑器相关状态
  const [currentChapterId, setCurrentChapterId] = useState<string | undefined>(undefined);
  const [currentChapterContent, setCurrentChapterContent] = useState<string>('');
  // 用于追踪编辑器当前加载的章节 ID，防止异步保存时的竞态条件
  const editorChapterIdRef = React.useRef<string | undefined>(undefined);

  // 世界观数据
  const [worldData, setWorldData] = useState<WorldData>({
    characters: [],
    locations: [],
    settings: [],
    guidelines: undefined,
    aiGuidelines: undefined,
  });
  const autoExtractFromImport = autoExtractFromImportRef.current;

  const refreshWorldData = useCallback(async () => {
    if (!workId) return false;

    try {
      const latest = await DataService.getWorldData(workId);
      const latestCount = (latest.characters?.length ?? 0)
        + (latest.locations?.length ?? 0)
        + (latest.settings?.length ?? 0);

      setWorldData((prev) => {
        const prevCount = (prev.characters?.length ?? 0)
          + (prev.locations?.length ?? 0)
          + (prev.settings?.length ?? 0);

        if (latestCount === 0 && prevCount > 0) {
          return prev;
        }
        if (latestCount === 0 && prevCount === 0) {
          return prev;
        }
        return latest as any;
      });

      return latestCount > 0;
    } catch (error) {
      console.warn('[WorkDetailView] Failed to refresh worldview data:', error);
      return false;
    }
  }, [workId]);
  const hasWorldviewCards = worldData.characters.length + worldData.locations.length + worldData.settings.length > 0;

  useEffect(() => {
    if (!workId || !autoExtractFromImport || hasWorldviewCards) return;

    let cancelled = false;
    const delays = [2000, 6000, 12000, 25000, 45000];
    let timer: ReturnType<typeof setTimeout> | null = null;

    const run = async (index: number) => {
      if (cancelled) return;
      const hasNewCards = await refreshWorldData();
      if (hasNewCards || cancelled) return;
      if (index < delays.length - 1) {
        timer = setTimeout(() => run(index + 1), delays[index + 1]);
      }
    };

    timer = setTimeout(() => run(0), delays[0]);

    return () => {
      cancelled = true;
      if (timer) {
        clearTimeout(timer);
      }
    };
  }, [workId, autoExtractFromImport, hasWorldviewCards, refreshWorldData]);
  // 世界观面板初始 tab（用于搜索导航定位）
  const [worldviewInitialTab, setWorldviewInitialTab] = useState<'characters' | 'places' | 'settings' | undefined>(undefined);
  // 世界观面板目标项 ID（用于搜索导航滚动定位）
  const [worldviewTargetItemId, setWorldviewTargetItemId] = useState<string | undefined>(undefined);
  const {
    tabs,
    activeTabId,
    createTab,
    closeTab,
    switchTab,
    updateTabTitle,
    replaceTabSession,
    attachSessionTab
  } = useTabManager(currentChapterId || workId || 'work', workId);

  const currentChapterMeta = chapters.find((chapter) => chapter.id === currentChapterId);
  const [showHistoryPanel, setShowHistoryPanel] = useState(false);
  const handleOpenHistory = useCallback(() => setShowHistoryPanel(true), []);
  const handleCloseHistory = useCallback(() => setShowHistoryPanel(false), []);

  const handleRestoreHistorySession = useCallback(
    async (session: HistorySessionItem) => {
      if (!activeTabId) return;

      // 尝试从后端拉取历史消息（优先 sessionId，其次 conversationId）
      const idsToTry = Array.from(
        new Set([session.sessionId, session.conversationId].filter(Boolean) as string[])
      );

      let messages: any[] = [];
      let resolvedConversationId = session.conversationId || session.sessionId || '';

      const loadLocalMessages = (id: string) => {
        if (typeof window === 'undefined') return { messages: [], conversationId: resolvedConversationId };
        try {
          const stored = localStorage.getItem(`agent_conversation_${id}`);
          if (!stored) return { messages: [], conversationId: resolvedConversationId };
          const parsed = JSON.parse(stored);
          return {
            messages: Array.isArray(parsed.messages) ? parsed.messages : [],
            conversationId: parsed.conversationId || resolvedConversationId
          };
        } catch (error) {
          console.warn('[WorkDetailView] 读取本地会话失败:', error);
          return { messages: [], conversationId: resolvedConversationId };
        }
      };
      for (const id of idsToTry) {
        try {
          const resp = await agentApi.getSessionMessages(id, { order: 'asc', limit: 200 });
          const rawMessages = Array.isArray(resp) ? resp : Array.isArray((resp as any)?.messages) ? (resp as any).messages : [];

          messages = rawMessages.map((m: any) => ({
            role: m.role === 'assistant' ? 'agent' : m.role,
            content: m.content,
            metadata: m.metadata,
            timestamp: m.created_at || m.createdAt || new Date().toISOString()
          }));

          if (messages.length > 0 || idsToTry.length === 1) {
            break;
          }
        } catch (error) {
          console.warn('[WorkDetailView] 加载历史消息失败，尝试下一个 ID:', id, error);
        }
      }

      // 后端为空时再尝试本地缓存
      if (messages.length === 0) {
        for (const id of idsToTry) {
          const local = loadLocalMessages(id);
          if (local.messages.length > 0) {
            messages = local.messages;
            resolvedConversationId = local.conversationId;
            break;
          }
        }
      }

      const sessionId = session.sessionId;
      const conversationId = resolvedConversationId;
      const nowIso = new Date().toISOString();
      const payload = {
        id: sessionId,
        conversationId,
        messages,
        createdAt: session.updatedAt || nowIso,
        updatedAt: session.updatedAt || nowIso,
        title: session.title || t('editor.sessionTab.history'),
        workId,
        chapterId: currentChapterId
      };

      try {
        localStorage.setItem(`agent_conversation_${sessionId}`, JSON.stringify(payload));
        const listKey = 'agent_conversation_sessions';
        const storedList = localStorage.getItem(listKey);
        const ids: string[] = storedList ? JSON.parse(storedList) : [];
        const updatedIds = [sessionId, ...ids.filter((id) => id !== sessionId)];
        localStorage.setItem(listKey, JSON.stringify(updatedIds));
      } catch (error) {
        console.warn('[WorkDetailView] 缓存历史会话失败:', error);
      }

      // 不覆盖当前标签，打开/切换到一个带历史会话的标签
      attachSessionTab(sessionId, session.title || t('editor.sessionTab.history'), conversationId);
      setShowHistoryPanel(false);
      showToast('info', t('workDetail.toast.switchedToHistorySession'));
    },
    [activeTabId, attachSessionTab, currentChapterId, showToast, workId]
  );

  // 默认打开 agent 面板
  React.useEffect(() => {
    if (workId) {
      setRightSidebarType('agent');
    }
  }, [workId, setRightSidebarType]);

  // 导出对话框状态
  const [showExportDialog, setShowExportDialog] = useState(false);

  // 折叠状态（从新建或导入进入时默认收起）
  const [isLeftCollapsed, setIsLeftCollapsed] = useState(isFromCreateOrImport);
  const [isRightCollapsed, setIsRightCollapsed] = useState(false);
  const [isEditorCollapsed, setIsEditorCollapsed] = useState(isFromCreateOrImport); // 编辑器收缩状态

  const DEFAULT_RIGHT_PANEL_WIDTH = 288; // 默认 288px (w-72)
  const COLLAPSED_RIGHT_PANEL_WIDTH = 0; // collapsed width - 完全隐藏

  // 右侧面板宽度
  const [rightPanelWidth, setRightPanelWidth] = useState(() => {
    const saved = localStorage.getItem('rightPanelWidth');
    return saved ? parseInt(saved, 10) : DEFAULT_RIGHT_PANEL_WIDTH;
  });
  const rightPanelWidthRef = useRef(rightPanelWidth);
  const [isResizing, setIsResizing] = useState(false);
  // 拖拽起始位置和起始宽度
  const resizeStartX = useRef<number>(0);
  const resizeStartWidth = useRef<number>(0);
  const workbenchRef = useRef<HTMLDivElement>(null);

  // 添加章节输入框状态
  const [isAddingChapter, setIsAddingChapter] = useState(false);
  const [newChapterTitle, setNewChapterTitle] = useState('');

  // 删除章节确认对话框状态
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [chapterToDelete, setChapterToDelete] = useState<string | null>(null);

  // 重命名章节状态
  const [editingChapterId, setEditingChapterId] = useState<string | null>(null);
  const [editingChapterTitle, setEditingChapterTitle] = useState('');

  /**
   * 转换 Chapter 到 NovelChapter 格式
   */
  const convertToNovelChapters = (chapters: Chapter[]): NovelChapter[] => {
    return chapters.map((chapter) => ({
      id: chapter.id,
      title: chapter.title,
      wordCount: chapter.wordCount,
      status: chapter.isPublished ? 'published' : 'draft',
      order: chapter.order,
      content: chapter.content,
      createdAt: new Date(chapter.createdAt),
      updatedAt: new Date(chapter.updatedAt),
    }));
  };

  /**
   * 加载作品和章节数据
   */
  useEffect(() => {
    const loadData = async () => {
      if (!workId) {
        setError(t('workDetail.error.workIdNotExist'));
        setIsLoading(false);
        clearLastWork();
        return;
      }

      try {
        setIsLoading(true);
        setError(null);
        // 每次加载/切换作品前先重置状态，避免沿用上一作品的章节内容
        setChapters([]);
        setCurrentChapterId(undefined);
        setCurrentChapterContent('');
        editorChapterIdRef.current = undefined;
        setWorldData({
          characters: [],
          locations: [],
          settings: [],
          guidelines: undefined,
          aiGuidelines: undefined,
        });

        // 检查是否有预加载数据（从导入页面跳转时携带）
        const rawLocationState = location.state;
        const nextLocationState =
          rawLocationState && typeof rawLocationState === 'object'
            ? { ...(rawLocationState as Record<string, unknown>) }
            : null;
        let shouldReplaceLocationState = false;
        const preloadedData = (rawLocationState as any)?.preloadedData;
        let workData, chaptersData, worldDataFromServer;

        // 验证预加载数据的有效性
        const isPreloadedDataValid = preloadedData?.work?.id &&
                                     Array.isArray(preloadedData?.chapters) &&
                                     preloadedData?.worldData;

        if (isPreloadedDataValid) {
          // 使用预加载数据，无需再次请求
          console.log('[WorkDetailView] 使用预加载数据');
          workData = preloadedData.work;
          chaptersData = preloadedData.chapters;
          worldDataFromServer = preloadedData.worldData;
          // 清除 preloadedData，保留其他 state 数据
          if (nextLocationState && 'preloadedData' in nextLocationState) {
            delete (nextLocationState as Record<string, unknown>).preloadedData;
            shouldReplaceLocationState = true;
          }
        } else {
          // 正常从服务器获取数据
          [workData, chaptersData, worldDataFromServer] = await Promise.all([
            DataService.getWork(workId),
            DataService.getChapters(workId),
            DataService.getWorldData(workId),
          ]);
        }

        setLastWork(workId, workData?.title);
        setWork(workData);
        setChapters(chaptersData);
        setWorldData(worldDataFromServer as any);

        // 处理搜索导航的定位参数
        const searchNavState = location.state as {
          targetChapterId?: string;
          openWorldview?: boolean;
          worldviewTab?: 'characters' | 'locations' | 'settings';
          targetItemId?: string;
          autoExtractWorldview?: boolean;
        } | null;

        // 如果有章节，处理章节选择逻辑
        if (chaptersData.length > 0) {
          let targetChapter = null;

          // 优先级1：搜索导航指定的章节
          if (searchNavState?.targetChapterId) {
            targetChapter = chaptersData.find((c: Chapter) => c.id === searchNavState.targetChapterId);
            if (targetChapter) {
              console.log('[WorkDetailView] 从搜索导航定位到章节:', targetChapter.title);
            }
          }

          // 优先级2：上次编辑的章节
          if (!targetChapter) {
            const lastChapterId = getLastChapter(workId);
            targetChapter = lastChapterId ? chaptersData.find((c: Chapter) => c.id === lastChapterId) : null;
            if (targetChapter) {
              console.log('[WorkDetailView] 恢复到上次编辑的章节:', targetChapter.title);
            }
          }

          // 优先级3：默认第一个章节
          if (!targetChapter) {
            targetChapter = chaptersData[0];
          }

          setCurrentChapterId(targetChapter.id);
          setCurrentChapterContent(targetChapter.content);
          editorChapterIdRef.current = targetChapter.id;
          setLastChapter(workId, targetChapter.id);
        }

        // 处理世界观面板定位（角色/地点/设定搜索）
        if (searchNavState?.openWorldview) {
          // 打开世界观面板
          setRightSidebarType('worldview');
          // 设置初始 tab（注意：搜索用 'locations'，面板用 'places'）
          const tabMap: Record<string, 'characters' | 'places' | 'settings'> = {
            'characters': 'characters',
            'locations': 'places',
            'settings': 'settings'
          };
          const mappedTab = searchNavState.worldviewTab ? tabMap[searchNavState.worldviewTab] : 'characters';
          setWorldviewInitialTab(mappedTab);
          // 设置目标项 ID（用于滚动定位）
          if (searchNavState.targetItemId) {
            setWorldviewTargetItemId(searchNavState.targetItemId);
          }
          console.log('[WorkDetailView] 从搜索导航打开世界观面板:', mappedTab, searchNavState.targetItemId);
        } else if (searchNavState?.autoExtractWorldview) {
          // 导入后默认回到 agent 面板
          setRightSidebarType('agent');
        }

        // 清除 location.state 中的搜索导航参数，避免刷新时重复执行
        if (searchNavState?.targetChapterId || searchNavState?.openWorldview || searchNavState?.autoExtractWorldview) {
          if (nextLocationState) {
            delete (nextLocationState as Record<string, unknown>).targetChapterId;
            delete (nextLocationState as Record<string, unknown>).openWorldview;
            delete (nextLocationState as Record<string, unknown>).worldviewTab;
            delete (nextLocationState as Record<string, unknown>).targetItemId;
            delete (nextLocationState as Record<string, unknown>).autoExtractWorldview;
          }
          shouldReplaceLocationState = true;
        }

        if (shouldReplaceLocationState) {
          const hasKeys = nextLocationState && Object.keys(nextLocationState).length > 0;
          navigate(location.pathname, {
            replace: true,
            state: hasKeys ? nextLocationState : null,
          });
        }

        // 如果没有章节，自动创建默认章节
        if (chaptersData.length === 0) {
          try {
            const defaultChapterData = {
              work_id: workId,
              title: t('workDetail.chapter.firstChapter'),
              content: '',
              order: 1,
              edit_event_id: crypto.randomUUID(),
            };
            const defaultChapter = await DataService.createChapter(defaultChapterData);
            setChapters([defaultChapter]);
            setCurrentChapterId(defaultChapter.id);
            setCurrentChapterContent('');
            editorChapterIdRef.current = defaultChapter.id;
            // 保存默认章节ID到 store
            setLastChapter(workId, defaultChapter.id);
            showToast('info', t('workDetail.toast.autoCreatedFirstChapter'));
          } catch (createError) {
            console.error('Failed to create default chapter:', createError);
            // 创建失败时，显示错误提示但不设置undefined
            // 保持章节列表为空，让用户手动创建
            showToast('error', t('workDetail.toast.createChapterFailed'));
            // 不设置currentChapterId为undefined，保持初始状态
          }
        }

        // 🔥 首次打开作品时，自动检查并触发分析（异步执行，不阻塞 UI）
        // 使用 localStorage 记录已触发过的作品，避免重复触发
        const AUTO_ANALYSIS_KEY = `auto-analysis-triggered-${workId}`;
        const hasTriggered = localStorage.getItem(AUTO_ANALYSIS_KEY);

        if (!hasTriggered && chaptersData.length > 0) {
          // 异步执行分析，不阻塞页面加载
          (async () => {
            try {
              const analysisStatus = await DataService.getAnalysisStatus(workId);
              // 只有在没有分析结果或分析失败时才触发，跳过 processing/pending/success 状态
              const skipStatuses = ['success', 'processing', 'pending'];
              if (!analysisStatus || !skipStatuses.includes(analysisStatus.status)) {
                console.log('[WorkDetailView] 首次打开作品，触发自动分析');
                await DataService.startNovelAnalysis(workId);
                showToast('info', t('workDetail.toast.autoStartedAnalysis'));
              } else {
                console.log('[WorkDetailView] 作品已有分析结果或正在分析，跳过');
              }
              // 无论是否触发分析，都标记为已处理
              localStorage.setItem(AUTO_ANALYSIS_KEY, 'true');
            } catch (analysisError) {
              console.warn('[WorkDetailView] 自动分析检查失败:', analysisError);
            }
          })();
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : t('workDetail.error.loadDataFailed');
        setError(message);
        showToast('error', message);
        clearLastWork();
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
    // 说明：setLastWork/clearLastWork 和 showToast 都是稳定的 zustand 函数，此处依赖仅跟 workId 相关，
    // 避免因函数引用变化导致的重复触发。
  }, [workId]);

  /**
   * 处理章节选择
   */
  const handleChapterSelect = useCallback((chapterId: string) => {
    const chapter = chapters.find((c) => c.id === chapterId);
    if (chapter) {
      // 取消正在进行的章节重命名编辑
      if (editingChapterId) {
        setEditingChapterId(null);
        setEditingChapterTitle('');
      }

      // 先更新章节ID，再更新内容，确保编辑器使用正确的章节数据
      setCurrentChapterId(chapterId);
      setCurrentChapterContent(chapter.content);
      editorChapterIdRef.current = chapterId; // 更新 ref

      // 保存当前章节ID到 store，用于下次返回时恢复
      if (workId) {
        setLastChapter(workId, chapterId);
      }

      // 调试日志
      console.log('[WorkDetailView] 切换章节:', {
        chapterId,
        title: chapter.title,
        contentLength: chapter.content?.length || 0,
      });
    }
  }, [chapters, editingChapterId, workId, setLastChapter]);

  /**
   * 处理添加章节
   */
  const handleAddChapter = useCallback(async (parentId?: string) => {
    // 显示输入框
    setIsAddingChapter(true);
  }, []);

  /**
   * 保存新章节
   */
  const handleSaveNewChapter = useCallback(async () => {
    if (!workId) return;
    if (!newChapterTitle.trim()) {
      showToast('warning', t('workDetail.toast.chapterTitleEmpty'));
      return;
    }

    try {
      // 生成唯一的编辑事件ID（用于幂等性）
      const editEventId = crypto.randomUUID();

      // 只发送后端需要的字段
      const chapterData = {
        work_id: workId,
        title: newChapterTitle.trim(),
        content: '',
        order: chapters.length + 1,
        edit_event_id: editEventId,
      };

      // 调用后端接口，后端会生成 ID
      const savedChapter = await DataService.createChapter(chapterData);

      // 使用后端返回的完整章节对象
      setChapters((prev) => [...prev, savedChapter]);

      // 取消正在进行的章节重命名编辑
      if (editingChapterId) {
        setEditingChapterId(null);
        setEditingChapterTitle('');
      }

      // 先清空当前内容，再选中新章节（确保编辑器内容被清空）
      setCurrentChapterContent('');
      // 使用 setTimeout 确保状态更新顺序正确
      setTimeout(() => {
        setCurrentChapterId(savedChapter.id);
        setCurrentChapterContent('');
        editorChapterIdRef.current = savedChapter.id; // 更新 ref
        // 保存新章节ID到 store
        setLastChapter(workId, savedChapter.id);
      }, 0);

      // 清空输入框并关闭
      setNewChapterTitle('');
      setIsAddingChapter(false);

      showToast('success', t('workDetail.toast.chapterAddSuccess'));

      // 🔥 新增章节后，自动触发重新分析（后台执行，不阻塞用户）
      try {
        console.log('[WorkDetailView] 新增章节，触发自动分析');
        await DataService.startNovelAnalysis(workId);
        showToast('info', t('workDetail.toast.triggeredAnalysisUpdate'));
      } catch (analysisError) {
        // 分析失败不影响主流程，静默处理
        console.warn('[WorkDetailView] 自动分析触发失败:', analysisError);
      }
    } catch (error) {
      showToast('error', t('workDetail.toast.chapterAddFailed'));
      console.error('Failed to add chapter:', error);
    }
  }, [workId, chapters.length, newChapterTitle, editingChapterId, showToast, setLastChapter]);

  /**
   * 取消添加章节
   */
  const handleCancelAddChapter = useCallback(() => {
    setNewChapterTitle('');
    setIsAddingChapter(false);
  }, []);

  /**
   * 开始编辑章节名称
   */
  const handleStartRenameChapter = useCallback((chapterId: string, currentTitle: string) => {
    setEditingChapterId(chapterId);
    setEditingChapterTitle(currentTitle);
  }, []);

  /**
   * 保存章节名称
   */
  const handleSaveChapterTitle = useCallback(async () => {
    if (!editingChapterId) return;
    if (!editingChapterTitle.trim()) {
      showToast('warning', t('workDetail.toast.chapterTitleEmpty'));
      return;
    }

    try {
      const chapter = chapters.find((c) => c.id === editingChapterId);
      if (!chapter) return;

      // 如果标题没有变化，直接取消编辑
      if (chapter.title === editingChapterTitle.trim()) {
        setEditingChapterId(null);
        setEditingChapterTitle('');
        return;
      }

      // 更新后端
      const updatedChapter = await DataService.updateChapter(editingChapterId, {
        title: editingChapterTitle.trim(),
      });

      // 更新本地状态
      setChapters((prev) =>
        prev.map((c) => (c.id === editingChapterId ? updatedChapter : c))
      );

      showToast('success', t('workDetail.toast.chapterTitleUpdated'));
    } catch (error) {
      showToast('error', t('workDetail.toast.chapterTitleUpdateFailed'));
      console.error('Failed to rename chapter:', error);
    } finally {
      setEditingChapterId(null);
      setEditingChapterTitle('');
    }
  }, [editingChapterId, editingChapterTitle, chapters, showToast]);

  /**
   * 取消编辑章节名称
   */
  const handleCancelRenameChapter = useCallback(() => {
    setEditingChapterId(null);
    setEditingChapterTitle('');
  }, []);

  /**
   * 处理保存章节（新增或编辑）
   */
  const handleSaveChapter = useCallback(async (chapterData: Partial<Chapter> & { id?: string }) => {
    if (!workId) return;
    if (!chapterData.title?.trim()) {
      showToast('warning', t('workDetail.toast.chapterTitleEmpty'));
      return;
    }

    try {
      // 判断是新增还是编辑
      const isNew = !chapterData.id || chapterData.id.startsWith('temp-');

      if (isNew) {
        // 新增章节
        const newChapterData = {
          work_id: workId,
          title: chapterData.title.trim(),
          content: chapterData.content || '',
          order: chapters.length + 1,
          edit_event_id: crypto.randomUUID(),
        };

        const savedChapter = await DataService.createChapter(newChapterData);

        // 更新章节列表
        setChapters((prev) => [...prev, savedChapter]);

        // 选中新章节
        setCurrentChapterId(savedChapter.id);
        setCurrentChapterContent(savedChapter.content);

        showToast('success', t('workDetail.toast.chapterAddSuccess'));
      } else {
        // 编辑章节
        const chapter = chapters.find((c) => c.id === chapterData.id);
        if (!chapter) return;

        const updatedChapter = {
          ...chapter,
          title: chapterData.title.trim(),
          content: chapterData.content || chapter.content,
          updated_at: new Date().toISOString(),
        };

        // 更新状态
        setChapters((prev) =>
          prev.map((c) => (c.id === chapterData.id ? updatedChapter : c))
        );

        // 保存到后端
        if (chapterData.id) {
          await DataService.updateChapter(chapterData.id, updatedChapter);
        }

        showToast('success', t('workDetail.toast.chapterUpdateSuccess'));
      }
    } catch (error) {
      const message =
        !chapterData.id || chapterData.id.startsWith('temp-')
          ? t('workDetail.toast.chapterAddFailed')
          : t('workDetail.toast.chapterUpdateFailed');
      showToast('error', message);
      console.error('Failed to save chapter:', error);
    }
  }, [workId, chapters, showToast]);

  /**
   * 处理删除章节（核心逻辑，不含确认对话框）
   */
  const executeDeleteChapter = useCallback(async (chapterId: string) => {
    if (!workId) return;

    try {
      // 先从后端删除（确保操作成功后再更新前端状态）
      await DataService.deleteChapter(chapterId);

      // 如果正在编辑被删除的章节名称，取消编辑
      if (editingChapterId === chapterId) {
        setEditingChapterId(null);
        setEditingChapterTitle('');
      }

      // 计算剩余章节
      const remainingChapters = chapters.filter((c) => c.id !== chapterId);
      const needsNewChapter = remainingChapters.length === 0;
      const isCurrentChapter = currentChapterId === chapterId;

      // 从状态中删除
      setChapters(remainingChapters);

      if (needsNewChapter) {
        // 删除了最后一个章节，自动创建新章节
        try {
          const defaultChapterData = {
            work_id: workId,
            title: t('workDetail.chapter.firstChapter'),
            content: '',
            order: 1,
            edit_event_id: crypto.randomUUID(),
          };
          const defaultChapter = await DataService.createChapter(defaultChapterData);
          setChapters([defaultChapter]);
          setCurrentChapterId(defaultChapter.id);
          setCurrentChapterContent('');
          editorChapterIdRef.current = defaultChapter.id;
          // 保存新章节ID到 store
          setLastChapter(workId, defaultChapter.id);
          showToast('info', t('workDetail.toast.autoCreatedNewChapter'));
        } catch (createError) {
          console.error('Failed to create default chapter after delete:', createError);
          // 创建失败时，显示错误提示但不设置undefined
          // 保持章节列表为空，让用户手动创建
          showToast('error', t('workDetail.toast.createChapterFailed'));
          // 不设置currentChapterId为undefined，保持空状态让编辑器显示提示
        }
      } else if (isCurrentChapter) {
        // 删除的是当前章节，切换到第一个剩余章节
        setCurrentChapterId(remainingChapters[0].id);
        setCurrentChapterContent(remainingChapters[0].content);
        editorChapterIdRef.current = remainingChapters[0].id;
        // 保存新章节ID到 store
        setLastChapter(workId, remainingChapters[0].id);
      }

      showToast('success', t('workDetail.toast.chapterDeleteSuccess'));
    } catch (error) {
      showToast('error', t('workDetail.toast.chapterDeleteFailed'));
      console.error('Failed to delete chapter:', error);
    }
  }, [workId, chapters, currentChapterId, editingChapterId, showToast, setLastChapter]);

  /**
   * 处理删除章节（带确认对话框）
   */
  const handleDeleteChapter = useCallback(async (chapterId: string) => {
    const chapter = chapters.find((c) => c.id === chapterId);
    if (!chapter) return;

    const confirmed = await confirm({
      title: t('workDetail.dialog.deleteChapter.title'),
      message: t('workDetail.dialog.deleteChapter.confirmMessage', { title: chapter.title }),
      confirmText: t('common.delete'),
      cancelText: t('common.cancel'),
      variant: 'danger',
    });

    if (!confirmed) {
      return;
    }

    await executeDeleteChapter(chapterId);
  }, [chapters, confirm, executeDeleteChapter]);

  /**
   * 处理章节移动/排序
   */
  const handleChapterMove = useCallback(async (chapterId: string, newOrder: number) => {
    try {
      // 更新章节顺序
      const updatedChapters = [...chapters];
      const chapterIndex = updatedChapters.findIndex((c) => c.id === chapterId);

      if (chapterIndex === -1) return;

      const [movedChapter] = updatedChapters.splice(chapterIndex, 1);
      updatedChapters.splice(newOrder, 0, movedChapter);

      // 重新分配 order
      const reorderedChapters = updatedChapters.map((chapter, index) => ({
        ...chapter,
        order: index,
        updateTime: new Date().toISOString(),
      }));

      // 更新状态
      setChapters(reorderedChapters);

      // 保存到后端
      await Promise.all(
        reorderedChapters.map((chapter) =>
          DataService.updateChapter(chapter.id, chapter)
        )
      );

      showToast('success', t('workDetail.toast.chapterOrderUpdateSuccess'));
    } catch (error) {
      showToast('error', t('workDetail.toast.chapterOrderUpdateFailed'));
      console.error('Failed to move chapter:', error);
    }
  }, [chapters, showToast]);

  /**
   * 处理编辑器保存
   */
  const handleEditorSave = useCallback(async (content: string, json: any) => {
    if (!currentChapterId) {
      console.warn('[WorkDetailView] 保存失败：没有选中的章节');
      return;
    }

    // 验证：确保保存的是当前编辑器正在编辑的章节
    // 防止章节切换时的竞态条件导致保存到错误的章节
    const chapterIdToSave = editorChapterIdRef.current;
    if (!chapterIdToSave || chapterIdToSave !== currentChapterId) {
      console.warn('[WorkDetailView] 保存失败：章节ID不匹配', {
        editorChapterId: chapterIdToSave,
        currentChapterId,
      });
      return;
    }

    // 生成唯一的编辑事件ID（用于幂等性）
    const editEventId = crypto.randomUUID();

    try {
      // 调试日志
      console.log('[WorkDetailView] 保存章节:', {
        chapterId: currentChapterId,
        editEventId,
        contentPreview: content.substring(0, 50) + '...',
      });

      // 更新章节内容
      setChapters((prevChapters) => {
        const chapter = prevChapters.find((c) => c.id === currentChapterId);
        if (!chapter) {
          console.warn('[WorkDetailView] 保存失败：章节不存在', currentChapterId);
          return prevChapters;
        }

        // 发送content和edit_event_id，让后端自动计算字数
        const updateData = {
          content,
          edit_event_id: editEventId,
        };

        // 先乐观更新本地状态
        const optimisticChapter = {
          ...chapter,
          content,
          updatedAt: new Date().toISOString(),
        };

        // 异步保存到后端，获取后端返回的完整数据（包括计算后的字数）
        DataService.updateChapter(currentChapterId, updateData)
          .then((savedChapter) => {
            // 使用后端返回的数据更新状态（包含准确的wordCount）
            setChapters((prev) =>
              prev.map((c) => (c.id === currentChapterId ? savedChapter : c))
            );
          })
          .catch((error) => {
            console.error('Failed to save chapter:', error);
          });

        // 先返回乐观更新的状态
        return prevChapters.map((c) =>
          c.id === currentChapterId ? optimisticChapter : c
        );
      });
    } catch (error) {
      showToast('error', t('workDetail.toast.saveFailed'));
      console.error('Failed to save chapter:', error);
    }
  }, [currentChapterId, showToast]);

  /**
   * 处理编辑作品
   */
  const handleEditWork = useCallback(() => {
    showToast('info', t('workDetail.toast.editWorkTodo'));
  }, [showToast]);

  /**
   * 处理删除作品
   */
  const handleDeleteWork = useCallback(() => {
    showToast('info', t('workDetail.toast.deleteWorkTodo'));
  }, [showToast]);

  // ==================== 世界观管理处理函数 ====================

  /**
   * 保存人物（新增或更新）
   */
  const handleCharacterSave = useCallback(async (character: Partial<Character>) => {
    if (!workId) return;

    try {
      const isNew = character.id?.startsWith('temp-');

      if (isNew) {
        // 准备发送到后端的数据（使用snake_case）
        const characterData = {
          work_id: workId,
          name: character.name!,
          description: character.description!,
          role: character.role,
          avatar: character.avatar,
          tags: character.tags,
          relationships: character.relationships,
        };

        // 保存到后端，获取真实ID
        const savedCharacter = await DataService.createCharacter(characterData as any);

        // 更新本地状态（使用后端返回的数据）
        setWorldData((prev) => ({
          ...prev,
          characters: [...prev.characters, savedCharacter as any],
        }));

        showToast('success', t('workDetail.toast.characterAddSuccess'));
      } else {
        // 准备更新数据（只发送可更新的字段）
        const updateData = {
          name: character.name,
          description: character.description,
          role: character.role,
          avatar: character.avatar,
          tags: character.tags,
          relationships: character.relationships,
        };

        // 保存到后端
        const savedCharacter = await DataService.updateCharacter(character.id!, updateData as any);

        // 更新本地状态（使用后端返回的数据）
        setWorldData((prev) => ({
          ...prev,
          characters: prev.characters.map((c) =>
            c.id === character.id ? savedCharacter as any : c
          ),
        }));

        showToast('success', t('workDetail.toast.characterUpdateSuccess'));
      }
    } catch (error) {
      const isNew = character.id?.startsWith('temp-');
      showToast('error', isNew ? t('workDetail.toast.characterAddFailed') : t('workDetail.toast.characterUpdateFailed'));
      console.error('Failed to save character:', error);
    }
  }, [workId, showToast]);

  const handleCharacterDelete = useCallback(async (id: string) => {
    const character = worldData.characters.find((c) => c.id === id);
    if (!character) return;

    const confirmed = await confirm({
      title: t('workDetail.dialog.deleteCharacter.title'),
      message: t('workDetail.dialog.deleteCharacter.message', { name: character.name }),
      confirmText: t('common.delete'),
      cancelText: t('common.cancel'),
      variant: 'danger',
    });

    if (!confirmed) {
      return;
    }

    try {
      // 从状态中删除
      setWorldData((prev) => ({
        ...prev,
        characters: prev.characters.filter((c) => c.id !== id),
      }));

      // 从后端删除
      await DataService.deleteCharacter(id);
      showToast('success', t('workDetail.toast.characterDeleteSuccess'));
    } catch (error) {
      showToast('error', t('workDetail.toast.characterDeleteFailed'));
      console.error('Failed to delete character:', error);
    }
  }, [worldData.characters, showToast]);

  /**
   * 地点管理 - 保存地点（新增或更新）
   */
  const handleLocationSave = useCallback(async (location: Partial<Location>) => {
    if (!workId) return;

    try {
      const isNew = location.id?.startsWith('temp-');

      if (isNew) {
        // 准备发送到后端的数据（使用snake_case）
        const locationData = {
          work_id: workId,
          name: location.name!,
          description: location.description!,
          type: location.type,
          image: location.image,
          tags: location.tags,
          related_locations: location.relatedLocations,
        };

        // 保存到后端，获取真实ID
        const savedLocation = await DataService.createLocation(locationData as any);

        // 更新本地状态（使用后端返回的数据）
        setWorldData((prev) => ({
          ...prev,
          locations: [...prev.locations, savedLocation as any],
        }));

        showToast('success', t('workDetail.toast.locationAddSuccess'));
      } else {
        // 准备更新数据（只发送可更新的字段）
        const updateData = {
          name: location.name,
          description: location.description,
          type: location.type,
          image: location.image,
          tags: location.tags,
          related_locations: location.relatedLocations,
        };

        // 保存到后端
        const savedLocation = await DataService.updateLocation(location.id!, updateData as any);

        // 更新本地状态（使用后端返回的数据）
        setWorldData((prev) => ({
          ...prev,
          locations: prev.locations.map((l) =>
            l.id === location.id ? savedLocation as any : l
          ),
        }));

        showToast('success', t('workDetail.toast.locationUpdateSuccess'));
      }
    } catch (error) {
      const isNew = location.id?.startsWith('temp-');
      showToast('error', isNew ? t('workDetail.toast.locationAddFailed') : t('workDetail.toast.locationUpdateFailed'));
      console.error('Failed to save location:', error);
    }
  }, [workId, showToast]);

  const handleLocationDelete = useCallback(async (id: string) => {
    const location = worldData.locations.find((l) => l.id === id);
    if (!location) return;

    const confirmed = await confirm({
      title: t('workDetail.dialog.deleteLocation.title'),
      message: t('workDetail.dialog.deleteLocation.message', { name: location.name }),
      confirmText: t('common.delete'),
      cancelText: t('common.cancel'),
      variant: 'danger',
    });

    if (!confirmed) {
      return;
    }

    try {
      // 从状态中删除
      setWorldData((prev) => ({
        ...prev,
        locations: prev.locations.filter((l) => l.id !== id),
      }));

      // 从后端删除
      await DataService.deleteLocation(id);
      showToast('success', t('workDetail.toast.locationDeleteSuccess'));
    } catch (error) {
      showToast('error', t('workDetail.toast.locationDeleteFailed'));
      console.error('Failed to delete location:', error);
    }
  }, [worldData.locations, showToast]);

  /**
   * 设定管理 - 保存设定（新增或更新）
   */
  const handleSettingSave = useCallback(async (setting: Partial<Setting>) => {
    if (!workId) return;

    try {
      const isNew = setting.id?.startsWith('temp-');

      if (isNew) {
        // 准备发送到后端的数据（使用snake_case）
        const settingData = {
          work_id: workId,
          title: setting.title!,
          category: setting.category,
          content: setting.content,
          tags: setting.tags,
          related_items: setting.relatedItems,
        };

        // 保存到后端，获取真实ID
        const savedSetting = await DataService.createSetting(settingData as any);

        // 更新本地状态（使用后端返回的数据）
        setWorldData((prev) => ({
          ...prev,
          settings: [...prev.settings, savedSetting as any],
        }));

        showToast('success', t('workDetail.toast.settingAddSuccess'));
      } else {
        // 准备更新数据（只发送可更新的字段）
        const updateData = {
          title: setting.title,
          category: setting.category,
          content: setting.content,
          tags: setting.tags,
          related_items: setting.relatedItems,
        };

        // 保存到后端
        const savedSetting = await DataService.updateSetting(setting.id!, updateData as any);

        // 更新本地状态（使用后端返回的数据）
        setWorldData((prev) => ({
          ...prev,
          settings: prev.settings.map((s) =>
            s.id === setting.id ? savedSetting as any : s
          ),
        }));

        showToast('success', t('workDetail.toast.settingUpdateSuccess'));
      }
    } catch (error) {
      const isNew = setting.id?.startsWith('temp-');
      showToast('error', isNew ? t('workDetail.toast.settingAddFailed') : t('workDetail.toast.settingUpdateFailed'));
      console.error('Failed to save setting:', error);
    }
  }, [workId, showToast]);

  const handleSettingDelete = useCallback(async (id: string) => {
    const setting = worldData.settings.find((s) => s.id === id);
    if (!setting) return;

    const confirmed = await confirm({
      title: t('workDetail.dialog.deleteSetting.title'),
      message: t('workDetail.dialog.deleteSetting.message', { title: setting.title }),
      confirmText: t('common.delete'),
      cancelText: t('common.cancel'),
      variant: 'danger',
    });

    if (!confirmed) {
      return;
    }

    try {
      // 从状态中删除
      setWorldData((prev) => ({
        ...prev,
        settings: prev.settings.filter((s) => s.id !== id),
      }));

      // 从后端删除
      await DataService.deleteSetting(id);
      showToast('success', t('workDetail.toast.settingDeleteSuccess'));
    } catch (error) {
      showToast('error', t('workDetail.toast.settingDeleteFailed'));
      console.error('Failed to delete setting:', error);
    }
  }, [worldData.settings, showToast]);

  /**
   * 作品规范 - 保存规范
   */
  const handleGuidelinesSave = useCallback(async (guidelines: Partial<WorkGuidelines>) => {
    if (!workId) return;

    try {
      // 更新本地状态
      setWorldData((prev) => ({
        ...prev,
        guidelines: {
          ...prev.guidelines,
          ...guidelines,
          workId,
          updatedAt: new Date(),
        } as any,
      }));

      // 保存到后端
      await DataService.saveGuidelines(workId, guidelines);

      showToast('success', t('workDetail.toast.guidelinesSaveSuccess'));
      console.log('[WorkDetailView] 作品规范已保存:', guidelines);
    } catch (error) {
      showToast('error', t('workDetail.toast.guidelinesSaveFailed'));
      console.error('Failed to save guidelines:', error);
    }
  }, [workId, showToast]);

  /**
   * AI创作规范 - 保存规范
   */
  const handleAIGuidelinesSave = useCallback(async (aiGuidelines: any) => {
    if (!workId) return;

    try {
      // 更新本地状态
      setWorldData((prev) => ({
        ...prev,
        aiGuidelines: {
          ...prev.aiGuidelines,
          ...aiGuidelines,
          workId,
        },
      }));

      // 保存到后端
      await DataService.saveAIGuidelines(workId, aiGuidelines);
      showToast('success', t('workDetail.toast.aiGuidelinesSaveSuccess'));
    } catch (error) {
      showToast('error', t('workDetail.toast.aiGuidelinesSaveFailed'));
      console.error('Failed to save AI guidelines:', error);
    }
  }, [workId, showToast]);

  /**
   * 拖动调整右侧面板宽度
   */
  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    // 记录拖拽起始位置和当前宽度
    resizeStartX.current = e.clientX;
    resizeStartWidth.current = rightPanelWidth;
    setIsResizing(true);
  }, [rightPanelWidth]);

  useEffect(() => {
    if (!isResizing) return;

    const handleMouseMove = (e: MouseEvent) => {
      // 计算鼠标移动的差值
      const diff = e.clientX - resizeStartX.current;
      // 往右拉 diff > 0，面板变大；往左拉 diff < 0，面板变小
      const newWidth = resizeStartWidth.current + diff;

      // 限制最小和最大宽度
      const minWidth = 240; // 最小 240px
      const maxWidth = 900; // 最大 900px
      const clampedWidth = Math.max(minWidth, Math.min(maxWidth, newWidth));

      rightPanelWidthRef.current = clampedWidth;
      setRightPanelWidth(clampedWidth);
    };

    const handleMouseUp = () => {
      setIsResizing(false);
      // 保存到 localStorage
      localStorage.setItem('rightPanelWidth', rightPanelWidthRef.current.toString());
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    // 防止文本选中
    document.body.style.userSelect = 'none';
    document.body.style.cursor = 'col-resize';

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.userSelect = '';
      document.body.style.cursor = '';
    };
  }, [isResizing]);

  useEffect(() => {
    rightPanelWidthRef.current = rightPanelWidth;
  }, [rightPanelWidth]);

  const findScrollableParent = useCallback((target: HTMLElement) => {
    const boundary = workbenchRef.current;
    let node: HTMLElement | null = target;
    while (node && node !== boundary) {
      const style = window.getComputedStyle(node);
      const overflowY = style.overflowY;
      const isScrollable = (overflowY === 'auto' || overflowY === 'scroll') && node.scrollHeight > node.clientHeight;
      if (isScrollable) return node;
      node = node.parentElement;
    }
    return null;
  }, []);

  const canScroll = useCallback((node: HTMLElement, deltaY: number) => {
    if (deltaY < 0) {
      return node.scrollTop > 0;
    }
    if (deltaY > 0) {
      return node.scrollTop + node.clientHeight < node.scrollHeight;
    }
    return false;
  }, []);

  const handleGlobalWheel = useCallback((event: React.WheelEvent<HTMLDivElement>) => {
    if (event.defaultPrevented || event.ctrlKey) return;
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;
    if (target.closest('[data-scroll-scope="chapter-list"]')) {
      return;
    }
    if (target.closest('input, textarea, select, [contenteditable="true"], .ProseMirror')) {
      return;
    }
    const aiContainer = document.querySelector('[data-ai-scroll-container="active"]') as HTMLElement | null;
    if (!aiContainer || aiContainer.clientHeight === 0) return;
    const scrollableParent = findScrollableParent(target);
    if (scrollableParent) {
      if (scrollableParent === aiContainer || canScroll(scrollableParent, event.deltaY)) {
        return;
      }
    }
    if (aiContainer.scrollHeight <= aiContainer.clientHeight) return;
    aiContainer.scrollTop += event.deltaY;
  }, [canScroll, findScrollableParent]);

  // 🆕 监听 Agent 章节操作的乐观更新事件
  useEffect(() => {
    const handleChapterPreview = (e: Event) => {
      const customEvent = e as CustomEvent;
      const { action_type, request_id, work_id, chapter_id, chapter_title, new_title, content, order } = customEvent.detail;

      // 只处理当前作品的事件
      if (work_id !== workId) return;

      if (action_type === 'create') {
        // 创建章节：立即添加到列表（带 _pending 标记）
        setChapters(prev => {
          const now = new Date().toISOString();
          const newChapter: Chapter = {
            id: chapter_id,
            workId: work_id,  // 驼峰命名
            title: chapter_title || '新章节',
            content: content || '',
            order: order || prev.length + 1,
            wordCount: 0,
            viewCount: 0,
            isPublished: false,
            publishedAt: null,
            createdAt: now,
            updatedAt: now,
            status: 'draft',
            // 乐观更新标记
            _pending: true,
            _request_id: request_id
          } as any;
          console.log('[WorkDetailView] 🆕 添加预览章节:', chapter_title);
          return [...prev, newChapter];
        });
      } else if (action_type === 'rename') {
        // 重命名：立即更新标题
        setChapters(prev => prev.map(ch => {
          if (ch.id === chapter_id) {
            return { ...ch, title: new_title, _pending: true, _old_title: ch.title, _request_id: request_id } as any;
          }
          return ch;
        }));
        console.log('[WorkDetailView] 🔄 预览重命名:', new_title);
      } else if (action_type === 'delete') {
        // 删除：标记为待删除
        setChapters(prev => prev.map(ch => {
          if (ch.id === chapter_id) {
            return { ...ch, _pending_delete: true, _request_id: request_id } as any;
          }
          return ch;
        }));
        console.log('[WorkDetailView] 🗑️ 标记待删除:', chapter_id);
      }
    };

    const handleChapterRevert = (e: Event) => {
      const customEvent = e as CustomEvent;
      const { action_type, request_id, work_id, chapter_id } = customEvent.detail;

      // 只处理当前作品的事件
      if (work_id !== workId) return;

      if (action_type === 'create') {
        // 移除预览章节
        setChapters(prev => prev.filter(ch => (ch as any)._request_id !== request_id));
        console.log('[WorkDetailView] 🗑️ 移除预览章节');
      } else if (action_type === 'rename') {
        // 恢复原标题
        setChapters(prev => prev.map(ch => {
          if ((ch as any)._request_id === request_id && (ch as any)._old_title) {
            const { _pending, _old_title, _request_id, ...rest } = ch as any;
            return { ...rest, title: _old_title };
          }
          return ch;
        }));
        console.log('[WorkDetailView] 🔄 恢复原标题');
      } else if (action_type === 'delete') {
        // 移除待删除标记
        setChapters(prev => prev.map(ch => {
          if ((ch as any)._request_id === request_id) {
            const { _pending_delete, _request_id, ...rest } = ch as any;
            return rest;
          }
          return ch;
        }));
        console.log('[WorkDetailView] ✅ 取消删除标记');
      }
    };

    const handleChapterConfirm = async (e: Event) => {
      const customEvent = e as CustomEvent;
      const { work_id } = customEvent.detail;
      // 只处理当前作品的事件
      if (work_id !== workId) return;

      // 从数据库重新加载章节列表
      if (!workId) return;
      try {
        const freshChapters = await DataService.getChapters(workId);
        setChapters(freshChapters);
        console.log('[WorkDetailView] 🔄 从数据库刷新章节列表');
      } catch (err) {
        console.error('[WorkDetailView] 刷新章节列表失败:', err);
      }
    };

    const refreshChaptersAndContent = async () => {
      if (!workId) return;
      try {
        const freshChapters = await DataService.getChapters(workId);
        setChapters(freshChapters);

        const activeChapterId = editorChapterIdRef.current || currentChapterId;
        if (activeChapterId) {
          const activeChapter = freshChapters.find(ch => ch.id === activeChapterId);
          if (activeChapter) {
            setCurrentChapterContent(activeChapter.content || '');
          }
        }

        console.log('[WorkDetailView] 🔄 刷新章节列表与当前内容');
      } catch (err) {
        console.error('[WorkDetailView] 刷新章节列表失败:', err);
      }
    };

    // v8.0: 监听操作回滚事件，刷新章节列表
    const handleOperationsRollback = async () => {
      await refreshChaptersAndContent();
    };

    const handleOperationsApplied = async () => {
      await refreshChaptersAndContent();
    };

    const handleJumpRevision = (e: Event) => {
      const customEvent = e as CustomEvent<{
        workId?: string;
        chapterId?: string;
      }>;
      const { workId: targetWorkId, chapterId: targetChapterId } = customEvent.detail || {};
      if (targetWorkId && targetWorkId !== workId) return;
      if (isEditorCollapsed) {
        setIsEditorCollapsed(false);
      }
      if (!targetChapterId || targetChapterId === currentChapterId) return;
      handleChapterSelect(targetChapterId);
    };

    window.addEventListener('agent-chapter-preview', handleChapterPreview as EventListener);
    window.addEventListener('agent-chapter-revert', handleChapterRevert as EventListener);
    window.addEventListener('agent-chapter-confirm', handleChapterConfirm as EventListener);
    window.addEventListener('agent-operations-rollback', handleOperationsRollback as EventListener);
    window.addEventListener('agent-operations-applied', handleOperationsApplied as EventListener);
    window.addEventListener('agent-jump-revision', handleJumpRevision as EventListener);

    return () => {
      window.removeEventListener('agent-chapter-preview', handleChapterPreview as EventListener);
      window.removeEventListener('agent-chapter-revert', handleChapterRevert as EventListener);
      window.removeEventListener('agent-chapter-confirm', handleChapterConfirm as EventListener);
      window.removeEventListener('agent-operations-rollback', handleOperationsRollback as EventListener);
      window.removeEventListener('agent-operations-applied', handleOperationsApplied as EventListener);
      window.removeEventListener('agent-jump-revision', handleJumpRevision as EventListener);
    };
  }, [workId, currentChapterId, handleChapterSelect, isEditorCollapsed]);

  // 如果 workId 不存在，不渲染任何内容（路由已切换到其他页面）
  if (!workId) {
    return null;
  }

  if (isLoading) {
    return <Loading />;
  }

  if (error || !work) {
    return (
      <div className={styles.errorContainer}>
        <div className={styles.errorContent}>
          <p className={styles.errorText}>{error || t('workDetail.error.workNotExist')}</p>
          <Button onClick={() => navigate('/works')}>{t('workDetail.actions.backToWorks')}</Button>
        </div>
      </div>
    );
  }

  // 转换章节数据为 NovelChapter 格式
  const novelChapters = convertToNovelChapters(chapters);

  return (
    <>
      <div
        ref={workbenchRef}
        onWheelCapture={handleGlobalWheel}
        className="flex bg-zinc-50/30 dark:bg-slate-900 h-full"
      >
        {/* 左侧章节面板 */}
        <div
          className={`bg-gradient-to-b from-white to-zinc-50/30 dark:from-slate-900 dark:to-slate-900 flex flex-col border-r border-zinc-100/80 dark:border-slate-700 transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] h-full overflow-hidden ${
            isLeftCollapsed ? 'w-0 border-r-0' : 'w-60'
          }`}
          data-scroll-scope="chapter-list"
        >
          {isLeftCollapsed ? null : (
            /* 展开状态 */
            <div className="flex-1 flex flex-col min-h-0">
              {/* 标题区域 - 与右侧工具栏对齐 */}
              <div className="px-3 py-1.5 flex items-center justify-between flex-shrink-0">
                <h2 className="text-[15px] text-zinc-800 dark:text-slate-100 tracking-tight">{t('workDetail.title')}</h2>
                <div className="flex items-center gap-1">
                  <button
                    type="button"
                    onClick={() => handleAddChapter()}
                    className="h-7 w-7 p-0 flex items-center justify-center text-zinc-500 hover:text-zinc-900 hover:bg-white hover:shadow-sm rounded-lg transition-all dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800"
                  >
                    <Plus className="h-5 w-5" />
                  </button>
                </div>
              </div>

              {/* 章节列表 */}
              <div className="flex-1 overflow-y-auto custom-scrollbar min-h-0 px-2 py-2">
                <div className="space-y-1">
                  {/* 新章节输入框 */}
                  {isAddingChapter && (
                    <div className="relative px-3 py-2.5 rounded-xl bg-white shadow-lg shadow-zinc-200/60 ring-1 ring-zinc-900/5 transition-all dark:bg-slate-800 dark:shadow-slate-900/40 dark:ring-slate-700">
                      {/* 顶部装饰线 */}
                      <div className="absolute top-0 left-3 right-3 h-0.5 rounded-full bg-gradient-to-r from-zinc-400 via-zinc-600 to-zinc-400 dark:from-blue-500 dark:via-blue-400 dark:to-blue-500" />

                      <div className="flex items-start gap-3 pt-0.5">
                        {/* 章节编号占位 */}
                        <div className="flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-[11px] bg-zinc-100/80 text-zinc-400 dark:bg-slate-700 dark:text-slate-400">
                          {chapters.length + 1}
                        </div>

                        {/* 输入框 */}
                        <div className="flex-1 min-w-0">
                          <input
                            autoFocus
                            type="text"
                            value={newChapterTitle}
                            onChange={(e) => setNewChapterTitle(e.target.value)}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') {
                                handleSaveNewChapter();
                              } else if (e.key === 'Escape') {
                                handleCancelAddChapter();
                              }
                            }}
                            placeholder={t('workDetail.chapter.titlePlaceholder')}
                            className="h-7 w-full text-[13px] border-0 px-0 bg-transparent focus:ring-0 focus:outline-none focus-visible:ring-0 focus-visible:outline-none placeholder:text-zinc-400 dark:text-slate-100 dark:placeholder:text-slate-500"
                            style={{ outline: 'none', boxShadow: 'none' }}
                          />

                          {/* 操作按钮 */}
                          <div className="flex items-center justify-between mt-2">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={handleCancelAddChapter}
                              className="h-6 px-2 text-[10px] bg-transparent hover:bg-zinc-100 text-zinc-500 hover:text-zinc-700 border-0 shadow-none dark:hover:bg-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
                            >
                              {t('common.cancel')}
                            </Button>
                            <Button
                              size="sm"
                              onClick={handleSaveNewChapter}
                              className="h-6 px-2 text-[10px] bg-zinc-800 hover:bg-zinc-900 text-white border-0 dark:bg-blue-600 dark:hover:bg-blue-500"
                            >
                              {t('common.save')}
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {novelChapters.map((chapter, index) => (
                    <div
                      key={chapter.id}
                      onClick={() => handleChapterSelect(chapter.id)}
                      className={`group relative px-3 py-2.5 rounded-xl cursor-pointer transition-all duration-300 ${
                        chapter.id === currentChapterId
                          ? 'bg-white shadow-lg shadow-zinc-200/60 ring-1 ring-zinc-900/5 dark:bg-slate-800 dark:shadow-slate-900/40 dark:ring-slate-700'
                          : 'text-zinc-700 hover:bg-white/60 hover:shadow-md hover:shadow-zinc-100 dark:text-slate-300 dark:hover:bg-slate-800/60'
                      }`}
                    >
                      {/* 顶部装饰线 */}
                      <div className={`absolute top-0 left-3 right-3 h-0.5 rounded-full transition-all duration-300 ${
                        chapter.id === currentChapterId
                          ? 'bg-gradient-to-r from-zinc-400 via-zinc-600 to-zinc-400 dark:from-blue-500 dark:via-blue-400 dark:to-blue-500'
                          : 'bg-transparent group-hover:bg-zinc-200 dark:group-hover:bg-slate-700'
                      }`} />

                      <div className="flex items-start gap-3 pt-0.5">
                        {/* 章节编号 */}
                        <div className={`flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-[11px] font-medium transition-all duration-300 ${
                          chapter.id === currentChapterId
                            ? 'bg-gradient-to-br from-zinc-700 to-zinc-900 text-white shadow-md shadow-zinc-900/20 dark:from-blue-600 dark:to-blue-700'
                            : 'bg-zinc-100/80 text-zinc-500 group-hover:bg-zinc-200 group-hover:text-zinc-700 dark:bg-slate-700 dark:text-slate-400 dark:group-hover:bg-slate-600 dark:group-hover:text-slate-300'
                        }`}>
                          {index + 1}
                        </div>

                        {/* 章节内容 */}
                        <div className="flex-1 min-w-0">
                          {editingChapterId === chapter.id ? (
                            /* 编辑模式 */
                            <div className="flex flex-col gap-2">
                              <input
                                autoFocus
                                type="text"
                                value={editingChapterTitle}
                                onChange={(e) => setEditingChapterTitle(e.target.value)}
                                onKeyDown={(e) => {
                                  e.stopPropagation();
                                  if (e.key === 'Enter') {
                                    handleSaveChapterTitle();
                                  } else if (e.key === 'Escape') {
                                    handleCancelRenameChapter();
                                  }
                                }}
                                onClick={(e) => e.stopPropagation()}
                                className="h-7 w-full text-[13px] border-0 px-0 bg-transparent focus:ring-0 focus:outline-none focus-visible:ring-0 focus-visible:outline-none placeholder:text-zinc-400 dark:text-slate-100 dark:placeholder:text-slate-500"
                                style={{ outline: 'none', boxShadow: 'none' }}
                              />
                              <div className="flex items-center justify-between">
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleCancelRenameChapter();
                                  }}
                                  className="h-6 px-2 text-[10px] bg-transparent hover:bg-zinc-100 text-zinc-500 hover:text-zinc-700 border-0 shadow-none dark:hover:bg-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
                                >
                                  {t('common.cancel')}
                                </Button>
                                <Button
                                  size="sm"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleSaveChapterTitle();
                                  }}
                                  className="h-6 px-2 text-[10px] bg-zinc-800 hover:bg-zinc-900 text-white border-0 dark:bg-blue-600 dark:hover:bg-blue-500"
                                >
                                  {t('common.save')}
                                </Button>
                              </div>
                            </div>
                          ) : (
                            /* 显示模式 */
                            <>
                              <div className="flex items-start justify-between gap-1">
                                <div className={`text-[13px] leading-snug truncate flex-1 transition-colors duration-300 ${
                                  chapter.id === currentChapterId ? 'text-zinc-900 dark:text-slate-100' : 'text-zinc-700 dark:text-slate-300'
                                }`}>
                                  {chapter.title.replace(/^第\d+章\s*/, '')}
                                </div>
                                <div className="flex items-center gap-0.5 flex-shrink-0">
                                  {/* 铅笔按钮 - 编辑章节名称 */}
                                  <button
                                    type="button"
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      handleStartRenameChapter(chapter.id, chapter.title);
                                    }}
                                    className={`h-6 w-6 p-0 rounded flex items-center justify-center border-0 bg-transparent opacity-0 group-hover:opacity-100 transition-all ${
                                      chapter.id === currentChapterId
                                        ? 'text-zinc-400 hover:text-zinc-700 hover:bg-zinc-100 dark:text-slate-500 dark:hover:text-slate-200 dark:hover:bg-slate-700'
                                        : 'text-zinc-400 hover:text-zinc-600 hover:bg-zinc-100 dark:text-slate-500 dark:hover:text-slate-300 dark:hover:bg-slate-700'
                                    }`}
                                    aria-label={t('workDetail.actions.editChapterTitle')}
                                  >
                                    <svg
                                      xmlns="http://www.w3.org/2000/svg"
                                      width="12"
                                      height="12"
                                      viewBox="0 0 24 24"
                                      fill="none"
                                      stroke="currentColor"
                                      strokeWidth="2"
                                      strokeLinecap="round"
                                      strokeLinejoin="round"
                                    >
                                      <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z" />
                                      <path d="m15 5 4 4" />
                                    </svg>
                                  </button>
                                  {/* 删除按钮 */}
                                  <button
                                    type="button"
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      setChapterToDelete(chapter.id);
                                      setDeleteDialogOpen(true);
                                    }}
                                    className={`h-6 w-6 p-0 rounded flex items-center justify-center border-0 bg-transparent opacity-0 group-hover:opacity-100 transition-all ${
                                      chapter.id === currentChapterId
                                        ? 'text-zinc-400 hover:text-red-500 hover:bg-red-50/80 dark:text-slate-500 dark:hover:text-red-400 dark:hover:bg-red-900/30'
                                        : 'text-zinc-400 hover:text-red-500 hover:bg-red-50 dark:text-slate-500 dark:hover:text-red-400 dark:hover:bg-red-900/30'
                                    }`}
                                    aria-label={t('workDetail.actions.deleteChapter')}
                                  >
                                    <svg
                                      xmlns="http://www.w3.org/2000/svg"
                                      width="12"
                                      height="12"
                                      viewBox="0 0 24 24"
                                      fill="none"
                                      stroke="currentColor"
                                      strokeWidth="2"
                                      strokeLinecap="round"
                                      strokeLinejoin="round"
                                    >
                                      <path d="M3 6h18"></path>
                                      <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                                      <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                                      <line x1="10" x2="10" y1="11" y2="17"></line>
                                      <line x1="14" x2="14" y1="11" y2="17"></line>
                                    </svg>
                                  </button>
                                </div>
                              </div>

                              {/* 字数统计与进度 */}
                              <div className="flex items-center gap-2 mt-2">
                                <div className={`text-[10px] transition-colors duration-300 ${
                                  chapter.id === currentChapterId ? 'text-zinc-500 dark:text-slate-400' : 'text-zinc-400 dark:text-slate-500'
                                }`}>
                                  {chapter.wordCount.toLocaleString()} {t('workDetail.chapter.words')}
                                </div>
                                {/* 进度指示器 */}
                                <div className={`flex-1 h-1 rounded-full transition-all duration-300 ${
                                  chapter.id === currentChapterId ? 'bg-zinc-100 dark:bg-slate-700' : 'bg-zinc-100/60 dark:bg-slate-700/50'
                                }`}>
                                  <div
                                    className={`h-full rounded-full transition-all duration-500 ${
                                      chapter.id === currentChapterId
                                        ? 'bg-gradient-to-r from-zinc-500 via-zinc-600 to-zinc-700 shadow-sm dark:from-blue-500 dark:via-blue-400 dark:to-blue-500'
                                        : 'bg-zinc-300 group-hover:bg-zinc-400 dark:bg-slate-600 dark:group-hover:bg-slate-500'
                                    }`}
                                    style={{ width: `${Math.min((chapter.wordCount / 5000) * 100, 100)}%` }}
                                  />
                                </div>
                              </div>
                            </>
                          )}
                        </div>
                      </div>

                      {/* 底部微光效果 */}
                      {chapter.id === currentChapterId && (
                        <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-zinc-200/50 to-transparent dark:via-slate-700" />
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* 中间 AI 面板区域 */}
        <div
          className={`relative bg-white dark:bg-slate-900 flex flex-col overflow-hidden ${isResizing ? '' : 'transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)]'}`}
          style={{
            flexGrow: isRightCollapsed ? 0 : (isEditorCollapsed ? 1 : 0),
            flexShrink: 1,
            flexBasis: `${isRightCollapsed ? COLLAPSED_RIGHT_PANEL_WIDTH : rightPanelWidth}px`,
          }}
        >
          {/* 可拖动的分隔条 - 仅在非收缩模式显示 */}
          {!isRightCollapsed && !isEditorCollapsed && (
            <div
              onMouseDown={handleMouseDown}
              className="absolute right-0 top-0 bottom-0 w-1 cursor-col-resize hover:bg-blue-400 transition-colors z-10 group"
              style={{ marginRight: '-2px' }}
            >
              <div className="absolute inset-y-0 -left-1 -right-1" />
            </div>
          )}

            <div className={`flex flex-col h-full min-h-0 ${isRightCollapsed ? 'opacity-0 pointer-events-none select-none' : ''}`}>
            {/* SessionTabBar - 始终占满宽度 */}
            <SessionTabBar
              tabs={tabs}
              activeTabId={activeTabId}
              onSwitchTab={switchTab}
              onCreateTab={createTab}
              onCloseTab={closeTab}
              onOpenHistory={handleOpenHistory}
              isLeftPanelCollapsed={isLeftCollapsed}
              onExpandLeftPanel={() => setIsLeftCollapsed(false)}
              onCollapseLeftPanel={() => setIsLeftCollapsed(true)}
              isEditorCollapsed={isEditorCollapsed}
              onToggleEditor={() => setIsEditorCollapsed(!isEditorCollapsed)}
            />

            {/* 内容区 - AIPanel 始终处理自己的滚动 */}
            <div className={`flex-1 min-h-0 overflow-hidden`}>
                <div className="h-full">
                {tabs.map((tab) => (
                  <div
                    key={tab.id}
                    style={{
                      display: tab.id === activeTabId ? 'block' : 'none',
                      height: '100%'
                    }}
                  >
                    <AIPanel
                      workId={workId!}
                      chapterId={currentChapterId}
                      sessionId={tab.sessionId}
                      onTitleChange={(title) => updateTabTitle(tab.id, title)}
                      isActive={tab.id === activeTabId}
                      expandedMode={isEditorCollapsed}
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* 右侧编辑器窗口 - 圆弧样式 */}
        <div
          className="flex flex-col bg-white dark:bg-slate-900 transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)]"
          style={{
            flex: isEditorCollapsed ? '0 0 0' : '1 1 0%',
            padding: isEditorCollapsed ? 0 : 12,
            opacity: isEditorCollapsed ? 0 : 1,
            overflow: 'hidden',
          }}
        >
          <div className="flex-1 flex flex-col rounded-2xl border border-zinc-200 dark:border-slate-700 bg-white dark:bg-slate-900 shadow-xl shadow-zinc-300/30 dark:shadow-slate-950/50 overflow-hidden">
            {rightSidebarType === 'worldview' ? (
              <WorldviewPanel
                workId={workId!}
                worldData={worldData}
                initialTab={worldviewInitialTab}
                targetItemId={worldviewTargetItemId}
                onTargetItemScrolled={() => setWorldviewTargetItemId(undefined)}
                onWorldDataUpdate={refreshWorldData}
              />
            ) : (
              <NovelEditor
                key={currentChapterId}
                content={currentChapterContent}
                onSave={handleEditorSave}
                placeholder={t('editor.startWriting')}
                autoSave={true}
                autoSaveInterval={3000}
                chapterTitle={currentChapterMeta?.title}
                chapterOrder={currentChapterMeta?.order}
                workId={workId}
                chapterId={currentChapterId || undefined}
                aiAutoCompleteEnabled={aiAutoCompleteEnabled}
                onToggleAIAutoComplete={handleToggleAIAutoComplete}
                isLeftPanelCollapsed={isLeftCollapsed}
                onExpandLeftPanel={() => setIsLeftCollapsed(false)}
                onCollapseLeftPanel={() => setIsLeftCollapsed(true)}
                isRightPanelCollapsed={isEditorCollapsed}
                onExpandRightPanel={() => setIsEditorCollapsed(false)}
                onCollapseRightPanel={() => setIsEditorCollapsed(true)}
                isAIPanelCollapsed={isRightCollapsed}
                onToggleAIPanel={() => setIsRightCollapsed(false)}
                onCollapseAIPanel={() => setIsRightCollapsed(true)}
              />
            )}
          </div>
        </div>
      </div>

      {/* 确认对话框 */}
      <ConfirmDialog
        isOpen={confirmState.isOpen}
        title={confirmState.title}
        message={confirmState.message}
        confirmText={confirmState.confirmText}
        cancelText={confirmState.cancelText}
        variant={confirmState.variant}
        onConfirm={confirmState.onConfirm}
        onCancel={closeConfirm}
      />

      {/* 导出对话框 */}
      {showExportDialog && (
        <ExportDialog
          workId={workId!}
          workTitle={work.title}
          onClose={() => setShowExportDialog(false)}
        />
      )}

      {showHistoryPanel && (
        <HistoryPanel
          workId={workId}
          chapterId={currentChapterId}
          onClose={handleCloseHistory}
          onRestore={handleRestoreHistorySession}
        />
      )}

      {/* 删除章节确认对话框 */}
      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent className="max-w-md">
          <AlertDialogHeader>
            <AlertDialogTitle className="text-[15px] text-zinc-900">{t('workDetail.dialog.deleteChapter.title')}</AlertDialogTitle>
            <AlertDialogDescription className="text-[13px] text-zinc-500 leading-relaxed">
              {t('workDetail.dialog.deleteChapter.message')}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel className="text-[12px] h-8 bg-transparent hover:bg-zinc-100 text-zinc-600 hover:text-zinc-900 border-zinc-200">
              {t('common.cancel')}
            </AlertDialogCancel>
            <AlertDialogAction
              onClick={async () => {
                if (chapterToDelete) {
                  await executeDeleteChapter(chapterToDelete);
                  setChapterToDelete(null);
                }
              }}
              className="text-[12px] h-8 bg-red-500 hover:bg-red-600 text-white"
            >
              {t('common.delete')}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
};

export default WorkDetailView;
