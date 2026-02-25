import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Button } from '../ui/button';
import { ScrollArea } from '../ui/scroll-area';
import { Progress } from '../ui/progress';
import { Users, MapPin, Settings2, Plus, Maximize2, RefreshCw, FileText } from 'lucide-react';
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
  onBeforeSyncKnowledgeToWorldview?: () => Promise<void> | void;
}

export function WorldviewPanel({
  workId,
  worldData,
  initialTab,
  targetItemId,
  onTargetItemScrolled,
  onWorldDataUpdate,
  onBeforeSyncKnowledgeToWorldview,
}: WorldviewPanelProps) {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { success: showSuccess, info: showInfo, warning: showWarning, error: showError } = useToast();
  const [worldviewTab, setWorldviewTab] = React.useState<'characters' | 'places' | 'settings'>(initialTab || 'characters');
  const [highlightedItemId, setHighlightedItemId] = React.useState<string | undefined>(undefined);

  // 世界观同步相关状态
  const [syncDialogOpen, setSyncDialogOpen] = React.useState(false);
  const [syncChanges, setSyncChanges] = React.useState<WorldviewChanges | null>(null);
  const [syncLoading, setSyncLoading] = React.useState(false);
  const [syncApplying, setSyncApplying] = React.useState(false);
  const [syncError, setSyncError] = React.useState<string | null>(null);
  const [syncMode, setSyncMode] = React.useState<'extract' | 'scan'>('scan');
  const [syncingKnowledge, setSyncingKnowledge] = React.useState(false);
  const [syncingKnowledgeToWorldview, setSyncingKnowledgeToWorldview] = React.useState(false);
  const [syncProgress, setSyncProgress] = React.useState<{
    visible: boolean;
    value: number;
    title: string;
    detail?: string;
    tone: 'running' | 'success' | 'warning' | 'error';
  }>({
    visible: false,
    value: 0,
    title: '',
    detail: '',
    tone: 'running',
  });
  const progressTimerRef = React.useRef<ReturnType<typeof setInterval> | null>(null);
  const progressCloseTimerRef = React.useRef<ReturnType<typeof setTimeout> | null>(null);

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

  const clearProgressTimers = React.useCallback(() => {
    if (progressTimerRef.current) {
      clearInterval(progressTimerRef.current);
      progressTimerRef.current = null;
    }
    if (progressCloseTimerRef.current) {
      clearTimeout(progressCloseTimerRef.current);
      progressCloseTimerRef.current = null;
    }
  }, []);

  React.useEffect(() => {
    return () => clearProgressTimers();
  }, [clearProgressTimers]);

  const startSyncProgress = React.useCallback((title: string, detail: string) => {
    clearProgressTimers();
    setSyncProgress({
      visible: true,
      value: 8,
      title,
      detail,
      tone: 'running',
    });
    progressTimerRef.current = setInterval(() => {
      setSyncProgress((prev) => {
        if (!prev.visible || prev.tone !== 'running') return prev;
        const next = prev.value < 40 ? prev.value + 8 : prev.value < 70 ? prev.value + 5 : prev.value + 3;
        return { ...prev, value: Math.min(next, 90) };
      });
    }, 280);
  }, [clearProgressTimers]);

  const finishSyncProgress = React.useCallback((state: 'success' | 'warning' | 'error', detail: string) => {
    clearProgressTimers();
    setSyncProgress({
      visible: true,
      value: state === 'warning' ? 96 : 100,
      title:
        state === 'success'
          ? '同步完成'
          : state === 'warning'
            ? '同步完成（未发现变化）'
            : '同步失败',
      detail,
      tone: state,
    });
    progressCloseTimerRef.current = setTimeout(() => {
      setSyncProgress((prev) => ({ ...prev, visible: false }));
    }, state === 'error' ? 2200 : 1600);
  }, [clearProgressTimers]);

  // 手动将卡片同步到 knowledge/*.md
  const handleSyncCardsToKnowledge = async () => {
    if (syncingKnowledge) return;
    setSyncingKnowledge(true);
    startSyncProgress('正在同步到知识库...', '正在生成并写入 knowledge/*.md');
    try {
      const result = await DataService.syncWorldviewCardsToKnowledge(workId);
      const updatedFiles = result.updatedFiles || [];
      const updatedCount = updatedFiles.length;
      const message =
        updatedCount > 0
          ? `已更新 ${updatedCount} 个知识库文件`
          : '知识库文件已是最新状态';
      showSuccess(
        '卡片已同步到知识库',
        `${message}（人物:${result.charactersCount} 地点:${result.locationsCount} 设定:${result.settingsCount}）`
      );
      // 触发父层刷新（世界观数据 + 文件树）
      onWorldDataUpdate?.();
      finishSyncProgress('success', message);
    } catch (err: any) {
      console.error('卡片同步到知识库失败:', err);
      const errorMsg = err?.message || '请稍后重试';
      showError('同步失败', errorMsg);
      finishSyncProgress('error', errorMsg);
    } finally {
      setSyncingKnowledge(false);
    }
  };

  // Sync the currently relevant knowledge file into worldview cards.
  const handleSyncFileToWorldview = async () => {
    if (syncingKnowledgeToWorldview) return;

    const targetPath = worldviewTab === 'characters'
      ? 'knowledge/characters.md'
      : 'knowledge/worldview.md';
    const targetLabel = worldviewTab === 'characters' ? '\u4eba\u7269\u6587\u4ef6' : '\u4e16\u754c\u89c2\u6587\u4ef6';

    setSyncingKnowledgeToWorldview(true);
    startSyncProgress('\u6b63\u5728\u4ece\u5bf9\u5e94\u6587\u4ef6\u540c\u6b65\u5230\u4e16\u754c\u89c2...', `\u6b63\u5728\u89e3\u6790 ${targetPath} \u5e76\u66f4\u65b0\u5361\u7247`);
    try {
      await onBeforeSyncKnowledgeToWorldview?.();

      const result = await DataService.syncKnowledgeToWorldviewCards(workId, [targetPath]);
      const createdCount = (result.created.characters || 0) + (result.created.locations || 0) + (result.created.settings || 0);
      const updatedCount = (result.updated.characters || 0) + (result.updated.locations || 0) + (result.updated.settings || 0);
      const deletedCount = (result.deleted.characters || 0) + (result.deleted.locations || 0) + (result.deleted.settings || 0);
      const changedCount = createdCount + updatedCount + deletedCount;

      const parsedCounts = result.parsedCounts || { characters: 0, locations: 0, settings: 0 };
      const parsedTotal = (parsedCounts.characters || 0) + (parsedCounts.locations || 0) + (parsedCounts.settings || 0);
      const missingFiles = result.missingFiles || [];
      const message = result.hasDbChanges
        ? `\u65b0\u589e ${createdCount} / \u66f4\u65b0 ${updatedCount} / \u5220\u9664 ${deletedCount}`
        : `\u5df2\u68c0\u67e5 ${parsedTotal} \u6761\uff0c\u5f53\u524d\u5361\u7247\u5df2\u662f\u6700\u65b0`;

      if (result.hasDbChanges) {
        showSuccess(
          `${targetLabel}\u5df2\u540c\u6b65\u5230\u4e16\u754c\u89c2`,
          `${targetPath} - ${message}`
        );
        finishSyncProgress('success', `\u5df2\u5e94\u7528 ${changedCount} \u9879\u53d8\u5316`);
      } else if (missingFiles.length > 0) {
        showWarning(
          `${targetLabel}\u540c\u6b65\u5b8c\u6210\uff0c\u4f46\u7f3a\u5c11\u53ef\u8bfb\u53d6\u6587\u4ef6`,
          `\u672a\u627e\u5230\uff1a${missingFiles.join(', ')}`
        );
        finishSyncProgress('warning', `\u7f3a\u5c11\u6587\u4ef6\uff1a${missingFiles.join(', ')}`);
      } else if (parsedTotal > 0) {
        showInfo(
          `${targetLabel}\u540c\u6b65\u5b8c\u6210\uff08\u65e0\u6570\u636e\u5e93\u53d8\u66f4\uff09`,
          `${targetPath} - ${message}`
        );
        finishSyncProgress('success', message);
      } else {
        showWarning(
          `${targetLabel}\u5df2\u6267\u884c\u540c\u6b65\uff0c\u4f46\u672a\u8bc6\u522b\u5230\u53ef\u89e3\u6790\u6761\u76ee`,
          `${targetPath} - \u8bf7\u786e\u8ba4\u6587\u4ef6\u5df2\u4fdd\u5b58\uff0c\u5e76\u4f7f\u7528 heading + \u5b57\u6bb5\uff08\u5982\uff1a\u89d2\u8272/\u63cf\u8ff0\uff09\u683c\u5f0f`
        );
        finishSyncProgress('warning', '\u672a\u8bc6\u522b\u5230\u53ef\u89e3\u6790\u6761\u76ee');
      }

      onWorldDataUpdate?.();
    } catch (err: any) {
      console.error('\u6587\u4ef6\u540c\u6b65\u5230\u4e16\u754c\u89c2\u5931\u8d25:', err);
      const errorMsg = err?.message || '\u8bf7\u7a0d\u540e\u91cd\u8bd5';
      showError('\u540c\u6b65\u5931\u8d25', errorMsg);
      finishSyncProgress('error', errorMsg);
    } finally {
      setSyncingKnowledgeToWorldview(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* 固定的标签切换 */}
      <div className="flex-shrink-0 px-3 pt-3 pb-2 bg-white dark:bg-slate-900">
        <div className="flex items-center justify-between">
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
              onClick={handleSyncFileToWorldview}
              disabled={syncingKnowledgeToWorldview}
              className="h-6 w-6 p-0 text-zinc-400 hover:text-blue-600 hover:bg-blue-50 dark:text-slate-400 dark:hover:text-blue-400 dark:hover:bg-blue-900/30 rounded-md transition-all disabled:opacity-60"
              title={worldviewTab === 'characters' ? '从人物文件同步到世界观' : '从世界观文件同步到世界观'}
            >
              <RefreshCw className={`h-3.5 w-3.5 ${syncingKnowledgeToWorldview ? 'animate-spin' : ''}`} />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleSyncCardsToKnowledge}
              disabled={syncingKnowledge}
              className="h-6 w-6 p-0 text-zinc-400 hover:text-emerald-600 hover:bg-emerald-50 dark:text-slate-400 dark:hover:text-emerald-400 dark:hover:bg-emerald-900/30 rounded-md transition-all disabled:opacity-60"
              title="将卡片同步到知识库文件"
            >
              <FileText className={`h-3.5 w-3.5 ${syncingKnowledge ? 'animate-pulse' : ''}`} />
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
      </div>

      {/* 可滚动的内容区域 */}
      <div className="flex-1 overflow-y-auto custom-scrollbar px-3 pb-3">
        {worldviewTab === 'characters' && (
        <div className="space-y-1.5">
          {characters && characters.length > 0 ? (
            characters.map((char) => (
              <div
                key={char.id}
                id={`worldview-item-${char.id}`}
                onClick={() => navigate(`/worldview/${workId}?type=character&id=${char.id}`)}
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
                onClick={() => navigate(`/worldview/${workId}?type=location&id=${location.id}`)}
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
                onClick={() => navigate(`/worldview/${workId}?type=setting&id=${setting.id}`)}
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
      </div>

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

      {syncProgress.visible && (
        <div className="fixed bottom-4 right-4 z-[10010] w-80 rounded-lg border border-zinc-200 bg-white/95 p-3 shadow-lg backdrop-blur-sm dark:border-slate-700 dark:bg-slate-900/95">
          <div className="mb-2 flex items-center justify-between">
            <span className="text-xs font-medium text-zinc-900 dark:text-slate-100">{syncProgress.title}</span>
            <span className="text-[11px] text-zinc-500 dark:text-slate-400">{Math.round(syncProgress.value)}%</span>
          </div>
          <Progress
            value={syncProgress.value}
            className={`h-1.5 bg-zinc-200 dark:bg-slate-700 ${
              syncProgress.tone === 'error'
                ? '[&>div]:bg-red-500'
                : syncProgress.tone === 'warning'
                  ? '[&>div]:bg-amber-500'
                  : syncProgress.tone === 'success'
                    ? '[&>div]:bg-emerald-500'
                    : '[&>div]:bg-blue-500'
            }`}
          />
          {syncProgress.detail && (
            <div className="mt-2 text-[11px] text-zinc-500 dark:text-slate-400">
              {syncProgress.detail}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
