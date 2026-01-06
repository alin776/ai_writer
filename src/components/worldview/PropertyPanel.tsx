/**
 * 属性面板组件
 * 显示节点或关系的详细信息
 */
import React, { useState, useEffect } from 'react';
import { X, Users, MapPin, BookOpen, Link2, Edit2, Trash2, Star, Save, Clock, Calendar, Edit, MoreVertical, ArrowRight, ArrowLeftRight, User, ChevronLeft, ChevronRight, Sparkles, Send, Loader2 } from 'lucide-react';
import { PieChart, Pie, Cell, Tooltip } from 'recharts';
import { Character, Location, Setting } from '@/types/novel';
import { Relationship, EntityType, getRelationshipOptions, getRelationshipExamples } from '@/types/relationship';
import { TimelineEvent, EventType, EVENT_TYPE_OPTIONS } from '@/types/timeline';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { ScrollArea } from '@/components/ui/scroll-area';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Checkbox } from '@/components/ui/checkbox';

type PanelMode = 'idle' | 'node' | 'relationship' | 'create' | 'timeline' | 'createTimeline';

interface PropertyPanelProps {
  mode: PanelMode;
  // 节点数据
  nodeData?: {
    id: string;
    type: EntityType;
    entity: Character | Location | Setting;
    initialEditMode?: boolean; // 是否初始进入编辑模式
  } | null;
  // 关系数据
  relationshipData?: {
    relationship: Relationship;
    sourceLabel: string;
    targetLabel: string;
  } | null;
  // 创建关系数据
  createRelationshipData?: {
    sourceId: string;
    sourceType: EntityType;
    sourceLabel: string;
    sourceDescription?: string;
    targetId: string;
    targetType: EntityType;
    targetLabel: string;
    targetDescription?: string;
    workId?: string;
  } | null;
  // 时间线事件数据
  timelineEventData?: {
    event: TimelineEvent;
    entityLabel: string;
  } | null;
  // 创建时间线事件数据
  createTimelineEventData?: {
    workId: string;
    entityId?: string;
    entityType?: EntityType;
    entityLabel?: string;
  } | null;
  // 统计数据
  stats: {
    characters: number;
    locations: number;
    settings: number;
    relationships: number;
    relationshipsByType: Record<string, number>;
  };
  // 相关关系列表
  relatedRelationships?: Relationship[];
  // 章节列表（用于时间线事件选择章节）
  chapters?: Array<{ id: string; title: string; order: number }>;
  // 实体列表（用于时间线事件选择实体）
  entities?: Array<{ id: string; type: EntityType; label: string }>;
  // 回调
  onClose: () => void;
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
  onSaveNode?: (updatedEntity: Character | Location | Setting) => Promise<void>;
  onDeleteNode?: () => void;
  onCreateRelationship?: (formData: {
    relationshipType: string;
    label: string;
    description: string;
    strength: number;
    direction: 'one-way' | 'two-way';
    color?: string;
    lineStyle: 'solid' | 'dashed' | 'dotted';
  }) => Promise<void>;
  onEditRelationship?: () => void;
  onSaveRelationship?: (relationshipId: string, formData: {
    relationshipType: string;
    label: string;
    description: string;
    strength: number;
    direction: 'one-way' | 'two-way';
    color?: string;
    lineStyle: 'solid' | 'dashed' | 'dotted';
  }) => Promise<void>;
  onDeleteRelationship?: () => void;
  onRelationshipClick?: (relationshipId: string) => void;
  // 时间线事件回调
  onCreateTimelineEvent?: (formData: {
    entityId: string;
    entityType: EntityType;
    eventType: EventType;
    title: string;
    description?: string;
    icon?: string;
    chapterId?: string;
    chapterNumber?: number;
    color?: string;
  }) => Promise<void>;
  onUpdateTimelineEvent?: (eventId: string, formData: Partial<TimelineEvent>) => Promise<void>;
  onDeleteTimelineEvent?: () => void;
}

