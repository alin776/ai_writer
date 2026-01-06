/**
 * 世界观关系图可视化组件
 * 使用 ReactFlow 展示角色、地点、设定之间的关系
 */
import React, { useCallback, useMemo, useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import {
  ReactFlow,
  Node,
  Edge,
  EdgeTypes,
  Controls,
  Background,
  BackgroundVariant,
  MiniMap,
  useNodesState,
  useEdgesState,
  useReactFlow,
  addEdge,
  Connection,
  MarkerType,
  Panel,
  Handle,
  Position,
  NodeProps,
  NodeTypes,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { WorldData } from '@/types/novel';
import { Relationship, EntityType, RELATIONSHIP_COLORS } from '@/types/relationship';
import { Users, MapPin, BookOpen, X, HelpCircle, PanelLeftClose, PanelLeft, Layers, ChevronLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import './WorldviewGraph.css';
import {
  LayoutAlgorithm,
  GlobalLayoutConfig,
  applyForceLayout,
  applyHierarchicalLayout,
  applyCircularLayout,
  applyGridLayout,
  applyTimelineLayout,
} from './layouts';
import CustomBezierEdge from './CustomBezierEdge';

type WorldNodeData = {
  label: string;
  role?: string;
  type?: string;
  category?: string;
  entityId: string;
  entityType: EntityType;
};

type WorldEdgeData = {
  relationshipId?: string;
  relationshipType?: string;
  description?: string;
  strength?: number;
  color?: string;
  lineStyle?: 'solid' | 'dashed' | 'dotted';
  edgeCount?: number;
  edgeIndex?: number;
  relationship?: Relationship;
};

type WorldNode = Node<WorldNodeData>;
type WorldEdge = Edge<WorldEdgeData>;

interface WorldviewGraphProps {
  worldData: WorldData;
  relationships?: Relationship[];
  editable?: boolean;
  onNodeClick?: (nodeId: string, nodeType: 'character' | 'location' | 'setting') => void;
  onConnect?: (sourceId: string, sourceType: EntityType, targetId: string, targetType: EntityType) => void;
  onEdgeClick?: (relationshipId: string) => void;
  selectedNodeId?: string; // 选中的节点ID（用于高亮显示）
  layoutConfig?: GlobalLayoutConfig; // 布局配置
  onLayoutApplied?: () => void; // 布局应用完成的回调
  searchText?: string; // 搜索文本
  filteredNodeTypes?: { character: boolean; location: boolean; setting: boolean }; // 过滤的节点类型
  focusMode?: boolean; // 焦点模式
  focusNodeId?: string; // 焦点节点ID
  focusNodeToView?: string; // 需要定位的节点ID（触发视野移动）
  connectionMode?: boolean; // 连线模式
  connectionModeSource?: { id: string; name: string; type: EntityType }; // 连线模式已选中的源节点
  onExitConnectionMode?: () => void; // 退出连线模式
  leftPanelCollapsed?: boolean; // 左侧面板是否收缩
  onToggleLeftPanel?: () => void; // 切换左侧面板
  rightPanelCollapsed?: boolean; // 右侧面板是否收缩
  onToggleRightPanel?: () => void; // 切换右侧面板
}

// 自定义节点组件 - 角色节点
const CharacterNode: React.FC<NodeProps<WorldNode>> = ({ data }) => {
  return (
    <div className="worldview-node character-node">
      {/* 4个方向的连接点 - 每个方向同时有source和target */}
      <Handle type="source" position={Position.Top} id="top-source" style={{ top: -6 }} />
      <Handle type="target" position={Position.Top} id="top-target" style={{ top: -6 }} />
      <Handle type="source" position={Position.Right} id="right-source" style={{ right: -6 }} />
      <Handle type="target" position={Position.Right} id="right-target" style={{ right: -6 }} />
      <Handle type="source" position={Position.Bottom} id="bottom-source" style={{ bottom: -6 }} />
      <Handle type="target" position={Position.Bottom} id="bottom-target" style={{ bottom: -6 }} />
      <Handle type="source" position={Position.Left} id="left-source" style={{ left: -6 }} />
      <Handle type="target" position={Position.Left} id="left-target" style={{ left: -6 }} />
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
const LocationNode: React.FC<NodeProps<WorldNode>> = ({ data }) => {
  return (
    <div className="worldview-node location-node">
      {/* 4个方向的连接点 - 每个方向同时有source和target */}
      <Handle type="source" position={Position.Top} id="top-source" style={{ top: -6 }} />
      <Handle type="target" position={Position.Top} id="top-target" style={{ top: -6 }} />
      <Handle type="source" position={Position.Right} id="right-source" style={{ right: -6 }} />
      <Handle type="target" position={Position.Right} id="right-target" style={{ right: -6 }} />
      <Handle type="source" position={Position.Bottom} id="bottom-source" style={{ bottom: -6 }} />
      <Handle type="target" position={Position.Bottom} id="bottom-target" style={{ bottom: -6 }} />
      <Handle type="source" position={Position.Left} id="left-source" style={{ left: -6 }} />
      <Handle type="target" position={Position.Left} id="left-target" style={{ left: -6 }} />
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
const SettingNode: React.FC<NodeProps<WorldNode>> = ({ data }) => {
  return (
    <div className="worldview-node setting-node">
      {/* 4个方向的连接点 - 每个方向同时有source和target */}
      <Handle type="source" position={Position.Top} id="top-source" style={{ top: -6 }} />
      <Handle type="target" position={Position.Top} id="top-target" style={{ top: -6 }} />
      <Handle type="source" position={Position.Right} id="right-source" style={{ right: -6 }} />
      <Handle type="target" position={Position.Right} id="right-target" style={{ right: -6 }} />
      <Handle type="source" position={Position.Bottom} id="bottom-source" style={{ bottom: -6 }} />
      <Handle type="target" position={Position.Bottom} id="bottom-target" style={{ bottom: -6 }} />
      <Handle type="source" position={Position.Left} id="left-source" style={{ left: -6 }} />
      <Handle type="target" position={Position.Left} id="left-target" style={{ left: -6 }} />
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
const nodeTypes: NodeTypes = {
  character: CharacterNode,
  location: LocationNode,
  setting: SettingNode,
};

// 边类型映射（自定义贝塞尔曲线边）
const edgeTypes: EdgeTypes = {
  customBezier: CustomBezierEdge,
};

/**
 * 将后端数据转换为 ReactFlow 的 nodes 和 edges
 */
const convertToGraphData = (
  worldData: WorldData, 
  relationships?: Relationship[]
): { nodes: WorldNode[]; edges: WorldEdge[] } => {
  const nodes: WorldNode[] = [];
  const edges: WorldEdge[] = [];

  // 布局配置
  const SPACING_X = 300;
  const SPACING_Y = 200;
  const START_Y = 100;

  // 1. 添加角色节点
  const characters = worldData.characters || [];
  console.log('[convertToGraphData] 开始创建节点，角色数量:', characters.length);
  characters.forEach((character, index) => {
    const nodeId = `character-${character.id}`;
    console.log(`[convertToGraphData] 创建角色节点: ${nodeId} (${character.name})`);
    nodes.push({
      id: nodeId,
      type: 'character',
      position: { x: 100, y: START_Y + index * SPACING_Y },
      data: { 
        label: character.name,
        role: character.role,
        entityId: character.id,
        entityType: 'character',
      },
      className: '', // 后面会动态设置
    });
  });

  // 2. 添加地点节点
  const locations = worldData.locations || [];
  locations.forEach((location, index) => {
    nodes.push({
      id: `location-${location.id}`,
      type: 'location',
      position: { x: 100 + SPACING_X, y: START_Y + index * SPACING_Y },
      data: { 
        label: location.name,
        type: location.type,
        entityId: location.id,
        entityType: 'location',
      },
    });
  });

  // 3. 添加设定节点
  const settings = worldData.settings || [];
  settings.forEach((setting, index) => {
    nodes.push({
      id: `setting-${setting.id}`,
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

  // 4. 添加关系边（从relationships数据）- 智能偏移支持多关系排版
  console.log('[convertToGraphData] 开始创建边，关系数量:', relationships?.length || 0);
  console.log('[convertToGraphData] 当前节点总数:', nodes.length);
  
  // 先分组：找出同一对节点之间的多条边
  const edgeGroups = new Map<string, Relationship[]>();
  
  if (relationships && relationships.length > 0) {
    // 第一遍：按节点对分组
    relationships.forEach((rel) => {
      // 验证关系数据的完整性
      if (!rel.sourceId || !rel.sourceType || !rel.targetId || !rel.targetType) {
        console.warn('[WorldviewGraph] 跳过无效关系（缺少必要字段）:', rel);
        return;
      }
      
      // 后端返回的是驼峰命名
      const sourceNodeId = `${rel.sourceType}-${rel.sourceId}`;
      const targetNodeId = `${rel.targetType}-${rel.targetId}`;
      
      // 验证节点是否存在
      const sourceExists = nodes.some(n => n.id === sourceNodeId);
      const targetExists = nodes.some(n => n.id === targetNodeId);
      
      if (!sourceExists || !targetExists) {
        console.warn(`[WorldviewGraph] 节点不存在，跳过关系: ${sourceNodeId} → ${targetNodeId}`);
        return;
      }
      
      // 创建边组key（不区分方向，A->B和B->A算同一组）
      const groupKey = [sourceNodeId, targetNodeId].sort().join('|');
      
      if (!edgeGroups.has(groupKey)) {
        edgeGroups.set(groupKey, []);
      }
      edgeGroups.get(groupKey)!.push(rel);
    });
    
    // 第二遍：为每组边计算偏移量并创建edges
    edgeGroups.forEach((rels, groupKey) => {
      const edgeCount = rels.length;
      console.log(`[convertToGraphData] 边组 ${groupKey} 有 ${edgeCount} 条边`);
      
      rels.forEach((rel, index) => {
        const sourceNodeId = `${rel.sourceType}-${rel.sourceId}`;
        const targetNodeId = `${rel.targetType}-${rel.targetId}`;
        
        // 计算线条粗细（根据强度1-10映射到1-5px）
        const strokeWidth = 1 + (rel.strength / 10) * 4;
      
        // 获取颜色
        const color =
          rel.color ||
          RELATIONSHIP_COLORS[rel.relationshipType as keyof typeof RELATIONSHIP_COLORS] ||
          RELATIONSHIP_COLORS.DEFAULT;
      
        // 线条样式
        let strokeDasharray = undefined;
        if (rel.lineStyle === 'dashed') {
          strokeDasharray = '10,5';
        } else if (rel.lineStyle === 'dotted') {
          strokeDasharray = '2,4';
        }
        
        // 🎯 终极升级：智能Handle选择 + 自定义贝塞尔曲线
        // undefined = ReactFlow从8个Handle中自动选择最近的
        // 偏移计算逻辑已移至 CustomBezierEdge 组件中
        edges.push({
          id: `rel-${rel.id}`,
          source: sourceNodeId,
          target: targetNodeId,
          
          // 🎯 智能Handle选择：ReactFlow自动选择8个Handle中距离最近的
          sourceHandle: undefined,
          targetHandle: undefined,
          
          // 🎯 使用自定义贝塞尔曲线边（平滑曲线）
          type: 'customBezier',
          
          label: edgeCount > 1 ? `${rel.label} (${index + 1})` : rel.label, // 多条边时显示序号
          animated: rel.strength >= 8,
          style: { 
            stroke: color,
            strokeWidth,
            strokeDasharray,
          },
          
          markerEnd: rel.direction === 'one-way' ? {
            type: MarkerType.ArrowClosed,
            width: 20,
            height: 20,
            color: color,
          } : undefined,
          markerStart: rel.direction === 'two-way' ? {
            type: MarkerType.ArrowClosed,
            width: 20,
            height: 20,
            color: color,
          } : undefined,
          data: {
            relationshipId: rel.id,
            relationshipType: rel.relationshipType,
            description: rel.description,
            strength: rel.strength,
            color,
            lineStyle: rel.lineStyle,
            relationship: rel,
            edgeIndex: index + 1, // 边的索引（从1开始）
            edgeCount: edgeCount, // 总边数
          },
        });
        console.log(`[convertToGraphData] 成功创建边: rel-${rel.id} (${rel.label}) - 使用动态锚点 + 贝塞尔曲线`);
      });
    });
  }

  return { nodes, edges };
};

// 视野控制组件（必须在ReactFlow内部使用）
const ViewportController: React.FC<{ focusNodeToView?: string; nodes: WorldNode[] }> = ({ focusNodeToView, nodes }) => {
  const { fitView } = useReactFlow<WorldNode, WorldEdge>();
  
  useEffect(() => {
    if (focusNodeToView) {
      // 构建完整的节点ID
      const fullNodeId = focusNodeToView.includes('-') 
        ? focusNodeToView 
        : `character-${focusNodeToView}`;
      
      // 检查节点是否存在
      const node = nodes.find(n => 
        n.id === fullNodeId || 
        n.id === `character-${focusNodeToView}` ||
        n.id === `location-${focusNodeToView}` ||
        n.id === `setting-${focusNodeToView}`
      );
      
      if (node) {
        // 定位到节点，带动画效果
        setTimeout(() => {
          fitView({
            nodes: [{ id: node.id }],
            duration: 800,
            padding: 0.3,
          });
        }, 100);
      }
    }
  }, [focusNodeToView, nodes, fitView]);
  
  return null;
};

const WorldviewGraph: React.FC<WorldviewGraphProps> = ({
  worldData,
  relationships,
  editable = false,
  onNodeClick,
  onConnect: onConnectCallback,
  onEdgeClick,
  selectedNodeId,
  layoutConfig,
  onLayoutApplied,
  searchText = '',
  filteredNodeTypes = { character: true, location: true, setting: true },
  focusMode = false,
  focusNodeId,
  focusNodeToView,
  connectionMode = false,
  connectionModeSource,
  onExitConnectionMode,
  leftPanelCollapsed = false,
  onToggleLeftPanel,
  rightPanelCollapsed = false,
  onToggleRightPanel,
}) => {
  const { t } = useTranslation();
  // 转换数据
  const graphData = useMemo(() => convertToGraphData(worldData, relationships), [worldData, relationships]);
  
  const [nodes, setNodes, onNodesChange] = useNodesState<WorldNode>(graphData.nodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState<WorldEdge>(graphData.edges);
  
  // 使用ref保存最新的nodes和edges
  const nodesRef = useRef<WorldNode[]>(nodes);
  const edgesRef = useRef<WorldEdge[]>(edges);
  
  useEffect(() => {
    nodesRef.current = nodes;
    edgesRef.current = edges;
  }, [nodes, edges]);
  
  // 同步外部relationships到edges
  useEffect(() => {
    const newGraphData = convertToGraphData(worldData, relationships);
    setEdges(newGraphData.edges);
  }, [relationships, worldData, setEdges]);
  
  // 应用布局算法
  useEffect(() => {
    if (!layoutConfig || layoutConfig.algorithm === 'custom') return;
    
    const applyLayout = () => {
      let newNodes: WorldNode[] = [];
      
      // 获取当前nodes和edges的快照
      const currentNodes = nodesRef.current;
      const currentEdges = edgesRef.current;
      
      switch (layoutConfig.algorithm) {
        case 'force':
          newNodes = applyForceLayout(currentNodes, currentEdges, layoutConfig) as WorldNode[];
          break;
        case 'hierarchical':
          newNodes = applyHierarchicalLayout(currentNodes, currentEdges, layoutConfig) as WorldNode[];
          break;
        case 'circular':
          newNodes = applyCircularLayout(currentNodes, currentEdges, layoutConfig) as WorldNode[];
          break;
        case 'grid':
          newNodes = applyGridLayout(currentNodes, currentEdges, layoutConfig) as WorldNode[];
          break;
        case 'timeline':
          newNodes = applyTimelineLayout(currentNodes, currentEdges, layoutConfig) as WorldNode[];
          break;
        default:
          return;
      }
      
      // 更新节点位置
      setNodes(newNodes);
      
      // 通知布局应用完成
      if (onLayoutApplied) {
        setTimeout(() => onLayoutApplied(), layoutConfig.duration || 1000);
      }
    };
    
    // 如果启用动画，使用requestAnimationFrame
    if (layoutConfig.animation) {
      requestAnimationFrame(applyLayout);
    } else {
      applyLayout();
    }
  }, [layoutConfig?.algorithm, layoutConfig?.direction, layoutConfig?.spacing]);
  
  // 将filteredNodeTypes转换为稳定的字符串，避免对象引用变化导致无限循环
  const filterKey = `${filteredNodeTypes?.character}-${filteredNodeTypes?.location}-${filteredNodeTypes?.setting}`;
  
  // 搜索过滤和焦点模式逻辑
  useEffect(() => {
    // 计算相关节点ID（用于焦点模式）
    const relatedNodeIds = new Set<string>();
    if (focusMode && focusNodeId) {
      relatedNodeIds.add(focusNodeId);
      
      edgesRef.current.forEach(edge => {
        const sourceId = (edge.source as string).replace(/^(character|location|setting)-/, '');
        const targetId = (edge.target as string).replace(/^(character|location|setting)-/, '');
        
        if (sourceId === focusNodeId) {
          relatedNodeIds.add(targetId);
        }
        if (targetId === focusNodeId) {
          relatedNodeIds.add(sourceId);
        }
      });
    }
    
    // 处理节点
    const processedNodes = nodesRef.current.map((node) => {
      let className = '';
      let hidden = false;
      
      // 1. 检查是否被选中
      if (node.data.entityId === selectedNodeId) {
        className = 'selected-node';
      }
      
      // 2. 检查节点类型过滤
      const nodeType = node.data.entityType as 'character' | 'location' | 'setting';
      if (filteredNodeTypes && !filteredNodeTypes[nodeType]) {
        hidden = true;
      }
      
      // 3. 检查搜索文本匹配
      if (searchText && !hidden) {
        const label = (node.data.label as string | undefined)?.toLowerCase() || '';
        const searchLower = searchText.toLowerCase();
        const matches = label.includes(searchLower);
        
        if (matches) {
          className += ' search-match';
        } else {
          className += ' search-dimmed';
        }
      }
      
      // 4. 焦点模式逻辑
      if (focusMode && focusNodeId) {
        const entityId = node.data.entityId as string;
        if (!relatedNodeIds.has(entityId)) {
          className += ' focus-dimmed';
        } else if (entityId === focusNodeId) {
          className += ' focus-center';
        } else {
          className += ' focus-related';
        }
      }
      
      return {
        ...node,
        className: className.trim(),
        hidden,
      };
    });
    
    // 处理边
    const processedEdges = edgesRef.current.map((edge) => {
      let className = '';
      let hidden = false;
      
      // 焦点模式下，只显示与焦点节点相关的边
      if (focusMode && focusNodeId) {
        const sourceId = (edge.source as string).replace(/^(character|location|setting)-/, '');
        const targetId = (edge.target as string).replace(/^(character|location|setting)-/, '');
        
        if (sourceId !== focusNodeId && targetId !== focusNodeId) {
          hidden = true;
        }
      }
      
      return {
        ...edge,
        className: className.trim(),
        hidden,
      };
    });
    
    // 更新nodes和edges
    setNodes(processedNodes);
    setEdges(processedEdges);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedNodeId, searchText, filterKey, focusMode, focusNodeId]);

  // 提示框状态
  const [showHint, setShowHint] = useState(true);
  const [showHelpButton, setShowHelpButton] = useState(false);

  // 小地图显示状态
  const [showMiniMap, setShowMiniMap] = useState(true);

  // 首次进入显示提示，3秒后自动隐藏
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowHint(false);
      setShowHelpButton(true);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  // 连接节点时触发
  const onConnect = useCallback(
    (params: Connection) => {
      if (!editable || !onConnectCallback) return;
      
      // 从节点ID中提取实际的entityId和entityType
      const sourceNode = nodes.find(n => n.id === params.source);
      const targetNode = nodes.find(n => n.id === params.target);
      
      if (sourceNode && targetNode) {
        const sourceId = sourceNode.data.entityId;
        const sourceType = sourceNode.data.entityType as EntityType;
        const targetId = targetNode.data.entityId;
        const targetType = targetNode.data.entityType as EntityType;
        
        onConnectCallback(sourceId, sourceType, targetId, targetType);
      }
    },
    [editable, onConnectCallback, nodes]
  );
  
  // Edge点击事件
  const onEdgeClickHandler = useCallback(
    (_: React.MouseEvent, edge: Edge<WorldEdgeData>) => {
      if (onEdgeClick && edge.data?.relationshipId) {
        onEdgeClick(edge.data.relationshipId);
      }
    },
    [onEdgeClick]
  );

  // 节点点击事件
  const onNodeClickHandler = useCallback(
    (_: React.MouseEvent, node: WorldNode) => {
      if (onNodeClick && node.data.entityId && node.data.entityType) {
        onNodeClick(node.data.entityId, node.data.entityType);
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
      {/* 连线模式提示条 */}
      {connectionMode && (
        <div className="absolute top-16 left-1/2 transform -translate-x-1/2 z-[60] bg-primary/90 text-primary-foreground border border-primary/30 px-4 py-2 rounded-lg shadow-lg flex items-center gap-3 backdrop-blur-sm animate-in fade-in duration-200 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 bg-primary-foreground rounded-full animate-pulse" />
            <span className="text-sm font-medium">{t('worldview.graph.connectionMode')}</span>
          </div>
          {connectionModeSource && (
            <div className="flex items-center gap-2 px-2.5 py-1 bg-primary-foreground/10 rounded-md">
              <span className="text-xs opacity-80">{t('worldview.graph.selectedSource')}</span>
              <span className="text-sm font-medium">{connectionModeSource.name}</span>
            </div>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={onExitConnectionMode}
            className="text-primary-foreground hover:bg-primary-foreground/10 ml-2 h-7 text-xs"
          >
            <X className="w-3.5 h-3.5 mr-1" />
            {t('worldview.graph.exit')}
          </Button>
        </div>
      )}

      <ReactFlow<WorldNode, WorldEdge>
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={editable ? onConnect : undefined}
        onNodeClick={onNodeClickHandler}
        onEdgeClick={onEdgeClickHandler}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        minZoom={0.2}
        maxZoom={4}
        connectOnClick={editable}
        defaultEdgeOptions={{
          type: 'customBezier',
          animated: false,
        }}
      >
        {/* 视野控制组件 */}
        <ViewportController focusNodeToView={focusNodeToView} nodes={nodes} />
        
        <Background variant={BackgroundVariant.Dots} gap={20} size={1} />

        {/* 缩放控制 */}
        <Controls showInteractive={false}>
          <button
            onClick={() => setShowMiniMap(!showMiniMap)}
            className="minimap-toggle-btn react-flow__controls-button"
            title={showMiniMap ? "隐藏小地图" : "显示小地图"}
          >
            <Layers className="w-4 h-4" style={{ fill: 'currentColor' }} />
          </button>
        </Controls>

        {showMiniMap && (
          <MiniMap
            nodeColor={(node) => {
              switch (node.type) {
                case 'character':
                  return '#3b82f6'; // blue
                case 'location':
                  return '#10b981'; // green
                case 'setting':
                  return '#f59e0b'; // amber
                default:
                  return '#6b7280'; // gray
              }
            }}
            position="bottom-right"
            className="worldview-minimap"
          />
        )}
        
        {/* 统计面板 */}
        <Panel position="top-left" className="worldview-stats-panel">
          {onToggleLeftPanel && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onToggleLeftPanel}
              className="h-7 w-7 p-0 mr-2"
              title={leftPanelCollapsed ? "展开侧边栏" : "收起侧边栏"}
            >
              {leftPanelCollapsed ? <PanelLeft className="w-4 h-4" /> : <PanelLeftClose className="w-4 h-4" />}
            </Button>
          )}
          <div className="stats-item">
            <Users className="w-4 h-4" />
            <span>{stats.characterCount} {t('worldview.graph.characters')}</span>
          </div>
          <div className="stats-item">
            <MapPin className="w-4 h-4" />
            <span>{stats.locationCount} {t('worldview.graph.locations')}</span>
          </div>
          <div className="stats-item">
            <BookOpen className="w-4 h-4" />
            <span>{stats.settingCount} {t('worldview.graph.settings')}</span>
          </div>
        </Panel>

        {/* 自动消失的提示框 */}
        {showHint && (
          <Panel position="top-right" className="worldview-hint-toast">
            <div className="hint-content">
              <span className="hint-icon">💡</span>
              <span className="hint-text">{t('worldview.graph.hint')}</span>
              <button
                onClick={() => setShowHint(false)}
                className="hint-close"
                aria-label={t('worldview.graph.closeHint')}
              >
                <X className="w-3 h-3" />
              </button>
            </div>
          </Panel>
        )}

        {/* 右上角快捷操作（提示消失后显示） */}
        {!showHint && (showHelpButton || (rightPanelCollapsed && onToggleRightPanel)) && (
          <Panel position="top-right" className="worldview-top-right-actions">
            {showHelpButton && (
              <button
                onClick={() => setShowHint(true)}
                className="help-btn"
                title={t('worldview.graph.showHint')}
              >
                <HelpCircle className="w-4 h-4" />
              </button>
            )}
            {rightPanelCollapsed && onToggleRightPanel && (
              <button
                onClick={onToggleRightPanel}
                className="help-btn"
                title="展开侧边栏"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
            )}
          </Panel>
        )}
      </ReactFlow>
    </div>
  );
};

export default WorldviewGraph;
