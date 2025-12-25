/**
 * 章节评论面板组件
 */
import { useState, useEffect, useRef, useCallback } from 'react';
import {
  X,
  MessageCircle,
  Send,
  Loader2,
  ThumbsUp,
  Reply,
  Flag,
  MoreHorizontal,
  ChevronDown,
  ChevronUp,
  Trash2,
  Smile,
} from 'lucide-react';
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar';
import { chapterCommentApi, ChapterComment, CommentLocationStats, ReportReason } from '../../services/chapterCommentApi';
import { useAuthStore } from '../../store/authStore';
import { useGlobalStore } from '../../store/globalStore';
import { format, differenceInHours, differenceInMinutes, differenceInDays } from 'date-fns';
import { zhCN } from 'date-fns/locale';

interface ChapterCommentPanelProps {
  chapterId: string;
  isOpen: boolean;
  onClose: () => void;
  filter?: {
    type: 'all' | 'paragraph' | 'sentence';
    paragraphIndex?: number;
    sentenceIndex?: number;
    quotedText?: string;  // 被引用的原文
  };
  onStatsUpdate?: (stats: CommentLocationStats) => void;
  // 主题相关 props，用于与阅读界面风格融合
  themeColors?: {
    backgroundColor: string;
    textColor: string;
    isDarkMode: boolean;
  };
}

