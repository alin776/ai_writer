import {
  ArrowLeft,
  Eye,
  Heart,
  Star,
  Clock,
  BookOpen,
  Users,
  MessageCircle,
  ChevronDown,
  ThumbsUp,
  Flag,
  Trash2,
} from 'lucide-react';
import { formatUserError } from '@/utils/formatUserError';
import { Novel } from './NovelCard';
import { ImageWithFallback } from './ImageWithFallback';
import { useState, useEffect, useRef, useMemo } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { DataService } from '../../services/DataService';
import Modal from '../common/Modal';
import { useGlobalStore } from '../../store/globalStore';
import { useWorkNavStore } from '../../store/workNavStore';
import { NovelReader } from './NovelReader';
import MiniEmojiPicker from '../../views/ChannelsView/components/MiniEmojiPicker';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../ui/select';

interface NovelDetailProps {
  novel: Novel;
  onBack: () => void;
  /** 是否从书架进入，如果是则隐藏"加入书架"按钮 */
  isFromBookshelf?: boolean;
  /** 来源：小说广场或书架，用于独立管理阅读状态 */
  source?: 'novel-square' | 'bookshelf';
  /** 高亮显示的评论ID，用于从通知跳转时滚动到对应评论 */
  highlightCommentId?: string | null;
  /** 初始章节ID，用于从通知跳转时直接打开指定章节 */
  initialChapterId?: string | null;
  /** 高亮显示的章节评论ID，用于从通知跳转时定位到具体评论 */
  highlightChapterCommentId?: string | null;
}

interface Chapter {
  id: string;
  title: string;
  order: number;
  wordCount: number;
  viewCount: number;
  publishedAt: string;
}

interface Comment {
  id: string;
  userId: string;
  user?: {
    id: string;
    username: string;
    avatar?: string;
  };
  content: string;
  likeCount: number;
  createdAt: string;
  isDeleted: boolean;
  parentId?: string;
  replyToUserId?: string;
  replyToUser?: {
    id: string;
    username: string;
    avatar?: string;
  };
  isLiked?: boolean;
  isDisliked?: boolean;
  userRating?: number;
  replyCount?: number;
  replies?: Comment[];
}

interface RatingStats {
  averageRating: number;
  ratingCount: number;
  ratingDistribution: { [key: number]: number };
  userRating: number | null;
}

