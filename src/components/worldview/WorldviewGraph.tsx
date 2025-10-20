/**
 * 世界观关系图可视化组件
 * 使用 ReactFlow 展示角色、地点、设定之间的关系
 */
import React, { useCallback, useMemo } from 'react';
import {
  ReactFlow,
  Node,
  Edge,
  Controls,
  Background,
  BackgroundVariant,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  MarkerType,
  Panel,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { WorldData } from '@/types/novel';
import { Users, MapPin, BookOpen } from 'lucide-react';
import './WorldviewGraph.css';

interface WorldviewGraphProps {
  worldData: WorldData;
  onNodeClick?: (nodeId: string, nodeType: 'character' | 'location' | 'setting') => void;
}

// 自定义节点组件 - 角色节点
const CharacterNode = ({ data }: any) => {
  return (
    <div className="worldview-node character-node">
      <div className="node-icon">
        <Users className="w-4 h-4" />
      </div>
      <div className="node-content">
        <div className="node-title">{data.label}</div>
        {data.role && <div className="node-subtitle">{data.role}</div>}
      </div>
    </div>
  );
};

// 自定义节点组件 - 地点节点
const LocationNode = ({ data }: any) => {
  return (
    <div className="worldview-node location-node">
      <div className="node-icon">
        <MapPin className="w-4 h-4" />
      </div>
      <div className="node-content">
        <div className="node-title">{data.label}</div>
        {data.type && <div className="node-subtitle">{data.type}</div>}
      </div>
    </div>
  );
};

// 自定义节点组件 - 设定节点
const SettingNode = ({ data }: any) => {
  return (
    <div className="worldview-node setting-node">
      <div className="node-icon">
        <BookOpen className="w-4 h-4" />
      </div>
      <div className="node-content">
        <div className="node-title">{data.label}</div>
        {data.category && <div className="node-subtitle">{data.category}</div>}
      </div>
    </div>
  );
};

// 节点类型映射
const nodeTypes = {
  character: CharacterNode,
  location: LocationNode,
  setting: SettingNode,
};

/**
 * 将后端数据转换为 ReactFlow 的 nodes 和 edges
 */
const convertToGraphData = (worldData: WorldData): { nodes: Node[]; edges: Edge[] } => {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  const edgeSet = new Set<string>(); // 用于去重边

  // 布局配置
  const SPACING_X = 300;
  const SPACING_Y = 200;
  const START_Y = 100;

  // 1. 添加角色节点
  const characters = worldData.characters || [];
  characters.forEach((character, index) => {
    nodes.push({
      id: `char-${character.id}`,
      type: 'character',
      position: { x: 100, y: START_Y + index * SPACING_Y },
      data: { 
        label: character.name,
        role: character.role,
        entityId: character.id,
        entityType: 'character',
      },
    });

    // 处理角色关系 (relationships 字段)
    if (character.relationships && Array.isArray(character.relationships)) {
      character.relationships.forEach((rel: any) => {
        if (rel.characterId) {
          const edgeId = `char-${character.id}-char-${rel.characterId}`;
          if (!edgeSet.has(edgeId)) {
            edges.push({
              id: edgeId,
              source: `char-${character.id}`,
              target: `char-${rel.characterId}`,
              label: rel.relationship || '关系',
              type: 'smoothstep',
              animated: false,
              markerEnd: {
                type: MarkerType.ArrowClosed,
                width: 15,
                height: 15,
              },
            });
            edgeSet.add(edgeId);
          }
        }
      });
    }
  });

  // 2. 添加地点节点
  const locations = worldData.locations || [];
  locations.forEach((location, index) => {
    nodes.push({
      id: `loc-${location.id}`,
      type: 'location',
      position: { x: 100 + SPACING_X, y: START_Y + index * SPACING_Y },
      data: { 
        label: location.name,
        type: location.type,
        entityId: location.id,
        entityType: 'location',
      },
    });

    // 处理地点关系 (related_locations 字段)
    if (location.relatedLocations && Array.isArray(location.relatedLocations)) {
      location.relatedLocations.forEach((relatedId: string) => {
        const edgeId = `loc-${location.id}-loc-${relatedId}`;
        if (!edgeSet.has(edgeId)) {
          edges.push({
            id: edgeId,
            source: `loc-${location.id}`,
            target: `loc-${relatedId}`,
            label: '相关',
            type: 'smoothstep',
            animated: false,
            style: { stroke: '#10b981' },
            markerEnd: {
              type: MarkerType.ArrowClosed,
              width: 15,
              height: 15,
              color: '#10b981',
            },
          });
          edgeSet.add(edgeId);
        }
      });
    }
  });

  // 3. 添加设定节点
  const settings = worldData.settings || [];
  settings.forEach((setting, index) => {
    nodes.push({
      id: `set-${setting.id}`,
      type: 'setting',
      position: { x: 100 + SPACING_X * 2, y: START_Y + index * SPACING_Y },
      data: { 
        label: setting.title,
        category: setting.category,
        entityId: setting.id,
        entityType: 'setting',
      },
    });
  });

  // 4. 自动创建一些合理的跨类型关系（示例）
  // 主角与第一个地点的关系
  if (characters.length > 0 && locations.length > 0) {
    const mainCharacter = characters.find(c => c.role === '主角') || characters[0];
    const firstLocation = locations[0];
    if (mainCharacter && firstLocation) {
      edges.push({
        id: `cross-char-${mainCharacter.id}-loc-${firstLocation.id}`,
        source: `char-${mainCharacter.id}`,
        target: `loc-${firstLocation.id}`,
        label: '活动于',
        type: 'smoothstep',
        animated: true,
        style: { stroke: '#8b5cf6', strokeDasharray: '5,5' },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          width: 15,
          height: 15,
          color: '#8b5cf6',
        },
      });
    }
  }

  return { nodes, edges };
};

