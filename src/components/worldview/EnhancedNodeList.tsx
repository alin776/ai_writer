import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Search, User, MapPin, BookOpen, Target, Plus, ChevronDown, FolderOpen, PanelLeftClose } from 'lucide-react';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Character, Location, Setting } from '@/types/novel';
import { EntityType } from '@/types/relationship';

interface EnhancedNodeListProps {
  characters: Character[];
  locations: Location[];
  settings: Setting[];
  onNodeClick: (nodeId: string, nodeType: EntityType) => void;
  onNodeDoubleClick: (nodeId: string, nodeType: EntityType) => void;
  onFocusNode?: (nodeId: string, nodeType: EntityType) => void;
  onCreateCharacter?: () => void;
  onCreateLocation?: () => void;
  onCreateSetting?: () => void;
  onOpenGroupPanel?: () => void;
  onCollapsePanel?: () => void;
  relationships?: any[];
}

export function EnhancedNodeList({
  characters,
  locations,
  settings,
  onNodeClick,
  onNodeDoubleClick,
  onFocusNode,
  onCreateCharacter,
  onCreateLocation,
  onCreateSetting,
  onOpenGroupPanel,
  onCollapsePanel
}: EnhancedNodeListProps) {
  const [searchText, setSearchText] = useState('');
  const [isCharactersOpen, setIsCharactersOpen] = useState(true);
  const [isLocationsOpen, setIsLocationsOpen] = useState(true);
  const [isSettingsOpen, setIsSettingsOpen] = useState(true);

  const filterEntities = <T extends { id: string; name?: string; title?: string; tags?: string[] }>(entities: T[]) => {
    return entities.filter(entity => {
      const name = entity.name || entity.title || '';
      const matchesSearch = name.toLowerCase().includes(searchText.toLowerCase());
      return matchesSearch;
    });
  };

  const filteredCharacters = filterEntities(characters);
  const filteredLocations = filterEntities(locations);
  const filteredSettings = filterEntities(settings);

  const EntityItem = ({
    entity,
    icon: Icon,
    type
  }: {
    entity: Character | Location | Setting;
    icon: any;
    type: EntityType;
  }) => {
    const name = 'name' in entity ? entity.name : entity.title;
    const tags = entity.tags || [];
    const [clickTimer, setClickTimer] = useState<NodeJS.Timeout | null>(null);

    const handleClick = () => {
      if (clickTimer) {
        // 双击
        clearTimeout(clickTimer);
        setClickTimer(null);
        onNodeDoubleClick(entity.id, type);
      } else {
        // 单击 - 延迟执行
        const timer = setTimeout(() => {
          onNodeClick(entity.id, type);
          setClickTimer(null);
        }, 250);
        setClickTimer(timer);
      }
    };

    return (
      <div
        className="flex items-center justify-between p-2.5 rounded-md cursor-pointer group transition-all duration-200 hover:bg-accent/40 hover:shadow-[0_1px_3px_rgba(0,0,0,0.06)]"
        onClick={handleClick}
      >
        <div className="flex items-center gap-2 flex-1 min-w-0">
          <Icon className="w-3.5 h-3.5 text-primary/70 flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <div className="truncate text-foreground text-sm">{name}</div>
            {tags.length > 0 && (
              <div className="flex gap-1 mt-1">
                {tags.slice(0, 2).map(tag => (
                  <Badge key={tag} variant="secondary" className="text-xs h-4 px-1.5">
                    {tag}
                  </Badge>
                ))}
              </div>
            )}
          </div>
        </div>
        {onFocusNode && (
          <Button
            variant="ghost"
            size="sm"
            className="opacity-0 group-hover:opacity-100 transition-opacity h-6 w-6 p-0"
            onClick={(e) => {
              e.stopPropagation();
              onFocusNode(entity.id, type);
            }}
          >
            <Target className="w-3 h-3" />
          </Button>
        )}
      </div>
    );
  };

  return (
    <div className="h-full flex flex-col text-sm overflow-hidden">
      {/* 搜索框 */}
      <div className="flex-shrink-0 px-2 py-3 overflow-hidden">
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-2.5 top-2 w-3.5 h-3.5 text-muted-foreground" />
            <Input
              placeholder="搜索节点..."
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              className="pl-8 h-8 text-sm bg-background border-0 shadow-sm"
            />
          </div>
          {(onCreateCharacter || onCreateLocation || onCreateSetting || onOpenGroupPanel) && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className="h-8 w-8 p-0 flex-shrink-0">
                  <Plus className="w-4 h-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-32">
                {onOpenGroupPanel && (
                  <>
                    <DropdownMenuItem onClick={onOpenGroupPanel}>
                      分组管理
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                  </>
                )}
                {onCreateCharacter && (
                  <DropdownMenuItem onClick={onCreateCharacter}>
                    新建角色
                  </DropdownMenuItem>
                )}
                {onCreateLocation && (
                  <DropdownMenuItem onClick={onCreateLocation}>
                    新建地点
                  </DropdownMenuItem>
                )}
                {onCreateSetting && (
                  <DropdownMenuItem onClick={onCreateSetting}>
                    新建设定
                  </DropdownMenuItem>
                )}
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      </div>

      {/* 节点列表 */}
      <div className="flex-1 min-h-0 overflow-y-auto custom-scrollbar">
        <div className="px-2 py-3 space-y-4">
          {/* 角色列表 */}
          <Collapsible open={isCharactersOpen} onOpenChange={setIsCharactersOpen} className="animate-fade-in group/section">
            <div className="flex items-center justify-between mb-2 relative overflow-hidden group/header">
              <CollapsibleTrigger className="flex items-center gap-2 flex-1 hover:opacity-70 transition-opacity relative focus:outline-none focus-visible:outline-none">
                <ChevronDown className={`w-3.5 h-3.5 text-muted-foreground transition-transform ${isCharactersOpen ? '' : '-rotate-90'}`} />
                <span className="text-foreground text-xs font-medium">角色</span>
                <Badge variant="secondary" className="ml-1 h-4 text-xs">{filteredCharacters.length}</Badge>
              </CollapsibleTrigger>
            </div>
            <CollapsibleContent className="space-y-1">
              {filteredCharacters.length > 0 ? (
                filteredCharacters.map(char => (
                  <EntityItem key={char.id} entity={char} icon={User} type="character" />
                ))
              ) : (
                <div className="text-muted-foreground text-xs text-center py-2">暂无角色</div>
              )}
            </CollapsibleContent>
          </Collapsible>

          {/* 地点列表 */}
          <Collapsible open={isLocationsOpen} onOpenChange={setIsLocationsOpen} className="animate-fade-in group/section">
            <div className="flex items-center justify-between mb-2 relative overflow-hidden group/header">
              <CollapsibleTrigger className="flex items-center gap-2 flex-1 hover:opacity-70 transition-opacity relative focus:outline-none focus-visible:outline-none">
                <ChevronDown className={`w-3.5 h-3.5 text-muted-foreground transition-transform ${isLocationsOpen ? '' : '-rotate-90'}`} />
                <span className="text-foreground text-xs font-medium">地点</span>
                <Badge variant="secondary" className="ml-1 h-4 text-xs">{filteredLocations.length}</Badge>
              </CollapsibleTrigger>
            </div>
            <CollapsibleContent className="space-y-1">
              {filteredLocations.length > 0 ? (
                filteredLocations.map(loc => (
                  <EntityItem key={loc.id} entity={loc} icon={MapPin} type="location" />
                ))
              ) : (
                <div className="text-muted-foreground text-xs text-center py-2">暂无地点</div>
              )}
            </CollapsibleContent>
          </Collapsible>

          {/* 设定列表 */}
          <Collapsible open={isSettingsOpen} onOpenChange={setIsSettingsOpen} className="animate-fade-in group/section">
            <div className="flex items-center justify-between mb-2 relative overflow-hidden group/header">
              <CollapsibleTrigger className="flex items-center gap-2 flex-1 hover:opacity-70 transition-opacity relative focus:outline-none focus-visible:outline-none">
                <ChevronDown className={`w-3.5 h-3.5 text-muted-foreground transition-transform ${isSettingsOpen ? '' : '-rotate-90'}`} />
                <span className="text-foreground text-xs font-medium">设定</span>
                <Badge variant="secondary" className="ml-1 h-4 text-xs">{filteredSettings.length}</Badge>
              </CollapsibleTrigger>
            </div>
            <CollapsibleContent className="space-y-1">
              {filteredSettings.length > 0 ? (
                filteredSettings.map(setting => (
                  <EntityItem key={setting.id} entity={setting} icon={BookOpen} type="setting" />
                ))
              ) : (
                <div className="text-muted-foreground text-xs text-center py-2">暂无设定</div>
              )}
            </CollapsibleContent>
          </Collapsible>
        </div>
      </div>
    </div>
  );
}
