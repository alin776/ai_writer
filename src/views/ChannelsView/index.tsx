import { useState, useEffect } from 'react';
import { ChannelList, type Channel } from './components/ChannelList';
import { ChatArea, type Message } from './components/ChatArea';
import { CreateFangroupDialog } from './components/CreateFangroupDialog';
import {
  getMyChannels,
  getAvailableChannels,
  joinChannel,
  leaveChannel,
  getChannelMessages,
  sendMessage as apiSendMessage,
  channelApi,
  type Channel as ApiChannel,
  type ChannelMessage
} from '@/services/channelApi';
import { useToast } from '@/hooks/useToast';
import { useAuthStore } from '@/store/authStore';

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
    currentUserRole: apiChannel.currentUserRole,
    joinRequirement: apiChannel.joinRequirement,
    canAccess: apiChannel.canAccess,
  };
};

// 转换 API ChannelMessage 到组件 Message 格式
const convertApiMessageToMessage = (apiMessage: ChannelMessage): Message => {
  return {
    id: apiMessage.id,
    userId: apiMessage.userId || '',
    userName: apiMessage.userName || '已删除用户',
    userAvatar: apiMessage.userAvatar,
    userHonor: apiMessage.userHonor,
    userTitle: apiMessage.userTitle,
    userTitleColor: apiMessage.userTitleColor,
    content: apiMessage.content,
    timestamp: new Date(apiMessage.createdAt),
    type: apiMessage.type,
  };
};

const ChannelsView: React.FC = () => {
  const { showToast } = useToast();
  const { user } = useAuthStore();
  const [activeChannelId, setActiveChannelId] = useState<string>('');
  const [channelMessages, setChannelMessages] = useState<{ [key: string]: Message[] }>({});
  const [userChannels, setUserChannels] = useState<Channel[]>([]);
  const [availableChannels, setAvailableChannels] = useState<Channel[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateDialog, setShowCreateDialog] = useState(false);

  const activeChannel = userChannels.find(c => c.id === activeChannelId);

  const currentUser = {
    id: user?.id || 'current-user',
    name: user?.username || '我',
    isCreator: activeChannel?.currentUserRole === 'owner',
  };

  // 加载用户频道
  useEffect(() => {
    const loadChannels = async () => {
      try {
        setLoading(true);
        const response = await getMyChannels();
        const channels = response.channels.map(convertApiChannelToChannel);
        setUserChannels(channels);

        // 设置默认选中第一个频道
        if (channels.length > 0 && !activeChannelId) {
          setActiveChannelId(channels[0].id);
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

    // 立即标记频道为已读（用户点击频道即表示开始阅读）
    channelApi.markChannelAsRead(activeChannelId).catch(err => {
      console.error('标记已读失败:', err);
    });

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
      } catch (error) {
        console.error('加载消息失败:', error);
        showToast('error', '加载消息失败');
      }
    };

    // 每次切换频道或重新进入时都重新加载消息
    loadMessages();

    // 定时刷新消息（每30秒）
    const interval = setInterval(loadMessages, 30000);

    return () => clearInterval(interval);
  }, [activeChannelId]);

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

  const handleJoinChannel = async (channelId: string) => {
    try {
      await joinChannel(channelId);

      // 从可加入列表移除
      const channelToJoin = availableChannels.find(c => c.id === channelId);
      if (channelToJoin) {
        setUserChannels(prev => [...prev, channelToJoin]);
        setAvailableChannels(prev => prev.filter(c => c.id !== channelId));
        setActiveChannelId(channelId);
        showToast('success', '成功加入频道');
      }
    } catch (error) {
      console.error('加入频道失败:', error);
      showToast('error', '加入频道失败');
    }
  };

  const handleCreateSuccess = async () => {
    // 重新加载频道列表
    try {
      const response = await getMyChannels();
      const channels = response.channels.map(convertApiChannelToChannel);
      setUserChannels(channels);

      // 选中新创建的频道（假设是列表第一个粉丝群）
      const newFangroup = channels.find(c => c.type === 'fangroup');
      if (newFangroup) {
        setActiveChannelId(newFangroup.id);
      }
    } catch (error) {
      console.error('重新加载频道失败:', error);
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
        setActiveChannelId(remainingChannels[0].id);
      } else {
        setActiveChannelId('');
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
      <div className="h-full flex items-center justify-center bg-white dark:bg-zinc-900">
        <div className="text-center">
          <div className="text-base text-gray-500 dark:text-gray-400">加载中...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex bg-white dark:bg-zinc-900 overflow-hidden" style={{ padding: 0 }}>
      {/* 频道列表 */}
      <ChannelList
        channels={userChannels}
        activeChannelId={activeChannelId}
        onChannelSelect={setActiveChannelId}
        onJoinChannel={handleJoinChannel}
        availableChannels={availableChannels}
        onCreateFangroup={() => setShowCreateDialog(true)}
      />

      {/* 聊天区域 */}
      {activeChannel && (
        <ChatArea
          channel={activeChannel}
          messages={messages}
          currentUser={currentUser}
          onSendMessage={handleSendMessage}
          onLeaveChannel={handleLeaveChannel}
        />
      )}

      {/* 无频道提示 */}
      {!activeChannel && !loading && (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="text-base text-gray-500 dark:text-gray-400">请选择一个频道</div>
          </div>
        </div>
      )}

      {/* 创建粉丝群对话框 */}
      <CreateFangroupDialog
        isOpen={showCreateDialog}
        onClose={() => setShowCreateDialog(false)}
        onSuccess={handleCreateSuccess}
      />
    </div>
  );
};

export default ChannelsView;
