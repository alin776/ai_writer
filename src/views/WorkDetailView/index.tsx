import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
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
import { SummaryPanel } from '../../components/editor/SummaryPanel';
import { AIPanel } from '../../components/editor/AIPanel';
import SessionTabBar from '../../components/editor/SessionTabBar';
import { useEditorStore } from '../../store/editorStore';
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
  const { showToast } = useGlobalStore();
  const { user, setUser } = useAuthStore();
  const { confirmState, confirm, closeConfirm } = useConfirm();
  const { rightSidebarType, setRightSidebarType } = useEditorStore();

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
      showToast('success', newValue ? 'AI 自动补全已开启' : 'AI 自动补全已关闭');
    } catch (error) {
      setUser({ ...user, preferences: currentPreferences });
      showToast('error', '更新设置失败');
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
        title: session.title || '历史会话',
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
      attachSessionTab(sessionId, session.title || '历史会话', conversationId);
      setShowHistoryPanel(false);
      showToast('info', '已切换到历史会话，可继续对话');
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

  // 折叠状态
  const [isLeftCollapsed, setIsLeftCollapsed] = useState(false);
  const [isRightCollapsed, setIsRightCollapsed] = useState(false);

  // 右侧面板宽度
  const [rightPanelWidth, setRightPanelWidth] = useState(() => {
    const saved = localStorage.getItem('rightPanelWidth');
    return saved ? parseInt(saved, 10) : 288; // 默认 288px (w-72)
  });
  const [isResizing, setIsResizing] = useState(false);

  // 添加章节输入框状态
  const [isAddingChapter, setIsAddingChapter] = useState(false);
  const [newChapterTitle, setNewChapterTitle] = useState('');

  // 删除章节确认对话框状态
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [chapterToDelete, setChapterToDelete] = useState<string | null>(null);

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
        setError('作品 ID 不存在');
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        setError(null);
        const [workData, chaptersData, worldDataFromServer] = await Promise.all([
          DataService.getWork(workId),
          DataService.getChapters(workId),
          DataService.getWorldData(workId),
        ]);
        setWork(workData);
        setChapters(chaptersData);
        setWorldData(worldDataFromServer as any);

        // 如果有章节，默认选中第一个
        if (chaptersData.length > 0) {
          setCurrentChapterId(chaptersData[0].id);
          setCurrentChapterContent(chaptersData[0].content);
          editorChapterIdRef.current = chaptersData[0].id; // 更新 ref
        }

        // 🔥 首次打开作品时，自动检查并触发分析
        // 使用 localStorage 记录已触发过的作品，避免重复触发
        const AUTO_ANALYSIS_KEY = `auto-analysis-triggered-${workId}`;
        const hasTriggered = localStorage.getItem(AUTO_ANALYSIS_KEY);

        if (!hasTriggered && chaptersData.length > 0) {
          try {
            // 检查是否已有分析结果
            const analysisStatus = await DataService.getAnalysisStatus(workId);

            // 如果没有分析结果或分析失败，则触发分析
            if (!analysisStatus || analysisStatus.status === 'failed') {
              console.log('[WorkDetailView] 首次打开作品，触发自动分析');
              await DataService.startNovelAnalysis(workId);
              showToast('info', '已自动开始分析小说内容');

              // 记录已触发，避免重复
              localStorage.setItem(AUTO_ANALYSIS_KEY, 'true');
            } else {
              console.log('[WorkDetailView] 作品已有分析结果，跳过自动分析');
            }
          } catch (analysisError) {
            // 分析失败不影响主流程，静默处理
            console.warn('[WorkDetailView] 自动分析检查失败:', analysisError);
          }
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : '加载数据失败';
        setError(message);
        showToast('error', message);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [workId, showToast]);

  /**
   * 处理章节选择
   */
  const handleChapterSelect = useCallback((chapterId: string) => {
    const chapter = chapters.find((c) => c.id === chapterId);
    if (chapter) {
      // 先更新章节ID，再更新内容，确保编辑器使用正确的章节数据
      setCurrentChapterId(chapterId);
      setCurrentChapterContent(chapter.content);
      editorChapterIdRef.current = chapterId; // 更新 ref

      // 调试日志
      console.log('[WorkDetailView] 切换章节:', {
        chapterId,
        title: chapter.title,
        contentLength: chapter.content?.length || 0,
      });
    }
  }, [chapters]);

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
      showToast('warning', '章节标题不能为空');
      return;
    }

    try {
      // 只发送后端需要的字段
      const chapterData = {
        work_id: workId,
        title: newChapterTitle.trim(),
        content: '',
        order: chapters.length + 1,
      };

      // 调用后端接口，后端会生成 ID
      const savedChapter = await DataService.createChapter(chapterData);

      // 使用后端返回的完整章节对象
      setChapters((prev) => [...prev, savedChapter]);

      // 先清空当前内容，再选中新章节（确保编辑器内容被清空）
      setCurrentChapterContent('');
      // 使用 setTimeout 确保状态更新顺序正确
      setTimeout(() => {
        setCurrentChapterId(savedChapter.id);
        setCurrentChapterContent('');
        editorChapterIdRef.current = savedChapter.id; // 更新 ref
      }, 0);

      // 清空输入框并关闭
      setNewChapterTitle('');
      setIsAddingChapter(false);

      showToast('success', '章节添加成功');

      // 🔥 新增章节后，自动触发重新分析（后台执行，不阻塞用户）
      try {
        console.log('[WorkDetailView] 新增章节，触发自动分析');
        await DataService.startNovelAnalysis(workId);
        showToast('info', '已触发小说分析更新');
      } catch (analysisError) {
        // 分析失败不影响主流程，静默处理
        console.warn('[WorkDetailView] 自动分析触发失败:', analysisError);
      }
    } catch (error) {
      showToast('error', '章节添加失败');
      console.error('Failed to add chapter:', error);
    }
  }, [workId, chapters.length, newChapterTitle, showToast]);

  /**
   * 取消添加章节
   */
  const handleCancelAddChapter = useCallback(() => {
    setNewChapterTitle('');
    setIsAddingChapter(false);
  }, []);

  /**
   * 处理保存章节（新增或编辑）
   */
  const handleSaveChapter = useCallback(async (chapterData: Partial<Chapter> & { id?: string }) => {
    if (!workId) return;
    if (!chapterData.title?.trim()) {
      showToast('warning', '章节标题不能为空');
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
        };

        const savedChapter = await DataService.createChapter(newChapterData);

        // 更新章节列表
        setChapters((prev) => [...prev, savedChapter]);

        // 选中新章节
        setCurrentChapterId(savedChapter.id);
        setCurrentChapterContent(savedChapter.content);

        showToast('success', '章节添加成功');
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

        showToast('success', '章节更新成功');
      }
    } catch (error) {
      const message =
        !chapterData.id || chapterData.id.startsWith('temp-')
          ? '章节添加失败'
          : '章节更新失败';
      showToast('error', message);
      console.error('Failed to save chapter:', error);
    }
  }, [workId, chapters, showToast]);

  /**
   * 处理删除章节
   */
  const handleDeleteChapter = useCallback(async (chapterId: string) => {
    const chapter = chapters.find((c) => c.id === chapterId);
    if (!chapter) return;

    const confirmed = await confirm({
      title: '删除章节',
      message: `确定要删除章节"${chapter.title}"吗？此操作不可恢复。`,
      confirmText: '删除',
      cancelText: '取消',
      variant: 'danger',
    });

    if (!confirmed) {
      return;
    }

    try {
      // 从状态中删除
      setChapters((prev) => prev.filter((c) => c.id !== chapterId));

      // 如果删除的是当前章节，切换到第一个章节
      if (currentChapterId === chapterId) {
        const remainingChapters = chapters.filter((c) => c.id !== chapterId);
        if (remainingChapters.length > 0) {
          setCurrentChapterId(remainingChapters[0].id);
          setCurrentChapterContent(remainingChapters[0].content);
          editorChapterIdRef.current = remainingChapters[0].id; // 更新 ref
        } else {
          setCurrentChapterId(undefined);
          setCurrentChapterContent('');
          editorChapterIdRef.current = undefined; // 更新 ref
        }
      }

      // 从后端删除
      await DataService.deleteChapter(chapterId);

      showToast('success', '章节删除成功');
    } catch (error) {
      showToast('error', '章节删除失败');
      console.error('Failed to delete chapter:', error);
    }
  }, [chapters, currentChapterId, showToast]);

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

      showToast('success', '章节顺序更新成功');
    } catch (error) {
      showToast('error', '章节顺序更新失败');
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

    try {
      // 调试日志
      console.log('[WorkDetailView] 保存章节:', {
        chapterId: currentChapterId,
        contentPreview: content.substring(0, 50) + '...',
      });

      // 更新章节内容
      setChapters((prevChapters) => {
        const chapter = prevChapters.find((c) => c.id === currentChapterId);
        if (!chapter) {
          console.warn('[WorkDetailView] 保存失败：章节不存在', currentChapterId);
          return prevChapters;
        }

        // 只发送content，让后端自动计算字数
        const updateData = {
          content,
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
      showToast('error', '保存失败');
      console.error('Failed to save chapter:', error);
    }
  }, [currentChapterId, showToast]);

  /**
   * 处理编辑作品
   */
  const handleEditWork = useCallback(() => {
    showToast('info', '编辑作品功能待实现');
  }, [showToast]);

  /**
   * 处理删除作品
   */
  const handleDeleteWork = useCallback(() => {
    showToast('info', '删除作品功能待实现');
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

        showToast('success', '人物添加成功');
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

        showToast('success', '人物更新成功');
      }
    } catch (error) {
      const isNew = character.id?.startsWith('temp-');
      showToast('error', isNew ? '人物添加失败' : '人物更新失败');
      console.error('Failed to save character:', error);
    }
  }, [workId, showToast]);

  const handleCharacterDelete = useCallback(async (id: string) => {
    const character = worldData.characters.find((c) => c.id === id);
    if (!character) return;

    const confirmed = await confirm({
      title: '删除人物',
      message: `确定要删除人物"${character.name}"吗？删除后相关数据将无法恢复。`,
      confirmText: '删除',
      cancelText: '取消',
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
      showToast('success', '人物删除成功');
    } catch (error) {
      showToast('error', '人物删除失败');
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

        showToast('success', '地点添加成功');
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

        showToast('success', '地点更新成功');
      }
    } catch (error) {
      const isNew = location.id?.startsWith('temp-');
      showToast('error', isNew ? '地点添加失败' : '地点更新失败');
      console.error('Failed to save location:', error);
    }
  }, [workId, showToast]);

  const handleLocationDelete = useCallback(async (id: string) => {
    const location = worldData.locations.find((l) => l.id === id);
    if (!location) return;

    const confirmed = await confirm({
      title: '删除地点',
      message: `确定要删除地点"${location.name}"吗？删除后相关数据将无法恢复。`,
      confirmText: '删除',
      cancelText: '取消',
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
      showToast('success', '地点删除成功');
    } catch (error) {
      showToast('error', '地点删除失败');
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

        showToast('success', '设定添加成功');
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

        showToast('success', '设定更新成功');
      }
    } catch (error) {
      const isNew = setting.id?.startsWith('temp-');
      showToast('error', isNew ? '设定添加失败' : '设定更新失败');
      console.error('Failed to save setting:', error);
    }
  }, [workId, showToast]);

  const handleSettingDelete = useCallback(async (id: string) => {
    const setting = worldData.settings.find((s) => s.id === id);
    if (!setting) return;

    const confirmed = await confirm({
      title: '删除设定',
      message: `确定要删除设定"${setting.title}"吗？删除后相关数据将无法恢复。`,
      confirmText: '删除',
      cancelText: '取消',
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
      showToast('success', '设定删除成功');
    } catch (error) {
      showToast('error', '设定删除失败');
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

      showToast('success', '作品规范保存成功');
      console.log('[WorkDetailView] 作品规范已保存:', guidelines);
    } catch (error) {
      showToast('error', '作品规范保存失败');
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
      showToast('success', 'AI创作规范保存成功');
    } catch (error) {
      showToast('error', 'AI创作规范保存失败');
      console.error('Failed to save AI guidelines:', error);
    }
  }, [workId, showToast]);

  /**
   * 拖动调整右侧面板宽度
   */
  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
  }, []);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing) return;

      // 计算新宽度（从右边缘往左计算）
      const newWidth = window.innerWidth - e.clientX;

      // 限制最小和最大宽度
      const minWidth = 240; // 最小 240px
      const maxWidth = 600; // 最大 600px
      const clampedWidth = Math.max(minWidth, Math.min(maxWidth, newWidth));

      setRightPanelWidth(clampedWidth);
    };

    const handleMouseUp = () => {
      if (isResizing) {
        setIsResizing(false);
        // 保存到 localStorage
        localStorage.setItem('rightPanelWidth', rightPanelWidth.toString());
      }
    };

    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      // 防止文本选中
      document.body.style.userSelect = 'none';
      document.body.style.cursor = 'col-resize';
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.userSelect = '';
      document.body.style.cursor = '';
    };
  }, [isResizing, rightPanelWidth]);

  if (isLoading) {
    return <Loading />;
  }

  if (error || !work) {
    return (
      <div className={styles.errorContainer}>
        <div className={styles.errorContent}>
          <p className={styles.errorText}>{error || '作品不存在'}</p>
          <Button onClick={() => navigate('/works')}>返回作品列表</Button>
        </div>
      </div>
    );
  }

  // 转换章节数据为 NovelChapter 格式
  const novelChapters = convertToNovelChapters(chapters);

  return (
    <>
      <div className="flex bg-zinc-50/30" style={{ height: 'calc(100vh - 60px)' }}>
        {/* 左侧章节面板 */}
        <div
          className={`bg-gradient-to-b from-white to-zinc-50/30 flex flex-col border-r border-zinc-100/80 transition-all duration-300 h-full overflow-hidden ${
            isLeftCollapsed ? 'w-12' : 'w-60'
          }`}
        >
          {isLeftCollapsed ? (
            /* 折叠状态 */
            <div className="flex flex-col items-center py-5 gap-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsLeftCollapsed(false)}
                className="h-10 w-10 p-0 text-zinc-400 hover:text-zinc-900 hover:bg-white hover:shadow-sm rounded-lg transition-all"
              >
                <ChevronRight className="h-6 w-6" />
              </Button>
              <div className="writing-mode-vertical text-[11px] text-zinc-400 tracking-widest" style={{ writingMode: 'vertical-rl' }}>
                目录
              </div>
            </div>
          ) : (
            /* 展开状态 */
            <div className="px-4 py-3 flex-1 flex flex-col min-h-0">
              {/* 标题区域 */}
              <div className="mb-3 flex-shrink-0">
                <div className="flex items-center justify-between mb-1">
                  <h2 className="text-[15px] text-zinc-800 tracking-tight">目录</h2>
                  <div className="flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleAddChapter()}
                      className="h-9 w-9 p-0 text-zinc-400 hover:text-zinc-900 hover:bg-white hover:shadow-sm rounded-lg transition-all"
                    >
                      <Plus className="h-6 w-6" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setIsLeftCollapsed(true)}
                      className="h-9 w-9 p-0 text-zinc-400 hover:text-zinc-900 hover:bg-white hover:shadow-sm rounded-lg transition-all"
                    >
                      <ChevronLeft className="h-6 w-6" />
                    </Button>
                  </div>
                </div>
                <div className="h-px bg-gradient-to-r from-zinc-200 via-zinc-100 to-transparent" />
              </div>

              {/* 章节列表 */}
              <div className="flex-1 overflow-y-auto custom-scrollbar -mx-2 min-h-0">
                <div className="px-2 space-y-1">
                  {/* 新章节输入框 */}
                  {isAddingChapter && (
                    <div className="relative px-3 py-2.5 rounded-xl bg-white shadow-lg shadow-zinc-200/60 ring-1 ring-zinc-900/5 transition-all">
                      {/* 顶部装饰线 */}
                      <div className="absolute top-0 left-3 right-3 h-0.5 rounded-full bg-gradient-to-r from-zinc-400 via-zinc-600 to-zinc-400" />

                      <div className="flex items-start gap-3 pt-0.5">
                        {/* 章节编号占位 */}
                        <div className="flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-[11px] bg-zinc-100/80 text-zinc-400">
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
                            placeholder="章节标题"
                            className="h-7 w-full text-[13px] border-0 px-0 bg-transparent focus:ring-0 focus:outline-none focus-visible:ring-0 focus-visible:outline-none placeholder:text-zinc-400"
                            style={{ outline: 'none', boxShadow: 'none' }}
                          />

                          {/* 操作按钮 */}
                          <div className="flex items-center justify-between mt-2">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={handleCancelAddChapter}
                              className="h-6 px-2 text-[10px] bg-transparent hover:bg-zinc-100 text-zinc-500 hover:text-zinc-700 border-0 shadow-none"
                            >
                              取消
                            </Button>
                            <Button
                              size="sm"
                              onClick={handleSaveNewChapter}
                              className="h-6 px-2 text-[10px] bg-zinc-800 hover:bg-zinc-900 text-white border-0"
                            >
                              保存
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
                          ? 'bg-white shadow-lg shadow-zinc-200/60 ring-1 ring-zinc-900/5'
                          : 'text-zinc-700 hover:bg-white/60 hover:shadow-md hover:shadow-zinc-100'
                      }`}
                    >
                      {/* 顶部装饰线 */}
                      <div className={`absolute top-0 left-3 right-3 h-0.5 rounded-full transition-all duration-300 ${
                        chapter.id === currentChapterId
                          ? 'bg-gradient-to-r from-zinc-400 via-zinc-600 to-zinc-400'
                          : 'bg-transparent group-hover:bg-zinc-200'
                      }`} />

                      <div className="flex items-start gap-3 pt-0.5">
                        {/* 章节编号 */}
                        <div className={`flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-[11px] font-medium transition-all duration-300 ${
                          chapter.id === currentChapterId
                            ? 'bg-gradient-to-br from-zinc-700 to-zinc-900 text-white shadow-md shadow-zinc-900/20'
                            : 'bg-zinc-100/80 text-zinc-500 group-hover:bg-zinc-200 group-hover:text-zinc-700'
                        }`}>
                          {index + 1}
                        </div>

                        {/* 章节内容 */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-2">
                            <div className={`text-[13px] leading-snug truncate flex-1 transition-colors duration-300 ${
                              chapter.id === currentChapterId ? 'text-zinc-900' : 'text-zinc-700'
                            }`}>
                              {chapter.title.replace(/^第\d+章\s*/, '')}
                            </div>
                            <button
                              type="button"
                              onClick={(e) => {
                                e.stopPropagation();
                                setChapterToDelete(chapter.id);
                                setDeleteDialogOpen(true);
                              }}
                              className={`h-6 w-6 p-0 rounded flex items-center justify-center border-0 bg-transparent opacity-0 group-hover:opacity-100 flex-shrink-0 transition-all ${
                                chapter.id === currentChapterId
                                  ? 'text-zinc-400 hover:text-red-500 hover:bg-red-50/80'
                                  : 'text-zinc-400 hover:text-red-500 hover:bg-red-50'
                              }`}
                              aria-label="删除章节"
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

                          {/* 字数统计与进度 */}
                          <div className="flex items-center gap-2 mt-2">
                            <div className={`text-[10px] transition-colors duration-300 ${
                              chapter.id === currentChapterId ? 'text-zinc-500' : 'text-zinc-400'
                            }`}>
                              {chapter.wordCount.toLocaleString()} 字
                            </div>
                            {/* 进度指示器 */}
                            <div className={`flex-1 h-1 rounded-full transition-all duration-300 ${
                              chapter.id === currentChapterId ? 'bg-zinc-100' : 'bg-zinc-100/60'
                            }`}>
                              <div
                                className={`h-full rounded-full transition-all duration-500 ${
                                  chapter.id === currentChapterId
                                    ? 'bg-gradient-to-r from-zinc-500 via-zinc-600 to-zinc-700 shadow-sm'
                                    : 'bg-zinc-300 group-hover:bg-zinc-400'
                                }`}
                                style={{ width: `${Math.min((chapter.wordCount / 5000) * 100, 100)}%` }}
                              />
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* 底部微光效果 */}
                      {chapter.id === currentChapterId && (
                        <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-zinc-200/50 to-transparent" />
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* 中间编辑器区域 */}
        <div className="flex-1 flex flex-col bg-white overflow-hidden">
          <NovelEditor
            key={currentChapterId}
            content={currentChapterContent}
            onSave={handleEditorSave}
            placeholder="开始写作..."
            autoSave={true}
            autoSaveInterval={3000}
            workId={workId}
            chapterId={currentChapterId || undefined}
            aiAutoCompleteEnabled={aiAutoCompleteEnabled}
            onToggleAIAutoComplete={handleToggleAIAutoComplete}
          />
        </div>

        {/* 右侧面板 */}
        <div
          className={`relative bg-white border-l border-zinc-100 flex flex-col transition-all duration-300 ${
            isRightCollapsed ? 'w-12' : ''
          }`}
          style={!isRightCollapsed ? { width: `${rightPanelWidth}px` } : undefined}
        >
          {/* 可拖动的分隔条 */}
          {!isRightCollapsed && (
            <div
              onMouseDown={handleMouseDown}
              className="absolute left-0 top-0 bottom-0 w-1 cursor-col-resize hover:bg-blue-400 transition-colors z-10 group"
              style={{ marginLeft: '-2px' }}
            >
              <div className="absolute inset-y-0 -left-1 -right-1" />
            </div>
          )}
          {isRightCollapsed ? (
            /* 折叠状态 */
            <div className="flex flex-col items-center py-5 gap-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsRightCollapsed(false)}
                className="h-10 w-10 p-0 text-zinc-400 hover:text-zinc-900 hover:bg-zinc-50 hover:shadow-sm rounded-lg transition-all"
              >
                <ChevronLeft className="h-6 w-6" />
              </Button>
              <div className="writing-mode-vertical text-[11px] text-zinc-400 tracking-widest" style={{ writingMode: 'vertical-rl' }}>
                {rightSidebarType === 'worldview' ? '世界观' : rightSidebarType === 'summary' ? '概括' : 'AI'}
              </div>
            </div>
          ) : (
            <>
              {/* SessionTabBar */}
              <SessionTabBar
                tabs={tabs}
                activeTabId={activeTabId}
                onSwitchTab={switchTab}
                onCreateTab={createTab}
                onCloseTab={closeTab}
                onOpenHistory={handleOpenHistory}
              />

              {/* 内容区 */}
              <div className="flex-1 overflow-hidden">
                {rightSidebarType === 'worldview' ? (
                  <WorldviewPanel
                    workId={workId!}
                    worldData={worldData}
                  />
                ) : rightSidebarType === 'summary' ? (
                  <SummaryPanel
                    workId={workId!}
                    currentChapterId={currentChapterId}
                    onToast={showToast}
                  />
                ) : (
                  tabs.map((tab) => (
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
                      />
                    </div>
                  ))
                )}
              </div>
            </>
          )}
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
            <AlertDialogTitle className="text-[15px] text-zinc-900">删除章节</AlertDialogTitle>
            <AlertDialogDescription className="text-[13px] text-zinc-500 leading-relaxed">
              确定要删除这个章节吗？此操作无法撤销，章节内容将永久丢失。
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel className="text-[12px] h-8 bg-transparent hover:bg-zinc-100 text-zinc-600 hover:text-zinc-900 border-zinc-200">
              取消
            </AlertDialogCancel>
            <AlertDialogAction
              onClick={async () => {
                if (chapterToDelete) {
                  const chapter = chapters.find((c) => c.id === chapterToDelete);
                  if (!chapter) return;

                  try {
                    // 从状态中删除
                    setChapters((prev) => prev.filter((c) => c.id !== chapterToDelete));

                    // 如果删除的是当前章节，切换到第一个章节
                    if (currentChapterId === chapterToDelete) {
                      const remainingChapters = chapters.filter((c) => c.id !== chapterToDelete);
                      if (remainingChapters.length > 0) {
                        setCurrentChapterId(remainingChapters[0].id);
                        setCurrentChapterContent(remainingChapters[0].content);
                        editorChapterIdRef.current = remainingChapters[0].id; // 更新 ref
                      } else {
                        setCurrentChapterId(undefined);
                        setCurrentChapterContent('');
                        editorChapterIdRef.current = undefined; // 更新 ref
                      }
                    }

                    // 从后端删除
                    await DataService.deleteChapter(chapterToDelete);
                    showToast('success', '章节删除成功');
                  } catch (error) {
                    showToast('error', '章节删除失败');
                  } finally {
                    setChapterToDelete(null);
                  }
                }
              }}
              className="text-[12px] h-8 bg-red-500 hover:bg-red-600 text-white"
            >
              删除
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
};

export default WorkDetailView;
