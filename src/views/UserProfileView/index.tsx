import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MoreHorizontal, Heart, BookOpen } from 'lucide-react';
import { getUserProfile, UserProfile } from '@/services/userApi';
import { sendFriendRequest, handleFriendRequest } from '@/services/friendApi';
import { useAuthStore } from '@/store/authStore';
import { useWorkNavStore } from '@/store/workNavStore';
import { useToast } from '@/hooks/useToast';
import { ImageWithFallback } from '@/components/library/ImageWithFallback';

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
  const { showToast } = useToast();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    if (userId) {
      loadProfile(userId);
    }
  }, [userId]);

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

  // 渲染操作按钮
  const renderActionButton = () => {
    if (!profile) return null;
    const { relation } = profile;

    // 自己
    if (relation.isSelf) {
      return (
        <button
          onClick={() => navigate('/settings')}
          className="px-6 py-2 rounded-full border border-gray-300 dark:border-gray-600 text-sm hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
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
          className="px-6 py-2 rounded-full border border-gray-300 dark:border-gray-600 text-sm hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
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
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
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
                    <button className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                      <MoreHorizontal className="w-5 h-5" />
                    </button>
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
                  <span><span className="font-medium text-gray-700 dark:text-gray-200">{formatNumber(stats.totalFavorites)}</span> 获赞与收藏</span>
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
    </div>
  );
};

export default UserProfileView;
