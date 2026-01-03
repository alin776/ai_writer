import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Search, X, FileText, Check, Loader2, Calendar } from 'lucide-react';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import * as channelApi from '@/services/channelApi';
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';

interface ChatSearchPageProps {
  channel: {
    id: string;
    name: string;
    type?: 'official' | 'fangroup' | 'work' | 'private';
  };
  displayName?: string; // 私聊频道时传入对方用户名
  isOpen: boolean;
  onClose: () => void;
  onMessageClick: (msgId: string) => void;
}

// 搜索结果消息类型
interface SearchMessage {
  id: string;
  content: string;
  type: string;
  createdAt: string;
  userId: string;
  userName: string;
  userAvatar: string | null;
  userTitle: string | null;
  userTitleColor: string | null;
  attachments: Array<{
    id: string;
    fileName: string;
    fileType: string;
    fileSize: number;
    fileUrl: string;
    thumbnailUrl: string | null;
  }>;
}

// 筛选条件
interface SearchFilters {
  keyword: string;
  contentType: 'all' | 'image_video' | 'file' | 'link' | null;
  userId: string | null;
  startDate: string | null;
  endDate: string | null;
}

// 频道成员类型
interface ChannelMember {
  id: string;
  userId: string;
  username: string;
  avatar: string | null;
}

// 分类标签配置
const FILTER_TABS = [
  { id: 'all', label: '全部' },
  { id: 'image_video', label: '图片与视频' },
  { id: 'file', label: '文件' },
  { id: 'link', label: '链接' },
] as const;

