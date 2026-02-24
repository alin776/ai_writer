/**
 * 章节评论面板组件
 */
import { useState, useEffect, useRef, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { useNavigate } from 'react-router-dom';
import {
  X,
  MessageCircle,
  Send,
  Loader2,
  ThumbsUp,
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
import type { CSSProperties } from 'react';
import { zhCN } from 'date-fns/locale';
import EmojiPicker from '../../views/ChannelsView/components/EmojiPicker';

interface ChapterCommentPanelProps {
  workId: string;
  chapterNum: number;
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
  highlightCommentId?: string | null;
  onLocateComment?: (comment: ChapterComment) => void;
}

export function ChapterCommentPanel({
  workId,
  chapterNum,
  isOpen,
  onClose,
  filter = { type: 'all' },
  onStatsUpdate,
  themeColors,
  highlightCommentId,
  onLocateComment,
}: ChapterCommentPanelProps) {
  const { backgroundColor = '#faf8f3', textColor = '#333333', isDarkMode = false } = themeColors || {};
  const { user } = useAuthStore();
  const { success, error: showError } = useGlobalStore();
  const navigate = useNavigate();

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
  const [emojiPickerStyle, setEmojiPickerStyle] = useState<CSSProperties>({});
  const [stickerDraftUrl, setStickerDraftUrl] = useState<string | null>(null);
  const [highlightedCommentId, setHighlightedCommentId] = useState<string | null>(null);

  const inputRef = useRef<HTMLTextAreaElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const emojiButtonRef = useRef<HTMLButtonElement>(null);
  const lastHandledHighlightRef = useRef<string | null>(null);
  const highlightScrollTimerRef = useRef<number | null>(null);
  const highlightClearTimerRef = useRef<number | null>(null);

  // 常用 emoji 列表

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
        adjustTextareaHeight();
      }, 0);
    } else {
      setNewComment(prev => prev + emoji);
    }
    setShowEmojiPicker(false);
  };

  const updateEmojiPickerPosition = useCallback(() => {
    if (!emojiButtonRef.current) return;
    const rect = emojiButtonRef.current.getBoundingClientRect();
    const pickerHeight = 384;
    const pickerWidth = 320;
    const spaceBelow = window.innerHeight - rect.bottom;
    const spaceAbove = rect.top;

    let top: number;
    if (spaceBelow >= pickerHeight) {
      top = rect.bottom + 8;
    } else if (spaceAbove >= pickerHeight) {
      top = rect.top - pickerHeight - 8;
    } else {
      top = spaceBelow >= spaceAbove ? rect.bottom + 8 : rect.top - pickerHeight - 8;
    }

    let left = rect.left;
    if (left + pickerWidth > window.innerWidth - 8) {
      left = window.innerWidth - pickerWidth - 8;
    }
    if (left < 8) left = 8;

    setEmojiPickerStyle({
      position: 'fixed',
      top: `${top}px`,
      left: `${left}px`,
      zIndex: 9999,
      width: `${pickerWidth}px`,
    });
  }, []);

  useEffect(() => {
    if (!showEmojiPicker) return;
    updateEmojiPickerPosition();

    const handleWindowChange = () => updateEmojiPickerPosition();
    window.addEventListener('resize', handleWindowChange);
    window.addEventListener('scroll', handleWindowChange, true);
    return () => {
      window.removeEventListener('resize', handleWindowChange);
      window.removeEventListener('scroll', handleWindowChange, true);
    };
  }, [showEmojiPicker, updateEmojiPickerPosition]);

  const insertSticker = (stickerUrl: string) => {
    setStickerDraftUrl(stickerUrl);
    setShowEmojiPicker(false);
    setTimeout(() => {
      inputRef.current?.focus();
      adjustTextareaHeight();
    }, 0);
  };

  // 自动调整输入框高度
  const adjustTextareaHeight = useCallback(() => {
    const textarea = inputRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
    }
  }, []);

  // 加载评论
  const loadComments = useCallback(async () => {
    if (!workId || !chapterNum) return;

    try {
      setLoading(true);
      const locationType = filter.type === 'all' ? undefined : filter.type;

      // When locating a specific comment, paginate until it is found (or all pages loaded).
      if (highlightCommentId && filter.type === 'all') {
        const pageSize = 100;
        let page = 1;
        let total = 0;
        let aggregated: ChapterComment[] = [];
        let found = false;

        while (!found) {
          const response = await chapterCommentApi.getComments(workId, chapterNum, {
            page,
            pageSize,
            locationType,
            paragraphIndex: filter.paragraphIndex,
            sentenceIndex: filter.sentenceIndex,
          });

          total = response.total;
          aggregated = aggregated.concat(response.items);

          found = response.items.some(
            (item) =>
              item.id === highlightCommentId ||
              (item.replies && item.replies.some((reply) => reply.id === highlightCommentId))
          );

          if (aggregated.length >= total || response.items.length === 0) {
            break;
          }
          page += 1;
        }

        setComments(aggregated);
      } else {
        const response = await chapterCommentApi.getComments(workId, chapterNum, {
          page: 1,
          pageSize: 100,
          locationType,
          paragraphIndex: filter.paragraphIndex,
          sentenceIndex: filter.sentenceIndex,
        });
        setComments(response.items);
      }
    } catch (err) {
      console.error('加载评论失败:', err);
      showError('加载评论失败');
    } finally {
      setLoading(false);
    }
  }, [workId, chapterNum, filter.type, filter.paragraphIndex, filter.sentenceIndex, highlightCommentId, showError]);

  // 加载评论统计
  const loadStats = useCallback(async () => {
    if (!workId || !chapterNum || !onStatsUpdate) return;

    try {
      const stats = await chapterCommentApi.getStats(workId, chapterNum);
      onStatsUpdate(stats);
    } catch (err) {
      console.error('加载评论统计失败:', err);
    }
  }, [workId, chapterNum, onStatsUpdate]);

  useEffect(() => {
    if (isOpen) {
      loadComments();
    }
  }, [isOpen, loadComments]);

  useEffect(() => {
    if (!highlightCommentId) {
      lastHandledHighlightRef.current = null;
      setHighlightedCommentId(null);
      if (highlightScrollTimerRef.current) {
        window.clearTimeout(highlightScrollTimerRef.current);
        highlightScrollTimerRef.current = null;
      }
      if (highlightClearTimerRef.current) {
        window.clearTimeout(highlightClearTimerRef.current);
        highlightClearTimerRef.current = null;
      }
    }
  }, [highlightCommentId]);

  const findCommentWithParent = (commentList: ChapterComment[], targetId: string): { comment: ChapterComment; parentId: string | null } | null => {
    for (const comment of commentList) {
      if (comment.id === targetId) {
        return { comment, parentId: null };
      }
      if (comment.replies && comment.replies.length > 0) {
        const reply = comment.replies.find(r => r.id === targetId);
        if (reply) {
          return { comment: reply, parentId: comment.id };
        }
      }
    }
    return null;
  };

  useEffect(() => {
    if (!highlightCommentId || comments.length === 0) return;
    if (lastHandledHighlightRef.current === highlightCommentId) return;

    const found = findCommentWithParent(comments, highlightCommentId);
    if (!found) return;

    lastHandledHighlightRef.current = highlightCommentId;
    onLocateComment?.(found.comment);

    if (found.parentId) {
      setExpandedReplies(prev => {
        if (prev.has(found.parentId!)) return prev;
        const next = new Set(prev);
        next.add(found.parentId!);
        return next;
      });
    }

    setHighlightedCommentId(highlightCommentId);

    if (highlightScrollTimerRef.current) {
      window.clearTimeout(highlightScrollTimerRef.current);
    }
    if (highlightClearTimerRef.current) {
      window.clearTimeout(highlightClearTimerRef.current);
    }

    highlightScrollTimerRef.current = window.setTimeout(() => {
      const el = document.getElementById(`chapter-comment-${highlightCommentId}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 200);

    highlightClearTimerRef.current = window.setTimeout(() => {
      setHighlightedCommentId(null);
    }, 3000);
  }, [highlightCommentId, comments]);

  useEffect(() => {
    return () => {
      if (highlightScrollTimerRef.current) {
        window.clearTimeout(highlightScrollTimerRef.current);
      }
      if (highlightClearTimerRef.current) {
        window.clearTimeout(highlightClearTimerRef.current);
      }
    };
  }, []);

  const emojiPickerPortal = showEmojiPicker && typeof document !== 'undefined'
    ? createPortal(
        <>
          <div className="fixed inset-0 z-40" onClick={() => setShowEmojiPicker(false)} />
          <div className="fixed z-50 emoji-picker" style={emojiPickerStyle}>
            <EmojiPicker
              onSelect={insertEmoji}
              onSelectSticker={insertSticker}
              onClose={() => setShowEmojiPicker(false)}
            />
          </div>
        </>,
        document.body
      )
    : null;

  // 提交评论
  const handleSubmit = async () => {
    const trimmedText = newComment.trim();
    const contentToSend = stickerDraftUrl
      ? (trimmedText ? `${trimmedText}\n![sticker](${stickerDraftUrl})` : `![sticker](${stickerDraftUrl})`)
      : trimmedText;
    if (!contentToSend || !user) return;

    try {
      setSubmitting(true);
      await chapterCommentApi.createComment(workId, chapterNum, {
        content: contentToSend,
        locationType: filter.type === 'all' ? 'chapter' : filter.type,
        paragraphIndex: filter.paragraphIndex,
        sentenceIndex: filter.sentenceIndex,
        parentId: replyingTo?.id,
        replyToUserId: replyingTo?.user?.id,
      });

      setNewComment('');
      setStickerDraftUrl(null);
      setReplyingTo(null);
      // 重置输入框高度
      if (inputRef.current) {
        inputRef.current.style.height = 'auto';
      }
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

  // 递归更新评论树中某个评论的状态
  const updateCommentInTree = (comments: ChapterComment[], commentId: string, updater: (c: ChapterComment) => ChapterComment): ChapterComment[] => {
    return comments.map(comment => {
      if (comment.id === commentId) {
        return updater(comment);
      }
      if (comment.replies && comment.replies.length > 0) {
        return {
          ...comment,
          replies: updateCommentInTree(comment.replies, commentId, updater)
        };
      }
      return comment;
    });
  };

  // 点赞 - 本地更新状态，避免重新加载
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
      // 本地更新状态
      setComments(prevComments => updateCommentInTree(prevComments, comment.id, (c) => ({
        ...c,
        isLiked: !c.isLiked,
        likeCount: c.isLiked ? c.likeCount - 1 : c.likeCount + 1,
      })));
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

  // 获取筛选标题（当前需求：只显示评论数）
  const getFilterTitle = () => null;

  // 计算总评论数（包括子评论）
  const getTotalCommentCount = (commentList: ChapterComment[]): number => {
    return commentList.reduce((total, comment) => {
      // 当前评论 + 递归计算子评论
      const replyCount = comment.replies ? getTotalCommentCount(comment.replies) : 0;
      return total + 1 + replyCount;
    }, 0);
  };

  // 渲染单条评论（带主题）- 使用小说评论风格
  const renderCommentWithTheme = (comment: ChapterComment, isReply = false) => {
    const isOwner = user?.id === comment.user?.id;
    const isHighlighted = highlightedCommentId === comment.id;
    const stickerUrls = comment.content
      ? Array.from(comment.content.matchAll(/!\[sticker\]\(([^)]+)\)/g)).map((m) => m[1])
      : [];
    const textContent = comment.content
      ? comment.content.replace(/!\[sticker\]\(([^)]+)\)/g, '').trim()
      : '';
    const hasTextLine = !!textContent || !!comment.replyToUser;

    return (
      <div
        key={comment.id}
        id={`chapter-comment-${comment.id}`}
        className={`flex gap-3 group ${isReply ? '-ml-2 mt-3' : 'py-3'} ${
          isHighlighted
            ? 'bg-blue-50 dark:bg-blue-900/30 ring-2 ring-blue-400 dark:ring-blue-500 rounded-lg animate-pulse'
            : ''
        }`}
      >
        {/* 头像 - 点击跳转到用户主页 */}
        {comment.user?.avatar ? (
          <div
            className={`${isReply ? 'w-6 h-6' : 'w-8 h-8'} rounded-full overflow-hidden flex-shrink-0 cursor-pointer`}
            onClick={() => comment.user?.id && navigate(`/user/${comment.user.id}`)}
          >
            <img
              src={comment.user.avatar}
              alt={comment.user.username}
              className="w-full h-full object-cover"
            />
          </div>
        ) : (
          <div
            className={`${isReply ? 'w-6 h-6 text-[10px]' : 'w-8 h-8 text-xs'} rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-medium flex-shrink-0 cursor-pointer`}
            onClick={() => comment.user?.id && navigate(`/user/${comment.user.id}`)}
          >
            {comment.user?.username?.[0]?.toUpperCase() || '?'}
          </div>
        )}

        {/* 评论内容 */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-0.5 flex-wrap">
            <span
              className="text-[13px] font-medium text-gray-900 dark:text-[#f1f1f1] cursor-pointer hover:underline"
              onClick={() => comment.user?.id && navigate(`/user/${comment.user.id}`)}
            >
              {comment.user?.username || '匿名用户'}
            </span>
            <span className="text-xs text-gray-500 dark:text-[#aaa]">
              {formatCommentTime(comment.createdAt)}
            </span>
            {/* 三点菜单 - hover时显示 */}
            <div className="relative ml-auto">
              <button
                onClick={() => setActiveMenu(activeMenu === comment.id ? null : comment.id)}
                className="p-1 rounded-full text-gray-400 hover:bg-gray-100 dark:hover:bg-[#272727] opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <MoreHorizontal className="w-4 h-4" />
              </button>

              {activeMenu === comment.id && (
                <>
                  <div className="fixed inset-0 z-10" onClick={() => setActiveMenu(null)} />
                  <div
                    className="absolute right-0 top-full mt-1 z-20 rounded-lg shadow-lg py-1 min-w-[100px]"
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
                      className="w-full flex items-center gap-2 px-3 py-1.5 text-xs text-gray-700 dark:text-[#f1f1f1] hover:bg-gray-100 dark:hover:bg-[#272727]"
                    >
                      <Flag className="w-3.5 h-3.5" />
                      举报
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* 引用文本 */}
          {comment.quotedText && (
            <div className="mb-1.5 text-xs text-gray-500 dark:text-[#aaa] italic">
              "{comment.quotedText.length > 30 ? comment.quotedText.slice(0, 30) + '...' : comment.quotedText}"
            </div>
          )}

          {/* 评论内容 - @回复用户和内容在同一行 */}
          {hasTextLine && (
            <p className="text-sm text-gray-800 dark:text-[#f1f1f1] leading-relaxed mb-1">
              {comment.replyToUser && (
                <span
                  className="text-[#3ea6ff] mr-1 cursor-pointer hover:underline"
                  onClick={() => comment.replyToUser?.id && navigate(`/user/${comment.replyToUser.id}`)}
                >
                  @{comment.replyToUser.username}
                </span>
              )}
              {textContent}
            </p>
          )}
          {stickerUrls.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-1">
              {stickerUrls.map((url) => (
                <img
                  key={url}
                  src={url}
                  alt="sticker"
                  className="rounded-lg border border-black/5 dark:border-white/10"
                  style={{
                    maxHeight: isReply ? 96 : 140,
                    maxWidth: isReply ? 160 : 220,
                  }}
                />
              ))}
            </div>
          )}

          {/* 操作按钮 - YouTube风格 */}
          <div className="flex items-center h-8 -ml-2">
            {/* 点赞按钮 */}
            <button
              onClick={() => handleLike(comment)}
              className={`flex items-center justify-center w-8 h-8 rounded-full transition-colors ${
                comment.isLiked
                  ? 'text-[#3ea6ff]'
                  : 'text-gray-500 dark:text-[#aaa] hover:bg-gray-100 dark:hover:bg-[#272727]'
              }`}
            >
              <ThumbsUp className="w-4 h-4" />
            </button>
            {comment.likeCount > 0 && (
              <span className="text-xs text-gray-500 dark:text-[#aaa] mr-1">{comment.likeCount}</span>
            )}

            {/* 回复按钮 - 主评论和二级评论都可以回复 */}
            <button
              onClick={() => startReply(comment)}
              className="h-8 px-3 text-xs font-medium text-gray-700 dark:text-[#f1f1f1] hover:bg-gray-100 dark:hover:bg-[#272727] rounded-full transition-colors"
            >
              回复
            </button>
          </div>

          {/* 回复列表 - 两层结构，所有回复平铺显示 */}
          {!isReply && comment.replyCount > 0 && (
              <div className="mt-2">
                {/* 展开按钮 - 未展开时显示 */}
                {!expandedReplies.has(comment.id) && (
                  <button
                    onClick={() => toggleReplies(comment.id)}
                    className="flex items-center gap-1 text-xs text-blue-500 hover:underline"
                  >
                    <ChevronDown className="w-3 h-3" />
                    查看 {comment.replyCount} 条回复
                  </button>
                )}

                {/* 回复列表 - 平铺显示，不递归 */}
                {expandedReplies.has(comment.id) && comment.replies && (
                  <div className="mt-2">
                    {comment.replies.map(reply => renderCommentWithTheme(reply, true))}
                    {/* 收起按钮 - 在回复列表后面 */}
                    <button
                      onClick={() => toggleReplies(comment.id)}
                      className="flex items-center gap-1 text-xs text-blue-500 hover:underline mt-2 -ml-2"
                    >
                      <ChevronUp className="w-3 h-3" />
                      收起回复
                    </button>
                  </div>
                )}
              </div>
            )}
        </div>
      </div>
    );
  };

  if (!isOpen) return null;

  return (
    <div
      ref={panelRef}
      className="h-full flex flex-col border-l border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 transition-colors"
    >
      {/* 头部 */}
      <div
        className="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-slate-700"
      >
        <div className="flex items-center justify-between">
          <h2
            className="text-sm font-bold flex items-center gap-2 truncate flex-1 mr-2"
            style={{ color: textColor }}
          >
            {getFilterTitle() && <span className="truncate">{getFilterTitle()}</span>}
            <span className="text-sm font-normal" style={{ color: textColor, opacity: 0.7 }}>
              {getTotalCommentCount(comments)}条评论
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

      {/* 发表评论区 - 频道风格 */}
      <div className="flex-shrink-0 p-3">
        {/* 主输入容器 - 使用与AIPanel相同的背景色 */}
        <div className="rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-800">
          {/* 回复预览 - 在容器内部顶部 */}
          {replyingTo && (
            <div
              className="flex items-center justify-between px-4 py-2 border-b"
              style={{
                borderColor: isDarkMode ? 'rgba(71,85,105,0.5)' : 'rgba(0,0,0,0.08)',
              }}
            >
              <div className="flex items-center gap-1.5 text-sm">
                <span style={{ color: textColor, opacity: 0.6 }}>回复</span>
                <span className="text-blue-500 font-medium">
                  @{replyingTo.user?.username}
                </span>
              </div>
              <button
                onClick={() => setReplyingTo(null)}
                className="p-1 rounded transition-colors hover:bg-black/10 dark:hover:bg-white/10"
                style={{ color: textColor, opacity: 0.5 }}
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}

            {/* 输入内容区域 */}
            <div className="px-4 py-3 space-y-3">
              {stickerDraftUrl && (
                <div className="flex items-center gap-3">
                  <div className="relative group">
                    <img
                      src={stickerDraftUrl}
                      alt="sticker"
                      className="rounded-lg border border-black/10 dark:border-white/10"
                      style={{ width: 96, height: 96, objectFit: 'contain' }}
                    />
                    <button
                      onClick={() => setStickerDraftUrl(null)}
                      className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-black/70 text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                      title="取消表情"
                    >
                      <X className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              )}
              {/* 输入框 */}
              <textarea
                ref={inputRef}
                value={newComment}
              onChange={(e) => {
                setNewComment(e.target.value);
                adjustTextareaHeight();
              }}
              placeholder={user ? '发表评论...' : '请先登录'}
              disabled={!user}
              className="w-full min-h-[40px] max-h-[120px] bg-transparent outline-none border-none text-sm placeholder:text-gray-400 dark:placeholder:text-slate-500 resize-none leading-relaxed disabled:opacity-50 disabled:cursor-not-allowed"
              style={{
                color: textColor,
              }}
              rows={1}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit();
                }
              }}
            />

            {/* 底部工具栏 */}
            <div className="flex items-center justify-between">
              {/* 左侧按钮组 */}
              <div className="flex items-center gap-1">
                {/* Emoji 选择器 */}
                <div className="relative">
                  <button
                    ref={emojiButtonRef}
                    onClick={() => {
                      if (!user) return;
                      setShowEmojiPicker((prev) => !prev);
                    }}
                    disabled={!user}
                    className="p-2 rounded-lg transition-colors hover:bg-black/10 dark:hover:bg-white/10 disabled:opacity-30"
                    style={{ color: textColor, opacity: 0.6 }}
                    title="插入表情"
                  >
                    <Smile className="w-4 h-4" />
                  </button>
                  {emojiPickerPortal}
                </div>
              </div>

              {/* 右侧发送按钮 - 圆形按钮，仅在有内容时显示 */}
              {(newComment.trim() || stickerDraftUrl) && (
                <button
                  onClick={handleSubmit}
                  disabled={(!newComment.trim() && !stickerDraftUrl) || submitting || !user}
                  className="w-9 h-9 rounded-full bg-blue-500 text-white flex items-center justify-center hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-95 shadow-sm"
                >
                  {submitting ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Send className="w-4 h-4" />
                  )}
                </button>
              )}
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
