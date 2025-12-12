import React from 'react';
import { Plus, Globe2, FileText, MessageSquare, MoreHorizontal, Clock3, PanelRightClose } from 'lucide-react';
import { useEditorStore, type RightSidebarType } from '../../store/editorStore';
import type { Tab } from '@/utils/tabStorage';
import clsx from 'clsx';

interface SessionTabBarProps {
  tabs: Tab[];
  activeTabId: string;
  onSwitchTab: (tabId: string) => void;
  onCreateTab: (afterTabId?: string) => Promise<any>;
  onCloseTab: (tabId: string) => void;
  onOpenHistory?: () => void;
  onCollapseRightPanel?: () => void;
}

/**
 * SessionTabBar 组件 - 会话标签栏
 *
 * 布局: [会话标签...] [+] [🌍] [📄] [💬] [×]
 */
export const SessionTabBar: React.FC<SessionTabBarProps> = ({
  tabs,
  activeTabId,
  onSwitchTab,
  onCreateTab,
  onCloseTab,
  onOpenHistory,
  onCollapseRightPanel,
}) => {
  const { rightSidebarType, toggleRightSidebar, closeRightSidebar } = useEditorStore();
  const [creating, setCreating] = React.useState(false);
  const tabsContainerRef = React.useRef<HTMLDivElement>(null);

  const handleCreate = async () => {
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
    { type: 'agent' as RightSidebarType, icon: MessageSquare, title: 'AI助手' },
    { type: 'summary' as RightSidebarType, icon: FileText, title: '概要' },
    { type: 'worldview' as RightSidebarType, icon: Globe2, title: '世界观' },
  ];

  const handleTabsWheel = (e: React.WheelEvent<HTMLDivElement>) => {
    const container = tabsContainerRef.current;
    if (!container) return;
    const delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
    if (delta === 0) return;
    container.scrollLeft += delta;
    e.preventDefault();
  };

  return (
    <div className="flex items-center justify-between h-10 px-3 border-b bg-white dark:bg-slate-900 border-gray-200 dark:border-slate-700">
      {/* 左侧：会话标签区域 */}
      <div
        ref={tabsContainerRef}
        onWheel={handleTabsWheel}
        className="flex items-center gap-1 flex-1 overflow-x-auto overflow-y-hidden"
      >
        {tabs.map((tab) => {
          const isActive = tab.id === activeTabId;
          const title = tab.title?.trim() || '新会话';

          return (
            <button
              key={tab.id}
              onClick={() => onSwitchTab(tab.id)}
              className={clsx(
                'group flex items-center gap-2 px-3 h-8 rounded-md border transition-all text-sm min-w-[120px]',
                isActive
                  ? 'bg-slate-100 dark:bg-slate-800 border-gray-200 dark:border-slate-600 text-slate-900 dark:text-slate-100 shadow-[0_1px_2px_rgba(0,0,0,0.05)]'
                  : 'bg-white dark:bg-slate-900 border-transparent text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:border-gray-200 dark:hover:border-slate-600'
              )}
              title={title}
            >
              <span className="truncate text-[13px]">{title}</span>
              {tabs.length > 1 && (
                <span
                  onClick={(e) => {
                    e.stopPropagation();
                    onCloseTab(tab.id);
                  }}
                  className="ml-1 text-slate-400 dark:text-slate-500 hover:text-slate-900 dark:hover:text-slate-200 text-xs transition-colors"
                  title="关闭会话"
                >
                  ×
                </span>
              )}
            </button>
          );
        })}

        {tabs.length === 0 && <span className="text-sm text-slate-400 dark:text-slate-500 px-2">暂无会话</span>}
      </div>

      {/* 右侧：功能按钮组 */}
      <div className="flex items-center gap-1">
        {/* + 新增会话按钮 */}
        <button
          className="p-1.5 rounded transition-all text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 hover:bg-gray-100 dark:hover:bg-slate-700"
          onClick={handleCreate}
          disabled={creating}
          title="新增会话"
        >
          <Plus className="w-4 h-4" />
        </button>

        {/* 功能图标按钮 */}
        {functionButtons.map(({ type, icon: Icon, title }) => (
          <button
            key={type}
            onClick={() => toggleRightSidebar(type)}
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

        {/* 历史入口：改为时钟图标，保持浅色风格 */}
        <button
          onClick={() => (onOpenHistory ? onOpenHistory() : closeRightSidebar())}
          className="p-1.5 rounded transition-all text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 hover:bg-gray-100 dark:hover:bg-slate-700"
          title="历史会话"
        >
          <Clock3 className="w-4 h-4" />
        </button>

        {/* 收起右侧面板 - 挪到历史会话之后 */}
        <button
          className="p-1.5 rounded transition-all text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-100 hover:bg-gray-100 dark:hover:bg-slate-700"
          onClick={() => onCollapseRightPanel?.()}
          title="收起侧栏"
        >
          <PanelRightClose className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default SessionTabBar;
