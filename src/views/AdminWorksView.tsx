import { useState, useEffect } from 'react';
import {
  Book,
  Search,
  Filter,
  MoreVertical,
  Eye,
  EyeOff,
  Star,
  StarOff,
  Trash2,
  AlertCircle,
} from 'lucide-react';
import { DataService } from '../services/DataService';
import { useGlobalStore } from '../store/globalStore';
import { ImageWithFallback } from '../components/library/ImageWithFallback';

interface Work {
  id: string;
  title: string;
  description: string;
  coverImage: string;
  genre: string;
  status: string;
  totalWords: number;
  totalChapters: number;
  viewCount: number;
  favoriteCount: number;
  averageRating: number;
  isPublished: boolean;
  isFeatured: boolean;
  publishedAt: string | null;
  authorName: string;
  authorId: string;
  publishedChapterCount: number;
  createdAt: string;
  updatedAt: string;
}

interface WorksListResponse {
  total: number;
  page: number;
  pageSize: number;
  items: Work[];
}

const GENRE_MAP: Record<string, string> = {
  fantasy: '玄幻',
  urban: '都市',
  romance: '言情',
  scifi: '科幻',
  wuxia: '武侠',
  game: '游戏',
  history: '历史',
  military: '军事',
  suspense: '悬疑',
  western_fantasy: '西幻',
  apocalypse: '末世',
  other: '其他',
};

const STATUS_MAP: Record<string, string> = {
  writing: '连载中',
  completed: '已完结',
  paused: '暂停',
};
const DEFAULT_COVER_IMAGE = '/default-cover.jpg';

