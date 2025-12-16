import { useState, useEffect, useRef } from 'react';
import { Search, BookOpen, Loader2 } from 'lucide-react';
import { NovelCard, Novel } from '../components/library/NovelCard';
import { FeaturedCarousel } from '../components/library/FeaturedCarousel';
import { NovelDetail } from '../components/library/NovelDetail';
import { DataService } from '../services/DataService';
import { useToast } from '../hooks/useToast';
import { useWorkNavStore } from '../store/workNavStore';

// 类型映射
const GENRE_MAP: Record<string, string> = {
  '全部': '',
  '玄幻': 'fantasy',
  '都市': 'urban',
  '言情': 'romance',
  '科幻': 'scifi',
  '武侠': 'wuxia',
  '游戏': 'game',
  '历史': 'history',
  '军事': 'military',
  '其他': 'other',
};

const STATUS_MAP: Record<string, string> = {
  '全部': '',
  '草稿': 'draft',
  '连载中': 'writing',
  '已完结': 'completed',
  '已弃坑': 'abandoned',
};

const SORT_MAP: Record<string, 'latest' | 'popular' | 'words'> = {
  '最新': 'latest',
  '最热': 'popular',
  '字数最多': 'words',
};

const categories = ['全部', '玄幻', '都市', '言情', '科幻', '武侠', '游戏', '历史', '军事', '其他'];
const statusFilters = ['全部', '连载中', '已完结'];
const sortOptions = ['最新', '最热', '字数最多'];