export function ChatSearchPage({ channel, displayName, isOpen, onClose, onMessageClick }: ChatSearchPageProps) {
  // 计算显示名称：私聊频道使用 displayName，其他使用 channel.name
  const channelDisplayName = channel.type === 'private' ? (displayName || '私聊') : channel.name;

  // 筛选条件
  const [filters, setFilters] = useState<SearchFilters>({
    keyword: '',
    contentType: 'all',
    userId: null,
    startDate: null,
    endDate: null,
  });

  // 搜索结果
  const [results, setResults] = useState<SearchMessage[]>([]);
  const [total, setTotal] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // UI状态
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [showMemberPicker, setShowMemberPicker] = useState(false);
  const [members, setMembers] = useState<ChannelMember[]>([]);
  const [selectedMember, setSelectedMember] = useState<ChannelMember | null>(null);

  // 分页
  const [skip, setSkip] = useState(0);
  const limit = 20;

  // 执行搜索
  const handleSearch = useCallback(async (resetResults = true) => {
    // "全部"标签允许搜索所有记录，其他情况至少需要关键词或内容类型
    const hasValidFilter = filters.contentType === 'all' || filters.keyword || filters.contentType || filters.userId || filters.startDate;
    if (!hasValidFilter) {
      return;
    }

    if (resetResults) {
      setSkip(0);
      setResults([]);
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await channelApi.searchMessages(channel.id, {
        keyword: filters.keyword || undefined,
        contentType: filters.contentType === 'all' ? undefined : (filters.contentType || undefined),
        userId: filters.userId || undefined,
        startDate: filters.startDate || undefined,
        endDate: filters.endDate || undefined,
        skip: resetResults ? 0 : skip,
        limit,
      });

      // 转换响应数据
      const messages: SearchMessage[] = response.messages.map((msg: any) => ({
        id: msg.id,
        content: msg.content,
        type: msg.type,
        createdAt: msg.createdAt || msg.created_at,
        userId: msg.userId || msg.user_id,
        userName: msg.userName || msg.user_name,
        userAvatar: msg.userAvatar || msg.user_avatar,
        userTitle: msg.userTitle || msg.user_title,
        userTitleColor: msg.userTitleColor || msg.user_title_color,
        attachments: (msg.attachments || []).map((att: any) => ({
          id: att.id,
          fileName: att.fileName || att.file_name,
          fileType: att.fileType || att.file_type,
          fileSize: att.fileSize || att.file_size,
          fileUrl: att.fileUrl || att.file_url,
          thumbnailUrl: att.thumbnailUrl || att.thumbnail_url,
        })),
      }));

      if (resetResults) {
        setResults(messages);
      } else {
        setResults(prev => [...prev, ...messages]);
      }
      setTotal(response.total);
      setHasMore(response.has_more);
    } catch (err: any) {
      setError(err.message || '搜索失败');
    } finally {
      setIsLoading(false);
    }
  }, [channel.id, filters, skip]);

  // 加载更多
  const handleLoadMore = () => {
    if (!isLoading && hasMore) {
      setSkip(prev => prev + limit);
    }
  };

  // skip变化时加载更多
  useEffect(() => {
    if (skip > 0) {
      handleSearch(false);
    }
  }, [skip]);

  // 加载成员列表
  useEffect(() => {
    if (isOpen) {
      channelApi.getChannelMembers(channel.id)
        .then((response: any) => {
          const memberList = response.members || response;
          setMembers(memberList.map((m: any) => ({
            id: m.id,
            userId: m.userId || m.user_id,
            username: m.username || m.userName,
            avatar: m.avatar || m.userAvatar,
          })));
        })
        .catch(() => {});
    }
  }, [isOpen, channel.id]);

  // 关闭时重置状态
  useEffect(() => {
    if (!isOpen) {
      // 关闭时重置状态
      setFilters({ keyword: '', contentType: 'all', userId: null, startDate: null, endDate: null });
      setResults([]);
      setTotal(0);
      setSkip(0);
      setError(null);
      setSelectedMember(null);
    } else {
      // 打开时自动加载"全部"记录
      setFilters(f => ({ ...f, contentType: 'all' }));
      setTimeout(() => handleSearch(), 100);
    }
  }, [isOpen]);

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* 遮罩层 + flex 居中容器 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/40 z-40 flex items-center justify-center"
            onClick={onClose}
          >
            {/* 居中弹窗 */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="relative w-[520px] h-[600px] bg-white dark:bg-[#18191c] rounded-lg shadow-2xl flex flex-col"
              onClick={(e) => e.stopPropagation()}
            >
              {/* 头部 */}
              <Header channelDisplayName={channelDisplayName} total={total} onClose={onClose} />

              {/* 搜索框 */}
              <SearchInput
                value={filters.keyword}
                onChange={(v) => setFilters(f => ({ ...f, keyword: v }))}
                onSearch={() => handleSearch()}
              />

              {/* 分类标签 */}
              <FilterTabs
                activeTab={filters.contentType || 'all'}
                onTabChange={(tab) => {
                  const newContentType = tab as typeof filters.contentType;
                  setFilters(f => ({ ...f, contentType: newContentType }));
                  // 切换标签时自动搜索
                  setTimeout(() => handleSearch(), 0);
                }}
                onDateClick={() => setShowDatePicker(true)}
                onMemberClick={() => setShowMemberPicker(true)}
                hasDateFilter={!!filters.startDate}
                hasMemberFilter={!!filters.userId}
              />

              {/* 搜索结果 */}
              <ResultList
                results={results}
                isLoading={isLoading}
                error={error}
                hasMore={hasMore}
                keyword={filters.keyword}
                onMessageClick={onMessageClick}
                onLoadMore={handleLoadMore}
              />

              {/* 日期选择弹窗 */}
              {showDatePicker && (
                <DatePickerPopover
                  startDate={filters.startDate}
                  endDate={filters.endDate}
                  onApply={(start, end) => {
                    setFilters(f => ({ ...f, startDate: start, endDate: end }));
                    setShowDatePicker(false);
                    if (filters.keyword || filters.contentType) {
                      setTimeout(() => handleSearch(), 0);
                    }
                  }}
                  onClear={() => {
                    setFilters(f => ({ ...f, startDate: null, endDate: null }));
                    setShowDatePicker(false);
                  }}
                  onClose={() => setShowDatePicker(false)}
                />
              )}

              {/* 成员选择弹窗 */}
              {showMemberPicker && (
                <MemberPickerPopover
                  members={members}
                  selectedId={filters.userId}
                  onSelect={(member) => {
                    setFilters(f => ({ ...f, userId: member?.userId || null }));
                    setSelectedMember(member);
                    setShowMemberPicker(false);
                    if (filters.keyword || filters.contentType) {
                      setTimeout(() => handleSearch(), 0);
                    }
                  }}
                  onClose={() => setShowMemberPicker(false)}
                />
              )}
            </motion.div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

// ==================== 子组件 ====================

// Header 组件
function Header({ channelDisplayName, total, onClose }: {
  channelDisplayName: string;
  total: number;
  onClose: () => void;
}) {
  return (
    <header className="flex items-center justify-between h-12 px-3 border-b border-gray-200 dark:border-[#2b2d31] flex-shrink-0">
      {/* 左侧占位 */}
      <div className="w-8"></div>

      {/* 标题居中 */}
      <h3 className="text-sm font-normal text-gray-700 dark:text-gray-200 truncate">
        "{channelDisplayName}"的聊天记录{total > 0 && `(${total})`}
      </h3>

      {/* 关闭按钮 */}
      <button
        onClick={onClose}
        className="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-700 rounded text-gray-500 dark:text-gray-400"
      >
        <X className="w-4 h-4" />
      </button>
    </header>
  );
}

// SearchInput 组件
function SearchInput({ value, onChange, onSearch }: {
  value: string;
  onChange: (v: string) => void;
  onSearch: () => void;
}) {
  return (
    <div className="px-3 py-2 flex-shrink-0">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 dark:text-gray-500" />
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && onSearch()}
          placeholder="搜索"
          className={cn(
            "w-full pl-9 pr-3 py-2 text-sm",
            "bg-gray-100 dark:bg-[#2b2d31] rounded",
            "text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500",
            "outline-none border border-transparent",
            "focus:border-gray-300 dark:focus:border-gray-600"
          )}
        />
      </div>
    </div>
  );
}

// FilterTabs 组件
function FilterTabs({
  activeTab,
  onTabChange,
  onDateClick,
  onMemberClick,
  hasDateFilter,
  hasMemberFilter
}: {
  activeTab: string | null;
  onTabChange: (tab: string) => void;
  onDateClick: () => void;
  onMemberClick: () => void;
  hasDateFilter: boolean;
  hasMemberFilter: boolean;
}) {
  return (
    <div className="flex items-center gap-4 px-4 py-2 border-b border-gray-200 dark:border-[#2b2d31] flex-shrink-0 overflow-x-auto">
      {FILTER_TABS.map(tab => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={cn(
            "text-sm transition-colors pb-2 relative whitespace-nowrap",
            activeTab === tab.id
              ? "text-blue-500 dark:text-blue-400"
              : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
          )}
        >
          {tab.label}
          {activeTab === tab.id && (
            <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-500 dark:bg-blue-400" />
          )}
        </button>
      ))}

      {/* 日期按钮 */}
      <button
        onClick={onDateClick}
        className={cn(
          "text-sm transition-colors pb-2 relative whitespace-nowrap",
          hasDateFilter
            ? "text-blue-500 dark:text-blue-400"
            : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
        )}
      >
        日期
        {hasDateFilter && (
          <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-500 dark:bg-blue-400" />
        )}
      </button>

      {/* 成员按钮 */}
      <button
        onClick={onMemberClick}
        className={cn(
          "text-sm transition-colors pb-2 relative whitespace-nowrap",
          hasMemberFilter
            ? "text-blue-500 dark:text-blue-400"
            : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
        )}
      >
        成员
        {hasMemberFilter && (
          <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-500 dark:bg-blue-400" />
        )}
      </button>
    </div>
  );
}

