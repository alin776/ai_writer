/**
 * 贴图 API 服务
 */

import { ApiAdapter } from './ApiAdapter';

const api = new ApiAdapter();

// ==================== 类型定义 ====================

export interface TenorSticker {
  id: string;
  url: string;
  previewUrl: string;
  description?: string;
}

export interface TenorSearchResponse {
  stickers: TenorSticker[];
  next?: string;
}

export interface UserSticker {
  id: string;
  name?: string;
  imageUrl: string;
  previewUrl?: string;
  source: 'upload' | 'tenor';
  createdAt: string;
}

export interface FavoriteSticker {
  id: string;
  stickerUrl: string;
  previewUrl?: string;
  source: 'upload' | 'tenor';
  tenorId?: string;
  createdAt: string;
}

// ==================== Tenor 搜索 API ====================

/**
 * 搜索 Tenor 贴图
 */
export const searchStickers = async (
  q: string,
  limit: number = 20,
  pos?: string
): Promise<TenorSearchResponse> => {
  const params: Record<string, string | number> = { q, limit };
  if (pos) params.pos = pos;

  // ApiAdapter 会自动把 snake_case 转成 camelCase
  const data = await api.get<{
    stickers: Array<{
      id: string;
      url: string;
      previewUrl: string;
      description?: string;
    }>;
    next?: string;
  }>('/stickers/search', params);

  return {
    stickers: data.stickers.map(s => ({
      id: s.id,
      url: s.url,
      previewUrl: s.previewUrl,
      description: s.description
    })),
    next: data.next
  };
};

/**
 * 获取热门贴图
 */
export const getTrendingStickers = async (
  limit: number = 20,
  pos?: string
): Promise<TenorSearchResponse> => {
  const params: Record<string, string | number> = { limit };
  if (pos) params.pos = pos;

  // ApiAdapter 会自动把 snake_case 转成 camelCase
  const data = await api.get<{
    stickers: Array<{
      id: string;
      url: string;
      previewUrl: string;
      description?: string;
    }>;
    next?: string;
  }>('/stickers/trending', params);

  return {
    stickers: data.stickers.map(s => ({
      id: s.id,
      url: s.url,
      previewUrl: s.previewUrl,
      description: s.description
    })),
    next: data.next
  };
};

// ==================== 用户自定义贴图 API ====================

/**
 * 获取用户自定义贴图列表
 */
export const getMyStickers = async (
  skip: number = 0,
  limit: number = 50
): Promise<UserSticker[]> => {
  // ApiAdapter 会自动把 snake_case 转成 camelCase
  const data = await api.get<Array<{
    id: string;
    name?: string;
    imageUrl: string;
    previewUrl?: string;
    source: string;
    createdAt: string;
  }>>('/stickers/my', { skip, limit });

  return data.map(s => ({
    id: s.id,
    name: s.name,
    imageUrl: s.imageUrl,
    previewUrl: s.previewUrl,
    source: s.source as 'upload' | 'tenor',
    createdAt: s.createdAt
  }));
};

/**
 * 上传自定义贴图
 */
export const uploadSticker = async (
  file: File,
  name?: string
): Promise<UserSticker> => {
  const formData = new FormData();
  formData.append('file', file);
  if (name) formData.append('name', name);

  // ApiAdapter 会自动把 snake_case 转成 camelCase
  const data = await api.post<{
    id: string;
    name?: string;
    imageUrl: string;
    previewUrl?: string;
    source: string;
    createdAt: string;
  }>('/stickers/upload', formData);

  return {
    id: data.id,
    name: data.name,
    imageUrl: data.imageUrl,
    previewUrl: data.previewUrl,
    source: data.source as 'upload' | 'tenor',
    createdAt: data.createdAt
  };
};

/**
 * 删除自定义贴图
 */
export const deleteSticker = async (stickerId: string): Promise<void> => {
  await api.delete(`/stickers/my/${stickerId}`);
};

// ==================== 收藏贴图 API ====================

/**
 * 获取收藏的贴图列表
 */
export const getFavoriteStickers = async (
  skip: number = 0,
  limit: number = 50
): Promise<FavoriteSticker[]> => {
  // ApiAdapter 会自动把 snake_case 转成 camelCase
  const data = await api.get<Array<{
    id: string;
    stickerUrl: string;
    previewUrl?: string;
    source: string;
    tenorId?: string;
    createdAt: string;
  }>>('/stickers/favorites', { skip, limit });

  return data.map(s => ({
    id: s.id,
    stickerUrl: s.stickerUrl,
    previewUrl: s.previewUrl,
    source: s.source as 'upload' | 'tenor',
    tenorId: s.tenorId,
    createdAt: s.createdAt
  }));
};

/**
 * 收藏贴图
 */
export const addFavoriteSticker = async (params: {
  stickerUrl: string;
  previewUrl?: string;
  source?: 'upload' | 'tenor';
  tenorId?: string;
}): Promise<FavoriteSticker> => {
  // ApiAdapter 会自动把 snake_case 转成 camelCase
  const data = await api.post<{
    id: string;
    stickerUrl: string;
    previewUrl?: string;
    source: string;
    tenorId?: string;
    createdAt: string;
  }>('/stickers/favorites', {
    sticker_url: params.stickerUrl,
    preview_url: params.previewUrl,
    source: params.source || 'tenor',
    tenor_id: params.tenorId
  });

  return {
    id: data.id,
    stickerUrl: data.stickerUrl,
    previewUrl: data.previewUrl,
    source: data.source as 'upload' | 'tenor',
    tenorId: data.tenorId,
    createdAt: data.createdAt
  };
};

/**
 * 取消收藏贴图
 */
export const removeFavoriteSticker = async (favoriteId: string): Promise<void> => {
  await api.delete(`/stickers/favorites/${favoriteId}`);
};

// 导出所有 API 函数
export const stickerApi = {
  searchStickers,
  getTrendingStickers,
  getMyStickers,
  uploadSticker,
  deleteSticker,
  getFavoriteStickers,
  addFavoriteSticker,
  removeFavoriteSticker,
};
