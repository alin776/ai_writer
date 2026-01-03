import { useState, useEffect } from 'react';
import { X, Search, UserPlus, Check, Loader2, Copy } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { useToast } from '@/hooks/useToast';
import { getFriends, FriendshipResponse } from '@/services/friendApi';
import { inviteToChannel, getChannelMembers } from '@/services/channelApi';

interface InviteToChannelDialogProps {
  isOpen: boolean;
  onClose: () => void;
  channelId: string;
  channelName: string;
}

export function InviteToChannelDialog({
  isOpen,
  onClose,
  channelId,
  channelName,
}: InviteToChannelDialogProps) {
  const { showToast } = useToast();
  const [friends, setFriends] = useState<FriendshipResponse[]>([]);
  const [memberIds, setMemberIds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [invitingIds, setInvitingIds] = useState<Set<string>>(new Set());
  const [invitedIds, setInvitedIds] = useState<Set<string>>(new Set());
  const [copied, setCopied] = useState(false);

  // 生成邀请链接
  const inviteLink = `${window.location.origin}/channels?join=${channelId}`;

  const handleCopyLink = async () => {
    try {
      await navigator.clipboard.writeText(inviteLink);
      setCopied(true);
      showToast('success', '邀请链接已复制');
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      showToast('error', '复制失败，请手动复制');
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen, channelId]);

  const loadData = async () => {
    try {
      setLoading(true);
      // 并行加载好友列表和频道成员
      const [friendsRes, membersRes] = await Promise.all([
        getFriends(),
        getChannelMembers(channelId),
      ]);
      setFriends(friendsRes.items || []);
      // 获取已在频道中的成员ID
      const existingMemberIds = new Set(membersRes.members.map((m: any) => m.id));
      setMemberIds(existingMemberIds);
    } catch (error) {
      console.error('加载数据失败:', error);
      showToast('error', '加载好友列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleInvite = async (friendId: string, friendName: string) => {
    try {
      setInvitingIds(prev => new Set(prev).add(friendId));
      await inviteToChannel(channelId, friendId);
      setInvitedIds(prev => new Set(prev).add(friendId));
      showToast('success', `已邀请 ${friendName} 加入频道`);
    } catch (error: any) {
      console.error('邀请失败:', error);
      const message = error?.response?.data?.detail || '邀请失败，请重试';
      showToast('error', message);
    } finally {
      setInvitingIds(prev => {
        const next = new Set(prev);
        next.delete(friendId);
        return next;
      });
    }
  };

  // 筛选好友：搜索 + 排除已在频道中的
  const filteredFriends = friends.filter(friendship => {
    const friend = friendship.friend;
    const matchSearch = !searchQuery ||
      friend.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (friend.fullName && friend.fullName.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchSearch;
  });

  // 分类：可邀请的和已在频道中的
  const invitableFriends = filteredFriends.filter(f => !memberIds.has(f.friend.id));
  const alreadyInChannel = filteredFriends.filter(f => memberIds.has(f.friend.id));

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* 遮罩 */}
      <div
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
      />

      {/* 对话框 - 固定高度 */}
      <div className="relative w-full max-w-md h-[520px] bg-white dark:bg-gray-800 rounded-xl shadow-xl overflow-hidden flex flex-col">
        {/* 头部 */}
        <div className="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <h3 className="text-base font-medium text-gray-900 dark:text-white">
            邀请好友至「{channelName}」
          </h3>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* 搜索框 */}
        <div className="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="搜索好友..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-sm bg-gray-100 dark:bg-gray-700 border-0 rounded-lg focus:ring-2 focus:ring-blue-500 text-gray-900 dark:text-white placeholder-gray-400"
            />
          </div>
        </div>

        {/* 好友列表 - 可滚动区域 */}
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="py-12 text-center text-gray-500">
              <Loader2 className="w-6 h-6 animate-spin mx-auto mb-2" />
              加载中...
            </div>
          ) : filteredFriends.length === 0 ? (
            <div className="py-12 text-center text-gray-500 dark:text-gray-400">
              {searchQuery ? '未找到匹配的好友' : '暂无好友'}
            </div>
          ) : (
            <>
              {/* 可邀请的好友 */}
              {invitableFriends.length > 0 && (
                <div className="p-2">
                  {invitableFriends.map((friendship) => (
                    <div
                      key={friendship.id}
                      className="flex items-center justify-between px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg"
                    >
                      <div className="flex items-center gap-3">
                        <Avatar className="w-10 h-10">
                          <AvatarImage src={friendship.friend.avatar} />
                          <AvatarFallback className="bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-white">
                            {friendship.friend.username[0]?.toUpperCase()}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <div className="text-sm font-medium text-gray-900 dark:text-white">
                            {friendship.friend.fullName || friendship.friend.username}
                          </div>
                          {friendship.friend.fullName && (
                            <div className="text-xs text-gray-500 dark:text-gray-400">
                              @{friendship.friend.username}
                            </div>
                          )}
                        </div>
                      </div>
                      <button
                        onClick={() => handleInvite(friendship.friend.id, friendship.friend.fullName || friendship.friend.username)}
                        disabled={invitingIds.has(friendship.friend.id) || invitedIds.has(friendship.friend.id)}
                        className={`flex items-center gap-1.5 px-4 py-1.5 text-sm font-medium rounded transition-colors ${
                          invitedIds.has(friendship.friend.id)
                            ? 'border border-gray-300 dark:border-gray-600 text-gray-400 dark:text-gray-500 cursor-default'
                            : invitingIds.has(friendship.friend.id)
                            ? 'border border-gray-300 dark:border-gray-600 text-gray-400 dark:text-gray-500 cursor-not-allowed'
                            : 'bg-gray-900 dark:bg-gray-100 hover:bg-gray-800 dark:hover:bg-white text-white dark:text-gray-900'
                        }`}
                      >
                        {invitedIds.has(friendship.friend.id) ? (
                          '已发送'
                        ) : invitingIds.has(friendship.friend.id) ? (
                          <>
                            <Loader2 className="w-4 h-4 animate-spin" />
                            邀请中
                          </>
                        ) : (
                          '邀请'
                        )}
                      </button>
                    </div>
                  ))}
                </div>
              )}

              {/* 已在频道中的好友 */}
              {alreadyInChannel.length > 0 && (
                <div className="p-2 border-t border-gray-200 dark:border-gray-700">
                  <div className="px-3 py-1.5 text-xs text-gray-500 dark:text-gray-400">
                    已在频道中
                  </div>
                  {alreadyInChannel.map((friendship) => (
                    <div
                      key={friendship.id}
                      className="flex items-center justify-between px-3 py-2 opacity-60"
                    >
                      <div className="flex items-center gap-3">
                        <Avatar className="w-10 h-10">
                          <AvatarImage src={friendship.friend.avatar} />
                          <AvatarFallback className="bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-white">
                            {friendship.friend.username[0]?.toUpperCase()}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <div className="text-sm font-medium text-gray-900 dark:text-white">
                            {friendship.friend.fullName || friendship.friend.username}
                          </div>
                          {friendship.friend.fullName && (
                            <div className="text-xs text-gray-500 dark:text-gray-400">
                              @{friendship.friend.username}
                            </div>
                          )}
                        </div>
                      </div>
                      <span className="text-xs text-gray-400 dark:text-gray-500">
                        已加入
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>

        {/* 邀请链接区域 - 固定在底部 */}
        <div className="flex-shrink-0 px-4 py-4 border-t border-gray-200 dark:border-gray-700">
          <div className="text-sm text-gray-500 dark:text-gray-400 mb-2">
            或者，向好友发送频道邀请链接
          </div>
          <div className="flex items-center gap-2">
            <input
              type="text"
              readOnly
              value={inviteLink}
              className="flex-1 px-3 py-2 text-sm bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 select-all"
              onClick={(e) => (e.target as HTMLInputElement).select()}
            />
            <button
              onClick={handleCopyLink}
              className={`px-4 py-2 text-sm font-medium rounded transition-colors flex items-center gap-1.5 ${
                copied
                  ? 'bg-green-500 text-white'
                  : 'bg-[#5865F2] hover:bg-[#4752C4] text-white'
              }`}
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4" />
                  已复制
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  复制
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
