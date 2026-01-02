/**
 * 消息转发对话框
 */
import { useState, useEffect, useMemo } from 'react';
import { X, Search, Loader2, Send, Image as ImageIcon, Hash, Smile, User } from 'lucide-react';
import { cn } from '@/lib/utils';
import { forwardMessage, getMyChannels, type Channel } from '@/services/channelApi';
import { getFriends, type FriendshipResponse } from '@/services/friendApi';
import { useGlobalStore } from '@/store/globalStore';
import MiniEmojiPicker from './MiniEmojiPicker';

interface ForwardMessageDialogProps {
  isOpen: boolean;
  onClose: () => void;
  sourceChannelId: string;
  messageId: string;
  messageContent: string;
  messageSender: string;
  messageAttachments?: {
    id: string;
    fileName: string;
    fileType?: string;
    fileUrl: string;
    thumbnailUrl?: string;
  }[];
}

export function ForwardMessageDialog({
  isOpen,
  onClose,
  sourceChannelId,
  messageId,
  messageContent,
  messageSender,
  messageAttachments,
}: ForwardMessageDialogProps) {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [friends, setFriends] = useState<FriendshipResponse[]>([]);
  const [selectedChannels, setSelectedChannels] = useState<Set<string>>(new Set());
  const [searchQuery, setSearchQuery] = useState('');
  const [comment, setComment] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isForwarding, setIsForwarding] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const { success: showSuccess, error: showError, warning: showWarning } = useGlobalStore();

  // 创建私聊频道ID到好友信息的映射
  const privateChannelFriendMap = useMemo(() => {
    const map = new Map<string, FriendshipResponse>();
    friends.forEach(f => {
      if (f.privateChannelId) {
        map.set(f.privateChannelId, f);
      }
    });
    return map;
  }, [friends]);

  // 获取频道显示名称
  const getChannelDisplayName = (channel: Channel) => {
    if (channel.type === 'private') {
      const friendInfo = privateChannelFriendMap.get(channel.id);
      if (friendInfo) {
        return friendInfo.friend.fullName || friendInfo.friend.username;
      }
    }
    return channel.name;
  };

  // 获取频道显示头像
  const getChannelDisplayAvatar = (channel: Channel) => {
    if (channel.type === 'private') {
      const friendInfo = privateChannelFriendMap.get(channel.id);
      if (friendInfo) {
        return friendInfo.friend.avatar;
      }
    }
    return channel.coverImage;
  };

  // 加载可选频道
  useEffect(() => {
    if (isOpen) {
      loadChannels();
    }
  }, [isOpen]);

  const loadChannels = async () => {
    setIsLoading(true);
    try {
      // 同时加载频道和好友列表
      const [channelResponse, friendResponse] = await Promise.all([
        getMyChannels(),
        getFriends(0, 100)
      ]);
      // 排除当前频道
      setChannels(channelResponse.channels.filter(c => c.id !== sourceChannelId));
      setFriends(friendResponse.items);
    } catch (error) {
      console.error('加载频道列表失败:', error);
      showError('加载频道列表失败');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredChannels = channels.filter(channel => {
    const displayName = getChannelDisplayName(channel);
    return displayName.toLowerCase().includes(searchQuery.toLowerCase());
  });

  const toggleChannel = (channelId: string) => {
    const newSelected = new Set(selectedChannels);
    if (newSelected.has(channelId)) {
      newSelected.delete(channelId);
    } else {
      if (newSelected.size >= 10) {
        showWarning('最多只能选择 10 个频道');
        return;
      }
      newSelected.add(channelId);
    }
    setSelectedChannels(newSelected);
  };

  const handleForward = async () => {
    if (selectedChannels.size === 0) {
      showWarning('请选择至少一个目标频道');
      return;
    }

    setIsForwarding(true);
    try {
      const response = await forwardMessage(sourceChannelId, messageId, {
        target_channel_ids: Array.from(selectedChannels),
        add_comment: comment || undefined,
      });

      if (response.forwarded_count > 0) {
        showSuccess(`成功转发到 ${response.forwarded_count} 个频道`);
      }
      if (response.failed_channels.length > 0) {
        showWarning(`${response.failed_channels.length} 个频道转发失败`);
      }

      handleClose();
    } catch (error) {
      console.error('转发失败:', error);
      showError('转发失败，请稍后重试');
    } finally {
      setIsForwarding(false);
    }
  };

  const handleClose = () => {
    onClose();
    setSelectedChannels(new Set());
    setSearchQuery('');
    setComment('');
    setShowEmojiPicker(false);
  };

  // 处理表情选择
  const handleEmojiSelect = (emoji: string) => {
    setComment(prev => prev + emoji);
    setShowEmojiPicker(false);
  };

  // 获取频道类型标签
  const getChannelTypeLabel = (type: string) => {
    switch (type) {
      case 'official': return '官方频道';
      case 'fangroup': return '粉丝群';
      case 'work': return '作品频道';
      case 'private': return '私聊';
      default: return '频道';
    }
  };

  // 计算图片附件数量
  const imageCount = messageAttachments?.filter(a => a.fileType?.startsWith('image/')).length || 0;

  // 获取第一张图片作为缩略图
  const thumbnailImage = messageAttachments?.find(a => a.fileType?.startsWith('image/'));

  if (!isOpen) return null;

  return (
    <>
      {/* 遮罩层 */}
      <div
        className="fixed inset-0 bg-black/50 z-50"
        onClick={handleClose}
      />

      {/* 对话框 */}
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[420px] max-h-[90vh] bg-white dark:bg-gray-800 rounded-xl shadow-2xl overflow-hidden flex flex-col">
        {/* 头部 - 固定 */}
        <div className="flex items-start justify-between p-5 pb-3 shrink-0">
          <div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white">转发给：</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">选择您想在何处分享此消息。</p>
          </div>
          <button
            onClick={handleClose}
            className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors -mt-1 -mr-1"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        {/* 搜索框 - 固定在头部下方 */}
        <div className="px-5 pb-4 shrink-0">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="搜索"
              className="w-full bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg pl-10 pr-4 py-2.5 text-sm text-gray-700 dark:text-gray-200 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* 频道列表 - 可滚动 */}
        <div className="flex-1 min-h-0 overflow-y-auto px-5">
          {isLoading ? (
            <div className="flex items-center justify-center h-32">
              <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
            </div>
          ) : filteredChannels.length === 0 ? (
            <div className="text-center text-gray-500 dark:text-gray-400 py-8 text-sm">
              {searchQuery ? '未找到匹配的频道' : '暂无可转发的频道'}
            </div>
          ) : (
            <div className="space-y-1">
              {filteredChannels.map((channel) => {
                const isSelected = selectedChannels.has(channel.id);
                const displayName = getChannelDisplayName(channel);
                const displayAvatar = getChannelDisplayAvatar(channel);
                const isPrivate = channel.type === 'private';
                return (
                  <label
                    key={channel.id}
                    className="flex items-center gap-3 p-2.5 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                  >
                      {/* 频道图标 - 圆形 */}
                      <div className={cn(
                        "w-10 h-10 rounded-full flex items-center justify-center shrink-0 overflow-hidden",
                        displayAvatar ? "" : "bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400"
                      )}>
                        {displayAvatar ? (
                          <img src={displayAvatar} className="w-full h-full object-cover" />
                        ) : isPrivate ? (
                          <User className="w-5 h-5" />
                        ) : (
                          <Hash className="w-5 h-5" />
                        )}
                      </div>

                      {/* 频道信息 */}
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                          {displayName}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {getChannelTypeLabel(channel.type)}
                        </div>
                      </div>

                      {/* 复选框 - 方形格子 */}
                      <div className={cn(
                        "w-6 h-6 rounded-md border-2 flex items-center justify-center shrink-0 transition-all",
                        isSelected
                          ? "bg-indigo-500 border-indigo-500"
                          : "border-gray-300 dark:border-gray-500 bg-white dark:bg-gray-700"
                      )}>
                        {isSelected && (
                          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="3">
                            <polyline points="20 6 9 17 4 12" strokeLinecap="round" strokeLinejoin="round" />
                          </svg>
                        )}
                      </div>
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => toggleChannel(channel.id)}
                        className="sr-only"
                      />
                    </label>
                  );
                })}
              </div>
            )}
        </div>

        {/* 底部：消息预览 + 输入框 + 发送按钮 - 固定在底部 */}
        <div className="px-5 pb-5 pt-4 border-t border-gray-100 dark:border-gray-700 space-y-3 shrink-0">
          {/* 消息预览卡片 */}
          <div className="flex gap-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">
                  {messageContent || '（无文字内容）'}
                </p>
                {imageCount > 0 && (
                  <div className="flex items-center gap-1 mt-1 text-xs text-gray-400">
                    <ImageIcon className="w-3.5 h-3.5" />
                    <span>{imageCount}张图片</span>
                  </div>
                )}
              </div>
              {/* 图片缩略图 */}
              {thumbnailImage && (
                <div className="w-16 h-12 rounded-md overflow-hidden shrink-0 bg-gray-200 dark:bg-gray-600">
                  <img
                    src={thumbnailImage.thumbnailUrl || thumbnailImage.fileUrl}
                    className="w-full h-full object-cover"
                  />
                </div>
              )}
            </div>

            {/* 添加评论输入框 */}
            <div>
              <div className="flex items-center gap-2 bg-gray-50 dark:bg-gray-700 rounded-lg px-3 py-2.5 border border-gray-200 dark:border-gray-600">
                <input
                  type="text"
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="添加一条可选消息......"
                  className="flex-1 bg-transparent text-sm text-gray-700 dark:text-gray-200 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none"
                  maxLength={500}
                />
                {/* 表情按钮 */}
                <button
                  type="button"
                  onClick={() => setShowEmojiPicker(!showEmojiPicker)}
                  className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors rounded hover:bg-gray-200 dark:hover:bg-gray-600"
                >
                  <Smile className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* 发送按钮 */}
            <button
              onClick={handleForward}
              disabled={selectedChannels.size === 0 || isForwarding}
              className={cn(
                "w-full py-2.5 rounded-lg font-medium text-sm transition-colors flex items-center justify-center gap-2",
                selectedChannels.size === 0 || isForwarding
                  ? "bg-gray-200 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed"
                  : "bg-indigo-500 hover:bg-indigo-600 text-white"
              )}
            >
              {isForwarding ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>转发中...</span>
                </>
              ) : (
                <>
                  <span>发送</span>
                  <Send className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
      </div>

      {/* 表情选择器 - 在对话框右侧外部 */}
      {showEmojiPicker && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setShowEmojiPicker(false)}
          />
          <div
            className="fixed z-50"
            style={{
              top: '50%',
              left: 'calc(50% + 220px)',
              transform: 'translateY(-50%)'
            }}
          >
            <MiniEmojiPicker
              onSelect={handleEmojiSelect}
              onClose={() => setShowEmojiPicker(false)}
            />
          </div>
        </>
      )}
    </>
  );
}

export default ForwardMessageDialog;
