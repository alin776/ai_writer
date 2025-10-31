import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../ui/button';
import { ScrollArea } from '../ui/scroll-area';
import { Users, MapPin, Settings2, Plus, Maximize2 } from 'lucide-react';
import type { WorldData, Character, Location, Setting } from '../../types/novel';

interface WorldviewPanelProps {
  workId: string;
  worldData: WorldData;
}

export function WorldviewPanel({ workId, worldData }: WorldviewPanelProps) {
  const navigate = useNavigate();
  const [worldviewTab, setWorldviewTab] = React.useState<'characters' | 'places' | 'settings'>('characters');

  const { characters, locations, settings } = worldData;

  // 打开世界观管理页面
  const handleOpenWorldview = () => {
    navigate(`/worldview/${workId}`);
  };

  return (
    <div className="p-3 h-full overflow-y-auto custom-scrollbar">
      {/* 标签切换 */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-1.5">
          <button
            onClick={() => setWorldviewTab('characters')}
            className={`px-2.5 py-1 rounded-md text-[11px] transition-all duration-200 ${
              worldviewTab === 'characters'
                ? 'bg-zinc-900 text-white'
                : 'text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900'
            }`}
          >
            人物
          </button>
          <button
            onClick={() => setWorldviewTab('places')}
            className={`px-2.5 py-1 rounded-md text-[11px] transition-all duration-200 ${
              worldviewTab === 'places'
                ? 'bg-zinc-900 text-white'
                : 'text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900'
            }`}
          >
            地点
          </button>
          <button
            onClick={() => setWorldviewTab('settings')}
            className={`px-2.5 py-1 rounded-md text-[11px] transition-all duration-200 ${
              worldviewTab === 'settings'
                ? 'bg-zinc-900 text-white'
                : 'text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900'
            }`}
          >
            设定
          </button>
        </div>
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleOpenWorldview}
            className="h-6 w-6 p-0 text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 rounded-md transition-all"
            title="打开世界观管理"
          >
            <Maximize2 className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>

      {/* 内容区域 */}
      {worldviewTab === 'characters' && (
        <div className="space-y-1.5">
          {characters && characters.length > 0 ? (
            characters.map((char) => (
              <div
                key={char.id}
                className="group p-2.5 rounded-lg border border-zinc-100 hover:border-zinc-200 hover:bg-zinc-50/50 hover:shadow-sm transition-all duration-200 cursor-pointer"
              >
                <div className="flex items-start justify-between mb-1.5">
                  <div className="text-[13px] text-zinc-900">{char.name}</div>
                  <div className="flex items-center gap-1">
                    {char.role && (
                      <div className="text-[10px] text-zinc-400 bg-zinc-100/70 px-1.5 py-0.5 rounded">
                        {char.role}
                      </div>
                    )}
                  </div>
                </div>
                <div className="text-[11px] text-zinc-500 leading-relaxed line-clamp-2">
                  {char.description}
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-12 text-zinc-300">
              <Users className="h-10 w-10 mx-auto mb-3 opacity-30" strokeWidth={1.5} />
              <p className="text-[11px] mb-4">暂无人物信息</p>
            </div>
          )}
        </div>
      )}

      {worldviewTab === 'places' && (
        <div className="space-y-1.5">
          {locations && locations.length > 0 ? (
            locations.map((location) => (
              <div
                key={location.id}
                className="group p-2.5 rounded-lg border border-zinc-100 hover:border-zinc-200 hover:bg-zinc-50/50 hover:shadow-sm transition-all duration-200 cursor-pointer"
              >
                <div className="flex items-start justify-between mb-1.5">
                  <div className="text-[13px] text-zinc-900">{location.name}</div>
                  <div className="flex items-center gap-1">
                    {location.type && (
                      <div className="text-[10px] text-zinc-400 bg-zinc-100/70 px-1.5 py-0.5 rounded">
                        {location.type}
                      </div>
                    )}
                  </div>
                </div>
                <div className="text-[11px] text-zinc-500 leading-relaxed line-clamp-2">
                  {location.description}
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-12 text-zinc-300">
              <MapPin className="h-10 w-10 mx-auto mb-3 opacity-30" strokeWidth={1.5} />
              <p className="text-[11px] mb-4">暂无地点信息</p>
            </div>
          )}
        </div>
      )}

      {worldviewTab === 'settings' && (
        <div className="space-y-1.5">
          {settings && settings.length > 0 ? (
            settings.map((setting) => (
              <div
                key={setting.id}
                className="group p-2.5 rounded-lg border border-zinc-100 hover:border-zinc-200 hover:bg-zinc-50/50 hover:shadow-sm transition-all duration-200 cursor-pointer"
              >
                <div className="flex items-start justify-between mb-1.5">
                  <div className="text-[13px] text-zinc-900">{setting.title}</div>
                  <div className="flex items-center gap-1">
                    {setting.category && (
                      <div className="text-[10px] text-zinc-400 bg-zinc-100/70 px-1.5 py-0.5 rounded">
                        {setting.category}
                      </div>
                    )}
                  </div>
                </div>
                <div className="text-[11px] text-zinc-500 leading-relaxed line-clamp-2">
                  {setting.content}
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-12 text-zinc-300">
              <Settings2 className="h-10 w-10 mx-auto mb-3 opacity-30" strokeWidth={1.5} />
              <p className="text-[11px] mb-4">暂无世界设定</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
