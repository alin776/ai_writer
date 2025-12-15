import { useState, useEffect, useRef } from 'react';
import { Search, BookOpen, Trash2, Clock } from 'lucide-react';
import { NovelCard, Novel } from '../components/library/NovelCard';
import { NovelDetail } from '../components/library/NovelDetail';
import { DataService } from '../services/DataService';
import { useWorkNavStore } from '../store/workNavStore';

// 类型映射:中文类型 -> 英文枚举
const GENRE_MAP: { [key: string]: string } = {
  全部: '',
  玄幻: 'fantasy',
  都市: 'urban',
  言情: 'romance',
  科幻: 'scifi',
  武侠: 'wuxia',
  游戏: 'game',
  历史: 'history',
  军事: 'military',
  其他: 'other',
};

// 英文类型 -> 中文类型
const GENRE_REVERSE_MAP: { [key: string]: string } = {
  fantasy: '玄幻',
  urban: '都市',
  romance: '言情',
  scifi: '科幻',
  wuxia: '武侠',
  game: '游戏',
  history: '历史',
  military: '军事',
  other: '其他',
};

// 状态映射:英文 -> 中文
const STATUS_MAP: { [key: string]: string } = {
  draft: '草稿',
  writing: '连载中',
  completed: '已完结',
  abandoned: '已弃坑',
};

interface BookshelfItem {
  id: string;
  novel: Novel;
  lastReadChapterOrder?: number;
  lastReadAt?: string;
  progress: number;
  addedAt: string;
}

const categories = ['全部', '玄幻', '都市', '言情', '科幻', '武侠', '游戏', '历史', '军事', '其他'];
const sortOptions = ['最近阅读', '添加时间', '更新时间'];

