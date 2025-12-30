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
  isEdited: boolean;
  replyToId?: string;
  reactionCount: number;
  createdAt: string;
  updatedAt: string;
  deletedAt?: string;
  editedAt?: string;
  // 用户信息
  userName?: string;
  userAvatar?: string;
  userTitle?: string;
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
 * 获取频道所有公告
 */
export const getChannelAnnouncements = async (
  channelId: string,
  skip: number = 0,
  limit: number = 20
): Promise<AnnouncementListResponse> => {
  return await api.get(`/channels/${channelId}/announcements?skip=${skip}&limit=${limit}`);
};

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

/**
 * 编辑消息
 */
export const editMessage = async (
  channelId: string,
  messageId: string,
  content: string
): Promise<ChannelMessage> => {
  return await api.patch(`/channels/${channelId}/messages/${messageId}`, { content });
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
 * 禁言成员
 */
export const muteMember = async (
  channelId: string,
  userId: string,
  durationMinutes: number
): Promise<{ message: string; muteUntil: string }> => {
  return await api.post(
    `/channels/${channelId}/members/${userId}/mute?duration_minutes=${durationMinutes}`
  );
};

/**
 * 取消禁言
 */
export const unmuteMember = async (
  channelId: string,
  userId: string
): Promise<{ message: string }> => {
  return await api.post(`/channels/${channelId}/members/${userId}/unmute`);
};

// ==================== 消息反应（Emoji Reactions）API ====================

export interface ReactionSummary {
  emoji: string;
  count: number;
  hasReacted: boolean;
}

export interface MessageReactionsResponse {
  messageId: string;
  reactions: ReactionSummary[];
  totalCount: number;
}

export interface ReactionUser {
  userId: string;
  username: string;
  avatar: string | null;
}

export interface ReactionDetailResponse {
  emoji: string;
  count: number;
  users: ReactionUser[];
}

// ==================== 置顶消息类型 ====================

export interface PinnedMessage {
  id: string;
  channelId: string;
  content: string;
  userId?: string;
  userName?: string;
  userAvatar?: string;
  isPinned: boolean;
  pinnedAt?: string;
  pinnedBy?: string;
  pinnedByName?: string;
  createdAt: string;
}

export interface PinnedMessagesListResponse {
  messages: PinnedMessage[];
  total: number;
}

/**
 * 添加消息反应
 */
export const addReaction = async (
  channelId: string,
  messageId: string,
  emoji: string
): Promise<{ message: string; action: string }> => {
  return await api.post(`/channels/${channelId}/messages/${messageId}/reactions`, {
    emoji
  });
};

/**
 * 移除消息反应
 */
export const removeReaction = async (
  channelId: string,
  messageId: string,
  emoji: string
): Promise<{ message: string }> => {
  return await api.delete(`/channels/${channelId}/messages/${messageId}/reactions/${encodeURIComponent(emoji)}`);
};

/**
 * 获取消息的所有反应汇总
 */
export const getMessageReactions = async (
  channelId: string,
  messageId: string
): Promise<MessageReactionsResponse> => {
  return await api.get(`/channels/${channelId}/messages/${messageId}/reactions`);
};

/**
 * 获取指定 emoji 反应的用户列表
 */
export const getReactionUsers = async (
  channelId: string,
  messageId: string,
  emoji: string,
  skip: number = 0,
  limit: number = 20
): Promise<ReactionDetailResponse> => {
  return await api.get(
    `/channels/${channelId}/messages/${messageId}/reactions/${encodeURIComponent(emoji)}/users?skip=${skip}&limit=${limit}`
  );
};

// ==================== 置顶消息 API ====================

/**
 * 置顶消息
 */
export const pinMessage = async (
  channelId: string,
  messageId: string
): Promise<{ message: string; action: string }> => {
  return await api.post(`/channels/${channelId}/messages/${messageId}/pin`);
};

/**
 * 取消置顶消息
 */
export const unpinMessage = async (
  channelId: string,
  messageId: string
): Promise<{ message: string; action: string }> => {
  return await api.delete(`/channels/${channelId}/messages/${messageId}/pin`);
};

/**
 * 获取频道的所有置顶消息
 */
export const getPinnedMessages = async (
  channelId: string
): Promise<PinnedMessagesListResponse> => {
  return await api.get(`/channels/${channelId}/pinned-messages`);
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

  // 消息撤回/编辑
  recallMessage,
  editMessage,

  // 搜索功能
  searchMessages,

  // 频道设置
  updateChannelSettings,

  // 成员权限
  muteMember,
  unmuteMember,

  // 消息反应
  addReaction,
  removeReaction,
  getMessageReactions,
  getReactionUsers,

  // 消息置顶
  pinMessage,
  unpinMessage,
  getPinnedMessages,
};
