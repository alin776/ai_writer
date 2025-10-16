/**
 * Mock 世界观数据（角色、地点、道具、设定）
 */
import type { Character, Location, Item } from '@/types';
import type { Setting } from '@/types/novel';

export const mockCharacters: Character[] = [
  {
    id: 'char-1-1',
    workId: 'work-1',
    name: '林风',
    description: '主角，凡人少年，机缘巧合踏上修仙之路',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=linfeng',
    age: 16,
    gender: 'male',
    personality: '善良、勤奋、坚韧不拔',
    background: '青云村人，自幼父母双亡，由老族长抚养长大',
    relationships: ['老族长（养父）', '师父（未出场）'],
    createTime: '2024-01-20T10:00:00Z',
    updateTime: '2024-01-20T10:00:00Z',
  },
  {
    id: 'char-1-2',
    workId: 'work-1',
    name: '老族长',
    description: '青云村的族长，林风的养父',
    age: 78,
    gender: 'male',
    personality: '慈祥、睿智',
    background: '青云村世代相传的族长，德高望重',
    createTime: '2024-01-20T10:05:00Z',
    updateTime: '2024-01-20T10:05:00Z',
  },
  {
    id: 'char-2-1',
    workId: 'work-2',
    name: '陈浩',
    description: '主角，银河帝国第七舰队的舰长',
    age: 32,
    gender: 'male',
    personality: '冷静、果敢、富有正义感',
    background: '军事学院优秀毕业生，战功赫赫',
    createTime: '2024-03-05T11:30:00Z',
    updateTime: '2024-03-05T11:30:00Z',
  },
];

export const mockLocations: Location[] = [
  {
    id: 'loc-1-1',
    workId: 'work-1',
    name: '青云村',
    description: '位于青云山脚下的小村庄，主角林风的故乡',
    image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400',
    type: 'nature',
    createTime: '2024-01-20T10:10:00Z',
    updateTime: '2024-01-20T10:10:00Z',
  },
  {
    id: 'loc-1-2',
    workId: 'work-1',
    name: '青云山',
    description: '一座灵气充沛的山脉，有许多修仙者在此修炼',
    type: 'nature',
    createTime: '2024-01-20T10:15:00Z',
    updateTime: '2024-01-20T10:15:00Z',
  },
  {
    id: 'loc-2-1',
    workId: 'work-2',
    name: '猎鹰号战舰',
    description: '银河帝国最新型的星际战舰，主角陈浩的座驾',
    type: 'other',
    createTime: '2024-03-05T11:35:00Z',
    updateTime: '2024-03-05T11:35:00Z',
  },
];

export const mockItems: Item[] = [
  {
    id: 'item-1-1',
    workId: 'work-1',
    name: '天机玉佩',
    description: '上古仙人遗留的传承玉佩，内含修炼心法',
    type: 'treasure',
    createTime: '2024-01-20T10:20:00Z',
    updateTime: '2024-01-20T10:20:00Z',
  },
  {
    id: 'item-1-2',
    workId: 'work-1',
    name: '碧云剑',
    description: '林风的第一把飞剑，品质中等',
    type: 'weapon',
    createTime: '2024-01-20T10:25:00Z',
    updateTime: '2024-01-20T10:25:00Z',
  },
  {
    id: 'item-2-1',
    workId: 'work-2',
    name: '量子通讯器',
    description: '可以进行超光速通讯的设备',
    type: 'tool',
    createTime: '2024-03-05T11:40:00Z',
    updateTime: '2024-03-05T11:40:00Z',
  },
];

export const mockSettings: Setting[] = [
  {
    id: 'setting-1-1',
    workId: 'work-1',
    title: '修炼境界体系',
    category: '世界观',
    content: '修炼境界分为：炼气期、筑基期、金丹期、元婴期、化神期、渡劫期、大乘期。每个境界又分为初期、中期、后期、圆满四个小境界。',
    tags: ['修炼', '境界'],
    relatedItems: [
      { type: 'character', id: 'char-1-1' },
    ],
    createdAt: new Date('2024-01-20T10:30:00Z'),
    updatedAt: new Date('2024-01-20T10:30:00Z'),
  },
  {
    id: 'setting-1-2',
    workId: 'work-1',
    title: '灵根系统',
    category: '魔法体系',
    content: '灵根分为金、木、水、火、土五行，以及罕见的雷、风、冰等变异灵根。林风拥有稀有的混沌灵根。',
    tags: ['灵根', '体质'],
    relatedItems: [
      { type: 'character', id: 'char-1-1' },
    ],
    createdAt: new Date('2024-01-20T10:35:00Z'),
    updatedAt: new Date('2024-01-20T10:35:00Z'),
  },
  {
    id: 'setting-2-1',
    workId: 'work-2',
    title: '银河帝国政体',
    category: '世界观',
    content: '银河帝国是人类在银河系建立的统一政权，采用君主立宪制，皇帝为虚位元首，实权掌握在议会手中。',
    tags: ['政治', '帝国'],
    relatedItems: [
      { type: 'character', id: 'char-2-1' },
    ],
    createdAt: new Date('2024-03-05T11:45:00Z'),
    updatedAt: new Date('2024-03-05T11:45:00Z'),
  },
  {
    id: 'setting-2-2',
    workId: 'work-2',
    title: '超光速航行技术',
    category: '科技',
    content: '通过扭曲空间实现超光速航行，理论最高速度可达光速的1000倍。航行时需要消耗大量能量。',
    tags: ['科技', '航行'],
    relatedItems: [
      { type: 'location', id: 'loc-2-1' },
    ],
    createdAt: new Date('2024-03-05T11:50:00Z'),
    updatedAt: new Date('2024-03-05T11:50:00Z'),
  },
];
