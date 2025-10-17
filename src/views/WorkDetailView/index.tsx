import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Edit, Trash2, Plus, BookOpen } from 'lucide-react';
import { Button, Card, Loading } from '../../components/common';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import type { Work, Chapter } from '../../types';
import type { Chapter as NovelChapter, WorldData, Character, Location, Setting } from '../../types/novel';
import { formatDate } from '../../utils/formatDate';
import NovelEditor from '../../components/editor/NovelEditor';
import ChapterTree from '../../components/editor/ChapterTree';
import WorldManager from '../../components/editor/WorldManager';
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
  });

  /**
   * 转换 Chapter 到 NovelChapter 格式
   */
  const convertToNovelChapters = (chapters: Chapter[]): NovelChapter[] => {
    return chapters.map((chapter) => ({
      id: chapter.id,
      title: chapter.title,
      wordCount: chapter.word_count,
      status: chapter.is_published ? 'published' : 'draft',
      order: chapter.order,
      content: chapter.content,
      createdAt: new Date(chapter.created_at),
      updatedAt: new Date(chapter.updated_at),
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
          DataService.getWorldData(workId).catch(() => ({ characters: [], locations: [], settings: [] })),
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
      setCurrentChapterId(chapterId);
      setCurrentChapterContent(chapter.content);
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
   * 处理编辑章节
   */
  const handleEditChapter = useCallback(async (chapterId: string) => {
    const chapter = chapters.find((c) => c.id === chapterId);
    if (!chapter) return;

    const newTitle = prompt('请输入新的章节标题：', chapter.title);
    if (!newTitle || !newTitle.trim()) {
      showToast('warning', '章节标题不能为空');
      return;
    }

    if (newTitle === chapter.title) return;

    try {
      const updatedChapter = {
        ...chapter,
        title: newTitle.trim(),
        updated_at: new Date().toISOString(),
      };

      // 更新状态
      setChapters((prev) =>
        prev.map((c) => (c.id === chapterId ? updatedChapter : c))
      );

      // 保存到后端
      await DataService.updateChapter(chapterId, updatedChapter);

      showToast('success', '章节标题更新成功');
    } catch (error) {
      showToast('error', '章节标题更新失败');
      console.error('Failed to edit chapter:', error);
    }
  }, [chapters, showToast]);

  /**
   * 处理删除章节
   */
  const handleDeleteChapter = useCallback(async (chapterId: string) => {
    const chapter = chapters.find((c) => c.id === chapterId);
    if (!chapter) return;

    if (!confirm(`确定要删除章节"${chapter.title}"吗？此操作不可恢复。`)) {
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
    if (!currentChapterId) return;

    try {
      // 计算字数
      const text = content.replace(/<[^>]*>/g, ''); // 移除 HTML 标签
      const wordCount = text.length;

      // 更新章节内容
      setChapters((prevChapters) => {
        const chapter = prevChapters.find((c) => c.id === currentChapterId);
        if (!chapter) return prevChapters;

        const updatedChapter = {
          ...chapter,
          content,
          word_count: wordCount,
          updated_at: new Date().toISOString(),
        };

        // 异步保存到后端（不阻塞UI更新）
        DataService.updateChapter(currentChapterId, updatedChapter).catch((error) => {
          console.error('Failed to save chapter:', error);
        });

        return prevChapters.map((c) =>
          c.id === currentChapterId ? updatedChapter : c
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
        // 创建新人物
        const newCharacter = {
          ...character,
          id: 'character-' + Date.now(),
          workId,
          createdAt: new Date(),
          updatedAt: new Date(),
        };

        // 更新本地状态
        setWorldData((prev) => ({
          ...prev,
          characters: [...prev.characters, newCharacter as any],
        }));

        // 保存到后端
        await DataService.createCharacter(newCharacter as any);
        showToast('success', '人物添加成功');
      } else {
        // 更新现有人物
        const updatedCharacter = {
          ...character,
          updatedAt: new Date(),
        };

        // 更新本地状态
        setWorldData((prev) => ({
          ...prev,
          characters: prev.characters.map((c) =>
            c.id === character.id ? updatedCharacter as any : c
          ),
        }));

        // 保存到后端
        await DataService.updateCharacter(character.id!, updatedCharacter as any);
        showToast('success', '人物更新成功');
      }
    } catch (error) {
      const isNew = character.id?.startsWith('temp-');
      showToast('error', isNew ? '人物添加失败' : '人物更新失败');
      console.error('Failed to save character:', error);
    }
  }, [workId, showToast]);

  const handleCharacterDelete = useCallback((id: string) => {
    const character = worldData.characters.find((c) => c.id === id);
    if (!character) return;

    if (!confirm(`确定要删除人物"${character.name}"吗？`)) {
      return;
    }

    setWorldData((prev) => ({
      ...prev,
      characters: prev.characters.filter((c) => c.id !== id),
    }));

    showToast('success', '人物删除成功');
  }, [worldData.characters, showToast]);

  /**
   * 地点管理 - 保存地点（新增或更新）
   */
  const handleLocationSave = useCallback(async (location: Partial<Location>) => {
    if (!workId) return;

    try {
      const isNew = location.id?.startsWith('temp-');

      if (isNew) {
        // 创建新地点
        const newLocation = {
          ...location,
          id: 'location-' + Date.now(),
          workId,
          createdAt: new Date(),
          updatedAt: new Date(),
        };

        // 更新本地状态
        setWorldData((prev) => ({
          ...prev,
          locations: [...prev.locations, newLocation as any],
        }));

        // 保存到后端
        await DataService.createLocation(newLocation as any);
        showToast('success', '地点添加成功');
      } else {
        // 更新现有地点
        const updatedLocation = {
          ...location,
          updatedAt: new Date(),
        };

        // 更新本地状态
        setWorldData((prev) => ({
          ...prev,
          locations: prev.locations.map((l) =>
            l.id === location.id ? updatedLocation as any : l
          ),
        }));

        // 保存到后端
        await DataService.updateLocation(location.id!, updatedLocation as any);
        showToast('success', '地点更新成功');
      }
    } catch (error) {
      const isNew = location.id?.startsWith('temp-');
      showToast('error', isNew ? '地点添加失败' : '地点更新失败');
      console.error('Failed to save location:', error);
    }
  }, [workId, showToast]);

  const handleLocationDelete = useCallback((id: string) => {
    const location = worldData.locations.find((l) => l.id === id);
    if (!location) return;

    if (!confirm(`确定要删除地点"${location.name}"吗？`)) {
      return;
    }

    setWorldData((prev) => ({
      ...prev,
      locations: prev.locations.filter((l) => l.id !== id),
    }));

    showToast('success', '地点删除成功');
  }, [worldData.locations, showToast]);

  /**
   * 设定管理 - 保存设定（新增或更新）
   */
  const handleSettingSave = useCallback(async (setting: Partial<Setting>) => {
    if (!workId) return;

    try {
      const isNew = setting.id?.startsWith('temp-');

      if (isNew) {
        // 创建新设定
        const newSetting = {
          ...setting,
          id: 'setting-' + Date.now(),
          workId,
          createdAt: new Date(),
          updatedAt: new Date(),
        };

        // 更新本地状态
        setWorldData((prev) => ({
          ...prev,
          settings: [...prev.settings, newSetting as any],
        }));

        // 保存到后端
        await DataService.createSetting(newSetting as any);
        showToast('success', '设定添加成功');
      } else {
        // 更新现有设定
        const updatedSetting = {
          ...setting,
          updatedAt: new Date(),
        };

        // 更新本地状态
        setWorldData((prev) => ({
          ...prev,
          settings: prev.settings.map((s) =>
            s.id === setting.id ? updatedSetting as any : s
          ),
        }));

        // 保存到后端
        await DataService.updateSetting(setting.id!, updatedSetting as any);
        showToast('success', '设定更新成功');
      }
    } catch (error) {
      const isNew = setting.id?.startsWith('temp-');
      showToast('error', isNew ? '设定添加失败' : '设定更新失败');
      console.error('Failed to save setting:', error);
    }
  }, [workId, showToast]);

  const handleSettingDelete = useCallback((id: string) => {
    const setting = worldData.settings.find((s) => s.id === id);
    if (!setting) return;

    if (!confirm(`确定要删除设定"${setting.title}"吗？`)) {
      return;
    }

    setWorldData((prev) => ({
      ...prev,
      settings: prev.settings.filter((s) => s.id !== id),
    }));

    showToast('success', '设定删除成功');
  }, [worldData.settings, showToast]);

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
    <div style={{ display: 'flex', width: '100%', height: '100vh', overflow: 'hidden' }}>
      {/* 左侧章节树 */}
      <div style={{ width: '280px', height: '100%', flexShrink: 0 }}>
        <ChapterTree
          chapters={novelChapters}
          currentChapterId={currentChapterId}
          onChapterSelect={handleChapterSelect}
          onChapterAdd={handleAddChapter}
          onChapterEdit={handleEditChapter}
          onChapterDelete={handleDeleteChapter}
          onChapterMove={handleChapterMove}
        />
      </div>

      {/* 中间编辑器区域 */}
      <div style={{ flex: 1, height: '100%', overflow: 'hidden' }}>
        <NovelEditor
          content={currentChapterContent}
          onSave={handleEditorSave}
          placeholder="开始写作..."
          autoSave={true}
          autoSaveInterval={3000}
        />
      </div>

      {/* 右侧世界观管理 */}
      <div style={{ width: '320px', height: '100%', flexShrink: 0 }}>
        <WorldManager
          worldData={worldData}
          onCharacterSave={handleCharacterSave}
          onCharacterDelete={handleCharacterDelete}
          onLocationSave={handleLocationSave}
          onLocationDelete={handleLocationDelete}
          onSettingSave={handleSettingSave}
          onSettingDelete={handleSettingDelete}
        />
      </div>
    </div>
  );
};

export default WorkDetailView;
