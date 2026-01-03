import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, AtSign, Megaphone, MoreVertical, Smile, Reply, AlertCircle, X, Users, Trash2, ArrowDown, Mail, Search, Edit2, Pin, Upload, Star, PanelLeftClose, PanelLeft, Image, MessageCircle, BookOpen, Coffee, FlaskConical, Hash, Forward, BellOff, Bell, UserPlus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { useGlobalStore } from '@/store/globalStore';
import type { Channel } from './ChannelList';
import { MemberManagementDialog } from './MemberManagementDialog';
import { MemberListPanel } from './MemberListPanel';
import { ReportMessageDialog } from './ReportMessageDialog';
import { getChannelMembers, type ChannelMember, channelApi, UnreadInfo, type ReactionSummary, type MessageAttachment, uploadAttachment, getMyChannels, updateChannelSettings, inviteToChannel } from '@/services/channelApi';
import { checkFriendship } from '@/services/friendApi';
import { useChannelWebSocket, type ChannelMessage, type ReactionEvent } from '@/hooks/useChannelWebSocket';
import { TypingIndicator } from './TypingIndicator';
import { MessageReactions } from './MessageReactions';
import EmojiPicker from './EmojiPicker';
import { FileUploader, FilePreview, ALLOWED_TYPES, formatFileSize } from './FileUploader';
import MessageAttachments from './MessageAttachments';
import { ChatSearchPage } from './ChatSearchPage';
import type { MessageEditEvent } from '@/hooks/useChannelWebSocket';
import { addFavoriteSticker } from '@/services/stickerApi';
import { useToast } from '@/hooks/useToast';
import { ToastContainer } from '@/components/ui/Toast';
import { UserProfilePopover } from './UserProfilePopover';
import { MessageActionBar } from './MessageActionBar';
import { ForwardMessageDialog } from './ForwardMessageDialog';
import { ChannelSettingsPanel } from './ChannelSettingsPanel';
import ConfirmDialog from '@/components/common/ConfirmDialog';
import InviteLinkPreview from './InviteLinkPreview';

