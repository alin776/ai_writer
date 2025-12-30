import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Button } from '../ui/button';
import { ScrollArea } from '../ui/scroll-area';
import { Users, MapPin, Settings2, Plus, Maximize2, RefreshCw } from 'lucide-react';
import type { WorldData, Character, Location, Setting, WorldviewChanges } from '../../types/novel';
import { WorldviewSyncDialog } from '../worldview/WorldviewSyncDialog';
import { DataService } from '@/services/DataService';
import { useToast } from '@/hooks/useToast';

interface WorldviewPanelProps {
  workId: string;
  worldData: WorldData;
  initialTab?: 'characters' | 'places' | 'settings';
  targetItemId?: string;
  onTargetItemScrolled?: () => void;
  onWorldDataUpdate?: () => void;  // 世界观数据更新后的回调
}

export function WorldviewPanel({ workId, worldData, initialTab, targetItemId, onTargetItemScrolled, onWorldDataUpdate }: WorldviewPanelProps) {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { success: showSuccess, error: showError } = useToast();
  const [worldviewTab, setWorldviewTab] = React.useState<'characters' | 'places' | 'settings'>(initialTab || 'characters');
  const [highlightedItemId, setHighlightedItemId] = React.useState<string | undefined>(undefined);

  // 世界观同步相关状态
  const [syncDialogOpen, setSyncDialogOpen] = React.useState(false);
  const [syncChanges, setSyncChanges] = React.useState<WorldviewChanges | null>(null);
  const [syncLoading, setSyncLoading] = React.useState(false);
  const [syncApplying, setSyncApplying] = React.useState(false);
  const [syncError, setSyncError] = React.useState<string | null>(null);
  const [syncMode, setSyncMode] = React.useState<'extract' | 'scan'>('scan');

  // 当 initialTab 变化时更新当前 tab
  React.useEffect(() => {
    if (initialTab) {
      setWorldviewTab(initialTab);
    }
  }, [initialTab]);

  // 滚动到目标项并高亮
  React.useEffect(() => {
    if (targetItemId) {
      // 延迟执行，确保 DOM 已渲染
      const timer = setTimeout(() => {
        const element = document.getElementById(`worldview-item-${targetItemId}`);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          setHighlightedItemId(targetItemId);
          // 3秒后移除高亮
          setTimeout(() => {
            setHighlightedItemId(undefined);
          }, 3000);
        }
        // 通知父组件滚动完成
        onTargetItemScrolled?.();
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [targetItemId, onTargetItemScrolled]);

  const { characters, locations, settings } = worldData;

  // 打开世界观管理页面
  const handleOpenWorldview = () => {
    navigate(`/worldview/${workId}`);
  };

  // 打开世界观同步对话框（批量扫描模式）
  const handleOpenSyncDialog = async () => {
    setSyncMode('scan');
    setSyncDialogOpen(true);
    setSyncLoading(true);
    setSyncError(null);
    setSyncChanges(null);

    try {
      const changes = await DataService.scanWorldviewChanges(workId, 1, undefined, 20);
      setSyncChanges(changes);
    } catch (err: any) {
      console.error('扫描世界观变化失败:', err);
      setSyncError(err.message || '扫描失败，请稍后重试');
    } finally {
      setSyncLoading(false);
    }
  };

  // 应用世界观变化
  const handleApplyChanges = async (selectedItems: {
    newCharacters: string[];
    newLocations: string[];
    newSettings: string[];
    relationshipChanges: string[];
  }) => {
    if (!syncChanges) return;

    setSyncApplying(true);
    try {
      const result = await DataService.applyWorldviewChanges(workId, syncChanges, {
        new_characters: selectedItems.newCharacters,
        new_locations: selectedItems.newLocations,
        new_settings: selectedItems.newSettings,
        relationship_changes: selectedItems.relationshipChanges,
      });

      // 显示成功提示
      const totalCreated = result.charactersCreated + result.locationsCreated + result.settingsCreated + (result.relationshipsCreated || 0);
      const parts = [`人物: ${result.charactersCreated}`, `地点: ${result.locationsCreated}`, `设定: ${result.settingsCreated}`];
      if (result.relationshipsCreated) {
        parts.push(`关系: ${result.relationshipsCreated}`);
      }
      showSuccess(
        `成功同步 ${totalCreated} 个世界观卡片`,
        parts.join(', ')
      );

      // 关闭对话框
      setSyncDialogOpen(false);

      // 通知父组件刷新世界观数据
      onWorldDataUpdate?.();
    } catch (err: any) {
      console.error('应用世界观变化失败:', err);
      showError('应用失败', err.message || '请稍后重试');
    } finally {
      setSyncApplying(false);
    }
  };

  // 关闭同步对话框
  const handleCloseSyncDialog = () => {
    setSyncDialogOpen(false);
    setSyncChanges(null);
    setSyncError(null);
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
                ? 'bg-zinc-900 text-white dark:bg-slate-200 dark:text-slate-900'
                : 'text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900 dark:text-slate-400 dark:hover:bg-slate-700 dark:hover:text-slate-100'
            }`}
          >
            {t('worldview.tabs.characters')}
          </button>
          <button
            onClick={() => setWorldviewTab('places')}
            className={`px-2.5 py-1 rounded-md text-[11px] transition-all duration-200 ${
              worldviewTab === 'places'
                ? 'bg-zinc-900 text-white dark:bg-slate-200 dark:text-slate-900'
                : 'text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900 dark:text-slate-400 dark:hover:bg-slate-700 dark:hover:text-slate-100'
            }`}
          >
            {t('worldview.tabs.locations')}
          </button>
          <button
            onClick={() => setWorldviewTab('settings')}
            className={`px-2.5 py-1 rounded-md text-[11px] transition-all duration-200 ${
              worldviewTab === 'settings'
                ? 'bg-zinc-900 text-white dark:bg-slate-200 dark:text-slate-900'
                : 'text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900 dark:text-slate-400 dark:hover:bg-slate-700 dark:hover:text-slate-100'
            }`}
          >
            {t('worldview.tabs.settings')}
          </button>
        </div>
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleOpenSyncDialog}
            className="h-6 w-6 p-0 text-zinc-400 hover:text-blue-600 hover:bg-blue-50 dark:text-slate-400 dark:hover:text-blue-400 dark:hover:bg-blue-900/30 rounded-md transition-all"
            title="从章节同步世界观"
          >
            <RefreshCw className="h-3.5 w-3.5" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleOpenWorldview}
            className="h-6 w-6 p-0 text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-700 rounded-md transition-all"
            title={t('worldview.actions.openWorldview')}
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
                id={`worldview-item-${char.id}`}
                className={`group p-2.5 rounded-lg border transition-all duration-200 cursor-pointer ${
                  highlightedItemId === char.id
                    ? 'border-blue-400 bg-blue-50 dark:border-blue-500 dark:bg-blue-900/30 ring-2 ring-blue-400/50'
                    : 'border-zinc-100 hover:border-zinc-200 hover:bg-zinc-50/50 hover:shadow-sm dark:border-slate-700 dark:hover:border-slate-600 dark:hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-start justify-between mb-1.5">
                  <div className="text-[13px] text-zinc-900 dark:text-slate-100">{char.name}</div>
                  <div className="flex items-center gap-1">
                    {char.role && (
                      <div className="text-[10px] text-zinc-400 bg-zinc-100/70 dark:text-slate-400 dark:bg-slate-700/70 px-1.5 py-0.5 rounded">
                        {char.role}
                      </div>
                    )}
                  </div>
                </div>
                <div className="text-[11px] text-zinc-500 dark:text-slate-400 leading-relaxed line-clamp-2">
                  {char.description}
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-12 text-zinc-300">
              <Users className="h-10 w-10 mx-auto mb-3 opacity-30" strokeWidth={1.5} />
              <p className="text-[11px] mb-4">{t('worldview.empty.characters')}</p>
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
                id={`worldview-item-${location.id}`}
                className={`group p-2.5 rounded-lg border transition-all duration-200 cursor-pointer ${
                  highlightedItemId === location.id
                    ? 'border-blue-400 bg-blue-50 dark:border-blue-500 dark:bg-blue-900/30 ring-2 ring-blue-400/50'
                    : 'border-zinc-100 hover:border-zinc-200 hover:bg-zinc-50/50 hover:shadow-sm dark:border-slate-700 dark:hover:border-slate-600 dark:hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-start justify-between mb-1.5">
                  <div className="text-[13px] text-zinc-900 dark:text-slate-100">{location.name}</div>
                  <div className="flex items-center gap-1">
                    {location.type && (
                      <div className="text-[10px] text-zinc-400 bg-zinc-100/70 dark:text-slate-400 dark:bg-slate-700/70 px-1.5 py-0.5 rounded">
                        {location.type}
                      </div>
                    )}
                  </div>
                </div>
                <div className="text-[11px] text-zinc-500 dark:text-slate-400 leading-relaxed line-clamp-2">
                  {location.description}
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-12 text-zinc-300">
              <MapPin className="h-10 w-10 mx-auto mb-3 opacity-30" strokeWidth={1.5} />
              <p className="text-[11px] mb-4">{t('worldview.empty.locations')}</p>
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
                id={`worldview-item-${setting.id}`}
                className={`group p-2.5 rounded-lg border transition-all duration-200 cursor-pointer ${
                  highlightedItemId === setting.id
                    ? 'border-blue-400 bg-blue-50 dark:border-blue-500 dark:bg-blue-900/30 ring-2 ring-blue-400/50'
                    : 'border-zinc-100 hover:border-zinc-200 hover:bg-zinc-50/50 hover:shadow-sm dark:border-slate-700 dark:hover:border-slate-600 dark:hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-start justify-between mb-1.5">
                  <div className="text-[13px] text-zinc-900 dark:text-slate-100">{setting.title}</div>
                  <div className="flex items-center gap-1">
                    {setting.category && (
                      <div className="text-[10px] text-zinc-400 bg-zinc-100/70 dark:text-slate-400 dark:bg-slate-700/70 px-1.5 py-0.5 rounded">
                        {setting.category}
                      </div>
                    )}
                  </div>
                </div>
                <div className="text-[11px] text-zinc-500 dark:text-slate-400 leading-relaxed line-clamp-2">
                  {setting.content}
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-12 text-zinc-300">
              <Settings2 className="h-10 w-10 mx-auto mb-3 opacity-30" strokeWidth={1.5} />
              <p className="text-[11px] mb-4">{t('worldview.empty.settings')}</p>
            </div>
          )}
        </div>
      )}

      {/* 世界观同步对话框 */}
      <WorldviewSyncDialog
        isOpen={syncDialogOpen}
        onClose={handleCloseSyncDialog}
        changes={syncChanges}
        isLoading={syncLoading}
        isApplying={syncApplying}
        error={syncError}
        onApply={handleApplyChanges}
        mode={syncMode}
      />
    </div>
  );
}
