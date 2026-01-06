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

  // 设定间关系
  SETTING_BASED: '基于',
  SETTING_DERIVED: '衍生于',
  SETTING_OPPOSE: '对立于',
  SETTING_CONTAIN: '包含于',

  // 地点与设定关系
  LOCATION_SETTING_APPLY: '适用于',
  LOCATION_SETTING_ORIGIN: '起源于',
  LOCATION_SETTING_SYMBOL: '象征于',

  // 自定义
  CUSTOM: '自定义',
} as const;

/**
 * 根据实体类型组合获取可用的关系选项
 */
export const RELATIONSHIP_TYPE_BY_ENTITY: Record<string, string[]> = {
  // 角色-角色
  'character-character': [
    RELATIONSHIP_TYPES.CHARACTER_FAMILY,
    RELATIONSHIP_TYPES.CHARACTER_MENTOR,
    RELATIONSHIP_TYPES.CHARACTER_FRIEND,
    RELATIONSHIP_TYPES.CHARACTER_ALLY,
    RELATIONSHIP_TYPES.CHARACTER_ENEMY,
    RELATIONSHIP_TYPES.CHARACTER_COLLEAGUE,
    RELATIONSHIP_TYPES.CHARACTER_LOVER,
    RELATIONSHIP_TYPES.CHARACTER_RIVAL,
  ],
  // 地点-地点
  'location-location': [
    RELATIONSHIP_TYPES.LOCATION_CONTAIN,
    RELATIONSHIP_TYPES.LOCATION_ADJACENT,
    RELATIONSHIP_TYPES.LOCATION_OPPOSE,
  ],
  // 设定-设定
  'setting-setting': [
    RELATIONSHIP_TYPES.SETTING_BASED,
    RELATIONSHIP_TYPES.SETTING_DERIVED,
    RELATIONSHIP_TYPES.SETTING_OPPOSE,
    RELATIONSHIP_TYPES.SETTING_CONTAIN,
  ],
  // 角色-地点（双向）
  'character-location': [
    RELATIONSHIP_TYPES.CHARACTER_LOCATION_LIVE,
    RELATIONSHIP_TYPES.CHARACTER_LOCATION_BORN,
    RELATIONSHIP_TYPES.CHARACTER_LOCATION_WORK,
    RELATIONSHIP_TYPES.CHARACTER_LOCATION_RULE,
    RELATIONSHIP_TYPES.CHARACTER_LOCATION_GUARD,
  ],
  'location-character': [
    RELATIONSHIP_TYPES.CHARACTER_LOCATION_LIVE,
    RELATIONSHIP_TYPES.CHARACTER_LOCATION_BORN,
    RELATIONSHIP_TYPES.CHARACTER_LOCATION_WORK,
    RELATIONSHIP_TYPES.CHARACTER_LOCATION_RULE,
    RELATIONSHIP_TYPES.CHARACTER_LOCATION_GUARD,
  ],
  // 角色-设定（双向）
  'character-setting': [
    RELATIONSHIP_TYPES.CHARACTER_SETTING_MASTER,
    RELATIONSHIP_TYPES.CHARACTER_SETTING_BELIEVE,
    RELATIONSHIP_TYPES.CHARACTER_SETTING_OWN,
    RELATIONSHIP_TYPES.CHARACTER_SETTING_BELONG,
  ],
  'setting-character': [
    RELATIONSHIP_TYPES.CHARACTER_SETTING_MASTER,
    RELATIONSHIP_TYPES.CHARACTER_SETTING_BELIEVE,
    RELATIONSHIP_TYPES.CHARACTER_SETTING_OWN,
    RELATIONSHIP_TYPES.CHARACTER_SETTING_BELONG,
  ],
  // 地点-设定（双向）
  'location-setting': [
    RELATIONSHIP_TYPES.LOCATION_SETTING_APPLY,
    RELATIONSHIP_TYPES.LOCATION_SETTING_ORIGIN,
    RELATIONSHIP_TYPES.LOCATION_SETTING_SYMBOL,
  ],
  'setting-location': [
    RELATIONSHIP_TYPES.LOCATION_SETTING_APPLY,
    RELATIONSHIP_TYPES.LOCATION_SETTING_ORIGIN,
    RELATIONSHIP_TYPES.LOCATION_SETTING_SYMBOL,
  ],
};

/**
 * 根据源类型和目标类型获取可用的关系选项
 * @param sourceType 源实体类型
 * @param targetType 目标实体类型
 * @returns 可用的关系类型数组
 */
export function getRelationshipOptions(sourceType: EntityType, targetType: EntityType): string[] {
  const key = `${sourceType}-${targetType}`;
  return RELATIONSHIP_TYPE_BY_ENTITY[key] || [RELATIONSHIP_TYPES.CUSTOM];
}

/**
 * 根据实体类型组合获取示例提示
 */
export const RELATIONSHIP_EXAMPLES_BY_ENTITY: Record<string, string> = {
  'character-character': '例如：好友、师父、敌人、恋人',
  'location-location': '例如：主城、分院、邻村',
  'setting-setting': '例如：基础功法、进阶版本',
  'character-location': '例如：出生地、修炼处、战场',
  'location-character': '例如：守护者、统治者、居民',
  'character-setting': '例如：掌门功法、信仰神明',
  'setting-character': '例如：创始人、传承者',
  'location-setting': '例如：发源地、圣地',
  'setting-location': '例如：适用范围、起源地',
};

/**
 * 根据源类型和目标类型获取示例提示
 * @param sourceType 源实体类型
 * @param targetType 目标实体类型
 * @returns 示例提示文本
 */
export function getRelationshipExamples(sourceType: EntityType, targetType: EntityType): string {
  const key = `${sourceType}-${targetType}`;
  return RELATIONSHIP_EXAMPLES_BY_ENTITY[key] || '例如：自定义关系标签';
}

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
