/**
 * 好友系统 API
 */
import { ApiAdapter } from './ApiAdapter';

const apiAdapter = new ApiAdapter();

// ========== 类型定义 ==========

export interface UserBrief {
  id: string;
  username: string;
  fullName: string | null;
  avatar: string | null;
}

export interface FriendRequest {
  id: string;
  fromUser: UserBrief;
  toUser: UserBrief;
  message: string | null;
  status: string;
  createdAt: string;
}

export interface FriendRequestListResponse {
  total: number;
  items: FriendRequest[];
}

export interface FriendshipResponse {
  id: string;
  friend: UserBrief;
  privateChannelId: string | null;
  lastMessageAt: string | null;  // 私聊频道最后消息时间
  createdAt: string;
}

export interface FriendListResponse {
  total: number;
  items: FriendshipResponse[];
}

export interface PendingRequestInfo {
  id: string;
  direction: 'sent' | 'received';
  status: string;
}

export interface FriendCheckResponse {
  isFriend: boolean;
  friendshipId?: string;
  privateChannelId?: string;
  pendingRequest?: PendingRequestInfo;
}

export interface PendingCountResponse {
  pendingCount: number;
}

export interface UserSearchResult {
  id: string;
  username: string;
  fullName: string | null;
  avatar: string | null;
  relationStatus: 'none' | 'friend' | 'request_sent' | 'request_received';
}

export interface UserSearchResponse {
  total: number;
  items: UserSearchResult[];
}

export interface AcceptRequestResponse {
  message: string;
  friendship: FriendshipResponse;
  privateChannelId: string;
}

// ========== API 函数 ==========

/**
 * 搜索用户
 */
export async function searchUsers(
  keyword: string,
  skip: number = 0,
  limit: number = 20
): Promise<UserSearchResponse> {
  return apiAdapter.get('/users/search', { keyword, skip, limit });
}

/**
 * 发送好友请求
 */
export async function sendFriendRequest(
  toUserId: string,
  message?: string
): Promise<FriendRequest> {
  return apiAdapter.post('/friends/request', {
    to_user_id: toUserId,
    message
  });
}

/**
 * 获取收到的好友请求
 */
export async function getReceivedRequests(
  status: string = 'pending',
  skip: number = 0,
  limit: number = 20
): Promise<FriendRequestListResponse> {
  return apiAdapter.get('/friends/requests/received', { status, skip, limit });
}

/**
 * 获取发出的好友请求
 */
export async function getSentRequests(
  status: string = 'pending',
  skip: number = 0,
  limit: number = 20
): Promise<FriendRequestListResponse> {
  return apiAdapter.get('/friends/requests/sent', { status, skip, limit });
}

/**
 * 处理好友请求（同意/拒绝）
 */
export async function handleFriendRequest(
  requestId: string,
  action: 'accept' | 'reject'
): Promise<AcceptRequestResponse | { message: string }> {
  return apiAdapter.put(`/friends/request/${requestId}`, { action });
}

/**
 * 获取待处理请求数量
 */
export async function getPendingCount(): Promise<PendingCountResponse> {
  return apiAdapter.get('/friends/requests/count');
}

/**
 * 获取好友列表
 */
export async function getFriends(
  skip: number = 0,
  limit: number = 50
): Promise<FriendListResponse> {
  return apiAdapter.get('/friends', { skip, limit });
}

/**
 * 删除好友
 */
export async function deleteFriend(friendId: string): Promise<{ message: string }> {
  return apiAdapter.delete(`/friends/${friendId}`);
}

/**
 * 检查好友关系
 */
export async function checkFriendship(userId: string): Promise<FriendCheckResponse> {
  return apiAdapter.get(`/friends/check/${userId}`);
}

// 默认导出
export default {
  searchUsers,
  sendFriendRequest,
  getReceivedRequests,
  getSentRequests,
  handleFriendRequest,
  getPendingCount,
  getFriends,
  deleteFriend,
  checkFriendship
};
