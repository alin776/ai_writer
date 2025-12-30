import { useState, useRef, useEffect, useCallback } from 'react';
import { Send, AtSign, Megaphone, MoreVertical, Smile, Reply, AlertCircle, X, Users, Trash2, ArrowDown, Mail, Search, Edit2, Pin, Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import type { Channel } from './ChannelList';
import { MemberManagementDialog } from './MemberManagementDialog';
import { ReportMessageDialog } from './ReportMessageDialog';
import { getChannelMembers, type ChannelMember, channelApi, UnreadInfo, type ReactionSummary, type MessageAttachment } from '@/services/channelApi';
import { useChannelWebSocket, type ChannelMessage, type ReactionEvent } from '@/hooks/useChannelWebSocket';
import { TypingIndicator } from './TypingIndicator';
import { MessageReactions } from './MessageReactions';
import EmojiPicker from './EmojiPicker';
import { FileUploader, FilePreview } from './FileUploader';
import MessageAttachments from './MessageAttachments';
import type { MessageEditEvent } from '@/hooks/useChannelWebSocket';

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
  isEdited?: boolean;
  editedAt?: Date;
  replyTo?: {
    id: string;
    userName: string;
    content: string;
  };
  reactions?: ReactionSummary[];
  attachments?: MessageAttachment[]; // 新增附件字段
}

interface ChatAreaProps {
  channel: Channel;
  messages: Message[];
  currentUser: {
    id: string;
    name: string;
    avatar?: string;
    isCreator?: boolean;
    role?: 'owner' | 'admin' | 'member';
  };
  onSendMessage: (content: string, type?: 'normal' | 'announcement', replyToId?: string) => void;
  onSendMessageWithAttachments?: (content: string, attachmentIds: string[], type?: 'normal' | 'announcement', replyToId?: string) => void;
  onMentionAll?: () => void;
  onLeaveChannel?: () => void;
  onNewMessage?: (message: ChannelMessage) => void;
  onMessageDelete?: (messageId: string) => void;
  onMessageEdit?: (event: MessageEditEvent) => void;
  onReactionAdd?: (event: ReactionEvent) => void;
  onReactionRemove?: (event: ReactionEvent) => void;
  onReactionsChange?: (messageId: string, reactions: ReactionSummary[]) => void;
  onPinChange?: () => void;
  scrollToMessageId?: string | null;
  pinnedMessagesBar?: React.ReactNode;
}

