import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  Plus,
  Search,
  Upload,
  Trash2,
  Edit2,
  FileText,
  Book,
  File,
  MoreVertical,
  FolderOpen,
  Tag,
  Calendar,
  RefreshCw,
  Sparkles,
  AlertTriangle,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import FilePicker from '@/components/common/FilePicker';
import { knowledgeApi, type KnowledgeItem as ApiKnowledgeItem } from '@/services/knowledgeApi';
import { ToastContainer } from '@/components/ui/Toast';
import { useToast } from '@/hooks/useToast';
import { useKnowledgeStore } from '@/store/knowledgeStore';
import { useDebounce } from 'use-debounce';


type SourceType = 'manual' | 'book_analysis' | 'ai_generated' | 'imported' | 'text' | 'file' | 'url';
type KnowledgeCategory = 'character' | 'worldview' | 'plot' | 'dialogue' | 'description' | 'technique' | 'reference' | 'other';

const CATEGORY_OPTIONS: { value: KnowledgeCategory; label: string }[] = [
  { value: 'technique', label: '写作技巧' },
  { value: 'character', label: '特色设定' },
  { value: 'worldview', label: '世界观' },
  { value: 'plot', label: '支线剧情' },
  { value: 'dialogue', label: '对话台词' },
  { value: 'description', label: '场景描写' },
  { value: 'reference', label: '参考资料' },
  { value: 'other', label: '其他' },
];

type KnowledgeItem = ApiKnowledgeItem & {
  category?: KnowledgeCategory | string;
  source_type?: SourceType;
};

const PAGE_SIZE = 20;

