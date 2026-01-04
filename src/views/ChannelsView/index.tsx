import { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ChannelList, type Channel } from './components/ChannelList';
import { ChatArea, type Message } from './components/ChatArea';
import { CreateFangroupDialog } from './components/CreateFangroupDialog';
import { InviteToChannelDialog } from './components/InviteToChannelDialog';
import PinnedMessagesBar from './components/PinnedMessagesBar';
import { cn } from '@/lib/utils';
import {
  getMyChannels,
  getAvailableChannels,
  joinChannel,
  leaveChannel,
  getChannelMessages,
  getMessagesAround,
  sendMessage as apiSendMessage,
  sendMessageWithAttachments as apiSendMessageWithAttachments,
  getChannelMembers,
  type Channel as ApiChannel,
  type ChannelMessage,
  type ReactionSummary,
  type MessageAttachment
} from '@/services/channelApi';
import { useToast } from '@/hooks/useToast';
import { useAuthStore } from '@/store/authStore';
import type { ChannelMessage as WsChannelMessage, ReactionEvent } from '@/hooks/useChannelWebSocket';

// 转换 API Channel 到组件 Channel 格式
const convertApiChannelToChannel = (apiChannel: ApiChannel): Channel => {
  return {
    id: apiChannel.id,
    name: apiChannel.name,
    type: apiChannel.type,
    status: apiChannel.status,
    creatorId: apiChannel.creatorId,
    description: apiChannel.description,
    bookTitle: apiChannel.bookTitle,
    author: apiChannel.author,
    collectCount: apiChannel.collectCount,
    isPermanent: apiChannel.isPermanent,
    warningDays: apiChannel.warningDays,
    coverImage: apiChannel.coverImage,
    lastMessageAt: apiChannel.lastMessageAt,
    isMuted: apiChannel.isMuted,  // 静音状态
  };
};

// 转换 API ChannelMessage 到组件 Message 格式
const convertApiMessageToMessage = (apiMessage: ChannelMessage): Message => {
  // 转换附件数据（ApiAdapter 已经转换为 camelCase）
  const attachments: MessageAttachment[] = apiMessage.attachments?.map((att: any) => ({
    id: att.id,
    fileName: att.fileName,
    fileType: att.fileType,
    fileSize: att.fileSize,
    fileUrl: att.fileUrl,
    thumbnailUrl: att.thumbnailUrl,
  })) || [];

  // 转换转发来源信息（ApiAdapter 已经转换为 camelCase）
  const forwardedFrom = apiMessage.forwardedFrom ? {
    messageId: apiMessage.forwardedFrom.messageId,
    channelId: apiMessage.forwardedFrom.channelId,
    channelName: apiMessage.forwardedFrom.channelName,
    userId: apiMessage.forwardedFrom.userId,
    userName: apiMessage.forwardedFrom.userName,
    userAvatar: apiMessage.forwardedFrom.userAvatar,
    content: apiMessage.forwardedFrom.content,
    createdAt: apiMessage.forwardedFrom.createdAt,
    attachments: apiMessage.forwardedFrom.attachments?.map((att: any) => ({
      id: att.id,
      fileName: att.fileName,
      fileType: att.fileType,
      fileUrl: att.fileUrl,
      thumbnailUrl: att.thumbnailUrl,
    })),
  } : undefined;

  return {
    id: apiMessage.id,
    userId: apiMessage.userId || '',
    userName: apiMessage.userName || '已删除用户',
    userAvatar: apiMessage.userAvatar,
    userBio: apiMessage.userBio,
    userTitle: apiMessage.userTitle,
    userTitleColor: apiMessage.userTitleColor,
    userOnlineStatus: apiMessage.userOnlineStatus,
    content: apiMessage.content,
    timestamp: new Date(apiMessage.createdAt),
    type: apiMessage.type,
    isPinned: apiMessage.isPinned || false,
    isEdited: apiMessage.isEdited || false,
    editedAt: apiMessage.editedAt ? new Date(apiMessage.editedAt) : undefined,
    forwardedFrom,
    attachments: attachments.length > 0 ? attachments : undefined,
  };
};

