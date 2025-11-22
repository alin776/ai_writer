import React, { useState, useEffect, useCallback } from 'react';
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
import { knowledgeApi } from '@/services/knowledgeApi';

/**
 * 知识条目类型
 */
// 知识分类
type KnowledgeCategory = 'character' | 'worldview' | 'plot' | 'dialogue' | 'description' | 'technique' | 'reference' | 'other';

const CATEGORY_OPTIONS: { value: KnowledgeCategory; label: string }[] = [
  { value: 'technique', label: '写作技巧' },
  { value: 'character', label: '人物设定' },
  { value: 'worldview', label: '世界观' },
  { value: 'plot', label: '情节灵感' },
  { value: 'dialogue', label: '对话金句' },
  { value: 'description', label: '场景描写' },
  { value: 'reference', label: '参考资料' },
  { value: 'other', label: '其他' },
];

interface KnowledgeItem {
  id: string;
  title: string;
  content?: string;
  category: KnowledgeCategory;
  source_type: 'text' | 'file' | 'url';
  file_type?: string;
  tags: string[];
  created_at: string;
  updated_at: string;
  chunk_count?: number;
}

/**
 * 个人知识库视图
 *
 * 功能：
 * - 知识条目列表展示
 * - 添加文本/上传文件
 * - 搜索/过滤
 * - 编辑/删除
 * - 标签管理
 */
