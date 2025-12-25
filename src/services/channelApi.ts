/**
 * 频道系统 API 服务
 */

import { ApiAdapter } from './ApiAdapter';

const api = new ApiAdapter();

// ==================== 类型定义 ====================

export interface Channel {
  id: string;
  name: string;
  description?: string;
  coverImage?: string;
  type: 'official' | 'fangroup' | 'work';
  status: 'active' | 'warning' | 'locked';
  creatorId?: string;
  workId?: string;
  isPermanent: boolean;
  isPinned: boolean;
  memberCount: number;
  messageCount: number;
  lastMessageAt?: string;
  warningDays?: number;
  createdAt: string;
  updatedAt: string;
  lockedAt?: string;
  // 作品频道额外字段
  bookTitle?: string;
  author?: string;
  collectCount?: number;
  // 当前用户在该频道中的角色
  currentUserRole?: 'owner' | 'admin' | 'member';
  // 进入要求
  joinRequirement?: string | null;
  canAccess?: boolean;
}

export interface ChannelListResponse {
  channels: Channel[];
  total: number;
}

export interface ChannelMember {
  id: string;
  userId: string;
  username: string;
  avatar?: string;
  role: 'owner' | 'admin' | 'member';
  customTitle?: string | null;  // 频道内自定义称号
  titleColor?: string | null;   // 称号颜色
  isMuted: boolean;             // 是否被禁言
  mutedUntil?: string | null;   // 禁言到期时间
  joinedAt: string;
}

export interface ChannelMemberListResponse {
  members: ChannelMember[];
  total: number;
}

export interface ChannelMessage {
  id: string;
  channelId: string;
  userId?: string;
  content: string;
  type: 'normal' | 'announcement' | 'mention';
  isPinned: boolean;
  isDeleted: boolean;
  replyToId?: string;
  reactionCount: number;
  createdAt: string;
  updatedAt: string;
  deletedAt?: string;
  // 用户信息
  userName?: string;
  userAvatar?: string;
  userHonor?: string;  // 用户全局称号
  userTitle?: string;  // 频道内自定义称号
  userTitleColor?: string;
}

export interface ChannelMessageListResponse {
  messages: ChannelMessage[];
  total: number;
  has_more: boolean;
}

// ==================== 频道 API ====================

/**
 * 获取当前用户加入的频道列表
 */
export const getMyChannels = async (): Promise<ChannelListResponse> => {
  const data = await api.get<ChannelListResponse>('/channels/my-channels');
  return data;
};

/**
 * 获取可加入的频道列表
 */
export const getAvailableChannels = async (params: {
  skip?: number;
  limit?: number;
}): Promise<ChannelListResponse> => {
  const data = await api.get<ChannelListResponse>('/channels/available-channels', { params });
  return data;
};

/**
 * 加入频道
 */
export const joinChannel = async (channelId: string): Promise<ChannelMember> => {
  const data = await api.post<ChannelMember>('/channels/join', {
    channel_id: channelId
  });
  return data;
};

/**
 * 退出频道
 *
 * @returns disbanded - true 表示频道已解散（粉丝群创建者退出），false 表示普通退出
 */
export const leaveChannel = async (channelId: string): Promise<{ message: string; disbanded: boolean }> => {
  const data = await api.delete<{ message: string; disbanded: boolean }>(`/channels/${channelId}/leave`);
  return data;
};

/**
 * 获取频道成员列表
 */
export const getChannelMembers = async (channelId: string): Promise<ChannelMemberListResponse> => {
  const data = await api.get<ChannelMemberListResponse>(`/channels/${channelId}/members`);
  return data;
};

/**
 * 踢出频道成员（仅创建者可操作）
 */
export const kickMember = async (channelId: string, userId: string): Promise<{ message: string }> => {
  const data = await api.delete<{ message: string }>(`/channels/${channelId}/members/${userId}`);
  return data;
};

/**
 * 禁言成员（仅创建者可操作）
 */