const PropertyPanel: React.FC<PropertyPanelProps> = ({
  mode,
  nodeData,
  relationshipData,
  createRelationshipData,
  timelineEventData,
  createTimelineEventData,
  stats,
  relatedRelationships = [],
  chapters = [],
  entities = [],
  onClose,
  isCollapsed = false,
  onToggleCollapse,
  onSaveNode,
  onDeleteNode,
  onCreateRelationship,
  onEditRelationship,
  onSaveRelationship,
  onDeleteRelationship,
  onRelationshipClick,
  onCreateTimelineEvent,
  onUpdateTimelineEvent,
  onDeleteTimelineEvent,
}) => {
  // 编辑状态
  const [isEditing, setIsEditing] = useState(nodeData?.initialEditMode || false);
  const [editedEntity, setEditedEntity] = useState<Character | Location | Setting | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  // 删除确认对话框状态
  const [deleteDialog, setDeleteDialog] = useState<{
    open: boolean;
    type: 'node' | 'relationship' | 'timeline' | null;
    name: string;
  }>({ open: false, type: null, name: '' });
  const [dontAskAgain, setDontAskAgain] = useState(false);

  // 创建关系表单状态
  const [createForm, setCreateForm] = useState({
    relationshipType: '好友关系',
    label: '',
    description: '',
    strength: 5,
    direction: 'one-way' as 'one-way' | 'two-way',
    color: '#8b5cf6',
    lineStyle: 'solid' as 'solid' | 'dashed' | 'dotted',
  });

  // AI 生成相关状态
  const [aiInput, setAiInput] = useState('');
  const [isGeneratingAI, setIsGeneratingAI] = useState(false);

  // 时间线事件表单状态
  const [timelineForm, setTimelineForm] = useState<Record<string, any>>({
    entityId: '',
    entityType: 'character' as EntityType,
    eventType: 'milestone' as EventType,
    title: '',
    description: '',
    icon: '🎯',
    chapterId: '',
    chapterNumber: 1,
    color: '#f59e0b',
  });

  // 编辑时间线事件状态
  const [editedEvent, setEditedEvent] = useState<TimelineEvent | null>(null);
  const [isEditingEvent, setIsEditingEvent] = useState(false);

  // 编辑关系状态
  const [isEditingRelationship, setIsEditingRelationship] = useState(false);
  const [editedRelationship, setEditedRelationship] = useState<{
    relationshipType: string;
    label: string;
    description: string;
    strength: number;
    direction: 'one-way' | 'two-way';
    color: string;
    lineStyle: 'solid' | 'dashed' | 'dotted';
  } | null>(null);

  // 饼状图激活状态
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  // 当nodeData变化时，重置编辑状态
  useEffect(() => {
    if (nodeData?.initialEditMode) {
      setEditedEntity({ ...nodeData.entity });
      setIsEditing(true);
    } else {
      setIsEditing(false);
      setEditedEntity(null);
    }
  }, [nodeData]);

  // 开始编辑
  const handleStartEdit = () => {
    if (nodeData) {
      setEditedEntity({ ...nodeData.entity });
      setIsEditing(true);
    }
  };

  // 取消编辑
  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditedEntity(null);
  };

  // 删除处理函数
  const handleDeleteClick = (type: 'node' | 'relationship' | 'timeline', name: string) => {
    // 检查本次会话是否勾选了"不再提醒"
    const skipConfirm = sessionStorage.getItem('worldview_skip_delete_confirm') === 'true';

    if (skipConfirm) {
      // 直接删除
      executeDelete(type);
    } else {
      // 显示确认对话框
      setDeleteDialog({ open: true, type, name });
      setDontAskAgain(false);
    }
  };

  const executeDelete = (type: 'node' | 'relationship' | 'timeline') => {
    if (type === 'node' && onDeleteNode) {
      onDeleteNode();
    } else if (type === 'relationship' && onDeleteRelationship) {
      onDeleteRelationship();
    } else if (type === 'timeline' && onDeleteTimelineEvent) {
      onDeleteTimelineEvent();
    }
  };

  const handleConfirmDelete = () => {
    // 如果勾选了"不再提醒"，保存到 sessionStorage
    if (dontAskAgain) {
      sessionStorage.setItem('worldview_skip_delete_confirm', 'true');
    }

    // 执行删除
    if (deleteDialog.type) {
      executeDelete(deleteDialog.type);
    }

    // 关闭对话框
    setDeleteDialog({ open: false, type: null, name: '' });
  };

  const handleCancelDelete = () => {
    setDeleteDialog({ open: false, type: null, name: '' });
    setDontAskAgain(false);
  };

  // 保存编辑
  const handleSaveEdit = async () => {
    if (editedEntity && onSaveNode) {
      setIsSaving(true);
      try {
        await onSaveNode(editedEntity);
        setIsEditing(false);
        setEditedEntity(null);
      } catch (error) {
        console.error('保存失败:', error);
      } finally {
        setIsSaving(false);
      }
    }
  };
  // 渲染空闲状态
  const renderIdleState = () => {
    // 关系类型分布
    const relationshipTypeCounts = stats.relationshipsByType;

    return (
      <div className="flex flex-col h-full text-sm">
        <div className="p-3 border-b border-border bg-gradient-to-r from-purple-50/50 via-amber-50/30 to-emerald-50/50 dark:from-purple-900/20 dark:via-amber-900/10 dark:to-emerald-900/20 flex items-center justify-between">
          <h3 className="text-foreground font-medium">世界观统计</h3>
          {onToggleCollapse && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onToggleCollapse}
              className="h-7 w-7 p-0"
              title={isCollapsed ? '展开侧边栏' : '收缩侧边栏'}
            >
              {isCollapsed ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
            </Button>
          )}
        </div>
        <div className="flex-1 overflow-y-auto custom-scrollbar">
          <div className="p-3 space-y-4">
            {/* 核心数据卡片 */}
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-gradient-to-br from-purple-50 to-purple-100/50 dark:from-purple-900/30 dark:to-purple-800/20 rounded-lg p-3 shadow-[0_1px_4px_rgba(139,92,246,0.15)]">
                <div className="flex items-center gap-2 mb-1">
                  <Users className="w-3.5 h-3.5 text-purple-600 dark:text-purple-400" />
                  <span className="text-xs text-purple-900/70 dark:text-purple-300/70">角色</span>
                </div>
                <div className="text-2xl text-purple-700 dark:text-purple-300 tabular-nums">{stats.characters}</div>
              </div>

              <div className="bg-gradient-to-br from-amber-50 to-amber-100/50 dark:from-amber-900/30 dark:to-amber-800/20 rounded-lg p-3 shadow-[0_1px_4px_rgba(245,158,11,0.15)]">
                <div className="flex items-center gap-2 mb-1">
                  <MapPin className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
                  <span className="text-xs text-amber-900/70 dark:text-amber-300/70">地点</span>
                </div>
                <div className="text-2xl text-amber-700 dark:text-amber-300 tabular-nums">{stats.locations}</div>
              </div>

              <div className="bg-gradient-to-br from-emerald-50 to-emerald-100/50 dark:from-emerald-900/30 dark:to-emerald-800/20 rounded-lg p-3 shadow-[0_1px_4px_rgba(16,185,129,0.15)]">
                <div className="flex items-center gap-2 mb-1">
                  <BookOpen className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
                  <span className="text-xs text-emerald-900/70 dark:text-emerald-300/70">设定</span>
                </div>
                <div className="text-2xl text-emerald-700 dark:text-emerald-300 tabular-nums">{stats.settings}</div>
              </div>

              <div className="bg-gradient-to-br from-blue-50 to-blue-100/50 dark:from-blue-900/30 dark:to-blue-800/20 rounded-lg p-3 shadow-[0_1px_4px_rgba(59,130,246,0.15)]">
                <div className="flex items-center gap-2 mb-1">
                  <Link2 className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
                  <span className="text-xs text-blue-900/70 dark:text-blue-300/70">关系</span>
                </div>
                <div className="text-2xl text-blue-700 dark:text-blue-300 tabular-nums">{stats.relationships}</div>
              </div>
            </div>

            {/* 饼状图 */}
            {(stats.characters + stats.locations + stats.settings + stats.relationships > 0) && (
              <div className="bg-gradient-to-br from-purple-50/30 via-white to-amber-50/30 dark:from-purple-900/20 dark:via-slate-800 dark:to-amber-900/20 rounded-xl p-3 shadow-[0_2px_8px_rgba(0,0,0,0.04)] dark:shadow-[0_2px_8px_rgba(0,0,0,0.3)] border border-purple-100/20 dark:border-slate-700/50">
                <div className="w-full h-[220px]">
                  <PieChart width={280} height={220}>
                    <Pie
                      data={[
                        { name: '角色', value: stats.characters, color: '#8b5cf6' },
                        { name: '地点', value: stats.locations, color: '#f59e0b' },
                        { name: '设定', value: stats.settings, color: '#10b981' },
                        { name: '关系', value: stats.relationships, color: '#3b82f6' }
                      ]}
                      cx="50%"
                      cy="50%"
                      innerRadius={38}
                      outerRadius={55}
                      paddingAngle={2}
                      dataKey="value"
                      activeIndex={activeIndex ?? undefined}
                      activeShape={{
                        innerRadius: 38,
                        outerRadius: 58,
                        stroke: '#ffffff',
                        strokeWidth: 2.5
                      } as any}
                      onMouseEnter={(_, index) => setActiveIndex(index)}
                      onMouseLeave={() => setActiveIndex(null)}
                      label={({ cx, cy, midAngle, outerRadius, payload }) => {
                        const RADIAN = Math.PI / 180;
                        const cos = Math.cos(-midAngle * RADIAN);
                        const sin = Math.sin(-midAngle * RADIAN);
                        const sx = cx + (outerRadius + 6) * cos;
                        const sy = cy + (outerRadius + 6) * sin;
                        const mx = cx + (outerRadius + 14) * cos;
                        const my = cy + (outerRadius + 14) * sin;
                        const ex = mx + (cos >= 0 ? 1 : -1) * 12;
                        const ey = my;
                        const textAnchor = cos >= 0 ? 'start' : 'end';

                        return (
                          <g>
                            <path
                              d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`}
                              stroke={payload.color}
                              fill="none"
                              strokeWidth={1.2}
                              opacity={0.4}
                            />
                            <text
                              x={ex + (cos >= 0 ? 4 : -4)}
                              y={ey + 3}
                              textAnchor={textAnchor}
                              fill={payload.color}
                              fontSize={10}
                              fontWeight={600}
                              style={{ pointerEvents: 'none' }}
                            >
                              {payload.value}
                            </text>
                          </g>
                        );
                      }}
                      labelLine={false}
                    >
                      <Cell fill="#8b5cf6" stroke="#ffffff" strokeWidth={2} style={{ cursor: 'pointer', outline: 'none' }} />
                      <Cell fill="#f59e0b" stroke="#ffffff" strokeWidth={2} style={{ cursor: 'pointer', outline: 'none' }} />
                      <Cell fill="#10b981" stroke="#ffffff" strokeWidth={2} style={{ cursor: 'pointer', outline: 'none' }} />
                      <Cell fill="#3b82f6" stroke="#ffffff" strokeWidth={2} style={{ cursor: 'pointer', outline: 'none' }} />
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'hsl(var(--card))',
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '6px',
                        fontSize: '11px',
                        padding: '6px 10px',
                        boxShadow: '0 2px 8px rgba(0,0,0,0.12)',
                      }}
                      itemStyle={{
                        color: 'hsl(var(--foreground))',
                      }}
                      labelStyle={{
                        color: 'hsl(var(--foreground))',
                      }}
                      formatter={(value: any, name: string) => [`${value}`, name]}
                    />
                  </PieChart>
                </div>
              </div>
            )}

            {/* 关系类型分布 */}
            {Object.keys(relationshipTypeCounts).length > 0 && (
              <div className="bg-blue-50/40 dark:bg-blue-950/30 rounded-lg p-3 border border-blue-100/30 dark:border-blue-800/30">
                <h4 className="text-foreground font-medium mb-3 flex items-center gap-2">
                  <div className="w-1 h-4 bg-blue-500 rounded-full" />
                  关系类型分布
                </h4>
                <div className="space-y-2">
                  {Object.entries(relationshipTypeCounts).map(([type, count]) => {
                    const total = Object.values(relationshipTypeCounts).reduce((a: number, b: number) => a + b, 0);
                    const percentage = total > 0 ? (count / total * 100).toFixed(0) : 0;
                    return (
                      <div key={type} className="space-y-1">
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-foreground/80">{type}</span>
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-muted-foreground">{percentage}%</span>
                            <span className="px-2 py-0.5 bg-secondary text-secondary-foreground rounded text-xs font-medium min-w-[28px] text-center">{count}</span>
                          </div>
                        </div>
                        <div className="h-1.5 bg-blue-100 dark:bg-blue-900/40 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-blue-400 to-blue-500 dark:from-blue-500 dark:to-blue-400 rounded-full transition-all duration-300"
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  // 渲染节点详情
  const renderNodeDetails = () => {
    if (!nodeData) return null;

    const { type, entity } = nodeData;
    const entityIcon = type === 'character' ? User : type === 'location' ? MapPin : BookOpen;
    const Icon = entityIcon;

    // 过滤相关关系（使用蛇形命名）
    const nodeRelations = relatedRelationships.filter(
      (rel) =>
        (rel.sourceId === nodeData.id && rel.sourceType === type) ||
        (rel.targetId === nodeData.id && rel.targetType === type)
    );

    const handleSave = () => {
      if (editedEntity) {
        handleSaveEdit();
      }
    };

    const currentEntity = isEditing && editedEntity ? editedEntity : entity;

    return (
      <div className="flex flex-col h-full text-sm">
        {/* 标题栏 */}
        <div className="p-6 pb-4 flex items-start justify-between">
          <div className="flex-1">
            {!isEditing ? (
              <h2
                className="text-2xl font-semibold text-foreground leading-relaxed m-0"
              >
                {type === 'setting'
                  ? (currentEntity as Setting).title
                  : (currentEntity as Character | Location).name}
              </h2>
            ) : (
              <Input
                value={
                  type === 'setting'
                    ? (currentEntity as Setting).title
                    : (currentEntity as Character | Location).name
                }
                onChange={(e) => {
                  if (type === 'setting') {
                    setEditedEntity({ ...(currentEntity as Setting), title: e.target.value });
                  } else {
                    setEditedEntity({ ...(currentEntity as Character | Location), name: e.target.value });
                  }
                }}
                className="text-xl font-semibold border-border"
              />
            )}
          </div>
          <div className="flex items-center gap-1">
            {!isEditing && (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                    <MoreVertical className="w-4 h-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-40">
                  <DropdownMenuItem
                    onClick={handleStartEdit}
                  >
                    <Edit className="w-3.5 h-3.5 mr-2" />
                    编辑
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    onClick={() => {
                      const name = 'name' in currentEntity ? currentEntity.name : 'title' in currentEntity ? currentEntity.title : '未知';
                      handleDeleteClick('node', name);
                    }}
                    variant="destructive"
                  >
                    <Trash2 className="w-3.5 h-3.5 mr-2" />
                    删除
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            )}
            <Button variant="ghost" size="sm" onClick={onClose} className="h-8 w-8 p-0">
              <X className="w-4 h-4" />
            </Button>
          </div>
        </div>

        <ScrollArea className="flex-1 custom-scrollbar">
          <div className={isEditing ? 'p-6 min-h-full flex flex-col' : 'p-6 space-y-5'}>
            {!isEditing ? (
              <>
                {/* 角色/分类 */}
                {((type === 'character' && (currentEntity as Character).role) ||
                  (type === 'location' && (currentEntity as Location).type) ||
                  (type === 'setting' && (currentEntity as Setting).category)) && (
                  <div className="flex items-center gap-3">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">
                      {type === 'character' ? '角色定位' : '分类'}
                    </div>
                    <div className="text-foreground">
                       {type === 'character' ? (currentEntity as Character).role :
                       type === 'location' ? (currentEntity as Location).type :
                       (currentEntity as Setting).category}
                    </div>
                  </div>
                )}

                {/* 描述 */}
                <div className="space-y-2 pt-4">
                  <p className="text-foreground/80 leading-relaxed whitespace-pre-wrap">
                    {(type === 'setting'
                      ? (currentEntity as Setting).content
                      : (currentEntity as Character | Location).description) || '暂无描述'}
                  </p>
                </div>

                {/* 标签 */}
                {currentEntity.tags && currentEntity.tags.length > 0 && (
                  <div className="flex items-start gap-3 pt-4 border-t border-border">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider whitespace-nowrap">
                      标签
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {currentEntity.tags.map((tag: string) => (
                        <span
                          key={tag}
                          className="px-2.5 py-1 text-xs border border-border rounded-full text-muted-foreground hover:border-foreground/20 transition-colors"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* 相关关系 */}
                {nodeRelations.length > 0 && (
                  <div className="space-y-3 pt-4 border-t border-border">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">
                      相关关系 · {nodeRelations.length}
                    </div>
                    <div className="space-y-1">
                      {nodeRelations.map(rel => {
                        const isSource = rel.sourceId === nodeData.id;

                        return (
                          <div
                            key={rel.id}
                            onClick={() => onRelationshipClick?.(rel.id)}
                            className="group flex items-center justify-between py-3 border-b border-border/50 last:border-0 hover:bg-accent/30 -mx-2 px-2 rounded transition-colors cursor-pointer"
                          >
                            <div className="flex-1 min-w-0">
                              <div className="text-foreground truncate">{rel.label || rel.relationshipType}</div>
                              <div className="text-xs text-muted-foreground mt-0.5">
                                {rel.relationshipType}
                              </div>
                            </div>
                            <ArrowRight className="w-4 h-4 text-muted-foreground/30 group-hover:text-muted-foreground group-hover:translate-x-0.5 transition-all flex-shrink-0 ml-2" />
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="flex flex-col gap-5 flex-1">
                {/* 编辑模式 */}
                {type === 'character' && (
                  <div className="space-y-2">
                    <Input
                      value={(currentEntity as Character).role || ''}
                      onChange={(e) => setEditedEntity({ ...(currentEntity as Character), role: e.target.value })}
                      placeholder="例如：主角、反派、配角..."
                      className="border-border"
                    />
                  </div>
                )}

                {type === 'location' && (
                  <div className="space-y-2">
                    <Input
                      value={(currentEntity as Location).type || ''}
                      onChange={(e) => setEditedEntity({ ...(currentEntity as Location), type: e.target.value })}
                      placeholder="请输入分类..."
                      className="border-border"
                    />
                  </div>
                )}

                {type === 'setting' && (
                  <div className="space-y-2">
                    <Input
                      value={(currentEntity as Setting).category || ''}
                      onChange={(e) => setEditedEntity({ ...(currentEntity as Setting), category: e.target.value })}
                      placeholder="请输入分类..."
                      className="border-border"
                    />
                  </div>
                )}

                <div className="space-y-2 pt-3">
                  <Textarea
                    value={type === 'setting' ? (currentEntity as Setting).content : (currentEntity as Character | Location).description || ''}
                    onChange={(e) => {
                      if (type === 'setting') {
                        setEditedEntity({ ...(currentEntity as Setting), content: e.target.value });
                      } else {
                        setEditedEntity({ ...(currentEntity as Character | Location), description: e.target.value });
                      }
                    }}
                    placeholder="详细描述此节点的相关信息..."
                    className="border-border min-h-[120px] resize-none bg-input-background dark:bg-input/30"
                    rows={6}
                  />
                </div>

                <div className="mt-auto flex justify-end gap-2 pt-2">
                  <Button onClick={handleSave} size="sm" disabled={isSaving}>
                    {isSaving ? '保存中...' : '保存'}
                  </Button>
                  <Button variant="outline" size="sm" onClick={handleCancelEdit}>
                    取消
                  </Button>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
      </div>
    );
  };

  // 渲染关系详情
  const renderRelationshipDetails = () => {
    if (!relationshipData) return null;

    const { relationship, sourceLabel, targetLabel } = relationshipData;

    // 根据源类型和目标类型动态获取关系类型选项
    const relationshipTypes = getRelationshipOptions(
      relationship.sourceType,
      relationship.targetType
    );

    // 获取动态示例提示
    const examplePlaceholder = getRelationshipExamples(
      relationship.sourceType,
      relationship.targetType
    );

    // 开始编辑
    const handleStartEditRelationship = () => {
      setEditedRelationship({
        relationshipType: relationship.relationshipType,
        label: relationship.label,
        description: relationship.description || '',
        strength: relationship.strength,
        direction: relationship.direction,
        color: relationship.color || '#8b5cf6',
        lineStyle: relationship.lineStyle,
      });
      setIsEditingRelationship(true);
    };

    // 取消编辑
    const handleCancelEditRelationship = () => {
      setIsEditingRelationship(false);
      setEditedRelationship(null);
    };

    // 保存编辑
    const handleSaveRelationship = async () => {
      if (editedRelationship && onSaveRelationship) {
        setIsSaving(true);
        try {
          await onSaveRelationship(relationship.id, editedRelationship);
          setIsEditingRelationship(false);
          setEditedRelationship(null);
        } catch (error) {
          console.error('保存关系失败:', error);
        } finally {
          setIsSaving(false);
        }
      }
    };

    const currentData = isEditingRelationship && editedRelationship ? editedRelationship : {
      relationshipType: relationship.relationshipType,
      label: relationship.label,
      description: relationship.description || '',
      strength: relationship.strength,
      direction: relationship.direction,
      color: relationship.color || '#8b5cf6',
      lineStyle: relationship.lineStyle,
    };

    return (
      <div className="flex flex-col h-full text-sm">
        {/* 标题栏 */}
        <div className="p-4 pb-3 flex items-start justify-between">
          <div className="flex items-center gap-2 flex-1">
            <span className="text-2xl text-foreground leading-snug">{sourceLabel}</span>
            <ArrowRight className="w-4 h-4 text-muted-foreground" />
            <span className="text-2xl text-foreground leading-snug">{targetLabel}</span>
          </div>
          <div className="flex items-center gap-1">
            {!isEditingRelationship && (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                    <MoreVertical className="w-4 h-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-40">
                  <DropdownMenuItem onClick={handleStartEditRelationship}>
                    <Edit className="w-3.5 h-3.5 mr-2" />
                    编辑
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    onClick={() => handleDeleteClick('relationship', relationship.label || '关系')}
                    variant="destructive"
                  >
                    <Trash2 className="w-3.5 h-3.5 mr-2" />
                    删除
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            )}
            <Button variant="ghost" size="sm" onClick={onClose} className="h-8 w-8 p-0">
              <X className="w-4 h-4" />
            </Button>
          </div>
        </div>

        <ScrollArea className="flex-1 custom-scrollbar">
          <div className="p-6 space-y-5">
            {isEditingRelationship ? (
              <>
                {/* 编辑模式 */}
                {/* 关系类型 */}
                <div className="space-y-2">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">关系类型</Label>
                  <Select
                    value={currentData.relationshipType}
                    onValueChange={(value) => setEditedRelationship(prev => prev ? {...prev, relationshipType: value} : null)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {relationshipTypes.map(type => (
                        <SelectItem key={type} value={type}>{type}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* 标签 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">标签</Label>
                  <Input
                    value={currentData.label}
                    onChange={(e) => setEditedRelationship(prev => prev ? {...prev, label: e.target.value} : null)}
                    placeholder={examplePlaceholder}
                  />
                </div>

                {/* 描述 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">描述</Label>
                  <Textarea
                    value={currentData.description}
                    onChange={(e) => setEditedRelationship(prev => prev ? {...prev, description: e.target.value} : null)}
                    placeholder="描述这个关系的详细信息"
                    className="bg-input-background dark:bg-input/30"
                    rows={3}
                  />
                </div>

                {/* 强度 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">强度</Label>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-foreground text-xs">{currentData.strength}/10</span>
                  </div>
                  <Slider
                    value={[currentData.strength]}
                    onValueChange={([value]) => setEditedRelationship(prev => prev ? {...prev, strength: value} : null)}
                    min={1}
                    max={10}
                    step={1}
                  />
                </div>

                {/* 方向 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">方向</Label>
                  <RadioGroup
                    value={currentData.direction}
                    onValueChange={(value: 'one-way' | 'two-way') => setEditedRelationship(prev => prev ? {...prev, direction: value} : null)}
                    className="space-y-2"
                  >
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="one-way" id="edit-unidirectional" />
                      <label htmlFor="edit-unidirectional" className="cursor-pointer text-sm">单向</label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="two-way" id="edit-bidirectional" />
                      <label htmlFor="edit-bidirectional" className="cursor-pointer text-sm">双向</label>
                    </div>
                  </RadioGroup>
                </div>

                {/* 颜色 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">颜色</Label>
                  <Input
                    type="color"
                    value={currentData.color}
                    onChange={(e) => setEditedRelationship(prev => prev ? {...prev, color: e.target.value} : null)}
                    className="h-10 cursor-pointer"
                  />
                </div>

                {/* 线型 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">线型</Label>
                  <Select
                    value={currentData.lineStyle}
                    onValueChange={(value: 'solid' | 'dashed' | 'dotted') => setEditedRelationship(prev => prev ? {...prev, lineStyle: value} : null)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="solid">实线</SelectItem>
                      <SelectItem value="dashed">虚线</SelectItem>
                      <SelectItem value="dotted">点线</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* 保存/取消按钮 */}
                <div className="flex gap-2 pt-4">
                  <Button onClick={handleSaveRelationship} size="sm" disabled={isSaving}>
                    {isSaving ? '保存中...' : '保存'}
                  </Button>
                  <Button variant="outline" size="sm" onClick={handleCancelEditRelationship}>
                    取消
                  </Button>
                </div>
              </>
            ) : (
              <>
                {/* 查看模式 */}
                {/* 关系类型 */}
                <div className="flex items-center gap-3">
                  <div className="text-xs text-muted-foreground uppercase tracking-wider">关系类型</div>
                  <div className="text-foreground">{relationship.relationshipType}</div>
                </div>

                {/* 标签 */}
                {relationship.label && (
                  <div className="flex items-center gap-3 pt-4 border-t border-border">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">标签</div>
                    <div className="text-foreground">{relationship.label}</div>
                  </div>
                )}

                {/* 描述 */}
                {relationship.description && (
                  <div className="space-y-2 pt-4 border-t border-border">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">描述</div>
                    <p className="text-foreground/80 leading-relaxed">{relationship.description}</p>
                  </div>
                )}

                {/* 强度 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <div className="text-xs text-muted-foreground uppercase tracking-wider">强度</div>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-1.5 bg-accent rounded-full overflow-hidden">
                      <div
                        className="h-full bg-foreground/60 transition-all"
                        style={{ width: `${(relationship.strength / 10) * 100}%` }}
                      />
                    </div>
                    <span className="text-foreground text-xs">{relationship.strength}/10</span>
                  </div>
                </div>

                {/* 方向 */}
                <div className="flex items-center gap-3 pt-4 border-t border-border">
                  <div className="text-xs text-muted-foreground uppercase tracking-wider">方向</div>
                  <div className="text-foreground">
                    {relationship.direction === 'two-way' ? '双向' : '单向'}
                  </div>
                </div>

                {/* 颜色 */}
                {relationship.color && (
                  <div className="flex items-center gap-3 pt-4 border-t border-border">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">颜色</div>
                    <div className="flex items-center gap-2">
                      <div
                        className="w-5 h-5 rounded border border-border"
                        style={{ backgroundColor: relationship.color }}
                      />
                      <span className="text-foreground text-xs">{relationship.color}</span>
                    </div>
                  </div>
                )}

                {/* 线型 */}
                <div className="flex items-center gap-3 pt-4 border-t border-border">
                  <div className="text-xs text-muted-foreground uppercase tracking-wider">线型</div>
                  <div className="text-foreground">
                    {relationship.lineStyle === 'solid' ? '实线' :
                     relationship.lineStyle === 'dashed' ? '虚线' : '点线'}
                  </div>
                </div>
              </>
            )}
          </div>
        </ScrollArea>
      </div>
    );
  };

  // 渲染创建关系表单
  const renderCreateRelationship = () => {
    if (!createRelationshipData) return null;

    const { sourceLabel, targetLabel, sourceType, targetType } = createRelationshipData;

    // 根据源类型和目标类型动态获取关系类型选项
    const relationshipTypes = getRelationshipOptions(sourceType, targetType);

    // 获取动态示例提示
    const examplePlaceholder = getRelationshipExamples(sourceType, targetType);

    // 如果当前选中的关系类型不在可用选项中，自动选择第一个
    const currentRelationshipType = relationshipTypes.includes(createForm.relationshipType)
      ? createForm.relationshipType
      : relationshipTypes[0] || '自定义';

    const handleSubmit = async () => {
      // 如果 label 为空，使用关系类型作为默认值
      const submitForm = {
        ...createForm,
        relationshipType: currentRelationshipType,
        label: createForm.label.trim() || currentRelationshipType,
      };

      setIsSaving(true);
      try {
        await onCreateRelationship?.(submitForm);
        // 重置表单
        setCreateForm({
          relationshipType: '好友关系',
          label: '',
          description: '',
          strength: 5,
          direction: 'one-way',
          color: '#8b5cf6',
          lineStyle: 'solid',
        });
        setAiInput(''); // 同时清空 AI 输入
      } catch (error) {
        console.error('创建关系失败:', error);
      } finally {
        setIsSaving(false);
      }
    };

    // AI 生成标签和描述
    const handleAIGenerate = async () => {
      if (!aiInput.trim()) return;
      if (!createRelationshipData.workId) {
        console.error('AI 生成失败: workId 为空');
        return;
      }

      setIsGeneratingAI(true);
      try {
        // 动态导入 DataService
        const { DataService } = await import('@/services/DataService');

        // 调用后端 AI 接口
        const result = await DataService.aiGenerateRelationship({
          workId: createRelationshipData.workId,
          userInput: aiInput.trim(),
          source: {
            id: createRelationshipData.sourceId,
            name: sourceLabel,
            type: createRelationshipData.sourceType,
            description: createRelationshipData.sourceDescription
          },
          target: {
            id: createRelationshipData.targetId,
            name: targetLabel,
            type: createRelationshipData.targetType,
            description: createRelationshipData.targetDescription
          },
          relationshipType: currentRelationshipType,
          direction: createForm.direction
        });

        setCreateForm(prev => ({
          ...prev,
          label: result.label.slice(0, 20),
          description: result.description,
        }));

        // 清空输入
        setAiInput('');
      } catch (error) {
        console.error('AI 生成失败:', error);
        // 降级：使用简单的本地生成
        const generatedLabel = `${sourceLabel}与${targetLabel}的${currentRelationshipType.replace('关系', '')}`;
        setCreateForm(prev => ({
          ...prev,
          label: generatedLabel.slice(0, 20),
          description: `基于您的想法：${aiInput}`,
        }));
        setAiInput('');
      } finally {
        setIsGeneratingAI(false);
      }
    };

    return (
      <div className="flex flex-col h-full text-sm">
        {/* 标题栏 */}
        <div className="p-4 pb-3 flex items-start justify-between">
          <div className="flex items-center gap-2 flex-1">
            <span className="text-2xl text-foreground leading-snug">{sourceLabel}</span>
            {createForm.direction === 'two-way' ? (
              <ArrowLeftRight className="w-4 h-4 text-muted-foreground" />
            ) : (
              <ArrowRight className="w-4 h-4 text-muted-foreground" />
            )}
            <span className="text-2xl text-foreground leading-snug">{targetLabel}</span>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose} className="h-8 w-8 p-0">
            <X className="w-4 h-4" />
          </Button>
        </div>

        <div className="flex-1 overflow-hidden">
          <ScrollArea className="h-full">
            <div className="p-6 space-y-5">
              {/* 关系类型 */}
              <div className="space-y-2">
                <Select
                  value={currentRelationshipType}
                  onValueChange={(value) => setCreateForm(prev => ({...prev, relationshipType: value}))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {relationshipTypes.map(type => (
                      <SelectItem key={type} value={type}>{type}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* 标签 */}
              <div className="space-y-2 pt-4">
                <Input
                  value={createForm.label}
                  onChange={(e) => setCreateForm(prev => ({...prev, label: e.target.value}))}
                  placeholder={examplePlaceholder}
                />
              </div>

              {/* 描述 */}
              <div className="space-y-2 pt-4">
                <Textarea
                  value={createForm.description}
                  onChange={(e) => setCreateForm(prev => ({...prev, description: e.target.value}))}
                  placeholder="描述这个关系的详细信息"
                  className="bg-input-background dark:bg-input/30"
                  rows={3}
                />
              </div>

              {/* 强度 */}
              <div className="space-y-2 pt-4">
                <div className="flex items-center justify-between">
                  <span className="text-foreground text-xs">{createForm.strength}/10</span>
                </div>
                <Slider
                  value={[createForm.strength]}
                  onValueChange={([value]) => setCreateForm(prev => ({...prev, strength: value}))}
                  min={1}
                  max={10}
                  step={1}
                />
              </div>

              {/* 方向 */}
              <div className="space-y-2 pt-4">
                <RadioGroup
                  value={createForm.direction}
                  onValueChange={(value: 'one-way' | 'two-way') => setCreateForm(prev => ({...prev, direction: value}))}
                  className="space-y-2"
                >
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="one-way" id="create-unidirectional" />
                    <label htmlFor="create-unidirectional" className="cursor-pointer text-sm">单向</label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="two-way" id="create-bidirectional" />
                    <label htmlFor="create-bidirectional" className="cursor-pointer text-sm">双向</label>
                  </div>
                </RadioGroup>
              </div>

              {/* 颜色 */}
              <div className="space-y-2 pt-4">
                <Input
                  type="color"
                  value={createForm.color}
                  onChange={(e) => setCreateForm(prev => ({...prev, color: e.target.value}))}
                  className="h-10 cursor-pointer"
                />
              </div>

              {/* 线型 */}
              <div className="space-y-2 pt-4">
                <Select
                  value={createForm.lineStyle}
                  onValueChange={(value: 'solid' | 'dashed' | 'dotted') => setCreateForm(prev => ({...prev, lineStyle: value}))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="solid">实线</SelectItem>
                    <SelectItem value="dashed">虚线</SelectItem>
                    <SelectItem value="dotted">点线</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* AI 智能填充区域 */}
              <div className="pt-6 border-t border-border mt-4">
                <div className="rounded-2xl border border-gray-200 bg-white shadow-sm px-4 py-3 dark:border-slate-700 dark:bg-slate-800">
                  <div className="flex flex-col gap-3">
                    <textarea
                      value={aiInput}
                      onChange={(e) => setAiInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey && aiInput.trim()) {
                          e.preventDefault();
                          handleAIGenerate();
                        }
                      }}
                      placeholder="输入你对这个关系的想法，AI 帮你完善标签和描述..."
                      className="w-full bg-transparent outline-none border-none text-[12px] placeholder:text-gray-400 resize-none leading-relaxed dark:text-slate-200 dark:placeholder:text-slate-500"
                      disabled={isGeneratingAI}
                      rows={2}
                      style={{
                        minHeight: '48px',
                        maxHeight: '120px',
                      }}
                    />
                    <div className="flex items-center justify-end">
                      {isGeneratingAI ? (
                        <button
                          disabled
                          className="w-10 h-10 rounded-full bg-gray-200 text-gray-500 flex items-center justify-center dark:bg-slate-700 dark:text-slate-400"
                        >
                          <Loader2 className="w-4 h-4 animate-spin" />
                        </button>
                      ) : aiInput.trim() ? (
                        <button
                          onClick={handleAIGenerate}
                          className="w-10 h-10 rounded-full transition-all flex items-center justify-center bg-gray-900 text-white hover:bg-gray-800 active:scale-95 shadow-sm dark:bg-blue-600 dark:hover:bg-blue-500"
                          aria-label="AI 生成"
                        >
                          <Send className="h-4 w-4" strokeWidth={2.4} />
                        </button>
                      ) : null}
                    </div>
                  </div>
                </div>
              </div>

              {/* 创建按钮 */}
              <div className="pt-4">
                <Button
                  className="w-full"
                  onClick={handleSubmit}
                  disabled={isSaving}
                >
                  {isSaving ? '创建中...' : '创建关系'}
                </Button>
              </div>
            </div>
          </ScrollArea>
        </div>
      </div>
    );
  };

  // 渲染时间线事件详情
  const renderTimelineEventDetails = () => {
    if (!timelineEventData) return null;

    const { event, entityLabel } = timelineEventData;
    const currentEvent = isEditingEvent && editedEvent ? editedEvent : event;

    // 获取事件类型配置
    const eventTypeConfig = EVENT_TYPE_OPTIONS.find((opt) => opt.value === currentEvent.eventType);

    const handleSaveEvent = async () => {
      if (editedEvent && onUpdateTimelineEvent) {
        setIsSaving(true);
        try {
          await onUpdateTimelineEvent(editedEvent.id, editedEvent);
          setIsEditingEvent(false);
          setEditedEvent(null);
        } finally {
          setIsSaving(false);
        }
      }
    };

    return (
      <div className="flex flex-col h-full text-sm">
        {/* 标题栏 */}
        <div className="p-6 pb-4 flex items-start justify-between">
          <h2
            className="text-2xl font-semibold text-foreground leading-relaxed m-0"
          >
            时间线事件
          </h2>
          <div className="flex items-center gap-1">
            {!isEditingEvent && (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                    <MoreVertical className="w-4 h-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-40">
                  <DropdownMenuItem
                    onClick={() => {
                      setEditedEvent({ ...event });
                      setIsEditingEvent(true);
                    }}
                  >
                    <Edit className="w-3.5 h-3.5 mr-2" />
                    编辑
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    onClick={() => handleDeleteClick('timeline', event.title)}
                    variant="destructive"
                  >
                    <Trash2 className="w-3.5 h-3.5 mr-2" />
                    删除
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            )}
            <Button variant="ghost" size="sm" onClick={onClose} className="h-8 w-8 p-0">
              <X className="w-4 h-4" />
            </Button>
          </div>
        </div>

        <ScrollArea className="flex-1 custom-scrollbar">
          <div className="p-6 space-y-5">
            {isEditingEvent ? (
              <>
                {/* 编辑模式 */}
                <div className="flex gap-2">
                  <Button onClick={handleSaveEvent} size="sm" disabled={isSaving}>
                    {isSaving ? '保存中...' : '保存'}
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      setIsEditingEvent(false);
                      setEditedEvent(null);
                    }}
                  >
                    取消
                  </Button>
                </div>

                {/* 关联实体 */}
                <div className="space-y-2">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">关联实体</Label>
                  <div className="text-foreground">{entityLabel}</div>
                </div>

                {/* 事件类型 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">事件类型</Label>
                  <Select
                    value={currentEvent.eventType}
                    onValueChange={(value: EventType) => setEditedEvent({ ...currentEvent, eventType: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {EVENT_TYPE_OPTIONS.map((opt) => (
                        <SelectItem key={opt.value} value={opt.value}>
                          {opt.icon} {opt.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* 事件标题 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">事件标题</Label>
                  <Input
                    value={currentEvent.title}
                    onChange={(e) => setEditedEvent({ ...currentEvent, title: e.target.value })}
                    placeholder="例如：获得神器、遇见导师"
                    className="border-border"
                  />
                </div>

                {/* 事件描述 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">事件描述</Label>
                  <Textarea
                    value={currentEvent.description || ''}
                    onChange={(e) => setEditedEvent({ ...currentEvent, description: e.target.value })}
                    placeholder="详细描述这个事件..."
                    className="border-border min-h-[100px] resize-none"
                    rows={4}
                  />
                </div>

                {/* 事件图标 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">事件图标</Label>
                  <Input
                    value={currentEvent.icon || ''}
                    onChange={(e) => setEditedEvent({ ...currentEvent, icon: e.target.value })}
                    placeholder="输入emoji，例如：🎯"
                    className="border-border"
                  />
                </div>

                {/* 颜色标记 */}
                <div className="space-y-2 pt-4 border-t border-border">
                  <Label className="text-xs text-muted-foreground uppercase tracking-wider">颜色标记</Label>
                  <Input
                    type="color"
                    value={currentEvent.color || '#f59e0b'}
                    onChange={(e) => setEditedEvent({ ...currentEvent, color: e.target.value })}
                    className="h-10 cursor-pointer border-border"
                  />
                </div>
              </>
            ) : (
              <>
                {/* 查看模式 */}
                {/* 关联实体 */}
                <div className="flex items-center gap-3">
                  <div className="text-xs text-muted-foreground uppercase tracking-wider">关联实体</div>
                  <div className="text-foreground">{entityLabel}</div>
                </div>

                {/* 事件类型 */}
                <div className="flex items-center gap-3 pt-4 border-t border-border">
                  <div className="text-xs text-muted-foreground uppercase tracking-wider">事件类型</div>
                  <div className="text-foreground">
                    {eventTypeConfig?.icon} {eventTypeConfig?.label}
                  </div>
                </div>

                {/* 事件标题 */}
                <div className="flex items-center gap-3 pt-4 border-t border-border">
                  <div className="text-xs text-muted-foreground uppercase tracking-wider">标题</div>
                  <div className="text-foreground">{currentEvent.title}</div>
                </div>

                {/* 事件描述 */}
                {currentEvent.description && (
                  <div className="space-y-2 pt-4 border-t border-border">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">描述</div>
                    <p className="text-foreground/80 leading-relaxed">{currentEvent.description}</p>
                  </div>
                )}

                {/* 事件图标 */}
                {currentEvent.icon && (
                  <div className="flex items-center gap-3 pt-4 border-t border-border">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">图标</div>
                    <div className="text-foreground text-xl">{currentEvent.icon}</div>
                  </div>
                )}

                {/* 所属章节 */}
                {currentEvent.chapterNumber && (
                  <div className="flex items-center gap-3 pt-4 border-t border-border">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">所属章节</div>
                    <div className="text-foreground">第 {currentEvent.chapterNumber} 章</div>
                  </div>
                )}

                {/* 颜色标记 */}
                {currentEvent.color && (
                  <div className="flex items-center gap-3 pt-4 border-t border-border">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">颜色标记</div>
                    <div className="flex items-center gap-2">
                      <div
                        className="w-5 h-5 rounded border border-border"
                        style={{ backgroundColor: currentEvent.color }}
                      />
                      <span className="text-foreground text-xs">{currentEvent.color}</span>
                    </div>
                  </div>
                )}

                {/* 创建时间 */}
                {currentEvent.createdAt && (
                  <div className="flex items-center gap-3 pt-4 border-t border-border">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">创建时间</div>
                    <div className="text-foreground text-xs">
                      {new Date(currentEvent.createdAt).toLocaleString('zh-CN')}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </ScrollArea>
      </div>
    );
  };

  // 渲染创建时间线事件表单
  const renderCreateTimelineEvent = () => {
    if (!createTimelineEventData) return null;

    const { workId, entityId, entityType, entityLabel } = createTimelineEventData;

    // 初始化表单（如果有预设实体）
    if (entityId && !timelineForm.entityId) {
      setTimelineForm({
        ...timelineForm,
        entityId,
        entityType: entityType || 'character',
      });
    }

    const handleSubmit = async () => {
      if (!timelineForm.title.trim()) {
        alert('请输入事件标题');
        return;
      }

      if (!timelineForm.entityId) {
        alert('请选择关联实体');
        return;
      }

      setIsSaving(true);
      try {
        await onCreateTimelineEvent?.({
          entityId: timelineForm.entityId,
          entityType: timelineForm.entityType,
          eventType: timelineForm.eventType,
          title: timelineForm.title,
          description: timelineForm.description || undefined,
          icon: timelineForm.icon || undefined,
          chapterId: timelineForm.chapterId || undefined,
          chapterNumber: timelineForm.chapterNumber || undefined,
          color: timelineForm.color,
        });
        // 重置表单
        setTimelineForm({
          entityId: '',
          entityType: 'character',
          eventType: 'milestone',
          title: '',
          description: '',
          icon: '🎯',
          chapterId: '',
          chapterNumber: 1,
          color: '#f59e0b',
        });
      } catch (error) {
        console.error('创建时间线事件失败:', error);
      } finally {
        setIsSaving(false);
      }
    };

    return (
      <div className="flex flex-col h-full text-sm">
        {/* 标题栏 */}
        <div className="p-6 pb-4 flex items-start justify-between">
          <h2
            className="text-xl font-semibold text-foreground leading-relaxed m-0"
          >
            创建时间线事件
          </h2>
          <Button variant="ghost" size="sm" onClick={onClose} className="h-8 w-8 p-0">
            <X className="w-4 h-4" />
          </Button>
        </div>

        <div className="flex-1 overflow-hidden">
          <ScrollArea className="h-full">
            <div className="p-6 space-y-5">
              {/* 关联实体 */}
              <div className="space-y-2">
                <Label className="text-xs text-muted-foreground uppercase tracking-wider">
                  关联实体 <span className="text-destructive">*</span>
                </Label>
                {entityLabel ? (
                  <div className="text-foreground">{entityLabel}</div>
                ) : (
                  <Select
                    value={timelineForm.entityId}
                    onValueChange={(value) => {
                      const selectedEntity = entities.find((ent) => ent.id === value);
                      setTimelineForm({
                        ...timelineForm,
                        entityId: value,
                        entityType: selectedEntity?.type || 'character',
                      });
                    }}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="请选择实体..." />
                    </SelectTrigger>
                    <SelectContent>
                      {entities.map((ent) => (
                        <SelectItem key={ent.id} value={ent.id}>
                          {ent.type === 'character' ? '👤' : ent.type === 'location' ? '📍' : '📖'} {ent.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              </div>

              {/* 事件类型 */}
              <div className="space-y-2 pt-4 border-t border-border">
                <Label className="text-xs text-muted-foreground uppercase tracking-wider">
                  事件类型 <span className="text-destructive">*</span>
                </Label>
                <Select
                  value={timelineForm.eventType}
                  onValueChange={(value: EventType) => {
                    const selectedType = EVENT_TYPE_OPTIONS.find((opt) => opt.value === value);
                    setTimelineForm({
                      ...timelineForm,
                      eventType: value,
                      icon: selectedType?.icon || '🎯',
                      color: selectedType?.color || '#f59e0b',
                    });
                  }}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {EVENT_TYPE_OPTIONS.map((opt) => (
                      <SelectItem key={opt.value} value={opt.value}>
                        {opt.icon} {opt.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* 事件标题 */}
              <div className="space-y-2 pt-4 border-t border-border">
                <Label className="text-xs text-muted-foreground uppercase tracking-wider">
                  事件标题 <span className="text-destructive">*</span>
                </Label>
                <Input
                  value={timelineForm.title}
                  onChange={(e) => setTimelineForm({ ...timelineForm, title: e.target.value })}
                  placeholder="例如：获得神器、遇见导师"
                />
              </div>

              {/* 事件描述 */}
              <div className="space-y-2 pt-4 border-t border-border">
                <Label className="text-xs text-muted-foreground uppercase tracking-wider">事件描述</Label>
                <Textarea
                  value={timelineForm.description}
                  onChange={(e) => setTimelineForm({ ...timelineForm, description: e.target.value })}
                  placeholder="详细描述这个事件..."
                  rows={4}
                />
              </div>

              {/* 事件图标 */}
              <div className="space-y-2 pt-4 border-t border-border">
                <Label className="text-xs text-muted-foreground uppercase tracking-wider">事件图标</Label>
                <Input
                  value={timelineForm.icon}
                  onChange={(e) => setTimelineForm({ ...timelineForm, icon: e.target.value })}
                  placeholder="输入emoji，例如：🎯"
                />
              </div>

              {/* 所属章节 */}
              <div className="space-y-2 pt-4 border-t border-border">
                <Label className="text-xs text-muted-foreground uppercase tracking-wider">所属章节（可选）</Label>
                <Select
                  value={timelineForm.chapterId || 'none'}
                  onValueChange={(value) => {
                    if (value === 'none') {
                      setTimelineForm({
                        ...timelineForm,
                        chapterId: '',
                        chapterNumber: undefined,
                      });
                    } else {
                      const selectedChapter = chapters.find((ch) => ch.id === value);
                      setTimelineForm({
                        ...timelineForm,
                        chapterId: value,
                        chapterNumber: selectedChapter?.order || 1,
                      });
                    }
                  }}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="不关联章节" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">不关联章节</SelectItem>
                    {chapters.map((ch) => (
                      <SelectItem key={ch.id} value={ch.id}>
                        第 {ch.order} 章 - {ch.title}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* 颜色标记 */}
              <div className="space-y-2 pt-4 border-t border-border">
                <Label className="text-xs text-muted-foreground uppercase tracking-wider">颜色标记</Label>
                <div className="flex gap-2">
                  {['#f59e0b', '#ef4444', '#3b82f6', '#10b981', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'].map(color => (
                    <button
                      key={color}
                      type="button"
                      onClick={() => setTimelineForm({ ...timelineForm, color })}
                      className={`w-7 h-7 rounded-full transition-all ${
                        timelineForm.color === color
                          ? 'scale-110 ring-2 ring-offset-2 ring-foreground/20'
                          : 'hover:scale-105 opacity-60'
                      }`}
                      style={{ backgroundColor: color }}
                    />
                  ))}
                </div>
              </div>

              {/* 创建按钮 */}
              <div className="pt-4">
                <Button
                  className="w-full"
                  onClick={handleSubmit}
                  disabled={isSaving || !timelineForm.title.trim() || !timelineForm.entityId}
                >
                  {isSaving ? '创建中...' : '创建事件'}
                </Button>
              </div>
            </div>
          </ScrollArea>
        </div>
      </div>
    );
  };

  return (
    <div className="property-panel h-full flex flex-col bg-card border-l border-border-light">
      <div className="panel-content flex-1 overflow-y-auto">
        {mode === 'idle' && renderIdleState()}
        {mode === 'node' && renderNodeDetails()}
        {mode === 'relationship' && renderRelationshipDetails()}
        {mode === 'create' && renderCreateRelationship()}
        {mode === 'timeline' && renderTimelineEventDetails()}
        {mode === 'createTimeline' && renderCreateTimelineEvent()}
      </div>

      {/* 删除确认对话框 */}
      <Dialog open={deleteDialog.open} onOpenChange={(open) => !open && handleCancelDelete()}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>确认删除</DialogTitle>
            <DialogDescription>
              您确定要删除 <span className="font-semibold text-foreground">"{deleteDialog.name}"</span> 吗？此操作无法撤销。
            </DialogDescription>
          </DialogHeader>

          <div className="flex items-center space-x-2 py-4">
            <Checkbox
              id="dont-ask-again"
              checked={dontAskAgain}
              onCheckedChange={(checked) => setDontAskAgain(checked === true)}
            />
            <label
              htmlFor="dont-ask-again"
              className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
            >
              本次登录不再提醒
            </label>
          </div>

          <DialogFooter className="gap-2 sm:gap-0">
            <Button variant="outline" onClick={handleCancelDelete}>
              取消
            </Button>
            <Button variant="destructive" onClick={handleConfirmDelete}>
              确认删除
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default PropertyPanel;
