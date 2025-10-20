/**
 * 搜索相关类型定义
 */

export interface WorkSearchResult {
  id: string;
  title: string;
  description?: string;
  genre?: string;
  wordCount: number;
  chapterCount: number;
  updatedAt: string;
}

export interface ChapterSearchResult {
  id: string;
  workId: string;
  workTitle: string;
  title: string;
  contentSnippet: string;
  wordCount: number;
  updatedAt: string;
}

export interface CharacterSearchResult {
  id: string;
  workId: string;
  workTitle: string;
  name: string;
  role?: string;
  description?: string;
}

export interface LocationSearchResult {
  id: string;
  workId: string;
  workTitle: string;
  name: string;
  type?: string;
  description?: string;
}

export interface SettingSearchResult {
  id: string;
  workId: string;
  workTitle: string;
  title: string;
  category?: string;
  content?: string;
}

export interface SearchResponse {
  query: string;
  total: number;
  works: WorkSearchResult[];
  chapters: ChapterSearchResult[];
  characters: CharacterSearchResult[];
  locations: LocationSearchResult[];
  settings: SettingSearchResult[];
}
