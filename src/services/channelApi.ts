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
  type: 'official' | 'fangroup' | 'work' | 'private';
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
  // 慢速模式
  slowmodeInterval?: number;
  // 静音状态
  isMuted?: boolean;
}

export interface ChannelListResponse {
  channels: Channel[];
  total: number;
}

export interface ChannelMember {
  id: string;
  userId: string;
  username: string;
  fullName?: string;
  avatar?: string;
  bio?: string;
  onlineStatus?: 'online' | 'idle' | 'dnd' | 'offline';
  title?: string;
  titleColor?: string;
  role: 'owner' | 'admin' | 'member';
  joinedAt: string;
  isMuted?: boolean;
  mutedUntil?: string;
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
  forwardedFromId?: string;  // 转发来源消息ID
  forwardedFrom?: {  // 转发来源详细信息（ApiAdapter 已转为 camelCase）
    messageId: string;
    channelId: string;
    channelName: string;
    userId?: string;
    userName: string;
    userAvatar?: string;
    userBio?: string;
    userHonor?: string;
    content: string;
    createdAt: string;
    attachments?: {
      id: string;
      fileName: string;
      fileType?: string;
      fileUrl: string;
      thumbnailUrl?: string;
    }[];
  };
  reactionCount: number;
  createdAt: string;
  updatedAt: string;
  deletedAt?: string;
  editedAt?: string;
  // 用户信息
  userName?: string;
  userAvatar?: string;
  userBio?: string;
  userTitle?: string;
  userTitleColor?: string;
  userOnlineStatus?: 'online' | 'idle' | 'dnd' | 'offline';
  // 附件
  attachments?: MessageAttachment[];
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
 * - 官方频道：直接加入，返回 status: "joined"
 * - 其他频道：创建申请，返回 status: "pending"
 */
export interface JoinChannelResponse {
  status: 'joined' | 'pending';
  message: string;
  member?: ChannelMember;
  request_id?: string;
}

export const joinChannel = async (channelId: string, joinMessage?: string): Promise<JoinChannelResponse> => {
  const data = await api.post<JoinChannelResponse>('/channels/join', {
    channel_id: channelId,
    message: joinMessage
  });
  return data;
};

/**
 * 邀请好友加入频道（发送私信邀请）
 */
export const inviteToChannel = async (channelId: string, userId: string): Promise<{
  message: string;
  inviteSent?: boolean;
  alreadyMember?: boolean;
  privateChannelId?: string;
}> => {
  const data = await api.post<{
    message: string;
    invite_sent?: boolean;
    already_member?: boolean;
    private_channel_id?: string;
  }>(`/channels/${channelId}/invite`, {
    user_id: userId
  });
  return {
    message: data.message,
    inviteSent: data.invite_sent,
    alreadyMember: data.already_member,
    privateChannelId: data.private_channel_id
  };
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
 * 获取指定消息及其前后的消息
 * 用于跳转到历史消息时加载消息上下文
 */
export const getMessagesAround = async (
  channelId: string,
  messageId: string,
  limit: number = 50
): Promise<ChannelMessageListResponse> => {
  const data = await api.get<ChannelMessageListResponse>(
    `/channels/${channelId}/messages/around/${messageId}`,
    { params: { limit } }
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
 * 上传频道封面
 */
export const uploadChannelCover = async (file: File): Promise<{ coverUrl: string }> => {
  const formData = new FormData();
  formData.append('file', file);

  // FormData 会自动设置 Content-Type，不需要手动指定
  const result = await api.post<{ coverUrl: string }>('/channels/upload-cover', formData);
  return result;
};

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
  has_more: boolean;
}

/**
 * 搜索频道消息
 * @param channelId 频道ID
 * @param options 搜索选项
 * @param options.keyword 搜索关键词（与contentType至少需要一个）
 * @param options.contentType 内容类型：image_video | file | link
 * @param options.userId 筛选发送者
 * @param options.startDate 起始日期 YYYY-MM-DD
 * @param options.endDate 结束日期 YYYY-MM-DD
 * @param options.skip 分页偏移
 * @param options.limit 每页数量
 */
export const searchMessages = async (
  channelId: string,
  options?: {
    keyword?: string;
    contentType?: 'image_video' | 'file' | 'link';
    userId?: string;
    startDate?: string;
    endDate?: string;
    skip?: number;
    limit?: number;
  }
): Promise<SearchResult> => {
  const params = new URLSearchParams();
  if (options?.keyword) params.append('keyword', options.keyword);
  if (options?.contentType) params.append('content_type', options.contentType);
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

// ==================== 附件类型 ====================

export interface MessageAttachment {
  id: string;
  fileName: string;
  fileType?: string;
  fileSize: number;
  fileUrl: string;
  thumbnailUrl?: string;
  createdAt?: string;
}

export interface AttachmentUploadResponse {
  id: string;
  fileName: string;
  fileType: string;
  fileSize: number;
  fileUrl: string;
  thumbnailUrl?: string;
}

// 扩展 ChannelMessage 类型以包含附件
export interface ChannelMessageWithAttachments extends ChannelMessage {
  attachments?: MessageAttachment[];
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

// ==================== 附件上传 API ====================

/**
 * 上传附件文件
 */
export const uploadAttachment = async (
  channelId: string,
  file: File
): Promise<AttachmentUploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  return await api.post(`/channels/${channelId}/upload`, formData);
};

/**
 * 发送带附件的消息
 */
export const sendMessageWithAttachments = async (
  channelId: string,
  content: string,
  attachmentIds: string[],
  messageType: 'normal' | 'announcement' = 'normal',
  replyToId?: string
): Promise<ChannelMessageWithAttachments> => {
  const params = new URLSearchParams();
  if (content) params.append('content', content);
  params.append('message_type', messageType);
  if (replyToId) params.append('reply_to_id', replyToId);
  attachmentIds.forEach(id => params.append('attachment_ids', id));

  return await api.post(`/channels/${channelId}/messages-with-attachments?${params.toString()}`);
};

/**
 * 获取消息的附件列表
 */
export const getMessageAttachments = async (
  channelId: string,
  messageId: string
): Promise<{ attachments: MessageAttachment[] }> => {
  return await api.get(`/channels/${channelId}/messages/${messageId}/attachments`);
};

// ==================== 消息转发 API ====================

export interface ForwardMessageRequest {
  target_channel_ids: string[];
  add_comment?: string;
}

export interface ForwardMessageResponse {
  forwardedCount: number;
  failedChannels: string[];
  messages: {
    channelId: string;
    channelName: string;
    messageId: string;
  }[];
}

export interface ForwardInfo {
  isForwarded: boolean;
  originalDeleted?: boolean;
  original?: {
    messageId: string;
    channelId: string;
    channelName: string;
    userName: string;
    content: string;
    createdAt: string;
  };
}

/**
 * 转发消息到其他频道
 */
export const forwardMessage = async (
  channelId: string,
  messageId: string,
  request: ForwardMessageRequest
): Promise<ForwardMessageResponse> => {
  return await api.post(`/channels/${channelId}/messages/${messageId}/forward`, request);
};

/**
 * 获取转发消息的原始信息
 */
export const getForwardInfo = async (
  channelId: string,
  messageId: string
): Promise<ForwardInfo> => {
  return await api.get(`/channels/${channelId}/messages/${messageId}/forward-info`);
};

// ==================== 加入申请管理 API ====================

export interface JoinRequest {
  id: string;
  channelId: string;
  userId: string;
  message?: string;
  status: 'pending' | 'approved' | 'rejected';
  reviewedBy?: string;
  reviewedAt?: string;
  rejectReason?: string;
  createdAt: string;
  userName?: string;
  userAvatar?: string;
  reviewerName?: string;
}

export interface JoinRequestListResponse {
  requests: JoinRequest[];
  total: number;
}

/**
 * 获取频道的加入申请列表（管理员）
 */
export const getJoinRequests = async (
  channelId: string,
  options?: {
    status?: 'pending' | 'approved' | 'rejected';
    page?: number;
    pageSize?: number;
  }
): Promise<JoinRequestListResponse> => {
  const params = new URLSearchParams();
  if (options?.status) params.append('status_filter', options.status);
  if (options?.page) params.append('page', options.page.toString());
  if (options?.pageSize) params.append('page_size', options.pageSize.toString());

  return await api.get(`/channels/${channelId}/join-requests?${params.toString()}`);
};

/**
 * 审核加入申请
 */
export const reviewJoinRequest = async (
  channelId: string,
  requestId: string,
  action: 'approve' | 'reject',
  rejectReason?: string
): Promise<{ message: string; status: string }> => {
  return await api.post(`/channels/${channelId}/join-requests/${requestId}/review`, {
    action,
    reject_reason: rejectReason
  });
};

/**
 * 获取我的加入申请列表
 */
export const getMyJoinRequests = async (
  options?: {
    status?: 'pending' | 'approved' | 'rejected';
    page?: number;
    pageSize?: number;
  }
): Promise<JoinRequestListResponse> => {
  const params = new URLSearchParams();
  if (options?.status) params.append('status_filter', options.status);
  if (options?.page) params.append('page', options.page.toString());
  if (options?.pageSize) params.append('page_size', options.pageSize.toString());

  return await api.get(`/channels/my-join-requests?${params.toString()}`);
};


// ==================== 频道通知设置 API ====================

export interface NotificationSettings {
  isMuted: boolean;
  muteUntil: string | null;
  notifyMentions: boolean;
  notifyAnnouncements: boolean;
}

/**
 * 获取频道通知设置
 */
export const getNotificationSettings = async (
  channelId: string
): Promise<NotificationSettings> => {
  return await api.get(`/channels/${channelId}/notification-settings`);
};

/**
 * 更新频道通知设置
 */
export const updateNotificationSettings = async (
  channelId: string,
  settings: {
    isMuted?: boolean;
    muteHours?: number;  // 静音时长（小时），最长8760（1年）
    notifyMentions?: boolean;
    notifyAnnouncements?: boolean;
  }
): Promise<NotificationSettings> => {
  const params = new URLSearchParams();
  if (settings.isMuted !== undefined) params.append('is_muted', settings.isMuted.toString());
  if (settings.muteHours !== undefined) params.append('mute_hours', settings.muteHours.toString());
  if (settings.notifyMentions !== undefined) params.append('notify_mentions', settings.notifyMentions.toString());
  if (settings.notifyAnnouncements !== undefined) params.append('notify_announcements', settings.notifyAnnouncements.toString());

  return await api.put(`/channels/${channelId}/notification-settings?${params.toString()}`);
};

// ==================== 共同频道 API ====================

/**
 * 获取与指定用户的共同频道
 */
export const getMutualChannels = async (userId: string): Promise<{
  channels: Channel[];
}> => {
  const data = await api.get<{ channels: Channel[] }>(`/channels/mutual/${userId}`);
  return data;
};

// ==================== 邀请链接预览 API ====================

export interface InvitePreview {
  channelId: string;
  channelName: string;
  channelIcon: string | null;
  channelType: string;
  memberCount: number;
  onlineCount: number;
  createdAt: string | null;
  isValid: boolean;
  isMember: boolean;  // 当前用户是否已是频道成员
}

/**
 * 获取邀请链接预览信息（无需登录）
 */
export const getInvitePreview = async (inviteCode: string): Promise<InvitePreview> => {
  // ApiAdapter 已经自动将 snake_case 转换为 camelCase，直接返回即可
  const data = await api.get<InvitePreview>(`/channels/invite/${inviteCode}/preview`);
  return data;
};

/**
 * 通过邀请码加入频道
 */
export const joinByInviteCode = async (inviteCode: string): Promise<{
  message: string;
  channelId: string;
  channelName: string;
}> => {
  // ApiAdapter 已经自动将 snake_case 转换为 camelCase，直接返回即可
  const data = await api.post<{
    message: string;
    channelId: string;
    channelName: string;
  }>(`/channels/join-by-invite/${inviteCode}`);
  return data;
};

/**
 * 创建频道邀请链接
 */
export const createInviteLink = async (
  channelId: string,
  options?: { maxUses?: number; expiresHours?: number }
): Promise<{
  id: string;
  code: string;
  maxUses: number | null;
  useCount: number;
  expiresAt: string | null;
  inviteUrl: string;
}> => {
  const params = new URLSearchParams();
  if (options?.maxUses) params.append('max_uses', options.maxUses.toString());
  if (options?.expiresHours) params.append('expires_hours', options.expiresHours.toString());

  const url = `/channels/${channelId}/invites${params.toString() ? `?${params.toString()}` : ''}`;
  // ApiAdapter 已经自动将 snake_case 转换为 camelCase，直接返回即可
  const data = await api.post<{
    id: string;
    code: string;
    maxUses: number | null;
    useCount: number;
    expiresAt: string | null;
    inviteUrl: string;
  }>(url);
  return data;
};

// 导出一个包含所有 API 函数的对象
export const channelApi = {
  // 频道管理
  getMyChannels,
  getAvailableChannels,
  joinChannel,
  createFangroup,
  uploadChannelCover,
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

  // 附件上传
  uploadAttachment,
  sendMessageWithAttachments,
  getMessageAttachments,

  // 消息转发
  forwardMessage,
  getForwardInfo,

  // 加入申请管理
  getJoinRequests,
  reviewJoinRequest,
  getMyJoinRequests,

  // 频道通知设置
  getNotificationSettings,
  updateNotificationSettings,

  // 邀请链接预览
  getInvitePreview,
  joinByInviteCode,
  createInviteLink,

  // 共同频道
  getMutualChannels,
};
