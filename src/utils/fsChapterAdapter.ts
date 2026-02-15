/**
 * 文件系统章节适配器
 *
 * 将 FSChapter（后端文件系统格式）转换为 Chapter（前端已有格式），
 * 使 WorkDetailView 中 50+ 处 chapter.id 引用无需修改。
 */
import type { FSChapter } from '../types/novel';
import type { Chapter } from '../types';

/**
 * 将 FSChapter 转换为前端 Chapter 格式
 * 生成合成 ID "fs-{num}"，兼容已有的 chapter.id 引用
 */
export function fsToChapter(fs: FSChapter, workId: string): Chapter {
  const now = new Date().toISOString();
  return {
    id: `fs-${fs.num}`,
    workId,
    title: fs.title,
    content: fs.content || '',
    wordCount: fs.wordCount,
    viewCount: 0,
    isPublished: fs.status === 'published',
    order: fs.num,
    publishedAt: null,
    createdAt: now,
    updatedAt: now,
    status: fs.status,
  };
}

/**
 * 从合成 ID 提取章节序号
 * "fs-3" → 3，无效 ID 返回 null
 */
export function chapterIdToNum(id: string): number | null {
  const match = id.match(/^fs-(\d+)$/);
  if (!match) return null;
  return parseInt(match[1], 10);
}
