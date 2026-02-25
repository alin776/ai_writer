import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useParams, Link, useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ArrowLeft, Edit, Trash2, BookOpen, BarChart3, BookMarked, Download, MessageSquare, ChevronLeft, ChevronRight } from 'lucide-react';
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
import { chaptersFs } from '../../services/chaptersFs';
import { docsFs } from '../../services/docsFs';
import type { FileNode } from '../../services/docsFs';
import { fsToChapter, chapterIdToNum, isDocId, docIdToPath } from '../../utils/fsChapterAdapter';
import { FileTreePanel } from '../../components/sidebar/FileTreePanel';
import { useGlobalStore } from '../../store/globalStore';
import { useAuthStore } from '../../store/authStore';
import type { Work, Chapter, CreateChapterData } from '../../types';
import type { Chapter as NovelChapter, WorldData, Character, Location, Setting, WorkGuidelines } from '../../types/novel';
import { formatDate } from '../../utils/formatDate';
import EditorWrapper from '../../components/editor/EditorWrapper';
import { WorldviewPanel } from '../../components/editor/WorldviewPanel';
import { AIPanel } from '../../components/editor/AIPanel';
import SessionTabBar from '../../components/editor/SessionTabBar';
import { useEditorStore } from '../../store/editorStore';
import { useWorkNavStore } from '../../store/workNavStore';
import { useConfirm } from '../../hooks/useConfirm';
import { useTabManager } from '../../hooks/useTabManager';
import { useEditorTabs } from '../../hooks/useEditorTabs';
import HistoryPanel from '../../components/agent/HistoryPanel';
import type { HistorySessionItem } from '@/types/agent';
import { agentApi } from '@/services/agentApi';
import styles from './WorkDetailView.module.css';

