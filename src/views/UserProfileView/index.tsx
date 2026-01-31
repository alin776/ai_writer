import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MoreHorizontal, Heart, BookOpen, Flag, User, Ban } from 'lucide-react';
import { getUserProfile, UserProfile } from '@/services/userApi';
import { sendFriendRequest, handleFriendRequest, reportUser } from '@/services/friendApi';
import { getMyChannels, type Channel, inviteToChannel } from '@/services/channelApi';
import { useAuthStore } from '@/store/authStore';
import { useWorkNavStore } from '@/store/workNavStore';
import { useToast } from '@/hooks/useToast';
import { ImageWithFallback } from '@/components/library/ImageWithFallback';
import { ToastContainer } from '@/components/ui/Toast';
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
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { ReportUserDialog } from '@/views/ChannelsView/components/ReportUserDialog';

// 数字格式化
const formatNumber = (num: number): string => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万';
  }
  return num.toLocaleString();
};

const UserProfileView = () => {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const { user: currentUser } = useAuthStore();
  const { showToast, messages, close } = useToast();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [showReportDialog, setShowReportDialog] = useState(false);
  const [myChannels, setMyChannels] = useState<Channel[]>([]);
  const [showFriendRequiredDialog, setShowFriendRequiredDialog] = useState(false);

  useEffect(() => {
    if (userId) {
      loadProfile(userId);
    }
  }, [userId]);

  // 获取我创建/管理的频道（用于邀请功能）
  useEffect(() => {
    const fetchChannels = async () => {
      try {
        const response = await getMyChannels();
        // 筛选出非私聊、非官方频道
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

  const loadProfile = async (id: string) => {
    try {
      setLoading(true);
      const data = await getUserProfile(id);
      setProfile(data);
    } catch (error) {
      console.error('加载用户主页失败:', error);
      showToast('error', '加载用户主页失败');
    } finally {
      setLoading(false);
    }
  };

  // 添加好友
  const handleAddFriend = async () => {
    if (!userId) return;
    try {
      setActionLoading(true);
      await sendFriendRequest(userId);
      showToast('success', '好友请求已发送');
      // 刷新页面数据
      await loadProfile(userId);
    } catch (error: any) {
      showToast('error', error.message || '发送好友请求失败');
    } finally {
      setActionLoading(false);
    }
  };

  // 同意好友请求
  const handleAcceptRequest = async () => {
    if (!profile?.relation.pendingRequest?.id) return;
    try {
      setActionLoading(true);
      await handleFriendRequest(profile.relation.pendingRequest.id, 'accept');
      showToast('success', '已添加好友');
      // 刷新页面数据
      if (userId) await loadProfile(userId);
    } catch (error: any) {
      showToast('error', error.message || '操作失败');
    } finally {
      setActionLoading(false);
    }
  };

  // 邀请至频道
  const handleInviteToChannel = async (channelId: string, channelName: string) => {
    if (!userId || !profile) return;

    // 检查是否是好友
    if (!profile.relation.isFriend) {
      setShowFriendRequiredDialog(true);
      return;
    }

    try {
      const result = await inviteToChannel(channelId, userId);
      if (result.alreadyMember) {
        showToast('info', `${profile?.user.fullName || profile?.user.username} 已是 ${channelName} 的成员`);
      } else if (result.inviteSent) {
        showToast('success', `已向 ${profile?.user.fullName || profile?.user.username} 发送 ${channelName} 的邀请`);
      } else {
        // 默认成功提示
        showToast('success', result.message || '邀请已发送');
      }
    } catch (error: any) {
      console.error('邀请失败:', error);
      showToast('error', error?.message || '邀请失败');
    }
  };

  // 渲染操作按钮
  const renderActionButton = () => {
    if (!profile) return null;
    const { relation } = profile;

    // 自己
    if (relation.isSelf) {
      return (
        <button
          onClick={() => navigate('/settings')}
          className="px-6 py-2.5 rounded-full bg-[#5865f2] hover:bg-[#4752c4] text-white text-sm font-medium transition-colors"
        >
          编辑资料
        </button>
      );
    }

    // 好友
    if (relation.isFriend) {
      return (
        <button
          onClick={() => navigate(`/channels?channelId=${relation.privateChannelId}`)}
          className="px-6 py-2.5 rounded-full bg-[#5865f2] hover:bg-[#4752c4] text-white text-sm font-medium transition-colors"
        >
          发消息
        </button>
      );
    }

    // 已发请求
    if (relation.pendingRequest?.direction === 'sent') {
      return (
        <button
          disabled
          className="px-6 py-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400 text-sm cursor-not-allowed"
        >
          等待确认
        </button>
      );
    }

    // 收到请求
    if (relation.pendingRequest?.direction === 'received') {
      return (
        <button
          onClick={handleAcceptRequest}
          disabled={actionLoading}
          className="px-6 py-2 rounded-full bg-red-500 text-white text-sm hover:bg-red-600 transition-colors disabled:opacity-50"
        >
          {actionLoading ? '处理中...' : '同意'}
        </button>
      );
    }

    // 陌生人
    return (
      <button
        onClick={handleAddFriend}
        disabled={actionLoading}
        className="px-6 py-2 rounded-full bg-red-500 text-white text-sm hover:bg-red-600 transition-colors disabled:opacity-50"
      >
        {actionLoading ? '发送中...' : '添加好友'}
      </button>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <p className="text-gray-500 dark:text-gray-400">用户不存在</p>
        <button
          onClick={() => navigate(-1)}
          className="mt-4 text-blue-500 hover:underline"
        >
          返回
        </button>
      </div>
    );
  }

  const { user, stats, relation, works } = profile;

  return (
    <div className="h-full w-full bg-white dark:bg-gray-900 text-gray-900 dark:text-white overflow-auto">
      <div className="max-w-4xl mx-auto px-4">
        {/* 用户信息区 */}
        <section className="py-8">
          <div className="flex flex-col items-center">
            {/* 头像+信息行 */}
            <div className="flex flex-row gap-6 sm:gap-8 items-start">
              {/* 头像 */}
              <div className="flex-shrink-0">
                <div className="w-28 h-28 sm:w-36 sm:h-36 rounded-full overflow-hidden border-2 border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800">
                  {user.avatar ? (
                    <img
                      src={user.avatar}
                      alt={user.fullName || user.username}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-3xl text-gray-400">
                      {(user.fullName || user.username)?.[0]?.toUpperCase()}
                    </div>
                  )}
                </div>
              </div>

              {/* 用户信息 */}
              <div className="min-w-0 text-left">
                {/* 昵称行 */}
                <div className="flex flex-row items-center gap-3 sm:gap-4 mb-2">
                  <h1 className="text-xl sm:text-2xl font-bold truncate">
                    {user.fullName || user.username}
                  </h1>
                  <div className="flex gap-2">
                    {renderActionButton()}
                    {/* 更多选项 - 非自己才显示 */}
                    {!relation.isSelf && (
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <button className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                            <MoreHorizontal className="w-5 h-5" />
                          </button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" className="w-[200px] !bg-white dark:!bg-[#18191c] !border-gray-200 dark:!border-transparent p-1.5" style={{ boxShadow: '0 8px 16px rgba(0, 0, 0, 0.15)' }}>
                          {/* 查看主要个人资料 */}
                          <DropdownMenuItem className="flex flex-col items-start text-gray-700 dark:text-[#b9bbbe] hover:text-gray-900 dark:hover:text-white focus:text-gray-900 dark:focus:text-white focus:bg-gray-100 dark:focus:bg-[#4752c4] rounded-sm">
                            <span>查看主要个人资料</span>
                            <span className="text-xs text-gray-500 dark:text-gray-400">也就是 {user.fullName || user.username}</span>
                          </DropdownMenuItem>

                          {/* 邀请至频道 - 有子菜单 */}
                          {myChannels.length > 0 && (
                            <DropdownMenuSub>
                              <DropdownMenuSubTrigger className="text-gray-700 dark:text-[#b9bbbe] hover:text-gray-900 dark:hover:text-white focus:text-gray-900 dark:focus:text-white focus:bg-gray-100 dark:focus:bg-[#4752c4] rounded-sm">
                                邀请至频道
                              </DropdownMenuSubTrigger>
                              <DropdownMenuSubContent className="w-[200px] max-h-[300px] overflow-y-auto !bg-white dark:!bg-[#18191c] !border-gray-200 dark:!border-transparent p-1.5" style={{ boxShadow: '0 8px 16px rgba(0, 0, 0, 0.15)' }}>
                                {myChannels.map((channel) => (
                                  <DropdownMenuItem
                                    key={channel.id}
                                    onSelect={() => handleInviteToChannel(channel.id, channel.name)}
                                    className="text-gray-700 dark:text-[#b9bbbe] hover:text-gray-900 dark:hover:text-white focus:text-gray-900 dark:focus:text-white focus:bg-gray-100 dark:focus:bg-[#4752c4] rounded-sm"
                                  >
                                    <span className="truncate">{channel.name}</span>
                                  </DropdownMenuItem>
                                ))}
                              </DropdownMenuSubContent>
                            </DropdownMenuSub>
                          )}

                          <DropdownMenuSeparator className="bg-gray-200 dark:bg-[#36393f] my-1.5" />

                          {/* 屏蔽 - 红色 */}
                          <DropdownMenuItem className="text-red-500 dark:text-[#ed4245] hover:!text-white focus:!text-white hover:!bg-red-500 focus:!bg-red-500 dark:hover:!bg-[#ed4245] dark:focus:!bg-[#ed4245] rounded-sm">
                            <Ban className="w-4 h-4 mr-2" />
                            屏蔽
                          </DropdownMenuItem>

                          {/* 举报用户个人资料 - 红色 */}
                          <DropdownMenuItem
                            onSelect={() => setShowReportDialog(true)}
                            className="text-red-500 dark:text-[#ed4245] hover:!text-white focus:!text-white hover:!bg-red-500 focus:!bg-red-500 dark:hover:!bg-[#ed4245] dark:focus:!bg-[#ed4245] rounded-sm"
                          >
                            <Flag className="w-4 h-4 mr-2" />
                            举报用户个人资料
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    )}
                  </div>
                </div>

                {/* 个人简介 */}
                {user.bio && (
                  <p className="text-gray-600 dark:text-gray-300 whitespace-pre-line mb-3 line-clamp-3">
                    {user.bio}
                  </p>
                )}

                {/* 统计数据 */}
                <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mb-3">
                  <span><span className="font-medium text-gray-700 dark:text-gray-200">{stats.workCount}</span> 作品</span>
                  <span><span className="font-medium text-gray-700 dark:text-gray-200">{formatNumber(stats.totalWords)}</span> 总字数</span>
                  <span><span className="font-medium text-gray-700 dark:text-gray-200">{formatNumber(stats.totalFavorites)}</span> 收藏</span>
                </div>

                {/* 称号 */}
                {user.honor && (
                  <span className="inline-block px-3 py-1 text-xs bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 rounded-full">
                    {user.honor}
                  </span>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* 作品网格 */}
        <div className="py-6">
          {works.length > 0 ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {works.map((work) => (
                <div
                  key={work.id}
                  onClick={() => {
                    useWorkNavStore.getState().setNovelSquareReadingState(work.id, false);
                    navigate('/library/novel-square');
                  }}
                  className="cursor-pointer group"
                >
                  {/* 封面 */}
                  <div className="rounded-lg overflow-hidden bg-gray-100 dark:bg-gray-800 mb-2">
                    <ImageWithFallback
                      src={work.coverImage || '/default-cover.jpg'}
                      alt={work.title}
                      className="w-full"
                      style={{ height: '200px', objectFit: 'cover', objectPosition: 'center' }}
                    />
                  </div>

                  {/* 作品信息 */}
                  <h3 className="text-sm font-medium truncate mb-1 group-hover:text-gray-600 dark:group-hover:text-gray-300 transition-colors">
                    {work.title}
                  </h3>
                  <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
                    <Heart className="w-3 h-3 mr-1" />
                    <span>{formatNumber(work.favoriteCount)}</span>
                    <span className="mx-2">·</span>
                    <span>{formatNumber(work.totalWords)}字</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="py-20 text-center text-gray-500 dark:text-gray-400">
              <BookOpen className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p>暂无作品</p>
            </div>
          )}
        </div>
      </div>

      {/* 举报用户对话框 */}
      {userId && profile && (
        <ReportUserDialog
          isOpen={showReportDialog}
          onClose={() => setShowReportDialog(false)}
          userId={userId}
          userName={profile.user.fullName || profile.user.username}
        />
      )}

      {/* 需要先添加好友的提示弹窗 */}
      <Dialog open={showFriendRequiredDialog} onOpenChange={setShowFriendRequiredDialog}>
        <DialogContent className="sm:max-w-[400px] !bg-white dark:!bg-[#2b2d31] !border-gray-200 dark:!border-transparent">
          <DialogHeader>
            <DialogTitle className="text-gray-900 dark:text-white">无法邀请</DialogTitle>
            <DialogDescription className="text-gray-600 dark:text-[#b5bac1]">
              你需要先添加 <span className="font-medium text-gray-900 dark:text-white">{profile?.user.fullName || profile?.user.username}</span> 为好友，才能邀请对方加入频道。
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="gap-2 sm:gap-0">
            <Button
              variant="ghost"
              onClick={() => setShowFriendRequiredDialog(false)}
              className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              取消
            </Button>
            <Button
              onClick={() => {
                setShowFriendRequiredDialog(false);
                handleAddFriend();
              }}
              className="bg-[#5865f2] hover:bg-[#4752c4] text-white"
            >
              添加好友
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Toast 通知容器 */}
      <ToastContainer messages={messages} onClose={close} />
    </div>
  );
};

export default UserProfileView;
