/**
 * WorksView 组件 - 重构后的作品列表页面
 *
 * 特点：
 * - 现代化倾斜(skew)设计风格
 * - 统计卡片展示
 * - 搜索、筛选、排序功能
 * - 进度条动画效果
 * - 悬停交互动画
 * - 编辑弹窗
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Plus,
  Upload,
  MoreVertical,
  Clock,
  BookOpen,
  FileText,
  Edit3,
  Trash2,
  Download,
  TrendingUp,
  Search,
  Pin,
  Circle,
  X
} from 'lucide-react';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import { useConfirm } from '../../hooks/useConfirm';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import type { Work, WorkStatus, WorkGenre } from '../../types';

// 默认封面路径
const DEFAULT_COVER_IMAGE = '/default-cover.jpg';

const WorksView: React.FC = () => {
  const navigate = useNavigate();
  const { showToast } = useGlobalStore();
  const { confirmState, confirm, closeConfirm } = useConfirm();

  // 数据状态
  const [works, setWorks] = useState<Work[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // 筛选和搜索状态
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStatus, setSelectedStatus] = useState<string>('all');
  const [selectedGenre, setSelectedGenre] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'date' | 'words' | 'title'>('date');

  // 编辑弹窗状态
  const [editingWork, setEditingWork] = useState<Work | null>(null);
  const [editFormData, setEditFormData] = useState({
    title: '',
    description: '',
    genre: '' as WorkGenre | '',
    status: 'draft' as WorkStatus,
    coverImage: ''
  });

  // 加载作品列表
  useEffect(() => {
    loadWorks();
  }, []);

  const loadWorks = async () => {
    try {
      setIsLoading(true);
      const data = await DataService.getWorks();
      setWorks(data);
    } catch (error) {
      console.error('加载作品失败:', error);
      showToast('error', '加载作品失败');
    } finally {
      setIsLoading(false);
    }
  };

  // 状态文本映射
  const getStatusText = (status: WorkStatus) => {
    const map: Record<WorkStatus, string> = {
      writing: '连载中',
      completed: '已完结',
      draft: '草稿',
      abandoned: '已弃坑'
    };
    return map[status] || '草稿';
  };

  // 状态颜色映射
  const getStatusColor = (status: WorkStatus) => {
    const map: Record<WorkStatus, string> = {
      writing: 'bg-green-100 text-green-700',
      completed: 'bg-blue-100 text-blue-700',
      draft: 'bg-gray-100 text-gray-600',
      abandoned: 'bg-red-100 text-red-600'
    };
    return map[status] || 'bg-gray-100 text-gray-600';
  };

  // 相对时间格式化
  const getRelativeTime = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return '今天';
    if (diffDays === 1) return '昨天';
    if (diffDays < 7) return `${diffDays}天前`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)}个月前`;
    return `${Math.floor(diffDays / 365)}年前`;
  };

  // 打开编辑弹窗
  const openEditModal = (work: Work) => {
    setEditingWork(work);
    setEditFormData({
      title: work.title,
      description: work.description || '',
      genre: work.genre,
      status: work.status,
      coverImage: work.coverImage || ''
    });
  };

  // 关闭编辑弹窗
  const closeEditModal = () => {
    setEditingWork(null);
  };

  // 保存编辑
  const saveEdit = async () => {
    if (!editingWork) return;

    try {
      await DataService.updateWork(editingWork.id, {
        title: editFormData.title,
        description: editFormData.description,
        genre: editFormData.genre as WorkGenre,
        status: editFormData.status,
        coverImage: editFormData.coverImage
      });

      // 重新加载数据
      await loadWorks();
      closeEditModal();
      showToast('success', '作品信息已更新');
    } catch (error) {
      console.error('保存失败:', error);
      showToast('error', '保存失败');
    }
  };

  // 删除作品
  const handleDelete = async (id: string, title: string) => {
    const confirmed = await confirm({
      title: '删除作品',
      message: `确定要删除《${title}》吗？此操作不可撤销。`,
      variant: 'danger',
    });

    if (!confirmed) return;

    try {
      await DataService.deleteWork(id);
      await loadWorks();
      showToast('success', '作品已删除');
    } catch (error) {
      console.error('删除失败:', error);
      showToast('error', '删除失败');
    }
  };

  // 继续创作 - 获取最后一个章节或创建新章节
  const handleContinueWriting = async (work: Work) => {
    try {
      // 获取该作品的章节列表
      const chapters = await DataService.getChapters(work.id);

      if (chapters.length > 0) {
        // 如果有章节，跳转到最后一个章节
        const lastChapter = chapters[chapters.length - 1];
        navigate(`/editor/${lastChapter.id}`);
      } else {
        // 如果没有章节，创建一个新章节
        const newChapter = await DataService.createChapter({
          work_id: work.id,
          title: '第一章',
          content: '',
          order: 1
        });
        navigate(`/editor/${newChapter.id}`);
      }
    } catch (error) {
      console.error('继续创作失败:', error);
      showToast('error', '无法打开编辑器');
    }
  };

  // 导出作品
  const handleExport = (work: Work) => {
    // TODO: 实现导出功能
    showToast('info', '导出功能即将上线');
  };

  // 筛选和排序
  const filteredWorks = works
    .filter(work => {
      const matchesSearch = work.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           (work.description && work.description.toLowerCase().includes(searchQuery.toLowerCase()));
      const matchesStatus = selectedStatus === 'all' || work.status === selectedStatus;
      const matchesGenre = selectedGenre === 'all' || work.genre === selectedGenre;
      return matchesSearch && matchesStatus && matchesGenre;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime();
        case 'words':
          return b.totalWords - a.totalWords;
        case 'title':
          return a.title.localeCompare(b.title, 'zh-CN');
        default:
          return 0;
      }
    });

  // 统计数据
  const totalWords = works.reduce((sum, work) => sum + work.totalWords, 0);
  const writingCount = works.filter(work => work.status === 'writing').length;

  // 获取本周新增字数（示例：使用最近7天内更新的作品字数）
  const weekNewWords = works
    .filter(work => {
      const diff = Date.now() - new Date(work.updatedAt).getTime();
      return diff < 7 * 24 * 60 * 60 * 1000;
    })
    .reduce((sum, work) => sum + work.totalWords, 0);

  // 所有类型列表
  const allGenres = ['all', ...Array.from(new Set(works.map(work => work.genre).filter(Boolean)))];

  // 类型显示名称映射
  const genreDisplayName: Record<string, string> = {
    fantasy: '玄幻',
    urban: '都市',
    romance: '言情',
    scifi: '科幻',
    wuxia: '武侠',
    game: '游戏',
    history: '历史',
    military: '军事',
    other: '其他'
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#fafafa] flex items-center justify-center">
        <div className="text-gray-500">加载中...</div>
      </div>
    );
  }

  return (
    <div className="bg-[#fafafa] flex flex-col overflow-hidden" style={{ height: 'calc(100vh - 56px)' }}>
      {/* Header */}
      <header className="bg-[#fafafa] border-b border-gray-200 flex-shrink-0">
        <div className="w-full max-w-[1400px] mx-auto px-12 py-6">
          {/* 第一行：标题和按钮 */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-6">
              <div className="relative">
                <div className="bg-black text-white px-8 py-3.5" style={{ transform: 'skewX(-2deg)' }}>
                  <h1 className="text-2xl font-medium" style={{ transform: 'skewX(2deg)' }}>我的作品</h1>
                </div>
              </div>
              <div className="flex items-center gap-1" style={{ fontSize: '13px' }}>
                <span className="text-gray-400">共</span>
                <span className="text-gray-900 font-medium">{works.length}</span>
                <span className="text-gray-400">部作品</span>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => showToast('info', '导入功能即将上线')}
                className="px-5 py-2.5 border border-gray-300 text-gray-700 hover:bg-white hover:border-gray-900 transition-colors flex items-center gap-2"
                style={{ transform: 'skewX(-2deg)', fontSize: '13px' }}
              >
                <Upload className="w-4 h-4" style={{ transform: 'skewX(2deg)' }} />
                <span style={{ transform: 'skewX(2deg)' }}>导入作品</span>
              </button>
              <button
                onClick={() => navigate('/works/create')}
                className="px-5 py-2.5 bg-black text-white hover:bg-gray-800 transition-colors flex items-center gap-2"
                style={{ transform: 'skewX(-2deg)', fontSize: '13px' }}
              >
                <Plus className="w-4 h-4" style={{ transform: 'skewX(2deg)' }} />
                <span style={{ transform: 'skewX(2deg)' }}>新建作品</span>
              </button>
            </div>
          </div>

          {/* 第二行：统计卡片 */}
          <div className="flex gap-4 mb-6">
            <div className="bg-white border border-gray-200 px-6 py-4 flex-1" style={{ transform: 'skewX(-2deg)' }}>
              <div style={{ transform: 'skewX(2deg)' }}>
                <div className="text-gray-400 mb-1.5" style={{ fontSize: '12px' }}>总字数</div>
                <div className="text-3xl text-gray-900 font-medium">{totalWords.toLocaleString()}</div>
              </div>
            </div>
            <div className="bg-white border border-gray-200 px-6 py-4 flex-1" style={{ transform: 'skewX(-2deg)' }}>
              <div style={{ transform: 'skewX(2deg)' }}>
                <div className="text-gray-400 mb-1.5" style={{ fontSize: '12px' }}>本周新增</div>
                <div className="text-3xl text-gray-900 font-medium">+{weekNewWords.toLocaleString()}</div>
              </div>
            </div>
            <div className="bg-white border border-gray-200 px-6 py-4 flex-1" style={{ transform: 'skewX(-2deg)' }}>
              <div style={{ transform: 'skewX(2deg)' }}>
                <div className="text-gray-400 mb-1.5" style={{ fontSize: '12px' }}>连载中</div>
                <div className="text-3xl text-gray-900 font-medium">{writingCount}</div>
              </div>
            </div>
          </div>

          {/* 第三行：搜索和筛选 */}
          <div className="flex items-center gap-3">
            {/* 搜索框 */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="搜索作品标题或简介..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 text-gray-900 placeholder:text-gray-400 focus:outline-none focus:border-gray-900 transition-colors"
                style={{ fontSize: '13px' }}
              />
            </div>

            {/* 状态筛选 */}
            <div className="flex gap-1">
              {['all', 'writing', 'draft', 'completed'].map(status => (
                <button
                  key={status}
                  onClick={() => setSelectedStatus(status)}
                  className={`px-3 py-2 border transition-colors ${
                    selectedStatus === status
                      ? 'bg-black text-white border-black'
                      : 'bg-white text-gray-700 border-gray-200 hover:border-gray-900'
                  }`}
                  style={{ transform: 'skewX(-2deg)', fontSize: '10px' }}
                >
                  <span style={{ transform: 'skewX(2deg)' }}>
                    {status === 'all' ? '全部' : getStatusText(status as WorkStatus)}
                  </span>
                </button>
              ))}
            </div>

            {/* 类型筛选 */}
            <select
              value={selectedGenre}
              onChange={(e) => setSelectedGenre(e.target.value)}
              className="px-3 py-2 bg-white border border-gray-200 text-gray-700 focus:outline-none focus:border-gray-900 transition-colors cursor-pointer"
              style={{ transform: 'skewX(-2deg)', fontSize: '10px' }}
            >
              {allGenres.map(genre => (
                <option key={genre} value={genre}>
                  {genre === 'all' ? '全部类型' : genreDisplayName[genre] || genre}
                </option>
              ))}
            </select>

            {/* 排序 */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="px-3 py-2 bg-white border border-gray-200 text-gray-700 focus:outline-none focus:border-gray-900 transition-colors cursor-pointer"
              style={{ transform: 'skewX(-2deg)', fontSize: '10px' }}
            >
              <option value="date">最近编辑</option>
              <option value="words">字数排序</option>
              <option value="title">标题排序</option>
            </select>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="w-full max-w-[1400px] mx-auto px-12 pt-8 overflow-y-auto scrollbar-hide flex-1">
        {filteredWorks.length === 0 ? (
          // 空状态
          <div className="flex flex-col items-center justify-center h-full">
            <div className="bg-white border border-gray-200 p-12 text-center" style={{ transform: 'skewX(-2deg)' }}>
              <div style={{ transform: 'skewX(2deg)' }}>
                <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg text-gray-900 mb-2">暂无作品</h3>
                <p className="text-gray-400 mb-6" style={{ fontSize: '11px' }}>
                  {searchQuery || selectedStatus !== 'all' || selectedGenre !== 'all'
                    ? '没有找到匹配的作品，试试调整筛选条件'
                    : '开始创作你的第一部作品吧'}
                </p>
                {!searchQuery && selectedStatus === 'all' && selectedGenre === 'all' && (
                  <button
                    onClick={() => navigate('/works/create')}
                    className="px-6 py-2.5 bg-black text-white hover:bg-gray-800 transition-colors inline-flex items-center gap-2"
                    style={{ transform: 'skewX(-2deg)', fontSize: '11px' }}
                  >
                    <Plus className="w-4 h-4" style={{ transform: 'skewX(2deg)' }} />
                    <span style={{ transform: 'skewX(2deg)' }}>新建作品</span>
                  </button>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredWorks.map((work) => (
              <div
                key={work.id}
                className="group bg-white overflow-hidden transition-all duration-300 ease-out border border-gray-100 hover:border-gray-900 h-[140px] hover:h-[160px] hover:my-4 hover:shadow-2xl relative cursor-pointer"
                style={{ transform: 'skewX(-2deg)', transitionProperty: 'all' }}
                onClick={() => navigate(`/works/${work.id}`)}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'skewX(-3deg)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'skewX(-2deg)';
                }}
              >
                <div className="flex h-full">
                  {/* Cover - 左侧封面 */}
                  <div className="w-[200px] flex-shrink-0 overflow-hidden" style={{ height: '100%' }}>
                    <img
                      src={work.coverImage || DEFAULT_COVER_IMAGE}
                      alt={work.title}
                      className="object-cover transition-transform duration-300 ease-out group-hover:scale-105"
                      style={{ width: '200px', height: '100%', display: 'block' }}
                      onError={(e) => {
                        // 如果图片加载失败，显示默认图标
                        e.currentTarget.style.display = 'none';
                        const parent = e.currentTarget.parentElement;
                        if (parent && !parent.querySelector('.fallback-icon')) {
                          const fallback = document.createElement('div');
                          fallback.className = 'fallback-icon absolute inset-0 w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center';
                          fallback.innerHTML = '<svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>';
                          parent.appendChild(fallback);
                        }
                      }}
                    />
                  </div>

                  {/* Content - 右侧信息 */}
                  <div className="flex-1 p-5 flex items-center transition-all duration-300 ease-out" style={{ transform: 'skewX(2deg)' }}>
                    <div className="flex-1 transition-transform duration-300 ease-out group-hover:scale-105" style={{ transformOrigin: 'left center' }}>
                      {/* Title & Status */}
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-lg font-medium text-gray-900 group-hover:text-black transition-colors">
                          {work.title}
                        </h3>
                        <span className={`px-2 py-0.5 ${getStatusColor(work.status)}`} style={{ fontSize: '11px' }}>
                          {getStatusText(work.status)}
                        </span>
                        {work.genre && (
                          <span className="px-2 py-0.5 bg-gray-50 text-gray-600" style={{ fontSize: '11px' }}>
                            {genreDisplayName[work.genre] || work.genre}
                          </span>
                        )}
                      </div>

                      {/* Description */}
                      {work.description && (
                        <p className="text-gray-500 mb-2 line-clamp-1" style={{ fontSize: '13px' }}>
                          {work.description}
                        </p>
                      )}

                      {/* Progress Bar - 进度条 */}
                      {work.totalWords > 0 && (
                        <div className="mb-2">
                          <div className="flex items-center gap-2 mb-0.5">
                            <span className="text-gray-400" style={{ fontSize: '10px' }}>创作进度</span>
                            <span className="text-gray-500" style={{ fontSize: '10px' }}>
                              {work.totalWords.toLocaleString()} / {(100000).toLocaleString()} 字
                            </span>
                          </div>
                          <div className="w-2/3 bg-gray-200 h-1 overflow-hidden" style={{ transform: 'skewX(-2deg)' }}>
                            <div
                              className={`h-1 transition-all ${work.status === 'writing' ? 'bg-black progress-stripes' : 'bg-black'}`}
                              style={{
                                width: `${Math.min((work.totalWords / 100000) * 100, 100)}%`,
                                boxShadow: '0 0 6px rgba(0, 0, 0, 0.2)'
                              }}
                            ></div>
                          </div>
                        </div>
                      )}

                      {/* Stats */}
                      <div className="flex items-center gap-4 text-gray-400" style={{ fontSize: '13px' }}>
                        <div className="flex items-center gap-1.5">
                          <Clock className="w-3.5 h-3.5" />
                          <span>{getRelativeTime(work.updatedAt)}</span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          <BookOpen className="w-3.5 h-3.5" />
                          <span>{work.totalChapters} 章节</span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          <FileText className="w-3.5 h-3.5" />
                          <span>{work.totalWords.toLocaleString()} 字</span>
                        </div>
                        {work.status === 'writing' && (
                          <div className="flex items-center gap-1.5 text-green-600">
                            <TrendingUp className="w-3.5 h-3.5" />
                            <span>更新中</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Actions - 右侧操作按钮 */}
                    <div className="flex items-center gap-2 ml-4 flex-shrink-0">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/works/${work.id}`);
                        }}
                        className="px-4 py-1.5 bg-black text-white hover:bg-gray-800 transition-colors"
                        style={{ transform: 'skewX(-2deg)', fontSize: '13px' }}
                      >
                        <span style={{ transform: 'skewX(2deg)', display: 'inline-block' }}>查看详情</span>
                      </button>

                      {/* Quick Actions - hover时显示 */}
                      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleContinueWriting(work);
                          }}
                          className="p-2 hover:bg-gray-100 transition-colors"
                          title="继续创作"
                        >
                          <BookOpen className="w-3.5 h-3.5 text-gray-600" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            openEditModal(work);
                          }}
                          className="p-2 hover:bg-gray-100 transition-colors"
                          title="编辑信息"
                        >
                          <Edit3 className="w-3.5 h-3.5 text-gray-600" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleExport(work);
                          }}
                          className="p-2 hover:bg-gray-100 transition-colors"
                          title="导出"
                        >
                          <Download className="w-3.5 h-3.5 text-gray-600" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDelete(work.id, work.title);
                          }}
                          className="p-2 hover:bg-red-50 transition-colors"
                          title="删除"
                        >
                          <Trash2 className="w-3.5 h-3.5 text-red-500" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* 编辑弹窗 */}
      {editingWork && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={closeEditModal}>
          <div className="bg-white w-[500px] max-h-[600px] overflow-y-auto scrollbar-hide" style={{ transform: 'skewX(-2deg)' }} onClick={(e) => e.stopPropagation()}>
            <div style={{ transform: 'skewX(2deg)' }} className="p-6">
              {/* 标题栏 */}
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg text-gray-900">编辑作品信息</h2>
                <button onClick={closeEditModal} className="p-1 hover:bg-gray-100 transition-colors">
                  <X className="w-4 h-4 text-gray-600" />
                </button>
              </div>

              {/* 表单 */}
              <div className="space-y-3">
                {/* 标题 */}
                <div>
                  <label className="block text-gray-700 mb-1" style={{ fontSize: '11px' }}>作品标题</label>
                  <input
                    type="text"
                    value={editFormData.title}
                    onChange={(e) => setEditFormData({ ...editFormData, title: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-200 text-gray-900 focus:outline-none focus:border-gray-900 transition-colors"
                    style={{ fontSize: '12px' }}
                    placeholder="输入作品标题"
                  />
                </div>

                {/* 简介 */}
                <div>
                  <label className="block text-gray-700 mb-1" style={{ fontSize: '11px' }}>作品简介</label>
                  <textarea
                    value={editFormData.description}
                    onChange={(e) => setEditFormData({ ...editFormData, description: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-200 text-gray-900 focus:outline-none focus:border-gray-900 transition-colors resize-none"
                    style={{ fontSize: '12px' }}
                    rows={2}
                    placeholder="输入作品简介"
                  />
                </div>

                {/* 类型和状态 */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-gray-700 mb-1" style={{ fontSize: '11px' }}>作品类型</label>
                    <select
                      value={editFormData.genre}
                      onChange={(e) => setEditFormData({ ...editFormData, genre: e.target.value as WorkGenre })}
                      className="w-full px-3 py-2 border border-gray-200 text-gray-900 focus:outline-none focus:border-gray-900 transition-colors cursor-pointer bg-white"
                      style={{ fontSize: '12px' }}
                    >
                      <option value="">选择类型</option>
                      {Object.entries(genreDisplayName).map(([value, label]) => (
                        <option key={value} value={value}>{label}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-gray-700 mb-1" style={{ fontSize: '11px' }}>作品状态</label>
                    <select
                      value={editFormData.status}
                      onChange={(e) => setEditFormData({ ...editFormData, status: e.target.value as WorkStatus })}
                      className="w-full px-3 py-2 border border-gray-200 text-gray-900 focus:outline-none focus:border-gray-900 transition-colors cursor-pointer bg-white"
                      style={{ fontSize: '12px' }}
                    >
                      <option value="draft">草稿</option>
                      <option value="writing">连载中</option>
                      <option value="completed">已完结</option>
                      <option value="abandoned">已弃坑</option>
                    </select>
                  </div>
                </div>

                {/* 封面图片上传 */}
                <div>
                  <label className="block text-gray-700 mb-1" style={{ fontSize: '11px' }}>封面图片</label>
                  <input
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    onChange={async (e) => {
                      const file = e.target.files?.[0];
                      if (file && editingWork) {
                        try {
                          const coverUrl = await DataService.uploadWorkCover(editingWork.id, file);
                          setEditFormData({ ...editFormData, coverImage: coverUrl });
                        } catch (error) {
                          console.error('上传封面失败:', error);
                          alert('上传封面失败，请重试');
                        }
                      }
                    }}
                    className="w-full px-3 py-2 border border-gray-200 text-gray-900 focus:outline-none focus:border-gray-900 transition-colors cursor-pointer bg-white"
                    style={{ fontSize: '12px' }}
                  />
                  {editFormData.coverImage && (
                    <div className="mt-2">
                      <img
                        src={editFormData.coverImage}
                        alt="封面预览"
                        className="w-full h-32 object-cover border border-gray-200"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none';
                        }}
                      />
                    </div>
                  )}
                </div>
              </div>

              {/* 底部按钮 */}
              <div className="flex items-center gap-2 mt-6">
                <button
                  onClick={closeEditModal}
                  className="flex-1 px-4 py-2.5 border border-gray-300 text-gray-700 hover:bg-white hover:border-gray-900 transition-colors"
                  style={{ transform: 'skewX(-2deg)', fontSize: '11px' }}
                >
                  <span style={{ transform: 'skewX(2deg)' }}>取消</span>
                </button>
                <button
                  onClick={saveEdit}
                  className="flex-1 px-4 py-2.5 bg-black text-white hover:bg-gray-800 transition-colors"
                  style={{ transform: 'skewX(-2deg)', fontSize: '11px' }}
                >
                  <span style={{ transform: 'skewX(2deg)' }}>保存修改</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 确认对话框 */}
      <ConfirmDialog
        isOpen={confirmState.isOpen}
        title={confirmState.title}
        message={confirmState.message}
        variant={confirmState.variant}
        onConfirm={confirmState.onConfirm}
        onCancel={closeConfirm}
      />
    </div>
  );
};

export default WorksView;
