import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserPlus, MoreVertical, Check, Clock, ChevronRight, ChevronDown, Flag } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';
import { checkFriendship, sendFriendRequest, type FriendCheckResponse } from '@/services/friendApi';
import { getMyChannels, getMutualChannels, type Channel, inviteToChannel } from '@/services/channelApi';
import type { ChannelMember } from '@/services/channelApi';
import { useAuthStore, type OnlineStatus } from '@/store/authStore';
import { useGlobalStore } from '@/store/globalStore';
import { useUserNotes } from '@/hooks/useUserNotes';
import ReportUserDialog from './ReportUserDialog';

// 在线状态颜色映射
const statusColors: Record<OnlineStatus, string> = {
  online: '#3ba55c',
  idle: '#f0b232',
  dnd: '#f23f43',
  offline: '#80848e',
};

interface PrivateChatUserPanelProps {
  user: ChannelMember;
  currentUserId: string;
  onClose: () => void;
}

type FriendStatus = 'none' | 'friend' | 'request_sent' | 'request_received' | 'loading';

export function PrivateChatUserPanel({
  user,
  currentUserId,
  onClose,
}: PrivateChatUserPanelProps) {
  const navigate = useNavigate();
  const { onlineStatus } = useAuthStore();
  const { success: showSuccess, error: showError, info: showInfo } = useGlobalStore();
  const { getNote, setNote, getDisplayName } = useUserNotes();

  const [friendStatus, setFriendStatus] = useState<FriendStatus>('loading');
  const [friendshipData, setFriendshipData] = useState<FriendCheckResponse | null>(null);
  const [myChannels, setMyChannels] = useState<Channel[]>([]);
  const [mutualChannels, setMutualChannels] = useState<Channel[]>([]);
  const [showMutualChannels, setShowMutualChannels] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showReportDialog, setShowReportDialog] = useState(false);
  const [noteInput, setNoteInput] = useState(''); // 备注输入框的本地状态

  // 是否是自己
  const isSelf = user.userId === currentUserId;

  // 原始用户名
  const originalName = user.fullName || user.username;

  // 显示名称（优先使用备注）
  const displayName = getDisplayName(user.userId, originalName);

  // 当前备注
  const currentNote = getNote(user.userId);

  // 初始化备注输入框
  useEffect(() => {
    setNoteInput(currentNote || '');
  }, [currentNote, user.userId]);

  // 保存用户备注
  const handleSaveNote = (value: string) => {
    setNoteInput(value);
    setNote(user.userId, value);
  };

  // 检查好友关系
  useEffect(() => {
    if (isSelf) {
      setFriendStatus('none');
      return;
    }

    const checkRelation = async () => {
      try {
        const result = await checkFriendship(user.userId);
        setFriendshipData(result);
        if (result.isFriend) {
          setFriendStatus('friend');
        } else if (result.pendingRequest) {
          setFriendStatus(result.pendingRequest.direction === 'sent' ? 'request_sent' : 'request_received');
        } else {
          setFriendStatus('none');
        }
      } catch (error) {
        console.error('检查好友关系失败:', error);
        setFriendStatus('none');
      }
    };

    checkRelation();
  }, [user.userId, isSelf]);

  // 获取我的频道（用于邀请功能）
  useEffect(() => {
    const fetchChannels = async () => {
      try {
        const response = await getMyChannels();
        const manageableChannels = response.channels.filter(
          ch => ch.type !== 'private' && ch.type !== 'official'
        );
        setMyChannels(manageableChannels);
      } catch (error) {
        console.error('获取频道列表失败:', error);
      }
    };

    fetchChannels();
  }, []);

  // 获取共同频道
  useEffect(() => {
    if (isSelf) return;

    const fetchMutualChannels = async () => {
      try {
        const response = await getMutualChannels(user.userId);
        setMutualChannels(response.channels || []);
      } catch (error) {
        console.error('获取共同频道失败:', error);
        // 如果 API 不存在，使用空数组
        setMutualChannels([]);
      }
    };

    fetchMutualChannels();
  }, [user.userId, isSelf]);

  // 添加好友
  const handleAddFriend = async () => {
    if (isSubmitting || friendStatus !== 'none') return;

    setIsSubmitting(true);
    try {
      await sendFriendRequest(user.userId);
      setFriendStatus('request_sent');
      showSuccess('好友请求已发送');
    } catch (error: any) {
      console.error('发送好友请求失败:', error);
      showError(error?.message || '发送好友请求失败');
    } finally {
      setIsSubmitting(false);
    }
  };

  // 查看完整个人资料
  const handleViewProfile = () => {
    navigate(`/user/${user.userId}`);
  };

  // 邀请至频道
  const handleInviteToChannel = async (channelId: string, channelName: string) => {
    if (friendStatus !== 'friend') {
      showError('需要先添加对方为好友才能邀请');
      return;
    }

    try {
      const result = await inviteToChannel(channelId, user.userId);
      if (result.alreadyMember) {
        showInfo(`${displayName} 已是 ${channelName} 的成员`);
      } else if (result.inviteSent) {
        showSuccess(`已向 ${displayName} 发送 ${channelName} 的邀请`);
      } else {
        showSuccess(result.message || '邀请已发送');
      }
    } catch (error: any) {
      console.error('邀请失败:', error);
      showError(error?.message || '邀请失败，请重试');
    }
  };

  // 获取添加好友按钮的图标和样式
  const getFriendButtonContent = () => {
    switch (friendStatus) {
      case 'loading':
        return { icon: <Clock className="w-4 h-4" />, className: 'bg-gray-500/60', title: '加载中...' };
      case 'friend':
        return { icon: <Check className="w-4 h-4" />, className: 'bg-[#3ba55c]', title: '已是好友' };
      case 'request_sent':
        return { icon: <Clock className="w-4 h-4" />, className: 'bg-[#faa61a]', title: '已发送请求' };
      case 'request_received':
        return { icon: <UserPlus className="w-4 h-4" />, className: 'bg-[#5865f2]', title: '对方已发送请求' };
      default:
        return { icon: <UserPlus className="w-4 h-4" />, className: 'bg-black/40 hover:bg-black/60', title: '添加好友' };
    }
  };

  const friendButtonContent = getFriendButtonContent();

  // 格式化加入时间
  const formatJoinDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  // 用户在线状态
  const userOnlineStatus = user.onlineStatus || 'offline';

  return (
    <div className="w-[280px] bg-white dark:bg-[#232428] flex flex-col h-full overflow-hidden border-l border-gray-200 dark:border-gray-700">
      {/* 顶部横幅区域 */}
      <div
        className="h-[100px] relative flex-shrink-0"
        style={{ background: 'linear-gradient(135deg, #f59e0b 0%, #f97316 100%)' }}
      >
        {/* 右上角操作按钮 */}
        {!isSelf && (
          <div className="absolute top-3 right-3 flex gap-2">
            {/* 添加好友按钮 */}
            <button
              onClick={handleAddFriend}
              disabled={friendStatus === 'loading' || friendStatus === 'friend' || friendStatus === 'request_sent' || isSubmitting}
              className={cn(
                "w-9 h-9 rounded-full flex items-center justify-center text-white transition-colors",
                friendButtonContent.className,
                (friendStatus === 'friend' || friendStatus === 'request_sent') && "cursor-default"
              )}
              title={friendButtonContent.title}
            >
              {friendButtonContent.icon}
            </button>

            {/* 更多选项按钮 */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="w-9 h-9 rounded-full bg-black/40 hover:bg-black/60 flex items-center justify-center text-white transition-colors">
                  <MoreVertical className="w-4 h-4" />
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-[188px] !bg-white dark:!bg-[#18191c] !border-gray-200 dark:!border-transparent p-1.5">
                <DropdownMenuItem
                  onClick={handleViewProfile}
                  className="text-gray-700 dark:text-[#b9bbbe] hover:text-gray-900 dark:hover:text-white focus:text-gray-900 dark:focus:text-white focus:bg-gray-100 dark:focus:bg-[#4752c4] rounded-sm"
                >
                  查看完整个人资料
                </DropdownMenuItem>

                {myChannels.length > 0 && (
                  <DropdownMenuSub>
                    <DropdownMenuSubTrigger className="text-gray-700 dark:text-[#b9bbbe] hover:text-gray-900 dark:hover:text-white focus:text-gray-900 dark:focus:text-white focus:bg-gray-100 dark:focus:bg-[#4752c4] rounded-sm">
                      邀请至频道
                    </DropdownMenuSubTrigger>
                    <DropdownMenuSubContent className="w-[200px] max-h-[300px] overflow-y-auto !bg-white dark:!bg-[#18191c] !border-gray-200 dark:!border-transparent p-1.5">
                      {myChannels.map((channel) => (
                        <DropdownMenuItem
                          key={channel.id}
                          onClick={() => handleInviteToChannel(channel.id, channel.name)}
                          className="text-gray-700 dark:text-[#b9bbbe] hover:text-gray-900 dark:hover:text-white focus:text-gray-900 dark:focus:text-white focus:bg-gray-100 dark:focus:bg-[#4752c4] rounded-sm"
                        >
                          <span className="truncate">{channel.name}</span>
                        </DropdownMenuItem>
                      ))}
                    </DropdownMenuSubContent>
                  </DropdownMenuSub>
                )}

                <DropdownMenuSeparator className="bg-gray-200 dark:bg-[#36393f] my-1.5" />

                <DropdownMenuItem className="text-gray-700 dark:text-[#b9bbbe] hover:text-gray-900 dark:hover:text-white focus:text-gray-900 dark:focus:text-white focus:bg-gray-100 dark:focus:bg-[#4752c4] rounded-sm">
                  屏蔽
                </DropdownMenuItem>
                <DropdownMenuItem
                  onClick={() => setShowReportDialog(true)}
                  className="text-red-500 dark:text-[#ed4245] hover:!text-white focus:!text-white hover:!bg-red-500 focus:!bg-red-500 dark:hover:!bg-[#ed4245] dark:focus:!bg-[#ed4245] rounded-sm"
                >
                  <Flag className="w-4 h-4 mr-2" />
                  举报用户
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        )}
      </div>

      {/* 用户信息区域 */}
      <div className="px-4 pt-14 pb-4 relative flex-shrink-0">
        {/* 头像 - 悬浮在横幅下方 */}
        <div className="absolute -top-12 left-4">
          <div className="relative">
            <Avatar className="w-[90px] h-[90px] border-[6px] border-white dark:border-[#232428]">
              <AvatarImage src={user.avatar} />
              <AvatarFallback className="text-3xl bg-gray-200 dark:bg-[#36393f] text-gray-600 dark:text-white">
                {displayName?.[0]?.toUpperCase() || 'U'}
              </AvatarFallback>
            </Avatar>
            {/* 在线状态指示器 */}
            <div
              className="absolute bottom-1 right-1 w-5 h-5 rounded-full border-[4px] border-white dark:border-[#232428]"
              style={{ backgroundColor: statusColors[userOnlineStatus] }}
            />
          </div>
        </div>

        {/* 用户名区域 */}
        <div className="mb-4">
          <div className="flex items-center gap-2">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white">
              {displayName}
            </h3>
            {/* 好友标识 */}
            {friendStatus === 'friend' && (
              <svg className="w-5 h-5 text-gray-500 dark:text-gray-400" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            )}
          </div>
          <p className="text-sm text-gray-500 dark:text-[#b9bbbe]">
            {originalName}
          </p>
        </div>

        {/* 添加备注输入框 */}
        {!isSelf && (
          <div className="mb-4">
            <input
              type="text"
              value={noteInput}
              onChange={(e) => handleSaveNote(e.target.value)}
              placeholder="添加备注（仅对您可见）"
              className="w-full px-3 py-2 text-sm bg-gray-100 dark:bg-[#1e1f22] border border-gray-200 dark:border-transparent rounded-md text-gray-700 dark:text-[#dcddde] placeholder-gray-400 dark:placeholder-[#72767d] focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-[#5865f2]"
            />
          </div>
        )}
      </div>

      {/* 可滚动内容区域 */}
      <div className="flex-1 overflow-y-auto">
        {/* 成员加入时间 */}
        <div className="px-4 py-3 border-t border-gray-200 dark:border-[#3f4147]">
          <h4 className="text-xs font-bold text-gray-500 dark:text-[#b9bbbe] uppercase mb-1">
            成员加入时间
          </h4>
          <p className="text-sm text-gray-700 dark:text-[#dcddde]">
            {user.joinedAt ? formatJoinDate(user.joinedAt) : '未知'}
          </p>
        </div>

        {/* 共同的频道 */}
        {!isSelf && (
          <div className="border-t border-gray-200 dark:border-[#3f4147]">
            <button
              onClick={() => setShowMutualChannels(!showMutualChannels)}
              className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-[#2b2d31] transition-colors"
            >
              <span className="text-sm text-gray-700 dark:text-[#dcddde]">
                共同的频道 — {mutualChannels.length}
              </span>
              {showMutualChannels ? (
                <ChevronDown className="w-5 h-5 text-gray-400 dark:text-[#b9bbbe]" />
              ) : (
                <ChevronRight className="w-5 h-5 text-gray-400 dark:text-[#b9bbbe]" />
              )}
            </button>

            {/* 共同频道列表 */}
            {showMutualChannels && mutualChannels.length > 0 && (
              <div className="px-4 pb-3 space-y-1">
                {mutualChannels.map((channel) => (
                  <div
                    key={channel.id}
                    className="flex items-center gap-3 px-2 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-[#35373c] cursor-pointer transition-colors"
                    onClick={() => {
                      navigate(`/channels?channelId=${channel.id}`);
                      onClose();
                    }}
                  >
                    <Avatar className="w-8 h-8">
                      <AvatarImage src={channel.coverImage} />
                      <AvatarFallback className="text-xs bg-gray-200 dark:bg-[#36393f] text-gray-600 dark:text-white">
                        {channel.name?.[0]?.toUpperCase() || '#'}
                      </AvatarFallback>
                    </Avatar>
                    <span className="text-sm text-gray-700 dark:text-[#dcddde] truncate">
                      {channel.name}
                    </span>
                  </div>
                ))}
              </div>
            )}

            {showMutualChannels && mutualChannels.length === 0 && (
              <div className="px-4 pb-3">
                <p className="text-sm text-gray-400 dark:text-[#72767d]">暂无共同频道</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 底部 - 查看完整个人资料 */}
      <div className="flex-shrink-0 px-4 py-3 border-t border-gray-200 dark:border-[#3f4147]">
        <button
          onClick={handleViewProfile}
          className="w-full text-center text-sm text-gray-500 dark:text-[#b9bbbe] hover:text-gray-700 dark:hover:text-white hover:underline transition-colors"
        >
          查看完整个人资料
        </button>
      </div>

      {/* 举报用户对话框 */}
      <ReportUserDialog
        isOpen={showReportDialog}
        onClose={() => setShowReportDialog(false)}
        userId={user.userId}
        userName={user.fullName || user.username}
      />
    </div>
  );
}

export default PrivateChatUserPanel;
