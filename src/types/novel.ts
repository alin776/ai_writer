/**
 * 小说相关类型定义
 */

// 章节状态
export type ChapterStatus = 'draft' | 'published' | 'archived';

// 章节类型
export interface Chapter {
  id: string;
  title: string;
  wordCount: number;
  status: ChapterStatus;
  order: number;
  content?: string; // 章节内容
  parentId?: string; // 父章节ID，支持子章节
  createdAt: Date;
  updatedAt: Date;
}

// 人物
export interface Character {
  id: string;
  workId?: string; // 所属作品ID
  name: string;
  avatar?: string;
  description: string;
  role?: string; // 角色定位：主角、配角等
  tags?: string[]; // 标签：性格特点等
  relationships?: {
    characterId: string;
    relationship: string;
  }[];
  createdAt?: Date;
  updatedAt?: Date;
}

// 地点
export interface Location {
  id: string;
  workId?: string; // 所属作品ID
  name: string;
  image?: string;
  description: string;
  type?: string; // 类型：城市、建筑、自然等
  tags?: string[];
  relatedLocations?: string[]; // 相关地点ID
  createdAt?: Date;
  updatedAt?: Date;
}

// 设定
export interface Setting {
  id: string;
  workId?: string; // 所属作品ID
  title: string;
  category?: string; // 分类：世界观、魔法体系、科技等
  content?: string;
  tags?: string[];
  relatedItems?: {
    type: 'character' | 'location' | 'setting';
    id: string;
  }[];
  createdAt?: Date;
  updatedAt?: Date;
}

// 世界观数据
export interface WorldData {
  characters: Character[];
  locations: Location[];
  settings: Setting[];
}

// 小说项目
export interface NovelProject {
  id: string;
  title: string;
  description: string;
  chapters: Chapter[];
  worldData: WorldData;
  createdAt: Date;
  updatedAt: Date;
}