// ResultList 组件
function ResultList({
  results,
  isLoading,
  error,
  hasMore,
  keyword,
  onMessageClick,
  onLoadMore
}: {
  results: SearchMessage[];
  isLoading: boolean;
  error: string | null;
  hasMore: boolean;
  keyword: string;
  onMessageClick: (id: string) => void;
  onLoadMore: () => void;
}) {
  if (error) {
    return (
      <div className="flex-1 flex items-center justify-center text-red-500 text-sm">
        {error}
      </div>
    );
  }

  if (!isLoading && results.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center">
        <Search className="w-12 h-12 text-gray-300 dark:text-gray-600 mb-4" />
        <p className="text-sm text-gray-400 dark:text-gray-500">输入关键词或选择类型开始搜索</p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto">
      {results.map((msg) => (
        <ResultItem
          key={msg.id}
          message={msg}
          keyword={keyword}
          onClick={() => onMessageClick(msg.id)}
        />
      ))}

      {/* 加载更多 */}
      {hasMore && (
        <div className="p-4 text-center">
          <button
            onClick={onLoadMore}
            disabled={isLoading}
            className="text-blue-500 dark:text-blue-400 hover:text-blue-600 dark:hover:text-blue-300 text-sm"
          >
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin inline" /> : '加载更多'}
          </button>
        </div>
      )}

      {/* 加载中 */}
      {isLoading && results.length === 0 && (
        <div className="flex justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-gray-400 dark:text-gray-500" />
        </div>
      )}
    </div>
  );
}

