import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Search, User, MapPin, BookOpen, Target, Plus, ChevronDown } from 'lucide-react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
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
  onCreateSetting
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
    <div className="flex flex-col h-full text-sm">
      {/* 搜索框 */}
      <div className="p-3 border-b border-border-light">
        <div className="relative">
          <Search className="absolute left-2.5 top-2 w-3.5 h-3.5 text-muted-foreground" />
          <Input
            placeholder="搜索节点..."
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            className="pl-8 h-8 text-sm bg-background border-0 shadow-sm"
          />
        </div>
      </div>

      {/* 节点列表 */}
      <ScrollArea className="flex-1 custom-scrollbar">
        <div className="p-3 space-y-4">
          {/* 角色列表 */}
          <Collapsible open={isCharactersOpen} onOpenChange={setIsCharactersOpen} className="animate-fade-in group/section">
            <div className="flex items-center justify-between mb-2 relative overflow-hidden group/header">
              <div className="absolute left-0 top-0 bottom-0 w-0 group-hover/header:w-[50%] bg-gradient-to-r from-orange-100/50 to-transparent transition-all duration-500 ease-out pointer-events-none" />
              <CollapsibleTrigger className="flex items-center gap-2 flex-1 hover:opacity-70 transition-opacity relative">
                <ChevronDown className={`w-3.5 h-3.5 text-muted-foreground transition-transform ${isCharactersOpen ? '' : '-rotate-90'}`} />
                <div className="w-6 h-6 rounded-md bg-character/10 flex items-center justify-center">
                  <User className="w-3.5 h-3.5 text-character" />
                </div>
                <span className="text-foreground text-xs font-medium">角色</span>
                <Badge variant="secondary" className="ml-1 h-4 text-xs">{filteredCharacters.length}</Badge>
              </CollapsibleTrigger>
              {onCreateCharacter && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onCreateCharacter}
                  className="h-6 w-6 p-0 opacity-0 group-hover/section:opacity-100 transition-opacity relative"
                >
                  <Plus className="w-3.5 h-3.5" />
                </Button>
              )}
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
              <div className="absolute left-0 top-0 bottom-0 w-0 group-hover/header:w-[50%] bg-gradient-to-r from-orange-100/50 to-transparent transition-all duration-500 ease-out pointer-events-none" />
              <CollapsibleTrigger className="flex items-center gap-2 flex-1 hover:opacity-70 transition-opacity relative">
                <ChevronDown className={`w-3.5 h-3.5 text-muted-foreground transition-transform ${isLocationsOpen ? '' : '-rotate-90'}`} />
                <div className="w-6 h-6 rounded-md bg-location/10 flex items-center justify-center">
                  <MapPin className="w-3.5 h-3.5 text-location" />
                </div>
                <span className="text-foreground text-xs font-medium">地点</span>
                <Badge variant="secondary" className="ml-1 h-4 text-xs">{filteredLocations.length}</Badge>
              </CollapsibleTrigger>
              {onCreateLocation && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onCreateLocation}
                  className="h-6 w-6 p-0 opacity-0 group-hover/section:opacity-100 transition-opacity relative"
                >
                  <Plus className="w-3.5 h-3.5" />
                </Button>
              )}
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
              <div className="absolute left-0 top-0 bottom-0 w-0 group-hover/header:w-[50%] bg-gradient-to-r from-orange-100/50 to-transparent transition-all duration-500 ease-out pointer-events-none" />
              <CollapsibleTrigger className="flex items-center gap-2 flex-1 hover:opacity-70 transition-opacity relative">
                <ChevronDown className={`w-3.5 h-3.5 text-muted-foreground transition-transform ${isSettingsOpen ? '' : '-rotate-90'}`} />
                <div className="w-6 h-6 rounded-md bg-setting/10 flex items-center justify-center">
                  <BookOpen className="w-3.5 h-3.5 text-setting" />
                </div>
                <span className="text-foreground text-xs font-medium">设定</span>
                <Badge variant="secondary" className="ml-1 h-4 text-xs">{filteredSettings.length}</Badge>
              </CollapsibleTrigger>
              {onCreateSetting && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onCreateSetting}
                  className="h-6 w-6 p-0 opacity-0 group-hover/section:opacity-100 transition-opacity relative"
                >
                  <Plus className="w-3.5 h-3.5" />
                </Button>
              )}
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
      </ScrollArea>
    </div>
  );
}