export const muteMember = async (
  channelId: string,
  userId: string,
  durationMinutes: number
): Promise<{ message: string; muteUntil: string }> => {
  const data = await api.post<{ message: string; muteUntil: string }>(
    `/channels/${channelId}/members/${userId}/mute?duration_minutes=${durationMinutes}`
  );
  return data;
};

/**
 * 解除禁言（仅创建者可操作）
 */
export const unmuteMember = async (channelId: string, userId: string): Promise<{ message: string }> => {
  const data = await api.post<{ message: string }>(`/channels/${channelId}/members/${userId}/unmute`);
  return data;
};

// ==================== 消息 API ====================

/**
 * 获取频道消息列表
 */
export const getChannelMessages = async (
  channelId: string,
  params: {
    skip?: number;
    limit?: number;
  }
): Promise<ChannelMessageListResponse> => {
  const data = await api.get<ChannelMessageListResponse>(
    `/channels/${channelId}/messages`,
    { params }
  );
  return data;
};

/**
 * 获取频道公告列表
 */
export const getChannelAnnouncements = async (
  channelId: string,
  params: {
    skip?: number;
    limit?: number;
  }
): Promise<ChannelMessageListResponse> => {
  const data = await api.get<ChannelMessageListResponse>(
    `/channels/${channelId}/announcements`,
    { params }
  );
  return data;
};

/**
 * 发送消息
 */
export const sendMessage = async (
  channelId: string,
  content: string,
  messageType: 'normal' | 'announcement' = 'normal',
  replyToId?: string
): Promise<ChannelMessage> => {
  // 构建 URL 参数
  const params = new URLSearchParams({
    content,
    message_type: messageType
  });

  if (replyToId) {
    params.append('reply_to_id', replyToId);
  }

  const data = await api.post<ChannelMessage>(
    `/channels/${channelId}/messages?${params.toString()}`,
    null
  );
  return data;
};

/**
 * 举报消息
 */
export const reportMessage = async (
  channelId: string,
  messageId: string,
  reason: 'spam' | 'inappropriate' | 'harassment' | 'other',
  description?: string
): Promise<{ message: string }> => {
  const params = new URLSearchParams({ reason });
  if (description) {
    params.append('description', description);
  }

  const data = await api.post<{ message: string }>(
    `/channels/${channelId}/messages/${messageId}/report?${params.toString()}`,
    null
  );
  return data;
};

// ==================== 粉丝群管理 API ====================

/**
 * 创建粉丝群
 */
export const createFangroup = async (data: {
  name: string;
  description?: string;
  cover_image?: string;
}): Promise<Channel> => {
  const result = await api.post<Channel>('/channels/create-fangroup', data);
  return result;
};

/**
 * 更新粉丝群信息
 */
export const updateFangroup = async (
  channelId: string,
  data: {
    name?: string;
    description?: string;
    cover_image?: string;
  }
): Promise<Channel> => {
  const result = await api.put<Channel>(`/channels/${channelId}`, data);
  return result;
};

/**
 * 删除粉丝群
 */
export const deleteFangroup = async (channelId: string): Promise<{ message: string }> => {
  const result = await api.delete<{ message: string }>(`/channels/${channelId}`);
  return result;
};

// ==================== 未读消息和@提醒 API ====================

export interface UnreadSummary {
  channels: {
    channelId: string;
    unreadCount: number;
    mentionCount: number;
    hasMention: boolean;
  }[];
}

export interface UnreadInfo {
  unreadCount: number;
  mentionCount: number;
  firstUnreadMessageId: string | null;
  latestMentionMessageId: string | null;
  lastReadMessageId: string | null;
}

/**
 * 标记频道为已读
 */
export const markChannelAsRead = async (
  channelId: string,
  messageId?: string
): Promise<{ message: string }> => {
  const params = new URLSearchParams();
  if (messageId) {
    params.append('message_id', messageId);
  }
  return await api.post(`/channels/${channelId}/mark-read?${params.toString()}`);
};

