import { useState, useMemo } from 'react';
import { Clock, User, MapPin, BookOpen, ChevronDown, ChevronRight, Search, X } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import type { TimelineEvent, ChapterAnchor } from '@/types/timeline';
import type { Character, Location, Setting } from '@/types/novel';
import type { Relationship } from '@/types/relationship';

// 实体联合类型，用于统一处理
type Entity =
  | (Character & { type: 'character' })
  | (Location & { type: 'location' })
  | (Setting & { type: 'setting' })
  | (Relationship & { type: 'relationship' });

interface TimelinePanelProps {
  workId?: string;
  events: TimelineEvent[];
  chapters: ChapterAnchor[];
  characters: Character[];
  locations: Location[];
  settings: Setting[];
  relationships: Relationship[];
  onEventClick: (event: TimelineEvent) => void;
  onAddEvent?: () => void;
  onEditEvent?: (event: TimelineEvent) => void;
  onDeleteEvent?: (eventId: string) => void;
}

export function TimelinePanel({
  workId,
  events,
  chapters,
  characters,
  locations,
  settings,
  relationships,
  onEventClick,
  onAddEvent,
  onEditEvent,
  onDeleteEvent
}: TimelinePanelProps) {
  // 状态管理
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedEntityId, setSelectedEntityId] = useState<string>('all');
  const [selectedEventType, setSelectedEventType] = useState<string>('all');
  const [collapsedChapters, setCollapsedChapters] = useState<Set<string>>(new Set());

  const sortedEvents = [...events].sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));

  // 构建统一的实体列表
  const entities = useMemo<Entity[]>(() => {
    const result: Entity[] = [];

    characters.forEach(char => {
      result.push({ ...char, type: 'character' as const });
    });

    locations.forEach(loc => {
      result.push({ ...loc, type: 'location' as const });
    });

    settings.forEach(setting => {
      result.push({ ...setting, type: 'setting' as const });
    });

    relationships.forEach(rel => {
      result.push({ ...rel, type: 'relationship' as const });
    });

    return result;
  }, [characters, locations, settings, relationships]);

  const getEntityById = (id: string, type: string) => {
    return entities.find(e => e.id === id && e.type === type);
  };

  const getEntityName = (entity: Entity): string => {
    if ('name' in entity) return entity.name;
    if ('title' in entity) return entity.title;
    if ('label' in entity) return entity.label;
    return '未知';
  };

  const getEntityIcon = (type: string) => {
    switch (type) {
      case 'character': return User;
      case 'location': return MapPin;
      case 'setting': return BookOpen;
      default: return Clock;
    }
  };

  // 事件类型列表
  const eventTypes = [
    { value: 'milestone', label: '里程碑' },
    { value: 'change', label: '变化' },
    { value: 'created', label: '创建' },
    { value: 'removed', label: '移除' },
    { value: 'conflict', label: '冲突' },
    { value: 'discovery', label: '发现' },
    { value: 'meeting', label: '相遇' },
    { value: 'departure', label: '离别' },
    { value: 'achievement', label: '成就' },
    { value: 'loss', label: '失去' },
    { value: 'transformation', label: '转变' }
  ];

  // 筛选事件
  const filteredEvents = useMemo(() => {
    return sortedEvents.filter(event => {
      // 搜索筛选
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        const matchTitle = event.title.toLowerCase().includes(query);
        const matchDescription = event.description?.toLowerCase().includes(query);
        if (!matchTitle && !matchDescription) return false;
      }

      // 实体筛选
      if (selectedEntityId !== 'all' && event.entityId !== selectedEntityId) {
        return false;
      }

      // 事件类型筛选
      if (selectedEventType !== 'all' && event.eventType !== selectedEventType) {
        return false;
      }

      return true;
    });
  }, [sortedEvents, searchQuery, selectedEntityId, selectedEventType]);

  // 按章节分组
  const groupedByChapter = useMemo(() => {
    const groups: { [key: string]: TimelineEvent[] } = {};
    const unassigned: TimelineEvent[] = [];

    filteredEvents.forEach(event => {
      if (event.chapterId) {
        if (!groups[event.chapterId]) {
          groups[event.chapterId] = [];
        }
        groups[event.chapterId].push(event);
      } else {
        unassigned.push(event);
      }
    });

    return { groups, unassigned };
  }, [filteredEvents]);

  // 章节排序
  const sortedChapters = useMemo(() => {
    return [...chapters].sort((a, b) => a.chapterNumber - b.chapterNumber);
  }, [chapters]);

  // 切换章节折叠状态
  const toggleChapter = (chapterId: string) => {
    const newCollapsed = new Set(collapsedChapters);
    if (newCollapsed.has(chapterId)) {
      newCollapsed.delete(chapterId);
    } else {
      newCollapsed.add(chapterId);
    }
    setCollapsedChapters(newCollapsed);
  };

  // 跳转到章节
  const scrollToChapter = (chapterId: string) => {
    const element = document.getElementById(`chapter-${chapterId}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // 确保章节是展开的
      const newCollapsed = new Set(collapsedChapters);
      newCollapsed.delete(chapterId);
      setCollapsedChapters(newCollapsed);
    }
  };

  // 渲染事件卡片
  const renderEventCard = (event: TimelineEvent, index: number) => {
    const entity = event.entityId && event.entityType
      ? getEntityById(event.entityId, event.entityType)
      : null;
    const EntityIcon = entity ? getEntityIcon(event.entityType || 'character') : Clock;

    return (
      <div key={event.id} className="relative pl-12 animate-fade-in">
        {/* 时间轴节点 */}
        <div
          className="absolute left-2.5 w-2 h-2 rounded-full border border-background"
          style={{ backgroundColor: event.color || '#3b82f6' }}
        />

        {/* 事件卡片 */}
        <div
          onClick={() => onEventClick(event)}
          className="bg-card rounded p-2 hover:bg-accent/20 transition-colors cursor-pointer group border border-transparent hover:border-border"
        >
          <div className="flex items-center gap-2 flex-wrap">
            {/* 标题和图标 */}
            <div className="flex items-center gap-1.5 flex-1 min-w-0">
              {event.icon && <span className="text-sm flex-shrink-0">{event.icon}</span>}
              <h3 className="text-foreground text-xs font-medium group-hover:text-primary transition-colors truncate">
                {event.title}
              </h3>
            </div>

            {/* 右侧标签组 */}
            <div className="flex items-center gap-1.5 flex-shrink-0">
              {event.eventType && (
                <Badge variant="secondary" className="h-4 text-[10px] px-1.5">
                  {eventTypes.find(t => t.value === event.eventType)?.label || event.eventType}
                </Badge>
              )}
              {entity && (
                <div className="flex items-center gap-1 px-1.5 py-0.5 bg-accent/50 rounded text-[10px]">
                  <EntityIcon className="w-3 h-3 text-primary/70" />
                  <span className="text-foreground">{getEntityName(entity)}</span>
                </div>
              )}
              {event.timestamp && (
                <span className="text-muted-foreground text-[10px] flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {new Date(event.timestamp).toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' })}
                </span>
              )}
            </div>
          </div>

          {event.description && (
            <p className="text-muted-foreground text-[11px] mt-1.5 leading-snug line-clamp-1">{event.description}</p>
          )}
        </div>
      </div>
    );
  };

  // 清除所有筛选
  const clearFilters = () => {
    setSearchQuery('');
    setSelectedEntityId('all');
    setSelectedEventType('all');
  };

  const hasActiveFilters = searchQuery || selectedEntityId !== 'all' || selectedEventType !== 'all';

  return (
    <div className="relative w-full h-full bg-gradient-to-br from-background to-muted/20 dark:from-background dark:to-muted/10 text-sm flex flex-col">
      {/* 顶部工具栏 */}
      <div className="border-b border-border bg-card/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="p-4 space-y-3">
          {/* 标题和快速跳转 */}
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-foreground text-lg font-medium">时间线视图</h2>
              <p className="text-muted-foreground text-xs mt-0.5">
                共 {filteredEvents.length} 个事件
                {hasActiveFilters && <span className="text-primary ml-1">(已筛选)</span>}
              </p>
            </div>

            {/* 章节快速跳转 */}
            {sortedChapters.length > 0 && (
              <Select onValueChange={scrollToChapter}>
                <SelectTrigger className="w-40 h-8 text-xs">
                  <SelectValue placeholder="跳转到章节..." />
                </SelectTrigger>
                <SelectContent>
                  {sortedChapters.map(chapter => (
                    <SelectItem key={chapter.chapterId} value={chapter.chapterId} className="text-xs">
                      第{chapter.chapterNumber}章 · {chapter.chapterTitle}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}
          </div>

          {/* 筛选工具栏 */}
          <div className="flex gap-2">
            {/* 搜索框 */}
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
              <Input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="搜索事件标题或描述..."
                className="pl-8 h-8 text-xs"
              />
              {searchQuery && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSearchQuery('')}
                  className="absolute right-1 top-1/2 -translate-y-1/2 h-6 w-6 p-0"
                >
                  <X className="w-3 h-3" />
                </Button>
              )}
            </div>

            {/* 实体筛选 */}
            <Select value={selectedEntityId} onValueChange={setSelectedEntityId}>
              <SelectTrigger className="w-32 h-8 text-xs">
                <SelectValue placeholder="全部实体" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all" className="text-xs">全部实体</SelectItem>
                {entities.map(entity => (
                  <SelectItem key={entity.id} value={entity.id} className="text-xs">
                    {getEntityName(entity)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* 事件类型筛选 */}
            <Select value={selectedEventType} onValueChange={setSelectedEventType}>
              <SelectTrigger className="w-28 h-8 text-xs">
                <SelectValue placeholder="全部类型" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all" className="text-xs">全部类型</SelectItem>
                {eventTypes.map(type => (
                  <SelectItem key={type.value} value={type.value} className="text-xs">
                    {type.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* 清除筛选 */}
            {hasActiveFilters && (
              <Button
                variant="ghost"
                size="sm"
                onClick={clearFilters}
                className="h-8 text-xs"
              >
                <X className="w-3 h-3 mr-1" />
                清除
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* 时间线内容 */}
      <ScrollArea className="flex-1 custom-scrollbar">
        <div className="p-6">
          <div className="max-w-4xl mx-auto">
            {/* 时间线 */}
            <div className="relative">
              {/* 时间线主轴 */}
              <div className="absolute left-3.5 top-0 bottom-0 w-px bg-border" />

              {/* 事件列表 */}
              <div className="space-y-4">
                {filteredEvents.length === 0 ? (
                  <div className="text-center py-16 text-muted-foreground">
                    <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-accent flex items-center justify-center">
                      <Clock className="w-8 h-8 text-muted-foreground/50" />
                    </div>
                    <p className="text-sm">
                      {hasActiveFilters ? '没有符合条件的事件' : '暂无时间线事件'}
                    </p>
                    <p className="mt-1 text-xs">
                      {hasActiveFilters ? '尝试调整筛选条件' : '点击右上角按钮创建事件'}
                    </p>
                  </div>
                ) : (
                  <>
                    {/* 按章节分组显示 */}
                    {sortedChapters.map(chapter => {
                      const chapterEvents = groupedByChapter.groups[chapter.chapterId] || [];
                      if (chapterEvents.length === 0) return null;

                      const isCollapsed = collapsedChapters.has(chapter.chapterId);

                      return (
                        <div key={chapter.chapterId} id={`chapter-${chapter.chapterId}`} className="space-y-2">
                          {/* 章节标题 */}
                          <div
                            onClick={() => toggleChapter(chapter.chapterId)}
                            className="flex items-center gap-2 cursor-pointer hover:bg-accent/20 py-1.5 px-2 -mx-2 rounded transition-colors"
                          >
                            <div className="flex items-center justify-center w-4 h-4 flex-shrink-0">
                              {isCollapsed ? (
                                <ChevronRight className="w-3.5 h-3.5 text-muted-foreground" />
                              ) : (
                                <ChevronDown className="w-3.5 h-3.5 text-muted-foreground" />
                              )}
                            </div>
                            <h3 className="text-foreground text-xs font-medium">
                              第 {chapter.chapterNumber} 章 · {chapter.chapterTitle}
                            </h3>
                            <span className="text-muted-foreground text-[10px] ml-1">
                              ({chapterEvents.length})
                            </span>
                          </div>

                          {/* 章节事件 */}
                          {!isCollapsed && (
                            <div className="space-y-1.5 mt-2">
                              {chapterEvents.map((event, idx) => renderEventCard(event, idx))}
                            </div>
                          )}
                        </div>
                      );
                    })}

                    {/* 未分配事件 */}
                    {groupedByChapter.unassigned.length > 0 && (
                      <div className="space-y-2">
                        {/* 未分配标题 */}
                        <div
                          onClick={() => toggleChapter('unassigned')}
                          className="flex items-center gap-2 cursor-pointer hover:bg-accent/20 py-1.5 px-2 -mx-2 rounded transition-colors"
                        >
                          <div className="flex items-center justify-center w-4 h-4 flex-shrink-0">
                            {collapsedChapters.has('unassigned') ? (
                              <ChevronRight className="w-3.5 h-3.5 text-muted-foreground" />
                            ) : (
                              <ChevronDown className="w-3.5 h-3.5 text-muted-foreground" />
                            )}
                          </div>
                          <h3 className="text-foreground text-xs font-medium">未分配章节</h3>
                          <span className="text-muted-foreground text-[10px] ml-1">
                            ({groupedByChapter.unassigned.length})
                          </span>
                        </div>

                        {/* 未分配事件 */}
                        {!collapsedChapters.has('unassigned') && (
                          <div className="space-y-1.5 mt-2">
                            {groupedByChapter.unassigned.map((event, idx) => renderEventCard(event, idx))}
                          </div>
                        )}
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </ScrollArea>
    </div>
  );
}
