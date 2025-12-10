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

import { useState, useEffect, useRef } from 'react';
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
  X,
  File,
  AlertCircle,
  CheckCircle
} from 'lucide-react';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import { useConfirm } from '../../hooks/useConfirm';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import type { Work, WorkStatus, WorkGenre } from '../../types';
import type { ImportOptions, ImportPreviewResponse } from '../../types/export';

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

  // 导入弹窗状态
  const [showImportModal, setShowImportModal] = useState(false);
  const [importFile, setImportFile] = useState<File | null>(null);
  const [importFormat, setImportFormat] = useState<'json' | 'markdown' | 'txt'>('json');
  const [importPreview, setImportPreview] = useState<ImportPreviewResponse | null>(null);
  const [isImporting, setIsImporting] = useState(false);
  const [isPreviewing, setIsPreviewing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

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

  // 继续创作 - 跳转到作品详情页
  const handleContinueWriting = (work: Work) => {
    // 直接跳转到作品详情页，作品详情页会自动定位到最后一章
    navigate(`/works/${work.id}`);
  };

  // 导出作品
  const handleExport = (work: Work) => {
    // TODO: 实现导出功能
    showToast('info', '导出功能即将上线');
  };

  // 打开导入弹窗
  const openImportModal = () => {
    setShowImportModal(true);
    setImportFile(null);
    setImportPreview(null);
    setImportFormat('json');
  };

  // 关闭导入弹窗
  const closeImportModal = () => {
    setShowImportModal(false);
    setImportFile(null);
    setImportPreview(null);
  };

  // 处理文件选择
  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setImportFile(file);
    setImportPreview(null);

    // 根据文件扩展名自动选择格式
    const ext = file.name.split('.').pop()?.toLowerCase();
    if (ext === 'json') {
      setImportFormat('json');
    } else if (ext === 'md' || ext === 'markdown') {
      setImportFormat('markdown');
    } else if (ext === 'txt') {
      setImportFormat('txt');
    }

    // 自动预览
    try {
      setIsPreviewing(true);
      const format = ext === 'json' ? 'json' : ext === 'md' || ext === 'markdown' ? 'markdown' : 'txt';
      const preview = await DataService.previewImport(file, format);
      setImportPreview(preview);
    } catch (error: any) {
      console.error('预览失败:', error);
      showToast('error', error?.message || '文件预览失败');
    } finally {
      setIsPreviewing(false);
    }
  };

  // 执行导入
  const handleImport = async () => {
    if (!importFile) {
      showToast('error', '请选择要导入的文件');
      return;
    }

    try {
      setIsImporting(true);
      const options: ImportOptions = {
        format: importFormat,
        createNew: true,
        includeWorldview: true,
        includeGuidelines: true
      };

      const result = await DataService.importWork(importFile, options);
      showToast('success', `导入成功！创建了 ${result.chaptersCreated} 个章节`);
      closeImportModal();
      await loadWorks(); // 重新加载作品列表

      // 导入成功后跳转到作品详情页
      navigate(`/works/${result.workId}`);
    } catch (error: any) {
      console.error('导入失败:', error);
      showToast('error', error?.message || '导入失败，请检查文件格式');
    } finally {
      setIsImporting(false);
    }
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
                onClick={openImportModal}
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

      {/* 导入弹窗 */}
      {showImportModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={closeImportModal}>
          <div className="bg-white w-[550px] max-h-[700px] overflow-y-auto scrollbar-hide" style={{ transform: 'skewX(-2deg)' }} onClick={(e) => e.stopPropagation()}>
            <div style={{ transform: 'skewX(2deg)' }} className="p-6">
              {/* 标题栏 */}
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg text-gray-900">导入作品</h2>
                <button onClick={closeImportModal} className="p-1 hover:bg-gray-100 transition-colors">
                  <X className="w-4 h-4 text-gray-600" />
                </button>
              </div>

              {/* 文件选择区域 */}
              <div className="mb-4">
                <label className="block text-gray-700 mb-2" style={{ fontSize: '12px' }}>选择文件</label>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".json,.md,.markdown,.txt"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <div
                  onClick={() => fileInputRef.current?.click()}
                  className="border-2 border-dashed border-gray-300 hover:border-gray-900 p-8 text-center cursor-pointer transition-colors"
                >
                  {importFile ? (
                    <div className="flex items-center justify-center gap-2">
                      <File className="w-5 h-5 text-gray-600" />
                      <span className="text-gray-900" style={{ fontSize: '13px' }}>{importFile.name}</span>
                      <span className="text-gray-400" style={{ fontSize: '11px' }}>
                        ({(importFile.size / 1024).toFixed(1)} KB)
                      </span>
                    </div>
                  ) : (
                    <div>
                      <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                      <p className="text-gray-600" style={{ fontSize: '13px' }}>点击选择文件或拖拽到此处</p>
                      <p className="text-gray-400 mt-1" style={{ fontSize: '11px' }}>支持 .json / .md / .txt 格式</p>
                    </div>
                  )}
                </div>
              </div>

              {/* 格式说明 */}
              <div className="mb-4 p-3 bg-gray-50 border border-gray-200" style={{ fontSize: '11px' }}>
                <p className="text-gray-600 mb-1"><strong>JSON格式</strong>：完整导入（作品+章节+世界观+规范）</p>
                <p className="text-gray-600 mb-1"><strong>Markdown格式</strong>：自动识别章节标题（## 或 第X章）</p>
                <p className="text-gray-600"><strong>TXT格式</strong>：自动分割章节</p>
              </div>

              {/* 预览加载中 */}
              {isPreviewing && (
                <div className="mb-4 p-4 bg-gray-50 border border-gray-200 text-center">
                  <div className="animate-spin w-6 h-6 border-2 border-gray-300 border-t-gray-900 rounded-full mx-auto mb-2"></div>
                  <p className="text-gray-600" style={{ fontSize: '12px' }}>正在解析文件...</p>
                </div>
              )}

              {/* 预览结果 */}
              {importPreview && !isPreviewing && (
                <div className="mb-4 p-4 bg-gray-50 border border-gray-200">
                  <h3 className="text-gray-900 font-medium mb-3" style={{ fontSize: '13px' }}>预览信息</h3>

                  <div className="space-y-2" style={{ fontSize: '12px' }}>
                    <div className="flex justify-between">
                      <span className="text-gray-600">作品标题</span>
                      <span className="text-gray-900 font-medium">{importPreview.work.title}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">章节数量</span>
                      <span className="text-gray-900">{importPreview.work.totalChapters} 章</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">总字数</span>
                      <span className="text-gray-900">{importPreview.work.totalWords.toLocaleString()} 字</span>
                    </div>
                    {importPreview.charactersCount > 0 && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">人物</span>
                        <span className="text-gray-900">{importPreview.charactersCount} 个</span>
                      </div>
                    )}
                    {importPreview.locationsCount > 0 && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">地点</span>
                        <span className="text-gray-900">{importPreview.locationsCount} 个</span>
                      </div>
                    )}
                  </div>

                  {/* 章节列表 */}
                  {importPreview.chapters.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <p className="text-gray-600 mb-2" style={{ fontSize: '11px' }}>章节列表（前5章）：</p>
                      <div className="space-y-1">
                        {importPreview.chapters.slice(0, 5).map((chapter, idx) => (
                          <div key={idx} className="flex justify-between text-gray-500" style={{ fontSize: '11px' }}>
                            <span className="truncate flex-1 mr-2">{chapter.title}</span>
                            <span>{chapter.wordCount.toLocaleString()} 字</span>
                          </div>
                        ))}
                        {importPreview.chapters.length > 5 && (
                          <p className="text-gray-400" style={{ fontSize: '11px' }}>
                            ...还有 {importPreview.chapters.length - 5} 章
                          </p>
                        )}
                      </div>
                    </div>
                  )}

                  {/* 警告信息 */}
                  {importPreview.warnings.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      {importPreview.warnings.map((warning, idx) => (
                        <div key={idx} className="flex items-center gap-2 text-yellow-600" style={{ fontSize: '11px' }}>
                          <AlertCircle className="w-3.5 h-3.5" />
                          <span>{warning}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* 底部按钮 */}
              <div className="flex items-center gap-2 mt-6">
                <button
                  onClick={closeImportModal}
                  className="flex-1 px-4 py-2.5 border border-gray-300 text-gray-700 hover:bg-white hover:border-gray-900 transition-colors"
                  style={{ transform: 'skewX(-2deg)', fontSize: '12px' }}
                  disabled={isImporting}
                >
                  <span style={{ transform: 'skewX(2deg)' }}>取消</span>
                </button>
                <button
                  onClick={handleImport}
                  disabled={!importFile || !importPreview || isImporting}
                  className={`flex-1 px-4 py-2.5 transition-colors flex items-center justify-center gap-2 ${
                    !importFile || !importPreview || isImporting
                      ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                      : 'bg-black text-white hover:bg-gray-800'
                  }`}
                  style={{ transform: 'skewX(-2deg)', fontSize: '12px' }}
                >
                  {isImporting ? (
                    <>
                      <div className="animate-spin w-4 h-4 border-2 border-white/30 border-t-white rounded-full"></div>
                      <span style={{ transform: 'skewX(2deg)' }}>导入中...</span>
                    </>
                  ) : (
                    <>
                      <CheckCircle className="w-4 h-4" style={{ transform: 'skewX(2deg)' }} />
                      <span style={{ transform: 'skewX(2deg)' }}>确认导入</span>
                    </>
                  )}
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
