/**
 * 实体分组类型定义
 * 用于世界观关系图的节点分组管理
 */

import { EntityType } from './relationship';

/**
 * 分组成员
 */
export interface GroupMember {
  id: string;
  groupId: string;
  entityId: string;
  entityType: EntityType;
  orderIndex: number;
  createdAt: string;
}

/**
 * 创建分组成员数据
 */
export interface CreateGroupMemberData {
  entityId: string;
  entityType: EntityType;
  orderIndex?: number;
}

/**
 * 实体分组
 */
export interface EntityGroup {
  id: string;
  workId: string;
  name: string;
  description?: string;
  groupType: 'manual' | 'auto';
  autoRule?: Record<string, any>;
  color?: string;
  icon?: string;
  parentGroupId?: string;
  orderIndex: number;
  members: GroupMember[];
  createdAt: string;
  updatedAt: string;
}

/**
 * 创建分组数据
 */
export interface CreateEntityGroupData {
  workId: string;
  name: string;
  description?: string;
  groupType?: 'manual' | 'auto';
  autoRule?: Record<string, any>;
  color?: string;
  icon?: string;
  parentGroupId?: string;
  orderIndex?: number;
}

/**
 * 更新分组数据
 */
export interface UpdateEntityGroupData {
  name?: string;
  description?: string;
  autoRule?: Record<string, any>;
  color?: string;
  icon?: string;
  parentGroupId?: string;
  orderIndex?: number;
}

/**
 * 批量添加成员请求
 */
export interface BatchAddMembersRequest {
  members: CreateGroupMemberData[];
}

/**
 * 批量移除成员请求
 */
export interface BatchRemoveMembersRequest {
  memberIds: string[];
}

/**
 * 默认分组颜色配置
 */
export const GROUP_COLORS = [
  '#3b82f6', // 蓝色
  '#10b981', // 绿色
  '#f59e0b', // 橙色
  '#8b5cf6', // 紫色
  '#ef4444', // 红色
  '#06b6d4', // 青色
  '#ec4899', // 粉色
  '#f97316', // 深橙
];

/**
 * 默认分组图标选项
 */
export const GROUP_ICONS = [
  '📁', '📂', '📊', '📋', '📌',
  '⭐', '❤️', '🔥', '💡', '🎯',
  '🏷️', '📦', '🗂️', '🎨', '🔧',
];
