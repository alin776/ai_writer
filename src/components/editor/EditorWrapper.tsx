/**
 * EditorWrapper — 兼容层
 *
 * 接收与 NovelEditor 相同的 props 签名，内部代理到 MilkdownEditor。
 * 保留顶部工具栏（章节标题 + 面板折叠按钮）。
 */
import React, { useCallback } from 'react';
import MilkdownEditor from './MilkdownEditor';
import EditorTabBar from './EditorTabBar';
import type { EditorTab } from '../../hooks/useEditorTabs';

interface EditorWrapperProps {
  content?: string;
  onSave?: (content: string, json: any) => void;
  placeholder?: string;
  autoSave?: boolean;
  autoSaveInterval?: number;
  chapterTitle?: string;
  chapterOrder?: number;
  workId?: string;
  chapterId?: string;
  aiAutoCompleteEnabled?: boolean;
  onToggleAIAutoComplete?: () => void;
  isLeftPanelCollapsed?: boolean;
  onExpandLeftPanel?: () => void;
  onCollapseLeftPanel?: () => void;
  isRightPanelCollapsed?: boolean;
  onExpandRightPanel?: () => void;
  onCollapseRightPanel?: () => void;
  isAIPanelCollapsed?: boolean;
  onToggleAIPanel?: () => void;
  onCollapseAIPanel?: () => void;
  onInlineAISend?: (message: string, context: any) => void;
  isInlineAILoading?: boolean;
  // 多标签页 props（可选，有值时渲染标签栏替代原页眉）
  tabs?: EditorTab[];
  activeTabId?: string | null;
  onTabSwitch?: (tabId: string) => void;
  onTabClose?: (tabId: string) => void;
}

const EditorWrapper: React.FC<EditorWrapperProps> = ({
  content = '',
  onSave,
  placeholder,
  autoSaveInterval = 3000,
  chapterTitle,
  chapterOrder,
  chapterId,
  isLeftPanelCollapsed,
  onExpandLeftPanel,
  onCollapseLeftPanel,
  isRightPanelCollapsed,
  onExpandRightPanel,
  onCollapseRightPanel,
  tabs,
  activeTabId,
  onTabSwitch,
  onTabClose,
}) => {
  // 代理 onSave：MilkdownEditor 返回 md string，第二个参数传 null
  const handleSave = useCallback((md: string) => {
    onSave?.(md, null);
  }, [onSave]);

  return (
    <div className="flex flex-col h-full">
      {/* 顶部：标签栏 or 章节标题 */}
      {tabs && tabs.length > 0 && onTabSwitch && onTabClose ? (
        <EditorTabBar
          tabs={tabs}
          activeTabId={activeTabId ?? null}
          onTabSwitch={onTabSwitch}
          onTabClose={onTabClose}
        />
      ) : (
        <div className="flex items-center justify-between px-4 h-8 border-b border-zinc-100 dark:border-slate-700 flex-shrink-0">
          <span className="text-sm text-zinc-700 dark:text-slate-200 font-medium truncate max-w-[300px]">
            {chapterOrder !== undefined && `第${chapterOrder}章 `}
            {chapterTitle || ''}
          </span>
        </div>
      )}

      {/* 编辑器内容区域 — 始终渲染 MilkdownEditor（内联 Diff 由 diffDecorationPlugin 处理） */}
      <div className="flex-1 min-h-0">
        <MilkdownEditor
          content={content}
          onSave={handleSave}
          autoSaveInterval={autoSaveInterval}
          placeholder={placeholder}
          storageKey={chapterId}
        />
      </div>
    </div>
  );
};

export default EditorWrapper;
