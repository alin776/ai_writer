import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Edit, Trash2, Plus, BookOpen, BarChart3, BookMarked, Download, MessageSquare } from 'lucide-react';
import { Button, Card, Loading } from '../../components/common';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import ExportDialog from '../../components/export/ExportDialog';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import type { Work, Chapter, CreateChapterData } from '../../types';
import type { Chapter as NovelChapter, WorldData, Character, Location, Setting, WorkGuidelines } from '../../types/novel';
import { formatDate } from '../../utils/formatDate';
import NovelEditor from '../../components/editor/NovelEditor';
import ChapterTree from '../../components/editor/ChapterTree';
import WorldviewSidebar from '../../components/editor/WorldviewSidebar';
import NovelAnalysisPanel from '../../components/editor/NovelAnalysisPanel';
import AgentChatPanel from '../../components/agent/AgentChatPanel';
import { useConfirm } from '../../hooks/useConfirm';
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
  const { confirmState, confirm, closeConfirm } = useConfirm();

  const [work, setWork] = useState<Work | null>(null);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 编辑器相关状态
  const [currentChapterId, setCurrentChapterId] = useState<string | undefined>(undefined);
  const [currentChapterContent, setCurrentChapterContent] = useState<string>('');

  // 世界观数据
  const [worldData, setWorldData] = useState<WorldData>({
    characters: [],
    locations: [],
    settings: [],
    guidelines: undefined,
    aiGuidelines: undefined,
  });

  // 右侧面板状态：'world' | 'analysis' | 'agent'
  const [rightPanel, setRightPanel] = useState<'world' | 'analysis' | 'agent'>('world');
  
  // 导出对话框状态
  const [showExportDialog, setShowExportDialog] = useState(false);

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
    if (!workId) return;

    const title = prompt('请输入章节标题：');
    if (!title || !title.trim()) {
      showToast('warning', '章节标题不能为空');
      return;
    }

    try {
      // 只发送后端需要的字段
      const chapterData = {
        work_id: workId,
        title: title.trim(),
        content: '',
        order: chapters.length + 1,
      };

      // 调用后端接口，后端会生成 ID
      const savedChapter = await DataService.createChapter(chapterData);

      // 使用后端返回的完整章节对象
      setChapters((prev) => [...prev, savedChapter]);

      // 选中新章节
      setCurrentChapterId(savedChapter.id);
      setCurrentChapterContent(savedChapter.content);

      showToast('success', '章节添加成功');
    } catch (error) {
      showToast('error', '章节添加失败');
      console.error('Failed to add chapter:', error);
    }
  }, [workId, chapters.length, showToast]);

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
        await DataService.updateChapter(chapterData.id, updatedChapter);

        showToast('success', '章节更新成功');
      }
    } catch (error) {
      showToast('error', isNew ? '章节添加失败' : '章节更新失败');
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
        } else {
          setCurrentChapterId(undefined);
          setCurrentChapterContent('');
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
      <div style={{ display: 'flex', width: '100%', height: '100vh', overflow: 'hidden' }}>
        {/* 左侧章节树 */}
        <div style={{ width: '280px', height: '100%', flexShrink: 0, display: 'flex', flexDirection: 'column' }}>
          {/* 顶部导出按钮 */}
          <div style={{ padding: '12px', borderBottom: '1px solid #333' }}>
            <button
              onClick={() => setShowExportDialog(true)}
              style={{
                width: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px',
                padding: '8px 12px',
                background: '#2563eb',
                color: '#fff',
                border: 'none',
                borderRadius: '6px',
                fontSize: '14px',
                fontWeight: 500,
                cursor: 'pointer',
                transition: 'all 0.2s',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = '#1d4ed8')}
              onMouseLeave={(e) => (e.currentTarget.style.background = '#2563eb')}
            >
              <Download size={16} />
              <span>导出作品</span>
            </button>
          </div>
          
          {/* 章节树 */}
          <div style={{ flex: 1, overflow: 'hidden' }}>
            <ChapterTree
              chapters={novelChapters}
              currentChapterId={currentChapterId}
              onChapterSelect={handleChapterSelect}
              onChapterSave={handleSaveChapter}
              onChapterDelete={handleDeleteChapter}
              onChapterMove={handleChapterMove}
            />
          </div>
        </div>

      {/* 中间编辑器区域 */}
      <div style={{ flex: 1, height: '100%', overflow: 'hidden' }}>
        <NovelEditor
          key={currentChapterId} // 关键：章节切换时重新创建编辑器实例
          content={currentChapterContent}
          onSave={handleEditorSave}
          placeholder="开始写作..."
          autoSave={true}
          autoSaveInterval={3000}
        />
      </div>

      {/* 右侧面板 */}
      <div style={{ width: '320px', height: '100%', flexShrink: 0, display: 'flex', flexDirection: 'column' }}>
        {/* 面板切换按钮 */}
        <div style={{ display: 'flex', borderBottom: '1px solid #333', background: '#1e1e1e' }}>
          <button
            onClick={() => setRightPanel('world')}
            style={{
              flex: 1,
              padding: '12px',
              background: rightPanel === 'world' ? '#252525' : 'transparent',
              color: rightPanel === 'world' ? '#fff' : '#9ca3af',
              border: 'none',
              borderBottom: rightPanel === 'world' ? '2px solid #3b82f6' : 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              fontSize: '14px',
              fontWeight: 500,
              transition: 'all 0.2s',
            }}
          >
            <BookMarked size={16} />
            <span>世界观</span>
          </button>
          <button
            onClick={() => setRightPanel('analysis')}
            style={{
              flex: 1,
              padding: '12px',
              background: rightPanel === 'analysis' ? '#252525' : 'transparent',
              color: rightPanel === 'analysis' ? '#fff' : '#9ca3af',
              border: 'none',
              borderBottom: rightPanel === 'analysis' ? '2px solid #3b82f6' : 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              fontSize: '14px',
              fontWeight: 500,
              transition: 'all 0.2s',
            }}
          >
            <BarChart3 size={16} />
            <span>概括</span>
          </button>
          <button
            onClick={() => setRightPanel('agent')}
            style={{
              flex: 1,
              padding: '12px',
              background: rightPanel === 'agent' ? '#252525' : 'transparent',
              color: rightPanel === 'agent' ? '#fff' : '#9ca3af',
              border: 'none',
              borderBottom: rightPanel === 'agent' ? '2px solid #3b82f6' : 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              fontSize: '14px',
              fontWeight: 500,
              transition: 'all 0.2s',
            }}
          >
            <MessageSquare size={16} />
            <span>Agent</span>
          </button>
        </div>

        {/* 面板内容 */}
        <div style={{ flex: 1, overflow: 'hidden' }}>
          {rightPanel === 'world' ? (
            <WorldviewSidebar
              workId={workId!}
              worldData={worldData}
            />
          ) : rightPanel === 'analysis' ? (
            <NovelAnalysisPanel
              workId={workId!}
              currentChapterId={currentChapterId}
              onToast={showToast}
            />
          ) : (
            <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <AgentChatPanel
                workId={workId!}
                chapterId={currentChapterId}
                className="h-full"
              />
            </div>
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
    </>
  );
};

export default WorkDetailView;
