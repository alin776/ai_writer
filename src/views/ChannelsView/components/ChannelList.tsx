import { useState, useEffect, useRef, useCallback } from 'react';
import { Hash, Lock, Users, MessageCircle, BookOpen, Coffee, FlaskConical, ChevronDown, ChevronRight, Bell, Plus, X, Search, AtSign, Edit2, UserPlus, User, Inbox } from 'lucide-react';
import { cn } from '@/lib/utils';
import { channelApi, UnreadSummary } from '@/services/channelApi';
import friendApi, { FriendshipResponse, FriendRequest as FriendRequestType, UserSearchResult } from '@/services/friendApi';
import { EditFangroupDialog } from './EditFangroupDialog';
import { useToast } from '@/hooks/useToast';

export interface Channel {
  id: string;
  name: string;
  type: 'official' | 'fangroup' | 'work' | 'private';
  status?: 'active' | 'warning' | 'locked';
  creatorId?: string;
  unreadCount?: number;
  warningDays?: number;
  bookTitle?: string;
  author?: string;
  collectCount?: number;
  isPermanent?: boolean;
  isPinned?: boolean;
  description?: string;
  coverImage?: string;
  lastMessageAt?: string;  // 最后消息时间，用于排序
  currentUserRole?: 'owner' | 'admin' | 'member';  // 当前用户在频道中的角色
}

interface ChannelListProps {
  channels: Channel[];
  activeChannelId: string;
  onChannelSelect: (channelId: string) => void;
  onJoinChannel?: (channelId: string) => Promise<void> | void;
  availableChannels?: Channel[];
  pendingChannelIds?: Set<string>;  // 已申请待审核的频道ID
  onCreateFangroup?: () => void;
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
  currentUserId?: string;  // 当前用户ID，用于判断是否为粉丝群创建者
  onChannelUpdate?: () => void;  // 频道信息更新回调
  onRefreshAvailable?: () => void;  // 刷新可加入频道列表
}