// ResultItem 组件
function ResultItem({
  message,
  keyword,
  onClick
}: {
  message: SearchMessage;
  keyword: string;
  onClick: () => void;
}) {
  const imageAtt = message.attachments.find(a =>
    a.fileType.startsWith('image/') || a.fileType.startsWith('video/')
  );
  const fileAtts = message.attachments.filter(a =>
    !a.fileType.startsWith('image/') && !a.fileType.startsWith('video/')
  );

  return (
    <div
      className="flex gap-3 px-3 py-3 hover:bg-gray-50 dark:hover:bg-[#2b2d31] cursor-pointer transition-colors"
      onClick={onClick}
    >
      {/* 头像 */}
      <Avatar className="w-10 h-10 rounded flex-shrink-0">
        <AvatarImage src={message.userAvatar || undefined} />
        <AvatarFallback className="bg-gray-200 dark:bg-gray-700 text-sm">
          {message.userName?.[0] || '?'}
        </AvatarFallback>
      </Avatar>

      {/* 内容区 */}
      <div className="flex-1 min-w-0">
        {/* 用户名和时间 */}
        <div className="flex items-center justify-between mb-1">
          <span className="text-sm text-gray-700 dark:text-gray-300">{message.userName}</span>
          <span className="text-xs text-gray-400 dark:text-gray-500">
            {format(new Date(message.createdAt), 'MM-dd HH:mm', { locale: zhCN })}
          </span>
        </div>

        {/* 图片预览 - 大面积展示 */}
        {imageAtt && (
          <div className="mb-2">
            <img
              src={imageAtt.thumbnailUrl || imageAtt.fileUrl}
              alt={imageAtt.fileName}
              className="max-w-[200px] max-h-[150px] rounded object-cover"
            />
          </div>
        )}

        {/* 消息内容 */}
        {message.content && (
          <MessageContent content={message.content} keyword={keyword} />
        )}

        {/* 文件附件 */}
        {fileAtts.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            {fileAtts.map(att => (
              <div key={att.id} className="inline-flex items-center gap-2 px-3 py-2 bg-gray-100 dark:bg-[#2b2d31] rounded">
                <FileText className="w-5 h-5 text-gray-400 dark:text-gray-500" />
                <span className="text-sm text-gray-600 dark:text-gray-400 truncate max-w-[120px]">
                  {att.fileName}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 定位到聊天位置链接 */}
      <div className="flex-shrink-0 self-center">
        <button
          onClick={(e) => { e.stopPropagation(); onClick(); }}
          className="text-xs text-blue-500 dark:text-blue-400 hover:text-blue-600 dark:hover:text-blue-300 whitespace-nowrap"
        >
          定位到聊天位置
        </button>
      </div>
    </div>
  );
}

// HighlightText 组件
function HighlightText({ text, keyword }: { text: string; keyword?: string }) {
  if (!keyword || !text) return <>{text}</>;

  const regex = new RegExp(`(${escapeRegex(keyword)})`, 'gi');
  const parts = text.split(regex);

  return (
    <>
      {parts.map((part, i) =>
        part.toLowerCase() === keyword.toLowerCase() ? (
          <mark key={i} className="bg-yellow-500/30 text-inherit px-0.5 rounded">
            {part}
          </mark>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </>
  );
}

// MessageContent 组件 - 处理表情包和普通文本
function MessageContent({ content, keyword }: { content: string; keyword?: string }) {
  // 检查是否是纯表情包消息 ![sticker](url)
  const stickerMatch = content.match(/^!\[sticker\]\((.+)\)$/);
  if (stickerMatch) {
    return (
      <div className="mb-1">
        <img
          src={stickerMatch[1]}
          alt="sticker"
          className="max-w-[120px] max-h-[120px] rounded object-contain"
          loading="lazy"
        />
      </div>
    );
  }

  // 检查是否包含图片 ![alt](url)
  const imageMatch = content.match(/^!\[([^\]]*)\]\((.+)\)$/);
  if (imageMatch) {
    return (
      <div className="mb-1">
        <img
          src={imageMatch[2]}
          alt={imageMatch[1] || 'image'}
          className="max-w-[150px] max-h-[120px] rounded object-cover"
          loading="lazy"
        />
      </div>
    );
  }

  // 普通文本内容
  return (
    <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
      <HighlightText text={content} keyword={keyword} />
    </p>
  );
}

function escapeRegex(str: string) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// DateInput 组件 - 自定义日期输入，支持中文占位符
function DateInput({ value, onChange, placeholder }: {
  value: string;
  onChange: (v: string) => void;
  placeholder: string;
}) {
  // 格式化显示
  const displayValue = value ? format(new Date(value), 'yyyy/MM/dd') : placeholder;

  return (
    <div className="flex-1 min-w-0 relative">
      {/* 显示层 */}
      <div
        className={cn(
          "flex items-center justify-between px-2 py-1.5 text-sm border border-gray-300 dark:border-[#36373d] rounded",
          "bg-white dark:bg-[#2b2d31]",
          value ? "text-gray-900 dark:text-gray-100" : "text-gray-400 dark:text-gray-500"
        )}
      >
        <span>{displayValue}</span>
        <Calendar className="w-4 h-4 text-gray-400 dark:text-gray-500 flex-shrink-0" />
      </div>
      {/* 透明原生日期选择器 - 绝对定位覆盖 */}
      <input
        type="date"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
        style={{ colorScheme: 'dark' }}
      />
    </div>
  );
}

// DatePickerPopover 组件
function DatePickerPopover({
  startDate,
  endDate,
  onApply,
  onClear,
  onClose
}: {
  startDate: string | null;
  endDate: string | null;
  onApply: (start: string | null, end: string | null) => void;
  onClear: () => void;
  onClose: () => void;
}) {
  const [start, setStart] = useState(startDate || '');
  const [end, setEnd] = useState(endDate || '');

  const handleQuickSelect = (days: number) => {
    const today = new Date();
    const endDate = format(today, 'yyyy-MM-dd');
    const startDate = format(new Date(today.getTime() - days * 24 * 60 * 60 * 1000), 'yyyy-MM-dd');
    setStart(startDate);
    setEnd(endDate);
  };

  return (
    <div className="absolute top-[120px] left-3 right-3 p-4 bg-white dark:bg-[#18191c] rounded-lg shadow-2xl border border-gray-200 dark:border-[#2b2d31] z-50">
      {/* 点击外部关闭 */}
      <div className="fixed inset-0 z-[-1]" onClick={onClose} />

      <div className="space-y-3">
        {/* 快捷选项 */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: '今天', days: 0 },
            { label: '最近7天', days: 7 },
            { label: '最近30天', days: 30 },
          ].map(item => (
            <button
              key={item.label}
              onClick={() => handleQuickSelect(item.days)}
              className="px-3 py-1 text-sm bg-gray-100 dark:bg-[#2b2d31] rounded hover:bg-gray-200 dark:hover:bg-[#36373d] text-gray-700 dark:text-gray-300"
            >
              {item.label}
            </button>
          ))}
        </div>

        {/* 日期输入 */}
        <div className="flex items-center gap-2">
          <DateInput value={start} onChange={setStart} placeholder="年/月/日" />
          <span className="text-gray-400 dark:text-gray-500 flex-shrink-0">至</span>
          <DateInput value={end} onChange={setEnd} placeholder="年/月/日" />
        </div>

        {/* 操作按钮 */}
        <div className="flex justify-end gap-2">
          <button
            onClick={onClear}
            className="px-3 py-1 text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
          >
            清除
          </button>
          <button
            onClick={() => onApply(start || null, end || null)}
            className="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-500"
          >
            确定
          </button>
        </div>
      </div>
    </div>
  );
}

// MemberPickerPopover 组件
function MemberPickerPopover({
  members,
  selectedId,
  onSelect,
  onClose
}: {
  members: ChannelMember[];
  selectedId: string | null;
  onSelect: (member: ChannelMember | null) => void;
  onClose: () => void;
}) {
  const [searchText, setSearchText] = useState('');

  const filteredMembers = members.filter(m =>
    m.username.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <div className="absolute top-[120px] left-3 right-3 bg-white dark:bg-[#18191c] rounded-lg shadow-2xl border border-gray-200 dark:border-[#2b2d31] z-50 overflow-hidden">
      {/* 点击外部关闭 */}
      <div className="fixed inset-0 z-[-1]" onClick={onClose} />

      {/* 搜索框 */}
      <div className="p-2 border-b border-gray-200 dark:border-[#2b2d31]">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 dark:text-gray-500" />
          <input
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            placeholder="搜索成员..."
            className="w-full pl-9 pr-3 py-1.5 text-sm bg-gray-100 dark:bg-[#2b2d31] rounded text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 outline-none"
          />
        </div>
      </div>

      {/* 清除选择 */}
      {selectedId && (
        <div
          onClick={() => onSelect(null)}
          className="flex items-center gap-2 p-2 cursor-pointer hover:bg-gray-50 dark:hover:bg-[#2b2d31] text-gray-500 dark:text-gray-400"
        >
          <X className="w-4 h-4" />
          <span className="text-sm">清除筛选</span>
        </div>
      )}

      {/* 成员列表 */}
      <div className="max-h-[240px] overflow-y-auto">
        {filteredMembers.map(member => (
          <div
            key={member.id}
            onClick={() => onSelect(member)}
            className={cn(
              "flex items-center gap-2 p-2 cursor-pointer",
              "hover:bg-gray-50 dark:hover:bg-[#2b2d31]",
              selectedId === member.userId && "bg-blue-50 dark:bg-[#2b2d31]"
            )}
          >
            <Avatar className="w-8 h-8 rounded">
              <AvatarImage src={member.avatar || undefined} />
              <AvatarFallback className="bg-gray-200 dark:bg-gray-600 text-xs">
                {member.username?.[0] || '?'}
              </AvatarFallback>
            </Avatar>
            <span className="flex-1 text-sm text-gray-700 dark:text-gray-200">{member.username}</span>
            {selectedId === member.userId && <Check className="w-4 h-4 text-green-500" />}
          </div>
        ))}
        {filteredMembers.length === 0 && (
          <div className="p-4 text-center text-sm text-gray-400 dark:text-gray-500">
            未找到成员
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatSearchPage;
