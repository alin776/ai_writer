/**
 * 世界观管理组件
 * 管理人物、地点、设定 - 支持内联编辑
 */
import React, { useState } from 'react';
import {
  Users,
  MapPin,
  BookOpen,
  Plus,
  Trash2,
  Save,
  X,
} from 'lucide-react';
import { WorldData, Character, Location, Setting } from '@/types/novel';

type TabType = 'characters' | 'locations' | 'settings';

interface WorldManagerProps {
  worldData: WorldData;
  onCharacterSave: (character: Partial<Character>) => void;
  onCharacterDelete: (id: string) => void;
  onLocationSave: (location: Partial<Location>) => void;
  onLocationDelete: (id: string) => void;
  onSettingSave: (setting: Partial<Setting>) => void;
  onSettingDelete: (id: string) => void;
}

const WorldManager: React.FC<WorldManagerProps> = ({
  worldData,
  onCharacterSave,
  onCharacterDelete,
  onLocationSave,
  onLocationDelete,
  onSettingSave,
  onSettingDelete,
}) => {
  const [activeTab, setActiveTab] = useState<TabType>('characters');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editingData, setEditingData] = useState<any>(null);

  // 开始编辑
  const startEditing = (item: any) => {
    setEditingId(item.id);
    setEditingData({ ...item });
  };

  // 取消编辑
  const cancelEditing = () => {
    setEditingId(null);
    setEditingData(null);
  };

  // 保存编辑
  const saveEditing = () => {
    if (!editingData) return;

    if (activeTab === 'characters') {
      onCharacterSave(editingData);
    } else if (activeTab === 'locations') {
      onLocationSave(editingData);
    } else if (activeTab === 'settings') {
      onSettingSave(editingData);
    }

    cancelEditing();
  };

  // 添加新项（创建临时编辑状态）
  const handleAdd = () => {
    const newId = 'temp-' + Date.now();
    const newItem: any = { id: newId, name: '', description: '' };

    if (activeTab === 'characters') {
      newItem.role = '';
    } else if (activeTab === 'locations') {
      newItem.type = '';
    } else if (activeTab === 'settings') {
      newItem.title = '';
      newItem.content = '';
      newItem.category = '';
    }

    setEditingId(newId);
    setEditingData(newItem);
  };

  // 渲染人物列表
  const renderCharacters = () => {
    const characters = worldData.characters || [];
    const items = editingId?.startsWith('temp-') && activeTab === 'characters'
      ? [editingData, ...characters]
      : characters;

    if (items.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center py-12 text-gray-400">
          <Users className="w-12 h-12 mb-2" />
          <p className="text-sm">暂无人物</p>
        </div>
      );
    }

    return (
      <div className="space-y-2">
        {items.map((character: Character) => {
          const isEditing = editingId === character.id;

          return (
            <div
              key={character.id}
              className={`p-3 rounded-lg border transition-all ${
                isEditing
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }`}
            >
              {isEditing ? (
                <div className="space-y-2">
                  <input
                    type="text"
                    value={editingData.name || ''}
                    onChange={(e) =>
                      setEditingData({ ...editingData, name: e.target.value })
                    }
                    placeholder="人物名称*"
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    autoFocus
                  />
                  <input
                    type="text"
                    value={editingData.role || ''}
                    onChange={(e) =>
                      setEditingData({ ...editingData, role: e.target.value })
                    }
                    placeholder="角色（如：主角、配角）"
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <textarea
                    value={editingData.description || ''}
                    onChange={(e) =>
                      setEditingData({ ...editingData, description: e.target.value })
                    }
                    placeholder="人物描述"
                    rows={2}
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  />
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={cancelEditing}
                      className="px-3 py-1 text-xs text-gray-600 hover:text-gray-800 flex items-center gap-1"
                    >
                      <X className="w-3 h-3" />
                      取消
                    </button>
                    <button
                      onClick={saveEditing}
                      disabled={!editingData.name?.trim()}
                      className="px-3 py-1 text-xs text-white bg-blue-600 rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-1"
                    >
                      <Save className="w-3 h-3" />
                      保存
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-medium text-gray-900 truncate">
                        {character.name}
                      </h4>
                      {character.role && (
                        <p className="text-xs text-gray-500 mt-0.5">{character.role}</p>
                      )}
                      {character.description && (
                        <p className="text-xs text-gray-600 mt-1 line-clamp-2">
                          {character.description}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center gap-1 ml-2">
                      <button
                        onClick={() => startEditing(character)}
                        className="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
                        title="编辑"
                      >
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                        </svg>
                      </button>
                      <button
                        onClick={() => {
                          if (confirm(`确定要删除人物"${character.name}"吗？`)) {
                            onCharacterDelete(character.id);
                          }
                        }}
                        className="p-1 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
                        title="删除"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    );
  };

  // 渲染地点列表
  const renderLocations = () => {
    const locations = worldData.locations || [];
    const items = editingId?.startsWith('temp-') && activeTab === 'locations'
      ? [editingData, ...locations]
      : locations;

    if (items.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center py-12 text-gray-400">
          <MapPin className="w-12 h-12 mb-2" />
          <p className="text-sm">暂无地点</p>
        </div>
      );
    }

    return (
      <div className="space-y-2">
        {items.map((location: Location) => {
          const isEditing = editingId === location.id;

          return (
            <div
              key={location.id}
              className={`p-3 rounded-lg border transition-all ${
                isEditing
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }`}
            >
              {isEditing ? (
                <div className="space-y-2">
                  <input
                    type="text"
                    value={editingData.name || ''}
                    onChange={(e) =>
                      setEditingData({ ...editingData, name: e.target.value })
                    }
                    placeholder="地点名称*"
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    autoFocus
                  />
                  <input
                    type="text"
                    value={editingData.type || ''}
                    onChange={(e) =>
                      setEditingData({ ...editingData, type: e.target.value })
                    }
                    placeholder="类型（如：城市、建筑、自然）"
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <textarea
                    value={editingData.description || ''}
                    onChange={(e) =>
                      setEditingData({ ...editingData, description: e.target.value })
                    }
                    placeholder="地点描述"
                    rows={2}
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  />
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={cancelEditing}
                      className="px-3 py-1 text-xs text-gray-600 hover:text-gray-800 flex items-center gap-1"
                    >
                      <X className="w-3 h-3" />
                      取消
                    </button>
                    <button
                      onClick={saveEditing}
                      disabled={!editingData.name?.trim()}
                      className="px-3 py-1 text-xs text-white bg-blue-600 rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-1"
                    >
                      <Save className="w-3 h-3" />
                      保存
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-medium text-gray-900 truncate">
                        {location.name}
                      </h4>
                      {location.type && (
                        <p className="text-xs text-gray-500 mt-0.5">{location.type}</p>
                      )}
                      {location.description && (
                        <p className="text-xs text-gray-600 mt-1 line-clamp-2">
                          {location.description}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center gap-1 ml-2">
                      <button
                        onClick={() => startEditing(location)}
                        className="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
                        title="编辑"
                      >
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                        </svg>
                      </button>
                      <button
                        onClick={() => {
                          if (confirm(`确定要删除地点"${location.name}"吗？`)) {
                            onLocationDelete(location.id);
                          }
                        }}
                        className="p-1 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
                        title="删除"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    );
  };

  // 渲染设定列表
  const renderSettings = () => {
    const settings = worldData.settings || [];
    const items = editingId?.startsWith('temp-') && activeTab === 'settings'
      ? [editingData, ...settings]
      : settings;

    if (items.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center py-12 text-gray-400">
          <BookOpen className="w-12 h-12 mb-2" />
          <p className="text-sm">暂无设定</p>
        </div>
      );
    }

    return (
      <div className="space-y-2">
        {items.map((setting: Setting) => {
          const isEditing = editingId === setting.id;

          return (
            <div
              key={setting.id}
              className={`p-3 rounded-lg border transition-all ${
                isEditing
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }`}
            >
              {isEditing ? (
                <div className="space-y-2">
                  <input
                    type="text"
                    value={editingData.title || ''}
                    onChange={(e) =>
                      setEditingData({ ...editingData, title: e.target.value })
                    }
                    placeholder="设定标题*"
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    autoFocus
                  />
                  <input
                    type="text"
                    value={editingData.category || ''}
                    onChange={(e) =>
                      setEditingData({ ...editingData, category: e.target.value })
                    }
                    placeholder="分类（如：世界观、魔法体系、科技）"
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <textarea
                    value={editingData.content || ''}
                    onChange={(e) =>
                      setEditingData({ ...editingData, content: e.target.value })
                    }
                    placeholder="设定内容"
                    rows={3}
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  />
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={cancelEditing}
                      className="px-3 py-1 text-xs text-gray-600 hover:text-gray-800 flex items-center gap-1"
                    >
                      <X className="w-3 h-3" />
                      取消
                    </button>
                    <button
                      onClick={saveEditing}
                      disabled={!editingData.title?.trim()}
                      className="px-3 py-1 text-xs text-white bg-blue-600 rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-1"
                    >
                      <Save className="w-3 h-3" />
                      保存
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-medium text-gray-900 truncate">
                        {setting.title}
                      </h4>
                      {setting.category && (
                        <p className="text-xs text-gray-500 mt-0.5">{setting.category}</p>
                      )}
                      {setting.content && (
                        <p className="text-xs text-gray-600 mt-1 line-clamp-2">
                          {setting.content}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center gap-1 ml-2">
                      <button
                        onClick={() => startEditing(setting)}
                        className="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
                        title="编辑"
                      >
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                        </svg>
                      </button>
                      <button
                        onClick={() => {
                          if (confirm(`确定要删除设定"${setting.title}"吗？`)) {
                            onSettingDelete(setting.id);
                          }
                        }}
                        className="p-1 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
                        title="删除"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="h-full flex flex-col bg-white border-l border-gray-200">
      {/* Tab 切换 */}
      <div className="flex border-b border-gray-200 bg-gray-50">
        <button
          className={`flex-1 px-3 py-2.5 text-sm font-medium transition-colors ${
            activeTab === 'characters'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-white'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
          }`}
          onClick={() => setActiveTab('characters')}
        >
          <Users className="w-4 h-4 inline-block mr-1" />
          人物
        </button>
        <button
          className={`flex-1 px-3 py-2.5 text-sm font-medium transition-colors ${
            activeTab === 'locations'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-white'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
          }`}
          onClick={() => setActiveTab('locations')}
        >
          <MapPin className="w-4 h-4 inline-block mr-1" />
          地点
        </button>
        <button
          className={`flex-1 px-3 py-2.5 text-sm font-medium transition-colors ${
            activeTab === 'settings'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-white'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
          }`}
          onClick={() => setActiveTab('settings')}
        >
          <BookOpen className="w-4 h-4 inline-block mr-1" />
          设定
        </button>
      </div>

      {/* 内容区域 */}
      <div className="flex-1 overflow-y-auto p-3">
        {/* 添加按钮 */}
        <button
          onClick={handleAdd}
          disabled={!!editingId}
          className="w-full mb-3 px-3 py-2 text-sm text-blue-600 border-2 border-dashed border-blue-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-1"
        >
          <Plus className="w-4 h-4" />
          添加{activeTab === 'characters' ? '人物' : activeTab === 'locations' ? '地点' : '设定'}
        </button>

        {/* 列表 */}
        {activeTab === 'characters' && renderCharacters()}
        {activeTab === 'locations' && renderLocations()}
        {activeTab === 'settings' && renderSettings()}
      </div>
    </div>
  );
};

export default WorldManager;