export default function AdminWorksView() {
  const { success, error } = useGlobalStore();
  const [works, setWorks] = useState<Work[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterGenre, setFilterGenre] = useState<string>('');
  const [filterStatus, setFilterStatus] = useState<string>('');
  const [filterPublished, setFilterPublished] = useState<string>('');

  // 加载小说列表
  const loadWorks = async () => {
    try {
      setLoading(true);
      const response = await DataService.adminGetAllWorks({
        skip: (page - 1) * pageSize,
        limit: pageSize,
        search: searchQuery || undefined,
        genre: filterGenre || undefined,
        status: filterStatus || undefined,
        isPublished: filterPublished ? filterPublished === 'true' : undefined,
      });

      setWorks(response.items);
      setTotal(response.total);
    } catch (err) {
      console.error('加载小说列表失败:', err);
      error('加载小说列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWorks();
  }, [page, searchQuery]);

  // 搜索
  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setPage(1);
  };

  // 切换发布状态
  const handleTogglePublish = async (workId: string, currentStatus: boolean) => {
    try {
      await DataService.adminToggleWorkPublish(workId, !currentStatus);
      success(currentStatus ? '已取消发布' : '已发布');
      loadWorks();
    } catch (err: any) {
      console.error('切换发布状态失败:', err);
      error(err.response?.data?.detail || '操作失败');
    }
  };

  // 切换推荐状态
  const handleToggleFeatured = async (workId: string, currentStatus: boolean) => {
    try {
      await DataService.adminToggleWorkFeatured(workId, !currentStatus);
      success(currentStatus ? '已取消推荐' : '已设为推荐');
      loadWorks();
    } catch (err: any) {
      console.error('切换推荐状态失败:', err);
      error(err.response?.data?.detail || '操作失败');
    }
  };

  // 删除小说
  const handleDelete = async (workId: string, title: string) => {
    if (!confirm(`确定要删除《${title}》吗？此操作不可恢复！`)) {
      return;
    }

    try {
      await DataService.adminDeleteWork(workId);
      success('删除成功');
      loadWorks();
    } catch (err: any) {
      console.error('删除失败:', err);
      error(err.response?.data?.detail || '删除失败');
    }
  };

  return (
    <div className="px-6 pb-6">
      <div className="sticky top-0 z-10 bg-gray-50 dark:bg-gray-900 pt-6">
        {/* 页头 */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Book className="w-7 h-7" />
            小说管理
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            管理所有用户创作的小说，包括审核、推荐和删除
          </p>
        </div>

        {/* 搜索和筛选栏 */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            {/* 搜索框 */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="搜索小说标题或作者..."
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* 筛选按钮 */}
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300">
              <Filter className="w-4 h-4" />
              <span>筛选</span>
            </button>
          </div>

          {/* 统计信息 */}
          <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <div className="text-sm text-gray-500 dark:text-gray-400">总小说数</div>
                <div className="text-2xl font-bold text-gray-900 dark:text-white">{total}</div>
              </div>
              <div>
                <div className="text-sm text-gray-500 dark:text-gray-400">已发布</div>
                <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                  {works.filter((w) => w.isPublished).length}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-500 dark:text-gray-400">推荐中</div>
                <div className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
                  {works.filter((w) => w.isFeatured).length}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-500 dark:text-gray-400">总字数</div>
                <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  {(works.reduce((sum, w) => sum + w.totalWords, 0) / 10000).toFixed(1)}万
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 小说列表 */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-gray-500 dark:text-gray-400">加载中...</div>
          </div>
        ) : works.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20">
            <AlertCircle className="w-12 h-12 text-gray-400 mb-4" />
            <p className="text-gray-500 dark:text-gray-400">暂无小说</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-600">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-80">
                    小说信息
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    作者
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    类型/状态
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    数据
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    状态
                  </th>
                  <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    操作
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {works.map((work) => (
                  <tr key={work.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                    <td className="px-4 py-4">
                      <div className="flex items-start gap-3 max-w-xs">
                        <ImageWithFallback
                          src={work.coverImage || DEFAULT_COVER_IMAGE}
                          alt={work.title}
                          className="w-10 h-14 object-cover rounded flex-shrink-0"
                        />
                        <div className="min-w-0 flex-1">
                          <div className="font-medium text-gray-900 dark:text-white text-sm truncate">
                            {work.title}
                          </div>
                          <div className="text-xs text-gray-500 dark:text-gray-400 line-clamp-2 mt-0.5">
                            {work.description || '暂无简介'}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900 dark:text-white">
                        {work.authorName}
                      </div>
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900 dark:text-white">
                        {GENRE_MAP[work.genre] || work.genre}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        {STATUS_MAP[work.status] || work.status}
                      </div>
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900 dark:text-white">
                        {work.totalChapters}章 / {(work.totalWords / 10000).toFixed(1)}万字
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        {work.viewCount}阅读 / {work.favoriteCount}收藏
                      </div>
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <div className="flex flex-col gap-1">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                            work.isPublished
                              ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                              : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-400'
                          }`}
                        >
                          {work.isPublished ? '已发布' : '未发布'}
                        </span>
                        {work.isFeatured && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400">
                            推荐中
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <div className="flex items-center justify-center gap-2">
                        <button
                          onClick={() => handleTogglePublish(work.id, work.isPublished)}
                          className="p-1.5 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded transition-colors"
                          title={work.isPublished ? '取消发布' : '发布小说'}
                        >
                          {work.isPublished ? (
                            <EyeOff className="w-4 h-4" />
                          ) : (
                            <Eye className="w-4 h-4" />
                          )}
                        </button>
                        <button
                          onClick={() => handleToggleFeatured(work.id, work.isFeatured)}
                          className="p-1.5 text-gray-400 hover:text-yellow-600 dark:hover:text-yellow-400 hover:bg-yellow-50 dark:hover:bg-yellow-900/20 rounded transition-colors"
                          title={work.isFeatured ? '取消推荐' : '设为推荐'}
                        >
                          {work.isFeatured ? (
                            <StarOff className="w-4 h-4" />
                          ) : (
                            <Star className="w-4 h-4" />
                          )}
                        </button>
                        <button
                          onClick={() => handleDelete(work.id, work.title)}
                          className="p-1.5 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors"
                          title="删除小说"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* 分页 */}
        {total > pageSize && (
          <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-500 dark:text-gray-400">
                显示 {(page - 1) * pageSize + 1} - {Math.min(page * pageSize, total)} / 共{' '}
                {total} 条
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700"
                >
                  上一页
                </button>
                <button
                  onClick={() => setPage((p) => p + 1)}
                  disabled={page * pageSize >= total}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700"
                >
                  下一页
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