export interface Message {
  id: string;
  userId: string;
  userName: string;
  userAvatar?: string;
  userBio?: string; // 用户简介
  userTitle?: string; // 用户称号
  userTitleColor?: string; // 称号颜色
  userOnlineStatus?: 'online' | 'idle' | 'dnd' | 'offline'; // 用户在线状态
  content: string;
  timestamp: Date;
  type?: 'normal' | 'announcement' | 'mention';
  isPinned?: boolean;
  isEdited?: boolean;
  editedAt?: Date;
  replyTo?: {
    id: string;
    userName: string;
    userAvatar?: string;  // 被引用用户头像
    userTitle?: string;   // 被引用用户称号
    userTitleColor?: string;  // 称号颜色
    content: string;
  };
  forwardedFrom?: {
    messageId: string;
    channelId: string;
    channelName: string;
    userId?: string;
    userName: string;
    userAvatar?: string;
    content: string;
    createdAt: string;
    attachments?: {
      id: string;
      fileName: string;
      fileType?: string;
      fileUrl: string;
      thumbnailUrl?: string;
    }[];
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
  onInviteToChannel?: () => void;
  onNewMessage?: (message: ChannelMessage) => void;
  onMessageDelete?: (messageId: string) => void;
  onMessageEdit?: (event: MessageEditEvent) => void;
  onReactionAdd?: (event: ReactionEvent) => void;
  onReactionRemove?: (event: ReactionEvent) => void;
  onReactionsChange?: (messageId: string, reactions: ReactionSummary[]) => void;
  onPinChange?: () => void;
  scrollToMessageId?: string | null;
  pinnedMessagesBar?: React.ReactNode;
  isChannelListCollapsed?: boolean;
  onToggleChannelList?: () => void;
  onNavigateToOriginalMessage?: (channelId: string, messageId: string) => void;
  onLoadMessagesAround?: (messageId: string) => Promise<boolean>;  // 加载消息附近的上下文，返回是否成功
}

export function ChatArea({ channel, messages, currentUser, onSendMessage, onSendMessageWithAttachments, onMentionAll, onLeaveChannel, onInviteToChannel, onNewMessage, onMessageDelete, onMessageEdit, onReactionAdd, onReactionRemove, onReactionsChange, onPinChange, scrollToMessageId, pinnedMessagesBar, isChannelListCollapsed, onToggleChannelList, onNavigateToOriginalMessage, onLoadMessagesAround }: ChatAreaProps) {
  const [messageInput, setMessageInput] = useState('');
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [emojiPickerPosition, setEmojiPickerPosition] = useState({ x: 0, y: 0 });
  const [reactionTargetMessageId, setReactionTargetMessageId] = useState<string | null>(null); // 添加反应的目标消息ID
  const [showSidebar, setShowSidebar] = useState(false);
  const [showMemberPanel, setShowMemberPanel] = useState(false); // 成员列表面板
  const [isMuted, setIsMuted] = useState(false); // 频道静音状态
  const [showMemberDialog, setShowMemberDialog] = useState(false);
  const [showReportDialog, setShowReportDialog] = useState(false);
  const [reportingMessageId, setReportingMessageId] = useState<string>('');
  const [forwardingMessage, setForwardingMessage] = useState<{
    id: string;
    content: string;
    sender: string;
    attachments?: MessageAttachment[];
  } | null>(null);
  const [replyingTo, setReplyingTo] = useState<Message | null>(null);
  const [showMentionMenu, setShowMentionMenu] = useState(false);
  const [mentionMenuPosition, setMentionMenuPosition] = useState({ x: 0, y: 0 });
  const [mentionFilter, setMentionFilter] = useState(''); // @ 后面的过滤词
  const [mentionStartIndex, setMentionStartIndex] = useState(-1); // @ 符号的位置
  const [mentionSelectedIndex, setMentionSelectedIndex] = useState(0); // 键盘选中的索引
  const [members, setMembers] = useState<ChannelMember[]>([]);
  const [privateChatPartnerName, setPrivateChatPartnerName] = useState<string | null>(null); // 私聊对方名称
  const [privateChatPartner, setPrivateChatPartner] = useState<ChannelMember | null>(null); // 私聊对方完整信息
  const [contextMenu, setContextMenu] = useState<{
    show: boolean;
    x: number;
    y: number;
    messageId: string;
  } | null>(null);
  const [userContextMenu, setUserContextMenu] = useState<{
    show: boolean;
    x: number;
    y: number;
    userId: string;
    userName: string;
    userAvatar?: string;
    userOnlineStatus?: 'online' | 'idle' | 'dnd' | 'offline';
  } | null>(null);
  const [unreadInfo, setUnreadInfo] = useState<UnreadInfo | null>(null);
  const [isAtBottom, setIsAtBottom] = useState(true);
  const [newMessageCount, setNewMessageCount] = useState(0);
  const [latestAnnouncement, setLatestAnnouncement] = useState<Message | null>(null);
  const [showSearchPage, setShowSearchPage] = useState(false);
  const [editingMessage, setEditingMessage] = useState<Message | null>(null);
  const [editContent, setEditContent] = useState('');
  // 公告编辑状态
  const [showAnnouncementDialog, setShowAnnouncementDialog] = useState(false);
  const [announcementContent, setAnnouncementContent] = useState('');
  // 群名称编辑状态
  const [showEditNameDialog, setShowEditNameDialog] = useState(false);
  const [editingChannelName, setEditingChannelName] = useState('');
  const [announcementFiles, setAnnouncementFiles] = useState<{
    id: string;
    fileName: string;
    fileType?: string;
    fileSize: number;
    fileUrl: string;
    thumbnailUrl?: string;
  }[]>([]);
  // 附件上传状态
  const [uploadedFiles, setUploadedFiles] = useState<{
    id: string;
    fileName: string;
    fileType?: string;
    fileSize: number;
    fileUrl: string;
    thumbnailUrl?: string;
  }[]>([]);
  // 公告删除确认对话框状态
  const [showDeleteAnnouncementDialog, setShowDeleteAnnouncementDialog] = useState(false);
  // 用户隐藏的公告ID（localStorage）
  const [hiddenAnnouncementId, setHiddenAnnouncementId] = useState<string | null>(null);
  // 用户资料弹出卡片状态
  const [userProfilePopover, setUserProfilePopover] = useState<{
    show: boolean;
    userId: string;
    userName: string;
    userAvatar?: string;
    userBio?: string;
    userTitle?: string;
    userTitleColor?: string;
    userOnlineStatus?: 'online' | 'idle' | 'dnd' | 'offline';
    position: { x: number; y: number };
  } | null>(null);
  // 可邀请的频道列表（用于右键菜单）
  const [invitableChannels, setInvitableChannels] = useState<{id: string; name: string; type: string}[]>([]);
  // 删除消息确认弹窗状态
  const [deleteMessageDialog, setDeleteMessageDialog] = useState<{
    show: boolean;
    messageId: string | null;
  }>({ show: false, messageId: null });
  const scrollRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const emojiButtonRef = useRef<HTMLButtonElement>(null);
  const mentionButtonRef = useRef<HTMLButtonElement>(null);
  const messageRefs = useRef<Map<string, HTMLDivElement>>(new Map());
  const { error: showError, warning: showWarning, success: showSuccess } = useGlobalStore();
  const { messages: toastMessages, success: toastSuccess, error: toastError, close: closeToast } = useToast();
  const navigate = useNavigate();

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

        // 私聊频道：找到对方用户并设置显示名称
        if (channel.type === 'private' && response.members.length > 0) {
          const partner = response.members.find(m => m.userId !== currentUser.id);
          if (partner) {
            setPrivateChatPartnerName(partner.fullName || partner.username);
            setPrivateChatPartner(partner); // 保存完整伙伴信息
          }
        } else {
          setPrivateChatPartnerName(null);
          setPrivateChatPartner(null);
        }
      } catch (error) {
        console.error('加载成员列表失败:', error);
      }
    };
    loadMembers();
  }, [channel.id, channel.type, currentUser.id]);

  // 当用户右键菜单打开时，获取可邀请的频道列表
  useEffect(() => {
    if (userContextMenu?.show) {
      const fetchInvitableChannels = async () => {
        try {
          const response = await getMyChannels();
          // 筛选出非私聊、非官方频道（官方频道每个人都在，不需要邀请）
          const channels = response.channels.filter(
            ch => ch.type !== 'private' && ch.type !== 'official'
          ).map(ch => ({
            id: ch.id,
            name: ch.name,
            type: ch.type
          }));
          setInvitableChannels(channels);
        } catch (error) {
          console.error('获取可邀请频道失败:', error);
          setInvitableChannels([]);
        }
      };
      fetchInvitableChannels();
    }
  }, [userContextMenu?.show]);

  // 用户进入频道时自动标记为已读
  useEffect(() => {
    // 延迟一点让消息加载完成，然后标记已读
    const timer = setTimeout(async () => {
      await channelApi.markChannelAsRead(channel.id);
      // 标记已读后清除未读信息，让分割线消失
      setUnreadInfo(prev => prev ? { ...prev, unreadCount: 0, mentionCount: 0 } : null);
    }, 500);
    return () => clearTimeout(timer);
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

  // 从 localStorage 加载用户隐藏的公告ID
  useEffect(() => {
    const storedHiddenId = localStorage.getItem(`hidden_announcement_${channel.id}`);
    setHiddenAnnouncementId(storedHiddenId);
  }, [channel.id]);

  // 处理公告关闭按钮点击
  const handleAnnouncementClose = () => {
    const isAdmin = currentUser.role === 'owner' || currentUser.role === 'admin';

    if (isAdmin) {
      // 管理员：显示确认对话框
      setShowDeleteAnnouncementDialog(true);
    } else {
      // 普通用户：直接隐藏公告（存储到localStorage）
      if (latestAnnouncement) {
        localStorage.setItem(`hidden_announcement_${channel.id}`, latestAnnouncement.id);
        setHiddenAnnouncementId(latestAnnouncement.id);
      }
    }
  };

  // 管理员确认删除公告
  const handleConfirmDeleteAnnouncement = async () => {
    if (!latestAnnouncement) return;

    try {
      await channelApi.recallMessage(channel.id, latestAnnouncement.id);
      setLatestAnnouncement(null);
      setShowDeleteAnnouncementDialog(false);
    } catch (error) {
      console.error('删除公告失败:', error);
      showError('删除公告失败');
    }
  };

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

  // 发送公告（从公告编辑对话框）
  const handleSendAnnouncement = () => {
    const hasContent = announcementContent.trim();
    const hasAttachments = announcementFiles.length > 0;

    if (!hasContent && !hasAttachments) return;

    // 如果有附件，使用带附件的发送方法
    if (hasAttachments && onSendMessageWithAttachments) {
      const attachmentIds = announcementFiles.map(f => f.id);
      onSendMessageWithAttachments(announcementContent, attachmentIds, 'announcement');
    } else if (hasContent) {
      onSendMessage(announcementContent, 'announcement');
    }

    // 清空并关闭对话框
    setAnnouncementContent('');
    setAnnouncementFiles([]);
    setShowAnnouncementDialog(false);
  };

  // 处理私信发送（从用户名片）
  const handleStartPrivateChat = async (targetUserId: string, message: string, privateChannelId: string) => {
    try {
      // 直接使用传入的 privateChannelId，避免重复查询好友关系
      await channelApi.sendMessage(privateChannelId, message, 'normal');

      // 导航到私聊频道
      navigate(`/channels?channelId=${privateChannelId}`);
      showSuccess('私信已发送');
    } catch (error) {
      console.error('发送私信失败:', error);
      showError('发送私信失败，请稍后重试');
    }
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

  // 处理粘贴事件 - 支持粘贴图片和文件
  const handlePaste = async (e: React.ClipboardEvent<HTMLTextAreaElement>) => {
    const files = e.clipboardData?.files;
    if (!files || files.length === 0) return;

    // 检查是否有文件被粘贴
    const fileArray = Array.from(files);
    const validFiles = fileArray.filter(file => ALLOWED_TYPES.includes(file.type));

    if (validFiles.length === 0) {
      // 如果粘贴的不是支持的文件类型，让默认的文本粘贴行为继续
      return;
    }

    // 阻止默认粘贴行为（因为我们要处理文件）
    e.preventDefault();

    // 检查文件数量限制
    const maxFiles = 5;
    const maxFileSize = 10 * 1024 * 1024; // 10MB
    const remainingSlots = maxFiles - uploadedFiles.length;

    if (remainingSlots <= 0) {
      showWarning(`最多只能上传 ${maxFiles} 个文件`);
      return;
    }

    const filesToUpload = validFiles.slice(0, remainingSlots);
    if (validFiles.length > remainingSlots) {
      showWarning(`最多只能上传 ${maxFiles} 个文件，已自动截取前 ${remainingSlots} 个`);
    }

    // 上传文件
    for (const file of filesToUpload) {
      // 验证文件大小
      if (file.size > maxFileSize) {
        showError(`文件 ${file.name} 大小超过限制（最大 ${formatFileSize(maxFileSize)}）`);
        continue;
      }

      try {
        const response = await uploadAttachment(channel.id, file);
        const uploadedFile = {
          id: response.id,
          fileName: response.fileName || file.name,
          fileType: response.fileType || file.type,
          fileSize: response.fileSize || file.size,
          fileUrl: response.fileUrl || '',
          thumbnailUrl: response.thumbnailUrl,
        };
        setUploadedFiles(prev => [...prev, uploadedFile]);
      } catch (err) {
        showError(`上传失败: ${file.name}`);
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

  const insertEmoji = async (emoji: string) => {
    // 如果是添加反应模式
    if (reactionTargetMessageId) {
      try {
        await channelApi.addReaction(channel.id, reactionTargetMessageId, emoji);
      } catch (e) {
        console.error('添加反应失败', e);
      }
      setReactionTargetMessageId(null);
      setShowEmojiPicker(false);
      return;
    }

    // 否则是插入文字模式
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

  // 处理贴图选择 - 发送贴图消息
  const handleStickerSelect = (stickerUrl: string) => {
    // 发送贴图作为图片消息
    const stickerMessage = `![sticker](${stickerUrl})`;
    if (onSendMessage) {
      onSendMessage(stickerMessage, 'normal', replyingTo?.id);
      setReplyingTo(null);
    }
    setShowEmojiPicker(false);
  };

  const toggleEmojiPicker = () => {
    if (!showEmojiPicker && emojiButtonRef.current) {
      const buttonRect = emojiButtonRef.current.getBoundingClientRect();
      // 表情窗口宽度 320px，高度 384px
      setEmojiPickerPosition({
        x: buttonRect.left + buttonRect.width / 2 - 160,
        y: buttonRect.top - 400
      });
    }
    setShowEmojiPicker(!showEmojiPicker);
  };

  // 点击外部关闭表情选择器和 @ 菜单
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      // 排除裁剪器对话框的点击（Portal 渲染到 body）
      const target = event.target as Element;
      if (target.closest('[role="dialog"]')) {
        return;
      }

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
    return { show: false };
  };

  // 渲染消息内容，支持 @用户名 高亮和贴图图片、链接点击
  const renderMessageContent = (content: string, isOwnMessage: boolean, onMentionClick?: (username: string, e: React.MouseEvent) => void) => {
    // 先检查是否是纯贴图消息 ![sticker](url)
    const stickerOnlyMatch = content.match(/^!\[sticker\]\((.+)\)$/);
    if (stickerOnlyMatch) {
      return (
        <img
          src={stickerOnlyMatch[1]}
          alt="sticker"
          className="max-w-[100px] max-h-[100px] rounded"
          loading="lazy"
        />
      );
    }

    // 处理混合内容：图片 + 文本 + @提及 + 链接
    // 合并正则匹配
    // 注意：用户名可能包含@（如邮箱），所以匹配到空格为止，而不是在@处停止
    // 添加链接匹配：https?://开头的URL
    const combinedRegex = /!\[([^\]]*)\]\(([^)]+)\)|@([^\s]+)|(https?:\/\/[^\s]+)/g;
    const parts: (string | React.ReactNode)[] = [];
    let lastIndex = 0;
    let match;
    let keyIndex = 0;

    while ((match = combinedRegex.exec(content)) !== null) {
      // 添加匹配之前的普通文本
      if (match.index > lastIndex) {
        parts.push(content.slice(lastIndex, match.index));
      }

      if (match[0].startsWith('![')) {
        // 图片匹配
        const alt = match[1] || 'image';
        const url = match[2];
        parts.push(
          <img
            key={`img-${keyIndex++}`}
            src={url}
            alt={alt}
            className="inline-block max-w-[100px] max-h-[100px] rounded align-middle"
            loading="lazy"
          />
        );
      } else if (match[0].startsWith('@')) {
        // @提及匹配 - 可点击显示用户名片
        const username = match[3];
        parts.push(
          <span
            key={`mention-${keyIndex++}`}
            className="inline-flex items-center px-1 rounded font-medium bg-cyan-100 dark:bg-cyan-900/40 text-cyan-700 dark:text-cyan-300 cursor-pointer hover:bg-cyan-200 dark:hover:bg-cyan-800/50 leading-normal"
            onClick={(e) => {
              e.stopPropagation();
              onMentionClick?.(username, e);
            }}
          >
            @{username}
          </span>
        );
      } else if (match[4]) {
        // 链接匹配
        const url = match[4];
        // 检测是否是邀请链接 - 格式: /invite/{code}
        // 邀请码可能包含字母、数字、- 和 _
        const inviteMatch = url.match(/\/invite\/([a-zA-Z0-9_-]+)/);
        if (inviteMatch) {
          const inviteCode = inviteMatch[1];
          parts.push(
            <InviteLinkPreview
              key={`invite-${keyIndex++}`}
              inviteCode={inviteCode}
              inviteUrl={url}
            />
          );
        } else {
          parts.push(
            <a
              key={`link-${keyIndex++}`}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 dark:text-blue-400 hover:underline"
              onClick={(e) => e.stopPropagation()}
            >
              {url}
            </a>
          );
        }
      }
      lastIndex = match.index + match[0].length;
    }

    // 添加剩余的普通文本
    if (lastIndex < content.length) {
      parts.push(content.slice(lastIndex));
    }

    return parts.length > 0 ? parts : content;
  };

  // 跳转到指定消息
  const jumpToMessage = async (messageId: string) => {
    const element = messageRefs.current.get(messageId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      // 高亮效果
      element.classList.add('highlight-message');
      setTimeout(() => element.classList.remove('highlight-message'), 2000);
    } else {
      // 消息不在当前加载的列表中，尝试加载
      console.log('[ChatArea] 消息不在当前列表中，尝试加载:', messageId);
      if (onLoadMessagesAround) {
        const success = await onLoadMessagesAround(messageId);
        if (success) {
          // 加载成功后，延迟执行跳转（等待渲染完成）
          setTimeout(() => {
            const newElement = messageRefs.current.get(messageId);
            if (newElement) {
              newElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
              newElement.classList.add('highlight-message');
              setTimeout(() => newElement.classList.remove('highlight-message'), 2000);
            }
          }, 200);
        } else {
          showWarning('消息加载失败，请稍后重试');
        }
      } else {
        showWarning('该消息不在当前页面，请向上滚动加载更多消息');
      }
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
      // 清除未读信息，让分割线和跳转按钮消失
      setUnreadInfo(prev => prev ? { ...prev, unreadCount: 0 } : null);
    }
  };

  // 跳转到@提醒
  const jumpToMention = () => {
    console.log('[ChatArea] jumpToMention called, unreadInfo:', unreadInfo);
    if (unreadInfo?.latestMentionMessageId) {
      console.log('[ChatArea] Jumping to mention message:', unreadInfo.latestMentionMessageId);
      jumpToMessage(unreadInfo.latestMentionMessageId);
      // 跳转后清除本地 mentionCount，让按钮消失
      setUnreadInfo(prev => prev ? { ...prev, mentionCount: 0 } : null);
    } else {
      console.warn('[ChatArea] No latestMentionMessageId found');
      showWarning('未找到@消息');
    }
  };

  // 回到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    setNewMessageCount(0);
    // 标记所有消息为已读
    channelApi.markChannelAsRead(channel.id);
    // 清除未读信息
    setUnreadInfo(prev => prev ? { ...prev, unreadCount: 0, mentionCount: 0 } : null);
  };

  // 快速添加表情反应
  const handleQuickReact = async (messageId: string, emoji: string) => {
    try {
      await channelApi.addReaction(channel.id, messageId, emoji);
    } catch (error: any) {
      console.error('添加反应失败:', error);
      showError(error.response?.data?.detail || '添加反应失败');
    }
  };

  // 判断是否是连续消息（同用户、5分钟内、非特殊消息）
  const isContinuation = (current: Message, previous: Message | null): boolean => {
    if (!previous) return false;
    if (current.userId !== previous.userId) return false;
    if (current.type === 'announcement' || previous.type === 'announcement') return false;
    if (current.replyTo) return false; // 有回复的消息打断连续

    const currentTime = current.timestamp instanceof Date
      ? current.timestamp.getTime()
      : new Date(current.timestamp).getTime();
    const previousTime = previous.timestamp instanceof Date
      ? previous.timestamp.getTime()
      : new Date(previous.timestamp).getTime();

    // 5分钟内的消息算连续
    return currentTime - previousTime < 5 * 60 * 1000;
  };

  // 删除消息
  const handleRecallMessage = async (messageId: string) => {
    try {
      await channelApi.recallMessage(channel.id, messageId);
      // WebSocket 会广播删除事件，父组件通过 onMessageDelete 回调更新消息列表
      showSuccess('消息已删除');
    } catch (error: any) {
      showError(error.response?.data?.detail || '删除失败');
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

  const statusInfo = getChannelStatusInfo();
  // 发布公告权限：粉丝群创建者 或 官方频道的群主/管理员 或 作品群的作者
  const canSendAnnouncement =
    (currentUser.isCreator && channel.type === 'fangroup') ||
    (channel.type === 'official' && (currentUser.role === 'owner' || currentUser.role === 'admin')) ||
    (channel.type === 'work' && currentUser.role === 'owner');

  return (
    <>
      {/* 高亮动画样式 */}
      <style>{`
        @keyframes highlight-fade {
          0% { background-color: rgba(59, 130, 246, 0.2); }
          100% { background-color: transparent; }
        }
        .highlight-message {
          animation: highlight-fade 2s ease-out;
        }
      `}</style>

      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* 频道头部 - 横跨整个宽度 */}
        <div className="p-3 border-b border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-900 flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                {/* 展开/收缩图标 */}
                <button
                  onClick={onToggleChannelList}
                  className="p-1 -ml-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded transition-colors"
                  title={isChannelListCollapsed ? "展开频道列表" : "收起频道列表"}
                >
                  {isChannelListCollapsed ? (
                    <PanelLeft className="w-4 h-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
                  ) : (
                    <PanelLeftClose className="w-4 h-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
                  )}
                </button>
                <h3 className="text-base font-medium dark:text-gray-100 truncate" title={channel.type === 'private' ? (privateChatPartnerName || '私聊') : channel.name}>
                  {channel.type === 'private' ? (privateChatPartnerName || '私聊') : channel.name}
                </h3>
                {channel.isPermanent && channel.type !== 'private' && (
                  <span className="text-xs text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/30 px-2 py-1 rounded">永久</span>
                )}
              </div>
            </div>
            <div className="flex items-center gap-1">
              {/* 邀请至频道按钮 - 非私聊频道显示 */}
              {channel.type !== 'private' && (
                <button
                  onClick={onInviteToChannel}
                  className="p-1.5 rounded transition-colors hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-400 dark:text-gray-500"
                  title="邀请至频道"
                >
                  <UserPlus className="w-4 h-4" />
                </button>
              )}
              {/* 频道静音按钮 - 非私聊频道显示 */}
              {channel.type !== 'private' && (
                <button
                  onClick={() => setIsMuted(!isMuted)}
                  className={cn(
                    "p-1.5 rounded transition-colors",
                    isMuted
                      ? "bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200"
                      : "hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-400 dark:text-gray-500"
                  )}
                  title={isMuted ? "取消静音" : "频道静音"}
                >
                  {isMuted ? <BellOff className="w-4 h-4" /> : <Bell className="w-4 h-4" />}
                </button>
              )}
              {/* 成员列表按钮 - 非私聊频道显示 */}
              {channel.type !== 'private' && (
                <button
                  onClick={() => setShowMemberPanel(!showMemberPanel)}
                  className={cn(
                    "p-1.5 rounded transition-colors",
                    showMemberPanel
                      ? "bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200"
                      : "hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-400 dark:text-gray-500"
                  )}
                  title={showMemberPanel ? "隐藏成员名单" : "显示成员名单"}
                >
                  <Users className="w-4 h-4" />
                </button>
              )}
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
            statusInfo.variant === 'default' && "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 border border-amber-100 dark:border-amber-800"
          )}>
            {statusInfo.text}
          </div>
        )}

        {/* 最新公告栏 - 紧凑单行样式 */}
        {latestAnnouncement && hiddenAnnouncementId !== latestAnnouncement.id && (
          <div
            className="mt-2 flex items-center gap-2 px-3 py-2 rounded-lg bg-amber-50 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-700 cursor-pointer hover:bg-amber-100 dark:hover:bg-amber-900/50 transition-colors"
            onClick={() => {
              jumpToMessage(latestAnnouncement.id);
              // 普通用户点击跳转后自动隐藏公告栏
              if (currentUser.role !== 'owner' && currentUser.role !== 'admin') {
                localStorage.setItem(`hidden_announcement_${channel.id}`, latestAnnouncement.id);
                setHiddenAnnouncementId(latestAnnouncement.id);
              }
            }}
          >
            <Megaphone className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
            <span className="text-xs font-medium text-amber-700 dark:text-amber-300 shrink-0">最新公告</span>
            <span className="text-xs text-amber-600 dark:text-amber-400 shrink-0">
              {latestAnnouncement.timestamp && !isNaN(latestAnnouncement.timestamp.getTime()) &&
                latestAnnouncement.timestamp.toLocaleString('zh-CN', {
                  month: '2-digit',
                  day: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit'
                })
              }
            </span>
            <p className="flex-1 text-sm text-amber-900 dark:text-amber-300 truncate min-w-0">
              {latestAnnouncement.content}
            </p>
            {/* 关闭按钮 - 管理员红色（删除），普通用户琥珀色（隐藏） */}
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleAnnouncementClose();
              }}
              className={cn(
                "p-1.5 rounded transition-colors flex-shrink-0",
                currentUser.role === 'owner' || currentUser.role === 'admin'
                  ? "hover:bg-red-100 dark:hover:bg-red-900/30 text-red-500 dark:text-red-400"
                  : "hover:bg-amber-200 dark:hover:bg-amber-800 text-amber-600 dark:text-amber-400"
              )}
              title={currentUser.role === 'owner' || currentUser.role === 'admin' ? '删除公告' : '关闭'}
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        )}
        </div>

        {/* 内容区域 - 聊天消息 + 成员列表面板 */}
        <div className="flex-1 flex overflow-hidden">
          {/* 聊天内容区域 */}
          <div
            className="flex-1 flex flex-col bg-white dark:bg-gray-900 min-w-0 relative"
            onContextMenu={(e) => {
              e.preventDefault();
            }}
          >
      {/* 置顶消息栏 */}
      {pinnedMessagesBar}

      {/* 消息列表 */}
      <ScrollArea className="flex-1" style={{ padding: '12px' }} ref={scrollRef}>
        <div className="space-y-3">
          {/* 频道欢迎区域 - Discord 风格 */}
          {channel.type !== 'private' && (
            <div className="px-4 pt-6 pb-4">
              {/* 频道图标 */}
              {(() => {
                // 官方频道使用矢量图标
                if (channel.type === 'official') {
                  let IconComponent = Hash;
                  if (channel.name.includes('公共酒馆')) IconComponent = MessageCircle;
                  else if (channel.name.includes('作者酒馆')) IconComponent = BookOpen;
                  else if (channel.name.includes('读者茶馆')) IconComponent = Coffee;
                  else if (channel.name.includes('官方实验室')) IconComponent = FlaskConical;

                  return (
                    <div className="w-[68px] h-[68px] flex items-center justify-center mb-4">
                      <IconComponent className="w-14 h-14 text-gray-500 dark:text-gray-400" strokeWidth={1.5} />
                    </div>
                  );
                }

                // 其他频道使用封面图或首字母
                return (
                  <div className="w-[68px] h-[68px] rounded-full bg-gray-100 dark:bg-[#36393f] flex items-center justify-center mb-4 overflow-hidden">
                    {channel.coverImage ? (
                      <img
                        src={channel.coverImage}
                        alt={channel.name}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <span className="text-2xl text-gray-600 dark:text-gray-300 font-bold">
                        {channel.name.charAt(0).toUpperCase()}
                      </span>
                    )}
                  </div>
                );
              })()}

              {/* 欢迎标题 */}
              <h1 className="text-[32px] font-bold text-gray-900 dark:text-white mb-2 leading-tight">
                欢迎来到 {channel.name}！
              </h1>

              {/* 频道起点描述 */}
              <p className="text-gray-500 dark:text-[#96989d] text-base leading-relaxed">
                这是 <span className="font-medium">{channel.name}</span> 频道的起点。
                {channel.description && (
                  <span className="ml-1">{channel.description}</span>
                )}
              </p>
            </div>
          )}

          {/* 私信频道欢迎区域 - 显示对方用户信息 */}
          {channel.type === 'private' && privateChatPartner && (
            <div className="px-4 pt-6 pb-4">
              {/* 用户头像 */}
              <div className="w-[68px] h-[68px] rounded-full bg-gray-100 dark:bg-[#36393f] flex items-center justify-center mb-4 overflow-hidden">
                {privateChatPartner.avatar ? (
                  <img
                    src={privateChatPartner.avatar}
                    alt={privateChatPartnerName || '用户'}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <span className="text-2xl text-gray-600 dark:text-gray-300 font-bold">
                    {(privateChatPartnerName || '用户').charAt(0).toUpperCase()}
                  </span>
                )}
              </div>

              {/* 用户名 */}
              <h1 className="text-[32px] font-bold text-gray-900 dark:text-white mb-2 leading-tight">
                {privateChatPartnerName || '用户'}
              </h1>

              {/* 私信起点描述 */}
              <p className="text-gray-500 dark:text-[#96989d] text-base leading-relaxed">
                这是您与 <span className="font-medium">{privateChatPartnerName || '用户'}</span> 私信记录的开头。
              </p>
            </div>
          )}

          {messages.map((message, index) => {
            const previousMessage = index > 0 ? messages[index - 1] : null;
            const isOwnMessage = message.userId === currentUser.id;
            const isAnnouncement = message.type === 'announcement';
            const isMention = message.type === 'mention';
            // 检测是否是纯贴图消息
            const isStickerOnly = message.content && /^!\[sticker\]\(.+\)$/.test(message.content);
            // 检测是否是纯附件消息（没有文字，只有附件）- 不需要边框和背景
            const isMediaOnly = !message.content && message.attachments && message.attachments.length > 0;
            // 不需要边框的情况：纯贴图 或 纯附件
            const noBorder = isStickerOnly || isMediaOnly;
            // 是否是连续消息
            const isContinuationMessage = isContinuation(message, previousMessage);
            const isBeingRepliedTo = replyingTo?.id === message.id; // 是否正在被回复
            // 是否是第一条未读消息
            const isFirstUnread = unreadInfo?.firstUnreadMessageId === message.id && unreadInfo?.unreadCount > 0;

            return (
              <React.Fragment key={message.id}>
                {/* 未读消息分割线 - 显示在第一条未读消息前 */}
                {isFirstUnread && (
                  <div className="relative flex items-center justify-center py-2 px-4">
                    <div className="absolute inset-0 flex items-center px-4">
                      <div className="w-full border-t border-red-300 dark:border-red-800" />
                    </div>
                    <span className="relative px-3 text-xs font-medium text-red-500 dark:text-red-400 bg-white dark:bg-gray-900">
                      {(() => {
                        const date = message.timestamp instanceof Date
                          ? message.timestamp
                          : new Date(message.timestamp);
                        return date.toLocaleDateString('zh-CN', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        });
                      })()}
                    </span>
                  </div>
                )}
              <div
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
                  "group relative px-4 transition-colors",
                  "hover:bg-black/[0.02] dark:hover:bg-white/[0.02]",
                  isContinuationMessage ? "py-0.5" : "py-1",
                  message.replyTo && "mt-2", // 有回复时增加顶部边距
                  isAnnouncement && "bg-amber-50/60 dark:bg-amber-900/30 rounded",
                  isBeingRepliedTo && "bg-purple-50 dark:bg-purple-900/20 rounded" // 被回复的消息浅紫色背景
                )}
              >
                {/* 回复引用区域 - 显示在消息上方，独立一行 */}
                {message.replyTo && (
                  <>
                    {/* SVG 连接线 */}
                    <svg
                      className="absolute left-[16px] top-[6px] w-[52px] h-[18px]"
                      style={{ pointerEvents: 'none' }}
                    >
                      <path
                        d="M 20 16 L 20 6 Q 20 2 24 2 L 50 2"
                        fill="none"
                        stroke="#a3a6aa"
                        className="dark:stroke-gray-600"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                    </svg>

                    {/* 引用区域 */}
                    <div
                      className="flex items-center gap-1.5 text-gray-500 dark:text-gray-400 text-sm cursor-pointer hover:text-gray-700 dark:hover:text-gray-300 ml-[52px] -mt-1.5"
                      onClick={() => jumpToMessage(message.replyTo!.id)}
                    >
                      {/* 被引用用户小头像 */}
                      <img
                        src={message.replyTo.userAvatar || message.userAvatar || '/default-avatar.png'}
                        alt={message.replyTo.userName}
                        className="w-4 h-4 rounded-full"
                        onError={(e) => {
                          (e.target as HTMLImageElement).src = '/default-avatar.png';
                        }}
                      />

                      {/* 被引用用户名 */}
                      <span className="text-gray-600 dark:text-gray-300 hover:underline font-medium">
                        @{message.replyTo.userName}
                      </span>

                      {/* 被引用内容摘要 - 过滤 markdown 格式 */}
                      <span className="truncate text-gray-400 dark:text-gray-500 max-w-[200px] flex items-center gap-1">
                        {/* 检测是否包含图片 */}
                        {/!\[.*?\]\(.*?\)/.test(message.replyTo.content) && (
                          <Image className="w-4 h-4 inline-block flex-shrink-0" />
                        )}
                        <span className="truncate">
                          {message.replyTo.content
                            .replace(/!\[.*?\]\(.*?\)/g, '')  // 移除图片标记
                            .replace(/\[.*?\]\(.*?\)/g, '[链接]')   // 替换链接为 [链接]
                            .trim()
                          }
                        </span>
                      </span>
                    </div>
                  </>
                )}

                {/* 主消息区域 - 头像 + 内容 */}
                <div className={cn(
                  "flex items-start",
                  message.replyTo ? "gap-3" : "gap-4"
                )}>
                {/* 头像区域 - 连续消息时显示时间占位 */}
                {isContinuationMessage ? (
                  <div className="w-10 flex-shrink-0 flex items-center justify-center">
                    <span className="text-gray-400 text-[11px] opacity-0 group-hover:opacity-100 transition-opacity">
                      {message.timestamp.toLocaleTimeString('zh-CN', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  </div>
                ) : (
                  <div
                    className="shrink-0 cursor-pointer mt-0.5"
                    onClick={(e) => {
                      e.stopPropagation();
                      setUserProfilePopover({
                        show: true,
                        userId: message.userId,
                        userName: message.userName,
                        userAvatar: message.userAvatar,
                        userBio: message.userBio,
                        userTitle: message.userTitle,
                        userTitleColor: message.userTitleColor,
                        userOnlineStatus: message.userOnlineStatus,
                        position: { x: e.clientX, y: e.clientY },
                      });
                    }}
                    onContextMenu={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      // 不显示自己的用户菜单
                      if (message.userId === currentUser.id) return;
                      setUserContextMenu({
                        show: true,
                        x: e.clientX,
                        y: e.clientY,
                        userId: message.userId,
                        userName: message.userName,
                        userAvatar: message.userAvatar,
                        userOnlineStatus: message.userOnlineStatus,
                      });
                    }}
                  >
                    <Avatar className="w-10 h-10 hover:ring-2 hover:ring-blue-400 transition-all">
                      <AvatarImage src={message.userAvatar} />
                      <AvatarFallback className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
                        {message.userName[0]}
                      </AvatarFallback>
                    </Avatar>
                  </div>
                )}

                <div className="flex-1 flex flex-col min-w-0">
                  {/* 用户信息栏 - 连续消息时隐藏 */}
                  {!isContinuationMessage && (
                    <div className="flex items-center gap-2 mb-0.5">
                    <span
                      className="text-gray-900 dark:text-gray-100 font-medium hover:underline cursor-pointer"
                      onClick={(e) => {
                        e.stopPropagation();
                        setUserProfilePopover({
                          show: true,
                          userId: message.userId,
                          userName: message.userName,
                          userAvatar: message.userAvatar,
                          userBio: message.userBio,
                          userTitle: message.userTitle,
                          userTitleColor: message.userTitleColor,
                          userOnlineStatus: message.userOnlineStatus,
                          position: { x: e.clientX, y: e.clientY },
                        });
                      }}
                    >
                      {message.userName}
                    </span>

                    {message.userTitle && (
                      <span
                        className="inline-flex items-center gap-0.5 text-[10px] px-1 rounded-[3px] font-medium text-white"
                        style={{ backgroundColor: message.userTitleColor || '#248046' }}
                      >
                        <svg className="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M13 3L4 14h7v7l9-11h-7V3z"/>
                        </svg>
                        {message.userTitle}
                      </span>
                    )}

                    <span className="text-gray-400 text-xs">
                      {message.timestamp.toLocaleString('zh-CN', {
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit',
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
                  )}

                  {/* 转发标记 */}
                  {message.forwardedFrom && (
                    <div className="flex items-center gap-1 text-xs text-emerald-600 dark:text-emerald-400 font-medium mt-0.5">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <polyline points="15 14 20 9 15 4" />
                        <path d="M4 20v-7a4 4 0 0 1 4-4h12" />
                      </svg>
                      <span>已转发</span>
                    </div>
                  )}

                  {/* 转发引用框 */}
                  {message.forwardedFrom && (
                    <div className="mt-2 border-l-4 border-indigo-500 bg-white dark:bg-gray-800 rounded-r-lg shadow-sm overflow-hidden max-w-md">
                      <div className="p-3">
                        {/* 原消息内容 */}
                        <p className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap break-words">
                          {message.forwardedFrom.content}
                        </p>

                        {/* 原消息附件（图片） */}
                        {message.forwardedFrom.attachments && message.forwardedFrom.attachments.length > 0 && (
                          <div className="mt-3 space-y-2">
                            {message.forwardedFrom.attachments
                              .filter(att => att.fileType?.startsWith('image/'))
                              .slice(0, 4)  // 最多显示4张图片
                              .map((att, idx) => (
                                <div key={att.id || idx} className="rounded-lg overflow-hidden bg-gray-100 dark:bg-gray-700">
                                  <img
                                    src={att.thumbnailUrl || att.fileUrl}
                                    alt={att.fileName}
                                    className="w-full max-h-48 object-cover cursor-pointer hover:opacity-90 transition-opacity"
                                    onClick={() => window.open(att.fileUrl, '_blank')}
                                  />
                                </div>
                              ))}
                            {/* 如果有更多图片 */}
                            {message.forwardedFrom.attachments.filter(att => att.fileType?.startsWith('image/')).length > 4 && (
                              <p className="text-xs text-gray-500">
                                +{message.forwardedFrom.attachments.filter(att => att.fileType?.startsWith('image/')).length - 4} 张图片
                              </p>
                            )}
                          </div>
                        )}
                      </div>
                      {/* 来源信息 - 药丸形状标签（在卡片内部） */}
                      <div className="px-3 pb-3">
                        <div
                          className="w-fit inline-flex items-center gap-1.5 px-3 py-1.5 bg-gray-100 dark:bg-gray-600/80 rounded-full cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-500 transition-colors group"
                          onClick={() => {
                            if (message.forwardedFrom && onNavigateToOriginalMessage) {
                              onNavigateToOriginalMessage(message.forwardedFrom.channelId, message.forwardedFrom.messageId);
                            }
                          }}
                        >
                          <span className="text-xs text-gray-500 dark:text-gray-300">
                            来自 <span className="text-indigo-600 dark:text-indigo-400 font-medium">#{message.forwardedFrom.channelName}</span>
                            <span className="mx-1">·</span>
                            <span>{new Date(message.forwardedFrom.createdAt).toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' }).replace('/', '月') + '日'}</span>
                          </span>
                          <svg className="w-3.5 h-3.5 text-gray-400 group-hover:text-indigo-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <polyline points="9 18 15 12 9 6" />
                          </svg>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* 消息内容区 */}
                  <div className={cn(
                    "max-w-full",
                    // @提及消息保留高亮背景
                    isMention && !isAnnouncement && "rounded-lg px-3 py-2 bg-blue-50/80 dark:bg-blue-900/30"
                    // 普通消息和公告消息：无边框、无内部背景（公告只在整行有背景）
                  )}>
                    {/* 消息内容（纯附件消息时不显示） */}
                    {message.content && (
                      <div className={cn(
                        "text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap break-words",
                        // 纯贴图消息不需要内边距
                        isStickerOnly ? "" : ""
                      )}>
                        {renderMessageContent(message.content, isOwnMessage, (username, e) => {
                          // 查找被@的用户信息
                          const mentionedMember = members.find(m => m.username === username);
                          // 即使找不到成员也显示名片（用用户名作为基本信息）
                          setUserProfilePopover({
                            show: true,
                            userId: mentionedMember?.userId || '',
                            userName: username,
                            userAvatar: mentionedMember?.avatar,
                            userBio: mentionedMember?.bio,
                            userTitle: mentionedMember?.title,
                            userTitleColor: mentionedMember?.titleColor,
                            userOnlineStatus: mentionedMember?.onlineStatus,
                            position: { x: e.clientX, y: e.clientY },
                          });
                        })}
                      </div>
                    )}

                    {/* 消息附件 */}
                    {message.attachments && message.attachments.length > 0 && (
                      <div className={cn(
                        "w-fit mt-1",
                        // 附件图片限制最大宽度
                        "[&_img]:max-w-[700px] [&_img]:rounded-lg [&_img]:cursor-pointer [&_img]:border [&_img]:border-gray-200 dark:[&_img]:border-gray-700"
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

                {/* 悬停操作栏 */}
                <MessageActionBar
                  messageId={message.id}
                  isOwnMessage={isOwnMessage}
                  isPinned={message.isPinned}
                  canEdit={(() => {
                    if (!isOwnMessage || !message.timestamp) return false;
                    const messageTime = message.timestamp instanceof Date
                      ? message.timestamp.getTime()
                      : new Date(message.timestamp).getTime();
                    return Date.now() - messageTime < 10 * 60 * 1000;
                  })()}
                  canRecall={isOwnMessage}
                  canPin={currentUser.role === 'owner' || currentUser.role === 'admin'}
                  hasImage={!!message.content?.match(/!\[.*?\]\((.+?)\)/)}
                  messageContent={message.content}
                  channelId={channel.id}
                  onReply={() => {
                    setReplyingTo(message);
                    textareaRef.current?.focus();
                  }}
                  onQuickReact={(emoji) => handleQuickReact(message.id, emoji)}
                  onOpenEmojiPicker={() => {
                    setReactionTargetMessageId(message.id);
                    setEmojiPickerPosition({
                      x: window.innerWidth - 400,
                      y: 200
                    });
                    setShowEmojiPicker(true);
                  }}
                  onEdit={() => {
                    setEditingMessage(message);
                    setEditContent(message.content);
                  }}
                  onRecall={() => {
                    setDeleteMessageDialog({ show: true, messageId: message.id });
                  }}
                  onPin={async () => {
                    try {
                      if (message.isPinned) {
                        await channelApi.unpinMessage(channel.id, message.id);
                      } else {
                        await channelApi.pinMessage(channel.id, message.id);
                      }
                      onPinChange?.();
                    } catch (error: any) {
                      showError(error.response?.data?.detail || (message.isPinned ? '取消置顶失败' : '置顶失败'));
                    }
                  }}
                  onReport={() => {
                    setReportingMessageId(message.id);
                    setShowReportDialog(true);
                  }}
                  onAddToSticker={async () => {
                    const imageMatch = message.content?.match(/!\[.*?\]\((.+?)\)/);
                    if (imageMatch?.[1]) {
                      try {
                        await addFavoriteSticker({
                          stickerUrl: imageMatch[1],
                          previewUrl: imageMatch[1],
                          source: 'tenor'
                        });
                        toastSuccess('添加成功', '已添加到表情收藏');
                      } catch (e: any) {
                        toastError('添加失败', e.response?.data?.detail || '请稍后重试');
                      }
                    }
                  }}
                  onForward={() => {
                    setForwardingMessage({
                      id: message.id,
                      content: message.content,
                      sender: message.userName,
                      attachments: message.attachments,
                    });
                  }}
                />
              </div>
              </React.Fragment>
            );
          })}
          {/* 滚动锚点 */}
          <div ref={messagesEndRef} />
        </div>

        {/* 浮动跳转按钮 */}
        <div className={cn(
          "fixed bottom-44 flex flex-col gap-2 z-10 transition-all duration-200",
          // 根据右侧面板显示情况调整位置
          channel.type !== 'private' && (showSidebar && showMemberPanel)
            ? "right-[512px]"  // 两个面板都显示：w-60*2 (480px) + right-8 (32px)
            : channel.type !== 'private' && (showSidebar || showMemberPanel)
              ? "right-[272px]"  // 只有一个面板：w-60 (240px) + right-8 (32px)
              : "right-8"
        )}>
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
        {/* 主输入容器 */}
        <div className={cn(
          "border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 shadow-sm",
          replyingTo ? "rounded-2xl" : "rounded-2xl"
        )}>
          {/* 回复预览 - Discord风格，在容器内部 */}
          {replyingTo && (
            <div className="flex items-center justify-between px-4 py-2 border-b border-gray-200 dark:border-slate-700">
              <div className="flex items-center gap-1.5 text-sm">
                <span className="text-gray-500 dark:text-gray-400">正在回复至</span>
                <span
                  className="text-blue-600 dark:text-blue-400 font-medium cursor-pointer hover:underline"
                  onClick={() => jumpToMessage(replyingTo.id)}
                >
                  {replyingTo.userName}
                </span>
              </div>
              <button
                onClick={() => setReplyingTo(null)}
                className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded text-gray-500 dark:text-gray-400"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* 输入内容区域 */}
          <div className="px-4 py-3 space-y-3">
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
              onPaste={handlePaste}
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

              {/* 搜索聊天记录按钮 */}
              <button
                onClick={() => setShowSearchPage(true)}
                className="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg text-gray-500 dark:text-slate-400 transition-colors"
                title="搜索聊天记录"
              >
                <Search className="w-4 h-4" />
              </button>

              {canSendAnnouncement && (
                <button
                  onClick={() => setShowAnnouncementDialog(true)}
                  disabled={channel.status === 'locked'}
                  className="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg text-amber-600 dark:text-amber-400 disabled:opacity-30 transition-colors"
                  title="发布公告"
                >
                  <Megaphone className="w-4 h-4" />
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
      </div>

      {/* 表情选择器 */}
      {showEmojiPicker && (
        <>
          {/* 遮罩层 */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => {
              setShowEmojiPicker(false);
              setReactionTargetMessageId(null);
            }}
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
              onSelectSticker={handleStickerSelect}
              onClose={() => {
                setShowEmojiPicker(false);
                setReactionTargetMessageId(null);
              }}
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
      {contextMenu && contextMenu.show && (() => {
        // 计算菜单位置，确保不超出屏幕
        const menuWidth = 188;
        const menuHeight = 350; // 预估菜单高度
        const padding = 10;

        let adjustedX = contextMenu.x;
        let adjustedY = contextMenu.y;

        // 防止超出右边缘
        if (contextMenu.x + menuWidth + padding > window.innerWidth) {
          adjustedX = window.innerWidth - menuWidth - padding;
        }

        // 防止超出底部
        if (contextMenu.y + menuHeight + padding > window.innerHeight) {
          adjustedY = window.innerHeight - menuHeight - padding;
        }

        // 防止超出左边缘
        if (adjustedX < padding) {
          adjustedX = padding;
        }

        // 防止超出顶部
        if (adjustedY < padding) {
          adjustedY = padding;
        }

        return (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setContextMenu(null)}
          />
          <div
            className="fixed bg-white dark:bg-[#18191c] rounded shadow-lg z-50 w-[188px] p-1.5"
            style={{
              left: `${adjustedX}px`,
              top: `${adjustedY}px`,
              boxShadow: '0 0 0 1px rgba(0,0,0,.05), 0 2px 10px rgba(0,0,0,.1)'
            }}
          >
            {(() => {
              const message = messages.find(m => m.id === contextMenu.messageId);
              const isOwnMessage = message?.userId === currentUser.id;
              const canPin = currentUser.role === 'owner' || currentUser.role === 'admin';

              // 检查消息是否包含图片/贴图
              const imageMatch = message?.content?.match(/!\[.*?\]\((.+?)\)/);
              const hasImage = !!imageMatch;
              const imageUrl = imageMatch?.[1];

              // 计算时间差
              let canRecall = isOwnMessage; // 只要是自己的消息就可以删除
              let canEdit = false;
              if (message?.timestamp) {
                const messageTime = message.timestamp instanceof Date
                  ? message.timestamp.getTime()
                  : new Date(message.timestamp).getTime();
                const now = Date.now();
                const timeDiff = now - messageTime;
                canEdit = isOwnMessage && timeDiff < 10 * 60 * 1000 && timeDiff >= 0;
              }

              // 添加到表情的处理函数
              const handleAddToSticker = async () => {
                if (!imageUrl) return;
                try {
                  await addFavoriteSticker({
                    stickerUrl: imageUrl,
                    previewUrl: imageUrl,
                    source: 'tenor'
                  });
                  toastSuccess('添加成功', '已添加到表情收藏');
                } catch (e: any) {
                  toastError('添加失败', e.response?.data?.detail || '请稍后重试');
                }
                setContextMenu(null);
              };

              // 复制文字
              const handleCopyText = () => {
                if (message?.content) {
                  // 移除markdown图片语法，只复制纯文本
                  const plainText = message.content
                    .replace(/!\[.*?\]\(.*?\)/g, '')
                    .replace(/\[.*?\]\(.*?\)/g, (match) => {
                      const textMatch = match.match(/\[(.*?)\]/);
                      return textMatch ? textMatch[1] : '';
                    })
                    .trim();
                  navigator.clipboard.writeText(plainText || message.content);
                  toastSuccess('已复制', '文字已复制到剪贴板');
                }
                setContextMenu(null);
              };

              // 复制消息链接
              const handleCopyLink = () => {
                const link = `${window.location.origin}/channels/${channel.id}?message=${message?.id}`;
                navigator.clipboard.writeText(link);
                toastSuccess('已复制', '消息链接已复制到剪贴板');
                setContextMenu(null);
              };

              // 快捷表情反应
              const quickReactions = ['👍', '💯', '👎', '😂'];
              // 悬浮子菜单的更多表情
              const moreReactions = ['❤️', '😊', '😢', '😮', '😡', '🎉', '🔥', '👀', '🙏', '💪', '✅', '❌'];
              const handleQuickReaction = async (emoji: string) => {
                if (message) {
                  try {
                    await channelApi.addReaction(channel.id, message.id, emoji);
                  } catch (e) {
                    console.error('添加反应失败', e);
                  }
                }
                setContextMenu(null);
              };

              // 菜单项样式
              const menuItemClass = "w-full px-2 py-1.5 text-sm text-left rounded-sm flex items-center justify-between text-gray-600 dark:text-[#b9bbbe] hover:bg-[#5865f2] hover:text-white transition-colors";
              const menuItemDangerClass = "w-full px-2 py-1.5 text-sm text-left rounded-sm flex items-center justify-between text-[#ed4245] hover:bg-[#ed4245] hover:text-white transition-colors";
              const dividerClass = "h-px bg-gray-200 dark:bg-[#2e3035] my-1";

              return (
                <>
                  {/* 顶部快捷表情栏 */}
                  <div className="flex gap-0.5 pb-2">
                    {quickReactions.map((emoji) => (
                      <button
                        key={emoji}
                        onClick={() => handleQuickReaction(emoji)}
                        className="w-8 h-8 flex items-center justify-center text-xl rounded hover:bg-gray-100 dark:hover:bg-[#4f545c99] hover:scale-110 transition-all"
                      >
                        {emoji}
                      </button>
                    ))}
                  </div>

                  {/* 添加反应 - 带悬浮子菜单 */}
                  <div className="relative group/reaction">
                    <button
                      className={menuItemClass}
                      onClick={(e) => {
                        // 点击打开完整表情选择器
                        if (message) {
                          setReactionTargetMessageId(message.id);
                          setEmojiPickerPosition({
                            x: Math.min(contextMenu.x + 200, window.innerWidth - 350),
                            y: Math.min(contextMenu.y, window.innerHeight - 450)
                          });
                          setShowEmojiPicker(true);
                        }
                        setContextMenu(null);
                      }}
                    >
                      <span>添加反应</span>
                      <svg className="w-2.5 h-2.5 opacity-60" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
                      </svg>
                    </button>

                    {/* 悬浮子菜单 - 更多表情 */}
                    <div className="absolute left-full top-0 ml-1 hidden group-hover/reaction:block">
                      <div className="bg-white dark:bg-[#18191c] rounded shadow-lg p-2 w-[200px]" style={{ boxShadow: '0 0 0 1px rgba(0,0,0,.05), 0 2px 10px rgba(0,0,0,.1)' }}>
                        <div className="grid grid-cols-6 gap-1">
                          {moreReactions.map((emoji) => (
                            <button
                              key={emoji}
                              onClick={() => handleQuickReaction(emoji)}
                              className="w-7 h-7 flex items-center justify-center text-lg rounded hover:bg-gray-100 dark:hover:bg-[#4f545c99] hover:scale-110 transition-all"
                            >
                              {emoji}
                            </button>
                          ))}
                        </div>
                        <div className="mt-2 pt-2 border-t border-gray-200 dark:border-[#2e3035]">
                          <button
                            onClick={(e) => {
                              if (message) {
                                setReactionTargetMessageId(message.id);
                                setEmojiPickerPosition({
                                  x: Math.min(contextMenu.x + 200, window.innerWidth - 350),
                                  y: Math.min(contextMenu.y, window.innerHeight - 450)
                                });
                                setShowEmojiPicker(true);
                              }
                              setContextMenu(null);
                            }}
                            className="w-full text-xs text-center py-1.5 text-gray-500 dark:text-gray-400 hover:text-[#5865f2] dark:hover:text-[#5865f2] hover:bg-gray-50 dark:hover:bg-[#2e3035] rounded transition-colors"
                          >
                            显示更多
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className={dividerClass} />

                  {/* 回复 */}
                  <button
                    className={menuItemClass}
                    onClick={() => {
                      if (message) {
                        setReplyingTo(message);
                        textareaRef.current?.focus();
                      }
                      setContextMenu(null);
                    }}
                  >
                    <span>回复</span>
                    <Reply className="w-4 h-4 opacity-80" />
                  </button>

                  {/* 转发 */}
                  <button
                    className={menuItemClass}
                    onClick={() => {
                      if (message) {
                        setForwardingMessage({
                          id: message.id,
                          content: message.content,
                          sender: message.userName,
                          attachments: message.attachments
                        });
                      }
                      setContextMenu(null);
                    }}
                  >
                    <span>转发</span>
                    <Forward className="w-4 h-4 opacity-80" />
                  </button>

                  {/* 编辑 */}
                  {canEdit && (
                    <button
                      className={menuItemClass}
                      onClick={() => {
                        if (message) {
                          setEditingMessage(message);
                          setEditContent(message.content);
                        }
                        setContextMenu(null);
                      }}
                    >
                      <span>编辑消息</span>
                      <Edit2 className="w-4 h-4 opacity-80" />
                    </button>
                  )}

                  {/* 置顶 */}
                  {canPin && message && (
                    <button
                      className={menuItemClass}
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
                      <span>{message.isPinned ? '取消置顶' : '置顶消息'}</span>
                      <Pin className="w-4 h-4 opacity-80" />
                    </button>
                  )}

                  <div className={dividerClass} />

                  {/* 复制文字 */}
                  <button className={menuItemClass} onClick={handleCopyText}>
                    <span>复制文字</span>
                    <svg className="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                    </svg>
                  </button>

                  {/* 复制消息链接 */}
                  <button className={menuItemClass} onClick={handleCopyLink}>
                    <span>复制消息链接</span>
                    <svg className="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                      <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                    </svg>
                  </button>

                  {/* 添加到表情（有图片时显示） */}
                  {hasImage && (
                    <>
                      <div className={dividerClass} />
                      <button className={menuItemClass} onClick={handleAddToSticker}>
                        <span>添加到表情</span>
                        <Star className="w-4 h-4 opacity-80" />
                      </button>
                    </>
                  )}

                  {/* 删除（自己的消息） */}
                  {canRecall && (
                    <>
                      <div className={dividerClass} />
                      <button
                        className={menuItemDangerClass}
                        onClick={() => {
                          setDeleteMessageDialog({ show: true, messageId: contextMenu.messageId });
                          setContextMenu(null);
                        }}
                      >
                        <span>删除信息</span>
                        <Trash2 className="w-4 h-4 opacity-80" />
                      </button>
                    </>
                  )}

                  {/* 举报（他人消息） */}
                  {!isOwnMessage && (
                    <>
                      <div className={dividerClass} />
                      <button
                        className={menuItemDangerClass}
                        onClick={() => {
                          setReportingMessageId(contextMenu.messageId);
                          setShowReportDialog(true);
                          setContextMenu(null);
                        }}
                      >
                        <span>举报消息</span>
                        <AlertCircle className="w-4 h-4 opacity-80" />
                      </button>
                    </>
                  )}
                </>
              );
            })()}
          </div>
        </>
        );
      })()}

      {/* 用户头像右键菜单 */}
      {userContextMenu && userContextMenu.show && (() => {
        // 计算菜单位置，确保不超出屏幕
        const menuWidth = 200;
        const menuHeight = 250; // 预估菜单高度
        const padding = 10;

        let adjustedX = userContextMenu.x;
        let adjustedY = userContextMenu.y;

        // 防止超出右边缘
        if (userContextMenu.x + menuWidth + padding > window.innerWidth) {
          adjustedX = window.innerWidth - menuWidth - padding;
        }

        // 防止超出底部
        if (userContextMenu.y + menuHeight + padding > window.innerHeight) {
          adjustedY = window.innerHeight - menuHeight - padding;
        }

        // 防止超出左边缘
        if (adjustedX < padding) {
          adjustedX = padding;
        }

        // 防止超出顶部
        if (adjustedY < padding) {
          adjustedY = padding;
        }

        return (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setUserContextMenu(null)}
          />
          <div
            className="fixed bg-white dark:bg-[#18191c] rounded shadow-lg z-50 w-[200px] p-1.5"
            style={{
              left: `${adjustedX}px`,
              top: `${adjustedY}px`,
              boxShadow: '0 0 0 1px rgba(0,0,0,.05), 0 2px 10px rgba(0,0,0,.1)'
            }}
          >
            {(() => {
              const menuItemClass = "w-full px-2 py-1.5 text-sm text-left rounded-sm flex items-center justify-between text-gray-600 dark:text-[#b9bbbe] hover:bg-[#5865f2] hover:text-white transition-colors";
              const menuItemDangerClass = "w-full px-2 py-1.5 text-sm text-left rounded-sm flex items-center justify-between text-[#ed4245] hover:bg-[#ed4245] hover:text-white transition-colors";
              const dividerClass = "h-px bg-gray-200 dark:bg-[#2e3035] my-1";

              return (
                <>
                  {/* 查看完整个人资料 */}
                  <button
                    className={menuItemClass}
                    onClick={() => {
                      // 直接跳转到个人主页
                      navigate(`/user/${userContextMenu.userId}`);
                      setUserContextMenu(null);
                    }}
                  >
                    <span>查看完整个人资料</span>
                  </button>

                  {/* 邀请至频道 - 带悬浮子菜单 */}
                  <div className="relative group/invite">
                    <button className={menuItemClass}>
                      <span>邀请至频道</span>
                      <svg className="w-2.5 h-2.5 opacity-60" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
                      </svg>
                    </button>

                    {/* 频道列表子菜单 */}
                    <div className="absolute left-full top-0 ml-1 hidden group-hover/invite:block">
                      <div className="bg-white dark:bg-[#18191c] rounded shadow-lg p-1.5 min-w-[150px] max-h-[300px] overflow-y-auto" style={{ boxShadow: '0 0 0 1px rgba(0,0,0,.05), 0 2px 10px rgba(0,0,0,.1)' }}>
                        {invitableChannels.length > 0 ? (
                          invitableChannels.map((ch) => (
                            <button
                              key={ch.id}
                              className="w-full px-2 py-1.5 text-sm text-left rounded-sm text-gray-600 dark:text-[#b9bbbe] hover:bg-[#5865f2] hover:text-white transition-colors truncate"
                              onClick={async () => {
                                try {
                                  const result = await inviteToChannel(ch.id, userContextMenu.userId);
                                  if (result.alreadyMember) {
                                    showWarning(`${userContextMenu.userName} 已是 ${ch.name} 的成员`);
                                  } else if (result.inviteSent) {
                                    showSuccess(`已向 ${userContextMenu.userName} 发送 ${ch.name} 的邀请`);
                                  } else {
                                    showSuccess(result.message);
                                  }
                                } catch (error: any) {
                                  console.error('邀请失败:', error);
                                  showError(error?.detail || error?.message || '邀请失败，请重试');
                                }
                                setUserContextMenu(null);
                              }}
                            >
                              {ch.name}
                            </button>
                          ))
                        ) : (
                          <div className="text-xs text-gray-400 dark:text-gray-500 px-2 py-1">
                            暂无可邀请的频道
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* 私信 - 在私聊频道中不显示，因为已经在私聊了 */}
                  {channel.type !== 'private' && (
                    <>
                      <div className={dividerClass} />
                      <button
                        className={menuItemClass}
                        onClick={async () => {
                          // 检查好友关系，如果是好友则直接跳转到私聊频道
                          try {
                            const result = await checkFriendship(userContextMenu.userId);
                            if (result.isFriend && result.privateChannelId) {
                              navigate(`/channels?channelId=${result.privateChannelId}`);
                            } else {
                              // 不是好友，打开用户名片让用户添加好友
                              setUserProfilePopover({
                                show: true,
                                userId: userContextMenu.userId,
                                userName: userContextMenu.userName,
                                userAvatar: userContextMenu.userAvatar,
                                userOnlineStatus: userContextMenu.userOnlineStatus,
                                position: { x: userContextMenu.x, y: userContextMenu.y },
                              });
                              showWarning('需要先添加对方为好友才能发送私信');
                            }
                          } catch (error) {
                            console.error('检查好友关系失败:', error);
                            showError('检查好友关系失败');
                          }
                          setUserContextMenu(null);
                        }}
                      >
                        <span>发送私信</span>
                        <Mail className="w-4 h-4 opacity-80" />
                      </button>
                    </>
                  )}

                  <div className={dividerClass} />

                  {/* 屏蔽 */}
                  <button
                    className={menuItemDangerClass}
                    onClick={() => {
                      // TODO: 屏蔽用户
                      setUserContextMenu(null);
                    }}
                  >
                    <span>屏蔽</span>
                  </button>

                  {/* 举报用户 */}
                  <button
                    className={menuItemDangerClass}
                    onClick={() => {
                      // 打开举报对话框
                      setReportingMessageId(''); // 清除消息举报
                      setShowReportDialog(true);
                      setUserContextMenu(null);
                    }}
                  >
                    <span>举报用户个人资料</span>
                  </button>
                </>
              );
            })()}
          </div>
        </>
        );
      })()}

      {/* 成员管理对话框 */}
      <MemberManagementDialog
        isOpen={showMemberDialog}
        onClose={() => setShowMemberDialog(false)}
        channelId={channel.id}
        channelName={channel.name}
        channelType={channel.type}
        currentUserId={currentUser.id}
        isCreator={currentUser.isCreator || false}
        userRole={currentUser.role || 'member'}
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

      {/* 转发对话框 */}
      <ForwardMessageDialog
        isOpen={!!forwardingMessage}
        onClose={() => setForwardingMessage(null)}
        sourceChannelId={channel.id}
        messageId={forwardingMessage?.id || ''}
        messageContent={forwardingMessage?.content || ''}
        messageSender={forwardingMessage?.sender || ''}
        messageAttachments={forwardingMessage?.attachments}
      />

      {/* 删除消息确认对话框 */}
      <ConfirmDialog
        isOpen={deleteMessageDialog.show}
        title="删除消息"
        message="确定要删除这条消息吗？删除后将无法恢复。"
        confirmText="删除"
        cancelText="取消"
        variant="danger"
        onConfirm={() => {
          if (deleteMessageDialog.messageId) {
            handleRecallMessage(deleteMessageDialog.messageId);
          }
        }}
        onCancel={() => setDeleteMessageDialog({ show: false, messageId: null })}
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

      {/* 公告编辑对话框 */}
      {showAnnouncementDialog && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md mx-4">
            {/* 标题栏 */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center gap-2">
                <Megaphone className="w-5 h-5 text-amber-600 dark:text-amber-400" />
                <h3 className="text-base font-medium dark:text-gray-100">发布公告</h3>
              </div>
              <button
                onClick={() => {
                  setShowAnnouncementDialog(false);
                  setAnnouncementContent('');
                  setAnnouncementFiles([]);
                }}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                <X className="w-4 h-4 dark:text-gray-400" />
              </button>
            </div>

            {/* 公告内容 */}
            <div className="p-4 space-y-4">
              <textarea
                value={announcementContent}
                onChange={(e) => setAnnouncementContent(e.target.value)}
                placeholder="输入公告内容..."
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm resize-none focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500"
                rows={4}
                autoFocus
              />

              {/* 已上传文件预览 */}
              <FilePreview
                files={announcementFiles}
                onRemove={(fileId) => setAnnouncementFiles(prev => prev.filter(f => f.id !== fileId))}
              />

              {/* 文件上传 */}
              <div className="flex items-center gap-2">
                <FileUploader
                  channelId={channel.id}
                  uploadedFiles={announcementFiles}
                  onFilesUploaded={(files) => setAnnouncementFiles(prev => [...prev, ...files])}
                  maxFiles={5}
                />
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  可添加附件（最多5个）
                </span>
              </div>

              <p className="text-xs text-amber-600 dark:text-amber-400">
                公告将发送给所有频道成员
              </p>
            </div>

            {/* 底部按钮 */}
            <div className="flex items-center justify-end gap-2 p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 rounded-b-lg">
              <button
                onClick={() => {
                  setShowAnnouncementDialog(false);
                  setAnnouncementContent('');
                  setAnnouncementFiles([]);
                }}
                className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                取消
              </button>
              <button
                onClick={handleSendAnnouncement}
                disabled={!announcementContent.trim() && announcementFiles.length === 0}
                className="px-4 py-2 text-sm bg-amber-600 text-white rounded hover:bg-amber-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1.5"
              >
                <Megaphone className="w-4 h-4" />
                发布公告
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 编辑群名称对话框 */}
      {showEditNameDialog && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
          onClick={() => setShowEditNameDialog(false)}
        >
          <div
            className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-sm mx-4"
            onClick={(e) => e.stopPropagation()}
          >
            {/* 标题栏 */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="text-base font-medium dark:text-gray-100">修改群名称</h3>
              <button
                onClick={() => {
                  setShowEditNameDialog(false);
                  setEditingChannelName('');
                }}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                <X className="w-4 h-4 dark:text-gray-400" />
              </button>
            </div>

            {/* 输入内容 */}
            <div className="p-4">
              <input
                type="text"
                value={editingChannelName}
                onChange={(e) => setEditingChannelName(e.target.value)}
                placeholder="请输入群名称"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500"
                maxLength={50}
                autoFocus
              />
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                {editingChannelName.length}/50
              </p>
            </div>

            {/* 底部按钮 */}
            <div className="flex items-center justify-end gap-2 p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 rounded-b-lg">
              <button
                onClick={() => {
                  setShowEditNameDialog(false);
                  setEditingChannelName('');
                }}
                className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                取消
              </button>
              <button
                onClick={async () => {
                  if (!editingChannelName.trim()) return;
                  try {
                    await updateChannelSettings(channel.id, { name: editingChannelName.trim() });
                    toastSuccess('群名称修改成功');
                    setShowEditNameDialog(false);
                    setEditingChannelName('');
                  } catch (error) {
                    console.error('修改群名称失败:', error);
                    toastError('修改群名称失败');
                  }
                }}
                disabled={!editingChannelName.trim() || editingChannelName === channel.name}
                className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                确定
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 删除公告确认对话框 */}
      {showDeleteAnnouncementDialog && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
          onClick={() => setShowDeleteAnnouncementDialog(false)}
        >
          <div
            className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-sm mx-4"
            onClick={(e) => e.stopPropagation()}
          >
            {/* 头部 */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="text-base font-medium dark:text-gray-100">删除公告</h3>
              <button
                onClick={() => setShowDeleteAnnouncementDialog(false)}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                <X className="w-4 h-4 dark:text-gray-400" />
              </button>
            </div>

            {/* 内容 */}
            <div className="p-4">
              <p className="text-sm text-gray-700 dark:text-gray-300 text-center">
                确定删除此公告？删除后所有人都无法看到。
              </p>
            </div>

            {/* 底部按钮 */}
            <div className="flex items-center justify-end gap-2 p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 rounded-b-lg">
              <button
                onClick={() => setShowDeleteAnnouncementDialog(false)}
                className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                取消
              </button>
              <button
                onClick={handleConfirmDeleteAnnouncement}
                className="px-4 py-2 text-sm bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
              >
                确认删除
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 聊天记录搜索页面 */}
      <ChatSearchPage
        channel={channel}
        displayName={privateChatPartnerName || undefined}
        isOpen={showSearchPage}
        onClose={() => setShowSearchPage(false)}
        onMessageClick={(msgId) => {
          setShowSearchPage(false);
          jumpToMessage(msgId);
        }}
      />

      {/* Toast 通知容器 */}
      <ToastContainer messages={toastMessages} onClose={closeToast} />

      {/* 用户资料弹出卡片 */}
      {userProfilePopover?.show && (
        <UserProfilePopover
          userId={userProfilePopover.userId}
          userName={userProfilePopover.userName}
          userAvatar={userProfilePopover.userAvatar}
          userBio={userProfilePopover.userBio}
          userTitle={userProfilePopover.userTitle}
          userTitleColor={userProfilePopover.userTitleColor}
          userOnlineStatus={userProfilePopover.userOnlineStatus}
          currentUserId={currentUser.id}
          channelId={channel.id}
          channelType={channel.type}
          position={userProfilePopover.position}
          onClose={() => setUserProfilePopover(null)}
          onStartPrivateChat={handleStartPrivateChat}
        />
      )}
          </div>

          {/* 成员列表面板 */}
          {showMemberPanel && channel.type !== 'private' && (
            <MemberListPanel
              members={members}
              onMemberClick={(member, e) => {
                // 点击成员显示用户卡片
                const rect = (e.target as HTMLElement).getBoundingClientRect();
                setUserProfilePopover({
                  show: true,
                  userId: member.userId,
                  userName: member.username,
                  userAvatar: member.avatar,
                  userBio: member.bio,
                  userTitle: member.title,
                  userTitleColor: member.titleColor,
                  userOnlineStatus: undefined,
                  position: { x: rect.left - 320, y: rect.top }
                });
              }}
            />
          )}

          {/* 频道设置面板 */}
          {showSidebar && channel.type !== 'private' && (
            <>
              {/* 点击外部关闭的遮罩层 */}
              <div
                className="fixed inset-0 z-10"
                onClick={() => setShowSidebar(false)}
              />
              <div className="relative z-20">
                <ChannelSettingsPanel
                  channel={channel}
                  members={members}
                  currentUser={currentUser}
                  onClose={() => setShowSidebar(false)}
                  onSearchChat={() => {
                    setShowSearchPage(true);
                    setShowSidebar(false);
                  }}
                  onManageMembers={() => {
                    setShowMemberDialog(true);
                    setShowSidebar(false);
                  }}
                  onAddMember={() => {
                    onInviteToChannel?.();
                    setShowSidebar(false);
                  }}
                  onRemoveMember={() => {
                    setShowMemberDialog(true);
                    setShowSidebar(false);
                  }}
                  onDissolveChannel={currentUser.role === 'owner' ? onLeaveChannel : undefined}
                  onLeaveChannel={currentUser.role !== 'owner' ? onLeaveChannel : undefined}
                  onViewMoreMembers={() => {
                    setShowMemberPanel(true);
                    setShowSidebar(false);
                  }}
                  onEditAnnouncement={() => {
                    setAnnouncementContent(latestAnnouncement?.content || channel.description || '');
                    setShowAnnouncementDialog(true);
                  }}
                  onEditChannelName={() => {
                    setEditingChannelName(channel.name);
                    setShowEditNameDialog(true);
                  }}
                  onMemberClick={(member, e) => {
                    setUserProfilePopover({
                      show: true,
                      userId: member.userId,
                      userName: member.username,
                      userAvatar: member.avatar,
                      userBio: member.bio,
                      userTitle: member.title,
                      userTitleColor: member.titleColor,
                      userOnlineStatus: member.onlineStatus,
                      position: { x: e.clientX - 320, y: e.clientY }
                    });
                  }}
                  announcement={latestAnnouncement ? {
                    content: latestAnnouncement.content,
                    authorName: latestAnnouncement.userName,
                    authorAvatar: latestAnnouncement.userAvatar,
                    updatedAt: latestAnnouncement.timestamp instanceof Date
                      ? latestAnnouncement.timestamp.toLocaleString('zh-CN')
                      : new Date(latestAnnouncement.timestamp).toLocaleString('zh-CN')
                  } : undefined}
                />
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
}
