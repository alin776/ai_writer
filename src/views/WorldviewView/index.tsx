/**
 * 世界观管理独立页面
 * 提供全屏的世界观构建体验
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Loader } from 'lucide-react';
import WorldManager from '@/components/editor/WorldManager';
import { DataService } from '@/services/DataService';
import { WorldData, Character, Location, Setting } from '@/types/novel';
import { useToast } from '@/hooks/useToast';

const WorldviewView: React.FC = () => {
  const { workId } = useParams<{ workId: string }>();
  const navigate = useNavigate();
  const { showToast } = useToast();

  const [loading, setLoading] = useState(true);
  const [workTitle, setWorkTitle] = useState('');
  const [worldData, setWorldData] = useState<WorldData>({
    characters: [],
    locations: [],
    settings: [],
    guidelines: {},
    aiGuidelines: {},
  });

  // 加载作品信息和世界观数据
  useEffect(() => {
    if (workId) {
      loadWorldData();
    }
  }, [workId]);

  const loadWorldData = async () => {
    if (!workId) return;

    try {
      setLoading(true);

      // 并发加载所有数据
      const [workData, characters, locations, settings, guidelines, aiGuidelines] = await Promise.all([
        DataService.getWork(workId),
        DataService.getCharacters(workId),
        DataService.getLocations(workId),
        DataService.getSettings(workId),
        DataService.getGuidelines(workId).catch(() => ({})),
        DataService.getAIGuidelines(workId).catch(() => ({})),
      ]);

      setWorkTitle(workData.title);
      setWorldData({
        characters,
        locations,
        settings,
        guidelines,
        aiGuidelines,
      });
    } catch (error) {
      console.error('加载世界观数据失败:', error);
      showToast('error', '加载失败');
    } finally {
      setLoading(false);
    }
  };

  // 角色保存
  const handleCharacterSave = async (character: Partial<Character>) => {
    if (!workId) return;

    try {
      if (character.id && !character.id.startsWith('temp-')) {
        await DataService.updateCharacter(character.id, character);
        showToast('success', '角色已更新');
      } else {
        await DataService.createCharacter({
          ...character,
          workId,
        } as any);
        showToast('success', '角色已创建');
      }
      await loadWorldData();
    } catch (error) {
      console.error('保存角色失败:', error);
      showToast('error', '保存失败');
    }
  };

  // 角色删除
  const handleCharacterDelete = async (id: string) => {
    try {
      await DataService.deleteCharacter(id);
      showToast('success', '角色已删除');
      await loadWorldData();
    } catch (error) {
      console.error('删除角色失败:', error);
      showToast('error', '删除失败');
    }
  };

  // 地点保存
  const handleLocationSave = async (location: Partial<Location>) => {
    if (!workId) return;

    try {
      if (location.id && !location.id.startsWith('temp-')) {
        await DataService.updateLocation(location.id, location);
        showToast('success', '地点已更新');
      } else {
        await DataService.createLocation({
          ...location,
          workId,
        } as any);
        showToast('success', '地点已创建');
      }
      await loadWorldData();
    } catch (error) {
      console.error('保存地点失败:', error);
      showToast('error', '保存失败');
    }
  };

  // 地点删除
  const handleLocationDelete = async (id: string) => {
    try {
      await DataService.deleteLocation(id);
      showToast('success', '地点已删除');
      await loadWorldData();
    } catch (error) {
      console.error('删除地点失败:', error);
      showToast('error', '删除失败');
    }
  };

  // 设定保存
  const handleSettingSave = async (setting: Partial<Setting>) => {
    if (!workId) return;

    try {
      if (setting.id && !setting.id.startsWith('temp-')) {
        await DataService.updateSetting(setting.id, setting);
        showToast('success', '设定已更新');
      } else {
        await DataService.createSetting({
          ...setting,
          workId,
        } as any);
        showToast('success', '设定已创建');
      }
      await loadWorldData();
    } catch (error) {
      console.error('保存设定失败:', error);
      showToast('error', '保存失败');
    }
  };

  // 设定删除
  const handleSettingDelete = async (id: string) => {
    try {
      await DataService.deleteSetting(id);
      showToast('success', '设定已删除');
      await loadWorldData();
    } catch (error) {
      console.error('删除设定失败:', error);
      showToast('error', '删除失败');
    }
  };

  // 作品规范保存
  const handleGuidelinesSave = async (guidelines: any) => {
    if (!workId) return;

    try {
      await DataService.saveGuidelines(workId, guidelines);
      showToast('success', '作品规范已保存');
      await loadWorldData();
    } catch (error) {
      console.error('保存作品规范失败:', error);
      showToast('error', '保存失败');
    }
  };

  // AI规范保存
  const handleAIGuidelinesSave = async (aiGuidelines: any) => {
    if (!workId) return;

    try {
      await DataService.saveAIGuidelines(workId, aiGuidelines);
      showToast('success', 'AI创作规范已保存');
      await loadWorldData();
    } catch (error) {
      console.error('保存AI规范失败:', error);
      showToast('error', '保存失败');
    }
  };

  // 返回上一页（更灵活）
  const handleBack = () => {
    navigate(-1);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <Loader className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-2" />
          <p className="text-sm text-gray-600">加载中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={handleBack}
            className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            返回编辑器
          </button>
          <div className="h-6 w-px bg-gray-300" />
          <div>
            <h1 className="text-lg font-semibold text-gray-900">{workTitle}</h1>
            <p className="text-xs text-gray-500">世界观管理</p>
          </div>
        </div>
        <div className="text-xs text-gray-500">
          {worldData.characters.length} 个角色 · {worldData.locations.length} 个地点 · {worldData.settings.length} 个设定
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        <WorldManager
          worldData={worldData}
          onCharacterSave={handleCharacterSave}
          onCharacterDelete={handleCharacterDelete}
          onLocationSave={handleLocationSave}
          onLocationDelete={handleLocationDelete}
          onSettingSave={handleSettingSave}
          onSettingDelete={handleSettingDelete}
          onGuidelinesSave={handleGuidelinesSave}
          onAIGuidelinesSave={handleAIGuidelinesSave}
        />
      </main>
    </div>
  );
};

export default WorldviewView;
