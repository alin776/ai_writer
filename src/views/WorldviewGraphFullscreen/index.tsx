/**
 * 世界观关系图全屏编辑页面
 * 提供专业的关系图编辑体验
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import {
  ArrowLeft,
  Network,
  Clock,
  Download,
  LayoutGrid,
  Loader,
  ChevronLeft,
  Users,
  MapPin,
  BookOpen,
  Plus,
  Search,
  Filter,
  User,
} from 'lucide-react';
import WorldviewGraph from '@/components/worldview/WorldviewGraph';
import PropertyPanel from '@/components/worldview/PropertyPanel';
import { TimelinePanel } from '@/components/worldview/TimelinePanel';
import { GroupPanel } from '@/components/worldview/GroupPanel';
import { LayoutSelector } from '@/components/worldview/LayoutSelector';
import { SearchPanel, SearchFilter } from '@/components/worldview/SearchPanel';
import { EnhancedNodeList } from '@/components/worldview/EnhancedNodeList';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { 
  LayoutAlgorithm, 
  GlobalLayoutConfig, 
  DEFAULT_LAYOUT_CONFIG,
  applyForceLayout,
  applyHierarchicalLayout,
  applyCircularLayout,
  applyGridLayout,
  applyTimelineLayout,
} from '@/components/worldview/layouts';
import { DataService } from '@/services/DataService';
import { WorldData, Character, Location, Setting } from '@/types/novel';
import { useToast } from '@/hooks/useToast';
import { Relationship, RelationshipFormData, CreateRelationshipData, EntityType } from '@/types/relationship';
import { TimelineEvent, ChapterAnchor } from '@/types/timeline';
import { EntityGroup, CreateEntityGroupData } from '@/types/group';
import { exportGraphAsPng, exportGraphAsSvg, exportGraphAsJson } from '@/utils/exportGraph';

type ViewMode = 'graph' | 'timeline';

const WorldviewGraphFullscreen: React.FC = () => {
  const { workId } = useParams<{ workId: string }>();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const { showToast } = useToast();

  // 状态管理
  const [loading, setLoading] = useState(true);
  const [workTitle, setWorkTitle] = useState('世界观管理');
  const [viewMode, setViewMode] = useState<ViewMode>('graph');
  const [worldData, setWorldData] = useState<WorldData>({
    characters: [],
    locations: [],
    settings: [],
    guidelines: {},
    aiGuidelines: {},
  });
  const [relationships, setRelationships] = useState<Relationship[]>([]);
  
  // 时间线相关状态
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>([]);
  const [chapterAnchors, setChapterAnchors] = useState<ChapterAnchor[]>([]);

  // 分组相关状态
  const [groups, setGroups] = useState<EntityGroup[]>([]);
  const [leftPanelTab, setLeftPanelTab] = useState<'nodes' | 'groups'>('nodes'); // 左侧面板Tab
  const [leftPanelCollapsed, setLeftPanelCollapsed] = useState(false); // 左侧面板收缩状态
  const [rightPanelCollapsed, setRightPanelCollapsed] = useState(false); // 右侧面板收缩状态
  const toggleRightPanel = () => setRightPanelCollapsed((prev) => !prev);

  // 布局相关状态
  const [currentLayout, setCurrentLayout] = useState<LayoutAlgorithm>('force');
  const [layoutConfig, setLayoutConfig] = useState<GlobalLayoutConfig>(DEFAULT_LAYOUT_CONFIG);

  // 导出相关状态
  const [exporting, setExporting] = useState(false);
  
  // 搜索和焦点模式状态
  const [searchFilter, setSearchFilter] = useState<SearchFilter>({
    searchText: '',
    nodeTypes: { character: true, location: true, setting: true },
    tags: [],
  });
  const [searchText, setSearchText] = useState(''); // 内联搜索文本
  const [nodeTypeFilter, setNodeTypeFilter] = useState<EntityType | 'all'>('all'); // 节点类型筛选
  const [focusMode, setFocusMode] = useState(false); // 焦点模式（简化版）
  const [focusModeEnabled, setFocusModeEnabled] = useState(false);
  const [focusNodeId, setFocusNodeId] = useState<string | undefined>(undefined);
  const [focusNodeToView, setFocusNodeToView] = useState<string | undefined>(undefined);
  
  // 编辑关系状态（用于属性面板编辑按钮）
  const [editingRelationship, setEditingRelationship] = useState<Relationship | null>(null);

  // 待确认的连接（用于显示临时边缘）
  const [pendingConnection, setPendingConnection] = useState<{
    sourceId: string;
    sourceType: EntityType;
    targetId: string;
    targetType: EntityType;
  } | null>(null);

  // 连线模式和选中状态
  const [connectionMode, setConnectionMode] = useState(false); // 是否开启连线模式
  const [selectedNode, setSelectedNode] = useState<{
    id: string;
    type: EntityType;
    label: string;
  } | null>(null);

  // 属性面板状态
  const [panelMode, setPanelMode] = useState<'idle' | 'node' | 'relationship' | 'create' | 'timeline' | 'createTimeline'>('idle');
  const [panelNodeData, setPanelNodeData] = useState<{
    id: string;
    type: EntityType;
    entity: Character | Location | Setting;
    initialEditMode?: boolean;
  } | null>(null);
  const [panelRelationshipData, setPanelRelationshipData] = useState<{
    relationship: Relationship;
    sourceLabel: string;
    targetLabel: string;
  } | null>(null);
  const [panelCreateRelationshipData, setPanelCreateRelationshipData] = useState<{
    sourceId: string;
    sourceType: EntityType;
    sourceLabel: string;
    targetId: string;
    targetType: EntityType;
    targetLabel: string;
  } | null>(null);
  const [panelTimelineEventData, setPanelTimelineEventData] = useState<{
    event: TimelineEvent;
    entityLabel: string;
  } | null>(null);
  const [panelCreateTimelineEventData, setPanelCreateTimelineEventData] = useState<{
    workId: string;
    entityId?: string;
    entityType?: EntityType;
    entityLabel?: string;
  } | null>(null);

  // 加载数据
  useEffect(() => {
    if (workId) {
      loadData();
    }
  }, [workId]);

  const loadData = async () => {
    if (!workId) return;

    try {
      setLoading(true);

      // 并发加载所有数据
      const [work, characters, locations, settings, guidelines, aiGuidelines, relationshipsData, timelineEventsData, chapterAnchorsData, groupsData] = await Promise.all([
        DataService.getWork(workId),
        DataService.getCharacters(workId),
        DataService.getLocations(workId),
        DataService.getSettings(workId),
        DataService.getGuidelines(workId).catch(() => undefined),
        DataService.getAIGuidelines(workId).catch(() => undefined),
        DataService.getRelationships(workId).catch(() => []),
        DataService.getTimelineEvents(workId).catch(() => []),
        DataService.getChapterAnchors(workId).catch(() => []),
        DataService.getWorkGroups(workId).catch(() => []),
      ]);

      setWorkTitle(work.title);
      setWorldData({
        characters,
        locations,
        settings,
        guidelines: guidelines ?? undefined,
        aiGuidelines: aiGuidelines ?? undefined,
      });
      
      // 调试：打印后端返回的关系数据
      console.log('=== 后端返回的关系数据 ===');
      console.log('关系数量:', relationshipsData.length);
      if (relationshipsData.length > 0) {
        console.log('第一条关系完整数据:', relationshipsData[0]);
        console.log('字段名列表:', Object.keys(relationshipsData[0]));
        console.log('sourceId:', relationshipsData[0].sourceId);
        console.log('sourceType:', relationshipsData[0].sourceType);
        console.log('targetId:', relationshipsData[0].targetId);
        console.log('targetType:', relationshipsData[0].targetType);
      }
      
      // 调试：打印实体数据，用于验证节点ID
      console.log('=== 实体数据 ===');
      console.log('角色数量:', characters.length);
      console.log('所有角色ID列表:');
      characters.forEach((c, i) => {
        console.log(`  角色${i+1}: ${c.id} - ${c.name}`);
      });
      
      console.log('地点数量:', locations.length);
      console.log('设定数量:', settings.length);
      
      // 验证关系引用的角色是否存在
      if (relationshipsData.length > 0) {
        console.log('\n=== 验证关系引用的实体 ===');
        relationshipsData.forEach((rel, i) => {
          const sourceExists = characters.find(c => c.id === rel.sourceId) ||
                               locations.find(l => l.id === rel.sourceId) ||
                               settings.find(s => s.id === rel.sourceId);
          const targetExists = characters.find(c => c.id === rel.targetId) ||
                               locations.find(l => l.id === rel.targetId) ||
                               settings.find(s => s.id === rel.targetId);
          
          console.log(`关系${i+1}: ${rel.label}`);
          console.log(`  源(${rel.sourceType}): ${rel.sourceId} - ${sourceExists ? '✅存在' : '❌不存在'}`);
          console.log(`  目标(${rel.targetType}): ${rel.targetId} - ${targetExists ? '✅存在' : '❌不存在'}`);
        });
      }
      
      setRelationships(relationshipsData);
      setTimelineEvents(timelineEventsData);
      setChapterAnchors(chapterAnchorsData);
      setGroups(groupsData);
      
      console.log('=== 时间线数据 ===');
      console.log('事件数量:', timelineEventsData.length);
      console.log('章节锚点数量:', chapterAnchorsData.length);
    } catch (error) {
      console.error('加载世界观数据失败:', error);
      showToast('error', '加载失败');
    } finally {
      setLoading(false);
    }
  };

  // 处理 URL 参数，自动打开详情面板
  useEffect(() => {
    if (loading) return; // 等待数据加载完成

    const type = searchParams.get('type') as EntityType | null;
    const id = searchParams.get('id');

    if (type && id) {
      const entity = getNodeData(id, type);
      if (entity) {
        // 打开属性面板显示详情
        setPanelNodeData({ id, type, entity });
        setPanelMode('node');
        // 定位到该节点
        setFocusNodeToView(`${type}-${id}`);
        // 清除 URL 参数，避免刷新时重复触发
        setSearchParams({}, { replace: true });
      }
    }
  }, [loading, searchParams, worldData]);

  // 获取节点标签
  const getNodeLabel = (nodeId: string, nodeType: EntityType): string => {
    if (nodeType === 'character') {
      const char = worldData.characters.find(c => c.id === nodeId);
      return char?.name || '';
    } else if (nodeType === 'location') {
      const loc = worldData.locations.find(l => l.id === nodeId);
      return loc?.name || '';
    } else if (nodeType === 'setting') {
      const set = worldData.settings.find(s => s.id === nodeId);
      return set?.title || '';
    }
    return '';
  };

  // 获取节点数据
  const getNodeData = (nodeId: string, nodeType: EntityType): Character | Location | Setting | null => {
    if (nodeType === 'character') {
      return worldData.characters.find(c => c.id === nodeId) || null;
    } else if (nodeType === 'location') {
      return worldData.locations.find(l => l.id === nodeId) || null;
    } else if (nodeType === 'setting') {
      return worldData.settings.find(s => s.id === nodeId) || null;
    }
    return null;
  };

  // 处理节点点击（点击选中模式）
  const handleNodeClickForConnection = (nodeId: string, nodeType: EntityType) => {
    // 焦点模式下：设置焦点节点
    if (focusModeEnabled) {
      setFocusNodeId(nodeId);
      const nodeLabel = getNodeLabel(nodeId, nodeType);
      showToast('success', `焦点模式：聚焦于 ${nodeLabel}`);
      return;
    }
    
    // 在连线模式下处理连线
    if (connectionMode) {
    
    const nodeLabel = getNodeLabel(nodeId, nodeType);
    
    if (!selectedNode) {
      // 第一次点击：选中节点
      setSelectedNode({ id: nodeId, type: nodeType, label: nodeLabel });
      showToast('info', `已选中 ${nodeLabel}，请点击目标节点建立关系`);
    } else if (selectedNode.id === nodeId) {
      // 点击同一个节点：取消选中
      setSelectedNode(null);
      showToast('info', '已取消选中');
    } else {
      // 第二次点击不同节点：在属性面板显示创建关系表单
      // 设置待确认连接（显示临时边缘）
      setPendingConnection({
        sourceId: selectedNode.id,
        sourceType: selectedNode.type,
        targetId: nodeId,
        targetType: nodeType,
      });
      setPanelCreateRelationshipData({
        sourceId: selectedNode.id,
        sourceType: selectedNode.type,
        sourceLabel: selectedNode.label,
        targetId: nodeId,
        targetType: nodeType,
        targetLabel: nodeLabel,
      });
      setPanelMode('create');
      setSelectedNode(null); // 清除选中状态
      setConnectionMode(false); // 退出连线模式
    }
      return;
    }
    
    // 非连线模式：显示节点详情
    const entity = getNodeData(nodeId, nodeType);
    if (entity) {
      setPanelNodeData({ id: nodeId, type: nodeType, entity });
      setPanelMode('node');
    }
  };
  
  // 切换连线模式
  const toggleConnectionMode = () => {
    if (connectionMode) {
      // 关闭连线模式，清除选中状态
      setConnectionMode(false);
      setSelectedNode(null);
      showToast('info', '已退出连线模式');
    } else {
      // 开启连线模式
      setConnectionMode(true);
      showToast('success', '已进入连线模式，点击两个节点建立关系');
    }
  };

  // 导出功能
  const handleExport = async (format: 'png' | 'svg' | 'json') => {
    setExporting(true);
    
    try {
      if (format === 'json') {
        // 导出JSON数据
        const exportData = {
          workId,
          workTitle,
          worldData,
          relationships,
          timelineEvents,
          chapterAnchors,
          groups,
          exportDate: new Date().toISOString(),
        };
        exportGraphAsJson(exportData, `${workTitle}-世界观数据.json`);
        showToast('success', 'JSON 数据导出成功');
      } else {
        // 导出PNG或SVG图片
        const graphElement = document.querySelector('.react-flow') as HTMLElement;
        if (!graphElement) {
          throw new Error('找不到图谱元素');
        }
        
        if (format === 'png') {
          await exportGraphAsPng(graphElement, `${workTitle}-世界观图谱.png`);
          showToast('success', 'PNG 图片导出成功');
        } else {
          await exportGraphAsSvg(graphElement, `${workTitle}-世界观图谱.svg`);
          showToast('success', 'SVG 图片导出成功');
        }
      }
    } catch (error: any) {
      console.error('导出失败:', error);
      showToast('error', error.message || '导出失败');
    } finally {
      setExporting(false);
    }
  };
  
  // 处理连接创建（拖拽连线）
  const handleConnect = (sourceId: string, sourceType: EntityType, targetId: string, targetType: EntityType) => {
    // 拖拽连线时，设置待确认连接并打开属性面板
    const sourceLabel = getNodeLabel(sourceId, sourceType);
    const targetLabel = getNodeLabel(targetId, targetType);

    // 设置待确认连接（显示临时边缘）
    setPendingConnection({ sourceId, sourceType, targetId, targetType });

    setPanelCreateRelationshipData({
      sourceId,
      sourceType,
      sourceLabel,
      targetId,
      targetType,
      targetLabel,
    });
    setPanelMode('create');
  };

  // 删除关系
  const handleDeleteRelationship = async (relationshipId: string) => {
    try {
      await DataService.deleteRelationship(relationshipId);
      setRelationships(relationships.filter(r => r.id !== relationshipId));
      showToast('success', '关系已删除');
    } catch (error) {
      console.error('删除关系失败:', error);
      showToast('error', '删除失败');
    }
  };

  // 返回作品详情页面
  const handleBack = () => {
    navigate(`/works/${workId}`);
  };

  // 获取布局名称
  const getLayoutName = (algorithm: LayoutAlgorithm): string => {
    const names: Record<LayoutAlgorithm, string> = {
      force: '力导向布局',
      hierarchical: '层级布局',
      circular: '环形布局',
      grid: '网格布局',
      timeline: '时间线布局',
      custom: '自定义布局',
    };
    return names[algorithm];
  };

  // 布局切换
  const handleLayoutChange = (algorithm: LayoutAlgorithm) => {
    setCurrentLayout(algorithm);
    const newConfig = { ...layoutConfig, algorithm };
    setLayoutConfig(newConfig);
    showToast('info', `正在应用${getLayoutName(algorithm)}...`);
  };

  // 统计数据
  const stats = {
    characters: worldData.characters.length,
    locations: worldData.locations.length,
    settings: worldData.settings.length,
    relationships: relationships.length,
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <Loader className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-2" />
          <p className="text-sm text-gray-500">加载中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-background text-sm">
      {/* 顶部导航栏 */}
      <header className="h-14 border-b border-border-light bg-card/50 backdrop-blur-md flex items-center justify-between px-5">
        {/* 左侧区域 */}
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={handleBack} className="hover:bg-accent h-8 w-8 p-0">
            <ArrowLeft className="w-4 h-4" />
          </Button>
          <div className="h-6 w-px bg-border-light" />
          <div>
            <div className="text-foreground text-2xl font-semibold tracking-wide" style={{ fontFamily: "'Ma Shan Zheng', cursive" }}>{workTitle}</div>

          </div>
        </div>

        {/* 中央区域 - 视图切换 */}
        <div className="flex items-center gap-2">
          <Button
            variant={viewMode === 'graph' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('graph')}
            className={`h-8 text-sm ${viewMode === 'graph' ? 'shadow-sm' : ''}`}
          >
            <Network className="w-3.5 h-3.5 mr-1.5" />
            关系图
          </Button>
          <Button
            variant={viewMode === 'timeline' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('timeline')}
            className={`h-8 text-sm ${viewMode === 'timeline' ? 'shadow-sm' : ''}`}
          >
            <Clock className="w-3.5 h-3.5 mr-1.5" />
            时间线
          </Button>
        </div>

        {/* 右侧操作区 */}
        <div className="flex items-center gap-2">
          {viewMode === 'graph' ? (
            <>
              {/* 创建关系按钮 */}
              <Button
                variant={connectionMode ? 'default' : 'outline'}
                size="sm"
                onClick={toggleConnectionMode}
                className={`h-8 text-sm ${connectionMode ? 'shadow-md' : ''}`}
              >
                <Plus className="w-3.5 h-3.5 mr-1.5" />
                {connectionMode ? '连线中' : '创建关系'}
              </Button>
            </>
          ) : (
            <Button size="sm" onClick={() => {
              setPanelCreateTimelineEventData({
                workId: workId!,
              });
              setPanelMode('createTimeline');
            }} className="h-8 text-sm">
              <Plus className="w-3.5 h-3.5 mr-1.5" />
              创建事件
            </Button>
          )}

          {viewMode === 'graph' && (
            <>
              {/* 搜索面板 - 胶囊样式 */}
              <div className="flex items-center gap-1.5 border border-input bg-background hover:bg-accent/50 rounded-md px-3 h-8 transition-colors">
                <Search className="w-3.5 h-3.5 text-muted-foreground flex-shrink-0" />
                <Input
                  placeholder="搜索角色、地点、设定..."
                  value={searchText}
                  onChange={(e) => setSearchText(e.target.value)}
                  className="w-40 border-0 bg-transparent h-6 text-sm focus-visible:ring-0 focus-visible:ring-offset-0 px-0"
                />
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <button
                      className="h-6 w-6 p-0 hover:bg-accent rounded flex items-center justify-center flex-shrink-0"
                      title="节点类型筛选"
                    >
                      <Filter className={`w-3.5 h-3.5 ${nodeTypeFilter === 'all' ? 'text-muted-foreground' : 'text-primary'}`} />
                    </button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end" className="w-36">
                    <DropdownMenuItem
                      onClick={() => setNodeTypeFilter('all')}
                      className={nodeTypeFilter === 'all' ? 'bg-accent' : ''}
                    >
                      <span className="w-4 h-4 mr-2 flex items-center justify-center">
                        {nodeTypeFilter === 'all' && '✓'}
                      </span>
                      全部
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      onClick={() => setNodeTypeFilter('character')}
                      className={nodeTypeFilter === 'character' ? 'bg-accent' : ''}
                    >
                      <User className="w-4 h-4 mr-2 text-character" />
                      角色
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      onClick={() => setNodeTypeFilter('location')}
                      className={nodeTypeFilter === 'location' ? 'bg-accent' : ''}
                    >
                      <MapPin className="w-4 h-4 mr-2 text-location" />
                      地点
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      onClick={() => setNodeTypeFilter('setting')}
                      className={nodeTypeFilter === 'setting' ? 'bg-accent' : ''}
                    >
                      <BookOpen className="w-4 h-4 mr-2 text-setting" />
                      设定
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
                <button
                  onClick={() => setFocusMode(!focusMode)}
                  className="h-6 w-6 p-0 hover:bg-accent rounded flex items-center justify-center flex-shrink-0"
                  title={focusMode ? "关闭焦点模式" : "开启焦点模式"}
                >
                  <div className={`w-3.5 h-3.5 rounded-full border-2 transition-colors ${
                    focusMode ? 'border-primary bg-primary' : 'border-muted-foreground'
                  }`}>
                    {focusMode && (
                      <div className="w-full h-full flex items-center justify-center">
                        <div className="w-1 h-1 rounded-full bg-white" />
                      </div>
                    )}
                  </div>
                </button>
              </div>

              {/* 布局选择器 */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm" className="h-8 text-sm">
                    <LayoutGrid className="w-3.5 h-3.5 mr-1.5" />
                    布局
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem onClick={() => handleLayoutChange('force')}>
                    力导向布局
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handleLayoutChange('hierarchical')}>
                    层级布局
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handleLayoutChange('circular')}>
                    环形布局
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handleLayoutChange('grid')}>
                    网格布局
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handleLayoutChange('timeline')}>
                    时间线布局
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </>
          )}

        </div>
      </header>

      {/* Main Content - 三栏布局 */}
      <div className="flex flex-1 overflow-hidden min-h-0">
        {/* 左侧边栏 */}
        {!leftPanelCollapsed && (
          <div className="w-56 border-r border-border-light bg-card flex flex-col overflow-hidden min-h-0">
            <Tabs value={leftPanelTab} onValueChange={(value) => setLeftPanelTab(value as 'nodes' | 'groups')} className="flex-1 flex flex-col min-h-0">
              <TabsContent value="nodes" className="flex-1 min-h-0 mt-0 data-[state=active]:flex data-[state=active]:flex-col">
                <EnhancedNodeList
                characters={worldData.characters}
                locations={worldData.locations}
                settings={worldData.settings}
                relationships={relationships}
                onNodeClick={(nodeId, nodeType) => {
                  // 单击：在图中高亮并定位
                  setSelectedNode({
                    id: nodeId,
                    type: nodeType,
                    label: getNodeLabel(nodeId, nodeType),
                  });
                  // 触发视野移动
                  setFocusNodeToView(`${nodeType}-${nodeId}`);
                  showToast('info', `已定位到 ${getNodeLabel(nodeId, nodeType)}`);
                }}
                onNodeDoubleClick={(nodeId, nodeType) => {
                  // 双击：打开右侧属性面板
                  const entity = getNodeData(nodeId, nodeType);
                  if (entity) {
                    setPanelNodeData({ id: nodeId, type: nodeType, entity });
                    setPanelMode('node');
                    showToast('success', `查看详情：${getNodeLabel(nodeId, nodeType)}`);
                  }
                }}
                onFocusNode={(nodeId, nodeType) => {
                  // 焦点模式聚焦
                  if (!focusModeEnabled) {
                    setFocusModeEnabled(true);
                  }
                  setFocusNodeId(nodeId);
                  showToast('success', `焦点模式：聚焦于 ${getNodeLabel(nodeId, nodeType)}`);
                }}
                onCreateCharacter={async () => {
                  try {
                    const newCharacter = await DataService.createCharacter({
                      workId: workId!,
                      name: '新角色',
                      description: '请添加角色描述',
                      role: '',
                      tags: [],
                      relationships: [],
                    });
                    setWorldData(prev => ({
                      ...prev,
                      characters: [...prev.characters, newCharacter],
                    }));
                    // 自动打开属性面板并进入编辑模式
                    setPanelNodeData({ 
                      id: newCharacter.id, 
                      type: 'character', 
                      entity: newCharacter,
                      initialEditMode: true 
                    });
                    setPanelMode('node');
                    showToast('success', '角色创建成功，请编辑详细信息');
                  } catch (error) {
                    console.error('创建角色失败:', error);
                    showToast('error', '创建失败');
                  }
                }}
                onCreateLocation={async () => {
                  try {
                    const newLocation = await DataService.createLocation({
                      workId: workId!,
                      name: '新地点',
                      description: '请添加地点描述',
                      type: '',
                      tags: [],
                    });
                    setWorldData(prev => ({
                      ...prev,
                      locations: [...prev.locations, newLocation],
                    }));
                    // 自动打开属性面板并进入编辑模式
                    setPanelNodeData({ 
                      id: newLocation.id, 
                      type: 'location', 
                      entity: newLocation,
                      initialEditMode: true 
                    });
                    setPanelMode('node');
                    showToast('success', '地点创建成功，请编辑详细信息');
                  } catch (error) {
                    console.error('创建地点失败:', error);
                    showToast('error', '创建失败');
                  }
                }}
                onCreateSetting={async () => {
                  try {
                    const newSetting = await DataService.createSetting({
                      workId: workId!,
                      title: '新设定',
                      category: '',
                      content: '请添加设定内容',
                      tags: [],
                    });
                    setWorldData(prev => ({
                      ...prev,
                      settings: [...prev.settings, newSetting],
                    }));
                    // 自动打开属性面板并进入编辑模式
                    setPanelNodeData({ 
                      id: newSetting.id, 
                      type: 'setting', 
                      entity: newSetting,
                      initialEditMode: true 
                    });
                    setPanelMode('node');
                    showToast('success', '设定创建成功，请编辑详细信息');
                  } catch (error) {
                    console.error('创建设定失败:', error);
                    showToast('error', '创建失败');
                  }
                }}
                onOpenGroupPanel={() => setLeftPanelTab('groups')}
                onCollapsePanel={() => setLeftPanelCollapsed(true)}
              />
            </TabsContent>
            <TabsContent value="groups" className="flex-1 min-h-0 mt-0 data-[state=active]:flex data-[state=active]:flex-col">
              <GroupPanel
                workId={workId!}
                groups={groups}
                characters={worldData.characters}
                locations={worldData.locations}
                settings={worldData.settings}
                onCreateGroup={async (data: CreateEntityGroupData) => {
                  try {
                    const newGroup = await DataService.createGroup(data);
                    setGroups(prev => [...prev, newGroup]);
                    showToast('success', '分组创建成功');
                  } catch (error) {
                    console.error('创建分组失败:', error);
                    showToast('error', '创建失败');
                  }
                }}
                onUpdateGroup={async (groupId: string, data: any) => {
                  try {
                    const updatedGroup = await DataService.updateGroup(groupId, data);
                    setGroups(prev => prev.map(g => g.id === groupId ? updatedGroup : g));
                    showToast('success', '分组已更新');
                  } catch (error) {
                    console.error('更新分组失败:', error);
                    showToast('error', '更新失败');
                  }
                }}
                onDeleteGroup={async (groupId: string) => {
                  try {
                    await DataService.deleteGroup(groupId);
                    setGroups(prev => prev.filter(g => g.id !== groupId));
                    showToast('success', '分组已删除');
                  } catch (error) {
                    console.error('删除分组失败:', error);
                    showToast('error', '删除失败');
                  }
                }}
                onAddMembers={async (groupId: string, members: any[]) => {
                  try {
                    const addedMembers = await DataService.addGroupMembers(groupId, members);
                    setGroups(prev => prev.map(g => 
                      g.id === groupId ? { ...g, members: [...g.members, ...addedMembers] } : g
                    ));
                    showToast('success', '成员已添加');
                  } catch (error) {
                    console.error('添加成员失败:', error);
                    showToast('error', '添加失败');
                  }
                }}
                onRemoveMember={async (groupId: string, memberId: string) => {
                  try {
                    await DataService.removeGroupMember(groupId, memberId);
                    setGroups(prev => prev.map(g =>
                      g.id === groupId ? { ...g, members: g.members.filter(m => m.id !== memberId) } : g
                    ));
                    showToast('success', '成员已移除');
                  } catch (error) {
                    console.error('移除成员失败:', error);
                    showToast('error', '移除失败');
                  }
                }}
                onBackToNodeList={() => setLeftPanelTab('nodes')}
                onCreateCharacter={async () => {
                  try {
                    const newCharacter = await DataService.createCharacter({
                      workId: workId!,
                      name: '新角色',
                      description: '请添加角色描述',
                      role: '',
                      tags: [],
                      relationships: [],
                    });
                    setWorldData(prev => ({
                      ...prev,
                      characters: [...prev.characters, newCharacter],
                    }));
                    setPanelNodeData({
                      id: newCharacter.id,
                      type: 'character',
                      entity: newCharacter,
                      initialEditMode: true
                    });
                    setPanelMode('node');
                    setLeftPanelTab('nodes');
                    showToast('success', '角色创建成功，请编辑详细信息');
                  } catch (error) {
                    console.error('创建角色失败:', error);
                    showToast('error', '创建失败');
                  }
                }}
                onCreateLocation={async () => {
                  try {
                    const newLocation = await DataService.createLocation({
                      workId: workId!,
                      name: '新地点',
                      description: '请添加地点描述',
                      type: '',
                      tags: [],
                    });
                    setWorldData(prev => ({
                      ...prev,
                      locations: [...prev.locations, newLocation],
                    }));
                    setPanelNodeData({
                      id: newLocation.id,
                      type: 'location',
                      entity: newLocation,
                      initialEditMode: true
                    });
                    setPanelMode('node');
                    setLeftPanelTab('nodes');
                    showToast('success', '地点创建成功，请编辑详细信息');
                  } catch (error) {
                    console.error('创建地点失败:', error);
                    showToast('error', '创建失败');
                  }
                }}
                onCreateSetting={async () => {
                  try {
                    const newSetting = await DataService.createSetting({
                      workId: workId!,
                      title: '新设定',
                      category: '',
                      content: '请添加设定内容',
                      tags: [],
                    });
                    setWorldData(prev => ({
                      ...prev,
                      settings: [...prev.settings, newSetting],
                    }));
                    setPanelNodeData({
                      id: newSetting.id,
                      type: 'setting',
                      entity: newSetting,
                      initialEditMode: true
                    });
                    setPanelMode('node');
                    setLeftPanelTab('nodes');
                    showToast('success', '设定创建成功，请编辑详细信息');
                  } catch (error) {
                    console.error('创建设定失败:', error);
                    showToast('error', '创建失败');
                  }
                }}
              />
            </TabsContent>
          </Tabs>
        </div>
        )}

        {/* Main Canvas - 主画布 */}
        <div className="flex-1 overflow-hidden h-full relative">
          {viewMode === 'timeline' && rightPanelCollapsed && panelMode !== 'idle' && (
            <div className="absolute top-3 right-3 z-20">
              <button
                onClick={toggleRightPanel}
                className="help-btn"
                title="展开侧边栏"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
            </div>
          )}
          {viewMode === 'graph' ? (
            <WorldviewGraph
              worldData={worldData}
              relationships={relationships}
              editable={true}
              onConnect={handleConnect}
              onNodeClick={handleNodeClickForConnection}
              onEdgeClick={(relationshipId) => {
                // 点击关系线，显示在属性面板
                const rel = relationships.find(r => r.id === relationshipId);
                if (rel) {
                  const sourceLabel = getNodeLabel(rel.sourceId, rel.sourceType);
                  const targetLabel = getNodeLabel(rel.targetId, rel.targetType);
                  setPanelRelationshipData({ relationship: rel, sourceLabel, targetLabel });
                  setPanelMode('relationship');
                }
              }}
              selectedNodeId={selectedNode?.id}
              layoutConfig={layoutConfig}
              onLayoutApplied={() => {
                showToast('success', `${getLayoutName(currentLayout)}已应用`);
              }}
              searchText={searchText}
              filteredNodeTypes={{
                character: nodeTypeFilter === 'all' || nodeTypeFilter === 'character',
                location: nodeTypeFilter === 'all' || nodeTypeFilter === 'location',
                setting: nodeTypeFilter === 'all' || nodeTypeFilter === 'setting',
              }}
              focusMode={focusModeEnabled}
              focusNodeId={focusNodeId}
              focusNodeToView={focusNodeToView}
              connectionMode={connectionMode}
              connectionModeSource={selectedNode ? { id: selectedNode.id, name: selectedNode.label, type: selectedNode.type } : undefined}
              onExitConnectionMode={toggleConnectionMode}
              leftPanelCollapsed={leftPanelCollapsed}
              onToggleLeftPanel={() => setLeftPanelCollapsed(!leftPanelCollapsed)}
              rightPanelCollapsed={rightPanelCollapsed}
              onToggleRightPanel={toggleRightPanel}
              pendingConnection={pendingConnection}
            />
          ) : (
            <TimelinePanel
              workId={workId!}
              events={timelineEvents}
              chapters={chapterAnchors}
              characters={worldData.characters}
              locations={worldData.locations}
              settings={worldData.settings}
              relationships={relationships}
              onAddEvent={() => {
                // 打开创建时间线事件面板
                setPanelCreateTimelineEventData({
                  workId: workId!,
                });
                setPanelMode('createTimeline');
              }}
              onEditEvent={(event: TimelineEvent) => {
                // 在属性面板显示事件详情
                const entity = worldData.characters.find(c => c.id === event.entityId) ||
                              worldData.locations.find(l => l.id === event.entityId) ||
                              worldData.settings.find(s => s.id === event.entityId);

                const entityLabel = event.entityType === 'character' ? (entity as Character)?.name :
                                   event.entityType === 'location' ? (entity as Location)?.name :
                                   (entity as Setting)?.title || '未知实体';

                setPanelTimelineEventData({ event, entityLabel });
                setPanelMode('timeline');
              }}
              onDeleteEvent={async (eventId: string) => {
                if (confirm('确定要删除这个时间线事件吗？')) {
                  try {
                    await DataService.deleteTimelineEvent(eventId);
                    setTimelineEvents(prev => prev.filter(e => e.id !== eventId));
                    showToast('success', '时间线事件已删除');
                  } catch (error) {
                    console.error('删除时间线事件失败:', error);
                    showToast('error', '删除失败');
                  }
                }
              }}
              onEventClick={(event: TimelineEvent) => {
                // 点击时间线事件，在属性面板显示详情
                const entity = worldData.characters.find(c => c.id === event.entityId) ||
                              worldData.locations.find(l => l.id === event.entityId) ||
                              worldData.settings.find(s => s.id === event.entityId);

                const entityLabel = event.entityType === 'character' ? (entity as Character)?.name :
                                   event.entityType === 'location' ? (entity as Location)?.name :
                                   (entity as Setting)?.title || '未知实体';

                setPanelTimelineEventData({ event, entityLabel });
                setPanelMode('timeline');
              }}
            />
          )}
        </div>

        {/* Right Panel - 右侧属性面板 */}
        <div className={`h-full transition-all duration-300 overflow-hidden ${rightPanelCollapsed ? 'w-0' : 'w-80'}`}>
          {!rightPanelCollapsed && (
            <PropertyPanel
              mode={panelMode}
              nodeData={panelNodeData}
              relationshipData={panelRelationshipData}
              createRelationshipData={panelCreateRelationshipData}
              stats={{
                characters: stats.characters,
                locations: stats.locations,
                settings: stats.settings,
                relationships: stats.relationships,
                relationshipsByType: relationships.reduce((acc, rel) => {
                  acc[rel.relationshipType] = (acc[rel.relationshipType] || 0) + 1;
                  return acc;
                }, {} as Record<string, number>),
              }}
              relatedRelationships={relationships}
              isCollapsed={rightPanelCollapsed}
              onToggleCollapse={toggleRightPanel}
              onClose={() => {
                setPanelMode('idle');
                setPanelNodeData(null);
                setPanelRelationshipData(null);
                setPanelCreateRelationshipData(null);
                setPanelTimelineEventData(null);
                setPanelCreateTimelineEventData(null);
                setPendingConnection(null); // 清除临时连接线
              }}
              onSaveNode={async (updatedEntity) => {
              if (panelNodeData) {
                const { type } = panelNodeData;
                const typeName = type === 'character' ? '角色' : type === 'location' ? '地点' : '设定';
                
                try {
                  if (type === 'character') {
                    await DataService.updateCharacter(updatedEntity.id, updatedEntity as Character);
                  } else if (type === 'location') {
                    await DataService.updateLocation(updatedEntity.id, updatedEntity as Location);
                  } else if (type === 'setting') {
                    await DataService.updateSetting(updatedEntity.id, updatedEntity as Setting);
                  }
                  
                  showToast('success', `${typeName}已更新`);
                  // 重新加载数据
                  await loadData();
                  // 更新面板数据
                  setPanelNodeData({ ...panelNodeData, entity: updatedEntity });
                } catch (error) {
                  console.error('更新失败:', error);
                  showToast('error', '更新失败');
                  throw error; // 让PropertyPanel知道保存失败
                }
              }
            }}
            onCreateRelationship={async (formData) => {
              if (!panelCreateRelationshipData || !workId) {
                showToast('error', '缺少作品ID或来源信息');
                return;
              }

              try {
                const createData: CreateRelationshipData = {
                  work_id: workId,
                  source_id: panelCreateRelationshipData.sourceId,
                  source_type: panelCreateRelationshipData.sourceType,
                  target_id: panelCreateRelationshipData.targetId,
                  target_type: panelCreateRelationshipData.targetType,
                  relationship_type: formData.relationshipType,
                  label: formData.label,
                  description: formData.description,
                  strength: formData.strength,
                  direction: formData.direction,
                  color: formData.color,
                  line_style: formData.lineStyle,
                };
                
                const newRelationship = await DataService.createRelationship(createData);
                console.log('新创建的关系:', newRelationship);
                // 立即更新关系列表，触发重新渲染
                setRelationships(prev => {
                  const updated = [...prev, newRelationship];
                  console.log('更新后的关系列表:', updated);
                  return updated;
                });
                showToast('success', '关系创建成功');

                // 关闭面板并清除临时连接线
                setPanelMode('idle');
                setPanelCreateRelationshipData(null);
                setPendingConnection(null);
              } catch (error: any) {
                console.error('创建关系失败:', error);
                console.error('错误详情:', {
                  message: error.message,
                  response: error.response?.data,
                  status: error.response?.status,
                  createData: {
                    work_id: workId,
                    source_id: panelCreateRelationshipData?.sourceId,
                    target_id: panelCreateRelationshipData?.targetId,
                  }
                });
                const errorDetail = error.response?.data?.detail || error.message || '未知错误';
                showToast('error', `创建失败: ${errorDetail}`);
                throw error;
              }
            }}
            onDeleteNode={async () => {
              if (panelNodeData) {
                const { type, entity } = panelNodeData;
                const typeName = type === 'character' ? '角色' : type === 'location' ? '地点' : '设定';

                try {
                  // 先删除相关关系
                  const relatedRels = relationships.filter(
                    (rel) =>
                      (rel.sourceId === entity.id && rel.sourceType === type) ||
                      (rel.targetId === entity.id && rel.targetType === type)
                  );

                  for (const rel of relatedRels) {
                    await DataService.deleteRelationship(rel.id);
                  }

                  // 再删除实体
                  if (type === 'character') {
                    await DataService.deleteCharacter(entity.id);
                  } else if (type === 'location') {
                    await DataService.deleteLocation(entity.id);
                  } else if (type === 'setting') {
                    await DataService.deleteSetting(entity.id);
                  }

                  showToast('success', `${typeName}已删除`);
                  // 重新加载数据
                  await loadData();
                  setPanelMode('idle');
                  setPanelNodeData(null);
                } catch (error) {
                  console.error('删除失败:', error);
                  showToast('error', '删除失败');
                }
              }
            }}
            onEditRelationship={() => {
              // 编辑关系功能可以后续扩展到属性面板
              showToast('info', '编辑关系功能开发中...');
            }}
            onDeleteRelationship={() => {
              if (panelRelationshipData) {
                handleDeleteRelationship(panelRelationshipData.relationship.id);
                setPanelMode('idle');
                setPanelRelationshipData(null);
              }
            }}
            onRelationshipClick={(relationshipId) => {
              const rel = relationships.find(r => r.id === relationshipId);
              if (rel) {
                const sourceLabel = getNodeLabel(rel.sourceId, rel.sourceType);
                const targetLabel = getNodeLabel(rel.targetId, rel.targetType);
                setPanelRelationshipData({ relationship: rel, sourceLabel, targetLabel });
                setPanelMode('relationship');
              }
            }}
            // 时间线事件相关props
            timelineEventData={panelTimelineEventData}
            createTimelineEventData={panelCreateTimelineEventData}
            chapters={chapterAnchors.map(anchor => ({
              id: anchor.chapterId,
              title: anchor.chapterTitle,
              order: anchor.chapterNumber,
            }))}
            entities={[
              ...worldData.characters.map(c => ({ id: c.id, type: 'character' as EntityType, label: c.name })),
              ...worldData.locations.map(l => ({ id: l.id, type: 'location' as EntityType, label: l.name })),
              ...worldData.settings.map(s => ({ id: s.id, type: 'setting' as EntityType, label: s.title })),
            ]}
            onCreateTimelineEvent={async (formData) => {
              try {
                const newEvent = await DataService.createTimelineEvent({
                  workId: workId!,
                  ...formData,
                });
                setTimelineEvents(prev => [...prev, newEvent]);
                showToast('success', '时间线事件创建成功');
                // 关闭面板
                setPanelMode('idle');
                setPanelCreateTimelineEventData(null);
              } catch (error) {
                console.error('创建时间线事件失败:', error);
                showToast('error', '创建失败');
                throw error;
              }
            }}
            onUpdateTimelineEvent={async (eventId, formData) => {
              try {
                const updatedEvent = await DataService.updateTimelineEvent(eventId, formData);
                setTimelineEvents(prev => prev.map(e => e.id === eventId ? updatedEvent : e));
                showToast('success', '时间线事件已更新');
                // 更新面板数据
                if (panelTimelineEventData) {
                  setPanelTimelineEventData({
                    ...panelTimelineEventData,
                    event: updatedEvent,
                  });
                }
              } catch (error) {
                console.error('更新时间线事件失败:', error);
                showToast('error', '更新失败');
                throw error;
              }
            }}
            onDeleteTimelineEvent={async () => {
              if (panelTimelineEventData) {
                try {
                  await DataService.deleteTimelineEvent(panelTimelineEventData.event.id);
                  setTimelineEvents(prev => prev.filter(e => e.id !== panelTimelineEventData.event.id));
                  showToast('success', '时间线事件已删除');
                  setPanelMode('idle');
                  setPanelTimelineEventData(null);
                } catch (error) {
                  console.error('删除时间线事件失败:', error);
                  showToast('error', '删除失败');
                }
              }
            }}
            />
          )}
        </div>
      </div>

    </div>
  );
};

export default WorldviewGraphFullscreen;
