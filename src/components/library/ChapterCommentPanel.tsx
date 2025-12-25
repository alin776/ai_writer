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
} from 'lucide-react';
import { chapterCommentApi, ChapterComment, CommentLocationStats, ReportReason } from '../../services/chapterCommentApi';
import { useAuthStore } from '../../store/authStore';
import { useGlobalStore } from '../../store/globalStore';
import { formatDistanceToNow } from 'date-fns';
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
}

export function ChapterCommentPanel({
  chapterId,
  isOpen,
  onClose,
  filter = { type: 'all' },
  onStatsUpdate,
}: ChapterCommentPanelProps) {
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

  const inputRef = useRef<HTMLTextAreaElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);

  // 加载评论
  const loadComments = useCallback(async () => {
    if (!chapterId) return;

    try {
      setLoading(true);
      const response = await chapterCommentApi.getComments(chapterId, {
        page: 1,
        pageSize: 100,
        locationType: filter.type === 'all' ? undefined : filter.type,
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

  // 渲染单条评论
  const renderComment = (comment: ChapterComment, isReply = false) => {
    const isOwner = user?.id === comment.user?.id;

    return (
      <div
        key={comment.id}
        className={`${isReply ? 'ml-6 mt-2' : 'py-2.5 border-b border-gray-100 dark:border-slate-700'}`}
      >
        <div className="flex items-start gap-2">
          {/* 头像 */}
          <div className="w-6 h-6 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white text-xs font-medium flex-shrink-0">
            {comment.user?.avatar ? (
              <img src={comment.user.avatar} alt="" className="w-full h-full rounded-full object-cover" />
            ) : (
              comment.user?.username?.charAt(0).toUpperCase() || '?'
            )}
          </div>

          <div className="flex-1 min-w-0">
            {/* 用户名和时间 */}
            <div className="flex items-center gap-1.5 mb-0.5">
              <span className="text-xs font-medium text-gray-900 dark:text-white">
                {comment.user?.username || '匿名用户'}
              </span>
              {comment.replyToUser && (
                <>
                  <span className="text-[10px] text-gray-400">回复</span>
                  <span className="text-xs text-blue-600 dark:text-blue-400">
                    @{comment.replyToUser.username}
                  </span>
                </>
              )}
              <span className="text-[10px] text-gray-400 dark:text-slate-500">
                {formatDistanceToNow(new Date(comment.createdAt), { locale: zhCN, addSuffix: true })}
              </span>
            </div>

            {/* 引用文本 */}
            {comment.quotedText && (
              <div className="mb-1.5 px-2 py-1 bg-gray-50 dark:bg-slate-800/50 border-l-2 border-blue-400 text-xs text-gray-600 dark:text-slate-400 italic">
                "{comment.quotedText}"
              </div>
            )}

            {/* 评论内容 */}
            <p className="text-xs text-gray-700 dark:text-slate-300 whitespace-pre-wrap break-words leading-relaxed">
              {comment.content}
            </p>

            {/* 操作栏 */}
            <div className="flex items-center gap-3 mt-1.5">
              <button
                onClick={() => handleLike(comment)}
                className={`flex items-center gap-0.5 text-[10px] transition-colors ${
                  comment.isLiked
                    ? 'text-blue-600 dark:text-blue-400'
                    : 'text-gray-400 hover:text-gray-600 dark:hover:text-slate-300'
                }`}
              >
                <ThumbsUp className="w-3 h-3" />
                <span>{comment.likeCount || ''}</span>
              </button>

              {!isReply && (
                <button
                  onClick={() => startReply(comment)}
                  className="flex items-center gap-0.5 text-[10px] text-gray-400 hover:text-gray-600 dark:hover:text-slate-300 transition-colors"
                >
                  <Reply className="w-3 h-3" />
                  <span>回复</span>
                </button>
              )}

              <div className="relative">
                <button
                  onClick={() => setActiveMenu(activeMenu === comment.id ? null : comment.id)}
                  className="p-0.5 text-gray-400 hover:text-gray-600 dark:hover:text-slate-300 transition-colors"
                >
                  <MoreHorizontal className="w-3 h-3" />
                </button>

                {activeMenu === comment.id && (
                  <>
                    <div className="fixed inset-0 z-10" onClick={() => setActiveMenu(null)} />
                    <div className="absolute left-0 top-full mt-1 z-20 bg-white dark:bg-slate-800 rounded shadow-lg border border-gray-200 dark:border-slate-700 py-0.5 min-w-[80px]">
                      {isOwner && (
                        <button
                          onClick={() => {
                            handleDelete(comment.id);
                            setActiveMenu(null);
                          }}
                          className="w-full flex items-center gap-1.5 px-2 py-1 text-xs text-red-600 hover:bg-gray-100 dark:hover:bg-slate-700"
                        >
                          <Trash2 className="w-3 h-3" />
                          删除
                        </button>
                      )}
                      <button
                        onClick={() => {
                          setShowReportDialog(comment.id);
                          setActiveMenu(null);
                        }}
                        className="w-full flex items-center gap-1.5 px-2 py-1 text-xs text-gray-700 dark:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-700"
                      >
                        <Flag className="w-3 h-3" />
                        举报
                      </button>
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* 回复列表 */}
            {!isReply && comment.replyCount > 0 && (
              <div className="mt-2">
                <button
                  onClick={() => toggleReplies(comment.id)}
                  className="flex items-center gap-0.5 text-[10px] text-blue-600 dark:text-blue-400 hover:underline"
                >
                  {expandedReplies.has(comment.id) ? (
                    <>
                      <ChevronUp className="w-2.5 h-2.5" />
                      收起 {comment.replyCount} 条回复
                    </>
                  ) : (
                    <>
                      <ChevronDown className="w-2.5 h-2.5" />
                      查看 {comment.replyCount} 条回复
                    </>
                  )}
                </button>

                {expandedReplies.has(comment.id) && comment.replies && (
                  <div className="mt-1.5">
                    {comment.replies.map(reply => renderComment(reply, true))}
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
    <>
      {/* 遮罩层 */}
      <div
        className="fixed inset-0 top-[52px] z-20 bg-black/30 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* 评论面板 */}
      <div
        ref={panelRef}
        className="fixed top-[52px] right-0 bottom-0 w-80 z-30 bg-white dark:bg-slate-900 shadow-2xl flex flex-col border-l border-gray-200 dark:border-slate-700"
      >
        {/* 头部 */}
        <div className="flex-shrink-0 px-3 py-2 border-b border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-800/50">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-bold text-gray-900 dark:text-white flex items-center gap-1.5 truncate flex-1 mr-2">
              <MessageCircle className="w-3.5 h-3.5 text-blue-500 flex-shrink-0" />
              <span className="truncate">{getFilterTitle()}</span>
              <span className="text-[10px] font-normal text-gray-500 flex-shrink-0">({comments.length})</span>
            </h2>
            <button
              onClick={onClose}
              className="p-0.5 text-gray-400 hover:text-gray-600 dark:text-slate-500 dark:hover:text-slate-300 transition-colors flex-shrink-0"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* 评论列表 */}
        <div className="flex-1 overflow-y-auto px-3">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
            </div>
          ) : comments.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-gray-400 dark:text-slate-500">
              <MessageCircle className="w-8 h-8 mb-2 opacity-50" />
              <p className="text-xs">暂无评论</p>
              <p className="text-[10px] mt-0.5">成为第一个评论的人吧</p>
            </div>
          ) : (
            <div className="py-1">
              {comments.map(comment => renderComment(comment))}
            </div>
          )}
        </div>

        {/* 发表评论区 */}
        <div className="flex-shrink-0 px-3 py-2 border-t border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-800/50">
          {replyingTo && (
            <div className="flex items-center justify-between mb-1.5 px-2 py-1 bg-blue-50 dark:bg-blue-900/20 rounded">
              <span className="text-[10px] text-blue-600 dark:text-blue-400">
                回复 @{replyingTo.user?.username}
              </span>
              <button
                onClick={() => setReplyingTo(null)}
                className="text-blue-600 dark:text-blue-400 hover:text-blue-800"
              >
                <X className="w-3 h-3" />
              </button>
            </div>
          )}

          <div className="flex items-end gap-1.5">
            <textarea
              ref={inputRef}
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              placeholder={user ? '发表评论...' : '请先登录'}
              disabled={!user}
              className="flex-1 px-2 py-1.5 text-xs bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded resize-none focus:outline-none focus:border-blue-400 dark:focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              rows={2}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                  handleSubmit();
                }
              }}
            />
            <button
              onClick={handleSubmit}
              disabled={!newComment.trim() || submitting || !user}
              className="px-2.5 py-1.5 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {submitting ? (
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
              ) : (
                <Send className="w-3.5 h-3.5" />
              )}
            </button>
          </div>
          <p className="text-[10px] text-gray-400 dark:text-slate-500 mt-1">
            Ctrl + Enter 发送
          </p>
        </div>
      </div>

      {/* 举报对话框 */}
      {showReportDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="bg-white dark:bg-slate-900 rounded-lg shadow-xl w-full max-w-xs mx-4 p-4">
            <h3 className="text-sm font-bold text-gray-900 dark:text-white mb-3">举报评论</h3>

            <div className="space-y-2 mb-3">
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
                  className="flex items-center gap-2 p-2 border border-gray-200 dark:border-slate-700 rounded cursor-pointer hover:bg-gray-50 dark:hover:bg-slate-800"
                >
                  <input
                    type="radio"
                    name="reportReason"
                    value={option.value}
                    checked={reportReason === option.value}
                    onChange={(e) => setReportReason(e.target.value as ReportReason)}
                    className="text-blue-600 w-3 h-3"
                  />
                  <span className="text-xs text-gray-700 dark:text-slate-300">{option.label}</span>
                </label>
              ))}
            </div>

            <textarea
              value={reportDescription}
              onChange={(e) => setReportDescription(e.target.value)}
              placeholder="详细描述（可选）"
              className="w-full px-2 py-1.5 text-xs bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded resize-none focus:outline-none focus:border-blue-400 mb-3"
              rows={2}
            />

            <div className="flex gap-2">
              <button
                onClick={() => {
                  setShowReportDialog(null);
                  setReportReason('');
                  setReportDescription('');
                }}
                className="flex-1 px-3 py-1.5 text-xs border border-gray-200 dark:border-slate-700 text-gray-700 dark:text-slate-300 rounded hover:bg-gray-50 dark:hover:bg-slate-800"
              >
                取消
              </button>
              <button
                onClick={() => handleReport(showReportDialog)}
                className="flex-1 px-3 py-1.5 text-xs bg-red-600 text-white rounded hover:bg-red-700"
              >
                提交举报
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default ChapterCommentPanel;
