/**
 * 作品导出服务 —— ZIP 压缩包 + 独立 Markdown 章节文件
 *
 * 纯前端实现，无需后端支持
 * 每个章节导出为独立的 .md 文件，打包为 ZIP 下载
 */

import JSZip from 'jszip';
import { chaptersFs } from './chaptersFs';
import { fsToChapter } from '@/utils/fsChapterAdapter';
import type { Work, Chapter } from '@/types';

/**
 * 导出选项
 */
export interface ExportOptions {
  /** 指定导出的章节范围，第一章从 1 开始计数 */
  chapterRange?: {
    start: number;
    end: number;
  };
}

/**
 * 导出结果
 */
export interface ExportResult {
  success: boolean;
  chapterCount: number;
  totalWords: number;
}

/**
 * 生成单个章节的 .md 文件名
 *
 * 始终以 chapter.order 作为前缀，保证文件名在 ZIP 内唯一，
 * 避免 JSZip 同名静默覆盖导致章节丢失。
 */
function buildChapterFilename(chapter: Chapter): string {
  const order = chapter.order;
  // 剥离标题中已有的「第X章」前缀，避免与 order 重复
  const rawTitle = (chapter.title || '').replace(/^第\d+章\s*/, '');

  // 清理 Windows 非法字符
  const safePart = rawTitle.replace(/[\\/:*?"<>|]+/g, '-').trim();
  const baseName = safePart ? `第${order}章 ${safePart}` : `第${order}章`;

  return `${baseName}.md`;
}

/**
 * 导出服务类
 */
class ExportServiceClass {
  /**
   * 导出作品为 ZIP 文件（每章一个 .md 文件）
   */
  async export(work: Work, options: ExportOptions = {}): Promise<ExportResult> {
    // 1. 获取所有章节元信息
    const fsList = await chaptersFs.list(work.id);
    const chapters = fsList.map(fs => fsToChapter(fs, work.id));

    // 2. 按 order 排序
    let sortedChapters = [...chapters].sort((a, b) => a.order - b.order);

    // 2.1 范围裁剪
    if (options.chapterRange) {
      const { start, end } = options.chapterRange;

      if (Number.isNaN(start) || Number.isNaN(end) || start <= 0 || end <= 0 || start > end) {
        throw new Error('导出章节范围格式不正确，请检查输入');
      }

      sortedChapters = sortedChapters.slice(start - 1, end);

      if (sortedChapters.length === 0) {
        throw new Error('指定范围内没有可导出的章节');
      }
    }

    // 3. 逐章获取正文
    const chaptersWithContent = await Promise.all(
      sortedChapters.map(async (ch) => {
        const full = await chaptersFs.get(work.id, ch.order);
        return { ...ch, content: full.content || '' };
      })
    );

    // 4. 用 JSZip 打包
    const zip = new JSZip();

    chaptersWithContent.forEach((chapter) => {
      const filename = buildChapterFilename(chapter);
      zip.file(filename, chapter.content);
    });

    const blob = await zip.generateAsync({ type: 'blob' });

    // 5. 触发下载
    const safeTitle = this.sanitizeFilename(work.title);
    this.downloadBlob(blob, `${safeTitle}.zip`);

    // 6. 返回结果
    return {
      success: true,
      chapterCount: chaptersWithContent.length,
      totalWords: chaptersWithContent.reduce((sum, ch) => sum + (ch.wordCount || 0), 0),
    };
  }

  /**
   * 清理文件名，移除非法字符
   */
  private sanitizeFilename(filename: string): string {
    let sanitized = filename.replace(/[\\/:*?"<>|]+/g, '-');
    sanitized = sanitized.replace(/^[\s.]+|[\s.]+$/g, '');
    sanitized = sanitized.replace(/-+/g, '-');
    sanitized = sanitized.substring(0, 200);
    return sanitized || '未命名作品';
  }

  /**
   * 触发 Blob 文件下载
   */
  private downloadBlob(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.style.display = 'none';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  }
}

/**
 * 导出服务单例
 */
export const ExportService = new ExportServiceClass();

// 向后兼容旧名称
export type { ExportOptions as TxtExportOptions };
export type { ExportResult as TxtExportResult };
export { ExportService as TxtExportService };