const ChannelsView: React.FC = () => {
  const { showToast } = useToast();
  const { user } = useAuthStore();
  const [searchParams, setSearchParams] = useSearchParams();
  const [activeChannelId, setActiveChannelId] = useState<string>('');
  const [channelMessages, setChannelMessages] = useState<{ [key: string]: Message[] }>({});
  const [userChannels, setUserChannels] = useState<Channel[]>([]);
  const [availableChannels, setAvailableChannels] = useState<Channel[]>([]);
  const [pendingChannelIds, setPendingChannelIds] = useState<Set<string>>(new Set());  // 已申请待审核的频道
  const [loading, setLoading] = useState(true);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showInviteDialog, setShowInviteDialog] = useState(false);
  const [joinResultDialog, setJoinResultDialog] = useState<{
    isOpen: boolean;
    type: 'success' | 'pending' | 'error';
    channelName?: string;
    message: string;
  }>({ isOpen: false, type: 'success', message: '' });
  const [userRole, setUserRole] = useState<'owner' | 'admin' | 'member'>('member');
  const [pinRefreshTrigger, setPinRefreshTrigger] = useState(0);
  const [scrollToMessageId, setScrollToMessageId] = useState<string | null>(null);
  const [pendingScrollToMessageId, setPendingScrollToMessageId] = useState<string | null>(null); // 切换频道后需要滚动到的消息
  const [isChannelListCollapsed, setIsChannelListCollapsed] = useState(false);
  const [initialChannelIdFromUrl, setInitialChannelIdFromUrl] = useState<string | null>(null);

  const activeChannel = userChannels.find(c => c.id === activeChannelId);

  // localStorage key for persisting active channel
  const LAST_CHANNEL_KEY = 'lastActiveChannelId';

  // 包装函数：切换频道时同时保存到 localStorage
  const handleChannelSelect = useCallback((channelId: string) => {
    setActiveChannelId(channelId);
    if (channelId) {
      localStorage.setItem(LAST_CHANNEL_KEY, channelId);
    } else {
      localStorage.removeItem(LAST_CHANNEL_KEY);
    }
  }, []);

  // 注意：URL 参数 (channelId, join) 直接在 loadChannels 中处理
  // 这里只处理页内导航的 channelId 参数（非初始加载）
  useEffect(() => {
    // 只在非初始加载时处理 channelId 参数
    if (!loading && userChannels.length > 0) {
      const channelIdFromUrl = searchParams.get('channelId');
      if (channelIdFromUrl) {
        setInitialChannelIdFromUrl(channelIdFromUrl);
        setSearchParams({}, { replace: true });
      }
    }
  }, [searchParams, loading, userChannels.length]);

  // 当用户频道加载完成后，处理初始频道 ID（页内导航）
  useEffect(() => {
    if (initialChannelIdFromUrl && userChannels.length > 0 && !loading) {
      const targetChannel = userChannels.find(c => c.id === initialChannelIdFromUrl);
      if (targetChannel) {
        setActiveChannelId(initialChannelIdFromUrl);
        setInitialChannelIdFromUrl(null);  // 清除，避免重复设置
      } else {
        // 频道不在列表中（可能是新创建的私聊频道），重新加载频道列表
        const reloadAndSwitch = async () => {
          try {
            const response = await getMyChannels();
            const channels = response.channels.map(convertApiChannelToChannel);
            setUserChannels(channels);

            // 再次检查目标频道是否存在
            const targetChannel = channels.find(c => c.id === initialChannelIdFromUrl);
            if (targetChannel) {
              setActiveChannelId(initialChannelIdFromUrl);
            }
          } catch (error) {
            console.error('重新加载频道失败:', error);
          }
          setInitialChannelIdFromUrl(null);
        };
        reloadAndSwitch();
      }
    }
  }, [initialChannelIdFromUrl, userChannels, loading]);

  const currentUser = {
    id: user?.id || 'current-user',
    name: user?.username || '我',
    isCreator: activeChannel?.creatorId === user?.id,
    role: userRole,
  };

  // 加载用户在当前频道的角色
  useEffect(() => {
    const loadUserRole = async () => {
      if (!activeChannelId || !user?.id) {
        setUserRole('member');
        return;
      }

      try {
        const response = await getChannelMembers(activeChannelId);
        const currentMember = response.members.find(m => m.userId === user.id);
        const role = currentMember?.role as 'owner' | 'admin' | 'member' || 'member';
        setUserRole(role);

        // 更新频道列表中的 currentUserRole，用于 ChannelList 判断编辑权限
        setUserChannels(prev => prev.map(ch =>
          ch.id === activeChannelId ? { ...ch, currentUserRole: role } : ch
        ));
      } catch (error) {
        console.error('加载用户角色失败:', error);
        setUserRole('member');
      }
    };

    loadUserRole();
  }, [activeChannelId, user?.id]);

  // 置顶变化回调
  const handlePinChange = useCallback(() => {
    setPinRefreshTrigger(prev => prev + 1);
    // 刷新消息列表以更新置顶状态
    if (activeChannelId) {
      const loadMessages = async () => {
        try {
          const response = await getChannelMessages(activeChannelId, { skip: 0, limit: 50 });
          const messages = response.messages.map(convertApiMessageToMessage);
          const messagesWithReply = messages.map(msg => {
            const apiMsg = response.messages.find(m => m.id === msg.id);
            if (apiMsg?.replyToId) {
              const replyToMsg = messages.find(m => m.id === apiMsg.replyToId);
              if (replyToMsg) {
                return {
                  ...msg,
                  isPinned: apiMsg.isPinned,
                  replyTo: {
                    id: replyToMsg.id,
                    userName: replyToMsg.userName,
                    content: replyToMsg.content,
                  },
                };
              }
            }
            return { ...msg, isPinned: apiMsg?.isPinned };
          });
          setChannelMessages(prev => ({
            ...prev,
            [activeChannelId]: messagesWithReply,
          }));
        } catch (error) {
          console.error('刷新消息失败:', error);
        }
      };
      loadMessages();
    }
  }, [activeChannelId]);

  // 点击置顶消息跳转
  const handlePinnedMessageClick = useCallback((messageId: string) => {
    // 使用一个新的值来触发跳转，即使是同一个消息也能重新触发
    setScrollToMessageId(null);
    setTimeout(() => setScrollToMessageId(messageId), 0);
  }, []);

  // 跳转到原始消息（转发消息来源）
  const handleNavigateToOriginalMessage = useCallback((channelId: string, messageId: string) => {
    if (channelId === activeChannelId) {
      // 同一频道，直接滚动到消息
      setScrollToMessageId(null);
      setTimeout(() => setScrollToMessageId(messageId), 0);
    } else {
      // 不同频道，检查是否已加入
      const targetChannel = userChannels.find(c => c.id === channelId);
      if (targetChannel) {
        // 已加入，切换频道并设置待滚动消息ID
        setPendingScrollToMessageId(messageId);
        setActiveChannelId(channelId);
      } else {
        // 未加入该频道
        showToast('warning', '您还未加入原消息所在的频道');
      }
    }
  }, [activeChannelId, userChannels, showToast]);

  // 加载指定消息及其附近的消息（用于跳转到历史消息）
  const handleLoadMessagesAround = useCallback(async (messageId: string): Promise<boolean> => {
    if (!activeChannelId) return false;

    try {
      console.log('[ChannelsView] 加载消息附近上下文:', messageId);
      const response = await getMessagesAround(activeChannelId, messageId, 50);

      // 先转换所有消息（不包含回复信息）
      const newMessages = response.messages.map(convertApiMessageToMessage);

      // 然后添加回复信息（与 loadMessages 逻辑一致）
      const newMessagesWithReply = newMessages.map(msg => {
        const apiMsg = response.messages.find(m => m.id === msg.id);
        if (apiMsg?.replyToId) {
          const replyToMsg = newMessages.find(m => m.id === apiMsg.replyToId);
          if (replyToMsg) {
            return {
              ...msg,
              replyTo: {
                id: replyToMsg.id,
                userName: replyToMsg.userName,
                content: replyToMsg.content,
              },
            };
          }
        }
        return msg;
      });

      // 更新消息列表（替换当前列表）
      setChannelMessages(prev => ({
        ...prev,
        [activeChannelId]: newMessagesWithReply
      }));

      console.log('[ChannelsView] 消息上下文加载成功，共', newMessagesWithReply.length, '条消息');
      return true;
    } catch (error) {
      console.error('[ChannelsView] 加载消息上下文失败:', error);
      showToast('error', '加载消息失败');
      return false;
    }
  }, [activeChannelId, showToast]);

  // 加载用户频道
  useEffect(() => {
    const loadChannels = async () => {
      try {
        setLoading(true);
        const response = await getMyChannels();
        console.log('[ChannelsView] 获取频道列表响应:', response);
        const channels = response.channels.map(convertApiChannelToChannel);
        console.log('[ChannelsView] 转换后的频道列表:', channels.map(c => ({ id: c.id, name: c.name, coverImage: c.coverImage })));
        setUserChannels(channels);

        // 直接从 URL 读取频道 ID（避免异步状态问题）
        const channelIdFromUrl = searchParams.get('channelId') || initialChannelIdFromUrl;
        const joinIdFromUrl = searchParams.get('join');

        // 优先处理 join 参数（邀请链接）
        if (joinIdFromUrl) {
          console.log('[ChannelsView] 检测到 join 参数:', joinIdFromUrl);
          // 检查是否已经在频道中
          const existingChannel = channels.find(c => c.id === joinIdFromUrl);
          if (existingChannel) {
            // 已经是成员，直接切换
            setActiveChannelId(joinIdFromUrl);
            setJoinResultDialog({
              isOpen: true,
              type: 'success',
              channelName: existingChannel.name,
              message: `您已经是「${existingChannel.name}」的成员`
            });
            setSearchParams({}, { replace: true });
          } else {
            // 需要加入频道
            try {
              const joinResult = await joinChannel(joinIdFromUrl);

              // 根据返回状态处理
              if (joinResult.status === 'joined') {
                // 真正加入成功，重新加载频道列表并切换
                const newResponse = await getMyChannels();
                const newChannels = newResponse.channels.map(convertApiChannelToChannel);
                setUserChannels(newChannels);
                setActiveChannelId(joinIdFromUrl);
                // 获取频道名称
                const joinedChannel = newChannels.find(c => c.id === joinIdFromUrl);
                setJoinResultDialog({
                  isOpen: true,
                  type: 'success',
                  channelName: joinedChannel?.name,
                  message: joinResult.message || '成功加入频道'
                });
              } else if (joinResult.status === 'pending') {
                // 申请已提交，等待审核
                // 从可加入频道列表中获取频道名称
                const targetChannel = availableChannels.find(c => c.id === joinIdFromUrl);
                setJoinResultDialog({
                  isOpen: true,
                  type: 'pending',
                  channelName: targetChannel?.name,
                  message: joinResult.message || '申请已提交，请等待管理员审核'
                });
                // 添加到待审核列表
                setPendingChannelIds(prev => new Set(prev).add(joinIdFromUrl));
                // 设置默认频道
                if (channels.length > 0) {
                  setActiveChannelId(channels[0].id);
                }
              } else {
                // 其他状态，设置默认频道
                if (channels.length > 0) {
                  setActiveChannelId(channels[0].id);
                }
              }
            } catch (joinError: unknown) {
              console.error('加入频道失败:', joinError);
              const errorMessage = joinError instanceof Error ? joinError.message : '加入频道失败';
              setJoinResultDialog({
                isOpen: true,
                type: 'error',
                message: errorMessage
              });
              // 加入失败，设置默认频道
              if (channels.length > 0) {
                setActiveChannelId(channels[0].id);
              }
            }
            setSearchParams({}, { replace: true });
          }
        } else if (channelIdFromUrl) {
          // 如果有 URL 参数指定的频道，优先使用它
          const targetChannel = channels.find(c => c.id === channelIdFromUrl);
          if (targetChannel) {
            setActiveChannelId(channelIdFromUrl);
            setInitialChannelIdFromUrl(null);
            // 清除 URL 参数
            setSearchParams({}, { replace: true });
          } else {
            // 目标频道不在列表中，设置默认频道
            console.log('[ChannelsView] 目标频道不在用户频道列表中:', channelIdFromUrl);
            if (channels.length > 0 && !activeChannelId) {
              setActiveChannelId(channels[0].id);
            }
          }
        } else {
          // 没有 URL 参数，尝试从 localStorage 恢复上次的频道
          const savedChannelId = localStorage.getItem('lastActiveChannelId');
          if (savedChannelId) {
            const savedChannel = channels.find(c => c.id === savedChannelId);
            if (savedChannel) {
              // 成功恢复上次的频道
              setActiveChannelId(savedChannelId);
            } else {
              // 保存的频道不存在（可能已退出），清除并使用默认
              localStorage.removeItem('lastActiveChannelId');
              if (channels.length > 0 && !activeChannelId) {
                setActiveChannelId(channels[0].id);
              }
            }
          } else {
            // 没有保存的频道，使用默认第一个
            if (channels.length > 0 && !activeChannelId) {
              setActiveChannelId(channels[0].id);
            }
          }
        }
      } catch (error) {
        console.error('加载频道失败:', error);
        showToast('error', '加载频道失败');
      } finally {
        setLoading(false);
      }
    };

    loadChannels();
  }, []);

  // 加载可加入的频道
  useEffect(() => {
    const loadAvailableChannels = async () => {
      try {
        const response = await getAvailableChannels({ skip: 0, limit: 20 });
        const channels = response.channels.map(convertApiChannelToChannel);
        setAvailableChannels(channels);
      } catch (error) {
        console.error('加载可加入频道失败:', error);
        showToast('error', '加载可加入频道失败');
      }
    };

    loadAvailableChannels();
  }, []);

  // 加载频道消息
  useEffect(() => {
    if (!activeChannelId) return;

    const loadMessages = async () => {
      try {
        const response = await getChannelMessages(activeChannelId, { skip: 0, limit: 50 });
        console.log('[DEBUG] 加载的消息:', response.messages); // 调试日志

        // 先转换所有消息（不包含回复信息）
        const messages = response.messages.map(convertApiMessageToMessage);

        // 然后添加回复信息
        const messagesWithReply = messages.map(msg => {
          const apiMsg = response.messages.find(m => m.id === msg.id);
          console.log('[DEBUG] 检查消息回复:', { msgId: msg.id, replyToId: apiMsg?.replyToId }); // 调试日志
          if (apiMsg?.replyToId) {
            const replyToMsg = messages.find(m => m.id === apiMsg.replyToId);
            console.log('[DEBUG] 找到被回复的消息:', replyToMsg); // 调试日志
            if (replyToMsg) {
              return {
                ...msg,
                replyTo: {
                  id: replyToMsg.id,
                  userName: replyToMsg.userName,
                  content: replyToMsg.content,
                },
              };
            }
          }
          return msg;
        });

        console.log('[DEBUG] 处理后的消息:', messagesWithReply); // 调试日志
        setChannelMessages(prev => ({
          ...prev,
          [activeChannelId]: messagesWithReply,
        }));

        // 检查是否有待滚动的消息（从转发消息跳转过来）
        if (pendingScrollToMessageId) {
          setTimeout(() => {
            setScrollToMessageId(pendingScrollToMessageId);
            setPendingScrollToMessageId(null);
          }, 100); // 延迟确保消息渲染完成
        }
      } catch (error) {
        console.error('加载消息失败:', error);
        showToast('error', '加载消息失败');
      }
    };

    // 如果该频道消息未加载过，则加载
    if (!channelMessages[activeChannelId]) {
      loadMessages();
    } else if (pendingScrollToMessageId) {
      // 消息已缓存，直接处理待滚动消息
      setTimeout(() => {
        setScrollToMessageId(pendingScrollToMessageId);
        setPendingScrollToMessageId(null);
      }, 100);
    }
  }, [activeChannelId, pendingScrollToMessageId]);

  const handleSendMessage = async (content: string, type: 'normal' | 'announcement' = 'normal', replyToId?: string) => {
    if (!activeChannelId) return;

    try {
      const apiMessage = await apiSendMessage(activeChannelId, content, type, replyToId);
      let newMessage = convertApiMessageToMessage(apiMessage);

      // 如果是回复消息，添加回复信息
      if (apiMessage.replyToId) {
        const currentMessages = channelMessages[activeChannelId] || [];
        const replyToMsg = currentMessages.find(m => m.id === apiMessage.replyToId);
        if (replyToMsg) {
          newMessage = {
            ...newMessage,
            replyTo: {
              id: replyToMsg.id,
              userName: replyToMsg.userName,
              content: replyToMsg.content,
            },
          };
        }
      }

      setChannelMessages(prev => ({
        ...prev,
        [activeChannelId]: [...(prev[activeChannelId] || []), newMessage],
      }));
    } catch (error) {
      console.error('发送消息失败:', error);
      showToast('error', '发送消息失败');
    }
  };

  // 发送带附件的消息
  const handleSendMessageWithAttachments = async (
    content: string,
    attachmentIds: string[],
    type: 'normal' | 'announcement' = 'normal',
    replyToId?: string
  ) => {
    if (!activeChannelId) return;

    try {
      const response = await apiSendMessageWithAttachments(
        activeChannelId,
        content,
        attachmentIds,
        type,
        replyToId
      );
      console.log('[DEBUG] sendMessageWithAttachments response:', response);

      // 转换附件数据（ApiAdapter 已经转换为 camelCase）
      const attachments: MessageAttachment[] = response.attachments?.map((att: any) => ({
        id: att.id,
        fileName: att.fileName,
        fileType: att.fileType,
        fileSize: att.fileSize,
        fileUrl: att.fileUrl,
        thumbnailUrl: att.thumbnailUrl,
      })) || [];

      const newMessage: Message = {
        id: response.id,
        userId: response.userId || '',
        userName: response.userName || '未知用户',
        userAvatar: response.userAvatar,
        userBio: response.userBio,
        userTitle: response.userTitle,
        userTitleColor: response.userTitleColor,
        userOnlineStatus: response.userOnlineStatus,
        content: response.content,
        timestamp: new Date(response.createdAt),
        type: response.type as 'normal' | 'announcement' | 'mention',
        isPinned: response.isPinned || false,
        isEdited: false,
        attachments,
      };

      // 如果是回复消息，添加回复信息
      if (response.replyToId) {
        const currentMessages = channelMessages[activeChannelId] || [];
        const replyToMsg = currentMessages.find(m => m.id === response.replyToId);
        if (replyToMsg) {
          newMessage.replyTo = {
            id: replyToMsg.id,
            userName: replyToMsg.userName,
            content: replyToMsg.content,
          };
        }
      }

      setChannelMessages(prev => ({
        ...prev,
        [activeChannelId]: [...(prev[activeChannelId] || []), newMessage],
      }));
    } catch (error) {
      console.error('发送消息失败:', error);
      showToast('error', '发送消息失败');
    }
  };

  // WebSocket 收到新消息
  const handleNewMessage = useCallback((wsMessage: WsChannelMessage) => {
    console.log('[DEBUG] WebSocket 收到新消息:', {
      messageId: wsMessage.id,
      channelId: wsMessage.channel_id,
      userId: wsMessage.user_id,
      content: wsMessage.content?.substring(0, 50),
      currentUserId: user?.id
    });

    // 跳过自己发送的消息（已经在 handleSendMessage 中本地添加了）
    // 注意：后端已经通过 exclude_user 排除了发送者，所以这个检查是备用的
    if (wsMessage.user_id === user?.id) {
      console.log('[DEBUG] 跳过自己发送的消息:', wsMessage.id);
      return;
    }

    // 转换附件数据（WebSocket 现在统一使用 camelCase）
    const attachments: MessageAttachment[] = wsMessage.attachments?.map((att) => ({
      id: att.id,
      fileName: att.fileName,
      fileType: att.fileType,
      fileSize: att.fileSize,
      fileUrl: att.fileUrl,
      thumbnailUrl: att.thumbnailUrl,
    })) || [];

    // 转换转发来源信息（WebSocket 使用 snake_case）
    const forwardedFrom = wsMessage.forwarded_from ? {
      messageId: wsMessage.forwarded_from.message_id,
      channelId: wsMessage.forwarded_from.channel_id,
      channelName: wsMessage.forwarded_from.channel_name,
      userId: wsMessage.forwarded_from.user_id,
      userName: wsMessage.forwarded_from.user_name,
      userAvatar: wsMessage.forwarded_from.user_avatar,
      content: wsMessage.forwarded_from.content,
      createdAt: wsMessage.forwarded_from.created_at,
      attachments: wsMessage.forwarded_from.attachments?.map((att: any) => ({
        id: att.id,
        fileName: att.file_name,
        fileType: att.file_type,
        fileUrl: att.file_url,
        thumbnailUrl: att.thumbnail_url,
      })),
    } : undefined;

    // 转换为组件格式
    const newMessage: Message = {
      id: wsMessage.id,
      userId: wsMessage.user_id,
      userName: wsMessage.user_name,
      userAvatar: wsMessage.user_avatar || undefined,
      userBio: wsMessage.user_bio || undefined,
      userTitle: wsMessage.user_title || undefined,
      userTitleColor: wsMessage.user_title_color || undefined,
      userOnlineStatus: wsMessage.user_online_status || undefined,
      content: wsMessage.content,
      timestamp: new Date(wsMessage.created_at),
      type: wsMessage.type as 'normal' | 'announcement' | 'mention',
      isPinned: wsMessage.is_pinned,
      isEdited: false,
      forwardedFrom,
      attachments: attachments.length > 0 ? attachments : undefined,
    };

    // 使用函数式更新，避免依赖 channelMessages
    setChannelMessages(prev => {
      // 检查是否已存在（防止重复）
      const existingMessages = prev[wsMessage.channel_id] || [];
      if (existingMessages.some(m => m.id === wsMessage.id)) {
        console.log('[DEBUG] 消息已存在，跳过:', wsMessage.id);
        return prev;
      }

      // 处理回复
      if (wsMessage.reply_to_id) {
        const replyToMsg = existingMessages.find(m => m.id === wsMessage.reply_to_id);
        if (replyToMsg) {
          newMessage.replyTo = {
            id: replyToMsg.id,
            userName: replyToMsg.userName,
            content: replyToMsg.content,
          };
        }
      }

      console.log('[DEBUG] 添加新消息到频道:', {
        channelId: wsMessage.channel_id,
        messageId: wsMessage.id,
        existingCount: existingMessages.length
      });

      return {
        ...prev,
        [wsMessage.channel_id]: [...existingMessages, newMessage],
      };
    });
  }, [user?.id]); // 添加 user?.id 依赖

  // WebSocket 收到消息删除
  const handleMessageDelete = useCallback((messageId: string) => {
    if (!activeChannelId) return;

    setChannelMessages(prev => ({
      ...prev,
      [activeChannelId]: (prev[activeChannelId] || []).filter(m => m.id !== messageId),
    }));
  }, [activeChannelId]);

  // WebSocket 收到消息编辑
  const handleMessageEdit = useCallback((event: { channel_id: string; message_id: string; content: string; edited_at: string; is_edited: boolean }) => {
    setChannelMessages(prev => ({
      ...prev,
      [event.channel_id]: (prev[event.channel_id] || []).map(msg => {
        if (msg.id === event.message_id) {
          return {
            ...msg,
            content: event.content,
            isEdited: event.is_edited,
            editedAt: event.edited_at ? new Date(event.edited_at) : undefined,
          };
        }
        return msg;
      }),
    }));
  }, []);

  // WebSocket 收到反应添加
  const handleReactionAdd = useCallback((event: ReactionEvent) => {
    setChannelMessages(prev => {
      const channelMsgs = prev[activeChannelId] || [];
      return {
        ...prev,
        [activeChannelId]: channelMsgs.map(msg => {
          if (msg.id === event.message_id) {
            const reactions = msg.reactions || [];
            const existingIndex = reactions.findIndex(r => r.emoji === event.emoji);
            let newReactions: ReactionSummary[];
            if (existingIndex >= 0) {
              newReactions = reactions.map((r, i) => {
                if (i === existingIndex) {
                  return { ...r, count: r.count + 1 };
                }
                return r;
              });
            } else {
              newReactions = [...reactions, { emoji: event.emoji, count: 1, hasReacted: false }];
            }
            return { ...msg, reactions: newReactions };
          }
          return msg;
        }),
      };
    });
  }, [activeChannelId]);

  // WebSocket 收到反应移除
  const handleReactionRemove = useCallback((event: ReactionEvent) => {
    setChannelMessages(prev => {
      const channelMsgs = prev[activeChannelId] || [];
      return {
        ...prev,
        [activeChannelId]: channelMsgs.map(msg => {
          if (msg.id === event.message_id) {
            const reactions = (msg.reactions || [])
              .map(r => {
                if (r.emoji === event.emoji) {
                  return { ...r, count: r.count - 1 };
                }
                return r;
              })
              .filter(r => r.count > 0);
            return { ...msg, reactions };
          }
          return msg;
        }),
      };
    });
  }, [activeChannelId]);

  // 本地反应状态变化（用户自己添加/移除反应）
  const handleReactionsChange = useCallback((messageId: string, reactions: ReactionSummary[]) => {
    if (!activeChannelId) return;

    setChannelMessages(prev => ({
      ...prev,
      [activeChannelId]: (prev[activeChannelId] || []).map(msg => {
        if (msg.id === messageId) {
          return { ...msg, reactions };
        }
        return msg;
      }),
    }));
  }, [activeChannelId]);

  const handleJoinChannel = async (channelId: string) => {
    try {
      const result = await joinChannel(channelId);

      if (result.status === 'joined') {
        // 官方频道：直接加入成功
        const channelToJoin = availableChannels.find(c => c.id === channelId);
        if (channelToJoin) {
          setUserChannels(prev => [...prev, channelToJoin]);
          setAvailableChannels(prev => prev.filter(c => c.id !== channelId));
          handleChannelSelect(channelId);
        }
        showToast('success', '成功加入频道');
      } else {
        // 非官方频道：申请已提交，等待审核
        // 标记为已申请状态
        setPendingChannelIds(prev => new Set(prev).add(channelId));
        showToast('success', result.message || '申请已提交，请等待管理员审核');
      }
    } catch (error: any) {
      console.error('加入频道失败:', error);
      // 显示具体的错误信息
      const errorMsg = error?.response?.data?.detail || '加入频道失败';
      showToast('error', errorMsg);
    }
  };

  const handleCreateSuccess = async () => {
    // 重新加载频道列表
    try {
      const response = await getMyChannels();
      console.log('[ChannelsView] 创建成功后重新获取频道列表:', response);
      const channels = response.channels.map(convertApiChannelToChannel);
      console.log('[ChannelsView] 创建成功后转换的频道:', channels.map(c => ({ id: c.id, name: c.name, type: c.type, coverImage: c.coverImage })));
      setUserChannels(channels);

      // 同时刷新可加入频道列表（编辑后信息需要同步）
      const availableResponse = await getAvailableChannels({ skip: 0, limit: 20 });
      const availableList = availableResponse.channels.map(convertApiChannelToChannel);
      setAvailableChannels(availableList);

      // 选中新创建的频道（假设是列表第一个粉丝群）
      const newFangroup = channels.find(c => c.type === 'fangroup');
      if (newFangroup) {
        handleChannelSelect(newFangroup.id);
      }
    } catch (error) {
      console.error('重新加载频道失败:', error);
    }
  };

  // 刷新可加入频道列表
  const handleRefreshAvailable = async () => {
    try {
      const response = await getAvailableChannels({ skip: 0, limit: 20 });
      const channels = response.channels.map(convertApiChannelToChannel);
      setAvailableChannels(channels);
    } catch (error) {
      console.error('刷新可加入频道失败:', error);
    }
  };

  const handleLeaveChannel = async () => {
    if (!activeChannelId || !activeChannel) return;

    try {
      const result = await leaveChannel(activeChannelId);

      // 从用户频道列表中移除
      setUserChannels(prev => prev.filter(c => c.id !== activeChannelId));

      // 清除该频道的消息
      setChannelMessages(prev => {
        const newMessages = { ...prev };
        delete newMessages[activeChannelId];
        return newMessages;
      });

      // 切换到其他频道或清空选中
      const remainingChannels = userChannels.filter(c => c.id !== activeChannelId);
      if (remainingChannels.length > 0) {
        handleChannelSelect(remainingChannels[0].id);
      } else {
        handleChannelSelect('');
      }

      // 显示提示
      if (result.disbanded) {
        showToast('success', '频道已解散');
      } else {
        showToast('success', '已退出频道');
      }
    } catch (error) {
      console.error('退出频道失败:', error);
      showToast('error', '退出频道失败');
    }
  };

  const messages = channelMessages[activeChannelId] || [];

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="text-base text-muted-foreground">加载中...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex bg-background overflow-hidden" style={{ padding: 0 }}>
      {/* 频道列表 - 带过渡动画 */}
      <div
        className={cn(
          "transition-all duration-300 ease-in-out overflow-hidden",
          isChannelListCollapsed ? "w-0" : "w-56"
        )}
      >
        <ChannelList
          channels={userChannels}
          activeChannelId={activeChannelId}
          onChannelSelect={handleChannelSelect}
          onJoinChannel={handleJoinChannel}
          availableChannels={availableChannels}
          pendingChannelIds={pendingChannelIds}
          onCreateFangroup={() => setShowCreateDialog(true)}
          isCollapsed={false}
          onToggleCollapse={() => setIsChannelListCollapsed(true)}
          currentUserId={user?.id}
          onChannelUpdate={handleCreateSuccess}
          onRefreshAvailable={handleRefreshAvailable}
        />
      </div>

      {/* 聊天区域 */}
      {activeChannel && (
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* 聊天主体 */}
          <ChatArea
            channel={activeChannel}
            messages={messages}
            currentUser={currentUser}
            onSendMessage={handleSendMessage}
            onSendMessageWithAttachments={handleSendMessageWithAttachments}
            onLeaveChannel={handleLeaveChannel}
            onInviteToChannel={() => setShowInviteDialog(true)}
            onNewMessage={handleNewMessage}
            onMessageDelete={handleMessageDelete}
            onMessageEdit={handleMessageEdit}
            onReactionAdd={handleReactionAdd}
            onReactionRemove={handleReactionRemove}
            onReactionsChange={handleReactionsChange}
            onPinChange={handlePinChange}
            onMuteChange={(isMuted) => {
              // 更新频道列表中的静音状态
              setUserChannels(prev => prev.map(c =>
                c.id === activeChannel.id ? { ...c, isMuted } : c
              ));
            }}
            scrollToMessageId={scrollToMessageId}
            isChannelListCollapsed={isChannelListCollapsed}
            onToggleChannelList={() => setIsChannelListCollapsed(!isChannelListCollapsed)}
            onNavigateToOriginalMessage={handleNavigateToOriginalMessage}
            onLoadMessagesAround={handleLoadMessagesAround}
            pinnedMessagesBar={
              <PinnedMessagesBar
                channelId={activeChannel.id}
                isAdmin={userRole === 'owner' || userRole === 'admin'}
                refreshTrigger={pinRefreshTrigger}
                onMessageClick={handlePinnedMessageClick}
              />
            }
          />
        </div>
      )}

      {/* 无频道提示 */}
      {!activeChannel && !loading && (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="text-base text-muted-foreground">请选择一个频道</div>
          </div>
        </div>
      )}

      {/* 创建粉丝群对话框 */}
      <CreateFangroupDialog
        isOpen={showCreateDialog}
        onClose={() => setShowCreateDialog(false)}
        onSuccess={handleCreateSuccess}
      />

      {/* 邀请好友至频道对话框 */}
      {activeChannel && (
        <InviteToChannelDialog
          isOpen={showInviteDialog}
          onClose={() => setShowInviteDialog(false)}
          channelId={activeChannel.id}
          channelName={activeChannel.name}
        />
      )}

      {/* 加入频道结果弹窗 */}
      {joinResultDialog.isOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-[#313338] rounded-lg p-6 max-w-sm w-full mx-4 shadow-xl">
            {/* 图标 */}
            <div className="flex justify-center mb-4">
              {joinResultDialog.type === 'success' && (
                <div className="w-16 h-16 rounded-full bg-[#23a55a]/20 flex items-center justify-center">
                  <svg className="w-8 h-8 text-[#23a55a]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              )}
              {joinResultDialog.type === 'pending' && (
                <div className="w-16 h-16 rounded-full bg-[#f0b232]/20 flex items-center justify-center">
                  <svg className="w-8 h-8 text-[#f0b232]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              )}
              {joinResultDialog.type === 'error' && (
                <div className="w-16 h-16 rounded-full bg-[#f23f43]/20 flex items-center justify-center">
                  <svg className="w-8 h-8 text-[#f23f43]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>
              )}
            </div>

            {/* 标题 */}
            <h3 className="text-lg font-semibold text-[#f2f3f5] text-center mb-2">
              {joinResultDialog.type === 'success' && '加入成功'}
              {joinResultDialog.type === 'pending' && '申请已提交'}
              {joinResultDialog.type === 'error' && '加入失败'}
            </h3>

            {/* 频道名称 */}
            {joinResultDialog.channelName && (
              <p className="text-[#b5bac1] text-center mb-2">
                {joinResultDialog.channelName}
              </p>
            )}

            {/* 消息 */}
            <p className="text-[#949ba4] text-sm text-center mb-6">
              {joinResultDialog.message}
            </p>

            {/* 按钮 */}
            <button
              onClick={() => setJoinResultDialog(prev => ({ ...prev, isOpen: false }))}
              className={cn(
                "w-full py-2.5 px-4 rounded-md text-white font-medium transition-colors",
                joinResultDialog.type === 'success' && "bg-[#5865f2] hover:bg-[#4752c4]",
                joinResultDialog.type === 'pending' && "bg-[#5865f2] hover:bg-[#4752c4]",
                joinResultDialog.type === 'error' && "bg-[#5865f2] hover:bg-[#4752c4]"
              )}
            >
              {joinResultDialog.type === 'success' ? '开始聊天' : '知道了'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChannelsView;
