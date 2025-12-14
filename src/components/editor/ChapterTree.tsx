/**
 * 章节树组件
 * 支持内联编辑、拖拽排序、新增章节
 */
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import {
  ChevronRight,
  ChevronDown,
  Plus,
  Trash2,
  FileText,
  Circle,
  CheckCircle2,
  Archive,
  Save,
  X,
} from 'lucide-react';
import { Chapter, ChapterStatus } from '@/types/novel';

interface ChapterTreeProps {
  chapters: Chapter[];
  currentChapterId?: string;
  onChapterSelect: (chapterId: string) => void;
  onChapterSave: (chapter: Partial<Chapter> & { id?: string }) => void;
  onChapterDelete: (chapterId: string) => void;
  onChapterMove?: (chapterId: string, newOrder: number) => void;
}

const ChapterTree: React.FC<ChapterTreeProps> = ({
  chapters,
  currentChapterId,
  onChapterSelect,
  onChapterSave,
  onChapterDelete,
  onChapterMove,
}) => {
  const { t } = useTranslation();
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set());
  const [draggedId, setDraggedId] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editingData, setEditingData] = useState<any>(null);

  // 获取状态图标
  const getStatusIcon = (status: ChapterStatus) => {
    switch (status) {
      case 'published':
        return <CheckCircle2 className="w-3 h-3 text-green-500" />;
      case 'archived':
        return <Archive className="w-3 h-3 text-gray-400" />;
      default:
        return <Circle className="w-3 h-3 text-yellow-500" />;
    }
  };

  // 获取状态文本
  const getStatusText = (status: ChapterStatus) => {
    switch (status) {
      case 'published':
        return t('editor.status.published');
      case 'archived':
        return t('editor.status.archived');
      default:
        return t('editor.status.draft');
    }
  };

  // 切换展开/折叠
  const toggleExpand = (chapterId: string) => {
    const newExpanded = new Set(expandedIds);
    if (newExpanded.has(chapterId)) {
      newExpanded.delete(chapterId);
    } else {
      newExpanded.add(chapterId);
    }
    setExpandedIds(newExpanded);
  };

  // 获取子章节
  const getChildChapters = (parentId?: string) => {
    return chapters
      .filter((c) => c.parentId === parentId)
      .sort((a, b) => a.order - b.order);
  };

  // 获取章节编号（从1开始）
  const getChapterNumber = (chapterId: string) => {
    const sortedChapters = [...chapters].sort((a, b) => a.order - b.order);
    return sortedChapters.findIndex((c) => c.id === chapterId) + 1;
  };

  // 格式化章节标题（添加编号）
  const formatChapterTitle = (title: string, chapterId: string) => {
    const chapterNum = getChapterNumber(chapterId);
    // 检查标题是否已经有"第X章"格式
    if (/^第\d+章/.test(title) || /^Chapter \d+/.test(title)) {
      return title;
    }
    return t('editor.chapterNumber', { n: chapterNum }) + ' ' + title;
  };

  // 开始编辑
  const startEditing = (chapter: Chapter) => {
    setEditingId(chapter.id);
    // 编辑时移除"第X章"前缀，只编辑实际标题
    const titleWithoutPrefix = chapter.title.replace(/^第\d+章\s*/, '');
    setEditingData({
      id: chapter.id,
      title: titleWithoutPrefix,
      content: chapter.content,
    });
  };

  // 取消编辑
  const cancelEditing = () => {
    setEditingId(null);
    setEditingData(null);
  };

  // 保存编辑
  const saveEditing = () => {
    if (!editingData || !editingData.title.trim()) {
      return;
    }

    // 保存时不添加编号，让显示时自动添加
    const saveData = {
      ...editingData,
      title: editingData.title.trim()
    };

    onChapterSave(saveData);
    cancelEditing();
  };

  // 添加新章节（内联编辑）
  const handleAdd = () => {
    const newId = 'temp-' + Date.now();
    const newChapter = {
      id: newId,
      title: '',
      content: '',
      order: chapters.length,
    };

    setEditingId(newId);
    setEditingData(newChapter);
  };

  // 拖拽开始
  const handleDragStart = (e: React.DragEvent, chapterId: string) => {
    setDraggedId(chapterId);
    e.dataTransfer.effectAllowed = 'move';
  };

  // 拖拽结束
  const handleDragEnd = () => {
    setDraggedId(null);
  };

  // 拖拽进入
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  // 放置
  const handleDrop = (e: React.DragEvent, targetId: string) => {
    e.preventDefault();
    if (draggedId && draggedId !== targetId && onChapterMove) {
      const targetChapter = chapters.find((c) => c.id === targetId);
      if (targetChapter) {
        onChapterMove(draggedId, targetChapter.order);
      }
    }
    setDraggedId(null);
  };

  // 渲染章节项
  const renderChapter = (chapter: Chapter, level: number = 0) => {
    const hasChildren = getChildChapters(chapter.id).length > 0;
    const isExpanded = expandedIds.has(chapter.id);
    const isActive = currentChapterId === chapter.id;
    const isDragging = draggedId === chapter.id;
    const isEditing = editingId === chapter.id;

    if (isEditing) {
      return (
        <div
          key={chapter.id}
          className="p-3 rounded-lg border border-blue-500 bg-blue-50 mb-2"
          style={{ marginLeft: `${level * 1.5}rem` }}
        >
          <div className="space-y-2">
            <input
              type="text"
              value={editingData.title || ''}
              onChange={(e) =>
                setEditingData({ ...editingData, title: e.target.value })
              }
              placeholder={t('editor.chapterTitlePlaceholder')}
              className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              autoFocus
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  saveEditing();
                } else if (e.key === 'Escape') {
                  cancelEditing();
                }
              }}
            />
            {editingData.title && (
              <div className="text-xs text-gray-500 mt-1">
                {t('editor.preview')}: {t('editor.chapterNumber', { n: chapters.length + (editingData.id?.startsWith('temp-') ? 1 : getChapterNumber(editingData.id)) })} {editingData.title}
              </div>
            )}
            <div className="flex justify-end gap-2">
              <button
                onClick={cancelEditing}
                className="px-2 py-1 text-xs text-gray-600 hover:text-gray-800 flex items-center gap-1"
              >
                <X className="w-3 h-3" />
                {t('common.cancel')}
              </button>
              <button
                onClick={saveEditing}
                disabled={!editingData.title?.trim()}
                className="px-2 py-1 text-xs text-white bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed rounded flex items-center gap-1"
              >
                <Save className="w-3 h-3" />
                {t('common.save')}
              </button>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div key={chapter.id} className="chapter-tree-item">
        <div
          className={`chapter-item ${isActive ? 'active' : ''} ${isDragging ? 'dragging' : ''}`}
          style={{ paddingLeft: `${level * 1.5 + 0.5}rem` }}
          draggable
          onDragStart={(e) => handleDragStart(e, chapter.id)}
          onDragEnd={handleDragEnd}
          onDragOver={handleDragOver}
          onDrop={(e) => handleDrop(e, chapter.id)}
        >
          {/* 展开/折叠按钮 */}
          <button
            className="expand-btn"
            onClick={() => hasChildren && toggleExpand(chapter.id)}
          >
            {hasChildren ? (
              isExpanded ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )
            ) : (
              <div className="w-4 h-4" />
            )}
          </button>

          {/* 章节图标 */}
          <FileText className="w-4 h-4 text-gray-400 flex-shrink-0" />

          {/* 章节信息 */}
          <div
            className="chapter-info flex-1"
            onClick={() => onChapterSelect(chapter.id)}
            onDoubleClick={() => startEditing(chapter)}
          >
            <div className="chapter-title">{formatChapterTitle(chapter.title, chapter.id)}</div>
            <div className="chapter-meta">
              {getStatusIcon(chapter.status)}
              <span className="status-text">{getStatusText(chapter.status)}</span>
              <span className="word-count">{(chapter.wordCount || 0).toLocaleString()} {t('editor.words')}</span>
            </div>
          </div>

          {/* 操作按钮 */}
          <div className="chapter-actions">
            <button
              className="action-btn"
              onClick={(e) => {
                e.stopPropagation();
                onChapterDelete(chapter.id);
              }}
              title={t('editor.deleteChapter')}
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* 子章节 */}
        {hasChildren && isExpanded && (
          <div className="chapter-children">
            {getChildChapters(chapter.id).map((child) =>
              renderChapter(child, level + 1)
            )}
          </div>
        )}
      </div>
    );
  };

  const rootChapters = getChildChapters();
  
  // 如果正在添加新章节，显示在列表顶部
  const displayChapters = editingId?.startsWith('temp-')
    ? [editingData as Chapter, ...rootChapters]
    : rootChapters;

  return (
    <div className="chapter-tree">
      {/* 头部 */}
      <div className="chapter-tree-header">
        <h3 className="tree-title">{t('editor.chapters')}</h3>
        <button
          className="add-chapter-btn"
          onClick={handleAdd}
          title={t('editor.addChapter')}
        >
          <Plus className="w-4 h-4" />
        </button>
      </div>

      {/* 章节列表 */}
      <div className="chapter-list">
        {displayChapters.length > 0 ? (
          displayChapters.map((chapter) => renderChapter(chapter))
        ) : (
          <div className="empty-state">
            <FileText className="w-12 h-12 text-gray-300 mb-2" />
            <p className="text-sm text-gray-400">{t('editor.noChapters')}</p>
            <button
              className="text-sm text-blue-500 hover:text-blue-600 mt-2"
              onClick={handleAdd}
            >
              {t('editor.createFirstChapter')}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChapterTree;
