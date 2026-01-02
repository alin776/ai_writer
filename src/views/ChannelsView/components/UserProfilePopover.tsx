import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserPlus, MoreVertical, Check, Clock, X, ChevronRight, User, UserX, Flag } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
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
import { getMyChannels, type Channel } from '@/services/channelApi';
import MiniEmojiPicker from './MiniEmojiPicker';
import ReportUserDialog from './ReportUserDialog';

export interface UserProfilePopoverProps {
  userId: string;
  userName: string;
  userAvatar?: string;
  userBio?: string;
  userTitle?: string;
  userTitleColor?: string;
  currentUserId: string;
  channelId?: string;
  channelType?: 'official' | 'fangroup' | 'work' | 'private';
  userRole?: 'owner' | 'admin' | 'member';
  position: { x: number; y: number };
  onClose: () => void;
  onStartPrivateChat?: (userId: string, message: string, privateChannelId: string) => void;
}

type FriendStatus = 'none' | 'friend' | 'request_sent' | 'request_received' | 'loading';

export function UserProfilePopover({
  userId,
  userName,
  userAvatar,
  userBio,
  userTitle,
  userTitleColor,
  currentUserId,
  channelType,
  userRole,
  position,
  onClose,
  onStartPrivateChat,
}: UserProfilePopoverProps) {
  const navigate = useNavigate();
  const popoverRef = useRef<HTMLDivElement>(null);
  const emojiButtonRef = useRef<HTMLButtonElement>(null);
  const [friendStatus, setFriendStatus] = useState<FriendStatus>('loading');
  const [friendshipData, setFriendshipData] = useState<FriendCheckResponse | null>(null);
  const [myChannels, setMyChannels] = useState<Channel[]>([]);
  const [mutualChannelCount, setMutualChannelCount] = useState(0);
  const [dmMessage, setDmMessage] = useState('');
  const [adjustedPosition, setAdjustedPosition] = useState(position);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [showReportDialog, setShowReportDialog] = useState(false);
  const [dmError, setDmError] = useState<string | null>(null); // 私信错误提示
  const showReportDialogRef = useRef(false);
  const ignoreClickOutsideRef = useRef(false);

  // 同步更新 ref
  useEffect(() => {
    showReportDialogRef.current = showReportDialog;
  }, [showReportDialog]);

  // 是否是自己
  const isSelf = userId === currentUserId;

  // 检查好友关系
  useEffect(() => {
    if (isSelf) {
      setFriendStatus('none');
      return;
    }

    const checkRelation = async () => {
      try {
        const result = await checkFriendship(userId);
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
  }, [userId, isSelf]);

  // 获取我创建/管理的频道（用于邀请功能）+ 计算共同频道数
  useEffect(() => {
    const fetchChannels = async () => {
      try {
        const response = await getMyChannels();
        // 筛选出非私聊、非官方频道（官方频道每个人都在，不需要邀请）
        const manageableChannels = response.channels.filter(
          ch => ch.type !== 'private' && ch.type !== 'official'
        );
        setMyChannels(manageableChannels);
        // 模拟共同频道数（实际应该从后端获取）
        // TODO: 后端需要提供获取两个用户共同频道的API
        setMutualChannelCount(Math.min(manageableChannels.length, 3));
      } catch (error) {
        console.error('获取频道列表失败:', error);
      }
    };

    fetchChannels();
  }, []);

  // 调整弹窗位置，防止超出屏幕
  useEffect(() => {
    if (popoverRef.current) {
      const rect = popoverRef.current.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      let newX = position.x;
      let newY = position.y;

      // 防止右侧超出
      if (position.x + rect.width > viewportWidth - 20) {
        newX = position.x - rect.width - 10;
      }

      // 防止底部超出
      if (position.y + rect.height > viewportHeight - 20) {
        newY = viewportHeight - rect.height - 20;
      }

      // 防止顶部超出
      if (newY < 20) {
        newY = 20;
      }

      // 防止左侧超出
      if (newX < 20) {
        newX = 20;
      }

      setAdjustedPosition({ x: newX, y: newY });
    }
  }, [position]);

  // 点击外部关闭
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      // 如果设置了忽略标志，跳过这次检测
      if (ignoreClickOutsideRef.current) {
        ignoreClickOutsideRef.current = false;
        return;
      }

      // 如果举报对话框打开，不关闭 popover（使用 ref 确保读取最新值）
      if (showReportDialogRef.current) return;

      // 检查是否点击在 DropdownMenu 内容上（通过 data-radix 属性识别）
      const target = e.target as HTMLElement;
      if (target.closest('[data-radix-menu-content]') || target.closest('[role="menu"]') || target.closest('[role="menuitem"]')) {
        return;
      }

      if (popoverRef.current && !popoverRef.current.contains(e.target as Node)) {
        onClose();
      }
    };

    // 延迟添加事件监听，防止立即触发关闭
    const timer = setTimeout(() => {
      document.addEventListener('mousedown', handleClickOutside);
    }, 100);

    return () => {
      clearTimeout(timer);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [onClose]);

  // ESC 关闭
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        // 如果举报对话框打开，先关闭对话框
        if (showReportDialog) {
          showReportDialogRef.current = false;
          setShowReportDialog(false);
          return;
        }
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [onClose, showReportDialog]);

  // 添加好友
  const handleAddFriend = async () => {
    if (isSubmitting || friendStatus !== 'none') return;

    setIsSubmitting(true);
    try {
      await sendFriendRequest(userId);
      setFriendStatus('request_sent');
    } catch (error) {
      console.error('发送好友请求失败:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  // 查看完整个人资料
  const handleViewProfile = () => {
    navigate(`/user/${userId}`);
    onClose();
  };

  // 发送私信
  const handleSendDM = () => {
    if (!dmMessage.trim()) return;

    // 清除之前的错误
    setDmError(null);

    // 检查好友关系状态
    if (friendStatus === 'loading') {
      setDmError('正在检查好友关系，请稍候...');
      return;
    }

    if (!friendshipData?.isFriend || !friendshipData?.privateChannelId) {
      setDmError('需要先添加对方为好友才能发送私信');
      return;
    }

    // 调用回调发送私信
    if (onStartPrivateChat) {
      onStartPrivateChat(userId, dmMessage.trim(), friendshipData.privateChannelId);
    } else {
      // 备用方案：直接导航到私聊频道（但消息不会发送）
      navigate(`/channels?channelId=${friendshipData.privateChannelId}`);
    }
    setDmMessage('');
    onClose();
  };

  // 邀请至频道
  const handleInviteToChannel = (channelId: string) => {
    // TODO: 实现邀请功能
    console.log('邀请用户到频道:', channelId);
    onClose();
  };

  // 获取添加好友按钮的图标和样式
  const getFriendButtonContent = () => {
    switch (friendStatus) {
      case 'loading':
        return { icon: <Clock className="w-4 h-4" />, className: 'bg-gray-500/60' };
      case 'friend':
        return { icon: <Check className="w-4 h-4" />, className: 'bg-[#3ba55c]' };
      case 'request_sent':
        return { icon: <Clock className="w-4 h-4" />, className: 'bg-[#faa61a]' };
      case 'request_received':
        return { icon: <UserPlus className="w-4 h-4" />, className: 'bg-[#5865f2]' };
      default:
        return { icon: <UserPlus className="w-4 h-4" />, className: 'bg-black/40 hover:bg-black/60' };
    }
  };

  const friendButtonContent = getFriendButtonContent();

  // 获取角色标签
  const getRoleLabel = () => {
    if (!userRole) return null;

    const roleConfig: Record<string, { label: string; color: string }> = {
      owner: { label: channelType === 'work' ? '作者' : '创建者', color: '#faa61a' },
      admin: { label: '管理员', color: '#747f8d' },
      member: { label: '成员', color: '#43b581' },
    };

    return roleConfig[userRole];
  };

  const roleInfo = getRoleLabel();

  return (
    <div
      ref={popoverRef}
      className="fixed z-50 w-[300px] !bg-white dark:!bg-[#232428] rounded-lg overflow-hidden"
      style={{
        left: adjustedPosition.x,
        top: adjustedPosition.y,
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
      }}
    >
      {/* 顶部背景横幅 - 使用精确的渐变色 */}
      <div
        className="h-[60px] relative"
        style={{ background: 'linear-gradient(135deg, #5865f2 0%, #3b83f6 100%)' }}
      >
        {/* 操作按钮 */}
        {!isSelf && (
          <div className="absolute top-2 right-2 flex gap-1.5">
            {/* 添加好友按钮 */}
            <button
              onClick={handleAddFriend}
              disabled={friendStatus === 'loading' || friendStatus === 'friend' || friendStatus === 'request_sent' || isSubmitting}
              className={cn(
                "w-8 h-8 rounded-full flex items-center justify-center text-white transition-colors",
                friendButtonContent.className,
                (friendStatus === 'friend' || friendStatus === 'request_sent') && "cursor-default"
              )}
              title={
                friendStatus === 'friend' ? '已是好友' :
                friendStatus === 'request_sent' ? '已发送请求' :
                friendStatus === 'request_received' ? '对方已发送请求' :
                '添加好友'
              }
            >
              {friendButtonContent.icon}
            </button>

            {/* 更多选项按钮 */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="w-8 h-8 rounded-full bg-black/40 hover:bg-black/60 flex items-center justify-center text-white transition-colors">
                  <MoreVertical className="w-4 h-4" />
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-[188px] !bg-white dark:!bg-[#18191c] !border-gray-200 dark:!border-transparent p-1.5" style={{ boxShadow: '0 8px 16px rgba(0, 0, 0, 0.15)' }}>
                <DropdownMenuItem onClick={handleViewProfile} className="text-gray-700 dark:text-[#b9bbbe] hover:text-gray-900 dark:hover:text-white focus:text-gray-900 dark:focus:text-white focus:bg-gray-100 dark:focus:bg-[#4752c4] rounded-sm">
                  查看完整个人资料
                </DropdownMenuItem>

                {myChannels.length > 0 && (
                  <DropdownMenuSub>
                    <DropdownMenuSubTrigger className="text-gray-700 dark:text-[#b9bbbe] hover:text-gray-900 dark:hover:text-white focus:text-gray-900 dark:focus:text-white focus:bg-gray-100 dark:focus:bg-[#4752c4] rounded-sm">
                      邀请至频道
                    </DropdownMenuSubTrigger>
                    <DropdownMenuSubContent className="w-[200px] max-h-[300px] overflow-y-auto !bg-white dark:!bg-[#18191c] !border-gray-200 dark:!border-transparent p-1.5" style={{ boxShadow: '0 8px 16px rgba(0, 0, 0, 0.15)' }}>
                      {myChannels.map((channel) => (
                        <DropdownMenuItem
                          key={channel.id}
                          onClick={() => handleInviteToChannel(channel.id)}
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
                  忽略
                </DropdownMenuItem>
                <DropdownMenuItem className="text-red-500 dark:text-[#ed4245] hover:!text-white focus:!text-white hover:!bg-red-500 focus:!bg-red-500 dark:hover:!bg-[#ed4245] dark:focus:!bg-[#ed4245] rounded-sm">
                  屏蔽
                </DropdownMenuItem>
                <DropdownMenuItem
                  onSelect={() => {
                    // 设置忽略标志，防止下拉菜单关闭时触发外部点击检测
                    ignoreClickOutsideRef.current = true;
                    // 更新 ref 和 state
                    showReportDialogRef.current = true;
                    setShowReportDialog(true);
                  }}
                  className="text-red-500 dark:text-[#ed4245] hover:!text-white focus:!text-white hover:!bg-red-500 focus:!bg-red-500 dark:hover:!bg-[#ed4245] dark:focus:!bg-[#ed4245] rounded-sm"
                >
                  举报用户个人资料
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        )}
      </div>

      {/* 用户信息区域 - padding: 48px 16px 16px */}
      <div className="px-4 pt-12 pb-4 relative">
        {/* 头像 - 80px, border 6px, position top -40px left 16px */}
        <div className="absolute -top-10 left-4">
          <div className="relative">
            <Avatar className="w-20 h-20 border-[6px] border-white dark:border-[#232428]">
              <AvatarImage src={userAvatar} />
              <AvatarFallback className="text-2xl bg-gray-200 dark:bg-[#36393f] text-gray-600 dark:text-white">
                {userName[0]}
              </AvatarFallback>
            </Avatar>
            {/* 在线状态指示器 - 16px, border 3px */}
            <div className="absolute bottom-1 right-1 w-4 h-4 rounded-full bg-[#3ba55c] border-[3px] border-white dark:border-[#232428]" />
          </div>
        </div>

        {/* 用户名和简介 - margin-bottom: 12px */}
        <div className="mb-3">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-0.5">{userName}</h3>
          {userBio && (
            <p className="text-sm text-gray-500 dark:text-[#b9bbbe] line-clamp-2" title={userBio}>
              {userBio.length > 50 ? userBio.slice(0, 50) + '...' : userBio}
            </p>
          )}
        </div>

        {/* 共同服务器信息 - font-size: 12px, color: #b9bbbe, margin-bottom: 12px */}
        {!isSelf && mutualChannelCount > 0 && (
          <div className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-[#b9bbbe] mb-3">
            <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
              <path d="M12 6c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm0 10c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z"/>
            </svg>
            <span>{mutualChannelCount} 个共同频道</span>
          </div>
        )}

        {/* 角色标签 - padding: 4px 8px, font-size: 12px, gap: 6px, margin-bottom: 16px */}
        {(userTitle || roleInfo) && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {userTitle && (
              <span
                className="inline-flex items-center gap-1 py-1 px-2 rounded text-xs"
                style={{
                  backgroundColor: userTitleColor ? `${userTitleColor}20` : '#292b2f',
                  color: userTitleColor || '#b9bbbe',
                }}
              >
                <span
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: userTitleColor || '#b9bbbe' }}
                />
                {userTitle}
              </span>
            )}
            {roleInfo && (
              <span
                className="inline-flex items-center gap-1 py-1 px-2 rounded text-xs"
                style={{
                  backgroundColor: `${roleInfo.color}20`,
                  color: roleInfo.color,
                }}
              >
                <span
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: roleInfo.color }}
                />
                {roleInfo.label}
              </span>
            )}
          </div>
        )}

        {/* 分隔线 - height: 1px, background: #36393f, margin: 12px 0 */}
        <div className="h-px bg-gray-200 dark:bg-[#36393f] my-3" />

        {/* 私信错误提示 */}
        {dmError && (
          <div className="text-xs text-red-500 dark:text-red-400 mb-2 px-1">
            {dmError}
          </div>
        )}

        {/* 私信输入框 - background: #40444b, border-radius: 8px, padding: 8px 12px */}
        {/* 在私聊频道中不显示，因为已经在私聊了 */}
        {!isSelf && channelType !== 'private' && (
          <div className="flex items-center bg-gray-100 dark:bg-[#40444b] rounded-lg py-2 px-3 gap-2">
            <input
              type="text"
              value={dmMessage}
              onChange={(e) => {
                setDmMessage(e.target.value);
                if (dmError) setDmError(null); // 输入时清除错误
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendDM();
                }
              }}
              placeholder={`私信 @${userName}`}
              className="flex-1 min-w-0 bg-transparent border-none outline-none text-sm text-gray-700 dark:text-[#dcddde] placeholder-gray-400 dark:placeholder-[#72767d]"
            />
            <button
              ref={emojiButtonRef}
              className="shrink-0 text-gray-500 dark:text-white/60 hover:text-gray-700 dark:hover:text-white transition-opacity"
              onClick={() => setShowEmojiPicker(!showEmojiPicker)}
            >
              <span className="text-lg leading-none">😊</span>
            </button>
          </div>
        )}

        {/* 自己的卡片显示查看资料按钮 */}
        {isSelf && (
          <Button
            onClick={handleViewProfile}
            variant="outline"
            className="w-full bg-[#4752c4] hover:bg-[#3c45a5] text-white border-none"
          >
            查看我的资料
          </Button>
        )}
      </div>

      {/* 表情选择器 - 在卡片右侧弹出，使用 fixed 定位 */}
      {showEmojiPicker && (
        <div
          className="fixed z-[60]"
          style={{
            left: adjustedPosition.x + 300 + 8, // 卡片x + 卡片宽度 + 间距
            top: adjustedPosition.y - 120, // 往上挪
          }}
        >
          <MiniEmojiPicker
            onSelect={(emoji) => {
              setDmMessage(prev => prev + emoji);
              setShowEmojiPicker(false);
            }}
            onClose={() => setShowEmojiPicker(false)}
          />
        </div>
      )}

      {/* 举报用户对话框 */}
      <ReportUserDialog
        isOpen={showReportDialog}
        onClose={() => {
          showReportDialogRef.current = false;
          setShowReportDialog(false);
        }}
        userId={userId}
        userName={userName}
      />
    </div>
  );
}

export default UserProfilePopover;