export function ChatArea({ channel, messages, currentUser, onSendMessage, onSendMessageWithAttachments, onMentionAll, onLeaveChannel, onNewMessage, onMessageDelete, onMessageEdit, onReactionAdd, onReactionRemove, onReactionsChange, onPinChange, scrollToMessageId, pinnedMessagesBar }: ChatAreaProps) {
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
  const [mentionFilter, setMentionFilter] = useState(''); // @ 后面的过滤词
  const [mentionStartIndex, setMentionStartIndex] = useState(-1); // @ 符号的位置
  const [mentionSelectedIndex, setMentionSelectedIndex] = useState(0); // 键盘选中的索引
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
  const [editingMessage, setEditingMessage] = useState<Message | null>(null);
  const [editContent, setEditContent] = useState('');
  // 附件上传状态
  const [uploadedFiles, setUploadedFiles] = useState<{
    id: string;
    fileName: string;
    fileType?: string;
    fileSize: number;
    fileUrl: string;
    thumbnailUrl?: string;
  }[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const emojiButtonRef = useRef<HTMLButtonElement>(null);
  const mentionButtonRef = useRef<HTMLButtonElement>(null);
  const messageRefs = useRef<Map<string, HTMLDivElement>>(new Map());

  // WebSocket 实时消息
  const { isConnected, typingUsers, onlineUsers, sendTyping } = useChannelWebSocket({
    channelId: channel.id,
    onMessage: onNewMessage,
    onMessageDelete: onMessageDelete,
    onMessageEdit: onMessageEdit,
    onReactionAdd: onReactionAdd,
    onReactionRemove: onReactionRemove
  });

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
    const hasContent = messageInput.trim();
    const hasAttachments = uploadedFiles.length > 0;

    if (!hasContent && !hasAttachments) return;

    // 如果有附件，使用带附件的发送方法
    if (hasAttachments && onSendMessageWithAttachments) {
      const attachmentIds = uploadedFiles.map(f => f.id);
      onSendMessageWithAttachments(messageInput, attachmentIds, type, replyingTo?.id);
      setUploadedFiles([]); // 清空附件
    } else if (hasContent) {
      onSendMessage(messageInput, type, replyingTo?.id);
    }

    setMessageInput('');
    setReplyingTo(null);  // 清除回复状态
  };

  // 计算过滤后的成员列表（用于键盘导航）
  const getFilteredMentionList = useCallback(() => {
    const list: { type: 'all' | 'member'; username: string; member?: ChannelMember }[] = [];

    // @全体成员选项（只有管理员和群主可以使用）
    if ((currentUser.role === 'owner' || currentUser.role === 'admin') &&
        (!mentionFilter || '全体成员'.includes(mentionFilter))) {
      list.push({ type: 'all', username: '全体成员' });
    }

    // 过滤成员（排除自己）
    members
      .filter(member => member.userId !== currentUser.id) // 排除当前用户
      .filter(member => !mentionFilter || member.username.toLowerCase().includes(mentionFilter.toLowerCase()))
      .forEach(member => {
        list.push({ type: 'member', username: member.username, member });
      });

    return list;
  }, [members, mentionFilter, currentUser.role, currentUser.id]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // @ 菜单打开时处理上下键和 Enter
    if (showMentionMenu) {
      const filteredList = getFilteredMentionList();

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setMentionSelectedIndex(prev =>
          prev < filteredList.length - 1 ? prev + 1 : 0
        );
        return;
      }

      if (e.key === 'ArrowUp') {
        e.preventDefault();
        setMentionSelectedIndex(prev =>
          prev > 0 ? prev - 1 : filteredList.length - 1
        );
        return;
      }

      if (e.key === 'Enter' && filteredList.length > 0) {
        e.preventDefault();
        const selected = filteredList[mentionSelectedIndex];
        if (selected) {
          insertMention(selected.username);
          setShowMentionMenu(false);
          setMentionFilter('');
          setMentionStartIndex(-1);
          setMentionSelectedIndex(0);
        }
        return;
      }

      if (e.key === 'Escape') {
        e.preventDefault();
        setShowMentionMenu(false);
        setMentionFilter('');
        setMentionStartIndex(-1);
        setMentionSelectedIndex(0);
        return;
      }
    }

    // 正常的 Enter 发送消息
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // 自动调整 textarea 高度
  const adjustTextareaHeight = useCallback(() => {
    const el = textareaRef.current;
    if (!el) return;

    if (!el.value || el.value.trim() === '') {
      el.style.height = '40px';
      el.style.overflowY = 'hidden';
      return;
    }

    el.style.height = '40px'; // 重置
    const maxH = 200;
    const contentHeight = el.scrollHeight;
    const nextHeight = Math.min(contentHeight, maxH);
    el.style.height = `${Math.max(nextHeight, 40)}px`;
    el.style.overflowY = contentHeight > maxH ? 'auto' : 'hidden';
  }, []);

  // 输入内容变化时调整高度
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    const cursorPos = e.target.selectionStart;
    setMessageInput(newValue);
    adjustTextareaHeight();

    // 发送正在输入事件
    if (newValue.trim()) {
      sendTyping();
    }

    // 检测 @ 符号触发成员选择
    const textBeforeCursor = newValue.substring(0, cursorPos);
    const atMatch = textBeforeCursor.match(/@([^\s@]*)$/);

    if (atMatch) {
      const atIndex = textBeforeCursor.lastIndexOf('@');
      const filter = atMatch[1] || '';

      // 过滤词变化时重置选中索引
      if (filter !== mentionFilter) {
        setMentionSelectedIndex(0);
      }

      setMentionStartIndex(atIndex);
      setMentionFilter(filter);

      // 计算菜单位置（在输入框上方）
      if (textareaRef.current) {
        const rect = textareaRef.current.getBoundingClientRect();
        setMentionMenuPosition({
          x: rect.left,
          y: rect.top - 10
        });
      }
      setShowMentionMenu(true);
    } else {
      // 没有 @ 或者 @ 后面有空格，关闭菜单
      if (showMentionMenu) {
        setShowMentionMenu(false);
        setMentionFilter('');
        setMentionStartIndex(-1);
        setMentionSelectedIndex(0);
      }
    }
  };

  // 发送后重置高度
  useEffect(() => {
    if (!messageInput) {
      adjustTextareaHeight();
    }
  }, [messageInput, adjustTextareaHeight]);

  const insertMention = (username?: string) => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    // 如果是从输入框触发的（mentionStartIndex >= 0），替换 @xxx 部分
    if (mentionStartIndex >= 0) {
      const textBefore = messageInput.substring(0, mentionStartIndex);
      const cursorPos = textarea.selectionStart;
      const textAfter = messageInput.substring(cursorPos);
      const mentionText = username ? `@${username} ` : '@';
      setMessageInput(textBefore + mentionText + textAfter);

      // 重置状态
      setMentionStartIndex(-1);
      setMentionFilter('');
      setMentionSelectedIndex(0);

      setTimeout(() => {
        const newPos = textBefore.length + mentionText.length;
        textarea.setSelectionRange(newPos, newPos);
        textarea.focus();
      }, 0);
    } else {
      // 从按钮触发的，在光标位置插入
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
      // 从按钮触发时，重置过滤词和起始位置
      setMentionFilter('');
      setMentionStartIndex(-1);
      setMentionSelectedIndex(0);
    } else {
      // 关闭时重置
      setMentionFilter('');
      setMentionStartIndex(-1);
      setMentionSelectedIndex(0);
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
      // 表情窗口宽度 320px，高度约 340px
      setEmojiPickerPosition({
        x: buttonRect.left + buttonRect.width / 2 - 160,
        y: buttonRect.top - 350
      });
    }
    setShowEmojiPicker(!showEmojiPicker);
  };

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
        setMentionFilter('');
        setMentionStartIndex(-1);
        setMentionSelectedIndex(0);
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

  // 外部触发跳转（从置顶消息栏点击）
  useEffect(() => {
    if (scrollToMessageId) {
      // 延迟一点确保消息已渲染
      setTimeout(() => jumpToMessage(scrollToMessageId), 100);
    }
  }, [scrollToMessageId]);

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

  // 编辑消息
  const handleEditMessage = async () => {
    if (!editingMessage || !editContent.trim()) return;

    try {
      await channelApi.editMessage(channel.id, editingMessage.id, editContent.trim());
      setEditingMessage(null);
      setEditContent('');
      // WebSocket 会广播更新，无需手动刷新
    } catch (error: any) {
      alert(error.response?.data?.detail || '编辑失败');
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
      className="flex-1 flex flex-col bg-white dark:bg-gray-900 h-full"
      onContextMenu={(e) => {
        // 阻止默认右键菜单，只允许自定义右键菜单
        e.preventDefault();
      }}
    >
      {/* 频道头部 */}
      <div className="p-3 border-b border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-900">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base font-medium dark:text-gray-100">{channel.name}</h3>
              {channel.isPermanent && (
                <span className="text-xs text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/30 px-2 py-1 rounded">永久</span>
              )}
              {channel.type === 'work' && channel.bookTitle && (
                <span className="text-sm text-gray-400 dark:text-gray-500">《{channel.bookTitle}》</span>
              )}
            </div>
            {channel.type === 'work' && channel.collectCount && (
              <p className="text-sm text-gray-400 dark:text-gray-500 mt-1">收藏 {channel.collectCount}</p>
            )}
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setShowSearchDialog(true)}
              className="p-1 hover:bg-gray-50 dark:hover:bg-gray-800 rounded"
              title="搜索消息"
            >
              <Search className="w-4 h-4 text-gray-400 dark:text-gray-500" />
            </button>
            <button
              onClick={() => setShowSidebar(true)}
              className="p-1 hover:bg-gray-50 dark:hover:bg-gray-800 rounded"
            >
              <MoreVertical className="w-4 h-4 text-gray-400 dark:text-gray-500" />
            </button>
          </div>
        </div>

        {/* 状态提示 */}
        {statusInfo.show && (
          <div className={cn(
            "mt-2 px-3 py-2 rounded text-sm",
            statusInfo.variant === 'destructive' && "bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 border border-red-100 dark:border-red-800",
            statusInfo.variant === 'default' && "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 border border-amber-100 dark:border-amber-800",
            statusInfo.variant === 'secondary' && "bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400 border border-gray-100 dark:border-gray-700"
          )}>
            {statusInfo.text}
          </div>
        )}

        {/* 最新公告栏 */}
        {latestAnnouncement && (
          <div
            onClick={() => jumpToMessage(latestAnnouncement.id)}
            className="mt-2 px-3 py-2 rounded bg-amber-50 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-700 cursor-pointer hover:bg-amber-100 dark:hover:bg-amber-900/50 transition-colors"
          >
            <div className="flex items-start gap-2">
              <Megaphone className="w-4 h-4 text-amber-600 dark:text-amber-400 mt-0.5 shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-medium text-amber-900 dark:text-amber-300">最新公告</span>
                  {latestAnnouncement.timestamp && !isNaN(latestAnnouncement.timestamp.getTime()) && (
                    <span className="text-xs text-amber-600 dark:text-amber-400">
                      {latestAnnouncement.timestamp.toLocaleString('zh-CN', {
                        month: '2-digit',
                        day: '2-digit',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  )}
                </div>
                <p className="text-sm text-amber-900 dark:text-amber-300 line-clamp-2">
                  {latestAnnouncement.content}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 置顶消息栏 */}
      {pinnedMessagesBar}

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
                  <AvatarFallback className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
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
                    <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{message.userName}</span>

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

                    <span className="text-xs text-gray-400 dark:text-gray-500">
                      {message.timestamp.toLocaleTimeString('zh-CN', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>

                    {message.isEdited && (
                      <span
                        className="text-xs text-gray-400 dark:text-gray-500 italic cursor-default"
                        title={message.editedAt ? `编辑于 ${message.editedAt.toLocaleString('zh-CN')}` : '已编辑'}
                      >
                        (已编辑)
                      </span>
                    )}

                    {isAnnouncement && (
                      <span className="text-xs text-amber-700 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/50 px-2 py-0.5 rounded flex items-center gap-1">
                        <Megaphone className="w-3 h-3" />
                        公告
                      </span>
                    )}
                  </div>

                  {/* 消息气泡（包含回复和内容） */}
                  <div className={cn(
                    "rounded-lg inline-block overflow-hidden max-w-full",
                    isOwnMessage
                      ? "bg-black dark:bg-gray-700 text-white"
                      : "bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700",
                    isMention && !isOwnMessage && "bg-blue-50/80 dark:bg-blue-900/30 border-blue-200 dark:border-blue-700",
                    isAnnouncement && "bg-amber-100 dark:bg-amber-900/50 border-amber-200 dark:border-amber-700 text-amber-900 dark:text-amber-200"
                  )}>
                    {/* 回复信息 - 点击跳转到原消息 */}
                    {message.replyTo && (
                      <>
                        <div
                          onClick={() => jumpToMessage(message.replyTo!.id)}
                          className={cn(
                            "text-xs px-3 py-2 cursor-pointer hover:opacity-80 transition-opacity flex items-center gap-1 max-w-xs sm:max-w-sm md:max-w-md",
                            isOwnMessage
                              ? "bg-gray-800 dark:bg-gray-600 text-gray-300"
                              : "bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-300"
                          )}
                        >
                          <div className="flex-1 min-w-0 truncate">
                            <span className="font-medium">{message.replyTo.userName}</span>
                            <span className="opacity-75">：{message.replyTo.content}</span>
                          </div>
                          <span className="text-gray-400 dark:text-gray-500 flex-shrink-0">›</span>
                        </div>
                        {/* 分隔线 */}
                        <div className={cn(
                          "h-px",
                          isOwnMessage ? "bg-gray-700 dark:bg-gray-500" : "bg-gray-200 dark:bg-gray-600"
                        )} />
                      </>
                    )}

                    {/* 消息内容（纯附件消息时不显示） */}
                    {message.content && (
                      <div className={cn(
                        "text-sm leading-relaxed px-3 py-2.5 whitespace-pre-wrap break-words",
                        isOwnMessage ? "text-white" : "text-gray-700 dark:text-gray-200",
                        isAnnouncement && "text-amber-900 dark:text-amber-200"
                      )}>
                        {message.content}
                      </div>
                    )}

                    {/* 消息附件 */}
                    {message.attachments && message.attachments.length > 0 && (
                      <div className={cn(
                        "px-3 w-fit",
                        message.content ? "pb-2" : "py-2"  // 纯附件消息时增加上下内边距
                      )}>
                        <MessageAttachments attachments={message.attachments} />
                      </div>
                    )}
                  </div>

                  {/* 消息反应 */}
                  <MessageReactions
                    channelId={channel.id}
                    messageId={message.id}
                    reactions={message.reactions || []}
                    onReactionsChange={(reactions) => onReactionsChange?.(message.id, reactions)}
                  />
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

      {/* 正在输入指示器 */}
      <TypingIndicator typingUsers={typingUsers} />

      {/* 输入区域 */}
      <div className="p-3 bg-white dark:bg-gray-900">
        {/* 回复预览 */}
        {replyingTo && (
          <div className="flex items-center gap-2 px-3 py-2 mb-2 bg-blue-50 dark:bg-blue-900/30 border-l-2 border-blue-500 dark:border-blue-400 rounded-lg">
            <Reply className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400 flex-shrink-0" />
            <div className="flex-1 min-w-0">
              <div className="text-xs text-blue-600 dark:text-blue-400 font-medium">
                回复 {replyingTo.userName}
              </div>
              <div className="text-xs text-gray-600 dark:text-gray-400 truncate">
                {replyingTo.content}
              </div>
            </div>
            <button
              onClick={() => setReplyingTo(null)}
              className="p-1 hover:bg-blue-100 dark:hover:bg-blue-800 rounded text-blue-600 dark:text-blue-400"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* 主输入容器 - AIPanel 风格 */}
        <div className="rounded-2xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 shadow-sm px-4 py-3 space-y-3">
          {/* 已上传文件预览 - 在输入框上方 */}
          <FilePreview
            files={uploadedFiles}
            onRemove={(fileId) => setUploadedFiles(prev => prev.filter(f => f.id !== fileId))}
          />

          {/* 输入框 */}
          <textarea
            ref={textareaRef}
            value={messageInput}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder={
              channel.status === 'locked'
                ? '频道已折叠'
                : replyingTo
                  ? `回复 ${replyingTo.userName}...`
                  : '输入消息...'
            }
            className="min-h-[40px] bg-transparent outline-none border-none text-[13px] placeholder:text-gray-400 dark:placeholder:text-slate-500 resize-none leading-relaxed dark:text-slate-200 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={channel.status === 'locked'}
            rows={1}
            style={{
              width: '100%',
              display: 'block',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
              overflowWrap: 'break-word',
              overflowY: 'hidden',
              overflowX: 'hidden',
            }}
          />

          {/* 底部工具栏 */}
          <div className="flex items-center justify-between">
            {/* 左侧按钮组 */}
            <div className="flex items-center gap-1">
              <button
                ref={mentionButtonRef}
                onClick={toggleMentionMenu}
                disabled={channel.status === 'locked'}
                className="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg text-gray-500 dark:text-slate-400 disabled:opacity-30 transition-colors"
              >
                <AtSign className="w-4 h-4" />
              </button>

              <button
                ref={emojiButtonRef}
                onClick={toggleEmojiPicker}
                className="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg text-gray-500 dark:text-slate-400 transition-colors"
              >
                <Smile className="w-4 h-4" />
              </button>

              {/* 文件上传按钮 */}
              <FileUploader
                channelId={channel.id}
                uploadedFiles={uploadedFiles}
                onFilesUploaded={(files) => setUploadedFiles(prev => [...prev, ...files])}
                disabled={channel.status === 'locked'}
                maxFiles={5}
              />

              {canSendAnnouncement && (
                <button
                  onClick={() => handleSend('announcement')}
                  disabled={(!messageInput.trim() && uploadedFiles.length === 0) || channel.status === 'locked'}
                  className="text-xs px-3 py-1.5 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg text-gray-600 dark:text-slate-400 disabled:opacity-30 transition-colors"
                >
                  发布公告
                </button>
              )}
            </div>

            {/* 右侧发送按钮 */}
            {(messageInput.trim() || uploadedFiles.length > 0) && (
              <button
                onClick={() => handleSend()}
                disabled={(!messageInput.trim() && uploadedFiles.length === 0) || channel.status === 'locked'}
                className="w-10 h-10 rounded-full bg-gray-900 dark:bg-blue-600 text-white flex items-center justify-center hover:bg-gray-800 dark:hover:bg-blue-500 disabled:opacity-30 disabled:cursor-not-allowed transition-all active:scale-95 shadow-sm"
              >
                <Send className="w-4 h-4" />
              </button>
            )}
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
            className="fixed emoji-picker z-50"
            style={{
              left: `${emojiPickerPosition.x}px`,
              top: `${emojiPickerPosition.y}px`
            }}
          >
            <EmojiPicker
              onSelect={insertEmoji}
              onClose={() => setShowEmojiPicker(false)}
            />
          </div>
        </>
      )}

      {/* @ 成员选择菜单 */}
      {showMentionMenu && (() => {
        const filteredList = getFilteredMentionList();
        return (
          <>
            {/* 遮罩层 */}
            <div
              className="fixed inset-0 z-40"
              onClick={() => {
                setShowMentionMenu(false);
                setMentionFilter('');
                setMentionStartIndex(-1);
                setMentionSelectedIndex(0);
              }}
            />
            {/* 成员菜单 */}
            <div
              className="fixed bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl mention-menu z-50 w-64"
              style={{
                left: `${mentionMenuPosition.x}px`,
                top: `${mentionMenuPosition.y}px`,
                transform: 'translateY(-100%)'
              }}
            >
              <div className="p-2 border-b border-gray-100 dark:border-gray-700">
                <h4 className="text-xs text-gray-600 dark:text-gray-400 px-2">
                  选择要 @ 的成员
                  {mentionFilter && <span className="ml-1 text-blue-500">"{mentionFilter}"</span>}
                  <span className="ml-2 text-gray-400">(↑↓选择 Enter确认)</span>
                </h4>
              </div>
              <div className="max-h-64 overflow-y-auto">
                {filteredList.map((item, index) => (
                  <button
                    key={item.type === 'all' ? 'all' : item.member?.id}
                    onClick={() => {
                      insertMention(item.username);
                      setShowMentionMenu(false);
                      setMentionFilter('');
                      setMentionStartIndex(-1);
                      setMentionSelectedIndex(0);
                    }}
                    className={cn(
                      "w-full px-3 py-2 text-xs text-left flex items-center gap-2 dark:text-gray-200 transition-colors",
                      index === mentionSelectedIndex
                        ? "bg-blue-50 dark:bg-blue-900/30"
                        : "hover:bg-gray-50 dark:hover:bg-gray-700"
                    )}
                  >
                    {item.type === 'all' ? (
                      <>
                        <div className="w-6 h-6 bg-blue-500 rounded flex items-center justify-center">
                          <Users className="w-4 h-4 text-white" />
                        </div>
                        <span className="font-medium">全体成员</span>
                      </>
                    ) : (
                      <>
                        <Avatar className="w-6 h-6 shrink-0">
                          <AvatarImage src={item.member?.avatar} />
                          <AvatarFallback className="text-xs bg-gray-800 dark:bg-gray-600 text-white dark:text-gray-300">
                            {item.username[0]?.toUpperCase() || 'U'}
                          </AvatarFallback>
                        </Avatar>
                        <span>{item.username}</span>
                        {item.member?.role === 'owner' && (
                          <span className="text-xs text-yellow-600">👑</span>
                        )}
                      </>
                    )}
                  </button>
                ))}

                {/* 无匹配结果提示 */}
                {filteredList.length === 0 && (
                  <div className="px-3 py-4 text-xs text-gray-400 dark:text-gray-500 text-center">
                    未找到匹配的成员
                  </div>
                )}
              </div>
            </div>
          </>
        );
      })()}

      {/* 右键消息菜单 */}
      {contextMenu && contextMenu.show && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setContextMenu(null)}
          />
          <div
            className="fixed bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl z-50 py-1 min-w-[140px]"
            style={{
              left: `${contextMenu.x}px`,
              top: `${contextMenu.y}px`
            }}
          >
            {(() => {
              const message = messages.find(m => m.id === contextMenu.messageId);
              const isOwnMessage = message?.userId === currentUser.id;
              const canPin = currentUser.role === 'owner' || currentUser.role === 'admin';

              // 计算时间差
              let canRecall = false;
              let canEdit = false;
              if (message?.timestamp) {
                const messageTime = message.timestamp instanceof Date
                  ? message.timestamp.getTime()
                  : new Date(message.timestamp).getTime();
                const now = Date.now();
                const timeDiff = now - messageTime;
                canRecall = isOwnMessage && timeDiff < 5 * 60 * 1000 && timeDiff >= 0; // 5分钟内
                canEdit = isOwnMessage && timeDiff < 10 * 60 * 1000 && timeDiff >= 0; // 10分钟内

                // 调试信息
                console.log('撤回/编辑检查:', {
                  messageTime: new Date(messageTime).toLocaleString(),
                  now: new Date(now).toLocaleString(),
                  timeDiff: Math.floor(timeDiff / 1000) + '秒',
                  canRecall,
                  canEdit,
                  isOwnMessage
                });
              }

              return (
                <>
                  <button
                    className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2 dark:text-gray-200"
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

                  {canEdit && (
                    <button
                      className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2 text-blue-600 dark:text-blue-400"
                      onClick={() => {
                        if (message) {
                          setEditingMessage(message);
                          setEditContent(message.content);
                        }
                        setContextMenu(null);
                      }}
                    >
                      <Edit2 className="w-3.5 h-3.5" />
                      编辑
                    </button>
                  )}

                  {canPin && message && (
                    <button
                      className={`w-full px-3 py-2 text-xs text-left hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2 ${message.isPinned ? 'text-orange-600 dark:text-orange-400' : 'text-amber-600 dark:text-amber-400'}`}
                      onClick={async () => {
                        try {
                          if (message.isPinned) {
                            await channelApi.unpinMessage(channel.id, message.id);
                          } else {
                            await channelApi.pinMessage(channel.id, message.id);
                          }
                          onPinChange?.();
                        } catch (error: any) {
                          alert(error.response?.data?.detail || (message.isPinned ? '取消置顶失败' : '置顶失败'));
                        }
                        setContextMenu(null);
                      }}
                    >
                      <Pin className="w-3.5 h-3.5" />
                      {message.isPinned ? '取消置顶' : '置顶'}
                    </button>
                  )}

                  {canRecall && (
                    <button
                      className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2 text-orange-600 dark:text-orange-400"
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
                      className="w-full px-3 py-2 text-xs text-left hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2 text-red-600 dark:text-red-400"
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
          <div className="fixed right-0 top-0 bottom-0 w-80 bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-700 z-50 flex flex-col shadow-2xl">
            {/* 关闭按钮 */}
            <button
              onClick={() => setShowSidebar(false)}
              className="absolute top-3 right-3 p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded"
            >
              <X className="w-4 h-4 text-gray-400 dark:text-gray-500" />
            </button>

            {/* 作品信息 */}
            {channel.type === 'work' && (
              <div className="p-4 border-b border-gray-100 dark:border-gray-700">
                <div className="flex gap-3">
                  <div className="w-16 h-22 bg-gray-100 dark:bg-gray-800 rounded flex-shrink-0 flex items-center justify-center">
                    <span className="text-xs text-gray-400 dark:text-gray-500">封面</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm mb-1 truncate dark:text-gray-100">{channel.bookTitle || channel.name}</h3>
                    <p className="text-xs text-gray-500 dark:text-gray-400">作者:{channel.author || '佚名'}</p>
                    <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">收藏 {channel.collectCount || 0}</p>
                  </div>
                </div>
              </div>
            )}

            {/* 频道信息 */}
            {channel.type !== 'work' && (
              <div className="p-4 border-b border-gray-100 dark:border-gray-700">
                <h3 className="text-sm mb-2 dark:text-gray-100">{channel.name}</h3>
                <p className="text-xs text-gray-500 dark:text-gray-400">{channel.description || '暂无描述'}</p>
              </div>
            )}

            {/* 管理选项 */}
            <div className="flex-1 overflow-y-auto">
              <div className="p-4">
                <h4 className="text-xs text-gray-500 dark:text-gray-400 mb-3">频道管理</h4>
                <div className="space-y-1">
                  {/* 粉丝群 - 创作者专属 */}
                  {currentUser.isCreator && channel.type === 'fangroup' && (
                    <>
                      <button
                        onClick={() => setShowMemberDialog(true)}
                        className="w-full flex items-center gap-2 px-3 py-2 text-xs text-left hover:bg-gray-50 dark:hover:bg-gray-800 rounded dark:text-gray-200"
                      >
                        <Users className="w-3.5 h-3.5" />
                        管理成员
                      </button>
                      <button
                        onClick={onLeaveChannel}
                        className="w-full flex items-center gap-2 px-3 py-2 text-xs text-left hover:bg-red-50 dark:hover:bg-red-900/30 rounded text-red-600 dark:text-red-400"
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
                      className="w-full flex items-center gap-2 px-3 py-2 text-xs text-left hover:bg-red-50 dark:hover:bg-red-900/30 rounded text-red-600 dark:text-red-400"
                    >
                      <X className="w-3.5 h-3.5" />
                      退出频道
                    </button>
                  )}

                  {/* 作品频道 - 都显示退出选项 */}
                  {channel.type === 'work' && (
                    <button
                      onClick={onLeaveChannel}
                      className="w-full flex items-center gap-2 px-3 py-2 text-xs text-left hover:bg-red-50 dark:hover:bg-red-900/30 rounded text-red-600 dark:text-red-400"
                    >
                      <X className="w-3.5 h-3.5" />
                      退出频道
                    </button>
                  )}

                  {/* 官方频道 - 不可退出 */}
                  {channel.type === 'official' && (
                    <p className="text-xs text-gray-400 dark:text-gray-500 px-3 py-2">官方频道无法退出</p>
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

      {/* 编辑对话框 */}
      {editingMessage && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md">
            {/* 标题栏 */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="text-base font-medium dark:text-gray-100">编辑消息</h3>
              <button
                onClick={() => {
                  setEditingMessage(null);
                  setEditContent('');
                }}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                <X className="w-4 h-4 dark:text-gray-400" />
              </button>
            </div>

            {/* 编辑内容 */}
            <div className="p-4 space-y-4">
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                placeholder="编辑消息内容..."
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                rows={4}
                autoFocus
              />
              <p className="text-xs text-gray-500 dark:text-gray-400">
                提示：只能在发送后10分钟内编辑消息
              </p>
            </div>

            {/* 底部按钮 */}
            <div className="flex items-center justify-end gap-2 p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
              <button
                onClick={() => {
                  setEditingMessage(null);
                  setEditContent('');
                }}
                className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                取消
              </button>
              <button
                onClick={handleEditMessage}
                disabled={!editContent.trim() || editContent.trim() === editingMessage.content}
                className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                保存修改
              </button>
            </div>
          </div>
        </div>
      )}

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
          <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] max-h-[700px] bg-white dark:bg-gray-800 rounded-lg shadow-2xl z-50 flex flex-col">
            {/* 头部 */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
              <h3 className="text-base font-medium dark:text-gray-100">搜索消息</h3>
              <button
                onClick={() => {
                  setShowSearchDialog(false);
                  setSearchKeyword('');
                  setSearchResults([]);
                }}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
              >
                <X className="w-4 h-4 text-gray-400 dark:text-gray-500" />
              </button>
            </div>

            {/* 搜索框 */}
            <div className="p-4 border-b border-gray-100 dark:border-gray-700">
              <div className="flex gap-2">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 dark:text-gray-500" />
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
                    className="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 dark:border-gray-600 rounded focus:outline-none focus:border-gray-400 dark:focus:border-gray-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                    autoFocus
                  />
                </div>
                <button
                  onClick={handleSearch}
                  disabled={!searchKeyword.trim() || isSearching}
                  className="px-4 py-2 text-sm bg-black dark:bg-white text-white dark:text-black rounded hover:bg-gray-800 dark:hover:bg-gray-200 disabled:bg-gray-300 dark:disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors"
                >
                  {isSearching ? '搜索中...' : '搜索'}
                </button>
              </div>
            </div>

            {/* 搜索结果 */}
            <div className="flex-1 overflow-y-auto p-4">
              {searchResults.length === 0 && !isSearching && searchKeyword && (
                <div className="text-center py-12 text-sm text-gray-400 dark:text-gray-500">
                  未找到匹配的消息
                </div>
              )}

              {searchResults.length === 0 && !searchKeyword && (
                <div className="text-center py-12 text-sm text-gray-400 dark:text-gray-500">
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
                      className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                    >
                      <div className="flex items-start gap-2 mb-2">
                        <Avatar className="w-6 h-6">
                          <AvatarImage src={message.userAvatar} />
                          <AvatarFallback className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
                            {message.userName[0]}
                          </AvatarFallback>
                        </Avatar>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-medium dark:text-gray-100">{message.userName}</span>
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
                            <span className="text-xs text-gray-400 dark:text-gray-500">
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
                      <p className="text-sm text-gray-700 dark:text-gray-300 pl-8 whitespace-pre-wrap break-words">{message.content}</p>
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
