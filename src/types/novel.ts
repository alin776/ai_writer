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

// 作品规范
export interface WorkGuidelines {
  id?: string;
  workId?: string;
  // 基本信息
  outline?: string; // 大纲流程
  style?: string; // 整体风格
  tone?: string; // 语言风格
  // 写作规范
  wordsPerChapter?: number; // 每章字数
  updateFrequency?: string; // 更新频率
  // 设定约束
  powerSystem?: string; // 力量体系
  worldRules?: string; // 世界规则
  // 创作目标
  targetAudience?: string; // 目标读者
  mainTheme?: string; // 主题
  plotDirection?: string; // 剧情走向
  // 其他
  notes?: string; // 备注
  createdAt?: Date;
  updatedAt?: Date;
}

// AI创作规范（基于商业化小说创作框架）
export interface AIGuidelines {
  id?: string;
  workId?: string;
  
  // 第一部分：创作规范
  businessGoal?: string;        // 商业目标
  targetAudience?: string;      // 目标读者
  commercialBenchmark?: string; // 商业对标
  highConcept?: string;         // 高概念卖点
  
  coreParadox?: string;         // 核心悖论/设定
  dominantEmotion?: string;     // 主导情感
  coreIpSymbols?: string;       // 核心IP符号
  
  protagonistArc?: string;      // 主角弧光
  coreConflict?: string;        // 核心关系冲突
  narrativeRhythm?: string;     // 叙事节奏
  
  writingStyle?: string;        // 文笔风格
  styleNotes?: string;          // 文风注意事项
  
  chapterLength?: string;       // 章节长度
  contentTaboos?: string;       // 内容禁忌
  
  // 第二部分：核心设定
  primaryGenre?: string;        // 一级类型
  secondaryTags?: string;       // 二级标签
  creativeTone?: string;        // 创作基调
  
  worldIntro?: string;          // 核心世界观
  mainLocations?: string;       // 主要场景/地点
  worldRules?: string;          // 世界规则
  
  powerSystemName?: string;     // 体系名称与原理
  powerLevels?: string;         // 等级划分
  powerCost?: string;           // 能力获取与代价
  
  protagonistName?: string;     // 主角姓名/代号
  protagonistIdentity?: string; // 核心身份
  protagonistTraits?: string;   // 强化缺陷与能力
  protagonistGoal?: string;     // 核心目标与动机
  
  conflictDesign?: string;      // 冲突点设计
  actOne?: string;              // 第一幕
  actTwo?: string;              // 第二幕
  actThree?: string;            // 第三幕
  
  isActive?: boolean;
  createdAt?: Date;
  updatedAt?: Date;
}

// 世界观数据
export interface WorldData {
  characters: Character[];
  locations: Location[];
  settings: Setting[];
  guidelines?: WorkGuidelines; // 作品规范
  aiGuidelines?: AIGuidelines; // AI创作规范
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

// ==================== 世界观同步相关类型 ====================

// 新增人物项
export interface NewCharacterItem {
  name: string;
  role?: string;
  description?: string;
  firstAppearance?: string;
  importance?: string;
  tags?: string[];
}

// 更新人物项
export interface UpdatedCharacterItem {
  name: string;
  changes: string;
}

// 新增地点项
export interface NewLocationItem {
  name: string;
  type?: string;
  description?: string;
  importance?: string;
  tags?: string[];
}

// 新增设定项
export interface NewSettingItem {
  title: string;
  category?: string;
  content?: string;
  tags?: string[];
}

// 人物关系变化项
export interface RelationshipChangeItem {
  from: string;
  to: string;
  oldRelation?: string;
  newRelation: string;
  reason?: string;
}

// 文件系统章节（匹配后端 ChapterResponse）
export interface FSChapter {
  num: number;
  title: string;
  status: string;
  wordCount: number;
  content?: string;
}

// 世界观变化响应
export interface WorldviewChanges {
  newCharacters: NewCharacterItem[];
  updatedCharacters: UpdatedCharacterItem[];
  newLocations: NewLocationItem[];
  newSettings: NewSettingItem[];
  relationshipChanges: RelationshipChangeItem[];
  scannedChapters?: number;
}

// 应用变化结果
export interface ApplyChangesResult {
  charactersCreated: number;
  charactersUpdated: number;
  locationsCreated: number;
  settingsCreated: number;
  relationshipsCreated: number;
}

// 世界观扫描进度（导入解析）
export interface WorldviewScanProgress {
  workId: string;
  status: 'idle' | 'pending' | 'running' | 'completed' | 'failed' | 'preparing' | 'applying';
  scanMode?: 'incremental' | 'full';
  chaptersTotal: number;
  chaptersProcessed: number;
  batchesTotal: number;
  batchesCompleted: number;
  progressPercentage: number;
  results?: {
    charactersCreated: number;
    charactersUpdated: number;
    locationsCreated: number;
    locationsUpdated: number;
    settingsCreated: number;
    settingsUpdated: number;
    relationshipsCreated: number;
  };
  lastError?: string;
  updatedAt?: string;
}
