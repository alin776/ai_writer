/**
 * 世界观侧边栏 - 简化版
 * 用于编辑器页面右侧，提供快速查看功能
 * 点击"打开世界观管理"可进入全屏编辑页面
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Users, MapPin, BookOpen, ExternalLink } from 'lucide-react';
import { WorldData } from '@/types/novel';

type TabType = 'characters' | 'locations' | 'settings';

interface WorldviewSidebarProps {
  workId: string;
  worldData: WorldData;
}

const WorldviewSidebar: React.FC<WorldviewSidebarProps> = ({ workId, worldData }) => {
  const [activeTab, setActiveTab] = useState<TabType>('characters');
  const navigate = useNavigate();
  const { t } = useTranslation();

  // 跳转到世界观管理页面
  const handleOpenWorldview = () => {
    navigate(`/worldview/${workId}`);
  };

  // 渲染角色列表（只读）
  const renderCharacters = () => {
    const characters = worldData.characters || [];

    if (characters.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center py-12 text-gray-400">
          <Users className="w-12 h-12 mb-2" />
          <p className="text-sm">{t('worldview.empty.noCharacters')}</p>
        </div>
      );
    }

    return (
      <div className="space-y-2">
        {characters.map((character) => (
          <div
            key={character.id}
            className="p-3 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-all cursor-pointer"
            onClick={handleOpenWorldview}
          >
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
            </div>
          </div>
        ))}
      </div>
    );
  };

  // 渲染地点列表（只读）
  const renderLocations = () => {
    const locations = worldData.locations || [];

    if (locations.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center py-12 text-gray-400">
          <MapPin className="w-12 h-12 mb-2" />
          <p className="text-sm">{t('worldview.empty.noLocations')}</p>
        </div>
      );
    }

    return (
      <div className="space-y-2">
        {locations.map((location) => (
          <div
            key={location.id}
            className="p-3 rounded-lg border border-gray-200 hover:border-green-300 hover:bg-green-50 transition-all cursor-pointer"
            onClick={handleOpenWorldview}
          >
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
            </div>
          </div>
        ))}
      </div>
    );
  };

  // 渲染设定列表（只读）
  const renderSettings = () => {
    const settings = worldData.settings || [];

    if (settings.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center py-12 text-gray-400">
          <BookOpen className="w-12 h-12 mb-2" />
          <p className="text-sm">{t('worldview.empty.noSettings')}</p>
        </div>
      );
    }

    return (
      <div className="space-y-2">
        {settings.map((setting) => (
          <div
            key={setting.id}
            className="p-3 rounded-lg border border-gray-200 hover:border-orange-300 hover:bg-orange-50 transition-all cursor-pointer"
            onClick={handleOpenWorldview}
          >
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
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="h-full flex flex-col bg-white border-l border-gray-200">
      {/* 打开世界观管理按钮 */}
      <div className="p-3 border-b border-gray-200">
        <button
          onClick={handleOpenWorldview}
          className="w-full px-4 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
        >
          <ExternalLink className="w-4 h-4" />
          {t('worldview.actions.openWorldview')}
        </button>
      </div>

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
          {t('worldview.tabs.characters')}
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
          {t('worldview.tabs.locations')}
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
          {t('worldview.tabs.settings')}
        </button>
      </div>

      {/* 内容区域（只读列表） */}
      <div className="flex-1 overflow-y-auto p-3">
        {/* 提示信息 */}
        <div className="mb-3 p-2 bg-blue-50 border border-blue-200 rounded text-xs text-blue-700">
          💡 {t('worldview.actions.clickToEdit')}
        </div>

        {/* 列表 */}
        {activeTab === 'characters' && renderCharacters()}
        {activeTab === 'locations' && renderLocations()}
        {activeTab === 'settings' && renderSettings()}
      </div>

      {/* 底部统计 */}
      <div className="p-3 border-t border-gray-200 bg-gray-50">
        <div className="flex items-center justify-around text-xs text-gray-600">
          <div className="flex items-center gap-1">
            <Users className="w-3.5 h-3.5" />
            <span>{worldData.characters?.length || 0}</span>
          </div>
          <div className="flex items-center gap-1">
            <MapPin className="w-3.5 h-3.5" />
            <span>{worldData.locations?.length || 0}</span>
          </div>
          <div className="flex items-center gap-1">
            <BookOpen className="w-3.5 h-3.5" />
            <span>{worldData.settings?.length || 0}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WorldviewSidebar;
