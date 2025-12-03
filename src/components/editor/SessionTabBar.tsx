import React from 'react';
import { Plus, Globe2, FileText, MessageSquare, X } from 'lucide-react';
import { useEditorStore, type RightSidebarType } from '../../store/editorStore';
import clsx from 'clsx';

/**
 * SessionTabBar 组件 - 会话标签栏
 *
 * 布局: [会话标签...] [+] [🌍] [📄] [💬] [×]
 */
export const SessionTabBar: React.FC = () => {
  const { rightSidebarType, toggleRightSidebar, closeRightSidebar } = useEditorStore();

  const functionButtons = [
    { type: 'agent' as RightSidebarType, icon: MessageSquare, title: 'AI助手' },
    { type: 'summary' as RightSidebarType, icon: FileText, title: '概括' },
    { type: 'worldview' as RightSidebarType, icon: Globe2, title: '世界观' },
  ];

  return (
    <div className="flex items-center justify-between h-10 px-3 border-b bg-white" style={{ borderColor: '#e5e7eb' }}>
      {/* 左侧：会话标签区域（暂时为空） */}
      <div className="flex items-center gap-1.5 flex-1">
        {/* 会话标签将在后续添加 */}
      </div>

      {/* 右侧：功能按钮组 */}
      <div className="flex items-center gap-1">
        {/* + 新增会话按钮 */}
        <button
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