const KnowledgeView: React.FC = () => {
  const [items, setItems] = useState<KnowledgeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTags] = useState<string[]>([]);

  // 对话框状态
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [showUploadDialog, setShowUploadDialog] = useState(false);
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [currentItem, setCurrentItem] = useState<KnowledgeItem | null>(null);

  // 表单状态
  const [formTitle, setFormTitle] = useState('');
  const [formContent, setFormContent] = useState('');
  const [formTags, setFormTags] = useState('');
  const [formCategory, setFormCategory] = useState<KnowledgeCategory>('technique');
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);

  // 加载知识列表
  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const data = await knowledgeApi.getList({
        search: searchQuery || undefined,
        tags: selectedTags.length > 0 ? selectedTags : undefined,
      });
      setItems(data.items || []);
    } catch (error) {
      console.error('Failed to load knowledge items:', error);
    } finally {
      setLoading(false);
    }
  }, [searchQuery, selectedTags]);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  // 添加文本知识
  const handleAddText = async () => {
    if (!formTitle.trim() || !formContent.trim()) return;

    try {
      setSubmitting(true);
      await knowledgeApi.create({
        title: formTitle.trim(),
        content: formContent.trim(),
        category: formCategory,
        tags: formTags.split(',').map(t => t.trim()).filter(Boolean),
      });
      setShowAddDialog(false);
      resetForm();
      loadItems();
    } catch (error) {
      console.error('Failed to add knowledge:', error);
    } finally {
      setSubmitting(false);
    }
  };

  // 上传文件
  const handleUpload = async () => {
    if (!uploadFile || !formTitle.trim()) return;

    try {
      setSubmitting(true);
      await knowledgeApi.upload(uploadFile, {
        title: formTitle.trim(),
        category: formCategory,
        tags: formTags.split(',').map(t => t.trim()).filter(Boolean),
      });
      setShowUploadDialog(false);
      resetForm();
      loadItems();
    } catch (error) {
      console.error('Failed to upload file:', error);
    } finally {
      setSubmitting(false);
    }
  };

  // 编辑知识
  const handleEdit = async () => {
    if (!currentItem || !formTitle.trim()) return;

    try {
      setSubmitting(true);
      await knowledgeApi.update(currentItem.id, {
        title: formTitle.trim(),
        content: formContent.trim() || undefined,
        category: formCategory,
        tags: formTags.split(',').map(t => t.trim()).filter(Boolean),
      });
      setShowEditDialog(false);
      resetForm();
      loadItems();
    } catch (error) {
      console.error('Failed to update knowledge:', error);
    } finally {
      setSubmitting(false);
    }
  };

  // 删除知识
  const handleDelete = async () => {
    if (!currentItem) return;

    try {
      setSubmitting(true);
      await knowledgeApi.delete(currentItem.id);
      setShowDeleteDialog(false);
      setCurrentItem(null);
      loadItems();
    } catch (error) {
      console.error('Failed to delete knowledge:', error);
    } finally {
      setSubmitting(false);
    }
  };

  // 重置表单
  const resetForm = () => {
    setFormTitle('');
    setFormContent('');
    setFormTags('');
    setFormCategory('technique');
    setUploadFile(null);
    setCurrentItem(null);
  };

  // 打开编辑对话框
  const openEditDialog = (item: KnowledgeItem) => {
    setCurrentItem(item);
    setFormTitle(item.title);
    setFormContent(item.content || '');
    setFormTags(item.tags.join(', '));
    setFormCategory(item.category || 'other');
    setShowEditDialog(true);
  };

  // 打开删除确认
  const openDeleteDialog = (item: KnowledgeItem) => {
    setCurrentItem(item);
    setShowDeleteDialog(true);
  };

  // 获取文件图标
  const getFileIcon = (item: KnowledgeItem) => {
    if (item.source_type === 'text') return <FileText className="w-4 h-4" />;
    if (item.file_type?.includes('pdf')) return <File className="w-4 h-4 text-red-500" />;
    if (item.file_type?.includes('epub')) return <Book className="w-4 h-4 text-purple-500" />;
    return <File className="w-4 h-4" />;
  };

  // 格式化日期
  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* 头部 */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">个人知识库</h1>
            <p className="text-sm text-gray-500 mt-1">
              管理您的参考资料、写作素材和灵感来源
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

        {/* 搜索和过滤 */}
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
          <Button
            variant="ghost"
            size="sm"
            onClick={loadItems}
          >
            <RefreshCw className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* 内容区 */}
      <div className="flex-1 overflow-auto p-6">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : items.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-gray-500">
            <FolderOpen className="w-12 h-12 mb-3 text-gray-300" />
            <p className="text-sm">暂无知识条目</p>
            <p className="text-xs mt-1">点击上方按钮添加您的第一条知识</p>
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {items.map((item) => (
              <div
                key={item.id}
                className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    {getFileIcon(item)}
                    <h3 className="font-medium text-gray-900 text-sm truncate">
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

                {/* 内容预览 */}
                {item.content && (
                  <p className="text-xs text-gray-500 line-clamp-2 mb-3">
                    {item.content}
                  </p>
                )}

                {/* 标签 */}
                {item.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-3">
                    {item.tags.slice(0, 3).map((tag) => (
                      <span
                        key={tag}
                        className="inline-flex items-center px-1.5 py-0.5 rounded text-xs bg-gray-100 text-gray-600"
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

                {/* 元信息 */}
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
        )}
      </div>

      {/* 添加文本对话框 */}
      <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>添加文本知识</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <label className="text-sm font-medium text-gray-700">标题</label>
              <Input
                value={formTitle}
                onChange={(e) => setFormTitle(e.target.value)}
                placeholder="输入标题..."
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">分类</label>
              <select
                value={formCategory}
                onChange={(e) => setFormCategory(e.target.value as KnowledgeCategory)}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {CATEGORY_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">内容</label>
              <textarea
                value={formContent}
                onChange={(e) => setFormContent(e.target.value)}
                placeholder="输入知识内容..."
                className="mt-1 w-full h-40 px-3 py-2 border border-gray-300 rounded-md text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">标签</label>
              <Input
                value={formTags}
                onChange={(e) => setFormTags(e.target.value)}
                placeholder="用逗号分隔，如：写作技巧, 人物塑造"
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

      {/* 上传文件对话框 */}
      <Dialog open={showUploadDialog} onOpenChange={setShowUploadDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>上传文件</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <label className="text-sm font-medium text-gray-700">标题</label>
              <Input
                value={formTitle}
                onChange={(e) => setFormTitle(e.target.value)}
                placeholder="输入标题..."
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">分类</label>
              <select
                value={formCategory}
                onChange={(e) => setFormCategory(e.target.value as KnowledgeCategory)}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {CATEGORY_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">文件</label>
              <div className="mt-1 border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                {uploadFile ? (
                  <div className="flex items-center justify-center gap-2">
                    <File className="w-5 h-5 text-gray-500" />
                    <span className="text-sm text-gray-700">{uploadFile.name}</span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setUploadFile(null)}
                    >
                      <Trash2 className="w-3 h-3" />
                    </Button>
                  </div>
                ) : (
                  <label className="cursor-pointer">
                    <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-500">点击选择文件</p>
                    <p className="text-xs text-gray-400 mt-1">支持 TXT, PDF, EPUB</p>
                    <input
                      type="file"
                      className="hidden"
                      accept=".txt,.pdf,.epub"
                      onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                    />
                  </label>
                )}
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">标签</label>
              <Input
                value={formTags}
                onChange={(e) => setFormTags(e.target.value)}
                placeholder="用逗号分隔，如：参考书籍, 武侠"
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

      {/* 编辑对话框 */}
      <Dialog open={showEditDialog} onOpenChange={setShowEditDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>编辑知识</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <label className="text-sm font-medium text-gray-700">标题</label>
              <Input
                value={formTitle}
                onChange={(e) => setFormTitle(e.target.value)}
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">分类</label>
              <select
                value={formCategory}
                onChange={(e) => setFormCategory(e.target.value as KnowledgeCategory)}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {CATEGORY_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
            {currentItem?.source_type === 'text' && (
              <div>
                <label className="text-sm font-medium text-gray-700">内容</label>
                <textarea
                  value={formContent}
                  onChange={(e) => setFormContent(e.target.value)}
                  className="mt-1 w-full h-40 px-3 py-2 border border-gray-300 rounded-md text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            )}
            <div>
              <label className="text-sm font-medium text-gray-700">标签</label>
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

      {/* 删除确认对话框 */}
      <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>确认删除</DialogTitle>
          </DialogHeader>
          <p className="text-sm text-gray-600 py-4">
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
