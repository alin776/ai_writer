/**
 * 章节树组件
 * 支持拖拽排序、新增章节、进入编辑
 */
import React, { useState } from 'react';
import {
  ChevronRight,
  ChevronDown,
  Plus,
  Edit2,
  Trash2,
  FileText,
  Circle,
  CheckCircle2,
  Archive,
} from 'lucide-react';
import { Chapter, ChapterStatus } from '@/types/novel';

interface ChapterTreeProps {
  chapters: Chapter[];
  currentChapterId?: string;
  onChapterSelect: (chapterId: string) => void;
  onChapterAdd: (parentId?: string) => void;
  onChapterEdit: (chapterId: string) => void;
  onChapterDelete: (chapterId: string) => void;
  onChapterMove: (chapterId: string, newOrder: number) => void;
}

const ChapterTree: React.FC<ChapterTreeProps> = ({
  chapters,
  currentChapterId,
  onChapterSelect,
  onChapterAdd,
  onChapterEdit,
  onChapterDelete,
  onChapterMove,
}) => {
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set());
  const [draggedId, setDraggedId] = useState<string | null>(null);

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
        return '已发布';
      case 'archived':
        return '已归档';
      default:
        return '草稿';
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
    if (draggedId && draggedId !== targetId) {
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
          >
            <div className="chapter-title">{chapter.title}</div>
            <div className="chapter-meta">
              {getStatusIcon(chapter.status)}
              <span className="status-text">{getStatusText(chapter.status)}</span>
              <span className="word-count">{chapter.wordCount.toLocaleString()} 字</span>
            </div>
          </div>

          {/* 操作按钮 */}
          <div className="chapter-actions">
            <button
              className="action-btn"
              onClick={(e) => {
                e.stopPropagation();
                onChapterEdit(chapter.id);
              }}
              title="编辑"
            >
              <Edit2 className="w-3.5 h-3.5" />
            </button>
            <button
              className="action-btn"
              onClick={(e) => {
                e.stopPropagation();
                onChapterDelete(chapter.id);
              }}
              title="删除"
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

  return (
    <div className="chapter-tree">
      {/* 头部 */}
      <div className="chapter-tree-header">
        <h3 className="tree-title">章节</h3>
        <button
          className="add-chapter-btn"
          onClick={() => onChapterAdd()}
          title="新增章节"
        >
          <Plus className="w-4 h-4" />
        </button>
      </div>

      {/* 章节列表 */}
      <div className="chapter-list">
        {rootChapters.length > 0 ? (
          rootChapters.map((chapter) => renderChapter(chapter))
        ) : (
          <div className="empty-state">
            <FileText className="w-12 h-12 text-gray-300 mb-2" />
            <p className="text-sm text-gray-400">暂无章节</p>
            <button
              className="text-sm text-blue-500 hover:text-blue-600 mt-2"
              onClick={() => onChapterAdd()}
            >
              创建第一个章节
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChapterTree;