export default function NovelSquareView() {
  // 获取持久化的浏览状态
  const {
    novelSquareBrowseState,
    setNovelSquareBrowseState,
    novelSquareReadingState,
    clearNovelSquareReadingState
  } = useWorkNavStore();

  // 从持久化状态初始化，如果没有则使用默认值
  const [selectedCategory, setSelectedCategory] = useState(novelSquareBrowseState?.category || '全部');
  const [searchQuery, setSearchQuery] = useState(novelSquareBrowseState?.searchQuery || '');
  const [selectedNovel, setSelectedNovel] = useState<Novel | null>(null);
  const [selectedStatus, setSelectedStatus] = useState(novelSquareBrowseState?.status || '全部');
  const [selectedSort, setSelectedSort] = useState(novelSquareBrowseState?.sort || '最新');

  const [novels, setNovels] = useState<Novel[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(novelSquareBrowseState?.page || 1);
  const [hasMore, setHasMore] = useState(true);

  const { showToast } = useToast();

  // 用于防止重复恢复状态
  const hasRestoredRef = useRef(false);
  // 用于标记是否已初始化加载
  const hasInitializedRef = useRef(false);

  // 根据类型生成默认封面
  const getDefaultCover = (genre: string): string => {
    const coverMap: Record<string, string> = {
      fantasy: 'https://images.unsplash.com/photo-1618681679873-c81d7a65f0e2?w=400&q=80', // 玄幻 - 魔法城堡
      urban: 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&q=80', // 都市 - 城市夜景
      romance: 'https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=400&q=80', // 言情 - 浪漫场景
      scifi: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&q=80', // 科幻 - 太空星球
      wuxia: 'https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=400&q=80', // 武侠 - 中国山水
      game: 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400&q=80', // 游戏 - 游戏场景
      history: 'https://images.unsplash.com/photo-1533613220915-609f661a6fe1?w=400&q=80', // 历史 - 古建筑
      military: 'https://images.unsplash.com/photo-1569098293970-f305919c7f9e?w=400&q=80', // 军事 - 军事题材
      other: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&q=80', // 其他 - 书籍
    };
    return coverMap[genre] || coverMap.other;
  };

  // 转换后端数据为前端Novel类型
  const convertToNovel = (work: any): Novel => {
    return {
      id: String(work.id),
      title: work.title,
      author: work.authorName,
      category: work.genre,
      description: work.description || '暂无简介',
      cover: work.coverImage || getDefaultCover(work.genre),
      views: work.viewCount,
      likes: work.favoriteCount || 0,
      rating: work.averageRating || 0,
      chapters: work.publishedChapterCount,
      status: work.status === 'writing' ? '连载中' : work.status === 'completed' ? '已完结' : '其他',
      isFeatured: work.isFeatured,
    };
  };

  // 加载小说列表（支持加载到指定页数）
  const loadNovels = async (reset = false, targetPage?: number) => {
    try {
      setLoading(true);
      const loadPage = targetPage || (reset ? 1 : page);

      // 如果需要加载到指定页，需要加载从第1页到目标页的所有数据
      const totalToLoad = reset && targetPage && targetPage > 1 ? targetPage * 20 : 20;
      const skipAmount = reset ? 0 : (loadPage - 1) * 20;

      const response = await DataService.getPublishedNovels({
        skip: skipAmount,
        limit: totalToLoad,
        genre: GENRE_MAP[selectedCategory],
        search: searchQuery.trim() || undefined,
        sortBy: SORT_MAP[selectedSort],
      });

      const newNovels = response.items.map(convertToNovel);

      if (reset) {
        setNovels(newNovels);
        setPage(targetPage || 1);
      } else {
        setNovels([...novels, ...newNovels]);
      }

      setHasMore(newNovels.length === totalToLoad);
    } catch (error: any) {
      console.error('加载小说列表失败:', error);
      showToast('error', '加载失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  // 保存浏览状态
  const saveBrowseState = () => {
    setNovelSquareBrowseState({
      page,
      category: selectedCategory,
      status: selectedStatus,
      sort: selectedSort,
      searchQuery,
    });
  };

  // 初始加载（恢复持久化状态或默认加载）
  useEffect(() => {
    if (hasInitializedRef.current) return;
    hasInitializedRef.current = true;

    // 如果有持久化的浏览状态，加载到对应页
    if (novelSquareBrowseState && novelSquareBrowseState.page > 1) {
      loadNovels(true, novelSquareBrowseState.page);
    } else {
      loadNovels(true);
    }
  }, []);

  // 筛选条件变化时重新加载
  useEffect(() => {
    // 跳过初始化时的加载
    if (!hasInitializedRef.current) return;
    loadNovels(true);
  }, [selectedCategory, selectedSort]);

  // 恢复阅读状态（仅在从阅读器返回详情页时）
  useEffect(() => {
    if (hasRestoredRef.current || !novelSquareReadingState) {
      return;
    }

    const restoreState = async () => {
      hasRestoredRef.current = true;
      const { novelId } = novelSquareReadingState;

      // 先在已加载的列表中查找
      const existingNovel = novels.find((n) => n.id === novelId);
      if (existingNovel) {
        setSelectedNovel(existingNovel);
        return;
      }

      // 创建临时 Novel 对象，NovelDetail 会负责加载完整数据
      setSelectedNovel({
        id: novelId,
        title: '加载中...',
        author: '',
        category: '其他',
        description: '',
        cover: '',
        views: 0,
        likes: 0,
        rating: 0,
        chapters: 0,
        status: '其他' as const,
      });
    };

    restoreState();
  }, [novelSquareReadingState, novels]);

  // 搜索防抖
  useEffect(() => {
    if (!hasInitializedRef.current) return;

    const timer = setTimeout(() => {
      if (searchQuery !== '') {
        loadNovels(true);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // 状态筛选（前端筛选）
  const filteredNovels = novels.filter((novel) => {
    if (selectedStatus === '全部') return true;
    return novel.status === selectedStatus;
  });

  // 处理轮播图点击详情
  const handleViewDetailById = async (workId: string) => {
    // 保存当前浏览状态
    saveBrowseState();

    // 先在已加载的列表中查找
    const existingNovel = novels.find((n) => n.id === workId);
    if (existingNovel) {
      setSelectedNovel(existingNovel);
      return;
    }

    // 如果不在列表中，创建一个临时的 Novel 对象
    // NovelDetail 组件会负责加载完整的数据（包括增加浏览量）
    // 这样避免了重复调用 API 导致浏览量增加两次
    setSelectedNovel({
      id: workId,
      title: '加载中...',
      author: '',
      category: '其他',
      description: '',
      cover: '',
      views: 0,
      likes: 0,
      rating: 0,
      chapters: 0,
      status: '其他' as const,
    });
  };

  // 点击小说卡片查看详情
  const handleViewNovelDetail = (novel: Novel) => {
    // 保存当前浏览状态
    saveBrowseState();
    setSelectedNovel(novel);
  };

  if (selectedNovel) {
    return (
      <NovelDetail
        novel={selectedNovel}
        onBack={() => {
          setSelectedNovel(null);
          // 用户主动返回时清除阅读状态
          clearNovelSquareReadingState();
        }}
        source="novel-square"
      />
    );
  }

  return (
    <div className="h-full flex flex-col bg-gray-50 dark:bg-slate-900 overflow-hidden">
      {/* 固定页眉区域 */}
      <div className="flex-shrink-0">
        <FeaturedCarousel onViewDetail={handleViewDetailById} />

        <div className="bg-white dark:bg-slate-900 border-b border-gray-200 dark:border-slate-700">
          <div className="max-w-6xl mx-auto px-6 py-4">
            <div className="flex items-center gap-4 mb-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 dark:text-slate-500" />
                <input
                  type="text"
                  placeholder="搜索作品或作者..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm text-gray-900 dark:text-white focus:outline-none focus:border-gray-400 dark:focus:border-slate-600 transition-colors"
                />
              </div>
              <button
                onClick={() => {
                  setSelectedCategory('全部');
                  setSelectedStatus('全部');
                  setSelectedSort('最新');
                  setSearchQuery('');
                  setPage(1);
                }}
                className="px-4 py-2 bg-black dark:bg-slate-700 text-white text-sm hover:bg-gray-800 dark:hover:bg-slate-600 transition-colors"
              >
                重置
              </button>
            </div>

            <div className="flex items-center gap-2">
              {categories.map((category) => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`px-3 py-1 text-sm transition-colors ${
                    selectedCategory === category
                      ? 'bg-black dark:bg-slate-700 text-white'
                      : 'bg-white dark:bg-slate-800 text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-700 border border-gray-200 dark:border-slate-700'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-2 mt-4">
              {statusFilters.map((status) => (
                <button
                  key={status}
                  onClick={() => setSelectedStatus(status)}
                  className={`px-3 py-1 text-sm transition-colors ${
                    selectedStatus === status
                      ? 'bg-black dark:bg-slate-700 text-white'
                      : 'bg-white dark:bg-slate-800 text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-700 border border-gray-200 dark:border-slate-700'
                  }`}
                >
                  {status}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-2 mt-4">
              {sortOptions.map((sort) => (
                <button
                  key={sort}
                  onClick={() => setSelectedSort(sort)}
                  className={`px-3 py-1 text-sm transition-colors ${
                    selectedSort === sort
                      ? 'bg-black dark:bg-slate-700 text-white'
                      : 'bg-white dark:bg-slate-800 text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-700 border border-gray-200 dark:border-slate-700'
                  }`}
                >
                  {sort}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 可滚动内容区 */}
      <main className="flex-1 overflow-auto">
        <div className="max-w-6xl mx-auto px-6 py-6">
        {loading && novels.length === 0 ? (
          <div className="flex justify-center items-center py-20">
            <Loader2 className="w-8 h-8 text-gray-400 dark:text-slate-500 animate-spin" />
          </div>
        ) : filteredNovels.length > 0 ? (
          <>
            <div className="grid grid-cols-6 gap-4">
              {filteredNovels.map((novel) => (
                <NovelCard key={novel.id} novel={novel} onViewDetail={() => handleViewNovelDetail(novel)} />
              ))}
            </div>

            {hasMore && (
              <div className="flex justify-center mt-8">
                <button
                  onClick={() => {
                    const newPage = page + 1;
                    setPage(newPage);
                    loadNovels(false);
                  }}
                  disabled={loading}
                  className="px-6 py-2 bg-black dark:bg-slate-700 text-white text-sm hover:bg-gray-800 dark:hover:bg-slate-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      加载中...
                    </span>
                  ) : (
                    '加载更多'
                  )}
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-20 bg-white dark:bg-slate-900">
            <BookOpen className="w-12 h-12 text-gray-300 dark:text-slate-600 mx-auto mb-4" />
            <p className="text-gray-500 dark:text-slate-400">暂无符合条件的小说</p>
          </div>
        )}
        </div>
      </main>
    </div>
  );
}
