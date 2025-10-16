/**
 * 编辑器左侧边栏
 * 包含章节树和世界观管理
 */
import React, { useState } from 'react';
import { FileText, Globe } from 'lucide-react';
import ChapterTree from './ChapterTree';
import WorldManager from './WorldManager';
import { Chapter, WorldData } from '@/types/novel';
import './sidebar-styles.css';

type SidebarTab = 'chapters' | 'world';

interface EditorSidebarProps {
  // 章节相关
  chapters: Chapter[];
  currentChapterId?: string;
  onChapterSelect: (chapterId: string) => void;
  onChapterAdd: (parentId?: string) => void;
  onChapterEdit: (chapterId: string) => void;
  onChapterDelete: (chapterId: string) => void;
  onChapterMove: (chapterId: string, newOrder: number) => void;

  // 世界观相关
  worldData: WorldData;
  onCharacterSave: (character: any) => void;
  onCharacterDelete: (id: string) => void;
  onLocationSave: (location: any) => void;
  onLocationDelete: (id: string) => void;
  onSettingSave: (setting: any) => void;
  onSettingDelete: (id: string) => void;
}

const EditorSidebar: React.FC<EditorSidebarProps> = ({
  chapters,
  currentChapterId,
  onChapterSelect,
  onChapterAdd,
  onChapterEdit,
  onChapterDelete,
  onChapterMove,
  worldData,
  onCharacterSave,
  onCharacterDelete,
  onLocationSave,
  onLocationDelete,
  onSettingSave,
  onSettingDelete,
}) => {
  const [activeTab, setActiveTab] = useState<SidebarTab>('chapters');

  return (
    <div className="editor-sidebar">
      {/* Tab 切换 */}
      <div className="sidebar-tabs">
        <button
          className={`sidebar-tab ${activeTab === 'chapters' ? 'active' : ''}`}
          onClick={() => setActiveTab('chapters')}
        >
          <FileText className="w-4 h-4" />
          <span>章节</span>
        </button>
        <button
          className={`sidebar-tab ${activeTab === 'world' ? 'active' : ''}`}
          onClick={() => setActiveTab('world')}
        >
          <Globe className="w-4 h-4" />
          <span>世界观</span>
        </button>
      </div>

      {/* 内容区 */}
      <div className="sidebar-content">
        {activeTab === 'chapters' ? (
          <ChapterTree
            chapters={chapters}
            currentChapterId={currentChapterId}
            onChapterSelect={onChapterSelect}
            onChapterAdd={onChapterAdd}
            onChapterEdit={onChapterEdit}
            onChapterDelete={onChapterDelete}
            onChapterMove={onChapterMove}
          />
        ) : (
          <WorldManager
            worldData={worldData}
            onCharacterSave={onCharacterSave}
            onCharacterDelete={onCharacterDelete}
            onLocationSave={onLocationSave}
            onLocationDelete={onLocationDelete}
            onSettingSave={onSettingSave}
            onSettingDelete={onSettingDelete}
          />
        )}
      </div>
    </div>
  );
};

export default EditorSidebar;
