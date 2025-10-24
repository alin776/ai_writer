/**
 * 世界观关系图全屏编辑页面
 * 提供专业的关系图编辑体验
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Network, 
  Clock, 
  Download, 
  LayoutGrid,
  Loader,
  Users,
  MapPin,
  BookOpen,
  Plus,
} from 'lucide-react';
import WorldviewGraph from '@/components/worldview/WorldviewGraph';
import PropertyPanel from '@/components/worldview/PropertyPanel';
import { TimelinePanel } from '@/components/worldview/TimelinePanel';
import { GroupPanel } from '@/components/worldview/GroupPanel';
import { LayoutSelector } from '@/components/worldview/LayoutSelector';
import { SearchPanel, SearchFilter } from '@/components/worldview/SearchPanel';
import { EnhancedNodeList } from '@/components/worldview/EnhancedNodeList';
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
  
  // 布局相关状态
  const [currentLayout, setCurrentLayout] = useState<LayoutAlgorithm>('force');
  const [layoutConfig, setLayoutConfig] = useState<GlobalLayoutConfig>(DEFAULT_LAYOUT_CONFIG);
  const [showLayoutSelector, setShowLayoutSelector] = useState(false);
  
  // 导出相关状态
  const [showExportMenu, setShowExportMenu] = useState(false);
  const [exporting, setExporting] = useState(false);
  
  // 搜索和焦点模式状态
  const [searchFilter, setSearchFilter] = useState<SearchFilter>({
    searchText: '',
    nodeTypes: { character: true, location: true, setting: true },
    tags: [],
  });
  const [focusModeEnabled, setFocusModeEnabled] = useState(false);
  const [focusNodeId, setFocusNodeId] = useState<string | undefined>(undefined);
  const [focusNodeToView, setFocusNodeToView] = useState<string | undefined>(undefined);
  
  // 编辑关系状态（用于属性面板编辑按钮）
  const [editingRelationship, setEditingRelationship] = useState<Relationship | null>(null);
  
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
        DataService.getGuidelines(workId).catch(() => ({})),
        DataService.getAIGuidelines(workId).catch(() => ({})),
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
        guidelines,
        aiGuidelines,
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
    setShowExportMenu(false);
    
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
  
  // 处理连接创建（拖拽连线 - 备用，目前不使用）
  const handleConnect = (sourceId: string, sourceType: EntityType, targetId: string, targetType: EntityType) => {
    // 拖拽连线时，也使用属性面板
    const sourceLabel = getNodeLabel(sourceId, sourceType);
    const targetLabel = getNodeLabel(targetId, targetType);

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

  // 导出功能（占位）
  const handleExport = () => {
    showToast('info', '导出功能开发中...');
  };

  // 布局切换
  const handleLayoutChange = (algorithm: LayoutAlgorithm) => {
    setCurrentLayout(algorithm);
    const newConfig = { ...layoutConfig, algorithm };
    setLayoutConfig(newConfig);
    showToast('info', `正在应用${getLayoutName(algorithm)}...`);
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
    <div className="worldview-graph-fullscreen h-screen flex flex-col bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="graph-header bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
        <div className="header-left flex items-center gap-4">
          <button
            onClick={handleBack}
            className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            返回
          </button>
          <div className="h-6 w-px bg-gray-300" />
          <div>
            <h1 style={{ color: '#111827' }} className="text-lg font-bold">{workTitle}</h1>
            <p className="text-xs text-gray-500">世界观关系图编辑器</p>
          </div>
        </div>

        <div className="header-center flex items-center gap-2">
          <button
            onClick={() => setViewMode('graph')}
            className={`flex items-center gap-2 px-4 py-2 text-sm rounded-lg transition-colors ${
              viewMode === 'graph'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <Network className="w-4 h-4" />
            关系图
          </button>
          <button
            onClick={() => setViewMode('timeline')}
            className={`flex items-center gap-2 px-4 py-2 text-sm rounded-lg transition-colors ${
              viewMode === 'timeline'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <Clock className="w-4 h-4" />
            时间线
          </button>
        </div>

        <div className="header-right flex items-center gap-2">
          {viewMode === 'graph' ? (
            <button
              onClick={toggleConnectionMode}
              className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                connectionMode
                  ? 'bg-blue-600 text-white hover:bg-blue-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <Plus className="w-4 h-4" />
              {connectionMode ? '连线模式（已开启）' : '创建关系'}
            </button>
          ) : (
            <button
              onClick={() => {
                setPanelCreateTimelineEventData({
                  workId: workId!,
                });
                setPanelMode('createTimeline');
              }}
              className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Plus className="w-4 h-4" />
              创建时间线事件
            </button>
          )}
          {viewMode === 'graph' && (
            <>
              {/* 搜索面板 */}
              <div className="w-80">
                <SearchPanel
                  onSearchChange={setSearchFilter}
                  onFocusModeToggle={(enabled) => {
                    setFocusModeEnabled(enabled);
                    if (!enabled) {
                      setFocusNodeId(undefined);
                    }
                    showToast(enabled ? 'success' : 'info', enabled ? '焦点模式已启用，点击节点查看关联' : '焦点模式已关闭');
                  }}
                  focusModeEnabled={focusModeEnabled}
                />
              </div>
              
              {/* 布局选择器 */}
              <div className="relative">
                <button
                  onClick={() => setShowLayoutSelector(!showLayoutSelector)}
                  className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <LayoutGrid className="w-4 h-4" />
                  布局
                </button>
                
                {showLayoutSelector && (
                  <div className="absolute top-full right-0 mt-2 z-50">
                    <LayoutSelector
                      currentLayout={currentLayout}
                      onLayoutChange={(algorithm) => {
                        handleLayoutChange(algorithm);
                        setShowLayoutSelector(false);
                      }}
                      config={layoutConfig}
                      onConfigChange={(config) => {
                        setLayoutConfig(prev => ({ ...prev, ...config }));
                      }}
                    />
                  </div>
                )}
              </div>
            </>
          )}
          {/* 导出按钮 */}
          <div className="relative">
            <button
              onClick={() => setShowExportMenu(!showExportMenu)}
              disabled={exporting}
              className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50"
            >
              <Download className="w-4 h-4" />
              {exporting ? '导出中...' : '导出'}
            </button>
            
            {showExportMenu && !exporting && (
              <div className="absolute top-full right-0 mt-2 z-50 bg-white border border-gray-200 rounded-lg shadow-lg py-2 w-40">
                <button
                  onClick={() => handleExport('png')}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  导出为 PNG
                </button>
                <button
                  onClick={() => handleExport('svg')}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  导出为 SVG
                </button>
                <button
                  onClick={() => handleExport('json')}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  导出为 JSON
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content - 三栏布局 */}
      <div className="graph-main flex flex-1 overflow-hidden">
        {/* Left Sidebar - 左侧边栏 */}
        <aside className="left-sidebar w-64 bg-white border-r border-gray-200 flex flex-col overflow-hidden">
          {/* Tab切换 */}
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setLeftPanelTab('nodes')}
              className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                leftPanelTab === 'nodes'
                  ? 'text-gray-900 bg-gray-100 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <Users className="w-4 h-4 inline-block mr-2" />
              节点列表
            </button>
            <button
              onClick={() => setLeftPanelTab('groups')}
              className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                leftPanelTab === 'groups'
                  ? 'text-gray-900 bg-gray-100 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
              </svg>
              分组管理
            </button>
          </div>

          {/* Tab内容 */}
          <div className="flex-1 overflow-hidden flex flex-col">
            {leftPanelTab === 'nodes' ? (
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
              />
            ) : (
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
              />
            )}
          </div>
        </aside>

        {/* Main Canvas - 主画布 */}
        <main className="main-canvas flex-1 bg-gray-50 relative">
          {/* 连线模式提示条 */}
          {connectionMode && (
            <div className="absolute top-4 left-1/2 transform -translate-x-1/2 z-10 bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                <span className="font-medium">连线模式已开启</span>
              </div>
              <span className="text-blue-100 text-sm">
                {selectedNode ? `已选中：${selectedNode.label}` : '请点击第一个节点'}
              </span>
              <button
                onClick={toggleConnectionMode}
                className="ml-2 px-3 py-1 bg-white/20 hover:bg-white/30 rounded text-sm transition-colors"
              >
                退出
              </button>
            </div>
          )}
          
          {viewMode === 'graph' ? (
            <div className="h-full">
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
                searchText={searchFilter.searchText}
                filteredNodeTypes={searchFilter.nodeTypes}
                focusMode={focusModeEnabled}
                focusNodeId={focusNodeId}
                focusNodeToView={focusNodeToView}
              />
            </div>
          ) : (
            <div className="h-full">
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
                onEditEvent={(event) => {
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
                onDeleteEvent={async (eventId) => {
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
                onEventClick={(event) => {
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
            </div>
          )}
        </main>

        {/* Right Panel - 右侧属性面板 */}
        <aside className="right-panel w-80 bg-white border-l border-gray-200 overflow-y-auto">
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
            onClose={() => {
              setPanelMode('idle');
              setPanelNodeData(null);
              setPanelRelationshipData(null);
              setPanelCreateRelationshipData(null);
              setPanelTimelineEventData(null);
              setPanelCreateTimelineEventData(null);
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
              if (!panelCreateRelationshipData) return;

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
                
                // 关闭面板
                setPanelMode('idle');
                setPanelCreateRelationshipData(null);
              } catch (error) {
                console.error('创建关系失败:', error);
                showToast('error', '创建失败');
                throw error;
              }
            }}
            onDeleteNode={async () => {
              if (panelNodeData) {
                const { type, entity } = panelNodeData;
                const name = type === 'character' ? (entity as Character).name :
                           type === 'location' ? (entity as Location).name :
                           (entity as Setting).title;
                
                const typeName = type === 'character' ? '角色' : type === 'location' ? '地点' : '设定';
                
                if (confirm(`确定要删除${typeName} "${name}" 吗？\n\n注意：这将同时删除与该${typeName}相关的所有关系。`)) {
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
              }
            }}
            onEditRelationship={() => {
              // 编辑关系功能可以后续扩展到属性面板
              showToast('info', '编辑关系功能开发中...');
            }}
            onDeleteRelationship={() => {
              if (panelRelationshipData && confirm('确定要删除这个关系吗？')) {
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
              if (panelTimelineEventData && confirm('确定要删除这个时间线事件吗？')) {
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
        </aside>
      </div>

      {/* Footer - 底部状态栏 */}
      <footer className="graph-footer bg-white border-t border-gray-200 px-6 py-2 flex items-center justify-between text-xs text-gray-500">
        <div className="footer-left flex items-center gap-4">
          <span>{stats.characters} 个角色</span>
          <span>·</span>
          <span>{stats.locations} 个地点</span>
          <span>·</span>
          <span>{stats.settings} 个设定</span>
          <span>·</span>
          <span>{stats.relationships} 个关系</span>
        </div>
        <div className="footer-right flex items-center gap-4">
          <span>缩放: 100%</span>
          <button className="text-blue-600 hover:text-blue-700">帮助</button>
        </div>
      </footer>

    </div>
  );
};

export default WorldviewGraphFullscreen;
