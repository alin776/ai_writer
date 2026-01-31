/**
 * 用户主页 API
 */
import { ApiAdapter } from './ApiAdapter';

const apiAdapter = new ApiAdapter();

// ========== 类型定义 ==========

export interface UserProfileStats {
  workCount: number;
  totalWords: number;
  totalFavorites: number;
  friendCount: number;
}

export interface PendingRequest {
  id: string;
  direction: 'sent' | 'received';
  status: string;
}

export interface UserRelation {
  isSelf: boolean;
  isFriend: boolean;
  privateChannelId: string | null;
  pendingRequest: PendingRequest | null;
}

export interface WorkBrief {
  id: string;
  title: string;
  coverImage: string | null;
  totalWords: number;
  favoriteCount: number;
  genre: string;
  status: string;
}

export interface UserInfo {
  id: string;
  username: string;
  fullName: string | null;
  avatar: string | null;
  bio: string | null;
  honor: string | null;
  createdAt: string;
}

export interface UserProfile {
  user: UserInfo;
  stats: UserProfileStats;
  relation: UserRelation;
  works: WorkBrief[];
}

// ========== API 函数 ==========

/**
 * 获取用户主页数据
 */
export async function getUserProfile(userId: string): Promise<UserProfile> {
  return apiAdapter.get(`/users/${userId}/profile`);
}

// 默认导出
export default {
  getUserProfile
};
