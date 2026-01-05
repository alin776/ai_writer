/**
 * 世界观同步对话框
 * 用于展示从章节提取的世界观变化，让用户确认后应用到卡片
 */
import React from 'react';
import { useTranslation } from 'react-i18next';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '../ui/dialog';
import { Button } from '../ui/button';
import { Checkbox } from '../ui/checkbox';
import { Badge } from '../ui/badge';
import { Users, MapPin, Settings2, GitBranch, Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';
import type { WorldviewChanges, ApplyChangesResult } from '@/types/novel';

interface WorldviewSyncDialogProps {
  isOpen: boolean;
  onClose: () => void;
  changes: WorldviewChanges | null;
  isLoading: boolean;
  isApplying: boolean;
  error: string | null;
  onApply: (selectedItems: SelectedItems) => Promise<void>;
  mode: 'extract' | 'scan';  // 提取模式 or 扫描模式
}

interface SelectedItems {
  newCharacters: string[];
  newLocations: string[];
  newSettings: string[];
  relationshipChanges: string[];  // 格式: "from->to"
}

export function WorldviewSyncDialog({
  isOpen,
  onClose,
  changes,
  isLoading,
  isApplying,
  error,
  onApply,
  mode,
}: WorldviewSyncDialogProps) {
  const { t } = useTranslation();

  // 选中状态
  const [selectedCharacters, setSelectedCharacters] = React.useState<Set<string>>(new Set());
  const [selectedLocations, setSelectedLocations] = React.useState<Set<string>>(new Set());
  const [selectedSettings, setSelectedSettings] = React.useState<Set<string>>(new Set());
  const [selectedRelationships, setSelectedRelationships] = React.useState<Set<string>>(new Set());

  // 当 changes 变化时，默认全选
  React.useEffect(() => {
    if (changes) {
      console.log('[WorldviewSyncDialog] changes received:', changes);
      const newChars = changes.newCharacters || [];
      const newLocs = changes.newLocations || [];
      const newSets = changes.newSettings || [];
      const relChanges = changes.relationshipChanges || [];
      setSelectedCharacters(new Set(newChars.map(c => c.name)));
      setSelectedLocations(new Set(newLocs.map(l => l.name)));
      setSelectedSettings(new Set(newSets.map(s => s.title)));
      setSelectedRelationships(new Set(relChanges.map(r => `${r.from}->${r.to}`)));
    }
  }, [changes]);

  const toggleCharacter = (name: string) => {
    setSelectedCharacters(prev => {
      const next = new Set(prev);
      if (next.has(name)) {
        next.delete(name);
      } else {
        next.add(name);
      }
      return next;
    });
  };

  const toggleLocation = (name: string) => {
    setSelectedLocations(prev => {
      const next = new Set(prev);
      if (next.has(name)) {
        next.delete(name);
      } else {
        next.add(name);
      }
      return next;
    });
  };

  const toggleSetting = (title: string) => {
    setSelectedSettings(prev => {
      const next = new Set(prev);
      if (next.has(title)) {
        next.delete(title);
      } else {
        next.add(title);
      }
      return next;
    });
  };

  const toggleRelationship = (key: string) => {
    setSelectedRelationships(prev => {
      const next = new Set(prev);
      if (next.has(key)) {
        next.delete(key);
      } else {
        next.add(key);
      }
      return next;
    });
  };

  const handleApply = async () => {
    await onApply({
      newCharacters: Array.from(selectedCharacters),
      newLocations: Array.from(selectedLocations),
      newSettings: Array.from(selectedSettings),
      relationshipChanges: Array.from(selectedRelationships),
    });
  };

  const hasChanges = changes && (
    (changes.newCharacters?.length || 0) > 0 ||
    (changes.newLocations?.length || 0) > 0 ||
    (changes.newSettings?.length || 0) > 0 ||
    (changes.updatedCharacters?.length || 0) > 0 ||
    (changes.relationshipChanges?.length || 0) > 0
  );

  const hasSelectedItems = selectedCharacters.size > 0 || selectedLocations.size > 0 || selectedSettings.size > 0 || selectedRelationships.size > 0;

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-w-2xl max-h-[85vh] flex flex-col overflow-hidden">
        <DialogHeader className="flex-shrink-0">
          <DialogTitle className="flex items-center gap-2">
            <GitBranch className="h-5 w-5" />
            {mode === 'extract' ? '章节世界观提取' : '批量扫描结果'}
          </DialogTitle>
          <DialogDescription>
            {mode === 'extract'
              ? 'AI 已分析章节内容，发现以下世界观变化。请确认要同步到卡片的项目。'
              : `AI 已扫描 ${changes?.scannedChapters || 0} 个章节，发现以下世界观变化。`
            }
          </DialogDescription>
        </DialogHeader>

        <div className="flex-1 min-h-0 overflow-y-auto pr-2">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-blue-500 mb-4" />
              <p className="text-sm text-zinc-500">
                {mode === 'extract' ? '正在分析章节内容...' : '正在扫描章节...'}
              </p>
            </div>
          ) : error ? (
            <div className="flex flex-col items-center justify-center py-12">
              <AlertCircle className="h-8 w-8 text-red-500 mb-4" />
              <p className="text-sm text-red-500">{error}</p>
            </div>
          ) : !hasChanges ? (
            <div className="flex flex-col items-center justify-center py-12">
              <CheckCircle2 className="h-8 w-8 text-green-500 mb-4" />
              <p className="text-sm text-zinc-500">未发现新的世界观变化</p>
              <p className="text-xs text-zinc-400 mt-1">当前章节的内容与已有世界观卡片一致</p>
            </div>
          ) : (
            <div className="space-y-6 py-2">
              {/* 新增人物 */}
              {changes && (changes.newCharacters?.length || 0) > 0 && (
                <div>
                  <h4 className="flex items-center gap-2 text-sm font-medium mb-3">
                    <Users className="h-4 w-4 text-blue-500" />
                    新增人物
                    <Badge variant="secondary" className="ml-1">
                      {changes.newCharacters.length}
                    </Badge>
                  </h4>
                  <div className="space-y-2">
                    {changes.newCharacters.map((char) => (
                      <div
                        key={char.name}
                        className="flex items-start gap-3 p-3 rounded-lg border border-zinc-100 dark:border-slate-700 hover:bg-zinc-50 dark:hover:bg-slate-800 transition-colors"
                      >
                        <Checkbox
                          checked={selectedCharacters.has(char.name)}
                          onCheckedChange={() => toggleCharacter(char.name)}
                        />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="font-medium text-sm">{char.name}</span>
                            {char.role && (
                              <Badge variant="outline" className="text-xs">
                                {char.role}
                              </Badge>
                            )}
                            {char.importance && (
                              <Badge
                                variant={char.importance === '高' ? 'default' : 'secondary'}
                                className="text-xs"
                              >
                                {char.importance}
                              </Badge>
                            )}
                          </div>
                          {char.description && (
                            <p className="text-xs text-zinc-500 dark:text-slate-400 mt-1 line-clamp-2">
                              {char.description}
                            </p>
                          )}
                          {char.firstAppearance && (
                            <p className="text-xs text-zinc-400 dark:text-slate-500 mt-1">
                              首次出现：{char.firstAppearance}
                            </p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 人物变化 */}
              {changes && (changes.updatedCharacters?.length || 0) > 0 && (
                <div>
                  <h4 className="flex items-center gap-2 text-sm font-medium mb-3">
                    <Users className="h-4 w-4 text-orange-500" />
                    人物变化
                    <Badge variant="secondary" className="ml-1">
                      {changes.updatedCharacters.length}
                    </Badge>
                  </h4>
                  <div className="space-y-2">
                    {changes.updatedCharacters.map((char, idx) => (
                      <div
                        key={`${char.name}-${idx}`}
                        className="p-3 rounded-lg border border-orange-100 dark:border-orange-900/30 bg-orange-50/50 dark:bg-orange-900/10"
                      >
                        <div className="font-medium text-sm">{char.name}</div>
                        <p className="text-xs text-zinc-600 dark:text-slate-400 mt-1">
                          {char.changes}
                        </p>
                      </div>
                    ))}
                  </div>
                  <p className="text-xs text-zinc-400 mt-2">
                    * 人物变化需要手动更新卡片内容
                  </p>
                </div>
              )}

              {/* 新增地点 */}
              {changes && (changes.newLocations?.length || 0) > 0 && (
                <div>
                  <h4 className="flex items-center gap-2 text-sm font-medium mb-3">
                    <MapPin className="h-4 w-4 text-green-500" />
                    新增地点
                    <Badge variant="secondary" className="ml-1">
                      {changes.newLocations.length}
                    </Badge>
                  </h4>
                  <div className="space-y-2">
                    {changes.newLocations.map((loc) => (
                      <div
                        key={loc.name}
                        className="flex items-start gap-3 p-3 rounded-lg border border-zinc-100 dark:border-slate-700 hover:bg-zinc-50 dark:hover:bg-slate-800 transition-colors"
                      >
                        <Checkbox
                          checked={selectedLocations.has(loc.name)}
                          onCheckedChange={() => toggleLocation(loc.name)}
                        />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="font-medium text-sm">{loc.name}</span>
                            {loc.type && (
                              <Badge variant="outline" className="text-xs">
                                {loc.type}
                              </Badge>
                            )}
                          </div>
                          {loc.description && (
                            <p className="text-xs text-zinc-500 dark:text-slate-400 mt-1 line-clamp-2">
                              {loc.description}
                            </p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 新增设定 */}
              {changes && (changes.newSettings?.length || 0) > 0 && (
                <div>
                  <h4 className="flex items-center gap-2 text-sm font-medium mb-3">
                    <Settings2 className="h-4 w-4 text-purple-500" />
                    新增设定
                    <Badge variant="secondary" className="ml-1">
                      {changes.newSettings.length}
                    </Badge>
                  </h4>
                  <div className="space-y-2">
                    {changes.newSettings.map((setting) => (
                      <div
                        key={setting.title}
                        className="flex items-start gap-3 p-3 rounded-lg border border-zinc-100 dark:border-slate-700 hover:bg-zinc-50 dark:hover:bg-slate-800 transition-colors"
                      >
                        <Checkbox
                          checked={selectedSettings.has(setting.title)}
                          onCheckedChange={() => toggleSetting(setting.title)}
                        />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="font-medium text-sm">{setting.title}</span>
                            {setting.category && (
                              <Badge variant="outline" className="text-xs">
                                {setting.category}
                              </Badge>
                            )}
                          </div>
                          {setting.content && (
                            <p className="text-xs text-zinc-500 dark:text-slate-400 mt-1 line-clamp-2">
                              {setting.content}
                            </p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 关系变化 */}
              {changes && (changes.relationshipChanges?.length || 0) > 0 && (
                <div>
                  <h4 className="flex items-center gap-2 text-sm font-medium mb-3">
                    <GitBranch className="h-4 w-4 text-cyan-500" />
                    关系变化
                    <Badge variant="secondary" className="ml-1">
                      {changes.relationshipChanges.length}
                    </Badge>
                  </h4>
                  <div className="space-y-2">
                    {changes.relationshipChanges.map((rel, idx) => {
                      const relKey = `${rel.from}->${rel.to}`;
                      return (
                        <div
                          key={`${rel.from}-${rel.to}-${idx}`}
                          className="flex items-start gap-3 p-3 rounded-lg border border-cyan-100 dark:border-cyan-900/30 bg-cyan-50/50 dark:bg-cyan-900/10 hover:bg-cyan-100/50 dark:hover:bg-cyan-900/20 transition-colors"
                        >
                          <Checkbox
                            checked={selectedRelationships.has(relKey)}
                            onCheckedChange={() => toggleRelationship(relKey)}
                          />
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 text-sm">
                              <span className="font-medium">{rel.from}</span>
                              <span className="text-zinc-400">→</span>
                              <span className="font-medium">{rel.to}</span>
                            </div>
                            <div className="flex items-center gap-2 mt-1 text-xs">
                              {rel.oldRelation && (
                                <>
                                  <span className="text-zinc-400 line-through">{rel.oldRelation}</span>
                                  <span className="text-zinc-400">→</span>
                                </>
                              )}
                              <span className="text-cyan-600 dark:text-cyan-400 font-medium">
                                {rel.newRelation}
                              </span>
                            </div>
                            {rel.reason && (
                              <p className="text-xs text-zinc-500 mt-1">{rel.reason}</p>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                  <p className="text-xs text-zinc-400 mt-2">
                    * 关系将自动创建到世界观图谱中
                  </p>
                </div>
              )}
            </div>
          )}
        </div>

        <DialogFooter className="mt-4 flex-shrink-0">
          <Button variant="outline" onClick={onClose} disabled={isApplying}>
            取消
          </Button>
          <Button
            onClick={handleApply}
            disabled={isLoading || isApplying || !hasSelectedItems}
          >
            {isApplying ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                应用中...
              </>
            ) : (
              `应用选中项 (${selectedCharacters.size + selectedLocations.size + selectedSettings.size + selectedRelationships.size})`
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