const WorldviewGraph: React.FC<WorldviewGraphProps> = ({ worldData, onNodeClick }) => {
  // 转换数据
  const graphData = useMemo(() => convertToGraphData(worldData), [worldData]);
  
  const [nodes, , onNodesChange] = useNodesState(graphData.nodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(graphData.edges);

  // 连接节点时触发
  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // 节点点击事件
  const onNodeClickHandler = useCallback(
    (_: React.MouseEvent, node: Node) => {
      if (onNodeClick && node.data.entityId && node.data.entityType) {
        onNodeClick(node.data.entityId as string, node.data.entityType);
      }
    },
    [onNodeClick]
  );

  // 统计信息
  const stats = useMemo(() => {
    const characterCount = worldData.characters?.length || 0;
    const locationCount = worldData.locations?.length || 0;
    const settingCount = worldData.settings?.length || 0;
    return { characterCount, locationCount, settingCount };
  }, [worldData]);

  return (
    <div className="worldview-graph-container">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClickHandler}
        nodeTypes={nodeTypes}
        fitView
        minZoom={0.2}
        maxZoom={4}
        defaultEdgeOptions={{
          type: 'smoothstep',
          animated: false,
        }}
      >
        <Background variant={BackgroundVariant.Dots} gap={20} size={1} />
        <Controls />
        
        {/* 统计面板 */}
        <Panel position="top-left" className="worldview-stats-panel">
          <div className="stats-item">
            <Users className="w-4 h-4" />
            <span>{stats.characterCount} 个角色</span>
          </div>
          <div className="stats-item">
            <MapPin className="w-4 h-4" />
            <span>{stats.locationCount} 个地点</span>
          </div>
          <div className="stats-item">
            <BookOpen className="w-4 h-4" />
            <span>{stats.settingCount} 个设定</span>
          </div>
        </Panel>

        {/* 提示面板 */}
        <Panel position="top-right" className="worldview-hint-panel">
          <div className="hint-text">
            💡 提示：拖动节点调整位置，滚轮缩放视图
          </div>
        </Panel>
      </ReactFlow>
    </div>
  );
};

export default WorldviewGraph;
