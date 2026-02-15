/**
 * 导入导出相关类型定义
 */

// ============= 导出相关 =============

export interface ExportOptions {
  format: 'json' | 'markdown' | 'docx';
  includeChapters: boolean;
  includeWorldview: boolean;
  includeGuidelines: boolean;
  includeAnalysis: boolean;
  chapterIds?: string[];
}

export interface ExportResponse {
  downloadUrl: string;
  fileName: string;
  fileSize: number;
  expiresAt: string;
}

// ============= 导入相关 =============

export interface ImportOptions {
  format: 'json' | 'markdown' | 'txt';
  createNew: boolean;
  workId?: string;
  includeWorldview: boolean;
  includeGuidelines: boolean;
  autoExtractWorldview?: boolean;
}

export interface ImportPreviewWork {
  title: string;
  description?: string;
  genre?: string;
  totalWords: number;
  totalChapters: number;
}

export interface ImportPreviewChapter {
  title: string;
  wordCount: number;
  order: number;
}

export interface ImportPreviewResponse {
  work: ImportPreviewWork;
  chapters: ImportPreviewChapter[];
  charactersCount: number;
  locationsCount: number;
  settingsCount: number;
  warnings: string[];
}

export interface ImportResponse {
  workId: string;
  chaptersCreated: number;
  charactersCreated: number;
  locationsCreated: number;
  settingsCreated: number;
  message: string;
}
