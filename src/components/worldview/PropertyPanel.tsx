/**
 * 属性面板组件
 * 显示节点或关系的详细信息
 */
import React, { useState, useEffect } from 'react';
import { X, Users, MapPin, BookOpen, Link2, Edit2, Trash2, Star, Save, Clock, Calendar } from 'lucide-react';
import { Character, Location, Setting } from '@/types/novel';
import { Relationship, EntityType } from '@/types/relationship';
import { TimelineEvent, EventType, EVENT_TYPE_OPTIONS } from '@/types/timeline';

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
    targetId: string;
    targetType: EntityType;
    targetLabel: string;
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
  onSaveNode,
  onDeleteNode,
  onCreateRelationship,
  onEditRelationship,
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

  // 时间线事件表单状态
  const [timelineForm, setTimelineForm] = useState({
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
    // 关系类型分布（取前5个）
    const topTypes = Object.entries(stats.relationshipsByType)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);

    return (
      <div className="space-y-6">
        {/* 统计概览 */}
        <div>
          <h3 className="text-sm font-semibold text-gray-600 uppercase mb-3">📊 世界观概览</h3>
          <div className="space-y-2">
            <div className="flex items-center justify-between p-2 bg-gray-100 rounded">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Users className="w-4 h-4" />
                <span>角色</span>
              </div>
              <span className="text-lg font-semibold text-gray-900">{stats.characters}</span>
            </div>
            <div className="flex items-center justify-between p-2 bg-gray-100 rounded">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <MapPin className="w-4 h-4" />
                <span>地点</span>
              </div>
              <span className="text-lg font-semibold text-gray-900">{stats.locations}</span>
            </div>
            <div className="flex items-center justify-between p-2 bg-gray-100 rounded">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <BookOpen className="w-4 h-4" />
                <span>设定</span>
              </div>
              <span className="text-lg font-semibold text-gray-900">{stats.settings}</span>
            </div>
            <div className="flex items-center justify-between p-2 bg-gray-100 rounded">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Link2 className="w-4 h-4" />
                <span>关系</span>
              </div>
              <span className="text-lg font-semibold text-gray-900">{stats.relationships}</span>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-200"></div>

        {/* 快捷操作 */}
        <div>
          <h3 className="text-sm font-semibold text-gray-600 uppercase mb-3">💡 快捷操作</h3>
          <div className="space-y-2 text-sm text-gray-500">
            <div className="flex items-start gap-2">
              <span className="text-blue-400">•</span>
              <span>点击节点查看详情</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-blue-400">•</span>
              <span>点击关系线编辑关系</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-blue-400">•</span>
              <span>使用[创建关系]建立新关系</span>
            </div>
          </div>
        </div>

        {/* 关系类型分布 */}
        {topTypes.length > 0 && (
          <>
            <div className="border-t border-gray-200"></div>
            <div>
              <h3 className="text-sm font-semibold text-gray-600 uppercase mb-3">🔥 关系类型分布</h3>
              <div className="space-y-2">
                {topTypes.map(([type, count]) => {
                  const percentage = (count / stats.relationships) * 100;
                  return (
                    <div key={type}>
                      <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                        <span>{type}</span>
                        <span>{count}</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all"
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </>
        )}
      </div>
    );
  };

  // 渲染节点详情
  const renderNodeDetails = () => {
    if (!nodeData) return null;

    const { type, entity } = nodeData;

    // 过滤相关关系（使用蛇形命名）
    const nodeRelations = relatedRelationships.filter(
      (rel) =>
        (rel.sourceId === nodeData.id && rel.sourceType === type) ||
        (rel.targetId === nodeData.id && rel.targetType === type)
    );

    // 角色详情
    if (type === 'character') {
      const character = (isEditing && editedEntity ? editedEntity : entity) as Character;
      return (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold text-gray-900 flex items-center gap-2">
              <Users className="w-5 h-5 text-blue-400" />
              角色详情
            </h3>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-900 transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="space-y-3">
            <div>
              <label className="block text-xs text-gray-500 mb-1">📛 姓名</label>
              {isEditing ? (
                <input
                  type="text"
                  value={character.name}
                  onChange={(e) => setEditedEntity({ ...character, name: e.target.value })}
                  className="w-full px-3 py-2 bg-white border border-blue-500 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              ) : (
                <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">{character.name}</div>
              )}
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-1">🎭 角色</label>
              {isEditing ? (
                <input
                  type="text"
                  value={character.role || ''}
                  onChange={(e) => setEditedEntity({ ...character, role: e.target.value })}
                  className="w-full px-3 py-2 bg-white border border-blue-500 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="例如：主角、配角"
                />
              ) : (
                <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">{character.role || '-'}</div>
              )}
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-1">📝 描述</label>
              {isEditing ? (
                <textarea
                  value={character.description || ''}
                  onChange={(e) => setEditedEntity({ ...character, description: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-750 border border-blue-500 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  rows={4}
                  placeholder="输入角色描述..."
                />
              ) : (
                <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-600 max-h-24 overflow-y-auto">
                  {character.description || '-'}
                </div>
              )}
            </div>
          </div>

          {/* 相关关系 */}
          {nodeRelations.length > 0 && (
            <>
              <div className="border-t border-gray-200"></div>
              <div>
                <h4 className="text-sm font-semibold text-gray-600 mb-2">🔗 相关关系 ({nodeRelations.length})</h4>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {nodeRelations.slice(0, 10).map((rel) => {
                    const isSource = rel.sourceId === nodeData.id;
                    return (
                      <div
                        key={rel.id}
                        onClick={() => onRelationshipClick?.(rel.id)}
                        className="p-2 bg-gray-100 hover:bg-gray-200 rounded cursor-pointer transition-colors"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-900">{rel.label}</span>
                          <div className="flex items-center gap-1">
                            {Array.from({ length: Math.min(rel.strength, 5) }).map((_, i) => (
                              <Star key={i} className="w-3 h-3 text-yellow-400 fill-yellow-400" />
                            ))}
                          </div>
                        </div>
                        <div className="text-xs text-gray-500 mt-1">
                          {isSource ? '→' : '←'} {rel.relationshipType}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </>
          )}

          {/* 操作按钮 */}
          <div className="border-t border-gray-700 pt-4 flex gap-2">
            {isEditing ? (
              <>
                <button
                  onClick={handleSaveEdit}
                  disabled={isSaving}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded transition-colors"
                >
                  <Save className="w-4 h-4" />
                  {isSaving ? '保存中...' : '保存'}
                </button>
                <button
                  onClick={handleCancelEdit}
                  disabled={isSaving}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 disabled:cursor-not-allowed rounded transition-colors"
                >
                  <X className="w-4 h-4" />
                  取消
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={handleStartEdit}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded transition-colors"
                >
                  <Edit2 className="w-4 h-4" />
                  编辑角色
                </button>
                <button
                  onClick={onDeleteNode}
                  className="flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-100 rounded transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </>
            )}
          </div>
        </div>
      );
    }

    // 地点详情
    if (type === 'location') {
      const location = (isEditing && editedEntity ? editedEntity : entity) as Location;
      return (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold text-gray-900 flex items-center gap-2">
              <MapPin className="w-5 h-5 text-green-400" />
              地点详情
            </h3>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-900 transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="space-y-3">
            <div>
              <label className="block text-xs text-gray-500 mb-1">📛 名称</label>
              {isEditing ? (
                <input
                  type="text"
                  value={location.name}
                  onChange={(e) => setEditedEntity({ ...location, name: e.target.value })}
                  className="w-full px-3 py-2 bg-white border border-green-500 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              ) : (
                <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">{location.name}</div>
              )}
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-1">🏷️ 类型</label>
              {isEditing ? (
                <input
                  type="text"
                  value={location.type || ''}
                  onChange={(e) => setEditedEntity({ ...location, type: e.target.value })}
                  className="w-full px-3 py-2 bg-white border border-green-500 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="例如：城市、建筑"
                />
              ) : (
                <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">{location.type || '-'}</div>
              )}
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-1">📝 描述</label>
              {isEditing ? (
                <textarea
                  value={location.description || ''}
                  onChange={(e) => setEditedEntity({ ...location, description: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-750 border border-green-500 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-green-500 resize-none"
                  rows={4}
                  placeholder="输入地点描述..."
                />
              ) : (
                <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-600 max-h-24 overflow-y-auto">
                  {location.description || '-'}
                </div>
              )}
            </div>
          </div>

          {/* 相关关系 */}
          {nodeRelations.length > 0 && (
            <>
              <div className="border-t border-gray-200"></div>
              <div>
                <h4 className="text-sm font-semibold text-gray-600 mb-2">🔗 相关关系 ({nodeRelations.length})</h4>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {nodeRelations.slice(0, 10).map((rel) => (
                    <div
                      key={rel.id}
                      onClick={() => onRelationshipClick?.(rel.id)}
                      className="p-2 bg-gray-100 hover:bg-gray-200 rounded cursor-pointer transition-colors"
                    >
                      <div className="text-sm text-gray-900">{rel.label}</div>
                      <div className="text-xs text-gray-500 mt-1">{rel.relationshipType}</div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {/* 操作按钮 */}
          <div className="border-t border-gray-700 pt-4 flex gap-2">
            {isEditing ? (
              <>
                <button
                  onClick={handleSaveEdit}
                  disabled={isSaving}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded transition-colors"
                >
                  <Save className="w-4 h-4" />
                  {isSaving ? '保存中...' : '保存'}
                </button>
                <button
                  onClick={handleCancelEdit}
                  disabled={isSaving}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 disabled:cursor-not-allowed rounded transition-colors"
                >
                  <X className="w-4 h-4" />
                  取消
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={handleStartEdit}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded transition-colors"
                >
                  <Edit2 className="w-4 h-4" />
                  编辑地点
                </button>
                <button
                  onClick={onDeleteNode}
                  className="flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-100 rounded transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </>
            )}
          </div>
        </div>
      );
    }

    // 设定详情
    if (type === 'setting') {
      const setting = (isEditing && editedEntity ? editedEntity : entity) as Setting;
      return (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold text-gray-900 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-orange-400" />
              设定详情
            </h3>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-900 transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="space-y-3">
            <div>
              <label className="block text-xs text-gray-500 mb-1">📛 标题</label>
              {isEditing ? (
                <input
                  type="text"
                  value={setting.title}
                  onChange={(e) => setEditedEntity({ ...setting, title: e.target.value })}
                  className="w-full px-3 py-2 bg-white border border-orange-500 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              ) : (
                <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">{setting.title}</div>
              )}
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-1">🏷️ 分类</label>
              {isEditing ? (
                <input
                  type="text"
                  value={setting.category || ''}
                  onChange={(e) => setEditedEntity({ ...setting, category: e.target.value })}
                  className="w-full px-3 py-2 bg-white border border-orange-500 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-orange-500"
                  placeholder="例如：武功、法宝"
                />
              ) : (
                <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">{setting.category || '-'}</div>
              )}
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-1">📝 内容</label>
              {isEditing ? (
                <textarea
                  value={setting.content || ''}
                  onChange={(e) => setEditedEntity({ ...setting, content: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-750 border border-orange-500 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-orange-500 resize-none"
                  rows={4}
                  placeholder="输入设定内容..."
                />
              ) : (
                <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-600 max-h-24 overflow-y-auto">
                  {setting.content || '-'}
                </div>
              )}
            </div>
          </div>

          {/* 相关关系 */}
          {nodeRelations.length > 0 && (
            <>
              <div className="border-t border-gray-200"></div>
              <div>
                <h4 className="text-sm font-semibold text-gray-600 mb-2">🔗 相关关系 ({nodeRelations.length})</h4>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {nodeRelations.slice(0, 10).map((rel) => (
                    <div
                      key={rel.id}
                      onClick={() => onRelationshipClick?.(rel.id)}
                      className="p-2 bg-gray-100 hover:bg-gray-200 rounded cursor-pointer transition-colors"
                    >
                      <div className="text-sm text-gray-900">{rel.label}</div>
                      <div className="text-xs text-gray-500 mt-1">{rel.relationshipType}</div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {/* 操作按钮 */}
          <div className="border-t border-gray-700 pt-4 flex gap-2">
            {isEditing ? (
              <>
                <button
                  onClick={handleSaveEdit}
                  disabled={isSaving}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-white bg-orange-600 hover:bg-orange-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded transition-colors"
                >
                  <Save className="w-4 h-4" />
                  {isSaving ? '保存中...' : '保存'}
                </button>
                <button
                  onClick={handleCancelEdit}
                  disabled={isSaving}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 disabled:cursor-not-allowed rounded transition-colors"
                >
                  <X className="w-4 h-4" />
                  取消
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={handleStartEdit}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-white bg-orange-600 hover:bg-orange-700 rounded transition-colors"
                >
                  <Edit2 className="w-4 h-4" />
                  编辑设定
                </button>
                <button
                  onClick={onDeleteNode}
                  className="flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-100 rounded transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </>
            )}
          </div>
        </div>
      );
    }

    return null;
  };

  // 渲染关系详情
  const renderRelationshipDetails = () => {
    if (!relationshipData) return null;

    const { relationship, sourceLabel, targetLabel } = relationshipData;

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Link2 className="w-5 h-5 text-purple-400" />
            关系详情
          </h3>
          <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 关系连接示意 */}
        <div className="p-3 bg-gray-100 rounded">
          <div className="flex items-center justify-between text-sm">
            <div className="text-gray-900 font-medium">{sourceLabel}</div>
            <div className="text-gray-500">
              {relationship.direction === 'two-way' ? '↔' : '→'}
            </div>
            <div className="text-gray-900 font-medium">{targetLabel}</div>
          </div>
        </div>

        <div className="space-y-3">
          {/* 关系类型 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🏷️ 关系类型</label>
            <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">
              {relationship.relationshipType}
            </div>
          </div>

          {/* 显示标签 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">📛 显示标签</label>
            <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">{relationship.label}</div>
          </div>

          {/* 关系描述 */}
          {relationship.description && (
            <div>
              <label className="block text-xs text-gray-500 mb-1">📝 关系描述</label>
              <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-600 max-h-24 overflow-y-auto">
                {relationship.description}
              </div>
            </div>
          )}

          {/* 关系强度 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">⚡ 关系强度</label>
            <div className="flex items-center gap-3">
              <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all"
                  style={{ width: `${(relationship.strength / 10) * 100}%` }}
                ></div>
              </div>
              <span className="text-sm text-gray-900 font-medium">{relationship.strength}/10</span>
            </div>
          </div>

          {/* 关系方向 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🔄 关系方向</label>
            <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">
              {relationship.direction === 'one-way' ? '单向 (A → B)' : '双向 (A ↔ B)'}
            </div>
          </div>

          {/* 视觉样式 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🎨 视觉样式</label>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-500">线条:</span>
                <span className="text-sm text-gray-900">
                  {relationship.lineStyle === 'solid' && '实线 —'}
                  {relationship.lineStyle === 'dashed' && '虚线 - - -'}
                  {relationship.lineStyle === 'dotted' && '点线 · · ·'}
                </span>
              </div>
              {relationship.color && (
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-500">颜色:</span>
                  <div
                    className="w-4 h-4 rounded border border-gray-300"
                    style={{ backgroundColor: relationship.color }}
                  ></div>
                  <span className="text-sm text-gray-900">{relationship.color}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* 操作按钮 */}
        <div className="border-t border-gray-700 pt-4 flex gap-2">
          <button
            onClick={onEditRelationship}
            className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 rounded transition-colors"
          >
            <Edit2 className="w-4 h-4" />
            编辑关系
          </button>
          <button
            onClick={onDeleteRelationship}
            className="flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-100 rounded transition-colors"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    );
  };

  // 渲染创建关系表单
  const renderCreateRelationship = () => {
    if (!createRelationshipData) return null;

    const { sourceLabel, targetLabel } = createRelationshipData;

    const handleSubmit = async () => {
      if (!createForm.label.trim()) {
        alert('请输入关系标签');
        return;
      }

      setIsSaving(true);
      try {
        await onCreateRelationship?.(createForm);
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
      } catch (error) {
        console.error('创建关系失败:', error);
      } finally {
        setIsSaving(false);
      }
    };

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Link2 className="w-5 h-5 text-blue-400" />
            创建关系
          </h3>
          <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 关系连接示意 */}
        <div className="p-3 bg-gray-100 rounded">
          <div className="flex items-center justify-between text-sm">
            <div className="text-white font-medium">{sourceLabel}</div>
            <div className="text-blue-400">→</div>
            <div className="text-gray-900 font-medium">{targetLabel}</div>
          </div>
        </div>

        <div className="space-y-3">
          {/* 关系类型 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🏷️ 关系类型 *</label>
            <select
              value={createForm.relationshipType}
              onChange={(e) => setCreateForm({ ...createForm, relationshipType: e.target.value })}
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="亲属关系">亲属关系</option>
              <option value="师徒关系">师徒关系</option>
              <option value="好友关系">好友关系</option>
              <option value="盟友关系">盟友关系</option>
              <option value="敌对关系">敌对关系</option>
              <option value="同事关系">同事关系</option>
              <option value="恋人关系">恋人关系</option>
              <option value="竞争关系">竞争关系</option>
            </select>
          </div>

          {/* 显示标签 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">📛 显示标签 *</label>
            <input
              type="text"
              value={createForm.label}
              onChange={(e) => setCreateForm({ ...createForm, label: e.target.value })}
              placeholder="例如：师徒、好友"
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* 关系描述 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">📝 关系描述</label>
            <textarea
              value={createForm.description}
              onChange={(e) => setCreateForm({ ...createForm, description: e.target.value })}
              placeholder="描述这段关系..."
              rows={3}
              className="w-full px-3 py-2 bg-gray-750 border border-gray-600 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            />
          </div>

          {/* 关系强度 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">⚡ 关系强度: {createForm.strength}/10</label>
            <input
              type="range"
              min="1"
              max="10"
              value={createForm.strength}
              onChange={(e) => setCreateForm({ ...createForm, strength: parseInt(e.target.value) })}
              className="w-full"
            />
          </div>

          {/* 关系方向 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🔄 关系方向</label>
            <div className="space-y-2">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  checked={createForm.direction === 'one-way'}
                  onChange={() => setCreateForm({ ...createForm, direction: 'one-way' })}
                  className="text-blue-500"
                />
                <span className="text-sm text-gray-600">单向 (A → B)</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  checked={createForm.direction === 'two-way'}
                  onChange={() => setCreateForm({ ...createForm, direction: 'two-way' })}
                  className="text-blue-500"
                />
                <span className="text-sm text-gray-300">双向 (A ↔ B)</span>
              </label>
            </div>
          </div>

          {/* 线条样式 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🎨 线条样式</label>
            <select
              value={createForm.lineStyle}
              onChange={(e) => setCreateForm({ ...createForm, lineStyle: e.target.value as any })}
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="solid">实线 —</option>
              <option value="dashed">虚线 - - -</option>
              <option value="dotted">点线 · · ·</option>
            </select>
          </div>

          {/* 线条颜色 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🎨 线条颜色</label>
            <div className="flex items-center gap-2">
              <input
                type="color"
                value={createForm.color}
                onChange={(e) => setCreateForm({ ...createForm, color: e.target.value })}
                className="w-12 h-8 bg-white border border-gray-300 rounded cursor-pointer"
              />
              <span className="text-sm text-gray-600">{createForm.color}</span>
            </div>
          </div>
        </div>

        {/* 操作按钮 */}
        <div className="border-t border-gray-700 pt-4 flex gap-2">
          <button
            onClick={handleSubmit}
            disabled={isSaving || !createForm.label.trim()}
            className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded transition-colors"
          >
            <Save className="w-4 h-4" />
            {isSaving ? '创建中...' : '创建关系'}
          </button>
          <button
            onClick={onClose}
            disabled={isSaving}
            className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 disabled:cursor-not-allowed rounded transition-colors"
          >
            <X className="w-4 h-4" />
            取消
          </button>
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

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Clock className="w-5 h-5 text-yellow-400" />
            时间线事件
          </h3>
          <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-3">
          {/* 关联实体 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🔗 关联实体</label>
            <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">{entityLabel}</div>
          </div>

          {/* 事件类型 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🏷️ 事件类型</label>
            {isEditingEvent ? (
              <select
                value={currentEvent.eventType}
                onChange={(e) => setEditedEvent({ ...currentEvent, eventType: e.target.value as EventType })}
                className="w-full px-3 py-2 bg-gray-750 border border-yellow-500 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-yellow-500"
              >
                {EVENT_TYPE_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.icon} {opt.label}
                  </option>
                ))}
              </select>
            ) : (
              <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">
                {eventTypeConfig?.icon} {eventTypeConfig?.label}
              </div>
            )}
          </div>

          {/* 事件标题 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">📛 事件标题</label>
            {isEditingEvent ? (
              <input
                type="text"
                value={currentEvent.title}
                onChange={(e) => setEditedEvent({ ...currentEvent, title: e.target.value })}
                className="w-full px-3 py-2 bg-gray-750 border border-yellow-500 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-yellow-500"
                placeholder="例如：获得神器、遇见导师"
              />
            ) : (
              <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">{currentEvent.title}</div>
            )}
          </div>

          {/* 事件描述 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">📝 事件描述</label>
            {isEditingEvent ? (
              <textarea
                value={currentEvent.description || ''}
                onChange={(e) => setEditedEvent({ ...currentEvent, description: e.target.value })}
                className="w-full px-3 py-2 bg-gray-750 border border-yellow-500 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-yellow-500 resize-none"
                rows={4}
                placeholder="详细描述这个事件..."
              />
            ) : (
              <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-600 max-h-24 overflow-y-auto">
                {currentEvent.description || '-'}
              </div>
            )}
          </div>

          {/* 事件图标 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🎨 事件图标</label>
            {isEditingEvent ? (
              <input
                type="text"
                value={currentEvent.icon || ''}
                onChange={(e) => setEditedEvent({ ...currentEvent, icon: e.target.value })}
                className="w-full px-3 py-2 bg-gray-750 border border-yellow-500 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-yellow-500"
                placeholder="输入emoji，例如：🎯"
              />
            ) : (
              <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">
                {currentEvent.icon || '-'}
              </div>
            )}
          </div>

          {/* 所属章节 */}
          {currentEvent.chapterNumber && (
            <div>
              <label className="block text-xs text-gray-500 mb-1">📖 所属章节</label>
              <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">
                第 {currentEvent.chapterNumber} 章
              </div>
            </div>
          )}

          {/* 颜色标记 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🎨 颜色标记</label>
            {isEditingEvent ? (
              <div className="flex items-center gap-2">
                <input
                  type="color"
                  value={currentEvent.color || '#f59e0b'}
                  onChange={(e) => setEditedEvent({ ...currentEvent, color: e.target.value })}
                  className="w-12 h-8 bg-white border border-gray-300 rounded cursor-pointer"
                />
                <span className="text-sm text-gray-300">{currentEvent.color || '#f59e0b'}</span>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <div
                  className="w-4 h-4 rounded border border-gray-600"
                  style={{ backgroundColor: currentEvent.color || '#f59e0b' }}
                ></div>
                <span className="text-sm text-white">{currentEvent.color || '#f59e0b'}</span>
              </div>
            )}
          </div>

          {/* 创建时间 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🕐 创建时间</label>
            <div className="px-3 py-2 bg-gray-750 rounded text-sm text-gray-300">
              {new Date(currentEvent.createdAt).toLocaleString('zh-CN')}
            </div>
          </div>
        </div>

        {/* 操作按钮 */}
        <div className="border-t border-gray-700 pt-4 flex gap-2">
          {isEditingEvent ? (
            <>
              <button
                onClick={async () => {
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
                }}
                disabled={isSaving}
                className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-white bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded transition-colors"
              >
                <Save className="w-4 h-4" />
                {isSaving ? '保存中...' : '保存'}
              </button>
              <button
                onClick={() => {
                  setIsEditingEvent(false);
                  setEditedEvent(null);
                }}
                disabled={isSaving}
                className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 disabled:cursor-not-allowed rounded transition-colors"
              >
                <X className="w-4 h-4" />
                取消
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => {
                  setEditedEvent({ ...event });
                  setIsEditingEvent(true);
                }}
                className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-white bg-yellow-600 hover:bg-yellow-700 rounded transition-colors"
              >
                <Edit2 className="w-4 h-4" />
                编辑事件
              </button>
              <button
                onClick={onDeleteTimelineEvent}
                className="flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-100 rounded transition-colors"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </>
          )}
        </div>
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
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Calendar className="w-5 h-5 text-yellow-400" />
            创建时间线事件
          </h3>
          <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-3">
          {/* 关联实体 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🔗 关联实体 *</label>
            {entityLabel ? (
              <div className="px-3 py-2 bg-gray-100 rounded text-sm text-gray-900">{entityLabel}</div>
            ) : (
              <select
                value={timelineForm.entityId}
                onChange={(e) => {
                  const selectedEntity = entities.find((ent) => ent.id === e.target.value);
                  setTimelineForm({
                    ...timelineForm,
                    entityId: e.target.value,
                    entityType: selectedEntity?.type || 'character',
                  });
                }}
                className="w-full px-3 py-2 bg-white border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-yellow-500"
              >
                <option value="">请选择实体...</option>
                {entities.map((ent) => (
                  <option key={ent.id} value={ent.id}>
                    {ent.type === 'character' && '👤'}
                    {ent.type === 'location' && '📍'}
                    {ent.type === 'setting' && '📖'}
                    {' '}{ent.label}
                  </option>
                ))}
              </select>
            )}
          </div>

          {/* 事件类型 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🏷️ 事件类型 *</label>
            <select
              value={timelineForm.eventType}
              onChange={(e) => {
                const selectedType = EVENT_TYPE_OPTIONS.find((opt) => opt.value === e.target.value);
                setTimelineForm({
                  ...timelineForm,
                  eventType: e.target.value as EventType,
                  icon: selectedType?.icon || '🎯',
                  color: selectedType?.color || '#f59e0b',
                });
              }}
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-yellow-500"
            >
              {EVENT_TYPE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.icon} {opt.label}
                </option>
              ))}
            </select>
          </div>

          {/* 事件标题 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">📛 事件标题 *</label>
            <input
              type="text"
              value={timelineForm.title}
              onChange={(e) => setTimelineForm({ ...timelineForm, title: e.target.value })}
              placeholder="例如：获得神器、遇见导师"
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
          </div>

          {/* 事件描述 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">📝 事件描述</label>
            <textarea
              value={timelineForm.description}
              onChange={(e) => setTimelineForm({ ...timelineForm, description: e.target.value })}
              placeholder="详细描述这个事件..."
              rows={3}
              className="w-full px-3 py-2 bg-gray-750 border border-gray-600 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-yellow-500 resize-none"
            />
          </div>

          {/* 事件图标 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🎨 事件图标</label>
            <input
              type="text"
              value={timelineForm.icon}
              onChange={(e) => setTimelineForm({ ...timelineForm, icon: e.target.value })}
              placeholder="输入emoji，例如：🎯"
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
          </div>

          {/* 所属章节 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">📖 所属章节（可选）</label>
            <select
              value={timelineForm.chapterId}
              onChange={(e) => {
                const selectedChapter = chapters.find((ch) => ch.id === e.target.value);
                setTimelineForm({
                  ...timelineForm,
                  chapterId: e.target.value,
                  chapterNumber: selectedChapter?.order || 1,
                });
              }}
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-yellow-500"
            >
              <option value="">不关联章节</option>
              {chapters.map((ch) => (
                <option key={ch.id} value={ch.id}>
                  第 {ch.order} 章 - {ch.title}
                </option>
              ))}
            </select>
          </div>

          {/* 颜色标记 */}
          <div>
            <label className="block text-xs text-gray-400 mb-1">🎨 颜色标记</label>
            <div className="flex items-center gap-2">
              <input
                type="color"
                value={timelineForm.color}
                onChange={(e) => setTimelineForm({ ...timelineForm, color: e.target.value })}
                className="w-12 h-8 bg-white border border-gray-300 rounded cursor-pointer"
              />
              <span className="text-sm text-gray-300">{timelineForm.color}</span>
            </div>
          </div>
        </div>

        {/* 操作按钮 */}
        <div className="border-t border-gray-700 pt-4 flex gap-2">
          <button
            onClick={handleSubmit}
            disabled={isSaving || !timelineForm.title.trim() || !timelineForm.entityId}
            className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-white bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded transition-colors"
          >
            <Save className="w-4 h-4" />
            {isSaving ? '创建中...' : '创建事件'}
          </button>
          <button
            onClick={onClose}
            disabled={isSaving}
            className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 disabled:cursor-not-allowed rounded transition-colors"
          >
            <X className="w-4 h-4" />
            取消
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="property-panel h-full flex flex-col">
      <div className="panel-content flex-1 overflow-y-auto p-4">
        {mode === 'idle' && renderIdleState()}
        {mode === 'node' && renderNodeDetails()}
        {mode === 'relationship' && renderRelationshipDetails()}
        {mode === 'create' && renderCreateRelationship()}
        {mode === 'timeline' && renderTimelineEventDetails()}
        {mode === 'createTimeline' && renderCreateTimelineEvent()}
      </div>
    </div>
  );
};

export default PropertyPanel;
