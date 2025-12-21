import { useState, useRef, useEffect } from 'react';
import { Send, AtSign, Megaphone, MoreVertical, Smile, Reply, AlertCircle, X, Users, Trash2, ArrowDown, Mail, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import type { Channel } from './ChannelList';
import { MemberManagementDialog } from './MemberManagementDialog';
import { ReportMessageDialog } from './ReportMessageDialog';
import { getChannelMembers, type ChannelMember, channelApi, UnreadInfo } from '@/services/channelApi';

export interface Message {
  id: string;
  userId: string;
  userName: string;
  userAvatar?: string;
  userTitle?: string; // 用户称号
  userTitleColor?: string; // 称号颜色
  content: string;
  timestamp: Date;
  type?: 'normal' | 'announcement' | 'mention';
  isPinned?: boolean;
  replyTo?: {
    id: string;
    userName: string;
    content: string;
  };
}

interface ChatAreaProps {
  channel: Channel;
  messages: Message[];
  currentUser: {
    id: string;
    name: string;
    avatar?: string;
    isCreator?: boolean;
  };
  onSendMessage: (content: string, type?: 'normal' | 'announcement', replyToId?: string) => void;
  onMentionAll?: () => void;
  onLeaveChannel?: () => void;
}

export function ChatArea({ channel, messages, currentUser, onSendMessage, onMentionAll, onLeaveChannel }: ChatAreaProps) {
  const [messageInput, setMessageInput] = useState('');
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [emojiPickerPosition, setEmojiPickerPosition] = useState({ x: 0, y: 0 });
  const [showSidebar, setShowSidebar] = useState(false);
  const [showMemberDialog, setShowMemberDialog] = useState(false);
  const [showReportDialog, setShowReportDialog] = useState(false);
  const [reportingMessageId, setReportingMessageId] = useState<string>('');
  const [replyingTo, setReplyingTo] = useState<Message | null>(null);
  const [showMentionMenu, setShowMentionMenu] = useState(false);
  const [mentionMenuPosition, setMentionMenuPosition] = useState({ x: 0, y: 0 });
  const [members, setMembers] = useState<ChannelMember[]>([]);
  const [contextMenu, setContextMenu] = useState<{
    show: boolean;
    x: number;
    y: number;
    messageId: string;
  } | null>(null);
  const [unreadInfo, setUnreadInfo] = useState<UnreadInfo | null>(null);
  const [isAtBottom, setIsAtBottom] = useState(true);
  const [newMessageCount, setNewMessageCount] = useState(0);
  const [latestAnnouncement, setLatestAnnouncement] = useState<Message | null>(null);
  const [showSearchDialog, setShowSearchDialog] = useState(false);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [searchResults, setSearchResults] = useState<Message[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const emojiButtonRef = useRef<HTMLButtonElement>(null);
  const mentionButtonRef = useRef<HTMLButtonElement>(null);
  const messageRefs = useRef<Map<string, HTMLDivElement>>(new Map());

  // 获取未读信息
  useEffect(() => {
    const fetchUnreadInfo = async () => {
      try {
        const info = await channelApi.getChannelUnreadInfo(channel.id);
        setUnreadInfo(info);
      } catch (error) {
        console.error('获取未读信息失败:', error);
      }
    };

    fetchUnreadInfo();
    const interval = setInterval(fetchUnreadInfo, 30000);
    return () => clearInterval(interval);
  }, [channel.id]);

  // 监听滚动位置
  useEffect(() => {
    const scrollElement = scrollRef.current?.querySelector('[data-slot="scroll-area-viewport"]');
    if (!scrollElement) return;

    const handleScroll = () => {
      const { scrollTop, scrollHeight, clientHeight } = scrollElement;
      const atBottom = scrollHeight - scrollTop - clientHeight < 50;
      setIsAtBottom(atBottom);

      // 如果滚动到底部，清除未读计数
      if (atBottom) {
        setNewMessageCount(0);
      }
    };

    scrollElement.addEventListener('scroll', handleScroll);
    return () => scrollElement.removeEventListener('scroll', handleScroll);
  }, []);

  // 自动滚动到底部（仅当已在底部时）
  useEffect(() => {
    if (isAtBottom) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    } else {
      // 不在底部时增加新消息计数
      setNewMessageCount(prev => prev + 1);
    }
  }, [messages.length]);

  // 加载成员列表
  useEffect(() => {
    const loadMembers = async () => {
      try {
        const response = await getChannelMembers(channel.id);
        setMembers(response.members);
      } catch (error) {
        console.error('加载成员列表失败:', error);
      }
    };
    loadMembers();
  }, [channel.id]);

  // 获取最新公告
  useEffect(() => {
    const fetchLatestAnnouncement = async () => {
      try {
        const response = await channelApi.getLatestAnnouncement(channel.id);
        const announcement = response.announcement;

        if (announcement) {
          setLatestAnnouncement({
            id: announcement.id,
            userId: '',
            userName: announcement.userName,
            userAvatar: announcement.userAvatar,
            userTitle: announcement.userTitle,
            userTitleColor: announcement.userTitleColor,
            content: announcement.content,
            timestamp: new Date(announcement.createdAt),
            type: 'announcement'
          });
        } else {
          setLatestAnnouncement(null);
        }
      } catch (error) {
        console.error('获取最新公告失败:', error);
        setLatestAnnouncement(null);
      }
    };

    fetchLatestAnnouncement();
  }, [channel.id, messages]); // 当消息更新时也重新获取

  const handleSend = (type: 'normal' | 'announcement' = 'normal') => {
    if (messageInput.trim()) {
      onSendMessage(messageInput, type, replyingTo?.id);
      setMessageInput('');
      setReplyingTo(null);  // 清除回复状态
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const insertMention = (username?: string) => {
    const textarea = textareaRef.current;
    if (textarea) {
      const cursorPos = textarea.selectionStart;
      const textBefore = messageInput.substring(0, cursorPos);
      const textAfter = messageInput.substring(cursorPos);
      const mentionText = username ? `@${username} ` : '@';
      setMessageInput(textBefore + mentionText + textAfter);

      setTimeout(() => {
        const newPos = cursorPos + mentionText.length;
        textarea.setSelectionRange(newPos, newPos);
        textarea.focus();
      }, 0);
    }
  };

  const toggleMentionMenu = () => {
    if (!showMentionMenu && mentionButtonRef.current) {
      const buttonRect = mentionButtonRef.current.getBoundingClientRect();
      setMentionMenuPosition({
        x: buttonRect.left,
        y: buttonRect.top - 10
      });
    }
    setShowMentionMenu(!showMentionMenu);
  };

  const insertEmoji = (emoji: string) => {
    const textarea = textareaRef.current;
    if (textarea) {
      const cursorPos = textarea.selectionStart;
      const textBefore = messageInput.substring(0, cursorPos);
      const textAfter = messageInput.substring(cursorPos);
      setMessageInput(textBefore + emoji + textAfter);

      setTimeout(() => {
        const newPos = cursorPos + emoji.length;
        textarea.setSelectionRange(newPos, newPos);
        textarea.focus();
      }, 0);
    }
    setShowEmojiPicker(false);
  };

  const toggleEmojiPicker = () => {
    if (!showEmojiPicker && emojiButtonRef.current) {
      const buttonRect = emojiButtonRef.current.getBoundingClientRect();
      // 表情窗口宽度 320px，高度约 300px
      // 让窗口显示在按钮正上方，居中对齐
      setEmojiPickerPosition({
        x: buttonRect.left + buttonRect.width / 2 - 160, // 160 = 320/2
        y: buttonRect.top - 310 // 310 = 表情窗口高度 + 10px间距
      });
    }
    setShowEmojiPicker(!showEmojiPicker);
  };

  // 常用表情列表
  const emojis = [
    '😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂',
    '🙂', '🙃', '😉', '😊', '😇', '🥰', '😍', '🤩',
    '😘', '😗', '😚', '😙', '😋', '😛', '😜', '🤪',
    '😝', '🤗', '🤭', '🤔', '🤨', '😐', '😑', '😶',
    '😏', '😒', '🙄', '😬', '🤥', '😌', '😔', '😪',
    '🤤', '😴', '😷', '🤒', '🤕', '🤢', '🤮', '🤧',
    '🥵', '🥶', '😱', '😨', '😰', '😥', '😢', '😭',
    '😤', '😠', '😡', '🤬', '😈', '👿', '💀', '☠️',
    '👍', '👎', '👏', '🙌', '👌', '✌️', '🤞', '🤟',
    '🤘', '🤙', '👈', '👉', '👆', '👇', '☝️', '✋',
    '🤚', '🖐️', '🖖', '👋', '🤝', '💪', '🙏', '✍️',
    '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍',
    '💔', '❣️', '💕', '💞', '💓', '💗', '💖', '💘',
    '💝', '💟', '⭐', '🌟', '✨', '💫', '🔥', '💯'
  ];

  // 点击外部关闭表情选择器和 @ 菜单
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (showEmojiPicker &&
          emojiButtonRef.current &&
          !emojiButtonRef.current.contains(event.target as Node) &&
          !(event.target as Element).closest('.emoji-picker')) {
        setShowEmojiPicker(false);
      }
      if (showMentionMenu &&
          mentionButtonRef.current &&
          !mentionButtonRef.current.contains(event.target as Node) &&
          !(event.target as Element).closest('.mention-menu')) {
        setShowMentionMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showEmojiPicker, showMentionMenu]);

  const getChannelStatusInfo = () => {
    if (channel.status === 'locked') {
      return {
        show: true,
        variant: 'destructive' as const,
        text: '该频道已折叠,连续7天无人发言'
      };
    }
    if (channel.status === 'warning') {
      return {
        show: true,
        variant: 'default' as const,
        text: `预警:距离频道折叠还有 ${7 - (channel.warningDays || 0)} 天,快来聊天唤醒频道吧!`
      };
    }
    if (channel.type === 'work' && !channel.isPermanent) {
      return {
        show: true,
        variant: 'secondary' as const,
        text: '试运行中:保持活跃满一个月可转为永久频道'
      };
    }
    return { show: false };
  };

  // 跳转到指定消息
  const jumpToMessage = (messageId: string) => {
    const element = messageRefs.current.get(messageId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      // 高亮效果
      element.classList.add('highlight-message');
      setTimeout(() => element.classList.remove('highlight-message'), 2000);
    }
  };

  // 跳转到未读消息
  const jumpToUnread = () => {
    if (unreadInfo?.firstUnreadMessageId) {
      jumpToMessage(unreadInfo.firstUnreadMessageId);
      // 标记为已读
      channelApi.markChannelAsRead(channel.id, unreadInfo.firstUnreadMessageId);
    }
  };

  // 跳转到@提醒
  const jumpToMention = () => {
    if (unreadInfo?.latestMentionMessageId) {
      jumpToMessage(unreadInfo.latestMentionMessageId);
    }
  };

  // 回到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    setNewMessageCount(0);
    // 标记所有消息为已读
    channelApi.markChannelAsRead(channel.id);
  };

  // 撤回消息
  const handleRecallMessage = async (messageId: string) => {
    try {
      await channelApi.recallMessage(channel.id, messageId);
      // 刷新消息列表（这里假设父组件会处理）
      window.location.reload(); // 简单实现，实际应该通过回调更新
    } catch (error: any) {
      alert(error.response?.data?.detail || '撤回失败');
    }
  };

  // 搜索消息
  const handleSearch = async () => {
    if (!searchKeyword.trim()) return;

    setIsSearching(true);
    try {
      const result = await channelApi.searchMessages(channel.id, searchKeyword, {});
      // 转换搜索结果为 Message 格式
      const formattedMessages: Message[] = result.messages.map((msg: any) => ({
        id: msg.id,
        userId: msg.userId,
        userName: msg.userName,
        userAvatar: msg.userAvatar,
        userTitle: msg.userTitle,
        userTitleColor: msg.userTitleColor,
        content: msg.content,
        timestamp: new Date(msg.createdAt),
        type: msg.messageType === 'announcement' ? 'announcement' : 'normal'
      }));
      setSearchResults(formattedMessages);
    } catch (error) {
      console.error('搜索失败:', error);
      alert('搜索失败');
    } finally {
      setIsSearching(false);
    }
  };

  const statusInfo = getChannelStatusInfo();
  const canSendAnnouncement = currentUser.isCreator && channel.type === 'fangroup';

  return (
    <div
      className="flex-1 flex flex-col bg-white h-full"
      onContextMenu={(e) => {
        // 阻止默认右键菜单，只允许自定义右键菜单
        e.preventDefault();
      }}
    >
      {/* 频道头部 */}
      <div style={{ padding: '12px', borderBottom: '1px solid #f3f4f6', backgroundColor: 'white' }}>
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base font-medium">{channel.name}</h3>
              {channel.isPermanent && (
                <span className="text-xs text-amber-600 bg-amber-50 px-2 py-1 rounded">永久</span>
              )}
              {channel.type === 'work' && channel.bookTitle && (
                <span className="text-sm text-gray-400">《{channel.bookTitle}》</span>
              )}
            </div>
            {channel.type === 'work' && channel.collectCount && (
              <p className="text-sm text-gray-400 mt-1">收藏 {channel.collectCount}</p>
            )}
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setShowSearchDialog(true)}
              className="p-1 hover:bg-gray-50 rounded"
              title="搜索消息"
            >
              <Search className="w-4 h-4 text-gray-400" />
            </button>
            <button
              onClick={() => setShowSidebar(true)}
              className="p-1 hover:bg-gray-50 rounded"
            >
              <MoreVertical className="w-4 h-4 text-gray-400" />
            </button>
          </div>
        </div>

        {/* 状态提示 */}
        {statusInfo.show && (
          <div className={cn(
            "mt-2 px-3 py-2 rounded text-sm",
            statusInfo.variant === 'destructive' && "bg-red-50 text-red-600 border border-red-100",
            statusInfo.variant === 'default' && "bg-amber-50 text-amber-700 border border-amber-100",
            statusInfo.variant === 'secondary' && "bg-gray-50 text-gray-600 border border-gray-100"
          )}>
            {statusInfo.text}
          </div>
        )}

        {/* 最新公告栏 */}
        {latestAnnouncement && (
          <div
            onClick={() => jumpToMessage(latestAnnouncement.id)}
            className="mt-2 px-3 py-2 rounded bg-amber-50 border border-amber-200 cursor-pointer hover:bg-amber-100 transition-colors"
          >
            <div className="flex items-start gap-2">
              <Megaphone className="w-4 h-4 text-amber-600 mt-0.5 shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-medium text-amber-900">最新公告</span>
                  {latestAnnouncement.timestamp && !isNaN(latestAnnouncement.timestamp.getTime()) && (
                    <span className="text-xs text-amber-600">
                      {latestAnnouncement.timestamp.toLocaleString('zh-CN', {
                        month: '2-digit',
                        day: '2-digit',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  )}
                </div>
                <p className="text-sm text-amber-900 line-clamp-2">
                  {latestAnnouncement.content}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 消息列表 */}
      <ScrollArea className="flex-1" style={{ padding: '12px' }} ref={scrollRef}>
        <div className="space-y-3">
          {messages.map((message) => {
            const isOwnMessage = message.userId === currentUser.id;
            const isAnnouncement = message.type === 'announcement';
            const isMention = message.type === 'mention';

            return (
              <div
                key={message.id}
                ref={(el) => {
                  if (el) {
                    messageRefs.current.set(message.id, el);
                  } else {
                    messageRefs.current.delete(message.id);
                  }
                }}
                onContextMenu={(e) => {
                  e.preventDefault();
                  setContextMenu({
                    show: true,
                    x: e.clientX,
                    y: e.clientY,
                    messageId: message.id
                  });
                }}
                className={cn(
                  "group flex gap-2.5 mb-4 transition-colors",
                  isOwnMessage ? "flex-row-reverse" : "flex-row",
                  isAnnouncement && "bg-amber-50/60 px-3 py-2 mx-0 rounded"
                )}
              >
                <Avatar className="w-8 h-8 shrink-0">
                  <AvatarImage src={message.userAvatar} />
                  <AvatarFallback className="text-xs bg-gray-100 text-gray-600">
                    {message.userName[0]}
                  </AvatarFallback>
                </Avatar>

                <div className={cn(
                  "flex flex-col max-w-[70%]",
                  isOwnMessage ? "items-end" : "items-start"
                )}>
                  <div className={cn(
                    "flex items-baseline gap-2 mb-1.5 flex-wrap",
                    isOwnMessage ? "flex-row-reverse" : "flex-row"
                  )}>
                    <span className="text-sm font-medium text-gray-900">{message.userName}</span>

                    {message.userTitle && (
                      <span
                        className="text-xs px-2 py-0.5 rounded"
                        style={{
                          color: message.userTitleColor || '#78716c',
                          backgroundColor: message.userTitleColor ? `${message.userTitleColor}15` : '#fafaf9'
                        }}
                      >
                        {message.userTitle}
                      </span>
                    )}

                    <span className="text-xs text-gray-400">
                      {message.timestamp.toLocaleTimeString('zh-CN', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>

                    {isAnnouncement && (
                      <span className="text-xs text-amber-700 bg-amber-100 px-2 py-0.5 rounded flex items-center gap-1">
                        <Megaphone className="w-3 h-3" />
                        公告
                      </span>
                    )}
                  </div>

                  {/* 消息气泡（包含回复和内容） */}
                  <div className={cn(
                    "rounded-lg inline-block overflow-hidden",
                    isOwnMessage
                      ? "bg-black text-white"
                      : "bg-white border border-gray-200",
                    isMention && !isOwnMessage && "bg-blue-50/80 border-blue-200",
                    isAnnouncement && "bg-amber-100 border-amber-200 text-amber-900"
                  )}>
                    {/* 回复信息 */}
                    {message.replyTo && (
                      <>
                        <div className={cn(
                          "text-xs px-3 py-2",
                          isOwnMessage
                            ? "bg-gray-800 text-gray-300"
                            : "bg-gray-50 text-gray-600"
                        )}>
                          <div className="truncate">
                            <span className="font-medium">{message.replyTo.userName}</span>
                            <span className="opacity-75">：{message.replyTo.content}</span>
                          </div>
                        </div>
                        {/* 分隔线 */}
                        <div className={cn(
                          "h-px",
                          isOwnMessage ? "bg-gray-700" : "bg-gray-200"
                        )} />
                      </>
                    )}

                    {/* 消息内容 */}
                    <div className={cn(
                      "text-sm leading-relaxed px-3 py-2.5",
                      isOwnMessage ? "text-white" : "text-gray-700",
                      isAnnouncement && "text-amber-900"
                    )}>
                      {message.content}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
          {/* 滚动锚点 */}
          <div ref={messagesEndRef} />
        </div>

        {/* 浮动跳转按钮 */}
        <div className="fixed bottom-24 right-8 flex flex-col gap-2 z-10">
          {/* 跳转到@提醒 */}
          {unreadInfo && unreadInfo.mentionCount > 0 && (
            <button
              onClick={jumpToMention}
              className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-full shadow-lg hover:bg-red-600 transition-colors"
              title="跳转到最新@提醒"
            >
              <AtSign className="w-4 h-4" />
              <span className="text-sm">{unreadInfo.mentionCount}</span>
            </button>
          )}

          {/* 跳转到未读消息 */}
          {unreadInfo && unreadInfo.unreadCount > 0 && !isAtBottom && (
            <button
              onClick={jumpToUnread}
              className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-full shadow-lg hover:bg-blue-600 transition-colors"
              title="跳转到第一条未读消息"
            >
              <Mail className="w-4 h-4" />
              <span className="text-sm">{unreadInfo.unreadCount > 99 ? '99+' : unreadInfo.unreadCount}</span>
            </button>
          )}

          {/* 回到底部 */}
          {!isAtBottom && (
            <button
              onClick={scrollToBottom}
              className="flex items-center gap-2 px-4 py-2 bg-gray-700 text-white rounded-full shadow-lg hover:bg-gray-800 transition-colors"
              title="回到底部"
            >
              <ArrowDown className="w-4 h-4" />
              {newMessageCount > 0 && (
                <span className="text-sm">{newMessageCount > 99 ? '99+' : newMessageCount}</span>
              )}
            </button>
          )}
        </div>
      </ScrollArea>

      {/* 输入区域 */}
      <div style={{ padding: '12px', borderTop: '1px solid #f3f4f6', backgroundColor: 'white' }}>
        <div className="space-y-2">
          <div className="flex gap-1">
            <button
              ref={mentionButtonRef}
              onClick={toggleMentionMenu}
              disabled={channel.status === 'locked'}
              className="p-1.5 hover:bg-gray-50 rounded text-gray-500 disabled:opacity-30"
            >
              <AtSign className="w-4 h-4" />
            </button>

            <button
              ref={emojiButtonRef}
              onClick={toggleEmojiPicker}
              className="p-1.5 hover:bg-gray-50 rounded text-gray-500"
            >
              <Smile className="w-4 h-4" />
            </button>

            {canSendAnnouncement && (
              <button
                onClick={() => handleSend('announcement')}
                disabled={!messageInput.trim() || channel.status === 'locked'}
                className="text-xs px-2 py-1 hover:bg-gray-50 rounded text-gray-600 disabled:opacity-30"
              >
                发布公告
              </button>
            )}
          </div>

          {/* 回复预览 */}
          {replyingTo && (
            <div className="flex items-center gap-2 px-3 py-2 bg-blue-50 border-l-2 border-blue-500">
              <Reply className="w-3.5 h-3.5 text-blue-600 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="text-xs text-blue-600 font-medium">
                  回复 {replyingTo.userName}
                </div>
                <div className="text-xs text-gray-600 truncate">
                  {replyingTo.content}
                </div>
              </div>
              <button
                onClick={() => setReplyingTo(null)}
                className="p-1 hover:bg-blue-100 rounded text-blue-600"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

          <div className="flex gap-2">
            <Textarea
              ref={textareaRef}
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                channel.status === 'locked'
                  ? '频道已折叠'
                  : replyingTo
                    ? `回复 ${replyingTo.userName}...`
                    : '输入消息...'
              }
              className="flex-1 min-h-[60px] resize-none text-xs border-gray-200 focus:border-gray-300"
              disabled={channel.status === 'locked'}
            />

            <button
              onClick={() => handleSend()}
              disabled={!messageInput.trim() || channel.status === 'locked'}
              className="self-end px-3 py-2 bg-black text-white rounded hover:bg-gray-800 disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* 表情选择器 */}
      {showEmojiPicker && (
        <>
          {/* 遮罩层 */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setShowEmojiPicker(false)}
          />
          {/* 表情窗口 */}
          <div
            className="fixed bg-white border border-gray-200 rounded-lg shadow-xl emoji-picker z-50 w-80"
            style={{
              left: `${emojiPickerPosition.x}px`,
              top: `${emojiPickerPosition.y}px`
            }}
          >
            <div className="p-3 border-b border-gray-100">
              <h4 className="text-xs text-gray-600">常用表情</h4>
            </div>
            <div className="grid grid-cols-8 gap-1 p-3 max-h-64 overflow-y-auto">
              {emojis.map((emoji, index) => (
                <button
                  key={index}
                  onClick={() => insertEmoji(emoji)}
                  className="text-2xl p-2 hover:bg-gray-50 rounded transition-colors"
                  title={emoji}
                >
                  {emoji}
                </button>
              ))}
            </div>
          </div>
        </>
      )}

      {/* @ 成员选择菜单 */}
      {showMentionMenu && (
        <>
          {/* 遮罩层 */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setShowMentionMenu(false)}
          />
          {/* 成员菜单 */}
          <div
            className="fixed bg-white border border-gray-200 rounded-lg shadow-xl mention-menu z-50 w-64"
            style={{
              left: `${mentionMenuPosition.x}px`,
              top: `${mentionMenuPosition.y}px`,
              transform: 'translateY(-100%)'
            }}
          >
            <div className="p-2 border-b border-gray-100">
              <h4 className="text-xs text-gray-600 px-2">选择要 @ 的成员</h4>
            </div>
            <div className="max-h-64 overflow-y-auto">
              {/* @全体成员选项 */}
              <button
                onClick={() => {
                  insertMention('全体成员');
                  setShowMentionMenu(false);
                }}
                className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 flex items-center gap-2"
              >
                <div className="w-6 h-6 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white text-xs">
                  全
                </div>
                <span className="font-medium">全体成员</span>
              </button>

              {/* 成员列表 */}
              {members.map((member) => (
                <button
                  key={member.id}
                  onClick={() => {
                    insertMention(member.username);
                    setShowMentionMenu(false);
                  }}
                  className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 flex items-center gap-2"
                >
                  <Avatar className="w-6 h-6 shrink-0">
                    <AvatarImage src={member.avatar} />
                    <AvatarFallback className="text-xs bg-gradient-to-br from-blue-400 to-purple-500 text-white">
                      {member.username[0]?.toUpperCase() || 'U'}
                    </AvatarFallback>
                  </Avatar>
                  <span>{member.username}</span>
                  {member.role === 'owner' && (
                    <span className="text-xs text-yellow-600">👑</span>
                  )}
                </button>
              ))}
            </div>
          </div>
        </>
      )}

      {/* 右键消息菜单 */}
      {contextMenu && contextMenu.show && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setContextMenu(null)}
          />
          <div
            className="fixed bg-white border border-gray-200 rounded-lg shadow-xl z-50 py-1 min-w-[140px]"
            style={{
              left: `${contextMenu.x}px`,
              top: `${contextMenu.y}px`
            }}
          >
            {(() => {
              const message = messages.find(m => m.id === contextMenu.messageId);
              const isOwnMessage = message?.userId === currentUser.id;

              // 计算时间差
              let canRecall = false;
              if (message?.timestamp) {
                const messageTime = message.timestamp instanceof Date
                  ? message.timestamp.getTime()
                  : new Date(message.timestamp).getTime();
                const now = Date.now();
                const timeDiff = now - messageTime;
                canRecall = isOwnMessage && timeDiff < 5 * 60 * 1000 && timeDiff >= 0; // 5分钟内

                // 调试信息
                console.log('撤回检查:', {
                  messageTime: new Date(messageTime).toLocaleString(),
                  now: new Date(now).toLocaleString(),
                  timeDiff: Math.floor(timeDiff / 1000) + '秒',
                  canRecall,
                  isOwnMessage
                });
              }

              return (
                <>
                  <button
                    className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 flex items-center gap-2"
                    onClick={() => {
                      if (message) {
                        setReplyingTo(message);
                        textareaRef.current?.focus();
                      }
                      setContextMenu(null);
                    }}
                  >
                    <Reply className="w-3.5 h-3.5" />
                    回复
                  </button>

                  {canRecall && (
                    <button
                      className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 flex items-center gap-2 text-orange-600"
                      onClick={() => {
                        if (window.confirm('确定要撤回这条消息吗？')) {
                          handleRecallMessage(contextMenu.messageId);
                        }
                        setContextMenu(null);
                      }}
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                      撤回
                    </button>
                  )}

                  {!isOwnMessage && (
                    <button
                      className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 flex items-center gap-2 text-red-600"
                      onClick={() => {
                        setReportingMessageId(contextMenu.messageId);
                        setShowReportDialog(true);
                        setContextMenu(null);
                      }}
                    >
                      <AlertCircle className="w-3.5 h-3.5" />
                      举报
                    </button>
                  )}
                </>
              );
            })()}
          </div>
        </>
      )}

      {/* 作品频道侧边栏 */}
      {showSidebar && (
        <>
          {/* 遮罩层 */}
          <div
            className="fixed inset-0 bg-black/20 z-40"
            onClick={() => setShowSidebar(false)}
          />

          {/* 侧边栏 */}
          <div className="fixed right-0 top-0 bottom-0 w-80 bg-white border-l border-gray-200 z-50 flex flex-col shadow-2xl">
            {/* 关闭按钮 */}
            <button
              onClick={() => setShowSidebar(false)}
              className="absolute top-3 right-3 p-1 hover:bg-gray-100 rounded"
            >
              <X className="w-4 h-4 text-gray-400" />
            </button>

            {/* 作品信息 */}
            {channel.type === 'work' && (
              <div className="p-4 border-b border-gray-100">
                <div className="flex gap-3">
                  <div className="w-16 h-22 bg-gray-100 rounded flex-shrink-0 flex items-center justify-center">
                    <span className="text-xs text-gray-400">封面</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm mb-1 truncate">{channel.bookTitle || channel.name}</h3>
                    <p className="text-xs text-gray-500">作者:{channel.author || '佚名'}</p>
                    <p className="text-xs text-gray-400 mt-1">收藏 {channel.collectCount || 0}</p>
                  </div>
                </div>
              </div>
            )}

            {/* 频道信息 */}
            {channel.type !== 'work' && (
              <div className="p-4 border-b border-gray-100">
                <h3 className="text-sm mb-2">{channel.name}</h3>
                <p className="text-xs text-gray-500">{channel.description || '暂无描述'}</p>
              </div>
            )}

            {/* 管理选项 */}
            <div className="flex-1 overflow-y-auto">
              <div className="p-4">
                <h4 className="text-xs text-gray-500 mb-3">频道管理</h4>
                <div className="space-y-1">
                  {/* 粉丝群 - 创作者专属 */}
                  {currentUser.isCreator && channel.type === 'fangroup' && (
                    <>
                      <button
                        onClick={() => setShowMemberDialog(true)}
                        className="w-full flex items-center gap-2 px-3 py-2 text-xs text-left hover:bg-gray-50 rounded"
                      >
                        <Users className="w-3.5 h-3.5" />
                        管理成员
                      </button>
                      <button
                        onClick={onLeaveChannel}
                        className="w-full flex items-center gap-2 px-3 py-2 text-xs text-left hover:bg-red-50 rounded text-red-600"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                        解散频道
                      </button>
                    </>
                  )}

                  {/* 粉丝群 - 普通成员 */}
                  {!currentUser.isCreator && channel.type === 'fangroup' && (
                    <button
                      onClick={onLeaveChannel}
                      className="w-full flex items-center gap-2 px-3 py-2 text-xs text-left hover:bg-red-50 rounded text-red-600"
                    >
                      <X className="w-3.5 h-3.5" />
                      退出频道
                    </button>
                  )}

                  {/* 作品频道 - 都显示退出选项 */}
                  {channel.type === 'work' && (
                    <button
                      onClick={onLeaveChannel}
                      className="w-full flex items-center gap-2 px-3 py-2 text-xs text-left hover:bg-red-50 rounded text-red-600"
                    >
                      <X className="w-3.5 h-3.5" />
                      退出频道
                    </button>
                  )}

                  {/* 官方频道 - 不可退出 */}
                  {channel.type === 'official' && (
                    <p className="text-xs text-gray-400 px-3 py-2">官方频道无法退出</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {/* 成员管理对话框 */}
      <MemberManagementDialog
        isOpen={showMemberDialog}
        onClose={() => setShowMemberDialog(false)}
        channelId={channel.id}
        channelName={channel.name}
        currentUserId={currentUser.id}
        isCreator={currentUser.isCreator || false}
      />

      {/* 举报对话框 */}
      <ReportMessageDialog
        isOpen={showReportDialog}
        onClose={() => {
          setShowReportDialog(false);
          setReportingMessageId('');
        }}
        channelId={channel.id}
        messageId={reportingMessageId}
      />

      {/* 搜索对话框 */}
      {showSearchDialog && (
        <>
          {/* 遮罩层 */}
          <div
            className="fixed inset-0 bg-black/40 z-50"
            onClick={() => {
              setShowSearchDialog(false);
              setSearchKeyword('');
              setSearchResults([]);
            }}
          />

          {/* 搜索弹窗 */}
          <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] max-h-[700px] bg-white rounded-lg shadow-2xl z-50 flex flex-col">
            {/* 头部 */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
              <h3 className="text-base font-medium">搜索消息</h3>
              <button
                onClick={() => {
                  setShowSearchDialog(false);
                  setSearchKeyword('');
                  setSearchResults([]);
                }}
                className="p-1 hover:bg-gray-100 rounded"
              >
                <X className="w-4 h-4 text-gray-400" />
              </button>
            </div>

            {/* 搜索框 */}
            <div className="p-4 border-b border-gray-100">
              <div className="flex gap-2">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="输入关键词搜索..."
                    value={searchKeyword}
                    onChange={(e) => setSearchKeyword(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        handleSearch();
                      }
                    }}
                    className="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 rounded focus:outline-none focus:border-gray-400"
                    autoFocus
                  />
                </div>
                <button
                  onClick={handleSearch}
                  disabled={!searchKeyword.trim() || isSearching}
                  className="px-4 py-2 text-sm bg-black text-white rounded hover:bg-gray-800 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  {isSearching ? '搜索中...' : '搜索'}
                </button>
              </div>
            </div>

            {/* 搜索结果 */}
            <div className="flex-1 overflow-y-auto p-4">
              {searchResults.length === 0 && !isSearching && searchKeyword && (
                <div className="text-center py-12 text-sm text-gray-400">
                  未找到匹配的消息
                </div>
              )}

              {searchResults.length === 0 && !searchKeyword && (
                <div className="text-center py-12 text-sm text-gray-400">
                  输入关键词开始搜索
                </div>
              )}

              {searchResults.length > 0 && (
                <div className="space-y-3">
                  {searchResults.map((message) => (
                    <div
                      key={message.id}
                      onClick={() => {
                        jumpToMessage(message.id);
                        setShowSearchDialog(false);
                        setSearchKeyword('');
                        setSearchResults([]);
                      }}
                      className="p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                    >
                      <div className="flex items-start gap-2 mb-2">
                        <Avatar className="w-6 h-6">
                          <AvatarImage src={message.userAvatar} />
                          <AvatarFallback className="text-xs bg-gray-100 text-gray-600">
                            {message.userName[0]}
                          </AvatarFallback>
                        </Avatar>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-medium">{message.userName}</span>
                            {message.userTitle && (
                              <span
                                className="text-xs px-1.5 py-0.5 rounded"
                                style={{
                                  color: message.userTitleColor || '#78716c',
                                  backgroundColor: message.userTitleColor ? `${message.userTitleColor}15` : '#fafaf9'
                                }}
                              >
                                {message.userTitle}
                              </span>
                            )}
                            <span className="text-xs text-gray-400">
                              {message.timestamp.toLocaleString('zh-CN', {
                                month: '2-digit',
                                day: '2-digit',
                                hour: '2-digit',
                                minute: '2-digit'
                              })}
                            </span>
                          </div>
                        </div>
                      </div>
                      <p className="text-sm text-gray-700 pl-8">{message.content}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
