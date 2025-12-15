import {
  ArrowLeft,
  Eye,
  Heart,
  Star,
  Clock,
  BookOpen,
  Share2,
  MessageCircle,
  ChevronDown,
  ThumbsUp,
  Flag,
  Trash2,
} from 'lucide-react';
import { Novel } from './NovelCard';
import { ImageWithFallback } from './ImageWithFallback';
import { useState, useEffect, useRef } from 'react';
import { DataService } from '../../services/DataService';
import Modal from '../common/Modal';
import { useGlobalStore } from '../../store/globalStore';
import { useWorkNavStore } from '../../store/workNavStore';
import { NovelReader } from './NovelReader';

interface NovelDetailProps {
  novel: Novel;
  onBack: () => void;
  /** 是否从书架进入，如果是则隐藏"加入书架"按钮 */
  isFromBookshelf?: boolean;
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
  isLiked?: boolean;
  userRating?: number;
}

interface RatingStats {
  averageRating: number;
  ratingCount: number;
  ratingDistribution: { [key: number]: number };
  userRating: number | null;
}

export function NovelDetail({ novel, onBack, isFromBookshelf = false }: NovelDetailProps) {
  const [expandedGroups, setExpandedGroups] = useState<Set<number>>(new Set([0]));
  const [userRating, setUserRating] = useState(0);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [visibleComments, setVisibleComments] = useState(5);

  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  const [commentContent, setCommentContent] = useState('');
  // 优先从全局 store 读取缓存的书架状态，避免页面切换时状态丢失
  const [isInBookshelf, setIsInBookshelf] = useState(() => useWorkNavStore.getState().bookshelfMap[novel.id] || false);
  const [loading, setLoading] = useState(true);
  const [ratingStats, setRatingStats] = useState<RatingStats | null>(null);
  const [reportingCommentId, setReportingCommentId] = useState<string | null>(null);
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);
  const [favoriteCount, setFavoriteCount] = useState(novel.likes || 0);

  // 存储从 API 加载的完整小说数据
  const [novelData, setNovelData] = useState<Novel>(novel);

  // 确认删除对话框
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteCommentId, setDeleteCommentId] = useState<string | null>(null);

  // 举报对话框
  const [showReportModal, setShowReportModal] = useState(false);
  const [reportReason, setReportReason] = useState('');
  const [reportDescription, setReportDescription] = useState('');

  // 阅读器状态
  const [showReader, setShowReader] = useState(false);
  const [selectedChapterId, setSelectedChapterId] = useState<string | undefined>(undefined);

  // Toast
  const { success, error: showError } = useGlobalStore();

  // 获取章节记忆功能和阅读状态
  const { getLastChapter, libraryReadingState, setLibraryReadingState, setBookshelfStatus } = useWorkNavStore();
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
          DataService.getWorkComments(novel.id).catch(() => ({ items: [] })),
          // API 失败时返回 null，保持本地缓存状态
          DataService.checkInBookshelf(novel.id).catch(() => null),
          DataService.getWorkRatingStats(novel.id).catch(() => null),
          DataService.getCurrentUser().catch(() => null),
        ]);

        // 更新小说数据（用于从轮播图等地方传入临时对象的情况）
        if (detailRes) {
          const genreMap: { [key: string]: string } = {
            fantasy: '玄幻', urban: '都市', romance: '言情', scifi: '科幻',
            wuxia: '武侠', game: '游戏', history: '历史', military: '军事', other: '其他',
          };
          const statusMap: { [key: string]: string } = {
            writing: '连载中', completed: '已完结', draft: '草稿', abandoned: '已弃坑',
          };
          setNovelData({
            id: detailRes.id,
            title: detailRes.title,
            author: detailRes.authorName,
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
      libraryReadingState?.novelId === novel.id &&
      libraryReadingState?.isReading
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
  }, [loading, chapters, libraryReadingState, novel.id, getLastChapter]);

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

      success(userRating > 0 ? '评分和评论发表成功！' : '评论发表成功！');
    } catch (error) {
      console.error('发表失败:', error);
      showError('发表失败，请重试');
    }
  };

  // 点赞/取消点赞评论
  const handleToggleLike = async (commentId: string, isLiked: boolean) => {
    try {
      if (isLiked) {
        await DataService.unlikeComment(commentId);
      } else {
        await DataService.likeComment(commentId);
      }

      // 更新评论列表中的点赞状态
      setComments(comments.map(comment => {
        if (comment.id === commentId) {
          return {
            ...comment,
            isLiked: !isLiked,
            likeCount: isLiked ? comment.likeCount - 1 : comment.likeCount + 1,
          };
        }
        return comment;
      }));
    } catch (error) {
      console.error('点赞操作失败:', error);
      showError('操作失败，请重试');
    }
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
      if (error?.response?.data?.detail) {
        showError(error.response.data.detail);
      } else {
        showError('举报失败，请重试');
      }
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
      if (error?.response?.data?.detail) {
        showError(error.response.data.detail);
      } else {
        showError('删除失败，请重试');
      }
    }
  };

  // 开始阅读
  const handleStartReading = (chapterId?: string) => {
    setSelectedChapterId(chapterId);
    setShowReader(true);
    // 保存阅读状态到 store，用于导航离开后返回时恢复
    setLibraryReadingState(novel.id, true);
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
        onBack={() => {
          setShowReader(false);
          // 从阅读器返回时，更新状态为不在阅读中（但保持小说选中状态）
          setLibraryReadingState(novel.id, false);
        }}
        initialChapters={chapters}
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
              书籍广场
            </button>
            <span className="text-gray-400 dark:text-slate-600">/</span>
            <span className="text-black dark:text-white">{novelData.title}</span>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 p-8 mb-6">
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
                  <span>作者：{novelData.author}</span>
                  <span className="px-2 py-1 bg-gray-100 dark:bg-slate-800 text-xs">{novelData.category}</span>
                  <span className="px-2 py-1 bg-black dark:bg-slate-700 text-white text-xs">{novelData.status}</span>
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
                <p className="text-sm text-gray-600 dark:text-slate-400 leading-relaxed">{novelData.description}</p>
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
                  className="px-8 py-3 bg-black dark:bg-slate-700 text-white text-sm hover:bg-gray-800 dark:hover:bg-slate-600 transition-colors"
                >
                  开始阅读
                </button>
                {/* 从书架进入时隐藏"加入书架"按钮 */}
                {!isFromBookshelf && (
                  <button
                    onClick={handleToggleBookshelf}
                    className={`px-6 py-3 border text-sm transition-colors flex items-center gap-2 ${
                      isInBookshelf
                        ? 'border-red-600 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20'
                        : 'border-gray-200 dark:border-slate-700 text-gray-600 dark:text-slate-400 hover:border-gray-300 dark:hover:border-slate-600 hover:text-black dark:hover:text-white'
                    }`}
                  >
                    <Heart className={`w-4 h-4 ${isInBookshelf ? 'fill-red-600' : ''}`} />
                    {isInBookshelf ? '已加入书架' : '加入书架'}
                  </button>
                )}
                <button className="px-6 py-3 border border-gray-200 dark:border-slate-700 text-gray-600 dark:text-slate-400 text-sm hover:border-gray-300 dark:hover:border-slate-600 hover:text-black dark:hover:text-white transition-colors flex items-center gap-2">
                  <Share2 className="w-4 h-4" />
                  分享
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* 章节目录 */}
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 mb-6">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-slate-700">
            <h2 className="text-sm text-gray-900 dark:text-white">章节目录</h2>
          </div>

          {loading ? (
            <div className="px-6 py-12 text-center text-gray-500 dark:text-slate-400">加载中...</div>
          ) : chapters.length === 0 ? (
            <div className="px-6 py-12 text-center text-gray-500 dark:text-slate-400">暂无章节</div>
          ) : (
            <div className="divide-y divide-gray-100 dark:divide-slate-700">
              {chapterGroups.map((group, groupIndex) => (
                <div key={groupIndex}>
                  <div
                    className="px-6 py-4 hover:bg-gray-50 dark:hover:bg-slate-800 cursor-pointer transition-colors flex items-center justify-between group"
                    onClick={() => toggleGroup(groupIndex)}
                  >
                    <div className="flex-1">
                      <h3 className="text-sm mb-1 group-hover:text-black dark:group-hover:text-white transition-colors text-gray-900 dark:text-white">
                        第{group[0].order}章 - 第{group[group.length - 1].order}章
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
                    <div className="bg-gray-50 dark:bg-slate-800/50">
                      {group.map((chapter) => (
                        <div
                          key={chapter.id}
                          className="px-12 py-3 hover:bg-gray-100 dark:hover:bg-slate-800 cursor-pointer transition-colors flex items-center justify-between group"
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

        {/* 评论区 */}
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-slate-700 flex items-center justify-between">
            <h2 className="text-sm flex items-center gap-2 text-gray-900 dark:text-white">
              <MessageCircle className="w-4 h-4" />
              读者评论
            </h2>
            <span className="text-xs text-gray-500 dark:text-slate-400">共 {comments.length} 条评论</span>
          </div>

          <div className="p-6">
            {/* 发表评论区 */}
            <div className="border border-gray-200 dark:border-slate-700 p-4 mb-4">
              <div className="mb-4">
                <div className="text-xs text-gray-600 dark:text-slate-400 mb-2">你的评分</div>
                <div className="flex items-center gap-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <Star
                      key={star}
                      className={`w-5 h-5 cursor-pointer transition-colors ${
                        star <= (hoveredRating || userRating)
                          ? 'fill-black dark:fill-white text-black dark:text-white'
                          : 'text-gray-300 dark:text-slate-600'
                      }`}
                      onClick={() => setUserRating(star)}
                      onMouseEnter={() => setHoveredRating(star)}
                      onMouseLeave={() => setHoveredRating(0)}
                    />
                  ))}
                  {userRating > 0 && (
                    <span className="ml-2 text-xs text-gray-600 dark:text-slate-400">{userRating}.0</span>
                  )}
                </div>
              </div>

              <textarea
                value={commentContent}
                onChange={(e) => setCommentContent(e.target.value)}
                className="w-full text-sm text-gray-600 dark:text-slate-400 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 p-2 outline-none resize-none"
                rows={3}
                placeholder="写下你的评论..."
              />
              <div className="flex justify-end mt-3">
                <button
                  onClick={handleSubmitComment}
                  className="px-6 py-2 bg-black dark:bg-slate-700 text-white text-xs hover:bg-gray-800 dark:hover:bg-slate-600 transition-colors"
                >
                  发表评论
                </button>
              </div>
            </div>

            {/* 评论列表 */}
            {loading ? (
              <div className="py-12 text-center text-gray-500 dark:text-slate-400">加载中...</div>
            ) : comments.length === 0 ? (
              <div className="py-12 text-center text-gray-500 dark:text-slate-400">暂无评论，快来抢沙发吧！</div>
            ) : (
              <>
                <div className="space-y-4">
                  {comments.slice(0, visibleComments).map((comment) => (
                    <div
                      key={comment.id}
                      className="border-b border-gray-100 dark:border-slate-700 pb-4 last:border-0"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-3">
                          {comment.user?.avatar ? (
                            <img
                              src={comment.user.avatar}
                              alt={comment.user.username}
                              className="w-10 h-10 rounded-full object-cover flex-shrink-0"
                              style={{ width: '40px', height: '40px' }}
                            />
                          ) : (
                            <div className="w-10 h-10 rounded-full bg-gray-200 dark:bg-slate-700 flex items-center justify-center text-sm font-medium text-gray-600 dark:text-slate-400 flex-shrink-0">
                              {comment.user?.username ? comment.user.username[0].toUpperCase() : '?'}
                            </div>
                          )}
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-black dark:text-white">{comment.user?.username || '匿名用户'}</span>
                            {comment.userRating && (
                              <div className="flex items-center gap-0.5">
                                {[1, 2, 3, 4, 5].map((star) => (
                                  <Star
                                    key={star}
                                    className={`w-3 h-3 ${
                                      star <= comment.userRating!
                                        ? 'fill-yellow-400 text-yellow-400'
                                        : 'text-gray-300 dark:text-slate-600'
                                    }`}
                                  />
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                        <span className="text-xs text-gray-400 dark:text-slate-500">
                          {formatTime(comment.createdAt)}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 dark:text-slate-400 mb-3">{comment.content}</p>

                      <div className="flex items-center gap-4">
                        <button
                          onClick={() => handleToggleLike(comment.id, comment.isLiked || false)}
                          className={`flex items-center gap-1 text-xs transition-colors ${
                            comment.isLiked
                              ? 'text-blue-600 dark:text-blue-400'
                              : 'text-gray-400 dark:text-slate-500 hover:text-gray-600 dark:hover:text-slate-400'
                          }`}
                        >
                          <ThumbsUp className={`w-3 h-3 ${comment.isLiked ? 'fill-blue-600 dark:fill-blue-400' : ''}`} />
                          <span>{comment.likeCount > 0 ? comment.likeCount : '点赞'}</span>
                        </button>

                        {currentUserId === comment.userId ? (
                          <button
                            onClick={() => handleDeleteComment(comment.id)}
                            className="flex items-center gap-1 text-xs text-gray-400 dark:text-slate-500 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                          >
                            <Trash2 className="w-3 h-3" />
                            <span>删除</span>
                          </button>
                        ) : (
                          <button
                            onClick={() => handleReportComment(comment.id)}
                            className="flex items-center gap-1 text-xs text-gray-400 dark:text-slate-500 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                          >
                            <Flag className="w-3 h-3" />
                            <span>举报</span>
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                {visibleComments < comments.length && (
                  <div className="text-center mt-4">
                    <button
                      className="text-sm text-gray-600 dark:text-slate-400 hover:text-black dark:hover:text-white transition-colors"
                      onClick={() => setVisibleComments(visibleComments + 5)}
                    >
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
            <select
              value={reportReason}
              onChange={(e) => setReportReason(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-gray-900 dark:text-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">请选择举报原因</option>
              <option value="spam">垃圾信息</option>
              <option value="abuse">辱骂内容</option>
              <option value="porn">色情内容</option>
              <option value="illegal">违法内容</option>
              <option value="false">虚假信息</option>
              <option value="other">其他</option>
            </select>
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