/** UUID v4 格式正则（用于过滤可安全发给后端 API 的 session ID） */
const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

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
    (location.state as Record<string, any> | null)?.fromCreate
  );

  if (workId && autoExtractWorkIdRef.current !== workId) {
    autoExtractFromImportRef.current = false;
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
  const [fileTree, setFileTree] = useState<FileNode[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 编辑器相关状态
  const [currentChapterId, setCurrentChapterId] = useState<string | undefined>(undefined);
  const [currentChapterContent, setCurrentChapterContent] = useState<string>('');
  // 用于追踪编辑器当前加载的章节 ID，防止异步保存时的竞态条件
  const editorChapterIdRef = React.useRef<string | undefined>(undefined);
  // 防止 StrictMode 双重触发时重复创建默认章节
  const isCreatingDefaultChapterRef = React.useRef(false);
  // diff 预览标志：RevisionCard 跳转时设为 true，跳过自动保存避免覆写未采纳内容
  const diffPreviewRef = React.useRef(false);
  // Track in-flight editor save so worldview sync can wait for disk flush.
  const pendingEditorSaveRef = React.useRef<Promise<void> | null>(null);

  // Worldview data
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

  const refreshFileTree = useCallback(async () => {
    if (!workId) return;
    try {
      const tree = await docsFs.tree(workId);
      setFileTree(tree);
    } catch (error) {
      console.warn('[WorkDetailView] Failed to refresh file tree:', error);
    }
  }, [workId]);

  const handleWorldviewPanelDataUpdate = useCallback(() => {
    // 世界观面板触发更新时，同时刷新卡片数据与文件树（知识库镜像文件）
    void refreshWorldData();
    void refreshFileTree();
  }, [refreshWorldData, refreshFileTree]);

  const waitForPendingEditorSave = useCallback(async () => {
    const pending = pendingEditorSaveRef.current;
    if (!pending) return;
    try {
      await pending;
    } catch (error) {
      console.warn('[WorkDetailView] Failed while waiting for editor save; continue sync:', error);
    }
  }, []);

  const hasWorldviewCards = worldData.characters.length + worldData.locations.length + worldData.settings.length > 0;

  useEffect(() => {
    if (!workId || !autoExtractFromImport || hasWorldviewCards) return;

    let cancelled = false;
    let notified = false;
    let idleAttempts = 0;
    const maxIdleAttempts = 5;
    let timer: ReturnType<typeof setTimeout> | null = null;

    const poll = async () => {
      if (cancelled || !workId) return;
      try {
        const progress = await DataService.getWorldviewScanProgress(workId);

        if (progress.status === 'idle') {
          idleAttempts += 1;
          const hasNewCards = await refreshWorldData();
          if (hasNewCards || idleAttempts >= maxIdleAttempts) {
            return 'stop';
          }
          return 'idle';
        }

        if (progress.status === 'running' || progress.status === 'pending' || progress.status === 'preparing' || progress.status === 'applying') {
          if (!notified) {
            showToast('info', '世界观解析进行中...');
            notified = true;
          }
          return 'running';
        }

        if (progress.status === 'completed') {
          await refreshWorldData();
          showToast('success', '世界观解析完成，已更新世界观');
          return 'stop';
        }

        if (progress.status === 'failed') {
          showToast('error', progress.lastError || '世界观解析失败');
          return 'stop';
        }
      } catch (error) {
        console.warn('[WorkDetailView] 获取世界观解析进度失败:', error);
        return 'idle';
      }
    };

    const scheduleNext = async () => {
      const status = await poll();
      if (cancelled || status === 'stop') return;
      const delay = status === 'running' ? 5000 : 8000;
      timer = setTimeout(scheduleNext, delay);
    };

    scheduleNext();

    return () => {
      cancelled = true;
      if (timer) {
        clearTimeout(timer);
      }
    };
  }, [workId, autoExtractFromImport, hasWorldviewCards, refreshWorldData, showToast]);
  // 世界观面板初始 tab（用于搜索导航定位）
  const [worldviewInitialTab, setWorldviewInitialTab] = useState<'characters' | 'places' | 'settings' | undefined>(undefined);
  // 世界观面板目标项 ID（用于搜索导航滚动定位）
  const [worldviewTargetItemId, setWorldviewTargetItemId] = useState<string | undefined>(undefined);
  const {
    tabs,
    activeTabId,
    isReady: isTabReady,
    createTab,
    closeTab,
    switchTab,
    updateTabTitle,
    replaceTabSession,
    attachSessionTab
  } = useTabManager(workId || '', workId);

  // 编辑器多标签页
  const {
    openTabs: editorTabs,
    activeTabId: activeEditorTabId,
    openTab: openEditorTab,
    closeTab: closeEditorTab,
    switchTab: switchEditorTab,
    updateTabTitle: updateEditorTabTitle,
  } = useEditorTabs(workId || '', chapters);

  const currentChapterMeta = chapters.find((chapter) => chapter.id === currentChapterId);
  const [showHistoryPanel, setShowHistoryPanel] = useState(false);
  const handleOpenHistory = useCallback(() => setShowHistoryPanel(true), []);
  const handleCloseHistory = useCallback(() => setShowHistoryPanel(false), []);

  const handleRestoreHistorySession = useCallback(
    async (session: HistorySessionItem) => {
      if (!activeTabId) return;

      // 尝试从后端拉取历史消息（conversationId 优先，它是后端 UUID）
      const allIds = Array.from(
        new Set([session.conversationId, session.sessionId].filter(Boolean) as string[])
      );
      // 只有 UUID 格式的 ID 才能安全地发给后端 API
      const backendIds = allIds.filter((id) => UUID_REGEX.test(id));

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
      for (const id of backendIds) {
        try {
          const resp = await agentApi.getSessionMessages(id, { order: 'asc', limit: 200 });
          const rawMessages = Array.isArray(resp) ? resp : Array.isArray((resp as any)?.messages) ? (resp as any).messages : [];

          messages = rawMessages.map((m: any) => ({
            role: m.role === 'assistant' ? 'agent' : m.role,
            content: m.content,
            metadata: m.metadata,
            timestamp: m.created_at || m.createdAt || new Date().toISOString()
          }));

          if (messages.length > 0 || backendIds.length === 1) {
            break;
          }
        } catch (error) {
          console.warn('[WorkDetailView] 加载历史消息失败，尝试下一个 ID:', id, error);
        }
      }

      // 后端为空时再尝试本地缓存（本地缓存可用任意格式 ID）
      if (messages.length === 0) {
        for (const id of allIds) {
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
          const [workDataResult, fsChapters, worldDataFromServerResult] = await Promise.all([
            DataService.getWork(workId),
            chaptersFs.list(workId),
            DataService.getWorldData(workId),
          ]);
          workData = workDataResult;
          chaptersData = fsChapters.map(fs => fsToChapter(fs, workId));
          worldDataFromServer = worldDataFromServerResult;
        }

        setLastWork(workId, workData?.title);
        setWork(workData);
        setChapters(chaptersData);

        // 加载文件树
        try {
          const tree = await docsFs.tree(workId);
          setFileTree(tree);
        } catch (err) {
          console.warn('[WorkDetailView] 加载文件树失败:', err);
        }
        setWorldData(worldDataFromServer as any);

        // 处理搜索导航的定位参数
        const searchNavState = location.state as {
          targetChapterId?: string;
          openWorldview?: boolean;
          worldviewTab?: 'characters' | 'locations' | 'settings';
          targetItemId?: string;
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
          setLastChapter(workId, targetChapter.id);

          // 初始加载时打开编辑器标签
          openEditorTab(targetChapter);

          // FS API: list 不含正文，需要单独加载内容
          try {
            const num = chapterIdToNum(targetChapter.id);
            if (num === null) return;
            const full = await chaptersFs.get(workId, num);
            const content = full.content || '';
            setCurrentChapterContent(content);
            // 更新本地缓存
            setChapters(prev => prev.map(c =>
              c.id === targetChapter.id ? { ...c, content } : c
            ));
          } catch {
            setCurrentChapterContent('');
          }
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
        }

        // 清除 location.state 中的搜索导航参数，避免刷新时重复执行
        if (searchNavState?.targetChapterId || searchNavState?.openWorldview) {
          if (nextLocationState) {
            delete (nextLocationState as Record<string, unknown>).targetChapterId;
            delete (nextLocationState as Record<string, unknown>).openWorldview;
            delete (nextLocationState as Record<string, unknown>).worldviewTab;
            delete (nextLocationState as Record<string, unknown>).targetItemId;
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

        // 如果没有章节，自动创建默认章节（ref 防重，避免 StrictMode 双重触发）
        if (chaptersData.length === 0 && !isCreatingDefaultChapterRef.current) {
          isCreatingDefaultChapterRef.current = true;
          try {
            const fsDefault = await chaptersFs.create(workId, {
              title: t('workDetail.chapter.firstChapter'),
            });
            const defaultChapter = fsToChapter(fsDefault, workId);
            setChapters([defaultChapter]);
            setCurrentChapterId(defaultChapter.id);
            setCurrentChapterContent('');
            // 保存默认章节ID到 store
            setLastChapter(workId, defaultChapter.id);
            showToast('info', t('workDetail.toast.autoCreatedFirstChapter'));
          } catch (createError) {
            console.error('Failed to create default chapter:', createError);
            // 创建失败时，显示错误提示但不设置undefined
            // 保持章节列表为空，让用户手动创建
            showToast('error', t('workDetail.toast.createChapterFailed'));
            // 不设置currentChapterId为undefined，保持初始状态
          } finally {
            isCreatingDefaultChapterRef.current = false;
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

  // 通过 useEffect 同步 editorChapterIdRef，确保卸载时 cleanup 仍能用旧 ID 保存
  useEffect(() => {
    if (currentChapterId) {
      editorChapterIdRef.current = currentChapterId;
    }
  }, [currentChapterId]);

  /**
   * 处理章节选择
   */
  const handleChapterSelect = useCallback(async (chapterId: string) => {
    diffPreviewRef.current = false;
    if (isEditorCollapsed) setIsEditorCollapsed(false);
    const chapter = chapters.find((c) => c.id === chapterId);
    if (chapter) {
      // 取消正在进行的章节重命名编辑
      if (editingChapterId) {
        setEditingChapterId(null);
        setEditingChapterTitle('');
      }

      // 打开编辑器标签
      openEditorTab(chapter);

      // 先清空内容，避免新编辑器用旧章节内容初始化（消除闪烁）
      setCurrentChapterContent('');
      // 再更新章节ID（触发 EditorWrapper 通过 key 重新挂载）
      setCurrentChapterId(chapterId);

      // 从 FS API 加载完整内容（list 不含正文）
      try {
        const num = chapterIdToNum(chapterId);
        if (num === null) return;
        const full = await chaptersFs.get(workId!, num);
        const content = full.content || '';
        setCurrentChapterContent(content);
        // 更新本地缓存
        setChapters(prev => prev.map(c =>
          c.id === chapterId ? { ...c, content } : c
        ));
      } catch {
        setCurrentChapterContent(chapter.content || '');
      }

      // 保存当前章节ID到 store，用于下次返回时恢复
      if (workId) {
        setLastChapter(workId, chapterId);
      }

      console.log('[WorkDetailView] 切换章节:', {
        chapterId,
        title: chapter.title,
      });
    }
  }, [chapters, editingChapterId, workId, setLastChapter, openEditorTab, isEditorCollapsed]);

  /**
   * 处理文件树选择（统一入口：章节走 handleChapterSelect，文档走 docsFs）
   */
  const handleFileSelect = useCallback(async (fileId: string) => {
    diffPreviewRef.current = false;
    if (isEditorCollapsed) setIsEditorCollapsed(false);
    if (isDocId(fileId)) {
      const path = docIdToPath(fileId);
      const fileName = path.split('/').pop() || path;
      openEditorTab({ id: fileId, title: fileName, order: 0 });
      setCurrentChapterContent('');
      setCurrentChapterId(fileId);
      try {
        const file = await docsFs.read(workId!, path);
        setCurrentChapterContent(file.content);
      } catch {
        setCurrentChapterContent('');
      }
    } else {
      handleChapterSelect(fileId);
    }
  }, [workId, handleChapterSelect, openEditorTab, isEditorCollapsed]);

  /**
   * 处理编辑器标签页切换（先加载内容，再切换编辑器）
   */
  const handleEditorTabSwitch = useCallback(async (tabId: string) => {
    diffPreviewRef.current = false;
    switchEditorTab(tabId);
    if (tabId === currentChapterId) return;

    // doc: 文件标签切换
    if (isDocId(tabId)) {
      const path = docIdToPath(tabId);
      setCurrentChapterContent('');
      setCurrentChapterId(tabId);
      editorChapterIdRef.current = tabId;
      try {
        const file = await docsFs.read(workId!, path);
        setCurrentChapterContent(file.content);
      } catch { /* ignore */ }
      return;
    }

    const chapter = chapters.find(c => c.id === tabId);
    if (!chapter) return;

    // 虚拟章节（缓冲区新建，磁盘不存在）→ 跳过 FS 加载，重新显示 diff
    if ((chapter as any)._pending) {
      setCurrentChapterContent((chapter as any)._diffModified || chapter.content || '');
      setCurrentChapterId(tabId);
      editorChapterIdRef.current = tabId;
      // EditorWrapper key 重挂载后重新触发 diff
      const diffModified = (chapter as any)._diffModified;
      if (diffModified) {
        setTimeout(() => {
          window.dispatchEvent(new CustomEvent('editor-inline-diff', {
            detail: { oldString: (chapter as any)._diffOriginal || '', newString: diffModified }
          }));
        }, 100);
      }
      return;
    }

    // 先加载内容，确保 EditorWrapper 重新挂载时有正确内容
    let content = chapter.content || '';
    try {
      const num = chapterIdToNum(tabId);
      if (num !== null) {
        const full = await chaptersFs.get(workId!, num);
        content = full.content || '';
      }
    } catch {
      // 使用本地缓存
    }

    // 同时更新内容和 chapterId，EditorWrapper 会用正确内容重新挂载
    setCurrentChapterContent(content);
    setCurrentChapterId(tabId);
    editorChapterIdRef.current = tabId;

    if (workId) {
      setLastChapter(workId, tabId);
    }
  }, [switchEditorTab, currentChapterId, chapters, workId, setLastChapter]);

  /**
   * 处理编辑器标签页关闭（同步清除编辑器内容）
   */
  const handleEditorTabClose = useCallback(async (tabId: string) => {
    // 先从当前 editorTabs 计算关闭后的新激活 tab
    const idx = editorTabs.findIndex(t => t.id === tabId);
    const remaining = editorTabs.filter(t => t.id !== tabId);

    // 关闭 tab（更新 editorTabs + activeEditorTabId）
    closeEditorTab(tabId);

    // 如果关闭的是当前正在显示的章节，需要同步编辑器内容
    if (tabId === currentChapterId) {
      if (remaining.length === 0) {
        // 所有 tab 都关闭了：清空编辑器并折叠面板
        setCurrentChapterId(undefined);
        setCurrentChapterContent('');
        setIsEditorCollapsed(true);
      } else {
        // 切换到相邻 tab（复用已有的切换逻辑加载内容）
        const newIdx = Math.min(idx, remaining.length - 1);
        await handleEditorTabSwitch(remaining[newIdx].id);
      }
    }
  }, [editorTabs, closeEditorTab, currentChapterId, handleEditorTabSwitch]);

  /**
   * 处理添加章节（文件树内联创建 chapters/ 下文件时调用）
   */
  const handleInlineChapterCreate = useCallback(async (title: string): Promise<FileNode[]> => {
    if (!workId) throw new Error('workId is missing');

    // 使用 FS API 创建章节（自动编号 + frontmatter）
    const fsChapter = await chaptersFs.create(workId, { title });
    const savedChapter = fsToChapter(fsChapter, workId);

    // 更新 chapters 状态
    setChapters((prev) => [...prev, savedChapter]);

    // 选中新章节
    setCurrentChapterContent('');
    setTimeout(() => {
      setCurrentChapterId(savedChapter.id);
      setCurrentChapterContent('');
      setLastChapter(workId, savedChapter.id);
    }, 0);

    showToast('success', t('workDetail.toast.chapterAddSuccess'));

    // 刷新文件树
    const tree = await docsFs.tree(workId);
    setFileTree(tree);

    // 自动触发分析
    try {
      await DataService.startNovelAnalysis(workId);
      showToast('info', t('workDetail.toast.triggeredAnalysisUpdate'));
    } catch (analysisError) {
      console.warn('[WorkDetailView] 自动分析触发失败:', analysisError);
    }

    return tree;
  }, [workId, showToast, setLastChapter, t]);

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

      // 更新后端（FS API）
      const num = chapterIdToNum(editingChapterId);
      if (num === null) return;
      const updatedFs = await chaptersFs.update(workId!, num, {
        title: editingChapterTitle.trim(),
      });
      const updatedChapter = fsToChapter(updatedFs, workId!);

      // 更新本地状态
      setChapters((prev) =>
        prev.map((c) => (c.id === editingChapterId ? updatedChapter : c))
      );

      // 同步更新编辑器标签标题
      updateEditorTabTitle(editingChapterId, updatedChapter.title, updatedChapter.order);

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
        // 新增章节（FS API）
        const fsChapter = await chaptersFs.create(workId, {
          title: chapterData.title.trim(),
          content: chapterData.content || '',
        });
        const savedChapter = fsToChapter(fsChapter, workId);

        // 更新章节列表
        setChapters((prev) => [...prev, savedChapter]);

        // 选中新章节
        setCurrentChapterId(savedChapter.id);
        setCurrentChapterContent(savedChapter.content);

        showToast('success', t('workDetail.toast.chapterAddSuccess'));
      } else {
        // 编辑章节（FS API）
        const chapter = chapters.find((c) => c.id === chapterData.id);
        if (!chapter) return;

        const num = chapterIdToNum(chapterData.id!);
        if (num === null) return;
        const updatedFs = await chaptersFs.update(workId, num, {
          title: chapterData.title.trim(),
          content: chapterData.content || chapter.content,
        });
        const updatedChapter = fsToChapter(updatedFs, workId);

        // 更新状态
        setChapters((prev) =>
          prev.map((c) => (c.id === chapterData.id ? updatedChapter : c))
        );

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
      // 关闭对应的编辑器标签
      closeEditorTab(chapterId);

      // 从 FS API 删除
      const num = chapterIdToNum(chapterId);
      if (num === null) return;
      await chaptersFs.remove(workId, num);

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
          const fsDefault = await chaptersFs.create(workId, {
            title: t('workDetail.chapter.firstChapter'),
          });
          const defaultChapter = fsToChapter(fsDefault, workId);
          setChapters([defaultChapter]);
          setCurrentChapterId(defaultChapter.id);
          setCurrentChapterContent('');
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
        // 保存新章节ID到 store
        setLastChapter(workId, remainingChapters[0].id);
      }

      showToast('success', t('workDetail.toast.chapterDeleteSuccess'));

      // 刷新文件树
      try {
        const tree = await docsFs.tree(workId);
        setFileTree(tree);
      } catch { /* ignore */ }
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
    showToast('info', '文件系统模式暂不支持拖拽排序');
  }, [showToast]);

  /**
   * 处理编辑器保存
   */
  const handleEditorSave = useCallback(async (content: string, json: any) => {
    if (!currentChapterId || !workId) {
      console.warn('[WorkDetailView] Save skipped: no active chapter');
      return;
    }

    // Skip autosave while previewing diff to avoid overwriting unapplied agent edits.
    if (diffPreviewRef.current) {
      return;
    }

    const chapterIdToSave = editorChapterIdRef.current;
    if (!chapterIdToSave || chapterIdToSave !== currentChapterId) {
      console.warn('[WorkDetailView] Save skipped: chapter id mismatch');
      return;
    }

    const saveTask = (async () => {
      try {
        // doc: file - write directly.
        if (isDocId(currentChapterId)) {
          const path = docIdToPath(currentChapterId);
          await docsFs.write(workId, path, content);
          console.log('[WorkDetailView] Saved document:', path);
          return;
        }

        const num = chapterIdToNum(currentChapterId);
        if (num === null) return;

        // Optimistic local update.
        setChapters((prev) =>
          prev.map((c) =>
            c.id === currentChapterId
              ? { ...c, content, updatedAt: new Date().toISOString() }
              : c
          )
        );

        // Persist to FS API.
        const saved = await chaptersFs.update(workId, num, { content });
        // Apply server-reported word count.
        setChapters((prev) =>
          prev.map((c) =>
            c.id === currentChapterId
              ? { ...c, wordCount: saved.wordCount }
              : c
          )
        );

        console.log('[WorkDetailView] Saved chapter:', {
          chapterId: currentChapterId,
          num,
          contentPreview: content.substring(0, 50) + '...',
        });
      } catch (error) {
        showToast('error', t('workDetail.toast.saveFailed'));
        console.error('Failed to save chapter:', error);
      }
    })();

    pendingEditorSaveRef.current = saveTask;
    try {
      await saveTask;
    } finally {
      if (pendingEditorSaveRef.current === saveTask) {
        pendingEditorSaveRef.current = null;
      }
    }
  }, [currentChapterId, workId, showToast]);

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
    if (target.closest('[data-scroll-scope="command-menu"]')) {
      return;
    }
    if (target.closest('[data-scroll-scope="chapter-list"]')) {
      return;
    }
    if (target.closest('[data-scroll-scope="editor-tabs"]')) {
      return;
    }
    if (target.closest('input, textarea, select, [contenteditable="true"], .ProseMirror, .diff-viewer')) {
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
      if (work_id !== workId) return;
      if (!workId) return;
      await refreshChaptersAndContent();
    };

    const refreshChaptersAndContent = async () => {
      if (!workId) return;
      try {
        const fsList = await chaptersFs.list(workId);
        const freshChapters = fsList.map(fs => fsToChapter(fs, workId));
        setChapters(freshChapters);

        // 刷新文件树
        try {
          const tree = await docsFs.tree(workId);
          setFileTree(tree);
        } catch { /* ignore */ }

        const activeChapterId = editorChapterIdRef.current || currentChapterId;
        if (activeChapterId) {
          if (isDocId(activeChapterId)) {
            // doc: 文件（知识库/世界观文件）刷新
            try {
              const path = docIdToPath(activeChapterId);
              const file = await docsFs.read(workId, path);
              setCurrentChapterContent(file.content);
            } catch { /* 文件可能已被删除 */ }
            // 刷新右侧世界观卡片数据
            try {
              await refreshWorldData();
            } catch { /* ignore */ }
          } else {
            // fs: 章节文件刷新
            try {
              const num = chapterIdToNum(activeChapterId);
              if (num === null) return;
              const full = await chaptersFs.get(workId, num);
              setCurrentChapterContent(full.content || '');
            } catch {
              // 章节可能已被删除
            }
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
        chapterTitle?: string;
        revisionType?: string;
        originalContent?: string;
        modifiedContent?: string;
        oldString?: string;
        newString?: string;
        diffPairs?: Array<{ oldString?: string; newString?: string }>;
        path?: string;
      }>;
      const {
        workId: targetWorkId,
        chapterId: targetChapterId,
        chapterTitle: targetChapterTitle,
        revisionType,
        originalContent,
        modifiedContent,
        oldString,
        newString,
        diffPairs,
        path: revisionPath,
      } = customEvent.detail || {};
      if (targetWorkId && targetWorkId !== workId) return;
      const normalizeTargetFileId = (value?: string): string | undefined => {
        if (typeof value !== 'string') return undefined;
        const trimmed = value.trim();
        if (!trimmed) return undefined;
        if (trimmed.startsWith('doc:')) {
          const normalizedPath = trimmed.slice(4).replace(/\\/g, '/').replace(/^\/+/, '');
          return `doc:${normalizedPath}`;
        }
        if (trimmed.startsWith('fs-')) {
          const num = parseInt(trimmed.slice(3), 10);
          return Number.isNaN(num) ? trimmed : `fs-${num}`;
        }
        return trimmed;
      };
      const normalizedRevisionPath = typeof revisionPath === 'string'
        ? revisionPath.replace(/\\/g, '/').replace(/^\/+/, '')
        : '';
      const inferredTargetChapterId = (() => {
        if (!normalizedRevisionPath) return undefined;
        const chapterMatch = normalizedRevisionPath.match(/^chapters\/(\d+)-[^/]+\.md$/i);
        if (chapterMatch) return `fs-${parseInt(chapterMatch[1], 10)}`;
        return `doc:${normalizedRevisionPath}`;
      })();
      const resolvedTargetChapterId = normalizeTargetFileId(targetChapterId) || inferredTargetChapterId;
      const normalizedCurrentChapterId = normalizeTargetFileId(currentChapterId) || currentChapterId;
      const previewBaseContent = (
        typeof oldString === 'string' && oldString.length > 0 ? oldString : undefined
      ) ?? (typeof originalContent === 'string' ? originalContent : '');
      const normalizedDiffPairs = Array.isArray(diffPairs)
        ? diffPairs
            .filter((pair) => typeof pair?.newString === 'string' && pair.newString.length > 0)
            .map((pair) => ({
              oldString: typeof pair.oldString === 'string' ? pair.oldString : '',
              newString: pair.newString as string,
            }))
        : [];
      const anchoredDiffPairs = normalizedDiffPairs.filter((pair) => pair.oldString.length > 0);

      // 标记进入 diff 预览模式，跳过自动保存
      diffPreviewRef.current = true;

      const hasDirectNewString = typeof newString === 'string' && newString.length > 0;
      const hasDirectOldString = typeof oldString === 'string' && oldString.length > 0;
      const canUseDirectDiff = hasDirectNewString && (hasDirectOldString || revisionType === 'create');

      const hasFallbackModified = typeof modifiedContent === 'string' && modifiedContent.length > 0;
      const hasFallbackOriginal =
        typeof originalContent === 'string' && (originalContent.length > 0 || revisionType === 'create');
      const canUseFallbackDiff = hasFallbackModified && hasFallbackOriginal;

      const dispatchBestEffortDiff = (baseText: string): boolean => {
        if (anchoredDiffPairs.length > 0) {
          // 顺序回放：后续 oldString 可能只在前一个 diff 应用后才出现
          const replayablePairs: Array<{ oldString: string; newString: string }> = [];
          let simulatedText = baseText;
          for (const pair of anchoredDiffPairs) {
            if (!pair.oldString || !simulatedText.includes(pair.oldString)) continue;
            replayablePairs.push(pair);
            simulatedText = simulatedText.replace(pair.oldString, pair.newString);
          }

          if (replayablePairs.length > 0) {
            replayablePairs.forEach((pair, index) => {
              window.dispatchEvent(new CustomEvent('editor-inline-diff', {
                detail: {
                  oldString: pair.oldString,
                  newString: pair.newString,
                  append: index > 0,
                }
              }));
            });
            return true;
          }
        }

        if (canUseDirectDiff) {
          const directOld = oldString ?? '';
          const canDispatchDirect = !hasDirectOldString || (baseText.length > 0 && baseText.includes(directOld));
          if (canDispatchDirect) {
            window.dispatchEvent(new CustomEvent('editor-inline-diff', {
              detail: { oldString: directOld, newString: newString as string }
            }));
            return true;
          }
        }

        if (canUseFallbackDiff) {
          const fallbackOld = originalContent ?? '';
          const hasFallbackOld = fallbackOld.length > 0;
          const canDispatchFallback = !hasFallbackOld || (baseText.length > 0 && baseText.includes(fallbackOld));
          if (canDispatchFallback) {
            window.dispatchEvent(new CustomEvent('editor-inline-diff', {
              detail: { oldString: fallbackOld, newString: modifiedContent as string }
            }));
            return true;
          }
        }

        return false;
      };

      // doc: 文件 — 打开文档并显示 diff
      if (resolvedTargetChapterId?.startsWith('doc:')) {
        if (isEditorCollapsed) setIsEditorCollapsed(false);
        const normalizeDocPath = (value: string) => value.replace(/\\/g, '/').replace(/^\/+/, '');
        const pathFromDocId = normalizeDocPath(docIdToPath(resolvedTargetChapterId));
        const pathFromRevision = normalizedRevisionPath && !normalizedRevisionPath.startsWith('chapters/')
          ? normalizeDocPath(normalizedRevisionPath)
          : '';
        const docPathCandidates = Array.from(
          new Set([pathFromDocId, pathFromRevision].filter((value): value is string => Boolean(value)))
        );
        if (docPathCandidates.length === 0) {
          setCurrentChapterContent(previewBaseContent);
          return;
        }

        const openDocTab = (docPath: string) => {
          const docId = `doc:${docPath}`;
          const fileName = docPath.split('/').pop() || docPath;
          openEditorTab({ id: docId, title: fileName, order: 0 });
          setCurrentChapterId(docId);
          return docId;
        };

        let activeDocPath = docPathCandidates[0];
        openDocTab(activeDocPath);

        const dispatchDiff = (baseText: string) => {
          if (!modifiedContent && anchoredDiffPairs.length === 0 && !canUseDirectDiff) return;
          // doc: 文件需要更长延迟：React 状态更新 + EditorWrapper key 重挂载 + Milkdown 初始化
          setTimeout(() => {
            dispatchBestEffortDiff(baseText);
            // 注意：定位失败时不截断编辑器内容，避免只显示一小块
          }, 600);
        };

        const applyPreview = (baseText: string) => {
          setCurrentChapterContent(baseText);
          dispatchDiff(baseText);
        };

        if (!workId) {
          applyPreview(previewBaseContent);
          return;
        }

        setCurrentChapterContent(''); // 先清空，避免新编辑器用旧内容初始化
        void (async () => {
          for (const candidatePath of docPathCandidates) {
            try {
              const file = await docsFs.read(workId, candidatePath);
              if (candidatePath !== activeDocPath) {
                activeDocPath = candidatePath;
                openDocTab(activeDocPath);
              }
              applyPreview(file.content || '');
              return;
            } catch {
              // try next candidate
            }
          }
          console.warn('[handleJumpRevision] docsFs.read failed for all candidates:', docPathCandidates);
          setCurrentChapterContent(previewBaseContent);
          dispatchDiff(previewBaseContent);
        })();
        return;
      }

      if (isEditorCollapsed) {
        setIsEditorCollapsed(false);
      }

      // 切换章节（如果不同）
      let needDelay = false;
      if (resolvedTargetChapterId && resolvedTargetChapterId !== normalizedCurrentChapterId) {
        const chapterExists = chapters.find((c) => c.id === resolvedTargetChapterId);
        if (chapterExists) {
          // 章节在磁盘上 → 正常切换
          handleChapterSelect(resolvedTargetChapterId);
          needDelay = true;
        } else {
          // 章节不在磁盘上（缓冲区新建）→ 添加虚拟章节 + 创建标签页
          const num = chapterIdToNum(resolvedTargetChapterId);
          const title = targetChapterTitle || `第${num ?? '?'}章`;
          // 添加到 chapters 列表（防止 useEditorTabs 清理标签）
          setChapters(prev => {
            if (prev.find(c => c.id === resolvedTargetChapterId)) return prev;
            const now = new Date().toISOString();
            return [...prev, {
              id: resolvedTargetChapterId,
              workId: workId || '',
              title,
              content: '',
              order: num ?? prev.length + 1,
              wordCount: 0,
              viewCount: 0,
              isPublished: false,
              publishedAt: null,
              createdAt: now,
              updatedAt: now,
              status: 'draft',
              _pending: true,
              _diffOriginal: previewBaseContent,
              _diffModified: modifiedContent || '',
            } as any];
          });
          openEditorTab({ id: resolvedTargetChapterId, title, order: num ?? 0 });
          setCurrentChapterContent(previewBaseContent);
          setCurrentChapterId(resolvedTargetChapterId);
        }
      }

      // 打开 diff 视图（如果有修改内容）
      // 优先使用磁盘内容做匹配，只回放能命中的 diff，避免 oldString 找不到
      if (anchoredDiffPairs.length > 0 || canUseDirectDiff || canUseFallbackDiff) {
        const shouldReloadFromDisk = typeof resolvedTargetChapterId === 'string' && resolvedTargetChapterId.startsWith('fs-');
        const baseDelay = needDelay ? 500 : (resolvedTargetChapterId !== normalizedCurrentChapterId ? 100 : 0);
        setTimeout(() => {
          const runDispatch = async () => {
            let baseText = previewBaseContent;
            if (shouldReloadFromDisk && workId) {
              const chapterNum = chapterIdToNum(resolvedTargetChapterId || '');
              if (chapterNum !== null) {
                try {
                  const full = await chaptersFs.get(workId, chapterNum);
                  baseText = full.content || '';
                  setCurrentChapterContent(baseText);
                } catch {
                  // ignore and fallback to previewBaseContent
                }
              }
            }
            const matched = dispatchBestEffortDiff(baseText);
            if (!matched) {
              // 定位失败时静默放弃，不截断编辑器内容
            }
          };
          void runDispatch();
        }, baseDelay);
      }

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
  }, [workId, currentChapterId, handleChapterSelect, isEditorCollapsed, chapters, openEditorTab]);

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
              {/* 文件树 */}
              <FileTreePanel
                workId={workId || ''}
                fileTree={fileTree}
                activeFileId={currentChapterId || null}
                onFileSelect={handleFileSelect}
                onChapterCreate={handleInlineChapterCreate}
                onTreeChange={setFileTree}
              />
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
            {/* SessionTabBar - 功能按钮栏 */}
            <SessionTabBar
              activeTabId={activeTabId}
              isReady={isTabReady}
              onCreateTab={createTab}
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

        {/* 右侧编辑器窗口 */}
        <div
          className="flex flex-col bg-white dark:bg-slate-900 transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)]"
          style={{
            flex: isEditorCollapsed ? '0 0 0' : '1 1 0%',
            opacity: isEditorCollapsed ? 0 : 1,
            overflow: 'hidden',
          }}
        >
          <div className="flex-1 flex flex-col border-l border-zinc-200 dark:border-slate-700 bg-white dark:bg-slate-900 overflow-hidden">
            {rightSidebarType === 'worldview' ? (
              <WorldviewPanel
                workId={workId!}
                worldData={worldData}
                initialTab={worldviewInitialTab}
                targetItemId={worldviewTargetItemId}
                onTargetItemScrolled={() => setWorldviewTargetItemId(undefined)}
                onWorldDataUpdate={handleWorldviewPanelDataUpdate}
                onBeforeSyncKnowledgeToWorldview={waitForPendingEditorSave}
              />
            ) : (
              <EditorWrapper
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
                isLeftPanelCollapsed={isLeftCollapsed}
                onExpandLeftPanel={() => setIsLeftCollapsed(false)}
                onCollapseLeftPanel={() => setIsLeftCollapsed(true)}
                isRightPanelCollapsed={isEditorCollapsed}
                onExpandRightPanel={() => setIsEditorCollapsed(false)}
                onCollapseRightPanel={() => setIsEditorCollapsed(true)}
                tabs={editorTabs}
                activeTabId={activeEditorTabId}
                onTabSwitch={handleEditorTabSwitch}
                onTabClose={handleEditorTabClose}
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
