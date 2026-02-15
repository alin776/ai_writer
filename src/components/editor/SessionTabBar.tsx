import React from 'react';
import { useTranslation } from 'react-i18next';
import { SquarePen, Globe2, Clock3, List, FileEdit } from 'lucide-react';
import { useEditorStore, type RightSidebarType } from '../../store/editorStore';
import clsx from 'clsx';

interface SessionTabBarProps {
  isReady?: boolean;
  onCreateTab: (afterTabId?: string) => Promise<any>;
  onOpenHistory?: () => void;
  activeTabId?: string;
  // 左侧面板（目录）展开/收缩
  isLeftPanelCollapsed?: boolean;
  onExpandLeftPanel?: () => void;
  onCollapseLeftPanel?: () => void;
  // 右侧编辑器展开/收缩
  isEditorCollapsed?: boolean;
  onToggleEditor?: () => void;
}

/**
 * SessionTabBar 组件 - 功能按钮栏
 *
 * 布局: [目录] [🕐] [🌍] [📖] [+]
 */
export const SessionTabBar: React.FC<SessionTabBarProps> = ({
  isReady = true,
  onCreateTab,
  onOpenHistory,
  activeTabId,
  isLeftPanelCollapsed = false,
  onExpandLeftPanel,
  onCollapseLeftPanel,
  isEditorCollapsed = false,
  onToggleEditor,
}) => {
  const { t } = useTranslation();
  const { rightSidebarType, toggleRightSidebar, closeRightSidebar } = useEditorStore();
  const [creating, setCreating] = React.useState(false);
  // 记录打开世界观前编辑器是否收缩
  const editorWasCollapsedRef = React.useRef<boolean | null>(null);

  const handleCreate = async () => {
    if (!isReady) return;
    if (creating) return;
    setCreating(true);
    try {
      await onCreateTab(activeTabId);
    } catch (err) {
      console.error('[SessionTabBar] create tab failed:', err);
    } finally {
      setCreating(false);
    }
  };

  const functionButtons = [
    { type: 'worldview' as RightSidebarType, icon: Globe2, title: t('editor.sessionTab.worldview') },
  ];

  return (
    <div className="flex items-center h-10 px-3 bg-white dark:bg-slate-900">
      {/* 功能按钮组 */}
      <div className="flex items-center gap-1">
        {/* 1. 目录展开/收缩按钮 */}
        {isLeftPanelCollapsed ? (
          <button
            onClick={() => onExpandLeftPanel?.()}
            className="p-1.5 rounded transition-all text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 hover:bg-gray-100 dark:hover:bg-slate-700"
            title={t('editor.toolbar.expandChapterList')}
          >
            <List className="w-4 h-4" />
          </button>
        ) : (
          <button
            onClick={() => onCollapseLeftPanel?.()}
            className="p-1.5 rounded transition-all text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 hover:bg-gray-100 dark:hover:bg-slate-700"
            title={t('editor.toolbar.collapseChapterList')}
          >
            <List className="w-4 h-4" />
          </button>
        )}

        {/* 2. 会话记录按钮 */}
        <button
          onClick={() => (onOpenHistory ? onOpenHistory() : closeRightSidebar())}
          className="p-1.5 rounded transition-all text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 hover:bg-gray-100 dark:hover:bg-slate-700"
          title={t('editor.sessionTab.history')}
        >
          <Clock3 className="w-4 h-4" />
        </button>

        {/* 3. 世界观按钮 */}
        {functionButtons.map(({ type, icon: Icon, title }) => (
          <button
            key={type}
            onClick={() => {
              const isOpening = rightSidebarType !== type;

              if (type === 'worldview' && onToggleEditor) {
                if (isOpening) {
                  editorWasCollapsedRef.current = isEditorCollapsed;
                  if (isEditorCollapsed) {
                    onToggleEditor();
                  }
                } else {
                  if (editorWasCollapsedRef.current === true && !isEditorCollapsed) {
                    onToggleEditor();
                  }
                  editorWasCollapsedRef.current = null;
                }
              }

              toggleRightSidebar(type);
            }}
            className={clsx(
              'p-1.5 rounded transition-all',
              rightSidebarType === type
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                : 'text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 hover:bg-gray-100 dark:hover:bg-slate-700'
            )}
            title={title}
          >
            <Icon className="w-4 h-4" />
          </button>
        ))}

        {/* 4. 编辑器展开/收缩按钮 */}
        {onToggleEditor && (
          <button
            onClick={onToggleEditor}
            className="p-1.5 rounded transition-all text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 hover:bg-gray-100 dark:hover:bg-slate-700"
            title={isEditorCollapsed ? t('editor.sessionTab.expandEditor') : t('editor.sessionTab.collapseEditor')}
          >
            <FileEdit className="w-4 h-4" />
          </button>
        )}

        {/* 5. 新增会话按钮 */}
        <button
          className={clsx(
            "p-1.5 rounded transition-all",
            isReady
              ? "text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 hover:bg-gray-100 dark:hover:bg-slate-700"
              : "text-gray-400 dark:text-slate-600 cursor-not-allowed"
          )}
          onClick={handleCreate}
          disabled={creating || !isReady}
          title={isReady ? t('editor.sessionTab.addSession') : t('common.loading')}
        >
          <SquarePen className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default SessionTabBar;
