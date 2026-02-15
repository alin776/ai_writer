/**
 * EditorTabBar — VS Code 风格的编辑器标签栏
 *
 * 标签格式：📄 06-重锁.md
 * 激活标签白底深色文字，非激活灰色文字 hover 变亮，X 关闭按钮。
 */
import React, { useCallback, useRef } from 'react';
import { FileText, X } from 'lucide-react';
import type { EditorTab } from '../../hooks/useEditorTabs';

interface EditorTabBarProps {
  tabs: EditorTab[];
  activeTabId: string | null;
  onTabSwitch: (tabId: string) => void;
  onTabClose: (tabId: string) => void;
}

const EditorTabBar: React.FC<EditorTabBarProps> = ({
  tabs,
  activeTabId,
  onTabSwitch,
  onTabClose,
}) => {
  if (tabs.length === 0) return null;

  const containerRef = useRef<HTMLDivElement>(null);

  // 鼠标滚轮 → 横向滚动
  const handleWheel = useCallback((e: React.WheelEvent) => {
    if (!containerRef.current) return;
    e.preventDefault();
    containerRef.current.scrollLeft += e.deltaY;
  }, []);

  return (
    <div
      ref={containerRef}
      onWheel={handleWheel}
      data-scroll-scope="editor-tabs"
      className="flex items-center h-8 border-b border-zinc-100 dark:border-slate-700 bg-transparent overflow-x-auto flex-shrink-0 scrollbar-hide"
    >
      {tabs.map(tab => {
        const isActive = tab.id === activeTabId;
        const label = `${String(tab.order).padStart(2, '0')}-${tab.title}.md`;

        return (
          <div
            key={tab.id}
            onClick={() => onTabSwitch(tab.id)}
            className={`group flex items-center gap-1.5 px-3 h-full cursor-pointer border-r border-zinc-100 dark:border-slate-700 select-none transition-colors duration-150 max-w-[200px] ${
              isActive
                ? 'bg-white dark:bg-slate-800 text-zinc-900 dark:text-slate-100'
                : 'text-zinc-500 dark:text-slate-400 hover:text-zinc-700 dark:hover:text-slate-200 hover:bg-zinc-50 dark:hover:bg-slate-800/60'
            }`}
          >
            <FileText className="h-3.5 w-3.5 flex-shrink-0 opacity-60" />
            <span className="text-xs truncate">{label}</span>
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onTabClose(tab.id);
              }}
              className={`h-4 w-4 flex items-center justify-center rounded-sm flex-shrink-0 transition-all ${
                isActive
                  ? 'opacity-60 hover:opacity-100 hover:bg-zinc-200 dark:hover:bg-slate-600'
                  : 'opacity-0 group-hover:opacity-60 hover:!opacity-100 hover:bg-zinc-200 dark:hover:bg-slate-600'
              }`}
              aria-label="关闭标签"
            >
              <X className="h-3 w-3" />
            </button>
          </div>
        );
      })}
    </div>
  );
};

export default EditorTabBar;