/**
 * 获取所有频道的未读统计
 */
export const getUnreadSummary = async (): Promise<UnreadSummary> => {
  return await api.get('/channels/unread-summary');
};

/**
 * 获取单个频道的详细未读信息
 */
export const getChannelUnreadInfo = async (channelId: string): Promise<UnreadInfo> => {
  return await api.get(`/channels/${channelId}/unread-info`);
};

// ==================== 公告系统 API ====================

export interface Announcement {
  id: string;
  content: string;
  createdAt: string;
  userName: string;
  userAvatar?: string;
  userTitle?: string;
  userTitleColor?: string;
  isPinned?: boolean;
}

export interface AnnouncementListResponse {
  announcements: Announcement[];
  total: number;
  hasMore: boolean;
}

/**
 * 获取最新公告
 */
export const getLatestAnnouncement = async (
  channelId: string
): Promise<{ announcement: Announcement | null }> => {
  return await api.get(`/channels/${channelId}/latest-announcement`);
};

// ==================== 消息管理 API ====================

/**
 * 撤回消息
 */
export const recallMessage = async (
  channelId: string,
  messageId: string
): Promise<{ message: string }> => {
  return await api.delete(`/channels/${channelId}/messages/${messageId}/recall`);
};

// ==================== 搜索功能 API ====================

export interface SearchResult {
  messages: ChannelMessage[];
  total: number;
  hasMore: boolean;
}

/**
 * 搜索频道消息
 */
export const searchMessages = async (
  channelId: string,
  keyword: string,
  options?: {
    userId?: string;
    startDate?: string;
    endDate?: string;
    skip?: number;
    limit?: number;
  }
): Promise<SearchResult> => {
  const params = new URLSearchParams({ keyword });
  if (options?.userId) params.append('user_id', options.userId);
  if (options?.startDate) params.append('start_date', options.startDate);
  if (options?.endDate) params.append('end_date', options.endDate);
  if (options?.skip !== undefined) params.append('skip', options.skip.toString());
  if (options?.limit !== undefined) params.append('limit', options.limit.toString());

  return await api.get(`/channels/${channelId}/search?${params.toString()}`);
};

// ==================== 频道设置 API ====================

/**
 * 更新频道设置
 */
export const updateChannelSettings = async (
  channelId: string,
  settings: {
    name?: string;
    description?: string;
    coverImage?: string;
  }
): Promise<{ message: string; channel: Channel }> => {
  const params = new URLSearchParams();
  if (settings.name) params.append('name', settings.name);
  if (settings.description) params.append('description', settings.description);
  if (settings.coverImage) params.append('cover_image', settings.coverImage);

  return await api.put(`/channels/${channelId}/settings?${params.toString()}`);
};

// ==================== 成员权限管理 API ====================
/**
 * 修改成员称号
 */
export const updateMemberTitle = async (
  channelId: string,
  userId: string,
  titleData: {
    customTitle?: string | null;
    titleColor?: string;
  }
): Promise<{ message: string; customTitle: string | null; titleColor: string | null }> => {
  return await api.patch(`/channels/${channelId}/members/${userId}/title`, titleData);
};

// 导出一个包含所有 API 函数的对象
export const channelApi = {
  // 频道管理
  getMyChannels,
  getAvailableChannels,
  joinChannel,
  createFangroup,
  leaveChannel,

  // 成员管理
  getChannelMembers,

  // 消息管理
  getChannelMessages,
  sendMessage,

  // 举报功能
  reportMessage,

  // 未读和@提醒
  markChannelAsRead,
  getUnreadSummary,
  getChannelUnreadInfo,

  // 公告功能
  getChannelAnnouncements,
  getLatestAnnouncement,

  // 消息撤回
  recallMessage,

  // 搜索功能
  searchMessages,

  // 频道设置
  updateChannelSettings,

  // 成员权限
  muteMember,
  unmuteMember,
  updateMemberTitle,
};