const KnowledgeView: React.FC = () => {
  // 使用 store 获取缓存的数据
  const { items: cachedItems, setItems: setCachedItems, shouldRefetch } = useKnowledgeStore();

  const [items, setItems] = useState<KnowledgeItem[]>(cachedItems);
  const [loading, setLoading] = useState(cachedItems.length === 0);
  const [searchQuery, setSearchQuery] = useState('');
  const [tagFilter, setTagFilter] = useState('');
  const [refreshing, setRefreshing] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [debouncedSearchQuery] = useDebounce(searchQuery.trim(), 300);
  const [debouncedTagFilter] = useDebounce(tagFilter.trim(), 300);

  // AbortController ref，用于取消正在进行的请求
  const abortControllerRef = useRef<AbortController | null>(null);
  const mountedRef = useRef(true);
  const requestIdRef = useRef(0);
  const sentinelRef = useRef<HTMLDivElement | null>(null);

  const [showAddDialog, setShowAddDialog] = useState(false);
  const [showUploadDialog, setShowUploadDialog] = useState(false);
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [currentItem, setCurrentItem] = useState<KnowledgeItem | null>(null);

  const [formTitle, setFormTitle] = useState('');
  const [formContent, setFormContent] = useState('');
  const [formTags, setFormTags] = useState('');
  const [formCategory, setFormCategory] = useState<KnowledgeCategory>('technique');
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const { warning: showWarning, success: showSuccess, error: showError, messages, close } = useToast();

  const loadItems = useCallback(
    async ({
      forceRefresh = false,
      page: targetPage = 1,
      append = false,
    }: { forceRefresh?: boolean; page?: number; append?: boolean } = {}) => {
      const normalizedSearch = debouncedSearchQuery;
      const normalizedTags = debouncedTagFilter;

      // 如果不强制刷新且缓存有效，直接使用缓存
      if (!append && !forceRefresh && !shouldRefetch(normalizedSearch, normalizedTags)) {
        setItems(cachedItems);
        setLoading(false);
        setRefreshing(false);
        setHasMore(cachedItems.length >= PAGE_SIZE);
        setPage(1);
        return;
      }

      // 取消之前的请求
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }

      // 创建新的 AbortController
      const controller = new AbortController();
      abortControllerRef.current = controller;
      const requestId = ++requestIdRef.current;

      try {
        if (append) {
          setLoadingMore(true);
        } else if (cachedItems.length === 0) {
          setLoading(true);
        } else {
          setRefreshing(true);
        }
        const tagList = normalizedTags.split(',').map((t) => t.trim()).filter(Boolean);
        const data = await knowledgeApi.getList(
          {
            search: normalizedSearch || undefined,
            tags: tagList.length > 0 ? tagList : undefined,
            limit: PAGE_SIZE,
            skip: (targetPage - 1) * PAGE_SIZE,
          },
          controller.signal
        );

        // 检查请求是否被取消或过期
        if (controller.signal.aborted || !mountedRef.current || requestId !== requestIdRef.current) return;

        const newItems = data.items || [];
        const total = data.total;
        let computedHasMore = false;

        setItems((prev) => {
          if (append) {
            const existingIds = new Set(prev.map((i) => i.id));
            const merged = [...prev];
            newItems.forEach((item) => {
              if (!existingIds.has(item.id)) {
                merged.push(item);
              }
            });
            computedHasMore = total !== undefined ? merged.length < total : newItems.length === PAGE_SIZE;
            return merged;
          }

          computedHasMore = total !== undefined ? newItems.length < total : newItems.length === PAGE_SIZE;
          return newItems;
        });

        if (!append) {
          setCachedItems(newItems, normalizedSearch, normalizedTags);
        }

        setHasMore(computedHasMore);
        setPage(targetPage);
      } catch (error: any) {
        // 忽略取消的请求错误
        if (error?.name === 'CanceledError' || error?.code === 'ERR_CANCELED') {
          return;
        }
        console.error('Failed to load knowledge items:', error);
      } finally {
        // 只有当请求没有被取消时才设置 loading 为 false
        if (!controller.signal.aborted && mountedRef.current && requestId === requestIdRef.current) {
          setLoading(false);
          setRefreshing(false);
          setLoadingMore(false);
        }
      }
    },
    [debouncedSearchQuery, debouncedTagFilter, shouldRefetch, cachedItems, setCachedItems]
  );

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  useEffect(() => {
    setPage(1);
    setHasMore(true);
    loadItems({ page: 1 });
  }, [debouncedSearchQuery, debouncedTagFilter, loadItems]);

  // 监听滚动到底部，自动加载更多
  useEffect(() => {
    const el = sentinelRef.current;
    if (!el || !hasMore || loading || refreshing || loadingMore) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const [entry] = entries;
        if (entry.isIntersecting && hasMore && !loading && !refreshing && !loadingMore) {
          loadItems({ forceRefresh: true, page: page + 1, append: true });
        }
      },
      { root: null, rootMargin: '200px' }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [hasMore, loading, refreshing, loadingMore, page, loadItems]);

  const resetForm = () => {
    setFormTitle('');
    setFormContent('');
    setFormTags('');
    setFormCategory('technique');
    setUploadFile(null);
    setCurrentItem(null);
  };

  const handleAddText = async () => {
    if (!formTitle.trim() || !formContent.trim()) return;

    try {
      setSubmitting(true);
      await knowledgeApi.create({
        title: formTitle.trim(),
        content: formContent.trim(),
        category: formCategory,
        tags: formTags.split(',').map((t) => t.trim()).filter(Boolean),
      });
      setShowAddDialog(false);
      resetForm();
      loadItems({ forceRefresh: true, page: 1 });
      showSuccess('添加成功', '知识条目已创建并向量化');
    } catch (error: any) {
      console.error('Failed to add knowledge:', error);
      const errorMessage = error?.response?.data?.detail
        || error?.detail
        || error?.message
        || '添加知识失败，请稍后重试';
      showError('添加失败', errorMessage);
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpload = async () => {
    if (!uploadFile || !formTitle.trim()) return;

    try {
      setSubmitting(true);
      const created = await knowledgeApi.upload(uploadFile, {
        title: formTitle.trim(),
        category: formCategory,
        tags: formTags.split(',').map((t) => t.trim()).filter(Boolean),
      });
      setShowUploadDialog(false);
      resetForm();
      loadItems({ forceRefresh: true, page: 1 });
      if (created?.extra_data?.vectorization_warning) {
        showWarning('向量化提示', created.extra_data.vectorization_warning);
      } else {
        showSuccess('上传成功', '知识条目已创建并向量化');
      }
    } catch (error: any) {
      console.error('Failed to upload file:', error);
      // 解析错误信息，支持多种后端错误格式
      const errorMessage = error?.response?.data?.detail
        || error?.detail
        || error?.message
        || '文件上传失败，请稍后重试';
      showError('上传失败', errorMessage);
    } finally {
      setSubmitting(false);
    }
  };

  const handleEdit = async () => {
    if (!currentItem || !formTitle.trim()) return;

    try {
      setSubmitting(true);
      await knowledgeApi.update(currentItem.id, {
        title: formTitle.trim(),
        content: formContent.trim() || undefined,
        category: formCategory,
        tags: formTags.split(',').map((t) => t.trim()).filter(Boolean),
      });
      setShowEditDialog(false);
      resetForm();
      loadItems({ forceRefresh: true, page: 1 });
      showSuccess('更新成功', '知识条目已更新');
    } catch (error: any) {
      console.error('Failed to update knowledge:', error);
      const errorMessage = error?.response?.data?.detail
        || error?.detail
        || error?.message
        || '更新知识失败，请稍后重试';
      showError('更新失败', errorMessage);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!currentItem) return;

    try {
      setSubmitting(true);
      await knowledgeApi.delete(currentItem.id);
      setShowDeleteDialog(false);
      setCurrentItem(null);
      loadItems({ forceRefresh: true, page: 1 });
      showSuccess('删除成功', '知识条目已删除');
    } catch (error: any) {
      console.error('Failed to delete knowledge:', error);
      const errorMessage = error?.response?.data?.detail
        || error?.detail
        || error?.message
        || '删除知识失败，请稍后重试';
      showError('删除失败', errorMessage);
    } finally {
      setSubmitting(false);
    }
  };

  const openEditDialog = (item: KnowledgeItem) => {
    setCurrentItem(item);
    setFormTitle(item.title);
    setFormContent(item.content || '');
    setFormTags(item.tags.join(', '));
    const nextCategory = CATEGORY_OPTIONS.some(opt => opt.value === item.category)
      ? (item.category as KnowledgeCategory)
      : 'other';
    setFormCategory(nextCategory);
    setShowEditDialog(true);
  };

  const openDeleteDialog = (item: KnowledgeItem) => {
    setCurrentItem(item);
    setShowDeleteDialog(true);
  };

  const getSourceIcon = (item: KnowledgeItem) => {
    switch (item.source_type) {
      case 'book_analysis':
        return <Book className="w-4 h-4 text-purple-600" />;
      case 'ai_generated':
        return <Sparkles className="w-4 h-4 text-amber-500" />;
      case 'imported':
        return <File className="w-4 h-4 text-blue-500" />;
      default:
        return <FileText className="w-4 h-4 text-gray-600" />;
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="h-full flex flex-col bg-gray-50 dark:bg-gray-900 overflow-hidden">
      <ToastContainer messages={messages} onClose={close} />
      {/* 固定页眉 */}
      <div className="flex-shrink-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-xl font-semibold text-gray-900 dark:text-gray-100">我的知识库</h1>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              存储参考资料、写作素材和创作灵感，创作时随时调用
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowUploadDialog(true)}
            >
              <Upload className="w-4 h-4 mr-1" />
              上传文件
            </Button>
            <Button
              size="sm"
              onClick={() => setShowAddDialog(true)}
            >
              <Plus className="w-4 h-4 mr-1" />
              添加文本
            </Button>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <Input
              placeholder="搜索知识..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9"
            />
          </div>
          <Input
            placeholder="标签筛选（逗号分隔）"
            value={tagFilter}
            onChange={(e) => setTagFilter(e.target.value)}
            className="max-w-xs"
          />
          <Button
            variant="ghost"
            size="sm"
            onClick={() => loadItems({ forceRefresh: true, page: 1 })}
            disabled={loading || refreshing}
          >
            <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin text-blue-600' : ''}`} />
          </Button>
        </div>
      </div>

      {/* 可滚动内容区 */}
      <div className="flex-1 overflow-auto p-6">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : items.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-gray-500">
            <FolderOpen className="w-12 h-12 mb-3 text-gray-300" />
            <p className="text-sm">暂无知识条目</p>
            <p className="text-xs mt-1">点击上方按钮创建你的第一个知识</p>
          </div>
        ) : (
          <>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {items.map((item) => (
                <div
                  key={item.id}
                  className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      {getSourceIcon(item)}
                      <h3 className="font-medium text-gray-900 dark:text-gray-100 text-sm truncate">
                        {item.title}
                      </h3>
                    </div>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                          <MoreVertical className="w-3 h-3" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => openEditDialog(item)}>
                          <Edit2 className="w-3 h-3 mr-2" />
                          编辑
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => openDeleteDialog(item)}>
                          <Trash2 className="w-3 h-3 mr-2 text-red-500" />
                          <span className="text-red-500">删除</span>
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>

                  {item.content && (
                    <p className="text-xs text-gray-500 line-clamp-2 mb-3">
                      {item.content.slice(0, 300)}
                    </p>
                  )}

                  {item.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1 mb-3">
                      {item.tags.slice(0, 3).map((tag) => (
                        <span
                          key={tag}
                          className="inline-flex items-center px-1.5 py-0.5 rounded text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300"
                        >
                          <Tag className="w-2 h-2 mr-1" />
                          {tag}
                        </span>
                      ))}
                      {item.tags.length > 3 && (
                        <span className="text-xs text-gray-400">
                          +{item.tags.length - 3}
                        </span>
                      )}
                    </div>
                  )}

                  {item.extra_data?.vectorization_warning && (
                    <div className="flex items-center gap-1 text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/30 border border-amber-100 dark:border-amber-800 rounded px-2 py-1 text-[11px] mb-3">
                      <AlertTriangle className="w-3 h-3" />
                      <span className="truncate">{item.extra_data.vectorization_warning}</span>
                    </div>
                  )}

                  <div className="flex items-center justify-between text-xs text-gray-400">
                    <div className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {formatDate(item.created_at)}
                    </div>
                    {item.chunk_count && (
                      <span>{item.chunk_count} 个片段</span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {loadingMore && (
              <div className="flex items-center justify-center py-4 text-sm text-gray-500">
                <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mr-2" />
                正在加载更多...
              </div>
            )}
            {!hasMore && items.length > 0 && (
              <div className="flex items-center justify-center py-3 text-xs text-gray-400">
                已经到底了
              </div>
            )}
            <div ref={sentinelRef} className="h-4" />
          </>
        )}
      </div>

      <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>添加文本知识</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">标题</label>
              <Input
                value={formTitle}
                onChange={(e) => setFormTitle(e.target.value)}
                placeholder="输入标题..."
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">分类</label>
              <Select value={formCategory} onValueChange={(value) => setFormCategory(value as KnowledgeCategory)}>
                <SelectTrigger className="mt-1 w-full">
                  <SelectValue placeholder="选择分类" />
                </SelectTrigger>
                <SelectContent>
                  {CATEGORY_OPTIONS.map((opt) => (
                    <SelectItem key={opt.value} value={opt.value}>
                      {opt.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">内容</label>
              <textarea
                value={formContent}
                onChange={(e) => setFormContent(e.target.value)}
                placeholder="输入知识内容..."
                className="mt-1 w-full h-40 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm resize-none bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">标签</label>
              <Input
                value={formTags}
                onChange={(e) => setFormTags(e.target.value)}
                placeholder="用逗号分隔，例如：写作技巧, 特色设定"
                className="mt-1"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowAddDialog(false)}>
              取消
            </Button>
            <Button onClick={handleAddText} disabled={submitting}>
              {submitting ? '添加中...' : '添加'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={showUploadDialog} onOpenChange={setShowUploadDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>上传文件</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">标题</label>
              <Input
                value={formTitle}
                onChange={(e) => setFormTitle(e.target.value)}
                placeholder="输入标题..."
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">分类</label>
              <Select value={formCategory} onValueChange={(value) => setFormCategory(value as KnowledgeCategory)}>
                <SelectTrigger className="mt-1 w-full">
                  <SelectValue placeholder="选择分类" />
                </SelectTrigger>
                <SelectContent>
                  {CATEGORY_OPTIONS.map((opt) => (
                    <SelectItem key={opt.value} value={opt.value}>
                      {opt.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">文件</label>
              <div className="mt-1">
                <FilePicker
                  file={uploadFile}
                  onChange={(file) => setUploadFile(file)}
                  accept=".txt,.md,.markdown,.pdf,.docx"
                  placeholder="点击选择文件"
                  description="支持 TXT / Markdown / PDF / DOCX（自动提取文本）"
                />
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">标签</label>
              <Input
                value={formTags}
                onChange={(e) => setFormTags(e.target.value)}
                placeholder="用逗号分隔，例如：参考书, 小说"
                className="mt-1"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowUploadDialog(false)}>
              取消
            </Button>
            <Button onClick={handleUpload} disabled={submitting || !uploadFile}>
              {submitting ? '上传中...' : '上传'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={showEditDialog} onOpenChange={setShowEditDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>编辑知识</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">标题</label>
              <Input
                value={formTitle}
                onChange={(e) => setFormTitle(e.target.value)}
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">分类</label>
              <Select value={formCategory} onValueChange={(value) => setFormCategory(value as KnowledgeCategory)}>
                <SelectTrigger className="mt-1 w-full">
                  <SelectValue placeholder="选择分类" />
                </SelectTrigger>
                <SelectContent>
                  {CATEGORY_OPTIONS.map((opt) => (
                    <SelectItem key={opt.value} value={opt.value}>
                      {opt.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            {(currentItem?.source_type === 'manual' || currentItem?.source_type === 'imported') && (
              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">内容</label>
                <textarea
                  value={formContent}
                  onChange={(e) => setFormContent(e.target.value)}
                  className="mt-1 w-full h-40 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm resize-none bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            )}
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">标签</label>
              <Input
                value={formTags}
                onChange={(e) => setFormTags(e.target.value)}
                className="mt-1"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowEditDialog(false)}>
              取消
            </Button>
            <Button onClick={handleEdit} disabled={submitting}>
              {submitting ? '保存中...' : '保存'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>确认删除</DialogTitle>
          </DialogHeader>
          <p className="text-sm text-gray-600 dark:text-gray-400 py-4">
            确定要删除「{currentItem?.title}」吗？此操作不可撤销。
          </p>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowDeleteDialog(false)}>
              取消
            </Button>
            <Button variant="destructive" onClick={handleDelete} disabled={submitting}>
              {submitting ? '删除中...' : '删除'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default KnowledgeView;