export function ChapterCommentPanel({
  chapterId,
  isOpen,
  onClose,
  filter = { type: 'all' },
  onStatsUpdate,
  themeColors,
}: ChapterCommentPanelProps) {
  const { backgroundColor = '#faf8f3', textColor = '#333333', isDarkMode = false } = themeColors || {};
  const { user } = useAuthStore();
  const { success, error: showError } = useGlobalStore();

  const [comments, setComments] = useState<ChapterComment[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [replyingTo, setReplyingTo] = useState<ChapterComment | null>(null);
  const [expandedReplies, setExpandedReplies] = useState<Set<string>>(new Set());
  const [showReportDialog, setShowReportDialog] = useState<string | null>(null);
  const [reportReason, setReportReason] = useState<ReportReason | ''>('');
  const [reportDescription, setReportDescription] = useState('');
  const [activeMenu, setActiveMenu] = useState<string | null>(null);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);

  const inputRef = useRef<HTMLTextAreaElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);

  // 常用 emoji 列表
  const commonEmojis = [
    '😀', '😂', '🤣', '😊', '😍', '🥰', '😘', '😋',
    '🤔', '😅', '😎', '🥳', '😭', '😤', '😱', '🤯',
    '👍', '👎', '👏', '🙏', '💪', '❤️', '🔥', '⭐',
    '💯', '✨', '🎉', '💔', '😈', '👀', '🤝', '💖',
  ];

  // 格式化时间显示
  const formatCommentTime = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMinutes = differenceInMinutes(now, date);
    const diffHours = differenceInHours(now, date);
    const diffDays = differenceInDays(now, date);

    if (diffMinutes < 1) {
      return '刚刚';
    } else if (diffMinutes < 60) {
      return `${diffMinutes}分钟前`;
    } else if (diffHours < 24) {
      return `${diffHours}小时前`;
    } else if (diffDays < 7) {
      return `${diffDays}天前`;
    } else {
      return format(date, 'MM-dd HH:mm', { locale: zhCN });
    }
  };

  // 插入 emoji
  const insertEmoji = (emoji: string) => {
    const textarea = inputRef.current;
    if (textarea) {
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newValue = newComment.slice(0, start) + emoji + newComment.slice(end);
      setNewComment(newValue);
      // 设置光标位置
      setTimeout(() => {
        textarea.focus();
        textarea.setSelectionRange(start + emoji.length, start + emoji.length);
      }, 0);
    } else {
      setNewComment(prev => prev + emoji);
    }
    setShowEmojiPicker(false);
  };

  // 加载评论
  const loadComments = useCallback(async () => {
    if (!chapterId) return;

    try {
      setLoading(true);
      const response = await chapterCommentApi.getComments(chapterId, {
        page: 1,
        pageSize: 100,
        locationType: filter.type === 'all' ? 'chapter' : filter.type,
        paragraphIndex: filter.paragraphIndex,
        sentenceIndex: filter.sentenceIndex,
      });
      setComments(response.items);
    } catch (err) {
      console.error('加载评论失败:', err);
      showError('加载评论失败');
    } finally {
      setLoading(false);
    }
  }, [chapterId, filter.type, filter.paragraphIndex, filter.sentenceIndex, showError]);

  // 加载评论统计
  const loadStats = useCallback(async () => {
    if (!chapterId || !onStatsUpdate) return;

    try {
      const stats = await chapterCommentApi.getStats(chapterId);
      onStatsUpdate(stats);
    } catch (err) {
      console.error('加载评论统计失败:', err);
    }
  }, [chapterId, onStatsUpdate]);

  useEffect(() => {
    if (isOpen) {
      loadComments();
    }
  }, [isOpen, loadComments]);

  // 提交评论
  const handleSubmit = async () => {
    if (!newComment.trim() || !user) return;

    try {
      setSubmitting(true);
      await chapterCommentApi.createComment(chapterId, {
        content: newComment.trim(),
        locationType: filter.type === 'all' ? 'chapter' : filter.type,
        paragraphIndex: filter.paragraphIndex,
        sentenceIndex: filter.sentenceIndex,
        parentId: replyingTo?.id,
        replyToUserId: replyingTo?.user?.id,
      });

      setNewComment('');
      setReplyingTo(null);
      success('评论发表成功');
      loadComments();
      loadStats();
    } catch (err) {
      console.error('发表评论失败:', err);
      showError('发表评论失败');
    } finally {
      setSubmitting(false);
    }
  };

  // 点赞
  const handleLike = async (comment: ChapterComment) => {
    if (!user) {
      showError('请先登录');
      return;
    }

    try {
      if (comment.isLiked) {
        await chapterCommentApi.unlikeComment(comment.id);
      } else {
        await chapterCommentApi.likeComment(comment.id);
      }
      loadComments();
    } catch (err) {
      console.error('操作失败:', err);
    }
  };

  // 删除评论
  const handleDelete = async (commentId: string) => {
    try {
      await chapterCommentApi.deleteComment(commentId);
      success('删除成功');
      loadComments();
      loadStats();
    } catch (err) {
      console.error('删除失败:', err);
      showError('删除失败');
    }
  };

  // 举报
  const handleReport = async (commentId: string) => {
    if (!reportReason) {
      showError('请选择举报原因');
      return;
    }

    try {
      await chapterCommentApi.reportComment(commentId, {
        reason: reportReason as ReportReason,
        description: reportDescription || undefined,
      });
      success('举报已提交');
      setShowReportDialog(null);
      setReportReason('');
      setReportDescription('');
    } catch (err) {
      console.error('举报失败:', err);
      showError('举报失败');
    }
  };

  // 切换回复展开状态
  const toggleReplies = (commentId: string) => {
    setExpandedReplies(prev => {
      const next = new Set(prev);
      if (next.has(commentId)) {
        next.delete(commentId);
      } else {
        next.add(commentId);
      }
      return next;
    });
  };

  // 开始回复
  const startReply = (comment: ChapterComment) => {
    setReplyingTo(comment);
    inputRef.current?.focus();
  };

  // 获取筛选标题
  const getFilterTitle = () => {
    if (filter.type === 'all') {
      return '章节评论';
    }
    // 段落或句子评论，显示引用文本
    if (filter.quotedText) {
      // 截取前30个字符，超出显示省略号
      const maxLen = 30;
      const text = filter.quotedText.length > maxLen
        ? filter.quotedText.slice(0, maxLen) + '...'
        : filter.quotedText;
      return `"${text}"`;
    }
    // 兜底显示
    if (filter.type === 'paragraph') {
      return `第 ${(filter.paragraphIndex ?? 0) + 1} 段评论`;
    }
    return `第 ${(filter.paragraphIndex ?? 0) + 1} 段第 ${(filter.sentenceIndex ?? 0) + 1} 句评论`;
  };

  // 渲染单条评论（带主题）
  const renderCommentWithTheme = (comment: ChapterComment, isReply = false) => {
    const isOwner = user?.id === comment.user?.id;

    return (
      <div
        key={comment.id}
        className={`${isReply ? 'ml-8 mt-3' : 'py-3'}`}
        style={{
          borderBottom: isReply ? 'none' : `1px solid ${isDarkMode ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)'}`,
        }}
      >
        <div className="flex items-start gap-3">
          {/* 头像 */}
          <Avatar className="w-8 h-8 shrink-0">
            <AvatarImage src={comment.user?.avatar} />
            <AvatarFallback className="text-xs bg-gradient-to-br from-blue-400 to-purple-500 text-white">
              {comment.user?.username?.charAt(0).toUpperCase() || '?'}
            </AvatarFallback>
          </Avatar>

          <div className="flex-1 min-w-0">
            {/* 用户名 */}
            <div className="flex items-center gap-2 mb-1">
              <span className="text-sm font-medium" style={{ color: textColor }}>
                {comment.user?.username || '匿名用户'}
              </span>
              {comment.replyToUser && (
                <>
                  <span className="text-xs opacity-50" style={{ color: textColor }}>回复</span>
                  <span className="text-xs text-blue-500">
                    {comment.replyToUser.username}
                  </span>
                </>
              )}
            </div>

            {/* 引用文本 */}
            {comment.quotedText && (
              <div
                className="mb-2 text-xs"
                style={{
                  color: textColor,
                  opacity: 0.7,
                }}
              >
                "{comment.quotedText.length > 30 ? comment.quotedText.slice(0, 30) + '...' : comment.quotedText}"
              </div>
            )}

            {/* 评论内容 */}
            <p
              className="text-sm whitespace-pre-wrap break-words leading-relaxed"
              style={{ color: textColor }}
            >
              {comment.content}
            </p>

            {/* 操作栏 */}
            <div className="flex items-center gap-4 mt-2">
              <button
                onClick={() => handleLike(comment)}
                className={`flex items-center gap-1 text-xs transition-colors ${
                  comment.isLiked ? 'text-blue-500' : ''
                }`}
                style={{ color: comment.isLiked ? undefined : textColor, opacity: comment.isLiked ? 1 : 0.5 }}
              >
                <ThumbsUp className="w-3.5 h-3.5" />
                <span>{comment.likeCount || ''}</span>
              </button>

              {!isReply && (
                <button
                  onClick={() => startReply(comment)}
                  className="flex items-center gap-1 text-xs transition-colors hover:text-blue-500"
                  style={{ color: textColor, opacity: 0.5 }}
                >
                  <Reply className="w-3.5 h-3.5" />
                  <span>回复</span>
                </button>
              )}

              <div className="relative">
                <button
                  onClick={() => setActiveMenu(activeMenu === comment.id ? null : comment.id)}
                  className="p-1 transition-colors hover:bg-black/10 dark:hover:bg-white/10 rounded"
                  style={{ color: textColor, opacity: 0.5 }}
                >
                  <MoreHorizontal className="w-3.5 h-3.5" />
                </button>

                {activeMenu === comment.id && (
                  <>
                    <div className="fixed inset-0 z-10" onClick={() => setActiveMenu(null)} />
                    <div
                      className="absolute left-0 top-full mt-1 z-20 rounded-lg shadow-lg py-1 min-w-[100px]"
                      style={{
                        backgroundColor: isDarkMode ? 'rgba(30,30,30,0.95)' : 'rgba(255,255,255,0.95)',
                        backdropFilter: 'blur(8px)',
                        border: `1px solid ${isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`,
                      }}
                    >
                      {isOwner && (
                        <button
                          onClick={() => {
                            handleDelete(comment.id);
                            setActiveMenu(null);
                          }}
                          className="w-full flex items-center gap-2 px-3 py-1.5 text-xs text-red-500 hover:bg-red-500/10"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                          删除
                        </button>
                      )}
                      <button
                        onClick={() => {
                          setShowReportDialog(comment.id);
                          setActiveMenu(null);
                        }}
                        className="w-full flex items-center gap-2 px-3 py-1.5 text-xs transition-colors"
                        style={{ color: textColor }}
                      >
                        <Flag className="w-3.5 h-3.5" />
                        举报
                      </button>
                    </div>
                  </>
                )}
              </div>

              {/* 时间显示在最右侧 */}
              <span className="text-xs opacity-40 ml-auto" style={{ color: textColor }}>
                {formatCommentTime(comment.createdAt)}
              </span>
            </div>

            {/* 回复列表 */}
            {!isReply && comment.replyCount > 0 && (
              <div className="mt-2">
                <button
                  onClick={() => toggleReplies(comment.id)}
                  className="flex items-center gap-1 text-xs text-blue-500 hover:underline"
                >
                  {expandedReplies.has(comment.id) ? (
                    <>
                      <ChevronUp className="w-3 h-3" />
                      收起 {comment.replyCount} 条回复
                    </>
                  ) : (
                    <>
                      <ChevronDown className="w-3 h-3" />
                      查看 {comment.replyCount} 条回复
                    </>
                  )}
                </button>

                {expandedReplies.has(comment.id) && comment.replies && (
                  <div className="mt-2">
                    {comment.replies.map(reply => renderCommentWithTheme(reply, true))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  if (!isOpen) return null;

  return (
    <div
      ref={panelRef}
      className="h-full flex flex-col border-l transition-colors"
      style={{
        borderColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)',
        backgroundColor: isDarkMode ? 'rgba(0,0,0,0.3)' : 'rgba(255,255,255,0.85)',
        backdropFilter: 'blur(12px)',
      }}
    >
      {/* 头部 */}
      <div
        className="flex-shrink-0 px-4 py-3 border-b"
        style={{
          borderColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)',
          backgroundColor: isDarkMode ? 'rgba(0,0,0,0.2)' : 'rgba(255,255,255,0.5)',
        }}
      >
        <div className="flex items-center justify-between">
          <h2
            className="text-sm font-bold flex items-center gap-2 truncate flex-1 mr-2"
            style={{ color: textColor }}
          >
            <span className="truncate">{getFilterTitle()}</span>
            <span
              className="text-xs font-normal px-1.5 py-0.5 rounded-full flex-shrink-0"
              style={{
                backgroundColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)',
                opacity: 0.7,
              }}
            >
              {comments.length}
            </span>
          </h2>
          <button
            onClick={onClose}
            className="p-1.5 rounded-full transition-colors hover:bg-black/10 dark:hover:bg-white/10 flex-shrink-0"
            style={{ color: textColor }}
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 评论列表 */}
      <div className="flex-1 overflow-y-auto px-4">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-6 h-6 animate-spin text-blue-500" />
          </div>
        ) : comments.length === 0 ? (
          <div
            className="flex flex-col items-center justify-center py-12 opacity-60"
            style={{ color: textColor }}
          >
            <MessageCircle className="w-10 h-10 mb-3 opacity-50" />
            <p className="text-sm">暂无评论</p>
            <p className="text-xs mt-1 opacity-70">成为第一个评论的人吧</p>
          </div>
        ) : (
          <div className="py-2">
            {comments.map(comment => renderCommentWithTheme(comment))}
          </div>
        )}
      </div>

      {/* 发表评论区 */}
      <div
        className="flex-shrink-0 px-4 py-3 border-t"
        style={{
          borderColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)',
          backgroundColor: isDarkMode ? 'rgba(0,0,0,0.2)' : 'rgba(255,255,255,0.5)',
        }}
      >
        {replyingTo && (
          <div
            className="flex items-center justify-between mb-2 px-2.5 py-1.5 rounded-lg"
            style={{
              backgroundColor: isDarkMode ? 'rgba(59,130,246,0.2)' : 'rgba(59,130,246,0.1)',
            }}
          >
            <span className="text-xs text-blue-500">
              回复 @{replyingTo.user?.username}
            </span>
            <button
              onClick={() => setReplyingTo(null)}
              className="text-blue-500 hover:text-blue-600"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        <div className="flex flex-col gap-2">
          <textarea
            ref={inputRef}
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder={user ? '发表评论...' : '请先登录'}
            disabled={!user}
            className="w-full px-3 py-2 text-sm rounded-lg border resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            style={{
              backgroundColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)',
              borderColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
              color: textColor,
            }}
            rows={2}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                handleSubmit();
              }
            }}
          />
          <div className="flex items-center justify-between">
            {/* Emoji 选择器 */}
            <div className="relative">
              <button
                onClick={() => user && setShowEmojiPicker(!showEmojiPicker)}
                disabled={!user}
                className="p-1.5 rounded-lg transition-colors hover:bg-black/10 dark:hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed"
                style={{ color: textColor, opacity: 0.6 }}
                title="插入表情"
              >
                <Smile className="w-5 h-5" />
              </button>
              {showEmojiPicker && (
                <>
                  <div className="fixed inset-0 z-10" onClick={() => setShowEmojiPicker(false)} />
                  <div
                    className="absolute bottom-full left-0 mb-2 p-2 rounded-lg shadow-lg z-20 w-64"
                    style={{
                      backgroundColor: isDarkMode ? 'rgba(30,30,30,0.95)' : 'rgba(255,255,255,0.95)',
                      backdropFilter: 'blur(8px)',
                      border: `1px solid ${isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`,
                    }}
                  >
                    <div className="grid grid-cols-8 gap-1">
                      {commonEmojis.map((emoji) => (
                        <button
                          key={emoji}
                          onClick={() => insertEmoji(emoji)}
                          className="w-7 h-7 flex items-center justify-center text-lg hover:bg-black/10 dark:hover:bg-white/10 rounded transition-colors"
                        >
                          {emoji}
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              )}
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs opacity-40" style={{ color: textColor }}>
                Ctrl+Enter 发送
              </span>
              <button
                onClick={handleSubmit}
                disabled={!newComment.trim() || submitting || !user}
                className="px-3 py-1.5 bg-blue-500 text-white text-sm rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {submitting ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  '发送'
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
      {/* 举报对话框 */}
      {showReportDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div
            className="rounded-2xl shadow-2xl w-full max-w-xs mx-4 p-5"
            style={{
              backgroundColor: isDarkMode ? 'rgba(30,30,30,0.95)' : 'rgba(255,255,255,0.95)',
              backdropFilter: 'blur(12px)',
            }}
          >
            <h3 className="text-sm font-bold mb-4" style={{ color: textColor }}>举报评论</h3>

            <div className="space-y-2 mb-4">
              {[
                { value: 'spam', label: '垃圾内容' },
                { value: 'abuse', label: '辱骂攻击' },
                { value: 'porn', label: '色情低俗' },
                { value: 'illegal', label: '违法违规' },
                { value: 'false', label: '虚假信息' },
                { value: 'other', label: '其他原因' },
              ].map(option => (
                <label
                  key={option.value}
                  className="flex items-center gap-2 p-2.5 rounded-lg cursor-pointer transition-colors"
                  style={{
                    backgroundColor: reportReason === option.value
                      ? (isDarkMode ? 'rgba(59,130,246,0.2)' : 'rgba(59,130,246,0.1)')
                      : (isDarkMode ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)'),
                    border: `1px solid ${isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)'}`,
                  }}
                >
                  <input
                    type="radio"
                    name="reportReason"
                    value={option.value}
                    checked={reportReason === option.value}
                    onChange={(e) => setReportReason(e.target.value as ReportReason)}
                    className="text-blue-500 w-3.5 h-3.5 accent-blue-500"
                  />
                  <span className="text-xs" style={{ color: textColor }}>{option.label}</span>
                </label>
              ))}
            </div>

            <textarea
              value={reportDescription}
              onChange={(e) => setReportDescription(e.target.value)}
              placeholder="详细描述（可选）"
              className="w-full px-3 py-2 text-xs rounded-lg border resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/50 mb-4"
              style={{
                backgroundColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)',
                borderColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
                color: textColor,
              }}
              rows={2}
            />

            <div className="flex gap-2">
              <button
                onClick={() => {
                  setShowReportDialog(null);
                  setReportReason('');
                  setReportDescription('');
                }}
                className="flex-1 px-3 py-2 text-xs rounded-lg transition-colors"
                style={{
                  backgroundColor: isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)',
                  color: textColor,
                }}
              >
                取消
              </button>
              <button
                onClick={() => handleReport(showReportDialog)}
                className="flex-1 px-3 py-2 text-xs bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
              >
                提交举报
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ChapterCommentPanel;