export default function MyBookshelfView() {
  const [selectedCategory, setSelectedCategory] = useState('全部');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedNovel, setSelectedNovel] = useState<Novel | null>(null);
  const [selectedSort, setSelectedSort] = useState('最近阅读');
  const [bookshelfItems, setBookshelfItems] = useState<BookshelfItem[]>([]);
  const [loading, setLoading] = useState(true);

  // 获取图书馆阅读状态
  const { libraryReadingState, clearLibraryReadingState } = useWorkNavStore();

  // 用于防止重复恢复状态
  const hasRestoredRef = useRef(false);

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

  // 将书架API响应转换为前端数据格式
  const convertToBookshelfItem = (item: any): BookshelfItem => {
    const novel: Novel = {
      id: String(item.id),
      title: item.title,
      author: item.authorName,
      category: GENRE_REVERSE_MAP[item.genre] || '其他',
      description: item.description || '暂无简介',
      cover: item.coverImage || getDefaultCover(item.genre),
      views: item.viewCount,
      likes: item.favoriteCount || 0,
      rating: item.averageRating || 0,
      chapters: item.publishedChapterCount,
      status: (STATUS_MAP[item.status] || '其他') as '连载中' | '已完结' | '其他',
    };

    // 计算阅读进度
    let progress = 0;
    if (item.lastReadChapterOrder && item.publishedChapterCount > 0) {
      // 已读完当前章节，所以进度 = (已读章节序号 / 总章节数) * 100
      progress = Math.round((item.lastReadChapterOrder / item.publishedChapterCount) * 100);
    }

    return {
      id: String(item.id),
      novel,
      lastReadChapterOrder: item.lastReadChapterOrder,
      lastReadAt: item.lastReadAt,
      progress,
      addedAt: item.addedAt,
    };
  };

  // 加载书架数据
  const loadBookshelf = async () => {
    try {
      setLoading(true);
      const response = await DataService.getBookshelf();
      // 后端返回 { total: number, items: [] } 格式
      const items = (response.items || []).map(convertToBookshelfItem);
      setBookshelfItems(items);
    } catch (error) {
      console.error('Failed to load bookshelf:', error);
    } finally {
      setLoading(false);
    }
  };

  // 组件挂载时加载数据
  useEffect(() => {
    loadBookshelf();
  }, []);

  // 恢复上次查看的小说状态（从左侧导航返回时）
  useEffect(() => {
    if (hasRestoredRef.current || !libraryReadingState || loading) {
      return;
    }

    const restoreState = () => {
      hasRestoredRef.current = true;
      const { novelId } = libraryReadingState;

      // 先在已加载的书架中查找
      const existingItem = bookshelfItems.find((item) => item.novel.id === novelId);
      if (existingItem) {
        setSelectedNovel(existingItem.novel);
        return;
      }

      // 如果不在书架中，创建临时 Novel 对象
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
  }, [libraryReadingState, loading, bookshelfItems]);

  // 筛选和排序逻辑
  const filteredAndSortedItems = bookshelfItems
    .filter((item) => {
      const matchesCategory =
        selectedCategory === '全部' || item.novel.category === selectedCategory;
      const matchesSearch =
        item.novel.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.novel.author.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    })
    .sort((a, b) => {
      if (selectedSort === '最近阅读') {
        if (!a.lastReadAt) return 1;
        if (!b.lastReadAt) return -1;
        return new Date(b.lastReadAt).getTime() - new Date(a.lastReadAt).getTime();
      } else if (selectedSort === '添加时间') {
        return new Date(b.addedAt).getTime() - new Date(a.addedAt).getTime();
      } else {
        // 更新时间 - 暂时使用添加时间
        return new Date(b.addedAt).getTime() - new Date(a.addedAt).getTime();
      }
    });

  // 移出书架
  const handleRemove = async (workId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await DataService.removeFromBookshelf(workId);
      setBookshelfItems(bookshelfItems.filter((item) => item.novel.id !== workId));
    } catch (error) {
      console.error('Failed to remove from bookshelf:', error);
      alert('移出书架失败，请重试');
    }
  };

  // 计算距离上次阅读的天数
  const getDaysAgo = (dateStr?: string): string => {
    if (!dateStr) return '--';
    const days = Math.floor((Date.now() - new Date(dateStr).getTime()) / (1000 * 60 * 60 * 24));
    if (days === 0) return '今天';
    if (days === 1) return '昨天';
    return `${days}天前`;
  };

  if (selectedNovel) {
    return (
      <NovelDetail
        novel={selectedNovel}
        onBack={() => {
          setSelectedNovel(null);
          // 用户主动返回时清除阅读状态
          clearLibraryReadingState();
        }}
      />
    );
  }

  return (
    <div className="h-full flex flex-col bg-gray-50 dark:bg-slate-900 overflow-hidden">
      {/* 固定页眉 */}
      <div className="flex-shrink-0 bg-white dark:bg-slate-900 border-b border-gray-200 dark:border-slate-700">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">我的书架</h1>
              <p className="text-sm text-gray-500 dark:text-slate-400">
                共收藏 {bookshelfItems.length} 部作品
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Clock className="w-5 h-5 text-gray-400 dark:text-slate-500" />
              <span className="text-sm text-gray-600 dark:text-slate-400">
                最后更新: {new Date().toLocaleDateString('zh-CN')}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4 mb-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 dark:text-slate-500" />
              <input
                type="text"
                placeholder="搜索书架中的作品..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm text-gray-900 dark:text-white focus:outline-none focus:border-gray-400 dark:focus:border-slate-600 transition-colors"
              />
            </div>
          </div>

          <div className="flex items-center justify-between">
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

            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-500 dark:text-slate-400">排序:</span>
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
        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block w-8 h-8 border-4 border-gray-300 dark:border-slate-600 border-t-black dark:border-t-white rounded-full animate-spin"></div>
            <p className="mt-4 text-gray-500 dark:text-slate-400">加载中...</p>
          </div>
        ) : filteredAndSortedItems.length > 0 ? (
          <div className="grid grid-cols-6 gap-4">
            {filteredAndSortedItems.map((item) => (
              <div key={item.id} className="relative group">
                <NovelCard novel={item.novel} onViewDetail={() => setSelectedNovel(item.novel)} />
                <button
                  onClick={(e) => handleRemove(item.novel.id, e)}
                  className="absolute top-2 left-2 p-1.5 bg-red-600 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-700"
                  title="移出书架"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
                <div className="mt-2 px-2">
                  <div className="flex items-center justify-between text-xs text-gray-500 dark:text-slate-400">
                    <span>
                      {item.lastReadChapterOrder ? `已读: 第${item.lastReadChapterOrder}章` : '未开始'}
                    </span>
                    <span>{getDaysAgo(item.lastReadAt)}</span>
                  </div>
                  <div className="mt-1 h-1 bg-gray-200 dark:bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-600 dark:bg-blue-500 rounded-full"
                      style={{ width: `${Math.min(100, Math.max(0, item.progress))}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-20 bg-white dark:bg-slate-900 rounded-lg border border-gray-200 dark:border-slate-700">
            <BookOpen className="w-16 h-16 text-gray-300 dark:text-slate-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">书架空空如也</h3>
            <p className="text-gray-500 dark:text-slate-400 mb-6">
              {searchQuery ? '没有找到符合条件的作品' : '快去小说广场挑选你喜欢的作品吧'}
            </p>
            {!searchQuery && (
              <button
                onClick={() => (window.location.href = '/library/novel-square')}
                className="px-6 py-2 bg-black dark:bg-slate-700 text-white text-sm hover:bg-gray-800 dark:hover:bg-slate-600 transition-colors"
              >
                前往小说广场
              </button>
            )}
          </div>
        )}
        </div>
      </main>
    </div>
  );
}
