/**
 * EditorWrapper — 兼容层
 *
 * 接收与 NovelEditor 相同的 props 签名，内部代理到 MilkdownEditor。
 * 保留顶部工具栏（章节标题 + 面板折叠按钮）。
 */
import React, { useCallback, useState } from 'react';
import { PanelLeftClose, PanelLeftOpen, PanelRightClose, PanelRightOpen } from 'lucide-react';
import MilkdownEditor from './MilkdownEditor';
import DiffViewer from '../agent/DiffViewer';

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
}) => {
  const [showDiff, setShowDiff] = useState(false);
  const [diffOriginal, setDiffOriginal] = useState('');

  // 代理 onSave：MilkdownEditor 返回 md string，第二个参数传 null
  const handleSave = useCallback((md: string) => {
    onSave?.(md, null);
  }, [onSave]);

  // 监听 diff 视图切换事件
  React.useEffect(() => {
    const handleShowDiff = (e: Event) => {
      const detail = (e as CustomEvent).detail;
      if (detail?.original !== undefined && detail?.modified !== undefined) {
        setDiffOriginal(detail.original);
        setShowDiff(true);
      }
    };
    const handleHideDiff = () => setShowDiff(false);

    window.addEventListener('editor-show-diff', handleShowDiff);
    window.addEventListener('editor-hide-diff', handleHideDiff);
    return () => {
      window.removeEventListener('editor-show-diff', handleShowDiff);
      window.removeEventListener('editor-hide-diff', handleHideDiff);
    };
  }, []);

  return (
    <div className="flex flex-col h-full">
      {/* 顶部工具栏 */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-zinc-100 dark:border-slate-700 flex-shrink-0">
        <div className="flex items-center gap-2">
          {/* 左侧面板折叠按钮 */}
          {isLeftPanelCollapsed && onExpandLeftPanel && (
            <button
              type="button"
              onClick={onExpandLeftPanel}
              className="h-7 w-7 flex items-center justify-center text-zinc-400 hover:text-zinc-700 hover:bg-zinc-100 rounded-lg transition-all dark:text-slate-500 dark:hover:text-slate-200 dark:hover:bg-slate-800"
            >
              <PanelLeftOpen className="h-4 w-4" />
            </button>
          )}
          {!isLeftPanelCollapsed && onCollapseLeftPanel && (
            <button
              type="button"
              onClick={onCollapseLeftPanel}
              className="h-7 w-7 flex items-center justify-center text-zinc-400 hover:text-zinc-700 hover:bg-zinc-100 rounded-lg transition-all dark:text-slate-500 dark:hover:text-slate-200 dark:hover:bg-slate-800"
            >
              <PanelLeftClose className="h-4 w-4" />
            </button>
          )}
          {/* 章节标题 */}
          <span className="text-sm text-zinc-700 dark:text-slate-200 font-medium truncate max-w-[300px]">
            {chapterOrder !== undefined && `第${chapterOrder}章 `}
            {chapterTitle || ''}
          </span>
        </div>

        <div className="flex items-center gap-1">
          {/* 右侧面板折叠按钮 */}
          {isRightPanelCollapsed && onExpandRightPanel && (
            <button
              type="button"
              onClick={onExpandRightPanel}
              className="h-7 w-7 flex items-center justify-center text-zinc-400 hover:text-zinc-700 hover:bg-zinc-100 rounded-lg transition-all dark:text-slate-500 dark:hover:text-slate-200 dark:hover:bg-slate-800"
            >
              <PanelRightOpen className="h-4 w-4" />
            </button>
          )}
          {!isRightPanelCollapsed && onCollapseRightPanel && (
            <button
              type="button"
              onClick={onCollapseRightPanel}
              className="h-7 w-7 flex items-center justify-center text-zinc-400 hover:text-zinc-700 hover:bg-zinc-100 rounded-lg transition-all dark:text-slate-500 dark:hover:text-slate-200 dark:hover:bg-slate-800"
            >
              <PanelRightClose className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      {/* 编辑器内容区域 */}
      <div className="flex-1 min-h-0">
        {showDiff ? (
          <div className="h-full overflow-y-auto p-4">
            <div className="mb-3 flex items-center justify-between">
              <span className="text-sm font-medium text-zinc-700 dark:text-slate-200">差异对比</span>
              <button
                type="button"
                onClick={() => setShowDiff(false)}
                className="text-xs text-zinc-500 hover:text-zinc-700 dark:text-slate-400 dark:hover:text-slate-200"
              >
                关闭对比
              </button>
            </div>
            <DiffViewer original={diffOriginal} modified={content} />
          </div>
        ) : (
          <MilkdownEditor
            content={content}
            onSave={handleSave}
            autoSaveInterval={autoSaveInterval}
            placeholder={placeholder}
            storageKey={chapterId}
          />
        )}
      </div>
    </div>
  );
};

export default EditorWrapper;