export function ChannelList({ channels, activeChannelId, onChannelSelect, onJoinChannel, availableChannels, pendingChannelIds, onCreateFangroup, currentUserId, onChannelUpdate, onRefreshAvailable }: ChannelListProps) {
  const { showToast } = useToast();

  // 按最后消息时间降序排序频道
  const sortByLastMessage = (a: Channel, b: Channel) => {
    const timeA = a.lastMessageAt ? new Date(a.lastMessageAt).getTime() : 0;
    const timeB = b.lastMessageAt ? new Date(b.lastMessageAt).getTime() : 0;
    return timeB - timeA;  // 降序，最新的在前
  };

  // 按最后消息时间降序排序好友
  const sortFriendsByLastMessage = (a: FriendshipResponse, b: FriendshipResponse) => {
    const timeA = a.lastMessageAt ? new Date(a.lastMessageAt).getTime() : 0;
    const timeB = b.lastMessageAt ? new Date(b.lastMessageAt).getTime() : 0;
    return timeB - timeA;  // 降序，最新的在前
  };

  const [expandedSections, setExpandedSections] = useState({
    official: true,
    fangroup: true,
    work: true,
    friends: true,  // 新增：好友分组
  });
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');  // 发现频道弹窗搜索
  const [localSearchQuery, setLocalSearchQuery] = useState('');  // 本地频道过滤
  const [showPlusMenu, setShowPlusMenu] = useState(false);  // +按钮下拉菜单
  const [unreadData, setUnreadData] = useState<Map<string, { unreadCount: number; mentionCount: number }>>(new Map());
  const [editingChannel, setEditingChannel] = useState<Channel | null>(null);  // 正在编辑的频道
  const plusMenuRef = useRef<HTMLDivElement>(null);

  // 好友系统相关状态
  const [friends, setFriends] = useState<FriendshipResponse[]>([]);
  const [pendingRequestCount, setPendingRequestCount] = useState(0);
  const [showFriendRequests, setShowFriendRequests] = useState(false);
  const [friendRequests, setFriendRequests] = useState<FriendRequestType[]>([]);

  // 发现弹窗用户搜索相关状态
  const [searchTab, setSearchTab] = useState<'all' | 'users' | 'channels'>('all');
  const [searchUsers, setSearchUsers] = useState<UserSearchResult[]>([]);
  const [isSearchingUsers, setIsSearchingUsers] = useState(false);
  const [isListScrolled, setIsListScrolled] = useState(false); // 列表是否滚动

  // 获取未读数据
  useEffect(() => {
    const fetchUnreadData = async () => {
      try {
        const summary = await channelApi.getUnreadSummary();
        const map = new Map();
        summary.channels.forEach(ch => {
          map.set(ch.channelId, {
            unreadCount: ch.unreadCount,
            mentionCount: ch.mentionCount
          });
        });
        setUnreadData(map);
      } catch (error) {
        console.error('获取未读数据失败:', error);
      }
    };

    // 首次加载立即获取
    fetchUnreadData();

    // 当切换频道时，延迟刷新（等待 ChatArea 标记已读完成）
    const refreshTimer = setTimeout(fetchUnreadData, 800);

    // 每30秒刷新一次未读数据
    const interval = setInterval(fetchUnreadData, 30000);

    return () => {
      clearTimeout(refreshTimer);
      clearInterval(interval);
    };
  }, [activeChannelId]); // 当切换频道时也刷新未读数据

  // 加载好友数据
  useEffect(() => {
    const loadFriendData = async () => {
      try {
        const [friendsRes, countRes] = await Promise.all([
          friendApi.getFriends(),
          friendApi.getPendingCount()
        ]);
        setFriends(friendsRes.items);
        setPendingRequestCount(countRes.pendingCount);
      } catch (error) {
        console.error('加载好友数据失败:', error);
      }
    };

    loadFriendData();

    // 每30秒刷新待处理数量
    const interval = setInterval(async () => {
      try {
        const res = await friendApi.getPendingCount();
        setPendingRequestCount(res.pendingCount);
      } catch (error) {
        console.error('刷新好友请求数量失败:', error);
      }
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  // 打开好友请求弹窗时加载请求列表
  useEffect(() => {
    if (showFriendRequests) {
      friendApi.getReceivedRequests().then(res => {
        setFriendRequests(res.items);
      }).catch(error => {
        console.error('加载好友请求失败:', error);
      });
    }
  }, [showFriendRequests]);

  // 处理好友请求
  const handleAcceptRequest = async (requestId: string) => {
    try {
      const res = await friendApi.handleFriendRequest(requestId, 'accept');
      setFriendRequests(prev => prev.filter(r => r.id !== requestId));
      setPendingRequestCount(prev => Math.max(0, prev - 1));
      if ('friendship' in res) {
        setFriends(prev => [res.friendship, ...prev]);
      }
      showToast('success', '已添加好友');
    } catch (error: any) {
      showToast('error', error.message || '操作失败');
    }
  };

  const handleRejectRequest = async (requestId: string) => {
    try {
      await friendApi.handleFriendRequest(requestId, 'reject');
      setFriendRequests(prev => prev.filter(r => r.id !== requestId));
      setPendingRequestCount(prev => Math.max(0, prev - 1));
      showToast('success', '已拒绝请求');
    } catch (error: any) {
      showToast('error', error.message || '操作失败');
    }
  };

  // 获取头像首字母和颜色
  const getAvatarInitial = (name: string) => name.charAt(0).toUpperCase();
  const getAvatarBgColor = (name: string) => {
    const colors = [
      'bg-red-500', 'bg-orange-500', 'bg-amber-500', 'bg-yellow-500',
      'bg-lime-500', 'bg-green-500', 'bg-emerald-500', 'bg-teal-500',
      'bg-cyan-500', 'bg-sky-500', 'bg-blue-500', 'bg-indigo-500',
      'bg-violet-500', 'bg-purple-500', 'bg-fuchsia-500', 'bg-pink-500'
    ];
    return colors[name.charCodeAt(0) % colors.length];
  };

  // 搜索用户（带防抖）
  const searchUserDebounceRef = useRef<NodeJS.Timeout | null>(null);
  const handleSearchUsers = useCallback((keyword: string) => {
    if (searchUserDebounceRef.current) {
      clearTimeout(searchUserDebounceRef.current);
    }

    if (!keyword.trim()) {
      setSearchUsers([]);
      return;
    }

    searchUserDebounceRef.current = setTimeout(async () => {
      setIsSearchingUsers(true);
      try {
        const res = await friendApi.searchUsers(keyword);
        setSearchUsers(res.items);
      } catch (error) {
        console.error('搜索用户失败:', error);
      } finally {
        setIsSearchingUsers(false);
      }
    }, 300);
  }, []);

  // 发送好友请求
  const handleSendFriendRequest = async (userId: string) => {
    try {
      await friendApi.sendFriendRequest(userId);
      // 更新搜索结果中的状态
      setSearchUsers(prev => prev.map(u =>
        u.id === userId ? { ...u, relationStatus: 'request_sent' as const } : u
      ));
      showToast('success', '好友请求已发送');
    } catch (error: any) {
      showToast('error', error.message || '发送失败');
    }
  };

  // 点击外部关闭+菜单
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (plusMenuRef.current && !plusMenuRef.current.contains(event.target as Node)) {
        setShowPlusMenu(false);
      }
    };
    if (showPlusMenu) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showPlusMenu]);

  // 防抖刷新可加入频道
  const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);
  const debouncedRefreshAvailable = useCallback(() => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    debounceTimerRef.current = setTimeout(() => {
      onRefreshAvailable?.();
    }, 300);
  }, [onRefreshAvailable]);

  // 清理防抖定时器
  useEffect(() => {
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, []);

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const getChannelIcon = (channel: Channel) => {
    if (channel.type === 'official') {
      if (channel.name.includes('公共酒馆')) return MessageCircle;
      if (channel.name.includes('作者酒馆')) return BookOpen;
      if (channel.name.includes('读者茶馆')) return Coffee;
      if (channel.name.includes('官方实验室')) return FlaskConical;
      return Hash;
    }

    if (channel.type === 'fangroup') return Users;

    if (channel.status === 'locked') return Lock;
    return Hash;
  };

  // 本地搜索过滤
  const filterBySearch = (channelList: Channel[]) => {
    if (!localSearchQuery.trim()) return channelList;
    const query = localSearchQuery.toLowerCase();
    return channelList.filter(c =>
      c.name.toLowerCase().includes(query) ||
      c.bookTitle?.toLowerCase().includes(query) ||
      c.author?.toLowerCase().includes(query)
    );
  };

  // 好友搜索过滤
  const filterFriendsBySearch = (friendList: FriendshipResponse[]) => {
    if (!localSearchQuery.trim()) return friendList;
    const query = localSearchQuery.toLowerCase();
    return friendList.filter(f =>
      f.friend.username.toLowerCase().includes(query) ||
      f.friend.fullName?.toLowerCase().includes(query)
    );
  };

  const officialChannels = filterBySearch(channels.filter(c => c.type === 'official'));
  const fangroupChannels = filterBySearch(channels.filter(c => c.type === 'fangroup'));
  const workChannels = filterBySearch(channels.filter(c => c.type === 'work'));
  const filteredFriends = filterFriendsBySearch(friends);

  const ChannelItem = ({ channel, clearSearchOnSelect }: { channel: Channel; clearSearchOnSelect?: boolean }) => {
    const Icon = getChannelIcon(channel);
    const isActive = channel.id === activeChannelId;
    const channelUnreadData = unreadData.get(channel.id);
    // 粉丝群或作品频道的创建者可以编辑，官方频道的管理员也可以编辑
    const canEdit = (
      ((channel.type === 'fangroup' || channel.type === 'work') && channel.creatorId === currentUserId) ||
      (channel.type === 'official' && (channel.currentUserRole === 'owner' || channel.currentUserRole === 'admin'))
    );

    // 点击头像编辑（粉丝群或作品频道创建者）
    const handleAvatarClick = (e: React.MouseEvent) => {
      if (canEdit) {
        e.stopPropagation();  // 阻止选中频道
        setEditingChannel(channel);
      }
    };

    const handleChannelClick = () => {
      onChannelSelect(channel.id);
      // 如果是从搜索结果点击，清空搜索框
      if (clearSearchOnSelect) {
        setLocalSearchQuery('');
      }
    };

    return (
      <button
        onClick={handleChannelClick}
        className={cn(
          "w-full flex items-center gap-2 px-2 py-2 rounded-lg transition-colors group relative overflow-hidden",
          isActive ? "bg-gray-200 text-gray-900 dark:bg-zinc-700 dark:text-gray-100" : "hover:bg-gray-50 dark:hover:bg-zinc-800 text-gray-700 dark:text-gray-300"
        )}
      >
        {/* 频道图标/头像 - 创建者/管理员可点击编辑 */}
        {canEdit ? (
          <div
            onClick={handleAvatarClick}
            className="relative shrink-0 cursor-pointer group/avatar w-5 h-5"
            title={channel.type === 'official' ? "点击编辑官方频道" : channel.type === 'work' ? "点击编辑作品频道" : "点击编辑粉丝群"}
          >
            {channel.coverImage ? (
              <img
                src={channel.coverImage}
                alt={channel.name}
                className="w-5 h-5 aspect-square rounded-full object-cover group-hover/avatar:ring-2 group-hover/avatar:ring-blue-500 transition-all"
              />
            ) : (
              <div className="w-5 h-5 aspect-square rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center group-hover/avatar:ring-2 group-hover/avatar:ring-blue-500 transition-all">
                <Icon className="w-3 h-3 text-gray-500 dark:text-gray-400" />
              </div>
            )}
            {/* 编辑图标遮罩 */}
            <div className="absolute inset-0 rounded-full bg-black/50 opacity-0 group-hover/avatar:opacity-100 transition-opacity flex items-center justify-center">
              <Edit2 className="w-2.5 h-2.5 text-white" />
            </div>
          </div>
        ) : channel.coverImage ? (
          <img
            src={channel.coverImage}
            alt={channel.name}
            className="shrink-0 w-5 h-5 aspect-square rounded-full object-cover"
          />
        ) : (
          <Icon className="shrink-0 opacity-60 w-5 h-5" />
        )}
        <span className="flex-1 w-0 text-left truncate text-sm" title={channel.name}>{channel.name}</span>

        {/* @提醒标识 - 优先级最高 */}
        {channelUnreadData && channelUnreadData.mentionCount > 0 && (
          <div className="flex items-center gap-1 bg-red-500 text-white rounded-full px-2 py-0.5">
            <AtSign className="w-3 h-3" />
            <span className="text-xs">{channelUnreadData.mentionCount}</span>
          </div>
        )}

        {/* 未读消息数 */}
        {channelUnreadData && channelUnreadData.unreadCount > 0 && channelUnreadData.mentionCount === 0 && (
          <span className={cn(
            "text-xs rounded-full h-5 min-w-5 px-1.5 flex items-center justify-center",
            isActive ? "bg-white text-black" : "bg-black text-white dark:bg-zinc-600 dark:text-white"
          )}>
            {channelUnreadData.unreadCount > 99 ? '99+' : channelUnreadData.unreadCount}
          </span>
        )}

        {channel.status === 'warning' && (
          <div className="flex items-center gap-0.5">
            <Bell className="w-4 h-4 text-red-500" />
            <span className="text-xs text-red-500">{channel.warningDays}d</span>
          </div>
        )}

        {channel.status === 'locked' && (
          <span className="text-xs text-gray-400 dark:text-gray-500">已折叠</span>
        )}
      </button>
    );
  };

  const SectionHeader = ({
    title,
    section,
    count,
  }: {
    title: string;
    section: keyof typeof expandedSections;
    count: number;
  }) => {
    const isExpanded = expandedSections[section];

    return (
      <button
        onClick={() => toggleSection(section)}
        className="w-full flex items-center gap-1.5 px-2 py-2 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors group"
      >
        {isExpanded ? (
          <ChevronDown className="w-4 h-4 shrink-0 text-gray-400 dark:text-gray-500" />
        ) : (
          <ChevronRight className="w-4 h-4 shrink-0 text-gray-400 dark:text-gray-500" />
        )}
        <span className="flex-1 text-left text-gray-500 dark:text-gray-400 text-sm uppercase tracking-wide">{title}</span>
        <span className="text-xs text-gray-400 dark:text-gray-500">{count}</span>
      </button>
    );
  };

  const handleJoinChannel = async (channelId: string) => {
    if (onJoinChannel) {
      await onJoinChannel(channelId);
      // 官方频道直接加入后关闭弹窗/清空搜索，非官方频道（申请）保持状态显示"已申请"
      const channel = availableChannels?.find(c => c.id === channelId);
      if (channel?.type === 'official') {
        setShowJoinModal(false);
        setSearchQuery('');
        setLocalSearchQuery('');  // 同时清空本地搜索
      }
    }
  };

  // 搜索结果面板用的可加入频道过滤（使用 localSearchQuery）
  const filteredAvailableChannels = (availableChannels || []).filter(channel => {
    if (!localSearchQuery.trim()) return false;  // 只在有搜索词时显示
    const query = localSearchQuery.toLowerCase();
    return channel.name.toLowerCase().includes(query) ||
      channel.bookTitle?.toLowerCase().includes(query) ||
      channel.author?.toLowerCase().includes(query);
  }).sort(sortByLastMessage);  // 按最后消息时间排序

  // 弹窗用的可加入频道过滤（使用 searchQuery）
  const modalFilteredChannels = (availableChannels || []).filter(channel =>
    channel.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    channel.bookTitle?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    channel.author?.toLowerCase().includes(searchQuery.toLowerCase())
  ).sort(sortByLastMessage);  // 按最后消息时间排序

  return (
    <div className="border-r border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-900 flex flex-col h-full w-56 min-w-56">
      {/* 顶部搜索框和+按钮 */}
      <div className={cn(
        "p-2 border-b transition-colors",
        isListScrolled ? "border-gray-100 dark:border-gray-700" : "border-transparent"
      )}>
        <div className="flex items-center gap-1">
          <div className="flex-1 relative">
            <Search className="absolute left-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-400 dark:text-gray-500" />
            <input
              type="text"
              placeholder="搜索"
              value={localSearchQuery}
              onChange={(e) => {
                setLocalSearchQuery(e.target.value);
                // 输入时防抖刷新可加入频道列表
                if (e.target.value.trim()) {
                  debouncedRefreshAvailable();
                }
              }}
              className="w-full pl-7 pr-7 py-1.5 text-xs border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:border-gray-300 dark:focus:border-gray-500"
            />
            {/* 清除按钮 */}
            {localSearchQuery && (
              <button
                onClick={() => setLocalSearchQuery('')}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-0.5 hover:bg-gray-200 dark:hover:bg-gray-600 rounded"
              >
                <X className="w-3 h-3 text-gray-400 dark:text-gray-500" />
              </button>
            )}
          </div>
          <div className="relative" ref={plusMenuRef}>
            <button
              onClick={() => setShowPlusMenu(!showPlusMenu)}
              className="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              title="更多操作"
            >
              <Plus className="w-4 h-4 text-gray-500 dark:text-gray-400" />
            </button>
            {/* 下拉菜单 */}
            {showPlusMenu && (
              <div className="absolute right-0 top-full mt-1 w-32 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50 py-1">
                <button
                  onClick={() => {
                    setShowPlusMenu(false);
                    onCreateFangroup?.();
                  }}
                  className="w-full flex items-center gap-2 px-3 py-2 text-xs text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <Users className="w-4 h-4" />
                  <span>创建群聊</span>
                </button>
                <button
                  onClick={() => {
                    setShowPlusMenu(false);
                    onRefreshAvailable?.();
                    setShowJoinModal(true);
                  }}
                  className="w-full flex items-center gap-2 px-3 py-2 text-xs text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <UserPlus className="w-4 h-4" />
                  <span>加好友/群</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 搜索结果面板 或 频道列表 */}
      {localSearchQuery.trim() ? (
        <div
          className="flex-1 overflow-y-auto sidebar-scrollbar"
          onScroll={(e) => setIsListScrolled(e.currentTarget.scrollTop > 0)}
        >
          <div className="p-2">
            {/* 我的频道 */}
            {(officialChannels.length > 0 || fangroupChannels.length > 0 || workChannels.length > 0) && (
              <div className="mb-3">
                <div className="text-xs text-gray-500 dark:text-gray-400 px-2 py-1 font-medium">我的频道</div>
                <div className="space-y-0.5">
                  {[...officialChannels, ...fangroupChannels, ...workChannels].sort(sortByLastMessage).map(channel => (
                    <ChannelItem key={channel.id} channel={channel} clearSearchOnSelect />
                  ))}
                </div>
              </div>
            )}

            {/* 我的好友 */}
            {filteredFriends.length > 0 && (
              <div className="mb-3">
                <div className="text-xs text-gray-500 dark:text-gray-400 px-2 py-1 font-medium">我的好友</div>
                <div className="space-y-0.5">
                  {filteredFriends.sort(sortFriendsByLastMessage).map(item => {
                    const displayName = item.friend.fullName || item.friend.username;
                    const isActive = item.privateChannelId === activeChannelId;
                    return (
                      <button
                        key={item.id}
                        onClick={() => {
                          if (item.privateChannelId) {
                            onChannelSelect(item.privateChannelId);
                            setLocalSearchQuery('');  // 清空搜索框
                          }
                        }}
                        className={cn(
                          "w-full flex items-center gap-2 px-2 py-2 rounded-lg transition-colors",
                          isActive
                            ? "bg-gray-200 text-gray-900 dark:bg-zinc-700 dark:text-gray-100"
                            : "hover:bg-gray-50 dark:hover:bg-zinc-800 text-gray-700 dark:text-gray-300"
                        )}
                      >
                        {item.friend.avatar ? (
                          <img
                            src={item.friend.avatar}
                            className="shrink-0 w-5 h-5 aspect-square rounded-full object-cover"
                          />
                        ) : (
                          <div className={cn(
                            "shrink-0 w-5 h-5 aspect-square rounded-full flex items-center justify-center text-white text-[10px] font-medium",
                            getAvatarBgColor(displayName)
                          )}>
                            {getAvatarInitial(displayName)}
                          </div>
                        )}
                        <span className="flex-1 w-0 text-left truncate text-sm">
                          {displayName}
                        </span>
                        {item.privateChannelId && unreadData.get(item.privateChannelId)?.unreadCount ? (
                          <span className="shrink-0 min-w-[18px] h-[18px] px-1 flex items-center justify-center text-[10px] font-medium bg-red-500 text-white rounded-full">
                            {unreadData.get(item.privateChannelId)!.unreadCount > 99 ? '99+' : unreadData.get(item.privateChannelId)!.unreadCount}
                          </span>
                        ) : null}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* 发现频道 */}
            {filteredAvailableChannels.length > 0 && (
              <div>
                <div className="text-xs text-gray-500 dark:text-gray-400 px-2 py-1 font-medium">发现频道</div>
                <div className="space-y-0.5">
                  {filteredAvailableChannels.map(channel => {
                    const Icon = getChannelIcon(channel);
                    return (
                      <div
                        key={channel.id}
                        className="flex items-center gap-2 px-2 py-2 rounded hover:bg-gray-50 dark:hover:bg-zinc-800 transition-colors"
                      >
                        {/* 频道图标 */}
                        {channel.coverImage ? (
                          <img
                            src={channel.coverImage}
                            alt={channel.name}
                            className="shrink-0 w-5 h-5 aspect-square rounded-full object-cover"
                          />
                        ) : (
                          <Icon className="shrink-0 opacity-60 w-5 h-5 text-gray-500 dark:text-gray-400" />
                        )}
                        {/* 频道名称 */}
                        <span className="flex-1 text-sm text-gray-700 dark:text-gray-300 truncate">{channel.name}</span>
                        {/* 申请/加入按钮 */}
                        <button
                          onClick={() => handleJoinChannel(channel.id)}
                          disabled={channel.status === 'locked' || pendingChannelIds?.has(channel.id)}
                          className={cn(
                            "px-2 py-1 text-xs rounded transition-colors",
                            pendingChannelIds?.has(channel.id)
                              ? "bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400"
                              : channel.status === 'locked'
                                ? "bg-gray-100 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed"
                                : "bg-blue-500 text-white hover:bg-blue-600"
                          )}
                        >
                          {pendingChannelIds?.has(channel.id) ? '已申请' : channel.type === 'official' ? '加入' : '申请'}
                        </button>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* 无结果 */}
            {officialChannels.length === 0 && fangroupChannels.length === 0 && workChannels.length === 0 && filteredFriends.length === 0 && filteredAvailableChannels.length === 0 && (
              <div className="text-center py-8 text-xs text-gray-400 dark:text-gray-500">
                未找到匹配的结果
              </div>
            )}
          </div>
        </div>
      ) : (
        <div
          className="flex-1 overflow-y-auto sidebar-scrollbar"
          onScroll={(e) => setIsListScrolled(e.currentTarget.scrollTop > 0)}
        >
          <div className="space-y-0.5 p-2">
            {/* 官方频道 */}
            <SectionHeader title="官方" section="official" count={channels.filter(c => c.type === 'official').length} />
            {expandedSections.official && (
              <div className="space-y-0.5 mb-2 ml-1">
                {channels.filter(c => c.type === 'official').sort(sortByLastMessage).map(channel => (
                  <ChannelItem key={channel.id} channel={channel} />
                ))}
              </div>
            )}

            {/* 好友请求条目 - 有未处理请求时显示 */}
            {pendingRequestCount > 0 && (
              <button
                onClick={() => setShowFriendRequests(true)}
                className="w-full flex items-center gap-2 px-2 py-2 hover:bg-gray-50 dark:hover:bg-zinc-800 rounded-lg transition-colors text-gray-700 dark:text-gray-300"
              >
                <div className="shrink-0 w-5 h-5 flex items-center justify-center">
                  <Users className="w-4 h-4 text-gray-500 dark:text-gray-400" />
                </div>
                <span className="flex-1 text-left text-sm">好友请求</span>
                <span className="px-1.5 py-0.5 text-xs bg-blue-500 text-white rounded-full min-w-[20px] text-center">
                  {pendingRequestCount}
                </span>
              </button>
            )}

            {/* 好友分组 */}
            {friends.length > 0 && (
              <>
                <button
                  onClick={() => setExpandedSections(prev => ({ ...prev, friends: !prev.friends }))}
                  className="w-full flex items-center gap-1.5 px-2 py-2 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors group"
                >
                  {expandedSections.friends ? (
                    <ChevronDown className="w-4 h-4 shrink-0 text-gray-400 dark:text-gray-500" />
                  ) : (
                    <ChevronRight className="w-4 h-4 shrink-0 text-gray-400 dark:text-gray-500" />
                  )}
                  <span className="flex-1 text-left text-gray-500 dark:text-gray-400 text-sm tracking-wide">好友</span>
                  <span className="text-xs text-gray-400 dark:text-gray-500">{friends.length}</span>
                </button>
                {expandedSections.friends && (
                  <div className="space-y-0.5 mb-2">
                    {[...friends].sort(sortFriendsByLastMessage).map(item => {
                      const displayName = item.friend.fullName || item.friend.username;
                      const isActive = item.privateChannelId === activeChannelId;
                      return (
                        <button
                          key={item.id}
                          onClick={() => item.privateChannelId && onChannelSelect(item.privateChannelId)}
                          className={cn(
                            "w-full flex items-center gap-2 px-2 py-2 rounded-lg transition-colors ml-1",
                            isActive
                              ? "bg-gray-200 text-gray-900 dark:bg-zinc-700 dark:text-gray-100"
                              : "hover:bg-gray-50 dark:hover:bg-zinc-800 text-gray-700 dark:text-gray-300"
                          )}
                        >
                          {item.friend.avatar ? (
                            <img
                              src={item.friend.avatar}
                              className="shrink-0 w-5 h-5 aspect-square rounded-full object-cover"
                            />
                          ) : (
                            <div className={cn(
                              "shrink-0 w-5 h-5 aspect-square rounded-full flex items-center justify-center text-white text-[10px] font-medium",
                              getAvatarBgColor(displayName)
                            )}>
                              {getAvatarInitial(displayName)}
                            </div>
                          )}
                          <span className="flex-1 w-0 text-left truncate text-sm">
                            {displayName}
                          </span>
                          {item.privateChannelId && unreadData.get(item.privateChannelId)?.unreadCount ? (
                            <span className="shrink-0 min-w-[18px] h-[18px] px-1 flex items-center justify-center text-[10px] font-medium bg-red-500 text-white rounded-full">
                              {unreadData.get(item.privateChannelId)!.unreadCount > 99 ? '99+' : unreadData.get(item.privateChannelId)!.unreadCount}
                            </span>
                          ) : null}
                        </button>
                      );
                    })}
                  </div>
                )}
              </>
            )}

            {/* 粉丝群 */}
            <SectionHeader title="私域" section="fangroup" count={channels.filter(c => c.type === 'fangroup').length} />
            {expandedSections.fangroup && (
              <div className="space-y-0.5 mb-2 ml-1">
                {channels.filter(c => c.type === 'fangroup').sort(sortByLastMessage).map(channel => (
                  <ChannelItem key={channel.id} channel={channel} />
                ))}
              </div>
            )}

            {/* 作品频道 */}
            <SectionHeader title="作品" section="work" count={channels.filter(c => c.type === 'work').length} />
            {expandedSections.work && (
              <div className="space-y-0.5 mb-2 ml-1">
                {channels.filter(c => c.type === 'work').sort(sortByLastMessage).map(channel => (
                  <ChannelItem key={channel.id} channel={channel} />
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* 加入频道弹窗 */}
      {showJoinModal && (
        <>
          {/* 遮罩层 */}
          <div
            className="fixed inset-0 bg-black/40 z-50"
            onClick={() => {
              setShowJoinModal(false);
              setSearchQuery('');
              setSearchUsers([]);
              setSearchTab('all');
            }}
          />

          {/* 弹窗 */}
          <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[480px] h-[600px] bg-white dark:bg-gray-800 rounded-lg shadow-2xl z-50 flex flex-col">
            {/* 头部 */}
            <div className="flex items-center justify-between p-3 border-b border-gray-100 dark:border-gray-700">
              <h3 className="text-sm dark:text-gray-100">全局搜索</h3>
              <button
                onClick={() => {
                  setShowJoinModal(false);
                  setSearchQuery('');
                  setSearchUsers([]);
                  setSearchTab('all');
                }}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
              >
                <X className="w-4 h-4 text-gray-400 dark:text-gray-500" />
              </button>
            </div>

            {/* 搜索框 */}
            <div className="p-3 border-b border-gray-100 dark:border-gray-700">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 dark:text-gray-500" />
                <input
                  type="text"
                  placeholder="搜索频道、作品或用户..."
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value);
                    handleSearchUsers(e.target.value);
                  }}
                  className="w-full pl-9 pr-3 py-2 text-xs border border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:border-gray-300 dark:focus:border-gray-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                />
              </div>
              {/* 标签栏 */}
              <div className="flex gap-2 mt-2">
                {(['all', 'users', 'channels'] as const).map(tab => (
                  <button
                    key={tab}
                    onClick={() => setSearchTab(tab)}
                    className={cn(
                      "px-3 py-1 text-xs rounded-full transition-colors",
                      searchTab === tab
                        ? "bg-black dark:bg-white text-white dark:text-black"
                        : "bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600"
                    )}
                  >
                    {tab === 'all' ? '全部' : tab === 'users' ? '用户' : '群聊'}
                  </button>
                ))}
              </div>
            </div>

            {/* 内容区域 */}
            <div className="flex-1 overflow-y-auto p-4">
              {/* 空状态：未输入关键词时 */}
              {!searchQuery.trim() ? (
                <div className="flex flex-col items-center justify-center h-full py-20">
                  <div className="w-20 h-20 rounded-2xl border-2 border-gray-300 dark:border-gray-600 flex items-center justify-center mb-4">
                    <Inbox className="w-10 h-10 text-gray-400 dark:text-gray-500" />
                  </div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">输入关键词搜索</p>
                </div>
              ) : (
                <>
              {/* 用户搜索结果 */}
              {(searchTab === 'all' || searchTab === 'users') && searchUsers.length > 0 && (
                <div className="mb-4">
                  <div className="text-xs text-gray-500 dark:text-gray-400 mb-2 font-medium">用户</div>
                  <div className="space-y-2">
                    {searchUsers.map(user => {
                      const displayName = user.fullName || user.username;
                      return (
                        <div key={user.id} className="flex items-start gap-3 p-3 border border-transparent rounded-lg hover:border-gray-200 dark:hover:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                          {/* 头像 */}
                          <div className="w-12 h-12 aspect-square rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center overflow-hidden flex-shrink-0">
                            {user.avatar ? (
                              <img src={user.avatar} className="w-full h-full aspect-square object-cover" />
                            ) : (
                              <div className={cn("w-full h-full flex items-center justify-center text-white text-lg font-medium", getAvatarBgColor(displayName))}>
                                {getAvatarInitial(displayName)}
                              </div>
                            )}
                          </div>
                          {/* 用户信息 */}
                          <div className="flex-1 min-w-0">
                            <h4 className="text-xs font-medium truncate dark:text-gray-100">{displayName}</h4>
                            <p className="text-[10px] text-gray-400 dark:text-gray-500 truncate">@{user.username}</p>
                          </div>
                          {/* 操作按钮 */}
                          <button
                            onClick={() => handleSendFriendRequest(user.id)}
                            disabled={user.relationStatus !== 'none'}
                            className={cn(
                              "px-3 py-1.5 text-xs rounded transition-colors flex-shrink-0",
                              user.relationStatus === 'none'
                                ? "bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200"
                                : user.relationStatus === 'friend'
                                  ? "bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 cursor-default"
                                  : "bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-default"
                            )}
                          >
                            {user.relationStatus === 'none' ? '添加' :
                              user.relationStatus === 'friend' ? '已是好友' :
                                user.relationStatus === 'request_sent' ? '已申请' : '待处理'}
                          </button>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* 频道搜索结果 */}
              {(searchTab === 'all' || searchTab === 'channels') && (
                <>
                  {searchTab === 'all' && searchUsers.length > 0 && modalFilteredChannels.length > 0 && (
                    <div className="text-xs text-gray-500 dark:text-gray-400 mb-2 font-medium">群聊</div>
                  )}
                  {modalFilteredChannels.length === 0 && searchUsers.length === 0 ? (
                    <div className="text-center py-8 text-xs text-gray-400 dark:text-gray-500">
                      {searchQuery ? '未找到匹配的结果' : '暂无可加入的频道'}
                    </div>
                  ) : modalFilteredChannels.length === 0 && searchTab === 'channels' ? (
                    <div className="text-center py-8 text-xs text-gray-400 dark:text-gray-500">
                      未找到匹配的频道
                    </div>
                  ) : (
                    <div className="space-y-2">
                  {modalFilteredChannels.map(channel => {
                    const Icon = getChannelIcon(channel);
                    return (
                      <div
                        key={channel.id}
                        className="flex items-start gap-3 p-3 border border-transparent rounded-lg hover:border-gray-200 dark:hover:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                      >
                        {/* 频道图标/封面 */}
                        <div className="w-12 h-12 aspect-square bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center flex-shrink-0 overflow-hidden">
                          {channel.coverImage ? (
                            <img
                              src={channel.coverImage}
                              alt={channel.name}
                              className="w-full h-full aspect-square object-cover"
                            />
                          ) : channel.type === 'work' ? (
                            <span className="text-xs text-gray-400 dark:text-gray-500">封面</span>
                          ) : (
                            <Icon className="w-5 h-5 text-gray-400 dark:text-gray-500" />
                          )}
                        </div>

                        {/* 频道信息 */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <h4
                              className="text-xs truncate dark:text-gray-100"
                              title={channel.name}
                            >
                              {channel.name}
                            </h4>
                            {channel.isPermanent && (
                              <span className="text-[10px] text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/30 px-1.5 py-0.5 rounded">永久</span>
                            )}
                          </div>

                          {channel.type === 'work' && (
                            <div className="text-[10px] text-gray-500 dark:text-gray-400 space-y-0.5">
                              <p>作者：{channel.author || '佚名'}</p>
                              {channel.description && (
                                <p className="text-[10px] line-clamp-2">{channel.description}</p>
                              )}
                            </div>
                          )}

                          {channel.type === 'fangroup' && channel.description && (
                            <p className="text-[10px] text-gray-500 dark:text-gray-400 line-clamp-2">{channel.description}</p>
                          )}

                          {channel.status === 'locked' && (
                            <p className="text-[10px] text-red-500 dark:text-red-400 mt-1">频道已折叠</p>
                          )}
                        </div>

                        {/* 加入按钮 */}
                        <button
                          onClick={() => handleJoinChannel(channel.id)}
                          disabled={channel.status === 'locked' || pendingChannelIds?.has(channel.id)}
                          className={cn(
                            "px-3 py-1.5 text-xs rounded transition-colors",
                            pendingChannelIds?.has(channel.id)
                              ? "bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-default"
                              : channel.status === 'locked'
                                ? "bg-gray-100 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed"
                                : "bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200"
                          )}
                        >
                          {channel.status === 'locked'
                            ? '已折叠'
                            : pendingChannelIds?.has(channel.id)
                              ? '已申请'
                              : channel.type === 'official'
                                ? '加入'
                                : '申请'}
                        </button>
                      </div>
                    );
                  })}
                    </div>
                  )}
                </>
              )}
                </>
              )}
            </div>
          </div>
        </>
      )}

      {/* 好友请求弹窗 */}
      {showFriendRequests && (
        <>
          <div className="fixed inset-0 bg-black/40 z-50" onClick={() => setShowFriendRequests(false)} />
          <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] max-h-[500px] bg-white dark:bg-gray-800 rounded-lg shadow-2xl z-50 flex flex-col">
            {/* 头部 */}
            <div className="flex items-center justify-between p-3 border-b border-gray-100 dark:border-gray-700">
              <h3 className="text-sm font-medium dark:text-gray-100">好友请求</h3>
              <button
                onClick={() => setShowFriendRequests(false)}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                <X className="w-4 h-4 text-gray-400 dark:text-gray-500" />
              </button>
            </div>

            {/* 请求列表 */}
            <div className="flex-1 overflow-y-auto p-3">
              {friendRequests.length === 0 ? (
                <div className="text-center py-8 text-xs text-gray-400 dark:text-gray-500">
                  暂无好友请求
                </div>
              ) : (
                <div className="space-y-2">
                  {friendRequests.map(request => {
                    const displayName = request.fromUser.fullName || request.fromUser.username;
                    return (
                      <div key={request.id} className="flex items-start gap-3 p-3 border border-gray-100 dark:border-gray-700 rounded-lg">
                        {/* 头像 */}
                        <div className="w-12 h-12 aspect-square rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center overflow-hidden flex-shrink-0">
                          {request.fromUser.avatar ? (
                            <img src={request.fromUser.avatar} className="w-full h-full aspect-square object-cover" />
                          ) : (
                            <div className={cn(
                              "w-full h-full flex items-center justify-center text-white text-lg font-medium",
                              getAvatarBgColor(displayName)
                            )}>
                              {getAvatarInitial(displayName)}
                            </div>
                          )}
                        </div>

                        {/* 信息 */}
                        <div className="flex-1 min-w-0">
                          <h4 className="text-xs font-medium dark:text-gray-100">
                            {displayName}
                          </h4>
                          {request.message && (
                            <p className="text-[10px] text-gray-500 dark:text-gray-400 mt-0.5 line-clamp-2">
                              {request.message}
                            </p>
                          )}
                          <p className="text-[10px] text-gray-400 dark:text-gray-500 mt-1">
                            {new Date(request.createdAt).toLocaleDateString()}
                          </p>
                        </div>

                        {/* 操作按钮 */}
                        <div className="flex gap-2 flex-shrink-0">
                          <button
                            onClick={() => handleRejectRequest(request.id)}
                            className="px-2.5 py-1 text-xs border border-gray-200 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300 transition-colors"
                          >
                            拒绝
                          </button>
                          <button
                            onClick={() => handleAcceptRequest(request.id)}
                            className="px-2.5 py-1 text-xs bg-black dark:bg-white text-white dark:text-black rounded hover:bg-gray-800 dark:hover:bg-gray-200 transition-colors"
                          >
                            同意
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        </>
      )}

      {/* 编辑粉丝群对话框 */}
      {editingChannel && (
        <EditFangroupDialog
          isOpen={!!editingChannel}
          onClose={() => setEditingChannel(null)}
          onSuccess={() => {
            setEditingChannel(null);
            onChannelUpdate?.();
          }}
          channel={editingChannel}
        />
      )}
    </div>
  );
}
