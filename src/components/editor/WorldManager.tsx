/**
 * 世界观管理组件
 * 管理人物、地点、设定 - 支持内联编辑
 */
import React, { useState } from 'react';
import {
  Users,
  MapPin,
  BookOpen,
  FileText,
  Plus,
  Trash2,
  Save,
  X,
} from 'lucide-react';
import { WorldData, Character, Location, Setting } from '@/types/novel';

type TabType = 'characters' | 'locations' | 'settings' | 'guidelines' | 'ai-guidelines';

interface WorldManagerProps {
  worldData: WorldData;
  onCharacterSave: (character: Partial<Character>) => void;
  onCharacterDelete: (id: string) => void;
  onLocationSave: (location: Partial<Location>) => void;
  onLocationDelete: (id: string) => void;
  onSettingSave: (setting: Partial<Setting>) => void;
  onSettingDelete: (id: string) => void;
  onGuidelinesSave?: (guidelines: any) => void;
  onAIGuidelinesSave?: (guidelines: any) => void;
}

const WorldManager: React.FC<WorldManagerProps> = ({
  worldData,
  onCharacterSave,
  onCharacterDelete,
  onLocationSave,
  onLocationDelete,
  onSettingSave,
  onSettingDelete,
  onGuidelinesSave,
  onAIGuidelinesSave,
}) => {
  const [activeTab, setActiveTab] = useState<TabType>('characters');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editingData, setEditingData] = useState<any>(null);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(['strategic']));

  // 折叠分组切换
  const toggleSection = (section: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(section)) {
      newExpanded.delete(section);
    } else {
      newExpanded.add(section);
    }
    setExpandedSections(newExpanded);
  };

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
                        onClick={() => onCharacterDelete(character.id)}
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
                        onClick={() => onLocationDelete(location.id)}
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
                        onClick={() => onSettingDelete(setting.id)}
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
        <button
          className={`flex-1 px-3 py-2.5 text-sm font-medium transition-colors ${
            activeTab === 'guidelines'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-white'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
          }`}
          onClick={() => setActiveTab('guidelines')}
        >
          <FileText className="w-4 h-4 inline-block mr-1" />
          规范
        </button>
        <button
          className={`flex-1 px-3 py-2.5 text-sm font-medium transition-colors ${
            activeTab === 'ai-guidelines'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-white'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
          }`}
          onClick={() => setActiveTab('ai-guidelines')}
        >
          <svg className="w-4 h-4 inline-block mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          AI规范
        </button>
      </div>

      {/* 内容区域 */}
      <div className="flex-1 overflow-y-auto p-3">
        {/* 添加按钮 - 作品规范和AI规范不显示 */}
        {activeTab !== 'guidelines' && activeTab !== 'ai-guidelines' && (
          <button
            onClick={handleAdd}
            disabled={!!editingId}
            className="w-full mb-3 px-3 py-2 text-sm text-blue-600 border-2 border-dashed border-blue-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-1"
          >
            <Plus className="w-4 h-4" />
            添加{activeTab === 'characters' ? '人物' : activeTab === 'locations' ? '地点' : '设定'}
          </button>
        )}

        {/* 列表 */}
        {activeTab === 'characters' && renderCharacters()}
        {activeTab === 'locations' && renderLocations()}
        {activeTab === 'settings' && renderSettings()}
        {activeTab === 'guidelines' && renderGuidelines()}
        {activeTab === 'ai-guidelines' && renderAIGuidelines()}
      </div>
    </div>
  );
  
  // 渲染作品规范
  function renderGuidelines() {
    const guidelines = worldData.guidelines || {};
    const isEditing = editingId === 'guidelines';
    
    return (
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-gray-900">作品规范</h3>
          {!isEditing && (
            <button
              onClick={() => {
                setEditingId('guidelines');
                setEditingData({ ...guidelines });
              }}
              className="px-3 py-1.5 text-xs text-white bg-blue-600 rounded hover:bg-blue-700 transition-colors"
            >
              {Object.keys(guidelines).length > 0 ? '编辑规范' : '设置规范'}
            </button>
          )}
        </div>

        {isEditing ? (
          <div className="space-y-4">
            <div className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">大纲流程</label>
                <textarea
                  value={editingData.outline || ''}
                  onChange={(e) => setEditingData({ ...editingData, outline: e.target.value })}
                  placeholder="输入大纲流程"
                  rows={3}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">整体风格</label>
                <input
                  type="text"
                  value={editingData.style || ''}
                  onChange={(e) => setEditingData({ ...editingData, style: e.target.value })}
                  placeholder="例如：古风、现代都市"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            <div className="flex justify-end gap-2 pt-4">
              <button onClick={cancelEditing} className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800">
                取消
              </button>
              <button
                onClick={() => {
                  if (onGuidelinesSave) {
                    onGuidelinesSave(editingData);
                    setEditingId(null);
                    setEditingData(null);
                  }
                }}
                className="px-4 py-2 text-sm text-white bg-blue-600 rounded-lg hover:bg-blue-700"
              >
                保存
              </button>
            </div>
          </div>
        ) : (
          Object.keys(guidelines).length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-gray-400">
              <FileText className="w-16 h-16 mb-3" />
              <p className="text-sm font-medium mb-1">暂未设置作品规范</p>
            </div>
          ) : (
            <div className="space-y-3 text-sm">
              {guidelines.outline && (
                <div className="p-3 bg-blue-50 rounded">
                  <div className="text-xs text-blue-600 mb-1 font-semibold">大纲流程</div>
                  <div className="text-gray-900">{guidelines.outline}</div>
                </div>
              )}
            </div>
          )
        )}
      </div>
    );
  }
  
  // 渲染AI创作规范 - 完整的32字段表单
  function renderAIGuidelines() {
    const aiGuidelines = worldData.aiGuidelines || {};
    const isEditing = editingId === 'ai-guidelines';
    
    return (
      <div className="h-full overflow-y-auto">
        <div className="flex items-center justify-between mb-4 sticky top-0 bg-white z-10 pb-3 border-b border-gray-200">
          <h3 className="text-sm font-semibold text-gray-900">AI创作规范</h3>
          {!isEditing && (
            <button
              onClick={() => {
                setEditingId('ai-guidelines');
                setEditingData({ ...aiGuidelines });
              }}
              className="px-3 py-1.5 text-xs text-white bg-blue-600 rounded hover:bg-blue-700 transition-colors"
            >
              {Object.keys(aiGuidelines).length > 0 ? '编辑规范' : '设置规范'}
            </button>
          )}
        </div>

{isEditing ? (
          <div className="space-y-6 pb-20">
            {/* 战略定位 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <button onClick={() => toggleSection('strategic')} className="w-full px-4 py-3 bg-gradient-to-r from-blue-50 to-blue-100 border-b border-blue-200 flex items-center justify-between hover:from-blue-100 hover:to-blue-150 transition-colors">
                <span className="text-sm font-semibold text-blue-900">📋 一、战略定位</span>
                <svg className={`w-5 h-5 text-blue-600 transition-transform ${expandedSections.has('strategic') ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
              </button>
              {expandedSections.has('strategic') && (
                <div className="p-4 space-y-3 bg-white">
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">商业目标</label><input type="text" value={editingData.businessGoal || ''} onChange={(e) => setEditingData({ ...editingData, businessGoal: e.target.value })} placeholder="例如：争取头部平台签约、冲击月票榜前100" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">目标读者</label><input type="text" value={editingData.targetAudience || ''} onChange={(e) => setEditingData({ ...editingData, targetAudience: e.target.value })} placeholder="例如：18-35岁男性，喜欢逆袭爽文" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">商业对标</label><input type="text" value={editingData.commercialBenchmark || ''} onChange={(e) => setEditingData({ ...editingData, commercialBenchmark: e.target.value })} placeholder="例如：《完美世界》《遮天》《诡秘之主》" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">高概念卖点</label><input type="text" value={editingData.highConcept || ''} onChange={(e) => setEditingData({ ...editingData, highConcept: e.target.value })} placeholder="当[经典类型]遇上[新奇元素]" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" /></div>
                </div>
              )}
            </div>

            {/* IP架构 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <button onClick={() => toggleSection('ip')} className="w-full px-4 py-3 bg-gradient-to-r from-purple-50 to-purple-100 border-b border-purple-200 flex items-center justify-between hover:from-purple-100 hover:to-purple-150 transition-colors">
                <span className="text-sm font-semibold text-purple-900">🎭 二、IP架构</span>
                <svg className={`w-5 h-5 text-purple-600 transition-transform ${expandedSections.has('ip') ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
              </button>
              {expandedSections.has('ip') && (
                <div className="p-4 space-y-3 bg-white">
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">核心悖论/设定</label><textarea value={editingData.coreParadox || ''} onChange={(e) => setEditingData({ ...editingData, coreParadox: e.target.value })} placeholder="例如：不能说话的播音员、害怕水的航海家" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">主导情感</label><input type="text" value={editingData.dominantEmotion || ''} onChange={(e) => setEditingData({ ...editingData, dominantEmotion: e.target.value })} placeholder="例如：逆袭的爽感、被理解的慰藉" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">核心IP符号</label><input type="text" value={editingData.coreIpSymbols || ''} onChange={(e) => setEditingData({ ...editingData, coreIpSymbols: e.target.value })} placeholder="例如：赤霄剑、九龙拉棺、吞天魔功" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent" /></div>
                </div>
              )}
            </div>

            {/* 叙事引擎 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <button onClick={() => toggleSection('narrative')} className="w-full px-4 py-3 bg-gradient-to-r from-green-50 to-green-100 border-b border-green-200 flex items-center justify-between hover:from-green-100 hover:to-green-150 transition-colors">
                <span className="text-sm font-semibold text-green-900">⚡ 三、叙事引擎</span>
                <svg className={`w-5 h-5 text-green-600 transition-transform ${expandedSections.has('narrative') ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
              </button>
              {expandedSections.has('narrative') && (
                <div className="p-4 space-y-3 bg-white">
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">主角弧光（缺陷/能力/转变）</label><textarea value={editingData.protagonistArc || ''} onChange={(e) => setEditingData({ ...editingData, protagonistArc: e.target.value })} placeholder="例如：自卑→自信、无能→强大" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">核心关系冲突</label><textarea value={editingData.coreConflict || ''} onChange={(e) => setEditingData({ ...editingData, coreConflict: e.target.value })} placeholder="例如：主角与师父的理念冲突" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">叙事节奏</label><input type="text" value={editingData.narrativeRhythm || ''} onChange={(e) => setEditingData({ ...editingData, narrativeRhythm: e.target.value })} placeholder="例如：3章一小爽，10章一大爽" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" /></div>
                </div>
              )}
            </div>

            {/* 文字质感 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <button onClick={() => toggleSection('writing')} className="w-full px-4 py-3 bg-gradient-to-r from-amber-50 to-amber-100 border-b border-amber-200 flex items-center justify-between hover:from-amber-100 hover:to-amber-150 transition-colors">
                <span className="text-sm font-semibold text-amber-900">✍️ 四、文字质感</span>
                <svg className={`w-5 h-5 text-amber-600 transition-transform ${expandedSections.has('writing') ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
              </button>
              {expandedSections.has('writing') && (
                <div className="p-4 space-y-3 bg-white">
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">文笔风格</label><input type="text" value={editingData.writingStyle || ''} onChange={(e) => setEditingData({ ...editingData, writingStyle: e.target.value })} placeholder="例如：冷峻简洁、华丽诗性" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">文风注意事项</label><textarea value={editingData.styleNotes || ''} onChange={(e) => setEditingData({ ...editingData, styleNotes: e.target.value })} placeholder="例如：避免冗长对话、多用动作描写" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent resize-none" /></div>
                </div>
              )}
            </div>

            {/* 技术规范 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <button onClick={() => toggleSection('technical')} className="w-full px-4 py-3 bg-gradient-to-r from-red-50 to-red-100 border-b border-red-200 flex items-center justify-between hover:from-red-100 hover:to-red-150 transition-colors">
                <span className="text-sm font-semibold text-red-900">⚙️ 五、技术规范</span>
                <svg className={`w-5 h-5 text-red-600 transition-transform ${expandedSections.has('technical') ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
              </button>
              {expandedSections.has('technical') && (
                <div className="p-4 space-y-3 bg-white">
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">章节长度</label><input type="text" value={editingData.chapterLength || ''} onChange={(e) => setEditingData({ ...editingData, chapterLength: e.target.value })} placeholder="例如：2000-3000字" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">内容禁忌</label><textarea value={editingData.contentTaboos || ''} onChange={(e) => setEditingData({ ...editingData, contentTaboos: e.target.value })} placeholder="例如：避免政治敏感、暴力血腥、色情内容" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent resize-none" /></div>
                </div>
              )}
            </div>

            <div className="border-t-4 border-gray-300 pt-6 mt-6"><h4 className="text-sm font-bold text-gray-900 mb-4">第二部分：核心设定</h4></div>

            {/* 小说类型 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <button onClick={() => toggleSection('genre')} className="w-full px-4 py-3 bg-gradient-to-r from-indigo-50 to-indigo-100 border-b border-indigo-200 flex items-center justify-between hover:from-indigo-100 hover:to-indigo-150 transition-colors">
                <span className="text-sm font-semibold text-indigo-900">📚 一、小说类型与体裁</span>
                <svg className={`w-5 h-5 text-indigo-600 transition-transform ${expandedSections.has('genre') ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
              </button>
              {expandedSections.has('genre') && (
                <div className="p-4 space-y-3 bg-white">
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">一级类型</label><input type="text" value={editingData.primaryGenre || ''} onChange={(e) => setEditingData({ ...editingData, primaryGenre: e.target.value })} placeholder="例如：玄幻、都市、科幻" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">二级标签</label><input type="text" value={editingData.secondaryTags || ''} onChange={(e) => setEditingData({ ...editingData, secondaryTags: e.target.value })} placeholder="例如：升级流、无敌流、系统流" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">创作基调</label><input type="text" value={editingData.creativeTone || ''} onChange={(e) => setEditingData({ ...editingData, creativeTone: e.target.value })} placeholder="例如：轻松诙谐、严肃沉重" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" /></div>
                </div>
              )}
            </div>

            {/* 世界背景 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <button onClick={() => toggleSection('world')} className="w-full px-4 py-3 bg-gradient-to-r from-cyan-50 to-cyan-100 border-b border-cyan-200 flex items-center justify-between hover:from-cyan-100 hover:to-cyan-150 transition-colors">
                <span className="text-sm font-semibold text-cyan-900">🌍 二、世界背景设定</span>
                <svg className={`w-5 h-5 text-cyan-600 transition-transform ${expandedSections.has('world') ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
              </button>
              {expandedSections.has('world') && (
                <div className="p-4 space-y-3 bg-white">
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">核心世界观简介</label><textarea value={editingData.worldIntro || ''} onChange={(e) => setEditingData({ ...editingData, worldIntro: e.target.value })} placeholder="用100字左右描述核心世界观" rows={3} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent resize-none" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">主要场景/地点</label><textarea value={editingData.mainLocations || ''} onChange={(e) => setEditingData({ ...editingData, mainLocations: e.target.value })} placeholder="例如：帝都、修仙门派、魔兽森林" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent resize-none" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">世界规则</label><textarea value={editingData.worldRules || ''} onChange={(e) => setEditingData({ ...editingData, worldRules: e.target.value })} placeholder="例如：弱肉强食、强者为尊" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent resize-none" /></div>
                </div>
              )}
            </div>

            {/* 力量体系 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <button onClick={() => toggleSection('power')} className="w-full px-4 py-3 bg-gradient-to-r from-pink-50 to-pink-100 border-b border-pink-200 flex items-center justify-between hover:from-pink-100 hover:to-pink-150 transition-colors">
                <span className="text-sm font-semibold text-pink-900">💪 三、力量体系/特殊设定</span>
                <svg className={`w-5 h-5 text-pink-600 transition-transform ${expandedSections.has('power') ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
              </button>
              {expandedSections.has('power') && (
                <div className="p-4 space-y-3 bg-white">
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">体系名称</label><input type="text" value={editingData.powerSystemName || ''} onChange={(e) => setEditingData({ ...editingData, powerSystemName: e.target.value })} placeholder="例如：修真境界、异能等级" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">等级划分</label><textarea value={editingData.powerLevels || ''} onChange={(e) => setEditingData({ ...editingData, powerLevels: e.target.value })} placeholder="例如：炼气、筑基、金丹、元婴" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent resize-none" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">代价与限制</label><textarea value={editingData.powerCost || ''} onChange={(e) => setEditingData({ ...editingData, powerCost: e.target.value })} placeholder="例如：需要消耗寿命、会失去情感" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent resize-none" /></div>
                </div>
              )}
            </div>

            <div className="border-t-4 border-gray-300 pt-6 mt-6"><h4 className="text-sm font-bold text-gray-900 mb-4">第三部分：人物与剧情</h4></div>

            {/* 主角设定 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <button onClick={() => toggleSection('protagonist')} className="w-full px-4 py-3 bg-gradient-to-r from-teal-50 to-teal-100 border-b border-teal-200 flex items-center justify-between hover:from-teal-100 hover:to-teal-150 transition-colors">
                <span className="text-sm font-semibold text-teal-900">👤 一、主角核心设定</span>
                <svg className={`w-5 h-5 text-teal-600 transition-transform ${expandedSections.has('protagonist') ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
              </button>
              {expandedSections.has('protagonist') && (
                <div className="p-4 space-y-3 bg-white">
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">主角名字</label><input type="text" value={editingData.protagonistName || ''} onChange={(e) => setEditingData({ ...editingData, protagonistName: e.target.value })} placeholder="例如：张三、叶凡" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">身份与背景</label><input type="text" value={editingData.protagonistIdentity || ''} onChange={(e) => setEditingData({ ...editingData, protagonistIdentity: e.target.value })} placeholder="例如：孤儿、废柴、天才" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">性格特点</label><input type="text" value={editingData.protagonistTraits || ''} onChange={(e) => setEditingData({ ...editingData, protagonistTraits: e.target.value })} placeholder="例如：隐忍、果敢、腹黑" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">终极目标</label><input type="text" value={editingData.protagonistGoal || ''} onChange={(e) => setEditingData({ ...editingData, protagonistGoal: e.target.value })} placeholder="例如：复仇、成仙、守护家人" className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent" /></div>
                </div>
              )}
            </div>

            {/* 剧情构思 */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <button onClick={() => toggleSection('plot')} className="w-full px-4 py-3 bg-gradient-to-r from-orange-50 to-orange-100 border-b border-orange-200 flex items-center justify-between hover:from-orange-100 hover:to-orange-150 transition-colors">
                <span className="text-sm font-semibold text-orange-900">📖 二、剧情构思</span>
                <svg className={`w-5 h-5 text-orange-600 transition-transform ${expandedSections.has('plot') ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
              </button>
              {expandedSections.has('plot') && (
                <div className="p-4 space-y-3 bg-white">
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">冲突设计</label><textarea value={editingData.conflictDesign || ''} onChange={(e) => setEditingData({ ...editingData, conflictDesign: e.target.value })} placeholder="例如：家族矛盾、种族冲突" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">第一幕（序章-30%）</label><textarea value={editingData.actOne || ''} onChange={(e) => setEditingData({ ...editingData, actOne: e.target.value })} placeholder="建立世界观，主角遭遇变故" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">第二幕（30%-70%）</label><textarea value={editingData.actTwo || ''} onChange={(e) => setEditingData({ ...editingData, actTwo: e.target.value })} placeholder="主角成长、遭遇挫折、升级打怪" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none" /></div>
                  <div><label className="block text-xs font-medium text-gray-700 mb-1">第三幕（70%-结局）</label><textarea value={editingData.actThree || ''} onChange={(e) => setEditingData({ ...editingData, actThree: e.target.value })} placeholder="最终对决、解决主要冲突" rows={2} className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none" /></div>
                </div>
              )}
            </div>

            {/* 保存/取消按钮 */}
            <div className="sticky bottom-0 bg-white border-t-2 border-gray-300 pt-4 pb-4 flex justify-end gap-3">
              <button
                onClick={() => {
                  setEditingId(null);
                  setEditingData(null);
                }}
                className="px-6 py-2.5 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                取消
              </button>
              <button
                onClick={() => {
                  if (onAIGuidelinesSave) {
                    onAIGuidelinesSave(editingData);
                    setEditingId(null);
                    setEditingData(null);
                  }
                }}
                className="px-6 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <Save className="w-4 h-4" />
                保存规范
              </button>
            </div>
          </div>
        ) : (
          Object.keys(aiGuidelines).length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-gray-400">
              <svg className="w-16 h-16 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <p className="text-sm font-medium mb-1">暂未设置AI创作规范</p>
              <p className="text-xs text-gray-400">点击"设置规范"按钮开始配置</p>
            </div>
          ) : (
            <div className="space-y-4 pb-6">
              {/* 查看模式：仅展示写作指导类字段，其他字段已分散到人物/地点/设定/规范 */}
              {aiGuidelines.businessGoal && <div className="p-3 bg-blue-50 rounded-lg"><div className="text-xs font-semibold text-blue-700 mb-1">📋 商业目标</div><div className="text-sm text-gray-900">{aiGuidelines.businessGoal}</div></div>}
              {aiGuidelines.targetAudience && <div className="p-3 bg-blue-50 rounded-lg"><div className="text-xs font-semibold text-blue-700 mb-1">🎯 目标读者</div><div className="text-sm text-gray-900">{aiGuidelines.targetAudience}</div></div>}
              {aiGuidelines.commercialBenchmark && <div className="p-3 bg-purple-50 rounded-lg"><div className="text-xs font-semibold text-purple-700 mb-1">📊 商业对标</div><div className="text-sm text-gray-900">{aiGuidelines.commercialBenchmark}</div></div>}
              {aiGuidelines.highConcept && <div className="p-3 bg-purple-50 rounded-lg"><div className="text-xs font-semibold text-purple-700 mb-1">💡 高概念卖点</div><div className="text-sm text-gray-900">{aiGuidelines.highConcept}</div></div>}
              {aiGuidelines.coreParadox && <div className="p-3 bg-green-50 rounded-lg"><div className="text-xs font-semibold text-green-700 mb-1">🎭 核心悖论</div><div className="text-sm text-gray-900 whitespace-pre-wrap">{aiGuidelines.coreParadox}</div></div>}
              {aiGuidelines.dominantEmotion && <div className="p-3 bg-green-50 rounded-lg"><div className="text-xs font-semibold text-green-700 mb-1">❤️ 主导情感</div><div className="text-sm text-gray-900">{aiGuidelines.dominantEmotion}</div></div>}
              {aiGuidelines.coreIpSymbols && <div className="p-3 bg-amber-50 rounded-lg"><div className="text-xs font-semibold text-amber-700 mb-1">⚡ 核心IP符号</div><div className="text-sm text-gray-900">{aiGuidelines.coreIpSymbols}</div></div>}
              {aiGuidelines.protagonistArc && <div className="p-3 bg-indigo-50 rounded-lg"><div className="text-xs font-semibold text-indigo-700 mb-1">📈 主角弧光</div><div className="text-sm text-gray-900 whitespace-pre-wrap">{aiGuidelines.protagonistArc}</div></div>}
              {aiGuidelines.coreConflict && <div className="p-3 bg-red-50 rounded-lg"><div className="text-xs font-semibold text-red-700 mb-1">⚔️ 核心冲突</div><div className="text-sm text-gray-900 whitespace-pre-wrap">{aiGuidelines.coreConflict}</div></div>}
              {aiGuidelines.narrativeRhythm && <div className="p-3 bg-cyan-50 rounded-lg"><div className="text-xs font-semibold text-cyan-700 mb-1">🎵 叙事节奏</div><div className="text-sm text-gray-900">{aiGuidelines.narrativeRhythm}</div></div>}
              {aiGuidelines.writingStyle && <div className="p-3 bg-pink-50 rounded-lg"><div className="text-xs font-semibold text-pink-700 mb-1">✍️ 文笔风格</div><div className="text-sm text-gray-900">{aiGuidelines.writingStyle}</div></div>}
              {aiGuidelines.styleNotes && <div className="p-3 bg-pink-50 rounded-lg"><div className="text-xs font-semibold text-pink-700 mb-1">📝 文风注意事项</div><div className="text-sm text-gray-900">{aiGuidelines.styleNotes}</div></div>}
              {aiGuidelines.chapterLength && <div className="p-3 bg-teal-50 rounded-lg"><div className="text-xs font-semibold text-teal-700 mb-1">📏 章节长度</div><div className="text-sm text-gray-900">{aiGuidelines.chapterLength}</div></div>}
              {aiGuidelines.contentTaboos && <div className="p-3 bg-red-50 rounded-lg"><div className="text-xs font-semibold text-red-700 mb-1">🚫 内容禁忌</div><div className="text-sm text-gray-900">{aiGuidelines.contentTaboos}</div></div>}
            </div>
          )
        )}
      </div>
    );
  }
};

export default WorldManager;
