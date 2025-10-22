/**
 * 增强版节点列表组件
 * 功能：智能助手 + 快速导航 + 状态筛选
 */
import React, { useState, useMemo } from 'react';
import { Users, MapPin, BookOpen, Search, AlertTriangle, Star, Clock, ChevronDown, ChevronRight, Target, Link2, Plus } from 'lucide-react';
import { Character, Location, Setting } from '@/types/novel';
import { Relationship, EntityType } from '@/types/relationship';

interface EnhancedNodeListProps {
  characters: Character[];
  locations: Location[];
  settings: Setting[];
  relationships: Relationship[];
  onNodeClick: (nodeId: string, nodeType: EntityType) => void;
  onNodeDoubleClick: (nodeId: string, nodeType: EntityType) => void;
  onNodeRightClick?: (nodeId: string, nodeType: EntityType, event: React.MouseEvent) => void;
  onFocusNode?: (nodeId: string, nodeType: EntityType) => void;
  onCreateCharacter?: () => void;
  onCreateLocation?: () => void;
  onCreateSetting?: () => void;
}

type FilterType = 'all' | 'connected' | 'isolated';

export const EnhancedNodeList: React.FC<EnhancedNodeListProps> = ({
  characters,
  locations,
  settings,
  relationships,
  onNodeClick,
  onNodeDoubleClick,
  onNodeRightClick,
  onFocusNode,
  onCreateCharacter,
  onCreateLocation,
  onCreateSetting,
}) => {
  const [searchText, setSearchText] = useState('');
  const [filterType, setFilterType] = useState<FilterType>('all');
  const [expandedSections, setExpandedSections] = useState({
    characters: true,
    locations: false,
    settings: true,
  });
  const [contextMenu, setContextMenu] = useState<{
    show: boolean;
    x: number;
    y: number;
    nodeId: string;
    nodeType: EntityType;
  } | null>(null);

  // 计算每个节点的关系数量
  const nodeRelationships = useMemo(() => {
    const counts: Record<string, number> = {};
    
    relationships.forEach(rel => {
      const sourceKey = `${rel.sourceType}-${rel.sourceId}`;
      const targetKey = `${rel.targetType}-${rel.targetId}`;
      counts[sourceKey] = (counts[sourceKey] || 0) + 1;
      counts[targetKey] = (counts[targetKey] || 0) + 1;
    });
    
    return counts;
  }, [relationships]);

  // 获取节点关系数
  const getRelationshipCount = (id: string, type: EntityType) => {
    return nodeRelationships[`${type}-${id}`] || 0;
  };

  // 过滤和搜索逻辑
  const filterNodes = <T extends { id: string; name?: string; title?: string }>(
    nodes: T[],
    type: EntityType
  ) => {
    return nodes.filter(node => {
      // 搜索过滤
      if (searchText) {
        const label = (node.name || node.title || '').toLowerCase();
        if (!label.includes(searchText.toLowerCase())) {
          return false;
        }
      }
      
      // 状态过滤
      const count = getRelationshipCount(node.id, type);
      if (filterType === 'connected' && count === 0) return false;
      if (filterType === 'isolated' && count > 0) return false;
      
      return true;
    });
  };

  const filteredCharacters = filterNodes(characters, 'character');
  const filteredLocations = filterNodes(locations, 'location');
  const filteredSettings = filterNodes(settings, 'setting');

  // 孤岛节点（无关系）
  const isolatedNodes = useMemo(() => {
    const isolated: Array<{ id: string; type: EntityType; label: string }> = [];
    
    characters.forEach(char => {
      if (getRelationshipCount(char.id, 'character') === 0) {
        isolated.push({ id: char.id, type: 'character', label: char.name });
      }
    });
    
    locations.forEach(loc => {
      if (getRelationshipCount(loc.id, 'location') === 0) {
        isolated.push({ id: loc.id, type: 'location', label: loc.name });
      }
    });
    
    settings.forEach(set => {
      if (getRelationshipCount(set.id, 'setting') === 0) {
        isolated.push({ id: set.id, type: 'setting', label: set.title });
      }
    });
    
    return isolated;
  }, [characters, locations, settings, nodeRelationships]);

  // 核心节点排行（关系最多的前5个）
  const topNodes = useMemo(() => {
    const allNodes: Array<{ id: string; type: EntityType; label: string; count: number }> = [];
    
    characters.forEach(char => {
      allNodes.push({
        id: char.id,
        type: 'character',
        label: char.name,
        count: getRelationshipCount(char.id, 'character'),
      });
    });
    
    locations.forEach(loc => {
      allNodes.push({
        id: loc.id,
        type: 'location',
        label: loc.name,
        count: getRelationshipCount(loc.id, 'location'),
      });
    });
    
    settings.forEach(set => {
      allNodes.push({
        id: set.id,
        type: 'setting',
        label: set.title,
        count: getRelationshipCount(set.id, 'setting'),
      });
    });
    
    return allNodes
      .filter(node => node.count > 0)
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);
  }, [characters, locations, settings, nodeRelationships]);

  // 切换分类展开/收起
  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  // 处理右键菜单
  const handleContextMenu = (e: React.MouseEvent, nodeId: string, nodeType: EntityType) => {
    e.preventDefault();
    if (onNodeRightClick) {
      setContextMenu({
        show: true,
        x: e.clientX,
        y: e.clientY,
        nodeId,
        nodeType,
      });
    }
  };

  // 关闭右键菜单
  React.useEffect(() => {
    const handleClick = () => setContextMenu(null);
    document.addEventListener('click', handleClick);
    return () => document.removeEventListener('click', handleClick);
  }, []);

  // 渲染节点项
  const renderNodeItem = (
    id: string,
    type: EntityType,
    label: string,
    relationCount: number
  ) => {
    const isCore = relationCount >= 5;
    const isIsolated = relationCount === 0;
    
    return (
      <div
        key={`${type}-${id}`}
        className="node-item group flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded cursor-pointer transition-colors"
        onClick={() => onNodeClick(id, type)}
        onDoubleClick={() => onNodeDoubleClick(id, type)}
        onContextMenu={(e) => handleContextMenu(e, id, type)}
      >
        {isCore && <Star className="w-3 h-3 text-yellow-400 flex-shrink-0" />}
        {isIsolated && <AlertTriangle className="w-3 h-3 text-orange-400 flex-shrink-0" />}
        {!isCore && !isIsolated && <span className="w-1 h-1 bg-gray-600 rounded-full flex-shrink-0" />}
        
        <span className="flex-1 truncate">{label}</span>
        
        {relationCount > 0 && (
          <span className="flex items-center gap-1 text-xs text-gray-500">
            <Link2 className="w-3 h-3" />
            {relationCount}
          </span>
        )}
      </div>
    );
  };

  return (
    <div className="enhanced-node-list flex flex-col h-full">
      {/* 智能助手区域 */}
      <div className="smart-assistant bg-gray-100 border-b border-gray-200 p-4 space-y-3">
        <div className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
          📊 智能助手
        </div>
        
        {/* 孤岛节点警告 */}
        {isolatedNodes.length > 0 && (
          <div className="bg-orange-500/10 border border-orange-500/30 rounded p-2">
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="w-4 h-4 text-orange-400" />
              <span className="text-xs font-medium text-orange-400">
                需要关注 ({isolatedNodes.length})
              </span>
            </div>
            <div className="space-y-1">
              {isolatedNodes.slice(0, 3).map(node => (
                <div
                  key={`${node.type}-${node.id}`}
                  className="text-xs text-gray-400 hover:text-white cursor-pointer truncate"
                  onClick={() => onNodeClick(node.id, node.type)}
                >
                  {node.label} - 无关系
                </div>
              ))}
              {isolatedNodes.length > 3 && (
                <button
                  onClick={() => setFilterType('isolated')}
                  className="text-xs text-orange-400 hover:text-orange-300"
                >
                  查看全部 {isolatedNodes.length} 个孤岛节点 →
                </button>
              )}
            </div>
          </div>
        )}
        
        {/* 核心节点排行 */}
        {topNodes.length > 0 && (
          <div className="bg-blue-500/10 border border-blue-500/30 rounded p-2">
            <div className="flex items-center gap-2 mb-2">
              <Star className="w-4 h-4 text-yellow-400" />
              <span className="text-xs font-medium text-blue-400">
                核心节点 Top {Math.min(topNodes.length, 3)}
              </span>
            </div>
            <div className="space-y-1">
              {topNodes.slice(0, 3).map((node, index) => (
                <div
                  key={`${node.type}-${node.id}`}
                  className="flex items-center gap-2 text-xs text-gray-400 hover:text-white cursor-pointer"
                  onClick={() => onNodeClick(node.id, node.type)}
                >
                  <span className="text-gray-500">{index + 1}.</span>
                  <span className="flex-1 truncate">{node.label}</span>
                  <span className="text-blue-400 font-medium">{node.count}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* 搜索和过滤区域 */}
      <div className="search-filter-area border-b border-gray-200 p-3 space-y-2">
        {/* 搜索框 */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            placeholder="搜索节点..."
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            className="w-full pl-9 pr-3 py-2 bg-white border border-gray-300 rounded text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-blue-500"
          />
        </div>
        
        {/* 过滤按钮 */}
        <div className="flex gap-2">
          <button
            onClick={() => setFilterType('all')}
            className={`flex-1 px-2 py-1 text-xs rounded transition-colors ${
              filterType === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            全部
          </button>
          <button
            onClick={() => setFilterType('connected')}
            className={`flex-1 px-2 py-1 text-xs rounded transition-colors ${
              filterType === 'connected'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            有关系
          </button>
          <button
            onClick={() => setFilterType('isolated')}
            className={`flex-1 px-2 py-1 text-xs rounded transition-colors ${
              filterType === 'isolated'
                ? 'bg-orange-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            孤岛⚠️
          </button>
        </div>
      </div>

      {/* 节点列表区域 */}
      <div className="node-list-area flex-1 overflow-y-auto p-3 space-y-3">
        {/* 角色列表 */}
        <div className="node-section">
          <div className="flex items-center justify-between px-2 py-1">
            <button
              onClick={() => toggleSection('characters')}
              className="flex-1 flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              {expandedSections.characters ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
              <Users className="w-4 h-4 text-blue-400" />
              <span>角色 ({filteredCharacters.length})</span>
            </button>
            {onCreateCharacter && (
              <button
                onClick={onCreateCharacter}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
                title="创建角色"
              >
                <Plus className="w-4 h-4 text-blue-600" />
              </button>
            )}
          </div>
          
          {expandedSections.characters && (
            <div className="mt-1 space-y-0.5">
              {filteredCharacters.map(char =>
                renderNodeItem(
                  char.id,
                  'character',
                  char.name,
                  getRelationshipCount(char.id, 'character')
                )
              )}
              {filteredCharacters.length === 0 && (
                <div className="px-3 py-2 text-xs text-gray-500">暂无匹配结果</div>
              )}
            </div>
          )}
        </div>

        {/* 地点列表 */}
        <div className="node-section">
          <div className="flex items-center justify-between px-2 py-1">
            <button
              onClick={() => toggleSection('locations')}
              className="flex-1 flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              {expandedSections.locations ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
              <MapPin className="w-4 h-4 text-green-400" />
              <span>地点 ({filteredLocations.length})</span>
            </button>
            {onCreateLocation && (
              <button
                onClick={onCreateLocation}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
                title="创建地点"
              >
                <Plus className="w-4 h-4 text-green-600" />
              </button>
            )}
          </div>
          
          {expandedSections.locations && (
            <div className="mt-1 space-y-0.5">
              {filteredLocations.map(loc =>
                renderNodeItem(
                  loc.id,
                  'location',
                  loc.name,
                  getRelationshipCount(loc.id, 'location')
                )
              )}
              {filteredLocations.length === 0 && (
                <div className="px-3 py-2 text-xs text-gray-500">暂无匹配结果</div>
              )}
            </div>
          )}
        </div>

        {/* 设定列表 */}
        <div className="node-section">
          <div className="flex items-center justify-between px-2 py-1">
            <button
              onClick={() => toggleSection('settings')}
              className="flex-1 flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              {expandedSections.settings ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
              <BookOpen className="w-4 h-4 text-orange-400" />
              <span>设定 ({filteredSettings.length})</span>
            </button>
            {onCreateSetting && (
              <button
                onClick={onCreateSetting}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
                title="创建设定"
              >
                <Plus className="w-4 h-4 text-orange-600" />
              </button>
            )}
          </div>
          
          {expandedSections.settings && (
            <div className="mt-1 space-y-0.5">
              {filteredSettings.map(set =>
                renderNodeItem(
                  set.id,
                  'setting',
                  set.title,
                  getRelationshipCount(set.id, 'setting')
                )
              )}
              {filteredSettings.length === 0 && (
                <div className="px-3 py-2 text-xs text-gray-500">暂无匹配结果</div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* 操作提示 */}
      <div className="hints-area border-t border-gray-200 p-3 bg-gray-100">
        <div className="text-xs text-gray-500 space-y-1">
          <div>💡 <span className="text-gray-400">单击</span> → 图中定位</div>
          <div>💡 <span className="text-gray-400">双击</span> → 查看详情</div>
          <div>💡 <span className="text-gray-400">右键</span> → 快捷操作</div>
        </div>
      </div>

      {/* 右键菜单 */}
      {contextMenu?.show && (
        <div
          className="fixed bg-white border border-gray-200 rounded shadow-lg py-1 z-50 min-w-[160px]"
          style={{ left: contextMenu.x, top: contextMenu.y }}
        >
          <button
            onClick={() => {
              onNodeClick(contextMenu.nodeId, contextMenu.nodeType);
              setContextMenu(null);
            }}
            className="w-full px-4 py-2 text-sm text-left text-gray-600 hover:bg-gray-100 hover:text-gray-900 flex items-center gap-2"
          >
            <Target className="w-4 h-4" />
            在图中定位
          </button>
          {onFocusNode && (
            <button
              onClick={() => {
                onFocusNode(contextMenu.nodeId, contextMenu.nodeType);
                setContextMenu(null);
              }}
              className="w-full px-4 py-2 text-sm text-left text-gray-600 hover:bg-gray-100 hover:text-gray-900 flex items-center gap-2"
            >
              <Target className="w-4 h-4" />
              焦点模式聚焦
            </button>
          )}
          <button
            onClick={() => {
              onNodeDoubleClick(contextMenu.nodeId, contextMenu.nodeType);
              setContextMenu(null);
            }}
            className="w-full px-4 py-2 text-sm text-left text-gray-600 hover:bg-gray-100 hover:text-gray-900 flex items-center gap-2"
          >
            <Users className="w-4 h-4" />
            查看详情
          </button>
        </div>
      )}
    </div>
  );
};