export function NovelDetail({ novel, onBack, isFromBookshelf = false, source = 'novel-square', highlightCommentId, initialChapterId, highlightChapterCommentId }: NovelDetailProps) {
  const navigate = useNavigate();
  const [expandedGroups, setExpandedGroups] = useState<Set<number>>(new Set([0]));
  const [userRating, setUserRating] = useState(0);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [visibleComments, setVisibleComments] = useState(5);

  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  const [commentContent, setCommentContent] = useState('');
  const [showCommentActions, setShowCommentActions] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [emojiPickerPosition, setEmojiPickerPosition] = useState<'top' | 'bottom'>('top');
  const emojiButtonRef = useRef<HTMLButtonElement>(null);
  const emojiPickerRef = useRef<HTMLDivElement>(null);
  const commentTextareaRef = useRef<HTMLTextAreaElement>(null);

  // 回复功能状态
  const [expandedReplies, setExpandedReplies] = useState<Set<string>>(new Set());
  const [replyToComment, setReplyToComment] = useState<{ commentId: string; username: string; parentId?: string; replyToUserId?: string; replyToReplyId?: string } | null>(null);
  const [replyContent, setReplyContent] = useState('');
  const [showReplyEmojiPicker, setShowReplyEmojiPicker] = useState(false);
  const replyEmojiButtonRef = useRef<HTMLButtonElement>(null);
  const replyEmojiPickerRef = useRef<HTMLDivElement>(null);
  const [replyEmojiPosition, setReplyEmojiPosition] = useState<'top' | 'bottom'>('bottom');

  // 评论排序状态
  const [commentSortBy, setCommentSortBy] = useState<'newest' | 'most_liked'>('newest');
  const [showSortMenu, setShowSortMenu] = useState(false);
  const sortMenuRef = useRef<HTMLDivElement>(null);

  // 高亮评论状态
  const [highlightedCommentId, setHighlightedCommentId] = useState<string | null>(null);
  const commentsSectionRef = useRef<HTMLDivElement>(null);

  // 存储从 API 加载的完整小说数据
  const [novelData, setNovelData] = useState<Novel>(novel);

  const descriptionParagraphs = useMemo(() => {
    const raw = (novelData?.description || '').split(/\n+/).map((p) => p.trim()).filter(Boolean);
    return raw.length > 0 ? raw : ['暂无简介'];
  }, [novelData?.description]);

  // 递归查找子评论所在的顶级评论
  const findParentCommentId = (targetId: string, comments: Comment[]): string | null => {
    for (const comment of comments) {
      if (comment.id === targetId) {
        return null; // 目标是顶级评论
      }
      if (comment.replies) {
        const foundInReplies = findInReplies(targetId, comment.replies);
        if (foundInReplies) {
          return comment.id; // 返回顶级评论 ID
        }
      }
    }
    return null;
  };

  // 递归在回复中查找目标评论
  const findInReplies = (targetId: string, replies: Comment[]): boolean => {
    for (const reply of replies) {
      if (reply.id === targetId) {
        return true;
      }
      if (reply.replies && findInReplies(targetId, reply.replies)) {
        return true;
      }
    }
    return false;
  };

  // 处理高亮评论滚动和闪烁效果
  useEffect(() => {
    if (highlightCommentId && comments.length > 0) {
      // 先查找是否为顶级评论
      const topLevelIndex = comments.findIndex(c => c.id === highlightCommentId);

      if (topLevelIndex !== -1) {
        // 目标是顶级评论
        if (topLevelIndex >= visibleComments) {
          setVisibleComments(topLevelIndex + 1);
        }
      } else {
        // 目标可能是子评论，查找其父级顶级评论
        const parentCommentId = findParentCommentId(highlightCommentId, comments);
        if (parentCommentId) {
          const parentIndex = comments.findIndex(c => c.id === parentCommentId);
          if (parentIndex !== -1) {
            // 确保父级评论在可见范围内
            if (parentIndex >= visibleComments) {
              setVisibleComments(parentIndex + 1);
            }
            // 展开父级评论的回复
            setExpandedReplies(prev => new Set(prev).add(parentCommentId));
          }
        }
      }

      setHighlightedCommentId(highlightCommentId);

      // 延迟滚动，确保评论已渲染
      setTimeout(() => {
        const commentElement = document.getElementById(`comment-${highlightCommentId}`);
        if (commentElement) {
          commentElement.scrollIntoView({ behavior: 'smooth', block: 'center' });

          // 3秒后移除高亮效果
          setTimeout(() => {
            setHighlightedCommentId(null);
          }, 3000);
        }
      }, 500);
    }
  }, [highlightCommentId, comments]);

  // 点击外部关闭表情选择器
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        showEmojiPicker &&
        emojiPickerRef.current &&
        emojiButtonRef.current &&
        !emojiPickerRef.current.contains(event.target as Node) &&
        !emojiButtonRef.current.contains(event.target as Node)
      ) {
        setShowEmojiPicker(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showEmojiPicker]);

  // 点击外部关闭子评论表情选择器
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        showReplyEmojiPicker &&
        replyEmojiPickerRef.current &&
        replyEmojiButtonRef.current &&
        !replyEmojiPickerRef.current.contains(event.target as Node) &&
        !replyEmojiButtonRef.current.contains(event.target as Node)
      ) {
        setShowReplyEmojiPicker(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showReplyEmojiPicker]);

  // 点击外部关闭排序菜单
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (showSortMenu && sortMenuRef.current && !sortMenuRef.current.contains(event.target as Node)) {
        setShowSortMenu(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showSortMenu]);

  // 排序改变时重新加载评论
  const handleSortChange = async (sortBy: 'newest' | 'most_liked') => {
    if (sortBy === commentSortBy) {
      setShowSortMenu(false);
      return;
    }
    setCommentSortBy(sortBy);
    setShowSortMenu(false);
    try {
      const commentsRes = await DataService.getWorkComments(novel.id, { sortBy });
      setComments(commentsRes.items || []);
    } catch (error) {
      console.error('加载评论失败:', error);
    }
  };

  // 优先从全局 store 读取缓存的书架状态，避免页面切换时状态丢失
  const [isInBookshelf, setIsInBookshelf] = useState(() => useWorkNavStore.getState().bookshelfMap[novel.id] || false);
  const [loading, setLoading] = useState(true);
  const [ratingStats, setRatingStats] = useState<RatingStats | null>(null);
  const [reportingCommentId, setReportingCommentId] = useState<string | null>(null);
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);
  const [currentUserAvatar, setCurrentUserAvatar] = useState<string | null>(null);
  const [currentUserName, setCurrentUserName] = useState<string | null>(null);
  const [favoriteCount, setFavoriteCount] = useState(novel.likes || 0);

  // 确认删除对话框
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteCommentId, setDeleteCommentId] = useState<string | null>(null);

  // 举报对话框
  const [showReportModal, setShowReportModal] = useState(false);
  const [reportReason, setReportReason] = useState('');
  const [reportDescription, setReportDescription] = useState('');

  // 阅读器状态
  const [showReader, setShowReader] = useState(false);
  const [selectedChapterId, setSelectedChapterId] = useState<string | undefined>(initialChapterId || undefined);

  // Toast
  const { success, error: showError } = useGlobalStore();

  // 获取章节记忆功能和阅读状态（根据来源使用不同的状态）
  const {
    getLastChapter,
    novelSquareReadingState,
    setNovelSquareReadingState,
    bookshelfReadingState,
    setBookshelfReadingState,
    setBookshelfStatus
  } = useWorkNavStore();

  // 根据来源获取对应的阅读状态
  const currentReadingState = source === 'bookshelf' ? bookshelfReadingState : novelSquareReadingState;
  const setCurrentReadingState = source === 'bookshelf' ? setBookshelfReadingState : setNovelSquareReadingState;
  // 订阅 store 中的书架状态，确保 persist 加载完成后能正确同步
  const storedBookshelfStatus = useWorkNavStore(state => state.bookshelfMap[novel.id]);

  // 防止 StrictMode 双重渲染导致的重复调用
  const hasLoadedRef = useRef<string | null>(null);
  // 防止重复自动进入阅读器
  const hasAutoEnteredReaderRef = useRef(false);
  // 标记 API 是否已经成功返回书架状态（用于防止 store 同步覆盖 API 结果）
  const hasBookshelfApiReturnedRef = useRef(false);

  // 当 novel prop 变化时，重置状态（防止快速切换小说时的状态残留）
  useEffect(() => {
    // 如果是新的小说，重置所有状态
    if (hasLoadedRef.current !== null && hasLoadedRef.current !== novel.id) {
      setNovelData(novel);
      setFavoriteCount(novel.likes || 0);
      setChapters([]);
      setComments([]);
      // 从全局 store 读取新小说的书架状态，而不是简单设为 false
      setIsInBookshelf(useWorkNavStore.getState().bookshelfMap[novel.id] || false);
      setRatingStats(null);
      setUserRating(0);
      setLoading(true);
      hasLoadedRef.current = null;
      // 重置 API 返回标记
      hasBookshelfApiReturnedRef.current = false;
    }
  }, [novel.id]);

  // 当 store 中的书架状态变化时（比如 persist 从 localStorage 加载完成），同步到本地状态
  // 只有在 API 还未成功返回时才同步，避免覆盖服务器返回的真实状态
  useEffect(() => {
    if (!hasBookshelfApiReturnedRef.current && storedBookshelfStatus !== undefined) {
      setIsInBookshelf(storedBookshelfStatus);
    }
  }, [storedBookshelfStatus]);

  // 加载作品详情数据
  useEffect(() => {
    // 如果已经加载过当前小说的数据，则跳过
    if (hasLoadedRef.current === novel.id) {
      return;
    }

    const loadData = async () => {
      try {
        setLoading(true);
        // 标记为已加载
        hasLoadedRef.current = novel.id;

        // 并行加载作品详情(含章节)、评论、书架状态、评分统计和当前用户信息
        const [detailRes, commentsRes, bookshelfStatus, ratingStatsRes, currentUser] = await Promise.all([
          DataService.getPublishedNovelDetail(novel.id),
          DataService.getWorkComments(novel.id, { sortBy: commentSortBy }).catch(() => ({ items: [] })),
          // API 失败时返回 null，保持本地缓存状态
          DataService.checkInBookshelf(novel.id).catch(() => null),
          DataService.getWorkRatingStats(novel.id).catch(() => null),
          DataService.getCurrentUser().catch(() => null),
        ]);

        // 更新小说数据（用于从轮播图等地方传入临时对象的情况）
        if (detailRes) {
          const genreMap: { [key: string]: string } = {
            fantasy: '玄幻', urban: '都市', romance: '言情', scifi: '科幻',
            wuxia: '武侠', game: '游戏', history: '历史', military: '军事',
            suspense: '悬疑', western_fantasy: '西幻', apocalypse: '末世', other: '其他',
          };
          const statusMap: { [key: string]: string } = {
            writing: '连载中', completed: '已完结', draft: '草稿', abandoned: '已弃坑',
          };
          setNovelData({
            id: detailRes.id,
            title: detailRes.title,
            author: detailRes.authorName,
            authorId: detailRes.authorId,
            authorAvatar: detailRes.authorAvatar,
            category: genreMap[detailRes.genre] || detailRes.genre,
            description: detailRes.description || '暂无简介',
            cover: detailRes.coverImage || novel.cover,
            views: detailRes.viewCount,
            likes: detailRes.favoriteCount || 0,
            rating: detailRes.averageRating || 0,
            chapters: detailRes.publishedChapterCount,
            status: (statusMap[detailRes.status] || '其他') as '连载中' | '已完结' | '其他',
          });
          setFavoriteCount(detailRes.favoriteCount || 0);
        }

        setChapters(detailRes?.chapters || []);
        setComments(commentsRes.items || []);
        // 处理书架状态：API 成功时以服务器为准，API 失败时保持本地缓存
        if (bookshelfStatus !== null) {
          hasBookshelfApiReturnedRef.current = true; // 标记 API 已成功返回
          // 注意：ApiAdapter 会将 snake_case 转换为 camelCase，所以是 inBookshelf 而不是 in_bookshelf
          const apiInBookshelf = bookshelfStatus.inBookshelf || false;
          // API 成功返回时，以服务器状态为准（确保数据同步）
          setIsInBookshelf(apiInBookshelf);
          setBookshelfStatus(novel.id, apiInBookshelf);
        }
        // 如果 API 失败（bookshelfStatus === null），保持初始化时从 store 读取的本地缓存状态
        setRatingStats(ratingStatsRes);
        setCurrentUserId(currentUser?.id || null);
        setCurrentUserAvatar(currentUser?.avatar || null);
        setCurrentUserName(currentUser?.username || null);
        if (ratingStatsRes?.userRating) {
          setUserRating(ratingStatsRes.userRating);
        }
      } catch (error) {
        console.error('加载作品详情失败:', error);
        // 加载失败时重置标记，允许重试
        hasLoadedRef.current = null;
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [novel.id]);

  // 自动进入阅读器（当从导航返回时恢复阅读状态）
  useEffect(() => {
    // 条件：数据已加载、有章节、未自动进入过、store 中记录了该小说正在阅读
    if (
      !loading &&
      chapters.length > 0 &&
      !hasAutoEnteredReaderRef.current &&
      currentReadingState?.novelId === novel.id &&
      currentReadingState?.isReading
    ) {
      hasAutoEnteredReaderRef.current = true;
      // 获取上次阅读的章节
      const lastChapterId = getLastChapter(novel.id);
      const targetChapterId = lastChapterId && chapters.some(c => c.id === lastChapterId)
        ? lastChapterId
        : chapters[0].id;
      // 自动进入阅读器
      setSelectedChapterId(targetChapterId);
      setShowReader(true);
    }
  }, [loading, chapters, currentReadingState, novel.id, getLastChapter]);

  // 从通知跳转时自动进入阅读模式
  useEffect(() => {
    if (
      !loading &&
      chapters.length > 0 &&
      initialChapterId &&
      !hasAutoEnteredReaderRef.current
    ) {
      hasAutoEnteredReaderRef.current = true;
      // 确保章节存在
      const targetChapter = chapters.find(c => c.id === initialChapterId);
      if (targetChapter) {
        setSelectedChapterId(initialChapterId);
        setShowReader(true);
      }
    }
  }, [loading, chapters, initialChapterId]);

  // 章节分组（每10章一组）
  const chapterGroups = chapters.reduce((groups: Chapter[][], chapter) => {
    const groupIndex = Math.floor((chapter.order - 1) / 10);
    if (!groups[groupIndex]) {
      groups[groupIndex] = [];
    }
    groups[groupIndex].push(chapter);
    return groups;
  }, []);

  const toggleGroup = (groupIndex: number) => {
    const newExpanded = new Set(expandedGroups);
    if (newExpanded.has(groupIndex)) {
      newExpanded.delete(groupIndex);
    } else {
      newExpanded.add(groupIndex);
    }
    setExpandedGroups(newExpanded);
  };

  // 加入/移出书架
  const handleToggleBookshelf = async () => {
    try {
      if (isInBookshelf) {
        await DataService.removeFromBookshelf(novel.id);
        setIsInBookshelf(false);
        // 同步更新全局 store
        setBookshelfStatus(novel.id, false);
        setFavoriteCount(prev => Math.max(0, prev - 1));
        success('已从书架移除');
      } else {
        const response = await DataService.addToBookshelf(novel.id);
        setIsInBookshelf(true);
        // 同步更新全局 store
        setBookshelfStatus(novel.id, true);
        // 只有当 already_exists 为 false 时才增加收藏数（避免重复计数）
        if (!response.alreadyExists) {
          setFavoriteCount(prev => prev + 1);
        }
        success('已加入书架');
      }
    } catch (error) {
      console.error('书架操作失败:', error);
      showError('操作失败，请重试');
    }
  };

  // 进入书友圈
  const handleEnterBookClub = async () => {
    try {
      // 直接调用 API 检查书架状态，确保使用最新状态
      let inBookshelf = false;
      try {
        const bookshelfStatus = await DataService.checkInBookshelf(novel.id);
        inBookshelf = bookshelfStatus.inBookshelf;
      } catch (checkError: any) {
        // 如果是 401 未授权错误，提示用户登录
        if (checkError?.response?.status === 401) {
          showError('请先登录');
          return;
        }
        // 其他错误，尝试使用本地状态
        console.error('检查书架状态失败:', checkError);
        inBookshelf = isInBookshelf;
      }

      if (!inBookshelf) {
        showError('请先收藏作品才能进入书友圈');
        return;
      }

      // 获取作品频道信息
      const channelInfo = await DataService.getWorkChannel(novel.id);

      if (!channelInfo.hasChannel) {
        showError('该作品暂无书友圈');
        return;
      }

      // 检查频道是否已锁定（作品已下架）
      if (channelInfo.channelStatus === 'locked') {
        showError('该书友圈已关闭（作品已下架）');
        return;
      }

      // 如果用户不是频道成员，先自动加入频道
      if (!channelInfo.isMember && channelInfo.channelId) {
        try {
          const { joinChannel } = await import('../../services/channelApi');
          await joinChannel(channelInfo.channelId);
        } catch (joinError) {
          console.error('自动加入频道失败:', joinError);
          // 加入失败也继续跳转，让频道页面处理
        }
      }

      // 跳转到频道页面，带上频道ID
      navigate(`/channels?channelId=${channelInfo.channelId}`);
    } catch (error) {
      console.error('进入书友圈失败:', error);
      showError('进入书友圈失败，请重试');
    }
  };

  // 发表评论（同时提交评分）
  const handleSubmitComment = async () => {
    if (!commentContent.trim()) {
      showError('请输入评论内容');
      return;
    }

    try {
      // 先提交评分（如果用户选择了评分）
      if (userRating > 0) {
        await DataService.rateWork(novel.id, userRating);
        // 重新加载评分统计
        const updatedStats = await DataService.getWorkRatingStats(novel.id);
        setRatingStats(updatedStats);
      }

      // 然后提交评论
      const newComment = await DataService.createComment(novel.id, { content: commentContent });
      setComments([newComment, ...comments]);
      setCommentContent('');
      // 重置 textarea 高度
      if (commentTextareaRef.current) {
        commentTextareaRef.current.style.height = 'auto';
      }

      success(userRating > 0 ? '评分和评论发表成功！' : '评论发表成功！');
    } catch (error) {
      console.error('发表失败:', error);
      showError('发表失败，请重试');
    }
  };

  // 递归在评论树中添加回复
  const addReplyToTree = (comments: Comment[], parentId: string, newReply: Comment): Comment[] => {
    return comments.map(comment => {
      if (comment.id === parentId) {
        return {
          ...comment,
          replies: [...(comment.replies || []), newReply],
          replyCount: (comment.replyCount || 0) + 1
        };
      }
      if (comment.replies && comment.replies.length > 0) {
        return {
          ...comment,
          replies: addReplyToTree(comment.replies, parentId, newReply)
        };
      }
      return comment;
    });
  };

  // 提交回复
  const handleSubmitReply = async (parentCommentId: string) => {
    if (!replyContent.trim()) {
      showError('请输入回复内容');
      return;
    }

    try {
      // 当回复一个回复时，parentId 应该是被回复评论的 ID（实现真正的树形嵌套）
      const actualParentId = replyToComment?.replyToReplyId || parentCommentId;

      console.log('提交回复参数:', {
        workId: novel.id,
        content: replyContent,
        parentId: actualParentId,
        replyToUserId: replyToComment?.replyToUserId
      });

      const newReply = await DataService.createComment(novel.id, {
        content: replyContent,
        parentId: actualParentId,
        replyToUserId: replyToComment?.replyToUserId
      });

      // 递归更新评论树
      setComments(prevComments => addReplyToTree(prevComments, actualParentId, newReply));

      // 展开回复列表（展开被回复评论所在的整条路径）
      setExpandedReplies(prev => {
        const next = new Set(prev);
        next.add(actualParentId);
        // 也展开顶级评论的回复
        next.add(parentCommentId);
        return next;
      });

      // 清空回复状态
      setReplyToComment(null);
      setReplyContent('');

      success('回复成功！');
    } catch (error: any) {
      console.error('回复失败:', error);
      console.error('错误详情:', error?.response?.data);
      const errorMessage = error?.response?.data?.detail || error?.message || '回复失败，请重试';
      showError(typeof errorMessage === 'string' ? errorMessage : '回复失败，请重试');
    }
  };

  // 递归更新评论树中某个评论的状态
  const updateCommentInTree = (comments: Comment[], commentId: string, updater: (c: Comment) => Comment): Comment[] => {
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

  // 点赞/取消点赞评论（包括回复）
  const handleToggleLike = async (commentId: string, isLiked: boolean) => {
    try {
      if (isLiked) {
        await DataService.unlikeComment(commentId);
      } else {
        await DataService.likeComment(commentId);
      }

      // 递归更新评论树中的点赞状态（点赞和踩互斥）
      setComments(prevComments => updateCommentInTree(prevComments, commentId, (c) => ({
        ...c,
        isLiked: !isLiked,
        likeCount: isLiked ? c.likeCount - 1 : c.likeCount + 1,
        // 点赞时自动取消踩
        isDisliked: !isLiked ? false : c.isDisliked,
      })));
    } catch (error) {
      console.error('点赞操作失败:', error);
      showError('操作失败，请重试');
    }
  };

  // 踩/取消踩评论（包括回复）
  const handleToggleDislike = async (commentId: string, isDisliked: boolean) => {
    try {
      if (isDisliked) {
        await DataService.undislikeComment(commentId);
      } else {
        await DataService.dislikeComment(commentId);
      }

      // 递归更新评论树中的踩状态（点赞和踩互斥）
      setComments(prevComments => updateCommentInTree(prevComments, commentId, (c) => ({
        ...c,
        isDisliked: !isDisliked,
        // 踩时自动取消点赞
        isLiked: !isDisliked ? false : c.isLiked,
        likeCount: !isDisliked && c.isLiked ? c.likeCount - 1 : c.likeCount,
      })));
    } catch (error) {
      console.error('踩操作失败:', error);
      showError('操作失败，请重试');
    }
  };

  // 递归渲染回复列表（支持无限层级）
  // 连接线逻辑参考 preview-youtube-comments.html
  const renderReplies = (replies: Comment[], rootCommentId: string, depth: number): React.ReactNode => {
    const MAX_DEPTH = 6;
    const isTopLevel = depth === 0;

    return replies.map((reply, replyIndex) => {
      const isFirst = replyIndex === 0;
      const isLast = replyIndex === replies.length - 1;
      const hasChildren = reply.replies && reply.replies.length > 0;

      return (
        // 外层容器：包含回复内容和子回复，垂直线基于此定位可正确延伸
        <div
          key={reply.id}
          id={`comment-${reply.id}`}
          className={`relative overflow-visible pt-3 ${
            highlightedCommentId === reply.id
              ? 'bg-blue-50 dark:bg-blue-900/30 animate-pulse ring-2 ring-blue-400 dark:ring-blue-500 rounded-lg'
              : ''
          }`}
        >
          {/* 垂直连接线 - 放在外层容器 */}
          <div
            className="absolute w-px bg-gray-300 dark:bg-[#3f3f3f]"
            style={{
              // 顶层对齐主评论头像中心(-36px)，嵌套层对齐父回复头像中心(-24px)
              left: isTopLevel ? '-36px' : '-24px',
              // 第一个回复向上延伸到父级头像下方
              top: isFirst ? (isTopLevel ? '-60px' : '-48px') : '-12px',
              // 非最后一个：延伸到底部连接下一个回复项
              // 最后一个（顶层）：延伸到"隐藏回复"按钮（-12px 填补 mt-3 间隙）
              // 最后一个（非顶层）：在弯折处停止
              bottom: isLast ? (isTopLevel ? '-12px' : 'calc(100% - 12px)') : '0'
            }}
          />
          {/* 弯折连接线 */}
          <div
            className="absolute border-b border-l border-gray-300 dark:border-[#3f3f3f] rounded-bl-xl"
            style={{
              left: isTopLevel ? '-36px' : '-24px',
              top: '12px',
              width: isTopLevel ? '36px' : '24px',
              height: '12px'
            }}
          />
          <div className="flex gap-3 relative group/reply overflow-visible">
          {/* 头像 - 点击跳转到用户主页 */}
          <Link to={reply.user?.id ? `/user/${reply.user.id}` : '#'} className="flex-shrink-0">
            {reply.user?.avatar ? (
              <div className="w-6 h-6 rounded-full overflow-hidden">
                <img src={reply.user.avatar} alt={reply.user.username} className="w-full h-full object-cover" />
              </div>
            ) : (
              <div className="w-6 h-6 rounded-full bg-gradient-to-br from-[#2196f3] to-[#4caf50] flex items-center justify-center text-white text-[10px] font-medium">
                {reply.user?.username?.[0]?.toUpperCase() || '?'}
              </div>
            )}
          </Link>

          <div className="flex-1 min-w-0 overflow-visible">
            <div className="flex items-center gap-2 mb-0.5">
              <Link to={reply.user?.id ? `/user/${reply.user.id}` : '#'} className="text-[13px] font-medium text-gray-900 dark:text-[#f1f1f1] hover:underline">
                @{reply.user?.username || '匿名用户'}
              </Link>
              <span className="text-xs text-gray-500 dark:text-[#aaa]">{formatTime(reply.createdAt)}</span>
              {depth > 0 && <span className="text-[10px] text-gray-400 dark:text-[#666]">Lv.{depth + 1}</span>}
              <button onClick={() => handleReportComment(reply.id)} className="ml-auto p-1 rounded-full text-gray-400 hover:bg-gray-100 dark:hover:bg-[#272727] opacity-0 group-hover/reply:opacity-100">
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg>
              </button>
            </div>
            <p className="text-sm text-gray-800 dark:text-[#f1f1f1] leading-relaxed">
              {reply.replyToUser && <Link to={`/user/${reply.replyToUser.id}`} className="text-[#3ea6ff] hover:underline mr-1">@{reply.replyToUser.username}</Link>}
              {reply.content}
            </p>

            {/* 操作按钮 */}
            <div className="flex items-center h-8 -ml-2 mt-0.5">
              <button onClick={() => handleToggleLike(reply.id, reply.isLiked || false)} className={`flex items-center justify-center w-8 h-8 rounded-full transition-colors ${reply.isLiked ? 'text-[#3ea6ff]' : 'text-gray-500 dark:text-[#aaa] hover:bg-gray-100 dark:hover:bg-[#272727]'}`}>
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><path d="M18.77,11h-4.23l1.52-4.94C16.38,5.03,15.54,4,14.38,4c-0.58,0-1.14,0.24-1.52,0.65L7,11H3v10h4h1h9.43 c1.06,0,1.98-0.67,2.19-1.61l1.34-6C21.23,12.15,20.18,11,18.77,11z M7,20H4v-8h3V20z M19.98,13.17l-1.34,6 C18.54,19.65,18.03,20,17.43,20H8v-8.61l5.6-6.06C13.79,5.12,14.08,5,14.38,5c0.26,0,0.5,0.11,0.63,0.3 c0.07,0.1,0.15,0.26,0.09,0.47l-1.52,4.94L13.18,12h1.35h4.23c0.41,0,0.8,0.17,1.03,0.46C19.92,12.61,20.05,12.86,19.98,13.17z"/></svg>
              </button>
              {reply.likeCount > 0 && <span className="text-xs text-gray-500 dark:text-[#aaa] mr-1">{reply.likeCount}</span>}
              <button onClick={() => handleToggleDislike(reply.id, reply.isDisliked || false)} className={`flex items-center justify-center w-8 h-8 rounded-full transition-colors ${reply.isDisliked ? 'text-[#3ea6ff]' : 'text-gray-500 dark:text-[#aaa] hover:bg-gray-100 dark:hover:bg-[#272727]'}`}>
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><path d="M17,4h-1H6.57C5.5,4,4.59,4.67,4.38,5.61l-1.34,6C2.77,12.85,3.82,14,5.23,14h4.23l-1.52,4.94C7.62,19.97,8.46,21,9.62,21 c0.58,0,1.14-0.24,1.52-0.65L17,14h4V4H17z M10.4,19.67C10.21,19.88,9.92,20,9.62,20c-0.26,0-0.5-0.11-0.63-0.3 c-0.07-0.1-0.15-0.26-0.09-0.47l1.52-4.94l0.4-1.29H9.46H5.23c-0.41,0-0.8-0.17-1.03-0.46c-0.12-0.15-0.25-0.4-0.18-0.71l1.34-6 C5.46,5.35,5.97,5,6.57,5H16v8.61L10.4,19.67z M20,13h-3V5h3V13z"/></svg>
              </button>
              {depth < MAX_DEPTH && (
                <button onClick={() => { setReplyToComment({ commentId: rootCommentId, username: reply.user?.username || '匿名用户', parentId: rootCommentId, replyToUserId: reply.user?.id, replyToReplyId: reply.id }); setReplyContent(''); }} className="h-8 px-3 text-xs font-medium text-gray-700 dark:text-[#f1f1f1] hover:bg-gray-100 dark:hover:bg-[#272727] rounded-full">
                  回复
                </button>
              )}
            </div>

            {/* 回复输入框 */}
            {replyToComment?.replyToReplyId === reply.id && (
              <div className="flex gap-3 mt-3">
                {currentUserAvatar ? (
                  <div className="w-6 h-6 rounded-full overflow-hidden flex-shrink-0"><img src={currentUserAvatar} alt={currentUserName || '我'} className="w-full h-full object-cover" /></div>
                ) : (
                  <div className="w-6 h-6 rounded-full bg-gradient-to-br from-[#667eea] to-[#764ba2] flex items-center justify-center text-white text-[10px] font-medium flex-shrink-0">{currentUserName?.[0]?.toUpperCase() || '我'}</div>
                )}
                <div className="flex-1">
                  <textarea value={replyContent} onChange={(e) => { setReplyContent(e.target.value); e.target.style.height = 'auto'; e.target.style.height = e.target.scrollHeight + 'px'; }} onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); if (replyContent.trim()) handleSubmitReply(rootCommentId); }}} className="w-full bg-transparent border-b border-gray-300 dark:border-[#303030] text-[13px] text-gray-900 dark:text-[#f1f1f1] py-1 outline-none resize-none overflow-hidden" placeholder="添加回复..." autoFocus rows={1} />
                  <div className="flex items-center justify-between mt-2">
                    <div className="relative">
                      <button
                        onClick={(e) => {
                          const button = e.currentTarget;
                          const rect = button.getBoundingClientRect();
                          const spaceBelow = window.innerHeight - rect.bottom;
                          const pickerHeight = 320;
                          setReplyEmojiPosition(spaceBelow < pickerHeight ? 'top' : 'bottom');
                          setShowReplyEmojiPicker(!showReplyEmojiPicker);
                        }}
                        className="p-1.5 text-gray-500 hover:bg-gray-100 dark:hover:bg-[#272727] rounded-full"
                      >
                        <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5-6c.78 2.34 2.72 4 5 4s4.22-1.66 5-4H7zm8-4c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm-6 0c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1z"/></svg>
                      </button>
                      {showReplyEmojiPicker && (
                        <>
                          <div
                            className="fixed inset-0 z-40"
                            onClick={() => setShowReplyEmojiPicker(false)}
                          />
                          <div className={`absolute left-0 z-50 ${replyEmojiPosition === 'top' ? 'bottom-full mb-2' : 'top-full mt-2'}`}>
                            <MiniEmojiPicker
                              onSelect={(emoji) => {
                                setReplyContent(prev => prev + emoji);
                              }}
                              onClose={() => setShowReplyEmojiPicker(false)}
                            />
                          </div>
                        </>
                      )}
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => { setReplyToComment(null); setReplyContent(''); setShowReplyEmojiPicker(false); }} className="px-3 py-1.5 text-xs text-gray-700 dark:text-[#f1f1f1] hover:bg-gray-100 dark:hover:bg-[#272727] rounded-full">取消</button>
                      <button onClick={() => handleSubmitReply(rootCommentId)} disabled={!replyContent.trim()} className={`px-3 py-1.5 text-xs font-medium rounded-full ${replyContent.trim() ? 'bg-[#3ea6ff] text-[#0f0f0f] hover:bg-[#65b8ff]' : 'bg-gray-200 dark:bg-[#272727] text-gray-400 cursor-not-allowed'}`}>回复</button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 递归渲染子回复 - 需要 overflow-visible 确保连接线不被裁剪 */}
            {reply.replies && reply.replies.length > 0 && depth < MAX_DEPTH && (
              <div className="mt-2 relative overflow-visible">{renderReplies(reply.replies, rootCommentId, depth + 1)}</div>
            )}
          </div>
        </div>
      </div>
      );
    });
  };

  // 打开举报对话框
  const handleReportComment = (commentId: string) => {
    setReportingCommentId(commentId);
    setShowReportModal(true);
    setReportReason('');
    setReportDescription('');
  };

  // 提交举报
  const handleSubmitReport = async () => {
    if (!reportReason) {
      showError('请选择举报原因');
      return;
    }

    try {
      await DataService.reportComment(reportingCommentId!, reportReason, reportDescription || undefined);
      success('举报成功，我们会尽快处理');
      setShowReportModal(false);
      setReportingCommentId(null);
      setReportReason('');
      setReportDescription('');
    } catch (error: any) {
      console.error('举报失败:', error);
      showError(formatUserError(error?.response?.data?.detail || error?.message));
    }
  };

  // 打开删除确认对话框
  const handleDeleteComment = (commentId: string) => {
    setDeleteCommentId(commentId);
    setShowDeleteConfirm(true);
  };

  // 确认删除评论
  const confirmDeleteComment = async () => {
    if (!deleteCommentId) return;

    try {
      await DataService.deleteComment(deleteCommentId);
      // 从评论列表中移除已删除的评论
      setComments(comments.filter(comment => comment.id !== deleteCommentId));
      success('评论已删除');
      setShowDeleteConfirm(false);
      setDeleteCommentId(null);
    } catch (error: any) {
      console.error('删除失败:', error);
      showError(formatUserError(error?.response?.data?.detail || error?.message));
    }
  };

  // 开始阅读
  const handleStartReading = (chapterId?: string) => {
    setSelectedChapterId(chapterId);
    setShowReader(true);
    // 保存阅读状态到 store，用于导航离开后返回时恢复
    setCurrentReadingState(novel.id, true);
  };

  // 格式化时间
  const formatTime = (dateStr: string): string => {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    if (days < 7) return `${days}天前`;
    return date.toLocaleDateString('zh-CN');
  };

  // 如果显示阅读器，渲染阅读器组件
  if (showReader) {
    return (
      <NovelReader
        workId={novel.id}
        chapterId={selectedChapterId}
        onBack={async () => {
          setShowReader(false);
          // 从阅读器返回时，更新状态为不在阅读中（但保持小说选中状态）
          setCurrentReadingState(novel.id, false);
          // 重新加载章节列表以刷新阅读量等统计（使用轻量接口，不增加浏览量）
          try {
            const chaptersRes = await DataService.getNovelChapters(novel.id);
            if (Array.isArray(chaptersRes)) {
              setChapters(chaptersRes);
            }
          } catch {
            // 静默失败，不影响返回体验
          }
        }}
        initialChapters={chapters}
        novelTitle={novelData?.title}
        highlightChapterCommentId={highlightChapterCommentId}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-slate-900">
      <header className="bg-white dark:bg-slate-900 border-b border-gray-200 dark:border-slate-700 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center gap-2 text-sm">
            <button
              onClick={onBack}
              className="text-gray-600 dark:text-slate-400 hover:text-black dark:hover:text-white transition-colors"
            >
              {source === 'bookshelf' ? '我的书架' : '小说广场'}
            </button>
            <span className="text-gray-400 dark:text-slate-600">/</span>
            <span className="text-black dark:text-white">{novelData.title}</span>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="bg-transparent p-8 mb-6">
          <div className="flex gap-8">
            <div className="flex-shrink-0">
              <ImageWithFallback
                src={novelData.cover}
                alt={novelData.title}
                className="w-48 rounded-lg"
                style={{ height: '256px', objectFit: 'cover' }}
              />
            </div>

            <div className="flex-1">
              <div className="mb-4">
                <h1 className="mb-3 text-gray-900 dark:text-white">{novelData.title}</h1>
                <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-slate-400 mb-4">
                  <div
                    className="flex items-center gap-2 cursor-pointer hover:text-black dark:hover:text-white transition-colors"
                    onClick={() => novelData.authorId && navigate(`/user/${novelData.authorId}`)}
                  >
                    {novelData.authorAvatar ? (
                      <img
                        src={novelData.authorAvatar}
                        alt={novelData.author}
                        className="w-6 h-6 rounded-full object-cover"
                      />
                    ) : (
                      <div className="w-6 h-6 rounded-full bg-gray-200 dark:bg-slate-700 flex items-center justify-center text-xs font-medium text-gray-600 dark:text-slate-400">
                        {novelData.author ? novelData.author[0].toUpperCase() : '?'}
                      </div>
                    )}
                    <span className="hover:underline">{novelData.author}</span>
                  </div>
                  <span className="px-2 py-1 bg-gray-100 dark:bg-slate-800 text-xs rounded-lg">{novelData.category}</span>
                  <span className="px-2 py-1 bg-black dark:bg-slate-700 text-white text-xs rounded-lg">{novelData.status}</span>
                </div>
              </div>

              <div className="flex items-center gap-6 mb-6 pb-6 border-b border-gray-100 dark:border-slate-700">
                <div className="flex items-center gap-2 text-sm">
                  <Star className="w-4 h-4 text-gray-500 dark:text-slate-400" />
                  <span className="text-gray-600 dark:text-slate-400">评分</span>
                  <span className="text-black dark:text-white">
                    {ratingStats ? `${ratingStats.averageRating}分 (${ratingStats.ratingCount}人)` : '暂无'}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <Eye className="w-4 h-4 text-gray-500 dark:text-slate-400" />
                  <span className="text-gray-600 dark:text-slate-400">阅读</span>
                  <span className="text-black dark:text-white">
                    {novelData.views > 10000 ? `${(novelData.views / 10000).toFixed(1)}万` : novelData.views}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <Heart className="w-4 h-4 text-gray-500 dark:text-slate-400" />
                  <span className="text-gray-600 dark:text-slate-400">收藏</span>
                  <span className="text-black dark:text-white">
                    {favoriteCount > 10000 ? `${(favoriteCount / 10000).toFixed(1)}万` : favoriteCount}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <BookOpen className="w-4 h-4 text-gray-500 dark:text-slate-400" />
                  <span className="text-gray-600 dark:text-slate-400">章节</span>
                  <span className="text-black dark:text-white">{chapters.length}章</span>
                </div>
              </div>

              <div className="mb-6">
                <h3 className="text-sm mb-3 text-gray-900 dark:text-white">作品简介</h3>
                <div className="space-y-2">
                  {descriptionParagraphs.map((paragraph, index) => {
                    const firstChar = index === 0 ? paragraph.charAt(0) : '';
                    const restText = index === 0 ? paragraph.slice(1) : paragraph;
                    return (
                      <p
                        key={`${index}-${paragraph.slice(0, 12)}`}
                        className="text-sm text-gray-600 dark:text-slate-400 leading-relaxed"
                        style={{ textIndent: index === 0 ? '0' : '2em', clear: index === 0 ? 'none' : 'both' }}
                      >
                        {index === 0 && firstChar && (
                          <span
                            className="float-left mr-2 text-2xl font-medium text-amber-500 dark:text-amber-300"
                            style={{ lineHeight: '1', paddingRight: '0.1em', marginLeft: '0.2em' }}
                          >
                            {firstChar}
                          </span>
                        )}
                        {restText}
                      </p>
                    );
                  })}
                </div>
              </div>

              <div className="flex items-center gap-3">
                <button
                  onClick={() => {
                    if (chapters.length > 0) {
                      // 优先使用上次阅读的章节，如果没有则从第一章开始
                      const lastChapterId = getLastChapter(novel.id);
                      const targetChapterId = lastChapterId && chapters.some(c => c.id === lastChapterId)
                        ? lastChapterId
                        : chapters[0].id;
                      handleStartReading(targetChapterId);
                    } else {
                      showError('暂无可阅读章节');
                    }
                  }}
                  className="px-8 py-3 bg-black dark:bg-slate-700 text-white text-sm rounded-lg hover:bg-gray-800 dark:hover:bg-slate-600 transition-colors"
                >
                  开始阅读
                </button>
                {/* 从书架进入时隐藏"加入书架"按钮 */}
                {!isFromBookshelf && (
                  <button
                    onClick={handleToggleBookshelf}
                    className={`px-6 py-3 border text-sm rounded-lg transition-colors flex items-center gap-2 ${
                      isInBookshelf
                        ? 'border-red-600 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20'
                        : 'border-gray-200 dark:border-slate-700 text-gray-600 dark:text-slate-400 hover:border-gray-300 dark:hover:border-slate-600 hover:text-black dark:hover:text-white'
                    }`}
                  >
                    <Heart className={`w-4 h-4 ${isInBookshelf ? 'fill-red-600' : ''}`} />
                    {isInBookshelf ? '已加入书架' : '加入书架'}
                  </button>
                )}
                <button
                  onClick={handleEnterBookClub}
                  className="px-6 py-3 border border-gray-200 dark:border-slate-700 text-gray-600 dark:text-slate-400 text-sm rounded-lg hover:border-gray-300 dark:hover:border-slate-600 hover:text-black dark:hover:text-white transition-colors flex items-center gap-2"
                >
                  <Users className="w-4 h-4" />
                  进入书友圈
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* 章节目录 */}
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl mb-6">
          {loading ? (
            <div className="px-6 py-12 text-center text-gray-500 dark:text-slate-400">加载中...</div>
          ) : chapters.length === 0 ? (
            <div className="px-6 py-12 text-center text-gray-500 dark:text-slate-400">暂无章节</div>
          ) : (
            <div className="divide-y divide-gray-100 dark:divide-slate-700">
              {chapterGroups.map((group, groupIndex) => (
                <div key={groupIndex}>
                  <div
                    className={`px-6 py-4 cursor-pointer transition-colors flex items-center justify-between group ${
                      groupIndex === 0 ? 'rounded-t-xl' : ''
                    } ${
                      groupIndex === chapterGroups.length - 1 && !expandedGroups.has(groupIndex) ? 'rounded-b-xl' : ''
                    }`}
                    onClick={() => toggleGroup(groupIndex)}
                  >
                    <div className="flex-1">
                      <h3 className="text-sm mb-1 group-hover:text-black dark:group-hover:text-white transition-colors text-gray-900 dark:text-white">
                        章节目录
                      </h3>
                      <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-slate-400">
                        <span className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {formatTime(group[group.length - 1].publishedAt)}
                        </span>
                        <span>{group.reduce((sum, chapter) => sum + chapter.wordCount, 0)}字</span>
                      </div>
                    </div>
                    <ChevronDown
                      className={`w-4 h-4 text-gray-300 dark:text-slate-600 group-hover:text-gray-600 dark:group-hover:text-slate-400 transition-all ${
                        expandedGroups.has(groupIndex) ? 'rotate-180' : ''
                      }`}
                    />
                  </div>
                  {expandedGroups.has(groupIndex) && (
                    <div className="px-2 py-1">
                      {group.map((chapter) => (
                        <div
                          key={chapter.id}
                          className="px-10 py-3 hover:bg-gray-100 dark:hover:bg-slate-700 cursor-pointer transition-colors flex items-center justify-between group rounded-lg"
                          onClick={() => handleStartReading(chapter.id)}
                        >
                          <div className="flex-1">
                            <h3 className="text-sm mb-1 group-hover:text-black dark:group-hover:text-white transition-colors text-gray-900 dark:text-white">
                              {chapter.title}
                            </h3>
                            <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-slate-400">
                              <span className="flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {formatTime(chapter.publishedAt)}
                              </span>
                              <span>{chapter.wordCount}字</span>
                              <span>{chapter.viewCount}阅读</span>
                            </div>
                          </div>
                          <BookOpen className="w-4 h-4 text-gray-300 dark:text-slate-600 group-hover:text-gray-600 dark:group-hover:text-slate-400 transition-colors" />
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 评论区 - YouTube风格 */}
        <div>
          {/* 标题栏 */}
          <div className="px-6 py-4 flex items-center gap-8">
            <h2 className="text-base font-medium text-gray-900 dark:text-[#f1f1f1]">
              {comments.length} 条评论
            </h2>
            <div className="relative" ref={sortMenuRef}>
              <button
                onClick={() => setShowSortMenu(!showSortMenu)}
                className="flex items-center gap-2 text-sm text-gray-700 dark:text-[#f1f1f1] hover:text-gray-500 dark:hover:text-[#aaa] transition-colors"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M3 18h6v-2H3v2zM3 6v2h18V6H3zm0 7h12v-2H3v2z"/>
                </svg>
                {commentSortBy === 'newest' ? '最新' : '最热'}
              </button>
              {showSortMenu && (
                <div className="absolute top-full left-0 mt-1 bg-white dark:bg-[#282828] rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 z-50 min-w-[100px]">
                  <button
                    onClick={() => handleSortChange('newest')}
                    className={`w-full px-4 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-[#3f3f3f] ${
                      commentSortBy === 'newest' ? 'text-blue-500 dark:text-[#3ea6ff]' : 'text-gray-700 dark:text-[#f1f1f1]'
                    }`}
                  >
                    最新
                  </button>
                  <button
                    onClick={() => handleSortChange('most_liked')}
                    className={`w-full px-4 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-[#3f3f3f] ${
                      commentSortBy === 'most_liked' ? 'text-blue-500 dark:text-[#3ea6ff]' : 'text-gray-700 dark:text-[#f1f1f1]'
                    }`}
                  >
                    最热
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="px-6 pb-8">
            {/* 发表评论区 - YouTube风格 */}
            <div className="flex gap-4 mb-8">
              {currentUserAvatar ? (
                <div className="w-10 h-10 rounded-full overflow-hidden flex-shrink-0">
                  <img
                    src={currentUserAvatar}
                    alt={currentUserName || '我'}
                    className="w-full h-full object-cover"
                  />
                </div>
              ) : (
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#667eea] to-[#764ba2] flex items-center justify-center text-white text-base font-medium flex-shrink-0">
                  {currentUserName ? currentUserName[0].toUpperCase() : '我'}
                </div>
              )}
              <div className="flex-1">
                <div className="mb-3">
                  <div className="text-xs text-gray-500 dark:text-[#aaa] mb-2">你的评分</div>
                  <div className="flex items-center gap-1">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star
                        key={star}
                        className={`w-5 h-5 cursor-pointer transition-colors ${
                          star <= (hoveredRating || userRating)
                            ? 'fill-[#f1c40f] text-[#f1c40f]'
                            : 'text-gray-400 dark:text-[#717171]'
                        }`}
                        onClick={() => setUserRating(star)}
                        onMouseEnter={() => setHoveredRating(star)}
                        onMouseLeave={() => setHoveredRating(0)}
                      />
                    ))}
                    {userRating > 0 && (
                      <span className="ml-2 text-xs text-gray-500 dark:text-[#aaa]">{userRating}.0</span>
                    )}
                  </div>
                </div>
                <textarea
                  ref={commentTextareaRef}
                  value={commentContent}
                  onChange={(e) => {
                    setCommentContent(e.target.value);
                    // 自动调整高度
                    e.target.style.height = 'auto';
                    e.target.style.height = e.target.scrollHeight + 'px';
                  }}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      if (commentContent.trim()) {
                        handleSubmitComment();
                      }
                    }
                  }}
                  className="w-full bg-transparent border-b border-gray-300 dark:border-[#303030] text-sm text-gray-900 dark:text-[#f1f1f1] placeholder-gray-400 dark:placeholder-[#aaa] py-2 outline-none focus:border-gray-900 dark:focus:border-[#f1f1f1] transition-colors resize-none overflow-hidden"
                  placeholder="添加评论..."
                  onFocus={() => setShowCommentActions(true)}
                  rows={1}
                />
                {showCommentActions && (
                  <div className="flex items-center justify-between mt-2">
                    <div className="relative">
                      <button
                        ref={emojiButtonRef}
                        onClick={(e) => {
                          if (!showEmojiPicker && emojiButtonRef.current) {
                            const rect = emojiButtonRef.current.getBoundingClientRect();
                            const spaceAbove = rect.top;
                            const pickerHeight = 320;
                            setEmojiPickerPosition(spaceAbove < pickerHeight ? 'bottom' : 'top');
                          }
                          setShowEmojiPicker(!showEmojiPicker);
                        }}
                        className="p-2 text-gray-500 dark:text-[#aaa] hover:bg-gray-100 dark:hover:bg-[#272727] rounded-full transition-colors"
                      >
                        <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5-6c.78 2.34 2.72 4 5 4s4.22-1.66 5-4H7zm8-4c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm-6 0c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1z"/>
                        </svg>
                      </button>
                      {/* 表情选择器 */}
                      {showEmojiPicker && (
                        <div ref={emojiPickerRef} className={`absolute left-0 z-50 ${emojiPickerPosition === 'top' ? 'bottom-full mb-2' : 'top-full mt-2'}`}>
                          <MiniEmojiPicker
                            onSelect={(emoji) => {
                              setCommentContent(prev => prev + emoji);
                              setShowEmojiPicker(false);
                            }}
                            onClose={() => setShowEmojiPicker(false)}
                          />
                        </div>
                      )}
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => {
                          setShowCommentActions(false);
                          setShowEmojiPicker(false);
                          setCommentContent('');
                        }}
                        className="px-4 py-2 text-sm text-gray-700 dark:text-[#f1f1f1] hover:bg-gray-100 dark:hover:bg-[#272727] rounded-full transition-colors"
                      >
                        取消
                      </button>
                      <button
                        onClick={handleSubmitComment}
                        disabled={!commentContent.trim()}
                        className={`px-4 py-2 text-sm font-medium rounded-full transition-colors ${
                          commentContent.trim()
                            ? 'bg-[#3ea6ff] text-[#0f0f0f] hover:bg-[#65b8ff]'
                            : 'bg-gray-200 dark:bg-[#272727] text-gray-400 dark:text-[#717171] cursor-not-allowed'
                        }`}
                      >
                        评论
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* 评论列表 - YouTube风格 */}
            {loading ? (
              <div className="py-12 text-center text-gray-500 dark:text-[#aaa]">加载中...</div>
            ) : comments.length === 0 ? (
              <div className="py-12 text-center text-gray-500 dark:text-[#aaa]">暂无评论，快来抢沙发吧！</div>
            ) : (
              <>
                <div className="space-y-4">
                  {comments.slice(0, visibleComments).map((comment) => (
                    <div
                      key={comment.id}
                      id={`comment-${comment.id}`}
                      className={`flex gap-4 group p-3 rounded-lg transition-all ${
                        highlightedCommentId === comment.id
                          ? 'bg-blue-50 dark:bg-blue-900/30 animate-pulse ring-2 ring-blue-400 dark:ring-blue-500'
                          : ''
                      }`}
                    >
                      {/* 头像 - 点击跳转到用户主页 */}
                      <Link to={comment.user?.id ? `/user/${comment.user.id}` : '#'} className="flex-shrink-0">
                        {comment.user?.avatar ? (
                          <div className="w-10 h-10 rounded-full overflow-hidden">
                            <img
                              src={comment.user.avatar}
                              alt={comment.user.username}
                              className="w-full h-full object-cover"
                            />
                          </div>
                        ) : (
                          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#e91e63] to-[#9c27b0] flex items-center justify-center text-white text-sm font-medium">
                            {comment.user?.username ? comment.user.username[0].toUpperCase() : '?'}
                          </div>
                        )}
                      </Link>

                      {/* 评论内容 */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <Link
                            to={comment.user?.id ? `/user/${comment.user.id}` : '#'}
                            className="text-[13px] font-medium text-gray-900 dark:text-[#f1f1f1] hover:underline"
                          >
                            @{comment.user?.username || '匿名用户'}
                          </Link>
                          <span className="text-xs text-gray-500 dark:text-[#aaa]">
                            {formatTime(comment.createdAt)}
                          </span>
                          {comment.userRating && (
                            <div className="flex items-center gap-0.5 ml-1">
                              {[1, 2, 3, 4, 5].map((star) => (
                                <Star
                                  key={star}
                                  className={`w-3 h-3 ${
                                    star <= comment.userRating!
                                      ? 'fill-[#f1c40f] text-[#f1c40f]'
                                      : 'text-gray-400 dark:text-[#717171]'
                                  }`}
                                />
                              ))}
                            </div>
                          )}
                          {/* 三点菜单 - hover时显示 */}
                          <button
                            onClick={() => currentUserId === comment.userId ? handleDeleteComment(comment.id) : handleReportComment(comment.id)}
                            className="ml-auto p-1 rounded-full text-gray-400 dark:text-[#aaa] hover:bg-gray-100 dark:hover:bg-[#272727] opacity-0 group-hover:opacity-100 transition-opacity"
                          >
                            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
                            </svg>
                          </button>
                        </div>

                        <p className="text-sm text-gray-800 dark:text-[#f1f1f1] mb-2 leading-relaxed">{comment.content}</p>

                        {/* 操作按钮 - YouTube风格 */}
                        <div className="flex items-center h-9 -ml-2">
                          {/* 点赞按钮 */}
                          <button
                            onClick={() => handleToggleLike(comment.id, comment.isLiked || false)}
                            className={`flex items-center justify-center w-9 h-9 rounded-full transition-colors ${
                              comment.isLiked
                                ? 'text-[#3ea6ff]'
                                : 'text-gray-500 dark:text-[#aaa] hover:bg-gray-100 dark:hover:bg-[#272727]'
                            }`}
                          >
                            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M18.77,11h-4.23l1.52-4.94C16.38,5.03,15.54,4,14.38,4c-0.58,0-1.14,0.24-1.52,0.65L7,11H3v10h4h1h9.43 c1.06,0,1.98-0.67,2.19-1.61l1.34-6C21.23,12.15,20.18,11,18.77,11z M7,20H4v-8h3V20z M19.98,13.17l-1.34,6 C18.54,19.65,18.03,20,17.43,20H8v-8.61l5.6-6.06C13.79,5.12,14.08,5,14.38,5c0.26,0,0.5,0.11,0.63,0.3 c0.07,0.1,0.15,0.26,0.09,0.47l-1.52,4.94L13.18,12h1.35h4.23c0.41,0,0.8,0.17,1.03,0.46C19.92,12.61,20.05,12.86,19.98,13.17z"/>
                            </svg>
                          </button>
                          {comment.likeCount > 0 && (
                            <span className="text-xs text-gray-500 dark:text-[#aaa] mr-1">{comment.likeCount}</span>
                          )}

                          {/* 踩按钮 */}
                          <button
                            onClick={() => handleToggleDislike(comment.id, comment.isDisliked || false)}
                            className={`flex items-center justify-center w-9 h-9 rounded-full transition-colors ${
                              comment.isDisliked
                                ? 'text-[#3ea6ff]'
                                : 'text-gray-500 dark:text-[#aaa] hover:bg-gray-100 dark:hover:bg-[#272727]'
                            }`}
                          >
                            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M17,4h-1H6.57C5.5,4,4.59,4.67,4.38,5.61l-1.34,6C2.77,12.85,3.82,14,5.23,14h4.23l-1.52,4.94C7.62,19.97,8.46,21,9.62,21 c0.58,0,1.14-0.24,1.52-0.65L17,14h4V4H17z M10.4,19.67C10.21,19.88,9.92,20,9.62,20c-0.26,0-0.5-0.11-0.63-0.3 c-0.07-0.1-0.15-0.26-0.09-0.47l1.52-4.94l0.4-1.29H9.46H5.23c-0.41,0-0.8-0.17-1.03-0.46c-0.12-0.15-0.25-0.4-0.18-0.71l1.34-6 C5.46,5.35,5.97,5,6.57,5H16v8.61L10.4,19.67z M20,13h-3V5h3V13z"/>
                            </svg>
                          </button>

                          {/* 回复按钮 */}
                          <button
                            onClick={() => {
                              if (replyToComment?.commentId === comment.id) {
                                setReplyToComment(null);
                                setReplyContent('');
                              } else {
                                setReplyToComment({
                                  commentId: comment.id,
                                  username: comment.user?.username || '匿名用户',
                                  parentId: comment.id,
                                  replyToUserId: comment.user?.id
                                });
                                setReplyContent('');
                              }
                            }}
                            className="h-9 px-4 ml-1 text-xs font-medium text-gray-700 dark:text-[#f1f1f1] hover:bg-gray-100 dark:hover:bg-[#272727] rounded-full transition-colors"
                          >
                            回复
                          </button>
                        </div>

                        {/* 回复输入框 - 只在回复主评论时显示（不是回复子回复） */}
                        {replyToComment?.commentId === comment.id && !replyToComment?.replyToReplyId && (
                          <div className="flex gap-3 mt-3 ml-14">
                            {currentUserAvatar ? (
                              <div className="w-6 h-6 rounded-full overflow-hidden flex-shrink-0">
                                <img src={currentUserAvatar} alt={currentUserName || '我'} className="w-full h-full object-cover" />
                              </div>
                            ) : (
                              <div className="w-6 h-6 rounded-full bg-gradient-to-br from-[#667eea] to-[#764ba2] flex items-center justify-center text-white text-[10px] font-medium flex-shrink-0">
                                {currentUserName ? currentUserName[0].toUpperCase() : '我'}
                              </div>
                            )}
                            <div className="flex-1">
                              <textarea
                                value={replyContent}
                                onChange={(e) => {
                                  setReplyContent(e.target.value);
                                  // 自动调整高度
                                  e.target.style.height = 'auto';
                                  e.target.style.height = e.target.scrollHeight + 'px';
                                }}
                                onKeyDown={(e) => {
                                  if (e.key === 'Enter' && !e.shiftKey) {
                                    e.preventDefault();
                                    if (replyContent.trim()) {
                                      handleSubmitReply(comment.id);
                                    }
                                  }
                                }}
                                className="w-full bg-transparent border-b border-gray-300 dark:border-[#303030] text-[13px] text-gray-900 dark:text-[#f1f1f1] placeholder-gray-400 dark:placeholder-[#aaa] py-1 outline-none focus:border-gray-900 dark:focus:border-[#f1f1f1] transition-colors resize-none overflow-hidden"
                                placeholder="添加回复..."
                                autoFocus
                                rows={1}
                              />
                              <div className="flex items-center justify-between mt-2">
                                <div className="relative">
                                  <button
                                    ref={replyEmojiButtonRef}
                                    onClick={(e) => {
                                      const button = e.currentTarget;
                                      const rect = button.getBoundingClientRect();
                                      const spaceBelow = window.innerHeight - rect.bottom;
                                      const pickerHeight = 320; // h-80 = 320px
                                      setReplyEmojiPosition(spaceBelow < pickerHeight ? 'top' : 'bottom');
                                      setShowReplyEmojiPicker(!showReplyEmojiPicker);
                                    }}
                                    className="p-1.5 text-gray-500 dark:text-[#aaa] hover:bg-gray-100 dark:hover:bg-[#272727] rounded-full transition-colors"
                                  >
                                    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5-6c.78 2.34 2.72 4 5 4s4.22-1.66 5-4H7zm8-4c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm-6 0c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1z"/>
                                    </svg>
                                  </button>
                                  {showReplyEmojiPicker && (
                                    <div
                                      ref={replyEmojiPickerRef}
                                      className={`absolute left-0 z-50 ${replyEmojiPosition === 'top' ? 'bottom-full mb-2' : 'top-full mt-2'}`}
                                    >
                                      <MiniEmojiPicker
                                        onSelect={(emoji) => {
                                          setReplyContent(prev => prev + emoji);
                                        }}
                                        onClose={() => setShowReplyEmojiPicker(false)}
                                      />
                                    </div>
                                  )}
                                </div>
                                <div className="flex gap-2">
                                  <button
                                    onClick={() => {
                                      setReplyToComment(null);
                                      setReplyContent('');
                                      setShowReplyEmojiPicker(false);
                                    }}
                                    className="px-3 py-1.5 text-xs text-gray-700 dark:text-[#f1f1f1] hover:bg-gray-100 dark:hover:bg-[#272727] rounded-full transition-colors"
                                  >
                                    取消
                                  </button>
                                  <button
                                    onClick={() => handleSubmitReply(comment.id)}
                                    disabled={!replyContent.trim()}
                                    className={`px-3 py-1.5 text-xs font-medium rounded-full transition-colors ${
                                      replyContent.trim()
                                        ? 'bg-[#3ea6ff] text-[#0f0f0f] hover:bg-[#65b8ff]'
                                        : 'bg-gray-200 dark:bg-[#272727] text-gray-400 dark:text-[#717171] cursor-not-allowed'
                                    }`}
                                  >
                                    回复
                                  </button>
                                </div>
                              </div>
                            </div>
                          </div>
                        )}

                        {/* 展开回复按钮 */}
                        {comment.replies && comment.replies.length > 0 && !expandedReplies.has(comment.id) && (
                          <button
                            onClick={() => setExpandedReplies(prev => new Set(prev).add(comment.id))}
                            className="flex items-center gap-2 px-4 py-2 -ml-4 mt-1 text-sm font-medium text-[#3ea6ff] hover:bg-[#3ea6ff]/10 rounded-full transition-colors"
                          >
                            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/>
                            </svg>
                            {comment.replies.length} 条回复
                          </button>
                        )}

                        {/* 回复列表 - 使用递归渲染支持无限层级 */}
                        {comment.replies && comment.replies.length > 0 && expandedReplies.has(comment.id) && (
                          <div className="mt-2 relative overflow-visible">
                            {renderReplies(comment.replies, comment.id, 0)}

                            {/* 隐藏回复按钮 */}
                            <button
                              onClick={() => setExpandedReplies(prev => {
                                const next = new Set(prev);
                                next.delete(comment.id);
                                return next;
                              })}
                              className="flex items-center gap-2 px-4 py-2 mt-3 relative text-sm font-medium text-[#3ea6ff] hover:bg-[#3ea6ff]/10 rounded-full transition-colors"
                            >
                              {/* 弯折连接线 - 对齐到根节点头像中心 */}
                              <div
                                className="absolute border-b border-l border-gray-300 dark:border-[#3f3f3f] rounded-bl-xl"
                                style={{
                                  left: '-36px',
                                  top: '0',
                                  width: '36px',
                                  height: '20px'
                                }}
                              />
                              <svg className="w-5 h-5 rotate-180" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/>
                              </svg>
                              隐藏回复
                            </button>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                {visibleComments < comments.length && (
                  <div className="mt-4 -ml-4">
                    <button
                      className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-[#3ea6ff] hover:bg-[#3ea6ff]/10 rounded-full transition-colors"
                      onClick={() => setVisibleComments(visibleComments + 5)}
                    >
                      <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/>
                      </svg>
                      加载更多评论
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>

      {/* 删除确认对话框 */}
      <Modal
        isOpen={showDeleteConfirm}
        onClose={() => setShowDeleteConfirm(false)}
        title="确认删除"
        size="sm"
        footer={
          <>
            <button
              onClick={() => setShowDeleteConfirm(false)}
              className="px-4 py-2 text-sm text-gray-600 dark:text-slate-400 hover:text-black dark:hover:text-white transition-colors"
            >
              取消
            </button>
            <button
              onClick={confirmDeleteComment}
              className="px-4 py-2 text-sm bg-red-600 text-white hover:bg-red-700 transition-colors rounded"
            >
              删除
            </button>
          </>
        }
      >
        <p className="text-sm text-gray-600 dark:text-slate-400">确定要删除这条评论吗？删除后无法恢复。</p>
      </Modal>

      {/* 举报对话框 */}
      <Modal
        isOpen={showReportModal}
        onClose={() => setShowReportModal(false)}
        title="举报评论"
        size="md"
        footer={
          <>
            <button
              onClick={() => setShowReportModal(false)}
              className="px-4 py-2 text-sm text-gray-600 dark:text-slate-400 hover:text-black dark:hover:text-white transition-colors"
            >
              取消
            </button>
            <button
              onClick={handleSubmitReport}
              className="px-4 py-2 text-sm bg-black dark:bg-slate-700 text-white hover:bg-gray-800 dark:hover:bg-slate-600 transition-colors rounded"
            >
              提交
            </button>
          </>
        }
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
              举报原因<span className="text-red-600">*</span>
            </label>
            <Select value={reportReason} onValueChange={setReportReason}>
              <SelectTrigger className="w-full text-sm">
                <SelectValue placeholder="请选择举报原因" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="spam">垃圾信息</SelectItem>
                <SelectItem value="abuse">辱骂内容</SelectItem>
                <SelectItem value="porn">色情内容</SelectItem>
                <SelectItem value="illegal">违法内容</SelectItem>
                <SelectItem value="false">虚假信息</SelectItem>
                <SelectItem value="other">其他</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
              详细描述（可选）
            </label>
            <textarea
              value={reportDescription}
              onChange={(e) => setReportDescription(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-gray-900 dark:text-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={4}
              placeholder="请详细描述举报原因..."
            />
          </div>
        </div>
      </Modal>
    </div>
  );
}
