/**
 * 时间线类型定义
 */

import { EntityType as BaseEntityType } from './relationship';

// 时间线的实体类型（扩展了基础类型，添加了 relationship）
export type TimelineEntityType = BaseEntityType | 'relationship';

// 为了保持向后兼容，也导出为 EntityType（仅在 timeline 上下文中使用）
export type EntityType = TimelineEntityType;

export type EventType = 'milestone' | 'change' | 'created' | 'removed' | 'conflict' | 'discovery' | 'meeting' | 'departure' | 'achievement' | 'loss' | 'transformation' | 'decision' | 'betrayal' | 'alliance' | 'revelation';

/**
 * 时间线事件
 */
export interface TimelineEvent {
  id: string;
  workId: string;
  entityId: string;
  entityType: EntityType;
  eventType: EventType;
  title: string;
  description?: string;
  icon?: string;
  chapterId?: string;
  chapterNumber?: number;
  timestamp?: number;
  color?: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * 创建时间线事件数据
 */
export interface CreateTimelineEventData {
  workId: string;
  entityId: string;
  entityType: EntityType;
  eventType: EventType;
  title: string;
  description?: string;
  icon?: string;
  chapterId?: string;
  chapterNumber?: number;
  timestamp?: number;
  color?: string;
}

/**
 * 更新时间线事件数据
 */
export interface UpdateTimelineEventData {
  entityId?: string;
  entityType?: EntityType;
  eventType?: EventType;
  title?: string;
  description?: string;
  icon?: string;
  chapterId?: string;
  chapterNumber?: number;
  timestamp?: number;
  color?: string;
}

/**
 * 章节锚点
 */
export interface ChapterAnchor {
  id: string;
  chapterId: string;
  chapterTitle: string;
  chapterNumber: number;
  timestamp: number;
}

/**
 * 时间线轨道
 */
export interface TimelineTrack {
  entityId: string;
  entityType: EntityType;
  entityLabel: string;
  color?: string;
  events: TimelineEvent[];
}

/**
 * 事件类型选项
 */
export const EVENT_TYPE_OPTIONS = [
  { value: 'milestone', label: '里程碑', icon: '🎯', color: '#f59e0b' },
  { value: 'change', label: '变化', icon: '🔄', color: '#3b82f6' },
  { value: 'created', label: '创建', icon: '✨', color: '#10b981' },
  { value: 'removed', label: '移除', icon: '❌', color: '#ef4444' },
  { value: 'conflict', label: '冲突', icon: '⚔️', color: '#dc2626' },
  { value: 'discovery', label: '发现', icon: '🔍', color: '#059669' },
  { value: 'meeting', label: '相遇', icon: '🤝', color: '#8b5cf6' },
  { value: 'departure', label: '离别', icon: '👋', color: '#6b7280' },
  { value: 'achievement', label: '成就', icon: '🏆', color: '#eab308' },
  { value: 'loss', label: '失去', icon: '💔', color: '#991b1b' },
  { value: 'transformation', label: '转变', icon: '🦋', color: '#7c3aed' },
  { value: 'decision', label: '决定', icon: '🎲', color: '#0891b2' },
  { value: 'betrayal', label: '背叛', icon: '🗡️', color: '#be123c' },
  { value: 'alliance', label: '结盟', icon: '🤜🤛', color: '#0284c7' },
  { value: 'revelation', label: '揭秘', icon: '💡', color: '#ca8a04' },
] as const;

/**
 * 实体类型颜色映射
 */
export const ENTITY_TYPE_COLORS: Record<EntityType, string> = {
  character: '#3b82f6', // 蓝色
  location: '#10b981',  // 绿色
  setting: '#f59e0b',   // 橙色
  relationship: '#8b5cf6', // 紫色
};
