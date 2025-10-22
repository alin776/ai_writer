/**
 * 世界观关系图 - 关系类型定义
 */

/**
 * 实体类型
 */
export type EntityType = 'character' | 'location' | 'setting';

/**
 * 关系方向
 */
export type RelationshipDirection = 'one-way' | 'two-way';

/**
 * 关系线条样式
 */
export type RelationshipLineStyle = 'solid' | 'dashed' | 'dotted';

/**
 * 关系类型预设
 */
export const RELATIONSHIP_TYPES = {
  // 角色间关系
  CHARACTER_FAMILY: '亲属关系',
  CHARACTER_MENTOR: '师徒关系',
  CHARACTER_FRIEND: '好友关系',
  CHARACTER_ALLY: '盟友关系',
  CHARACTER_ENEMY: '敌对关系',
  CHARACTER_COLLEAGUE: '同事关系',
  CHARACTER_LOVER: '恋人关系',
  CHARACTER_RIVAL: '竞争关系',
  
  // 角色与地点关系
  CHARACTER_LOCATION_LIVE: '居住于',
  CHARACTER_LOCATION_BORN: '出生于',
  CHARACTER_LOCATION_WORK: '工作于',
  CHARACTER_LOCATION_RULE: '统治于',
  CHARACTER_LOCATION_GUARD: '守护于',
  
  // 角色与设定关系
  CHARACTER_SETTING_MASTER: '掌握',
  CHARACTER_SETTING_BELIEVE: '信仰',
  CHARACTER_SETTING_OWN: '拥有',
  CHARACTER_SETTING_BELONG: '从属',
  
  // 地点间关系
  LOCATION_CONTAIN: '包含于',
  LOCATION_ADJACENT: '邻近于',
  LOCATION_OPPOSE: '对立于',
  
  // 自定义
  CUSTOM: '自定义',
} as const;

/**
 * 关系类型颜色配置
 */
export const RELATIONSHIP_COLORS = {
  [RELATIONSHIP_TYPES.CHARACTER_FAMILY]: '#ef4444', // 红色 - 亲属
  [RELATIONSHIP_TYPES.CHARACTER_MENTOR]: '#a855f7', // 紫色 - 师徒
  [RELATIONSHIP_TYPES.CHARACTER_FRIEND]: '#10b981', // 绿色 - 好友
  [RELATIONSHIP_TYPES.CHARACTER_ALLY]: '#3b82f6', // 蓝色 - 盟友
  [RELATIONSHIP_TYPES.CHARACTER_ENEMY]: '#f97316', // 橙色 - 敌对
  [RELATIONSHIP_TYPES.CHARACTER_COLLEAGUE]: '#6b7280', // 灰色 - 同事
  [RELATIONSHIP_TYPES.CHARACTER_LOVER]: '#ec4899', // 粉色 - 恋人
  [RELATIONSHIP_TYPES.CHARACTER_RIVAL]: '#f59e0b', // 琥珀色 - 竞争
  DEFAULT: '#6b7280', // 灰色 - 默认
};

/**
 * 关系接口
 */
export interface Relationship {
  id: string;
  workId: string;
  
  // 源节点
  sourceId: string;
  sourceType: EntityType;
  
  // 目标节点
  targetId: string;
  targetType: EntityType;
  
  // 关系属性
  relationshipType: string;  // 关系类型（如"师徒关系"）
  label: string;             // 显示标签
  description?: string;      // 详细描述
  strength: number;          // 关系强度 (1-10)
  direction: RelationshipDirection;
  
  // 时间线（可选）
  startChapterId?: string;
  endChapterId?: string;
  startTime?: string;
  endTime?: string;
  
  // 样式
  color?: string;
  lineStyle: RelationshipLineStyle;
  
  // 标签和分类
  tags?: string[];
  category?: string;
  
  // 元数据
  createdAt: string;
  updatedAt: string;
}

/**
 * 创建关系数据（发送到后端）
 */
export interface CreateRelationshipData {
  work_id: string;
  source_id: string;
  source_type: EntityType;
  target_id: string;
  target_type: EntityType;
  relationship_type: string;
  label: string;
  description?: string;
  strength?: number;
  direction?: RelationshipDirection;
  color?: string;
  line_style?: RelationshipLineStyle;
  tags?: string[];
}

/**
 * 更新关系数据
 */
export interface UpdateRelationshipData {
  relationship_type?: string;
  label?: string;
  description?: string;
  strength?: number;
  direction?: RelationshipDirection;
  color?: string;
  line_style?: RelationshipLineStyle;
  tags?: string[];
}

/**
 * 关系表单数据（用于对话框）
 */
export interface RelationshipFormData {
  relationshipType: string;
  label: string;
  description?: string;
  strength: number;
  direction: RelationshipDirection;
  color?: string;
  lineStyle: RelationshipLineStyle;
}

/**
 * 关系统计
 */
export interface RelationshipStats {
  total: number;
  byType: Record<string, number>;
  bySourceType: Record<EntityType, number>;
  byTargetType: Record<EntityType, number>;
}
