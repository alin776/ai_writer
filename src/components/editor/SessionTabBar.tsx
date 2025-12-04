import React from 'react';
import { Plus, Globe2, FileText, MessageSquare, X } from 'lucide-react';
import { useEditorStore, type RightSidebarType } from '../../store/editorStore';
import type { Tab } from '@/utils/tabStorage';
import clsx from 'clsx';

interface SessionTabBarProps {
  tabs: Tab[];
  activeTabId: string;
  onSwitchTab: (tabId: string) => void;
  onCreateTab: (afterTabId?: string) => void;
  onCloseTab: (tabId: string) => void;
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
}) => {
  const { rightSidebarType, toggleRightSidebar, closeRightSidebar } = useEditorStore();

  const functionButtons = [
    { type: 'agent' as RightSidebarType, icon: MessageSquare, title: 'AI助手' },
    { type: 'summary' as RightSidebarType, icon: FileText, title: '概要' },
    { type: 'worldview' as RightSidebarType, icon: Globe2, title: '世界观' },
  ];

  return (
    <div className="flex items-center justify-between h-10 px-3 border-b bg-white" style={{ borderColor: '#e5e7eb' }}>
      {/* 左侧：会话标签区域 */}
      <div className="flex items-center gap-1 flex-1 overflow-x-auto">
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
                  ? 'bg-[#f1f5f9] border-[#e5e7eb] text-[#0f172a] shadow-[0_1px_2px_rgba(0,0,0,0.05)]'
                  : 'bg-white border-transparent text-[#475569] hover:bg-[#f8fafc] hover:border-[#e5e7eb]'
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
                  className="ml-1 text-[#94a3b8] hover:text-[#0f172a] text-xs transition-colors"
                  title="关闭会话"
                >
                  ×
                </span>
              )}
            </button>
          );
        })}

        {tabs.length === 0 && <span className="text-sm text-[#94a3b8] px-2">暂无会话</span>}
      </div>

      {/* 右侧：功能按钮组 */}
      <div className="flex items-center gap-1">
        {/* + 新增会话按钮 */}
        <button
          className="p-1.5 rounded transition-all"
          style={{ color: '#6b7280' }}
          onClick={() => onCreateTab(activeTabId)}
          onMouseEnter={(e) => {
            e.currentTarget.style.color = '#111827';
            e.currentTarget.style.backgroundColor = '#f3f4f6';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.color = '#6b7280';
            e.currentTarget.style.backgroundColor = 'transparent';
          }}
          title="新增会话"
        >
          <Plus className="w-4 h-4" />
        </button>

        {/* 功能图标按钮 */}
        {functionButtons.map(({ type, icon: Icon, title }) => (
          <button
            key={type}
            onClick={() => toggleRightSidebar(type)}
            className={clsx('p-1.5 rounded transition-all')}
            style={
              rightSidebarType === type
                ? { backgroundColor: '#eff6ff', color: '#2563eb' }
                : { color: '#6b7280' }
            }
            onMouseEnter={(e) => {
              if (rightSidebarType !== type) {
                e.currentTarget.style.color = '#111827';
                e.currentTarget.style.backgroundColor = '#f3f4f6';
              }
            }}
            onMouseLeave={(e) => {
              if (rightSidebarType !== type) {
                e.currentTarget.style.color = '#6b7280';
                e.currentTarget.style.backgroundColor = 'transparent';
              }
            }}
            title={title}
          >
            <Icon className="w-4 h-4" />
          </button>
        ))}

        {/* 关闭按钮 */}
        <button
          onClick={closeRightSidebar}
          className="p-1.5 rounded transition-all"
          style={{ color: '#6b7280' }}
          onMouseEnter={(e) => {
            e.currentTarget.style.color = '#111827';
            e.currentTarget.style.backgroundColor = '#f3f4f6';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.color = '#6b7280';
            e.currentTarget.style.backgroundColor = 'transparent';
          }}
          title="关闭"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default SessionTabBar;
