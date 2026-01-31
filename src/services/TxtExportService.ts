/**
 * TXT 格式导出服务
 *
 * 纯前端实现，无需后端支持
 * 支持导出作品标题、简介、所有章节内容
 */

import { DataService } from './DataService';
import type { Work, Chapter } from '@/types';
import { htmlToPlainText } from '@/utils/wordCount';

/**
 * TXT 导出选项
 */
export interface TxtExportOptions {
  /** 是否包含简介，默认 true */
  includeDescription?: boolean;
  /** 作者名，可选 */
  authorName?: string;
  /** 段落缩进字符，默认全角空格 */
  indentChar?: string;
  /** 指定导出的章节范围，第一章从 1 开始计数 */
  chapterRange?: {
    start: number;
    end: number;
  };
}

/**
 * 默认导出选项
 */
type ResolvedTxtExportOptions = {
  includeDescription: boolean;
  authorName: string;
  indentChar: string;
  chapterRange?: {
    start: number;
    end: number;
  };
};

const DEFAULT_OPTIONS: ResolvedTxtExportOptions = {
  includeDescription: true,
  authorName: '',
  indentChar: '　　', // 两个全角空格
};

/**
 * 导出结果
 */
export interface TxtExportResult {
  success: boolean;
  chapterCount: number;
  totalWords: number;
}

/**
 * TXT 导出服务类
 */
class TxtExportServiceClass {
  /**
   * 导出作品为 TXT 文件
   * @param work 作品信息
   * @param options 导出选项
   * @returns 导出结果
   */
  async export(work: Work, options: TxtExportOptions = {}): Promise<TxtExportResult> {
    const mergedOptions: ResolvedTxtExportOptions = { ...DEFAULT_OPTIONS, ...options };

    // 1. 获取所有章节
    const chapters = await DataService.getChapters(work.id);

    // 2. 按 order 排序
    let sortedChapters = [...chapters].sort((a, b) => a.order - b.order);

    // 2.1 如果指定了范围，按照范围裁剪章节（用下标切片而非 order 过滤）
    if (mergedOptions.chapterRange) {
      const { start, end } = mergedOptions.chapterRange;

      if (Number.isNaN(start) || Number.isNaN(end) || start <= 0 || end <= 0 || start > end) {
        throw new Error('导出章节范围格式不正确，请检查输入');
      }

      sortedChapters = sortedChapters.slice(start - 1, end);

      if (sortedChapters.length === 0) {
        throw new Error('指定范围内没有可导出的章节');
      }
    }

    // 3. 格式化内容
    const content = this.formatContent(work, sortedChapters, mergedOptions);

    // 4. 清理文件名并触发下载
    const safeFilename = this.sanitizeFilename(work.title);
    this.downloadFile(content, `${safeFilename}.txt`);

    // 5. 返回导出结果
    return {
      success: true,
      chapterCount: sortedChapters.length,
      totalWords: sortedChapters.reduce((sum, ch) => sum + (ch.wordCount || 0), 0),
    };
  }

  /**
   * 清理文件名，移除非法字符
   * Windows 禁止字符: \ / : * ? " < > |
   */
  private sanitizeFilename(filename: string): string {
    // 1. 移除 Windows/Unix 保留字符
    let sanitized = filename.replace(/[\\/:*?"<>|]+/g, '-');

    // 2. 移除前导和尾随的点和空格
    sanitized = sanitized.replace(/^[\s.]+|[\s.]+$/g, '');

    // 3. 合并连续的连字符
    sanitized = sanitized.replace(/-+/g, '-');

    // 4. 限制长度（保守值，确保兼容各系统）
    sanitized = sanitized.substring(0, 200);

    // 5. 如果清理后为空，使用默认名称
    return sanitized || '未命名作品';
  }

  /**
   * 格式化导出内容
   */
  private formatContent(
    work: Work,
    chapters: Chapter[],
    options: ResolvedTxtExportOptions
  ): string {
    const lines: string[] = [];

    // 标题
    lines.push(work.title);

    // 作者（如果提供）
    if (options.authorName) {
      lines.push(`作者：${options.authorName}`);
    }

    // 简介
    if (options.includeDescription && work.description) {
      lines.push('简介：');
      const descParagraphs = htmlToPlainText(work.description).split('\n');
      for (const para of descParagraphs) {
        if (para.trim()) {
          lines.push(`${options.indentChar}${para.trim()}`);
        } else {
          lines.push('');
        }
      }
      lines.push(''); // 空行分隔
    }

    // 章节内容
    for (let idx = 0; idx < chapters.length; idx++) {
      const chapter = chapters[idx];
      // 章节标题：使用范围起始编号/原 order，避免重复添加「第X章」前缀
      const chapterNumber = options.chapterRange
        ? options.chapterRange.start + idx
        : chapter.order ?? idx + 1;

      let chapterTitle: string;
      if (/^第\d+章/.test(chapter.title)) {
        chapterTitle = chapter.title;
      } else {
        chapterTitle = `第${chapterNumber}章 ${chapter.title}`;
      }

      // 使用全角括号包裹，避免 Markdown 粗体在 TXT 中失效
      lines.push(`【${chapterTitle}】`);

      // 章节正文，先转纯文本再按行输出，保留段落换行
      if (chapter.content) {
        const paragraphs = htmlToPlainText(chapter.content).split('\n');
        for (const para of paragraphs) {
          if (para.trim()) {
            lines.push(`${options.indentChar}${para.trim()}`);
          } else {
            lines.push('');
          }
        }
      }

      // 章节间空行
      lines.push('');
    }

    return lines.join('\n');
  }

  /**
   * 触发文件下载
   */
  private downloadFile(content: string, filename: string): void {
    // 添加 BOM 以确保 Windows 记事本正确识别 UTF-8
    const BOM = '\uFEFF';
    const blob = new Blob([BOM + content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.style.display = 'none';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // 释放 URL 对象
    URL.revokeObjectURL(url);
  }
}

/**
 * TXT 导出服务单例
 */
export const TxtExportService = new TxtExportServiceClass();
