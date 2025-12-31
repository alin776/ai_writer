import { useState, useEffect } from 'react';
import { Hash, Lock, Users, MessageCircle, BookOpen, Coffee, FlaskConical, ChevronDown, ChevronRight, ChevronLeft, Bell, Plus, X, Search, AtSign, Edit2 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { channelApi, UnreadSummary } from '@/services/channelApi';
import { EditFangroupDialog } from './EditFangroupDialog';

export interface Channel {
  id: string;
  name: string;
  type: 'official' | 'fangroup' | 'work';
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
}

export function ChannelList({ channels, activeChannelId, onChannelSelect, onJoinChannel, availableChannels, pendingChannelIds, onCreateFangroup, isCollapsed = false, onToggleCollapse, currentUserId, onChannelUpdate }: ChannelListProps) {
  const [expandedSections, setExpandedSections] = useState({
    official: true,
    fangroup: true,
    work: true,
  });
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [unreadData, setUnreadData] = useState<Map<string, { unreadCount: number; mentionCount: number }>>(new Map());
  const [editingChannel, setEditingChannel] = useState<Channel | null>(null);  // 正在编辑的频道

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

  const officialChannels = channels.filter(c => c.type === 'official');
  const fangroupChannels = channels.filter(c => c.type === 'fangroup');
  const workChannels = channels.filter(c => c.type === 'work');

  const ChannelItem = ({ channel }: { channel: Channel }) => {
    const Icon = getChannelIcon(channel);
    const isActive = channel.id === activeChannelId;
    const channelUnreadData = unreadData.get(channel.id);
    const isCreator = channel.type === 'fangroup' && channel.creatorId === currentUserId;

    // 点击头像编辑（仅粉丝群创建者）
    const handleAvatarClick = (e: React.MouseEvent) => {
      if (isCreator) {
        e.stopPropagation();  // 阻止选中频道
        setEditingChannel(channel);
      }
    };

    return (
      <button
        onClick={() => onChannelSelect(channel.id)}
        className={cn(
          "w-full flex items-center gap-2 px-2 py-2 rounded transition-colors group relative",
          isActive ? "bg-black text-white dark:bg-zinc-800" : "hover:bg-gray-50 dark:hover:bg-zinc-800 text-gray-700 dark:text-gray-300"
        )}
      >
        {/* 频道图标/头像 - 粉丝群创建者可点击编辑 */}
        {isCreator ? (
          <div
            onClick={handleAvatarClick}
            className="relative shrink-0 cursor-pointer group/avatar"
            title="点击编辑粉丝群"
          >
            {channel.coverImage ? (
              <img
                src={channel.coverImage}
                alt={channel.name}
                className="w-5 h-5 rounded-full object-cover group-hover/avatar:ring-2 group-hover/avatar:ring-blue-500 transition-all"
              />
            ) : (
              <div className="w-5 h-5 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center group-hover/avatar:ring-2 group-hover/avatar:ring-blue-500 transition-all">
                <Users className="w-3 h-3 text-gray-500 dark:text-gray-400" />
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
            className="shrink-0 w-5 h-5 rounded-full object-cover"
          />
        ) : (
          <Icon className="shrink-0 opacity-60 w-5 h-5" />
        )}
        <span className="flex-1 text-left truncate text-sm">{channel.name}</span>

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
    isFirst?: boolean;
  }) => {
    const isExpanded = expandedSections[section];

    return (
      <button
        onClick={() => toggleSection(section)}
        className="w-full flex items-center gap-1.5 px-2 py-2 hover:bg-gray-50 dark:hover:bg-gray-800 rounded transition-colors group"
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
      // 官方频道直接加入后关闭弹窗，非官方频道（申请）保持弹窗打开显示"已申请"状态
      const channel = availableChannels?.find(c => c.id === channelId);
      if (channel?.type === 'official') {
        setShowJoinModal(false);
        setSearchQuery('');
      }
    }
  };

  const filteredAvailableChannels = (availableChannels || []).filter(channel =>
    channel.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    channel.bookTitle?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    channel.author?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="border-r border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-900 flex flex-col h-full w-56 min-w-56">
      <ScrollArea className="flex-1">
        <div className="space-y-0.5 p-2">
          {/* 官方频道 */}
          <SectionHeader title="官方" section="official" count={officialChannels.length} />
          {expandedSections.official && (
            <div className="space-y-0.5 mb-2 ml-1">
              {officialChannels.map(channel => (
                <ChannelItem key={channel.id} channel={channel} />
              ))}
            </div>
          )}

          {/* 粉丝群 */}
          <SectionHeader title="私域" section="fangroup" count={fangroupChannels.length} />
          {expandedSections.fangroup && (
            <div className="space-y-0.5 mb-2 ml-1">
              {/* 创建粉丝群按钮 */}
              {onCreateFangroup && (
                <button
                  onClick={onCreateFangroup}
                  className="w-full flex items-center gap-2 px-2 py-2 rounded transition-colors hover:bg-blue-50 dark:hover:bg-blue-900/30 text-blue-600 dark:text-blue-400"
                >
                  <Plus className="shrink-0 w-4 h-4" />
                  <span className="flex-1 text-left text-sm">创建粉丝群</span>
                </button>
              )}
              {fangroupChannels.map(channel => (
                <ChannelItem key={channel.id} channel={channel} />
              ))}
            </div>
          )}

          {/* 作品频道 */}
          <SectionHeader title="作品" section="work" count={workChannels.length} />
          {expandedSections.work && (
            <div className="space-y-0.5 mb-2 ml-1">
              {workChannels.map(channel => (
                <ChannelItem key={channel.id} channel={channel} />
              ))}
            </div>
          )}
        </div>
      </ScrollArea>

      {/* 底部操作栏 */}
      <div className="border-t border-gray-100 dark:border-gray-700 p-2 flex justify-center items-center relative">
        {onJoinChannel && availableChannels && availableChannels.length > 0 && (
          <button
            onClick={() => setShowJoinModal(true)}
            className="absolute left-2 text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
          >
            发现频道
          </button>
        )}
        <button
          onClick={onToggleCollapse}
          className="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-800 rounded transition-colors"
          title="收起频道列表"
        >
          <ChevronLeft className="w-4 h-4 text-gray-400 dark:text-gray-500" />
        </button>
      </div>

      {/* 加入频道弹窗 */}
      {showJoinModal && (
        <>
          {/* 遮罩层 */}
          <div
            className="fixed inset-0 bg-black/40 z-50"
            onClick={() => {
              setShowJoinModal(false);
              setSearchQuery('');
            }}
          />

          {/* 弹窗 */}
          <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[480px] max-h-[600px] bg-white dark:bg-gray-800 rounded-lg shadow-2xl z-50 flex flex-col">
            {/* 头部 */}
            <div className="flex items-center justify-between p-3 border-b border-gray-100 dark:border-gray-700">
              <h3 className="text-sm dark:text-gray-100">发现频道</h3>
              <button
                onClick={() => {
                  setShowJoinModal(false);
                  setSearchQuery('');
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
                  placeholder="搜索频道、作品或作者..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 text-xs border border-gray-200 dark:border-gray-600 rounded focus:outline-none focus:border-gray-300 dark:focus:border-gray-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                />
              </div>
            </div>

            {/* 频道列表 */}
            <div className="flex-1 overflow-y-auto p-4">
              {filteredAvailableChannels.length === 0 ? (
                <div className="text-center py-8 text-xs text-gray-400 dark:text-gray-500">
                  {searchQuery ? '未找到匹配的频道' : '暂无可加入的频道'}
                </div>
              ) : (
                <div className="space-y-2">
                  {filteredAvailableChannels.map(channel => {
                    const Icon = getChannelIcon(channel);
                    return (
                      <div
                        key={channel.id}
                        className="flex items-start gap-3 p-3 border border-gray-100 dark:border-gray-700 rounded-lg hover:border-gray-200 dark:hover:border-gray-600 transition-colors"
                      >
                        {/* 频道图标/封面 */}
                        <div className="w-12 h-12 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center flex-shrink-0 overflow-hidden">
                          {channel.coverImage ? (
                            <img
                              src={channel.coverImage}
                              alt={channel.name}
                              className="w-full h-full object-cover"
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
                            <h4 className="text-xs truncate dark:text-gray-100">
                              {channel.type === 'work' && channel.bookTitle
                                ? `《${channel.bookTitle}》`
                                : channel.name}
                            </h4>
                            {channel.isPermanent && (
                              <span className="text-[10px] text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/30 px-1.5 py-0.5 rounded">永久</span>
                            )}
                          </div>

                          {channel.type === 'work' && (
                            <div className="text-[10px] text-gray-500 dark:text-gray-400 space-y-0.5">
                              <p>作者：{channel.author || '佚名'}</p>
                              <p>收藏：{channel.collectCount || 0}</p>
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
